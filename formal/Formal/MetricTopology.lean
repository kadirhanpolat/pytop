import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Formal.SetTopology

/-!
# Yol 6: Metrik Uzay Topolojisi

Bir metrik uzaydan türetilen topoloji ve temel özelliklerinin Lean 4 ile
formal doğrulaması.

## Yapı

* **MetricSpace** — uzaklık fonksiyonu + 4 aksiyom.
* **metricTopology** — açık toplar yoluyla türetilen topoloji.
* **openBall_isOpen** — her açık top açıktır.
* **epsDelta ↔ topoCont** — ε-δ sürekliliği ↔ topolojik süreklilik.
-/

namespace MetricTopology

open SetTopology

variable {α β : Type*}

-- ──────────────────────────────────────────────────────────
-- 1. Metrik uzay yapısı
-- ──────────────────────────────────────────────────────────

/-- Bir **metrik uzay**: uzaklık fonksiyonu + aksiyomlar. -/
structure MetricSpace (α : Type*) where
  dist          : α → α → ℝ
  dist_self     : ∀ x : α, dist x x = 0
  dist_symm     : ∀ x y : α, dist x y = dist y x
  dist_nonneg   : ∀ x y : α, 0 ≤ dist x y
  dist_triangle : ∀ x y z : α, dist x z ≤ dist x y + dist y z
  dist_pos      : ∀ x y : α, x ≠ y → 0 < dist x y

-- ──────────────────────────────────────────────────────────
-- 2. Açık top ve türetilmiş topoloji
-- ──────────────────────────────────────────────────────────

/-- `x` merkezli `r` yarıçaplı **açık top**. -/
def openBall (M : MetricSpace α) (x : α) (r : ℝ) : Set α :=
  {y | M.dist x y < r}

theorem mem_openBall {M : MetricSpace α} {x y : α} {r : ℝ} :
    y ∈ openBall M x r ↔ M.dist x y < r :=
  Iff.rfl

/-- Metrik uzaydan türetilen **topoloji**: her nokta bir açık topla örtülür. -/
def metricTopology (M : MetricSpace α) : Topology α where
  isOpen U := ∀ x ∈ U, ∃ r > 0, openBall M x r ⊆ U
  empty_open := fun _ hx => False.elim ((Set.mem_empty_iff_false _).mp hx)
  univ_open  := fun x _ => ⟨1, by norm_num, Set.subset_univ _⟩
  union_open := by
    intro F hF x ⟨W, hWF, hxW⟩
    obtain ⟨r, hr, hball⟩ := hF W hWF x hxW
    exact ⟨r, hr, hball.trans (Set.subset_sUnion_of_mem hWF)⟩
  inter_open := by
    intro U V hU hV x ⟨hxU, hxV⟩
    obtain ⟨r₁, hr₁, hb₁⟩ := hU x hxU
    obtain ⟨r₂, hr₂, hb₂⟩ := hV x hxV
    refine ⟨min r₁ r₂, lt_min hr₁ hr₂, fun y hy => ?_⟩
    rw [mem_openBall] at hy
    exact ⟨hb₁ (mem_openBall.mpr (lt_of_lt_of_le hy (min_le_left _ _))),
           hb₂ (mem_openBall.mpr (lt_of_lt_of_le hy (min_le_right _ _)))⟩

-- ──────────────────────────────────────────────────────────
-- 3. Açık top gerçekten açıktır
-- ──────────────────────────────────────────────────────────

/-- Her açık top, metrik topolojide açıktır. -/
theorem openBall_isOpen (M : MetricSpace α) (x : α) (r : ℝ) :
    (metricTopology M).isOpen (openBall M x r) := by
  intro y hy
  rw [mem_openBall] at hy
  refine ⟨r - M.dist x y, by linarith, fun z hz => ?_⟩
  rw [mem_openBall] at hz ⊢
  calc M.dist x z ≤ M.dist x y + M.dist y z := M.dist_triangle x y z
       _           < M.dist x y + (r - M.dist x y) := by linarith
       _           = r                              := by linarith

