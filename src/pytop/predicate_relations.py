"""Relations defined by binary predicates.

Provides:
- ``MathRelation``      — relation represented by a predicate on two MathSets
- ``relation_on``       — homogeneous constructor: R ⊆ base × base
- ``relation_between``  — heterogeneous constructor: R ⊆ domain × codomain
- Structural tests      — is_reflexive_on, is_symmetric_on, is_transitive_on, ...
- Pre-built constants   — leq (≤), lt (<), geq (≥), gt (>), divides (∣)

Usage
-----
>>> leq.holds(2, 5)
True
>>> leq.restrict_to([1, 2, 3])
{(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)}
>>> divides.holds(3, 12)
True
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

from .predicate_sets import MathSet, N_plus, R


class PredicateRelationError(ValueError):
    """Raised when a predicate-defined relation operation fails."""


# ---------------------------------------------------------------------------
# MathRelation
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MathRelation:
    """A binary relation defined by a predicate over two :class:`MathSet`s.

    The relation ``R ⊆ domain × codomain`` holds for ``(x, y)`` iff
    ``x ∈ domain``, ``y ∈ codomain``, and ``predicate(x, y)`` is True.

    Parameters
    ----------
    name:
        Symbol or name (e.g. ``"≤"``, ``"∣"``).
    domain:
        Left-hand :class:`MathSet`.
    codomain:
        Right-hand :class:`MathSet`.
    predicate:
        ``predicate(x, y)`` returns True iff ``(x, y) ∈ R``.
    description:
        Optional longer description.
    """

    name: str
    domain: MathSet
    codomain: MathSet
    predicate: Callable[[Any, Any], bool] = field(
        compare=False, hash=False, repr=False,
    )
    description: str = ""

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def holds(self, x: Any, y: Any) -> bool:
        """Return True iff ``(x, y) ∈ R``.

        Checks that *x* ∈ domain and *y* ∈ codomain before applying the
        predicate; returns False (not an error) if either is out of range.
        """
        return (
            self.domain.contains(x)
            and self.codomain.contains(y)
            and bool(self.predicate(x, y))
        )

    def __call__(self, x: Any, y: Any) -> bool:
        return self.holds(x, y)

    # ------------------------------------------------------------------
    # Materialisation
    # ------------------------------------------------------------------

    def restrict_to(self, elements: Iterable[Any]) -> set[tuple[Any, Any]]:
        """Return ``{(x, y) : x, y ∈ elements and (x,y) ∈ R}``."""
        elems = list(elements)
        return {(x, y) for x in elems for y in elems if self.holds(x, y)}

    def restrict_between(
        self,
        domain_elements: Iterable[Any],
        codomain_elements: Iterable[Any],
    ) -> set[tuple[Any, Any]]:
        """Return ``{(x, y) : x ∈ dom_elems, y ∈ cod_elems, (x,y) ∈ R}``."""
        dom = list(domain_elements)
        cod = list(codomain_elements)
        return {(x, y) for x in dom for y in cod if self.holds(x, y)}

    # ------------------------------------------------------------------
    # Derived relations
    # ------------------------------------------------------------------

    def inverse(self) -> MathRelation:
        """Return the inverse relation R⁻¹ where (y,x) ∈ R⁻¹ iff (x,y) ∈ R."""
        pred = self.predicate
        return MathRelation(
            name=f"{self.name}⁻¹",
            domain=self.codomain,
            codomain=self.domain,
            predicate=lambda y, x: pred(x, y),
            description=f"Inverse of {self.name}",
        )

    def compose(self, other: MathRelation) -> MathRelation:
        """Return ``other ∘ self``: ``(x, z)`` holds iff ``∃y: self(x,y) ∧ other(y,z)``.

        The intermediate set is ``self.codomain`` (= ``other.domain``).
        The predicate does a pointwise existential check: it requires a
        sample from the intermediate set to be provided via
        ``restrict_to`` or checked by the caller.

        Note: the composed predicate is **not** closed-form — it raises
        ``PredicateRelationError`` when called unless a finite intermediate
        set can be derived from the domain sampler.
        """
        if self.codomain.name != other.domain.name:
            raise PredicateRelationError(
                f"Cannot compose: codomain of {self.name!r} ({self.codomain.name}) "
                f"does not match domain of {other.name!r} ({other.domain.name})."
            )
        mid = self.codomain
        pred_self = self.predicate
        pred_other = other.predicate

        def composed_pred(x: Any, z: Any) -> bool:
            if mid._sample_fn is None:
                raise PredicateRelationError(
                    f"Composition of {self.name} ∘ {other.name} requires a sampler "
                    f"on the intermediate set {mid.name!r}."
                )
            intermediates = mid._sample_fn(200, None)
            return any(
                mid.contains(y) and pred_self(x, y) and pred_other(y, z)
                for y in intermediates
            )

        return MathRelation(
            name=f"({other.name} ∘ {self.name})",
            domain=self.domain,
            codomain=other.codomain,
            predicate=composed_pred,
            description=f"Composition of {self.name} and {other.name}",
        )

    # ------------------------------------------------------------------
    # Structural tests (on finite sample)
    # ------------------------------------------------------------------

    def is_reflexive_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is reflexive on *elements*: ∀x, (x,x) ∈ R."""
        return all(self.holds(x, x) for x in elements)

    def is_symmetric_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is symmetric on *elements*: (x,y) → (y,x)."""
        elems = list(elements)
        return all(
            self.holds(y, x)
            for x in elems for y in elems
            if self.holds(x, y)
        )

    def is_transitive_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is transitive on *elements*."""
        elems = list(elements)
        return all(
            self.holds(x, z)
            for x in elems for y in elems for z in elems
            if self.holds(x, y) and self.holds(y, z)
        )

    def is_antisymmetric_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is antisymmetric on *elements*: (x,y)∧(y,x) → x=y."""
        elems = list(elements)
        return all(
            x == y
            for x in elems for y in elems
            if self.holds(x, y) and self.holds(y, x)
        )

    def is_partial_order_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is a partial order (reflexive + antisymmetric + transitive)."""
        elems = list(elements)
        return (
            self.is_reflexive_on(elems)
            and self.is_antisymmetric_on(elems)
            and self.is_transitive_on(elems)
        )

    def is_total_order_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is a total order (partial order + totality)."""
        elems = list(elements)
        return self.is_partial_order_on(elems) and all(
            self.holds(x, y) or self.holds(y, x)
            for x in elems for y in elems
        )

    def is_equivalence_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff R is an equivalence (reflexive + symmetric + transitive)."""
        elems = list(elements)
        return (
            self.is_reflexive_on(elems)
            and self.is_symmetric_on(elems)
            and self.is_transitive_on(elems)
        )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.name}: {self.domain.name} × {self.codomain.name}"


