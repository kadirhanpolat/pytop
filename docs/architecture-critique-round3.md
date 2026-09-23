# Architecture Critique — P12.5, Round 3 (revision 3)

**Date:** 2026-09-23
**Design reviewed:** `docs/superpowers/specs/2026-09-22-p12-5-infinite-complexes-design.md` rev. 3
**Prior registers:** `docs/architecture-critique.md` (round 1) · `docs/architecture-critique-round2.md` (round 2)
**Lenses:** 3, narrowed to the changed surface (decidability honesty, mathematical correctness, buildability + cost)
**New findings:** 19 · **Critical: 2** · High: 5 · Medium: 5 · Low: 2 · Sound: 5

> **Trend:** 15 → 5 → 2 Criticals. The design is converging and the remaining
> defects are local. Both Criticals are the *same error class* the author already
> made once in rev 2 — a universally quantified condition over an empty set.

---

## Critical

| ID | Lenses | Claim attacked | Failure scenario | Disposition |
|----|--------|----------------|------------------|-------------|
| R3-C-01 | Honesty, Math | §4 step 2: "smallest `N ≥ degree+1` **within the supplied range** such that every step `i ≥ N` **in range** adds only cells of dimension ≥ `degree+2`" | `N = M` (the last stage index) makes the step set `{i : N ≤ i ≤ M-1}` **empty**, so the condition holds **vacuously for every input**. Both lenses transcribed the spec literally and confirmed: (a) `stages[i] = CWComplex({0: i+1})` — discrete points, (D_0) violated at every step — returns `N=4`, `verified_steps=()`, `group = ℤ⁵`, for a colimit whose `H₀` has infinite rank; (b) `K_i = ⋁_i S¹` — (D_1) violated at every step — returns `betti = 3/5/11/39` for 4/6/12/40 stages, no error. `InsufficientStagesError` becomes unreachable except as an arity check, so §8 test 3 describes an input that cannot exist. **Rev 2's constant-lens-tower bug was the identical error class**; the chain-map check fixed R2-C-02's *nesting* half, but nothing survived to check the hypothesis connecting `K_N` to `K`. | **Fix** |
| R3-C-02 | Honesty | §3.2: "no enum, no flag, no witness payload — none of that machinery exists in Part A because none of it is needed", i.e. Part A has "no caller-supplied object to be uncertain about" | `infinite_lens_homology(p, degree)` — **`p` is caller input** and the spec states no precondition. `_lens_skeleton(0, n)` has all-zero boundaries, so the function returns ℤ in **every** degree 0–6, where BZ/0 = K(ℤ,1) = S¹ has `H_k = 0` for k ≥ 2. `p = 0` is not absurd: the repo's own `cw_lens_space` documents and accepts it. §7's blocking curated row cannot catch it — `km_homology_cyclic(m, ·)` raises for `m < 1`, so the gate is silent exactly where the answer is wrong. The Part A/Part B split was drawn around *towers* and forgot *parameters*. | **Fix** |

---

## High

