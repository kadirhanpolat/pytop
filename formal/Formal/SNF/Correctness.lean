import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Formal.SNF.Positivity
import Formal.SNF.Divisibility
import Formal.SNF.Chain
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
| `clearLoop_stable`               | **proved** (in `Termination.lean`) |
| `snfOuterStep_pos`               | **proved** (in `Positivity.lean`) |
| `snfOuterStep_divides_submatrix` | partial (in `Divisibility.lean`) |
| `pytopSNF_divisibilityChain`     | `sorry` (in `Chain.lean`) |
| `pytopSNF_positive`              | `sorry` (in `Positivity.lean`) |
| `pytopSNF_fuel_independent`      | `sorry` |

## Termination note

`clearLoop_stable` is proved in `Formal.SNF.Termination`.
The key insight is that `clearPass` is **idempotent** (proved), which means
`clearLoop` stabilises after at most one `clearPass` application.
-/

namespace PytopSNF

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

-- `clearLoop A t (k+1) = clearLoop A t (k+2)` holds unconditionally:
-- if isCleared, both sides equal A; otherwise clearPass is idempotent, so
-- clearLoop_stuck applies to both.
private lemma clearLoop_succ_stable (A : IntMatrix) (t k : Nat) :
    clearLoop A t (k + 1) = clearLoop A t (k + 2) := by
  rw [clearLoop_succ, clearLoop_succ]
  split_ifs with hc
  · rfl
  · have hcpB : clearPass (clearPass A t) t = clearPass A t := by
      by_cases hpiv : entry A t t = 0
      · have hcp : clearPass A t = A := by unfold clearPass; rw [if_pos hpiv]
        rw [hcp]; exact hcp
      · exact clearPass_idempotent A t hpiv
    exact (clearLoop_stuck (clearPass A t) t k hcpB).trans
          (clearLoop_stuck (clearPass A t) t (k + 1) hcpB).symm

-- All fuel values ≥ 1 give the same clearLoop result.
private lemma clearLoop_fuel_eq (A : IntMatrix) (t k : Nat) :
    clearLoop A t 1 = clearLoop A t (k + 1) := by
  induction k with
  | zero => rfl
  | succ n ih => rw [← clearLoop_succ_stable A t n]; exact ih

-- snfOuterStep result is the same for any two innerFuel values ≥ 1.
-- Proof: subst both fuels to k+1 form, then simp rewrites all clearLoop calls.
private lemma snfOuterStep_fuel_eq (A : IntMatrix) (t f₁ f₂ : Nat)
    (h₁ : 1 ≤ f₁) (h₂ : 1 ≤ f₂) :
    snfOuterStep A t f₁ = snfOuterStep A t f₂ := by
  obtain ⟨k₁, rfl⟩ : ∃ k, f₁ = k + 1 := ⟨f₁ - 1, by omega⟩
  obtain ⟨k₂, rfl⟩ : ∃ k, f₂ = k + 1 := ⟨f₂ - 1, by omega⟩
  have hcl : ∀ B, clearLoop B t (k₁ + 1) = clearLoop B t (k₂ + 1) := fun B =>
    (clearLoop_fuel_eq B t k₁).symm.trans (clearLoop_fuel_eq B t k₂)
  simp only [snfOuterStep, hcl]

-- pytopSNFWithFuel.go is independent of innerFuel when both values are ≥ 1.
private lemma go_fuel_eq (n : Nat) (M : IntMatrix) (t : Nat) (acc : List Int) (f₁ f₂ : Nat)
    (h₁ : 1 ≤ f₁) (h₂ : 1 ≤ f₂) :
    pytopSNFWithFuel.go f₁ n M t acc = pytopSNFWithFuel.go f₂ n M t acc := by
  induction n generalizing M t acc with
  | zero => simp only [pytopSNFWithFuel.go]
  | succ k ih =>
    simp only [pytopSNFWithFuel.go]
    split_ifs with hbounds
    · rfl
    · rw [snfOuterStep_fuel_eq M t f₁ f₂ h₁ h₂]
      rcases snfOuterStep M t f₂ with ⟨M', dOpt⟩
      rcases dOpt with _ | d'
      · rfl
      · exact ih M' (t + 1) (d' :: acc)

/-- The fuel in `pytopSNF` is sufficient: the result equals `pytopSNFWithFuel`
    with any larger inner fuel.

    Proof: `clearLoop` stabilises after 1 step unconditionally (idempotency of
    `clearPass`), so all inner-fuel values ≥ 1 give identical results. Since
    the standard fuel `m·n·(|A|+1) ≥ 1` when mn > 0, and k ≥ that bound ≥ 1,
    both calls produce the same output. -/
theorem pytopSNF_fuel_independent (A : IntMatrix) (k : Nat)
    (hk : numRows A * numCols A * (sumAbs A + 1) ≤ k) :
    pytopSNFWithFuel (min (numRows A) (numCols A)) k A =
    pytopSNF A := by
  simp only [pytopSNF, pytopSNFWithFuel]
  rcases Nat.eq_zero_or_pos (numRows A * numCols A) with hmn | hmn
  · have hmin : min (numRows A) (numCols A) = 0 := by
      rcases Nat.mul_eq_zero.mp hmn with hm | hn
      · simp [hm]
      · simp [hn]
    simp [hmin, pytopSNFWithFuel.go]
  · have hsf_pos : 1 ≤ numRows A * numCols A * (sumAbs A + 1) :=
        Nat.mul_pos hmn (Nat.succ_pos _)
    have hk_pos : 1 ≤ k := hsf_pos.trans hk
    exact go_fuel_eq (min (numRows A) (numCols A)) A 0 []
        k (numRows A * numCols A * (sumAbs A + 1)) hk_pos hsf_pos

end PytopSNF
