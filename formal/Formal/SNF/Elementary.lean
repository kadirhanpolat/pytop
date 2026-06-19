import Formal.SNF.Defs
import Mathlib.Data.List.Basic
import Mathlib.Data.Int.Basic

/-!
# Elementary Row/Column Operations

Formalises the four operations used by `_smith_normal_form_python`.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Row operations
-- ---------------------------------------------------------------------------

/-- Swap rows i and j (0-indexed). -/
def swapRows (A : IntMatrix) (i j : Nat) : IntMatrix :=
  A.mapIdx fun k row =>
    if k = i then A.getD j row
    else if k = j then A.getD i row
    else row

/-- Add `factor * A[src]` to row `dst`. -/
def addRow (A : IntMatrix) (src dst : Nat) (factor : Int) : IntMatrix :=
  A.mapIdx fun k row =>
    if k = dst then
      let srcRow := A.getD src []
      row.mapIdx fun c x => x + factor * srcRow.getD c 0
    else row

-- ---------------------------------------------------------------------------
-- Column operations
-- ---------------------------------------------------------------------------

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

@[simp]
theorem swapRows_numRows (A : IntMatrix) (i j : Nat) :
    numRows (swapRows A i j) = numRows A := by
  simp [swapRows, numRows]

@[simp]
theorem addRow_numRows (A : IntMatrix) (src dst : Nat) (factor : Int) :
    numRows (addRow A src dst factor) = numRows A := by
  simp [addRow, numRows]

@[simp]
theorem swapCols_numRows (A : IntMatrix) (i j : Nat) :
    numRows (swapCols A i j) = numRows A := by
  simp [swapCols, numRows]

@[simp]
theorem addCol_numRows (A : IntMatrix) (src dst : Nat) (factor : Int) :
    numRows (addCol A src dst factor) = numRows A := by
  simp [addCol, numRows]

-- ---------------------------------------------------------------------------
-- Entry-level properties
-- ---------------------------------------------------------------------------

/-- After swapping rows i and j, entry (i, c) equals old entry (j, c). -/
theorem swapRows_entry_i (A : IntMatrix) (i j c : Nat) :
    entry (swapRows A i j) i c = entry A j c := by
  sorry

/-- addRow leaves all rows except `dst` unchanged. -/
theorem addRow_entry_unaffected (A : IntMatrix) (src dst k c : Nat) (factor : Int)
    (hk : k ≠ dst) :
    entry (addRow A src dst factor) k c = entry A k c := by
  sorry

/-- addCol leaves all columns except `dst` unchanged. -/
theorem addCol_entry_unaffected (A : IntMatrix) (src dst k c : Nat) (factor : Int)
    (hc : c ≠ dst) :
    entry (addCol A src dst factor) k c = entry A k c := by
  sorry

/-- addRow at position (dst, t) adds factor * entry (src, t). -/
theorem addRow_entry_dst (A : IntMatrix) (src dst c : Nat) (factor : Int) :
    entry (addRow A src dst factor) dst c =
    entry A dst c + factor * entry A src c := by
  sorry

/-- addCol at position (k, dst) adds factor * entry (k, src). -/
theorem addCol_entry_dst (A : IntMatrix) (src dst k : Nat) (factor : Int) :
    entry (addCol A src dst factor) k dst =
    entry A k dst + factor * entry A k src := by
  sorry

end PytopSNF
