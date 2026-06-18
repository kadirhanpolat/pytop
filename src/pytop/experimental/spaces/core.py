"""Computable topological spaces: the representation protocol and verdicts.

This is the architectural keystone for moving pytop's point-set topology from
"finite only" toward research grade. A :class:`Space` represents a topological
space by *finite data plus algorithms* — so finite spaces, finitely-presented
infinite spaces (cofinite, order, metric, ...) and opaque/oracle spaces all share
one interface, and generic algorithms target the interface rather than a concrete
class.

Honesty about decidability is a first-class contract: every predicate returns a
:class:`Verdict` that says whether the answer is **decided**, only
**semi-decidable**, **undecidable**, or a **heuristic** — never a silent guess.
Decided verdicts carry a *witness* (a separating pair of opens, a finite
subcover, a connecting path) or a *counterexample*.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Decidability(Enum):
    """How firmly a predicate's answer is established."""

    DECIDED = "decided"            # the value is proven (True or False)
    SEMI_DECIDABLE = "semi"        # verified one direction only (e.g. found a witness)
    UNDECIDABLE = "undecidable"    # not decidable from the representation
    HEURISTIC = "heuristic"        # best-effort, not a proof


class CarrierKind(Enum):
    """Cardinality class of a space's underlying point set."""

    FINITE = "finite"
    COUNTABLE = "countable"
    UNCOUNTABLE = "uncountable"


class NotEnumerableError(Exception):
    """Raised when a space's points cannot be enumerated (infinite carrier)."""


@dataclass(frozen=True)
class CardinalValue:
    """A cardinal number: a finite non-negative integer or a symbolic infinite cardinal.

    Follows the same honesty contract as :class:`Verdict`: the system reports
    ``unknown`` rather than guessing when a cardinal cannot be determined from
    the available representation.

    Attributes
    ----------
    finite : int or None
        The integer value when the cardinal is finite.
    symbol : str or None
        ``"ℵ₀"``, ``"𝔠"`` (= 2^ℵ₀), or ``"unknown"`` for infinite / undetermined.
    """

    finite: int | None = None
    symbol: str | None = None

    def __post_init__(self) -> None:
        if self.finite is None and self.symbol is None:
            raise ValueError("CardinalValue requires either finite or symbol.")
        if self.finite is not None and self.finite < 0:
            raise ValueError("finite cardinal must be non-negative.")

    @classmethod
    def of(cls, n: int) -> CardinalValue:
        return cls(finite=n)

    @classmethod
    def aleph_0(cls) -> CardinalValue:
        return cls(symbol="ℵ₀")

    @classmethod
    def continuum(cls) -> CardinalValue:
        return cls(symbol="𝔠")

    @classmethod
    def unknown(cls) -> CardinalValue:
        return cls(symbol="unknown")

    def is_finite_cardinal(self) -> bool:
        return self.finite is not None

    def __repr__(self) -> str:
        return str(self.finite) if self.finite is not None else (self.symbol or "unknown")

    def __str__(self) -> str:
        return repr(self)


@dataclass(frozen=True)
class Verdict:
    """The outcome of a topological predicate, with decidability and a witness.

    ``value`` is ``True`` / ``False`` when known, or ``None`` when not decided.
    ``witness`` justifies a ``True`` (e.g. separating opens); ``counterexample``
    justifies a ``False`` (e.g. an inseparable pair).
    """

    value: bool | None
    decidability: Decidability
    reason: str = ""
    witness: Any = None
    counterexample: Any = None

    @classmethod
    def true(cls, reason: str = "", witness: Any = None) -> Verdict:
        return cls(True, Decidability.DECIDED, reason, witness=witness)

    @classmethod
    def false(cls, reason: str = "", counterexample: Any = None) -> Verdict:
        return cls(False, Decidability.DECIDED, reason, counterexample=counterexample)

    @classmethod
    def undecidable(cls, reason: str = "") -> Verdict:
        return cls(None, Decidability.UNDECIDABLE, reason)

    @property
    def is_decided(self) -> bool:
        return self.decidability is Decidability.DECIDED

    def __bool__(self) -> bool:
        # Guard against `if verdict:` misuse — an undecided verdict is not truthy.
        return self.value is True


class Space(ABC):
    """A computable topological space.

    Concrete representations implement :meth:`contains` (point membership) and
    :meth:`point_separation` (can two points be separated by disjoint opens?).
    Finite/enumerable spaces also implement :meth:`points` and :meth:`open_sets`.
    Infinite spaces may override :meth:`certificate` to answer a whole-space
    property question from a construction-level theorem (e.g. "every metric space
    is Hausdorff").
    """

    name: str = "space"
    carrier_kind: CarrierKind = CarrierKind.FINITE
    # Provenance for constructed spaces (set by construction wrappers); ``None``
    # for base representations. The reasoning engine uses it for preservation.
    construction: Any = None

    @abstractmethod
    def contains(self, point: Any) -> bool:
        """Return whether ``point`` belongs to the carrier."""

    def is_finite(self) -> bool:
        return self.carrier_kind is CarrierKind.FINITE

    def points(self) -> Iterable[Any]:
        """Enumerate the carrier. Raises for non-enumerable spaces."""

        raise NotEnumerableError(f"{self.name!r} does not expose an enumerable carrier.")

    def open_sets(self) -> Iterable[Any]:
        """Enumerate the topology (open sets). Raises for non-enumerable spaces."""

        raise NotEnumerableError(f"{self.name!r} does not expose an enumerable topology.")

    def point_separation(self, x: Any, y: Any) -> Verdict:
        """Can the distinct points ``x`` and ``y`` be separated by disjoint opens?

        Default: undecidable. Representations override with their own logic.
        """

        return Verdict.undecidable(f"{self.name!r} cannot decide point separation.")

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        """Known cardinal invariant from a construction-level theorem.

        ``invariant`` is one of ``"weight"``, ``"density"``, ``"character"``,
        ``"cellularity"``. Returns ``None`` when the representation has no
        certificate (the generic engine then reports ``CardinalValue.unknown()``).
        Override in concrete infinite-space representations to supply the answer.
        """

        return None

    def certificate(self, prop: str) -> Verdict | None:
        """Whole-space answer for a property from a construction-level theorem.

        ``prop`` is a property key such as ``"T0"``, ``"T1"``, ``"T2"``,
        ``"regular"``, ``"normal"``, ``"compact"`` or ``"connected"``. Returns
        ``None`` when the representation has no certificate for it (the generic
        predicate then falls back to computation or reports undecidable). This is
        how a finitely-presented infinite space answers from the mathematics of
        its construction (e.g. "every metric space is normal").
        """

        return None


__all__ = [
    "CardinalValue",
    "Decidability",
    "CarrierKind",
    "NotEnumerableError",
    "Verdict",
    "Space",
]
