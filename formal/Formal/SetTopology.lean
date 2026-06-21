import Mathlib.Data.Set.Basic
import Mathlib.Data.Set.Lattice

/-!
# Yol 5: Küme Teorik Topoloji

Filtre kullanmadan, doğrudan **açık kümeler ailesi** üzerinden topolojik uzay
aksiyomları, ayrılma özellikleri, kapalı kümeler ve süreklilik.

## Yapı

* `Topology α`    — açık küme aksiyomlarını sağlayan yapı.
* `isT0 / isT1 / isT2` — Kolmogorov, Fréchet, Hausdorff ayrılma aksiyomları.
* `isClosed`      — tümleyeni açık olan küme.
* `isContinuous`  — ön görüntü açık kümeyi açık kümeye götürür.
* `isCompact`     — her açık örtünün sonlu alt örtüsü vardır.

## Kanıtlanan teoremler (sorry yok)

* `t2_implies_t1`              : T2 → T1
* `t1_implies_t0`              : T1 → T0
* `t2_implies_t0`              : T2 → T0 (geçişli)
* `closed_empty / univ`        : ∅ ve univ kapalıdır
* `closed_inter`               : iki kapalının kesişimi kapalıdır  (De Morgan)
* `closed_union`               : iki kapalının birleşimi kapalıdır (De Morgan)
* `continuous_const / id`      : sabit ve özdeşlik fonksiyonları süreklidir
* `continuous_comp`            : bileşim süreklidir
* `continuous_preimage_closed` : kapalının ön görüntüsü kapalıdır
* `compact_empty`              : boş küme kompakttır
* `compact_singleton`          : tek noktalı küme kompakttır
-/

namespace SetTopology

variable {α β γ : Type*}

-- ──────────────────────────────────────────────────────────
-- 1. Topolojik uzay yapısı
-- ──────────────────────────────────────────────────────────

/-- Açık küme aksiyomlarını sağlayan **topolojik uzay** yapısı. -/
structure Topology (α : Type*) where
  isOpen : Set α → Prop
  empty_open : isOpen ∅
  univ_open : isOpen Set.univ
  union_open : ∀ (F : Set (Set α)), (∀ s, s ∈ F → isOpen s) → isOpen (⋃₀ F)
  inter_open : ∀ (U V : Set α), isOpen U → isOpen V → isOpen (U ∩ V)

-- ──────────────────────────────────────────────────────────
-- 2. Türetilmiş açık küme lemması
-- ──────────────────────────────────────────────────────────

/-- İki açık kümenin birleşimi açıktır. -/
theorem open_union (τ : Topology α) {U V : Set α}
    (hU : τ.isOpen U) (hV : τ.isOpen V) : τ.isOpen (U ∪ V) := by
  have heq : U ∪ V = ⋃₀ (setOf fun s => s = U ∨ s = V) := by
    ext x
    simp only [Set.mem_union, Set.mem_sUnion, Set.mem_setOf_eq]
    constructor
    · intro hx
      cases hx with
      | inl h => exact ⟨U, Or.inl rfl, h⟩
      | inr h => exact ⟨V, Or.inr rfl, h⟩
    · intro ⟨s, hs, hxs⟩
      cases hs with
      | inl h => exact Or.inl (h ▸ hxs)
      | inr h => exact Or.inr (h ▸ hxs)
  rw [heq]
  apply τ.union_open
  intro s hs
  simp only [Set.mem_setOf_eq] at hs
  cases hs with
  | inl h => exact h ▸ hU
  | inr h => exact h ▸ hV

-- ──────────────────────────────────────────────────────────
-- 3. Ayrılma aksiyomları
-- ──────────────────────────────────────────────────────────

/-- **T0 (Kolmogorov)**: iki farklı noktayı ayıran açık küme vardır. -/
def isT0 (τ : Topology α) : Prop :=
  ∀ x y : α, x ≠ y → ∃ U, τ.isOpen U ∧ (x ∈ U ↔ y ∉ U)

/-- **T1 (Fréchet)**: her farklı x, y için x'i içerip y'yi dışarıda bırakan
    açık küme vardır. -/
def isT1 (τ : Topology α) : Prop :=
  ∀ x y : α, x ≠ y → ∃ U, τ.isOpen U ∧ x ∈ U ∧ y ∉ U

/-- **T2 (Hausdorff)**: her iki farklı nokta ayrık açık kümelerle ayrılır. -/
def isT2 (τ : Topology α) : Prop :=
  ∀ x y : α, x ≠ y →
    ∃ U V, τ.isOpen U ∧ τ.isOpen V ∧ x ∈ U ∧ y ∈ V ∧ U ∩ V = ∅

-- ──────────────────────────────────────────────────────────
-- 4. Ayrılma zinciri: T2 → T1 → T0
-- ──────────────────────────────────────────────────────────

/-- Her Hausdorff uzayı T1'dir. -/
theorem t2_implies_t1 (τ : Topology α) (h : isT2 τ) : isT1 τ := by
  intro x y hne
  obtain ⟨U, V, hU, _hV, hxU, hyV, hdisj⟩ := h x y hne
  refine ⟨U, hU, hxU, ?_⟩
  intro hyU
  have hmem : y ∈ U ∩ V := Set.mem_inter hyU hyV
  rw [hdisj] at hmem
  exact hmem

/-- Her T1 uzayı T0'dır. -/
theorem t1_implies_t0 (τ : Topology α) (h : isT1 τ) : isT0 τ := by
  intro x y hne
  obtain ⟨U, hU, hxU, hyU⟩ := h x y hne
  exact ⟨U, hU, ⟨fun _ => hyU, fun _ => hxU⟩⟩

/-- **Zincir**: T2 → T0. -/
theorem t2_implies_t0 (τ : Topology α) (h : isT2 τ) : isT0 τ :=
  t1_implies_t0 τ (t2_implies_t1 τ h)

-- ──────────────────────────────────────────────────────────
-- 5. Kapalı kümeler
-- ──────────────────────────────────────────────────────────

/-- **Kapalı küme**: tümleyeni açık olan küme. -/
def isClosed (τ : Topology α) (C : Set α) : Prop := τ.isOpen Cᶜ

/-- Boş küme kapalıdır. -/
theorem closed_empty (τ : Topology α) : isClosed τ ∅ := by
  unfold isClosed
  have h : (∅ : Set α)ᶜ = Set.univ := by ext; simp
  rw [h]; exact τ.univ_open

/-- Evrensel küme kapalıdır. -/
theorem closed_univ (τ : Topology α) : isClosed τ Set.univ := by
  unfold isClosed
  have h : (Set.univ : Set α)ᶜ = ∅ := by ext; simp
  rw [h]; exact τ.empty_open

/-- İki kapalı kümenin kesişimi kapalıdır. De Morgan: (C ∩ D)ᶜ = Cᶜ ∪ Dᶜ -/
theorem closed_inter (τ : Topology α) {C D : Set α}
    (hC : isClosed τ C) (hD : isClosed τ D) : isClosed τ (C ∩ D) := by
  unfold isClosed at *
  have h : (C ∩ D)ᶜ = Cᶜ ∪ Dᶜ := by
    ext x
    simp only [Set.mem_compl_iff, Set.mem_inter_iff, Set.mem_union, not_and_or]
  rw [h]; exact open_union τ hC hD

/-- İki kapalı kümenin birleşimi kapalıdır. De Morgan: (C ∪ D)ᶜ = Cᶜ ∩ Dᶜ -/
theorem closed_union (τ : Topology α) {C D : Set α}
    (hC : isClosed τ C) (hD : isClosed τ D) : isClosed τ (C ∪ D) := by
  unfold isClosed at *
  have h : (C ∪ D)ᶜ = Cᶜ ∩ Dᶜ := by
    ext x
    simp only [Set.mem_compl_iff, Set.mem_union, Set.mem_inter_iff, not_or]
  rw [h]; exact τ.inter_open _ _ hC hD

-- ──────────────────────────────────────────────────────────
-- 6. Sürekli fonksiyonlar
-- ──────────────────────────────────────────────────────────

