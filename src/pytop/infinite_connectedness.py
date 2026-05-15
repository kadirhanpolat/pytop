"""Structured connectedness analysis for supported infinite space families."""

from __future__ import annotations

from typing import Any

from .connectedness import analyze_connectedness
from .infinite_spaces import CocountableSpace, CofiniteSpace, DiscreteInfiniteSpace, IndiscreteInfiniteSpace, InfiniteTopologicalSpace
from .result import Result


KNOWN_TRUE = {
    DiscreteInfiniteSpace: set(),
    IndiscreteInfiniteSpace: {'connected', 'path_connected'},
    CofiniteSpace: {'connected'},
    CocountableSpace: {'connected'},
}

KNOWN_FALSE = {
    DiscreteInfiniteSpace: {'connected', 'path_connected'},
}


def analyze_infinite_connectedness(space: Any, property_name: str = 'connected') -> Result:
    if not isinstance(space, InfiniteTopologicalSpace):
        return analyze_connectedness(space, property_name)
    property_name = str(property_name).strip().lower().replace('-', '_').replace(' ', '_')
    for cls, features in KNOWN_TRUE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.true(
                mode='exact',
                value=property_name,
                justification=[f'{cls.__name__} has a class-level exact connectedness classification for {property_name}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': cls.__name__},
            )
    for cls, features in KNOWN_FALSE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.false(
                mode='exact',
                value=property_name,
                justification=[f'{cls.__name__} has a class-level exact connectedness classification for {property_name}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': cls.__name__},
            )
    return analyze_connectedness(space, property_name)


def is_connected_infinite(space: Any) -> Result:
    return analyze_infinite_connectedness(space, 'connected')


def is_path_connected_infinite(space: Any) -> Result:
    return analyze_infinite_connectedness(space, 'path_connected')


def infinite_connectedness_report(space: Any) -> dict[str, Result]:
    return {
        'connected': is_connected_infinite(space),
        'path_connected': is_path_connected_infinite(space),
    }
