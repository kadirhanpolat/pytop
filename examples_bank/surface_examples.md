# Surface Examples -- GEO-07

This examples page records standard surface profiles in a conservative way. The package stores dependable metadata for familiar models, but it does not prove the surface-classification theorem and it does not classify arbitrary polygon edge identifications.

## Minimal Python use

```python
from pytop import known_surface_profile, surface_profile_summary, as_manifold_profile

torus = known_surface_profile("torus")
summary = surface_profile_summary(torus)
manifold_view = as_manifold_profile(torus)

assert summary["genus"] == 1
assert summary["orientability"] == "orientable"
assert manifold_view.dimension == 2
```
