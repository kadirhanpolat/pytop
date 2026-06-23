# Formal Verification Roadmap

Status as of 2026-06-23. **All theorems proved. Phase 11 complete.**

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
- [x] `clearPass_col_residue` — `|entry (clearPass A t) i t| < |entry A t t|`
- [x] `clearPass_row_residue` — symmetric for rows
- [x] `clearPass_col_emod` / `clearPass_row_emod` — exact residue values
- [x] `clearPass_idempotent` — `clearPass (clearPass A t) t = clearPass A t` (pivot ≠ 0)
- [x] `minNonzeroAbs_zero_iff` — zero iff all submatrix entries zero (needs `hwf`)
- [x] `clearLoop_stable` — stabilises once `fuel ≥ minNonzeroAbs A t`
- [x] `clearLoop_preserves_pivot`
- [x] `clearLoop_col_t_of_succ` — column-t entry after fuel ≥ 1 equals `clearPass` value
- [x] `clearLoop_col_lt_pivot` — off-pivot column-t entries strictly bounded by pivot
- [x] Private helpers: `foldl_addRow_not_mem_row`, `foldl_addCol_not_mem_col`,
  `foldl_addRow_pres_row_t`, `foldl_addCol_pres_col_t`, `foldl_addRow_identity`,
  `foldl_addCol_identity`, `addRow_zero`, `addCol_zero`, `int_ediv_zero_of_nonneg_natAbs_lt`

### Positivity (`Positivity.lean`)
- [x] `clearLoop_preserves_pivot`
- [x] `isCleared_col_zero`
- [x] `clearLoop_pivot_ne_zero`
- [x] `swapped_pivot_ne_zero`
- [x] `findPivot_indices_ge` — found pivot indices are ≥ t
- [x] `enforceDivisibility_preserves_pivot` + `findSome?_exists`
- [x] `enforceDivisibility_pivot_ne_zero` — if col-t entries bounded, pivot survives
- [x] `add_ne_zero_of_natAbs_lt` — helper for pivot preservation under addRow
- [x] `snfOuterStep_pos` — `snfOuterStep` returns `some d` with `d > 0` (fuel ≥ 1)
- [x] `pytopSNF_positive` — all invariant factors positive

### Divisibility (`Divisibility.lean`)
- [x] `submatrix_entry`, `mem_of_getElem?_some`
- [x] `pivotDividesAll_correct`
- [x] `dvd_natAbs_cast`
- [x] `snfOuterStep_divides_submatrix` Branch 1 — `pivotDividesAll A₃ t` case
- [x] `snfOuterStep_divides_submatrix` Branch 2 — `¬pivotDividesAll A₃ t` case
  (uses `enforceDivisibility_pivot_ne_zero` + divisibility invariant propagation)

### Chain (`Chain.lean`)
- [x] `isDivisibilityChain_cons_cons` — helper for list induction
- [x] `isDivisibilityChain_append_one` — extending a chain by one element
- [x] `factor_dvd_next` Branch 1 — `snfOuterStep` returns `some d` with `last_d ∣ d`
- [x] `factor_dvd_next` Branch 2 — none/cleared case
- [x] `go_divisibility_chain` — invariant induction through outer loop
- [x] `pytopSNF_divisibilityChain` — `IsDivisibilityChain (pytopSNF A)`

### Correctness (`Correctness.lean`)
- [x] `clearLoop_succ_stable` — `clearLoop A t (k+1) = clearLoop A t (k+2)` unconditionally
- [x] `clearLoop_fuel_eq` — `clearLoop A t 1 = clearLoop A t (k+1)` for all k
- [x] `snfOuterStep_fuel_eq` — fuel-independent for fuel ≥ 1
- [x] `go_fuel_eq` — outer loop fuel-independent for inner fuel ≥ 1
- [x] `pytopSNF_fuel_independent` — any `k ≥ m·n·(|A|+1)` gives the same result
- [x] `pytopSNF_isInvariantFactors` — `IsInvariantFactors (pytopSNF A)` ✓

