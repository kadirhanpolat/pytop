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

/-- Bir sütunu indirgeme adımı. `partial` — terminasyon pivot'un azalmasına dayanır,
    burada formal ispat ertelenmiştir. -/
partial def reduceCol (col : Z2Col) (tab : PivotTab) (M : Z2Matrix) : Z2Col :=
  match col.getLast? with
  | none   => col
  | some i =>
    match tab.getD i none with
    | none   => col
    | some k =>
      reduceCol (symmDiff col (M.getD k [])) tab M

/-- Matrisin tamamını sol-sağ indirgeme.
    `List.zipWith Prod.mk (List.range n) M` yerine enumerasyon için. -/
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
-- 4b. reduce_is_reduced  (ertelenmiş)
-- ──────────────────────────────────────────────────────────

-- TODO(formal): `reduceCol` şu an `partial def` olduğundan Lean kernel'i
-- terminasyon certificate üretmiyor ve bu theorem hakkında structural/well-founded
-- induction yapılamıyor.  Tam kanıt için iki yol:
--   A) `reduceCol`'u fuel-based `def`'e çevir (n : Nat parametresi ekle),
--   B) `termination_by col.getLast?.getD 0` ile `reduce`+`reduceCol`'un
--      ortak invariantını mutual induction ile kanıtla
--      (invariant: tab[i] = some k ↔ (M[k]).getLast? = some i).
-- Matematiksel doğruluk açık; sadece Lean altyapısı eksik.
/-- `reduce M`, `isReduced` koşulunu sağlar.
    **[sorry]** — `partial def reduceCol` terminasyon kanıtı bekliyor. -/
theorem reduce_is_reduced (M : Z2Matrix) : isReduced (reduce M) := by
  sorry

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
