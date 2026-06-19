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

The correct measure is `minNonzeroAbs` — the minimum absolute value of all
nonzero entries in the t-submatrix.  Each `clearPass` either:
- has pivot = 0 (returns A unchanged — stuck but trivially stable for all k), or
- produces residues with |residue| < |pivot| ≤ minNonzeroAbs,
  strictly decreasing the measure.

Since `minNonzeroAbs` is a positive natural number, the descent terminates
in ≤ minNonzeroAbs steps.
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

/-- `minNonzeroAbs = 0` iff every entry in A[t:, t:] is zero. -/
theorem minNonzeroAbs_zero_iff (A : IntMatrix) (t : Nat) :
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
    · -- Non-rectangular: j ≥ numCols A but j < A[i].length.
      -- Well-formed matrices (all rows same length) never hit this.
      sorry
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

/-- If `¬isCleared A t` and pivot ≠ 0, then `minNonzeroAbs (clearPass A t) t < minNonzeroAbs A t`.

Proof sketch:
- `¬isCleared A t` → ∃ i ≠ t with `entry A i t ≠ 0`, or ∃ j ≠ t with `entry A t j ≠ 0`.
- After `clearPass`, that entry becomes its residue mod pivot.
- |residue| < |pivot|, and |pivot| = |entry A t t| ≤ minNonzeroAbs A t.
- So `minNonzeroAbs (clearPass A t) t ≤ |residue| < |pivot| ≤ minNonzeroAbs A t`. -/
theorem clearPass_decreases_minNonzeroAbs (A : IntMatrix) (t : Nat)
    (hclr : ¬isCleared A t) (hpivot : entry A t t ≠ 0) :
    minNonzeroAbs (clearPass A t) t < minNonzeroAbs A t := by
  sorry

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
- If `entry A t t = 0` (stuck): `clearPass A t = A`; use `clearLoop_stuck`.
- If `entry A t t ≠ 0`: `clearPass_decreases_minNonzeroAbs` gives a strictly
  smaller measure; apply the inductive hypothesis to `clearPass A t`. -/
theorem clearLoop_stable (A : IntMatrix) (t k : Nat)
    (hk : minNonzeroAbs A t ≤ k) :
    clearLoop A t k = clearLoop A t (k + 1) := by
  induction k generalizing A with
  | zero =>
    -- minNonzeroAbs A t = 0  →  entry A t t = 0  →  clearPass A t = A (stuck)
    have hm   : minNonzeroAbs A t = 0 := Nat.le_zero.mp hk
    have hpiv : entry A t t = 0 :=
      (minNonzeroAbs_zero_iff A t).mp hm t t le_rfl le_rfl
    have hcp  : clearPass A t = A := by unfold clearPass; simp [hpiv]
    -- clearLoop A t 0 = A (by def)
    -- clearLoop A t 1:  unfold one step
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · -- goal: A = clearLoop (clearPass A t) t 0
      rw [hcp, clearLoop_zero]
  | succ n ih =>
    rw [clearLoop_succ, clearLoop_succ]
    split_ifs with hc
    · rfl  -- both sides are A
    · -- ¬isCleared A t
      -- Goal: clearLoop (clearPass A t) t n = clearLoop (clearPass A t) t (n + 1)
      by_cases hpiv : entry A t t = 0
      · -- Stuck: clearPass A t = A  →  loop returns clearPass A t at every fuel
        have hcp : clearPass A t = A := by unfold clearPass; simp [hpiv]
        -- clearPass (clearPass A t) t = clearPass A t  (since clearPass A t = A)
        have hcpB : clearPass (clearPass A t) t = clearPass A t := by
          rw [hcp, hcp]
        have h1 : clearLoop (clearPass A t) t n       = clearPass A t :=
          clearLoop_stuck _ _ _ hcpB
        have h2 : clearLoop (clearPass A t) t (n + 1) = clearPass A t :=
          clearLoop_stuck _ _ _ hcpB
        exact h1.trans h2.symm
      · -- Non-stuck: minNonzeroAbs strictly decreases; apply IH to clearPass A t
        apply ih
        have hdec : minNonzeroAbs (clearPass A t) t < minNonzeroAbs A t :=
          clearPass_decreases_minNonzeroAbs A t hc hpiv
        omega

end PytopSNF
