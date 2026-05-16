"""Metric-space adapters and finite exact metric support.

This module keeps metric-facing names inside the core package while aligning
with the structured `Result` model used elsewhere in `pytop`.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from itertools import combinations
from itertools import product as cartesian_product
from math import isclose, sqrt
from typing import Any

from .finite_spaces import FiniteTopologicalSpace
from .infinite_spaces import MetricLikeSpace
from .result import Result
from .spaces import TopologicalSpace

DistanceLike = Callable[[Any, Any], float] | dict[tuple[Any, Any], float]


@dataclass
class MetricSpace(TopologicalSpace):
    """Topological-space wrapper carrying metric data.

    Parameters
    ----------
    carrier:
        Underlying set or point collection.
    distance:
        Either a callable `d(x, y)` or a symmetric dictionary keyed by pairs.
    metadata:
        Optional metadata. Representation is inferred unless explicitly given.
    tags:
        Additional semantic tags.
    """

    distance: DistanceLike | None = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('metric')
        if _has_finite_length(self.carrier):
            self.add_tags('finite')
            self.metadata.setdefault('representation', 'finite')
        else:
            self.metadata.setdefault('representation', 'infinite_metric')

    def distance_between(self, x: Any, y: Any) -> float:
        return _distance_between(self.distance, x, y)


@dataclass
class FiniteMetricSpace(MetricSpace):
    """A metric space whose carrier is explicitly finite."""

    carrier: Sequence[Any] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('finite')
        self.metadata['representation'] = 'finite'


@dataclass
class SymbolicMetricSpace(MetricLikeSpace):
    """A theorem-facing metric representation for infinite or implicit spaces."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('metric')
        self.metadata['representation'] = 'infinite_metric'


def open_ball(space: MetricSpace, center: Any, radius: float) -> set[Any]:
    if radius < 0:
        raise ValueError('Open-ball radius must be nonnegative.')
    if space.carrier is None:
        raise ValueError('Open balls require an explicit carrier.')
    return {point for point in space.carrier if space.distance_between(center, point) < radius}


def closed_ball(space: MetricSpace, center: Any, radius: float) -> set[Any]:
    """Return the closed ball around ``center`` with radius ``radius``.

    The carrier must be explicit because this package materializes balls by
    enumeration. Negative radii are rejected.
    """

    if radius < 0:
        raise ValueError('Closed-ball radius must be nonnegative.')
    if space.carrier is None:
        raise ValueError('Closed balls require an explicit carrier.')
    return {point for point in space.carrier if space.distance_between(center, point) <= radius}


def distance_to_subset(space: MetricSpace, point: Any, subset: Iterable[Any]) -> float:
    """Return ``d(point, A)`` for an explicit nonempty subset ``A``."""

    members = _normalize_explicit_subset(subset, name='subset')
    return min(space.distance_between(point, member) for member in members)


def distance_between_subsets(
    space: MetricSpace,
    subset_a: Iterable[Any],
    subset_b: Iterable[Any],
) -> float:
    """Return the minimum distance between two explicit nonempty subsets."""

    left = _normalize_explicit_subset(subset_a, name='subset_a')
    right = _normalize_explicit_subset(subset_b, name='subset_b')
    return min(space.distance_between(x, y) for x in left for y in right)


def diameter_of_subset(space: MetricSpace, subset: Iterable[Any]) -> float:
    """Return the diameter of an explicit nonempty subset.

    The empty-set diameter is convention-sensitive, so this helper rejects
    empty subsets instead of silently choosing a convention.
    """

    members = _normalize_explicit_subset(subset, name='subset')
    if len(members) == 1:
        return 0.0
    return max(space.distance_between(x, y) for x, y in combinations(members, 2))


def is_bounded_subset(space: MetricSpace, subset: Iterable[Any]) -> bool:
    """Return whether an explicit subset is bounded.

    Every explicit finite subset is bounded in a metric space; the helper still
    computes the diameter so that malformed distance data surfaces promptly.
    """

    members = _normalize_explicit_subset_allow_empty(subset, name='subset')
    if not members:
        return True
    _ = diameter_of_subset(space, members)
    return True


def capped_metric(distance: DistanceLike, *, cap: float = 1.0) -> Callable[[Any, Any], float]:
    """Return the transformed metric ``min(cap, d)``."""

    if cap <= 0:
        raise ValueError('The cap must be strictly positive.')

    def transformed(x: Any, y: Any) -> float:
        return min(cap, _distance_between(distance, x, y))

    return transformed



