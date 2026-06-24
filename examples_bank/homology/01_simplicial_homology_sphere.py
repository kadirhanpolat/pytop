"""Example: Homology of a 2-Sphere (S²)

Problem:
  Compute the homology groups H_0(S²), H_1(S²), H_2(S²) using the standard
  triangulation of the 2-sphere (boundary of a tetrahedron).

Solution:
  Build S² as a face-closed SimplicialComplex (simplices given as tuples) and
  compute homology one degree at a time with pytop.simplicial_homology.

Expected:
  H_0(S²) = Z   (connected)
  H_1(S²) = 0   (simply connected)
  H_2(S²) = Z   (one enclosed 2-dimensional void)
"""

import pytop

# S² as the boundary of a tetrahedron: 4 vertices, 6 edges, 4 triangles.
# Simplices are iterables of vertices; the complex must be face-closed.
vertices = [(0,), (1,), (2,), (3,)]
edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
triangles = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]

S2 = pytop.SimplicialComplex(vertices + edges + triangles)

print("S² Homology:")
for degree in range(3):
    H = pytop.simplicial_homology(S2, degree)
    line = f"  H_{degree}(S²) = Z^{H.betti}"
    if H.torsion:
        line += f" (+) {H.torsion}"
    print(line)
