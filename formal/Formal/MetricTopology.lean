import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.Archimedean.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Algebra.Field.GeomSum
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
    tam olarak bir sabit noktası vardır. -/
theorem banach_fixed_point (M : MetricSpace α) [inst : Nonempty α] (hM : isComplete M)
    (f : α → α) (hf : isContraction M f) :
    ∃! p : α, f p = p := by
  obtain ⟨k, hk0, hk1, hLip⟩ := hf
  suffices h : ∃ p : α, f p = p by
    obtain ⟨p, hp⟩ := h
    exact ⟨p, hp, fun q hq => (fixedPoint_unique M f ⟨k, hk0, hk1, hLip⟩ p q hp hq).symm⟩
  obtain ⟨x₀⟩ := inst
  -- Eğer x₀ zaten sabit noktaysa, doğrudan ver.
  by_cases hfixed : f x₀ = x₀
  · exact ⟨x₀, hfixed⟩
  have hd0 : 0 < M.dist x₀ (f x₀) := M.dist_pos x₀ (f x₀) (fun h => hfixed h.symm)
  have h1k : 0 < 1 - k := by linarith
  -- Yineleme dizisi: seqₙ = fⁿ(x₀)
  let seq : ℕ → α := fun n => f^[n] x₀
  -- Adım bağı: d(seqₙ, seqₙ₊₁) ≤ kⁿ · d₀
  have hstep : ∀ n : ℕ, M.dist (seq n) (seq (n + 1)) ≤ k ^ n * M.dist x₀ (f x₀) := by
    intro n
    induction n with
    | zero =>
      simp [seq, Function.iterate_succ_apply', Function.iterate_zero_apply]
    | succ n ih =>
      -- Rewrite seq(n+1) and seq(n+2) to their f-composition forms
      have hn1 : seq (n + 1) = f (seq n) := by
        simp [seq, Function.iterate_succ_apply']
      have hn2 : seq (n + 2) = f (seq (n + 1)) := by
        simp [seq, Function.iterate_succ_apply']
      -- Three rewrites: seq(n+1)→f(seq n), seq(n+2)→f(seq(n+1))→f(f(seq n))
      rw [hn1, hn2, hn1]
      -- Goal: M.dist (f (seq n)) (f (f (seq n))) ≤ k^(n+1) * M.dist x₀ (f x₀)
      have h1 : M.dist (f (seq n)) (f (f (seq n))) ≤ k * M.dist (seq n) (f (seq n)) :=
        hLip (seq n) (f (seq n))
      have h2 : M.dist (seq n) (f (seq n)) ≤ k ^ n * M.dist x₀ (f x₀) := hn1 ▸ ih
      nlinarith [mul_nonneg hk0 (pow_nonneg hk0 n), pow_succ k n]
  -- Kısmi toplam bağı: d(seqₘ, seqₘ₊ₚ) ≤ (∑ᵢ<ₚ k^(m+i)) · d₀
  have hpsum : ∀ m p : ℕ,
      M.dist (seq m) (seq (m + p)) ≤
        (Finset.range p).sum (fun i => k ^ (m + i)) * M.dist x₀ (f x₀) := by
    intro m p
    induction p with
    | zero => simp [seq, M.dist_self]
    | succ p ihp =>
      rw [show m + (p + 1) = m + p + 1 from by omega, Finset.sum_range_succ]
      calc M.dist (seq m) (seq (m + p + 1))
          ≤ M.dist (seq m) (seq (m + p)) + M.dist (seq (m + p)) (seq (m + p + 1))
              := M.dist_triangle _ _ _
        _ ≤ (Finset.range p).sum (fun i => k ^ (m + i)) * M.dist x₀ (f x₀) +
              k ^ (m + p) * M.dist x₀ (f x₀) := by linarith [ihp, hstep (m + p)]
        _ = ((Finset.range p).sum (fun i => k ^ (m + i)) + k ^ (m + p)) * M.dist x₀ (f x₀)
              := by ring
  -- Geometrik seri bağı: ∑ᵢ<ₚ k^(m+i) ≤ kᵐ / (1−k)
  have hgeom : ∀ m p : ℕ,
      (Finset.range p).sum (fun i => k ^ (m + i)) ≤ k ^ m / (1 - k) := by
    intro m p
    have hfact : (Finset.range p).sum (fun i => k ^ (m + i)) =
        k ^ m * (Finset.range p).sum (fun i => k ^ i) := by
      simp [Finset.mul_sum, pow_add]
    rw [hfact]
    clear hfact
    -- Kapalı form: (∑ᵢ<ₚ kⁱ) · (1−k) = 1 − kᵖ  (induction)
    have hform : (Finset.range p).sum (fun i => k ^ i) * (1 - k) = 1 - k ^ p := by
      induction p with
      | zero => simp
      | succ p ih => rw [Finset.sum_range_succ, add_mul, ih]; ring
    have hkp : 0 ≤ k ^ p := pow_nonneg hk0 p
    have hkm : 0 ≤ k ^ m := pow_nonneg hk0 m
    -- ∑ᵢ<ₚ kⁱ ≤ 1/(1−k)  iff  ∑ᵢ<ₚ kⁱ · (1−k) ≤ 1
    have hle : (Finset.range p).sum (fun i => k ^ i) ≤ 1 / (1 - k) := by
      rw [le_div_iff₀ h1k]; linarith [hform]
    calc k ^ m * (Finset.range p).sum (fun i => k ^ i)
        ≤ k ^ m * (1 / (1 - k)) := mul_le_mul_of_nonneg_left hle hkm
      _ = k ^ m / (1 - k) := by ring
  -- Mesafe bağı: d(seqₘ, seqₘ₊ₚ) ≤ kᵐ/(1−k) · d₀
  have hdist : ∀ m p : ℕ,
      M.dist (seq m) (seq (m + p)) ≤ k ^ m / (1 - k) * M.dist x₀ (f x₀) :=
    fun m p => (hpsum m p).trans (mul_le_mul_of_nonneg_right (hgeom m p) (le_of_lt hd0))
  -- seq Cauchy dizisidir
  have hcauchy : isCauchy M seq := by
    intro ε hε
    set c := ε * (1 - k) / M.dist x₀ (f x₀) with hc_def
    have hc : 0 < c := div_pos (mul_pos hε h1k) hd0
    obtain ⟨N, hN⟩ := exists_pow_lt_of_lt_one hc hk1
    -- N'den büyük her j için tek taraflı bağ
    have hbound : ∀ j, N ≤ j → ∀ p, M.dist (seq j) (seq (j + p)) < ε := by
      intro j hj p
      have hpow : k ^ j ≤ k ^ N :=
        pow_le_pow_of_le_one hk0 (le_of_lt hk1) hj
      have hstep2 : k ^ N * M.dist x₀ (f x₀) < ε * (1 - k) := by
        have hcv : c * M.dist x₀ (f x₀) = ε * (1 - k) := by
          rw [hc_def, div_mul_cancel₀]
          exact ne_of_gt hd0
        calc k ^ N * M.dist x₀ (f x₀)
            < c * M.dist x₀ (f x₀) := mul_lt_mul_of_pos_right hN hd0
          _ = ε * (1 - k) := hcv
      calc M.dist (seq j) (seq (j + p))
          ≤ k ^ j / (1 - k) * M.dist x₀ (f x₀) := hdist j p
        _ ≤ k ^ N / (1 - k) * M.dist x₀ (f x₀) := by
              apply mul_le_mul_of_nonneg_right _ (le_of_lt hd0)
              exact (div_le_div_iff_of_pos_right h1k).mpr hpow
        _ < ε := by
              rw [show k ^ N / (1 - k) * M.dist x₀ (f x₀) =
                    k ^ N * M.dist x₀ (f x₀) / (1 - k) from by ring,
                  div_lt_iff₀ h1k]
              linarith
    refine ⟨N, fun m n hm hn => ?_⟩
    rcases lt_or_ge n m with hmn | hmn
    · -- n < m
      rw [M.dist_symm, show m = n + (m - n) from (Nat.add_sub_cancel' hmn.le).symm]
      exact hbound n hn _
    · -- m ≤ n
      rw [show n = m + (n - m) from (Nat.add_sub_cancel' hmn).symm]
      exact hbound m hm _
  -- Limiti al
  obtain ⟨L, hL⟩ := hM seq hcauchy
  -- f(seqₙ) = seqₙ₊₁
  have hfseq : ∀ n, f (seq n) = seq (n + 1) := fun n => by
    simp [seq, Function.iterate_succ_apply']
  -- seqₙ₊₁ → L
  have hL1 : convergesTo M (fun n => seq (n + 1)) L := by
    intro ε hε
    obtain ⟨N, hN⟩ := hL ε hε
    exact ⟨N, fun n hn => hN (n + 1) (Nat.le_succ_of_le hn)⟩
  -- f(seqₙ) → f(L)
  have hfL : convergesTo M (fun n => seq (n + 1)) (f L) := by
    intro ε hε
    by_cases hk0' : k = 0
    · obtain ⟨N, hN⟩ := hL ε hε
      refine ⟨N, fun n hn => ?_⟩
      -- beta-reduce then rewrite seq(n+1) = f(seq n)
      change M.dist (seq (n + 1)) (f L) < ε
      rw [← hfseq n]
      have h0 := hLip (seq n) L
      rw [hk0', zero_mul] at h0
      linarith [M.dist_nonneg (f (seq n)) (f L)]
    · have hkpos : 0 < k := lt_of_le_of_ne hk0 (Ne.symm hk0')
      obtain ⟨N, hN⟩ := hL (ε / k) (div_pos hε hkpos)
      refine ⟨N, fun n hn => ?_⟩
      change M.dist (seq (n + 1)) (f L) < ε
      rw [← hfseq n]
      calc M.dist (f (seq n)) (f L)
          ≤ k * M.dist (seq n) L := hLip _ _
        _ < k * (ε / k) := by nlinarith [hN n hn, M.dist_nonneg (seq n) L]
        _ = ε := by field_simp [hkpos.ne']
  -- Limit özgünlüğünden f(L) = L
  exact ⟨L, limit_unique M _ (f L) L hfL hL1⟩

end MetricTopology
