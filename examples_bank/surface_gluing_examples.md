# Surface Gluing Examples -- GEO-07

This page introduces polygon edge-identification words for the geometric topology bridge. The notation follows one explicit convention: a boundary word is read counterclockwise, and `x^-1` means that the second occurrence of edge `x` is read with the reversed orientation.

| Surface model | Edge word | Expected orientability hint |
|---|---|---|
| Sphere | `a a^-1` | orientable |
| Torus | `a b a^-1 b^-1` | orientable |
| Projective plane | `a a` | nonorientable |
| Klein bottle | `a b a^-1 b` | nonorientable |

```python
from pytop import gluing_profile_summary, standard_gluing_profile

torus = standard_gluing_profile("torus")
summary = gluing_profile_summary(torus)
assert summary["pairing_valid"]
assert summary["orientability_hint"] == "orientable"
```

The orientability value is a convention-bound hint, not a full surface-classification algorithm.
