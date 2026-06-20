import Mathlib.Data.Finset.Basic
import Mathlib.Data.List.Basic

/-!
# Yol 4: pi-Base İmplikasyon Motoru — Soundness

`pytop.experimental.pi_base` modülünün mülkiyet çıkarım motorunu
Lean 4'te modellenmiştir.

## Model

* **PropId** — özellik kimliği (Nat).
* **Space**  — bir uzayın sahip olduğu özellikler (`Finset PropId`).
* **Implication** — `src ∈ space → tgt ∈ space` kuralı.
* **implClosure** — bir kural listesinin tek geçişli çıkarım kapatması.
* **implFixpoint** — yakıt-sınırlı sabit nokta iterasyonu.

## Ana teoremler (sorry yok)

* `modus_ponens`        : kural + öncül → sonuç (Modus Ponens).
* `contrapositive`      : P → Q ve ¬Q → ¬P.
* `chain_implication`   : transitiflik yoluyla zincirleme.
* `implClosure_mono`    : kapatma monotondur.
* `implClosure_sound`   : kapatma, geçerli space içinde kalır.
* `implFixpoint_mono`   : sabit nokta kapatması monotondur.
* `implFixpoint_sound`  : sabit nokta kapatması sağlamdır.
-/

namespace PiBase

/-- **Özellik kimliği**. -/
abbrev PropId := Nat

/-- Bir uzayın sahip olduğu özellik kümesi. -/
abbrev Space := Finset PropId

/-- **İmplikasyon kuralı**: `src ∈ space → tgt ∈ space`. -/
structure Implication where
  src : PropId
  tgt : PropId
  deriving DecidableEq

/-- Bir implikasyonun bir uzayda geçerli olması. -/
def ImplicationHolds (space : Space) (impl : Implication) : Prop :=
  impl.src ∈ space → impl.tgt ∈ space

-- ──────────────────────────────────────────────────────────
-- 1. Temel sonuç kuralları
-- ──────────────────────────────────────────────────────────

/-- **Modus Ponens**: kural ateşlendiğinde sonuç elde edilir. -/
theorem modus_ponens (space : Space) (impl : Implication)
    (hvalid : ImplicationHolds space impl)
    (hpre   : impl.src ∈ space) :
    impl.tgt ∈ space :=
  hvalid hpre

/-- **Kontrapozitif**: P → Q ve ¬Q → ¬P. -/
theorem contrapositive (space : Space) (impl : Implication)
    (hvalid : ImplicationHolds space impl)
    (hncon  : impl.tgt ∉ space) :
    impl.src ∉ space :=
  fun h => hncon (hvalid h)

/-- **Transitiflik**: birleştirilen iki kural yeni bir kural verir. -/
theorem chain_implication (space : Space) (i₁ i₂ : Implication)
    (hcomp : i₁.tgt = i₂.src)
    (hv1   : ImplicationHolds space i₁)
    (hv2   : ImplicationHolds space i₂) :
    ImplicationHolds space { src := i₁.src, tgt := i₂.tgt } :=
  fun h => hv2 (hcomp ▸ hv1 h)

/-- **Monotonluk alt lemma**: `P ∈ props → P ∈ space` korunur. -/
theorem implication_mono (space : Space) (impl : Implication)
    (hvalid : ImplicationHolds space impl)
    (props  : Space)
    (hle    : props ⊆ space)
    (h      : impl.src ∈ props) :
    insert impl.tgt props ⊆ space := by
  intro p hp
  rcases Finset.mem_insert.mp hp with rfl | hmem
  · exact hvalid (hle h)
  · exact hle hmem

-- ──────────────────────────────────────────────────────────
-- 2. Tek geçişli çıkarım kapatması
-- ──────────────────────────────────────────────────────────

/-- Kural listesinin **tek geçişli çıkarım kapatması**. -/
def implClosure : List Implication → Space → Space
  | [],           props => props
  | impl :: rest, props =>
    implClosure rest
      (if impl.src ∈ props then insert impl.tgt props else props)