| ID | Lens | Finding | Disposition |
|----|------|---------|-------------|
| R3-H-01 | Math | **The `N ≥ degree+1` floor is not a hypothesis of the theorem** and rejects valid towers. §2.3's theorem constrains nothing about `N` relative to `k`; `k+1` is a property of §3.1's *specific* towers. Verified: `stages = [{0:1,3:1}, {0:1,3:1,5:1}, {0:1,3:1,5:2}, {0:1,3:1,5:3}]`, degree 3 — every step adds only 5-cells, (D_3) holds at `N=0`, `H_3(K_0) = ℤ` is already correct — but the floor raises `InsufficientStagesError`, and the promised "how many more stages would be needed" is a false statement in exactly this case. | **Fix** (delete the floor; search from `N=0`; keep `degree+1` inside Part A only) |
| R3-H-02 | Math | **`StageInclusion` cannot represent an orientation-reversing subcomplex inclusion.** `images: Mapping[int, tuple[int,...]]` is an unsigned cell-to-cell map, but a cellular inclusion is the identity on cells only when both complexes orient shared cells identically. Verified: `K_0 = ℝP²` as `{1:[[0]], 2:[[2]]}` and `K_1 = ℝP³` with the 2-cell oppositely oriented `{1:[[0]], 2:[[-2]], 3:[[0]]}` is a legal `CWComplex` with `H_1 = ℤ/2`, `H_3 = ℤ` — a genuine ℝP³ containing that ℝP² — yet the only expressible ι fails with `NotATowerError: [[-2]] vs [[2]]`. A correct tower is rejected and the message blames the user's topology for the data model's missing sign. | **Fix** (signed entries) |
| R3-H-03 | Architect | **Part C deleted the only bound on *construction* and replaced it with a bound on *reduction*.** `rips_betti_scan(z2, (0,0), eps=10.0, radii=[5.0], max_degree=3)` is legal with documented defaults: the Euclidean ℤ² disk R=5 has 81 points and diameter 10, so at ε=10 it is a full clique; `vietoris_rips_filtration(..., max_dimension=4)` materialises ~27.4M index tuples before returning, and the `∂_k` shape guard needs `f_vector()`/`simplexes_by_dimension`, which exist only *after* the complex is built — the guard cannot fire and the call OOMs. The rev-3 argument ("SNF cost doesn't track simplex count") is true and **irrelevant to enumeration cost**. R2-C-04 re-opened on the other axis. | **Fix** (keep both bounds) |
| R3-H-04 | Architect | **`betti_z` rows are ragged and §7's `(1,0,0,0)` is wrong at R=1.** `betti_numbers` returns a contiguous tuple of length `dimension + 1`. Measured (arbitration below): R=1 gives `{0:5, 1:8, 2:4}`, dimension 2, `betti = (1,0,0)` — a 3-tuple; R=2,3,4 give 4-tuples. The asserted `(1,0,0,0)` at R=1 is a length mismatch — a red CI test with no bug in the code, the **third** repetition of "unverified expected value in a validation table" (cf. round 2 R2-M-01). | **Fix** (normalise rows to `max_degree+1`; correct §7) |
| R3-H-05 | Honesty, Math, Architect | **`Assumptions` carries zero bits and names the wrong hypothesis.** `tail_dimension_graded` is hardcoded `True` at its sole construction site, so `__bool__` is a constant `False` — a dunder whose documented `True` state is unreachable. Meanwhile `ConditionalHomology` has no `__bool__`, so `bool(result)` is always `True`: the natural guard passes unconditionally and the correct guard never fires. The name also says "dimension_graded", which §2.3 identifies as rev 2's *degree-independent* hypothesis that rev 3 replaced. And the record names one tail assumption of at least four — it omits that stages beyond `M` exist at all, that the tail ι are injective, and that they are chain maps. Round 1's M-02 ("mandatory witness payload") is still unmet: rev 2 shipped a sentence, rev 3 ships a constant. | **Fix** |

---

## Medium

