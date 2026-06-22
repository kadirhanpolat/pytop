"""Tests for computational homotopy engines: is_contractible_simplicial, has_sphere_homology."""

from __future__ import annotations

import pytest

from pytop.homotopy import has_sphere_homology, is_contractible_simplicial


# ---------------------------------------------------------------------------
# Helpers: canonical examples
# ---------------------------------------------------------------------------


def _filled_simplex_2d() -> list[list[int]]:
    """Filled triangle (contractible, dim 2)."""
    return [[0, 1, 2], [0, 1], [0, 2], [1, 2], [0], [1], [2]]


def _circle_s1() -> list[list[int]]:
    """Boundary of triangle ≃ S¹."""
    return [[0, 1], [1, 2], [2, 0], [0], [1], [2]]


def _sphere_s2() -> list[list[int]]:
    """Boundary of tetrahedron ≃ S²."""
    verts = [0, 1, 2, 3]
    faces = [
        [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3],
    ]
    edges = [[u, v] for u, v in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]]
    return faces + edges + [[v] for v in verts]


def _point() -> list[list[int]]:
    """Single vertex (contractible)."""
    return [[0]]


def _two_isolated_vertices() -> list[list[int]]:
    """Two disjoint vertices (disconnected ≃ S⁰)."""
    return [[0], [1]]


def _wedge_two_circles() -> list[list[int]]:
    """Figure-eight: S¹ ∨ S¹ (β₁=2)."""
    # Common vertex 0; triangle 0-1-2 and triangle 0-3-4
    return [
        [0, 1], [1, 2], [2, 0],
        [0, 3], [3, 4], [4, 0],
        [0], [1], [2], [3], [4],
    ]


def _cone_over_circle() -> list[list[int]]:
    """Cone over S¹ = filled disk (contractible)."""
    return [
        [0, 1, 4], [1, 2, 4], [2, 0, 4],
        [0, 1], [1, 2], [2, 0],
        [0, 4], [1, 4], [2, 4],
        [0], [1], [2], [4],
    ]


# ---------------------------------------------------------------------------
# is_contractible_simplicial
# ---------------------------------------------------------------------------


class TestIsContractibleSimplicial:
    def test_single_point_contractible(self):
        assert is_contractible_simplicial(_point()) is True

    def test_filled_triangle_contractible(self):
        assert is_contractible_simplicial(_filled_simplex_2d()) is True

    def test_cone_over_circle_contractible(self):
        assert is_contractible_simplicial(_cone_over_circle()) is True

    def test_path_graph_contractible(self):
        # 0-1-2 (tree)
        sc = [[0, 1], [1, 2], [0], [1], [2]]
        assert is_contractible_simplicial(sc) is True

    def test_single_edge_contractible(self):
        assert is_contractible_simplicial([[0, 1], [0], [1]]) is True

    def test_circle_not_contractible(self):
        assert is_contractible_simplicial(_circle_s1()) is False

    def test_sphere_s2_not_contractible(self):
        assert is_contractible_simplicial(_sphere_s2()) is False

    def test_two_isolated_vertices_not_contractible(self):
        # Disconnected — H₀ = ℤ²
        assert is_contractible_simplicial(_two_isolated_vertices()) is False

    def test_wedge_two_circles_not_contractible(self):
        # β₁ = 2
        assert is_contractible_simplicial(_wedge_two_circles()) is False

    def test_returns_bool(self):
        result = is_contractible_simplicial(_point())
        assert isinstance(result, bool)

    def test_face_closure_not_required(self):
        # Provide only maximal faces; face closure done internally
        sc = [[0, 1, 2]]  # filled triangle, faces omitted
        assert is_contractible_simplicial(sc) is True

    def test_torus_not_contractible(self):
        from pytop.simplicial_filtration import torus_filtration
        fc = torus_filtration()
        simplices = [list(s) for s in fc.simplices]
        # The torus is not contractible: H₁(T²) = ℤ² ≠ 0
        assert is_contractible_simplicial(simplices) is False


# ---------------------------------------------------------------------------
# has_sphere_homology
# ---------------------------------------------------------------------------


class TestHasSphereHomology:
    # S⁰
    def test_two_points_is_s0(self):
        assert has_sphere_homology(_two_isolated_vertices(), n=0) is True

    def test_single_point_not_s0(self):
        # H₀ = ℤ (1 component), but S⁰ needs 2 components
        assert has_sphere_homology(_point(), n=0) is False

    # S¹
    def test_circle_is_s1(self):
        assert has_sphere_homology(_circle_s1(), n=1) is True

    def test_circle_not_s0(self):
        assert has_sphere_homology(_circle_s1(), n=0) is False

    def test_circle_not_s2(self):
        assert has_sphere_homology(_circle_s1(), n=2) is False

    # S²
    def test_sphere_s2_is_s2(self):
        assert has_sphere_homology(_sphere_s2(), n=2) is True

    def test_sphere_s2_not_s1(self):
        assert has_sphere_homology(_sphere_s2(), n=1) is False

    # contractible spaces
    def test_point_not_any_sphere(self):
        # Point: H₀ = ℤ, nothing else — not S^n for n ≥ 1
        assert has_sphere_homology(_point(), n=1) is False
        assert has_sphere_homology(_point(), n=2) is False

    def test_filled_triangle_not_s2(self):
        assert has_sphere_homology(_filled_simplex_2d(), n=2) is False

    def test_filled_triangle_not_s1(self):
        assert has_sphere_homology(_filled_simplex_2d(), n=1) is False

    # wedge (not a sphere)
    def test_wedge_not_s1(self):
        assert has_sphere_homology(_wedge_two_circles(), n=1) is False

    # type
    def test_returns_bool(self):
        result = has_sphere_homology(_circle_s1(), n=1)
        assert isinstance(result, bool)

    def test_raises_on_negative_n(self):
        with pytest.raises(ValueError, match="non-negative"):
            has_sphere_homology(_circle_s1(), n=-1)

    def test_n_zero_correctness(self):
        # Two isolated triangles (face-closed by _face_close internally): H₀ = ℤ²
        # Each filled triangle is contractible; two disjoint → H₀ = ℤ² = H₀(S⁰)
        sc = [[0, 1, 2], [3, 4, 5]]
        assert has_sphere_homology(sc, n=0) is True
