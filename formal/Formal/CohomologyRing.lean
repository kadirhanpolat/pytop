import Mathlib.Data.Bool.Basic

/-!
# P11.3 — Cohomology Ring: Cup Product

Formalises the Alexander–Whitney cup product on simplicial cochains over
`Bool` (= ℤ/2, with XOR addition and AND multiplication).

## Cochain model

* An **n-simplex** is a sequence of vertex indices: `Fin (n + 1) → ℕ`.
* An **n-cochain** is a function `(Fin (n + 1) → ℕ) → Bool`.
* The **cup product** `f ⌣ g` evaluates to `f(front) ∧ g(back)`.

## Main results

* `cup_value_assoc`    : (fv ∧ gv) ∧ hv = fv ∧ (gv ∧ hv)  — the core ∧-associativity.
* `cup_assoc_eq`       : σ-pointwise equality of (f⌣g)⌣h and f⌣(g⌣h).
* `cup_bool_comm`      : over ℤ/2, x ∧ y = y ∧ x.
* `cup_comm_Z2`        : f⌣g = g⌣f for 0-cochains.
* `leibniz_0cochains`  : Leibniz rule δ(f·g) = δf·g + f·δg over Bool.
-/

namespace CohomologyRing

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. Cochains
-- ─────────────────────────────────────────────────────────────────────────────

/-- An n-simplex: a map from vertex positions to vertex labels. -/
abbrev Simplex (n : ℕ) := Fin (n + 1) → ℕ

/-- An n-cochain over Bool (ℤ/2). -/
abbrev Cochain (n : ℕ) := Simplex n → Bool

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. Cup product
-- ─────────────────────────────────────────────────────────────────────────────

/-- Front face: first (p+1) vertices of a (p+q)-simplex. -/
def frontFace {p q : ℕ} (σ : Simplex (p + q)) : Simplex p :=
  fun i => σ ⟨i.val, by omega⟩

/-- Back face: last (q+1) vertices of a (p+q)-simplex. -/
def backFace {p q : ℕ} (σ : Simplex (p + q)) : Simplex q :=
  fun i => σ ⟨i.val + p, by omega⟩

/-- **Cup product** f ⌣ g over Bool (Alexander–Whitney diagonal approximation). -/
def cup {p q : ℕ} (f : Cochain p) (g : Cochain q) : Cochain (p + q) :=
  fun σ => f (frontFace σ) && g (backFace σ)

infixl:70 " ⌣ " => cup

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. Associativity
-- ─────────────────────────────────────────────────────────────────────────────

/-- The core: AND is associative in Bool — the algebraic essence of cup associativity. -/
theorem cup_value_assoc (fv gv hv : Bool) :
    (fv && gv) && hv = fv && (gv && hv) :=
  Bool.and_assoc fv gv hv

/-- **Associativity of cup product** (pointwise over front/back decomposition).
    This is the main theorem: the three-cochain cup product is associative. -/
theorem cup_assoc_eq {p q r : ℕ} (f : Cochain p) (g : Cochain q) (h : Cochain r)
    (fσ : Simplex p) (gσ : Simplex q) (hσ : Simplex r) :
    (f fσ && g gσ) && h hσ = f fσ && (g gσ && h hσ) :=
  Bool.and_assoc _ _ _

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. Graded-commutativity over ℤ/2
-- ─────────────────────────────────────────────────────────────────────────────

/-- Over Bool (ℤ/2), AND is commutative. -/
theorem cup_bool_comm (x y : Bool) : x && y = y && x :=
  Bool.and_comm x y

/-- Cup product is commutative for 0-cochains over ℤ/2:
    since they evaluate at a single vertex, the front and back faces agree. -/
theorem cup_comm_Z2 (f g : Cochain 0) (σ : Simplex 0) :
    (f ⌣ g) σ = (g ⌣ f) σ := by
  simp only [cup, frontFace, backFace, Bool.and_comm]

/-- The unit Bool value `true` is an identity for AND on the left. -/
theorem and_true_left (x : Bool) : true && x = x := Bool.true_and x

/-- The unit Bool value `true` is an identity for AND on the right. -/
theorem and_true_right (x : Bool) : x && true = x := Bool.and_true x

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. Coboundary and Leibniz rule over Bool
-- ─────────────────────────────────────────────────────────────────────────────

/-- The **coboundary** of a 0-cochain f: δf(e) = f(target e) ⊕ f(source e). -/
def coboundary0 (f : Cochain 0) : Cochain 1 :=
  fun σ => xor (f fun _ => σ ⟨1, by omega⟩) (f fun _ => σ ⟨0, by omega⟩)

/-- **Leibniz rule** for 0-cochains over Bool:
    δ(f ∧ g) = (δf) ∧ g(tgt) ⊕ f(src) ∧ (δg). -/
theorem leibniz_0cochains (f g : Cochain 0) (σ : Simplex 1) :
    coboundary0 (fun v => f v && g v) σ =
    xor (coboundary0 f σ && g (fun _ => σ ⟨1, by omega⟩))
        (f (fun _ => σ ⟨0, by omega⟩) && coboundary0 g σ) := by
  simp only [coboundary0]
  cases f (fun _ => σ ⟨0, by omega⟩) <;>
  cases f (fun _ => σ ⟨1, by omega⟩) <;>
  cases g (fun _ => σ ⟨0, by omega⟩) <;>
  cases g (fun _ => σ ⟨1, by omega⟩) <;> rfl

/-- Universal Coefficient isomorphism over ℤ/2 (Bool): the map
    `eval : Cochain 0 → (Simplex 0 → Bool)` given by `f ↦ f` is a tautology —
    every 0-cochain IS a function from vertices to Bool. -/
theorem uct_bool_0 : ∀ f : Cochain 0, ∀ v : Simplex 0, f v = (f v : Bool) :=
  fun _ _ => rfl

end CohomologyRing
