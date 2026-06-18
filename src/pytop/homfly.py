"""HOMFLY-PT polynomial via skein recursion on braid closures.

The HOMFLY-PT polynomial is the two-variable knot/link invariant ``P(a, z)``
defined by the skein relation

    a · P(L₊) − a⁻¹ · P(L₋) = z · P(L₀),     P(unknot) = 1,

where ``L₊`` and ``L₋`` differ by a single crossing change and ``L₀`` is the
oriented (Seifert) smoothing of that crossing.  It specialises to the Jones
polynomial via ``(a, z) ↦ (t⁻¹, t^½ − t^−½)`` and to the (Conway-normalised)
Alexander polynomial via ``(a, z) ↦ (1, t^½ − t^−½)``.

This module computes ``P`` from a **braid word** — the closure of the braid —
because a braid carries a canonical downward orientation: every crossing is a
generator ``σᵢ^{±1}``, the oriented smoothing ``L₀`` is simply *deletion* of
that letter, and a crossing change is *negation* of the letter.

Algorithm
---------
We recurse on the skein relation, always resolving an *under-first* crossing of
a fixed traversal of the link:

* the **smoothing** branch deletes a letter → one fewer crossing;
* the **crossing-change** branch turns an under-first crossing into an
  over-first one → strictly lowers the *descending defect* ``μ`` (the number of
  crossings first met as the under-strand).

The over/under status of every *other* crossing is independent of the one we
flip, so a single switch lowers ``μ`` by exactly one.  When ``μ = 0`` the
diagram is *descending* and therefore an unlink; its value is ``δ^{c−1}`` for
``c`` components, with ``δ = (a − a⁻¹) / z``.  Termination follows from the
well-founded measure ``(crossing count, μ)`` ordered lexicographically.

Pure Python, exact integer arithmetic, no dependencies.  The recursion is
exponential in the crossing number in the worst case; it is intended for the
small diagrams of the knot tables, not large-scale computation.

Braid-word convention
----------------------
A braid word is a sequence of nonzero integers; ``+i`` is the generator
``σᵢ`` (a positive crossing) and ``−i`` is ``σᵢ⁻¹`` (a negative crossing),
where ``i`` is a 1-based strand index in ``1 ≤ i ≤ n−1``.  For a positive
generator the strand entering from the left (position ``i``) passes *over*.

Examples
--------
* closure of ``σ₁³`` on 2 strands → right-handed trefoil,
* closure of ``σ₁²`` on 2 strands → (positive) Hopf link,
* closure of ``σ₁ σ₂⁻¹ σ₁ σ₂⁻¹`` on 3 strands → figure-eight knot,
* empty word on ``n`` strands → ``n``-component unlink.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

from .knot_invariants import Laurent

__all__ = [
    "Laurent2",
    "homfly_polynomial",
]


# ---------------------------------------------------------------------------
# Two-variable Laurent polynomial in (a, z)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Laurent2:
    """A Laurent polynomial in two variables ``a`` and ``z``.

    Exponents are integers (possibly negative — this is a *Laurent* polynomial
    in both variables); coefficients are integers.  Stored sparsely as a dict
    mapping ``(exp_a, exp_z)`` to the coefficient; zero coefficients are
    dropped, so equality is structural.
    """

    coeffs: dict[tuple[int, int], int] = field(default_factory=dict)

    def __init__(self, coeffs: dict[tuple[int, int], int] | None = None) -> None:
        cleaned: dict[tuple[int, int], int] = {}
        for exponent, coefficient in (coeffs or {}).items():
            if coefficient == 0:
                continue
            exp_a, exp_z = exponent
            key = (int(exp_a), int(exp_z))
            cleaned[key] = cleaned.get(key, 0) + coefficient
        cleaned = {key: c for key, c in cleaned.items() if c != 0}
        object.__setattr__(self, "coeffs", cleaned)

    # -- constructors -------------------------------------------------------

    @classmethod
    def monomial(cls, exp_a: int, exp_z: int, coefficient: int = 1) -> Laurent2:
        return cls({(exp_a, exp_z): coefficient})

    @classmethod
    def zero(cls) -> Laurent2:
        return cls({})

    @classmethod
    def one(cls) -> Laurent2:
        return cls({(0, 0): 1})

    # -- ring operations ----------------------------------------------------

    def __add__(self, other: Laurent2) -> Laurent2:
        merged = dict(self.coeffs)
        for exponent, coefficient in other.coeffs.items():
            merged[exponent] = merged.get(exponent, 0) + coefficient
        return Laurent2(merged)

    def __sub__(self, other: Laurent2) -> Laurent2:
        return self + other.scaled(-1)

    def scaled(self, factor: int) -> Laurent2:
        return Laurent2({exp: c * factor for exp, c in self.coeffs.items()})

    def __mul__(self, other: Laurent2) -> Laurent2:
        product: dict[tuple[int, int], int] = {}
        for (a1, z1), c1 in self.coeffs.items():
            for (a2, z2), c2 in other.coeffs.items():
                key = (a1 + a2, z1 + z2)
                product[key] = product.get(key, 0) + c1 * c2
        return Laurent2(product)

    def __pow__(self, power: int) -> Laurent2:
        if power < 0:
            raise ValueError("Laurent2.__pow__ supports nonnegative integer powers only.")
        result = Laurent2.one()
        base = self
        for _ in range(power):
            result = result * base
        return result

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Laurent2) and self.coeffs == other.coeffs

    def __hash__(self) -> int:
        return hash(frozenset(self.coeffs.items()))

    def is_zero(self) -> bool:
        return not self.coeffs

    # -- specialisations ----------------------------------------------------

    def to_jones(self) -> Laurent:
        """Return the Jones polynomial ``V(t)`` via ``(a, z) ↦ (t⁻¹, t^½ − t^−½)``.

        Valid for diagrams whose HOMFLY-PT has only non-negative ``z`` powers
        (every knot, and any link whose value is a genuine polynomial in
        ``z``).  Raises :class:`ValueError` if a negative ``z`` power is
        present (e.g. a raw unlink value), where the substitution is a rational
        function rather than a Laurent polynomial.
        """

        return self._specialise(a_to_inverse_t=True)

    def to_alexander(self) -> Laurent:
        """Return the Conway-normalised Alexander polynomial ``Δ(t)`` via
        ``(a, z) ↦ (1, t^½ − t^−½)``.

        Subject to the same non-negative ``z``-power requirement as
        :meth:`to_jones`.
        """

        return self._specialise(a_to_inverse_t=False)

    def _specialise(self, *, a_to_inverse_t: bool) -> Laurent:
        if any(exp_z < 0 for (_, exp_z) in self.coeffs):
            raise ValueError(
                "specialisation requires non-negative z-powers; the value is a "
                "rational function in t (e.g. an unlink)."
            )
        z_in_t = Laurent({Fraction(1, 2): 1, Fraction(-1, 2): -1})
        result = Laurent.zero()
        for (exp_a, exp_z), coefficient in self.coeffs.items():
            a_factor = (
                Laurent.monomial(Fraction(-exp_a), coefficient)
                if a_to_inverse_t
                else Laurent.monomial(Fraction(0), coefficient)
            )
            result = result + a_factor * (z_in_t ** exp_z)
        return result

    # -- display ------------------------------------------------------------

    def __repr__(self) -> str:
        if not self.coeffs:
            return "0"
        terms = []
        for exp_a, exp_z in sorted(self.coeffs):
            terms.append(f"{self.coeffs[(exp_a, exp_z)]}*a^{exp_a}*z^{exp_z}")
        return " + ".join(terms)


# ---------------------------------------------------------------------------
# Skein-relation building blocks
# ---------------------------------------------------------------------------

# δ = (a − a⁻¹) / z  — value increment per extra unlink component.
_DELTA = Laurent2({(1, -1): 1, (-1, -1): -1})

# Skein coefficients (see module docstring):
#   positive crossing:  P(L₊) = a⁻² · P(L₋) + a⁻¹z · P(L₀)
#   negative crossing:  P(L₋) = a²  · P(L₊) − a z  · P(L₀)
_A_MINUS_2 = Laurent2({(-2, 0): 1})
_A_MINUS_1_Z = Laurent2({(-1, 1): 1})
_A_PLUS_2 = Laurent2({(2, 0): 1})
_A_PLUS_1_Z = Laurent2({(1, 1): 1})


def _delta_power(exponent: int) -> Laurent2:
    """Return ``δ^exponent`` (``exponent`` ≥ 0); ``δ⁰`` is the unit ``1``."""

    return _DELTA ** exponent


# ---------------------------------------------------------------------------
# Braid-closure traversal: component count + descending defect
# ---------------------------------------------------------------------------


def _braid_trace(word: list[int], n_strands: int) -> tuple[int, int, int | None]:
    """Traverse the closure of a braid word.

    Returns ``(num_components, defect, bad_index)`` where:

    * ``num_components`` — number of closed curves (cycles of the underlying
      strand permutation),
    * ``defect`` — number of crossings whose *first* visit, in this fixed
      traversal, is as the under-strand,
    * ``bad_index`` — the index in ``word`` of one such under-first crossing,
      or ``None`` when ``defect == 0``.

    The traversal order (and hence which strand reaches each crossing first)
    depends only on the strand permutation — the absolute generator indices —
    and is independent of the crossing signs.  Flipping the sign of a single
    crossing therefore flips only that crossing's over/under status.
    """

    crossings = len(word)
    # first_over[t] is True when crossing t is first met as the over-strand.
    first_over: dict[int, bool] = {}
    started = [False] * (n_strands + 1)
    num_components = 0

    for origin in range(1, n_strands + 1):
        if started[origin]:
            continue
        num_components += 1
        position = origin
        while True:
            started[position] = True
            current = position
            for index in range(crossings):
                pivot = abs(word[index])
                if current == pivot or current == pivot + 1:
                    entering_left = current == pivot
                    positive = word[index] > 0
                    over = entering_left if positive else (not entering_left)
                    if index not in first_over:
                        first_over[index] = over
                    current = pivot + 1 if current == pivot else pivot
                # otherwise the strand runs straight past this crossing
            position = current
            if position == origin:
                break

    defect = sum(1 for over in first_over.values() if not over)
    bad_index: int | None = None
    for index in range(crossings):
        if first_over.get(index) is False:
            bad_index = index
            break
    return num_components, defect, bad_index


# ---------------------------------------------------------------------------
# Skein recursion
# ---------------------------------------------------------------------------


def _skein(word: list[int], n_strands: int, memo: dict[tuple[int, ...], Laurent2]) -> Laurent2:
    key = tuple(word)
    cached = memo.get(key)
    if cached is not None:
        return cached

    components, defect, bad_index = _braid_trace(word, n_strands)

    if defect == 0:
        # Descending diagram → unlink with `components` components.
        result = _delta_power(components - 1)
    else:
        assert bad_index is not None  # defect > 0 guarantees a bad crossing
        positive_crossing = word[bad_index] > 0

        switched = list(word)
        switched[bad_index] = -switched[bad_index]
        smoothed = word[:bad_index] + word[bad_index + 1 :]

        value_switched = _skein(switched, n_strands, memo)
        value_smoothed = _skein(smoothed, n_strands, memo)

        if positive_crossing:
            # current = L₊ : P(L₊) = a⁻² P(L₋) + a⁻¹z P(L₀)
            result = _A_MINUS_2 * value_switched + _A_MINUS_1_Z * value_smoothed
        else:
            # current = L₋ : P(L₋) = a² P(L₊) − a z P(L₀)
            result = _A_PLUS_2 * value_switched - _A_PLUS_1_Z * value_smoothed

    memo[key] = result
    return result


def homfly_polynomial(braid_word: Any, n_strands: int) -> Laurent2:
    """Return the HOMFLY-PT polynomial of the closure of a braid word.

    Parameters
    ----------
    braid_word:
        A sequence of nonzero integers; ``+i`` is ``σᵢ`` and ``−i`` is
        ``σᵢ⁻¹`` (1-based strand index, ``1 ≤ |i| ≤ n_strands − 1``).
    n_strands:
        The number of braid strands ``n ≥ 1``.

    Returns
    -------
    Laurent2
        The HOMFLY-PT polynomial ``P(a, z)`` in the skein normalisation
        ``a·P(L₊) − a⁻¹·P(L₋) = z·P(L₀)`` with ``P(unknot) = 1``.

    Raises
    ------
    ValueError
        If ``n_strands < 1`` or a generator index is ``0`` or out of range.

    Examples
    --------
    >>> homfly_polynomial([], 1)            # unknot
    1*a^0*z^0
    >>> homfly_polynomial([1, 1, 1], 2)     # right-handed trefoil
    -1*a^-4*z^0 + 2*a^-2*z^0 + 1*a^-2*z^2
    """

    if n_strands < 1:
        raise ValueError("A braid needs at least one strand.")
    word = [int(letter) for letter in braid_word]
    for letter in word:
        if letter == 0 or abs(letter) >= n_strands:
            raise ValueError(
                f"Invalid braid generator {letter} for {n_strands} strands."
            )
    return _skein(word, n_strands, {})
