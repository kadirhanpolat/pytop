# pytop — Formal SNF Verification

Lean 4 (v4.31.0) + Mathlib formal verification of the Smith Normal Form algorithm
used in [`pytop.exact_linalg`](https://github.com/kadirhanpolat/pytop).

## Goal

Prove that `pytopSNF` (a fuel-bounded implementation of integer SNF via elementary
row/column operations) is correct: it terminates, produces positive invariant factors,
and the factors form a divisibility chain.

## Status: **Complete — but read the build caveat**

All theorems proved: **24** `.lean` files outside `.lake`, **219** theorems/lemmas,
**0 `sorry` tactics**.

> ### ⚠️ "0 sorry" is grep-verified, not kernel-verified, for Phase 11
>
> The zero-sorry claim is a text search over the sources. For the SNF and
> point-set modules it is backed by a real build. For the five Phase 11 files it
> is **not**:
>
> - `Formal.lean` imports `MayerVietoris`, `VanKampen`, `CohomologyRing`,
>   `PersistencePairing` and `SpectralSequences`. **None of the five has an
>   `.olean` in `formal/.lake/build`** — they have never been compiled in this
>   tree. `SetTopology` and 8 of the 9 `SNF/*` files have one (`SNF/TestLemmas.lean` is imported by nothing, so none is expected).
> - `SetTopologyAltProofs.lean` is **not imported by `Formal.lean` at all**, so
>   `lake build` never reaches it either.
> - There is **no `lake` job in `.github/workflows/`**. Nothing compiles this
>   directory on CI, so no build result is pinned to a commit.
>
> Until `lake build` is run over the full import graph — and ideally wired into
> CI — treat Phase 11 as *written and sorry-free in source*, not as
> kernel-checked. Only the Lean kernel can turn the first into the second.

For the modules that *are* compiled, `lake build` passes with 0 errors, 0 sorries.

```
pytopSNF_isInvariantFactors : IsInvariantFactors (pytopSNF A)
  ├── pytopSNF_positive          : ∀ d ∈ pytopSNF A, 0 < d
  └── pytopSNF_divisibilityChain : IsDivisibilityChain (pytopSNF A)

pytopSNF_fuel_independent :
  numRows A * numCols A * (sumAbs A + 1) ≤ k →
  pytopSNFWithFuel (min m n) k A = pytopSNF A
```

## Module Map

```
Formal/SNF/
  Defs.lean               — IntMatrix, entry, numRows/numCols, IsSmithNF spec
  Elementary.lean         — addRow, addCol, swapRows, swapCols + entry lemmas
  Algorithm.lean          — clearPass, clearLoop, findPivot, pytopSNF definitions
  Termination.lean        — clearLoop stabilises (idempotency of clearPass)
  Positivity.lean         — invariant factors are positive (pivot preservation chain)
  Divisibility.lean       — pivotDividesAll + snfOuterStep divisibility
  Chain.lean              — divisibility chain of invariant factors
  Correctness.lean        — top-level IsSmithNF theorem + fuel sufficiency
  TestLemmas.lean         — scratch / sanity checks

Formal/
  SetTopology.lean        — point-set topology: T0–T4 axioms, closure/interior,
                            compactness, continuity, 34 proved theorems
  SetTopologyAltProofs.lean — 24 alternative proofs of SetTopology results in 5 strategies:
                            [ÇY] by contradiction, [KT] contrapositive, [D] alternative
                            direct, [De] interior-closure duality, [Tak] simp-heavy
  MetricTopology.lean     — metric spaces: ε-δ continuity ↔ topological, Cauchy sequences,
                            Banach fixed-point (existence + uniqueness)
  Basic.lean              — set-theoretic utilities
  Homology.lean           — simplicial homology (descriptive layer)
  EulerChar.lean          — Euler characteristic
  PiBase.lean             — pi-Base property reasoning
  PersHomology.lean       — persistent homology stubs

Formal/  (Phase 11 — imported by Formal.lean, but NEVER COMPILED in this tree:
          no .olean exists for any of the five; see the build caveat above)
  MayerVietoris.lean      — connecting morphism well-definedness, snake diagram
  VanKampen.lean          — Tietze equivalence, pushout universal property
  CohomologyRing.lean     — cup product associativity, Leibniz rule over ℤ/2
  PersistencePairing.lean — reduction is perfect, births are distinct
  SpectralSequences.lean  — d∘d = 0, convergence of constant sequences

tools/
  bilingual_docs.py       — generates bilingual (EN/TR) Markdown proof documentation
                            from SetTopology.lean; dependency-free, template-driven
  data/                   — JSON template and terminology files
```

## Proof Status

### SNF module

| File | Status |
|------|--------|
| Defs.lean | — (pure defs) |
| Elementary.lean | **all proved** — `addRow_entry_{emod,dst,unaffected}`, `addCol_*`, `swapRows_*`, `foldl_*` |
| Algorithm.lean | — (pure defs) |
| Termination.lean | **all proved** — `clearPass_{col,row}_residue`, `clearPass_idempotent`, `minNonzeroAbs_zero_iff`, `clearLoop_stable`, `clearLoop_stuck`, `clearLoop_preserves_pivot`, `clearLoop_{col_t_of_succ,col_lt_pivot}` |
| Positivity.lean | **all proved** — `snfOuterStep_pos`, `pytopSNF_positive`, `findPivot_indices_ge`, `enforceDivisibility_pivot_ne_zero` |
| Divisibility.lean | **all proved** — `pivotDividesAll_correct`, `snfOuterStep_divides_submatrix` (both branches) |
| Chain.lean | **all proved** — `factor_dvd_next` (both branches), `pytopSNF_divisibilityChain` |
| Correctness.lean | **all proved** — `pytopSNF_isInvariantFactors`, `pytopSNF_fuel_independent` |

### Topology modules

| File | Theorems | Status |
|------|----------|--------|
| SetTopology.lean | 34 | **all proved** — T0–T4 separation, closure/interior duality, compactness, continuity, diagonal characterisation, 0 sorry |
| SetTopologyAltProofs.lean | 24 | **all proved** — alternative strategies for SetTopology results (by contradiction, contrapositive, direct, duality, simp-heavy), 0 sorry. **Never compiled:** not imported by `Formal.lean`, so `lake build` never reaches it. |
| MetricTopology.lean | ~15 | **all proved** — ε-δ ↔ topological continuity, Cauchy sequences, Banach fixed-point (existence *and* uniqueness), **0 sorry**. The previously noted "1 sorry: contraction uniqueness" is gone: the file contains no `sorry` tactic, and it is compiled (`MetricTopology.olean` is present). |

### Phase 11 modules

`MayerVietoris.lean`, `VanKampen.lean`, `CohomologyRing.lean`,
`PersistencePairing.lean` and `SpectralSequences.lean` are listed in
`formal/ROADMAP.md` with their theorems. They are **not** given a status row here
because none of them has been compiled — see the build caveat at the top of this
file. `formal/ROADMAP.md` also records the `Bridge.lean` gap: `IsSmithNF` is
positivity plus divisibility chain only, with no matrix-equivalence clause.

## Building

```bash
lake build
```

Requires Lean 4.31.0 and Mathlib v4.31.0 (managed by `lake`).

## Proof Architecture

### Termination: idempotency, not descent

The key insight is that `clearPass` is **idempotent** when the pivot is nonzero:
`clearPass (clearPass A t) t = clearPass A t`. This holds because after one pass,
every off-diagonal column-t and row-t entry is a remainder `r = a % pivot`, with
`0 ≤ r < |pivot|`, so the second pass computes factor `r / pivot = 0` — identity.

Consequence: `clearLoop A t f` is the same for **all `f ≥ 1`**. No fuel-descent
argument needed. The outer loop fuel `min(m,n)` bounds the number of diagonal steps.

### Positivity: bypassing `isCleared`

`snfOuterStep_pos` avoids proving `isCleared A₃ t` (which is not always true).
Instead: with fuel ≥ 1, `clearLoop_col_lt_pivot` shows every off-pivot column-t entry
is strictly bounded by the pivot, so `enforceDivisibility` cannot zero the pivot.

### Chain: `factor_dvd_next` via invariant propagation

The divisibility chain is proved by threading a loop invariant through the outer `go`
recursion: at step `t`, every recorded factor divides all entries in the t-submatrix.
Elementary ops (swapRows/Cols, clearLoop, enforceDivisibility) preserve this invariant.
`pivotDividesAll` then guarantees the next factor divides the new pivot.

### Fuel sufficiency

`pytopSNF_fuel_independent` shows any `k ≥ m·n·(|A|+1)` gives the same result as
the standard fuel. Proof: idempotency → all `clearLoop` calls with fuel ≥ 1 coincide
→ `snfOuterStep` is fuel-independent for fuel ≥ 1 → outer `go` loop is too.
