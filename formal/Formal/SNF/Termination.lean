import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Mathlib.Data.Int.GCD
import Mathlib.Algebra.Order.Group.Unbundled.Int
import Mathlib.Data.List.Nodup

/-!
# Termination of the Inner Clearing Loop

We prove that `clearLoop A t fuel` stabilises once `fuel ≥ minNonzeroAbs A t`.

## Key insight

`sumAbs` is NOT a suitable decreasing measure for the inner loop.
Counter-example: A = [[2, 100], [3, 0]], t = 0, pivot = 2.
After one `clearPass`:  row 1 becomes [3%2, 0 - 1*100] = [1, -100].
`sumAbs` goes from 105 to 203 — it **increases**.

`minNonzeroAbs` is NOT a reliable decreasing measure either.
Counter-example: A = [[2, 1], [3, 0]], t = 0.
After one `clearPass`: [[2, 1], [1, -1]], minNonzeroAbs = 1 = 1 (no decrease).

## Correct proof strategy: idempotency

`clearPass` is idempotent when pivot ≠ 0:
  `clearPass (clearPass A t) t = clearPass A t`
because after one pass, every off-diagonal entry in col t and row t is a residue
with |residue| < |pivot|, so the second pass has factor 0 at every row/col — identity.

This idempotency means: after one `clearPass`, the matrix is a fixed point of
`clearPass`, so `clearLoop_stuck` applies to show both sides of the stability
goal equal `clearPass A t`.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Equation lemmas for clearLoop (avoid simp unfolding recursively)
-- ---------------------------------------------------------------------------

@[simp]
theorem clearLoop_zero (A : IntMatrix) (t : Nat) :
    clearLoop A t 0 = A := rfl

theorem clearLoop_succ (A : IntMatrix) (t k : Nat) :
    clearLoop A t (k + 1) =
    if isCleared A t then A else clearLoop (clearPass A t) t k := rfl

-- ---------------------------------------------------------------------------
-- Minimum nonzero absolute value in A[t:, t:]
-- ---------------------------------------------------------------------------

/-- Minimum |nonzero entry| in the t-submatrix, or 0 if all entries are zero. -/
def minNonzeroAbs (A : IntMatrix) (t : Nat) : Nat :=
  let m := numRows A; let n := numCols A
  (List.range (m - t)).foldl (fun acc i =>
    (List.range (n - t)).foldl (fun acc' j =>
      let v := (entry A (i + t) (j + t)).natAbs
      if v = 0 then acc'
      else match acc' with
        | 0 => v        -- 0 is the "no nonzero seen yet" sentinel
        | b => min v b)
      acc)
    0

-- ---------------------------------------------------------------------------
-- Private helpers for minNonzeroAbs_zero_iff
-- ---------------------------------------------------------------------------

-- Abbreviation for the inner foldl step (transparent for unification)
private abbrev mnaStepFn (A : IntMatrix) (i t : Nat) (acc' j : Nat) : Nat :=
  let v := (entry A (i + t) (j + t)).natAbs
  if v = 0 then acc' else match acc' with | 0 => v | b => min v b

private lemma inner_eq_acc_of_zero (l : List Nat) (A : IntMatrix) (i t acc : Nat)
    (h : ∀ j ∈ l, (entry A (i + t) (j + t)).natAbs = 0) :
    l.foldl (mnaStepFn A i t) acc = acc := by
  induction l generalizing acc with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons, mnaStepFn]
    have hx := h x (List.mem_cons.mpr (Or.inl rfl))
    simp only [hx, ite_true]
    exact ih _ (fun j hj => h j (List.mem_cons.mpr (Or.inr hj)))

private lemma inner_pos_of_pos (l : List Nat) (A : IntMatrix) (i t acc : Nat)
    (hacc : 0 < acc) : 0 < l.foldl (mnaStepFn A i t) acc := by
  induction l generalizing acc with
  | nil => exact hacc
  | cons x xs ih =>
    simp only [List.foldl_cons, mnaStepFn]
    split_ifs with hv
    · exact ih acc hacc
    · cases acc with
      | zero => omega
      | succ b =>
        apply ih
        -- 0 < min v (b+1): both v > 0 (from hv) and b+1 > 0
        simp only [Nat.min_def]; split_ifs with h <;> omega

private lemma inner_pos_of_nonzero (l : List Nat) (A : IntMatrix) (i t j₀ : Nat)
    (hj₀ : j₀ ∈ l) (hv : (entry A (i + t) (j₀ + t)).natAbs ≠ 0) :
    0 < l.foldl (mnaStepFn A i t) 0 := by
  induction l with
  | nil => simp at hj₀
  | cons x xs ih =>
    simp only [List.foldl_cons, mnaStepFn]
    rcases List.mem_cons.mp hj₀ with h_eq | hj₀'
    · -- h_eq : j₀ = x; rewrite hv to use x
      rw [h_eq] at hv
      simp only [if_neg hv]
      exact inner_pos_of_pos xs A i t _ (by omega)
    · -- j₀ ∈ xs
      by_cases hvx : (entry A (i + t) (x + t)).natAbs = 0
      · -- step from 0 gives 0; apply IH
        simp only [hvx, ite_true]
        exact ih hj₀'
      · -- step from 0 gives v_x > 0; inner_pos_of_pos carries it
        simp only [if_neg hvx]
        exact inner_pos_of_pos xs A i t (entry A (i + t) (x + t)).natAbs (by omega)

