"""Example: Persistent Homology of a Circle

Problem:
  Sample points from a circle and recover its loop with persistent homology.

Solution:
  Wrap the points in a FiniteMetricSpace and call pytop.persistent_homology to
  build a Vietoris-Rips filtration and track H_0/H_1 features across scales.

Expected:
  A single long-lived (essential) H_1 bar — the circle's loop — alongside many
  short-lived bars that are sampling noise.
"""

import math

import pytop
from pytop import FiniteMetricSpace

# 12 points evenly spaced on the unit circle.
points = [
    (math.cos(2 * math.pi * k / 12), math.sin(2 * math.pi * k / 12))
    for k in range(12)
]

# Finite metric space with Euclidean distance.
space = FiniteMetricSpace(carrier=tuple(points), distance=math.dist)

# Vietoris-Rips persistence up to dimension 1, scale 2.5.
pairs = pytop.persistent_homology(space, max_dimension=1, max_scale=2.5)

h1 = [p for p in pairs if p.dimension == 1]
loop = max(h1, key=lambda p: p.persistence)

print("Circle (12 points) - Persistent Homology:")
print(f"  total H_1 bars: {len(h1)} (most are short-lived sampling noise)")
print(
    f"  dominant loop: birth={loop.birth:.3f}, death={loop.death}, "
    f"essential={loop.is_essential}"
)
