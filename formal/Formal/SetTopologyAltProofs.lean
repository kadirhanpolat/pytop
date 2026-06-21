import Formal.SetTopology

/-!
# SetTopology — Alternatif İspat Yöntemleri
# SetTopology — Alternative Proof Methods

`Formal/SetTopology.lean` içindeki seçili teoremlerin alternatif ispatları.
Her ispat, orijinalden farklı bir strateji veya Lean taktik düzenlemesi kullanır.

## Strateji etiketleri

| Etiket | Yöntem                        | Lean örneği                       |
|--------|-------------------------------|-----------------------------------|
| [ÇY]   | Çelişki yoluyla               | `by_contra` + `False` türetme     |
| [KT]   | Karşıt ters                   | `contrapose!` yoluyla ¬Q → ¬P    |
| [D]    | Alternatif doğrudan           | farklı lemma/taktik seçimi        |
| [Tak]  | Taktik-yoğun                 | `simp` ağırlıklı                  |
| [De]   | Dualite                       | iç ↔ kapanış tümleyen dönüşümü   |
-/

namespace SetTopology
namespace Alt

variable {α β γ : Type*}

-- ══════════════════════════════════════════════════════════════
-- §1  Çelişki yoluyla (By contradiction) [ÇY]
-- ══════════════════════════════════════════════════════════════

section ByContradiction

/-!
Orijinal ispatların büyük çoğunluğu "doğrudan" kurulur.
Bu bölümde aynı teoremler `by_contra` ile açıkça False türeterek ispat edilir.
Matematiksel içgörü: hangi varsayım hangi somut çelişkiyi doğurur?
-/

/-- [ÇY] T2 → T1: y ∈ U varsayımı U ∩ V = ∅ ile çelişir. -/
theorem t2_implies_t1_bycontra (τ : Topology α) (h : isT2 τ) : isT1 τ := by
  intro x y hne
  obtain ⟨U, V, hU, _hV, hxU, hyV, hdisj⟩ := h x y hne
  refine ⟨U, hU, hxU, fun hyU => ?_⟩
  have hmem : y ∈ U ∩ V := ⟨hyU, hyV⟩
  rw [hdisj] at hmem; exact hmem.elim

/-- [ÇY] int(A) ⊆ A: x ∈ int(A) ve x ∉ A birlikte U ⊆ A ile çelişir. -/
theorem interior_subset_bycontra (τ : Topology α) (A : Set α) :
    interior τ A ⊆ A := by
  intro x hx
  by_contra hxA
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hx
  obtain ⟨U, ⟨_, hUA⟩, hxU⟩ := hx
  exact hxA (hUA hxU)

/-- [ÇY] T1 → T0: T0 başarısız olursa T1 tanığı çelişki üretir.

    Matematiksel argüman: T1 bize U veriyor; bu U aynı zamanda T0'ı da sağlar. -/
theorem t1_implies_t0_bycontra (τ : Topology α) (h : isT1 τ) : isT0 τ := by
  intro x y hne
  by_contra h0
  simp only [not_exists, not_and] at h0
  -- h0 : ∀ U, τ.isOpen U → ¬(x ∈ U ↔ y ∉ U)
  obtain ⟨U, hU, hxU, hyU⟩ := h x y hne
  exact h0 U hU ⟨fun _ => hyU, fun _ => hxU⟩

/-- [ÇY] cl(A) ⊆ cl(B) — A ⊆ B: x ∉ cl(B) varsayımı,
    B'yi içeren ama x'i dışarıda bırakan bir C kapalı küme verir;
    A ⊆ B ⊆ C olduğundan x ∈ cl(A) ise x ∈ C olmalı — çelişki. -/
theorem closure_mono_bycontra (τ : Topology α) {A B : Set α} (h : A ⊆ B) :
    closure τ A ⊆ closure τ B := by
  intro x hx
  by_contra hxnB
  simp only [closure, Set.mem_sInter, Set.mem_setOf_eq, not_forall] at hxnB
  obtain ⟨C, ⟨hCcl, hBC⟩, hxC⟩ := hxnB
  simp only [closure, Set.mem_sInter, Set.mem_setOf_eq] at hx
  exact hxC (hx C ⟨hCcl, h.trans hBC⟩)

/-- [ÇY] T2 ↔ diagonal kapalı (→ yön): p.1 = p.2 varsayımı U ∩ V = ∅ ile çelişir.

    `by_contra` + `simp [ne_eq, not_not]` yapısı, orijinalin
    doğrudan `intro hab` yapısından farklıdır. -/
