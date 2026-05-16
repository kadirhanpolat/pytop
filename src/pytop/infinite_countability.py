"""Structured countability analysis for supported infinite space families."""

from __future__ import annotations

from typing import Any

from .countability import analyze_countability, render_countability_report
from .infinite_spaces import (
    CocountableSpace,
    CofiniteSpace,
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
    InfiniteTopologicalSpace,
)
from .result import Result

KNOWN_TRUE = {
    DiscreteInfiniteSpace: {'first_countable'},
    IndiscreteInfiniteSpace: {'first_countable', 'second_countable', 'separable', 'lindelof'},
    CofiniteSpace: {'separable'},
    CocountableSpace: {'lindelof'},
}

KNOWN_FALSE = {
    CocountableSpace: {'first_countable', 'second_countable', 'separable'},
}


def analyze_infinite_countability(space: Any, property_name: str = 'first_countable') -> Result:
    if not isinstance(space, InfiniteTopologicalSpace):
        return analyze_countability(space, property_name)
    property_name = str(property_name).strip().lower().replace('-', '_').replace(' ', '_')
    if isinstance(space, DiscreteInfiniteSpace) and property_name in {'second_countable', 'separable', 'lindelof'}:
        if space.has_tag('countable'):
            return Result.true(
                mode='exact',
                value=property_name,
                justification=[f'Countable discrete spaces are exactly {property_name.replace("_", " ")}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': 'DiscreteInfiniteSpace'},
            )
        if space.has_tag('uncountable'):
            return Result.false(
                mode='exact',
                value=property_name,
                justification=[f'Uncountable discrete spaces fail {property_name.replace("_", " ")}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': 'DiscreteInfiniteSpace'},
            )
    if isinstance(space, CofiniteSpace) and property_name in {'first_countable', 'second_countable'}:
        if space.has_tag('countable'):
            return Result.true(
                mode='exact',
                value=property_name,
                justification=[f'Countable cofinite spaces are exactly {property_name.replace("_", " ")}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': 'CofiniteSpace'},
            )
        return Result.false(
            mode='exact',
            value=property_name,
            justification=[f'Uncountable cofinite spaces fail {property_name.replace("_", " ")}.'],
            metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': 'CofiniteSpace'},
        )
    for cls, features in KNOWN_TRUE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.true(
                mode='exact',
                value=property_name,
                justification=[f'{cls.__name__} has a class-level exact countability classification for {property_name}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': cls.__name__},
            )
    for cls, features in KNOWN_FALSE.items():
        if isinstance(space, cls) and property_name in features:
            return Result.false(
                mode='exact',
                value=property_name,
                justification=[f'{cls.__name__} has a class-level exact countability classification for {property_name}.'],
                metadata={'representation': space.metadata.get('representation'), 'property': property_name, 'source': cls.__name__},
            )
    return analyze_countability(space, property_name)


def is_first_countable_infinite(space: Any) -> Result:
    return analyze_infinite_countability(space, 'first_countable')


def is_second_countable_infinite(space: Any) -> Result:
    return analyze_infinite_countability(space, 'second_countable')


def is_separable_infinite(space: Any) -> Result:
    return analyze_infinite_countability(space, 'separable')


def is_lindelof_infinite(space: Any) -> Result:
    return analyze_infinite_countability(space, 'lindelof')


def infinite_countability_report(space: Any) -> dict[str, Result]:
    return {
        'first_countable': is_first_countable_infinite(space),
        'second_countable': is_second_countable_infinite(space),
        'separable': is_separable_infinite(space),
        'lindelof': is_lindelof_infinite(space),
    }


def render_infinite_countability_report(space: Any) -> str:
    report = infinite_countability_report(space)
    header = f"Infinite-space countability report for {space.__class__.__name__}"
    lines = [header, ""]
    for key in ('first_countable', 'second_countable', 'separable', 'lindelof'):
        result = report[key]
        status = 'yes' if result.is_true else 'no' if result.is_false else 'conditional' if result.is_conditional else 'unknown'
        suffix = f" ({result.mode})"
        source = str(result.metadata.get('source', '')).strip()
        if source:
            suffix += f" [{source}]"
        lines.append(f"- {key}: {status}{suffix}")
    lines.append("")
    lines.append("General report mirror:")
    lines.append(render_countability_report(space))
    return "\n".join(lines)


__all__ = [
    "KNOWN_TRUE",
    "KNOWN_FALSE",
    "analyze_infinite_countability",
    "is_first_countable_infinite",
    "is_second_countable_infinite",
    "is_separable_infinite",
    "is_lindelof_infinite",
    "infinite_countability_report",
    "render_infinite_countability_report",
]
