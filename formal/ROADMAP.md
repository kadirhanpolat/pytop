# Formal Verification Roadmap

Status as of 2026-06-20.

## Completed

### Elementary operations (`Elementary.lean`)
- [x] `addRow_entry_unaffected` / `addCol_entry_unaffected`
- [x] `addRow_entry_dst` / `addCol_entry_dst`
- [x] `swapRows_entry_i`
- [x] `foldl_addRow_pres_pivot` / `foldl_addCol_pres_pivot`
- [x] `addRow_entry_emod` — `entry (addRow A t i factor) i t = entry A i t % entry A t t`
- [x] `addCol_entry_emod` — symmetric for columns

### Termination (`Termination.lean`)
- [x] `clearPass_preserves_pivot`
- [x] `clearLoop_zero`, `clearLoop_succ`, `clearLoop_stuck`
- [x] `clearLoop_stable` (partial)
- [x] `clearPass_col_residue` — `|entry (clearPass A t) i t| < |entry A t t|`
- [x] `clearPass_row_residue` — `|entry (clearPass A t) t j| < |entry A t t|` (needs `j ∈ range (numCols A)`)
- [x] Private helpers: `foldl_addRow_not_mem_row`, `foldl_addCol_not_mem_col`, `foldl_addRow_pres_row_t`, `foldl_addCol_pres_col_t`

### Positivity (`Positivity.lean`)
- [x] `clearLoop_preserves_pivot`
- [x] `isCleared_col_zero`
- [x] `clearLoop_pivot_ne_zero`
- [x] `swapped_pivot_ne_zero`
- [x] `enforceDivisibility_preserves_pivot` + `findSome?_exists`

### Divisibility (`Divisibility.lean`)
- [x] `submatrix_entry`, `mem_of_getElem?_some`
- [x] `pivotDividesAll_correct`
- [x] `dvd_natAbs_cast`
- [x] `snfOuterStep_divides_submatrix` Branch 1

## Next Steps

### Termination (remaining)
- [ ] `minNonzeroAbs_zero_iff` — `minNonzeroAbs A t = 0 ↔ isCleared A t`
- [ ] `clearPass_decreases_minNonzeroAbs` — combines `clearPass_{col,row}_residue`
  with `minNonzeroAbs` monotonicity; needs `¬isCleared → ∃ nonzero entry in range`

### Positivity (remaining)
- [ ] `findPivot_entry_nonzero` — nonzero entry exists when matrix not cleared
- [ ] `swapRows_swapCols_diagonal` — swap moves found pivot to (t,t)
- [ ] `snfOuterStep_pos` Branch 2 (`hcleared₃`)
- [ ] `pytopSNF_positive` — induction on `go` fuel

### Divisibility (remaining)
- [ ] `snfOuterStep_divides_submatrix` Branch 2 — fuel-sufficiency gap

### Chain (`Chain.lean`)
- [ ] `factor_dvd_next` Branch 1 (needs `findPivot_entry_nonzero`)
- [ ] `factor_dvd_next` Branch 2 (needs `hcleared₃` fuel gap)
- [ ] `pytopSNF_divisibilityChain`

### Correctness (`Correctness.lean`)
- [ ] All main theorems (depends on all above)

## Key Blockers

**Fuel-sufficiency gap**: `snfOuterStep_pos Branch 2` and `Chain Branch 2` both require
showing that `innerFuel ≥ minNonzeroAbs A₂ t`. This follows from
`clearPass_decreases_minNonzeroAbs` (once proved) + `clearLoop_stable`, but the chain
needs to be assembled carefully.

**`findPivot_entry_nonzero`**: requires showing that if the submatrix has a nonzero entry,
`findPivot` returns a nonzero position. Straightforward from `findPivot` definition via
`List.foldl` case analysis.
