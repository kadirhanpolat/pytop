import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Formal.SNF.Positivity
import Mathlib.Data.Int.GCD

/-!
# Divisibility: the recorded factor divides all remaining entries

We prove `snfOuterStep_divides_submatrix`: whenever `snfOuterStep A t f = (M', some d)`,
the factor `d` divides every entry of `M'` strictly below/right of position `(t, t)`.

## Proof chain

1. **`submatrix_entry`**: `entry (submatrix A t) k l = entry A (t + k) (t + l)`.
   Proof: `List.getElem?_map` + `List.getElem?_drop`.

2. **`mem_of_getElem?_some`** (private helper): `l[i]? = some x → x ∈ l`.
   Uses `List.getElem?_eq_none_iff` + `List.getElem?_eq_getElem` + `List.getElem_mem`.

3. **`pivotDividesAll_correct`**: `pivotDividesAll A t = true ∧ pivot ≠ 0 →
   ∀ i > t, j > t, pivot ∣ entry A i j`.
   Proof: reindex via `submatrix_entry`, case-split on `getElem?`, extract membership,
   apply `List.all_eq_true` twice, convert Bool residue to `Int` via `decide_eq_true_eq`.

4. **`snfOuterStep_divides_submatrix`**: Split on `pivotDividesAll` branches;
   both delegate to step 3.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Submatrix entry connection
-- ---------------------------------------------------------------------------

/-- `entry (submatrix A t) k l = entry A (t + k) (t + l)`.

Proof: `(A.drop t).map (·.drop t)` at index `k` equals `A[t + k]?.map (·.drop t)`
(via `List.getElem?_map` + `List.getElem?_drop`), then dropping `t` from that row
and indexing at `l` gives `row[t + l]?` by `List.getElem?_drop` again. -/
private lemma submatrix_entry (A : IntMatrix) (t k l : Nat) :
    entry (submatrix A t) k l = entry A (t + k) (t + l) := by
  simp only [submatrix, entry]
  rw [show ((A.drop t).map (·.drop t))[k]? = A[t + k]?.map (·.drop t) from by
    rw [List.getElem?_map, List.getElem?_drop]]
  rcases A[t + k]? with _ | row
  · rfl
  · simp only [Option.map_some, Option.bind_some, List.getElem?_drop]

-- ---------------------------------------------------------------------------
-- Private helper: membership from getElem?
-- ---------------------------------------------------------------------------

/-- `l[i]? = some x → x ∈ l`. -/
private lemma mem_of_getElem?_some {α : Type*} {l : List α} {i : Nat} {x : α}
    (h : l[i]? = some x) : x ∈ l := by
  have hlt : i < l.length := by
    by_contra hge
    push_neg at hge
    rw [List.getElem?_eq_none_iff.mpr hge] at h
    exact absurd h (by simp)
  have heq : l[i]'hlt = x := by
    have := List.getElem?_eq_getElem hlt (l := l)
    rw [this] at h
    exact Option.some.inj h
  exact heq ▸ List.getElem_mem hlt

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
  -- Translate entry A i j to entry (submatrix A (t+1)) (i-(t+1)) (j-(t+1))
  have hik : t + 1 + (i - (t + 1)) = i := Nat.add_sub_cancel' (by omega)
  have hjl : t + 1 + (j - (t + 1)) = j := Nat.add_sub_cancel' (by omega)
  rw [← hik, ← hjl, ← submatrix_entry A (t + 1) (i - (t + 1)) (j - (t + 1))]
  -- Goal: entry A t t ∣ entry (submatrix A (t+1)) (i-(t+1)) (j-(t+1))
  set M := submatrix A (t + 1)
  set k := i - (t + 1)
  set ll := j - (t + 1)
  simp only [entry]
  -- Case-split on whether the row exists
  rcases h_Mk : M[k]? with _ | row
  · simp
  -- Case-split on whether the column entry exists
  rcases h_rowl : row[ll]? with _ | x
  · simp [h_rowl]
  simp only [h_rowl, Option.bind_some, Option.getD_some]
  -- Deduce membership from getElem? using the helper
  have hmem_row : row ∈ M := mem_of_getElem?_some h_Mk
  have hmem_x   : x ∈ row := mem_of_getElem?_some h_rowl
  -- Normalize h to ∀ row ∈ M, ∀ x ∈ row, x % pivot = 0
  -- (List.all_eq_true unfolds both nested `all` checks; decide_eq_true_eq drops `decide`)
  simp only [List.all_eq_true, decide_eq_true_eq] at h
  exact Int.dvd_of_emod_eq_zero (h row hmem_row x hmem_x)