private lemma outer_pos_of_acc_pos (l : List Nat) (A : IntMatrix) (t n_t acc : Nat)
    (hacc : 0 < acc) :
    0 < l.foldl (fun a i => (List.range n_t).foldl (mnaStepFn A i t) a) acc := by
  induction l generalizing acc with
  | nil => exact hacc
  | cons x xs ih =>
    simp only [List.foldl_cons]
    exact ih _ (inner_pos_of_pos (List.range n_t) A x t acc hacc)

private lemma outer_pos_of_nonzero (l : List Nat) (A : IntMatrix) (t n_t i₀ j₀ : Nat)
    (hi₀ : i₀ ∈ l) (hj₀ : j₀ ∈ List.range n_t)
    (hv : (entry A (i₀ + t) (j₀ + t)).natAbs ≠ 0) :
    0 < l.foldl (fun a i => (List.range n_t).foldl (mnaStepFn A i t) a) 0 := by
  induction l with
  | nil => simp at hi₀
  | cons x xs ih =>
    simp only [List.foldl_cons]
    rcases List.mem_cons.mp hi₀ with rfl | hi₀'
    · exact outer_pos_of_acc_pos xs A t n_t _
        (inner_pos_of_nonzero (List.range n_t) A i₀ t j₀ hj₀ hv)
    · by_cases hx : 0 < (List.range n_t).foldl (mnaStepFn A x t) 0
      · exact outer_pos_of_acc_pos xs A t n_t _ hx
      · push_neg at hx; rw [Nat.le_zero.mp hx]; exact ih hi₀'

private lemma outer_zero_of_all_zero (l : List Nat) (A : IntMatrix) (t n_t : Nat)
    (h : ∀ i' ∈ l, ∀ j' ∈ List.range n_t, (entry A (i' + t) (j' + t)).natAbs = 0) :
    l.foldl (fun a i => (List.range n_t).foldl (mnaStepFn A i t) a) 0 = 0 := by
  induction l with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons]
    rw [inner_eq_acc_of_zero (List.range n_t) A x t 0
        (fun j hj => h x (List.mem_cons.mpr (Or.inl rfl)) j hj)]
    exact ih (fun i' hi' j' hj' => h i' (List.mem_cons.mpr (Or.inr hi')) j' hj')

/-- `minNonzeroAbs = 0` iff every entry in A[t:, t:] is zero.

The well-formedness hypothesis `hwf` (all rows have the same width as the first row) is
needed to handle the case where a wide inner row has a nonzero entry beyond `numCols A`. -/
theorem minNonzeroAbs_zero_iff (A : IntMatrix) (t : Nat)
    (hwf : ∀ i, i < A.length → (A.getD i []).length = numCols A) :
    minNonzeroAbs A t = 0 ↔ ∀ i j, t ≤ i → t ≤ j → entry A i j = 0 := by
  simp only [minNonzeroAbs, numRows, numCols]
  set n_t := (A.head?.map List.length).getD 0 - t
  -- Rewrite the foldl in terms of mnaStepFn for the helpers
  change (List.range (A.length - t)).foldl
      (fun a i => (List.range n_t).foldl (mnaStepFn A i t) a) 0 = 0 ↔
    ∀ i j, t ≤ i → t ≤ j → entry A i j = 0
  constructor
  · intro hfoldl i j hi hj
    by_contra hne
    -- entry A i j ≠ 0 → i < A.length, j < A[i].length
    have hi_lt : i < A.length := by
      by_contra hge; push_neg at hge
      simp [entry, List.getElem?_eq_none_iff.mpr hge] at hne
    have hAt : A[i]? = some A[i] := List.getElem?_eq_getElem hi_lt
    have hj_lt : j < (A[i]).length := by
      by_contra hge; push_neg at hge
      simp [entry, hAt, List.getElem?_eq_none_iff.mpr hge] at hne
    have hv : (entry A i j).natAbs ≠ 0 := by rwa [Ne, Int.natAbs_eq_zero]
    by_cases hj_nc : j < (A.head?.map List.length).getD 0
    · -- j in column range: (i-t, j-t) is in both foldl ranges
      have hi' : i - t ∈ List.range (A.length - t) := List.mem_range.mpr (by omega)
      have hj' : j - t ∈ List.range n_t := List.mem_range.mpr (by simp only [n_t]; omega)
      have hv' : (entry A (i - t + t) (j - t + t)).natAbs ≠ 0 := by
        rwa [Nat.sub_add_cancel hi, Nat.sub_add_cancel hj]
      have hpos := outer_pos_of_nonzero _ A t n_t (i - t) (j - t) hi' hj' hv'
      omega
    · -- Non-rectangular branch: WF says row i has width numCols A, contradicting hj_nc.
      have hwfi := hwf i hi_lt
      -- hwfi : (A.getD i []).length = numCols A
      have hAiD : (A.getD i []).length = (A[i]).length := by
        simp [List.getD, List.getElem?_eq_getElem hi_lt]
      simp only [numCols] at hwfi
      omega
  · intro hall
    apply outer_zero_of_all_zero
    intro i' hi' j' hj'
    simp only [List.mem_range] at hi' hj'
    rw [Int.natAbs_eq_zero]
    exact hall (i' + t) (j' + t) (Nat.le_add_left t i') (Nat.le_add_left t j')

