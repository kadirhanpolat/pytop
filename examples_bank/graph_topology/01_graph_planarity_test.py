"""Example: Graph Planarity Testing

Problem:
  Decide whether K5 and K3,3 are planar (the two Kuratowski obstructions — they
  are not), and confirm a simple cycle is.

Solution:
  pytop.is_planar takes an edge list (tuples of vertices) and runs the linear-time
  left-right planarity test, so it never raises on large graphs.

Expected:
  cycle planar = True
  K5   planar  = False
  K3,3 planar  = False
"""

import pytop

cycle = [(0, 1), (1, 2), (2, 3), (3, 0)]
k5_edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
k33_edges = [(i, j) for i in range(3) for j in range(3, 6)]

print("Planarity Testing:")
print(f"  4-cycle planar: {pytop.is_planar(cycle)}")
print(f"  K5 planar:      {pytop.is_planar(k5_edges)}")
print(f"  K3,3 planar:    {pytop.is_planar(k33_edges)}")
