"""Example: Complete TDA Pipeline on a Rips Complex

Problem:
  Apply the full TDA pipeline (Rips filtration -> reduction -> barcode) to a
  random 2D dataset.

Solution:
  pytop.TDAPipeline is an immutable fluent builder. Feed points to .rips(),
  choose a reduction with .reduce(), then read off barcodes per dimension.

Expected:
  H_0 has one bar per connected component (30 points -> 30 H_0 bars);
  H_1 collects loop features (mostly short-lived noise at this scale).
"""

import random

import pytop

random.seed(42)
points = [(random.random(), random.random()) for _ in range(30)]

pipeline = (
    pytop.TDAPipeline()
    .rips(points, max_dimension=1, max_scale=0.5)
    .reduce(method="twist")
)

print("TDA Pipeline Result:")
print(f"  H_0 bars: {len(pipeline.barcode(dimension=0))}")
print(f"  H_1 bars: {len(pipeline.barcode(dimension=1))}")
print(f"  Betti numbers: {pytop.persistence_betti_numbers(pipeline.pairs())}")
