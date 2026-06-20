import Formal.Homology
import Mathlib.Data.List.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Yol 2: Euler Karakteristiği

**Euler–Poincaré teoremi**: sonlu bir zincir kompleksinde Euler karakteristiği
hem zincir grup rankları hem de Betti sayıları üzerinden aynı değeri verir.

```
χ = Σ_k (-1)^k rank(C_k) = Σ_k (-1)^k β_k
```

## Kanıt stratejisi

`alternatingSum (c₀ :: c₁ :: ...)  =  c₀ - c₁ + c₂ - ...` tanımlanır.
`c_k = β_k + r_k + r_{k+1}` varsayımıyla toplamlar telescopes: iki ardışık
`r_k` terimi birbirini götürür; sınır koşulları `r_0 = r_{N+1} = 0` sayesinde
sınır terimleri de kaybolur.
-/

namespace EulerChar

-- ──────────────────────────────────────────────────────────
-- 1. Dönüşümlü toplam
-- ──────────────────────────────────────────────────────────

/-- **Dönüşümlü toplam**: `a₀ - a₁ + a₂ - ⋯` -/
def alternatingSum : List Int → Int
  | []           => 0
  | x :: rest    => x - alternatingSum rest

@[simp] theorem alternatingSum_nil  : alternatingSum [] = 0 := rfl
@[simp] theorem alternatingSum_singleton (x : Int) : alternatingSum [x] = x := by
  simp [alternatingSum]
@[simp] theorem alternatingSum_cons (x : Int) (rest : List Int) :
    alternatingSum (x :: rest) = x - alternatingSum rest := rfl

-- ──────────────────────────────────────────────────────────
-- 2. Somut örnekler (sorry yok)
-- ──────────────────────────────────────────────────────────

/-- Nokta: β₀ = 1, χ = 1. -/
example : alternatingSum [1] = 1 := by simp

/-- Kapalı aralık: 2 köşe, 1 kenar → χ = 2 − 1 = 1. -/
example : alternatingSum [2, 1] = 1 := by simp [alternatingSum]

/-- Çember S¹ (minimal CW): 1 köşe + 1 kenar → χ = 0. -/
example : alternatingSum [1, 1] = 0 := by simp [alternatingSum]

/-- Torus T² (minimal CW): 1 köşe + 2 kenar + 1 yüzey → χ = 0. -/
example : alternatingSum [1, 2, 1] = 0 := by simp [alternatingSum]

/-- RP² (minimal CW): 1 köşe + 1 kenar + 1 yüzey → χ = 1. -/
example : alternatingSum [1, 1, 1] = 1 := by simp [alternatingSum]

/-- Klein şişesi: 1 köşe + 2 kenar + 1 yüzey → χ = 0. -/
example : alternatingSum [1, 2, 1] = 0 := by simp [alternatingSum]

-- ──────────────────────────────────────────────────────────
-- 3. Teleskop lemması (somut, ispat edilmiş)
-- ──────────────────────────────────────────────────────────

/-- 3 boyutlu özel teleskop: `(β₀+r₁) − (β₁+r₁+r₂) + (β₂+r₂) = β₀ − β₁ + β₂`. -/
lemma telescope_3 (β₀ β₁ β₂ r₁ r₂ : Int) :
    alternatingSum [β₀ + r₁, β₁ + r₁ + r₂, β₂ + r₂] =
    alternatingSum [β₀, β₁, β₂] := by
  simp only [alternatingSum_cons, alternatingSum_singleton, alternatingSum_nil]; ring

/-- 2 boyutlu özel teleskop: `(β₀+r₁) − (β₁+r₁) = β₀ − β₁`. -/
lemma telescope_2 (β₀ β₁ r₁ : Int) :
    alternatingSum [β₀ + r₁, β₁ + r₁] = alternatingSum [β₀, β₁] := by
  simp only [alternatingSum_cons, alternatingSum_singleton, alternatingSum_nil]; ring

