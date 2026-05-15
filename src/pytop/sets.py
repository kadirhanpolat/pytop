"""Foundational set helpers for the early chapters of the ecosystem.

The functions in this module intentionally stay finite and explicit. They are
designed to support foundational exercises, notebooks, and tests involving
subsets, power sets, indexed families, complements relative to a fixed
universe, and elementary Cartesian products.
"""

from __future__ import annotations

from itertools import chain, combinations
from typing import Any, Iterable, Mapping


class SetOperationError(ValueError):
    """Raised when a foundational set operation receives invalid input."""


def normalize_set(values: Iterable[Any]) -> frozenset[Any]:
    """Return a frozenset view of *values*.

    The helper keeps the public surface consistent across modules and tests.
    """

    return frozenset(values)


def normalize_universe(universe: Iterable[Any]) -> frozenset[Any]:
    """Normalize a universe for complement-style operations."""

    return normalize_set(universe)


def equal_sets(left: Iterable[Any], right: Iterable[Any]) -> bool:
    """Return whether two iterables define the same set."""

    return normalize_set(left) == normalize_set(right)


def is_subset(subset: Iterable[Any], superset: Iterable[Any]) -> bool:
    """Return whether *subset* is contained in *superset*."""

    return normalize_set(subset).issubset(normalize_set(superset))


def is_proper_subset(subset: Iterable[Any], superset: Iterable[Any]) -> bool:
    """Return whether *subset* is a strict subset of *superset*."""

    left = normalize_set(subset)
    right = normalize_set(superset)
    return left < right


def power_set(values: Iterable[Any]) -> set[frozenset[Any]]:
    """Return the full power set of a finite iterable.

    The output is a set of ``frozenset`` blocks so it can itself be compared
    as a mathematical set.
    """

    items = tuple(dict.fromkeys(values))
    return {
        frozenset(combo)
        for r in range(len(items) + 1)
        for combo in combinations(items, r)
    }


def set_union(*sets_: Iterable[Any]) -> set[Any]:
    """Return the union of one or more iterables."""

    if not sets_:
        return set()
    return set().union(*(set(part) for part in sets_))


def set_intersection(*sets_: Iterable[Any]) -> set[Any]:
    """Return the intersection of one or more iterables.

    The empty intersection is treated as the empty set because no universe is
    provided.
    """

    if not sets_:
        return set()
    iterator = iter(sets_)
    result = set(next(iterator))
    for part in iterator:
        result &= set(part)
    return result


def set_difference(left: Iterable[Any], right: Iterable[Any]) -> set[Any]:
    r"""Return the relative complement ``left \ right``."""

    return set(left) - set(right)


def complement(subset: Iterable[Any], universe: Iterable[Any]) -> set[Any]:
    """Return the complement of *subset* inside *universe*."""

    subset_set = set(subset)
    universe_set = set(universe)
    if not subset_set.issubset(universe_set):
        raise SetOperationError("A complement can only be taken for a subset of the given universe.")
    return universe_set - subset_set


def cartesian_product(left: Iterable[Any], right: Iterable[Any]) -> set[tuple[Any, Any]]:
    """Return the Cartesian product ``left × right``."""

    left_items = tuple(left)
    right_items = tuple(right)
    return {(x, y) for x in left_items for y in right_items}


def indexed_union(family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> set[Any]:
    """Return the union of an indexed family.

    Both mappings and plain iterables of sets are accepted.
    """

    members = _family_members(family)
    return set(chain.from_iterable(members))


def indexed_intersection(family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> set[Any]:
    """Return the intersection of an indexed family.

    Without a fixed universe, the intersection of the empty family is taken
    to be the empty set.
    """

    members = [set(member) for member in _family_members(family)]
    if not members:
        return set()
    result = members[0].copy()
    for member in members[1:]:
        result &= member
    return result


def are_disjoint(left: Iterable[Any], right: Iterable[Any]) -> bool:
    """Return whether two sets are disjoint."""

    return set(left).isdisjoint(set(right))


def _family_members(family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]]) -> list[Iterable[Any]]:
    if isinstance(family, Mapping):
        return list(family.values())
    return list(family)


__all__ = [
    'SetOperationError',
    'normalize_set',
    'normalize_universe',
    'equal_sets',
    'is_subset',
    'is_proper_subset',
    'power_set',
    'set_union',
    'set_intersection',
    'set_difference',
    'complement',
    'cartesian_product',
    'indexed_union',
    'indexed_intersection',
    'are_disjoint',
]