theorem t2_diagonal_forward_bycontra (τ : Topology α) (ht2 : isT2 τ) :
    (prodTopology τ τ).isOpen {p : α × α | p.1 ≠ p.2} := by
  intro ⟨x, y⟩ hne
  obtain ⟨U, V, hUo, hVo, hxU, hyV, hUV⟩ := ht2 x y hne
  refine ⟨U, V, hUo, hVo, hxU, hyV, ?_⟩
  intro p ⟨hpU, hpV⟩
  by_contra hab
  simp only [Set.mem_setOf_eq, ne_eq, not_not] at hab
  -- hab : p.1 = p.2
  have haV : p.1 ∈ V := hab ▸ hpV
  have hmem : p.1 ∈ U ∩ V := ⟨hpU, haV⟩
  rw [hUV] at hmem; exact hmem.elim

end ByContradiction

-- ══════════════════════════════════════════════════════════════
-- §2  Karşıt ters (Contrapositive) [KT]
-- ══════════════════════════════════════════════════════════════

section ByContrapositive

/-!
Karşıt ters yapısı, "negatif" tanım üzerinden çalışan teoremler için
sıklıkla daha doğal olur: "x dışarıdaysa nereden dışarıda kalıyor?"
-/

/-- [KT] int(A ∪ B) ⊇ int(A) ∪ int(B): karşıt ters.

    x ∉ int(A ∪ B) ise her açık U ⊆ A ∪ B, x'i kapsamaz.
    Her açık U ⊆ A, U ⊆ A ∪ B olduğundan yine x'i kapsamaz → x ∉ int(A).
    Benzer şekilde x ∉ int(B). -/
theorem interior_union_subset_contra (τ : Topology α) (A B : Set α) :
    interior τ A ∪ interior τ B ⊆ interior τ (A ∪ B) := by
  intro x
  contrapose!
  -- Hedef: x ∉ int(A ∪ B) → x ∉ int(A) ∧ x ∉ int(B)
  intro hxnAB
  simp only [Set.mem_union, not_or]
  constructor
  · intro hxA
    apply hxnAB
    simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hxA ⊢
    obtain ⟨U, ⟨hUo, hUA⟩, hxU⟩ := hxA
    exact ⟨U, ⟨hUo, hUA.trans Set.subset_union_left⟩, hxU⟩
  · intro hxB
    apply hxnAB
    simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hxB ⊢
    obtain ⟨U, ⟨hUo, hUB⟩, hxU⟩ := hxB
    exact ⟨U, ⟨hUo, hUB.trans Set.subset_union_right⟩, hxU⟩

/-- [KT] int(A) ⊆ int(B) — A ⊆ B: karşıt ters.

    x ∉ int(B) ise, x ∈ int(A) varsayımıyla int(A) ⊆ int(B) üzerinden
    x ∈ int(B) türetilir — çelişki. -/
theorem interior_mono_contra (τ : Topology α) {A B : Set α} (h : A ⊆ B) :
    interior τ A ⊆ interior τ B := by
  intro x
  contrapose!
  intro hxnB hxA
  apply hxnB
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq] at hxA ⊢
  obtain ⟨U, ⟨hUo, hUA⟩, hxU⟩ := hxA
  exact ⟨U, ⟨hUo, hUA.trans h⟩, hxU⟩

/-- [KT] Yoğun küme her açık kümeyle kesişir: kesişmeme çelişkiye yol açar.

    U ∩ A = ∅ varsayımıyla A ⊆ Uᶜ; Uᶜ kapalı, cl(A) ⊆ Uᶜ;
    ama cl(A) = univ → U'da bir x olmalı ve x ∈ Uᶜ — çelişki. -/
theorem isDense_meets_open_contra (τ : Topology α) {A : Set α} (hd : isDense τ A)
    {U : Set α} (hUo : τ.isOpen U) (hUne : U.Nonempty) : (U ∩ A).Nonempty := by
  by_contra hempty
  rw [Set.not_nonempty_iff_eq_empty] at hempty
  have hAUc : A ⊆ Uᶜ := fun a haA haU => by
    have : a ∈ (∅ : Set α) := hempty ▸ Set.mem_inter haU haA
    exact this.elim
  have hUcCl : isClosed τ Uᶜ := by unfold isClosed; rw [compl_compl]; exact hUo
  have hclUc : closure τ A ⊆ Uᶜ :=
    Set.sInter_subset_of_mem ⟨hUcCl, hAUc⟩
  obtain ⟨x, hxU⟩ := hUne
  exact hclUc (hd.symm ▸ Set.mem_univ x) hxU

