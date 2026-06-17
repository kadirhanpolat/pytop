"""Known-answer tests for the constructive knot/link invariants."""

from __future__ import annotations

from fractions import Fraction

from pytop import (
    KnotDiagram,
    Laurent,
    alexander_polynomial_from_braid,
    is_valid_pd_code,
    jones_polynomial,
    kauffman_bracket,
    linking_number,
    writhe,
)
from pytop.knots import get_knot_profiles


def _laurent(terms: dict[int, int]) -> Laurent:
    return Laurent({Fraction(k): v for k, v in terms.items()})


# Standard PD codes (Knot Atlas style)
TREFOIL_PD = [(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)]
FIGURE_EIGHT_PD = [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)]


def _trefoil():
    # right-handed trefoil in this module's convention (see module docstring)
    return KnotDiagram(TREFOIL_PD, signs=(-1, -1, -1))


def _figure_eight():
    return KnotDiagram(FIGURE_EIGHT_PD, signs=(1, -1, 1, -1))


# --------------------------------------------------------------------------
# Structural validity
# --------------------------------------------------------------------------

def test_pd_codes_are_well_formed():
    assert is_valid_pd_code(_trefoil())
    assert is_valid_pd_code(_figure_eight())


def test_writhe():
    assert writhe(_trefoil()) == -3
    assert writhe(_figure_eight()) == 0


# --------------------------------------------------------------------------
# Jones polynomial known answers
# --------------------------------------------------------------------------

def test_jones_unknot_is_one():
    # An unknot diagram with no crossings.
    unknot = KnotDiagram([], signs=())
    assert jones_polynomial(unknot) == Laurent.one()


def test_jones_trefoil():
    # right-handed trefoil: V = -t^-4 + t^-3 + t^-1
    assert jones_polynomial(_trefoil()) == _laurent({-4: -1, -3: 1, -1: 1})


def test_jones_figure_eight():
    # amphichiral: V = t^-2 - t^-1 + 1 - t + t^2
    assert jones_polynomial(_figure_eight()) == _laurent({-2: 1, -1: -1, 0: 1, 1: -1, 2: 1})


def test_kauffman_bracket_trefoil_powers():
    bracket = kauffman_bracket(_trefoil())
    # bracket of the trefoil: A^7 - A^3 - A^-5
    assert bracket == _laurent({7: 1, 3: -1, -5: -1})


# --------------------------------------------------------------------------
# Alexander polynomial via braid closure
# --------------------------------------------------------------------------

def test_alexander_trefoil():
    # trefoil = closure of sigma_1^3 in B_2 ; Delta = t - 1 + t^-1
    poly = alexander_polynomial_from_braid([1, 1, 1], 2)
    assert poly == _laurent({-1: 1, 0: -1, 1: 1})


def test_alexander_figure_eight():
    # figure-eight = closure of (sigma_1 sigma_2^-1)^2 in B_3 ; Delta = t - 3 + t^-1
    poly = alexander_polynomial_from_braid([1, -2, 1, -2], 3)
    assert poly == _laurent({-1: 1, 0: -3, 1: 1})


def test_alexander_unknot():
    poly = alexander_polynomial_from_braid([1], 2)
    assert poly == Laurent.one()


# --------------------------------------------------------------------------
# Linking number
# --------------------------------------------------------------------------

def test_linking_number_hopf():
    assert linking_number([1, 1]) == 1
    assert linking_number([-1, -1]) == -1


# --------------------------------------------------------------------------
# Cross-validate crossing numbers against the descriptive knots.py profiles
# --------------------------------------------------------------------------

def test_crossing_numbers_match_profiles():
    profiles = {p.key: p.crossing_count for p in get_knot_profiles()}
    assert _trefoil().crossing_number == profiles["trefoil_knot"]
    assert _figure_eight().crossing_number == profiles["figure_eight_knot"]
