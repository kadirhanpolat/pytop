import Mathlib.Data.Bool.Basic
import Mathlib.Data.Fin.Basic

/-!
# P11.3 — Cohomology Ring: Cup Product

Formalises the Alexander–Whitney cup product on simplicial cochains over
`Bool` (= ℤ/2, with XOR addition and AND multiplication).

## Cochain model

* An **n-simplex** is a sequence of vertex indices: `Fin (n + 1) → ℕ`.
* An **n-cochain** is a function `(Fin (n + 1) → ℕ) → Bool`.
* The **cup product** `f ⌣ g` evaluates to `f(front) ∧ g(back)`.

## Main results

* `cup_value_assoc`    : (fv ∧ gv) ∧ hv = fv ∧ (gv ∧ hv) — the Bool identity behind associativity.
* `cup_assoc`          : ((f ⌣ g) ⌣ h) σ = (f ⌣ (g ⌣ h)) σ' on every (p+q+r)-simplex σ, where σ'
                         is σ re-indexed along p + q + r = p + (q + r) — associativity of the cup
                         product itself, i.e. the front/back faces line up.
* `cup_bool_comm`      : over ℤ/2, x ∧ y = y ∧ x.
* `cup_comm_Z2`        : f⌣g = g⌣f for 0-cochains.
* `leibniz_0cochains`  : Leibniz rule δ(f·g) = δf·g + f·δg for 0-cochains over Bool.

## Scope

Cochains here are Bool-valued functions on ordered vertex sequences; there is no simplicial
complex, coboundary in degrees > 0, or passage to cohomology classes. The statements are about
the cochain-level operations only.
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

@[simp] theorem frontFace_apply {p q : ℕ} (σ : Simplex (p + q)) (i : Fin (p + 1)) :
    frontFace σ i = σ ⟨i.val, by omega⟩ := rfl

@[simp] theorem backFace_apply {p q : ℕ} (σ : Simplex (p + q)) (i : Fin (q + 1)) :
    backFace σ i = σ ⟨i.val + p, by omega⟩ := rfl

/-- **Cup product** f ⌣ g over Bool (Alexander–Whitney diagonal approximation). -/
def cup {p q : ℕ} (f : Cochain p) (g : Cochain q) : Cochain (p + q) :=
  fun σ => f (frontFace σ) && g (backFace σ)

infixl:70 " ⌣ " => cup

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. Associativity
-- ─────────────────────────────────────────────────────────────────────────────

/-- The core: AND is associative in Bool — the algebraic essence of cup associativity. -/
theorem cup_value_assoc (fv gv hv : Bool) :
    ((fv && gv) && hv) = (fv && (gv && hv)) :=
  Bool.and_assoc fv gv hv

/-- **Associativity of the cup product**: on a (p+q+r)-simplex σ, `(f ⌣ g) ⌣ h` takes the value
    `f ⌣ (g ⌣ h)` takes on σ re-indexed along `p + q + r = p + (q + r)`. The content is that the
    three faces agree: vertices `0..p`, `p..p+q` and `p+q..p+q+r` either way. -/
theorem cup_assoc {p q r : ℕ} (f : Cochain p) (g : Cochain q) (h : Cochain r)
    (σ : Simplex (p + q + r)) :
    ((f ⌣ g) ⌣ h) σ = (f ⌣ (g ⌣ h)) (fun i => σ (Fin.cast (by omega) i)) := by
  simp only [cup]
  rw [Bool.and_assoc]
  -- The first two faces agree definitionally; the last needs i + (p + q) = i + q + p.
  congr 1
  congr 1
  congr 1
  funext i
  simp only [backFace_apply, Fin.cast_mk]
  congr 1
  simp only [Fin.mk.injEq]
  omega

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. Graded-commutativity over ℤ/2
-- ─────────────────────────────────────────────────────────────────────────────

/-- Over Bool (ℤ/2), AND is commutative. -/
theorem cup_bool_comm (x y : Bool) : (x && y) = (y && x) :=
  Bool.and_comm x y

/-- Cup product is commutative for 0-cochains over ℤ/2:
    since they evaluate at a single vertex, the front and back faces agree. -/
theorem cup_comm_Z2 (f g : Cochain 0) (σ : Simplex 0) :
    (f ⌣ g) σ = (g ⌣ f) σ := by
  have faces : frontFace (p := 0) (q := 0) σ = backFace (p := 0) (q := 0) σ := by
    funext i; simp [frontFace, backFace]
  simp only [cup, faces]
  exact Bool.and_comm _ _

/-- The unit Bool value `true` is an identity for AND on the left. -/
theorem and_true_left (x : Bool) : (true && x) = x := Bool.true_and x

/-- The unit Bool value `true` is an identity for AND on the right. -/
theorem and_true_right (x : Bool) : (x && true) = x := Bool.and_true x

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

end CohomologyRing
