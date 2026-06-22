import Mathlib.Data.List.Basic
import Mathlib.Data.List.Pairwise
import Mathlib.Data.List.Count

/-!
# Yol 3: Sürekli Homolojiyi Z/2 Redüksiyonu

`pytop.persistent_homology` modülünün temel algoritmik doğruluğunu
Lean 4'te modellenmiştir.

## Model

* **Z2Col** — `List Nat`: sıralı satır indeksleri (1 olan girdiler).
* **Z2Matrix** — `List Z2Col`: sütunların listesi.
* **low** — en büyük satır indeksi (pivot).
* **symmDiff** — Z/2 sütun toplamı (simetrik fark).
* **reduce** — soldan sağa sütun indirgeme.
* **persistencePairs** — (doğum, ölüm) indeksleri.

## Ana teoremler

* `symmDiff_comm`  : simetrik fark simetriktir (kanıtlandı).
* `symmDiff_self`  : Z/2'de kendi kendine toplama sıfır verir (kanıtlandı).
-/

namespace PersHomology

/-- Z/2 matris sütunu: 1 olan satır indekslerinin sıralı listesi. -/
abbrev Z2Col := List Nat

/-- Z/2 matris: sütunların listesi. -/
abbrev Z2Matrix := List Z2Col

-- ──────────────────────────────────────────────────────────
-- 1. Temel işlemler
-- ──────────────────────────────────────────────────────────

/-- Bir sütunun **pivot** satırı: en büyük satır indeksi. -/
def low (col : Z2Col) : Option Nat := col.getLast?

/-- Sütun sıfır mı? -/
def isZeroCol (col : Z2Col) : Bool := col.isEmpty

/-- Z/2 **sütun toplamı**: iki sıralı listenin simetrik farkı.
    Sonuç sıralıdır eğer her iki girdi sıralıysa. -/
def symmDiff : Z2Col → Z2Col → Z2Col
  | [],      bs      => bs
  | as,      []      => as
  | a :: as, b :: bs =>
    if a < b      then a :: symmDiff as (b :: bs)
    else if b < a then b :: symmDiff (a :: as) bs
    else               symmDiff as bs
termination_by a b => a.length + b.length

-- ──────────────────────────────────────────────────────────
-- 2. symmDiff özellikleri (helpers; some proved, some sorry)
-- ──────────────────────────────────────────────────────────

theorem symmDiff_nil_left (l : Z2Col) : symmDiff [] l = l := by
  unfold symmDiff; cases l <;> rfl

theorem symmDiff_nil_right (l : Z2Col) : symmDiff l [] = l := by
  unfold symmDiff; cases l <;> rfl

/-- Z/2'de sütun iki kez toplama sıfır verir. -/
theorem symmDiff_self (l : Z2Col) (h : List.Pairwise (· < ·) l) :
    symmDiff l l = [] := by
  induction l with
  | nil => simp [symmDiff]
  | cons a as ih =>
    have halt : ¬a < a := by omega
    have step : symmDiff (a :: as) (a :: as) = symmDiff as as := by
      simp only [symmDiff, if_neg halt]
    rw [step]
    exact ih h.tail

/-- Simetrik fark simetriktir. -/
theorem symmDiff_comm (a b : Z2Col) : symmDiff a b = symmDiff b a := by
  induction a generalizing b with
  | nil => simp [symmDiff_nil_left, symmDiff_nil_right]
  | cons ha as ih =>
    induction b with
    | nil => simp [symmDiff_nil_left, symmDiff_nil_right]
    | cons hb bs ih_b =>
      rcases Nat.lt_or_ge ha hb with h | h
      · -- ha < hb
        have lhs : symmDiff (ha :: as) (hb :: bs) = ha :: symmDiff as (hb :: bs) := by
          simp only [symmDiff]; exact if_pos h
        have rhs : symmDiff (hb :: bs) (ha :: as) = ha :: symmDiff (hb :: bs) as := by
          simp only [symmDiff]; rw [if_neg (by omega : ¬hb < ha), if_pos h]
        rw [lhs, rhs, ih (hb :: bs)]
      · -- ha ≥ hb  (h : hb ≤ ha)
        rcases Nat.lt_or_eq_of_le h with h2 | h2
        · -- hb < ha
          have lhs : symmDiff (ha :: as) (hb :: bs) = hb :: symmDiff (ha :: as) bs := by
            simp only [symmDiff]; rw [if_neg (by omega : ¬ha < hb), if_pos h2]
          have rhs : symmDiff (hb :: bs) (ha :: as) = hb :: symmDiff bs (ha :: as) := by
            simp only [symmDiff]; exact if_pos h2
          rw [lhs, rhs, ih_b]
        · -- hb = ha  (i.e., ha = hb)
          have halt : ¬ha < ha := by omega
          have lhs : symmDiff (ha :: as) (hb :: bs) = symmDiff as bs := by
            simp only [symmDiff, h2, if_neg halt]
          have rhs : symmDiff (hb :: bs) (ha :: as) = symmDiff bs as := by
            simp only [symmDiff, h2, if_neg halt]
          rw [lhs, rhs, ih bs]

-- helpers for symmDiff_assoc
private theorem mem_sd_or_ph {x : Nat} {a b : Z2Col} (h : x ∈ symmDiff a b) :
    x ∈ a ∨ x ∈ b := by
  induction a generalizing b with
  | nil => exact Or.inr (symmDiff_nil_left b ▸ h)
  | cons ha as ih_a =>
    induction b with
    | nil => exact Or.inl (symmDiff_nil_right (ha :: as) ▸ h)
    | cons hb bs ih_b =>
      simp only [symmDiff] at h
      rcases Nat.lt_trichotomy ha hb with hab | rfl | hab
      · rw [if_pos hab] at h
        rcases List.mem_cons.mp h with rfl | h'
        · exact Or.inl (List.mem_cons.mpr (Or.inl rfl))
        · rcases ih_a h' with h'' | h''
          · exact Or.inl (List.mem_cons.mpr (Or.inr h''))
          · exact Or.inr h''
      · rw [if_neg (Nat.lt_irrefl _), if_neg (Nat.lt_irrefl _)] at h
        rcases ih_a h with h'' | h''
        · exact Or.inl (List.mem_cons.mpr (Or.inr h''))
        · exact Or.inr (List.mem_cons.mpr (Or.inr h''))
      · rw [if_neg (by omega : ¬ha < hb), if_pos hab] at h
        rcases List.mem_cons.mp h with rfl | h'
        · exact Or.inr (List.mem_cons.mpr (Or.inl rfl))
        · rcases ih_b h' with h'' | h''
          · exact Or.inl h''
          · exact Or.inr (List.mem_cons.mpr (Or.inr h''))

