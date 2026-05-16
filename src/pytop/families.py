"""Families of sets, covers, refinements, and partitions.

This module provides a small explicit layer for the foundational chapters of
the book ecosystem. The goal is not abstract generality but clear, finite,
testable behavior for common classroom constructions.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from itertools import combinations
from typing import Any

from .sets import indexed_union


def normalize_family(family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> tuple[frozenset[Any], ...]:
    """Normalize a family to an ordered tuple of frozensets."""

    members = family.values() if isinstance(family, Mapping) else family
    return tuple(frozenset(member) for member in members)


def is_pairwise_disjoint_family(family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> bool:
    """Return whether every two distinct members are disjoint."""

    normalized = normalize_family(family)
    return all(left.isdisjoint(right) for left, right in combinations(normalized, 2))


def is_disjoint_family(family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> bool:
    """Alias for pairwise disjointness.

    In this project, foundational notes use “disjoint family” in the usual
    pairwise sense, so the alias keeps the public surface linguistically
    simple.
    """

    return is_pairwise_disjoint_family(family)


def is_cover(universe: Iterable[Any], family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> bool:
    """Return whether *family* covers *universe*."""

    universe_set = set(universe)
    return universe_set.issubset(indexed_union(family))


def is_subcover(
    universe: Iterable[Any],
    subfamily: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
    family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> bool:
    """Return whether *subfamily* is a subcover of *family* for *universe*."""

    normalized_sub = list(normalize_family(subfamily))
    normalized_family = list(normalize_family(family))
    return all(member in normalized_family for member in normalized_sub) and is_cover(universe, normalized_sub)


def is_refinement(
    candidate: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
    reference: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> bool:
    """Return whether every candidate member sits inside some reference member."""

    candidate_family = normalize_family(candidate)
    reference_family = normalize_family(reference)
    return all(any(member.issubset(container) for container in reference_family) for member in candidate_family)


def is_partition(universe: Iterable[Any], family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> bool:
    """Return whether *family* is a partition of *universe*."""

    normalized = normalize_family(family)
    if any(len(member) == 0 for member in normalized):
        return False
    return is_pairwise_disjoint_family(normalized) and indexed_union(normalized) == set(universe)


__all__ = [
    'normalize_family',
    'is_pairwise_disjoint_family',
    'is_disjoint_family',
    'is_cover',
    'is_subcover',
    'is_refinement',
    'is_partition',
]
