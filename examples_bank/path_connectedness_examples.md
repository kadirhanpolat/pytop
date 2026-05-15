# Path and Path-Connectedness Examples -- v0.1.118

This examples surface supports `GEO-05`: paths, loops, and path-connectedness
diagnostics. The module records profiles and finite known-path graphs. It does
not verify analytic continuity for arbitrary functions.

## Path profiles and loops

```python
from pytop.paths import path_profile, is_loop_path

arc = path_profile("arc_ab", "a", "b", points=("a", "m", "b"))
loop = path_profile("loop_a", "a", "a", points=("a", "m", "a"))

assert arc.start == "a"
assert arc.end == "b"
assert is_loop_path(loop) is True
```

## Reverse and concatenate

```python
from pytop.paths import concatenate_path_profiles, reverse_path_profile

ab = path_profile("ab", "a", "b", points=("a", "b"))
bc = path_profile("bc", "b", "c", points=("b", "c"))

ba = reverse_path_profile(ab)
ac = concatenate_path_profiles(ab, bc, name="ac")

assert ba.start == "b"
assert ba.end == "a"
assert ac.points == ("a", "b", "c")
```

## Finite path-connectedness diagnostic

```python
from pytop.paths import path_connectedness_diagnostic

diagnostic = path_connectedness_diagnostic({"a", "b", "c"}, [ab, bc])

assert diagnostic.connected is True
assert diagnostic.certification == "finite-path-graph"
```

This diagnostic sees the finite graph of recorded path endpoints. It is useful
for examples and quick checks, but it does not collapse connectedness and
path-connectedness into the same concept.
