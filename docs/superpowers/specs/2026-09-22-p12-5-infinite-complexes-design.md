# P12.5 — Countably Infinite Complexes

**Status:** DRAFT — revision 4 (post round-3 critique)
**Date:** 2026-09-23
**Milestone:** Phase 12, P12.5
**Target version:** v1.8.0
**Layer:** `src/pytop/experimental/` (API Design Rule #3)
**Critique registers:** `docs/architecture-critique.md` (round 1: 41 findings / 15 Critical) ·
`docs/architecture-critique-round2.md` (round 2: 27 / 5) ·
`docs/architecture-critique-round3.md` (round 3: 19 / 2)

> **Revision history.** Rev 1: five-module package with a stage loop, induced maps
> and a three-tier certificate engine — 15 Critical. Rev 2: collapsed to one
> module per arbitration D1/D2 — 5 Critical. Rev 3: "provenness" removed from
> caller-supplied state via a Part A / Part B split — 2 Critical. Rev 4 (this)
> closes both, and both were the **same error class**: a ∀ over an empty set.

---

## 1. Problem

pytop computes homology of *finite* complexes. ℝP^∞, ℂP^∞, BZ/p, the Rips complex
of the ℤ² lattice — none can be handed to `cellular_homology` at all.

---

## 2. Mathematical foundation

### 2.1 Direct limit

`K = ⋃_i K_i` with `K_0 ⊆ K_1 ⊆ ⋯` finite. Chains are compactly supported, so
`H_k(K) ≅ colim_i H_k(K_i)`.

### 2.2 The trap that constrains the design

`ℤ --×2--> ℤ --×2--> ⋯` has every group ℤ and every Betti number 1, colimit
ℤ[1/2]. Stopping because the Betti numbers stopped changing is unsound; so is
stopping because induced maps were isomorphisms for some number of consecutive
stages. **This design never infers stabilization from observation.**

### 2.3 The structural theorem

Attaching a cell of dimension `d` affects only `H_{d-1}` and `H_d`.

> **Theorem.** If every cell added after stage `N` has dimension ≥ `k+2`, then
> `H_k(K_N) ≅ H_k(K)`.

Threshold `k+2`, not `k+1`: a `(k+1)`-cell can kill a class in `H_k`.

> **(D_k) at N.** For every `i ≥ N`, every cell added at step `i → i+1` has
> dimension ≥ `k+2`.

**Verified at chain level** (round 3): for `i ≥ N` the added generators sit in
degrees ≥ `k+2`, so `C_j` and `∂_j` are ι-conjugate for `j ≤ k+1`, hence
`H_k(K_i) → H_k(K_{i+1})` is an isomorphism and equals `H_k` of the colimit.

**`N` is not constrained relative to `k`.** Rev 3 imposed a floor `N ≥ degree+1`;
that is a property of §3's *specific* towers, not a hypothesis of the theorem, and
it rejected valid input — a tower adding only 5-cells has (D_3) at `N=0` with
`H_3(K_0) = ℤ` already correct, yet the floor raised (round 3, R3-H-01). Part B
searches from `N = 0`. `degree+1` survives only inside Part A, where it is a fact
about those four towers.

### 2.4 What can and cannot be certified

(D_k) quantifies over all `i ≥ N`; verification over supplied stages establishes a
finite window, never the tail. The line is drawn by **kind of API**:

- **Part A** — four functions whose towers are built in this module and whose
  (D_k) argument is closed-form, stated in the docstring and tested. They return a
  plain `HomologyResult`.
- **Part B** — user-supplied stages *and* inclusions; verifies the chain-map law
  and (D_k) on a **non-empty** window; always returns a conditional result with a
  structured record of what was assumed.

**Part A's freedom from witnesses is a claim about *towers*, not about
*parameters*.** Rev 3 wrote "no caller-supplied object to be uncertain about" and
overlooked that `infinite_lens_homology(p, …)` takes `p`: `_lens_skeleton(0, n)`
has all-zero boundaries and returns ℤ in every degree, where `BZ/0 = K(ℤ,1) = S¹`
has `H_k = 0` for `k ≥ 2` — and §7's curated gate is silent there because
`km_homology_cyclic` raises for `m < 1` (round 3, R3-C-02). **Every Part A
parameter carries its own precondition.**

### 2.5 A refuted concern (recorded so it is not re-litigated)

Integer coefficient explosion does **not** occur: instrumented over `∂ₖ` and all
four SNF transforms for ℤ² (ε=√2, R=3–6) and ℤ³ (ε=1.5, R=2), `max|entry|` never
exceeded 1 — simplicial boundary matrices are totally unimodular. No modular/CRT
SNF work is warranted.

---

## 3. Part A — standard spaces

```python
def rp_infinity_homology(degree: int) -> HomologyResult
def cp_infinity_homology(degree: int) -> HomologyResult
def s_infinity_homology(degree: int) -> HomologyResult
def infinite_lens_homology(p: int, degree: int) -> HomologyResult   # requires p >= 1
```

Each is `cellular_homology(<skeleton>(degree+1), degree)`. Preconditions
(`degree ≥ 0`, `p ≥ 1`) use P19.1 WHY-HOW-THEN messages.

### 3.1 Skeleton builders

Two are shipped and satisfy (D_k): `cw_real_projective_space(n)` (step `n→n+1`
adds an `(n+1)`-cell) and `cw_complex_projective_space(n)` (adds a `(2n+2)`-cell).

Two are written here. **`cw_lens_space` cannot be wrapped** — it takes only `p`
and returns a fixed 3-dimensional complex, so the literal wrapper is a constant
tower returning a proven-false group (round 2, R2-C-03).

**`_lens_skeleton(p, n)`**, `p ≥ 1`:

```
cell_counts   = {k: 1 for k in 0..n}
boundary_maps = {k: [[p]] if k % 2 == 0 else [[0]]  for k in 1..n}
```

Verified (twice, independently): **at the evaluation index**,
`cellular_homology(_lens_skeleton(p, k+1), k)` = ℤ (k=0), ℤ/p (k odd), 0 (k even>0)
for p=2,3,5 over degrees 0–6. The phrase "at the evaluation index" is load-bearing:
on a *fixed* skeleton the top degree is `ker ∂_n`, so `H_5(_lens_skeleton(5,5)) = ℤ`,
not ℤ/5 (round 3, R3-L-01). Also verified: `_lens_skeleton(2,n)` is **byte-identical**
to `cw_real_projective_space(n)` for n=0..7, and `cw_lens_space(p).boundary_maps`
equals the dimension-3 truncation exactly.

**`_s_infinity_skeleton(n)`** — the antipodal structure. **`cw_sphere` must not be
used**: it is `{0:1, n:1}`, under which `S^n ⊄ S^{n+1}`.

```
cell_counts   = {k: 2 for k in 0..n}
boundary_maps = {k: [[1, (-1)**k], [(-1)**k, 1]]  for k in 1..n}
```

Verified: `H_*` = (ℤ,0,…,0,ℤ) for n=1..5; `H₀ = ℤ²` at **n=0** (S⁰ is two points);
at the evaluation index ℤ (k=0), 0 (k>0). The all-zero-boundary variant passes
`d∘d=0` and yields ℤ² in every degree, so these matrices are a **required test
vector**.

### 3.2 Why these carry no confidence field

They are ordinary library functions: construction in the module, theorem in the
docstring, tests in CI — exactly like `cellular_homology(cw_torus(), 1)`. The
uncertainty machinery of Part B exists for caller-supplied towers, and Part A
takes none. Parameters are guarded instead (§2.4).

---

## 4. Part B — user-supplied towers

```python
@dataclass(frozen=True)
class StageInclusion:
    """Signed cell map C_*(K_i) ↪ C_*(K_{i+1}), per degree.

    images[k][j] = (target_index, sign) for the j-th k-cell of K_i, sign in {+1, -1}.
    Stored as tuples, not a Mapping, so the frozen dataclass is genuinely hashable.
    """
    images: tuple[tuple[int, tuple[tuple[int, int], ...]], ...]
```

The sign is required, not decorative: a cellular inclusion is the identity on
cells only when both complexes orient the shared cells identically. `ℝP² ⊂ ℝP³`
with the 2-cell oppositely oriented (`∂₂ = [[-2]]` vs `[[2]]`) is a legal
`CWComplex` and a genuine subcomplex inclusion, but an unsigned ι fails the
chain-map law and the tower is rejected with a message blaming the user's
topology for the data model's missing sign (round 3, R3-H-02).

```python
class TailAssumption(Enum):
    STAGES_EXIST      = "stages_exist"          # stages beyond the last supplied one
    INCLUSIONS_VALID  = "inclusions_valid"      # tail ι injective and chain maps
    CELL_DIMENSIONS   = "cell_dimensions"       # tail steps add only cells of dim >= min_dim


@dataclass(frozen=True)
class Assumptions:
    assumed: frozenset[TailAssumption]
    min_tail_cell_dimension: int      # = degree + 2
    evaluated_stage: int
    verified_steps: tuple[int, ...]   # non-empty by construction


@dataclass(frozen=True)
class ConditionalHomology:
    group: HomologyResult
    assumptions: Assumptions

    def __bool__(self) -> bool:
        """False whenever anything was assumed — which, for Part B, is always."""
        return not self.assumptions.assumed


def colimit_homology(
    stages: Sequence[CWComplex],
    inclusions: Sequence[StageInclusion],   # len(stages) - 1 entries
    degree: int,
) -> ConditionalHomology
```

Rev 3 put `__bool__` on `Assumptions` with the sense inverted, so
`bool(result.assumptions)` was a constant `False` while `bool(result)` — the guard
a caller actually writes — was a constant `True` from the dataclass default. Rev 4
puts the guard on the object callers hold and names three assumptions instead of
one (round 3, R3-H-05).

**Algorithm.**

1. **Chain-map verification.** Each `inclusions[i]` must be injective per degree
   and satisfy `∂^{i+1}_k ∘ ι_k = ι_{k-1} ∘ ∂^i_k` for every `k`, with ι_k the
   signed matrix built from `images`. Otherwise raise `NotATowerError` naming the
   step, degree and the two matrices. Comparing `cell_counts` verifies nothing —
   `stage(i) = cw_moore_space(i+2, 1)` has constant counts `{0:1,1:1,2:1}`, is
   pairwise non-nested, and `H₁` runs ℤ/2, ℤ/3, ℤ/4, ℤ/5, ℤ/6 (round 2, R2-C-02).
   The check does bite here: `∂^{i+1}_2∘ι_2 = [[i+3]] ≠ [[i+2]] = ι_1∘∂^i_2`.
2. **Window search.** With `M = len(stages) - 1` steps indexed `0 … M-1`, find the
   smallest `N ∈ {0, …, M-1}` such that every step `i ∈ [N, M-1]` adds only cells
   of dimension ≥ `degree + 2` — read off as the target cells outside the image of
   ι. **The upper bound `M-1` is what makes the window non-empty.** If no such `N`
   exists, raise `InsufficientStagesError` reporting the last violating step and
   dimension.
   *Rev 3 allowed `N = M`, making the step set empty and the condition vacuously
   true for every input*: discrete points `{0: i+1}` returned ℤ⁵ and `⋁_i S¹`
   returned `betti = 3/5/11/39`, both for colimits of infinite rank, and
   `InsufficientStagesError` was unreachable (round 3, R3-C-01). This was the same
   empty-∀ error as rev 2's constant lens tower.
3. Return `cellular_homology(stages[N], degree)` with
   `Assumptions(assumed=frozenset(TailAssumption), min_tail_cell_dimension=degree+2,
   evaluated_stage=N, verified_steps=tuple(range(N, M)))`.

The corrected search was transcribed and run before entering this revision:

| Tower | degree | Result |
|---|---|---|
| discrete points `{0:i+1}` | 0 | **raises** ✓ |
| `⋁_i S¹` `{0:1,1:i}` | 1 | **raises** ✓ |
| `⋁_i S²` `{0:1,2:i}` | 0 | `N=0`, steps (0,1,2), ℤ ✓ |
| only 5-cells `{0:1,3:1,5:j}` | 3 | `N=0`, steps (0,1,2), ℤ ✓ (floor removed) |
| ℝP^n tower | 1 | `N=2`, steps (2,3,4), ℤ/2 ✓ |
| ℝP^n tower | 3 | `N=4`, steps (4,5,6), ℤ/2 ✓ |

`N = degree+1` emerges on its own for the standard towers, which is why deleting
the floor costs nothing.

**What this function actually proves.** `H_degree` of the colimit of the
**supplied chain complexes along the supplied chain maps**, conditional on the
tail assumptions. It equals `H_degree(⋃ K_i)` only if the caller's ι really come
from subcomplex inclusions — which it **cannot check**: cellular chain complexes
retain only the degrees of attaching maps, so `K_0 = CWComplex({0:1, 4:1})` (=S⁴)
mapping into `cw_complex_projective_space(2)` passes step 1 trivially (all
boundaries zero) even though `{e⁰, e⁴}` is not a subcomplex of ℂP² — `e⁴` is
attached by the Hopf map (round 3, R3-M-01). The algebra is sound; the topological
reading is the caller's responsibility, and the docstring says so.

**Errors.** `NotATowerError(ValueError)`, `InsufficientStagesError(ValueError)`,
on the `CWComplexError(ValueError)` precedent. `InsufficientStagesError` reports
the window search's negative result — **not** a prediction of how many more stages
are needed, which is exactly the tail §2.2 forbids inferring.

---

## 5. Part C — Rips Betti scan (claim-free)

```python
class ProperMetric(Protocol):
    def ball(self, center: Any, radius: float) -> Sequence[Any]: ...
    def distance(self, x: Any, y: Any) -> float: ...


class ScanStop(Enum):
    POINT_CAP    = "point_cap"      # ball too large, before any pairwise work
    DENSITY_CAP  = "density_cap"    # ball too dense, before construction
    BOUNDARY_CAP = "boundary_cap"   # matrix too large, after construction


def rips_betti_scan(
    metric: ProperMetric,
    center: Any,
    eps: float,
    radii: Sequence[float],
    max_degree: int,                      # required — no default
    *,
    max_points: int = 200,                # measured, see §5.1
    max_simplices: int = 20_000,          # measured, flag-complex size bound
    max_boundary_dim: int = 400,          # measured, bounds max(rows, cols)
) -> RipsBettiScan


@dataclass(frozen=True)
class RipsBettiScan:
    eps: float
    max_degree: int
    radii: tuple[float, ...]              # only the radii actually completed
    betti_z: tuple[tuple[int, ...], ...]  # integral; each row exactly max_degree+1 entries
    stopped_at_radius: float | None
    stopped_reason: ScanStop | None
```

**It makes no claim about the infinite complex.** A growing sequence does not
imply a large colimit (a system with `H₁(K_i) = ℤ^i` whose inclusions kill every
earlier generator has colimit 0), and this function tests no induced map. First
line of the docstring.

**Rows are normalised** to exactly `max_degree + 1` entries — zero-padded below,
top degree truncated. `betti_numbers` returns a tuple of length
`complex.dimension + 1`, which varies with the radius: measured, the ε=√2
Euclidean disk gives `dimension = 2` at R=1 and `dimension = 3` at R=2..4, so raw
rows are ragged (round 3, R3-H-04).

**Faithful truncation.** The Rips complex is built to dimension `max_degree + 1`,
because `H_k` is faithful only when simplices up to dimension `k+1` are present —
the rule the P16.2 `betti_parity` work uses. `max_degree` is required so no caller
inherits a wrong default.

**Coefficients are named in the field.** `betti_z` is integral, via
`simplicial_homology`.

**Three bounds, all stop-and-record.** `max_points` rejects an oversized ball
before any pairwise work; `max_simplices` rejects a *dense* ball using a
flag-complex size bound (`Σ_v C(deg v, i)` over the 1-skeleton) computed before
construction; `max_boundary_dim` caps `max(rows, cols)` of any `∂_k` after it.
All three set `stopped_at_radius`/`stopped_reason` and return the completed
radii — none raises, so partial results survive.

A point cap alone is the wrong instrument: the Euclidean disk of radius 5 has 81
points — under any sane cap — but diameter 10, so at `eps = 10` it is a single
clique whose truncated Rips complex has ~2.7·10⁷ simplices. Density, not point
count, predicts the blow-up.

Rev 3 had only `max_boundary_dim`, arguing SNF cost does not track simplex count.
True, and irrelevant to **enumeration** cost: `rips_betti_scan(z2, (0,0), eps=10.0,
radii=[5.0], max_degree=3)` is legal with rev-3 defaults, and the R=5 Euclidean
disk (81 points, diameter 10) is a full clique at ε=10 — `vietoris_rips_filtration`
materialises ~27.4M index tuples before returning, and the `∂_k` guard needs
`f_vector()`, which exists only *after* the complex is built, so the guard could
never fire (round 3, R3-H-03).

### 5.1 On the three defaults

**Measured, not argued.** Euclidean ℤ² disk, ε=√2, built to dimension 4, this
machine with python-flint:

| R | points | simplices | largest `∂` | scan time |
|---|---|---|---|---|
| 3 | 29 | 201 | 84 | 0.02 s |
| 4 | 49 | 377 | 156 | 0.07 s |
| 5 | 81 | 665 | 272 | 0.27 s |
| 6 | 113 | 961 | 392 | 0.66 s |
| 7 | 149 | 1 297 | 528 | 1.78 s |
| 8 | 197 | 1 745 | 708 | 6.38 s |

`max_boundary_dim = 400` therefore gates a first call at ≈0.7 s on this family,
and `max_simplices = 20 000` admits every row of §7 (the ε=√2 bound at R=6 is
≈18 400) while rejecting the ε=10 clique by six orders of magnitude. The
non-flint and sparse routes (`_sparse_snf_inner`, `SPARSE_MIN_DIM=30`,
`SPARSE_MAX_DENSITY=0.30`) remain unmeasured; the repo has no SNF timing at any
size, since `docs/PERFORMANCE.md` is a stub reading `Total Runtime: 0.0000
seconds`. Users on the pure-Python path should expect the `docs/COMPLEXITY.md`
5–8× factor and lower the caps accordingly.

### 5.2 Required adapters (explicit deliverables)

- `ProperMetric` → `vietoris_rips_filtration`: the latter needs `.carrier` +
  `.distance_between`, so `FiniteMetricSpace(carrier=tuple(metric.ball(center, R)),
  distance=metric.distance)` per radius.
- `FilteredComplex` → `SimplicialComplex`: `SimplicialComplex(fc.simplices)`,
  sound **only because** `max_scale=eps` keeps the truncated Rips complex
  face-closed (a face's diameter never exceeds its coface's), so
  `require_face_closed=True` passes. Note `fc.simplices` carry positional indices
  into the ball, not points.

### 5.3 Lattice helper

```python
def z_lattice(n: int, *, norm: Literal["l2", "l1", "linf"] = "l2") -> ProperMetric
```

Nothing in the repo supplies one: `coarse_geometry`'s `"z_lattice"` is a
Descriptive-layer tag, `grid_graph` is a test fixture, and `closed_ball`
comprehends over `space.carrier` and so cannot serve an infinite lattice. Without
this helper `ProperMetric` would ship with zero implementations and Part C would
be unusable (round 3, R3-M-04). The norm is explicit because the validation
numbers depend on it (§7).

**Preconditions:** `radii` strictly increasing; `eps > 0`; `max_degree ≥ 0`;
`n ≥ 1`. Properness is the provider's contract (`ball` returns a `Sequence`), not
an undecidable runtime assertion — enumerating a ball of ℚ² would not terminate,
so rev 2's "validated properness" would have hung before it could report
(round 2, R2-M-03).

---

## 6. Deliverables and exports

One module, `src/pytop/experimental/infinite_complexes.py`.

Exported from `pytop/experimental/__init__.py` (16 names): `rp_infinity_homology`,
`cp_infinity_homology`, `s_infinity_homology`, `infinite_lens_homology`,
`colimit_homology`, `StageInclusion`, `TailAssumption`, `Assumptions`,
`ConditionalHomology`, `rips_betti_scan`, `ProperMetric`, `ScanStop`,
`RipsBettiScan`, `z_lattice`, `NotATowerError`, `InsufficientStagesError`.
Nothing is added to `pytop/__init__.py` (Rule #3). Verified: no collisions with
existing exports.

Internal reuse (private, ruff- and mypy-legal): `cellular_homology._mat_mul` and
`CWComplex._boundary_matrix` for the chain-map law. All cell-count arithmetic uses
`.get(k, 0)` because `CWComplex.__post_init__` strips zero-valued keys.

No `Confidence` enum. Rev 2 justified one on import-graph grounds that its own
export section refuted (round 2, R2-H-10); with Part A returning plain
`HomologyResult` and Part B returning structured `Assumptions`, no third
vocabulary is needed.

---

## 7. Validation

| Object | Expected | Check |
|---|---|---|
| ℝP^∞ | ℤ, ℤ/2, 0, ℤ/2, … | computed; **blocking** literal expected values in the test file |
| ℂP^∞ | ℤ in even degrees | computed; **blocking** literals |
| BZ/p (p≥1) | ℤ, ℤ/p, 0, ℤ/p, … | computed; **blocking** literals; plus `infinite_lens_homology(2,k) == rp_infinity_homology(k)`, true *by construction* |
| BZ/p truncation | — | `_lens_skeleton(p,3)` equals `cw_lens_space(p)` cell-for-cell (verified, p=5) |
| S^∞ | ℤ, 0, 0, … | computed; boundary matrices as explicit test vectors incl. `H₀(S⁰) = ℤ²` |
| all four | — | **non-blocking** consistency note against `eilenberg_maclane` |
| ℝP^∞, ℂP^∞ | — | external differential test via the Docker SageMath pattern (`PYTOP_SAGE_ORACLE=1`), opt-in |
| ℤ², **Euclidean** disk, ε=1 | b₁ = 0, 4, 16, 32, 60 at R=1..5 | scan output only; **no colimit claim** |
| ℤ², Euclidean disk, ε=√2, `max_degree=3` | `(1,0,0,0)` at R=2,3,4; **`(1,0,0)` raw at R=1**, normalised to `(1,0,0,0)` | scan output only |

**On `eilenberg_maclane`.** Rev 1 wrongly called it an oracle; rev 2 demoted it to
a non-blocking note, leaving CI with zero always-on validation; rev 3 made it
blocking. Rev 4 splits the difference, because a *blocking* gate on a hardcoded
table converts independence into coupling — a maintainer facing red CI can fix
either side, and a legitimate future correction to the Descriptive-layer module
would red this one for an unrelated reason (round 3). So: **expected values are
inlined as literals in the test file and blocking**; the `eilenberg_maclane`
comparison stays as a separate **non-blocking** consistency test. Note
`HomologyResult.torsion` is `(2,)` while `KGnHomology.torsion[k]` is per-degree —
that comparison needs an explicit adapter or it fails on shape, not mathematics.

**On the lattice rows.** The metric is named: 0, 4, 16, 32, 60 is correct for the
Euclidean disk *only*, and ℓ¹ balls give 0, 4, 12, 24, 40. Round 2's R2-M-01 also
claimed ℓ^∞ gives 4, 16, 36, 64, 100; **that is wrong and was measured to be
0 throughout** — under the sup norm a unit square is a 4-clique, so the flag
complex fills it and no 1-cycle survives. 4, 16, 36, 64, 100 is the cycle rank of
the ℓ^∞ *1-skeleton*, which is not what a Rips complex at `max_degree ≥ 1`
reports. The correction strengthens the case for an explicit `norm`: the norm
changes the answer qualitatively, not just numerically. "At the
tested radii", never "at every R".

---

## 8. Testing plan

TDD. `tests/experimental/test_infinite_complexes.py`.

1. **Vacuity regression** — the discrete-points tower `{0: i+1}` at degree 0 and
   `⋁_i S¹` at degree 1 must raise `InsufficientStagesError`, never return a group.
   (Round 3, R3-C-01.)
2. **No spurious floor** — `⋁_i S²` at degree 0 and the only-5-cells tower at
   degree 3 return `N=0` without raising. (R3-H-01.)
3. **Non-tower rejection** — `cw_moore_space(k+2, 1)` stages with identity-shaped
   inclusions raise `NotATowerError`. (R2-C-02.)
4. **Signed inclusion** — `ℝP² ⊂ ℝP³` with the 2-cell oppositely oriented is
   **accepted** with signs and rejected without. (R3-H-02.)
5. **Interpretation caveat** — the `S⁴ → ℂP²` chain embedding is accepted, and a
   test asserts the docstring's scope claim is what the result records. (R3-M-01.)
6. **Part A parameter guards** — `infinite_lens_homology(0, k)` and negative `p`
   raise; `degree < 0` raises. (R3-C-02.)
7. **`_s_infinity_skeleton` test vectors** — `∂_{k-1}∂_k = 0`; `∂_2 = [[1,1],[1,1]]`
   with `H₁(S²) = 0`; `H₀(S⁰) = ℤ²`; **the all-zero-boundary variant is asserted to
   give the wrong answer**, so the test fails if it is simplified away.
8. **`_lens_skeleton` cross-checks** — byte-identity with `cw_real_projective_space`
   at p=2; dimension-3 truncation equals `cw_lens_space(p)`.
9. **Blocking literals** for all four Part A functions over degrees 0–8.
10. **Row normalisation** — the ε=√2 scan at R=1 (raw `(1,0,0)`) and R=2 (raw
    `(1,0,0,0)`) both return rows of length `max_degree+1`. (R3-H-04.)
11. **Both scan bounds fire** — a configuration tripping `max_points` and one
    tripping `max_boundary_dim` each return promptly with `stopped_reason` set to
    the right `ScanStop` member and `len(radii) < len(requested)`. (R3-H-03,
    R3-M-02.)
12. **Cost ceiling in CI** — the ℤ³ ε=1.5 configuration that ran >600 s unbounded
    returns in seconds.
13. ≥80% coverage; ruff-clean; mypy-clean.

---

## 9. Non-goals

- Certified integral homology of infinite Rips complexes (no structural theorem;
  the observational route costs hours for a non-proof). Part C replaces it.
- Persistent homology / barcodes of infinite complexes.
- Injectivity testing and rank lower bounds (round 1, M-09) — deferred; until then
  no rank claim is made.
- A Z/2 persistence fast path (round 1, M-08) — deferred.
- Field/relative coefficients; cohomology of infinite complexes (`lim¹`).
- Any change to existing finite-complex APIs.
