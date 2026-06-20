import Formal.SNF.Defs
import Mathlib.Data.List.Basic
import Mathlib.Data.Int.Basic

/-!
# Elementary Row/Column Operations

Defines the four elementary operations used by the SNF algorithm and proves
their entry-level properties.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Definitions
-- ---------------------------------------------------------------------------

/-- Swap rows i and j (0-indexed). -/
def swapRows (A : IntMatrix) (i j : Nat) : IntMatrix :=
  A.mapIdx fun k row =>
    if k = i then A.getD j row
    else if k = j then A.getD i row
    else row

/-- Add `factor * row[src]` to row `dst`. -/
def addRow (A : IntMatrix) (src dst : Nat) (factor : Int) : IntMatrix :=
  A.mapIdx fun k row =>
    if k = dst then
      let srcRow := A.getD src []
      row.mapIdx fun c x => x + factor * srcRow.getD c 0
    else row

/-- Swap columns i and j. -/
def swapCols (A : IntMatrix) (i j : Nat) : IntMatrix :=
  A.map fun row =>
    row.mapIdx fun k x =>
      if k = i then row.getD j x
      else if k = j then row.getD i x
      else x

/-- Add `factor * col[src]` to column `dst`. -/
def addCol (A : IntMatrix) (src dst : Nat) (factor : Int) : IntMatrix :=
  A.map fun row =>
    row.mapIdx fun k x =>
      if k = dst then x + factor * row.getD src 0
      else x

-- ---------------------------------------------------------------------------
-- Dimension preservation
-- ---------------------------------------------------------------------------

@[simp] theorem swapRows_numRows (A : IntMatrix) (i j : Nat) :
    numRows (swapRows A i j) = numRows A := by simp [swapRows, numRows]

@[simp] theorem addRow_numRows (A : IntMatrix) (src dst : Nat) (factor : Int) :
    numRows (addRow A src dst factor) = numRows A := by simp [addRow, numRows]

@[simp] theorem swapCols_numRows (A : IntMatrix) (i j : Nat) :
    numRows (swapCols A i j) = numRows A := by simp [swapCols, numRows]

@[simp] theorem addCol_numRows (A : IntMatrix) (src dst : Nat) (factor : Int) :
    numRows (addCol A src dst factor) = numRows A := by simp [addCol, numRows]

-- ---------------------------------------------------------------------------
-- Private helpers
-- ---------------------------------------------------------------------------

/-- `(l.mapIdx f)[k]? = l[k]?.map (f k)`. -/
private theorem mapIdx_getElem? {α β : Type*}
    (l : List α) (f : ℕ → α → β) (k : ℕ) :
    (l.mapIdx f)[k]? = l[k]?.map (f k) := by
  induction l generalizing k f with
  | nil => simp
  | cons head tail ih =>
    rw [List.mapIdx_cons]
    cases k with
    | zero => simp
    | succ n =>
      simp only [List.getElem?_cons_succ]
      exact ih (f ∘ Nat.succ) n

/-- `(A.getD i []).getD j 0 = entry A i j`.

Proved by relating `List.getD` to `Option.getD` via `simp [List.getD]`. -/
private theorem getD_eq_entry (A : IntMatrix) (i j : Nat) :
    (A.getD i []).getD j 0 = entry A i j := by
  simp only [entry]
  -- List.getD A i [] = (A[i]?).getD []  (by simp [List.getD])
  rw [show A.getD i [] = (A[i]?).getD [] from by simp [List.getD]]
  cases A[i]? with
  | none => simp
  | some row => simp [List.getD]

-- ---------------------------------------------------------------------------
-- Core entry lemmas
-- ---------------------------------------------------------------------------

