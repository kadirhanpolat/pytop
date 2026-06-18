"""Tests for LinkDiagram, linking_number, linking_matrix, multivariable_alexander.

Covers:
- LinkDiagram construction and validation
- LinkDiagram.from_knot conversion
- linking_number for Hopf link, unlink, trivial cases
- linking_matrix for Hopf link, unlink, knot
- multivariable_alexander (knot path + multi-component links)
- components property
- n_components field
"""
from __future__ import annotations

import pytest

from pytop.knot_invariants import (
    KnotDiagram,
    LinkDiagram,
    linking_matrix,
    linking_number,
    multivariable_alexander,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

def hopf_link() -> LinkDiagram:
    """Negative Hopf link: two components, two negative crossings.

    PD code from standard reference; arc 0,2 → component 0, arcs 1,3 → component 1.
    component_map index = arc label (0-based).
    """
    return LinkDiagram(
        crossings=[(1, 4, 2, 3), (3, 2, 4, 1)],
        signs=[-1, -1],
        n_components=2,
        component_map=[0, 1, 0, 1],  # arc 0→comp0, arc1→comp1, arc2→comp0, arc3→comp1
    )


def positive_hopf_link() -> LinkDiagram:
    """Positive Hopf link: two components, two positive crossings."""
    return LinkDiagram(
        crossings=[(1, 4, 2, 3), (3, 2, 4, 1)],
        signs=[1, 1],
        n_components=2,
        component_map=[0, 1, 0, 1],
    )


def unlink() -> LinkDiagram:
    """Two unlinked unknots — no crossings between them."""
    # Encode a 2-component unlink: 2 separate unknots with no crossing
    # We use a "virtual" diagram with zero crossings; n_components=2
    return LinkDiagram(
        crossings=[],
        signs=[],
        n_components=2,
        component_map=[],
    )


def unknot_diagram() -> KnotDiagram:
    """Right-handed trefoil for from_knot conversion tests."""
    return KnotDiagram(pd=[(1, 4, 2, 3), (3, 6, 4, 5), (5, 2, 6, 1)], signs=(-1, -1, -1))


# ---------------------------------------------------------------------------
# 1. LinkDiagram construction
# ---------------------------------------------------------------------------

class TestLinkDiagramConstruction:
    def test_basic_construction(self) -> None:
        ld = hopf_link()
        assert ld.n_components == 2
        assert len(ld.crossings) == 2
        assert len(ld.signs) == 2

    def test_crossing_length_validation(self) -> None:
        with pytest.raises(ValueError, match="4-tuple"):
            LinkDiagram(
                crossings=[(1, 2, 3)],  # type: ignore[list-item]
                signs=[1],
                n_components=1,
                component_map=[0, 0, 0],
            )

    def test_signs_alignment_validation(self) -> None:
        with pytest.raises(ValueError, match="align"):
            LinkDiagram(
                crossings=[(1, 2, 3, 4)],
                signs=[1, -1],  # too many
                n_components=1,
                component_map=[0, 0, 0, 0],
            )

    def test_invalid_sign_value(self) -> None:
        with pytest.raises(ValueError, match="sign"):
            LinkDiagram(
                crossings=[(1, 2, 3, 4)],
                signs=[0],
                n_components=1,
                component_map=[0, 0, 0, 0],
            )

    def test_component_map_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="component_map"):
            LinkDiagram(
                crossings=[(1, 2, 3, 4)],
                signs=[1],
                n_components=1,
                component_map=[0, 0, 5, 0],  # 5 >= n_components=1
            )

    def test_empty_crossings_valid(self) -> None:
        ld = unlink()
        assert ld.n_components == 2
        assert ld.crossings == []


# ---------------------------------------------------------------------------
# 2. LinkDiagram.from_knot
# ---------------------------------------------------------------------------

