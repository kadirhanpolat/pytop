"""Example: Persistent Homology of a Circle

Problem:
  Construct a Vietoris-Rips filtration on points sampled from a circle
  and compute persistent homology.

Solution:
  Use pytop.vietoris_rips_filtration and pytop.persistent_homology to
  track H_0 and H_1 barcodes as filtration parameter grows.
"""

import pytop

# Sample points on a unit circle
points = [
    (1.0, 0.0), (0.71, 0.71), (0.0, 1.0), (-0.71, 0.71),
    (-1.0, 0.0), (-0.71, -0.71), (0.0, -1.0), (0.71, -0.71)
]

# Build Rips filtration
filtration = pytop.vietoris_rips_filtration(points, max_radius=2.5)

# Compute persistent homology
pairs = pytop.persistent_homology(filtration)

print("Circle (8 points) - Persistent Homology:")
for dim, (birth, death) in pairs:
    print(f"  dim {dim}: ({birth:.3f}, {death:.3f})")

# H_1 should have a long bar (circle persistence)
h1_bars = [(b, d) for d, (b, d) in pairs if d == 1]
if h1_bars:
    print(f"
Longest H_1 bar: {h1_bars[0]}")
