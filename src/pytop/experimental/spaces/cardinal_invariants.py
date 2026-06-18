"""Computed cardinal invariants for representable spaces.

Implements *computed* versions of the four classical cardinal functions:

* **weight** w(X) — minimum cardinality of a base.
* **density** d(X) — minimum cardinality of a dense subset.
* **character** χ(X) — supremum of minimum local-base sizes at each point.
* **cellularity** c(X) — supremum of cardinalities of pairwise-disjoint
  families of nonempty open sets.

For **finite spaces** every invariant is computed exactly from the topology
(using the enumerated open sets). For **infinite spaces** the answer comes
from ``space.cardinal_certificate(invariant)``; when no certificate is
available the honest result is :meth:`CardinalValue.unknown`.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any

from .core import CardinalValue, NotEnumerableError, Space

# --------------------------------------------------------------------------
# Internal helpers
# --------------------------------------------------------------------------

def _finite_topo(space: Space) -> tuple[list[Any], set[frozenset]]:
    pts = list(space.points())
    opens = {frozenset(o) for o in space.open_sets()}
    return pts, opens


def _is_base(candidate: set[frozenset], topology: set[frozenset]) -> bool:
    """True iff candidate is a base for topology."""
    for u in topology:
        if not u:
            continue
        for x in u:
            if not any(b for b in candidate if x in b and b <= u):
                return False
    return True


def _min_base_size(topology: set[frozenset]) -> int:
    non_empty = sorted(topology - {frozenset()}, key=lambda s: (len(s), sorted(map(repr, s))))
    for size in range(len(non_empty) + 1):
        for cand in combinations(non_empty, size):
            if _is_base(set(cand), topology):
                return size
    return len(non_empty)


def _min_dense_size(pts: list[Any], non_empty_opens: set[frozenset]) -> int:
    if not non_empty_opens:
        return 0
    for size in range(len(pts) + 1):
        for cand in combinations(pts, size):
            d = frozenset(cand)
            if all(d & o for o in non_empty_opens):
                return size
    return len(pts)


def _local_char_at(x: Any, opens: set[frozenset]) -> int:
    """Minimum local-base size at point x."""
    nbhds = [o for o in opens if x in o]
    for size in range(len(nbhds) + 1):
        for cand in combinations(nbhds, size):
            cl = list(cand)
            if all(any(b <= u for b in cl) for u in nbhds):
                return size
    return len(nbhds)


def _max_disjoint_size(opens: set[frozenset]) -> int:
    """Maximum pairwise-disjoint family of nonempty open sets."""
    non_empty = sorted(opens - {frozenset()}, key=lambda s: (len(s), sorted(map(repr, s))))
    for size in range(len(non_empty), 0, -1):
        for cand in combinations(non_empty, size):
            if all(not (a & b) for a, b in combinations(cand, 2)):
                return size
    return 0


def _from_certificate(space: Space, invariant: str) -> CardinalValue:
    cert = space.cardinal_certificate(invariant)
    return cert if cert is not None else CardinalValue.unknown()


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def weight(space: Space) -> CardinalValue:
    """w(X): minimum cardinality of a base for the topology.

    For finite spaces: the exact size of a smallest base is computed by
    checking subsets of the open sets in order of size (complete decision).
    For infinite spaces: uses ``space.cardinal_certificate("weight")``.

    Examples
    --------
    >>> from pytop.experimental.spaces import discrete_finite_space
    >>> from pytop.experimental.spaces.cardinal_invariants import weight
    >>> weight(discrete_finite_space({0, 1, 2}))
    3
    """
    if space.is_finite():
        try:
            _, opens = _finite_topo(space)
        except NotEnumerableError:
            return CardinalValue.unknown()
        return CardinalValue.of(_min_base_size(opens))
    return _from_certificate(space, "weight")


def density(space: Space) -> CardinalValue:
    """d(X): minimum cardinality of a dense subset.

    A subset D is dense iff every nonempty open set intersects D.
    For finite spaces: computed exactly.
    For infinite spaces: uses ``space.cardinal_certificate("density")``.

    Examples
    --------
    >>> from pytop.experimental.spaces import FiniteSpace
    >>> from pytop.experimental.spaces.cardinal_invariants import density
    >>> indiscrete = FiniteSpace("indiscrete", {0, 1, 2}, [set(), {0, 1, 2}])
    >>> density(indiscrete)  # any single point is dense
    1
    """
    if space.is_finite():
        try:
            pts, opens = _finite_topo(space)
        except NotEnumerableError:
            return CardinalValue.unknown()
        return CardinalValue.of(_min_dense_size(pts, opens - {frozenset()}))
    return _from_certificate(space, "density")


def character(space: Space) -> CardinalValue:
    """χ(X): supremum of minimum local-base sizes across all points.

    The character at a point x is the minimum cardinality of a local base
    (a neighbourhood base) at x. χ(X) = sup_{x ∈ X} χ(x, X).
    For finite spaces: computed exactly (max over all points).
    For infinite spaces: uses ``space.cardinal_certificate("character")``.

    Examples
    --------
    >>> from pytop.experimental.spaces import discrete_finite_space
    >>> from pytop.experimental.spaces.cardinal_invariants import character
    >>> character(discrete_finite_space({0, 1, 2}))
    1
    """
    if space.is_finite():
        try:
            pts, opens = _finite_topo(space)
        except NotEnumerableError:
            return CardinalValue.unknown()
        if not pts:
            return CardinalValue.of(0)
        return CardinalValue.of(max(_local_char_at(x, opens) for x in pts))
    return _from_certificate(space, "character")


def cellularity(space: Space) -> CardinalValue:
    """c(X): supremum of cardinalities of pairwise-disjoint families of nonempty opens.

    Also called the *Suslin number*. For finite spaces: computed exactly by
    finding the largest pairwise-disjoint family of nonempty open sets.
    For infinite spaces: uses ``space.cardinal_certificate("cellularity")``.

    Examples
    --------
    >>> from pytop.experimental.spaces import FiniteSpace
    >>> from pytop.experimental.spaces.cardinal_invariants import cellularity
    >>> space = FiniteSpace("chain3", {0,1,2}, [set(),{2},{1,2},{0,1,2}])
    >>> cellularity(space)
    1
    """
    if space.is_finite():
        try:
            _, opens = _finite_topo(space)
        except NotEnumerableError:
            return CardinalValue.unknown()
        return CardinalValue.of(_max_disjoint_size(opens))
    return _from_certificate(space, "cellularity")


__all__ = [
    "CardinalValue",
    "weight",
    "density",
    "character",
    "cellularity",
]
