# Metric Map Taxonomy Examples -- v0.1.113

This examples surface supports `GEO-02`: map types between metric spaces. It is
intentionally profile-based. Exact certification is restricted to explicit
finite metric spaces; symbolic entries record known labels without pretending to
prove arbitrary analytic facts.

## Exact finite identity

```python
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_map_taxonomy import classify_finite_metric_map

line = FiniteMetricSpace(
    carrier=(0, 1, 2),
    distance=lambda x, y: abs(x - y),
    metadata={"name": "three point line"},
)

profile = classify_finite_metric_map(line, line, {0: 0, 1: 1, 2: 2}, name="id")
assert profile.isometry is True
assert profile.similarity is True
assert profile.non_expansive is True
assert profile.homeomorphism is True
```

## Similarity that is not non-expansive

```python
domain = FiniteMetricSpace(carrier=(0, 1, 2), distance=lambda x, y: abs(x - y))
codomain = FiniteMetricSpace(carrier=(0, 2, 4), distance=lambda x, y: abs(x - y))

double = classify_finite_metric_map(
    domain,
    codomain,
    {0: 0, 1: 2, 2: 4},
    name="double",
)

assert double.lipschitz_constant == 2
assert double.similarity_ratio == 2
assert double.non_expansive is False
assert double.homeomorphism is True
```

## Constant finite map

```python
domain = FiniteMetricSpace(carrier=("a", "b"), distance=lambda x, y: 0 if x == y else 1)
codomain = FiniteMetricSpace(carrier=("p", "q"), distance=lambda x, y: 0 if x == y else 1)

constant = classify_finite_metric_map(domain, codomain, {"a": "p", "b": "p"})

assert constant.lipschitz is True
assert constant.non_expansive is True
assert constant.isometry is False
assert constant.homeomorphism is False
```

## Symbolic profile

```python
from pytop.metric_map_taxonomy import metric_map_profile

symbolic = metric_map_profile(name="f", lipschitz=True, lipschitz_constant=3)
assert symbolic.lipschitz is True
assert symbolic.continuous is None
assert symbolic.certification == "symbolic-profile"
```

The last example records a claim supplied by the caller. It does not infer
continuity, uniform continuity, or homeomorphism unless those labels are also
provided or an exact finite classification is requested.