/-- **Süreklilik**: her açık kümenin ön görüntüsü açıktır. -/
def isContinuous (τ : Topology α) (σ : Topology β) (f : α → β) : Prop :=
  ∀ V : Set β, σ.isOpen V → τ.isOpen (f ⁻¹' V)

/-- Sabit fonksiyon süreklidir. -/
theorem continuous_const (τ : Topology α) (σ : Topology β) (b : β) :
    isContinuous τ σ (fun _ => b) := by
  intro V _hV
  by_cases hb : b ∈ V
  · have : (fun (_ : α) => b) ⁻¹' V = Set.univ := by ext; simp [hb]
    rw [this]; exact τ.univ_open
  · have : (fun (_ : α) => b) ⁻¹' V = ∅ := by ext; simp [hb]
    rw [this]; exact τ.empty_open

/-- Özdeşlik fonksiyonu süreklidir. -/
theorem continuous_id (τ : Topology α) : isContinuous τ τ id :=
  fun _V hV => hV

/-- Süreklilerin bileşimi süreklidir. -/
theorem continuous_comp
    (τ : Topology α) (σ : Topology β) (ρ : Topology γ)
    {f : α → β} {g : β → γ}
    (hf : isContinuous τ σ f) (hg : isContinuous σ ρ g) :
    isContinuous τ ρ (g ∘ f) :=
  fun W hW => hf _ (hg W hW)

/-- Sürekli fonksiyonlar kapalı kümelerin ön görüntüsünü kapalı tutar. -/
theorem continuous_preimage_closed
    (τ : Topology α) (σ : Topology β)
    {f : α → β} (hf : isContinuous τ σ f)
    {C : Set β} (hC : isClosed σ C) : isClosed τ (f ⁻¹' C) := by
  unfold isClosed at *
  have h : (f ⁻¹' C)ᶜ = f ⁻¹' Cᶜ := by
    ext x
    simp only [Set.mem_compl_iff, Set.mem_preimage]
  rw [h]; exact hf _ hC

-- ──────────────────────────────────────────────────────────
-- 7. Kompaktlık
-- ──────────────────────────────────────────────────────────

/-- **Kompakt küme**: her açık örtünün sonlu alt örtüsü vardır.
    Sonlu alt örtü `Fin n → Set α` ile modellenir. -/
def isCompact (τ : Topology α) (K : Set α) : Prop :=
  ∀ (F : Set (Set α)),
    (∀ s, s ∈ F → τ.isOpen s) →
    K ⊆ ⋃₀ F →
    ∃ (n : ℕ) (G : Fin n → Set α), (∀ i, G i ∈ F) ∧ K ⊆ ⋃ i, G i

/-- Boş küme kompakttır. -/
theorem compact_empty (τ : Topology α) : isCompact τ ∅ := by
  intro _F _hF _hcover
  exact ⟨0, Fin.elim0, fun i => i.elim0, Set.empty_subset _⟩

/-- Tek noktalı küme kompakttır. -/
theorem compact_singleton (τ : Topology α) (x : α) : isCompact τ {x} := by
  intro F _hF hcover
  have hx : x ∈ ⋃₀ F := hcover (Set.mem_singleton x)
  rw [Set.mem_sUnion] at hx
  obtain ⟨U, hUF, hxU⟩ := hx
  refine ⟨1, fun _ => U, fun _ => hUF, ?_⟩
  intro y hy
  simp only [Set.mem_singleton_iff] at hy
  subst hy
  exact Set.mem_iUnion.mpr ⟨0, hxU⟩

-- ──────────────────────────────────────────────────────────
-- 8. İç operatörü
-- ──────────────────────────────────────────────────────────

/-- Bir kümenin **iç noktaları**: A'nın içinde kalan tüm açık kümelerin birleşimi. -/
def interior (τ : Topology α) (A : Set α) : Set α :=
  ⋃₀ {U | τ.isOpen U ∧ U ⊆ A}

/-- İç bölge açıktır. -/
theorem interior_open (τ : Topology α) (A : Set α) : τ.isOpen (interior τ A) := by
  unfold interior
  apply τ.union_open
  intro s hs
  exact hs.1

/-- İç bölge kümenin içindedir: int(A) ⊆ A. -/
theorem interior_subset (τ : Topology α) (A : Set α) : interior τ A ⊆ A := by
  intro x hx
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hx
  obtain ⟨U, ⟨_, hUA⟩, hxU⟩ := hx
  exact hUA hxU

/-- A açık ⟺ A = int(A). -/
theorem open_iff_eq_interior (τ : Topology α) {A : Set α} :
    τ.isOpen A ↔ A = interior τ A := by
  constructor
  · intro hA
    apply Set.Subset.antisymm
    · intro x hxA
      simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq]
      exact ⟨A, ⟨hA, fun _ hh => hh⟩, hxA⟩
    · exact interior_subset τ A
  · intro h; rw [h]; exact interior_open τ A

/-- Açık kümeler iç bölgelerini içerir: A açık, A ⊆ B → A ⊆ int(B). -/
theorem open_subset_interior (τ : Topology α) {A B : Set α}
    (hA : τ.isOpen A) (hAB : A ⊆ B) : A ⊆ interior τ B := by
  intro x hxA
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq]
  exact ⟨A, ⟨hA, hAB⟩, hxA⟩

/-- İç operatörü monotondur: A ⊆ B → int(A) ⊆ int(B). -/
theorem interior_mono (τ : Topology α) {A B : Set α} (h : A ⊆ B) :
    interior τ A ⊆ interior τ B := by
  intro x hx
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hx ⊢
  obtain ⟨U, ⟨hU, hUA⟩, hxU⟩ := hx
  exact ⟨U, ⟨hU, hUA.trans h⟩, hxU⟩

-- ──────────────────────────────────────────────────────────
-- 9. Kapanış operatörü
-- ──────────────────────────────────────────────────────────

/-- Bir kümenin **kapanışı**: A'yı içeren tüm kapalı kümelerin kesişimi. -/
def closure (τ : Topology α) (A : Set α) : Set α :=
  ⋂₀ {C | isClosed τ C ∧ A ⊆ C}

/-- Kapanış kapalıdır. -/
theorem closure_closed (τ : Topology α) (A : Set α) : isClosed τ (closure τ A) := by
  simp only [isClosed, closure]
  rw [Set.compl_sInter]
  apply τ.union_open
  intro s hs
  simp only [Set.mem_image, Set.mem_setOf_eq] at hs
  obtain ⟨C, ⟨hCclosed, _⟩, rfl⟩ := hs
  exact hCclosed

/-- Küme kendi kapanışının içindedir: A ⊆ cl(A). -/
theorem subset_closure (τ : Topology α) (A : Set α) : A ⊆ closure τ A := by
  intro x hxA
  simp only [closure, Set.mem_sInter, Set.mem_setOf_eq]
  intro C ⟨_, hAC⟩
  exact hAC hxA

/-- A kapalı ↔ cl(A) = A. -/
theorem closed_iff_eq_closure (τ : Topology α) {A : Set α} :
    isClosed τ A ↔ closure τ A = A := by
  constructor
  · intro hA
    apply Set.Subset.antisymm
    · simp only [closure]
      apply Set.sInter_subset_of_mem
      exact ⟨hA, fun _ hh => hh⟩
    · exact subset_closure τ A
  · intro h; rw [← h]; exact closure_closed τ A

/-- Kapanış operatörü monotondur: A ⊆ B → cl(A) ⊆ cl(B). -/
theorem closure_mono (τ : Topology α) {A B : Set α} (h : A ⊆ B) :
    closure τ A ⊆ closure τ B := by
  simp only [closure]
  apply Set.sInter_subset_sInter
  intro C ⟨hCclosed, hBC⟩
  exact ⟨hCclosed, h.trans hBC⟩

/-- Kapanış idempotentir: cl(cl(A)) = cl(A). -/
theorem closure_closure (τ : Topology α) (A : Set α) :
    closure τ (closure τ A) = closure τ A :=
  (closed_iff_eq_closure τ).mp (closure_closed τ A)

-- ──────────────────────────────────────────────────────────
-- 10. Sınır operatörü
-- ──────────────────────────────────────────────────────────

/-- Bir kümenin **sınırı**: kapanış eksi iç bölge. -/
def boundary (τ : Topology α) (A : Set α) : Set α :=
  closure τ A \ interior τ A

/-- Sınır kapalıdır. -/
theorem boundary_closed (τ : Topology α) (A : Set α) : isClosed τ (boundary τ A) := by
  unfold boundary isClosed
  have heq : (closure τ A \ interior τ A)ᶜ = (closure τ A)ᶜ ∪ interior τ A := by
    ext x
    simp only [Set.mem_compl_iff, Set.mem_sdiff, Set.mem_union, Set.mem_compl_iff]
    constructor
    · intro hx
      rcases Classical.em (x ∈ closure τ A) with h | h
      · exact Or.inr (not_not.mp fun h' => hx ⟨h, h'⟩)
      · exact Or.inl h
    · intro hx ⟨h1, h2⟩
      rcases hx with h | h
      · exact h h1
      · exact h2 h
  rw [heq]
  exact open_union τ (closure_closed τ A) (interior_open τ A)

/-- Sınır, kapanışın içindedir: ∂A ⊆ cl(A). -/
theorem boundary_subset_closure (τ : Topology α) (A : Set α) :
    boundary τ A ⊆ closure τ A :=
  fun _ hx => hx.1

/-- İç bölge ile sınır ayrıktır: int(A) ∩ ∂A = ∅. -/
theorem interior_disjoint_boundary (τ : Topology α) (A : Set α) :
    interior τ A ∩ boundary τ A = ∅ := by
  ext x
  simp only [Set.mem_inter_iff, boundary, Set.mem_sdiff, Set.mem_empty_iff_false]
  constructor
  · intro ⟨hx, _, hnx⟩; exact hnx hx
  · exact False.elim

/-- Kapanış = iç bölge ∪ sınır: cl(A) = int(A) ∪ ∂A. -/
theorem closure_eq_interior_union_boundary (τ : Topology α) (A : Set α) :
    closure τ A = interior τ A ∪ boundary τ A := by
  ext x
  simp only [boundary, Set.mem_union, Set.mem_sdiff]
  constructor
  · intro hx
    by_cases h : x ∈ interior τ A
    · exact Or.inl h
    · exact Or.inr ⟨hx, h⟩
  · intro hx
    rcases hx with hx | ⟨hx, _⟩
    · exact subset_closure τ A (interior_subset τ A hx)
    · exact hx

-- ──────────────────────────────────────────────────────────
-- 11. Kuratowski kapanış aksiyomları
-- ──────────────────────────────────────────────────────────

/-- Kuratowski 4. aksiyomu: cl(A ∪ B) = cl(A) ∪ cl(B). -/
theorem closure_union (τ : Topology α) (A B : Set α) :
    closure τ (A ∪ B) = closure τ A ∪ closure τ B := by
  apply Set.Subset.antisymm
  · -- cl(A ∪ B) ⊆ cl(A) ∪ cl(B)
    -- cl(A) ∪ cl(B) is closed (by closed_union) and contains A ∪ B
    apply Set.sInter_subset_of_mem
    simp only [closure, Set.mem_setOf_eq]
    constructor
    · exact closed_union τ (closure_closed τ A) (closure_closed τ B)
    · exact Set.union_subset_union (subset_closure τ A) (subset_closure τ B)
  · -- cl(A) ∪ cl(B) ⊆ cl(A ∪ B)
    apply Set.union_subset
    · exact closure_mono τ (Set.subset_union_left)
    · exact closure_mono τ (Set.subset_union_right)

/-- Kuratowski aksiyomları özeti (4 özellik). -/
theorem kuratowski_axioms (τ : Topology α) (A B : Set α) :
    closure τ ∅ = ∅ ∧
    A ⊆ closure τ A ∧
    closure τ (closure τ A) = closure τ A ∧
    closure τ (A ∪ B) = closure τ A ∪ closure τ B := by
  exact ⟨(closed_iff_eq_closure τ).mp (closed_empty τ),
         subset_closure τ A, closure_closure τ A, closure_union τ A B⟩

-- ──────────────────────────────────────────────────────────
-- 12. Altuzay topolojisi
-- ──────────────────────────────────────────────────────────

/-- `S` alt kümesi üzerinde τ tarafından indüklenen **altuzay topolojisi**. -/
def subtopology (τ : Topology α) (S : Set α) : Topology S where
  isOpen V := ∃ U : Set α, τ.isOpen U ∧ V = (fun x : S => x.val) ⁻¹' U
  empty_open := ⟨∅, τ.empty_open, by ext ⟨_, _⟩; simp⟩
  univ_open  := ⟨Set.univ, τ.univ_open, by ext ⟨_, _⟩; simp⟩
  union_open := by
    intro F hF
    let G := {U : Set α | ∃ V ∈ F, τ.isOpen U ∧ V = (fun x : S => x.val) ⁻¹' U}
    refine ⟨⋃₀ G, τ.union_open G (fun s hs => ?_), ?_⟩
    · simp only [G, Set.mem_setOf_eq] at hs; obtain ⟨_, _, hso, _⟩ := hs; exact hso
    · ext ⟨x, _⟩
      constructor
      · intro hx
        obtain ⟨V, hVF, hxV⟩ := Set.mem_sUnion.mp hx
        obtain ⟨U, hUo, heq⟩ := hF V hVF; subst heq
        exact Set.mem_sUnion.mpr ⟨U, ⟨_, hVF, hUo, rfl⟩, hxV⟩
      · intro hx
        obtain ⟨U, hUmem, hxU⟩ := Set.mem_sUnion.mp hx
        simp only [G, Set.mem_setOf_eq] at hUmem
        obtain ⟨V, hVF, -, heq⟩ := hUmem; subst heq
        exact Set.mem_sUnion.mpr ⟨_, hVF, hxU⟩
  inter_open := by
    intro U V hU hV
    obtain ⟨P, hPo, rfl⟩ := hU
    obtain ⟨Q, hQo, rfl⟩ := hV
    refine ⟨P ∩ Q, τ.inter_open P Q hPo hQo, ?_⟩
    ext ⟨x, _⟩
    simp only [Set.mem_inter_iff, Set.mem_preimage]

/-- Altuzay açık kümeleri, büyük uzayın açık kümelerinin izi. -/
theorem subtopology_open_iff (τ : Topology α) (S : Set α) (V : Set S) :
    (subtopology τ S).isOpen V ↔
    ∃ U : Set α, τ.isOpen U ∧ V = (fun x : S => x.val) ⁻¹' U :=
  Iff.rfl

/-- Büyük uzayda açık olan kümenin altuzaydaki izi açıktır. -/
theorem subtopology_open_of_open (τ : Topology α) (S : Set α) (U : Set α)
    (hU : τ.isOpen U) : (subtopology τ S).isOpen ((fun x : S => x.val) ⁻¹' U) :=
  ⟨U, hU, rfl⟩

-- ──────────────────────────────────────────────────────────
-- 13. Ürün topolojisi
-- ──────────────────────────────────────────────────────────

/-- `α × β` üzerinde **ürün topolojisi**: her noktanın silindir komşuluğu vardır. -/
def prodTopology (τ : Topology α) (σ : Topology β) : Topology (α × β) where
  isOpen W := ∀ p ∈ W, ∃ U V, τ.isOpen U ∧ σ.isOpen V ∧ p.1 ∈ U ∧ p.2 ∈ V ∧ U ×ˢ V ⊆ W
  empty_open := fun _ hp => (Set.mem_empty_iff_false _).mp hp |>.elim
  univ_open  := fun p _ => ⟨Set.univ, Set.univ, τ.univ_open, σ.univ_open,
                             Set.mem_univ _, Set.mem_univ _, Set.subset_univ _⟩
  union_open := by
    intro F hF p ⟨W, hWF, hpW⟩
    obtain ⟨U, V, hUo, hVo, hpU, hpV, hUVW⟩ := hF W hWF p hpW
    exact ⟨U, V, hUo, hVo, hpU, hpV, hUVW.trans (Set.subset_sUnion_of_mem hWF)⟩
  inter_open := by
    intro U V hU hV p ⟨hpU, hpV⟩
    obtain ⟨A, B, hAo, hBo, hpA, hpB, hABU⟩ := hU p hpU
    obtain ⟨C, D, hCo, hDo, hpC, hpD, hCDV⟩ := hV p hpV
    exact ⟨A ∩ C, B ∩ D, τ.inter_open A C hAo hCo, σ.inter_open B D hBo hDo,
           ⟨hpA, hpC⟩, ⟨hpB, hpD⟩,
           fun q hq => ⟨hABU ⟨hq.1.1, hq.2.1⟩, hCDV ⟨hq.1.2, hq.2.2⟩⟩⟩

/-- Ürün topolojisinde silindir açıktır: U açık ∧ V açık → U ×ˢ V açık. -/
theorem prodTopology_cylinder_open (τ : Topology α) (σ : Topology β)
    {U : Set α} {V : Set β} (hU : τ.isOpen U) (hV : σ.isOpen V) :
    (prodTopology τ σ).isOpen (U ×ˢ V) :=
  fun _ ⟨hpU, hpV⟩ => ⟨U, V, hU, hV, hpU, hpV, fun _ hq => hq⟩

-- ──────────────────────────────────────────────────────────
-- 14. Homeomorfizma
-- ──────────────────────────────────────────────────────────

/-- `f : α → β` bir **homeomorfizmadır** eğer:
    sürekli + birim + ters de sürekli. -/
structure Homeomorphism (τ : Topology α) (σ : Topology β) where
  toFun    : α → β
  invFun   : β → α
  left_inv  : Function.LeftInverse invFun toFun
  right_inv : Function.RightInverse invFun toFun
  cont      : isContinuous τ σ toFun
  cont_inv  : isContinuous σ τ invFun

/-- Homeomorfizma refleksiftir. -/
def Homeomorphism.refl (τ : Topology α) : Homeomorphism τ τ where
  toFun    := id
  invFun   := id
  left_inv  := fun _ => rfl
  right_inv := fun _ => rfl
  cont      := fun V hV => by simp only [Set.preimage_id]; exact hV
  cont_inv  := fun V hV => by simp only [Set.preimage_id]; exact hV

/-- Homeomorfizma simetriktir. -/
def Homeomorphism.symm (h : Homeomorphism τ σ) : Homeomorphism σ τ where
  toFun    := h.invFun
  invFun   := h.toFun
  left_inv  := h.right_inv
  right_inv := h.left_inv
  cont      := h.cont_inv
  cont_inv  := h.cont

/-- Homeomorfizma transitiftir. -/
def Homeomorphism.trans {γ : Type*} {ρ : Topology γ}
    (h₁ : Homeomorphism τ σ) (h₂ : Homeomorphism σ ρ) : Homeomorphism τ ρ where
  toFun    := h₂.toFun ∘ h₁.toFun
  invFun   := h₁.invFun ∘ h₂.invFun
  left_inv  := fun x => by
    show h₁.invFun (h₂.invFun (h₂.toFun (h₁.toFun x))) = x
    rw [h₂.left_inv, h₁.left_inv]
  right_inv := fun y => by
    show h₂.toFun (h₁.toFun (h₁.invFun (h₂.invFun y))) = y
    rw [h₁.right_inv, h₂.right_inv]
  cont      := continuous_comp τ σ ρ h₁.cont h₂.cont
  cont_inv  := continuous_comp ρ σ τ h₂.cont_inv h₁.cont_inv

/-- Homeomorfizma açık kümeleri korur. -/
theorem Homeomorphism.isOpen_iff (h : Homeomorphism τ σ) {U : Set α} :
    τ.isOpen U ↔ σ.isOpen (h.toFun '' U) := by
  constructor
  · intro hU
    suffices heq : h.toFun '' U = h.invFun ⁻¹' U by
      rw [heq]; exact h.cont_inv U hU
    ext y; simp only [Set.mem_image, Set.mem_preimage]
    constructor
    · rintro ⟨x, hxU, rfl⟩; rw [h.left_inv]; exact hxU
    · intro hy; exact ⟨h.invFun y, hy, h.right_inv y⟩
  · intro hV
    suffices heq : U = h.toFun ⁻¹' (h.toFun '' U) by
      rw [heq]; exact h.cont (h.toFun '' U) hV
    ext x; simp only [Set.mem_preimage, Set.mem_image]
    constructor
    · intro hx; exact ⟨x, hx, rfl⟩
    · rintro ⟨y, hy, heq⟩
      exact Function.LeftInverse.injective h.left_inv heq ▸ hy

-- ──────────────────────────────────────────────────────────
-- 15. Yoğun kümeler
-- ──────────────────────────────────────────────────────────

/-- `A` kümesi τ topolojisinde **yoğundur**: `closure τ A = Set.univ`. -/
def isDense (τ : Topology α) (A : Set α) : Prop := closure τ A = Set.univ

/-- A yoğundur ↔ her boş olmayan açık küme A ile kesişir. -/
theorem isDense_iff (τ : Topology α) (A : Set α) :
    isDense τ A ↔ ∀ U, τ.isOpen U → U.Nonempty → (U ∩ A).Nonempty := by
  simp only [isDense]
  constructor
  · intro hdense U hUo ⟨x, hxU⟩
    by_contra hempty
    rw [Set.not_nonempty_iff_eq_empty] at hempty
    -- A ⊆ Uᶜ (since U ∩ A = ∅)
    have hAUc : A ⊆ Uᶜ := fun a haA haU =>
      (Set.mem_empty_iff_false a).mp (hempty ▸ Set.mem_inter haU haA)
    -- cl(A) ⊆ Uᶜ (Uᶜ is closed and contains A)
    have hUc_cl : isClosed τ Uᶜ := by unfold isClosed; rw [compl_compl]; exact hUo
    have hclUc : closure τ A ⊆ Uᶜ :=
      Set.sInter_subset_of_mem ⟨hUc_cl, hAUc⟩
    -- But x ∈ cl(A) = univ and x ∈ U — contradiction
    exact hclUc (hdense.symm ▸ Set.mem_univ x) hxU
  · intro h
    apply Set.eq_univ_of_forall
    intro x
    simp only [closure, Set.mem_sInter, Set.mem_setOf_eq]
    intro C ⟨hCclosed, hAC⟩
    by_contra hxC
    obtain ⟨a, haC, haA⟩ := h Cᶜ hCclosed ⟨x, hxC⟩
    exact haC (hAC haA)

/-- cl(A) = univ ↔ A yoğundur. -/
theorem dense_iff_closure_eq_univ (τ : Topology α) (A : Set α) :
    isDense τ A ↔ closure τ A = Set.univ :=
  Iff.rfl

/-- A ⊆ B ve A yoğun → B yoğundur. -/
theorem dense_mono (τ : Topology α) {A B : Set α} (hAB : A ⊆ B) (hA : isDense τ A) :
    isDense τ B := by
  unfold isDense at *
  apply Set.eq_univ_of_forall
  intro x
  exact closure_mono τ hAB (hA.symm ▸ Set.mem_univ x)

-- ──────────────────────────────────────────────────────────
-- 16. Bağlantılılık
-- ──────────────────────────────────────────────────────────

/-- τ **bağlantılıdır**: ∅ ve univ dışında clopen küme yoktur. -/
def isConnected (τ : Topology α) : Prop :=
  ∀ U : Set α, τ.isOpen U ∧ isClosed τ U → U = ∅ ∨ U = Set.univ

/-- Bağlantılılık ≡ boş olmayan açık ayrışım yoktur. -/
theorem connected_iff_no_partition (τ : Topology α) :
    isConnected τ ↔
    ∀ U V : Set α, τ.isOpen U → τ.isOpen V → U ∩ V = ∅ → U ∪ V = Set.univ →
      U = ∅ ∨ V = ∅ := by
  simp only [isConnected]
  constructor
  · intro hconn U V hUo hVo hdisj hcov
    -- V = Uᶜ (from the partition)
    have hVUc : V = Uᶜ := by
      ext x; constructor
      · intro hxV hxU
        exact (Set.mem_empty_iff_false x).mp (hdisj ▸ Set.mem_inter hxU hxV)
      · intro hxUc
        have : x ∈ U ∪ V := hcov ▸ Set.mem_univ x
        exact this.resolve_left hxUc
    subst hVUc
    have hUcl : isClosed τ U := hVo
    rcases hconn U ⟨hUo, hUcl⟩ with rfl | rfl
    · exact Or.inl rfl
    · right; simp
  · intro h U ⟨hUo, hUcl⟩
    rcases h U Uᶜ hUo hUcl (Set.inter_compl_self U) (Set.union_compl_self U) with rfl | hUc
    · exact Or.inl rfl
    · right
      rw [← compl_compl U, hUc]
      ext x; simp

-- ──────────────────────────────────────────────────────────
-- 17. T₁ → tek noktalı kümeler kapalıdır
-- ──────────────────────────────────────────────────────────

/-- T1'de her tekil küme kapalıdır. -/
theorem t1_singleton_closed (τ : Topology α) (h : isT1 τ) (x : α) :
    isClosed τ {x} := by
  unfold isClosed
  have heq : {x}ᶜ = ⋃₀ {U | τ.isOpen U ∧ x ∉ U} := by
    ext y
    simp only [Set.mem_compl_iff, Set.mem_singleton_iff, Set.mem_sUnion, Set.mem_setOf_eq]
    constructor
    · intro hyx
      obtain ⟨U, hU, hyU, hxU⟩ := h y x hyx
      exact ⟨U, ⟨hU, hxU⟩, hyU⟩
    · rintro ⟨U, ⟨_, hxU⟩, hyU⟩ rfl
      exact hxU hyU
  rw [heq]
  exact τ.union_open _ (fun U hU => hU.1)

-- ──────────────────────────────────────────────────────────
-- 18. T₃ (Düzenli) ve T₄ (Normal) + implication zinciri
-- ──────────────────────────────────────────────────────────

/-- **T₃ (Düzenli)**: T1 + her kapalı küme ile onu içermeyen
    nokta ayrı açık mahallere sahip. -/
def isT3 (τ : Topology α) : Prop :=
  isT1 τ ∧ ∀ (x : α) (C : Set α), isClosed τ C → x ∉ C →
    ∃ U V, τ.isOpen U ∧ τ.isOpen V ∧ x ∈ U ∧ C ⊆ V ∧ U ∩ V = ∅

/-- **T₄ (Normal)**: T1 + ayrık iki kapalı küme ayrı açık kümelerle ayrılır. -/
def isT4 (τ : Topology α) : Prop :=
  isT1 τ ∧ ∀ (C D : Set α), isClosed τ C → isClosed τ D → C ∩ D = ∅ →
    ∃ U V, τ.isOpen U ∧ τ.isOpen V ∧ C ⊆ U ∧ D ⊆ V ∧ U ∩ V = ∅

/-- T₄ → T₃. -/
theorem t4_implies_t3 (τ : Topology α) (h : isT4 τ) : isT3 τ := by
  obtain ⟨hT1, hNorm⟩ := h
  refine ⟨hT1, fun x C hC hxC => ?_⟩
  have hxCl : isClosed τ {x} := t1_singleton_closed τ hT1 x
  have hdisj : {x} ∩ C = ∅ := by
    ext y
    simp only [Set.mem_inter_iff, Set.mem_singleton_iff, Set.mem_empty_iff_false, iff_false]
    rintro ⟨rfl, hyC⟩; exact hxC hyC
  obtain ⟨U, V, hU, hV, hxU, hCV, hdj⟩ := hNorm {x} C hxCl hC hdisj
  exact ⟨U, V, hU, hV, hxU (Set.mem_singleton_iff.mpr rfl), hCV, hdj⟩

/-- T₃ → T₂. -/
theorem t3_implies_t2 (τ : Topology α) (h : isT3 τ) : isT2 τ := by
  obtain ⟨hT1, hReg⟩ := h
  intro x y hne
  have hyCl : isClosed τ {y} := t1_singleton_closed τ hT1 y
  have hxny : x ∉ ({y} : Set α) := by simp only [Set.mem_singleton_iff]; exact hne
  obtain ⟨U, V, hU, hV, hxU, hyV, hdj⟩ := hReg x {y} hyCl hxny
  exact ⟨U, V, hU, hV, hxU, hyV (Set.mem_singleton_iff.mpr rfl), hdj⟩

/-- **Zincir**: T₄ → T₂. -/
theorem t4_implies_t2 (τ : Topology α) (h : isT4 τ) : isT2 τ :=
  t3_implies_t2 τ (t4_implies_t3 τ h)

-- ──────────────────────────────────────────────────────────
-- 19. Kompaktlık — ek teoremler
-- ──────────────────────────────────────────────────────────

/-- İki kompakt kümenin birleşimi kompakttır. -/
theorem compact_union (τ : Topology α) {K₁ K₂ : Set α}
    (h₁ : isCompact τ K₁) (h₂ : isCompact τ K₂) : isCompact τ (K₁ ∪ K₂) := by
  intro F hF hcover
  obtain ⟨n₁, G₁, hG₁, hsub₁⟩ := h₁ F hF (Set.subset_union_left.trans hcover)
  obtain ⟨n₂, G₂, hG₂, hsub₂⟩ := h₂ F hF (Set.subset_union_right.trans hcover)
  refine ⟨n₁ + n₂,
    fun i => if h : i.val < n₁ then G₁ ⟨i.val, h⟩
             else G₂ ⟨i.val - n₁, by omega⟩,
    fun i => ?_, fun x hx => ?_⟩
  · dsimp only
    split_ifs with h
    · exact hG₁ _
    · exact hG₂ _
  · rcases hx with hxK₁ | hxK₂
    · obtain ⟨j, hxj⟩ := Set.mem_iUnion.mp (hsub₁ hxK₁)
      refine Set.mem_iUnion.mpr ⟨⟨j.val, by omega⟩, ?_⟩
      simp only [dif_pos j.isLt]; exact hxj
    · obtain ⟨j, hxj⟩ := Set.mem_iUnion.mp (hsub₂ hxK₂)
      refine Set.mem_iUnion.mpr ⟨⟨n₁ + j.val, by omega⟩, ?_⟩
      simp only [show ¬(n₁ + j.val < n₁) from by omega, dif_neg, not_false_eq_true,
                 Nat.add_sub_cancel_left]
      exact hxj

/-- Kompakt kümenin kapalı alt kümesi kompakttır. -/
theorem compact_closed_subset (τ : Topology α) {K A : Set α}
    (hK : isCompact τ K) (hAK : A ⊆ K) (hAcl : isClosed τ A) :
    isCompact τ A := by
  intro F hF hcoverA
  by_cases hAne : A = ∅
  · exact ⟨0, Fin.elim0, fun i => i.elim0, hAne ▸ Set.empty_subset _⟩
  obtain ⟨x₀, hx₀A⟩ := Set.nonempty_iff_ne_empty.mpr hAne
  obtain ⟨U₀, hU₀F, hx₀U₀⟩ := Set.mem_sUnion.mp (hcoverA hx₀A)
  -- Genişletilmiş örtü: F ∪ {Aᶜ} K'yı örter
  have hF' : ∀ s, s ∈ insert Aᶜ F → τ.isOpen s := by
    intro s hs
    simp only [Set.mem_insert_iff] at hs
    rcases hs with rfl | hs
    · exact hAcl
    · exact hF s hs
  have hcoverK : K ⊆ ⋃₀ insert Aᶜ F := by
    intro x hxK
    simp only [Set.mem_sUnion, Set.mem_insert_iff]
    by_cases hxA : x ∈ A
    · obtain ⟨U, hUF, hxU⟩ := Set.mem_sUnion.mp (hcoverA hxA)
      exact ⟨U, Or.inr hUF, hxU⟩
    · exact ⟨Aᶜ, Or.inl rfl, hxA⟩
  obtain ⟨n, G, hGF', hKsub⟩ := hK (insert Aᶜ F) hF' hcoverK
  -- Aᶜ'yi G'den U₀ ile değiştir
  let G' : Fin n → Set α := fun i => if G i = Aᶜ then U₀ else G i
  refine ⟨n, G', fun i => ?_, fun x hxA => ?_⟩
  · dsimp only [G']
    split_ifs with h
    · exact hU₀F
    · have hgi := hGF' i
      simp only [Set.mem_insert_iff] at hgi
      rcases hgi with hgieq | hgiF
      · exact absurd hgieq h
      · exact hgiF
  · obtain ⟨j, hxj⟩ := Set.mem_iUnion.mp (hKsub (hAK hxA))
    refine Set.mem_iUnion.mpr ⟨j, ?_⟩
    dsimp only [G']
    split_ifs with h
    · have hxAc : x ∉ A := by rw [← Set.mem_compl_iff, ← h]; exact hxj
      exact absurd hxA hxAc
    · exact hxj

-- ──────────────────────────────────────────────────────────
-- 21. İç / Kapanış dualitesi (tümleyen)
-- ──────────────────────────────────────────────────────────

/-- Tümleyen kümenin iç bölgesi = kapanışın tümleyeni: `int(Aᶜ) = cl(A)ᶜ`. -/
theorem interior_compl (τ : Topology α) (A : Set α) :
    interior τ Aᶜ = (closure τ A)ᶜ := by
  apply Set.Subset.antisymm
  · -- int(Aᶜ) ⊆ cl(A)ᶜ
    intro x hx
    simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hx
    obtain ⟨U, ⟨hUo, hUAc⟩, hxU⟩ := hx
    simp only [Set.mem_compl_iff]
    intro hxcl
    have hUcCl : isClosed τ Uᶜ := by unfold isClosed; rw [compl_compl]; exact hUo
    have hAUc : A ⊆ Uᶜ := fun a haA haU => hUAc haU haA
    exact (Set.mem_sInter.mp hxcl Uᶜ ⟨hUcCl, hAUc⟩) hxU
  · -- cl(A)ᶜ ⊆ int(Aᶜ)
    intro x hxncl
    simp only [Set.mem_compl_iff] at hxncl
    have hexist : ∃ C, isClosed τ C ∧ A ⊆ C ∧ x ∉ C := by
      by_contra h
      apply hxncl
      simp only [closure, Set.mem_sInter, Set.mem_setOf_eq]
      intro C ⟨hCcl, hAC⟩
      by_contra hxC
      exact h ⟨C, hCcl, hAC, hxC⟩
    obtain ⟨C, hCcl, hAC, hxC⟩ := hexist
    simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq]
    exact ⟨Cᶜ, ⟨hCcl, Set.compl_subset_compl.mpr hAC⟩, hxC⟩

/-- Tümleyen kümenin kapanışı = iç bölgenin tümleyeni: `cl(Aᶜ) = int(A)ᶜ`. -/
theorem closure_compl (τ : Topology α) (A : Set α) :
    closure τ Aᶜ = (interior τ A)ᶜ := by
  have h := interior_compl τ Aᶜ
  rw [compl_compl] at h
  -- h : interior τ A = (closure τ Aᶜ)ᶜ
  rw [h, compl_compl]

-- ──────────────────────────────────────────────────────────
-- 22. T₁ eşdeğerliği: tekil kümelerin kapalılığı
-- ──────────────────────────────────────────────────────────

/-- T1 ↔ her tekil küme kapalıdır. -/
theorem t1_iff_singletons_closed (τ : Topology α) :
    isT1 τ ↔ ∀ x : α, isClosed τ {x} := by
  constructor
  · exact t1_singleton_closed τ
  · intro h x y hne
    refine ⟨{y}ᶜ, h y, ?_, ?_⟩
    · simp [hne]
    · simp

-- ──────────────────────────────────────────────────────────
-- 23. Sonlu birleşimler: Fin n indeksli kapalıların birleşimi
-- ──────────────────────────────────────────────────────────

/-- `Fin n`-indeksli sonlu kapalı küme ailesi kapalıdır. -/
theorem closed_sUnion_finite (τ : Topology α) :
    ∀ {n : ℕ} (F : Fin n → Set α), (∀ i, isClosed τ (F i)) → isClosed τ (⋃ i, F i) := by
  intro n
  induction n with
  | zero =>
    intro F _
    rw [show (⋃ i : Fin 0, F i) = ∅ from
          Set.iUnion_eq_empty.mpr (fun i => i.elim0)]
    exact closed_empty τ
  | succ n ih =>
    intro F hF
    have heq : (⋃ i : Fin (n + 1), F i) =
        F (Fin.last n) ∪ ⋃ i : Fin n, F (Fin.castSucc i) := by
      ext x
      simp only [Set.mem_iUnion, Set.mem_union]
      constructor
      · rintro ⟨i, hx⟩
        by_cases h : i = Fin.last n
        · exact Or.inl (h ▸ hx)
        · exact Or.inr ⟨⟨i.val,
              Nat.lt_of_le_of_ne (Nat.lt_succ_iff.mp i.isLt) (fun heq => h (Fin.ext heq))⟩, hx⟩
      · rintro (hx | ⟨j, hx⟩)
        · exact ⟨Fin.last n, hx⟩
        · exact ⟨Fin.castSucc j, hx⟩
    rw [heq]
    exact closed_union τ (hF (Fin.last n))
      (ih (F ∘ Fin.castSucc) (fun i => hF (Fin.castSucc i)))

-- ──────────────────────────────────────────────────────────
-- 24. Ürün topolojisi — izdüşümler ve evrensel özellik
-- ──────────────────────────────────────────────────────────

/-- Birinci izdüşüm `π₁ : α × β → α` ürün topolojisinde süreklidir. -/
theorem prodTopology_proj1_continuous (τ : Topology α) (σ : Topology β) :
    isContinuous (prodTopology τ σ) τ Prod.fst := by
  intro U hU
  have heq : (Prod.fst : α × β → α) ⁻¹' U = U ×ˢ (Set.univ : Set β) := by
    ext ⟨x, y⟩; simp
  rw [heq]; exact prodTopology_cylinder_open τ σ hU σ.univ_open

/-- İkinci izdüşüm `π₂ : α × β → β` ürün topolojisinde süreklidir. -/
theorem prodTopology_proj2_continuous (τ : Topology α) (σ : Topology β) :
    isContinuous (prodTopology τ σ) σ Prod.snd := by
  intro V hV
  have heq : (Prod.snd : α × β → β) ⁻¹' V = (Set.univ : Set α) ×ˢ V := by
    ext ⟨x, y⟩; simp
  rw [heq]; exact prodTopology_cylinder_open τ σ τ.univ_open hV

/-- **Evrensel özellik**: `f : γ → α × β` sürekli ↔ her bileşen süreklidir. -/
theorem continuous_to_product {ρ : Topology γ} (τ : Topology α) (σ : Topology β)
    (f : γ → α × β) :
    isContinuous ρ (prodTopology τ σ) f ↔
      isContinuous ρ τ (Prod.fst ∘ f) ∧ isContinuous ρ σ (Prod.snd ∘ f) := by
  constructor
  · intro hf
    exact ⟨continuous_comp ρ (prodTopology τ σ) τ hf (prodTopology_proj1_continuous τ σ),
           continuous_comp ρ (prodTopology τ σ) σ hf (prodTopology_proj2_continuous τ σ)⟩
  · intro ⟨hf1, hf2⟩ W hW
    -- f⁻¹(W) = ⋃ açık silindirler; tümü ρ'da açık
    suffices h : f ⁻¹' W = ⋃₀ {S | ρ.isOpen S ∧ S ⊆ f ⁻¹' W} by
      rw [h]; exact ρ.union_open _ (fun S hS => hS.1)
    ext z
    simp only [Set.mem_sUnion, Set.mem_setOf_eq, Set.mem_preimage]
    constructor
    · intro hzW
      obtain ⟨U, V, hUo, hVo, hfzU, hfzV, hUVW⟩ := hW (f z) hzW
      exact ⟨(Prod.fst ∘ f) ⁻¹' U ∩ (Prod.snd ∘ f) ⁻¹' V,
             ⟨ρ.inter_open _ _ (hf1 U hUo) (hf2 V hVo),
              fun w ⟨hwU, hwV⟩ => hUVW ⟨hwU, hwV⟩⟩, hfzU, hfzV⟩
    · rintro ⟨S, ⟨_, hSW⟩, hzS⟩
      exact hSW hzS

-- ──────────────────────────────────────────────────────────
-- 25. İç operatörünün cebirsel özellikleri
-- ──────────────────────────────────────────────────────────

/-- `int(A ∩ B) = int(A) ∩ int(B)`. -/
theorem interior_inter (τ : Topology α) (A B : Set α) :
    interior τ (A ∩ B) = interior τ A ∩ interior τ B := by
  apply Set.Subset.antisymm
  · intro x hx
    simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hx ⊢
    obtain ⟨U, ⟨hUo, hUAB⟩, hxU⟩ := hx
    exact ⟨⟨U, ⟨hUo, hUAB.trans Set.inter_subset_left⟩, hxU⟩,
           ⟨U, ⟨hUo, hUAB.trans Set.inter_subset_right⟩, hxU⟩⟩
  · intro x hx
    simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq,
               Set.mem_inter_iff] at hx ⊢
    obtain ⟨⟨U, ⟨hUo, hUA⟩, hxU⟩, ⟨V, ⟨hVo, hVB⟩, hxV⟩⟩ := hx
    exact ⟨U ∩ V, ⟨τ.inter_open U V hUo hVo, Set.inter_subset_inter hUA hVB⟩, hxU, hxV⟩

/-- `cl(A ∩ B) ⊆ cl(A) ∩ cl(B)`. -/
theorem closure_inter_subset (τ : Topology α) (A B : Set α) :
    closure τ (A ∩ B) ⊆ closure τ A ∩ closure τ B :=
  Set.subset_inter
    (closure_mono τ Set.inter_subset_left)
    (closure_mono τ Set.inter_subset_right)

-- ──────────────────────────────────────────────────────────
-- 26. Sonlu kesişim: açık kümelerin sonlu kesişimi açıktır
-- ──────────────────────────────────────────────────────────

/-- `Fin n`-indeksli sonlu açık küme ailesinin kesişimi açıktır. -/
theorem open_iInter_finite (τ : Topology α) :
    ∀ {n : ℕ} (G : Fin n → Set α), (∀ i, τ.isOpen (G i)) → τ.isOpen (⋂ i, G i) := by
  intro n
  induction n with
  | zero =>
    intro G _
    have : (⋂ i : Fin 0, G i) = Set.univ := by simp
    rw [this]; exact τ.univ_open
  | succ n ih =>
    intro G hG
    have heq : (⋂ i : Fin (n + 1), G i) =
        G (Fin.last n) ∩ ⋂ i : Fin n, G (Fin.castSucc i) := by
      ext x
      simp only [Set.mem_iInter, Set.mem_inter_iff]
      exact ⟨fun h => ⟨h (Fin.last n), fun i => h (Fin.castSucc i)⟩,
             fun ⟨hl, hr⟩ => Fin.lastCases hl hr⟩
    rw [heq]
    exact τ.inter_open _ _ (hG (Fin.last n))
      (ih (G ∘ Fin.castSucc) (fun i => hG (Fin.castSucc i)))

-- ──────────────────────────────────────────────────────────
-- 27. Sürekli fonksiyonun kompakt kümenin görüntüsü kompakttır
-- ──────────────────────────────────────────────────────────

/-- Sürekli bir fonksiyonun kompakt bir kümedeki görüntüsü kompakttır. -/
theorem compact_continuous_image (τ : Topology α) (σ : Topology β)
    {f : α → β} (hf : isContinuous τ σ f) {K : Set α} (hK : isCompact τ K) :
    isCompact σ (f '' K) := by
  intro F hF hcover
  -- Geri-çekim ailesi: F' = {f⁻¹(V) | V ∈ F}
  have hF'open : ∀ s ∈ (fun V => f ⁻¹' V) '' F, τ.isOpen s := by
    rintro _ ⟨V, hVF, rfl⟩; exact hf V (hF V hVF)
  have hcoverK : K ⊆ ⋃₀ ((fun V => f ⁻¹' V) '' F) := by
    intro x hxK
    obtain ⟨V, hVF, hfxV⟩ := Set.mem_sUnion.mp (hcover ⟨x, hxK, rfl⟩)
    exact Set.mem_sUnion.mpr ⟨f ⁻¹' V, Set.mem_image_of_mem _ hVF, hfxV⟩
  obtain ⟨n, G, hGF, hKsub⟩ := hK _ hF'open hcoverK
  -- Her G i = f⁻¹(V i) için V i seç
  have hchoice : ∀ i : Fin n, ∃ V ∈ F, f ⁻¹' V = G i := by
    intro i; obtain ⟨V, hVF, hVG⟩ := hGF i; exact ⟨V, hVF, hVG⟩
  choose V hVF hVG using hchoice
  refine ⟨n, V, hVF, ?_⟩
  rintro y ⟨x, hxK, rfl⟩
  obtain ⟨j, hxGj⟩ := Set.mem_iUnion.mp (hKsub hxK)
  have hxV : x ∈ f ⁻¹' V j := by rw [hVG j]; exact hxGj
  exact Set.mem_iUnion.mpr ⟨j, hxV⟩

-- ──────────────────────────────────────────────────────────
-- 28. Hausdorff uzayında kompakt küme kapalıdır
-- ──────────────────────────────────────────────────────────

/-- T₂ (Hausdorff) uzayında her kompakt küme kapalıdır. -/
theorem compact_t2_closed (τ : Topology α) (ht2 : isT2 τ) {K : Set α}
    (hK : isCompact τ K) : isClosed τ K := by
  unfold isClosed
  rw [open_iff_eq_interior]
  apply Set.Subset.antisymm _ (interior_subset τ Kᶜ)
  intro y hyKc
  rw [Set.mem_compl_iff] at hyKc
  -- K'yı örten T₂-ayrım açık ailesi
  obtain ⟨n, G, hGF, hKsub⟩ := hK
    {U | ∃ x ∈ K, ∃ V, τ.isOpen U ∧ x ∈ U ∧ τ.isOpen V ∧ y ∈ V ∧ U ∩ V = ∅}
    (by rintro s ⟨_, _, _, hs, _, _, _, _⟩; exact hs)
    (by
      intro x hxK
      obtain ⟨U, V, hUo, hVo, hxU, hyV, hUV⟩ := ht2 x y (fun h => hyKc (h ▸ hxK))
      exact Set.mem_sUnion.mpr ⟨U, ⟨x, hxK, V, hUo, hxU, hVo, hyV, hUV⟩, hxU⟩)
  -- Her G i için eşlenik açık V i seç
  have hVex : ∀ i : Fin n, ∃ V, τ.isOpen V ∧ y ∈ V ∧ G i ∩ V = ∅ := by
    intro i
    obtain ⟨_, _, V, _, _, hVo, hyV, hGV⟩ := hGF i
    exact ⟨V, hVo, hyV, hGV⟩
  choose V hVo hyV hGV using hVex
  -- W = ⋂ V i: açık, y ∈ W, W ⊆ Kᶜ
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq]
  refine ⟨⋂ i, V i, ⟨open_iInter_finite τ V hVo, ?_⟩, Set.mem_iInter.mpr hyV⟩
  intro z hzW
  rw [Set.mem_compl_iff]
  intro hzK
  obtain ⟨j, hzGj⟩ := Set.mem_iUnion.mp (hKsub hzK)
  have hmem : z ∈ G j ∩ V j := ⟨hzGj, Set.mem_iInter.mp hzW j⟩
  rw [hGV j] at hmem
  exact hmem.elim

-- ──────────────────────────────────────────────────────────
-- 29. Sürekli fonksiyonun bağlantılı uzayın görüntüsü bağlantılıdır
-- ──────────────────────────────────────────────────────────

/-- Sürekli ve örten bir fonksiyonun bağlantılı uzaydan görüntüsü bağlantılıdır. -/
theorem connected_continuous_image (τ : Topology α) (σ : Topology β)
    (f : α → β) (hf : isContinuous τ σ f) (hfS : Function.Surjective f)
    (hconn : isConnected τ) : isConnected σ := by
  intro U ⟨hUo, hUcl⟩
  have hfUo  : τ.isOpen (f ⁻¹' U)   := hf U hUo
  have hfUcl : isClosed τ (f ⁻¹' U) := continuous_preimage_closed τ σ hf hUcl
  rcases hconn (f ⁻¹' U) ⟨hfUo, hfUcl⟩ with h | h
  · -- f⁻¹(U) = ∅ → U = ∅
    left; ext y; constructor
    · intro hyU
      obtain ⟨x, rfl⟩ := hfS y
      have hxU : x ∈ f ⁻¹' U := hyU
      rw [h] at hxU; exact hxU.elim
    · exact False.elim
  · -- f⁻¹(U) = univ → U = univ
    right; ext y; simp only [Set.mem_univ, iff_true]
    obtain ⟨x, rfl⟩ := hfS y
    have : x ∈ Set.univ := Set.mem_univ x
    rwa [← h] at this

-- ──────────────────────────────────────────────────────────
-- 30. İç/kapanış dualite sonuçları
-- ──────────────────────────────────────────────────────────

/-- `interior τ A = (closure τ Aᶜ)ᶜ` — dualite sonucu. -/
theorem interior_eq_compl_closure_compl (τ : Topology α) (A : Set α) :
    interior τ A = (closure τ Aᶜ)ᶜ := by
  have h := interior_compl τ Aᶜ
  simp only [compl_compl] at h
  exact h

/-- `closure τ A = (interior τ Aᶜ)ᶜ` — dualite sonucu. -/
theorem closure_eq_compl_interior_compl (τ : Topology α) (A : Set α) :
    closure τ A = (interior τ Aᶜ)ᶜ := by
  have h := closure_compl τ Aᶜ
  simp only [compl_compl] at h
  exact h

-- ──────────────────────────────────────────────────────────
-- 31. Sürekli fonksiyon kapanış görüntüsünü içerir
-- ──────────────────────────────────────────────────────────

/-- Sürekli `f` için `f '' (closure τ A) ⊆ closure σ (f '' A)`. -/
theorem continuous_closure_image (τ : Topology α) (σ : Topology β)
    {f : α → β} (hf : isContinuous τ σ f) (A : Set α) :
    f '' closure τ A ⊆ closure σ (f '' A) := by
  rintro y ⟨x, hxcl, rfl⟩
  simp only [closure, Set.mem_sInter, Set.mem_setOf_eq]
  intro C ⟨hCcl, hfAC⟩
  have hfCcl : isClosed τ (f ⁻¹' C) := continuous_preimage_closed τ σ hf hCcl
  have hAfC  : A ⊆ f ⁻¹' C := fun a haA => hfAC (Set.mem_image_of_mem f haA)
  have hcl_sub : closure τ A ⊆ f ⁻¹' C := Set.sInter_subset_of_mem ⟨hfCcl, hAfC⟩
  exact hcl_sub hxcl

-- ──────────────────────────────────────────────────────────
-- 32. Kompakt uzaydan T₂ uzaya biyektif sürekli → homeomorfizma
-- ──────────────────────────────────────────────────────────

/-- Kompakt uzaydan T₂ (Hausdorff) uzaya biyektif sürekli fonksiyon homeomorfizmadır. -/
theorem compact_t2_homeomorphism (τ : Topology α) (σ : Topology β)
    (hτK : isCompact τ Set.univ) (hσT2 : isT2 σ)
    (f : α → β) (hcont : isContinuous τ σ f)
    (hinj : Function.Injective f) (hsurj : Function.Surjective f) :
    ∃ h : Homeomorphism τ σ, h.toFun = f := by
  choose g hgf using hsurj
  have hgf_left : ∀ x : α, g (f x) = x := fun x => hinj (hgf (f x))
  have hgcont : isContinuous σ τ g := by
    intro U hUo
    have heq : g ⁻¹' U = (f '' Uᶜ)ᶜ := by
      ext y
      simp only [Set.mem_preimage, Set.mem_compl_iff, Set.mem_image]
      constructor
      · intro hgy ⟨x, hxUc, hfx⟩
        have hxeq : x = g y := by
          have h := congr_arg g hfx
          rw [hgf_left] at h; exact h
        exact absurd hgy (hxeq ▸ hxUc)
      · intro hnotimg
        by_contra hgy
        exact hnotimg ⟨g y, hgy, hgf y⟩
    rw [heq]
    have hUcCl : isClosed τ Uᶜ := by unfold isClosed; rw [compl_compl]; exact hUo
    exact compact_t2_closed σ hσT2
      (compact_continuous_image τ σ hcont
        (compact_closed_subset τ hτK (Set.subset_univ Uᶜ) hUcCl))
  exact ⟨⟨f, g, hgf_left, hgf, hcont, hgcont⟩, rfl⟩

-- ──────────────────────────────────────────────────────────
-- 33. T₂ ↔ çapraz kapalı
-- ──────────────────────────────────────────────────────────

/-- `isT2 τ ↔ isClosed (prodTopology τ τ) {p | p.1 = p.2}`. -/
theorem t2_iff_diagonal_closed (τ : Topology α) :
    isT2 τ ↔ isClosed (prodTopology τ τ) {p : α × α | p.1 = p.2} := by
  constructor
  · intro ht2
    unfold isClosed
    have heq : {p : α × α | p.1 = p.2}ᶜ = {p | p.1 ≠ p.2} := by
      ext ⟨a, b⟩; simp [Ne]
    rw [heq]
    intro ⟨x, y⟩ hne
    obtain ⟨U, V, hUo, hVo, hxU, hyV, hUV⟩ := ht2 x y hne
    refine ⟨U, V, hUo, hVo, hxU, hyV, ?_⟩
    intro ⟨a, b⟩ ⟨haU, hbV⟩
    show a ≠ b
    intro hab
    have haV : a ∈ V := by rw [hab]; exact hbV
    have hmem : a ∈ U ∩ V := ⟨haU, haV⟩
    rw [hUV] at hmem; exact hmem.elim
  · intro hdiag x y hne
    unfold isClosed at hdiag
    have heq : {p : α × α | p.1 = p.2}ᶜ = {p | p.1 ≠ p.2} := by
      ext ⟨a, b⟩; simp [Ne]
    rw [heq] at hdiag
    obtain ⟨U, V, hUo, hVo, hxU, hyV, hUVsub⟩ := hdiag (x, y) hne
    refine ⟨U, V, hUo, hVo, hxU, hyV, ?_⟩
    ext z
    simp only [Set.mem_inter_iff, Set.mem_empty_iff_false, iff_false]
    intro ⟨hzU, hzV⟩
    have hmemProd : (z, z) ∈ U ×ˢ V := ⟨hzU, hzV⟩
    exact hUVsub hmemProd rfl

-- ──────────────────────────────────────────────────────────
-- 34. İç birleşim alt kümesi
-- ──────────────────────────────────────────────────────────

/-- `interior τ A ∪ interior τ B ⊆ interior τ (A ∪ B)`. -/
theorem interior_union_subset (τ : Topology α) (A B : Set α) :
    interior τ A ∪ interior τ B ⊆ interior τ (A ∪ B) := by
  apply Set.union_subset
  · exact interior_mono τ Set.subset_union_left
  · exact interior_mono τ Set.subset_union_right

-- ──────────────────────────────────────────────────────────
-- 20. Sierpinski Topolojisi ve Urysohn Ayrılma Teoremi
-- ──────────────────────────────────────────────────────────

/-- **Sierpinski topolojisi** `Bool` üzerinde: boş küme ve `true` içeren her küme açıktır.
    Bu, iki noktalı uzaylar üzerindeki en kaba T₀ topolojisidir. -/
def sierpinskiTopology : Topology Bool where
  isOpen U := U = ∅ ∨ true ∈ U
  empty_open := Or.inl rfl
  univ_open  := Or.inr (Set.mem_univ true)
  union_open := by
    intro F hF
    by_cases h : ∃ s ∈ F, true ∈ s
    · right
      obtain ⟨s, hsF, hts⟩ := h
      exact Set.mem_sUnion.mpr ⟨s, hsF, hts⟩
    · left
      ext x
      simp only [Set.mem_sUnion, Set.mem_empty_iff_false, iff_false]
      intro ⟨s, hsF, hxs⟩
      rcases hF s hsF with rfl | hts
      · exact hxs.elim
      · exact h ⟨s, hsF, hts⟩
  inter_open := by
    intro U V hU hV
    rcases hU with rfl | htU
    · left; exact Set.empty_inter V
    · rcases hV with rfl | htV
      · left; exact Set.inter_empty U
      · right; exact ⟨htU, htV⟩

/-- **Urysohn Ayrılma Teoremi**: Normal (T₄) uzayda ayrık iki kapalı küme,
    Sierpinski uzayına sürekli bir fonksiyonla ayrılır.

    Neden Sierpinski? Hedef topoloji keyfi olsaydı teorem yanlış olurdu
    (örnek: bağlantılı α, ayrık σ). Sierpinski uzayında ön görüntüler yalnızca
    ∅, V veya α olabilir — hepsi τ'da açıktır. -/
theorem urysohn_lemma (τ : Topology α) (hT4 : isT4 τ) (C D : Set α)
    (hC : isClosed τ C) (hD : isClosed τ D) (hdisj : C ∩ D = ∅) :
    ∃ f : α → Bool, isContinuous τ sierpinskiTopology f ∧
      (∀ x ∈ C, f x = false) ∧ (∀ x ∈ D, f x = true) := by
  obtain ⟨_hT1, hNorm⟩ := hT4
  obtain ⟨U, V, _hU, hV, hCU, hDV, hdisj2⟩ := hNorm C D hC hD hdisj
  -- Klasik karar verilebilirlik: Set üyeliği Prop, Lean'in `if` ifadesi için instance gerekir
  haveI hdec : ∀ x : α, Decidable (x ∈ V) := fun x => Classical.propDecidable _
  -- f(x) = true iff x ∈ V  (V açık komşuluk: D ⊆ V, U ∩ V = ∅ → C ∩ V = ∅)
  refine ⟨fun x => if x ∈ V then true else false, ?_, ?_, ?_⟩
  · -- Süreklilik: f⁻¹(W) her zaman ∅, V veya α'dır
    intro W hW
    have hW' : W = ∅ ∨ true ∈ W := hW
    rcases hW' with rfl | htW
    · simp only [Set.preimage_empty]; exact τ.empty_open
    · by_cases hfW : false ∈ W
      · -- true ∈ W ve false ∈ W → ön görüntü = α
        have heq : (fun x : α => if x ∈ V then (true : Bool) else false) ⁻¹' W = Set.univ := by
          ext x; simp only [Set.mem_preimage, Set.mem_univ, iff_true]
          split_ifs with hxV
          · exact htW
          · exact hfW
        rw [heq]; exact τ.univ_open
      · -- sadece true ∈ W → ön görüntü = V (açık)
        have heq : (fun x : α => if x ∈ V then (true : Bool) else false) ⁻¹' W = V := by
          ext x; simp only [Set.mem_preimage]
          constructor
          · intro h
            by_contra hxnV
            have hf : (if x ∈ V then (true : Bool) else false) = false := if_neg hxnV
            rw [hf] at h; exact hfW h
          · intro hxV; rw [if_pos hxV]; exact htW
        rw [heq]; exact hV
  · -- f|_C = false: x ∈ C → x ∈ U → x ∉ V (çünkü U ∩ V = ∅)
    intro x hxC
    apply if_neg
    intro hxV
    have hmem : x ∈ U ∩ V := ⟨hCU hxC, hxV⟩
    rw [hdisj2] at hmem; exact hmem.elim
  · -- f|_D = true: x ∈ D → x ∈ V
    intro x hxD
    exact if_pos (hDV hxD)

end SetTopology
