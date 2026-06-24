"""Example: Size-Aware Auto Reduction Routing (method="auto")

Problem:
  Since P17.3, persistent_homology(method="auto") routes small complexes to the
  Twist reduction and large Rips complexes to the de Silva dual cohomology — a
  speed optimization. Confirm the routing is transparent: "auto" must produce
  barcodes byte-identical to the explicit "twist" method.

Solution:
  Build a small Rips filtration from a circle sample and compare the persistence
  pairs from method="auto" against method="twist".

Expected:
  Identical barcodes; the circle's one essential H_1 loop is recovered either way.
"""

import math

import pytop
from pytop import FiniteMetricSpace

# 15 points on the unit circle
points = [
    (math.cos(2 * math.pi * k / 15), math.sin(2 * math.pi * k / 15))
    for k in range(15)
]
space = FiniteMetricSpace(carrier=tuple(points), distance=math.dist)

auto = pytop.persistent_homology(space, max_dimension=1, max_scale=2.5, method="auto")
twist = pytop.persistent_homology(space, max_dimension=1, max_scale=2.5, method="twist")

print("auto == twist (byte-identical barcodes):", auto == twist)

loop = max((p for p in auto if p.dimension == 1), key=lambda p: p.persistence)
print(f"dominant H_1 loop: birth={loop.birth:.3f}, death={loop.death}, "
      f"essential={loop.is_essential}")