-- ──────────────────────────────────────────────────────────
-- 4. ε-δ ↔ topolojik süreklilik (noktasal)
-- ──────────────────────────────────────────────────────────

/-- **ε-δ sürekliliği** `x₀` noktasında. -/
def epsilonDeltaContinuous (M : MetricSpace α) (N : MetricSpace β)
    (f : α → β) (x₀ : α) : Prop :=
  ∀ ε > 0, ∃ δ > 0, ∀ x, M.dist x₀ x < δ → N.dist (f x₀) (f x) < ε

/-- ε-δ sürekliliği → topolojik lokal süreklilik. -/
theorem epsDelta_implies_topoCont (M : MetricSpace α) (N : MetricSpace β)
    (f : α → β) (x₀ : α) (h : epsilonDeltaContinuous M N f x₀) :
    ∀ V : Set β, (metricTopology N).isOpen V → f x₀ ∈ V →
      ∃ U : Set α, (metricTopology M).isOpen U ∧ x₀ ∈ U ∧ U ⊆ f ⁻¹' V := by
  intro V hVo hfxV
  obtain ⟨ε, hε, hball⟩ := hVo (f x₀) hfxV
  obtain ⟨δ, hδ, hfd⟩ := h ε hε
  refine ⟨openBall M x₀ δ, openBall_isOpen M x₀ δ,
          mem_openBall.mpr (by rw [M.dist_self]; exact hδ), fun x hx => ?_⟩
  simp only [Set.mem_preimage]
  apply hball
  rw [mem_openBall]
  exact hfd x (mem_openBall.mp hx)

