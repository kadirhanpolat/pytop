import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Mathlib.Data.Int.GCD

/-!
# Positivity of SNF Invariant Factors

We prove that every factor returned by `pytopSNF` is strictly positive.

## Proof chain

1. `findPivot A t = some (pi, pj)` → `entry A pi pj ≠ 0` (sorry).
2. Swapping rows/cols moves the pivot to (t,t) (sorry).
3. **`clearLoop_preserves_pivot`** — proved here by induction on fuel.
4. Combining 1–3: the diagonal entry at (t,t) is always nonzero after setup.
5. `snfOuterStep_pos` — sorry-scaffolded, with key structural cases.
6. `pytopSNF_positive` — sorry; follows by induction on the `go` helper.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Sub-lemmas (sorry'd algebraic steps)
-- ---------------------------------------------------------------------------

/-- `findPivot` only returns positions with nonzero entries. -/
theorem findPivot_entry_nonzero (A : IntMatrix) (t pi pj : Nat)
    (h : findPivot A t = some (pi, pj)) :
    entry A pi pj ≠ 0 := by
  sorry

/-- Swapping rows pi↔t then cols pj↔t places the (pi, pj) entry at (t, t). -/
theorem swapRows_swapCols_diagonal (A : IntMatrix) (pi pj t : Nat) :
    entry (swapCols (swapRows A pi t) pj t) t t = entry A pi pj := by
  sorry

-- ---------------------------------------------------------------------------
-- clearLoop preserves the diagonal entry at (t, t)  [KEY PROVED THEOREM]
-- ---------------------------------------------------------------------------

/-- `clearLoop` does not change the diagonal entry at position (t, t).

Induction on fuel:
- Base (`k = 0`): `clearLoop A t 0 = A` by `clearLoop_zero`.
- Step (`k = n+1`):
  - If `isCleared A t`: returns A unchanged.
  - Else: returns `clearLoop (clearPass A t) t n`.
    By IH (generalised over A), `entry (clearLoop (clearPass A t) t n) t t`
    = `entry (clearPass A t) t t` = `entry A t t` (clearPass_preserves_pivot). -/
theorem clearLoop_preserves_pivot (A : IntMatrix) (t k : Nat) :
    entry (clearLoop A t k) t t = entry A t t := by
  induction k generalizing A with
  | zero => simp [clearLoop_zero]
  | succ n ih =>
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · rw [ih (clearPass A t), clearPass_preserves_pivot]

-- ---------------------------------------------------------------------------
-- Derived lemmas about the pivot
-- ---------------------------------------------------------------------------

/-- After swapping (pi,pj) to the diagonal, that entry is nonzero. -/
theorem swapped_pivot_ne_zero (A : IntMatrix) (t pi pj : Nat)
    (hfp : findPivot A t = some (pi, pj)) :
    entry (swapCols (swapRows A pi t) pj t) t t ≠ 0 := by
  rw [swapRows_swapCols_diagonal]
  exact findPivot_entry_nonzero A t pi pj hfp

/-- After `clearLoop`, the diagonal entry is still the original pivot value (nonzero). -/
theorem clearLoop_pivot_ne_zero (A : IntMatrix) (t pi pj innerFuel : Nat)
    (hfp : findPivot A t = some (pi, pj)) :
    entry (clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel) t t ≠ 0 := by
  rw [clearLoop_preserves_pivot]
  exact swapped_pivot_ne_zero A t pi pj hfp

-- ---------------------------------------------------------------------------
-- findSome? existence helper (avoids depending on Mathlib API name)
-- ---------------------------------------------------------------------------

private lemma findSome?_exists {α β : Type*} {l : List α} {f : α → Option β} {b : β}
    (h : l.findSome? f = some b) : ∃ a ∈ l, f a = some b := by
  induction l with
  | nil => simp [List.findSome?] at h
  | cons a as ih =>
    unfold List.findSome? at h
    rcases hfa : f a with _ | b'
    · simp only [hfa] at h
      obtain ⟨x, hx, hxf⟩ := ih h
      exact ⟨x, List.mem_cons.mpr (Or.inr hx), hxf⟩
    · simp only [hfa] at h
      exact ⟨a, List.mem_cons.mpr (Or.inl rfl), hfa.trans h⟩

-- ---------------------------------------------------------------------------
-- isCleared and enforceDivisibility
-- ---------------------------------------------------------------------------

/-- When `isCleared A t`, every entry in column t (except row t) is zero. -/
theorem isCleared_col_zero (A : IntMatrix) (t i : Nat) (ht : i ≠ t)
    (hcleared : isCleared A t = true) :
    entry A i t = 0 := by
  simp only [isCleared, Bool.and_eq_true, List.all_eq_true] at hcleared
  obtain ⟨hcol, _⟩ := hcleared
  by_cases hi : i < numRows A
  · have hmem : i ∈ List.range (numRows A) := List.mem_range.mpr hi
    have hcheck := hcol i hmem
    simp only [Bool.or_eq_true, decide_eq_true_eq] at hcheck
    rcases hcheck with rfl | h
    · exact absurd rfl ht
    · exact h
  · -- i ≥ numRows A → A[i]? = none → entry = 0
    push_neg at hi
    have hge : A.length ≤ i := by simpa [numRows] using hi
    have hni : A[i]? = none := List.getElem?_eq_none_iff.mpr hge
    simp [entry, hni]

/-- `enforceDivisibility A t` does not change `entry A t t` when the matrix
    is cleared (column t is zero off the diagonal).

Proof: if `bad = none`, the matrix is unchanged.  If `bad = some (i, j)`, the
algorithm returns `addRow A i t 1`.  By `addRow_entry_dst`:
  `entry (addRow A i t 1) t t = entry A t t + 1 * entry A i t`.
Since `isCleared A t` and `i > t`, `entry A i t = 0` by `isCleared_col_zero`. -/
theorem enforceDivisibility_preserves_pivot (A : IntMatrix) (t : Nat)
    (hcleared : isCleared A t = true) :
    entry (enforceDivisibility A t) t t = entry A t t := by
  unfold enforceDivisibility
  -- Case 1: pivot = 0 → unchanged
  by_cases hpivot_ne : entry A t t = 0
  · simp [hpivot_ne]
  -- Case 2: pivot ≠ 0
  · simp only [hpivot_ne, ite_false]
    -- Derive row bound from hpivot_ne : entry A t t ≠ 0
    have ht_row : t < numRows A := by
      simp only [numRows]
      by_contra hge
      push_neg at hge
      have hne : A[t]? = none := List.getElem?_eq_none_iff.mpr hge
      simp [entry, hne] at hpivot_ne
    -- Derive column bound
    have ht_col : t < (A.getD t []).length := by
      have hAt : A[t]? = some (A[t]'ht_row) :=
        List.getElem?_eq_getElem ht_row
      rw [show A.getD t [] = A[t]'ht_row from by simp [List.getD, hAt]]
      by_contra hge
      push_neg at hge
      have hcol : (A[t]'ht_row)[t]? = none := List.getElem?_eq_none_iff.mpr hge
      simp [entry, hAt, hcol] at hpivot_ne
    -- Case-split on bad
    set m := numRows A
    set n := numCols A
    set bad := (List.range m).findSome? fun i =>
      if i ≤ t then none
      else (List.range n).findSome? fun j =>
        if j ≤ t then none
        else if entry A i j % entry A t t ≠ 0 then some (i, j) else none
    rcases hbad : bad with _ | ⟨i, _j⟩
    · -- bad = none: unchanged
      rfl
    · -- bad = some (i, _j): return addRow A i t 1
      simp only
      -- entry A i t = 0  (isCleared_col_zero, needs i > t)
      have hi_gt : t < i := by
        -- Extract witness k from the outer findSome? (bad = some (i, _j))
        obtain ⟨k, hk_mem, hk_val⟩ := findSome?_exists hbad
        simp only [List.mem_range] at hk_mem   -- hk_mem : k < m
        -- Outer guard: if k ≤ t then none → k must satisfy t < k
        by_cases hkt : k ≤ t
        · simp [if_pos hkt] at hk_val          -- none = some _ → False → goal closed
        · simp only [if_neg hkt] at hk_val
          -- hk_val : inner findSome? for row k = some (i, _j)
          obtain ⟨j0, _, hj0_val⟩ := findSome?_exists hk_val
          -- Inner guard: if j0 ≤ t then none
          by_cases hj0t : j0 ≤ t
          · simp [if_pos hj0t] at hj0_val      -- none = some _ → False → goal closed
          · simp only [if_neg hj0t] at hj0_val
            split_ifs at hj0_val with hmod
            · -- some (k, j0) = some (i, _j)  →  i = k, and t < k from hkt
              -- (split_ifs auto-closes the ¬hmod branch where hj0_val : none = some _)
              have hik : k = i := (Prod.ext_iff.mp (Option.some.inj hj0_val)).1
              simp only [Nat.not_le] at hkt; omega
      have hentry_it : entry A i t = 0 :=
        isCleared_col_zero A t i (Nat.ne_of_gt hi_gt) hcleared
      -- Apply addRow_entry_dst
      rw [addRow_entry_dst A i t t 1 ht_row ht_col]
      simp [hentry_it]

-- ---------------------------------------------------------------------------
-- snfOuterStep returns a positive factor
-- ---------------------------------------------------------------------------

/-- A nonzero integer has positive `natAbs`, viewed as an integer. -/
theorem natAbs_cast_pos {x : Int} (h : x ≠ 0) : (0 : Int) < ↑x.natAbs :=
  Int.natCast_pos.mpr (Int.natAbs_pos.mpr h)

/-- Every factor returned by `snfOuterStep` is strictly positive.

Proof sketch (sorry'd):
- `findPivot` returns none → result is `none` → h : none = some d → contradiction.
- `findPivot` returns `some (pi, pj)`:
  - A₂ = swapCols (swapRows A pi t) pj t:  entry A₂ t t = entry A pi pj ≠ 0
  - A₃ = clearLoop A₂ t innerFuel:
    entry A₃ t t = entry A₂ t t ≠ 0  (clearLoop_preserves_pivot)
  - If pivotDividesAll A₃:  d = ↑(entry A₃ t t).natAbs > 0  ✓
  - Else:  A₄ = enforceDivisibility A₃ t;  A₅ = clearLoop A₄ t innerFuel
    entry A₄ t t = entry A₃ t t ≠ 0  (enforceDivisibility_preserves_pivot — sorry'd)
    entry A₅ t t = entry A₄ t t ≠ 0  (clearLoop_preserves_pivot)
    If pivotDividesAll A₅:  d = ↑(entry A₅ t t).natAbs > 0  ✓
    Else:  result is none → h : none = some d → contradiction. -/
theorem snfOuterStep_pos (A : IntMatrix) (t innerFuel : Nat) (d : Int)
    (h : (snfOuterStep A t innerFuel).2 = some d) : 0 < d := by
  unfold snfOuterStep at h
  cases hfp : findPivot A t with
  | none =>
    -- (A, none).2 = none ≠ some d
    rw [hfp] at h; simp at h
  | some pij =>
    obtain ⟨pi, pj⟩ := pij
    rw [hfp] at h
    simp only at h
    -- h is about a two-level if-then-else; split_ifs generates 3 goals:
    --   (1) outer true, (2) outer false + inner true, (3) both false → none = some d
    -- split_ifs creates 3 sub-goals for the two nested ifs in h, but the third
    -- (none = some d) is auto-closed by split_ifs via simp, leaving 2 open goals.
    split_ifs at h with hpda hpda'
    · -- Case 1: pivotDividesAll A₃ t = true
      -- h : some ↑(entry A₃ t t).natAbs = some d
      set A₃ := clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel
      have hd : d = ↑(entry A₃ t t).natAbs :=
        (Option.some.inj h).symm
      rw [hd]
      exact natAbs_cast_pos (clearLoop_pivot_ne_zero A t pi pj innerFuel hfp)

    · -- Case 2: ¬ pivotDividesAll A₃ t, pivotDividesAll A₅ t = true
      -- h : some ↑(entry A₅ t t).natAbs = some d
      have hd : d = ↑(entry _ t t).natAbs := (Option.some.inj h).symm
      rw [hd]
      -- Need: entry A₅ t t ≠ 0
      -- Chain: A₂ → A₃ = clearLoop A₂ → A₄ = enforceDivisibility A₃ → A₅ = clearLoop A₄
      -- entry A₃ t t ≠ 0  (clearLoop_pivot_ne_zero)
      -- entry A₄ t t = entry A₃ t t  (enforceDivisibility_preserves_pivot — needs isCleared A₃)
      -- entry A₅ t t = entry A₄ t t  (clearLoop_preserves_pivot)
      set A₂ := swapCols (swapRows A pi t) pj t
      set A₃ := clearLoop A₂ t innerFuel
      have hA₃_ne : entry A₃ t t ≠ 0 := clearLoop_pivot_ne_zero A t pi pj innerFuel hfp
      -- isCleared A₃ t: with sufficient fuel, clearLoop always clears (sorry'd)
      have hcleared₃ : isCleared A₃ t = true := by sorry
      have hA₄ : entry (enforceDivisibility A₃ t) t t = entry A₃ t t :=
        enforceDivisibility_preserves_pivot A₃ t hcleared₃
      have hA₅ : entry (clearLoop (enforceDivisibility A₃ t) t innerFuel) t t =
                 entry (enforceDivisibility A₃ t) t t :=
        clearLoop_preserves_pivot (enforceDivisibility A₃ t) t innerFuel
      -- chain: entry (clearLoop A₄) t t = entry A₄ t t = entry A₃ t t ≠ 0
      have hfinal : entry (clearLoop (enforceDivisibility A₃ t) t innerFuel) t t ≠ 0 := by
        rw [hA₅, hA₄]; exact hA₃_ne
      exact natAbs_cast_pos hfinal

-- ---------------------------------------------------------------------------
-- pytopSNF_positive
-- ---------------------------------------------------------------------------

/-- Every factor in the output of `pytopSNF A` is strictly positive. -/
theorem pytopSNF_positive (A : IntMatrix) : ∀ d ∈ pytopSNF A, 0 < d := by
  sorry
  -- Induction on `pytopSNFWithFuel.go` outerFuel:
  -- At each step, if snfOuterStep returns some d then 0 < d by snfOuterStep_pos,
  -- and d is prepended to acc.  After acc.reverse, all elements are positive.

end PytopSNF
