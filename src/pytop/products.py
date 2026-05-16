"""Unified product constructions.

Finite products are computed exactly. Infinite or symbolic products are
delegated to the symbolic construction layer.
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import product as cartesian_product
from typing import Any

from .finite_spaces import FiniteTopologicalSpace
from .infinite_constructions import product as infinite_product


def product(*spaces: Any, metadata: dict[str, Any] | None = None):
    metadata = dict(metadata or {})
    if spaces and all(_space_is_finite(space) and hasattr(space, 'topology') for space in spaces):
        return _finite_product(*spaces, metadata=metadata)
    return infinite_product(*spaces, metadata=metadata)


def binary_product(left: Any, right: Any, *, metadata: dict[str, Any] | None = None):
    return product(left, right, metadata=metadata)


def _finite_product(*spaces: Any, metadata: dict[str, Any] | None = None) -> FiniteTopologicalSpace:
    metadata = dict(metadata or {})
    carriers = [tuple(getattr(space, 'carrier', ())) for space in spaces]
    carrier = tuple(cartesian_product(*carriers))
    basis = []
    open_families = []
    for space in spaces:
        family = [set(U) for U in getattr(space, 'topology', ())]
        open_families.append(family)
    for basic_factors in cartesian_product(*open_families):
        basic_set = set(cartesian_product(*basic_factors))
        basis.append(basic_set)
    topology = _topology_from_basis(carrier, basis)
    tags = set.intersection(*(set(getattr(space, 'tags', set())) for space in spaces)) if spaces else set()
    if len(spaces) > 1 and all('connected' in getattr(space, 'tags', set()) for space in spaces):
        tags.add('connected')
    if all('compact' in getattr(space, 'tags', set()) for space in spaces):
        tags.add('compact')
    return FiniteTopologicalSpace(
        carrier=carrier,
        topology=[set(U) for U in sorted(topology, key=lambda s: (len(s), tuple(sorted(map(repr, s)))))],
        metadata={
            'representation': 'finite',
            'construction': 'product',
            'description': metadata.get('description', 'Finite product topological space.'),
            **metadata,
        },
        tags=tags,
    )


def _topology_from_basis(carrier: Iterable[Any], basis: list[set[Any]]) -> set[frozenset[Any]]:
    carrier_list = list(carrier)
    topology: set[frozenset[Any]] = set()
    for mask in range(1 << len(carrier_list)):
        subset = {carrier_list[i] for i in range(len(carrier_list)) if mask & (1 << i)}
        if _is_open_from_basis(subset, basis):
            topology.add(frozenset(subset))
    return topology


def _is_open_from_basis(subset: set[Any], basis: list[set[Any]]) -> bool:
    if not subset:
        return True
    for point in subset:
        if not any(point in B and B.issubset(subset) for B in basis):
            return False
    return True


def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False


__all__ = ['product', 'binary_product']
