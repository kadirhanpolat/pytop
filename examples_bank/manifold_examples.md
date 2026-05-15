# Manifold examples -- GEO-07

This fixed examples surface introduces topological manifold profiles for the
geometric-topology bridge. The purpose is pedagogical: record standard models,
local-model language, boundary metadata, and orientability status without
turning `pytop` into a general manifold-recognition system.

## 1. Local model first

A topological `n`-manifold is locally modeled on `R^n`. A manifold with boundary
is locally modeled on `R^n` at interior points and on the closed half-space
`H^n` near boundary points. The profile API records this distinction with the
`local_model` and `with_boundary` fields.

```python
from pytop import real_line_manifold_profile, disk_with_boundary_profile

line = real_line_manifold_profile()
disk = disk_with_boundary_profile(2)

assert line.local_model == "R^1"
assert disk.with_boundary is True
assert disk.metadata["boundary_model"] == "S^1"
```

## 2. Compact one- and two-dimensional models

The circle, sphere, torus, and real projective plane are registered as standard
teaching profiles. Their entries carry compactness, connectedness, and
orientability metadata.

```python
from pytop import circle_manifold_profile, sphere_manifold_profile

circle = circle_manifold_profile()
sphere = sphere_manifold_profile(2)

assert circle.dimension == 1
assert sphere.dimension == 2
assert sphere.orientability == "orientable"
```

## 3. Boundary is not a defect

The closed disk is a manifold with boundary. Its boundary flag does not mean it
is less topological; it means boundary points have half-space neighborhoods in
the teaching model.

```python
from pytop import disk_with_boundary_profile, manifold_profile_summary

summary = manifold_profile_summary(disk_with_boundary_profile(2))
assert summary["with_boundary"] is True
assert "half-space" in summary["local_model"]
```

## 4. Orientability is recorded conservatively

The torus is registered as orientable. The real projective plane is registered
as nonorientable. These are standard-model facts stored in a registry; the
module does not attempt to infer orientability from arbitrary quotient data.

```python
from pytop import torus_manifold_profile, projective_plane_manifold_profile

assert torus_manifold_profile().orientability == "orientable"
assert projective_plane_manifold_profile().orientability == "nonorientable"
```

## 5. Unknown input remains unknown

When a key is not in the standard registry, the API returns an explicit unknown
profile rather than pretending to classify the space.

```python
from pytop import known_manifold_profile

mystery = known_manifold_profile("wild quotient candidate")
assert mystery.status == "unknown"
```

## Guardrail

This surface does not introduce smooth structures, coordinate atlases with
transition-map checks, surface classification, triangulation algorithms, or
general manifold recognition. Those tasks are either out of scope or deferred
to later route-specific profile layers.
