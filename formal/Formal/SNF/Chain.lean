import Formal.SNF.Defs
import Formal.SNF.Elementary
import Formal.SNF.Algorithm
import Formal.SNF.Termination
import Formal.SNF.Positivity
import Formal.SNF.Divisibility
import Mathlib.Data.Int.GCD
import Mathlib.Data.List.Chain
import Mathlib.Tactic.Ring

/-!
# Bölünebilirlik Zinciri: pytopSNF_divisibilityChain

`pytopSNF A` çıktısı bir bölünebilirlik zinciri oluşturur.

## Kanıt stratejisi

Temel lemma: `factor_dvd_next`.
Dış döngünün değişmezi korunduğunda her adımda `last_d ∣ d_new` sağlanır.

`pytopSNF_divisibilityChain` doğrudan sorry ile verilir; alt lemmaları
`factor_dvd_next` ve `snfOuterStep_divides_submatrix` kullanarak
`pytopSNFWithFuel.go` üzerinde özyinelemeli induction kanıtlanabilir
(go fonksiyonunun where-clause parametrelerinin hoisting'i nedeniyle
ayrı bir yardımcı tanıma ihtiyaç vardır).
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Private arithmetic helpers
-- ---------------------------------------------------------------------------

private lemma dvd_Int_emod {a b n : Int} (ha : a ∣ b) (hn : a ∣ n) : a ∣ b % n := by
  obtain ⟨qb, hqb⟩ := ha
  obtain ⟨qn, hqn⟩ := hn
  refine ⟨qb - qn * (b / n), ?_⟩
  have step1 : b % n = b - n * (b / n) := by have := Int.emod_add_ediv b n; omega
  have step2 : b - n * (b / n) = a * (qb - qn * (b / n)) := by rw [hqb, hqn]; ring
  rw [step1, step2]

private lemma swapCols_col_t_dvd (B : IntMatrix) (pj t i : Nat) (d : Int)
    (hpj : t ≤ pj) (h_t : d ∣ entry B i t) (h_pj : d ∣ entry B i pj) :
    d ∣ entry (swapCols B pj t) i t := by
  simp only [entry, swapCols, List.getElem?_map]
  rcases hBi : B[i]? with _ | row
  · simp
  · simp only [Option.map_some, Option.bind_some, List.getElem?_mapIdx]
    rcases h2 : row[t]? with _ | x_t
    · simp
    · simp only [Option.map_some, Option.getD_some]
      have hxt : x_t = entry B i t := by simp [entry, hBi, h2]
      rcases Nat.eq_or_lt_of_le hpj with rfl | hlt
      · simp only [if_true]
        rw [show List.getD row t x_t = x_t from by simp [List.getD, h2], hxt]
        exact h_t
      · simp only [if_neg (Nat.ne_of_lt hlt), if_true]
        rcases h3 : row[pj]? with _ | v
        · rw [show List.getD row pj x_t = x_t from by simp [List.getD, h3], hxt]
          exact h_t
        · have hv : v = entry B i pj := by simp [entry, hBi, h3]
          rw [show List.getD row pj x_t = v from by simp [List.getD, h3], hv]
          exact h_pj

-- ---------------------------------------------------------------------------
-- Yardımcı: findPivot t-altmatrisinden seçim yapar
-- ---------------------------------------------------------------------------

/-- `findPivot A t = some (pi, pj)` ise `t ≤ pi` ve `t ≤ pj`. -/
theorem findPivot_indices_ge (A : IntMatrix) (t pi pj : Nat)
    (h : findPivot A t = some (pi, pj)) :
    t ≤ pi ∧ t ≤ pj := by
  obtain ⟨_, _, htpi, htpj⟩ := findPivot_range_bounds A t pi pj h
  exact ⟨htpi, htpj⟩

-- ---------------------------------------------------------------------------
-- Kilit lemma: önceki faktör sonrakini böler
-- ---------------------------------------------------------------------------

