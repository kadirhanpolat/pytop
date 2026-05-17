"""Sets defined by membership predicates (set comprehension).

Provides:
- ``MathSet``           — set represented by a predicate, not enumeration
- ``set_of``            — comprehension constructor: {x ∈ base : predicate(x)}
- Base set constants    — N, Z, Q, R, C, Sigma (and derived N_plus, Z_plus, R_plus)
- Word aliases          — natural_numbers, integers, rationals, reals, complex_numbers,
                          alphabet, positive_naturals, positive_integers, positive_reals

Usage
-----
>>> 5 in N
True
>>> evens = set_of(N, lambda n: n % 2 == 0, name="Even ℕ")
>>> 4 in evens
True
>>> evens.to_frozenset(range(10))
frozenset({0, 2, 4, 6, 8})
>>> N.sample(5)
[0, 1, 2, 3, 4]
"""

from __future__ import annotations

import string
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from fractions import Fraction
from random import Random
from typing import Any


class PredicateSetError(ValueError):
    """Raised when a predicate-defined set operation fails."""


# ---------------------------------------------------------------------------
# MathSet
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MathSet:
    """A mathematical set represented by a membership predicate.

    Unlike ``frozenset``, a ``MathSet`` may describe an infinite collection
    (e.g. ℝ, ℕ).  Membership is checked by calling *predicate*.  Explicit
    enumeration is not available; use :meth:`to_frozenset` to materialise a
    finite portion, or :meth:`sample` to draw representative elements.

    Parameters
    ----------
    name:
        Human-readable name shown in ``repr`` and error messages (e.g. ``"ℕ"``).
    description:
        Optional longer description.
    predicate:
        ``predicate(x)`` returns ``True`` iff *x* belongs to this set.
    _sample_fn:
        Optional sampler ``(n, seed) -> list[Any]`` that returns *n* elements
        belonging to this set.  Required for :meth:`sample`.
    """

    name: str
    description: str = ""
    predicate: Callable[[Any], bool] = field(
        default=lambda x: True,
        compare=False, hash=False, repr=False,
    )
    _sample_fn: Callable[[int, int | None], list[Any]] | None = field(
        default=None,
        compare=False, hash=False, repr=False,
    )

    # ------------------------------------------------------------------
    # Membership
    # ------------------------------------------------------------------

    def contains(self, x: Any) -> bool:
        """Return True iff *x* belongs to this set."""
        return bool(self.predicate(x))

    def __contains__(self, x: Any) -> bool:
        return self.contains(x)

    # ------------------------------------------------------------------
    # Comprehension
    # ------------------------------------------------------------------

    def where(
        self,
        predicate: Callable[[Any], bool],
        name: str = "",
        description: str = "",
    ) -> MathSet:
        """Return the subset ``{x ∈ self : predicate(x)}``.

        Parameters
        ----------
        predicate:
            Additional membership condition.
        name:
            Name for the resulting set (auto-generated if empty).
        description:
            Optional description.

        Examples
        --------
        >>> evens = N.where(lambda n: n % 2 == 0, name="Even ℕ")
        >>> 4 in evens
        True
        """
        outer_pred = self.predicate
        combined = lambda x: outer_pred(x) and predicate(x)  # noqa: E731
        auto_name = name or f"{{x ∈ {self.name} : P(x)}}"

        base_sampler = self._sample_fn

        def comprehension_sample(n: int, seed: int | None = None) -> list[Any]:
            if base_sampler is None:
                raise PredicateSetError(
                    f"Cannot sample from comprehension of {self.name}: "
                    "base set has no sampler."
                )
            rng = Random(seed)
            results: list[Any] = []
            batch_size = max(n * 10, 100)
            attempts = 0
            while len(results) < n and attempts < 20:
                candidates = base_sampler(batch_size, rng.randint(0, 2 ** 32))
                for x in candidates:
                    if predicate(x):
                        results.append(x)
                        if len(results) == n:
                            break
                attempts += 1
            return results[:n]

        return MathSet(
            name=auto_name,
            description=description,
            predicate=combined,
            _sample_fn=comprehension_sample,
        )

    # ------------------------------------------------------------------
    # Set operations
    # ------------------------------------------------------------------

    def intersection(self, other: MathSet) -> MathSet:
        """Return ``self ∩ other``."""
        p_self, p_other = self.predicate, other.predicate
        return MathSet(
            name=f"({self.name} ∩ {other.name})",
            predicate=lambda x: p_self(x) and p_other(x),
        )

    def union(self, other: MathSet) -> MathSet:
        """Return ``self ∪ other``."""
        p_self, p_other = self.predicate, other.predicate
        return MathSet(
            name=f"({self.name} ∪ {other.name})",
            predicate=lambda x: p_self(x) or p_other(x),
        )

    def complement_in(self, universe: MathSet) -> MathSet:
        """Return ``universe \\ self``."""
        p_self, p_universe = self.predicate, universe.predicate
        return MathSet(
            name=f"({universe.name} \\ {self.name})",
            predicate=lambda x: p_universe(x) and not p_self(x),
        )

    def __and__(self, other: MathSet) -> MathSet:
        return self.intersection(other)

    def __or__(self, other: MathSet) -> MathSet:
        return self.union(other)

    # ------------------------------------------------------------------
    # Materialisation
    # ------------------------------------------------------------------

    def to_frozenset(self, elements: Iterable[Any]) -> frozenset[Any]:
        """Return a frozenset of those *elements* that belong to this set.

        Examples
        --------
        >>> N.where(lambda n: n % 2 == 0).to_frozenset(range(10))
        frozenset({0, 2, 4, 6, 8})
        """
        return frozenset(x for x in elements if self.contains(x))

    def sample(self, n: int, seed: int | None = None) -> list[Any]:
        """Return a list of *n* elements belonging to this set.

        Requires that the set was constructed with a sampler.

        Raises
        ------
        PredicateSetError
            If no sampler is available.
        """
        if self._sample_fn is None:
            raise PredicateSetError(
                f"No sampler defined for {self.name!r}. "
                "Use to_frozenset(elements) to materialise a finite portion."
            )
        return self._sample_fn(n, seed)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return self.name