end ByContrapositive

-- ══════════════════════════════════════════════════════════════
-- §3  Alternatif doğrudan ispatlar (Alternative direct) [D]
-- ══════════════════════════════════════════════════════════════

section AlternativeDirect

/-!
"Doğrudan" ama orijinalden farklı: farklı bir ara lemma, farklı taktik seçimi
ya da daha kompakt bir terim-mod ifadesi.
-/

/-- [D] T2 → T0: T1 basamağını atlayarak tek adımda.

    Hausdorff ayrımından y ∉ U, U ∩ V = ∅ ile doğrudan türetilir;
    U T0 tanığı olarak kullanılır. -/
theorem t2_implies_t0_direct (τ : Topology α) (h : isT2 τ) : isT0 τ := by
  intro x y hne
  obtain ⟨U, V, hU, _hV, hxU, hyV, hdisj⟩ := h x y hne
  have hyU : y ∉ U := by
    intro hyU
    have hmem : y ∈ U ∩ V := ⟨hyU, hyV⟩
    rw [hdisj] at hmem; exact hmem.elim
  exact ⟨U, hU, Iff.intro (fun _ => hyU) (fun _ => hxU)⟩

/-- [D] T2 → T1: taktik modu, `⟨...⟩` bir adımda.

    Orijinal `refine` + `rw` zinciri kurar; bu versiyon `have` ile çelişkiyi
    daha açık gösterir. -/
theorem t2_implies_t1_have (τ : Topology α) (h : isT2 τ) : isT1 τ := by
  intro x y hne
  obtain ⟨U, V, hU, _hV, hxU, hyV, hdisj⟩ := h x y hne
  exact ⟨U, hU, hxU, fun hyU => by
    have hmem : y ∈ U ∩ V := ⟨hyU, hyV⟩
    rw [hdisj] at hmem; exact hmem.elim⟩

/-- [D] Kapalı kümeler kesişimi: `Classical.em` ile De Morgan.

    Orijinal `not_and_or` simp lemmasını kullanır.
    Bu versiyon klasik mantıkta ayrım yaparak açıkça kurulur. -/
theorem closed_inter_em (τ : Topology α) {C D : Set α}
    (hC : isClosed τ C) (hD : isClosed τ D) : isClosed τ (C ∩ D) := by
  unfold isClosed at *
  have hDeM : (C ∩ D)ᶜ = Cᶜ ∪ Dᶜ := by
    ext x
    constructor
    · intro hx
      rcases Classical.em (x ∈ C) with hxC | hxC
      · exact Or.inr (fun hxD => hx ⟨hxC, hxD⟩)
      · exact Or.inl hxC
    · rintro (hxCc | hxDc) ⟨hxC, hxD⟩
      · exact hxCc hxC
      · exact hxDc hxD
  rw [hDeM]; exact open_union τ hC hD

/-- [D] Sabit fonksiyon sürekli: `rcases` ile `by_cases` yerine. -/
theorem continuous_const_rcases (τ : Topology α) (σ : Topology β) (b : β) :
    isContinuous τ σ (fun _ => b) := by
  intro V _
  rcases Classical.em (b ∈ V) with hb | hb
  · convert τ.univ_open using 1; ext; simp [hb]
  · convert τ.empty_open using 1; ext; simp [hb]

/-- [D] A açık ↔ A = int(A): `open_subset_interior` lemmasına delege.

    Orijinal, A ⊆ int(A)'yı `simp` ile kurar.
    Bu versiyon mevcut `open_subset_interior` lemmasını kullanır. -/
theorem open_iff_eq_interior_alt (τ : Topology α) {A : Set α} :
    τ.isOpen A ↔ A = interior τ A :=
  ⟨fun hA => Set.Subset.antisymm
      (open_subset_interior τ hA (le_refl A))
      (interior_subset τ A),
   fun h => h ▸ interior_open τ A⟩

/-- [D] T1 ↔ tekil kümeler kapalıdır: `Iff.intro` terim modu. -/
theorem t1_iff_singletons_closed_term (τ : Topology α) :
    isT1 τ ↔ ∀ x : α, isClosed τ {x} :=
  Iff.intro (t1_singleton_closed τ) (fun h x y hne =>
    ⟨{y}ᶜ, h y, by simp [hne], by simp⟩)

