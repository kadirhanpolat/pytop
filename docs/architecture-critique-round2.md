# Architecture Critique — P12.5, Round 2 (revision 2)

**Date:** 2026-09-22
**Design reviewed:** `docs/superpowers/specs/2026-09-22-p12-5-infinite-complexes-design.md` rev. 2
**Round 1 register:** `docs/architecture-critique.md` (41 findings, 15 Critical)
**Lenses:** 4 (mathematical correctness, decidability honesty, codebase integration + cost, YAGNI)
**New findings:** 27 · **Critical: 5** · High: 11 · Medium: 8 · Sound/Sized: 3

> **Verdict:** revision 2's collapse was the right call — 24 round-1 findings are
> verified as genuinely fixed, including 9 of the 15 Criticals. But the collapse
> carried one defect through under a new name, and introduced four more. A
> revision 3 is required; the fixes are almost entirely *deletions*.

---

## Round 1 findings verified as genuinely fixed

Confirmed independently by at least one lens reading the source, not the document:

| Round-1 ID | Why it is gone |
|---|---|
| C-01, C-03, H-08 | The Rips certificate engine, `EMPIRICAL_ISO`, `patience` and the hidden radius schedule are deleted outright; no `DECIDED` path for Rips exists |
| C-04, C-05, C-06 | No `induced_map_on_homology`, no presentation matrices, no `exact_linalg.cokernel` call site remains — the transposed-convention failure mode has nothing left to fail in |
| C-07 (Rips half) | Positional `list(space.carrier)` indices are harmless now that no index is compared across radii |
| C-08, M-10, M-05 | `CWComplex` is reused (its `d∘d=0` guard therefore applies); `HomologyResult` reused; `StageObservation` gone |
| C-09, C-10, C-13, H-06 | `budget` gone; partial return with `truncated_at` (but see R2-C-04 — the bound is on the wrong quantity) |
| C-11, C-12, H-09 | The stage loop, the induced map and the unchecked `[I;0]` chain map are gone with it |
| C-14, M-03, M-11 | One module; no `CertificateKind`; export surface stated |
| H-01, M-06, M-07, L-01 | "Skeletal" replaced by (DG) with the ℂP^∞ check shown; coefficient-explosion refutation recorded |
| H-02, H-10 | `eilenberg_maclane` demoted from "oracle"; the colimit-0 counterexample kills the growth inference |

**Independently confirmed sound:** the index `n = degree + 1` (§2.3/§3.1). Derived
from the LES of `(K, K_N)`: under the hypothesis, `H_{k+1}(K,K_N) = H_k(K,K_N) = 0`,
so `H_k(K_N) ≅ H_k(K)`. Sharp in both directions — `H₁(ℝP¹) = ℤ ≠ ℤ/2` shows
`degree+0` fails, and no conforming tower makes `degree+1` fail. Revision 1's
`degree+2` was merely over-conservative. Verified in-repo for degrees 0–6 on
ℝP^∞, ℂP^∞ and antipodal S^∞.

---

## Critical findings against revision 2