/-- Topolojik lokal süreklilik → ε-δ sürekliliği. -/
theorem topoCont_implies_epsDelta (M : MetricSpace α) (N : MetricSpace β)
    (f : α → β) (x₀ : α)
    (h : ∀ V : Set β, (metricTopology N).isOpen V → f x₀ ∈ V →
         ∃ U : Set α, (metricTopology M).isOpen U ∧ x₀ ∈ U ∧ U ⊆ f ⁻¹' V) :
    epsilonDeltaContinuous M N f x₀ := by
  intro ε hε
  obtain ⟨U, hUo, hx₀U, hUfV⟩ := h (openBall N (f x₀) ε)
    (openBall_isOpen N (f x₀) ε)
    (mem_openBall.mpr (by rw [N.dist_self]; exact hε))
  obtain ⟨δ, hδ, hball⟩ := hUo x₀ hx₀U
  refine ⟨δ, hδ, fun x hx => ?_⟩
  have hxU : x ∈ U := hball (mem_openBall.mpr hx)
  have hfxV := hUfV hxU
  simp only [Set.mem_preimage] at hfxV
  rwa [mem_openBall] at hfxV

-- ──────────────────────────────────────────────────────────
-- 5. Cauchy dizileri ve metrik tamlık
-- ──────────────────────────────────────────────────────────

/-- Bir dizi **Cauchy dizisidir** eğer elemanlar eninde sonunda
    birbirine keyfi yakın olursa. -/
def isCauchy (M : MetricSpace α) (seq : ℕ → α) : Prop :=
  ∀ ε > 0, ∃ N : ℕ, ∀ m n : ℕ, N ≤ m → N ≤ n → M.dist (seq m) (seq n) < ε

/-- Bir dizi `L`'ye **yakınsar** eğer elemanlar `L`'ye keyfi yakın olursa. -/
def convergesTo (M : MetricSpace α) (seq : ℕ → α) (L : α) : Prop :=
  ∀ ε > 0, ∃ N : ℕ, ∀ n : ℕ, N ≤ n → M.dist (seq n) L < ε

/-- Her yakınsak dizi bir Cauchy dizisidir. -/
theorem convergent_is_cauchy (M : MetricSpace α) (seq : ℕ → α) (L : α)
    (h : convergesTo M seq L) : isCauchy M seq := by
  intro ε hε
  obtain ⟨N, hN⟩ := h (ε / 2) (by linarith)
  refine ⟨N, fun m n hm hn => ?_⟩
  calc M.dist (seq m) (seq n)
      ≤ M.dist (seq m) L + M.dist L (seq n) := M.dist_triangle _ _ _
    _ = M.dist (seq m) L + M.dist (seq n) L := by rw [M.dist_symm (seq n) L]
    _ < ε / 2 + ε / 2                       := by linarith [hN m hm, hN n hn]
    _ = ε                                    := by linarith

/-- Bir dizinin limiti benzersizdir (T2 özelliği). -/
theorem limit_unique (M : MetricSpace α) (seq : ℕ → α) (L₁ L₂ : α)
    (h₁ : convergesTo M seq L₁) (h₂ : convergesTo M seq L₂) : L₁ = L₂ := by
  by_contra hne
  have hd : 0 < M.dist L₁ L₂ := M.dist_pos L₁ L₂ hne
  set ε := M.dist L₁ L₂ / 2 with hε_def
  obtain ⟨N₁, hN₁⟩ := h₁ ε (by linarith)
  obtain ⟨N₂, hN₂⟩ := h₂ ε (by linarith)
  set N := max N₁ N₂
  have h1 := hN₁ N (Nat.le_max_left _ _)
  have h2 := hN₂ N (Nat.le_max_right _ _)
  have htri : M.dist L₁ L₂ ≤ M.dist (seq N) L₁ + M.dist (seq N) L₂ := by
    calc M.dist L₁ L₂ ≤ M.dist L₁ (seq N) + M.dist (seq N) L₂ := M.dist_triangle _ _ _
         _ = M.dist (seq N) L₁ + M.dist (seq N) L₂ := by rw [M.dist_symm]
  linarith

/-- **Tam metrik uzay**: her Cauchy dizisi yakınsar. -/
def isComplete (M : MetricSpace α) : Prop :=
  ∀ seq : ℕ → α, isCauchy M seq → ∃ L : α, convergesTo M seq L

-- ──────────────────────────────────────────────────────────
-- 6. Banach Sabit Nokta Teoremi
-- ──────────────────────────────────────────────────────────

/-- **Büzülme dönüşümü**: `k < 1` sabitiyle mesafeyi azaltan fonksiyon. -/
def isContraction (M : MetricSpace α) (f : α → α) : Prop :=
  ∃ k : ℝ, 0 ≤ k ∧ k < 1 ∧ ∀ x y : α, M.dist (f x) (f y) ≤ k * M.dist x y

/-- Sabit nokta benzersizdir. -/
theorem fixedPoint_unique (M : MetricSpace α) (f : α → α)
    (hf : isContraction M f) (p q : α) (hp : f p = p) (hq : f q = q) : p = q := by
  obtain ⟨k, hk0, hk1, hLip⟩ := hf
  by_contra hpq
  have hdist : 0 < M.dist p q := M.dist_pos p q hpq
  have hle : M.dist p q ≤ k * M.dist p q := by
    calc M.dist p q = M.dist (f p) (f q) := by rw [hp, hq]
         _          ≤ k * M.dist p q     := hLip p q
  nlinarith

/-- **Banach Sabit Nokta Teoremi**: Tam metrik uzayda büzülme dönüşümünün
    tam olarak bir sabit noktası vardır.
    Varlık kanıtı iterasyon dizisinin Cauchy olduğunu gerektirir
    (geometrik seri yaklaşımı); burada ertelenmiştir. -/
theorem banach_fixed_point (M : MetricSpace α) (hM : isComplete M)
    (f : α → α) (hf : isContraction M f) :
    ∃! p : α, f p = p := by
  obtain ⟨k, hk0, hk1, hLip⟩ := hf
  -- Varlık: herhangi x₀'dan başlayarak xₙ₊₁ = f xₙ dizisi Cauchy'dir.
  -- Geometrik seri bağı: d(xₘ, xₙ) ≤ kⁿ/(1-k) · d(x₁,x₀) → 0
  suffices h : ∃ p : α, f p = p by
    obtain ⟨p, hp⟩ := h
    exact ⟨p, hp, fun q hq => (fixedPoint_unique M f ⟨k, hk0, hk1, hLip⟩ p q hp hq).symm⟩
  sorry

end MetricTopology
