"""Finite order and lattice helpers.

The focus of this module is deliberately modest: it provides usable exact tools
for finite posets, especially those that arise from Alexandroff/order examples.
"""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Iterable
from typing import Any

from .alexandroff import is_partial_order, normalize_carrier, reflexive_transitive_closure
from .result import Result


class OrderLatticeError(ValueError):
    """Raised when an invalid order/lattice query is made."""


def _carrier_and_relation(obj: Any) -> tuple[tuple[Any, ...], set[tuple[Any, Any]]]:
    if hasattr(obj, "carrier") and hasattr(obj, "relation"):
        carrier = normalize_carrier(getattr(obj, "carrier"))
        relation = reflexive_transitive_closure(carrier, getattr(obj, "relation"))
        return carrier, relation
    if isinstance(obj, tuple) and len(obj) == 2:
        carrier, relation = obj
        carrier_tuple = normalize_carrier(carrier)
        relation_set = reflexive_transitive_closure(carrier_tuple, relation)
        return carrier_tuple, relation_set
    raise OrderLatticeError("Expected an order-space object or a (carrier, relation) pair.")


def leq(obj: Any, x: Any, y: Any) -> bool:
    carrier, relation = _carrier_and_relation(obj)
    if x not in carrier or y not in carrier:
        raise OrderLatticeError("Elements must belong to the carrier.")
    return (x, y) in relation


def lower_bounds(obj: Any, x: Any, y: Any) -> set[Any]:
    carrier, relation = _carrier_and_relation(obj)
    return {z for z in carrier if (z, x) in relation and (z, y) in relation}


def upper_bounds(obj: Any, x: Any, y: Any) -> set[Any]:
    carrier, relation = _carrier_and_relation(obj)
    return {z for z in carrier if (x, z) in relation and (y, z) in relation}


def maximal_elements(obj: Any, subset: Iterable[Any]) -> set[Any]:
    _, relation = _carrier_and_relation(obj)
    subset_set = set(subset)
    return {x for x in subset_set if not any(x != y and (x, y) in relation for y in subset_set)}


def minimal_elements(obj: Any, subset: Iterable[Any]) -> set[Any]:
    _, relation = _carrier_and_relation(obj)
    subset_set = set(subset)
    return {x for x in subset_set if not any(x != y and (y, x) in relation for y in subset_set)}


def meet(obj: Any, x: Any, y: Any) -> Any | None:
    lbs = lower_bounds(obj, x, y)
    maxima = maximal_elements(obj, lbs)
    if len(maxima) == 1:
        return next(iter(maxima))
    return None


def join(obj: Any, x: Any, y: Any) -> Any | None:
    ubs = upper_bounds(obj, x, y)
    minima = minimal_elements(obj, ubs)
    if len(minima) == 1:
        return next(iter(minima))
    return None


def is_lattice(obj: Any) -> Result:
    carrier, relation = _carrier_and_relation(obj)
    if not is_partial_order(carrier, relation):
        return Result.false(
            mode="exact",
            value="lattice",
            justification=["Lattice checks require a finite partial order; antisymmetry failed."],
            metadata={"carrier_size": len(carrier)},
        )
    for x in carrier:
        for y in carrier:
            m = meet((carrier, relation), x, y)
            j = join((carrier, relation), x, y)
            if m is None or j is None:
                return Result.false(
                    mode="exact",
                    value="lattice",
                    justification=[f"The pair ({x!r}, {y!r}) does not have both a unique meet and a unique join."],
                    metadata={"carrier_size": len(carrier), "failing_pair": (x, y), "meet": m, "join": j},
                )
    return Result.true(
        mode="exact",
        value="lattice",
        justification=["Every pair of elements has a unique meet and a unique join."],
        metadata={"carrier_size": len(carrier)},
    )


def covering_pairs(obj: Any) -> set[tuple[Any, Any]]:
    carrier, relation = _carrier_and_relation(obj)
    covers: set[tuple[Any, Any]] = set()
    for x, y in relation:
        if x == y:
            continue
        if not any(x != z and y != z and (x, z) in relation and (z, y) in relation for z in carrier):
            covers.add((x, y))
    return covers


def hasse_edges(obj: Any) -> set[tuple[Any, Any]]:
    return covering_pairs(obj)



def hasse_profile(obj: Any) -> dict[str, Any]:
    """Return a compact Hasse-diagram-oriented profile for a finite poset."""

    carrier, relation = _carrier_and_relation(obj)
    covers = covering_pairs((carrier, relation))
    return {
        'carrier_size': len(carrier),
        'carrier': carrier,
        'relation_size': len(relation),
        'cover_count': len(covers),
        'covers': sorted(covers, key=lambda pair: (repr(pair[0]), repr(pair[1]))),
        'linear_extension': linear_extension((carrier, relation)) if is_partial_order(carrier, relation) else None,
    }

def linear_extension(obj: Any) -> list[Any]:
    carrier, relation = _carrier_and_relation(obj)
    if not is_partial_order(carrier, relation):
        raise OrderLatticeError("Linear extensions require a finite partial order.")
    covers = covering_pairs((carrier, relation))
    outgoing: dict[Any, set[Any]] = defaultdict(set)
    indegree: dict[Any, int] = {x: 0 for x in carrier}
    for x, y in covers:
        outgoing[x].add(y)
        indegree[y] += 1
    queue = deque(sorted((x for x in carrier if indegree[x] == 0), key=repr))
    result: list[Any] = []
    while queue:
        x = queue.popleft()
        result.append(x)
        for y in sorted(outgoing[x], key=repr):
            indegree[y] -= 1
            if indegree[y] == 0:
                queue.append(y)
    if len(result) != len(carrier):
        raise OrderLatticeError("Failed to compute a linear extension.")
    return result


__all__ = [
    "OrderLatticeError",
    "leq",
    "lower_bounds",
    "upper_bounds",
    "minimal_elements",
    "maximal_elements",
    "meet",
    "join",
    "is_lattice",
    "covering_pairs",
    "hasse_edges",
    "hasse_profile",
    "linear_extension",
]