| ID | Lens | Finding | Disposition |
|----|------|---------|-------------|
| R3-M-01 | Math | **Step 1 establishes a chain-complex embedding, not a subcomplex inclusion**, while §2.1/§2.3 are stated about a *space*. Verified: `K_0 = CWComplex({0:1, 4:1})` (= S⁴) and `K_1 = cw_complex_projective_space(2)` with `images = {0:(0,), 2:(), 4:(0,)}` — all boundaries zero, chain-map law holds trivially, step 1 **accepts** — but `{e⁰, e⁴}` is not a subcomplex of ℂP²: `e⁴` is attached by the Hopf map, whose image meets `e²`. There is no space `⋃K_i` here. **The algebra is sound** (the architect lens independently confirmed the chain-level argument is *sufficient* for the isomorphism); what is unearned is the topological *interpretation*. | **Fix** (state what is actually proven) |
| R3-M-02 | Honesty, Architect | **Part C's outcome is prose again and its truncation test cannot fail.** `stopped_reason: str` is the shape round 2 rejected as R2-H-06 — a caller cannot branch on "boundary dim exceeded" vs "point cap exceeded" without parsing English. §8 test 7's `len(betti_z) == len(radii)` is true by the dataclass's own definition, so the "truncation honesty" test is unfalsifiable; the only real signal is `stopped_at_radius is not None` and nothing tests it. | **Fix** (enum; assert the real signal) |
| R3-M-03 | Architect | **The per-radius point cap is a behaviour with no parameter and a contradictory error policy.** §5 says the scan "caps points per radius and raises naming the radius", but the signature has no `max_points`, no field records it, and no value is stated. The two guards also disagree: `max_boundary_dim` stops-and-records (partial results preserved) while the points cap *raises* (completed radii discarded). Rev 3's remaining dangling name. | **Fix** |
| R3-M-04 | Architect | **The ℤⁿ lattice helper is load-bearing but unexported and unspecified.** Confirmed nothing in the repo supplies one (`coarse_geometry`'s `"z_lattice"` is a Descriptive-layer *tag*; `grid_graph` is a test fixture; `closed_ball` comprehends over `space.carrier`). As written, `ProperMetric` ships with **zero** exported implementations and Part C is unusable without the user writing the lattice. No signature, no `n`, no norm selector. | **Fix** (`z_lattice(n, *, norm=…)`, export it) |
| R3-M-05 | Architect | **The two required adapters are unnamed deliverables.** (a) `ProperMetric` exposes `distance`, but `vietoris_rips_filtration` requires `.carrier` + `.distance_between`, so a `FiniteMetricSpace(carrier=tuple(metric.ball(center,R)), distance=metric.distance)` wrapper is mandatory; (b) `simplicial_homology` needs a `SimplicialComplex`, and `SimplicialComplex(fc.simplices)` is sound **only because** `max_scale=eps` keeps the truncated Rips complex face-closed. Note `fc.simplices` are positional indices, not lattice points. | **Fix** (name both; state the face-closure licence) |

---

## Low

| ID | Lens | Finding |
|----|------|---------|
| R3-L-01 | Math | §3.1's lens verification sentence never names the skeleton it was evaluated on. On a *fixed* skeleton the top degree is `ker ∂_n`, so `H_5(_lens_skeleton(5,5)) = ℤ`, not ℤ/5. Harmless for Part A (which evaluates at `degree+1 > degree`) but invites a test that fails at odd `n` for no bug. **Fix:** rewrite as "at the evaluation index". |
| R3-L-02 | Architect | `StageInclusion` is declared `frozen=True` with a `Mapping` field, so `__hash__` is auto-generated over a dict and `hash(...)` raises `TypeError`. (`__eq__`, `repr`, pickling are fine — R2-M-05 is genuinely dissolved.) **Fix:** normalise to a tuple-of-pairs or document the unhashability. |

---

## Arbitration — a direct conflict between two lenses

**Claim:** §7's ε=√2 row, `b = (1,0,0,0)` at R=1..4.

- **Math lens:** verified `(1,0,0,0)` at R=1,2,3,4 with the complex built to dimension `max_degree+1 = 4`.
- **Architect lens:** at R=1 the disk is `{0:5, 1:8, 2:4}` with no 3-simplex, so `dimension == 2` and `betti_numbers` returns a **3-tuple** `(1,0,0)`; the asserted 4-tuple is a length mismatch.

**Measured by the orchestrator** (`py -3.14`, Euclidean disk, ε=√2, built to dimension 4):

| R | points | simplex counts | `K.dimension` | `betti_numbers(K)` |
|---|---|---|---|---|
| 1 | 5 | `{0:5, 1:8, 2:4}` | 2 | `(1, 0, 0)` — length 3 |
| 2 | 13 | `{0:13, 1:32, 2:24, 3:4}` | 3 | `(1, 0, 0, 0)` |
| 3 | 29 | `{0:29, 1:84, 2:72, 3:16}` | 3 | `(1, 0, 0, 0)` |
| 4 | 49 | `{0:49, 1:156, 2:140, 3:32}` | 3 | `(1, 0, 0, 0)` |

**Resolution: the architect lens is correct.** The math lens's simplex counts were
right but its R=1 Betti tuple was not. Rows are genuinely ragged across radii, and
§7's row is wrong as written. Rev 4 normalises `betti_z` rows to exactly
`max_degree + 1` entries and states the R=1 value correctly.

---

## Verified sound (re-checked independently, no finding raised)

- **`_lens_skeleton(p, n)`** — `∂` alternating `[[0]]`/`[[p]]` is the cellular chain
  complex of `S^∞/ℤ_p`; at the evaluation index gives ℤ, ℤ/p, 0, ℤ/p, … for p=2,3,5
  over degrees 0–6. Byte-identity with `cw_real_projective_space(n)` confirmed for
  n=0..7 (counts *and* boundary maps). `cw_lens_space(p).boundary_maps` equals the
  dimension-3 truncation exactly.
- **`_s_infinity_skeleton(n)`** — `[[1,(−1)^k],[(−1)^k,1]]` matches the stated
  attaching formula; `∂_k∂_{k+1} = 0` in both matrix orders; `H_*` = (ℤ,0,…,0,ℤ) for
  n=1..5 and `H₀(S⁰) = ℤ²`. The all-zero-boundary variant gives ℤ² in every degree,
  so §8 test 4 is a **necessary** test vector, not ceremony.
- **The (D_k) ⟹ stability argument at chain level** — for `i ≥ N`, `C_j` and `∂_j` are
  ι-conjugate for `j ≤ k+1`, so `H_k(K_i) → H_k(K_{i+1})` is an isomorphism and equals
  `H_k` of the colimit. The `k+2` threshold (not `k+1`) is correct. No topological
  subcomplex test is needed for the *algebraic* conclusion (cf. R3-M-01 for the
  interpretive caveat).
- **§7's ε=1 row** — independently re-derived from the grid graph (triangle-free, so
  `b₁ = E − V + 1`): V = 5,13,29,49,81 and E = 4,16,44,80,140 give **0, 4, 16, 32, 60** ✓.
  Metric caveat confirmed: ℓ^∞ gives 4,16,36,64,100; ℓ¹ gives 0,4,12,24,40.
