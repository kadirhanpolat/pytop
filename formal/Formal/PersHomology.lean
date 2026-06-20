import Mathlib.Data.List.Basic
import Mathlib.Data.List.Pairwise

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
-- 5. Persistence çiftleri
-- ──────────────────────────────────────────────────────────

/-- İndirgeme sonucundan **persistence çiftleri**: `(doğum=i, ölüm=j)`. -/
def persistencePairs (M : Z2Matrix) : List (Nat × Nat) :=
  let red := reduce M
  (List.zipWith Prod.mk (List.range red.length) red).filterMap
    (fun (jcol : Nat × Z2Col) =>
      let (j, col) := jcol
      col.getLast?.map (fun i => (i, j)))

end PersHomology
