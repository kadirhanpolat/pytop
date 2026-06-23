"""Example: Complete TDA Pipeline on Rips Complex

Problem:
  Apply full TDA pipeline (Rips -> Persistence -> Descriptor) to a dataset.

Solution:
  Use pytop.TDAPipeline for end-to-end computation.
"""

import pytop
import random

random.seed(42)

# Generate random points in 2D
points = [(random.random(), random.random()) for _ in range(30)]

# Build and analyze TDA pipeline
pipeline = (pytop.TDAPipeline()
    .rips(max_radius=0.5)
    .reduce(method="twist")
    .pairs()
    .barcode()
)

result = pipeline.run(points)

print("TDA Pipeline Result:")
print(f"  H_0 count: {len([p for p in result.barcode if p[0] == 0])}")
print(f"  H_1 count: {len([p for p in result.barcode if p[0] == 1])}")
