"""Unified subspace constructions.

Finite spaces are handled exactly by intersecting the ambient topology with the
chosen subset. Infinite and symbolic spaces are delegated to the symbolic
construction layer while preserving stable tags and metadata.
"""

from __future__ import annotations

from typing import Any, Iterable

from .finite_spaces import FiniteTopologicalSpace
from .infinite_constructions import subspace as infinite_subspace


def subspace(space: Any, subset: Iterable[Any] | Any, *, closed: bool = False, open: bool = False, dense: bool = False, metadata: dict[str, Any] | None = None):
    metadata = dict(metadata or {})
    if _space_is_finite(space) and hasattr(space, 'topology'):
        subset_set = set(subset)
        topology = {frozenset(set(U) & subset_set) for U in getattr(space, 'topology', ())}
        finite = FiniteTopologicalSpace(
            carrier=tuple(x for x in getattr(space, 'carrier', ()) if x in subset_set),
            topology=[set(U) for U in sorted(topology, key=lambda s: (len(s), tuple(sorted(map(repr, s)))))],
            metadata={
                **getattr(space, 'metadata', {}),
                **metadata,
                'representation': 'finite',
                'construction': 'subspace',
                'description': metadata.get('description', f'Finite subspace of {getattr(space, "carrier", None)!r}.'),
            },
            tags=set(getattr(space, 'tags', set())),
        )
        if closed:
            finite.add_tags('closed_subspace')
        if open:
            finite.add_tags('open_subspace')
        if dense:
            finite.add_tags('dense_subspace')
        return finite
    return infinite_subspace(space, subset, closed=closed, open=open, dense=dense, metadata=metadata)


def finite_subspace(space: Any, subset: Iterable[Any], *, metadata: dict[str, Any] | None = None) -> FiniteTopologicalSpace:
    result = subspace(space, subset, metadata=metadata)
    if not isinstance(result, FiniteTopologicalSpace):
        raise TypeError('finite_subspace expected a finite ambient space.')
    return result


def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False


__all__ = ['subspace', 'finite_subspace']
