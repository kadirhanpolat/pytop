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
  -- Invariant: any stored position has a nonzero entry.
  let Inv := fun (acc : Option ((Nat × Nat) × Nat)) =>
    ∀ p q b, acc = some ((p, q), b) → entry A p q ≠ 0
  -- One inner step preserves Inv.
  have step_pres : ∀ (i j : Nat) (acc : Option ((Nat × Nat) × Nat)),
      Inv acc →
      Inv (if entry A (i + t) (j + t) = 0 then acc
           else match acc with
             | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
             | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                 some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                               else acc) := by
    intro i j acc hP p q b heq
    by_cases hx : entry A (i + t) (j + t) = 0
    · rw [if_pos hx] at heq; exact hP p q b heq
    · rw [if_neg hx] at heq
      rcases acc with _ | ⟨⟨r, s⟩, b'⟩
      · -- acc = none: result is some ((i+t, j+t), ...)
        dsimp only at heq
        obtain ⟨hpq, _⟩ := Prod.mk.inj (Option.some.inj heq)
        obtain ⟨hp, hq⟩ := Prod.mk.inj hpq
        rw [← hp, ← hq]; exact hx
      · -- acc = some ((r, s), b'): result is if ... < b' then ... else some ((r, s), b')
        dsimp only at heq
        split_ifs at heq with hlt
        · obtain ⟨hpq, _⟩ := Prod.mk.inj (Option.some.inj heq)
          obtain ⟨hp, hq⟩ := Prod.mk.inj hpq
          rw [← hp, ← hq]; exact hx
        · exact hP p q b heq
  -- Inner foldl (over columns) preserves Inv.
  have inner_pres : ∀ (l : List Nat) (i : Nat) (acc : Option ((Nat × Nat) × Nat)),
      Inv acc →
      Inv (l.foldl (fun acc' j =>
          if entry A (i + t) (j + t) = 0 then acc'
          else match acc' with
            | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
            | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                              else acc')
        acc) := by
    intro l i acc hP
    induction l generalizing acc with
    | nil => simpa using hP
    | cons j js ih =>
      simp only [List.foldl_cons]
      exact ih _ (step_pres i j acc hP)
  -- Outer foldl (over rows) preserves Inv.
  have outer_pres : ∀ (l : List Nat) (acc : Option ((Nat × Nat) × Nat)),
      Inv acc →
      Inv (l.foldl (fun acc' i =>
          (List.range (numCols A - t)).foldl (fun acc'' j =>
            if entry A (i + t) (j + t) = 0 then acc''
            else match acc'' with
              | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
              | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                  some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                                else acc'')
            acc')
        acc) := by
    intro l acc hP
    induction l generalizing acc with
    | nil => simpa using hP
    | cons i is ih =>
      simp only [List.foldl_cons]
      exact ih _ (inner_pres _ i acc hP)
  -- Initial accumulator satisfies Inv vacuously.
  have hP0 : Inv none := fun _ _ _ hh => by simp at hh
  -- The full double-foldl satisfies Inv.
  have hFull : Inv ((List.range (numRows A - t)).foldl (fun acc' i =>
      (List.range (numCols A - t)).foldl (fun acc'' j =>
          if entry A (i + t) (j + t) = 0 then acc''
          else match acc'' with
            | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
            | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                              else acc'')
        acc')
    none) := outer_pres _ none hP0
  -- Connect to findPivot via definitional equality + Option.map.
  simp only [findPivot] at h
  rw [Option.map_eq_some_iff] at h
  obtain ⟨⟨⟨p, q⟩, bval⟩, hfold, hpair⟩ := h
  simp only [] at hpair
  obtain ⟨rfl, rfl⟩ := Prod.mk.inj hpair
  exact hFull p q bval hfold

-- ---------------------------------------------------------------------------
-- Private helpers for swapRows_swapCols_diagonal
-- ---------------------------------------------------------------------------

/-- Bounds from findPivot: pi < numRows A, t < numRows A, t ≤ pi, t ≤ pj. -/
lemma findPivot_range_bounds (A : IntMatrix) (t pi pj : Nat)
    (h : findPivot A t = some (pi, pj)) :
    pi < numRows A ∧ t < numRows A ∧ t ≤ pi ∧ t ≤ pj := by
  let Inv := fun (acc : Option ((Nat × Nat) × Nat)) =>
    ∀ p q b, acc = some ((p, q), b) → p < numRows A ∧ t ≤ p ∧ t ≤ q
  have step_pres : ∀ (i j : Nat) (acc : Option ((Nat × Nat) × Nat)),
      i + t < numRows A → Inv acc →
      Inv (if entry A (i + t) (j + t) = 0 then acc
           else match acc with
             | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
             | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                 some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                               else acc) := by
    intro i j acc hi hP p q b heq
    by_cases hx : entry A (i + t) (j + t) = 0
    · rw [if_pos hx] at heq; exact hP p q b heq
    · rw [if_neg hx] at heq
      rcases acc with _ | ⟨⟨r, s⟩, b'⟩
      · dsimp only at heq
        obtain ⟨hpq, _⟩ := Prod.mk.inj (Option.some.inj heq)
        obtain ⟨hp, hq⟩ := Prod.mk.inj hpq
        exact ⟨hp ▸ hi, hp ▸ Nat.le_add_left t i, hq ▸ Nat.le_add_left t j⟩
      · dsimp only at heq
        split_ifs at heq with hlt
        · obtain ⟨hpq, _⟩ := Prod.mk.inj (Option.some.inj heq)
          obtain ⟨hp, hq⟩ := Prod.mk.inj hpq
          exact ⟨hp ▸ hi, hp ▸ Nat.le_add_left t i, hq ▸ Nat.le_add_left t j⟩
        · exact hP p q b heq
  have inner_pres : ∀ (l : List Nat) (i : Nat) (acc : Option ((Nat × Nat) × Nat)),
      i + t < numRows A → Inv acc →
      Inv (l.foldl (fun acc' j =>
          if entry A (i + t) (j + t) = 0 then acc'
          else match acc' with
            | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
            | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                              else acc')
        acc) := by
    intro l i acc hi hP
    induction l generalizing acc with
    | nil => simpa using hP
    | cons j js ih =>
      simp only [List.foldl_cons]
      exact ih _ (step_pres i j acc hi hP)
  have outer_pres : ∀ (l : List Nat) (acc : Option ((Nat × Nat) × Nat)),
      (∀ i, i ∈ l → i + t < numRows A) → Inv acc →
      Inv (l.foldl (fun acc' i =>
          (List.range (numCols A - t)).foldl (fun acc'' j =>
            if entry A (i + t) (j + t) = 0 then acc''
            else match acc'' with
              | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
              | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                  some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                                else acc'')
            acc')
        acc) := by
    intro l acc hil hP
    induction l generalizing acc with
    | nil => simpa using hP
    | cons i is ih =>
      simp only [List.foldl_cons]
      apply ih
      · exact fun k hk => hil k (List.mem_cons.mpr (Or.inr hk))
      · exact inner_pres _ i acc (hil i (List.mem_cons.mpr (Or.inl rfl))) hP
  have hFull : Inv ((List.range (numRows A - t)).foldl (fun acc' i =>
      (List.range (numCols A - t)).foldl (fun acc'' j =>
          if entry A (i + t) (j + t) = 0 then acc''
          else match acc'' with
            | none => some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
            | some (_, b') => if (entry A (i + t) (j + t)).natAbs < b' then
                                some ((i + t, j + t), (entry A (i + t) (j + t)).natAbs)
                              else acc'')
        acc')
    none) :=
    outer_pres _ none (fun i hi => by simp [List.mem_range] at hi; omega)
               (fun _ _ _ hh => by simp at hh)
  simp only [findPivot] at h
  rw [Option.map_eq_some_iff] at h
  obtain ⟨⟨⟨p, q⟩, bval⟩, hfold, hpair⟩ := h
  simp only [] at hpair
  obtain ⟨rfl, rfl⟩ := Prod.mk.inj hpair
  obtain ⟨hpi_lt, hpi_ge, hpj_ge⟩ := hFull p q bval hfold
  exact ⟨hpi_lt, Nat.lt_of_le_of_lt hpi_ge hpi_lt, hpi_ge, hpj_ge⟩

/-- Row t of `swapRows A pi t` equals row pi of A. -/
private lemma swapRows_entry_t_at_pi (A : IntMatrix) (pi t c : Nat)
    (hpi : pi < numRows A) (ht : t < numRows A) :
    entry (swapRows A pi t) t c = entry A pi c := by
  have hpi' : pi < A.length := hpi
  have ht' : t < A.length := ht
  simp only [entry, swapRows, List.getElem?_mapIdx, List.getElem?_eq_getElem ht',
             Option.map_some, Option.bind_some]
  by_cases htp : t = pi
  · subst htp; simp only [if_true]
    rw [show List.getD A t A[t] = A[t] from by simp [List.getD, List.getElem?_eq_getElem ht']]
    simp [List.getElem?_eq_getElem ht']
  · rw [if_neg htp, if_true]
    simp [List.getD, List.getElem?_eq_getElem hpi']

/-- `(swapRows A pi t).getD t [] = A.getD pi []`. -/
private lemma swapRows_getD_t (A : IntMatrix) (pi t : Nat)
    (hpi : pi < numRows A) (ht : t < numRows A) :
    (swapRows A pi t).getD t [] = A.getD pi [] := by
  have hpi' : pi < A.length := hpi
  have ht' : t < A.length := ht
  simp only [List.getD, swapRows, List.getElem?_mapIdx, List.getElem?_eq_getElem ht',
             Option.map_some, Option.getD_some]
  by_cases htp : t = pi
  · subst htp; simp only [if_true]
    simp [List.getElem?_eq_getElem ht']
  · rw [if_neg htp, if_true]
    simp [List.getElem?_eq_getElem hpi']

/-- Swapping columns pj↔t places column pj at position (t,t), given column bounds. -/
private lemma swapCols_entry_t_at_pj (B : IntMatrix) (pj t : Nat)
    (ht : t < numRows B)
    (ht_row : t < (B.getD t []).length)
    (hpj : pj < (B.getD t []).length) :
    entry (swapCols B pj t) t t = entry B t pj := by
  have ht' : t < B.length := ht
  have hBt : B[t]? = some B[t] := List.getElem?_eq_getElem ht'
  have hrow_eq : B.getD t [] = B[t] := by simp [List.getD, hBt]
  rw [hrow_eq] at ht_row hpj
  have ht_row' : B[t][t]? = some B[t][t] := List.getElem?_eq_getElem ht_row
  have hpj' : B[t][pj]? = some B[t][pj] := List.getElem?_eq_getElem hpj
  simp only [entry, swapCols, List.getElem?_map, hBt, Option.map_some, Option.bind_some,
             List.getElem?_mapIdx, ht_row', Option.getD_some, hpj']
  by_cases htp : t = pj
  · subst htp; simp only [if_true]; simp [List.getD, ht_row']
  · rw [if_neg htp, if_true]; simp [List.getD, hpj']

/-- Swapping rows pi↔t then cols pj↔t places the (pi, pj) entry at (t, t). -/
theorem swapRows_swapCols_diagonal (A : IntMatrix) (pi pj t : Nat)
    (hpi : pi < numRows A) (ht : t < numRows A)
    (htpj : t ≤ pj) (hne : entry A pi pj ≠ 0) :
    entry (swapCols (swapRows A pi t) pj t) t t = entry A pi pj := by
  have hpi' : pi < A.length := hpi
  have hAt : A[pi]? = some A[pi] := List.getElem?_eq_getElem hpi'
  have hpj_bound : pj < (A.getD pi []).length := by
    rw [show A.getD pi [] = A[pi] from by simp [List.getD, hAt]]
    by_contra hge
    simp only [not_lt] at hge
    simp [entry, hAt, List.getElem?_eq_none_iff.mpr hge] at hne
  have ht_col : t < (A.getD pi []).length := Nat.lt_of_le_of_lt htpj hpj_bound
  set B := swapRows A pi t with hB_def
  have hBt : B.getD t [] = A.getD pi [] := swapRows_getD_t A pi t hpi ht
  have hBrows : numRows B = numRows A := by simp [B, swapRows, numRows]
  have hstep2 : entry B t pj = entry A pi pj := swapRows_entry_t_at_pi A pi t pj hpi ht
  have hBt_row : t < (B.getD t []).length := hBt ▸ ht_col
  have hBpj : pj < (B.getD t []).length := hBt ▸ hpj_bound
  rw [swapCols_entry_t_at_pj B pj t (hBrows ▸ ht) hBt_row hBpj, hstep2]

-- ---------------------------------------------------------------------------
-- Derived lemmas about the pivot
-- ---------------------------------------------------------------------------

/-- After swapping (pi,pj) to the diagonal, that entry is nonzero. -/
theorem swapped_pivot_ne_zero (A : IntMatrix) (t pi pj : Nat)
    (hfp : findPivot A t = some (pi, pj)) :
    entry (swapCols (swapRows A pi t) pj t) t t ≠ 0 := by
  have hne := findPivot_entry_nonzero A t pi pj hfp
  obtain ⟨hpi, ht, _, htpj⟩ := findPivot_range_bounds A t pi pj hfp
  rw [swapRows_swapCols_diagonal A pi pj t hpi ht htpj hne]
  exact hne

/-- After `clearLoop`, the diagonal entry is still the original pivot value (nonzero). -/
theorem clearLoop_pivot_ne_zero (A : IntMatrix) (t pi pj innerFuel : Nat)
    (hfp : findPivot A t = some (pi, pj)) :
    entry (clearLoop (swapCols (swapRows A pi t) pj t) t innerFuel) t t ≠ 0 := by
  rw [clearLoop_preserves_pivot]
  exact swapped_pivot_ne_zero A t pi pj hfp

-- ---------------------------------------------------------------------------
-- findSome? existence helper (avoids depending on Mathlib API name)
-- ---------------------------------------------------------------------------

lemma findSome?_exists {α β : Type*} {l : List α} {f : α → Option β} {b : β}
    (h : l.findSome? f = some b) : ∃ a ∈ l, f a = some b := by
  induction l with
  | nil => simp [List.findSome?] at h
  | cons a as ih =>
    unfold List.findSome? at h
    rcases hfa : f a with _ | b'
    · simp only [hfa] at h
      obtain ⟨x, hx, hxf⟩ := ih h
      exact ⟨x, List.mem_cons.mpr (Or.inr hx), hxf⟩
    · simp only [hfa] at h
      exact ⟨a, List.mem_cons.mpr (Or.inl rfl), hfa.trans h⟩

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
  unfold enforceDivisibility
  -- Case 1: pivot = 0 → unchanged
  by_cases hpivot_ne : entry A t t = 0
  · simp [hpivot_ne]
  -- Case 2: pivot ≠ 0
  · simp only [hpivot_ne, ite_false]
    -- Derive row bound from hpivot_ne : entry A t t ≠ 0
    have ht_row : t < numRows A := by
      simp only [numRows]
      by_contra hge
      push_neg at hge
      have hne : A[t]? = none := List.getElem?_eq_none_iff.mpr hge
      simp [entry, hne] at hpivot_ne
    -- Derive column bound
    have ht_col : t < (A.getD t []).length := by
      have hAt : A[t]? = some (A[t]'ht_row) :=
        List.getElem?_eq_getElem ht_row
      rw [show A.getD t [] = A[t]'ht_row from by simp [List.getD, hAt]]
      by_contra hge
      push_neg at hge
      have hcol : (A[t]'ht_row)[t]? = none := List.getElem?_eq_none_iff.mpr hge
      simp [entry, hAt, hcol] at hpivot_ne
    -- Case-split on bad
    set m := numRows A
    set n := numCols A
    set bad := (List.range m).findSome? fun i =>
      if i ≤ t then none
      else (List.range n).findSome? fun j =>
        if j ≤ t then none
        else if entry A i j % entry A t t ≠ 0 then some (i, j) else none
    rcases hbad : bad with _ | ⟨i, _j⟩
    · -- bad = none: unchanged
      rfl
    · -- bad = some (i, _j): return addRow A i t 1
      simp only
      -- entry A i t = 0  (isCleared_col_zero, needs i > t)
      have hi_gt : t < i := by
        -- Extract witness k from the outer findSome? (bad = some (i, _j))
        obtain ⟨k, hk_mem, hk_val⟩ := findSome?_exists hbad
        simp only [List.mem_range] at hk_mem   -- hk_mem : k < m
        -- Outer guard: if k ≤ t then none → k must satisfy t < k
        by_cases hkt : k ≤ t
        · simp [if_pos hkt] at hk_val          -- none = some _ → False → goal closed
        · simp only [if_neg hkt] at hk_val
          -- hk_val : inner findSome? for row k = some (i, _j)
          obtain ⟨j0, _, hj0_val⟩ := findSome?_exists hk_val
          -- Inner guard: if j0 ≤ t then none
          by_cases hj0t : j0 ≤ t
          · simp [if_pos hj0t] at hj0_val      -- none = some _ → False → goal closed
          · simp only [if_neg hj0t] at hj0_val
            split_ifs at hj0_val with hmod
            · -- some (k, j0) = some (i, _j)  →  i = k, and t < k from hkt
              -- (split_ifs auto-closes the ¬hmod branch where hj0_val : none = some _)
              have hik : k = i := (Prod.ext_iff.mp (Option.some.inj hj0_val)).1
              simp only [Nat.not_le] at hkt; omega
      have hentry_it : entry A i t = 0 :=
        isCleared_col_zero A t i (Nat.ne_of_gt hi_gt) hcleared
      -- Apply addRow_entry_dst
      rw [addRow_entry_dst A i t t 1 ht_row ht_col]
      simp [hentry_it]

-- ---------------------------------------------------------------------------
-- Helpers for snfOuterStep_pos
-- ---------------------------------------------------------------------------

/-- If `a.natAbs < b.natAbs`, then `a + b ≠ 0`. -/
private lemma add_ne_zero_of_natAbs_lt {a b : Int} (h : a.natAbs < b.natAbs) : a + b ≠ 0 := by
  intro hab
  have heq : a = -b := by omega
  have : a.natAbs = b.natAbs := by rw [heq, Int.natAbs_neg]
  omega

/-- `enforceDivisibility` does not zero the pivot when all column-t off-diagonal entries
    are strictly smaller in absolute value than the pivot. -/
lemma enforceDivisibility_pivot_ne_zero (B : IntMatrix) (t : Nat)
    (hpivot : entry B t t ≠ 0)
    (hbound : ∀ i, i ≠ t → (entry B i t).natAbs < (entry B t t).natAbs) :
    entry (enforceDivisibility B t) t t ≠ 0 := by
  unfold enforceDivisibility
  simp only [hpivot, ite_false]
  set m := numRows B
  set bad := (List.range m).findSome? fun i =>
    if i ≤ t then none
    else (List.range (numCols B)).findSome? fun j =>
      if j ≤ t then none
      else if entry B i j % entry B t t ≠ 0 then some (i, j) else none
  cases hbad : bad with
  | none => simp; exact hpivot
  | some ij =>
    obtain ⟨i, _j⟩ := ij
    simp only
    -- Extract i > t
    have hi_gt : t < i := by
      obtain ⟨k, hk_mem, hk_val⟩ := findSome?_exists hbad
      simp only [List.mem_range] at hk_mem
      by_cases hkt : k ≤ t
      · simp [if_pos hkt] at hk_val
      · simp only [if_neg hkt] at hk_val
        obtain ⟨j0, _, hj0_val⟩ := findSome?_exists hk_val
        by_cases hj0t : j0 ≤ t
        · simp [if_pos hj0t] at hj0_val
        · simp only [if_neg hj0t] at hj0_val
          split_ifs at hj0_val with hmod
          · have hik : k = i := (Prod.ext_iff.mp (Option.some.inj hj0_val)).1
            simp only [Nat.not_le] at hkt; omega
    -- Extract i < numRows B
    have hi_lt : i < m := by
      obtain ⟨k, hk_mem, hk_val⟩ := findSome?_exists hbad
      simp only [List.mem_range] at hk_mem
      by_cases hkt : k ≤ t
      · simp [if_pos hkt] at hk_val
      · simp only [if_neg hkt] at hk_val
        obtain ⟨j0, _, hj0_val⟩ := findSome?_exists hk_val
        by_cases hj0t : j0 ≤ t
        · simp [if_pos hj0t] at hj0_val
        · simp only [if_neg hj0t] at hj0_val
          split_ifs at hj0_val with hmod
          · have hik : k = i := (Prod.ext_iff.mp (Option.some.inj hj0_val)).1
            rw [← hik]; simpa [numRows] using hk_mem
    -- Row and column bounds at t from hpivot
    have ht_row : t < numRows B := by
      simp only [numRows]
      by_contra hge; push_neg at hge
      exact hpivot (by simp [entry, List.getElem?_eq_none_iff.mpr hge])
    have ht_col : t < (B.getD t []).length := by
      have hBt : B[t]? = some (B[t]'ht_row) := List.getElem?_eq_getElem ht_row
      rw [show B.getD t [] = B[t]'ht_row from by simp [List.getD, hBt]]
      by_contra hge; push_neg at hge
      exact hpivot (by simp [entry, hBt, List.getElem?_eq_none_iff.mpr hge])
    rw [addRow_entry_dst B i t t 1 ht_row ht_col, one_mul, add_comm]
    exact add_ne_zero_of_natAbs_lt (hbound i (Nat.ne_of_gt hi_gt))

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
    (h_fuel : 1 ≤ innerFuel)
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
    · -- Case 2: ¬ pivotDividesAll A₃ t, pivotDivisAll A₅ t = true
      have hd : d = ↑(entry _ t t).natAbs := (Option.some.inj h).symm
      rw [hd]
      set A₂ := swapCols (swapRows A pi t) pj t
      set A₃ := clearLoop A₂ t innerFuel
      have hA₂_ne : entry A₂ t t ≠ 0 := swapped_pivot_ne_zero A t pi pj hfp
      have hA₃_ne : entry A₃ t t ≠ 0 := clearLoop_pivot_ne_zero A t pi pj innerFuel hfp
      -- entry (enforceDivisibility A₃ t) t t ≠ 0: no isCleared required —
      -- all col-t off-diagonal entries of A₃ are bounded by clearLoop_col_lt_pivot.
      have hA₄_ne : entry (enforceDivisibility A₃ t) t t ≠ 0 :=
        enforceDivisibility_pivot_ne_zero A₃ t hA₃_ne
          (fun i hit => clearLoop_col_lt_pivot A₂ t i innerFuel hA₂_ne hit h_fuel)
      have hfinal : entry (clearLoop (enforceDivisibility A₃ t) t innerFuel) t t ≠ 0 := by
        rw [clearLoop_preserves_pivot]; exact hA₄_ne
      exact natAbs_cast_pos hfinal

-- ---------------------------------------------------------------------------
-- pytopSNF_positive
-- ---------------------------------------------------------------------------

/-- Inner induction: `pytopSNFWithFuel.go` accumulates only positive elements. -/
private lemma go_positive (innerFuel n : Nat) (M : IntMatrix) (t : Nat) (acc : List Int)
    (h_fuel : 1 ≤ innerFuel)
    (hacc : ∀ d ∈ acc, 0 < d) :
    ∀ d ∈ pytopSNFWithFuel.go innerFuel n M t acc, 0 < d := by
  induction n generalizing M t acc with
  | zero =>
    simp only [pytopSNFWithFuel.go]
    exact fun d hd => hacc d (List.mem_reverse.mp hd)
  | succ k ih =>
    intro d hd
    simp only [pytopSNFWithFuel.go] at hd
    split_ifs at hd with hbounds
    · exact hacc d (List.mem_reverse.mp hd)
    · rcases hstep : snfOuterStep M t innerFuel with ⟨M', dOpt⟩
      rw [hstep] at hd
      rcases dOpt with _ | d'
      · exact hacc d (List.mem_reverse.mp hd)
      · -- hd : d ∈ pytopSNFWithFuel.go innerFuel k M' (t+1) (d' :: acc)
        apply ih M' (t + 1) (d' :: acc)
        · intro e he
          simp only [List.mem_cons] at he
          -- Avoid rfl-substitution of d' by using rw on the goal instead
          cases he with
          | inl h =>
            rw [h]
            exact snfOuterStep_pos M t innerFuel d' h_fuel (by rw [hstep])
          | inr h => exact hacc e h
        · exact hd

/-- Every factor in the output of `pytopSNF A` is strictly positive. -/
theorem pytopSNF_positive (A : IntMatrix) : ∀ d ∈ pytopSNF A, 0 < d := by
  simp only [pytopSNF, pytopSNFWithFuel]
  -- Case-split on whether m*n = 0 (empty matrix → output []) or m*n ≥ 1 (innerFuel ≥ 1)
  rcases Nat.eq_zero_or_pos (numRows A * numCols A) with hmn | hmn
  · -- m*n = 0 → min m n = 0 → go returns [] → vacuously true
    have hmin : min (numRows A) (numCols A) = 0 := by
      rcases Nat.mul_eq_zero.mp hmn with hm | hn
      · simp [hm]
      · simp [hn]
    simp [hmin, pytopSNFWithFuel.go]
  · -- m*n ≥ 1 → innerFuel = m*n*(sumAbs+1) ≥ 1
    have h_fuel : 1 ≤ numRows A * numCols A * (sumAbs A + 1) :=
      Nat.mul_pos hmn (Nat.succ_pos _)
    exact go_positive _ _ _ _ _ h_fuel (by simp)

end PytopSNF
