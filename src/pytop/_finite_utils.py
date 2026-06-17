"""Shared finite-topology utility functions.

These pure-computation helpers (_sort_family, _powerset) were previously
duplicated across finite_operator_engine, finite_basis_engine, and filters.
They live here so a single fix propagates to all callers.

Return-type contract
--------------------
- ``_sort_family``  → ``tuple[frozenset[Any], ...]``
- ``_powerset``     → ``tuple[frozenset[Any], ...]``  (includes the empty set)
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import combinations
from typing import Any


def _sort_family(family: Iterable[frozenset[Any]]) -> tuple[frozenset[Any], ...]:
    """Return a deduplicated, canonically sorted tuple of frozensets.

    Sorting key: (size ascending, repr of sorted elements).
    """
    unique = set(family)
    return tuple(
        sorted(unique, key=lambda block: (len(block), tuple(map(repr, sorted(block, key=repr)))))
    )


def _powerset(carrier_set: frozenset[Any]) -> tuple[frozenset[Any], ...]:
    """Return all subsets of *carrier_set* as sorted frozensets (∅ included)."""
    points = sorted(carrier_set, key=repr)
    subsets: list[frozenset[Any]] = []
    for size in range(len(points) + 1):
        for combo in combinations(points, size):
            subsets.append(frozenset(combo))
    return tuple(subsets)


__all__ = ["_sort_family", "_powerset"]
