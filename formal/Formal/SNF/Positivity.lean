import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Mathlib.Data.Int.GCD

/-!
# Positivity of SNF Invariant Factors

We prove that every factor returned by `pytopSNF` is strictly positive.

## Proof chain

1. `findPivot A t = some (pi, pj)` → `entry A pi pj ≠ 0` (sorry).
2. Swapping rows/cols moves the pivot to (t,t) (sorry).
3. **`clearLoop_preserves_pivot`** — proved here by induction on fuel.
4. Combining 1–3: the diagonal entry at (t,t) is always nonzero after setup.
5. `snfOuterStep_pos` — sorry-scaffolded, with key structural cases.
6. `pytopSNF_positive` — sorry; follows by induction on the `go` helper.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Sub-lemmas (sorry'd algebraic steps)
-- ---------------------------------------------------------------------------

/-- `findPivot` only returns positions with nonzero entries. -/
theorem findPivot_entry_nonzero (A : IntMatrix) (t pi pj : Nat)
    (h : findPivot A t = some (pi, pj)) :
    entry A pi pj ≠ 0 := by
  sorry

/-- Swapping rows pi↔t then cols pj↔t places the (pi, pj) entry at (t, t). -/
theorem swapRows_swapCols_diagonal (A : IntMatrix) (pi pj t : Nat) :
    entry (swapCols (swapRows A pi t) pj t) t t = entry A pi pj := by
  sorry

-- ---------------------------------------------------------------------------
-- clearLoop preserves the diagonal entry at (t, t)  [KEY PROVED THEOREM]
-- ---------------------------------------------------------------------------

/-- `clearLoop` does not change the diagonal entry at position (t, t).

Induction on fuel:
- Base (`k = 0`): `clearLoop A t 0 = A` by `clearLoop_zero`.
- Step (`k = n+1`):
  - If `isCleared A t`: returns A unchanged.
  - Else: returns `clearLoop (clearPass A t) t n`.
    By IH (generalised over A), `entry (clearLoop (clearPass A t) t n) t t`
    = `entry (clearPass A t) t t` = `entry A t t` (clearPass_preserves_pivot). -/
theorem clearLoop_preserves_pivot (A : IntMatrix) (t k : Nat) :
    entry (clearLoop A t k) t t = entry A t t := by
  induction k generalizing A with
  | zero => simp [clearLoop_zero]
  | succ n ih =>
    rw [clearLoop_succ]
    split_ifs with hc
    · rfl
    · rw [ih (clearPass A t), clearPass_preserves_pivot]

-- ---------------------------------------------------------------------------
-- Derived lemmas about the pivot
-- ---------------------------------------------------------------------------

/-- After swapping (pi,pj) to the diagonal, that entry is nonzero. -/
theorem swapped_pivot_ne_zero (A : IntMatrix) (t pi pj : Nat)
    (hfp : findPivot A t = some (pi, pj)) :
    entry (swapCols (swapRows A pi t) pj t) t t ≠ 0 := by
  rw [swapRows_swapCols_diagonal]
  exact findPivot_entry_nonzero A t pi pj hfp

/-- After `clearLoop`, the diagonal entry is still the original pivot value (nonzero). -/
theorem clearLoop_pivot_ne_zero (A : IntMatrix) (t pi pj innerFuel : Nat)
    (hfp : findPivot A t = some (pi, pj)) :
    entry (clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel) t t ≠ 0 := by
  rw [clearLoop_preserves_pivot]
  exact swapped_pivot_ne_zero A t pi pj hfp

-- ---------------------------------------------------------------------------
-- isCleared and enforceDivisibility
-- ---------------------------------------------------------------------------

/-- When `isCleared A t`, every entry in column t (except row t) is zero. -/
theorem isCleared_col_zero (A : IntMatrix) (t i : Nat) (ht : i ≠ t)
    (hcleared : isCleared A t = true) :
    entry A i t = 0 := by
  simp only [isCleared, Bool.and_eq_true, List.all_eq_true] at hcleared
  obtain ⟨hcol, _⟩ := hcleared
  by_cases hi : i < numRows A
  · have hmem : i ∈ List.range (numRows A) := List.mem_range.mpr hi
    have hcheck := hcol i hmem
    simp only [Bool.or_eq_true, decide_eq_true_eq] at hcheck
    rcases hcheck with rfl | h
    · exact absurd rfl ht
    · exact h
  · -- i ≥ numRows A → A[i]? = none → entry = 0
    push_neg at hi
    have hge : A.length ≤ i := by simpa [numRows] using hi
    have hni : A[i]? = none := List.getElem?_eq_none_iff.mpr hge
    simp [entry, hni]

/-- `enforceDivisibility A t` does not change `entry A t t` when the matrix
    is cleared (column t is zero off the diagonal).

Proof: if `bad = none`, the matrix is unchanged.  If `bad = some (i, j)`, the
algorithm returns `addRow A i t 1`.  By `addRow_entry_dst`:
  `entry (addRow A i t 1) t t = entry A t t + 1 * entry A i t`.
Since `isCleared A t` and `i > t`, `entry A i t = 0` by `isCleared_col_zero`. -/
theorem enforceDivisibility_preserves_pivot (A : IntMatrix) (t : Nat)
    (hcleared : isCleared A t = true) :
    entry (enforceDivisibility A t) t t = entry A t t := by
  -- Key: bad = some (i, _j) → addRow A i t 1 is returned;
  -- entry (addRow A i t 1) t t = entry A t t + 1 * entry A i t = entry A t t
  -- since isCleared A t → entry A i t = 0 for i ≠ t.
  -- The findSome? API needed to extract i > t is sorry'd.
  sorry

-- ---------------------------------------------------------------------------
-- snfOuterStep returns a positive factor
-- ---------------------------------------------------------------------------

/-- A nonzero integer has positive `natAbs`, viewed as an integer. -/
theorem natAbs_cast_pos {x : Int} (h : x ≠ 0) : (0 : Int) < ↑x.natAbs :=
  Int.natCast_pos.mpr (Int.natAbs_pos.mpr h)

/-- Every factor returned by `snfOuterStep` is strictly positive.

Proof sketch (sorry'd):
- `findPivot` returns none → result is `none` → h : none = some d → contradiction.
- `findPivot` returns `some (pi, pj)`:
  - A₂ = swapCols (swapRows A pi t) pj t:  entry A₂ t t = entry A pi pj ≠ 0
  - A₃ = clearLoop A₂ t innerFuel:
    entry A₃ t t = entry A₂ t t ≠ 0  (clearLoop_preserves_pivot)
  - If pivotDividesAll A₃:  d = ↑(entry A₃ t t).natAbs > 0  ✓
  - Else:  A₄ = enforceDivisibility A₃ t;  A₅ = clearLoop A₄ t innerFuel
    entry A₄ t t = entry A₃ t t ≠ 0  (enforceDivisibility_preserves_pivot — sorry'd)
    entry A₅ t t = entry A₄ t t ≠ 0  (clearLoop_preserves_pivot)
    If pivotDividesAll A₅:  d = ↑(entry A₅ t t).natAbs > 0  ✓
    Else:  result is none → h : none = some d → contradiction. -/
theorem snfOuterStep_pos (A : IntMatrix) (t innerFuel : Nat) (d : Int)
    (h : (snfOuterStep A t innerFuel).2 = some d) : 0 < d := by
  unfold snfOuterStep at h
  cases hfp : findPivot A t with
  | none =>
    -- (A, none).2 = none ≠ some d
    rw [hfp] at h; simp at h
  | some pij =>
    obtain ⟨pi, pj⟩ := pij
    rw [hfp] at h
    simp only at h
    -- h is about a two-level if-then-else; split_ifs generates 3 goals:
    --   (1) outer true, (2) outer false + inner true, (3) both false → none = some d
    -- split_ifs creates 3 sub-goals for the two nested ifs in h, but the third
    -- (none = some d) is auto-closed by split_ifs via simp, leaving 2 open goals.
    split_ifs at h with hpda hpda'
    · -- Case 1: pivotDividesAll A₃ t = true
      -- h : some ↑(entry A₃ t t).natAbs = some d
      set A₃ := clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel
      have hd : d = ↑(entry A₃ t t).natAbs :=
        (Option.some.inj h).symm
      rw [hd]
      exact natAbs_cast_pos (clearLoop_pivot_ne_zero A t pi pj innerFuel hfp)

    · -- Case 2: ¬ pivotDividesAll A₃ t, pivotDividesAll A₅ t = true
      -- h : some ↑(entry A₅ t t).natAbs = some d
      have hd : d = ↑(entry _ t t).natAbs := (Option.some.inj h).symm
      rw [hd]
      -- Need: entry A₅ t t ≠ 0
      -- Chain: A₂ → A₃ = clearLoop A₂ → A₄ = enforceDivisibility A₃ → A₅ = clearLoop A₄
      -- entry A₃ t t ≠ 0  (clearLoop_pivot_ne_zero)
      -- entry A₄ t t = entry A₃ t t  (enforceDivisibility_preserves_pivot — needs isCleared A₃)
      -- entry A₅ t t = entry A₄ t t  (clearLoop_preserves_pivot)
      set A₂ := swapCols (swapRows A pi t) pj t
      set A₃ := clearLoop A₂ t innerFuel
      have hA₃_ne : entry A₃ t t ≠ 0 := clearLoop_pivot_ne_zero A t pi pj innerFuel hfp
      -- isCleared A₃ t: with sufficient fuel, clearLoop always clears (sorry'd)
      have hcleared₃ : isCleared A₃ t = true := by sorry
      have hA₄ : entry (enforceDivisibility A₃ t) t t = entry A₃ t t :=
        enforceDivisibility_preserves_pivot A₃ t hcleared₃
      have hA₅ : entry (clearLoop (enforceDivisibility A₃ t) t innerFuel) t t =
                 entry (enforceDivisibility A₃ t) t t :=
        clearLoop_preserves_pivot (enforceDivisibility A₃ t) t innerFuel
      -- chain: entry (clearLoop A₄) t t = entry A₄ t t = entry A₃ t t ≠ 0
      have hfinal : entry (clearLoop (enforceDivisibility A₃ t) t innerFuel) t t ≠ 0 := by
        rw [hA₅, hA₄]; exact hA₃_ne
      exact natAbs_cast_pos hfinal

-- ---------------------------------------------------------------------------
-- pytopSNF_positive
-- ---------------------------------------------------------------------------

/-- Every factor in the output of `pytopSNF A` is strictly positive. -/
theorem pytopSNF_positive (A : IntMatrix) : ∀ d ∈ pytopSNF A, 0 < d := by
  sorry
  -- Induction on `pytopSNFWithFuel.go` outerFuel:
  -- At each step, if snfOuterStep returns some d then 0 < d by snfOuterStep_pos,
  -- and d is prepended to acc.  After acc.reverse, all elements are positive.

end PytopSNF
