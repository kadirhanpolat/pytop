"""Construction closure for finite spaces: subspace, product, sum, quotient.

Each construction consumes finite :class:`FiniteSpace` inputs and returns a
:class:`FiniteSpace`, so the generic predicates compose on constructed spaces
(e.g. a product of Hausdorff spaces can be *computed* and *checked* to be
Hausdorff). This is the finite case of the closure required for research-grade
point-set topology; infinite/Tychonoff closure via preservation theorems is a
later milestone (see ``docs/CAPABILITIES_AND_ROADMAP.md``).
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import combinations
from typing import Any

from .representations import FiniteSpace


def _close_under_unions(basis: Iterable[frozenset]) -> set[frozenset]:
    """Return all (finite) unions of basis elements, including the empty set."""

    opens: set[frozenset] = {frozenset()}
    opens.update(frozenset(b) for b in basis)
    changed = True
    while changed:
        changed = False
        current = list(opens)
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                union = current[i] | current[j]
                if union not in opens:
                    opens.add(union)
                    changed = True
    return opens


def subspace(space: FiniteSpace, subset: Iterable[Any], *, name: str | None = None) -> FiniteSpace:
    """Return the subspace topology on ``subset`` ⊆ carrier (opens are ``O ∩ A``)."""

    a = frozenset(subset)
    carrier = frozenset(space.points())
    if not a <= carrier:
        raise ValueError("subspace carrier must be a subset of the original carrier.")
    opens = {frozenset(o) & a for o in space.open_sets()}
    return FiniteSpace(name or f"{space.name}|A", a, opens)


def binary_product(a: FiniteSpace, b: FiniteSpace, *, name: str | None = None) -> FiniteSpace:
    """Return the product space ``a × b`` with the product topology."""

    carrier = [(x, y) for x in a.points() for y in b.points()]
    basis = [
        frozenset((x, y) for x in u for y in v)
        for u in a.open_sets()
        for v in b.open_sets()
    ]
    opens = _close_under_unions(basis)
    return FiniteSpace(name or f"{a.name}×{b.name}", carrier, opens)


def disjoint_sum(a: FiniteSpace, b: FiniteSpace, *, name: str | None = None) -> FiniteSpace:
    """Return the topological sum ``a ⊔ b`` (opens are ``U ⊔ V``)."""

    carrier = [(0, x) for x in a.points()] + [(1, y) for y in b.points()]
    opens = {
        frozenset([(0, x) for x in u] + [(1, y) for y in v])
        for u in a.open_sets()
        for v in b.open_sets()
    }
    return FiniteSpace(name or f"{a.name}⊔{b.name}", carrier, opens)


def quotient(
    space: FiniteSpace,
    partition: Iterable[Iterable[Any]],
    *,
    name: str | None = None,
) -> FiniteSpace:
    """Return the quotient space for a ``partition`` of the carrier.

    A set of blocks is open iff its preimage (the union of those blocks) is open
    in ``space`` — the quotient topology. Blocks are named by a representative.
    """

    blocks = [frozenset(block) for block in partition]
    carrier = frozenset(space.points())
    covered: set[Any] = set()
    for block in blocks:
        if not block:
            raise ValueError("partition blocks must be nonempty.")
        if covered & block:
            raise ValueError("partition blocks must be disjoint.")
        covered |= block
    if covered != carrier:
        raise ValueError("partition must cover the whole carrier.")

    rep_of_block = {min(block, key=repr): block for block in blocks}
    reps = list(rep_of_block)
    space_opens = {frozenset(o) for o in space.open_sets()}

    quotient_opens: list[frozenset] = []
    for size in range(len(reps) + 1):
        for chosen in combinations(reps, size):
            preimage = frozenset().union(*(rep_of_block[r] for r in chosen)) if chosen else frozenset()
            if preimage in space_opens:
                quotient_opens.append(frozenset(chosen))
    return FiniteSpace(name or f"{space.name}/~", reps, quotient_opens)


__all__ = [
    "subspace",
    "binary_product",
    "disjoint_sum",
    "quotient",
]