/-- 4 boyutlu teleskop. -/
lemma telescope_4 (β₀ β₁ β₂ β₃ r₁ r₂ r₃ : Int) :
    alternatingSum [β₀ + r₁, β₁ + r₁ + r₂, β₂ + r₂ + r₃, β₃ + r₃] =
    alternatingSum [β₀, β₁, β₂, β₃] := by
  simp only [alternatingSum_cons, alternatingSum_singleton, alternatingSum_nil]; ring

-- ──────────────────────────────────────────────────────────
-- 4. Genel Euler–Poincaré teoremi
-- ──────────────────────────────────────────────────────────

-- Helper: alternatingSum cs - alternatingSum bs = rs[0] - (-1)^n * rs[n]
-- Σ_k (-1)^k (c_k - β_k) = Σ_k (-1)^k (r_k + r_{k+1}) telescopes to r_0 + (-1)^{n-1} r_n
private lemma euler_telescope (cs bs rs : List Int)
    (hcb : cs.length = bs.length)
    (hri : rs.length = cs.length + 1)
    (hrel : ∀ k < cs.length, cs.getD k 0 = bs.getD k 0 + rs.getD k 0 + rs.getD (k+1) 0) :
    alternatingSum cs - alternatingSum bs =
      rs.getD 0 0 - (-1 : Int)^cs.length * rs.getD cs.length 0 := by
  induction cs generalizing bs rs with
  | nil =>
    rcases bs with _ | ⟨b, bs'⟩
    · simp [alternatingSum]
    · simp at hcb
  | cons c cs' ih =>
    rcases bs with _ | ⟨β, bs'⟩
    · simp at hcb
    rcases rs with _ | ⟨r₀, rs'⟩
    · simp at hri
    simp only [List.length_cons] at hcb hri
    have hcb' : cs'.length = bs'.length := by omega
    have hri' : rs'.length = cs'.length + 1 := by omega
    have hrel0 : c = β + r₀ + rs'.getD 0 0 := by
      have h := hrel 0 (Nat.zero_lt_succ _)
      simp only [List.getD_cons_zero, List.getD_cons_succ] at h
      exact h
    have hrel' : ∀ k < cs'.length,
        cs'.getD k 0 = bs'.getD k 0 + rs'.getD k 0 + rs'.getD (k+1) 0 := by
      intro k hk
      have h := hrel (k + 1) (by simp only [List.length_cons]; omega)
      simp only [List.getD_cons_succ] at h
      exact h
    have ihh := ih bs' rs' hcb' hri' hrel'
    have hsign : (-1 : Int)^(cs'.length + 1) * rs'.getD cs'.length 0 =
                 -((-1 : Int)^cs'.length * rs'.getD cs'.length 0) := by
      rw [pow_succ, mul_neg_one, neg_mul]
    simp only [alternatingSum_cons, List.length_cons, List.getD_cons_zero, List.getD_cons_succ]
    linarith

/-- **Euler–Poincaré teoremi** (genel): boundary image rankları teleskope eder.

Hipotezler:
* `h_len_cb`   : zincir rankları ve Betti sayıları aynı uzunlukta.
* `h_len_ri`   : image rankları bir fazla (r₀ ve r_{N+1} dahil).
* `h_boundary` : `r_0 = 0` ve `r_{N+1} = 0` (sınır koşulları).
* `h_rel`      : `c_k = β_k + r_k + r_{k+1}` her `k` için.
-/
theorem euler_poincare
    (chainRanks bettiNums imageRanks : List Int)
    (h_len_cb : chainRanks.length = bettiNums.length)
    (h_len_ri : imageRanks.length = chainRanks.length + 1)
    (h_boundary : imageRanks.getD 0 0 = 0 ∧ imageRanks.getD chainRanks.length 0 = 0)
    (h_rel : ∀ k, k < chainRanks.length →
      chainRanks.getD k 0 =
      bettiNums.getD k 0 + imageRanks.getD k 0 + imageRanks.getD (k + 1) 0) :
    alternatingSum chainRanks = alternatingSum bettiNums := by
  have h := euler_telescope chainRanks bettiNums imageRanks h_len_cb h_len_ri h_rel
  simp only [h_boundary.1, h_boundary.2, mul_zero, sub_zero] at h
  linarith

end EulerChar
