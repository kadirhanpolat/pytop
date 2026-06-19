# pytop — Formal SNF Verification

Lean 4 (v4.31.0) + Mathlib formal verification of the Smith Normal Form algorithm
used in [`pytop.exact_linalg`](https://github.com/kadirhanpolat/pytop).

## Goal

Prove that `pytopSNF` (a fuel-bounded implementation of integer SNF via elementary
row/column operations) is correct: it terminates, produces positive invariant factors,
and the factors form a divisibility chain.

## Module Map

```
Formal/SNF/
  Defs.lean          — IntMatrix, entry, numRows/numCols, IsSmithNF spec
  Elementary.lean    — addRow, addCol, swapRows, swapCols + entry lemmas
  Algorithm.lean     — clearPass, clearLoop, findPivot, pytopSNF definitions
  Termination.lean   — clearLoop stabilises once fuel ≥ minNonzeroAbs
  Positivity.lean    — invariant factors are positive (pivot preservation chain)
  Divisibility.lean  — pivotDividesAll + snfOuterStep divisibility
  Chain.lean         — divisibility chain of invariant factors
  Correctness.lean   — top-level IsSmithNF theorem
  TestLemmas.lean    — scratch / sanity checks
```

## Proof Status

| File | Proved | Remaining |
|------|--------|-----------|
| Defs.lean | — (pure defs) | — |
| Elementary.lean | all theorems incl. `addRow_entry_emod`, `addCol_entry_emod` | — |
| Algorithm.lean | — (pure defs) | — |
| Termination.lean | `clearPass_col_residue`, `clearPass_row_residue`, `clearPass_preserves_pivot`, helpers | `minNonzeroAbs_zero_iff`, `clearPass_decreases_minNonzeroAbs` |
| Positivity.lean | `clearLoop_preserves_pivot`, `isCleared_col_zero`, `clearLoop_pivot_ne_zero`, `enforceDivisibility_preserves_pivot` | `findPivot_entry_nonzero`, `snfOuterStep_pos` branch 2, `pytopSNF_positive` |
| Divisibility.lean | `pivotDividesAll_correct`, `snfOuterStep_divides_submatrix` branch 1 | branch 2 |
| Chain.lean | — | `factor_dvd_next`, `pytopSNF_divisibilityChain` |
| Correctness.lean | — | all main theorems |

## Building

```bash
lake build
```

Requires Lean 4.31.0 and Mathlib v4.31.0 (managed by `lake`).

## Proof Architecture

The central termination argument: `minNonzeroAbs` (minimum |entry| in the t-submatrix)
strictly decreases after each `clearPass` whenever the matrix is not yet cleared.
Each clearing step produces a remainder `r = a % pivot`, and `|r| < |pivot| ≤ minNonzeroAbs`,
giving a natural-number descent that bounds the fuel needed.

Key helper proved in `Elementary.lean`:
- `addRow_entry_emod` / `addCol_entry_emod`: after applying the clearing factor, the
  modified entry equals `a % pivot` (proved via `Int.emod_def` + ring arithmetic).

Key structural lemmas in `Termination.lean`:
- `clearPass_col_residue`: after `clearPass`, every off-pivot column-t entry has
  strictly smaller `natAbs` than the pivot.
- `clearPass_row_residue`: same for row-t entries (requires `j ∈ range (numCols A)`).
- `foldl_addRow_pres_row_t` / `foldl_addCol_pres_col_t`: the respective foldls
  preserve pivot-row / pivot-column entries.
