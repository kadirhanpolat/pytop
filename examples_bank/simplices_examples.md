# Simplices Examples -- v0.1.114

This examples surface supports `GEO-03`: a small combinatorial vocabulary for
simplexes. The model uses finite vertex sets only. Coordinates, PL topology,
homology, and triangulation algorithms are intentionally deferred.

## Basic dimensions

```python
from pytop.simplices import Simplex

point = Simplex(["p"])
edge = Simplex(["a", "b"])
triangle = Simplex(["a", "b", "c"])
tetrahedron = Simplex(["a", "b", "c", "d"])

assert point.dimension == 0
assert edge.dimension == 1
assert triangle.dimension == 2
assert tetrahedron.dimension == 3
```

## Faces and boundary faces

```python
triangle = Simplex(["a", "b", "c"])

all_faces = {face.vertices for face in triangle.faces()}
boundary = {face.vertices for face in triangle.boundary_faces()}

assert frozenset(["a", "b", "c"]) in all_faces
assert boundary == {
    frozenset(["a", "b"]),
    frozenset(["a", "c"]),
    frozenset(["b", "c"]),
}
```

## Equality by vertex set

```python
assert Simplex(["a", "b", "c"]) == Simplex(["c", "a", "b"])
```

The equality rule is intentionally combinatorial: two simplexes with the same
vertices are the same abstract simplex, regardless of input order.
