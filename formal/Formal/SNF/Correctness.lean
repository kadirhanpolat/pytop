import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Mathlib.Data.Int.GCD
import Mathlib.Data.List.Basic

/-!
# SNF Correctness Theorems

States and partially proves that `pytopSNF` computes genuine invariant factors.

## Proof strategy

The algorithm maintains the following **loop invariant** at outer step `t`:

> There exist unimodular matrices U, V such that `current_M = U · A_init · V`,
> the top-left t×t block is diagonal with entries d₀, …, d_{t-1},
> and `d_{k-1} | d_k` for k < t.

Each elementary operation is left/right multiplication by a matrix with
determinant ±1, so unimodularity is preserved.  The divisibility condition
follows because `snfOuterStep` only records a factor after `pivotDividesAll`
returns true, ensuring `d_t | M[i][j]` for all i,j > t.

## Current status

| Theorem | Status |
|---------|--------|
| `clearLoop_stable`               | **proved** (in `Termination.lean`, sorried sub-lemmas) |
| `pytopSNF_fuel_independent`      | `sorry` |
| `snfOuterStep_pos`               | `sorry` |
| `pytopSNF_positive`              | `sorry` |
| `snfOuterStep_divides_submatrix` | `sorry` |
| `pytopSNF_divisibilityChain`     | `sorry` |

## Termination note

`clearLoop_stable` is proved in `Formal.SNF.Termination`.
The key insight is that `sumAbs` is **not** a suitable decreasing measure
(it can increase after `clearPass` — counter-example: [[2,100],[3,0]]).
The correct measure is `minNonzeroAbs`, which strictly decreases via
GCD descent (Euclidean algorithm analogue).
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Positivity
-- ---------------------------------------------------------------------------

/-- Every factor returned by `snfOuterStep` is positive (comes from `natAbs`). -/
theorem snfOuterStep_pos (A : IntMatrix) (t innerFuel : Nat) (d : Int)
    (h : (snfOuterStep A t innerFuel).2 = some d) : 0 < d := by
  sorry

/-- All elements of `pytopSNF A` are positive. -/
theorem pytopSNF_positive (A : IntMatrix) : ∀ d ∈ pytopSNF A, 0 < d := by
  sorry

-- ---------------------------------------------------------------------------
-- Divisibility chain
-- ---------------------------------------------------------------------------

/-- After `snfOuterStep` records factor `d`, `d` divides every remaining entry. -/
theorem snfOuterStep_divides_submatrix (A : IntMatrix) (t innerFuel : Nat)
    (M' : IntMatrix) (d : Int)
    (h : snfOuterStep A t innerFuel = (M', some d)) :
    ∀ i j : Nat, t < i → t < j → d ∣ entry M' i j := by
  sorry

/-- The output of `pytopSNF` is a divisibility chain. -/
theorem pytopSNF_divisibilityChain (A : IntMatrix) :
    IsDivisibilityChain (pytopSNF A) := by
  sorry

-- ---------------------------------------------------------------------------
-- Main result
-- ---------------------------------------------------------------------------

/-- `pytopSNF A` is a valid set of invariant factors. -/
theorem pytopSNF_isInvariantFactors (A : IntMatrix) :
    IsInvariantFactors (pytopSNF A) :=
  { positive := pytopSNF_positive A
  , divChain := pytopSNF_divisibilityChain A }

-- ---------------------------------------------------------------------------
-- Fuel sufficiency
-- ---------------------------------------------------------------------------

/-- The fuel in `pytopSNF` is sufficient: the result equals `pytopSNFWithFuel`
    with any larger inner fuel.

    This follows from `clearLoop_stable` (proved in `Termination.lean`):
    once innerFuel ≥ minNonzeroAbs A t ≤ sumAbs A, the result is stable. -/
theorem pytopSNF_fuel_independent (A : IntMatrix) (k : Nat)
    (hk : numRows A * numCols A * (sumAbs A + 1) ≤ k) :
    pytopSNFWithFuel (min (numRows A) (numCols A)) k A =
    pytopSNF A := by
  sorry

end PytopSNF
