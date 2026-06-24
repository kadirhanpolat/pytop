"""Example: Cardinal Invariants of a Finite Space

Problem:
  Compute cardinal invariants (weight, density, character, cellularity) of a
  finite topological space.

Solution:
  Build a finite space with pytop.experimental.spaces.discrete_finite_space and
  evaluate each invariant function. These are exact for finite spaces.

Expected (discrete topology on 4 points):
  weight      = 4   (every singleton is a basic open set)
  density     = 4   (no proper subset is dense)
  character   = 1   (each point has a minimal neighborhood)
  cellularity = 4   (4 pairwise-disjoint nonempty opens)
"""

from pytop.experimental.spaces import (
    cellularity,
    character,
    density,
    discrete_finite_space,
    weight,
)

space = discrete_finite_space([1, 2, 3, 4])

print("Discrete Space (4 points):")
print(f"  Weight:      {weight(space)}")
print(f"  Density:     {density(space)}")
print(f"  Character:   {character(space)}")
print(f"  Cellularity: {cellularity(space)}")
