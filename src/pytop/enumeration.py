"""Enumeration helpers for finite topological spaces.

The current implementation focuses on small explicit finite carriers. This is
sufficient for examples, tests, and pedagogical generation, while keeping the
API honest about combinatorial growth.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable

from .finite_spaces import FiniteTopologicalSpace
from .separation import is_hausdorff, is_t0, is_t1



def enumerate_topologies(carrier: Iterable[Any]) -> list[FiniteTopologicalSpace]:
    points = tuple(carrier)
    subsets = _all_subsets(points)
    candidates = []
    for family_bits in range(1 << len(subsets)):
        family = [subsets[i] for i in range(len(subsets)) if family_bits & (1 << i)]
        family_sets = {frozenset(U) for U in family}
        if frozenset() not in family_sets or frozenset(points) not in family_sets:
            continue
        if _is_topology(family_sets):
            candidates.append(
                FiniteTopologicalSpace(
                    carrier=points,
                    topology=[set(U) for U in sorted(family_sets, key=lambda s: (len(s), tuple(sorted(map(repr, s)))))],
                    metadata={
                        "representation": "finite",
                        "construction": "enumerated",
                        "description": f"Enumerated finite topology on {len(points)} points.",
                    },
                    tags={"enumerated"},
                )
            )
    return candidates



def enumerate_topologies_on_n_points(n: int) -> list[FiniteTopologicalSpace]:
    if n < 0:
        raise ValueError("n must be nonnegative.")
    return enumerate_topologies(tuple(range(n)))



def enumerate_t0_topologies(carrier: Iterable[Any]) -> list[FiniteTopologicalSpace]:
    return [space for space in enumerate_topologies(carrier) if is_t0(space).is_true]



def enumerate_t1_topologies(carrier: Iterable[Any]) -> list[FiniteTopologicalSpace]:
    return [space for space in enumerate_topologies(carrier) if is_t1(space).is_true]



def enumerate_hausdorff_topologies(carrier: Iterable[Any]) -> list[FiniteTopologicalSpace]:
    return [space for space in enumerate_topologies(carrier) if is_hausdorff(space).is_true]



def count_topologies_on_n_points(n: int) -> int:
    return len(enumerate_topologies_on_n_points(n))



def _all_subsets(points: tuple[Any, ...]) -> list[frozenset[Any]]:
    subsets: list[frozenset[Any]] = []
    for size in range(len(points) + 1):
        for subset in combinations(points, size):
            subsets.append(frozenset(subset))
    return subsets



def _is_topology(family: set[frozenset[Any]]) -> bool:
    items = list(family)
    if frozenset() not in family:
        return False
    for left in items:
        for right in items:
            if left & right not in family:
                return False
            if left | right not in family:
                return False
    return True


__all__ = [
    "enumerate_topologies",
    "enumerate_topologies_on_n_points",
    "enumerate_t0_topologies",
    "enumerate_t1_topologies",
    "enumerate_hausdorff_topologies",
    "count_topologies_on_n_points",
]
