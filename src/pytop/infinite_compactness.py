"""Structured compactness analysis for supported infinite space families."""

from __future__ import annotations

from typing import Any

from .compactness import analyze_compactness
from .infinite_spaces import CocountableSpace, CofiniteSpace, DiscreteInfiniteSpace, IndiscreteInfiniteSpace, InfiniteTopologicalSpace
from .result import Result


KNOWN_TRUE = {
    IndiscreteInfiniteSpace: {'compact', 'lindelof'},
    CofiniteSpace: {'compact'},
    CocountableSpace: {'lindelof'},
}

KNOWN_FALSE = {
    DiscreteInfiniteSpace: {'compact'},
    CocountableSpace: {'compact'},
}


def analyze_infinite_compactness(space: Any, property_name: str = 'compact') -> Result:
    if not isinstance(space, InfiniteTopologicalSpace):
        return analyze_compactness(space, property_name)
    property_name = str(property_name).strip().lower().replace('-', '_').replace(' ', '_')
    for cls, features in KNOWN_TRUE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.true(
                mode='exact',
                value=property_name,
                justification=[f'{cls.__name__} has a class-level exact compactness classification for {property_name}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': cls.__name__},
            )
    for cls, features in KNOWN_FALSE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.false(
                mode='exact',
                value=property_name,
                justification=[f'{cls.__name__} has a class-level exact compactness classification for {property_name}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': cls.__name__},
            )
    return analyze_compactness(space, property_name)


def is_compact_infinite(space: Any) -> Result:
    return analyze_infinite_compactness(space, 'compact')


def is_lindelof_infinite(space: Any) -> Result:
    return analyze_infinite_compactness(space, 'lindelof')


def infinite_compactness_report(space: Any) -> dict[str, Result]:
    return {
        'compact': is_compact_infinite(space),
        'lindelof': is_lindelof_infinite(space),
    }