/-- [D] cl(A ∪ B) = cl(A) ∪ cl(B): `sInter_subset_of_mem` doğrudan.

    Orijinal `simp only [closure, Set.mem_setOf_eq]` ile açar; burada
    üyelik kanıtı `sInter_subset_of_mem`'e hemen verilir. -/
theorem closure_union_direct (τ : Topology α) (A B : Set α) :
    closure τ (A ∪ B) = closure τ A ∪ closure τ B := by
  apply Set.Subset.antisymm
  · apply Set.sInter_subset_of_mem
    exact ⟨closed_union τ (closure_closed τ A) (closure_closed τ B),
           Set.union_subset_union (subset_closure τ A) (subset_closure τ B)⟩
  · exact Set.union_subset
      (closure_mono τ Set.subset_union_left)
      (closure_mono τ Set.subset_union_right)

/-- [D] int(A ∩ B) = int(A) ∩ int(B): `ext + constructor` yoluyla.

    Orijinal antisimetri kurar; burada iki yön `ext + constructor` ile açık. -/
theorem interior_inter_ext (τ : Topology α) (A B : Set α) :
    interior τ (A ∩ B) = interior τ A ∩ interior τ B := by
  ext x
  simp only [interior, Set.mem_sUnion, Set.mem_setOf_eq, Set.mem_inter_iff]
  constructor
  · rintro ⟨U, ⟨hUo, hUAB⟩, hxU⟩
    exact ⟨⟨U, ⟨hUo, hUAB.trans Set.inter_subset_left⟩, hxU⟩,
           ⟨U, ⟨hUo, hUAB.trans Set.inter_subset_right⟩, hxU⟩⟩
  · rintro ⟨⟨U, ⟨hUo, hUA⟩, hxU⟩, ⟨V, ⟨hVo, hVB⟩, hxV⟩⟩
    exact ⟨U ∩ V, ⟨τ.inter_open U V hUo hVo, Set.inter_subset_inter hUA hVB⟩, hxU, hxV⟩

/-- [D] int(A) ⊆ int(B) — A ⊆ B: `sUnion_subset_sUnion` ile.

    Orijinal eleman çıkarıp yeniden koyar (intro + simp + obtain + exact).
    Bu versiyon sUnion monotonluğunu doğrudan uygular:
    ⋃{açık ⊆ A} ⊆ ⋃{açık ⊆ B}. -/
theorem interior_mono_sUnion (τ : Topology α) {A B : Set α} (h : A ⊆ B) :
    interior τ A ⊆ interior τ B := by
  unfold interior
  apply Set.sUnion_subset_sUnion
  exact fun U ⟨hUo, hUA⟩ => ⟨hUo, hUA.trans h⟩

/-- [D] T4 → T2: aşamalı zinciri tek `exact` ile. -/
theorem t4_implies_t2_chain (τ : Topology α) (h : isT4 τ) : isT2 τ :=
  t3_implies_t2 τ (t4_implies_t3 τ h)

end AlternativeDirect

-- ══════════════════════════════════════════════════════════════
-- §4  Dualite yoluyla (Interior ↔ Closure duality) [De]
-- ══════════════════════════════════════════════════════════════

section Duality

/-!
`interior τ Aᶜ = (closure τ A)ᶜ` ve `closure τ Aᶜ = (interior τ A)ᶜ` eşitlikleri
bir **dualite** oluşturur. Bu bölümdeki ispatlar bu köprüyü kullanır.
-/

/-- [De] int(A) = cl(Aᶜ)ᶜ — `interior_compl` yerine `closure_compl` yoluyla.

    Orijinal `interior_eq_compl_closure_compl`, `interior_compl τ Aᶜ` kullanır.
    Bu versiyon `closure_compl τ A`'dan başlayıp çift tümleyen basitleştirir. -/
theorem interior_via_closure_compl (τ : Topology α) (A : Set α) :
    interior τ A = (closure τ Aᶜ)ᶜ := by
  have h : closure τ Aᶜ = (interior τ A)ᶜ := closure_compl τ A
  rw [h, compl_compl]

/-- [De] cl(A) = int(Aᶜ)ᶜ — `closure_compl` yerine `interior_compl` yoluyla. -/
theorem closure_via_interior_compl (τ : Topology α) (A : Set α) :
    closure τ A = (interior τ Aᶜ)ᶜ := by
  have h : interior τ Aᶜ = (closure τ A)ᶜ := interior_compl τ A
  rw [h, compl_compl]

