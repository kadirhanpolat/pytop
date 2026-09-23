# Architecture Critique — P12.5 Infinite Complexes Design

**Date:** 2026-09-22
**Design reviewed:** `docs/superpowers/specs/2026-09-22-p12-5-infinite-complexes-design.md` (DRAFT)
**Lenses:** 5 independent adversarial agents (mathematical correctness, decidability honesty, codebase integration, scale/performance, YAGNI)
**Total distinct findings:** 41 · **Critical: 15** · High: 10 · Medium: 11 · Low: 1 (refutation)

> **Verdict: the design does not survive review.** The skill's calibration
> threshold is 5 Criticals ("stop — the design needs rework before
> implementation"); this design drew 15. No code was written. The rework
> direction is given by Deliberations 1–2 below, which together delete most of
> the machinery the other findings attack.

---

## What survived

Two claims were independently verified and stand:

- **§5's Rips targets are numerically correct.** ℤ² at ε=1 gives b₁ = 0, 4, 16,
  32, 60 over disks R=1..5 (grid graph, triangle-free — H₁ genuinely of infinite
  rank). ℤ² at ε=√2 gives b₀=1, b₁=b₂=b₃=0 at every stage (acyclic). Note the
  maximal simplices at ε=√2 are **3**-simplices, not the 2-cells the design assumed.
- **Integer coefficient explosion does not occur here.** Instrumented SNF on every
  ∂ₖ and all four transform matrices: `max|entry|` never exceeded 1 — simplicial
  boundary matrices are totally unimodular. Cost is O(m³) Python constants and
  O(m²) transform allocation, not bignum arithmetic.

---

## Critical findings

| ID | Lens(es) | Claim attacked | Failure scenario | Arbitration | Disposition |
|----|----------|----------------|------------------|-------------|-------------|
| C-01 | Honesty, Math | §3.4 `EVENTUALLY_CONSTANT → DECIDED ("K is really finite")` | §4.2 never defines the radius schedule `R_i`. On ℤ² ε=1 the shells sit at 1 and √2≈1.414, so R = 1.0, 1.1, 1.2, 1.3 all return the identical 5-point disk: 4 equal stages, identity inclusions, every induced map trivially iso → engine returns **DECIDED, H₁=0** for the complex whose H₁ has countably infinite rank. Defeats the design's own designated negative control. | Sound and severe. Stage equality proves nothing about the tail. | **Fix** |
| C-02 | Honesty, Math, YAGNI | §4.1 `stable_range(k)=k+1` "declared … and cross-checked against `new_cell_dimensions`" | Both are `InfiniteComplex` methods supplied by the *same* representation and both default to `None`; the engine never inspects `stage_chain_complex`, the data it actually holds. A family declaring `stable_range(k)=k+1` while attaching a (k+1)-cell at stage 50 returns a wrong group labelled DECIDED. Checking a finite prefix cannot establish a hypothesis quantified over all `i > N`. | Sound. A self-signed certificate is not a proof. | **Fix** |
| C-03 | Honesty, Scale | §3.4 `EMPIRICAL_ISO → HEURISTIC` at `patience=3` | Lacunary wedge (circles on the ℤ-ray at distances 2ⁿ): induced maps are genuine isomorphisms for arbitrarily long stretches, then a new generator appears. `patience=3` → "betti=2"; `patience=100` → "betti=7". No fixed patience is sound. Worse, measured: on ℤ² ε=√2, b₁=0 at *every* stage, so the map test is vacuous and EMPIRICAL_ISO fires at stage 4 — §2.2's fallacy in disguise. | Sound. This is the ×2 trap moved up one level, not avoided. | **Fix** |
| C-04 | Architect, Math | §2.2 "pytop already has the machinery (`induced_map_on_homology`) … no excuse for the cheap version" | `simplicial_maps.py:216` takes `SimplicialMap`, whose `__post_init__` validates `domain.vertices`. `cw_real_projective_space(5)` has cells, not vertices — the CW half cannot call it at all. The only chain-level route is private `mayer_vietoris._induced_on_hk`, fed only by `_compute_homology_data(K: SimplicialComplex, k)`. | Sound. The design's central reuse claim is false for half of it. | **Fix** |
| C-05 | Architect, Math | §2.3 "presentations `H_k(K_i) = ℤ^{n_i}/im(P_i)`" | No pytop API returns `P`. `cellular_homology` and `simplicial_homology` both return `HomologyResult(degree, betti, torsion)` — no generator basis, no relations. Only private `_HomologyData` carries them, simplicial-only. This directly contradicts §7's non-goal "any change to existing finite-complex APIs". | Sound. Requires a new public chain-level homology-data API in core, as its own PR. | **Fix** |
| C-06 | Architect | §2.3 "cokernel of the block matrix `[M | P_{i+1}]`" | `exact_linalg.cokernel` computes ℤ^cols / row-lattice — rows are relations. The design's `M` follows `InducedHomologyMap`'s convention (rows = target generators). Source ℤ, target ℤ², `M=[[1],[0]]`: correct answer "not surjective"; `cokernel([[1],[0]])` returns 0 → engine declares **iso and stops**. Every non-square induced map fails in the unsafe direction. The ×2 example misses this because it is 1×1. | Sound, and the unsafe direction makes it worse than a crash. | **Fix** |
| C-07 | Architect, Math | §4.1/§4.2 inclusion chain map `[I; 0]` | `vietoris_rips_filtration` simplices are tuples of **positions in `list(space.carrier)`**. Vertex index 7 is `(1,−1)` at radius 3 and `(0,−2)` at radius 4, so `[I;0]` encodes a non-inclusion and `∂∘ι ≠ ι∘∂`. Separately, `CWComplex` stores only `cell_counts` — cells have no identity, so "stage-i cells are the first basis vectors of stage i+1" is unstatable, and `cw_from_simplicial` reorders cells by simplex sort order. | Sound. The chain-map law must be machine-checked, not assumed. | **Fix** |
| C-08 | Architect | §3.1 new `ChainComplex` type | `CWComplex` already is "boundary matrices by degree" **and** enforces `d∘d=0` in `__post_init__`. `MorseChainComplex` and `FilteredChainComplex` are the same shape again. The new type is the fifth and the only one without the invariant: a family with `d₂∘d₃≠0` sails through and returns confident garbage under a DECIDED certificate. | Sound. Reuse `CWComplex`; do not add a fifth. | **Fix** |
| C-09 | Scale | §3.3 `budget=12` + §4.2 `integer_lattice(n, eps)` | ℤ³ ε=1.5 at stage 12 is 7 153 points → 7 153/64 377/143 060/92 989 simplices. ∂₂ as `list[list[int]]` is 9.21e9 cells = **73.7 GB of pointers**; ∂₃ is **106 GB**. `_smith_normal_form` needs the matrix dense before it can measure density to route to the sparse path. | Sound (measured). Unallocatable on any machine. | **Fix** |
| C-10 | Scale | §4.2 `integer_lattice` advertised for general `n` | ℤ³ ε=1.5 **stage 3** is 123 points; flint `fmpz_mat.snf()` on its 762×1424 ∂₂ ran **>600 s without finishing** across three runs, vs 0.052 s at stage 2. The engine never reaches stage 4, let alone budget=12. | Sound (measured). The advertised example is unrunnable. | **Fix** |
| C-11 | Scale | §3.3 "compute the induced map to stage i+1" | That path is `mayer_vietoris._snf_ext` — pure Python, maintaining P, Pinv, Q, Qinv — which **flint does not accelerate**. Measured 89.8 s at 708 edges vs 0.6 s for the same stage's plain Betti (**150×**). Fitted exponent 4.25 extrapolates to ~54 min per call, two calls per stage, for the trivial ℤ² ε=√2 case whose answer is already correct at stage 1. ℤ³ stage 12 transforms alone ≈ 394 GB. | Sound (measured). The iso test must not go through cycle-basis presentations. | **Fix** |
| C-12 | Scale | §2.3 block-cokernel test | Measured: the block grows to **1 208×2 624 (3.17 M dense entries)** at stage 11→12 for ℤ² ε=√2 degree 1. Each stage pays SNF(∂ₖ) + SNF(∂ₖ₊₁) + extended-SNF(×2) + SNF(block) = **five reductions per stage, twelve stages**. | Sound. A rank check with `compute_transforms=False` replaces a cokernel-with-generators. | **Fix** |
| C-13 | Scale | §3.3 signature; §6 validates only `degree/budget/patience ≥ …` | Nothing caps simplices, memory or wall time. A user runs `infinite_homology(integer_lattice(3,1.5), degree=2)` and walks away: the process sits inside flint's `snf()` with no output, no progress, no interruptibility (the C call ignores signals), climbing toward an allocation it never reaches — and the `trace` §3.4 promises for UNDECIDABLE results is lost because the function never returns. | Sound. Bounds and partial results are mandatory, not polish. | **Fix** |
| C-14 | YAGNI | §3.1 five-module ~1 250 LOC package | §2.4's theorem plus the shipped `cw_real_projective_space` / `cw_complex_projective_space` / `cw_lens_space` means the proven answer to H₃(ℝP^∞) is already `cellular_homology(cw_real_projective_space(5), 3)`. On the flagship family the stage loop, induced maps, iso test and certificates **never execute**. | See Deliberation 1. Correct that the loop never fires — but the dimension hypothesis must still be *verified*, not assumed. | **Fix** |
| C-15 | YAGNI, Scale | §4.2 `LocallyFiniteRips` + §5's two Rips rows | §4.2 concedes "no structural certificate is generally available"; §5's two targets are "must report UNDECIDABLE" and an empirical stabilization. Scale: "the entire Rips family can only ever return HEURISTIC or UNDECIDABLE — hours of integral SNF for a verdict the design itself labels non-proof." | See Deliberation 2. Replace with a claim-free Betti scan. | **Fix** |

---

## High findings

| ID | Lens(es) | Claim attacked | Failure scenario | Disposition |
|----|----------|----------------|------------------|-------------|
| H-01 | Math | §2.4 "for a *skeletal* system, where stage i adds only i-dimensional cells" | `cw_complex_projective_space(n)` has `cell_counts={2k: 1}` — step n→n+1 adds a (2n+2)-cell, so ℂP^∞, a listed §4.1 factory, violates the design's own definition. The real hypothesis is "∀ i ≥ N, every cell added at step i has dim ≥ k+2". | **Fix** |
| H-02 | Honesty, Architect, Math | §5 "independent in-repo oracle: `eilenberg_maclane.py`" | `km_homology_cyclic` is `torsion.append((m,))` for odd k — a literal transcription of the known answer; `km_homology_z(n=2)` hardcodes `betti = 1 if k%2==0`; `km_homology_z2` just calls `km_homology_cyclic(2,·)`, so the table lists one function twice as two oracles. A sign error in `cw_real_projective_space`'s `d_k = 1+(−1)^k` is undetectable. Three lenses caught this independently. | **Fix** |
| H-03 | Honesty, Architect | §3.3 `betti: int | None` as a sibling field of `decidability` | `sum(r.betti or 0 …)` and `if result.betti:` silently convert "undecided" into H_k = 0 — the most dangerous available collision, since 0 is the *correct* answer for ℂP^∞ in odd degrees and S^∞ above degree 0. `torsion` has no `None` state, so UNDECIDABLE reports `torsion=()`, indistinguishable from proven torsion-freeness. `Verdict` in `spaces/core.py` already defines `__bool__` specifically to stop this. | **Fix** |
| H-04 | Honesty | §4.1 silence on `stable_range` contradicting observed data | Four implementations are equally consistent with the document (trust / ignore / raise / take max) and three ship a wrong DECIDED. Also uncovered: `stable_range` declared while `new_cell_dimensions` returns `None` (the §3.2 default) is a bare self-assertion with no cross-check at all. | **Fix** |
| H-05 | Architect | §3.4 "reuse `Decidability` from `experimental.spaces.core`" | The import executes `experimental/__init__.py` (~15 profile modules incl. `pi_base`, `pi_base_atlas`) and `spaces/__init__.py` (`pi1` → `van_kampen`, `pi_base_bridge`, `reasoning`). A user wanting H₁ of a tree pays for the pi-Base bridge and the van Kampen engine at import time, and the module breaks when `spaces` is promoted. | **Fix** |
| H-06 | Scale, Honesty, Architect | §3.3 `budget=12` | Simultaneously too small for CW (`rp_infinity()` at degree 12 needs stage 13 → **UNDECIDABLE for a case §2.4 proves DECIDED**) and 3–5 orders of magnitude too large for Rips. A resource limit is reported as a mathematical limit. | **Fix** |
| H-07 | Architect | §3.3 `StageObservation`, §3.1 `StabilityCertificate`, `is_induced_iso` | None are defined. `StageObservation` appears once and is absent from the `core.py` inventory; `StabilityCertificate` has no fields; `is_induced_iso` — the single algorithmic deliverable of §2.3 — has no signature. §6.2's regression test cannot be written against an undefined return shape. | **Fix** |
| H-08 | Scale | §4.2 `R_i` (appears in exactly one sentence) | Cost differs by orders of magnitude between `R_i = i` and `R_i = 2^i` (stage 12 = radius 4096 ≈ 5.3e7 points in ℤ²). Six of §5's seven targets have no ∂₂ at all, so **CI goes green while the advertised `integer_lattice(3,…)` hangs**. | **Fix** |
| H-09 | Math | §3.2 `[I;0]` chain map | Nothing in the repo checks ∂^{i+1}∘ι = ι∘∂^i; `verify_chain_complex()` checks only d∘d=0. A non-chain-map ι makes every iso verdict noise. | **Fix** |
| H-10 | Honesty | §3.4 "a user can see betti went 1, 4, 9, 16 — it is growing" | §2.3 deliberately discards the injectivity test, so a system with `H₁(K_i)=ℤ^i` whose inclusions kill all previous generators (colimit 0) produces the identical trace. The one interpretation offered for a failed run is an inference the engine has no evidence for. | **Fix** |

---

## Medium findings

| ID | Lens(es) | Finding | Disposition |
|----|----------|---------|-------------|
| M-01 | Honesty | Budget-exhausted-without-refutation should map to `SEMI_DECIDABLE`, not `UNDECIDABLE` | **Reject** (see Deliberation 5) |
| M-02 | Honesty, Architect | `Decidability` is documented for *predicates* ("the value is proven True or False") and paired with `Verdict`; reusing it for an abelian group transfers unearned credibility | **Fix** (doc + mandatory witness payload) |
| M-03 | YAGNI | `CertificateKind` is a second vocabulary layered on `Decidability`; a fifth case forces lockstep edits to two enums and a mapping table | **Fix** (collapse to `decidability` + `reason`) |
| M-04 | YAGNI | `EVENTUALLY_CONSTANT` fires only when the user wrapped a finite complex — a validation error dressed as a tier | **Fix** (subsumed by C-01) |
| M-05 | YAGNI | `StageObservation` is debug logging promoted to frozen public API under the 18-month P19.2 window | **Fix** (`stage_betti: tuple[int,...]`) |
| M-06 | Math | §4.2's exhaustion argument cites the wrong hypothesis; properness, `R_i → ∞`, strict vertex growth and flag-truncation dimension are all unvalidated preconditions (ℚ², ℝ², infinite-star hang or truncate silently) | **Fix** |
| M-07 | Math | "Rips of a ball = induced subcomplex" holds only under the *ambient* metric; a graph factory recomputing distances intrinsically breaks the subcomplex property. `infinite_binary_tree(depth_step)` takes no `eps` at all | **Fix** |
| M-08 | Scale | One Z/2 persistence pass yields the full 12-stage b₁ trace in <10 ms vs ~45 s (flint) / hours (induced-map path) — a 4 500×–10⁶× gap | **Defer** (see Deliberation 4) |
| M-09 | Math, Honesty | No `INFINITE_RANK` certificate or `rank_lower_bound`, so the one §5 answer actually known (ℤ² ε=1) is enshrined as "must report UNDECIDABLE" | **Defer** |
| M-10 | Architect | `InfiniteHomologyResult` invents a fourth abelian-group representation (`HomologyResult`, `AbelianGroup`, `KGnHomology` exist); violates API_DESIGN rule #1 | **Fix** (`group: HomologyResult | None`) |
| M-11 | Architect | Neither `pytop/__init__.py` nor `experimental/__init__.py` export surface is mentioned anywhere (API_DESIGN rule #5) | **Fix** |

## Low

| ID | Lens | Finding | Disposition |
|----|------|---------|-------------|
| L-01 | Scale | Coefficient explosion is **measurably absent** — `max|entry|` stays 1 across all ∂ₖ and all four transforms. Do not spend design effort on modular/CRT SNF; state the bound so future reviewers stop chasing it | **Fix** (document the refutation) |

---

## Phase 3 — Deliberations

### Deliberation 1 — C-14: "the CW half is one existing call"

**Advocate.** §2.4's theorem plus the shipped CW factories means H₃(ℝP^∞) is
already `cellular_homology(cw_real_projective_space(5), 3)`. On the flagship
family the stage loop, the induced maps, the iso test and the certificate
machinery never execute. ~1 250 LOC to reach a line that exists today.

**Devil's advocate.** The theorem's hypothesis must be *verified*, not assumed —
that is finding C-02 exactly. A bare `cellular_homology(family(k+2), k)` assumes
the family is skeletal with no check whatsoever, which is strictly worse than
the design under attack. And H-01 shows the hypothesis is subtler than
"skeletal": ℂP^∞ adds a (2n+2)-cell per step.

**Arbitration.** YAGNI is right about the loop and wrong about the check. The
stage loop, induced-map computation and iso test exist solely to serve the Rips
family; for CW they are dead code. The correct CW path is: verify the dimension
bound from the actual `cell_counts` deltas of the stages — cheap, structural, no
SNF, no induced map — then evaluate at `degree+2`. That keeps the proof obligation
C-02 demands while deleting the machinery C-04/C-05/C-06/C-11/C-12 attack.
**Disposition: Fix.**

### Deliberation 2 — C-15: cut the Rips family

**Advocate.** Both §5 Rips targets are non-answers. Measured cost is hours of
integral SNF for a verdict the design itself labels non-proof, and ℤ³ hangs at
stage 3 of 12.

**Devil's advocate.** The roadmap item says "Convergence algorithms for infinite
Rips / infinite CW complexes". Cutting Rips means not closing P12.5 as written.
And an honest UNDECIDABLE is a feature per Part IV, not a failure.

**Arbitration.** Roadmap wording is a goal, not a contract, and shipping
hours-long computations that can never prove anything is worse than not shipping
them. The honest middle is the one YAGNI proposed and Scale measured:
`rips_betti_scan(metric, eps, radii) -> tuple[int, ...]` returning the per-radius
Betti sequence and making **no stability claim at all** — obtained in <10 ms by a
single persistence pass. That closes the roadmap's intent honestly and cheaply.
**Disposition: Fix** — replace `LocallyFiniteRips` and its engine integration
with a claim-free scan; no certificate tiers for Rips.

### Deliberation 3 — C-04/C-05/C-06: the reuse claims are false

**Advocate.** Three lenses verified against source: `induced_map_on_homology`
refuses CW input; no public API returns presentation matrices; `cokernel` is
transposed relative to the design's matrix convention and fails in the unsafe
direction on non-square maps.

**Devil's advocate.** These are implementation details, fixable while coding.

**Arbitration.** No — they invalidate the LOC estimate and the §7 non-goal. As
written, building this first requires a new *public chain-level homology-data
API in core*, which is a separate PR with its own review. This is the strongest
evidence that Deliberations 1 and 2 are correct: once the stage loop is gone for
CW and the integral stabilization is gone for Rips, this core change shrinks to
nothing. **Disposition: Fix** (and largely dissolved by D1+D2).

### Deliberation 4 — M-08: Z/2 persistence pre-filter

**Advocate.** Measured 4 500×–10⁶× faster; delivers the complete per-stage Betti
trace in under 10 ms.

**Devil's advocate.** Z/2 barcodes carry no integral torsion and cannot decide
the ×2 trap — the trap the design exists to avoid. ℝP^∞'s answer *is* torsion
(ℤ/2), so a Z/2 route is blind to exactly the flagship case.

**Arbitration.** Sound as a locator, unsound as an answer. But if D1 removes the
stage loop for CW and D2 removes integral stabilization for Rips, there is no
expensive loop left to pre-filter — the optimisation's target disappears. Keep it
in reserve for the claim-free scan, where no claim is made anyway.
**Disposition: Defer.**

### Deliberation 5 — M-01: remap budget exhaustion to SEMI_DECIDABLE

**Advocate.** "Stabilization fails at stage ≥ N" is r.e. — a finite search
exhibits a non-iso induced map — so a bounded search that found no refutation is
the textbook semi-decidable situation, and `UNDECIDABLE` under-claims.

**Devil's advocate.** `core.py:30` defines `SEMI_DECIDABLE` as "verified one
direction only (e.g. **found a witness**)". Budget exhaustion found *no* witness.
Relabelling "I ran out of compute" as a sharper epistemic status is precisely the
credibility-borrowing this same lens condemns in M-02. A resource limit is not a
mathematical status.

**Arbitration. Reject.** The underlying concern is real but the remedy is Scale's,
not this one: keep a distinct `BUDGET_EXHAUSTED` outcome separate from a genuine
`NONE`, so a resource limit is never reported as a mathematical limit. That fixes
the confusion without borrowing an epistemic label the search did not earn.
**Disposition: Reject (concern addressed via H-06).**

---

## Consequence for the milestone

Applying D1 + D2 collapses the design from five modules / ~1 250 LOC to roughly
one module: a verified-dimension-bound CW evaluator plus a claim-free Rips Betti
scan. That version is dramatically smaller, has no false DECIDED path, needs no
core API change, and still closes P12.5's stated intent. The register above should
be re-run against the revised design before implementation begins.
