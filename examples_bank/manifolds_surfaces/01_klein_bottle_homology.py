"""Example: Homology of Klein Bottle

Problem:
  Compute homology of the Klein bottle K.

Expected:
  H_0(K) = Z        (connected)
  H_1(K) = Z ⊕ Z/2  (one generator + torsion)
  H_2(K) = 0        (non-orientable)
"""

import pytop

filtration = pytop.klein_bottle_filtration()
H = pytop.homology(filtration)

print("Klein Bottle:")
for dim in range(len(H.betti_numbers)):
    betti = H.betti_numbers[dim]
    torsion = H.torsion_coefficients[dim] if dim < len(H.torsion_coefficients) else []
    print(f"  H_{dim} = Z^{betti}", end="")
    if torsion:
        print(f" ⊕ {torsion}")
    else:
        print()

print(f"  Euler characteristic: {H.euler_characteristic}")
