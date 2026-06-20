# pytop — Formal SNF Verification

Lean 4 (v4.31.0) + Mathlib formal verification of the Smith Normal Form algorithm
used in [`pytop.exact_linalg`](https://github.com/kadirhanpolat/pytop).

## Goal

Prove that `pytopSNF` (a fuel-bounded implementation of integer SNF via elementary
row/column operations) is correct: it terminates, produces positive invariant factors,
and the factors form a divisibility chain.

## Status: **Complete**

All theorems proved. `lake build` passes with 0 errors, 0 sorries.

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
  Defs.lean          — IntMatrix, entry, numRows/numCols, IsSmithNF spec
  Elementary.lean    — addRow, addCol, swapRows, swapCols + entry lemmas
  Algorithm.lean     — clearPass, clearLoop, findPivot, pytopSNF definitions
  Termination.lean   — clearLoop stabilises (idempotency of clearPass)
  Positivity.lean    — invariant factors are positive (pivot preservation chain)
  Divisibility.lean  — pivotDividesAll + snfOuterStep divisibility
  Chain.lean         — divisibility chain of invariant factors
  Correctness.lean   — top-level IsSmithNF theorem + fuel sufficiency
  TestLemmas.lean    — scratch / sanity checks
```

## Proof Status

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