| ID | Lenses | Claim attacked | Failure scenario | Disposition |
|----|--------|----------------|------------------|-------------|
| R2-C-01 | YAGNI, Honesty, Math | §3.1 `proven_dimension_graded: bool = False  # True only for in-module factories` + §2.4 "a user tower can never reach PROVEN" | The comment is the only enforcement. `CWTower(stage=my_broken_stage, name="rp_infinity", proven_dimension_graded=True)` is a legal construction of a public frozen dataclass and returns `Confidence.PROVEN` on an arbitrary group. Round 1's C-02 is intact — the self-signed certificate merely moved from a method to a field, one keyword argument wide. §5 test 2 is unfalsifiable: it can only exhibit towers it built itself with the default. | **Fix** |
| R2-C-02 | Math, Architect, Honesty | §3.1 step 2 "comparing `cell_counts` … no count may decrease (that would mean the stages are not nested)" | Cell counts cannot certify a subcomplex inclusion — `CWComplex` gives cells no identity and the algorithm never compares `boundary_maps` across stages. Three independent counterexamples, all built from shipped constructors and all passing `d∘d=0`: (a) `stage(i) = cw_moore_space(i+2, 1)` — counts constant at `{0:1,1:1,2:1}`, check passes **vacuously**, stages pairwise non-nested, H₁ runs ℤ/2, ℤ/3, ℤ/4, ℤ/5, ℤ/6, and `degree=1` returns ℤ/4 for an object with no colimit; (b) ℝP² with `d₂=[[2]]` followed by a 4-cell complex with `d₂=[[5]]` — no count decreases, sole increase is dim 3 at step 0, "(DG) verified"; (c) counts increasing in dim ≥ i+1 while an existing cell's attaching map is silently rewritten. This is round 1's C-07 surviving on the CW side. | **Fix** |
| R2-C-03 | all 4 | §3.4 "the first three wrap the shipped `cw_real_projective_space`, `cw_complex_projective_space`, `cw_lens_space`" + §4's `L(p,q)^∞` "computed" row | Verified: `cw_lens_space(p: int)` takes **only `p`** and returns a fixed `cell_counts={0:1,1:1,2:1,3:1}`, dimension 3 — there is no stage index, and the design also invents a `q` the function does not have. The literal implementation `stage = lambda n: cw_lens_space(p)` is a **constant** tower, on which R2-C-02's vacuous check passes, so `infinite_cw_homology(infinite_lens_space(5), 3)` returns ℤ labelled **PROVEN** where H₃ = ℤ/5. A proven-false group, and §4's row cannot catch it because it is uncomputable from the cited factory. Same class as round 1's C-04/C-05: an unverified reuse claim, repeated. | **Fix** |
| R2-C-04 | Architect | §3.2 "`max_simplices` is a hard stop, not advice", justified with the ℤ³ ε=1.5 R=3 measurement | That very case is ~2 309 simplices — **under the 5 000 cap** — and its `∂₂` (762×1424) did not finish a flint SNF in 600 s across three runs. So `rips_betti_scan(lattice3, 1.5, [1,2,3])` returns two radii in milliseconds and then never returns, with `truncated_at` still `None`. Cost is driven by boundary-matrix shape and rank, not simplex count, and the two are not monotonically related (3 689 ℤ² simplices = 19.7 s vs 2 309 ℤ³ simplices = >600 s). Round 1's C-13 is relabelled, not fixed. | **Fix** |
| R2-C-05 | YAGNI | §3.1 `verify_extra_stages: int = 2` vs §5 test 3 "no public function accepts a `patience`-like parameter" | The two sections contradict each other. The knob controls the only load-bearing part of the check — a finite sample of an infinite tail — and changes the outcome: a tower violating the hypothesis at step `n+1` **raises** at the default and returns **CONDITIONAL** at 0. That is patience semantics verbatim. | **Fix** |

---

## High findings