def normalized_metric(distance: DistanceLike) -> Callable[[Any, Any], float]:
    """Return the transformed metric ``d/(1+d)``."""

    def transformed(x: Any, y: Any) -> float:
        base = _distance_between(distance, x, y)
        return base / (1.0 + base)

    return transformed



def finite_product_metric_space(
    *spaces: MetricSpace,
    mode: str = 'max',
    metadata: dict[str, Any] | None = None,
    tags: Iterable[str] = (),
) -> FiniteMetricSpace:
    """Return a finite product metric space for explicit finite factors.

    Parameters
    ----------
    spaces:
        Metric spaces with explicit finite carriers. A single tuple/list of
        spaces is also accepted.
    mode:
        One of ``max``, ``sum``, or ``euclidean``.
    """

    factors = _normalize_product_factors(spaces)
    carriers = [tuple(space.carrier) for space in factors]
    product_carrier = tuple(cartesian_product(*carriers))

    if mode not in {'max', 'sum', 'euclidean'}:
        raise ValueError("mode must be one of {'max', 'sum', 'euclidean'}." )

    def product_distance(x: Sequence[Any], y: Sequence[Any]) -> float:
        if len(x) != len(factors) or len(y) != len(factors):
            raise ValueError('Product points must have one coordinate per factor.')
        component_distances = [
            factor.distance_between(x[idx], y[idx]) for idx, factor in enumerate(factors)
        ]
        if mode == 'max':
            return max(component_distances, default=0.0)
        if mode == 'sum':
            return sum(component_distances)
        return sqrt(sum(value * value for value in component_distances))

    payload = dict(metadata or {})
    payload.setdefault('representation', 'finite')
    payload.setdefault('source', 'finite_product_metric_space')
    payload['product_metric_mode'] = mode
    payload['factor_count'] = len(factors)
    payload['factor_representations'] = [
        factor.metadata.get('representation', 'finite') for factor in factors
    ]
    return FiniteMetricSpace(
        carrier=product_carrier,
        distance=product_distance,
        metadata=payload,
        tags=set(tags) | {'metric', 'finite', 'product'},
    )



def validate_metric(space: MetricSpace, *, tolerance: float = 1e-12) -> Result:
    """Validate metric axioms when the carrier is explicitly finite.

    For finite carriers the answer is exact. For non-explicit carriers, the
    function returns an honest symbolic/unknown result.
    """

    if not _has_finite_length(space.carrier):
        return Result.unknown(
            mode='symbolic',
            value='metric_axioms',
            justification=['Metric validation requires an explicit finite carrier or external assumptions.'],
            metadata={'representation': space.metadata.get('representation', 'infinite_metric')},
        )

    points = list(space.carrier)

    for x in points:
        try:
            diagonal = space.distance_between(x, x)
        except Exception as exc:
            return _metric_failure_result(
                'Distance evaluation failed while checking the diagonal axiom.',
                metadata={'point': x, 'exception': repr(exc)},
            )
        if not isclose(diagonal, 0.0, abs_tol=tolerance):
            return Result.false(
                mode='exact',
                value='metric_axioms',
                justification=['The identity axiom d(x,x)=0 failed for at least one point.'],
                metadata={'point': x, 'distance_xx': diagonal},
            )

    for x, y in combinations(points, 2):
        try:
            dxy = space.distance_between(x, y)
            dyx = space.distance_between(y, x)
        except Exception as exc:
            return _metric_failure_result(
                'Distance evaluation failed while checking positivity or symmetry.',
                metadata={'pair': (x, y), 'exception': repr(exc)},
            )
        if dxy <= tolerance or dyx <= tolerance:
            return Result.false(
                mode='exact',
                value='metric_axioms',
                justification=['Distinct points must have strictly positive distance.'],
                metadata={'pair': (x, y), 'distance_xy': dxy, 'distance_yx': dyx},
            )
        if not isclose(dxy, dyx, abs_tol=tolerance):
            return Result.false(
                mode='exact',
                value='metric_axioms',
                justification=['The symmetry axiom d(x,y)=d(y,x) failed.'],
                metadata={'pair': (x, y), 'distance_xy': dxy, 'distance_yx': dyx},
            )

    for x in points:
        for y in points:
            for z in points:
                try:
                    dxy = space.distance_between(x, y)
                    dxz = space.distance_between(x, z)
                    dzy = space.distance_between(z, y)
                except Exception as exc:
                    return _metric_failure_result(
                        'Distance evaluation failed while checking the triangle inequality.',
                        metadata={'triple': (x, y, z), 'exception': repr(exc)},
                    )
                if dxy - (dxz + dzy) > tolerance:
                    return Result.false(
                        mode='exact',
                        value='metric_axioms',
                        justification=['The triangle inequality failed.'],
                        metadata={
                            'triple': (x, y, z),
                            'distance_xy': dxy,
                            'distance_xz': dxz,
                            'distance_zy': dzy,
                        },
                    )

    return Result.true(
        mode='exact',
        value='metric_axioms',
        justification=['All metric axioms hold on the explicit finite carrier.'],
        proof_outline=[
            'Checked identity, positivity, symmetry, and triangle inequality on all relevant tuples.'
        ],
        metadata={'representation': space.metadata.get('representation', 'finite')},
    )



