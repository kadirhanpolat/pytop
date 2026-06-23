"""Tests for shape_theory.py computational engines (link_complex, manifold check, shape classification)."""

from __future__ import annotations

import pytest

from pytop.shape_theory import (
    has_trivial_shape_sc,
    is_manifold_triangulation,
    link_complex,
    shape_anr_check_sc,
)

# ---------------------------------------------------------------------------
# Fixtures: canonical simplicial complexes
# ---------------------------------------------------------------------------

# Boundary of tetrahedron = S²
BDRY_TETRA = [
    [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3],
    [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3],
    [0], [1], [2], [3],
]

# Filled tetrahedron (3-ball) = contractible
FILLED_TETRA = BDRY_TETRA + [[0, 1, 2, 3]]

# Circle (boundary of triangle) = S¹
CIRCLE = [[0, 1], [1, 2], [2, 0], [0], [1], [2]]

# Filled triangle = D² (disk) = contractible
DISK = [[0, 1, 2], [0, 1], [0, 2], [1, 2], [0], [1], [2]]

# Two disjoint points (S^0)
S0 = [[0], [1]]

# Heawood 7-vertex torus triangulation: Z₇ cyclic, χ = 7 - 21 + 14 = 0.
# Two orbit types: {0,1,3} → 013,124,235,346,045,156,026
#                  {0,3,4} → 034,145,256,036,014,125,023 (wait, standard Möbius-type)
# Simpler: from two base triangles {0,1,3} and {0,3,4} under i→(i+1)%7.
TORUS_7 = [
    [0,1,3],[1,2,4],[2,3,5],[3,4,6],[0,4,5],[1,5,6],[0,2,6],
    [0,3,4],[1,4,5],[2,5,6],[0,3,6],[0,1,4],[1,2,5],[2,3,6],
]


# ---------------------------------------------------------------------------
# link_complex
# ---------------------------------------------------------------------------

class TestLinkComplex:
    def test_link_in_disk_is_edge(self):
        lk = link_complex(DISK, 0)
        as_frozen = {frozenset(s) for s in lk}
        assert frozenset({1, 2}) in as_frozen  # edge 1-2 is in link(0)

    def test_link_in_circle_is_two_points(self):
        lk = link_complex(CIRCLE, 0)
        vertices = {frozenset(s) for s in lk if len(s) == 1}
        assert frozenset({1}) in vertices
        assert frozenset({2}) in vertices

    def test_link_in_bdry_tetra_is_triangle(self):
        lk = link_complex(BDRY_TETRA, 0)
        as_frozen = {frozenset(s) for s in lk}
        # link of 0 contains edges 1-2, 1-3, 2-3 and vertices 1,2,3
        assert frozenset({1, 2}) in as_frozen
        assert frozenset({1, 3}) in as_frozen
        assert frozenset({2, 3}) in as_frozen
        assert frozenset({1}) in as_frozen

    def test_link_vertex_not_in_complex_is_empty(self):
        lk = link_complex(DISK, 99)
        assert lk == []

    def test_link_isolated_vertex_is_empty(self):
        lk = link_complex([[0], [1]], 0)
        assert lk == []

    def test_link_is_face_closed(self):
        lk = link_complex(BDRY_TETRA, 0)
        as_frozen = {frozenset(s) for s in lk}
        # Every edge in the link must have its vertices in the link
        for s in list(as_frozen):
            if len(s) == 2:
                for v in s:
                    assert frozenset({v}) in as_frozen

    def test_link_has_sphere_homology_for_s2(self):
        # link of each vertex of S² triangulation is S¹
        from pytop.homotopy import has_sphere_homology
        for v in [0, 1, 2, 3]:
            lk = link_complex(BDRY_TETRA, v)
            assert has_sphere_homology(lk, 1)


# ---------------------------------------------------------------------------
# is_manifold_triangulation
# ---------------------------------------------------------------------------

