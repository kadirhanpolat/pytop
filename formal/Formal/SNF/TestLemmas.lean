import Mathlib.Data.List.Basic

example (l : List Nat) (i : Nat) (h : i < l.length) : l[i]? = some l[i] := by
  exact?

example (l : List Nat) (i : Nat) : l.getD i 0 = l[i]?.getD 0 := by
  simp [List.getD]

example (l : List Nat) (i : Nat) (h : l.length ≤ i) : l[i]? = none := by
  exact?