| ID | Lenses | Finding | Disposition |
|----|--------|---------|-------------|
| R2-H-01 | Math, Honesty | **(DG) is sufficient but not necessary**, and rejects ordinary exhaustions. The theorem for degree `k` needs only **(D_k)**: cells added at steps `i ≥ k+1` have dim ≥ `k+2`. Counterexample: `stage(i) = CWComplex({0:1, 2:i})` = ⋁ᵢS², genuinely nested; `degree=0` is provable, yet (DG) fails at step 2 (2 < 3) inside the verify window → `TowerHypothesisError` on a correct computation. §2.4's "verification failure is a bug in the tower" is therefore false. | **Fix** |
| R2-H-02 | Math | §3.1 step 2 verifies from step 0, but the theorem never uses steps `< n`: those cells are already inside `K_n`. Most checks are irrelevant, and `verified_steps` counts them as evidence. | **Fix** |
| R2-H-03 | Math | §3.4 mandates the antipodal S^∞ structure but never states its boundary maps: `∂_k(e^k_±) = e^{k−1}_± + (−1)^k e^{k−1}_∓`, matrix `[[1,(−1)^k],[(−1)^k,1]]`. The obvious wrong implementation (all-zero boundaries) passes `d∘d=0` and yields `H_k = ℤ²` in every degree. Worse, the prescribed guard test `H_*(stage(n)) = (ℤ,0,…,0,ℤ)` is **false at n=0** — S⁰ is two points, `H₀ = ℤ²` — so it fails on the tower's own base stage and will be weakened rather than fixed. | **Fix** |
| R2-H-04 | Honesty | §3.3 `group()` "returns the group regardless of confidence" reintroduces H-03. `proven_group()` returns `None` for *every* user tower, so the unguarded twin is the only path that ever returns data for user input — and it has the shorter name. `_group` also remains reachable and appears in the frozen `repr`. | **Fix** |
| R2-H-05 | Honesty | Two-valued `Confidence` reports **provenance, not evidence**: a tower verified over 200 steps and one over 2 carry the identical label, and `verified_steps` never moves it. There is no outcome for "stage function raised", "`d∘d ≠ 0`", or "(DG) holds but nesting unverified" — those escape as foreign exceptions, so a caller sweeping degrees 0–10 gets a traceback instead of a per-degree status. | **Fix** |
| R2-H-06 | Honesty | Round 1's M-02 disposition was "**Fix** (doc + mandatory witness payload)". Revision 2 kept the doc and dropped the payload: `reason: str` cannot distinguish "(DG) assumed on the tail" from "(DG) assumed **and** nestedness assumed **and** the stage function is non-deterministic". `Verdict` carries structured witnesses plus a truthiness guard; this carries a sentence. | **Fix** |
| R2-H-07 | Architect, Honesty | §3.2 `max_dimension: int = 1` means the reported `betti` is that of the **1-skeleton**, not of the ball's Rips complex — a claim about a *finite* object that the colimit disclaimer does not cover and `truncated_at` (which names only the `max_simplices` stop) cannot express. §4's ε=√2 row needs `max_dimension ≥ 3` and is unreachable at the documented default. | **Fix** |
| R2-H-08 | Architect | `RipsBettiScan.betti: tuple[tuple[int, ...], ...]` matches no repo function. `betti_numbers` needs a `SimplicialComplex` and there is no `FilteredComplex → SimplicialComplex` converter; `persistence_betti_numbers` returns a sparse `dict[int,int]` **over Z/2**. The field is either unbuildable or a densified Z/2 rank labelled "betti". | **Fix** |
| R2-H-09 | Architect, Math | §3.2 has no `center` and no ambient-ball provider exists: `closed_ball(space, center, radius)` materialises `{p for p in space.carrier if …}` — it iterates the whole carrier and does not terminate on ℤ²; `FiniteMetricSpace.carrier` is finite by construction; no lattice factory exists. Three unbudgeted adapters are required. | **Fix** |
| R2-H-10 | Honesty, Architect, YAGNI | §3.3's import-graph justification for a bespoke `Confidence` enum is **self-refuted by §3.5**: the new names are exported from `experimental/__init__.py`, which already imports `pi_base`/`pi_base_atlas` at module level, so that cost is paid by importing this module at all. `spaces/core.py` itself imports only stdlib. The honest argument (CONDITIONAL has no `Decidability` analogue) is already in the same bullet. | **Fix** |
| R2-H-11 | Honesty | §4's four "computed" rows test the engine against itself — `infinite_cw_homology` **is** `cellular_homology(stage(n), degree)`, so comparing "at several indices" compares two points the hypothesis makes trivially equal. What actually catches a bad factory is the curated column. The only independent check is opt-in Sage, so **CI goes green with zero blocking independent validation behind a `PROVEN` label.** Revision 2 over-corrected by demoting `eilenberg_maclane` to a non-blocking note. | **Fix** |

---

## Medium findings

