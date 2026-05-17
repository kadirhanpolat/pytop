"""Functions defined by rules (formulas).

Provides:
- ``MathFunction``  — function represented by a rule ``f: domain → codomain``
- ``function_from`` — constructor
- Structural tests  — is_injective_on, is_surjective_on, is_bijective_on
- Pre-built constants — successor, square, double, abs_value, negate_fn

Usage
-----
>>> square(4)
16
>>> square.restrict_to(range(5))
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
>>> double.compose(successor)(3)
8
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

from .predicate_sets import MathSet, N, R, Z


class PredicateFunctionError(ValueError):
    """Raised when a predicate-defined function operation fails."""


# ---------------------------------------------------------------------------
# MathFunction
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MathFunction:
    """A mathematical function defined by a rule.

    Unlike a plain ``dict``, a :class:`MathFunction` may operate on
    infinite domains (e.g. ℕ → ℕ).  :meth:`apply` evaluates the rule
    and validates that the result belongs to the codomain.

    Parameters
    ----------
    name:
        Human-readable name or formula (e.g. ``"x²"``).
    domain:
        Source :class:`MathSet`.
    codomain:
        Target :class:`MathSet`.
    rule:
        Callable ``rule(x)`` returning the image of *x*.
    description:
        Optional longer description.
    """

    name: str
    domain: MathSet
    codomain: MathSet
    rule: Callable[[Any], Any] = field(compare=False, hash=False, repr=False)
    description: str = ""

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def apply(self, x: Any) -> Any:
        """Return ``f(x)``.

        Raises
        ------
        PredicateFunctionError
            If *x* ∉ domain or ``rule(x)`` ∉ codomain.
        """
        if not self.domain.contains(x):
            raise PredicateFunctionError(
                f"{x!r} is not in domain {self.domain.name!r}."
            )
        result = self.rule(x)
        if not self.codomain.contains(result):
            raise PredicateFunctionError(
                f"Rule maps {x!r} → {result!r}, which is not in "
                f"codomain {self.codomain.name!r}."
            )
        return result

    def __call__(self, x: Any) -> Any:
        return self.apply(x)

    # ------------------------------------------------------------------
    # Materialisation
    # ------------------------------------------------------------------

    def restrict_to(self, elements: Iterable[Any]) -> dict[Any, Any]:
        """Return ``{x: f(x) for x in elements if x ∈ domain}``.

        Elements outside the domain are silently skipped; elements whose
        image is outside the codomain raise :exc:`PredicateFunctionError`.
        """
        return {x: self.apply(x) for x in elements if self.domain.contains(x)}

    # ------------------------------------------------------------------
    # Composition
    # ------------------------------------------------------------------

    def compose(self, other: MathFunction) -> MathFunction:
        """Return ``self ∘ other``: ``(self ∘ other)(x) = self(other(x))``.

        Requires ``other.codomain.name == self.domain.name``.

        Raises
        ------
        PredicateFunctionError
            If the codomain of *other* does not match the domain of *self*.
        """
        if other.codomain.name != self.domain.name:
            raise PredicateFunctionError(
                f"Cannot compose {self.name!r} ∘ {other.name!r}: "
                f"codomain of {other.name!r} is {other.codomain.name!r} "
                f"but domain of {self.name!r} is {self.domain.name!r}."
            )
        rule_self = self.rule
        rule_other = other.rule
        return MathFunction(
            name=f"({self.name} ∘ {other.name})",
            domain=other.domain,
            codomain=self.codomain,
            rule=lambda x: rule_self(rule_other(x)),
            description=f"Composition of {self.name} and {other.name}",
        )

    # ------------------------------------------------------------------
    # Structural tests (on finite samples)
    # ------------------------------------------------------------------

    def is_injective_on(self, elements: Iterable[Any]) -> bool:
        """Return True iff f is injective on *elements* (distinct values)."""
        elems = [x for x in elements if self.domain.contains(x)]
        images = [self.rule(x) for x in elems]
        return len(set(map(repr, images))) == len(images)

    def is_surjective_on(
        self,
        domain_elements: Iterable[Any],
        codomain_elements: Iterable[Any],
    ) -> bool:
        """Return True iff every element of *codomain_elements* is hit."""
        images = {
            repr(self.rule(x))
            for x in domain_elements
            if self.domain.contains(x)
        }
        return all(repr(y) in images for y in codomain_elements)

    def is_bijective_on(
        self,
        domain_elements: Iterable[Any],
        codomain_elements: Iterable[Any],
    ) -> bool:
        """Return True iff f is bijective on the given finite sets."""
        dom = [x for x in domain_elements if self.domain.contains(x)]
        cod = list(codomain_elements)
        return self.is_injective_on(dom) and self.is_surjective_on(dom, cod)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"{self.name}: {self.domain.name} → {self.codomain.name}"


# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------

def function_from(
    domain: MathSet,
    codomain: MathSet,
    rule: Callable[[Any], Any],
    name: str = "",
    description: str = "",
) -> MathFunction:
    """Return a :class:`MathFunction` from *domain* to *codomain* via *rule*.

    Parameters
    ----------
    domain:
        Source :class:`MathSet`.
    codomain:
        Target :class:`MathSet`.
    rule:
        A callable ``rule(x)`` returning the image of *x*.
    name:
        Human-readable name or formula (e.g. ``"x²"``).
    description:
        Optional description.

    Examples
    --------
    >>> cube = function_from(N, N, lambda x: x**3, name="x³")
    >>> cube(3)
    27
    """
    return MathFunction(
        name=name or f"f: {domain.name} → {codomain.name}",
        domain=domain,
        codomain=codomain,
        rule=rule,
        description=description,
    )


# ---------------------------------------------------------------------------
# Pre-built function constants
# ---------------------------------------------------------------------------

successor: MathFunction = function_from(
    N, N, lambda x: x + 1,
    name="succ",
    description="Successor function n ↦ n+1 on ℕ",
)

square: MathFunction = function_from(
    N, N, lambda x: x ** 2,
    name="x²",
    description="Square function n ↦ n² on ℕ",
)

double: MathFunction = function_from(
    Z, Z, lambda x: 2 * x,
    name="2x",
    description="Doubling function n ↦ 2n on ℤ",
)

abs_value: MathFunction = function_from(
    R, R, lambda x: abs(x),
    name="|x|",
    description="Absolute value function on ℝ",
)

negate_fn: MathFunction = function_from(
    R, R, lambda x: -x,
    name="-x",
    description="Negation function x ↦ -x on ℝ",
)


__all__ = [
    # Error
    "PredicateFunctionError",
    # Class
    "MathFunction",
    # Constructor
    "function_from",
    # Pre-built constants
    "successor", "square", "double", "abs_value", "negate_fn",
]
