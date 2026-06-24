"""Example: Alexander Polynomial of the Trefoil Knot

Problem:
  Compute the Alexander polynomial of the trefoil knot (3_1).

Solution:
  The trefoil is the (2, 3) torus knot, so its Alexander polynomial follows from
  pytop.torus_knot_alexander_poly, returned as a {power: coefficient} mapping.

Expected:
  Alexander(trefoil) = t - 1 + t^(-1)   i.e. {1: 1, 0: -1, -1: 1}
"""

import pytop

# Trefoil = torus knot T(2, 3).
alexander = pytop.torus_knot_alexander_poly(2, 3)

print("Trefoil Knot (3_1):")
print(f"  Alexander polynomial {{power: coeff}}: {alexander}")

# Render as a readable Laurent polynomial in t.
terms = [
    f"{coeff:+d}·t^{power}" for power, coeff in sorted(alexander.items(), reverse=True)
]
print(f"  = {' '.join(terms)}")
