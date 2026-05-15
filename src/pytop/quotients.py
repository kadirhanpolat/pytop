"""Unified quotient constructions.

Finite quotients are computed exactly from explicit partitions or finite maps.
Infinite and symbolic quotients use the symbolic quotient layer.
"""

from __future__ import annotations

from typing import Any, Iterable

from .finite_spaces import FiniteTopologicalSpace
from .infinite_quotients import analyze_quotient_map as analyze_symbolic_quotient_map
from .infinite_quotients import make_quotient_map as make_symbolic_quotient_map
from .infinite_quotients import quotient_space as symbolic_quotient_space
from .infinite_quotients import quotient_space_from_map as symbolic_quotient_from_map
from .maps import FiniteMap, analyze_map_property


def quotient_space(space: Any, partition: Iterable[Iterable[Any]] | str, *, metadata: dict[str, Any] | None = None):
    metadata = dict(metadata or {})
    if _space_is_finite(space) and hasattr(space, 'topology') and not isinstance(partition, str):
        return _finite_quotient_from_partition(space, partition, metadata=metadata)
    return symbolic_quotient_space(space, str(partition), metadata=metadata)


def quotient_space_from_map(map_obj: Any, *, metadata: dict[str, Any] | None = None):
    metadata = dict(metadata or {})
    if isinstance(map_obj, FiniteMap) and _space_is_finite(map_obj.domain) and _space_is_finite(map_obj.codomain):
        return _finite_quotient_from_map(map_obj, metadata=metadata)
    return symbolic_quotient_from_map(map_obj, metadata=metadata)


def make_quotient_map(domain: Any, codomain: Any, *, mapping: dict[Any, Any] | None = None, name: str = 'q', metadata: dict[str, Any] | None = None):
    metadata = dict(metadata or {})
    if mapping is not None and _space_is_finite(domain) and _space_is_finite(codomain):
        return FiniteMap(domain=domain, codomain=codomain, name=name, mapping=mapping, metadata=metadata, tags={'surjective'})
    return make_symbolic_quotient_map(domain, codomain, name=name, metadata=metadata)


def analyze_quotient_map(map_obj: Any):
    if isinstance(map_obj, FiniteMap):
        return analyze_map_property(map_obj, 'quotient')
    return analyze_symbolic_quotient_map(map_obj)


def _finite_quotient_from_partition(space: Any, partition: Iterable[Iterable[Any]], *, metadata: dict[str, Any] | None = None) -> FiniteTopologicalSpace:
    metadata = dict(metadata or {})
    classes = _normalize_partition(partition)
    quotient_points = tuple(range(len(classes)))
    projection = {x: i for i, cls in enumerate(classes) for x in cls}
    topology = _finite_quotient_topology(space, projection, quotient_points)
    return FiniteTopologicalSpace(
        carrier=quotient_points,
        topology=[set(U) for U in sorted(topology, key=lambda s: (len(s), tuple(sorted(map(repr, s)))))],
        metadata={
            **getattr(space, 'metadata', {}),
            **metadata,
            'representation': 'finite',
            'construction': 'quotient',
            'description': metadata.get('description', 'Finite quotient space.'),
            'partition_size': len(classes),
        },
        tags=set(getattr(space, 'tags', set())) | {'quotient_space'},
    )


def _finite_quotient_from_map(map_obj: FiniteMap, *, metadata: dict[str, Any] | None = None) -> FiniteTopologicalSpace:
    metadata = dict(metadata or {})
    projection = map_obj.graph_dict()
    codomain_points = tuple(getattr(map_obj.codomain, 'carrier', ()))
    topology = _finite_quotient_topology(map_obj.domain, projection, codomain_points)
    return FiniteTopologicalSpace(
        carrier=codomain_points,
        topology=[set(U) for U in sorted(topology, key=lambda s: (len(s), tuple(sorted(map(repr, s)))))],
        metadata={
            **getattr(map_obj.codomain, 'metadata', {}),
            **metadata,
            'representation': 'finite',
            'construction': 'quotient_from_map',
            'description': metadata.get('description', f'Finite quotient realized by map {getattr(map_obj, "name", "q")}.'),
        },
        tags=set(getattr(map_obj.codomain, 'tags', set())) | {'quotient_space'},
    )


def _finite_quotient_topology(space: Any, projection: dict[Any, Any], quotient_points: Iterable[Any]) -> set[frozenset[Any]]:
    domain_open_sets = {frozenset(U) for U in getattr(space, 'topology', ())}
    quotient_points = list(quotient_points)
    topology: set[frozenset[Any]] = set()
    for mask in range(1 << len(quotient_points)):
        subset = {quotient_points[i] for i in range(len(quotient_points)) if mask & (1 << i)}
        preimage = frozenset({x for x, qx in projection.items() if qx in subset})
        if preimage in domain_open_sets:
            topology.add(frozenset(subset))
    return topology


def _normalize_partition(partition: Iterable[Iterable[Any]]) -> list[set[Any]]:
    classes = [set(cls) for cls in partition if set(cls)]
    return classes


def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False


__all__ = ['quotient_space', 'quotient_space_from_map', 'make_quotient_map', 'analyze_quotient_map']