# ---------------------------------------------------------------------------
# Constructors
# ---------------------------------------------------------------------------

def relation_on(
    base: MathSet,
    predicate: Callable[[Any, Any], bool],
    name: str = "",
    description: str = "",
) -> MathRelation:
    """Return the homogeneous relation ``{(x,y) ∈ base² : predicate(x,y)}``.

    Parameters
    ----------
    base:
        The single underlying :class:`MathSet` (domain == codomain).
    predicate:
        Binary predicate determining membership.
    name:
        Relation symbol or name.
    description:
        Optional description.

    Examples
    --------
    >>> even_sum = relation_on(N, lambda x, y: (x + y) % 2 == 0, name="even-sum")
    >>> even_sum.holds(2, 4)
    True
    """
    return MathRelation(
        name=name or f"R ⊆ {base.name}²",
        domain=base,
        codomain=base,
        predicate=predicate,
        description=description,
    )


def relation_between(
    domain: MathSet,
    codomain: MathSet,
    predicate: Callable[[Any, Any], bool],
    name: str = "",
    description: str = "",
) -> MathRelation:
    """Return the heterogeneous relation ``{(x,y) ∈ domain × codomain : predicate(x,y)}``.

    Parameters
    ----------
    domain:
        Left-hand :class:`MathSet`.
    codomain:
        Right-hand :class:`MathSet`.
    predicate:
        Binary predicate determining membership.
    name:
        Relation symbol or name.
    description:
        Optional description.
    """
    return MathRelation(
        name=name or f"R ⊆ {domain.name} × {codomain.name}",
        domain=domain,
        codomain=codomain,
        predicate=predicate,
        description=description,
    )


# ---------------------------------------------------------------------------
# Pre-built relation constants
# ---------------------------------------------------------------------------

leq: MathRelation = relation_on(
    R, lambda x, y: x <= y,
    name="≤",
    description="Less-than-or-equal on ℝ",
)

lt: MathRelation = relation_on(
    R, lambda x, y: x < y,
    name="<",
    description="Strict less-than on ℝ",
)

geq: MathRelation = relation_on(
    R, lambda x, y: x >= y,
    name="≥",
    description="Greater-than-or-equal on ℝ",
)

gt: MathRelation = relation_on(
    R, lambda x, y: x > y,
    name=">",
    description="Strict greater-than on ℝ",
)

divides: MathRelation = relation_on(
    N_plus, lambda x, y: y % x == 0,
    name="∣",
    description="Divisibility on ℕ⁺: x ∣ y iff y mod x = 0",
)


__all__ = [
    # Error
    "PredicateRelationError",
    # Class
    "MathRelation",
    # Constructors
    "relation_on",
    "relation_between",
    # Pre-built constants
    "leq", "lt", "geq", "gt", "divides",
]
