import Formal.SNF.Defs
import Formal.SNF.Elementary
import Mathlib.Data.Int.GCD

/-!
# SNF Algorithm

A fuel-based Lean 4 transcription of `_smith_normal_form_python`.
-/

namespace PytopSNF

-- ---------------------------------------------------------------------------
-- Helpers
-- ---------------------------------------------------------------------------

/-- Sum of absolute values of all matrix entries. -/
def sumAbs (A : IntMatrix) : Nat :=
  A.foldl (fun acc row => acc + row.foldl (fun a x => a + x.natAbs) 0) 0

/-- Find smallest-magnitude nonzero entry in A[t:, t:]; returns its position. -/
def findPivot (A : IntMatrix) (t : Nat) : Option (Nat × Nat) :=
  let m := numRows A; let n := numCols A
  ((List.range (m - t)).foldl fun acc i =>
    (List.range (n - t)).foldl (fun acc' j =>
      let x := entry A (i + t) (j + t)
      if x = 0 then acc'
      else match acc' with
        | none => some ((i + t, j + t), x.natAbs)
        | some (_, b) => if x.natAbs < b then some ((i + t, j + t), x.natAbs) else acc')
      acc)
    none
  |>.map (·.1)

/-- One clearing pass: zero out column t and row t using addRow/addCol. -/
def clearPass (A : IntMatrix) (t : Nat) : IntMatrix :=
  let m := numRows A
  let n := numCols A
  let pivot := entry A t t
  if pivot = 0 then A
  else
    let A₁ := (List.range m).foldl (fun M i =>
      if i = t then M
      else addRow M t i (-(entry M i t / entry M t t))) A
    (List.range n).foldl (fun M j =>
      if j = t then M
      else addCol M t j (-(entry M t j / entry M t t))) A₁

/-- True if every off-diagonal entry in row t and col t is zero. -/
def isCleared (A : IntMatrix) (t : Nat) : Bool :=
  let m := numRows A
  let n := numCols A
  (List.range m).all (fun i => i = t || entry A i t = 0) &&
  (List.range n).all (fun j => j = t || entry A t j = 0)

/-- Repeat clearPass until isCleared (bounded by fuel). -/
def clearLoop : IntMatrix → Nat → Nat → IntMatrix
  | A, _,       0        => A
  | A, t, fuel + 1 => if isCleared A t then A else clearLoop (clearPass A t) t fuel

/-- True if entry (t,t) divides every entry in A[t+1:, t+1:]. -/
def pivotDividesAll (A : IntMatrix) (t : Nat) : Bool :=
  let pivot := entry A t t
  if pivot = 0 then true
  else (submatrix A (t + 1)).all (fun row => row.all (fun x => x % pivot = 0))

/-- Force divisibility: add a "bad" row to row t to trigger GCD descent. -/
def enforceDivisibility (A : IntMatrix) (t : Nat) : IntMatrix :=
  let pivot := entry A t t
  if pivot = 0 then A
  else
    let m := numRows A; let n := numCols A
    let bad := (List.range m).findSome? fun i =>
      if i ≤ t then none
      else (List.range n).findSome? fun j =>
        if j ≤ t then none
        else if entry A i j % pivot ≠ 0 then some (i, j) else none
    match bad with
    | none      => A
    | some (i, _) => addRow A i t 1

-- ---------------------------------------------------------------------------
-- Outer step
-- ---------------------------------------------------------------------------

/-- Perform one SNF step at diagonal position `t`. -/
def snfOuterStep (A : IntMatrix) (t innerFuel : Nat) : IntMatrix × Option Int :=
  match findPivot A t with
  | none => (A, none)
  | some (pi, pj) =>
    let A₁ := swapRows A pi t
    let A₂ := swapCols A₁ pj t
    let A₃ := clearLoop A₂ t innerFuel
    if pivotDividesAll A₃ t then
      (A₃, some (entry A₃ t t).natAbs)
    else
      let A₄ := enforceDivisibility A₃ t
      let A₅ := clearLoop A₄ t innerFuel
      (A₅, if pivotDividesAll A₅ t then some (entry A₅ t t).natAbs else none)

-- ---------------------------------------------------------------------------
-- Main algorithm
-- ---------------------------------------------------------------------------

/-- SNF algorithm with explicit fuel. -/
def pytopSNFWithFuel (outerFuel innerFuel : Nat) (A : IntMatrix) : List Int :=
  go outerFuel A 0 []
where
  go : Nat → IntMatrix → Nat → List Int → List Int
    | 0,     _, _,  acc => acc.reverse
    | n + 1, M, t,  acc =>
      if t ≥ min (numRows M) (numCols M) then acc.reverse
      else
        let (M', dOpt) := snfOuterStep M t innerFuel
        match dOpt with
        | none   => acc.reverse
        | some d => go n M' (t + 1) (d :: acc)

/-- The invariant factors of `A` (sufficient fuel derived from matrix size). -/
def pytopSNF (A : IntMatrix) : List Int :=
  let m := numRows A; let n := numCols A
  pytopSNFWithFuel (min m n) (m * n * (sumAbs A + 1)) A

end PytopSNF