class TestFromKnot:
    def test_from_knot_n_components(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        assert ld.n_components == 1

    def test_from_knot_crossings_preserved(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        assert len(ld.crossings) == len(kd.pd)

    def test_from_knot_signs_preserved(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        assert list(ld.signs) == list(kd.signs)

    def test_from_knot_all_arcs_component_zero(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        assert all(c == 0 for c in ld.component_map)

    def test_from_knot_component_map_length(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        # component_map length = number of distinct arc labels
        labels: set = set()
        for crossing in kd.pd:
            labels.update(crossing)
        assert len(ld.component_map) == len(labels)


# ---------------------------------------------------------------------------
# 3. components property
# ---------------------------------------------------------------------------

class TestComponentsProperty:
    def test_hopf_components_count(self) -> None:
        ld = hopf_link()
        comps = ld.components
        assert len(comps) == 2

    def test_hopf_components_cover_all_arcs(self) -> None:
        ld = hopf_link()
        comps = ld.components
        all_arcs = comps[0] | comps[1]
        assert all_arcs == set(range(len(ld.component_map)))

    def test_knot_single_component(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        comps = ld.components
        assert len(comps) == 1


# ---------------------------------------------------------------------------
# 4. linking_number
# ---------------------------------------------------------------------------

class TestLinkingNumber:
    def test_hopf_link_negative(self) -> None:
        ld = hopf_link()
        lk = linking_number(ld, 0, 1)
        assert lk == -1

    def test_hopf_link_symmetric(self) -> None:
        ld = hopf_link()
        assert linking_number(ld, 0, 1) == linking_number(ld, 1, 0)

    def test_positive_hopf_link(self) -> None:
        ld = positive_hopf_link()
        lk = linking_number(ld, 0, 1)
        assert lk == 1

    def test_unlink_is_zero(self) -> None:
        ld = unlink()
        lk = linking_number(ld, 0, 1)
        assert lk == 0

    def test_same_component_is_zero(self) -> None:
        ld = hopf_link()
        assert linking_number(ld, 0, 0) == 0
        assert linking_number(ld, 1, 1) == 0

    def test_out_of_range_component_raises(self) -> None:
        ld = hopf_link()
        with pytest.raises(ValueError):
            linking_number(ld, 0, 5)

    def test_negative_component_index_raises(self) -> None:
        ld = hopf_link()
        with pytest.raises(ValueError):
            linking_number(ld, -1, 0)

    def test_knot_single_component_self_zero(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        assert linking_number(ld, 0, 0) == 0


# ---------------------------------------------------------------------------
# 5. linking_matrix
# ---------------------------------------------------------------------------

class TestLinkingMatrix:
    def test_hopf_diagonal_zero(self) -> None:
        ld = hopf_link()
        mat = linking_matrix(ld)
        assert mat[0][0] == 0
        assert mat[1][1] == 0

    def test_hopf_matrix_off_diagonal(self) -> None:
        ld = hopf_link()
        mat = linking_matrix(ld)
        assert mat[0][1] == -1
        assert mat[1][0] == -1

    def test_hopf_matrix_symmetric(self) -> None:
        ld = hopf_link()
        mat = linking_matrix(ld)
        assert mat[0][1] == mat[1][0]

    def test_unlink_matrix_all_zero(self) -> None:
        ld = unlink()
        mat = linking_matrix(ld)
        assert mat == [[0, 0], [0, 0]]

    def test_knot_matrix_is_1x1_zero(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        mat = linking_matrix(ld)
        assert mat == [[0]]

    def test_positive_hopf_matrix_positive(self) -> None:
        ld = positive_hopf_link()
        mat = linking_matrix(ld)
        assert mat[0][1] == 1
        assert mat[1][0] == 1


# ---------------------------------------------------------------------------
# 6. multivariable_alexander
# ---------------------------------------------------------------------------

class TestMultivariableAlexander:
    def test_knot_returns_dict(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        result = multivariable_alexander(ld)
        assert isinstance(result, dict)

    def test_knot_result_has_tuple_keys(self) -> None:
        kd = unknot_diagram()
        ld = LinkDiagram.from_knot(kd)
        result = multivariable_alexander(ld)
        for key in result:
            assert isinstance(key, tuple)

    def test_hopf_link_alexander_is_one(self) -> None:
        # The multivariable Alexander polynomial of the Hopf link is 1 (up to units).
        ld = hopf_link()
        assert multivariable_alexander(ld) == {(0, 0): 1}

    def test_unlink_alexander_is_zero(self) -> None:
        # A split link has vanishing Alexander polynomial.
        ld = unlink()
        assert multivariable_alexander(ld) == {}
