# Fundamental Group Profile Examples -- pytop v0.1.120

This page supports `GEO-05` with a conservative first layer for fundamental
group profiles. The API records standard teaching models and basepoint
metadata. It is not a general fundamental group calculator.

## Trivial group profile

```python
from pytop import fundamental_group_summary, known_fundamental_group_profile

profile = known_fundamental_group_profile("contractible_space")
summary = fundamental_group_summary(profile)

assert summary["kind"] == "trivial"
assert summary["status"] == "certified"
assert summary["rank"] == 0
```

## Infinite cyclic profile

```python
from pytop import known_fundamental_group_profile

circle = known_fundamental_group_profile("circle")

assert circle.kind == "infinite_cyclic"
assert circle.generators == ("loop",)
```

This is a standard teaching profile for `pi_1(S^1)`. The module does not prove
the theorem or compute fundamental groups of arbitrary spaces.

## Free group profile

```python
from pytop import free_group_profile

profile = free_group_profile(
    "figure-eight space",
    basepoint="wedge point",
    generators=("a", "b"),
)

assert profile.kind == "free"
assert profile.rank == 2
```

## Unknown cases stay unknown

```python
from pytop import known_fundamental_group_profile

profile = known_fundamental_group_profile("mystery_space")

assert profile.status == "unknown"
```

Missing registry data is not interpreted as a nontriviality theorem, a
triviality theorem, or a presentation.
