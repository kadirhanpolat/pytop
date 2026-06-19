import Mathlib.Data.Int.GCD
import Mathlib.Data.List.Basic

/-!
# Smith Normal Form — Definitions

Formalises the mathematical objects underlying `pytop.exact_linalg.smith_normal_form`.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Integer matrices
-- ---------------------------------------------------------------------------

/-- An integer matrix as a list of rows. -/
abbrev IntMatrix := List (List Int)

/-- Number of rows. -/
def numRows (A : IntMatrix) : Nat := A.length

/-- Number of columns (length of first row, 0 if empty). -/
def numCols (A : IntMatrix) : Nat := (A.head?.map List.length).getD 0

/-- Safe entry access — returns 0 if out of bounds. -/
def entry (A : IntMatrix) (i j : Nat) : Int :=
  (A[i]?.bind (·[j]?)).getD 0

/-- The submatrix A[t:, t:]. -/
def submatrix (A : IntMatrix) (t : Nat) : IntMatrix :=
  (A.drop t).map (·.drop t)

-- ---------------------------------------------------------------------------
-- Divisibility chain
-- ---------------------------------------------------------------------------

/-- `ds` is a divisibility chain if each element divides the next. -/
def IsDivisibilityChain (ds : List Int) : Prop :=
  ∀ i : Fin (ds.length - 1),
    ds.get ⟨i.val, by omega⟩ ∣ ds.get ⟨i.val + 1, by omega⟩

/-- The invariant factors are positive and form a divisibility chain. -/
structure IsInvariantFactors (factors : List Int) : Prop where
  positive  : ∀ d ∈ factors, 0 < d
  divChain  : IsDivisibilityChain factors

-- ---------------------------------------------------------------------------
-- Smith Normal Form spec
-- ---------------------------------------------------------------------------

/-- A list is an SNF witness for `A` if it is a valid set of invariant factors.
    The explicit matrix equation is formalised in `Bridge.lean`. -/
structure IsSmithNF (A : IntMatrix) (factors : List Int) : Prop where
  invFactors : IsInvariantFactors factors

end PytopSNF
