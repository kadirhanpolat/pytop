"""Example: Homology of a 2-Sphere (S²)

Problem:
  Compute the homology groups H_0(S²), H_1(S²), H_2(S²) using the standard
  triangulation of the 2-sphere (tetrahedron).

Solution:
  Use pytop's simplicial_complex and homology modules to build S² as the
  boundary of a tetrahedron and compute its homology.

Expected:
  H_0(S²) = Z        (connected)
  H_1(S²) = 0        (simply connected)
  H_2(S²) = Z        (2-dimensional void)
"""

import pytop

# Build S² as boundary of tetrahedron: 4 vertices, 6 edges, 4 triangles
vertices = frozenset(range(4))

edges = frozenset([
    frozenset([0, 1]),
    frozenset([0, 2]),
    frozenset([0, 3]),
    frozenset([1, 2]),
    frozenset([1, 3]),
    frozenset([2, 3]),
])

triangles = frozenset([
    frozenset([0, 1, 2]),
    frozenset([0, 1, 3]),
    frozenset([0, 2, 3]),
    frozenset([1, 2, 3]),
])

simplex_list = list(vertices) + list(edges) + list(triangles)
S2 = pytop.SimplicialComplex(simplex_list)

# Compute homology
H = pytop.homology(S2)

print("S² Homology:")
for dim, (betti, torsion) in enumerate(zip(H.betti_numbers, H.torsion_coefficients)):
    print(f"  H_{dim}(S²) = Z^{betti}", end="")
    if torsion:
        print(f" ⊕ {torsion}")
    else:
        print()

print("\nVerification:")
print(f"  χ(S²) = {H.euler_characteristic} (expected: 2)")
