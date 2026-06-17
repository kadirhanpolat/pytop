"""Construction wrapper spaces that carry provenance for preservation reasoning.

Unlike the eager finite constructions in :mod:`constructions` (which materialize a
``FiniteSpace``), these wrappers record *how* a space was built — product, subspace,
sum, quotient of given operands — and work for **infinite** operands too. The
reasoning engine (:mod:`reasoning`) reads this provenance and applies
preservation theorems, so it can decide properties of constructed infinite spaces
without enumerating them.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from .core import CarrierKind, Space


@dataclass(frozen=True)
class Construction:
    """Provenance of a constructed space: a construction ``kind`` and its operands."""

    kind: str
    operands: tuple[Space, ...]
    extra: Any = None


def _combined_kind(spaces: Iterable[Space]) -> CarrierKind:
    kinds = {s.carrier_kind for s in spaces}
    if CarrierKind.UNCOUNTABLE in kinds:
        return CarrierKind.UNCOUNTABLE
    if CarrierKind.COUNTABLE in kinds:
        return CarrierKind.COUNTABLE
    return CarrierKind.FINITE


class ProductSpace(Space):
    """The product of finitely many spaces (carries product provenance)."""

    def __init__(self, factors: Sequence[Space], name: str | None = None) -> None:
        factors = tuple(factors)
        if not factors:
            raise ValueError("a product needs at least one factor.")
        self._factors = factors
        self.name = name or "×".join(f.name for f in factors)
        self.carrier_kind = _combined_kind(factors)
        self.construction = Construction("product", factors)

    def contains(self, point: Any) -> bool:
        return (
            isinstance(point, tuple)
            and len(point) == len(self._factors)
            and all(f.contains(c) for f, c in zip(self._factors, point))
        )


class SumSpace(Space):
    """The topological sum (disjoint union) of finitely many spaces."""

    def __init__(self, summands: Sequence[Space], name: str | None = None) -> None:
        summands = tuple(summands)
        if not summands:
            raise ValueError("a sum needs at least one summand.")
        self._summands = summands
        self.name = name or "⊔".join(s.name for s in summands)
        self.carrier_kind = _combined_kind(summands)
        self.construction = Construction("sum", summands)

    def contains(self, point: Any) -> bool:
        if not (isinstance(point, tuple) and len(point) == 2):
            return False
        tag, value = point
        return 0 <= tag < len(self._summands) and self._summands[tag].contains(value)


class SubspaceSpace(Space):
    """A subspace of a parent space, carved out by a membership predicate."""

    def __init__(self, parent: Space, member: Callable[[Any], bool], name: str | None = None) -> None:
        self._parent = parent
        self._member = member
        self.name = name or f"{parent.name}|A"
        self.carrier_kind = parent.carrier_kind
        self.construction = Construction("subspace", (parent,))

    def contains(self, point: Any) -> bool:
        return self._parent.contains(point) and bool(self._member(point))


class QuotientSpace(Space):
    """A quotient of a parent space by an equivalence (recorded as provenance)."""

    def __init__(self, parent: Space, relation_name: str = "~", name: str | None = None) -> None:
        self._parent = parent
        self.name = name or f"{parent.name}/{relation_name}"
        self.carrier_kind = parent.carrier_kind
        self.construction = Construction("quotient", (parent,), relation_name)

    def contains(self, point: Any) -> bool:  # pragma: no cover - quotient points are classes
        return True


__all__ = [
    "Construction",
    "ProductSpace",
    "SumSpace",
    "SubspaceSpace",
    "QuotientSpace",
]
