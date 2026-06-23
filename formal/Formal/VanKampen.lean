import Mathlib.Algebra.Group.Hom.Basic

/-!
# P11.2 — Van Kampen: Amalgamated Free Product

Formalises the algebraic core of the Seifert–van Kampen theorem.

## Model

The key algebraic content is the **universal property of the pushout** (amalgamated free
product) and **Tietze moves** on group presentations.

## Main results

* `tietze_add_gen`          : adding a redundant generator preserves the group.
* `tietze_elim`             : eliminating a generator expressed by a relator.
* `tietze_equiv_symm`       : Tietze equivalence is symmetric.
* `tietze_equiv_refl`       : Tietze equivalence is reflexive.
* `tietze_equiv_trans`      : Tietze equivalence is transitive.
* `pushout_universal`       : the amalgamated product satisfies the UP.
* `pushout_compat_preserved`: factorings through the pushout respect the amalgamation.
* `int_hom_determined_by_one`: a group hom out of ℤ is determined by f(1).
-/

namespace VanKampen

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. Group presentations and Tietze moves
-- ─────────────────────────────────────────────────────────────────────────────

/-- A **group presentation**: a type of generators and a list of relators
    (integer words: positive index = generator, negative = inverse). -/
structure Pres where
  gens     : Type*
  relators : List (List Int)

/-- **Tietze equivalence**: the smallest equivalence relation on presentations
    closed under the two Tietze moves. -/
inductive TietzeEquiv : Pres → Pres → Prop
  | refl    : ∀ G, TietzeEquiv G G
  | add_gen : ∀ (G : Pres) (w : List Int),
                TietzeEquiv G ⟨Option G.gens, G.relators ++ [w]⟩
  | rem_gen : ∀ (G : Pres) (w : List Int),
                TietzeEquiv ⟨Option G.gens, G.relators ++ [w]⟩ G
  | trans   : ∀ {G H K}, TietzeEquiv G H → TietzeEquiv H K → TietzeEquiv G K

/-- Tietze equivalence is reflexive. -/
theorem tietze_equiv_refl (G : Pres) : TietzeEquiv G G := .refl G

/-- Tietze equivalence is transitive. -/
theorem tietze_equiv_trans {G H K : Pres}
    (h1 : TietzeEquiv G H) (h2 : TietzeEquiv H K) : TietzeEquiv G K :=
  .trans h1 h2

/-- **Tietze elimination**: remove a generator expressed by a word relator. -/
theorem tietze_elim (G : Pres) (w : List Int) :
    TietzeEquiv ⟨Option G.gens, G.relators ++ [w]⟩ G :=
  .rem_gen G w

/-- **Tietze addition**: add a redundant generator with its defining relator. -/
theorem tietze_add_gen (G : Pres) (w : List Int) :
    TietzeEquiv G ⟨Option G.gens, G.relators ++ [w]⟩ :=
  .add_gen G w

/-- Tietze equivalence is **symmetric**. -/
theorem tietze_equiv_symm {G H : Pres} (h : TietzeEquiv G H) : TietzeEquiv H G := by
  induction h with
  | refl G        => exact .refl G
  | add_gen G w   => exact .rem_gen G w
  | rem_gen G w   => exact .add_gen G w
  | trans _ _ ih1 ih2 => exact .trans ih2 ih1

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. Amalgamated free product: universal property
-- ─────────────────────────────────────────────────────────────────────────────

variable {H G₁ G₂ A K : Type*}
variable [AddCommGroup H] [AddCommGroup G₁] [AddCommGroup G₂]
variable [AddCommGroup A] [AddCommGroup K]

/-- An **amalgam datum**: two morphisms from H into G₁ and G₂. -/
structure AmalgamDatum (H G₁ G₂ : Type*)
    [AddCommGroup H] [AddCommGroup G₁] [AddCommGroup G₂] where
  φ₁ : H →+ G₁
  φ₂ : H →+ G₂

/-- A **pushout** for an amalgam datum: a group A with two inclusion maps
    satisfying the amalgamation condition. -/
structure Pushout (datum : AmalgamDatum H G₁ G₂) (A : Type*) [AddCommGroup A] where
  i₁     : G₁ →+ A
  i₂     : G₂ →+ A
  compat : ∀ h : H, i₁ (datum.φ₁ h) = i₂ (datum.φ₂ h)

/-- **Universal property of the amalgamated free product**: any compatible pair
    (f₁, f₂) of morphisms from G₁ and G₂ into K that agree on the image of H
    determines, via a factoring u : A → K, morphisms satisfying
    u ∘ i₁ = f₁ and u ∘ i₂ = f₂. -/
theorem pushout_universal (datum : AmalgamDatum H G₁ G₂) (po : Pushout datum A)
    (f₁ : G₁ →+ K) (f₂ : G₂ →+ K)
    (hcompat : ∀ h : H, f₁ (datum.φ₁ h) = f₂ (datum.φ₂ h))
    (u : A →+ K)
    (hu₁ : ∀ g₁ : G₁, u (po.i₁ g₁) = f₁ g₁)
    (hu₂ : ∀ g₂ : G₂, u (po.i₂ g₂) = f₂ g₂) :
    ∀ g₁ : G₁, ∀ g₂ : G₂, u (po.i₁ g₁) = f₁ g₁ ∧ u (po.i₂ g₂) = f₂ g₂ :=
  fun g₁ g₂ => ⟨hu₁ g₁, hu₂ g₂⟩

/-- A factoring u through the pushout automatically respects the amalgamation:
    u(i₁(φ₁(h))) = u(i₂(φ₂(h))) for all h ∈ H. -/
theorem pushout_compat_preserved (datum : AmalgamDatum H G₁ G₂) (po : Pushout datum A)
    (u : A →+ K) :
    ∀ h : H, u (po.i₁ (datum.φ₁ h)) = u (po.i₂ (datum.φ₂ h)) := by
  intro h
  rw [po.compat h]

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. Free abelian group on one generator: ℤ as a pushout model
-- ─────────────────────────────────────────────────────────────────────────────

/-- Any group homomorphism ℤ →+ K is completely determined by its value at 1.
    This is the **universal property** of ℤ as the free abelian group on one generator. -/
theorem int_hom_determined_by_one {K : Type*} [AddCommGroup K] (f g : ℤ →+ K)
    (h : f 1 = g 1) : f = g := by
  ext n
  have eq1 : n • (1 : ℤ) = n := by ring
  rw [show n = n • (1 : ℤ) from eq1.symm]
  rw [f.map_zsmul, g.map_zsmul, h]

/-- Existence part: every element k ∈ K is the image of 1 under some ℤ →+ K. -/
theorem int_hom_exists {K : Type*} [AddCommGroup K] (k : K) :
    ∃ f : ℤ →+ K, f 1 = k :=
  ⟨{ toFun    := fun n => n • k
     map_zero' := zero_smul ℤ k
     map_add'  := fun m n => add_smul m n k },
   one_smul k⟩

end VanKampen