- **Part B is buildable from existing primitives** — ι_k is the 0/1 matrix with `1` at
  `(images[k][j], j)`; both sides of the chain-map law need `_mat_mul` and the
  zero-filled `∂_k`, which exist as private symbols (`cellular_homology._mat_mul`,
  `CWComplex._boundary_matrix`). Reuse is ruff- and mypy-legal. All cell-count
  arithmetic must use `.get(k, 0)` because `__post_init__` strips zero-valued keys.
  The 13 export names collide with nothing in `experimental/__init__.py`.

---

## Unmeasured claim carried forward

`max_boundary_dim = 400` was justified in rev 3 as "≈ 2 s on the pure-Python path".
The architect lens had no execution tool this session and **said so rather than
inventing numbers**. The orchestrator measured the flint path instead: Euclidean
ℤ², ε=√2, built to dimension 4 — R=6 is 113 points / 961 simplices with largest
`∂` of 392×368, and `betti_numbers` takes **0.20 s** (R=5: 0.08 s, R=4: 0.02 s).
So 400 is comfortable *with* flint. The non-flint and sparse routes
(`_sparse_snf_inner` via `SPARSE_MIN_DIM=30`/`SPARSE_MAX_DENSITY=0.30`) remain
unmeasured, and the repo has no SNF timing at any size — `docs/PERFORMANCE.md` is a
stub reading `Total Runtime: 0.0000 seconds`. The rev-3 claim also never said
whether 400 bounds `min(rows,cols)`, `max(rows,cols)` or `rows+cols`.

**Disposition: Defer to implementation.** The default is set by measurement during
the build, not by another critique round; rev 4 states which quantity is bounded
and marks the value provisional.

---

## Fixes verified by the orchestrator before entering revision 4

The corrected step-2 search — *smallest `N` in `0 … M-1` (window non-empty by
construction) such that every step `i ∈ [N, M-1]` adds only cells of dimension
≥ `degree+2`; no such `N` ⟹ raise* — was transcribed and run against all six
cases:

| Tower | degree | Result | Expected |
|---|---|---|---|
| discrete points `{0: i+1}` | 0 | **raises** | must raise (R3-C-01a) |
| `⋁_i S¹` `{0:1, 1:i}` | 1 | **raises** | must raise (R3-C-01b) |
| `⋁_i S²` `{0:1, 2:i}` | 0 | `N=0`, steps (0,1,2), ℤ | accepted (R3-H-01) |
| only 5-cells `{0:1,3:1,5:j}` | 3 | `N=0`, steps (0,1,2), ℤ | accepted, floor removed (R3-H-01) |
| ℝP^n tower | 1 | `N=2`, steps (2,3,4), ℤ/2 | `N = degree+1` emerges naturally |
| ℝP^n tower | 3 | `N=4`, steps (4,5,6), ℤ/2 | `N = degree+1` emerges naturally |

Both Criticals' counterexamples now raise; both wrongly-rejected valid towers are
now accepted; and removing the floor does not disturb the standard towers, where
`N` comes out as `degree+1` on its own.