private theorem sd_sorted_ph (a b : Z2Col)
    (haP : List.Pairwise (· < ·) a) (hbP : List.Pairwise (· < ·) b) :
    List.Pairwise (· < ·) (symmDiff a b) := by
  induction a generalizing b with
  | nil => rwa [symmDiff_nil_left]
  | cons ha as ih_a =>
    induction b with
    | nil => rwa [symmDiff_nil_right]
    | cons hb bs ih_b =>
      have ⟨ha_all, ha_tl⟩ := List.pairwise_cons.mp haP
      have ⟨hb_all, hb_tl⟩ := List.pairwise_cons.mp hbP
      simp only [symmDiff]
      rcases Nat.lt_trichotomy ha hb with h | rfl | h
      · rw [if_pos h]
        apply List.pairwise_cons.mpr
        refine ⟨fun x hx => ?_, ih_a (hb :: bs) ha_tl hbP⟩
        rcases mem_sd_or_ph hx with hx_as | hx_hbbs
        · exact ha_all x hx_as
        · rcases List.mem_cons.mp hx_hbbs with rfl | hx_bs
          · exact h
          · exact Nat.lt_trans h (hb_all x hx_bs)
      · rw [if_neg (Nat.lt_irrefl _), if_neg (Nat.lt_irrefl _)]
        exact ih_a bs ha_tl hb_tl
      · rw [if_neg (by omega : ¬ha < hb), if_pos h]
        apply List.pairwise_cons.mpr
        refine ⟨fun x hx => ?_, ih_b hb_tl⟩
        rcases mem_sd_or_ph hx with hx_haas | hx_bs
        · rcases List.mem_cons.mp hx_haas with rfl | hx_as
          · exact h
          · exact Nat.lt_trans h (ha_all x hx_as)
        · exact hb_all x hx_bs

private theorem count_sd_mod2_ph (x : Nat) (a b : Z2Col) :
    List.count x (symmDiff a b) % 2 = (List.count x a + List.count x b) % 2 := by
  induction a generalizing b with
  | nil => simp [symmDiff_nil_left]
  | cons ha as ih_a =>
    induction b with
    | nil => simp [symmDiff_nil_right]
    | cons hb bs ih_b =>
      simp only [symmDiff]
      rcases Nat.lt_trichotomy ha hb with h | rfl | h
      · rw [if_pos h]
        simp only [List.count_cons]
        have h_ih := ih_a (hb :: bs)
        simp only [List.count_cons] at h_ih
        omega
      · rw [if_neg (Nat.lt_irrefl _), if_neg (Nat.lt_irrefl _), ih_a bs]
        simp only [List.count_cons]
        split_ifs <;> omega
      · rw [if_neg (by omega : ¬ha < hb), if_pos h]
        simp only [List.count_cons]
        have h_ih := ih_b
        simp only [List.count_cons] at h_ih
        omega

private theorem sorted_count_le1_ph (x : Nat) (l : Z2Col)
    (hl : List.Pairwise (· < ·) l) : List.count x l ≤ 1 := by
  induction l with
  | nil => simp
  | cons h t ih =>
    have ⟨h_all, h_tl⟩ := List.pairwise_cons.mp hl
    by_cases hxh : x = h
    · subst hxh
      have hct : List.count x t = 0 :=
        List.count_eq_zero.mpr fun hy => absurd (h_all x hy) (Nat.lt_irrefl x)
      simp [hct, beq_self_eq_true]
    · have hne : h ≠ x := fun heq => hxh heq.symm
      have hbv : ¬((h == x) = true) := fun heq => hne (beq_iff_eq.mp heq)
      have heqc : List.count x (h :: t) = List.count x t := by
        simp only [List.count_cons, if_neg hbv]; omega
      rw [heqc]; exact ih h_tl

private theorem mem_iff_count_pos_ph {x : Nat} {l : List Nat} :
    x ∈ l ↔ 0 < List.count x l := by
  induction l with
  | nil => simp
  | cons h t ih =>
    simp only [List.mem_cons, List.count_cons]
    by_cases hxh : x = h
    · subst hxh; simp [beq_self_eq_true]
    · have hne : h ≠ x := fun heq => hxh heq.symm
      have hbv : ¬((h == x) = true) := fun heq => hne (beq_iff_eq.mp heq)
      simp only [List.count_cons, if_neg hbv]
      constructor
      · rintro (rfl | ht)
        · exact absurd rfl hxh
        · have h' := ih.mp ht; omega
      · intro hct
        exact Or.inr (ih.mpr (by omega))

private theorem sorted_ext_ph (a b : Z2Col)
    (haP : List.Pairwise (· < ·) a) (hbP : List.Pairwise (· < ·) b)
    (hmem : ∀ x, x ∈ a ↔ x ∈ b) : a = b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons hb bs =>
      exact absurd ((hmem hb).mpr (List.mem_cons.mpr (Or.inl rfl))) (by simp)
  | cons ha as ih_a =>
    cases b with
    | nil =>
      exact absurd ((hmem ha).mp (List.mem_cons.mpr (Or.inl rfl))) (by simp)
    | cons hb bs =>
      have ⟨ha_all, ha_tl⟩ := List.pairwise_cons.mp haP
      have ⟨hb_all, hb_tl⟩ := List.pairwise_cons.mp hbP
      have hle : ha ≤ hb := by
        rcases List.mem_cons.mp ((hmem hb).mpr (List.mem_cons.mpr (Or.inl rfl)))
            with rfl | h_in_as
        · exact Nat.le_refl _
        · exact Nat.le_of_lt (ha_all hb h_in_as)
      have hge : hb ≤ ha := by
        rcases List.mem_cons.mp ((hmem ha).mp (List.mem_cons.mpr (Or.inl rfl)))
            with rfl | h_in_bs
        · exact Nat.le_refl _
        · exact Nat.le_of_lt (hb_all ha h_in_bs)
      have heq : ha = hb := Nat.le_antisymm hle hge
      subst heq
      congr 1
      apply ih_a bs ha_tl hb_tl
      intro x
      constructor
      · intro hx_as
        rcases List.mem_cons.mp ((hmem x).mp (List.mem_cons.mpr (Or.inr hx_as)))
            with h_eq | h_in_bs
        · have hlt := ha_all x hx_as; rw [h_eq] at hlt
          exact absurd hlt (Nat.lt_irrefl _)
        · exact h_in_bs
      · intro hx_bs
        rcases List.mem_cons.mp ((hmem x).mpr (List.mem_cons.mpr (Or.inr hx_bs)))
            with h_eq | h_in_as
        · have hlt := hb_all x hx_bs; rw [h_eq] at hlt
          exact absurd hlt (Nat.lt_irrefl _)
        · exact h_in_as