-- ---------------------------------------------------------------------------
-- natAbs of the recorded factor divides the same entries
-- ---------------------------------------------------------------------------

/-- `a ∣ b → (a.natAbs : Int) ∣ b`. -/
theorem dvd_natAbs_cast {a b : Int} (h : a ∣ b) : (a.natAbs : Int) ∣ b :=
  Int.natAbs_dvd.mpr h

-- ---------------------------------------------------------------------------
-- Main theorem: snfOuterStep records a factor that divides the remainder
-- ---------------------------------------------------------------------------

/-- After `snfOuterStep` records factor `d`, `d` divides every entry of M' at
    position (i, j) with i > t and j > t.

**Branch 1** (`pivotDividesAll A₃ t`): M' = A₃, d = ↑(entry A₃ t t).natAbs.
  `pivotDividesAll_correct` + `dvd_natAbs_cast`.

**Branch 2** (`¬ pivotDividesAll A₃ t`, `pivotDividesAll A₅ t`): M' = A₅, d = ↑(entry A₅ t t).natAbs.
  Same argument; `entry A₅ t t ≠ 0` follows from the pivot-preservation chain
  `clearLoop_preserves_pivot` + `enforceDivisibility_preserves_pivot` (which requires
  `isCleared A₃ t`, still sorry'd pending the fuel-sufficiency argument).

**Branch 3** (both false): `snfOuterStep` returns `none`, contradicting `h`. -/
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
    split_ifs at h with hpda hpda'
    · -- Branch 1: pivotDividesAll A₃ t = true
      obtain ⟨hM', hd⟩ := Prod.mk.inj h
      subst hM'
      set A₃ := clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel
      have hd_eq : d = ↑(entry A₃ t t).natAbs := (Option.some.inj hd).symm
      subst hd_eq
      intro i j hi hj
      have hpivot : entry A₃ t t ≠ 0 :=
        clearLoop_pivot_ne_zero A t pi pj innerFuel hfp
      exact dvd_natAbs_cast (pivotDividesAll_correct A₃ t hpda hpivot i j hi hj)
    · -- Branch 2: ¬ pivotDividesAll A₃ t, pivotDividesAll A₅ t = true
      obtain ⟨hM', hd⟩ := Prod.mk.inj h
      subst hM'
      have hd_eq : d = ↑(entry _ t t).natAbs := (Option.some.inj hd).symm
      subst hd_eq
      intro i j hi hj
      set A₃ := clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel
      set A₄ := enforceDivisibility A₃ t
      set A₅ := clearLoop A₄ t innerFuel
      have hpivot₅ : entry A₅ t t ≠ 0 := by
        -- Chain: A₅ tt = A₄ tt = A₃ tt ≠ 0
        have h_A5_A4 : entry A₅ t t = entry A₄ t t :=
          clearLoop_preserves_pivot A₄ t innerFuel
        have h_A4_A3 : entry A₄ t t = entry A₃ t t := by
          apply enforceDivisibility_preserves_pivot
          -- `isCleared A₃ t = true` holds when innerFuel ≥ minNonzeroAbs A₂ t.
          -- This follows from clearLoop_stable (Termination.lean) but requires
          -- a fuel-sufficiency argument connecting pytopSNF's innerFuel bound
          -- to the actual minNonzeroAbs value.  Deferred to a follow-up.
          sorry
        rw [h_A5_A4, h_A4_A3]
        exact clearLoop_pivot_ne_zero A t pi pj innerFuel hfp
      exact dvd_natAbs_cast (pivotDividesAll_correct A₅ t hpda' hpivot₅ i j hi hj)
    · -- Branch 3: both false → snfOuterStep returns none, contradicts h
      simp at h

end PytopSNF