# ---------------------------------------------------------------------------
# Base set constants
# ---------------------------------------------------------------------------

def _z_sampler(n: int, seed: int | None = None) -> list[int]:
    rng = Random(seed)
    return [rng.randint(-max(n, 10), max(n, 10)) for _ in range(n)]


def _q_sampler(n: int, seed: int | None = None) -> list[Fraction]:
    rng = Random(seed)
    return [
        Fraction(rng.randint(-20, 20), rng.randint(1, 10))
        for _ in range(n)
    ]


def _r_sampler(n: int, seed: int | None = None) -> list[float]:
    rng = Random(seed)
    return [rng.uniform(-100.0, 100.0) for _ in range(n)]


def _c_sampler(n: int, seed: int | None = None) -> list[complex]:
    rng = Random(seed)
    return [
        complex(rng.uniform(-10.0, 10.0), rng.uniform(-10.0, 10.0))
        for _ in range(n)
    ]


N: MathSet = MathSet(
    name="ℕ",
    description="Natural numbers {0, 1, 2, ...}",
    predicate=lambda x: isinstance(x, int) and not isinstance(x, bool) and x >= 0,
    _sample_fn=lambda n, seed: list(range(n)),
)

Z: MathSet = MathSet(
    name="ℤ",
    description="Integers {..., -2, -1, 0, 1, 2, ...}",
    predicate=lambda x: isinstance(x, int) and not isinstance(x, bool),
    _sample_fn=_z_sampler,
)

Q: MathSet = MathSet(
    name="ℚ",
    description="Rational numbers",
    predicate=lambda x: isinstance(x, (Fraction,)) or (isinstance(x, int) and not isinstance(x, bool)),
    _sample_fn=_q_sampler,
)

R: MathSet = MathSet(
    name="ℝ",
    description="Real numbers (int, float, Fraction)",
    predicate=lambda x: isinstance(x, (int, float, Fraction)) and not isinstance(x, bool),
    _sample_fn=_r_sampler,
)

C: MathSet = MathSet(
    name="ℂ",
    description="Complex numbers",
    predicate=lambda x: (
        isinstance(x, (int, float, complex, Fraction)) and not isinstance(x, bool)
    ),
    _sample_fn=_c_sampler,
)

Sigma: MathSet = MathSet(
    name="Σ",
    description="Lowercase Latin alphabet {a, b, ..., z}",
    predicate=lambda x: isinstance(x, str) and len(x) == 1 and x in string.ascii_lowercase,
    _sample_fn=lambda n, seed: list(string.ascii_lowercase[:min(n, 26)]),
)

# Derived constants (built via comprehension)
N_plus: MathSet = N.where(lambda x: x > 0, name="ℕ⁺", description="Positive natural numbers")
Z_plus: MathSet = Z.where(lambda x: x > 0, name="ℤ⁺", description="Positive integers")
R_plus: MathSet = R.where(lambda x: x > 0, name="ℝ⁺", description="Positive real numbers")

# ---------------------------------------------------------------------------
# Word aliases
# ---------------------------------------------------------------------------

natural_numbers = N
integers = Z
rationals = Q
reals = R
complex_numbers = C
alphabet = Sigma
positive_naturals = N_plus
positive_integers = Z_plus
positive_reals = R_plus


# ---------------------------------------------------------------------------
# Comprehension constructor
# ---------------------------------------------------------------------------

def set_of(
    base: MathSet,
    predicate: Callable[[Any], bool],
    name: str = "",
    description: str = "",
) -> MathSet:
    """Return ``{x ∈ base : predicate(x)}`` as a :class:`MathSet`.

    This is an alias for ``base.where(predicate, name, description)``.

    Parameters
    ----------
    base:
        The ambient set to draw elements from.
    predicate:
        Membership condition.
    name:
        Optional name for the resulting set.
    description:
        Optional description.

    Examples
    --------
    >>> evens = set_of(N, lambda n: n % 2 == 0, name="Even ℕ")
    >>> evens.to_frozenset(range(10))
    frozenset({0, 2, 4, 6, 8})
    """
    return base.where(predicate, name=name, description=description)


__all__ = [
    # Error
    "PredicateSetError",
    # Class
    "MathSet",
    # Constructor
    "set_of",
    # Base sets (symbols)
    "N", "Z", "Q", "R", "C", "Sigma",
    "N_plus", "Z_plus", "R_plus",
    # Base sets (words)
    "natural_numbers", "integers", "rationals", "reals", "complex_numbers", "alphabet",
    "positive_naturals", "positive_integers", "positive_reals",
]
