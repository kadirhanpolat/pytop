# Homotopy Profile Examples -- pytop v0.1.119

This page supports `GEO-05` with conservative homotopy profile examples.
The API records claims, labels relative constraints, and distinguishes
`not_certified` from `unknown`. It is not a general homotopy decision
procedure.

## Positive profile with a witness label

```python
from pytop import homotopic, homotopy_summary

profile = homotopic(
    "straight_path_a_to_b",
    "curved_path_a_to_b",
    relative_to={"a", "b"},
    witness="endpoint-fixed planar deformation",
)

assert profile.status == "homotopic"
assert profile.has_relative_label
assert homotopy_summary(profile)["relative_to"] == ("a", "b")
```

## Missing certificate is not a negative theorem

```python
from pytop import not_certified_homotopy

profile = not_certified_homotopy("map_f", "map_g")

assert profile.status == "not_certified"
```

`not_certified` means the current profile data has no supplied certificate.
It does not assert that the two maps are not homotopic.

## Unknown registry lookup

```python
from pytop import known_contractible_profile

registered = known_contractible_profile("closed_interval")
unregistered = known_contractible_profile("circle")

assert registered.status == "certified"
assert unregistered.status == "unknown"
```

The registry is intentionally small. It contains only safe teaching examples
such as one-point spaces, closed intervals, convex disks, and filled simplices.

## Deformation-retraction profile

```python
from pytop import deformation_retraction_profile

profile = deformation_retraction_profile(
    "annulus_to_core_circle_profile",
    space="annulus",
    subspace="core circle",
    status="not_certified",
    strong=True,
    notes=("symbolic profile only",),
)

assert profile.strong
assert profile.status == "not_certified"
```

This keeps deformation-retraction language available without pretending that
arbitrary spaces have been analyzed.
