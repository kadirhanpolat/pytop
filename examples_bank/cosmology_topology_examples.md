# Cosmology topology examples -- MAN-03

- Version: `v0.2.502`
- Route: `MAN-03`
- Source lane: Adams & Franzosa, Chapter 14.4--14.5
- Scope: universe geometry, global topology and observational signatures

## A. Purpose

This note records non-verbatim, teaching-oriented example patterns for the
cosmology side of the applied topology lane. The goal is not to turn `pytop`
into a numerical cosmology package. The goal is to give the topology book
project a clear bridge from 3-manifold profiles to the question: how can a
locally Euclidean-looking universe have a nontrivial global shape?

## B. Example families

### B.1 Spherical, flat and hyperbolic model contrast

A learner first separates local geometry from global topology.

- Spherical models carry positive-curvature local geometry and include compact
  quotient examples such as spherical space forms.
- Flat models can be globally noncompact, as in Euclidean 3-space, or compact,
  as in the 3-torus obtained by identifying opposite faces.
- Hyperbolic models use negative-curvature local geometry and provide a rich
  class of compact or finite-volume quotient spaces.

Teaching point: local measurements do not by themselves determine global
manifold type. This is the same conceptual move used throughout topology:
nearby behavior and global identification data must be tracked separately.

### B.2 Cosmic crystallography

If a compact quotient model makes the same physical objects visible through
multiple topological copies, then pairwise distance data may show repeated
peaks. The example should be used qualitatively: it demonstrates what kind of
signature a global identification could leave in observational data, while also
warning that astronomical noise and evolution can obscure the signal.

### B.3 Matched circles in the sky

In compact-universe candidates, the last-scattering surface can intersect its
topological copies. A simplified teaching model asks students to imagine that
one physical circle is seen from two directions; matched circle patterns then
become a possible signature of the global topology.

### B.4 CMB large-scale pattern comparison

The cosmic microwave background gives a broad pattern surface on which global
shape restrictions may leave traces. The correct pedagogical emphasis is not
"topology predicts a single visible picture" but "topology constrains which
large-scale patterns are compatible with a candidate manifold family."

## C. Links to code profiles

- `UniverseGeometryProfile` stores the spherical, flat and hyperbolic geometry
  families.
- `CosmicTopologyObservationProfile` stores the observational signature
  families: cosmic crystallography, matched CMB circles and broad CMB pattern
  comparison.
- The profiles deliberately avoid numerical cosmology claims; they are metadata
  records for examples, lessons and later question-bank items.

## D. Question-bank seeds

1. Explain why a 3-torus and Euclidean 3-space can be locally similar but
   globally different.
2. Give one qualitative signal that could suggest a compact quotient universe.
3. Explain why absence of a simple repeated pattern is not by itself a proof
   that the universe is globally trivial.
4. Compare the role of quotient construction in flat universe examples with its
   role in earlier quotient-topology chapters.
