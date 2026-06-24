"""Example: Homology of the Klein Bottle

Problem:
  Compute the homology of the Klein bottle K, including its torsion.

Solution:
  pytop.klein_bottle_filtration provides a minimal triangulation. Turn its
  simplices into a SimplicialComplex and compute homology degree by degree —
  simplicial_homology reports both Betti numbers and torsion coefficients.

Expected:
  H_0(K) = Z            (connected)
  H_1(K) = Z (+) Z/2    (one free generator + 2-torsion)
  H_2(K) = 0            (non-orientable)
"""

import pytop

# Minimal triangulation of the Klein bottle, as a face-closed complex.
filtration = pytop.klein_bottle_filtration()
K = pytop.SimplicialComplex(filtration.simplices)

print("Klein Bottle:")
for degree in range(3):
    H = pytop.simplicial_homology(K, degree)
    line = f"  H_{degree}(K) = Z^{H.betti}"
    if H.torsion:
        line += " (+) " + " (+) ".join(f"Z/{t}" for t in H.torsion)
    print(line)
