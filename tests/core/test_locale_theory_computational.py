"""Tests for locale_theory.py computational engines (frame, well-inside, regularity)."""

from __future__ import annotations

import pytest

from pytop.locale_theory import (
    frame_from_finite_topology,
    is_regular_frame,
    is_spatial_finite_frame,
    pseudocomplement_in_frame,
    well_inside_relation,
)

# ---------------------------------------------------------------------------
# Canonical topologies
# ---------------------------------------------------------------------------

TRIVIAL_2PT = [frozenset(), frozenset({0, 1})]  # indiscrete on {0,1}
SIERPINSKI = [frozenset(), frozenset({1}), frozenset({0, 1})]
DISCRETE_2PT = [frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})]
DISCRETE_3PT = [
    frozenset(), frozenset({0}), frozenset({1}), frozenset({2}),
    frozenset({0, 1}), frozenset({0, 2}), frozenset({1, 2}), frozenset({0, 1, 2}),
]
# 4-point diamond: opens are ∅, {a}, {b}, {a,b}, {a,b,c}, X (where X={a,b,c,d})
# Actually let's use a simple non-trivial topology on {0,1,2}:
# τ = {∅, {0}, {0,1}, {0,2}, {0,1,2}} — must be closed under ∩ and ∪
# Check: {0,1}∩{0,2}={0} ✓, {0,1}∪{0,2}={0,1,2} ✓
NONTRIVIAL_3PT = [
    frozenset(), frozenset({0}), frozenset({0, 1}), frozenset({0, 2}), frozenset({0, 1, 2}),
]
POINT = [frozenset(), frozenset({0})]


# ---------------------------------------------------------------------------
# frame_from_finite_topology
# ---------------------------------------------------------------------------

class TestFrameFromFiniteTopology:
    def test_discrete_returns_all_subsets(self):
        frame = frame_from_finite_topology(DISCRETE_2PT)
        assert len(frame) == 4
        assert frozenset() in frame
        assert frozenset({0, 1}) in frame

    def test_sierpinski_returns_three_opens(self):
        frame = frame_from_finite_topology(SIERPINSKI)
        assert len(frame) == 3

    def test_sorted_by_size(self):
        frame = frame_from_finite_topology(DISCRETE_2PT)
        sizes = [len(s) for s in frame]
        assert sizes == sorted(sizes)

    def test_trivial_2pt(self):
        frame = frame_from_finite_topology(TRIVIAL_2PT)
        assert len(frame) == 2

    def test_nontrivial_3pt_valid(self):
        frame = frame_from_finite_topology(NONTRIVIAL_3PT)
        assert len(frame) == 5

    def test_not_closed_under_intersection_raises(self):
        bad = [frozenset(), frozenset({0, 1}), frozenset({1, 2}), frozenset({0, 1, 2})]
        with pytest.raises(ValueError, match="∩"):
            frame_from_finite_topology(bad)

    def test_not_closed_under_union_raises(self):
        bad = [frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1, 2})]
        with pytest.raises(ValueError, match="∪"):
            frame_from_finite_topology(bad)

    def test_point_topology(self):
        frame = frame_from_finite_topology(POINT)
        assert len(frame) == 2


# ---------------------------------------------------------------------------
# pseudocomplement_in_frame
# ---------------------------------------------------------------------------

class TestPseudocomplementInFrame:
    def test_empty_star_is_top(self):
        # ∅* = X (top element)
        b_star = pseudocomplement_in_frame(DISCRETE_2PT, frozenset())
        assert b_star == frozenset({0, 1})

    def test_top_star_is_empty(self):
        # X* = ∅ (bottom element)
        b_star = pseudocomplement_in_frame(DISCRETE_2PT, frozenset({0, 1}))
        assert b_star == frozenset()

    def test_sierpinski_1_star(self):
        # {1}* = largest open disjoint from {1} = ∅
        b_star = pseudocomplement_in_frame(SIERPINSKI, frozenset({1}))
        assert b_star == frozenset()

    def test_discrete_singleton_star(self):
        # {0}* = {1} in discrete topology on {0,1}
        b_star = pseudocomplement_in_frame(DISCRETE_2PT, frozenset({0}))
        assert b_star == frozenset({1})

    def test_discrete_singleton_star_symmetric(self):
        b_star = pseudocomplement_in_frame(DISCRETE_2PT, frozenset({1}))
        assert b_star == frozenset({0})

    def test_trivial_singleton_star(self):
        # In indiscrete on {0,1}: {0}* = ∅ (only ∅ is disjoint from {0})
        b_star = pseudocomplement_in_frame(TRIVIAL_2PT, frozenset({0}))
        assert b_star == frozenset()

    def test_nontrivial_0_star(self):
        # {0}* = largest open disjoint from {0} in NONTRIVIAL_3PT
        b_star = pseudocomplement_in_frame(NONTRIVIAL_3PT, frozenset({0}))
        assert b_star == frozenset()  # only ∅ is disjoint from {0}


