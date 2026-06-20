import Formal.SNF.Defs
import Formal.SNF.Algorithm
import Formal.SNF.Positivity
import Formal.SNF.Correctness
import Mathlib.Data.List.Basic

/-!
# Yol 1: Homolojisel Ranklar

`pytopSNF` çıktısından **rank**, **nullity**, **Betti sayısı** ve **torsion
katsayıları** tanımlar.  Bütün teoremler sorry olmadan ispat edilmiştir.

## Ana sonuçlar

* `matRank_le_min`   : rank ≤ min(satır, sütun)
* `rank_nullity`     : rank + nullity = numCols
* `torsionFactors_gt_one` : torsion katsayıları > 1
-/

namespace PytopHomology

open PytopSNF

-- ──────────────────────────────────────────────────────────
-- 1. Tanımlar
-- ──────────────────────────────────────────────────────────

/-- Matrisin **rankı**: `pytopSNF` çıktısının uzunluğu. -/
def matRank (A : IntMatrix) : Nat := (pytopSNF A).length

/-- **Kernel boyutu** (nullity). -/
def nullity (A : IntMatrix) : Nat := numCols A - matRank A

/-- **Torsion katsayıları**: 1'den büyük değişmez çarpanlar. -/
def torsionFactors (A : IntMatrix) : List Int :=
  (pytopSNF A).filter (fun d => decide (1 < d))

/-- **n. Betti sayısı**: β_n = nullity(∂_n) − rank(∂_{n+1}). -/
def bettiNumber (dn dn1 : IntMatrix) : Nat :=
  nullity dn - matRank dn1

-- ──────────────────────────────────────────────────────────
-- 2. Rank sınırı
-- ──────────────────────────────────────────────────────────

/-- `pytopSNFWithFuel.go` en fazla `n + acc.length` sonuç üretir. -/
private lemma go_length_le (innerFuel : Nat) :
    ∀ (n : Nat) (M : IntMatrix) (t : Nat) (acc : List Int),
    (pytopSNFWithFuel.go innerFuel n M t acc).length ≤ n + acc.length := by
  intro n
  induction n with
  | zero =>
    intros M t acc
    simp only [pytopSNFWithFuel.go, List.length_reverse]
    omega
  | succ k ih =>
    intros M t acc
    simp only [pytopSNFWithFuel.go]
    split_ifs
    · simp only [List.length_reverse]; omega
    · rcases snfOuterStep M t innerFuel with ⟨M', dOpt⟩
      rcases dOpt with _ | d'
      · simp only [List.length_reverse]; omega
      · show (pytopSNFWithFuel.go innerFuel k M' (t + 1) (d' :: acc)).length ≤ k + 1 + acc.length
        have h := ih M' (t + 1) (d' :: acc)
        simp only [List.length_cons] at h
        omega

/-- Rank ≤ min(satır sayısı, sütun sayısı). -/
theorem matRank_le_min (A : IntMatrix) :
    matRank A ≤ min (numRows A) (numCols A) := by
  unfold matRank pytopSNF pytopSNFWithFuel
  have h := go_length_le (numRows A * numCols A * (sumAbs A + 1))
              (min (numRows A) (numCols A)) A 0 []
  simpa using h

/-- Rank ≤ sütun sayısı. -/
theorem matRank_le_numCols (A : IntMatrix) : matRank A ≤ numCols A :=
  (matRank_le_min A).trans (Nat.min_le_right _ _)

/-- Rank ≤ satır sayısı. -/
theorem matRank_le_numRows (A : IntMatrix) : matRank A ≤ numRows A :=
  (matRank_le_min A).trans (Nat.min_le_left _ _)

-- ──────────────────────────────────────────────────────────
-- 3. Rank–Nullity Teoremi
-- ──────────────────────────────────────────────────────────

/-- **Rank–Nullity**: rank + nullity = numCols. -/
theorem rank_nullity (A : IntMatrix) :
    matRank A + nullity A = numCols A :=
  Nat.add_sub_cancel' (matRank_le_numCols A)

-- ──────────────────────────────────────────────────────────
-- 4. Torsion katsayılar
-- ──────────────────────────────────────────────────────────

/-- Torsion katsayılar pozitiftir. -/
theorem torsionFactors_pos (A : IntMatrix) :
    ∀ d ∈ torsionFactors A, 0 < d := by
  intro d hd
  simp only [torsionFactors, List.mem_filter] at hd
  exact (pytopSNF_isInvariantFactors A).positive d hd.1

/-- Torsion katsayılar 1'den büyüktür. -/
theorem torsionFactors_gt_one (A : IntMatrix) :
    ∀ d ∈ torsionFactors A, 1 < d := by
  intro d hd
  simp only [torsionFactors, List.mem_filter] at hd
  exact of_decide_eq_true hd.2

/-- Torsion katsayı sayısı ≤ rank. -/
theorem torsionFactors_length_le (A : IntMatrix) :
    (torsionFactors A).length ≤ matRank A := by
  unfold torsionFactors matRank
  induction pytopSNF A with
  | nil => simp
  | cons d ds ih =>
    simp only [List.filter_cons]
    split_ifs
    · simp only [List.length_cons]; omega
    · exact ih.trans (Nat.le_succ _)

-- ──────────────────────────────────────────────────────────
-- 5. Betti sayısı
-- ──────────────────────────────────────────────────────────

/-- Betti sayısı genişlemesi: `nullity - rank(∂_{n+1})`. -/
theorem bettiNumber_unfold (dn dn1 : IntMatrix) :
    bettiNumber dn dn1 = numCols dn - matRank dn - matRank dn1 := by
  simp only [bettiNumber, nullity]

/-- Betti sayısı ≤ nullity(∂_n). -/
theorem bettiNumber_le_nullity (dn dn1 : IntMatrix) :
    bettiNumber dn dn1 ≤ nullity dn :=
  Nat.sub_le _ _

/-- Betti sayısı ≤ sütun sayısı. -/
theorem bettiNumber_le_numCols (dn dn1 : IntMatrix) :
    bettiNumber dn dn1 ≤ numCols dn := by
  unfold bettiNumber nullity; omega

/-- `bettiNumber + rank(∂_{n+1}) ≤ nullity + rank(∂_{n+1})` (rank-nullity). -/
theorem bettiNumber_add_rank_le (dn dn1 : IntMatrix) :
    bettiNumber dn dn1 + matRank dn1 ≤ nullity dn + matRank dn1 :=
  Nat.add_le_add_right (Nat.sub_le _ _) _

end PytopHomology