-- ---------------------------------------------------------------------------
-- Stuck loop: clearPass returns A when pivot = 0
-- ---------------------------------------------------------------------------

/-- When `clearPass A t = A` (pivot is zero), the loop is stuck and
    `clearLoop A t k = A` for every fuel `k`. -/
theorem clearLoop_stuck (A : IntMatrix) (t k : Nat)
    (hcp : clearPass A t = A) : clearLoop A t k = A := by
  induction k with
  | zero => simp
  | succ n ih =>
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · rw [hcp, ih]

-- ---------------------------------------------------------------------------
-- clearPass strictly decreases minNonzeroAbs when pivot ≠ 0
-- ---------------------------------------------------------------------------

/-- The pivot entry (t,t) is unchanged by clearPass.

Proof: clearPass does a row-clearing fold (each step is `addRow M t i _` with
`i ≠ t`, so `addRow_entry_unaffected` applies) followed by a col-clearing fold
(each step is `addCol M t j _` with `j ≠ t`, so `addCol_entry_unaffected`
applies).  The two `foldl_*_pres_pivot` helpers from `Elementary.lean` package
this fold induction. -/
theorem clearPass_preserves_pivot (A : IntMatrix) (t : Nat) :
    entry (clearPass A t) t t = entry A t t := by
  simp only [clearPass]
  split_ifs with h
  · rfl
  · rw [foldl_addCol_pres_pivot (List.range (numCols A)) _ t
          (fun M j => -(entry M t j / entry M t t)),
        foldl_addRow_pres_pivot (List.range (numRows A)) A t
          (fun M i => -(entry M i t / entry M t t))]

/-- `clearLoop` does not change the diagonal entry at position (t, t). -/
theorem clearLoop_preserves_pivot (A : IntMatrix) (t k : Nat) :
    entry (clearLoop A t k) t t = entry A t t := by
  induction k generalizing A with
  | zero => simp [clearLoop_zero]
  | succ n ih =>
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · rw [ih (clearPass A t), clearPass_preserves_pivot]

-- Private helpers for clearPass_col_residue / clearPass_row_residue --

private lemma foldl_addCol_pres_col_t (l : List Nat) (A : IntMatrix) (t k : Nat) :
    entry (l.foldl (fun M j => if j = t then M else addCol M t j (-(entry M t j / entry M t t))) A) k t =
    entry A k t := by
  induction l generalizing A with
  | nil => simp
  | cons j js ih =>
    simp only [List.foldl_cons]
    split_ifs with hj
    · exact ih A
    · rw [ih (addCol A t j _), addCol_entry_unaffected A t j k t _ (Ne.symm hj)]

private lemma foldl_addRow_not_mem_row (l : List Nat) (A : IntMatrix) (t i c : Nat)
    (hi : i ∉ l) :
    entry (l.foldl (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A) i c =
    entry A i c := by
  induction l generalizing A with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons]
    simp only [List.mem_cons, not_or] at hi
    obtain ⟨hxi, hxs⟩ := hi
    split_ifs with hxt
    · exact ih A hxs
    · rw [ih (addRow A t x _) hxs, addRow_entry_unaffected A t x i c _ hxi]

/-- After `clearPass`, every off-pivot entry in column t satisfies
    `|entry (clearPass A t) i t| < |entry A t t|` (when pivot ≠ 0, i ≠ t). -/
