import Mathlib.Algebra.Group.Hom.Basic

/-!
# P11.5 — Spectral Sequences: Formal Properties

Models a spectral sequence as a ℕ-indexed family of chain complexes over an additive group.
Every chain complex satisfies d ∘ d = 0 **by construction**; the file proves consequences.

## Main results

* `d_sq_zero`              : d(d(x)) = 0 — the fundamental chain complex identity.
* `image_sub_kernel`       : im(d) ⊆ ker(d) — every boundary is a cycle.
* `const_convergent`       : the constant spectral sequence converges.
* `stabilizes_mono`        : stabilisation is upward-closed in the page index.
* `same_diff_implies_same_stab` : two sequences agreeing from r₀ onward share stabilisation.
-/

namespace SpectralSequences

-- ─────────────────────────────────────────────────────────────────────────────
-- 1.  Chain complex
-- ─────────────────────────────────────────────────────────────────────────────

/-- A **chain complex** over an additive group: a group endomorphism d with d ∘ d = 0. -/
structure ChainCx (α : Type*) [AddCommGroup α] where
  d  : α →+ α
  sq : ∀ x : α, d (d x) = 0

variable {α : Type*} [AddCommGroup α]

/-- d² = 0 — directly from the chain complex axiom. -/
theorem d_sq_zero (c : ChainCx α) (x : α) : c.d (c.d x) = 0 :=
  c.sq x

/-- Every element in the image of d is a cycle (lies in ker d). -/
theorem image_sub_kernel (c : ChainCx α) {x : α} (hx : ∃ y : α, c.d y = x) :
    c.d x = 0 := by
  obtain ⟨y, rfl⟩ := hx
  exact c.sq y

/-- The **zero chain complex**: d ≡ 0 is a valid chain complex. -/
def zeroCx : ChainCx α where
  d  := 0
  sq := fun _ => rfl

/-- For the zero chain complex, every element is a cycle. -/
theorem zero_cx_all_cycles (x : α) : (zeroCx (α := α)).d x = 0 := rfl

-- ─────────────────────────────────────────────────────────────────────────────
-- 2.  Spectral sequence
-- ─────────────────────────────────────────────────────────────────────────────

/-- A **spectral sequence**: a ℕ-indexed family of chain complexes (pages). -/
structure SpectralSeq (α : Type*) [AddCommGroup α] where
  page : ℕ → ChainCx α

/-- The sequence **stabilises at r₀**: every page r ≥ r₀ equals page r₀. -/
def StabilizesAt (ss : SpectralSeq α) (r₀ : ℕ) : Prop :=
  ∀ r : ℕ, r₀ ≤ r → ss.page r = ss.page r₀

/-- A spectral sequence **converges** if it eventually stabilises. -/
def Convergent (ss : SpectralSeq α) : Prop :=
  ∃ r₀ : ℕ, StabilizesAt ss r₀

-- ─────────────────────────────────────────────────────────────────────────────
-- 3.  Convergence theorems
-- ─────────────────────────────────────────────────────────────────────────────

/-- The constant spectral sequence (every page the same) converges at r₀ = 0. -/
theorem const_convergent (c : ChainCx α) :
    Convergent ⟨fun _ => c⟩ :=
  ⟨0, fun _ _ => rfl⟩

/-- Stabilisation is upward-closed: if it stabilises at r₀ and r₀ ≤ r₁,
    it also stabilises at r₁. -/
theorem stabilizes_mono (ss : SpectralSeq α) {r₀ r₁ : ℕ} (h : r₀ ≤ r₁)
    (hs : StabilizesAt ss r₀) : StabilizesAt ss r₁ := by
  intro r hr
  rw [hs r (h.trans hr), hs r₁ h]

/-- If two spectral sequences agree on all pages ≥ r₀ and one stabilises at r₀,
    so does the other. -/
theorem same_diff_implies_same_stab (ss₁ ss₂ : SpectralSeq α) (r₀ : ℕ)
    (hpage : ∀ r : ℕ, r₀ ≤ r → ss₁.page r = ss₂.page r)
    (hs₁ : StabilizesAt ss₁ r₀) : StabilizesAt ss₂ r₀ := by
  intro r hr
  rw [← hpage r hr, hs₁ r hr, hpage r₀ le_rfl]

/-- If a spectral sequence stabilises at r₀, it converges. -/
theorem stabilizes_implies_convergent (ss : SpectralSeq α) (r₀ : ℕ)
    (hs : StabilizesAt ss r₀) : Convergent ss :=
  ⟨r₀, hs⟩

/-- Stabilisation witnesses propagate upward: stabilising at r₀ implies stabilising at r₀ + 1. -/
theorem stabilizes_succ (ss : SpectralSeq α) {r₀ : ℕ} (hs : StabilizesAt ss r₀) :
    StabilizesAt ss (r₀ + 1) :=
  stabilizes_mono ss (Nat.le_add_right r₀ 1) hs

/-- A spectral sequence whose pages are all equal converges at every stage. -/
theorem const_pages_convergent (ss : SpectralSeq α) (c : ChainCx α)
    (hconst : ∀ r : ℕ, ss.page r = c) : Convergent ss :=
  ⟨0, fun r _ => (hconst r).trans (hconst 0).symm⟩

end SpectralSequences
