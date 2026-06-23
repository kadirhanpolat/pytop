import Formal.PersHomology

/-!
# P11.4 — Persistence Pairing Perfection

Two main theorems:
* `pairing_is_perfect`        : `isReduced (reduce M)` — no two non-zero columns share a pivot.
* `pairs_have_distinct_births`: birth indices in `persistencePairs M` are pairwise distinct.
-/

namespace PersistencePairing

open PersHomology

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. Pivot injectivity
-- ─────────────────────────────────────────────────────────────────────────────

/-- A reduced matrix has no two distinct non-zero columns sharing the same pivot row. -/
lemma isReduced_pivot_injective {R : Z2Matrix} (hred : isReduced R)
    {j1 j2 : Fin R.length} (hne : j1 ≠ j2) {i : Nat}
    (h1 : (R.get j1).getLast? = some i)
    (h2 : (R.get j2).getLast? = some i) : False := by
  rcases hred j1 j2 hne with h | h
  · simp [h] at h1
  · exact h (h1.trans h2.symm)

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. pairing_is_perfect
-- ─────────────────────────────────────────────────────────────────────────────

/-- The persistence algorithm produces a perfectly paired reduced matrix. -/
theorem pairing_is_perfect (M : Z2Matrix)
    (hsorted : ∀ col ∈ M, List.Pairwise (· < ·) col)
    (hbound  : ∀ col ∈ M, ∀ i ∈ col, i < M.length) :
    isReduced (reduce M) :=
  reduce_is_reduced M hsorted hbound

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. isReduced strips to tail
-- ─────────────────────────────────────────────────────────────────────────────

private lemma isReduced_tail {col : Z2Col} {R' : Z2Matrix}
    (hred : isReduced (col :: R')) : isReduced R' := by
  intro j1 j2 hne
  have h := hred ⟨j1.val + 1, by simp; omega⟩ ⟨j2.val + 1, by simp; omega⟩
    (by simp only [Fin.mk.injEq]; exact Fin.val_ne_of_ne hne)
  simpa [List.get_cons_succ] using h

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. Pivot list is Nodup for any reduced matrix
-- ─────────────────────────────────────────────────────────────────────────────

/-- If R is reduced then the list of its column pivots (non-empty column last elements)
    contains no duplicates. -/
private lemma filterMap_getLast_nodup_of_isReduced :
    ∀ (R : Z2Matrix), isReduced R → (R.filterMap List.getLast?).Nodup := by
  intro R
  induction R with
  | nil => simp
  | cons col R' ih =>
    intro hred
    simp only [List.filterMap_cons]
    rcases hpiv : col.getLast? with _ | i
    · exact ih R' (isReduced_tail hred)
    · simp only [List.nodup_cons]
      refine ⟨?_, ih R' (isReduced_tail hred)⟩
      -- Show pivot i does not appear in R'.filterMap getLast?
      intro hi
      rw [List.mem_filterMap] at hi
      obtain ⟨col', hcol'_mem, hcol'_some⟩ := hi
      -- Get positional index of col' inside R'
      rw [List.mem_iff_getElem] at hcol'_mem
      obtain ⟨k, hk, hkeq⟩ := hcol'_mem
      -- R'[k] = col', so R'[k].getLast? = some i
      have hk_piv : (R'.get ⟨k, hk⟩).getLast? = some i := by
        rw [List.get_eq_getElem]; rw [← hkeq]; exact hcol'_some
      -- In R = col :: R', column 0 and column k+1 both have pivot i
      have hcontra := hred ⟨0, by simp⟩ ⟨k + 1, by simp; omega⟩
        (by simp [Fin.ext_iff])
      simp only [List.get_cons_zero, List.get_cons_succ] at hcontra
      rcases hcontra with h | h
      · exact absurd hpiv (h ▸ (by simp))
      · exact h (hpiv.trans hk_piv.symm)

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. filterMap of second components of zipWith = filterMap of the list itself
-- ─────────────────────────────────────────────────────────────────────────────

/-- Filtering by second component's getLast? on a zipWith-with-nats is the same
    as filtering the original list, for any index list l. -/
private lemma zipWith_filterMap_snd_eq_aux (l : List Nat) (R : Z2Matrix) :
    (List.zipWith Prod.mk l R).filterMap (fun p => p.2.getLast?) =
    (R.take l.length).filterMap List.getLast? := by
  induction R generalizing l with
  | nil => simp
  | cons col R' ih =>
    cases l with
    | nil => simp
    | cons j t =>
      simp only [List.zipWith_cons_cons, List.filterMap_cons, List.length_cons,
                 List.take_succ_cons, ih t]
      rcases col.getLast? with _ | i <;> simp

private lemma zipWith_range_filterMap_snd_eq (R : Z2Matrix) :
    (List.zipWith Prod.mk (List.range R.length) R).filterMap (fun p => p.2.getLast?) =
    R.filterMap List.getLast? := by
  rw [zipWith_filterMap_snd_eq_aux]
  simp [List.take_length]

-- ─────────────────────────────────────────────────────────────────────────────
-- 6. map Prod.fst of persistencePairs = filterMap getLast? of reduce M
-- ─────────────────────────────────────────────────────────────────────────────

private lemma map_fst_filterMap_eq (L : List (Nat × Z2Col)) :
    (L.filterMap (fun p => p.2.getLast?.map fun i => (i, p.1))).map Prod.fst =
    L.filterMap fun p => p.2.getLast? := by
  induction L with
  | nil => simp
  | cons p rest ih =>
    simp only [List.filterMap_cons]
    rcases h : p.2.getLast? with _ | i
    · simp [h]; exact ih
    · simp only [h, Option.map_some, List.map_cons]; exact congrArg (List.cons i) ih

private lemma map_fst_pairs_eq (M : Z2Matrix) :
    (persistencePairs M).map Prod.fst =
    (reduce M).filterMap List.getLast? := by
  simp only [persistencePairs]
  rw [map_fst_filterMap_eq]
  exact zipWith_range_filterMap_snd_eq (reduce M)

-- ─────────────────────────────────────────────────────────────────────────────
-- 7. Main theorem: births are pairwise distinct
-- ─────────────────────────────────────────────────────────────────────────────

/-- Birth indices in `persistencePairs M` are pairwise distinct.
    Follows from `isReduced (reduce M)`: every non-zero column has a unique pivot row. -/
theorem pairs_have_distinct_births (M : Z2Matrix)
    (hsorted : ∀ col ∈ M, List.Pairwise (· < ·) col)
    (hbound  : ∀ col ∈ M, ∀ i ∈ col, i < M.length) :
    ((persistencePairs M).map Prod.fst).Nodup := by
  rw [map_fst_pairs_eq]
  exact filterMap_getLast_nodup_of_isReduced (reduce M)
    (reduce_is_reduced M hsorted hbound)

end PersistencePairing
