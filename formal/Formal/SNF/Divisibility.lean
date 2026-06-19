import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Formal.SNF.Positivity
import Mathlib.Data.Int.GCD

/-!
# Divisibility: the recorded factor divides all remaining entries

We prove `snfOuterStep_divides_submatrix`: whenever `snfOuterStep A t f = (M', some d)`,
the factor `d` divides every entry of `M'` below and to the right of position `(t, t)`.

## Proof chain

1. **`pivotDividesAll_correct`**: If `pivotDividesAll M t = true` and pivot ≠ 0,
   then `entry M t t ∣ entry M i j` for all `i > t`, `j > t`.
   Proof: unfold the Bool `List.all` check; `x % pivot = 0 ↔ pivot ∣ x`.

2. **`natAbs_dvd_of_dvd`**: `a ∣ b → (a.natAbs : Int) ∣ b`.
   Follows from `Int.natAbs_dvd`.

3. **`snfOuterStep_divides_submatrix`**: Split on the two `pivotDividesAll` branches;
   both use steps 1–2.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Bool all-check implies algebraic divisibility
-- ---------------------------------------------------------------------------

/-- If `pivotDividesAll A t = true` and pivot is nonzero,
    then `entry A t t` divides every entry in the strict submatrix A[t+1:, t+1:]. -/
theorem pivotDividesAll_correct (A : IntMatrix) (t : Nat)
    (h : pivotDividesAll A t = true) (hpivot : entry A t t ≠ 0) :
    ∀ i j : Nat, t < i → t < j → entry A t t ∣ entry A i j := by
  simp only [pivotDividesAll, hpivot, ite_false] at h
  -- h : (submatrix A (t+1)).all (fun row => row.all (fun x => x % entry A t t = 0)) = true
  intro i j hi hj
  sorry
  -- Proof sketch:
  -- `submatrix A (t+1) = (A.drop (t+1)).map (·.drop (t+1))`
  -- `List.all_iff_forall` on the outer list gives: for each row in A.drop (t+1), inner all holds.
  -- The i-th row of A.drop (t+1) is A[i] (for i ≥ t+1).
  -- Inner all: for each x in row.drop (t+1), x % pivot = 0.
  -- The j-th element of A[i].drop (t+1) is entry A i j (for j ≥ t+1).
  -- x % pivot = 0 → pivot ∣ x → entry A t t ∣ entry A i j.

-- ---------------------------------------------------------------------------
-- natAbs of the recorded factor divides the same entries
-- ---------------------------------------------------------------------------

/-- `a ∣ b → (a.natAbs : Int) ∣ b`.

Since `a` and `↑a.natAbs` differ only in sign, divisibility is the same. -/
theorem dvd_natAbs_cast {a b : Int} (h : a ∣ b) : (a.natAbs : Int) ∣ b :=
  Int.natAbs_dvd.mpr h

-- ---------------------------------------------------------------------------
-- Main theorem: snfOuterStep records a factor that divides the remainder
-- ---------------------------------------------------------------------------

/-- After `snfOuterStep` records factor `d`, `d` divides every entry of M' at
    row > t and column > t.

Proof structure:
- `findPivot` returns none → result is none → h contradicts `some d`.
- `pivotDividesAll A₃ t = true`:  M' = A₃, d = ↑(entry A₃ t t).natAbs.
  `pivotDividesAll_correct` gives `entry A₃ t t ∣ entry A₃ i j`.
  `dvd_natAbs_cast` converts to `d ∣ entry A₃ i j`.
- `¬ pivotDividesAll A₃ t`, `pivotDividesAll A₅ t = true`:  M' = A₅, same argument. -/
theorem snfOuterStep_divides_submatrix (A : IntMatrix) (t innerFuel : Nat)
    (M' : IntMatrix) (d : Int)
    (h : snfOuterStep A t innerFuel = (M', some d)) :
    ∀ i j : Nat, t < i → t < j → d ∣ entry M' i j := by
  unfold snfOuterStep at h
  cases hfp : findPivot A t with
  | none =>
    rw [hfp] at h; simp at h
  | some pij =>
    obtain ⟨pi, pj⟩ := pij
    rw [hfp] at h
    simp only at h
    -- Split on the two pivotDividesAll branches (third case, both false, is auto-closed)
    split_ifs at h with hpda hpda'
    · -- Branch 1: pivotDividesAll A₃ t = true
      -- h : (A₃, ↑(entry A₃ t t).natAbs) = (M', some d)
      -- Extract M' = A₃ and d = ↑(entry A₃ t t).natAbs
      obtain ⟨hM', hd⟩ := Prod.mk.inj h
      subst hM'
      set A₃ := clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel
      have hd_eq : d = ↑(entry A₃ t t).natAbs :=
        (Option.some.inj hd).symm
      subst hd_eq
      -- Now goal: ↑(entry M' t t).natAbs ∣ entry M' i j  for i,j > t
      intro i j hi hj
      have hpivot : entry A₃ t t ≠ 0 :=
        clearLoop_pivot_ne_zero A t pi pj innerFuel hfp
      exact dvd_natAbs_cast (pivotDividesAll_correct A₃ t hpda hpivot i j hi hj)
    · -- Branch 2: ¬ pivotDividesAll A₃ t, pivotDividesAll A₅ t = true
      -- h : (A₅, some ↑(entry A₅ t t).natAbs) = (M', some d)
      obtain ⟨hM', hd⟩ := Prod.mk.inj h
      subst hM'
      have hd_eq : d = ↑(entry _ t t).natAbs := (Option.some.inj hd).symm
      subst hd_eq
      intro i j hi hj
      set A₃ := clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel
      set A₄ := enforceDivisibility A₃ t
      set A₅ := clearLoop A₄ t innerFuel
      have hpivot₅ : entry A₅ t t ≠ 0 := by
        sorry -- entry A₅ t t = entry A₃ t t ≠ 0:
              -- enforceDivisibility_preserves_pivot + clearLoop_preserves_pivot
      exact dvd_natAbs_cast (pivotDividesAll_correct A₅ t hpda' hpivot₅ i j hi hj)
    · -- Case 3: ¬ pivotDividesAll A₃ t, ¬ pivotDividesAll A₅ t
      -- h : (A₅, none) = (M', some d)  — the pair's second component gives none = some d
      simp at h

end PytopSNF