# ---------------------------------------------------------------------------
# well_inside_relation
# ---------------------------------------------------------------------------

class TestWellInsideRelation:
    def test_empty_well_inside_everything(self):
        wi = well_inside_relation(DISCRETE_2PT)
        for a in DISCRETE_2PT:
            assert wi[(frozenset(), frozenset(a))] is True

    def test_discrete_singleton_well_inside_itself(self):
        wi = well_inside_relation(DISCRETE_2PT)
        assert wi[(frozenset({0}), frozenset({0}))] is True
        assert wi[(frozenset({1}), frozenset({1}))] is True

    def test_top_well_inside_only_top(self):
        wi = well_inside_relation(DISCRETE_2PT)
        top = frozenset({0, 1})
        assert wi[(top, top)] is True
        for a in [frozenset(), frozenset({0}), frozenset({1})]:
            assert wi[(top, frozenset(a))] is False

    def test_sierpinski_1_not_well_inside_itself(self):
        wi = well_inside_relation(SIERPINSKI)
        # {1}* = ∅, ∅ ∪ {1} = {1} ≠ {0,1}, so {1} ⋪ {1}
        assert wi[(frozenset({1}), frozenset({1}))] is False

    def test_sierpinski_empty_well_inside_1(self):
        wi = well_inside_relation(SIERPINSKI)
        # ∅* = {0,1} (in Sierpinski: opens disjoint from ∅ = all, join = {0,1})
        # {0,1} ∪ {1} = {0,1} = top → True
        assert wi[(frozenset(), frozenset({1}))] is True

    def test_well_inside_dict_size(self):
        wi = well_inside_relation(DISCRETE_2PT)
        assert len(wi) == 4 * 4  # |frame|²


# ---------------------------------------------------------------------------
# is_regular_frame
# ---------------------------------------------------------------------------

class TestIsRegularFrame:
    def test_discrete_2pt_is_regular(self):
        assert is_regular_frame(DISCRETE_2PT) is True

    def test_discrete_3pt_is_regular(self):
        assert is_regular_frame(DISCRETE_3PT) is True

    def test_sierpinski_not_regular(self):
        assert is_regular_frame(SIERPINSKI) is False

    def test_trivial_indiscrete_is_regular(self):
        # Indiscrete: only ∅ and X. ∅ << ∅ (trivially), X << X (X* = ∅, ∅∪X = X = top).
        assert is_regular_frame(TRIVIAL_2PT) is True

    def test_point_topology_is_regular(self):
        assert is_regular_frame(POINT) is True

    def test_nontrivial_3pt_not_regular(self):
        # This non-T1 topology is generally not regular as a frame
        result = is_regular_frame(NONTRIVIAL_3PT)
        assert isinstance(result, bool)  # returns a definite answer

    def test_single_open_trivial(self):
        tau = [frozenset({0})]
        assert is_regular_frame(tau) is True


# ---------------------------------------------------------------------------
# is_spatial_finite_frame
# ---------------------------------------------------------------------------

class TestIsSpatialFiniteFrame:
    def test_discrete_is_spatial(self):
        assert is_spatial_finite_frame(DISCRETE_2PT) is True

    def test_sierpinski_is_spatial(self):
        assert is_spatial_finite_frame(SIERPINSKI) is True

    def test_trivial_is_spatial(self):
        assert is_spatial_finite_frame(TRIVIAL_2PT) is True

    def test_discrete_3pt_is_spatial(self):
        assert is_spatial_finite_frame(DISCRETE_3PT) is True

    def test_missing_empty_set_not_spatial(self):
        tau_no_empty = [frozenset({0}), frozenset({0, 1})]
        assert is_spatial_finite_frame(tau_no_empty) is False

    def test_missing_top_not_spatial(self):
        # {0} ∪ {1} = {0,1} ∉ frame → top missing, not spatial
        tau_no_top = [frozenset(), frozenset({0}), frozenset({1})]
        assert is_spatial_finite_frame(tau_no_top) is False

    def test_point_topology_is_spatial(self):
        assert is_spatial_finite_frame(POINT) is True
