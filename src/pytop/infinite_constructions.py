"""Symbolic infinite-space constructions integrated with the `Result` model.

The functions in this module build supported symbolic spaces and propagate only
those properties that are stable under the named construction in a mathematically
standard way.
"""

from __future__ import annotations

from typing import Any

from .infinite_spaces import BasisDefinedSpace, InfiniteTopologicalSpace, MetricLikeSpace


def subspace(space: Any, subset_label: Any, *, closed: bool = False, open: bool = False, dense: bool = False, metadata: dict[str, Any] | None = None):
    metadata = dict(metadata or {})
    description = metadata.get('description', f'Subspace of {getattr(space, "carrier", "X")!r} determined by {subset_label!r}.')
    tags = _stable_subspace_tags(space)
    if closed:
        tags.add('closed_subspace')
    if open:
        tags.add('open_subspace')
    if dense:
        tags.add('dense_subspace')
    if _space_has(space, 'compact'):
        tags.add('ambient_compact')
    if _space_has(space, 'connected'):
        tags.add('ambient_connected')

    metadata.setdefault('description', description)
    metadata.setdefault('construction', 'subspace')
    metadata.setdefault('ambient_representation', getattr(space, 'metadata', {}).get('representation', 'symbolic_general'))
    metadata.setdefault('subset_label', subset_label)

    cls = _construction_class_for(space)
    return cls(
        carrier=subset_label,
        metadata={**metadata, 'tags': sorted(tags)},
        tags=tags,
    )


def product(*spaces: Any, metadata: dict[str, Any] | None = None):
    if not spaces:
        raise ValueError('product requires at least one space.')
    metadata = dict(metadata or {})
    tags: set[str] = set()
    carrier = tuple(getattr(space, 'carrier', None) for space in spaces)

    if all(_space_has(space, 'metric') for space in spaces):
        tags.add('metric')
    if all(_space_has(space, 't0') for space in spaces):
        tags.add('t0')
    if all(_space_has(space, 't1') for space in spaces):
        tags.add('t1')
    if all(_space_has(space, 'hausdorff') for space in spaces):
        tags.add('hausdorff')
    if all(_space_has(space, 'first_countable') for space in spaces):
        tags.add('first_countable')
    if all(_space_has(space, 'second_countable') for space in spaces):
        tags.add('second_countable')
    if all(_space_has(space, 'connected') for space in spaces):
        tags.add('connected')
    if all(_space_has(space, 'path_connected') for space in spaces):
        tags.add('path_connected')
    if all(_space_has(space, 'compact') for space in spaces):
        tags.add('compact')

    metadata.setdefault('description', 'Finite product of symbolic spaces.')
    metadata.setdefault('construction', 'product')
    metadata.setdefault('factor_representations', [getattr(space, 'metadata', {}).get('representation', 'symbolic_general') for space in spaces])
    cls = MetricLikeSpace if 'metric' in tags else InfiniteTopologicalSpace
    return cls(carrier=carrier, metadata={**metadata, 'tags': sorted(tags)}, tags=tags)


def disjoint_sum(*spaces: Any, metadata: dict[str, Any] | None = None):
    if not spaces:
        raise ValueError('disjoint_sum requires at least one space.')
    metadata = dict(metadata or {})
    tags: set[str] = set()
    carrier = tuple((i, getattr(space, 'carrier', None)) for i, space in enumerate(spaces))

    if len(spaces) > 1:
        tags.update({'not_connected', 'not_path_connected'})
    if all(_space_has(space, 'compact') for space in spaces):
        tags.add('compact')
    if all(_space_has(space, 'first_countable') for space in spaces):
        tags.add('first_countable')
    if all(_space_has(space, 'second_countable') for space in spaces):
        tags.add('second_countable')

    metadata.setdefault('description', 'Finite disjoint sum of symbolic spaces.')
    metadata.setdefault('construction', 'disjoint_sum')
    metadata.setdefault('summand_representations', [getattr(space, 'metadata', {}).get('representation', 'symbolic_general') for space in spaces])
    return InfiniteTopologicalSpace(carrier=carrier, metadata={**metadata, 'tags': sorted(tags)}, tags=tags)


def _stable_subspace_tags(space: Any) -> set[str]:
    stable = {'metric', 't0', 't1', 'hausdorff', 'first_countable', 'second_countable', 'separable', 'discrete', 'indiscrete'}
    return {tag for tag in getattr(space, 'tags', set()) if tag in stable}


def _construction_class_for(space: Any):
    if isinstance(space, MetricLikeSpace) or _space_has(space, 'metric'):
        return MetricLikeSpace
    if isinstance(space, BasisDefinedSpace):
        return BasisDefinedSpace
    return InfiniteTopologicalSpace


def _space_has(space: Any, tag: str) -> bool:
    return str(tag).strip().lower() in getattr(space, 'tags', set())


__all__ = ['subspace', 'product', 'disjoint_sum']
