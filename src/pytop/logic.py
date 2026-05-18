"""Propositional logic and quantifier helpers for foundational mathematics.

Provides `Proposition` (a labeled truth value), connective operations
(negate, conjunction, disjunction, implies, iff), and finite quantifiers
(for_all, there_exists, unique_exists).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Proposition:
    """A named propositional statement with a concrete truth value.

    Parameters
    ----------
    name:
        Human-readable label for the statement.
    truth_value:
        Boolean truth value of the statement.
    """

    name: str
    truth_value: bool

    def __bool__(self) -> bool:
        return self.truth_value

    def __repr__(self) -> str:
        return f"{self.name}={'T' if self.truth_value else 'F'}"


def negate(p: Proposition) -> Proposition:
    """Return ¬p."""
    return Proposition(f"¬({p.name})", not p.truth_value)


def conjunction(*props: Proposition) -> Proposition:
    """Return p₁ ∧ p₂ ∧ … (logical AND of all propositions)."""
    if not props:
        raise ValueError("conjunction requires at least one proposition.")
    name = " ∧ ".join(f"({q.name})" for q in props)
    return Proposition(name, all(bool(q) for q in props))


def disjunction(*props: Proposition) -> Proposition:
    """Return p₁ ∨ p₂ ∨ … (logical OR of all propositions)."""
    if not props:
        raise ValueError("disjunction requires at least one proposition.")
    name = " ∨ ".join(f"({q.name})" for q in props)
    return Proposition(name, any(bool(q) for q in props))


def implies(p: Proposition, q: Proposition) -> Proposition:
    """Return p → q  (equivalent to ¬p ∨ q)."""
    return Proposition(f"({p.name}) → ({q.name})", (not bool(p)) or bool(q))


def iff(p: Proposition, q: Proposition) -> Proposition:
    """Return p ↔ q  (equivalent to (p → q) ∧ (q → p))."""
    return Proposition(f"({p.name}) ↔ ({q.name})", bool(p) == bool(q))


def for_all(carrier: Iterable[Any], predicate: Callable[[Any], bool]) -> bool:
    """Return True iff predicate holds for every element of carrier (∀).

    Parameters
    ----------
    carrier:
        Finite iterable of elements to quantify over.
    predicate:
        A callable that returns a bool for each element.
    """
    return all(predicate(x) for x in carrier)


def there_exists(carrier: Iterable[Any], predicate: Callable[[Any], bool]) -> bool:
    """Return True iff predicate holds for at least one element of carrier (∃)."""
    return any(predicate(x) for x in carrier)


def unique_exists(carrier: Iterable[Any], predicate: Callable[[Any], bool]) -> bool:
    """Return True iff predicate holds for exactly one element of carrier (∃!)."""
    count = 0
    for x in carrier:
        if predicate(x):
            count += 1
            if count > 1:
                return False
    return count == 1


__all__ = [
    "Proposition",
    "negate",
    "conjunction",
    "disjunction",
    "implies",
    "iff",
    "for_all",
    "there_exists",
    "unique_exists",
]
