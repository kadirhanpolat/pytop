import Mathlib.Algebra.Group.Hom.Basic

/-!
# P11.1 — Mayer–Vietoris: Connecting Homomorphism

Formalises the algebraic core of the Mayer–Vietoris long exact sequence:
the **connecting homomorphism** δ and its well-definedness.

## Model

A **short exact sequence** (SES) 0 → A →ⁱ B →ᵖ C → 0 is encoded as a
structure with exactness witnessed at every position.

## Main results

* `delta_well_defined`       : two lifts of the same c ∈ C differ by an element of im i.
* `ses_i_injective`          : the left map i is injective (exactness at A).
* `ses_p_zero_of_im`         : p ∘ i = 0 (exactness gives ker p ⊇ im i).
* `snake_delta_exists`       : given a commutative square of SES's and c ∈ ker h,
                               a unique preimage in A' exists via the snake diagram.
* `snake_delta_independent`  : the choice of lift b does not affect the A'-class.
-/

namespace MayerVietoris

variable {A B C A' B' C' : Type*}
variable [AddCommGroup A] [AddCommGroup B] [AddCommGroup C]
variable [AddCommGroup A'] [AddCommGroup B'] [AddCommGroup C']

-- ─────────────────────────────────────────────────────────────────────────────
-- 1.  Short exact sequence
-- ─────────────────────────────────────────────────────────────────────────────

/-- A **short exact sequence** 0 → A →ⁱ B →ᵖ C → 0.
    * `i_inj`      : i is injective (exactness at A).
    * `exact_at_B` : ker p = im i (exactness at B).
    * `p_surj`     : p is surjective (exactness at C). -/
structure SES (A B C : Type*) [AddCommGroup A] [AddCommGroup B] [AddCommGroup C] where
  i          : A →+ B
  p          : B →+ C
  i_inj      : Function.Injective i
  exact_at_B : ∀ b : B, p b = 0 ↔ ∃ a : A, i a = b
  p_surj     : Function.Surjective p

-- ─────────────────────────────────────────────────────────────────────────────
-- 2.  Basic SES lemmas
-- ─────────────────────────────────────────────────────────────────────────────

/-- p ∘ i = 0: the composition of the two maps is zero. -/
theorem ses_p_zero_of_im (ses : SES A B C) (a : A) : ses.p (ses.i a) = 0 :=
  (ses.exact_at_B _).mpr ⟨a, rfl⟩

/-- i is injective — restated for external use. -/
theorem ses_i_injective (ses : SES A B C) : Function.Injective ses.i :=
  ses.i_inj

/-- p is surjective — restated for external use. -/
theorem ses_p_surjective (ses : SES A B C) : Function.Surjective ses.p :=
  ses.p_surj

-- ─────────────────────────────────────────────────────────────────────────────
-- 3.  Connecting homomorphism — well-definedness
-- ─────────────────────────────────────────────────────────────────────────────

/-- **delta_well_defined**: if p(b₁) = p(b₂) then b₁ − b₂ ∈ im i.
    This is the key step showing the connecting morphism δ : C → A/im(f) is
    independent of the choice of lift. -/
theorem delta_well_defined (ses : SES A B C) {b₁ b₂ : B}
    (h : ses.p b₁ = ses.p b₂) : ∃ a : A, ses.i a = b₁ - b₂ := by
  apply (ses.exact_at_B _).mp
  simp [map_sub, h]

/-- Mayer–Vietoris lift independence: two lifts of the same c ∈ C differ by im i. -/
theorem mv_connecting_indep (ses : SES A B C) (c : C)
    (b₁ b₂ : B) (h₁ : ses.p b₁ = c) (h₂ : ses.p b₂ = c) :
    ∃ a : A, ses.i a = b₁ - b₂ :=
  delta_well_defined ses (h₁.trans h₂.symm)

-- ─────────────────────────────────────────────────────────────────────────────
-- 4.  Snake diagram
-- ─────────────────────────────────────────────────────────────────────────────

/-- **snake_delta_exists**: given a commutative morphism of SES's
    ```
       0 → A  →ⁱ  B  →ᵖ  C  → 0
           ↓f      ↓g      ↓h
       0 → A' →ⁱ' B' →ᵖ' C' → 0
    ```
    and an element b ∈ B whose image in C' is zero (h(p(b)) = 0),
    g(b) lies in im i', i.e., there exists a' ∈ A' with i'(a') = g(b). -/
theorem snake_delta_exists (ses : SES A B C) (ses' : SES A' B' C')
    (f : A →+ A') (g : B →+ B') (h : C →+ C')
    (comm_i : ∀ a : A, g (ses.i a) = ses'.i (f a))
    (comm_p : ∀ b : B, h (ses.p b) = ses'.p (g b))
    (b : B) (hzero : h (ses.p b) = 0) :
    ∃ a' : A', ses'.i a' = g b := by
  apply (ses'.exact_at_B (g b)).mp
  rw [← comm_p b, hzero]

/-- **snake_delta_independent**: with two lifts b, b' of the same c and the snake
    diagram above, the A'-preimages a', a'' of g(b) and g(b') satisfy
    i'(a' − a'') ∈ im i', i.e., they define the same class in A'/im(f). -/
theorem snake_delta_independent (ses : SES A B C) (ses' : SES A' B' C')
    (f : A →+ A') (g : B →+ B') (h : C →+ C')
    (comm_i : ∀ a : A, g (ses.i a) = ses'.i (f a))
    (comm_p : ∀ b : B, h (ses.p b) = ses'.p (g b))
    (c : C) (b₁ b₂ : B) (hb₁ : ses.p b₁ = c) (hb₂ : ses.p b₂ = c)
    (hzero : h c = 0)
    (a₁ a₂ : A') (ha₁ : ses'.i a₁ = g b₁) (ha₂ : ses'.i a₂ = g b₂) :
    ∃ a : A, f a = a₁ - a₂ := by
  -- b₁ - b₂ ∈ ker p, so ∃ a, i(a) = b₁ - b₂
  obtain ⟨a, ha⟩ := mv_connecting_indep ses c b₁ b₂ hb₁ hb₂
  use a
  apply ses'.i_inj
  -- i'(f(a)) = g(i(a)) = g(b₁ - b₂) = g(b₁) - g(b₂) = i'(a₁) - i'(a₂) = i'(a₁ - a₂)
  calc ses'.i (f a)
      = g (ses.i a)              := (comm_i a).symm
    _ = g (b₁ - b₂)             := by rw [ha]
    _ = g b₁ - g b₂             := map_sub g b₁ b₂
    _ = ses'.i a₁ - ses'.i a₂   := by rw [ha₁, ha₂]
    _ = ses'.i (a₁ - a₂)        := (map_sub ses'.i a₁ a₂).symm

end MayerVietoris
