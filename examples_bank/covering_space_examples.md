# Covering Space Examples -- pytop v0.1.121

This page supports the covering-space bridge with conservative profiles. The
API records standard examples, sheet counts, and local-homeomorphism
assumptions. It is not a general covering verifier.

## Real line to circle

```python
from pytop import covering_profile_summary, known_covering_profile

profile = known_covering_profile("real_line_to_circle")
summary = covering_profile_summary(profile)

assert summary["total_space"] == "R"
assert summary["base_space"] == "S^1"
assert summary["sheet_count"] == "countably infinite"
```

The fundamental group note links deck-translation intuition with the standard
profile `pi_1(S^1) = Z`.

## Degree-n circle covering

```python
from pytop import circle_degree_covering_profile

profile = circle_degree_covering_profile(3)

assert profile.sheet_count == 3
assert "multiplies by 3" in profile.fundamental_group_note
```

This records the standard map `z -> z^n` for a concrete positive integer `n`.

## Trivial covering

```python
from pytop import known_covering_profile

profile = known_covering_profile("trivial_two_sheet_cover")

assert profile.sheet_count == 2
assert profile.is_certified
```

## Assumed profile

```python
from pytop import assumed_covering_map_profile

profile = assumed_covering_map_profile(
    "teaching_cover",
    total_space="E",
    base_space="B",
    sheet_count="finite",
)

assert profile.status == "assumed"
assert profile.has_local_homeomorphism_warning
```

The local homeomorphism condition is explicitly carried as an assumption.