theorem clearPass_col_residue (A : IntMatrix) (t i : Nat)
    (hi : i ≠ t) (hpivot : entry A t t ≠ 0) :
    (entry (clearPass A t) i t).natAbs < (entry A t t).natAbs := by
  simp only [clearPass, if_neg hpivot]
  rw [foldl_addCol_pres_col_t]
  suffices h : entry ((List.range (numRows A)).foldl
      (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A) i t =
      entry A i t % entry A t t by
    rw [h]
    have hlt := Int.natAbs_lt_natAbs_of_nonneg_of_lt
      (Int.emod_nonneg (entry A i t) hpivot) (Int.emod_lt_abs (entry A i t) hpivot)
    simpa [Int.abs_eq_natAbs] using hlt
  by_cases hmem : i ∈ List.range (numRows A)
  · obtain ⟨lpre, lsuf, hsplit⟩ := List.append_of_mem hmem
    have hnodup : (List.range (numRows A)).Nodup := List.nodup_range
    rw [hsplit] at hnodup
    rw [List.nodup_append'] at hnodup
    obtain ⟨_, hcon_nodup, hdisj⟩ := hnodup
    have hi_not_pre : i ∉ lpre :=
      fun h_pre => (hdisj h_pre) (List.mem_cons.mpr (Or.inl rfl))
    have hi_not_suf : i ∉ lsuf := (List.nodup_cons.mp hcon_nodup).1
    rw [hsplit, List.foldl_append, List.foldl_cons]
    set M_pre := lpre.foldl
        (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A
    have hpre_i : entry M_pre i t = entry A i t :=
      foldl_addRow_not_mem_row lpre A t i t hi_not_pre
    have hpre_t : entry M_pre t t = entry A t t :=
      foldl_addRow_pres_pivot lpre A t (fun M k => -(entry M k t / entry M t t))
    split_ifs with hit
    · exact absurd hit hi
    · rw [foldl_addRow_not_mem_row lsuf _ t i t hi_not_suf,
          addRow_entry_emod M_pre t i, hpre_i, hpre_t]
  · rw [foldl_addRow_not_mem_row _ A t i t hmem]
    have hi_ge : numRows A ≤ i := by rwa [List.mem_range, not_lt] at hmem
    have hi_none : A[i]? = none :=
      List.getElem?_eq_none_iff.mpr (by simpa [numRows] using hi_ge)
    simp [entry, hi_none]

/-- Exact residue value for column t after clearPass:
    `entry (clearPass A t) i t = entry A i t % entry A t t`. -/
lemma clearPass_col_emod (A : IntMatrix) (t i : Nat)
    (hi : i ≠ t) (hpivot : entry A t t ≠ 0) :
    entry (clearPass A t) i t = entry A i t % entry A t t := by
  simp only [clearPass, if_neg hpivot]
  rw [foldl_addCol_pres_col_t]
  by_cases hmem : i ∈ List.range (numRows A)
  · obtain ⟨lpre, lsuf, hsplit⟩ := List.append_of_mem hmem
    have hnodup : (List.range (numRows A)).Nodup := List.nodup_range
    rw [hsplit] at hnodup; rw [List.nodup_append'] at hnodup
    obtain ⟨_, hcon_nodup, hdisj⟩ := hnodup
    have hi_not_pre : i ∉ lpre :=
      fun h_pre => (hdisj h_pre) (List.mem_cons.mpr (Or.inl rfl))
    have hi_not_suf : i ∉ lsuf := (List.nodup_cons.mp hcon_nodup).1
    rw [hsplit, List.foldl_append, List.foldl_cons]
    set M_pre := lpre.foldl
        (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A
    have hpre_i : entry M_pre i t = entry A i t :=
      foldl_addRow_not_mem_row lpre A t i t hi_not_pre
    have hpre_t : entry M_pre t t = entry A t t :=
      foldl_addRow_pres_pivot lpre A t (fun M k => -(entry M k t / entry M t t))
    split_ifs with hit
    · exact absurd hit hi
    · rw [foldl_addRow_not_mem_row lsuf _ t i t hi_not_suf,
          addRow_entry_emod M_pre t i, hpre_i, hpre_t]
  · rw [foldl_addRow_not_mem_row _ A t i t hmem]
    have hi_ge : numRows A ≤ i := by rwa [List.mem_range, not_lt] at hmem
    have hi_none : A[i]? = none :=
      List.getElem?_eq_none_iff.mpr (by simpa [numRows] using hi_ge)
    simp [entry, hi_none]

private lemma foldl_addRow_pres_row_t (l : List Nat) (A : IntMatrix) (t c : Nat) :
    entry (l.foldl (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A) t c =
    entry A t c := by
  induction l generalizing A with
  | nil => simp
  | cons k ks ih =>
    simp only [List.foldl_cons]
    split_ifs with hkt
    · exact ih A
    · rw [ih (addRow A t k _), addRow_entry_unaffected A t k t c _ (Ne.symm hkt)]

private lemma foldl_addCol_not_mem_col (l : List Nat) (A : IntMatrix) (t r c : Nat)
    (hc : c ∉ l) :
    entry (l.foldl (fun M j => if j = t then M else addCol M t j (-(entry M t j / entry M t t))) A) r c =
    entry A r c := by
  induction l generalizing A with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons]
    simp only [List.mem_cons, not_or] at hc
    obtain ⟨hxc, hxs⟩ := hc
    split_ifs with hxt
    · exact ih A hxs
    · rw [ih (addCol A t x _) hxs, addCol_entry_unaffected A t x r c _ hxc]

/-- After `clearPass`, every off-pivot entry in row t satisfies
    `|entry (clearPass A t) t j| < |entry A t t|` (when pivot ≠ 0, j ≠ t, j in column range). -/
theorem clearPass_row_residue (A : IntMatrix) (t j : Nat)
    (hj : j ≠ t) (hpivot : entry A t t ≠ 0)
    (hbound : j ∈ List.range (numCols A)) :
    (entry (clearPass A t) t j).natAbs < (entry A t t).natAbs := by
  simp only [clearPass, if_neg hpivot]
  set A₁ := (List.range (numRows A)).foldl
      (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A
  have hA₁_tj : entry A₁ t j = entry A t j := foldl_addRow_pres_row_t _ A t j
  have hA₁_tt : entry A₁ t t = entry A t t := foldl_addRow_pres_row_t _ A t t
  suffices h : entry ((List.range (numCols A)).foldl
      (fun M j' => if j' = t then M else addCol M t j' (-(entry M t j' / entry M t t))) A₁) t j =
      entry A t j % entry A t t by
    rw [h]
    have hlt := Int.natAbs_lt_natAbs_of_nonneg_of_lt
      (Int.emod_nonneg (entry A t j) hpivot) (Int.emod_lt_abs (entry A t j) hpivot)
    simpa [Int.abs_eq_natAbs] using hlt
  rw [← hA₁_tj, ← hA₁_tt]
  obtain ⟨lpre, lsuf, hsplit⟩ := List.append_of_mem hbound
  have hnodup : (List.range (numCols A)).Nodup := List.nodup_range
  rw [hsplit] at hnodup
  rw [List.nodup_append'] at hnodup
  obtain ⟨_, hcon_nodup, hdisj⟩ := hnodup
  have hj_not_pre : j ∉ lpre :=
    fun h_pre => (hdisj h_pre) (List.mem_cons.mpr (Or.inl rfl))
  have hj_not_suf : j ∉ lsuf := (List.nodup_cons.mp hcon_nodup).1
  rw [hsplit, List.foldl_append, List.foldl_cons]
  set M_pre := lpre.foldl
      (fun M j' => if j' = t then M else addCol M t j' (-(entry M t j' / entry M t t))) A₁
  have hpre_j : entry M_pre t j = entry A₁ t j :=
    foldl_addCol_not_mem_col lpre A₁ t t j hj_not_pre
  have hpre_t : entry M_pre t t = entry A₁ t t :=
    foldl_addCol_pres_col_t lpre A₁ t t
  split_ifs with hjt
  · exact absurd hjt hj
  · rw [foldl_addCol_not_mem_col lsuf _ t t j hj_not_suf,
        addCol_entry_emod M_pre t j, hpre_j, hpre_t]

/-- Exact residue value for row t after clearPass:
    `entry (clearPass A t) t j = entry A t j % entry A t t`. -/
private lemma clearPass_row_emod (A : IntMatrix) (t j : Nat)
    (hj : j ≠ t) (hpivot : entry A t t ≠ 0)
    (hbound : j ∈ List.range (numCols A)) :
    entry (clearPass A t) t j = entry A t j % entry A t t := by
  simp only [clearPass, if_neg hpivot]
  set A₁ := (List.range (numRows A)).foldl
      (fun M k => if k = t then M else addRow M t k (-(entry M k t / entry M t t))) A
  have hA₁_tj : entry A₁ t j = entry A t j := foldl_addRow_pres_row_t _ A t j
  have hA₁_tt : entry A₁ t t = entry A t t := foldl_addRow_pres_row_t _ A t t
  rw [← hA₁_tj, ← hA₁_tt]
  obtain ⟨lpre, lsuf, hsplit⟩ := List.append_of_mem hbound
  have hnodup : (List.range (numCols A)).Nodup := List.nodup_range
  rw [hsplit] at hnodup; rw [List.nodup_append'] at hnodup
  obtain ⟨_, hcon_nodup, hdisj⟩ := hnodup
  have hj_not_pre : j ∉ lpre :=
    fun h_pre => (hdisj h_pre) (List.mem_cons.mpr (Or.inl rfl))
  have hj_not_suf : j ∉ lsuf := (List.nodup_cons.mp hcon_nodup).1
  rw [hsplit, List.foldl_append, List.foldl_cons]
  set M_pre := lpre.foldl
      (fun M j' => if j' = t then M else addCol M t j' (-(entry M t j' / entry M t t))) A₁
  have hpre_j : entry M_pre t j = entry A₁ t j :=
    foldl_addCol_not_mem_col lpre A₁ t t j hj_not_pre
  have hpre_t : entry M_pre t t = entry A₁ t t :=
    foldl_addCol_pres_col_t lpre A₁ t t
  split_ifs with hjt
  · exact absurd hjt hj
  · rw [foldl_addCol_not_mem_col lsuf _ t t j hj_not_suf,
        addCol_entry_emod M_pre t j, hpre_j, hpre_t]

-- ---------------------------------------------------------------------------
-- Helpers for clearPass_idempotent
-- ---------------------------------------------------------------------------

private lemma list_mapIdx_id {α : Type*} (l : List α) :
    l.mapIdx (fun _ x => x) = l := by
  induction l with
  | nil => rfl
  | cons a as ih => simp [List.mapIdx_cons, ih]

private lemma addRow_zero (A : IntMatrix) (src dst : Nat) :
    addRow A src dst 0 = A := by
  simp only [addRow]
  -- After unfolding addRow, `let srcRow` is zeta-reduced by simp, so goal has getD directly.
  have key : ∀ (k : Nat) (row : List Int),
      (if k = dst then
        row.mapIdx (fun c x => x + (0 : Int) * (A.getD src []).getD c 0)
       else row) = row := by
    intro k row
    split_ifs
    · have step : ∀ c (x : Int), x + (0 : Int) * (A.getD src []).getD c 0 = x := by
        intro c x; omega
      simp_rw [step]
      exact list_mapIdx_id row
    · rfl
  simp_rw [key]
  exact list_mapIdx_id A

private lemma addCol_zero (A : IntMatrix) (src dst : Nat) :
    addCol A src dst 0 = A := by
  simp only [addCol]
  have key : ∀ (row : List Int),
      row.mapIdx (fun k x => if k = dst then x + (0 : Int) * row.getD src 0 else x) = row := by
    intro row
    have step : ∀ k (x : Int), (if k = dst then x + (0 : Int) * row.getD src 0 else x) = x := by
      intro k x
      split_ifs
      · omega
      · rfl
    simp_rw [step]
    exact list_mapIdx_id row
  simp_rw [key]
  exact List.map_id A

/-- `0 ≤ a` and `a.natAbs < b.natAbs` imply `a / b = 0` (Euclidean division). -/
private lemma int_ediv_zero_of_nonneg_natAbs_lt {a b : Int} (hb : b ≠ 0)
    (h1 : 0 ≤ a) (h2 : a.natAbs < b.natAbs) : a / b = 0 := by
  have h2' : a < (b.natAbs : Int) :=
    calc a = (a.natAbs : Int) := (Int.natAbs_of_nonneg h1).symm
         _ < (b.natAbs : Int) := by exact_mod_cast h2
  rcases Int.lt_or_gt_of_ne hb with hb_neg | hb_pos
  · -- b < 0: write b = -(-b) and use Int.ediv_neg
    have hb_natAbs : (b.natAbs : Int) = -b := by
      conv_lhs => rw [show b.natAbs = (-b).natAbs from (Int.natAbs_neg b).symm]
      exact Int.natAbs_of_nonneg (le_of_lt (Int.neg_pos.mpr hb_neg))
    rw [hb_natAbs] at h2'
    -- h2' : a < -b  (and -b > 0)
    rw [show b = -(-b) from (neg_neg b).symm, Int.ediv_neg]
    simp [Int.ediv_eq_zero_of_lt h1 h2']
  · -- b > 0
    have hb_natAbs : (b.natAbs : Int) = b :=
      Int.natAbs_of_nonneg (le_of_lt hb_pos)
    rw [hb_natAbs] at h2'
    exact Int.ediv_eq_zero_of_lt h1 h2'

-- numCols is preserved by addRow, addCol, and clearPass

private lemma numCols_addRow (A : IntMatrix) (src dst : Nat) (f : Int) :
    numCols (addRow A src dst f) = numCols A := by
  cases A with
  | nil => simp [numCols, addRow]
  | cons row rows =>
    simp only [numCols, addRow, List.mapIdx_cons, List.head?_cons, Option.map_some]
    split_ifs <;> simp [List.length_mapIdx]

private lemma numCols_addCol (A : IntMatrix) (src dst : Nat) (f : Int) :
    numCols (addCol A src dst f) = numCols A := by
  cases A with
  | nil => simp [numCols, addCol]
  | cons row rows => simp [numCols, addCol, List.length_mapIdx]

private lemma numCols_clearPass (A : IntMatrix) (t : Nat) :
    numCols (clearPass A t) = numCols A := by
  simp only [clearPass]
  split_ifs with h
  · rfl
  · have hrp : ∀ (l : List Nat) (M : IntMatrix),
        numCols (l.foldl
            (fun N i => if i = t then N else addRow N t i (-(entry N i t / entry N t t))) M) =
        numCols M := by
      intro l M; induction l generalizing M with
      | nil => simp
      | cons k ks ih =>
        simp only [List.foldl_cons]
        split_ifs <;> [exact ih M; rw [ih, numCols_addRow]]
    have hcp : ∀ (l : List Nat) (M : IntMatrix),
        numCols (l.foldl
            (fun N j => if j = t then N else addCol N t j (-(entry N t j / entry N t t))) M) =
        numCols M := by
      intro l M; induction l generalizing M with
      | nil => simp
      | cons k ks ih =>
        simp only [List.foldl_cons]
        split_ifs <;> [exact ih M; rw [ih, numCols_addCol]]
    rw [hcp, hrp]

/-- When all row factors are zero the row-phase foldl is the identity. -/
private lemma foldl_addRow_identity (l : List Nat) (A : IntMatrix) (t : Nat)
    (hf : ∀ i ∈ l, i ≠ t → entry A i t / entry A t t = 0) :
    l.foldl (fun M i => if i = t then M else addRow M t i (-(entry M i t / entry M t t))) A = A := by
  induction l generalizing A with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons]
    by_cases hxt : x = t
    · simp only [hxt, ite_true]
      exact ih A (fun i hi hit => hf i (List.mem_cons.mpr (Or.inr hi)) hit)
    · simp only [if_neg hxt]
      have hfac : -(entry A x t / entry A t t) = 0 := by
        rw [hf x (List.mem_cons.mpr (Or.inl rfl)) hxt, neg_zero]
      rw [hfac, addRow_zero]
      exact ih A (fun i hi hit => hf i (List.mem_cons.mpr (Or.inr hi)) hit)

/-- When all col factors are zero the col-phase foldl is the identity. -/
private lemma foldl_addCol_identity (l : List Nat) (A : IntMatrix) (t : Nat)
    (hf : ∀ j ∈ l, j ≠ t → entry A t j / entry A t t = 0) :
    l.foldl (fun M j => if j = t then M else addCol M t j (-(entry M t j / entry M t t))) A = A := by
  induction l generalizing A with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons]
    by_cases hxt : x = t
    · simp only [hxt, ite_true]
      exact ih A (fun j hj hjt => hf j (List.mem_cons.mpr (Or.inr hj)) hjt)
    · simp only [if_neg hxt]
      have hfac : -(entry A t x / entry A t t) = 0 := by
        rw [hf x (List.mem_cons.mpr (Or.inl rfl)) hxt, neg_zero]
      rw [hfac, addCol_zero]
      exact ih A (fun j hj hjt => hf j (List.mem_cons.mpr (Or.inr hj)) hjt)

/-- `clearPass` is idempotent when pivot ≠ 0:
    `clearPass (clearPass A t) t = clearPass A t`. -/
theorem clearPass_idempotent (A : IntMatrix) (t : Nat)
    (hpivot : entry A t t ≠ 0) :
    clearPass (clearPass A t) t = clearPass A t := by
  set B := clearPass A t with hB_def
  have hBtt : entry B t t = entry A t t := clearPass_preserves_pivot A t
  have hBpiv : entry B t t ≠ 0 := hBtt ▸ hpivot
  simp only [clearPass, if_neg hBpiv]
  -- Row phase on B is identity: each factor is 0
  have hrow : (List.range (numRows B)).foldl (fun M i =>
      if i = t then M else addRow M t i (-(entry M i t / entry M t t))) B = B := by
    apply foldl_addRow_identity
    intro i _hmem hit
    have h_nn : 0 ≤ entry B i t := by
      rw [clearPass_col_emod A t i hit hpivot]
      exact Int.emod_nonneg (entry A i t) hpivot
    have h_lt : (entry B i t).natAbs < (entry B t t).natAbs := by
      rw [hBtt]; exact clearPass_col_residue A t i hit hpivot
    exact int_ediv_zero_of_nonneg_natAbs_lt hBpiv h_nn h_lt
  rw [hrow]
  -- Col phase on B is identity: each factor is 0
  -- numCols B = numCols A so the col-phase range matches clearPass_row_emod
  have hBnCols : numCols B = numCols A := numCols_clearPass A t
  apply foldl_addCol_identity
  intro j hmem hjt
  have hmemA : j ∈ List.range (numCols A) := hBnCols ▸ hmem
  have h_nn : 0 ≤ entry B t j := by
    rw [clearPass_row_emod A t j hjt hpivot hmemA]
    exact Int.emod_nonneg (entry A t j) hpivot
  have h_lt : (entry B t j).natAbs < (entry B t t).natAbs := by
    rw [hBtt]; exact clearPass_row_residue A t j hjt hpivot hmemA
  exact int_ediv_zero_of_nonneg_natAbs_lt hBpiv h_nn h_lt

-- ---------------------------------------------------------------------------
-- Main theorem: clearLoop stabilises once fuel ≥ minNonzeroAbs
-- ---------------------------------------------------------------------------

/-- `clearLoop A t k` equals `clearLoop A t (k + 1)` whenever `k ≥ minNonzeroAbs A t`.

Proof by induction on `k`:

**Base case (k = 0, so minNonzeroAbs A t = 0):**
All submatrix entries are zero, so in particular `entry A t t = 0`,
so `clearPass A t = A`.  Then `clearLoop_stuck` shows both sides equal `A`.

**Inductive step (k = n + 1):**
- If `isCleared A t`: both sides immediately return `A`.
- Otherwise, show `clearPass (clearPass A t) t = clearPass A t`:
  - If `entry A t t = 0`: `clearPass A t = A`; so `clearPass (clearPass A t) t = A = clearPass A t`. ✓
  - If `entry A t t ≠ 0`: `clearPass_idempotent` gives the result directly. ✓
  Apply `clearLoop_stuck` to `clearPass A t` to conclude both sides of the goal
  equal `clearPass A t`. -/
theorem clearLoop_stable (A : IntMatrix) (t k : Nat)
    (hwf : ∀ i, i < A.length → (A.getD i []).length = numCols A)
    (hk : minNonzeroAbs A t ≤ k) :
    clearLoop A t k = clearLoop A t (k + 1) := by
  induction k generalizing A with
  | zero =>
    have hm   : minNonzeroAbs A t = 0 := Nat.le_zero.mp hk
    have hpiv : entry A t t = 0 :=
      (minNonzeroAbs_zero_iff A t hwf).mp hm t t le_rfl le_rfl
    have hcp  : clearPass A t = A := by unfold clearPass; simp [hpiv]
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · rw [hcp, clearLoop_zero]
  | succ n _ih =>
    rw [clearLoop_succ, clearLoop_succ]
    split_ifs with hc
    · rfl
    · -- ¬isCleared A t
      -- show clearPass (clearPass A t) t = clearPass A t, then use clearLoop_stuck
      have hcpB : clearPass (clearPass A t) t = clearPass A t := by
        by_cases hpiv : entry A t t = 0
        · have hcp : clearPass A t = A := by unfold clearPass; simp [hpiv]
          rw [hcp, hcp]
        · exact clearPass_idempotent A t hpiv
      exact (clearLoop_stuck _ _ _ hcpB).trans (clearLoop_stuck _ _ _ hcpB).symm

-- ---------------------------------------------------------------------------
-- clearPass fixed-point and column bound lemmas
-- ---------------------------------------------------------------------------

/-- When `isCleared A t`, `clearPass A t = A` (all factors are 0). -/
private lemma clearPass_of_isCleared (A : IntMatrix) (t : Nat)
    (hcl : isCleared A t = true) :
    clearPass A t = A := by
  unfold clearPass
  by_cases hpivot : entry A t t = 0
  · simp [hpivot]
  · simp only [hpivot, ite_false]
    simp only [isCleared, Bool.and_eq_true, List.all_eq_true] at hcl
    obtain ⟨hcol_all, hrow_all⟩ := hcl
    have hrow_id : (List.range (numRows A)).foldl (fun M i =>
        if i = t then M else addRow M t i (-(entry M i t / entry M t t))) A = A := by
      apply foldl_addRow_identity
      intro i hmem hit
      have hcheck := hcol_all i hmem
      simp only [Bool.or_eq_true, decide_eq_true_eq] at hcheck
      rcases hcheck with rfl | h
      · exact absurd rfl hit
      · simp [h]
    rw [hrow_id]
    apply foldl_addCol_identity
    intro j hmem hjt
    have hcheck := hrow_all j hmem
    simp only [Bool.or_eq_true, decide_eq_true_eq] at hcheck
    rcases hcheck with rfl | h
    · exact absurd rfl hjt
    · simp [h]

/-- If `clearPass B t = B`, then `clearLoop B t k = B` for any fuel. -/
private lemma clearLoop_idempotent_base (B : IntMatrix) (t k : Nat)
    (hfix : clearPass B t = B) :
    clearLoop B t k = B := by
  induction k with
  | zero => simp [clearLoop_zero]
  | succ n ih =>
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · rw [hfix, ih]

/-- With fuel `k + 1`, the column-t entry of `clearLoop A t` equals that of `clearPass A t`. -/
lemma clearLoop_col_t_of_succ (A : IntMatrix) (t k i : Nat)
    (hpivot : entry A t t ≠ 0) :
    entry (clearLoop A t (k + 1)) i t = entry (clearPass A t) i t := by
  rw [clearLoop_succ]
  split_ifs with hc
  · rw [clearPass_of_isCleared A t hc]
  · rw [clearLoop_idempotent_base (clearPass A t) t k (clearPass_idempotent A t hpivot)]

/-- With fuel ≥ 1, column-t entries of `clearLoop A t` are strictly bounded by the pivot. -/
lemma clearLoop_col_lt_pivot (A : IntMatrix) (t i innerFuel : Nat)
    (hpivot : entry A t t ≠ 0) (hit : i ≠ t) (hfuel : 1 ≤ innerFuel) :
    (entry (clearLoop A t innerFuel) i t).natAbs < (entry (clearLoop A t innerFuel) t t).natAbs := by
  obtain ⟨k, rfl⟩ : ∃ k, innerFuel = k + 1 := ⟨innerFuel - 1, by omega⟩
  rw [clearLoop_col_t_of_succ A t k i hpivot, clearLoop_preserves_pivot]
  exact clearPass_col_residue A t i hit hpivot

end PytopSNF