| ID | Lens | Finding | Disposition |
|----|------|---------|-------------|
| R2-M-01 | Math | §4's ℤ² b₁ row (0, 4, 16, 32, 60) is correct **only** for the Euclidean disk. Re-verified: ℓ^∞ balls give 4, 16, 36, 64, 100; ℓ¹ balls give 0, 4, 12, 24, 40. With `space: Any` the ball shape is the metric's, so an ℓ¹ or ℓ^∞ lattice helper turns §4 into a red CI test with no bug in the code. | **Fix** (name the metric) |
| R2-M-02 | Math | §4's "maximal simplices are 3-simplices" is false at R=1, where the ℓ² disk at ε=√2 gives `{0:5, 1:8, 2:4}` — no 3-simplices. And "at every R" is a ∀ claim a finite scan cannot make, in a document whose thesis is that it never infers from observation. | **Fix** |
| R2-M-03 | Math, Architect | "Each ball finite (properness)" is listed as a *validated* precondition but is undecidable on `space: Any` — enumerating a ball of ℚ² or ℝ² does not terminate, so the validation hangs before it can emit its WHY-HOW-THEN message. Round 1's M-06 was marked Fix; revision 2 re-asserts it as done without changing what makes it undecidable. | **Fix** (bounded guard, narrow protocol) |
| R2-M-04 | Architect | `TowerHypothesisError` is raised in §2.4/§3.1 and exported in §3.5 but never defined — round 1's H-07 class, repeated. Repo precedent: `CWComplexError(ValueError)`. | **Fix** |
| R2-M-05 | Architect | `CWTower.stage: Callable` on a frozen `eq=True` dataclass: `rp_infinity() == rp_infinity()` is `False`, `repr` embeds a closure address (non-deterministic doctests — the repo ships doctests), and closures are unpicklable. | **Fix** or dissolved by R2-C-01's fix |
| R2-M-06 | YAGNI | `InfiniteHomologyResult`'s 6 fields include 3 echoes of the caller's own input (`evaluated_at_stage = degree+1`, `verified_steps`, `confidence` = a copy of the tower flag). Four new public types carry P19.2's 18-month deprecation obligation. | **Fix** |
| R2-M-07 | YAGNI | `RipsBettiScan` (5 fields) and `CWTower` (3 fields, one of which R2-C-01 deletes) may not earn their keep over a callable parameter and a `dict[float, tuple[int,...]]`. | **Fix** |
| R2-M-08 | Honesty, YAGNI | §5 test 3 guards a parameter *name*, not a behaviour; the ×2/lacunary fallacy is reconstructible in three lines over `RipsBettiScan.betti`. Replace with a behavioural test: build the ×2 and lacunary towers, assert the label is invariant under `verify_extra_stages ∈ {2, 50}`. | **Fix** |

---

## Sound / correctly sized

- **`n = degree + 1` is correct and sharp** (Math, with in-repo verification at degrees 0–6).
- **The confidence axis was not over-corrected** (YAGNI): `CONDITIONAL` + a reason
  string *is* the "computed but do not trust it" channel; deleting the third and
  fourth tiers, `budget`, `patience` and the certificate type was right and should
  not be reopened. The one genuine over-correction is narrower — §3.1 step 2 turns
  a legitimate slow-indexed tower into an exception (R2-H-01).
- **§3.4's `cw_sphere` warning is correct** (Architect): `cw_sphere(n)` is `{0:1, n:1}`,
  so that tower would indeed not be nested.

---

## Consequence

Three of the five Criticals (R2-C-01, R2-C-02, R2-C-03) share one root cause: the
design tries to certify a *user-supplied tower* through data the type system does
not carry. Cell counts cannot express nesting, a boolean cannot express a proof,
and a factory that has no stage index cannot be wrapped into one.

The convergent recommendation across all four lenses is to stop treating
"provenness" as tower state:

- the four standard spaces become **concrete functions** with their own in-module
  proofs and tests, returning a plain `HomologyResult` like any other library
  function — no confidence field, because nothing is being asserted about caller
  input;
- the generic path requires **machine-checkable inclusion data** (a cell-index
  injection per step, checked against `∂^{i+1}∘ι = ι∘∂^i`) and verifies the
  degree-relative **(D_k)** only on steps `≥ degree+1`, always returning a
  conditional result with a structured assumption record;
- the Rips scan is bounded by **boundary-matrix dimension**, states its coefficient
  field and its truncation degree, and takes an explicit `center` plus a narrow
  ball protocol.
