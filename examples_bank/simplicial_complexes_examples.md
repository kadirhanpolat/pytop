# Simplicial Complexes Examples -- v0.1.115

This examples surface supports `GEO-04`: finite abstract simplicial complexes.
The implementation is combinatorial and finite. Homology, triangulation
algorithms, and PL classification are intentionally deferred.

## Generate a filled triangle complex

```python
from pytop.simplicial_complexes import generated_subcomplex

triangle = generated_subcomplex([["a", "b", "c"]])

assert triangle.dimension == 2
assert triangle.f_vector() == (3, 3, 1)
assert triangle.euler_characteristic() == 1
```

## Facets and skeletons

```python
complex_obj = generated_subcomplex([["a", "b", "c"], ["c", "d"]])

facets = {facet.vertices for facet in complex_obj.facets()}
one_skeleton = complex_obj.skeleton(1)

assert facets == {frozenset(["a", "b", "c"]), frozenset(["c", "d"])}
assert one_skeleton.dimension == 1
```

## Face-closure diagnostics

```python
from pytop.simplicial_complexes import face_closure_diagnostic

diagnostic = face_closure_diagnostic([["a", "b", "c"]])

assert diagnostic.is_face_closed is False
assert frozenset(["a", "b"]) in diagnostic.missing_faces
```

The diagnostic is useful when teaching why a lone triangle without its faces is
not yet a simplicial complex.