/-- Sıralı sütunlarda Z/2 simetrik fark ilişkilendiricidir. -/
theorem symmDiff_assoc (a b c : Z2Col)
    (haP : List.Pairwise (· < ·) a)
    (hbP : List.Pairwise (· < ·) b)
    (hcP : List.Pairwise (· < ·) c) :
    symmDiff a (symmDiff b c) = symmDiff (symmDiff a b) c := by
  have hbc := sd_sorted_ph b c hbP hcP
  have hab := sd_sorted_ph a b haP hbP
  apply sorted_ext_ph _ _ (sd_sorted_ph a _ haP hbc) (sd_sorted_ph _ c hab hcP)
  intro x
  have count_eq : List.count x (symmDiff a (symmDiff b c)) =
                  List.count x (symmDiff (symmDiff a b) c) := by
    have lhs_mod := count_sd_mod2_ph x a (symmDiff b c)
    have rhs_mod := count_sd_mod2_ph x (symmDiff a b) c
    have bc_mod  := count_sd_mod2_ph x b c
    have ab_mod  := count_sd_mod2_ph x a b
    have hle_a   := sorted_count_le1_ph x a haP
    have hle_b   := sorted_count_le1_ph x b hbP
    have hle_c   := sorted_count_le1_ph x c hcP
    have hle_bc  := sorted_count_le1_ph x _ hbc
    have hle_ab  := sorted_count_le1_ph x _ hab
    have hle_lhs := sorted_count_le1_ph x _ (sd_sorted_ph a _ haP hbc)
    have hle_rhs := sorted_count_le1_ph x _ (sd_sorted_ph _ c hab hcP)
    omega
  rw [mem_iff_count_pos_ph, count_eq, ← mem_iff_count_pos_ph]

-- ──────────────────────────────────────────────────────────
-- 3. Redükte form
-- ──────────────────────────────────────────────────────────

/-- Bir matris **redükte formdadır** eğer her sıfırdan farklı sütunun
    pivot satırı benzersizse. -/
def isReduced (M : Z2Matrix) : Prop :=
  ∀ j1 j2 : Fin M.length, j1 ≠ j2 →
    (M.get j1).getLast? = none ∨ (M.get j1).getLast? ≠ (M.get j2).getLast?

-- ──────────────────────────────────────────────────────────
-- 4. İndirgeme algoritması
-- ──────────────────────────────────────────────────────────

/-- Pivot sütun tablosu. -/
def PivotTab := List (Option Nat)

-- ──────────────────────────────────────────────────────────
-- 4. İndirgeme algoritması (fuel-based)
-- ──────────────────────────────────────────────────────────

-- TabInv: tab[i] = some k  ↔  accM[k] son elemanı i
private def TabInv (accM : Z2Matrix) (tab : PivotTab) : Prop :=
  (∀ i k, tab.getD i none = some k →
      k < accM.length ∧ (accM.getD k []).getLast? = some i) ∧
  (∀ k i, k < accM.length → (accM.getD k []).getLast? = some i →
      tab.getD i none = some k)

-- getLast? membership (needed below, defined here to avoid forward reference)
private lemma getLast?_mem_ph' {col : Z2Col} {ci : Nat}
    (h : col.getLast? = some ci) : ci ∈ col := by
  induction col with
  | nil => simp at h
  | cons a t ih =>
    rcases t with _ | ⟨b, rest⟩
    · simp [List.getLast?] at h; exact List.mem_cons.mpr (Or.inl h.symm)
    · exact List.mem_cons.mpr (Or.inr (ih h))

private lemma tabInv_nil (n : Nat) : TabInv [] (List.replicate n none) := by
  constructor
  · intro i k h
    have hrep : (List.replicate n (none : Option Nat)).getD i none = none := by
      simp only [List.getD_eq_getElem?_getD, List.getElem?_replicate]
      split_ifs <;> rfl
    rw [hrep] at h; exact absurd h (by simp)
  · intro k i hk; exact absurd hk (Nat.not_lt_zero k)

-- getD helpers (proved by structural induction to avoid Mathlib API version dependencies)
private lemma getD_append_left_r {α} (l1 l2 : List α) (k : Nat) (d : α) (h : k < l1.length) :
    (l1 ++ l2).getD k d = l1.getD k d := by
  induction l1 generalizing k with
  | nil => exact absurd h (Nat.not_lt_zero _)
  | cons a t ih =>
    cases k with
    | zero => rfl
    | succ n => exact ih n (Nat.lt_of_succ_lt_succ h)

private lemma getD_snoc_last {α} (l : List α) (a d : α) :
    (l ++ [a]).getD l.length d = a := by
  induction l with
  | nil => rfl
  | cons b t ih => exact ih

private lemma getD_out_of_bounds {α} (l : List α) (k : Nat) (d : α) (h : l.length ≤ k) :
    l.getD k d = d := by
  induction l generalizing k with
  | nil => cases k <;> rfl
  | cons a t ih =>
    cases k with
    | zero => exact absurd h (by simp)
    | succ n => exact ih n (Nat.le_of_succ_le_succ h)

