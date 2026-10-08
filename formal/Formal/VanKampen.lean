import Mathlib.Algebra.Group.Hom.Basic
import Mathlib.Data.Int.Cast.Lemmas

/-!
# P11.2 — Van Kampen: Amalgamated Free Product

Formalises the algebraic core of the Seifert–van Kampen theorem.

## Model

The key algebraic content is the **universal property of the pushout** (amalgamated free
product) and **Tietze moves** on group presentations.

## Main results

* `tietze_equiv_refl` / `tietze_equiv_symm` / `tietze_equiv_trans` : `TietzeEquiv` is an
  equivalence relation (symmetry is the content: each move has an inverse move).
* `tietze_add_gen`, `tietze_elim` : the two generating moves, as constructors.
* `pushout_compat_preserved` : a map out of a pushout respects the amalgamation.
* `pushout_universal` : bookkeeping — a map `u` that agrees with `f₁` and `f₂` on the two
  inclusions does so for every pair of elements.
* `int_hom_determined_by_one`, `int_hom_exists` : ℤ is free abelian on `1`.

## Scope

`Pres` and `TietzeEquiv` are syntactic — no group is attached to a presentation — so nothing
here says Tietze moves preserve the presented group, and `Pushout` is a cocone rather than a
constructed amalgamated free product. pytop's computational van Kampen lives in
`src/pytop/van_kampen.py`; this file formalises only the relational bookkeeping around it.
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
    (h : f 1 = g 1) : f = g :=
  AddMonoidHom.ext_int h

/-- Existence part: every element k ∈ K is the image of 1 under some ℤ →+ K. -/
theorem int_hom_exists {K : Type*} [AddCommGroup K] (k : K) :
    ∃ f : ℤ →+ K, f 1 = k :=
  ⟨zmultiplesHom K k, by simp⟩

end VanKampen
