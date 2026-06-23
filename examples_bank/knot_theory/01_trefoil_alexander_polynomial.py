"""Example: Alexander Polynomial of Trefoil Knot

Problem:
  Compute the Alexander polynomial of the trefoil knot.

Solution:
  Use pytop.alexander_polynomial() to compute the invariant.

Expected:
  Alexander(trefoil) = t - 1 + t^(-1)
"""

import pytop

knot = pytop.Knot.trefoil()
alex_poly = pytop.alexander_polynomial(knot)

print("Trefoil Knot (3_1):")
print(f"  Alexander polynomial: {alex_poly}")
print(f"  Is palindromic: {alex_poly == alex_poly.reverse()}")
