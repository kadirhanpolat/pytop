"""Known-answer and invariance tests for the HOMFLY-PT polynomial.

The HOMFLY-PT polynomial ``P(a, z)`` is computed from a braid word via the
skein relation ``a·P(L₊) − a⁻¹·P(L₋) = z·P(L₀)`` with ``P(unknot) = 1``.

Test strategy
-------------
1. **Known answers** — unknot, unlinks, Hopf link, trefoil, figure-eight
   against the standard ``(a, z)`` HOMFLY-PT values.
2. **Specialisation differential** — ``a = t⁻¹`` reproduces pytop's Jones
   polynomial; ``a = 1`` reproduces pytop's braid Alexander polynomial.
3. **Invariance** — Markov stabilisation (±) and braid conjugation leave the
   closure's HOMFLY-PT unchanged, certifying it is a genuine link invariant.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from pytop import (
    KnotDiagram,
    Laurent2,
    alexander_polynomial_from_braid,
    homfly_polynomial,
    jones_polynomial,
)
from pytop.knot_invariants import _normalize_alexander


def _l2(terms: dict[tuple[int, int], int]) -> Laurent2:
    return Laurent2(terms)


# Standard braid words (closure = the named link).
TREFOIL = ([1, 1, 1], 2)            # right-handed trefoil 3_1
MIRROR_TREFOIL = ([-1, -1, -1], 2)  # left-handed trefoil (mirror)
FIGURE_EIGHT = ([1, -2, 1, -2], 3)  # amphichiral 4_1
HOPF_POS = ([1, 1], 2)              # positive Hopf link

# pytop's PD-code trefoil (right-handed per its own docstring).
TREFOIL_PD = KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))


# ---------------------------------------------------------------------------
# Laurent2 algebra
# ---------------------------------------------------------------------------


class TestLaurent2Algebra:
    def test_zero_and_one(self):
        assert Laurent2.zero().is_zero()
        assert Laurent2.one() == _l2({(0, 0): 1})

    def test_addition_collects_like_terms(self):
        # Arrange
        left = _l2({(1, 0): 1, (0, 1): 2})
        right = _l2({(1, 0): 3})
        # Act
        total = left + right
        # Assert
        assert total == _l2({(1, 0): 4, (0, 1): 2})

    def test_zero_coefficients_are_dropped(self):
        assert _l2({(1, 0): 1, (2, 0): 0}) == _l2({(1, 0): 1})

    def test_subtraction_cancels(self):
        poly = _l2({(3, -2): 5, (0, 0): 1})
        assert (poly - poly).is_zero()

    def test_multiplication_adds_exponents(self):
        # (a·z⁻¹)·(a⁻¹·z⁻¹) = z⁻²
        product = _l2({(1, -1): 1}) * _l2({(-1, -1): 1})
        assert product == _l2({(0, -2): 1})

    def test_power_of_delta(self):
        delta = _l2({(1, -1): 1, (-1, -1): -1})
        assert delta ** 0 == Laurent2.one()
        assert delta ** 2 == _l2({(2, -2): 1, (0, -2): -2, (-2, -2): 1})

    def test_negative_power_rejected(self):
        with pytest.raises(ValueError):
            _ = Laurent2.one() ** -1

    def test_equality_and_hash_are_structural(self):
        a = _l2({(1, 0): 1, (0, 1): 2})
        b = _l2({(0, 1): 2, (1, 0): 1})
        assert a == b
        assert hash(a) == hash(b)


# ---------------------------------------------------------------------------
# Known-answer HOMFLY-PT values
# ---------------------------------------------------------------------------


class TestKnownValues:
    def test_unknot_is_one(self):
        assert homfly_polynomial([], 1) == Laurent2.one()
        assert homfly_polynomial([1], 2) == Laurent2.one()       # closure of σ₁
        assert homfly_polynomial([-1], 2) == Laurent2.one()      # closure of σ₁⁻¹

    def test_two_component_unlink_is_delta(self):
        # δ = (a − a⁻¹)/z
        assert homfly_polynomial([], 2) == _l2({(1, -1): 1, (-1, -1): -1})

    def test_three_component_unlink_is_delta_squared(self):
        assert homfly_polynomial([], 3) == _l2({(2, -2): 1, (0, -2): -2, (-2, -2): 1})

    def test_positive_hopf_link(self):
        # P = a⁻¹z + (a⁻¹ − a⁻³)z⁻¹
        expected = _l2({(-1, 1): 1, (-1, -1): 1, (-3, -1): -1})
        assert homfly_polynomial(*HOPF_POS) == expected

    def test_right_handed_trefoil(self):
        # P = −a⁻⁴ + 2a⁻² + a⁻²z²
        expected = _l2({(-4, 0): -1, (-2, 0): 2, (-2, 2): 1})
        assert homfly_polynomial(*TREFOIL) == expected

    def test_figure_eight(self):
        # P = a² − 1 + a⁻² − z²   (amphichiral: symmetric under a ↦ a⁻¹)
        expected = _l2({(2, 0): 1, (0, 0): -1, (-2, 0): 1, (0, 2): -1})
        assert homfly_polynomial(*FIGURE_EIGHT) == expected

    def test_mirror_trefoil_is_a_inverse_of_trefoil(self):
        original = homfly_polynomial(*TREFOIL)
        mirror = homfly_polynomial(*MIRROR_TREFOIL)
        flipped = Laurent2({(-ea, ez): c for (ea, ez), c in original.coeffs.items()})
        assert mirror == flipped


# ---------------------------------------------------------------------------
# Specialisation differential tests
# ---------------------------------------------------------------------------


class TestSpecialisations:
    def test_mirror_trefoil_specialises_to_pytop_jones(self):
        # pytop's PD trefoil is right-handed; the σ₁³ closure is its mirror,
        # so the mirror braid reproduces pytop's Jones value exactly.
        jones_from_homfly = homfly_polynomial(*MIRROR_TREFOIL).to_jones()
        assert jones_from_homfly == jones_polynomial(TREFOIL_PD)

    def test_trefoil_specialises_to_alexander(self):
        alex = _normalize_alexander(homfly_polynomial(*TREFOIL).to_alexander())
        assert alex == alexander_polynomial_from_braid(*TREFOIL)

    def test_figure_eight_specialises_to_alexander(self):
        alex = _normalize_alexander(homfly_polynomial(*FIGURE_EIGHT).to_alexander())
        assert alex == alexander_polynomial_from_braid(*FIGURE_EIGHT)

    def test_figure_eight_jones_is_known(self):
        # V(4_1) = t² − t + 1 − t⁻¹ + t⁻²
        jones = homfly_polynomial(*FIGURE_EIGHT).to_jones()
        expected = {
            Fraction(2): 1,
            Fraction(1): -1,
            Fraction(0): 1,
            Fraction(-1): -1,
            Fraction(-2): 1,
        }
        assert jones.coeffs == expected

    def test_specialisation_rejects_negative_z_powers(self):
        # The raw 2-unlink value has a z⁻¹ term → not a Laurent polynomial in t.
        unlink = homfly_polynomial([], 2)
        with pytest.raises(ValueError):
            unlink.to_jones()
        with pytest.raises(ValueError):
            unlink.to_alexander()


# ---------------------------------------------------------------------------
# Link-invariance (Markov moves + conjugation)
# ---------------------------------------------------------------------------


class TestInvariance:
    def test_positive_markov_stabilisation(self):
        # closure(β in Bₙ) = closure(β·σₙ in Bₙ₊₁)
        assert homfly_polynomial([1, 1, 1], 2) == homfly_polynomial([1, 1, 1, 2], 3)

    def test_negative_markov_stabilisation(self):
        assert homfly_polynomial([1, 1, 1], 2) == homfly_polynomial([1, 1, 1, -2], 3)

    def test_conjugation_invariance(self):
        # closure(αβ) = closure(βα)
        assert homfly_polynomial([1, 1, 2, -1], 3) == homfly_polynomial([1, 2, -1, 1], 3)

    def test_reidemeister_two_cancellation(self):
        # Inserting σ₁σ₁⁻¹ is a Reidemeister-II move; the closure is unchanged.
        assert homfly_polynomial([1, 1, 1], 2) == homfly_polynomial([1, 1, 1, 1, -1], 2)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_zero_strands_rejected(self):
        with pytest.raises(ValueError):
            homfly_polynomial([], 0)

    def test_generator_out_of_range_rejected(self):
        with pytest.raises(ValueError):
            homfly_polynomial([2], 2)  # σ₂ needs ≥ 3 strands

    def test_zero_generator_rejected(self):
        with pytest.raises(ValueError):
            homfly_polynomial([0], 2)