/-- `addRow` leaves every row except `dst` unchanged. -/
theorem addRow_entry_unaffected (A : IntMatrix) (src dst k c : Nat) (factor : Int)
    (hk : k ≠ dst) :
    entry (addRow A src dst factor) k c = entry A k c := by
  simp only [entry, addRow, mapIdx_getElem?, if_neg hk, Option.map_id']

/-- `addCol` leaves every column except `dst` unchanged. -/
theorem addCol_entry_unaffected (A : IntMatrix) (src dst k c : Nat) (factor : Int)
    (hc : c ≠ dst) :
    entry (addCol A src dst factor) k c = entry A k c := by
  simp only [entry, addCol, List.getElem?_map]
  cases A[k]? with
  | none => simp
  | some r => simp [if_neg hc]

/-- `addRow` at (dst, c) satisfies the expected additive formula.
    The out-of-bounds case (c past end of row dst) is sorry'd. -/
theorem addRow_entry_dst (A : IntMatrix) (src dst c : Nat) (factor : Int)
    (hdst : dst < numRows A) (hc : c < (A.getD dst []).length) :
    entry (addRow A src dst factor) dst c =
    entry A dst c + factor * entry A src c := by
  have hdst' : dst < A.length := hdst
  have hAi  : A[dst]? = some A[dst]  := List.getElem?_eq_getElem hdst'
  have hgetd : A.getD dst [] = A[dst] := by simp [List.getD, hAi]
  have hc'  : c < A[dst].length      := hgetd ▸ hc
  have hrow : A[dst][c]? = some A[dst][c] := List.getElem?_eq_getElem hc'
  have hlhs : entry (addRow A src dst factor) dst c =
              A[dst][c] + factor * (A.getD src []).getD c 0 := by
    simp [entry, addRow, mapIdx_getElem?, hAi, hrow, show dst = dst from rfl]
  have hrhs : entry A dst c = A[dst][c] := by simp [entry, hAi, hrow]
  rw [hlhs, hrhs]; congr 1; congr 1
  exact getD_eq_entry A src c

/-- `addCol` at (k, dst) satisfies the expected additive formula.
    The out-of-bounds case is sorry'd. -/
theorem addCol_entry_dst (A : IntMatrix) (src dst k : Nat) (factor : Int)
    (hk : k < numRows A) (hdst : dst < (A.getD k []).length) :
    entry (addCol A src dst factor) k dst =
    entry A k dst + factor * entry A k src := by
  have hk'  : k < A.length                := hk
  have hAk  : A[k]? = some A[k]           := List.getElem?_eq_getElem hk'
  have hgetd : A.getD k [] = A[k]         := by simp [List.getD, hAk]
  have hdst' : dst < A[k].length          := hgetd ▸ hdst
  have hcol : A[k][dst]? = some A[k][dst] := List.getElem?_eq_getElem hdst'
  have hlhs : entry (addCol A src dst factor) k dst =
              A[k][dst] + factor * A[k].getD src 0 := by
    simp [entry, addCol, List.getElem?_map, mapIdx_getElem?, hAk, hcol,
          show dst = dst from rfl]
  have hrhs : entry A k dst = A[k][dst] := by simp [entry, hAk, hcol]
  have hsrc : entry A k src = A[k].getD src 0 := by
    simp only [entry, hAk, Option.map_some]; simp [List.getD]
  rw [hlhs, hrhs, ← hsrc]

/-- Swapping rows i↔j places old row j at position i (requires both in bounds). -/
theorem swapRows_entry_i (A : IntMatrix) (i j c : Nat)
    (hi : i < numRows A) (hj : j < numRows A) :
    entry (swapRows A i j) i c = entry A j c := by
  have hi' : i < A.length := hi
  have hj' : j < A.length := hj
  simp only [entry, swapRows, mapIdx_getElem?]
  rw [List.getElem?_eq_getElem hi']
  simp only [Option.map_some, if_true]
  -- goal: (some (A.getD j A[i])).bind (·[c]?)).getD 0 = entry A j c
  rw [show A.getD j A[i] = A[j] from by
        simp [List.getD, List.getElem?_eq_getElem hj']]
  simp [List.getElem?_eq_getElem hj']

/-- Swapping rows i↔j leaves row k unchanged when k ≠ i and k ≠ j. -/
theorem swapRows_entry_ne (A : IntMatrix) (i j k c : Nat)
    (hki : k ≠ i) (hkj : k ≠ j) :
    entry (swapRows A i j) k c = entry A k c := by
  simp only [entry, swapRows, mapIdx_getElem?]
  cases A[k]? with
  | none => simp
  | some row => simp only [Option.map_some, Option.bind_some, if_neg hki, if_neg hkj]

-- ---------------------------------------------------------------------------
-- Fold-invariant helpers (used by clearPass_preserves_pivot in Termination.lean)
-- ---------------------------------------------------------------------------

/-- A foldl row-clearing loop preserves `entry _ t t`. -/
theorem foldl_addRow_pres_pivot (l : List Nat)
    (A : IntMatrix) (t : Nat)
    (f : IntMatrix → Nat → Int) :
    entry (l.foldl (fun M i =>
        if i = t then M else addRow M t i (f M i)) A) t t =
    entry A t t := by
  induction l generalizing A with
  | nil => simp
  | cons i is ih =>
    simp only [List.foldl_cons]
    split_ifs with hi
    · exact ih A
    · rw [ih (addRow A t i (f A i)),
          addRow_entry_unaffected A t i t t (f A i) (Ne.symm hi)]

/-- A foldl col-clearing loop preserves `entry _ t t`. -/
theorem foldl_addCol_pres_pivot (l : List Nat)
    (A : IntMatrix) (t : Nat)
    (f : IntMatrix → Nat → Int) :
    entry (l.foldl (fun M j =>
        if j = t then M else addCol M t j (f M j)) A) t t =
    entry A t t := by
  induction l generalizing A with
  | nil => simp
  | cons j js ih =>
    simp only [List.foldl_cons]
    split_ifs with hj
    · exact ih A
    · rw [ih (addCol A t j (f A j)),
          addCol_entry_unaffected A t j t t (f A j) (Ne.symm hj)]

/-- After applying the clearPass row-clearing factor, the (i, t) entry equals
    `entry A i t % entry A t t`. Works unconditionally (out-of-bounds → 0 on both sides). -/
theorem addRow_entry_emod (A : IntMatrix) (t i : Nat) :
    entry (addRow A t i (-(entry A i t / entry A t t))) i t =
    entry A i t % entry A t t := by
  by_cases h_i : i < numRows A
  · by_cases h_t : t < (A.getD i []).length
    · -- in-bounds: addRow_entry_dst + explicit rewrite chain (ring fails on Int ediv)
      rw [addRow_entry_dst A t i t _ h_i h_t, Int.emod_def, Int.neg_mul,
          ← Int.sub_eq_add_neg, mul_comm (entry A i t / entry A t t)]
    · -- column t out of bounds for row i: both sides are 0
      simp only [not_lt] at h_t
      have hi' : i < A.length := h_i
      have hrow_eq : A.getD i [] = A[i] :=
        by simp [List.getD, List.getElem?_eq_getElem hi']
      have ht_nn : A[i].length ≤ t := hrow_eq ▸ h_t
      have hentry : entry A i t = 0 := by
        simp only [entry, List.getElem?_eq_getElem hi', Option.bind_some,
                   List.getElem?_eq_none_iff.mpr ht_nn, Option.getD_none]
      simp only [hentry, Int.zero_ediv, neg_zero, Int.zero_emod]
      simp only [entry, addRow, mapIdx_getElem?, List.getElem?_eq_getElem hi',
                 Option.map_some, Option.bind_some, eq_self_iff_true, if_true,
                 mapIdx_getElem?]
      rw [List.getElem?_eq_none_iff.mpr ht_nn]
      simp
  · -- row i out of bounds: both sides are 0
    simp only [not_lt] at h_i
    have hi_ge : A.length ≤ i := by simpa [numRows] using h_i
    have hi_none : A[i]? = none := List.getElem?_eq_none_iff.mpr hi_ge
    have hentry : entry A i t = 0 := by simp [entry, hi_none]
    simp only [hentry, Int.zero_ediv, neg_zero, Int.zero_emod]
    simp [entry, addRow, mapIdx_getElem?, hi_none]

/-- After applying the clearPass col-clearing factor, the (t, j) entry equals
    `entry A t j % entry A t t`. Works unconditionally (out-of-bounds → 0 on both sides). -/
theorem addCol_entry_emod (A : IntMatrix) (t j : Nat) :
    entry (addCol A t j (-(entry A t j / entry A t t))) t j =
    entry A t j % entry A t t := by
  by_cases h_t : t < numRows A
  · by_cases h_j : j < (A.getD t []).length
    · rw [addCol_entry_dst A t j t _ h_t h_j, Int.emod_def, Int.neg_mul,
          ← Int.sub_eq_add_neg, mul_comm (entry A t j / entry A t t)]
    · simp only [not_lt] at h_j
      have ht' : t < A.length := h_t
      have hrow_eq : A.getD t [] = A[t] :=
        by simp [List.getD, List.getElem?_eq_getElem ht']
      have hj_nn : A[t].length ≤ j := hrow_eq ▸ h_j
      have hentry : entry A t j = 0 := by
        simp only [entry, List.getElem?_eq_getElem ht', Option.bind_some,
                   List.getElem?_eq_none_iff.mpr hj_nn, Option.getD_none]
      simp only [hentry, Int.zero_ediv, neg_zero, Int.zero_emod]
      simp only [entry, addCol, List.getElem?_map, List.getElem?_eq_getElem ht',
                 Option.map_some, Option.bind_some]
      rw [List.getElem?_eq_none_iff.mpr (by simp [hj_nn])]
      simp
  · simp only [not_lt] at h_t
    have ht_ge : A.length ≤ t := by simpa [numRows] using h_t
    have ht_none : A[t]? = none := List.getElem?_eq_none_iff.mpr ht_ge
    have hentry : entry A t j = 0 := by simp [entry, ht_none]
    simp only [hentry, Int.zero_ediv, neg_zero, Int.zero_emod]
    simp [entry, addCol, List.getElem?_map, ht_none]

end PytopSNF
