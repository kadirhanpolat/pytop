"""Symbolic quotient-space support for infinite settings."""

from __future__ import annotations

from typing import Any

from .infinite_maps import QuotientMap, SymbolicMap, analyze_infinite_map_property
from .infinite_spaces import InfiniteTopologicalSpace


def quotient_space(domain: Any, relation_label: str, *, metadata: dict[str, Any] | None = None) -> InfiniteTopologicalSpace:
    metadata = dict(metadata or {})
    tags = {'quotient_space'}
    if str(getattr(domain, 'metadata', {}).get('representation', '')).startswith('infinite_'):
        tags.add('infinite')
    metadata.setdefault('description', f'Quotient of {getattr(domain, "carrier", "X")!r} by relation {relation_label!r}.')
    metadata.setdefault('construction', 'quotient')
    metadata.setdefault('relation_label', relation_label)
    return InfiniteTopologicalSpace(carrier=f'{getattr(domain, "carrier", "X")}/{relation_label}', metadata={**metadata, 'tags': sorted(tags)}, tags=tags)


def quotient_space_from_map(map_obj: SymbolicMap, *, metadata: dict[str, Any] | None = None) -> InfiniteTopologicalSpace:
    metadata = dict(metadata or {})
    codomain = getattr(map_obj, 'codomain', None)
    tags = set(getattr(codomain, 'tags', set())) | {'quotient_space'}
    if analyze_infinite_map_property(map_obj, 'quotient').is_true:
        tags.add('realized_by_quotient_map')
    metadata.setdefault('description', f'Quotient space realized by map {getattr(map_obj, "name", "q")}.')
    metadata.setdefault('construction', 'quotient_from_map')
    metadata.setdefault('map_name', getattr(map_obj, 'name', 'q'))
    return InfiniteTopologicalSpace(carrier=getattr(codomain, 'carrier', None), metadata={**getattr(codomain, 'metadata', {}), **metadata, 'tags': sorted(tags)}, tags=tags)


def make_quotient_map(domain: Any, codomain: Any, *, name: str = 'q', metadata: dict[str, Any] | None = None) -> QuotientMap:
    return QuotientMap(domain=domain, codomain=codomain, name=name, metadata=dict(metadata or {}))


def analyze_quotient_map(map_obj: SymbolicMap):
    return analyze_infinite_map_property(map_obj, 'quotient')


__all__ = ['quotient_space', 'quotient_space_from_map', 'make_quotient_map', 'analyze_quotient_map']