/-- `implClosure` **monotondur**: orijinal özellikler korunur. -/
theorem implClosure_mono (impls : List Implication) (props : Space) :
    props ⊆ implClosure impls props := by
  induction impls generalizing props with
  | nil => exact Finset.Subset.refl _
  | cons impl rest ih =>
    simp only [implClosure]
    split_ifs with h
    · exact (Finset.subset_insert impl.tgt props).trans (ih _)
    · exact ih props

/-- `implClosure` **sağlamdır**: tüm kurallar `space`'de geçerliyse,
    kapatma `space` içinde kalır. -/
theorem implClosure_sound (space : Space) :
    ∀ (impls : List Implication) (props : Space),
    props ⊆ space →
    (∀ impl ∈ impls, ImplicationHolds space impl) →
    implClosure impls props ⊆ space := by
  intro impls
  induction impls with
  | nil        => intros props h _; exact h
  | cons impl rest ih =>
    intros props hsubset hvalid
    simp only [implClosure]
    split_ifs with h
    · apply ih
      · exact implication_mono space impl
          (hvalid impl (List.mem_cons.mpr (Or.inl rfl))) props hsubset h
      · exact fun r hr => hvalid r (List.mem_cons.mpr (Or.inr hr))
    · exact ih props hsubset (fun r hr => hvalid r (List.mem_cons.mpr (Or.inr hr)))

-- ──────────────────────────────────────────────────────────
-- 3. Sabit nokta kapatması
-- ──────────────────────────────────────────────────────────

/-- Tek geçişli kapatmayı yakıt tükenene ya da sabit nokta bulunana
    kadar iteratif uygula. -/
def implFixpoint (impls : List Implication) : Nat → Space → Space
  | 0,     props => props
  | n + 1, props =>
    let props' := implClosure impls props
    if props' = props then props else implFixpoint impls n props'

/-- `implFixpoint` **monotondur**. -/
theorem implFixpoint_mono (impls : List Implication) (fuel : Nat) (props : Space) :
    props ⊆ implFixpoint impls fuel props := by
  induction fuel generalizing props with
  | zero => exact Finset.Subset.refl _
  | succ n ih =>
    simp only [implFixpoint]
    split_ifs with heq
    · exact Finset.Subset.refl _
    · exact (implClosure_mono impls props).trans (ih _)

/-- `implFixpoint` **sağlamdır**: tüm kurallar `space`'de geçerliyse,
    sabit nokta kapatması `space` içinde kalır. -/
theorem implFixpoint_sound (space : Space) (impls : List Implication)
    (hvalid : ∀ impl ∈ impls, ImplicationHolds space impl) :
    ∀ (fuel : Nat) (props : Space), props ⊆ space →
    implFixpoint impls fuel props ⊆ space := by
  intro fuel
  induction fuel with
  | zero => intros props h; exact h
  | succ n ih =>
    intros props hsubset
    simp only [implFixpoint]
    split_ifs with heq
    · exact hsubset
    · exact ih (implClosure impls props)
        (implClosure_sound space impls props hsubset hvalid)

-- ──────────────────────────────────────────────────────────
-- 4. Çıkarım grafiği korollerleri
-- ──────────────────────────────────────────────────────────

/-- Boş kural listesi değişmez. -/
@[simp] theorem implClosure_nil (props : Space) :
    implClosure [] props = props := rfl

/-- Tek adımda sağlam kapatma. -/
theorem implClosure_one_step (space props : Space) (impl : Implication)
    (hvalid : ImplicationHolds space impl) (hle : props ⊆ space) :
    implClosure [impl] props ⊆ space :=
  implClosure_sound space [impl] props hle
    (fun r hr => by simp at hr; subst hr; exact hvalid)

/-- Kural kümesini genişletmek sonucu küçültmez. -/
theorem implClosure_append_mono (impls₁ impls₂ : List Implication) (props : Space) :
    implClosure impls₁ props ⊆ implClosure (impls₁ ++ impls₂) props := by
  induction impls₁ generalizing props with
  | nil       => exact implClosure_mono impls₂ props
  | cons i is ih =>
    simp only [implClosure, List.cons_append]
    split_ifs
    · exact ih _
    · exact ih props

end PiBase