/-- [De] Keyfi kapalı ailenin kesişimi kapalıdır — SetTopology.lean'da YOKTUR.

    Kanıt: açık birleşim aksiyomunun tam duali.
    `isClosed τ (⋂₀ F)` ↔ `τ.isOpen (⋃₀ {Cᶜ | C ∈ F})` açık. -/
theorem isClosed_sInter (τ : Topology α)
    {F : Set (Set α)} (hF : ∀ C ∈ F, isClosed τ C) :
    isClosed τ (⋂₀ F) := by
  unfold isClosed
  rw [Set.compl_sInter]
  apply τ.union_open
  rintro _ ⟨C, hCF, rfl⟩
  exact hF C hCF

/-- [De] cl(A ∪ B) = cl(A) ∪ cl(B): tümleyen dönüşümü yoluyla.

    Temel zincir (tümleyenlerde çalışarak):
    `(cl(A∪B))ᶜ = int((A∪B)ᶜ) = int(Aᶜ∩Bᶜ) = int(Aᶜ)∩int(Bᶜ) = (cl A)ᶜ∩(cl B)ᶜ = (cl A∪cl B)ᶜ`
    Tümleyen enjektif olduğundan sonuç çıkar. -/
theorem closure_union_duality (τ : Topology α) (A B : Set α) :
    closure τ (A ∪ B) = closure τ A ∪ closure τ B := by
  apply compl_injective
  -- Hedef: (cl(A ∪ B))ᶜ = (cl(A) ∪ cl(B))ᶜ
  rw [Set.compl_union,
      ← interior_compl τ A, ← interior_compl τ B,
      ← interior_inter, ← Set.compl_union,
      ← interior_compl τ (A ∪ B)]

end Duality

-- ══════════════════════════════════════════════════════════════
-- §5  Taktik-yoğun (Tactic-heavy) [Tak]
-- ══════════════════════════════════════════════════════════════

section TacticHeavy

/-!
Bu bölümdeki ispatlar `simp` ile mümkün olan en kısa ifadeyi hedefler.
-/

/-- [Tak] Boş küme kapalı: `unfold` + `rw` yerine `simp`. -/
theorem closed_empty_simp (τ : Topology α) : isClosed τ ∅ := by
  unfold isClosed
  simp only [Set.compl_empty, τ.univ_open]

/-- [Tak] Evrensel küme kapalı. -/
theorem closed_univ_simp (τ : Topology α) : isClosed τ Set.univ := by
  unfold isClosed
  simp only [Set.compl_univ, τ.empty_open]

/-- [Tak] cl(A) monoton: `sInter_subset_sInter` + lambda, tek satır. -/
theorem closure_mono_simp (τ : Topology α) {A B : Set α} (h : A ⊆ B) :
    closure τ A ⊆ closure τ B := by
  simp only [closure]
  exact Set.sInter_subset_sInter (fun C ⟨hCcl, hBC⟩ => ⟨hCcl, h.trans hBC⟩)

/-- [Tak] Bağlantılılık: konjunksiyon → iki ayrı öncül.

    `isConnected` tanımı `U, (h1 ∧ h2) → ...` biçimindedir; `and_imp` ile
    `U, h1 → h2 → ...` formuna dönüştürülür. -/
theorem connected_curried (τ : Topology α) :
    isConnected τ ↔
    ∀ U : Set α, τ.isOpen U → isClosed τ U → U = ∅ ∨ U = Set.univ := by
  unfold isConnected
  simp only [and_imp]

/-- [Tak] Sürekli fonksiyon kapanış görüntüsünü içerir:
    `hxcl`'yi simp ile açıp doğrudan uygulama.

    Orijinal, `Set.sInter_subset_of_mem` ile zincir kurar; burada
    `closure` tanımını `hxcl`'de açarak `∀ D, ... → x ∈ D` formunu alırız,
    ardından `f ⁻¹' C`'yi argüman olarak veririz. -/
theorem continuous_closure_image_simp (τ : Topology α) (σ : Topology β)
    {f : α → β} (hf : isContinuous τ σ f) (A : Set α) :
    f '' closure τ A ⊆ closure σ (f '' A) := by
  rintro y ⟨x, hxcl, rfl⟩
  simp only [closure, Set.mem_sInter, Set.mem_setOf_eq]
  intro C ⟨hCcl, hfAC⟩
  simp only [closure, Set.mem_sInter, Set.mem_setOf_eq] at hxcl
  exact hxcl _ ⟨continuous_preimage_closed τ σ hf hCcl,
                fun a haA => hfAC (Set.mem_image_of_mem f haA)⟩

end TacticHeavy

end Alt
end SetTopology
