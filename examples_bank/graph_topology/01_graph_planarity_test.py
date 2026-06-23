"""Example: Graph Planarity Testing

Problem:
  Determine if K5 and K33 are planar (they should not be).

Solution:
  Use pytop.is_planar() for O(V+E) Brandes planarity test.
"""

import pytop

# K5: Complete graph on 5 vertices
k5_edges = [(i, j) for i in range(5) for j in range(i+1, 5)]
k5 = pytop.Graph(vertices=set(range(5)), edges=k5_edges)

# K33: Complete bipartite
k33_edges = [(i, j) for i in range(3) for j in range(3, 6)]
k33 = pytop.Graph(vertices=set(range(6)), edges=k33_edges)

print("Planarity Testing:")
print(f"  K5 planar: {pytop.is_planar(k5)}")
print(f"  K33 planar: {pytop.is_planar(k33)}")
