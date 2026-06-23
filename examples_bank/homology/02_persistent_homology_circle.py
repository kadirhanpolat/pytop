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
h0_count = len([p for p in pairs if p[0] == 0])
h1_count = len([p for p in pairs if p[0] == 1])
print(f"  H_0 bars: {h0_count}")
print(f"  H_1 bars: {h1_count}")
