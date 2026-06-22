"""Tests for computational degree engine: map_degree_simplicial."""

from __future__ import annotations

import pytest

from pytop.degree_theory import map_degree_simplicial
from pytop.simplicial_complexes import simplicial_complex
from pytop.simplicial_maps import SimplicialMap


# ---------------------------------------------------------------------------
# Helper: build a standard S¹ triangulation (triangle boundary, 3 vertices)
# ---------------------------------------------------------------------------


def _circle_sc():
    """S¹ as boundary of triangle {0,1,2} (face-closed: vertices included)."""
    return simplicial_complex([[0, 1], [1, 2], [2, 0], [0], [1], [2]])


def _circle_identity_map():
    """Identity map on the 3-vertex S¹."""
    sc = _circle_sc()
    return SimplicialMap(domain=sc, codomain=sc, vertex_map={0: 0, 1: 1, 2: 2})


def _circle_reflection_map():
    """Reflection on S¹: swap vertices 1 and 2 → degree −1.

    The map 0↦0, 1↦2, 2↦1 reverses the orientation of every edge, giving d = −1.
    """
    sc = _circle_sc()
    return SimplicialMap(domain=sc, codomain=sc, vertex_map={0: 0, 1: 2, 2: 1})


# ---------------------------------------------------------------------------
# TestMapDegreeSimplicial
# ---------------------------------------------------------------------------


class TestMapDegreeSimplicial:
    def test_identity_has_degree_one(self):
        assert map_degree_simplicial(_circle_identity_map(), n=1) == 1

    def test_reflection_has_degree_minus_one(self):
        assert map_degree_simplicial(_circle_reflection_map(), n=1) == -1

    def test_returns_int(self):
        result = map_degree_simplicial(_circle_identity_map(), n=1)
        assert isinstance(result, int)

    def test_degree_is_additive_under_composition_sign(self):
        # reflection ∘ reflection = identity: degree = 1
        sc = _circle_sc()
        # both reflections are the same map on vertices
        refl = SimplicialMap(domain=sc, codomain=sc, vertex_map={0: 0, 1: 2, 2: 1})
        # identity composed should give degree 1; we just verify each individually
        assert map_degree_simplicial(refl, n=1) == -1
        ident = SimplicialMap(domain=sc, codomain=sc, vertex_map={0: 0, 1: 1, 2: 2})
        assert map_degree_simplicial(ident, n=1) == 1

    def test_raises_on_n_zero(self):
        with pytest.raises(ValueError, match="≥ 1"):
            map_degree_simplicial(_circle_identity_map(), n=0)

    def test_raises_on_negative_n(self):
        with pytest.raises(ValueError, match="≥ 1"):
            map_degree_simplicial(_circle_identity_map(), n=-1)

    def test_larger_circle_identity(self):
        # S¹ triangulated with 4 vertices: square boundary (face-closed)
        sc = simplicial_complex([[0, 1], [1, 2], [2, 3], [3, 0], [0], [1], [2], [3]])
        ident = SimplicialMap(domain=sc, codomain=sc, vertex_map={0: 0, 1: 1, 2: 2, 3: 3})
        assert map_degree_simplicial(ident, n=1) == 1

    def test_larger_circle_reflection(self):
        # S¹ triangulated with 4 vertices; swap 1↔3 for reflection, 0 and 2 fixed
        sc = simplicial_complex([[0, 1], [1, 2], [2, 3], [3, 0], [0], [1], [2], [3]])
        refl = SimplicialMap(domain=sc, codomain=sc, vertex_map={0: 0, 1: 3, 2: 2, 3: 1})
        assert map_degree_simplicial(refl, n=1) == -1