def induced_topological_space(space: MetricSpace) -> TopologicalSpace:
    """Return a `TopologicalSpace` induced by the metric.

    On explicit finite carriers, the induced topology is the discrete topology.
    This is a mathematically exact simplification: every finite metric space is
    discrete. For implicit/infinite carriers, the function returns a symbolic
    topological space tagged as metric.
    """

    if _has_finite_length(space.carrier):
        validation = validate_metric(space)
        if validation.is_false:
            raise ValueError('The supplied finite distance data does not define a metric.')
        points = tuple(space.carrier)
        topology = _power_set(points)
        return FiniteTopologicalSpace(
            carrier=points,
            topology=topology,
            metadata={
                'description': 'Topology induced from an explicit finite metric space.',
                'representation': 'finite',
                'source': 'metric',
                'tags': sorted(set(space.metadata.get('tags', [])) | {'metric', 'finite', 'discrete'}),
            },
            tags={'metric', 'finite', 'discrete'},
        )

    return TopologicalSpace.symbolic(
        description='Topology induced by a metric representation.',
        representation='infinite_metric',
        tags={'metric'},
    )



def _metric_failure_result(reason: str, *, metadata: dict[str, Any]) -> Result:
    return Result.false(
        mode='exact',
        value='metric_axioms',
        justification=[reason],
        metadata=metadata,
    )



def _distance_between(distance: DistanceLike | None, x: Any, y: Any) -> float:
    if distance is None:
        raise ValueError('A metric space requires a distance specification.')
    if callable(distance):
        return float(distance(x, y))
    for key in ((x, y), (y, x)):
        if key in distance:
            return float(distance[key])
    raise KeyError(f'No distance data available for pair {(x, y)!r}.')



def _normalize_explicit_subset(subset: Iterable[Any], *, name: str) -> tuple[Any, ...]:
    members = _normalize_explicit_subset_allow_empty(subset, name=name)
    if not members:
        raise ValueError(f'{name} must be a nonempty explicit subset.')
    return members



def _normalize_explicit_subset_allow_empty(subset: Iterable[Any], *, name: str) -> tuple[Any, ...]:
    if subset is None or isinstance(subset, (str, bytes)):
        raise ValueError(f'{name} must be an explicit iterable of points.')
    try:
        members = tuple(subset)
    except TypeError as exc:
        raise ValueError(f'{name} must be an explicit iterable of points.') from exc
    return members



def _normalize_product_factors(spaces: tuple[MetricSpace, ...]) -> tuple[MetricSpace, ...]:
    if len(spaces) == 1 and isinstance(spaces[0], (list, tuple)):
        candidate = tuple(spaces[0])
    else:
        candidate = tuple(spaces)
    if not candidate:
        raise ValueError('finite_product_metric_space requires at least one factor.')
    normalized: list[MetricSpace] = []
    for idx, space in enumerate(candidate):
        if not isinstance(space, MetricSpace):
            raise TypeError(f'Factor {idx} is not a MetricSpace instance.')
        if not _has_finite_length(space.carrier):
            raise ValueError('finite_product_metric_space requires explicit finite carriers for all factors.')
        normalized.append(space)
    return tuple(normalized)



def _has_finite_length(obj: Any) -> bool:
    if isinstance(obj, (str, bytes)) or obj is None:
        return False
    try:
        len(obj)
    except Exception:
        return False
    return True



def _power_set(points: Sequence[Any]) -> list[set[Any]]:
    items = list(points)
    out: list[set[Any]] = []
    for mask in range(1 << len(items)):
        subset = {items[i] for i in range(len(items)) if mask & (1 << i)}
        out.append(subset)
    return out


__all__ = [
    "DistanceLike",
    "MetricSpace",
    "FiniteMetricSpace",
    "SymbolicMetricSpace",
    "open_ball",
    "closed_ball",
    "distance_to_subset",
    "distance_between_subsets",
    "diameter_of_subset",
    "is_bounded_subset",
    "capped_metric",
    "normalized_metric",
    "finite_product_metric_space",
    "validate_metric",
    "induced_topological_space",
]
