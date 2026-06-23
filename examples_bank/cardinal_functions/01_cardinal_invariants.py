"""Example: Cardinal Invariants of Finite Space

Problem:
  Compute cardinal invariants (weight, density, character, cellularity)
  for a finite topological space.

Solution:
  Use pytop.cardinal_invariants() for automatic computation.
"""

import pytop

# Create a finite space
space = pytop.discrete_topology(1, 2, 3, 4)

# Compute invariants
invs = pytop.cardinal_invariants(space)

print("Discrete Space (4 points):")
print(f"  Weight: {invs.weight}")
print(f"  Density: {invs.density}")
print(f"  Character: {invs.character}")
print(f"  Cellularity: {invs.cellularity}")