private lemma getD_set_eq_r {α} (l : List α) (i : Nat) (v d : α) (h : i < l.length) :
    (l.set i v).getD i d = v := by
  induction l generalizing i with
  | nil => exact absurd h (Nat.not_lt_zero _)
  | cons a t ih =>
    cases i with
    | zero => rfl
    | succ n => exact ih n (Nat.lt_of_succ_lt_succ h)

private lemma getD_set_ne_r {α} (l : List α) (i j : Nat) (v d : α) (h : i ≠ j) :
    (l.set i v).getD j d = l.getD j d := by
  induction l generalizing i j with
  | nil => cases i <;> cases j <;> rfl
  | cons a t ih =>
    cases i with
    | zero => cases j with
      | zero => exact absurd rfl h
      | succ m => rfl
    | succ n => cases j with
      | zero => rfl
      | succ m => exact ih n m (fun heq => h (congrArg Nat.succ heq))

private lemma length_set_r {α} (l : List α) (i : Nat) (v : α) :
    (l.set i v).length = l.length := by
  induction l generalizing i with
  | nil => cases i <;> rfl
  | cons a t ih => cases i with
    | zero => rfl
    | succ n => simp [List.set, ih n]

-- Helper lemmas reusing existing private functions in this namespace
private lemma getLast?_count_one_r {l : Z2Col} {i : Nat}
    (hl : l.getLast? = some i) (hP : List.Pairwise (· < ·) l) : List.count i l = 1 := by
  have h1 := mem_iff_count_pos_ph.mp (getLast?_mem_ph' hl)
  have h2 := sorted_count_le1_ph i l hP; omega

private lemma not_mem_symmDiff_eqLast {col other : Z2Col} {i : Nat}
    (hc  : col.getLast? = some i)   (hcP : List.Pairwise (· < ·) col)
    (ho  : other.getLast? = some i) (hoP : List.Pairwise (· < ·) other) :
    i ∉ symmDiff col other := by
  rw [mem_iff_count_pos_ph]
  have hmod := count_sd_mod2_ph i col other
  rw [getLast?_count_one_r hc hcP, getLast?_count_one_r ho hoP] at hmod
  have hle := sorted_count_le1_ph i _ (sd_sorted_ph col other hcP hoP); omega

private lemma sorted_le_getLast? {l : Z2Col} {i x : Nat}
    (hl : l.getLast? = some i) (hP : List.Pairwise (· < ·) l) (hx : x ∈ l) : x ≤ i := by
  induction l with
  | nil => simp at hl
  | cons a t ih =>
    rcases List.mem_cons.mp hx with rfl | hxt
    · cases t with
      | nil =>
        -- [a].getLast? = some a definitionally, so a = i
        have heq : x = i := Option.some.inj (show List.getLast? [x] = some i from hl)
        omega
      | cons b rest =>
        have ha := (List.pairwise_cons.mp hP).1
        -- (a :: b :: rest).getLast? reduces to (b :: rest).getLast? definitionally
        have ht : (b :: rest).getLast? = some i := hl
        exact Nat.le_of_lt (ha i (getLast?_mem_ph' ht))
    · cases t with
      | nil => exact absurd hxt (by simp)
      | cons b rest =>
        have ht : (b :: rest).getLast? = some i := hl
        exact ih ht hP.tail hxt

private lemma symmDiff_getLast?_lt_r {col other : Z2Col} {i : Nat}
    (hc  : col.getLast? = some i)   (hcP : List.Pairwise (· < ·) col)
    (ho  : other.getLast? = some i) (hoP : List.Pairwise (· < ·) other) :
    (symmDiff col other).getLast? = none ∨
    ∃ j, (symmDiff col other).getLast? = some j ∧ j < i := by
  rcases h : (symmDiff col other).getLast? with _ | j
  · exact Or.inl rfl
  · apply Or.inr; refine ⟨j, rfl, ?_⟩
    have hmem := getLast?_mem_ph' h
    have hle : j ≤ i := by
      rcases mem_sd_or_ph hmem with hj | hj
      · exact sorted_le_getLast? hc hcP hj
      · exact sorted_le_getLast? ho hoP hj
    rcases Nat.lt_or_eq_of_le hle with hlt | rfl
    · exact hlt
    · exact absurd hmem (not_mem_symmDiff_eqLast hc hcP ho hoP)

/-- Fuel-based sütun indirgeme. Fuel = başlangıç pivot + 1 yeterlidir. -/
def reduceColFuel : Nat → Z2Col → PivotTab → Z2Matrix → Z2Col
  | 0,     col, _,   _  => col
  | n + 1, col, tab, M  =>
    match col.getLast? with
    | none   => col
    | some i =>
      match tab.getD i none with
      | none   => col
      | some k => reduceColFuel n (symmDiff col (M.getD k [])) tab M

private lemma reduceColFuel_of_zero (n : Nat) (col : Z2Col) (tab : PivotTab) (M : Z2Matrix)
    (h : col.getLast? = none) : reduceColFuel n col tab M = col := by
  cases n <;> simp [reduceColFuel, h]

private lemma reduceColFuel_sorted (n : Nat) (col : Z2Col) (tab : PivotTab) (M : Z2Matrix)
    (hc : List.Pairwise (· < ·) col)
    (hM : ∀ k, List.Pairwise (· < ·) (M.getD k [])) :
    List.Pairwise (· < ·) (reduceColFuel n col tab M) := by
  induction n generalizing col with
  | zero => exact hc
  | succ n ih =>
    cases hL : col.getLast? with
    | none =>
      have heq : reduceColFuel (n + 1) col tab M = col := by
        unfold reduceColFuel; simp [hL]
      rw [heq]; exact hc
    | some i =>
      cases hT : tab.getD i none with
      | none =>
        have heq : reduceColFuel (n + 1) col tab M = col := by
          simp only [reduceColFuel, hL, hT]
        rw [heq]; exact hc
      | some k =>
        have heq : reduceColFuel (n + 1) col tab M =
            reduceColFuel n (symmDiff col (M.getD k [])) tab M := by
          simp only [reduceColFuel, hL, hT]
        rw [heq]
        exact ih _ (sd_sorted_ph col _ hc (hM k))

/-- Fuel yeterli olduğunda sonuç ya sıfır ya da serbest pivotlu sütundur. -/
private lemma reduceColFuel_free (n : Nat) (col : Z2Col) (tab : PivotTab) (M : Z2Matrix)
    (htab : TabInv M tab)
    (hc   : List.Pairwise (· < ·) col)
    (hM   : ∀ k, List.Pairwise (· < ·) (M.getD k []))
    (hf   : col.getLast?.getD 0 < n) :
    (reduceColFuel n col tab M).getLast? = none ∨
    ∃ i, (reduceColFuel n col tab M).getLast? = some i ∧ tab.getD i none = none := by
  induction n generalizing col with
  | zero => rcases h : col.getLast? <;> simp_all
  | succ n ih =>
    cases hL : col.getLast? with
    | none =>
      have heq : reduceColFuel (n + 1) col tab M = col := by
        unfold reduceColFuel; simp [hL]
      rw [heq]; exact Or.inl hL
    | some i =>
      cases hT : tab.getD i none with
      | none =>
        have heq : reduceColFuel (n + 1) col tab M = col := by
          simp only [reduceColFuel, hL, hT]
        rw [heq]; exact Or.inr ⟨i, hL, hT⟩
      | some k =>
        have heq : reduceColFuel (n + 1) col tab M =
            reduceColFuel n (symmDiff col (M.getD k [])) tab M := by
          simp only [reduceColFuel, hL, hT]
        rw [heq]
        have hMlast : (M.getD k []).getLast? = some i := (htab.1 i k hT).2
        rcases symmDiff_getLast?_lt_r hL hc hMlast (hM k) with hnil | ⟨j, hj, hjlt⟩
        · left; rw [reduceColFuel_of_zero _ _ _ _ hnil]; exact hnil
        · apply ih
          · exact sd_sorted_ph col _ hc (hM k)
          · simp only [hj, Option.getD]; simp only [hL, Option.getD] at hf; omega

/-- İndirgeme sırasında tüm ara pivotlar fuel sayısından küçüktür. -/
private lemma reduceColFuel_bound_n (n : Nat) (col : Z2Col) (tab : PivotTab) (M : Z2Matrix)
    (htab : TabInv M tab)
    (hc : List.Pairwise (· < ·) col)
    (hM : ∀ k, List.Pairwise (· < ·) (M.getD k []))
    (hf : col.getLast?.getD 0 < n) :
    ∀ ci, (reduceColFuel n col tab M).getLast? = some ci → ci < n := by
  induction n generalizing col with
  | zero => exact (Nat.not_lt_zero _ hf).elim
  | succ n ih =>
    intro ci hci
    cases hL : col.getLast? with
    | none =>
      have heq : reduceColFuel (n + 1) col tab M = col := by simp only [reduceColFuel, hL]
      rw [heq, hL] at hci; exact absurd hci (by simp)
    | some p =>
      have hfp : p < n + 1 := by rwa [hL, Option.getD_some] at hf
      cases hT : tab.getD p none with
      | none =>
        have heq : reduceColFuel (n + 1) col tab M = col := by simp only [reduceColFuel, hL, hT]
        rw [heq, hL] at hci
        have hcp := Option.some.inj hci
        omega
      | some k =>
        have heq : reduceColFuel (n + 1) col tab M =
            reduceColFuel n (symmDiff col (M.getD k [])) tab M := by
          simp only [reduceColFuel, hL, hT]
        rw [heq] at hci
        have hMlast : (M.getD k []).getLast? = some p := (htab.1 p k hT).2
        rcases symmDiff_getLast?_lt_r hL hc hMlast (hM k) with hnil | ⟨j, hj, hjlt⟩
        · rw [reduceColFuel_of_zero _ _ _ _ hnil, hnil] at hci; exact absurd hci (by simp)
        · have hihf : (symmDiff col (M.getD k [])).getLast?.getD 0 < n := by
            rw [hj, Option.getD_some]; omega
          exact Nat.lt_succ_of_lt (ih _ (sd_sorted_ph col _ hc (hM k)) hihf ci hci)

/-- Bir sütunu indirgeme adımı. -/
def reduceCol (col : Z2Col) (tab : PivotTab) (M : Z2Matrix) : Z2Col :=
  reduceColFuel (col.getLast?.getD 0 + 1) col tab M

/-- Matrisin tamamını sol-sağ indirgeme. -/
def reduce (M : Z2Matrix) : Z2Matrix :=
  let tab : PivotTab := List.replicate M.length none
  let indexed := List.zipWith Prod.mk (List.range M.length) M
  (indexed.foldl (fun (acc : Z2Matrix × PivotTab) (jcol : Nat × Z2Col) =>
    let (accM, accTab) := acc
    let (j, col) := jcol
    let col' := reduceCol col accTab accM
    let accTab' := match col'.getLast? with
      | none   => accTab
      | some i => accTab.set i (some j)
    (accM ++ [col'], accTab')) ([], tab)).1

-- ──────────────────────────────────────────────────────────
-- 4b. reduce_is_reduced  (kanıtlandı)
-- ──────────────────────────────────────────────────────────

private def reduceStep (acc : Z2Matrix × PivotTab) (jcol : Nat × Z2Col) :
    Z2Matrix × PivotTab :=
  let (accM, accTab) := acc
  let (j, col) := jcol
  let col' := reduceCol col accTab accM
  let accTab' := match col'.getLast? with
    | none   => accTab
    | some i => accTab.set i (some j)
  (accM ++ [col'], accTab')

private def ReduceInv (accM : Z2Matrix) (accTab : PivotTab) (tabLen : Nat) : Prop :=
  tabLen = accTab.length ∧
  TabInv accM accTab ∧
  (∀ k, List.Pairwise (· < ·) (accM.getD k [])) ∧
  isReduced accM

private lemma reduceInv_init (n : Nat) :
    ReduceInv [] (List.replicate n none) n := by
  refine ⟨by simp, tabInv_nil n, ?_, ?_⟩
  · intro k; exact List.Pairwise.nil
  · intro j1; exact j1.elim0

private lemma reduceInv_step
    (accM : Z2Matrix) (accTab : PivotTab) (tabLen : Nat) (j : Nat) (col : Z2Col)
    (hInv   : ReduceInv accM accTab tabLen)
    (hj     : j = accM.length)
    (hcol_s : List.Pairwise (· < ·) col)
    (hcol_b : ∀ i ∈ col, i < tabLen) :
    ReduceInv (reduceStep (accM, accTab) (j, col)).1
              (reduceStep (accM, accTab) (j, col)).2
              tabLen := by
  obtain ⟨htabLen, htab, hMs, hred⟩ := hInv
  simp only [reduceStep]
  set col'    := reduceCol col accTab accM
  set accTab' := match col'.getLast? with
    | none   => accTab
    | some i => accTab.set i (some j)
  have hM_sorted : ∀ k, List.Pairwise (· < ·) (accM.getD k []) := hMs
  have hcol'_s : List.Pairwise (· < ·) col' :=
    reduceColFuel_sorted _ col accTab accM hcol_s hM_sorted
  have hcol'_free :
      col'.getLast? = none ∨
      ∃ i, col'.getLast? = some i ∧ accTab.getD i none = none :=
    reduceColFuel_free _ col accTab accM htab hcol_s hM_sorted (Nat.lt_succ_self _)
  have hcol'_bound : ∀ ci, col'.getLast? = some ci → ci < tabLen := by
    intro ci hci
    cases hL : col.getLast? with
    | none =>
      have hcol'_none : col'.getLast? = none := by
        have hcol'_def : col' = col := by
          show reduceColFuel (col.getLast?.getD 0 + 1) col accTab accM = col
          exact reduceColFuel_of_zero _ _ _ _ hL
        rw [hcol'_def, hL]
      rw [hcol'_none] at hci; exact absurd hci (by simp)
    | some p =>
      have hpm : p < tabLen := hcol_b p (getLast?_mem_ph' hL)
      have hlt_fuel : ci < col.getLast?.getD 0 + 1 :=
        reduceColFuel_bound_n _ col accTab accM htab hcol_s hM_sorted (Nat.lt_succ_self _) ci hci
      rw [hL, Option.getD_some] at hlt_fuel; omega
  -- 1. tabLen = accTab'.length
  have htabLen' : tabLen = accTab'.length := by
    simp only [accTab']
    split <;> simp [length_set_r, htabLen]
  -- 2. TabInv (accM ++ [col']) accTab'
  have htab' : TabInv (accM ++ [col']) accTab' := by
    constructor
    · intro i k hk
      rcases hfree : col'.getLast? with _ | ci
      · simp only [accTab', hfree] at hk
        obtain ⟨hklt, hklast⟩ := htab.1 i k hk
        exact ⟨by simp only [List.length_append, List.length_singleton]; omega,
               by rw [getD_append_left_r _ _ _ _ hklt]; exact hklast⟩
      · simp only [accTab', hfree] at hk
        by_cases hie : i = ci
        · have hci_lt : ci < tabLen := hcol'_bound ci hfree
          subst hie
          rw [getD_set_eq_r _ _ _ _ (by rw [← htabLen]; exact hci_lt)] at hk
          have hkj : k = j := (Option.some.inj hk).symm
          subst hkj; subst hj
          exact ⟨by simp, by rw [getD_snoc_last]; exact hfree⟩
        · rw [getD_set_ne_r _ _ _ _ _ (Ne.symm hie)] at hk
          obtain ⟨hklt, hklast⟩ := htab.1 i k hk
          exact ⟨by simp only [List.length_append, List.length_singleton]; omega,
                 by rw [getD_append_left_r _ _ _ _ hklt]; exact hklast⟩
    · intro k i hklt hklast
      rw [List.length_append, List.length_singleton] at hklt
      rcases Nat.lt_or_eq_of_le (Nat.lt_succ_iff.mp hklt) with hk | hk
      · have hklast_old : (accM.getD k []).getLast? = some i := by
          rwa [getD_append_left_r _ _ _ _ hk] at hklast
        have htab_k := htab.2 k i hk hklast_old
        rcases hfree : col'.getLast? with _ | ci
        · simp only [accTab', hfree]; exact htab_k
        · simp only [accTab', hfree]
          by_cases hie : i = ci
          · obtain ⟨ci', hci', hfree_none⟩ := hcol'_free.resolve_left (by simp [hfree])
            have hci_eq : ci' = ci := Option.some.inj (hci'.symm.trans hfree)
            subst hci_eq
            subst hie
            rw [htab_k] at hfree_none; exact absurd hfree_none (by simp)
          · rw [getD_set_ne_r _ _ _ _ _ (Ne.symm hie)]; exact htab_k
      · subst hk; subst hj
        have hklast_new : col'.getLast? = some i := by
          rwa [getD_snoc_last] at hklast
        rcases hfree : col'.getLast? with _ | ci
        · rw [hfree] at hklast_new; exact absurd hklast_new (by simp)
        · simp only [accTab', hfree]
          have hci : ci = i := Option.some.inj (hklast_new ▸ hfree ▸ rfl)
          have hi_lt : i < tabLen := hcol'_bound i hklast_new
          subst hci
          rw [getD_set_eq_r _ _ _ _ (by rw [← htabLen]; exact hi_lt)]
  -- 3. sortedness
  have hMs' : ∀ k, List.Pairwise (· < ·) ((accM ++ [col']).getD k []) := by
    intro k
    by_cases hk : k < accM.length
    · rw [getD_append_left_r _ _ _ _ hk]; exact hMs k
    · by_cases hk2 : k = accM.length
      · subst hk2; rw [getD_snoc_last]; exact hcol'_s
      · rw [getD_out_of_bounds _ _ _ (by simp; omega)]; exact List.Pairwise.nil
  -- 4. isReduced (accM ++ [col'])
  have hred' : isReduced (accM ++ [col']) := by
    intro j1 j2 hne
    have hlen : (accM ++ [col']).length = accM.length + 1 := by simp
    -- get of appended list (j typed to match j1/j2 exactly)
    have get_acc : ∀ (j : Fin (accM ++ [col']).length) (h : j.val < accM.length),
        (accM ++ [col']).get j = accM.get ⟨j.val, h⟩ := fun j h => by
      simp [List.getElem_append_left h]
    have get_col' : (accM ++ [col']).get ⟨accM.length, by simp⟩ = col' := by
      simp [List.getElem_append_right (Nat.le_refl _)]
    -- getD to get conversion (via universal helper, avoids dependency issues in induction)
    have getD_acc : ∀ (n : Nat) (h : n < accM.length),
        (accM.getD n []).getLast? = (accM.get ⟨n, h⟩).getLast? := by
      suffices key : ∀ (l : Z2Matrix) (n : Nat) (h : n < l.length), l.getD n [] = l.get ⟨n, h⟩ from
        fun n h => by rw [key accM n h]
      intro l
      induction l with
      | nil => intro n h; exact absurd h (by simp)
      | cons a t ih =>
        intro n h
        cases n with
        | zero => rfl
        | succ k => exact ih k (by simpa using h)
    have hj1_le : j1.val ≤ accM.length := by have := j1.isLt; omega
    have hj2_le : j2.val ≤ accM.length := by have := j2.isLt; omega
    rcases Nat.lt_or_eq_of_le hj1_le with hlt1 | heq1
    · rcases Nat.lt_or_eq_of_le hj2_le with hlt2 | heq2
      · -- Both in accM
        have hne' : (⟨j1.val, hlt1⟩ : Fin accM.length) ≠ ⟨j2.val, hlt2⟩ := by
          intro h; apply hne; ext
          exact (Fin.ext_iff (a := ⟨j1.val, hlt1⟩) (b := ⟨j2.val, hlt2⟩)).mp h
        have := hred ⟨j1.val, hlt1⟩ ⟨j2.val, hlt2⟩ hne'
        rw [get_acc j1 hlt1, get_acc j2 hlt2]; exact this
      · -- j1 in accM, j2 = col'
        have hj2 : j2 = ⟨accM.length, by simp⟩ := Fin.ext (by omega)
        rw [get_acc j1 hlt1, hj2, get_col']
        rcases hdi_eq : (accM.get ⟨j1.val, hlt1⟩).getLast? with _ | di
        · exact Or.inl rfl
        · right; intro heq
          rcases hcol'_free with hnil | ⟨ci, hci, hfree⟩
          · rw [hnil] at heq; exact absurd heq (Option.some_ne_none _)
          · have hdi : di = ci := Option.some.inj (heq.trans hci)
            have hgetD : (accM.getD j1.val []).getLast? = some di :=
              (getD_acc j1.val hlt1).trans hdi_eq
            exact absurd (htab.2 j1.val ci hlt1 (hdi ▸ hgetD))
              (by change ¬ (List.getD accTab ci none = some _); rw [hfree]; exact (Option.some_ne_none _).symm)
    · rcases Nat.lt_or_eq_of_le hj2_le with hlt2 | heq2
      · -- j1 = col', j2 in accM
        have hj1 : j1 = ⟨accM.length, by simp⟩ := Fin.ext (by omega)
        rw [hj1, get_col', get_acc j2 hlt2]
        rcases hcol'_free with hnil | ⟨ci, hci, hfree⟩
        · exact Or.inl hnil
        · rw [hci]; right; intro heq
          have hgetD : (accM.getD j2.val []).getLast? = some ci := by
            rw [getD_acc j2.val hlt2]; exact heq.symm
          exact absurd (htab.2 j2.val ci hlt2 hgetD)
            (by change ¬ (List.getD accTab ci none = some _); rw [hfree]; exact (Option.some_ne_none _).symm)
      · exact absurd (Fin.ext (by omega)) hne
  exact ⟨htabLen', htab', hMs', hred'⟩

-- getD to get: structural induction, independent of library naming
private lemma getD_eq_get_r {α : Type*} (l : List α) (d : α) (n : Nat) (h : n < l.length) :
    l.getD n d = l.get ⟨n, h⟩ := by
  induction l generalizing n with
  | nil => exact absurd h (by simp)
  | cons a t ih =>
    cases n with
    | zero => rfl
    | succ k => exact ih k (by simpa using h)

-- (zipWith Prod.mk (range M.length) M)[j] = (j, M.getD j [])
private lemma zipWith_range_getD (M : Z2Matrix) (j : Nat) (hj : j < M.length) :
    (List.zipWith Prod.mk (List.range M.length) M)[j]'(by simp [List.length_zipWith]; omega) =
    (j, M.getD j []) := by
  simp only [List.getElem_zipWith, List.getElem_range]
  congr 1
  exact (getD_eq_get_r M [] j hj).symm

/-- `reduce M`, sıralı ve sınırlı sütunlara sahip matrisler için `isReduced` koşulunu sağlar. -/
theorem reduce_is_reduced (M : Z2Matrix)
    (hsorted : ∀ col ∈ M, List.Pairwise (· < ·) col)
    (hbound  : ∀ col ∈ M, ∀ i ∈ col, i < M.length) :
    isReduced (reduce M) := by
  set indexed := List.zipWith Prod.mk (List.range M.length) M
  set tab     := List.replicate M.length none
  -- reduce M = (indexed.foldl reduceStep ([], tab)).1 by definitional equality
  show isReduced (indexed.foldl reduceStep ([], tab)).1
  -- indexed is equivalent to the range map (use getElem-based extensionality)
  have hIndexed : indexed = (List.range M.length).map (fun j => (j, M.getD j [])) := by
    apply List.ext_getElem
    · simp [indexed, List.length_zipWith]
    · intro i h1 h2
      simp only [List.getElem_map, List.getElem_range]
      exact zipWith_range_getD M i (by simp [indexed, List.length_zipWith] at h1; omega)
  -- Convert foldl over indexed to foldl over range
  have foldl_eq : indexed.foldl reduceStep ([], tab) =
      (List.range M.length).foldl (fun acc j => reduceStep acc (j, M.getD j [])) ([], tab) := by
    rw [hIndexed, List.foldl_map]
  rw [foldl_eq]
  -- Prove invariant by induction on k elements processed
  suffices h : ∀ k ≤ M.length,
      let acc := (List.range k).foldl (fun acc j => reduceStep acc (j, M.getD j [])) ([], tab)
      acc.1.length = k ∧ ReduceInv acc.1 acc.2 M.length by
    exact (h M.length (Nat.le_refl M.length)).2.2.2.2
  intro k hk
  induction k with
  | zero => exact ⟨rfl, reduceInv_init M.length⟩
  | succ n ih =>
    obtain ⟨hlen, hInv⟩ := ih (Nat.le_of_succ_le hk)
    have hn : n < M.length := Nat.lt_of_succ_le hk
    rw [List.range_succ, List.foldl_append]
    simp only [List.foldl_cons, List.foldl_nil]
    refine ⟨?_, ?_⟩
    · simp only [reduceStep, List.length_append, List.length_singleton] at hlen ⊢; omega
    · -- M.getD n [] sorted and bounded, via structural getD→get conversion
      -- getD_eq_get_r converts getD to List.get; List.get_mem gives membership
      have hgetD : M.getD n [] = M.get ⟨n, hn⟩ := getD_eq_get_r M [] n hn
      have hcol_s : List.Pairwise (· < ·) (M.getD n []) := by
        rw [hgetD]; exact hsorted _ (List.getElem_mem hn)
      have hcol_b : ∀ i ∈ M.getD n [], i < M.length := by
        rw [hgetD]; exact hbound _ (List.getElem_mem hn)
      -- hlen : acc.1.length = n, but reduceInv_step needs j = accM.length (i.e., n = acc.1.length)
      exact reduceInv_step _ _ M.length n (M.getD n []) hInv hlen.symm hcol_s hcol_b

-- ──────────────────────────────────────────────────────────
-- 5. Persistence çiftleri
-- ──────────────────────────────────────────────────────────

/-- İndirgeme sonucundan **persistence çiftleri**: `(doğum=i, ölüm=j)`. -/
def persistencePairs (M : Z2Matrix) : List (Nat × Nat) :=
  let red := reduce M
  (List.zipWith Prod.mk (List.range red.length) red).filterMap
    (fun (jcol : Nat × Z2Col) =>
      let (j, col) := jcol
      col.getLast?.map (fun i => (i, j)))

-- ──────────────────────────────────────────────────────────
-- 6. Persistence çiftlerinin özellikleri
-- ──────────────────────────────────────────────────────────

private lemma getLast?_mem_ph {col : Z2Col} {ci : Nat}
    (h : col.getLast? = some ci) : ci ∈ col := by
  induction col with
  | nil => simp at h
  | cons a t ih =>
    rcases t with _ | ⟨b, rest⟩
    · simp [List.getLast?] at h
      exact List.mem_cons.mpr (Or.inl h.symm)
    · have h' : (b :: rest).getLast? = some ci := h
      exact List.mem_cons.mpr (Or.inr (ih h'))

private lemma zipWith_map_fst_ph (l₁ : List Nat) (l₂ : List Z2Col) :
    (List.zipWith Prod.mk l₁ l₂).map Prod.fst = l₁.take l₂.length := by
  induction l₁ generalizing l₂ with
  | nil => simp
  | cons a t₁ ih =>
    cases l₂ with
    | nil => simp
    | cons b t₂ => simp [List.zipWith_cons_cons, ih]

private lemma filterMap_snd_in_fst_ph (jcols : List (Nat × Z2Col)) (j : Nat)
    (h : j ∈ (jcols.filterMap (fun p => p.2.getLast?.map (fun i => (i, p.1)))).map Prod.snd) :
    j ∈ jcols.map Prod.fst := by
  simp only [List.mem_map, List.mem_filterMap] at h
  obtain ⟨⟨a, b⟩, ⟨⟨k, c⟩, h_mem, h_some⟩, h_snd⟩ := h
  simp only [List.mem_map]
  rcases hc : c.getLast? with _ | ci
  · simp [hc] at h_some
  · simp only [hc, Option.map_some] at h_some
    have hkb : k = b := (Prod.mk.inj (Option.some.inj h_some)).2
    exact ⟨(k, c), h_mem, hkb.trans h_snd⟩

private lemma filterMap_snd_nodup_ph (jcols : List (Nat × Z2Col))
    (hnd : (jcols.map Prod.fst).Nodup) :
    ((jcols.filterMap (fun p => p.2.getLast?.map (fun i => (i, p.1)))).map Prod.snd).Nodup := by
  induction jcols with
  | nil => simp
  | cons head t ih =>
    obtain ⟨j, col⟩ := head
    simp only [List.map_cons, List.nodup_cons] at hnd
    obtain ⟨hj, hnd_t⟩ := hnd
    simp only [List.filterMap_cons]
    rcases col.getLast? with _ | i
    · simp only [Option.map_none]
      exact ih hnd_t
    · simp only [Option.map_some, List.map_cons, List.nodup_cons]
      exact ⟨fun hj_in => hj (filterMap_snd_in_fst_ph t j hj_in), ih hnd_t⟩

/-- Persistence çiftlerindeki ölüm indeksleri (j değerleri) birbirinden farklıdır.
    Kanıt yalnızca `List.range` yapısına dayanır; `reduce_is_reduced`'e bağlı değildir. -/
theorem pairs_have_distinct_deaths (M : Z2Matrix) :
    ((persistencePairs M).map Prod.snd).Nodup := by
  simp only [persistencePairs]
  apply filterMap_snd_nodup_ph
  rw [zipWith_map_fst_ph]
  simp [List.nodup_range]

/-- Alt-üçgen (lower-triangular) matris koşuluyla her persistence çiftinde doğum < ölüm.
    Koşul: `reduce M`'deki her `j`. sütununun tüm satır indeksleri `j`'den küçük. -/
theorem pairs_birth_lt_death (M : Z2Matrix)
    (hlt : ∀ jcol ∈ List.zipWith Prod.mk (List.range (reduce M).length) (reduce M),
           ∀ x ∈ jcol.2, x < jcol.1) :
    ∀ p ∈ persistencePairs M, p.1 < p.2 := by
  intro p hp
  simp only [persistencePairs, List.mem_filterMap] at hp
  obtain ⟨⟨k, col⟩, h_mem, h_some⟩ := hp
  rcases hcol : col.getLast? with _ | ci
  · simp [hcol] at h_some
  · simp only [hcol, Option.map_some] at h_some
    have h_eq : (ci, k) = p := Option.some.inj h_some
    have hci_in : ci ∈ col := getLast?_mem_ph hcol
    rw [← h_eq]
    exact hlt (k, col) h_mem ci hci_in

end PersHomology
