# Euclidean Topology Examples -- pytop v0.1.122

This page supports `GEO-06` with profile-based Euclidean topology examples.
The bridge records balls, disks, spheres, punctured-sphere intuition,
stereographic projection intuition, and projective previews. It does not prove
invariance of domain or classify projective spaces.

## Balls and disks

```python
from pytop import closed_disk_profile, open_ball_profile

ball = open_ball_profile(2)
disk = closed_disk_profile(2)

assert ball.kind == "open_ball"
assert disk.boundary == "S^1"
```

## Spheres

```python
from pytop import sphere_profile

sphere = sphere_profile(2)

assert sphere.model == "S^2 subset R^3"
assert sphere.intrinsic_dimension == 2
```

## Sphere minus one point

```python
from pytop import punctured_sphere_profile

profile = punctured_sphere_profile(2)

assert profile.status == "preview"
assert "R^2" in profile.intuition
```

The statement is kept as teaching intuition here; coordinate proofs are left to
future notebook work.

## Stereographic projection intuition

```python
from pytop import stereographic_projection_profile

profile = stereographic_projection_profile(2)

assert profile.kind == "stereographic_projection"
assert profile.is_preview
```

## Projective previews

```python
from pytop import projective_preview_profile

line = projective_preview_profile("projective_line")
plane = projective_preview_profile("projective_plane")

assert "antipodal" in line.model
assert plane.status == "preview"
```

Projective examples are preview labels for later quotient and surface work, not
a full projective-space classification.