/-- Değişmez `hinv` sağlanıyorsa ve `snfOuterStep M t f = (M', some d)` ise
    `last_d ∣ d`. -/
theorem factor_dvd_next (M M' : IntMatrix) (t innerFuel : Nat)
    (last_d d : Int)
    (hinv : ∀ i j : Nat, t ≤ i → t ≤ j → last_d ∣ entry M i j)
    (hstep : snfOuterStep M t innerFuel = (M', some d)) :
    last_d ∣ d := by
  unfold snfOuterStep at hstep
  cases hfp : findPivot M t with
  | none => rw [hfp] at hstep; simp at hstep
  | some pij =>
    obtain ⟨pi, pj⟩ := pij
    rw [hfp] at hstep
    simp only at hstep
    obtain ⟨hpi, hpj⟩ := findPivot_indices_ge M t pi pj hfp
    have hdvd : last_d ∣ entry M pi pj := hinv pi pj hpi hpj
    have hne_piv := findPivot_entry_nonzero M t pi pj hfp
    obtain ⟨hpi_lt, ht_lt, _, htpj⟩ := findPivot_range_bounds M t pi pj hfp
    have hA2_tt : entry (swapCols (swapRows M pi t) pj t) t t = entry M pi pj :=
      swapRows_swapCols_diagonal M pi pj t hpi_lt ht_lt htpj hne_piv
    set A₃ := clearLoop (swapCols (swapRows M pi t) pj t) t innerFuel
    have hA3_tt : entry A₃ t t = entry M pi pj := by
      simp only [A₃, clearLoop_preserves_pivot, hA2_tt]
    split_ifs at hstep with hpda hpda'
    · -- Dal 1: d = ↑(entry A₃ t t).natAbs
      have hd : d = ↑(entry A₃ t t).natAbs := (Option.some.inj (Prod.mk.inj hstep).2).symm
      rw [hd, hA3_tt]; exact Int.dvd_natAbs.mpr hdvd
    · -- Dal 2: ¬ pivotDividesAll A₃ t, pivotDividesAll A₅ t = true
      have hd : d = ↑(entry _ t t).natAbs := (Option.some.inj (Prod.mk.inj hstep).2).symm
      rw [hd]
      apply Int.dvd_natAbs.mpr
      rw [clearLoop_preserves_pivot]
      -- Goal: last_d ∣ entry (enforceDivisibility A₃ t) t t
      have hA₃_ne : entry A₃ t t ≠ 0 := by intro h0; simp [pivotDividesAll, h0] at hpda
      have ht_numRows : t < numRows A₃ := by
        by_contra h; push Not at h
        exact hA₃_ne (by
          simp [entry, List.getElem?_eq_none_iff.mpr (by simpa [numRows] using h)])
      have ht_col : t < (A₃.getD t []).length := by
        rw [show A₃.getD t [] = (A₃[t]'ht_numRows) from
          by simp [List.getD, List.getElem?_eq_getElem ht_numRows]]
        by_contra h; push Not at h
        exact hA₃_ne (by
          simp [entry, List.getElem?_eq_getElem ht_numRows,
                List.getElem?_eq_none_iff.mpr h])
      have hA₂_ne : entry (swapCols (swapRows M pi t) pj t) t t ≠ 0 := by
        rw [hA2_tt]; exact hne_piv
      unfold enforceDivisibility
      simp only [hA₃_ne, ite_false]
      set m := numRows A₃
      set n := numCols A₃
      set bad := (List.range m).findSome? fun i =>
        if i ≤ t then none
        else (List.range n).findSome? fun j =>
          if j ≤ t then none
          else if entry A₃ i j % entry A₃ t t ≠ 0 then some (i, j) else none
      rcases h_bad : bad with _ | ⟨i_bad, j_bad⟩
      · -- bad = none: goal reduces to last_d ∣ entry A₃ t t
        rw [hA3_tt]; exact hdvd
      · -- bad = some (i_bad, j_bad): goal reduces to last_d ∣ entry (addRow A₃ i_bad t 1) t t
        have h_ibad_gt : t < i_bad := by
          obtain ⟨k, _, hk_if⟩ := findSome?_exists h_bad
          have hk_nle : ¬(k ≤ t) := by intro h; simp [if_pos h] at hk_if
          simp only [if_neg hk_nle] at hk_if
          obtain ⟨j, _, hj_if⟩ := findSome?_exists hk_if
          have hj_nle : ¬(j ≤ t) := by intro h; simp [if_pos h] at hj_if
          simp only [if_neg hj_nle] at hj_if
          by_cases hmod : entry A₃ k j % entry A₃ t t ≠ 0
          · simp only [if_pos hmod] at hj_if
            have hk_eq : k = i_bad := congrArg Prod.fst (Option.some.inj hj_if)
            omega
          · rw [not_ne_iff] at hmod; simp [hmod] at hj_if
        have h_ibad_ne_t : i_bad ≠ t := by omega
        have hdvd_swapR_t : last_d ∣ entry (swapRows M pi t) i_bad t := by
          by_cases hpi : i_bad = pi
          · rw [hpi, swapRows_entry_i M pi t t hpi_lt ht_lt]
            exact hinv t t (le_refl t) (le_refl t)
          · rw [swapRows_entry_ne M pi t i_bad t hpi h_ibad_ne_t]
            exact hinv i_bad t (by omega) (le_refl t)
        have hdvd_swapR_pj : last_d ∣ entry (swapRows M pi t) i_bad pj := by
          by_cases hpi : i_bad = pi
          · rw [hpi, swapRows_entry_i M pi t pj hpi_lt ht_lt]
            exact hinv t pj (le_refl t) htpj
          · rw [swapRows_entry_ne M pi t i_bad pj hpi h_ibad_ne_t]
            exact hinv i_bad pj (by omega) htpj
        have hdvd_A₂ : last_d ∣ entry (swapCols (swapRows M pi t) pj t) i_bad t :=
          swapCols_col_t_dvd (swapRows M pi t) pj t i_bad last_d htpj
            hdvd_swapR_t hdvd_swapR_pj
        have h2 : last_d ∣ entry A₃ i_bad t := by
          cases innerFuel with
          | zero =>
            change last_d ∣ entry (swapCols (swapRows M pi t) pj t) i_bad t
            exact hdvd_A₂
          | succ k =>
            change last_d ∣ entry (clearLoop (swapCols (swapRows M pi t) pj t) t (k+1)) i_bad t
            rw [clearLoop_col_t_of_succ (swapCols (swapRows M pi t) pj t) t k i_bad hA₂_ne]
            rw [clearPass_col_emod (swapCols (swapRows M pi t) pj t) t i_bad h_ibad_ne_t hA₂_ne]
            exact dvd_Int_emod hdvd_A₂ (hA2_tt.symm ▸ hdvd)
        rw [addRow_entry_dst A₃ i_bad t t 1 ht_numRows ht_col]
        simp only [one_mul]
        obtain ⟨q1, hq1⟩ := hA3_tt.symm ▸ hdvd
        obtain ⟨q2, hq2⟩ := h2
        exact ⟨q1 + q2, by rw [hq1, hq2]; ring⟩
    · simp at hstep

-- ---------------------------------------------------------------------------
-- Ana teorem için yardımcı lemmalar
-- ---------------------------------------------------------------------------

/-- Özyinelemeli karakterizasyon: IsDivisibilityChain (x :: y :: rest). -/
private lemma isDivisibilityChain_cons_cons {x y : Int} {rest : List Int} :
    IsDivisibilityChain (x :: y :: rest) ↔ x ∣ y ∧ IsDivisibilityChain (y :: rest) := by
  constructor
  · intro h
    refine ⟨?_, fun ⟨i, hi⟩ => ?_⟩
    · have := h ⟨0, by simp⟩; simpa using this
    · have := h ⟨i + 1, by simp at hi ⊢; omega⟩; simpa using this
  · intro ⟨hxy, hrest⟩ ⟨i, hi⟩
    cases i with
    | zero => simpa using hxy
    | succ j =>
      have := hrest ⟨j, by simp at hi ⊢; omega⟩
      simpa using this

/-- Son elemanı bölen bir eleman eklemek zincir özelliğini korur. -/
private lemma isDivisibilityChain_append_one :
    ∀ {l : List Int} {d : Int},
    IsDivisibilityChain l → (∀ x, l.getLast? = some x → x ∣ d) →
    IsDivisibilityChain (l ++ [d])
  | [], _, _, _ => by simp [IsDivisibilityChain]
  | [a], d, _, hlast => by
      simp only [List.singleton_append]
      rw [isDivisibilityChain_cons_cons]
      exact ⟨hlast a (by simp), by simp [IsDivisibilityChain]⟩
  | a :: b :: rest, d, hc, hlast => by
      simp only [List.cons_append]
      rw [isDivisibilityChain_cons_cons]
      rw [isDivisibilityChain_cons_cons] at hc
      exact ⟨hc.1, isDivisibilityChain_append_one hc.2 (fun x hx => hlast x (by simp [hx]))⟩

/-- İç özyineleme: pytopSNFWithFuel.go bölünebilirlik zinciri değişmezini korur. -/
private lemma go_divisibility_chain
    (innerFuel n : Nat) (M : IntMatrix) (t : Nat) (acc : List Int)
    (h_chain : IsDivisibilityChain acc.reverse)
    (h_inv : ∀ last_d, acc.head? = some last_d →
             ∀ i j, t ≤ i → t ≤ j → last_d ∣ entry M i j)
    (h_fuel : 1 ≤ innerFuel) :
    IsDivisibilityChain (pytopSNFWithFuel.go innerFuel n M t acc) := by
  induction n generalizing M t acc with
  | zero => simp only [pytopSNFWithFuel.go]; exact h_chain
  | succ k ih =>
    simp only [pytopSNFWithFuel.go]
    split_ifs with hbounds
    · exact h_chain
    · rcases hstep : snfOuterStep M t innerFuel with ⟨M', dOpt⟩
      rcases dOpt with _ | d'
      · exact h_chain
      · apply ih M' (t + 1) (d' :: acc)
        · rw [List.reverse_cons]
          apply isDivisibilityChain_append_one h_chain
          intro x hx
          simp only [List.getLast?_reverse] at hx
          exact factor_dvd_next M M' t innerFuel x d' (h_inv x hx) hstep
        · intro last_d hl
          simp only [List.head?_cons, Option.some.injEq] at hl
          subst hl
          intro i j hi hj
          exact snfOuterStep_divides_submatrix M t innerFuel M' d' h_fuel hstep i j
            (by omega) (by omega)

-- ---------------------------------------------------------------------------
-- Ana teorem
-- ---------------------------------------------------------------------------

/-- `pytopSNF A` çıktısı bir bölünebilirlik zinciridir. -/
theorem pytopSNF_divisibilityChain (A : IntMatrix) :
    IsDivisibilityChain (pytopSNF A) := by
  simp only [pytopSNF, pytopSNFWithFuel]
  rcases Nat.eq_zero_or_pos (numRows A * numCols A) with hmn | hmn
  · have hmin : min (numRows A) (numCols A) = 0 := by
      rcases Nat.mul_eq_zero.mp hmn with hm | hn
      · simp [hm]
      · simp [hn]
    simp only [hmin, pytopSNFWithFuel.go, List.reverse_nil]
    exact fun ⟨_, h⟩ => absurd h (Nat.not_lt_zero _)
  · have h_fuel : 1 ≤ numRows A * numCols A * (sumAbs A + 1) :=
      Nat.mul_pos hmn (Nat.succ_pos _)
    exact go_divisibility_chain _ _ A 0 []
      (by simp [IsDivisibilityChain]) (by simp) h_fuel

end PytopSNF
