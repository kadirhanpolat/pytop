"""Tests for the three extended Space representations:
ProductMetricSpace, LexicographicSquareSpace, CantorSpaceRepresentation.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from pytop.experimental.spaces import (
    CantorSpaceRepresentation,
    LexicographicSquareSpace,
    ProductMetricSpace,
    cantor_space,
    is_compact,
    is_connected,
    is_first_countable,
    is_hausdorff,
    is_lindelof,
    is_normal,
    is_regular,
    is_second_countable,
    is_separable,
    is_t0,
    is_t1,
    is_t5,
    is_t6,
    is_tychonoff,
    lexicographic_square,
    rational_plane,
)
from pytop.experimental.spaces.cardinal_invariants import (
    cellularity,
    character,
    density,
    weight,
)
from pytop.experimental.spaces.core import CardinalValue, Decidability


# ==========================================================================
# ProductMetricSpace
# ==========================================================================


class TestProductMetricSpace:

    def _q2(self) -> ProductMetricSpace:
        return rational_plane()

    # -- construction & membership ------------------------------------------

    def test_rational_plane_factory(self):
        q2 = rational_plane()
        assert q2.name == "Q²"

    def test_contains_rational_pairs(self):
        q2 = self._q2()
        assert q2.contains((Fraction(1, 2), Fraction(3, 4)))
        assert q2.contains((0, 0))
        assert q2.contains((1, -1))

    def test_does_not_contain_non_tuples(self):
        q2 = self._q2()
        assert not q2.contains(Fraction(1, 2))
        assert not q2.contains([0, 0])

    def test_does_not_contain_float_pair(self):
        q2 = self._q2()
        assert not q2.contains((0.5, 0.5))  # floats not in member_x

    def test_does_not_contain_wrong_length(self):
        q2 = self._q2()
        assert not q2.contains((0, 0, 0))

    # -- point separation ---------------------------------------------------

    def test_point_separation_horizontal(self):
        q2 = self._q2()
        v = q2.point_separation((0, 0), (1, 0))
        assert v.value is True
        assert v.decidability.value == "decided"
        radius = v.witness[0][1]
        assert radius == Fraction(1, 2)

    def test_point_separation_vertical(self):
        q2 = self._q2()
        v = q2.point_separation((0, 0), (0, 1))
        assert v.value is True
        radius = v.witness[0][1]
        assert radius == Fraction(1, 2)

    def test_point_separation_diagonal_uses_sup(self):
        q2 = self._q2()
        x = (Fraction(0), Fraction(0))
        y = (Fraction(3, 4), Fraction(1, 4))
        v = q2.point_separation(x, y)
        assert v.value is True
        # sup distance = max(3/4, 1/4) = 3/4; radius = 3/8
        assert v.witness[0][1] == Fraction(3, 8)

    # -- certificates -------------------------------------------------------

    def test_hausdorff(self):
        assert is_hausdorff(self._q2()).value is True

    def test_t0(self):
        assert is_t0(self._q2()).value is True

    def test_t1(self):
        assert is_t1(self._q2()).value is True

    def test_regular(self):
        assert is_regular(self._q2()).value is True

    def test_normal(self):
        assert is_normal(self._q2()).value is True

    def test_tychonoff(self):
        assert is_tychonoff(self._q2()).value is True

    def test_t5(self):
        assert is_t5(self._q2()).value is True

    def test_t6(self):
        assert is_t6(self._q2()).value is True

    def test_first_countable(self):
        assert is_first_countable(self._q2()).value is True

    def test_character_is_aleph0(self):
        c = character(self._q2())
        assert c == CardinalValue.aleph_0()

    def test_custom_product_space(self):
        # Integer lattice Z² with L∞ metric
        z2 = ProductMetricSpace(
            "Z²",
            distance_x=lambda a, b: Fraction(abs(a - b)),
            member_x=lambda p: isinstance(p, int),
            distance_y=lambda a, b: Fraction(abs(a - b)),
            member_y=lambda p: isinstance(p, int),
        )
        assert z2.contains((0, 0))
        assert z2.contains((-3, 7))
        assert not z2.contains((Fraction(1, 2), 0))
        v = z2.point_separation((0, 0), (1, 1))
        assert v.value is True
        assert v.witness[0][1] == Fraction(1, 2)

    def test_separation_witness_structure(self):
        q2 = self._q2()
        v = q2.point_separation((0, 0), (2, 0))
        pt, radius = v.witness[0]
        assert pt == (0, 0)
        assert radius == Fraction(1)


# ==========================================================================
# LexicographicSquareSpace
# ==========================================================================


class TestLexicographicSquareSpace:

    def _lex(self) -> LexicographicSquareSpace:
        return lexicographic_square()

    # -- construction & membership ------------------------------------------

    def test_factory(self):
        s = lexicographic_square()
        assert "lex" in s.name.lower()

    def test_contains_rational_pairs_in_unit_square(self):
        s = self._lex()
        assert s.contains((0, 0))
        assert s.contains((1, 1))
        assert s.contains((Fraction(1, 2), Fraction(3, 4)))

    def test_rejects_out_of_range(self):
        s = self._lex()
        assert not s.contains((Fraction(2), Fraction(0)))
        assert not s.contains((Fraction(-1), Fraction(0)))
        assert not s.contains((0, Fraction(3, 2)))

    def test_rejects_non_tuples(self):
        s = self._lex()
        assert not s.contains(Fraction(1, 2))
        assert not s.contains([0, 0])

    # -- point separation ---------------------------------------------------

    def test_separation_different_first_coord(self):
        s = self._lex()
        v = s.point_separation((Fraction(1, 4), Fraction(0)),
                                (Fraction(3, 4), Fraction(0)))
        assert v.value is True
        assert v.witness["split_first_coord"] == Fraction(1, 2)

    def test_separation_same_first_different_second(self):
        s = self._lex()
        v = s.point_separation((Fraction(1, 2), Fraction(1, 4)),
                                (Fraction(1, 2), Fraction(3, 4)))
        assert v.value is True
        assert v.witness["fiber_first_coord"] == Fraction(1, 2)
        assert v.witness["split_second_coord"] == Fraction(1, 2)

    def test_separation_close_first_coord(self):
        s = self._lex()
        a = Fraction(1, 3)
        b = a + Fraction(1, 100)
        v = s.point_separation((a, Fraction(0)), (b, Fraction(0)))
        assert v.value is True
        split = v.witness["split_first_coord"]
        assert a < split < b

    def test_separation_is_decided(self):
        s = self._lex()
        v = s.point_separation((0, 0), (1, 1))
        assert v.decidability == Decidability.DECIDED

    # -- separation axiom predicates ----------------------------------------

    def test_is_t0(self):
        assert is_t0(self._lex()).value is True

    def test_is_t1(self):
        assert is_t1(self._lex()).value is True

    def test_is_hausdorff(self):
        assert is_hausdorff(self._lex()).value is True

    def test_is_regular(self):
        assert is_regular(self._lex()).value is True

    def test_is_normal(self):
        assert is_normal(self._lex()).value is True

    def test_is_tychonoff(self):
        assert is_tychonoff(self._lex()).value is True

    def test_is_t5(self):
        assert is_t5(self._lex()).value is True

    def test_is_compact(self):
        assert is_compact(self._lex()).value is True

    def test_is_connected(self):
        assert is_connected(self._lex()).value is True

    def test_is_lindelof(self):
        assert is_lindelof(self._lex()).value is True

    def test_is_first_countable(self):
        assert is_first_countable(self._lex()).value is True

    def test_not_second_countable(self):
        v = is_second_countable(self._lex())
        assert v.value is False
        assert "fiber" in v.reason.lower() or "disjoint" in v.reason.lower()

    def test_not_separable(self):
        v = is_separable(self._lex())
        assert v.value is False

    # -- cardinal invariants ------------------------------------------------

    def test_character_is_aleph0(self):
        c = character(self._lex())
        assert c == CardinalValue.aleph_0()

    def test_cellularity_is_continuum(self):
        c = cellularity(self._lex())
        assert c == CardinalValue.continuum()

    # -- T6 is undecided for lex square -------------------------------------

    def test_t6_undecided(self):
        # The lex square has no T6 certificate — the predicate reports undecidable.
        v = is_t6(self._lex())
        assert v.value is None
        assert v.decidability == Decidability.UNDECIDABLE

    # -- counterexample witnesses in false certificates ---------------------

    def test_not_second_countable_has_counterexample(self):
        v = is_second_countable(self._lex())
        assert v.counterexample is not None

    def test_not_separable_has_counterexample(self):
        v = is_separable(self._lex())
        assert v.counterexample is not None


# ==========================================================================
# CantorSpaceRepresentation
# ==========================================================================


class TestCantorSpaceRepresentation:

    def _cantor(self) -> CantorSpaceRepresentation:
        return cantor_space()

    # -- construction & membership ------------------------------------------

    def test_factory(self):
        c = cantor_space()
        assert "cantor" in c.name.lower() or "0,1" in c.name

    def test_contains_binary_tuples(self):
        c = self._cantor()
        assert c.contains((0, 1, 0, 0))
        assert c.contains(())
        assert c.contains((1, 1, 1))

    def test_rejects_non_binary(self):
        c = self._cantor()
        assert not c.contains((0, 2, 1))
        assert not c.contains((0, -1))

    def test_rejects_non_tuples(self):
        c = self._cantor()
        assert not c.contains([0, 1])
        assert not c.contains("01")

    # -- point separation ---------------------------------------------------

    def test_separation_first_bit_differs(self):
        c = self._cantor()
        v = c.point_separation((0, 1), (1, 0))
        assert v.value is True
        assert v.witness["bit_position"] == 0
        assert v.witness["value"] == 0

    def test_separation_later_bit(self):
        c = self._cantor()
        v = c.point_separation((0, 0, 0), (0, 0, 1))
        assert v.value is True
        assert v.witness["bit_position"] == 2

    def test_separation_prefix_is_undecidable(self):
        c = self._cantor()
        v = c.point_separation((0, 1), (0, 1, 0))
        assert v.value is None
        assert v.decidability == Decidability.UNDECIDABLE

    def test_separation_same_prefix_undecidable(self):
        c = self._cantor()
        v = c.point_separation((1,), (1,))
        # Same finite prefix — cannot separate
        assert v.decidability == Decidability.UNDECIDABLE

    # -- separation axiom predicates ----------------------------------------

    def test_is_t0(self):
        assert is_t0(self._cantor()).value is True

    def test_is_t1(self):
        assert is_t1(self._cantor()).value is True

    def test_is_hausdorff(self):
        assert is_hausdorff(self._cantor()).value is True

    def test_is_regular(self):
        assert is_regular(self._cantor()).value is True

    def test_is_normal(self):
        assert is_normal(self._cantor()).value is True

    def test_is_tychonoff(self):
        assert is_tychonoff(self._cantor()).value is True

    def test_is_t5(self):
        assert is_t5(self._cantor()).value is True

    def test_is_t6(self):
        assert is_t6(self._cantor()).value is True

    def test_is_compact(self):
        assert is_compact(self._cantor()).value is True

    def test_is_not_connected(self):
        v = is_connected(self._cantor())
        assert v.value is False
        assert v.counterexample is not None

    def test_is_lindelof(self):
        assert is_lindelof(self._cantor()).value is True

    def test_is_separable(self):
        assert is_separable(self._cantor()).value is True

    def test_is_second_countable(self):
        assert is_second_countable(self._cantor()).value is True

    def test_is_first_countable(self):
        assert is_first_countable(self._cantor()).value is True

    # -- cardinal invariants ------------------------------------------------

    def test_weight_is_aleph0(self):
        assert weight(self._cantor()) == CardinalValue.aleph_0()

    def test_density_is_aleph0(self):
        assert density(self._cantor()) == CardinalValue.aleph_0()

    def test_character_is_aleph0(self):
        assert character(self._cantor()) == CardinalValue.aleph_0()

    def test_cellularity_is_aleph0(self):
        assert cellularity(self._cantor()) == CardinalValue.aleph_0()

    # -- counterexample & reason quality ------------------------------------

    def test_disconnected_has_counterexample(self):
        v = is_connected(self._cantor())
        assert "cylinder" in v.counterexample.lower() or "z[0]" in v.counterexample

    def test_separation_reason_names_cylinder(self):
        c = self._cantor()
        v = c.point_separation((0,), (1,))
        assert "cylinder" in v.reason.lower() or "C_0" in v.reason

    # -- custom CantorSpaceRepresentation -----------------------------------

    def test_custom_name(self):
        c = CantorSpaceRepresentation("my_cantor")
        assert c.name == "my_cantor"
        assert is_compact(c).value is True


# ==========================================================================
# Cross-representation comparisons
# ==========================================================================


class TestCrossRepresentationContrasts:
    """Mathematical contrasts that distinguish the three new representations."""

    def test_second_countability_contrasts(self):
        # Cantor space is second-countable (cylinder base)
        # Lex square is NOT second-countable
        # ProductMetricSpace has no generic second-countability certificate
        # (it depends on the factor spaces — left undecidable by design)
        assert is_second_countable(cantor_space()).value is True
        assert is_second_countable(lexicographic_square()).value is False
        q2_sc = is_second_countable(rational_plane())
        assert q2_sc.decidability == Decidability.UNDECIDABLE

    def test_lex_square_connected_cantor_not(self):
        assert is_connected(lexicographic_square()).value is True
        assert is_connected(cantor_space()).value is False

    def test_all_three_are_hausdorff(self):
        for sp in [rational_plane(), lexicographic_square(), cantor_space()]:
            assert is_hausdorff(sp).value is True

    def test_compact_status(self):
        # ℚ² is not compact (not bounded, or: open cover without finite subcover)
        # Lex square and Cantor space are compact
        q2_compact = is_compact(rational_plane())
        # ℚ² has no compact certificate → undecidable from this representation
        assert q2_compact.value is None or q2_compact.value is False
        assert is_compact(lexicographic_square()).value is True
        assert is_compact(cantor_space()).value is True

    def test_lex_square_not_separable_others_are(self):
        assert is_separable(lexicographic_square()).value is False
        assert is_separable(cantor_space()).value is True

    def test_t6_cantor_yes_lex_undecided(self):
        assert is_t6(cantor_space()).value is True
        v_lex = is_t6(lexicographic_square())
        assert v_lex.value is None  # no certificate supplied