## Phase 11: Algebraic Topology Extensions (2026-06-23)

Five new proof files extending the formal corpus to 13 files:

### MayerVietoris.lean (P11.1)
- [x] `delta_well_defined`          — two lifts of c ∈ C differ by im(i)
- [x] `mv_connecting_indep`         — Mayer–Vietoris connecting morphism independence
- [x] `ses_p_zero_of_im`            — p ∘ i = 0 from exactness
- [x] `snake_delta_exists`          — connecting element exists via snake diagram
- [x] `snake_delta_independent`     — snake connecting element is well-defined in A'

### VanKampen.lean (P11.2)
- [x] `tietze_equiv_refl / symm / trans` — Tietze equivalence is an equivalence relation
- [x] `tietze_add_gen`              — Tietze move I (add generator)
- [x] `tietze_elim`                 — Tietze move II (eliminate generator)
- [x] `pushout_universal`           — UP of amalgamated free product
- [x] `pushout_compat_preserved`    — factorings respect amalgamation
- [x] `int_hom_determined_by_one`   — ℤ is the free abelian group on one generator
- [x] `int_hom_exists`              — existence part of the free group UP

### CohomologyRing.lean (P11.3)
- [x] `cup_value_assoc`             — (f∧g)∧h = f∧(g∧h) — core associativity
- [x] `cup_assoc_eq`                — cup product associativity (pointwise)
- [x] `cup_bool_comm`               — commutativity of ∧ over Bool (ℤ/2)
- [x] `cup_comm_Z2`                 — cup product commutative for 0-cochains
- [x] `leibniz_0cochains`           — Leibniz rule δ(f∧g) = δf∧g ⊕ f∧δg

### PersistencePairing.lean (P11.4)
- [x] `pairing_is_perfect`          — `isReduced (reduce M)` (from existing reduce_is_reduced)
- [x] `pairs_have_distinct_births`  — birth indices in persistencePairs are Nodup
  Key lemmas: `isReduced_tail`, `filterMap_getLast_nodup_of_isReduced`,
              `zipWith_filterMap_snd_eq`, `map_fst_filterMap_eq`, `map_fst_pairs_eq`

### SpectralSequences.lean (P11.5)
- [x] `d_sq_zero`                   — d ∘ d = 0 (by structure invariant)
- [x] `image_sub_kernel`            — im(d) ⊆ ker(d)
- [x] `const_convergent`            — constant spectral sequence converges
- [x] `stabilizes_mono`             — stabilisation is upward-closed
- [x] `same_diff_implies_same_stab` — sequences agreeing from r₀ share stabilisation
- [x] `const_pages_convergent`      — sequence with constant pages converges

## Key Proof Insights

### Why descent was abandoned

The original roadmap planned a `clearPass_decreases_minNonzeroAbs` descent argument.
This is **false**: example `A = [[2, 100], [3, 0]]` at `t=0` increases `sumAbs` after
one `clearPass`. The correct termination proof uses `clearPass_idempotent` instead:
after one pass, every off-pivot entry is a remainder, so the second pass computes
factor 0 at every row/col — the loop is already stable.

### Why `isCleared` was bypassed in positivity

`snfOuterStep_pos` Branch 2 cannot rely on `isCleared A₃ t` being true (it need not
be). Instead, `clearLoop_col_lt_pivot` bounds off-pivot column-t entries by the pivot,
making `enforceDivisibility_pivot_ne_zero` applicable without clearing.

### Fuel sufficiency via idempotency

`pytopSNF_fuel_independent` doesn't use `clearLoop_stable` at all. The key lemma
`clearLoop_succ_stable` (`clearLoop A t (k+1) = clearLoop A t (k+2)`) is proved
unconditionally from `clearPass_idempotent`, showing that all fuel values ≥ 1 give
identical results. This makes `snfOuterStep` and the outer `go` loop both
fuel-independent for inner fuel ≥ 1.
