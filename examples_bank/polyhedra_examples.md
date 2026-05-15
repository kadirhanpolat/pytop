# Polyhedra Examples and Bridge -- v0.1.116

This examples surface supports `GEO-04`: connecting simplexes and finite
simplicial complexes with polyhedron intuition. It is original teaching
material for the package. It does not copy book text, exercises, examples, or
proofs, and it does not enter PL-topology classification or homology.

## Simplex to complex to polyhedron

A `Simplex` is the combinatorial record of one nonempty finite vertex set. A
`SimplicialComplex` is a finite family of simplexes that is closed under
nonempty faces. A polyhedron is the geometric intuition obtained when such a
complex is pictured as glued geometric pieces.

```python
from pytop.simplicial_complexes import generated_subcomplex

filled_triangle = generated_subcomplex([["a", "b", "c"]])

assert filled_triangle.dimension == 2
assert filled_triangle.f_vector() == (3, 3, 1)
assert filled_triangle.euler_characteristic() == 1
```

Interpretation:

- the vertices are the 0-dimensional pieces,
- the edges are the 1-dimensional pieces,
- the triangle is the 2-dimensional piece,
- the polyhedron intuition is a filled triangular patch.

## Boundary-only triangle

```python
from pytop.simplicial_complexes import generated_subcomplex

triangle_boundary = generated_subcomplex([
    ["a", "b"],
    ["b", "c"],
    ["a", "c"],
])

assert triangle_boundary.dimension == 1
assert triangle_boundary.f_vector() == (3, 3)
assert triangle_boundary.euler_characteristic() == 0
assert triangle_boundary.connectedness_preview()["connected"] is True
```

Interpretation: the same three labeled vertices can support either a filled
triangle or only its boundary. The combinatorial model records that distinction
before any drawing is made.

## Subdivision intuition

A subdivision should be read here as a teaching-level refinement idea: replace
a coarse piece by smaller compatible pieces without changing the intended
underlying shape. For example, one edge `["a", "b"]` may be pictured as two
edges `["a", "m"]` and `["m", "b"]` with a new midpoint label `m`.

```python
coarse_edge = generated_subcomplex([["a", "b"]])
subdivided_edge = generated_subcomplex([["a", "m"], ["m", "b"]])

assert coarse_edge.dimension == 1
assert subdivided_edge.dimension == 1
assert coarse_edge.f_vector() == (2, 1)
assert subdivided_edge.f_vector() == (3, 2)
```

This package does not claim to decide when two complexes have homeomorphic
realizations. The example only shows how the combinatorial bookkeeping changes
under a simple refinement.

## Topological space versus combinatorial model

The finite complex is data: vertices, simplexes, facets, skeletons, and
incidence. The associated polyhedron intuition is spatial: a picture assembled
from points, intervals, triangles, or higher-dimensional pieces. The bridge is
useful because many geometric topology examples begin with a picture but need a
finite combinatorial record for checking faces, dimensions, and adjacency.

The current code supports the record. Later routes may add more examples, but
homology, arbitrary triangulation recognition, and PL classification remain
deferred.