class TestIsManifoldTriangulation:
    def test_boundary_tetra_is_2_manifold(self):
        assert is_manifold_triangulation(BDRY_TETRA, 2) is True

    def test_circle_is_1_manifold(self):
        assert is_manifold_triangulation(CIRCLE, 1) is True

    def test_disk_is_not_closed_2_manifold(self):
        # Boundary vertices have link = interval (contractible), not S¹
        assert is_manifold_triangulation(DISK, 2) is False

    def test_torus_is_2_manifold(self):
        assert is_manifold_triangulation(TORUS_7, 2) is True

    def test_sphere_not_1_manifold(self):
        # S² is not a 1-manifold (vertex links are triangles, not S^0)
        assert is_manifold_triangulation(BDRY_TETRA, 1) is False

    def test_two_points_is_0_manifold(self):
        # 0-manifold: each vertex link is S^{-1} = ∅ → has_sphere_homology([], -1) needed
        with pytest.raises(ValueError):
            is_manifold_triangulation(S0, 0)  # n must be ≥ 1

    def test_invalid_n_raises(self):
        with pytest.raises(ValueError):
            is_manifold_triangulation(DISK, 0)

    def test_negative_n_raises(self):
        with pytest.raises(ValueError):
            is_manifold_triangulation(DISK, -1)


# ---------------------------------------------------------------------------
# has_trivial_shape_sc
# ---------------------------------------------------------------------------

class TestHasTrivialShapeSc:
    def test_disk_is_contractible(self):
        assert has_trivial_shape_sc(DISK) is True

    def test_filled_tetra_is_contractible(self):
        assert has_trivial_shape_sc(FILLED_TETRA) is True

    def test_circle_is_not_contractible(self):
        assert has_trivial_shape_sc(CIRCLE) is False

    def test_sphere_s2_is_not_contractible(self):
        assert has_trivial_shape_sc(BDRY_TETRA) is False

    def test_single_point_is_contractible(self):
        assert has_trivial_shape_sc([[0]]) is True

    def test_two_disjoint_points_not_contractible(self):
        assert has_trivial_shape_sc(S0) is False

    def test_cone_over_circle_is_contractible(self):
        # Cone(S¹): add vertex 3 connected to all of [0,1,2]
        cone = CIRCLE + [[0, 3], [1, 3], [2, 3], [0, 1, 3], [1, 2, 3], [0, 2, 3], [3]]
        assert has_trivial_shape_sc(cone) is True

    def test_torus_not_contractible(self):
        assert has_trivial_shape_sc(TORUS_7) is False


# ---------------------------------------------------------------------------
# shape_anr_check_sc
# ---------------------------------------------------------------------------

class TestShapeAnrCheckSc:
    def test_disk_is_compact_ar(self):
        r = shape_anr_check_sc(DISK)
        assert r["is_anr"] is True
        assert r["is_fanr"] is True
        assert r["is_movable"] is True
        assert r["has_trivial_shape"] is True
        assert r["shape_class"] == "compact_ar"

    def test_circle_is_anr_not_ar(self):
        r = shape_anr_check_sc(CIRCLE)
        assert r["is_anr"] is True
        assert r["has_trivial_shape"] is False
        assert r["shape_class"] == "anr"

    def test_sphere_is_anr(self):
        r = shape_anr_check_sc(BDRY_TETRA)
        assert r["is_anr"] is True
        assert r["shape_class"] == "anr"

    def test_vertex_count_circle(self):
        r = shape_anr_check_sc(CIRCLE)
        assert r["vertex_count"] == 3

    def test_max_simplex_dim_circle(self):
        r = shape_anr_check_sc(CIRCLE)
        assert r["max_simplex_dim"] == 1

    def test_max_simplex_dim_sphere(self):
        r = shape_anr_check_sc(BDRY_TETRA)
        assert r["max_simplex_dim"] == 2

    def test_vertex_count_sphere(self):
        r = shape_anr_check_sc(BDRY_TETRA)
        assert r["vertex_count"] == 4

    def test_single_point_is_compact_ar(self):
        r = shape_anr_check_sc([[0]])
        assert r["has_trivial_shape"] is True
        assert r["vertex_count"] == 1
        assert r["max_simplex_dim"] == 0

    def test_face_closure_automatic(self):
        # Pass only maximal simplices — face closure should happen automatically
        r = shape_anr_check_sc([[0, 1, 2]])
        assert r["is_anr"] is True
        assert r["has_trivial_shape"] is True
