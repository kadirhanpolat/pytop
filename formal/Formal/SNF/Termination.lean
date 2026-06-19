import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Mathlib.Data.Int.GCD

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

/-- `minNonzeroAbs = 0` iff every entry in A[t:, t:] is zero. -/
theorem minNonzeroAbs_zero_iff (A : IntMatrix) (t : Nat) :
    minNonzeroAbs A t = 0 ↔ ∀ i j, t ≤ i → t ≤ j → entry A i j = 0 := by
  sorry

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

/-- The pivot entry (t,t) is unchanged by clearPass. -/
theorem clearPass_preserves_pivot (A : IntMatrix) (t : Nat) :
    entry (clearPass A t) t t = entry A t t := by
  simp only [clearPass]
  split_ifs with h
  · rfl
  · sorry  -- addRow modifies i ≠ t; addCol modifies j ≠ t; (t,t) is untouched

/-- After `clearPass`, every off-pivot entry in column t satisfies
    `|entry (clearPass A t) i t| < |entry A t t|` (when pivot ≠ 0, i ≠ t). -/
theorem clearPass_col_residue (A : IntMatrix) (t i : Nat)
    (hi : i ≠ t) (hpivot : entry A t t ≠ 0) :
    (entry (clearPass A t) i t).natAbs < (entry A t t).natAbs := by
  sorry  -- new entry = old - (old / pivot) * pivot = old % pivot; |%| < |pivot|

/-- After `clearPass`, every off-pivot entry in row t satisfies
    `|entry (clearPass A t) t j| < |entry A t t|` (when pivot ≠ 0, j ≠ t). -/
theorem clearPass_row_residue (A : IntMatrix) (t j : Nat)
    (hj : j ≠ t) (hpivot : entry A t t ≠ 0) :
    (entry (clearPass A t) t j).natAbs < (entry A t t).natAbs := by
  sorry  -- same argument, column direction

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
