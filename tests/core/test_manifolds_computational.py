"""Tests for computational manifold engine: euler_characteristic_simplicial."""

from __future__ import annotations

import pytest

from pytop.manifolds import euler_characteristic_simplicial


class TestEulerCharacteristicSimplicial:
    # ------------------------------------------------------------------
    # Points and edges
    # ------------------------------------------------------------------

    def test_single_point_chi_one(self):
        assert euler_characteristic_simplicial([[0]]) == 1

    def test_two_isolated_points_chi_two(self):
        assert euler_characteristic_simplicial([[0], [1]]) == 2

    def test_single_edge_chi_one(self):
        # Edge [0,1]: f₀=2, f₁=1 → χ = 2 - 1 = 1
        assert euler_characteristic_simplicial([[0, 1]]) == 1

    def test_path_n3_chi_one(self):
        # Path 0-1-2: f₀=3, f₁=2 → χ = 3 - 2 = 1
        assert euler_characteristic_simplicial([[0, 1], [1, 2]]) == 1

    # ------------------------------------------------------------------
    # Circles
    # ------------------------------------------------------------------

    def test_triangle_boundary_chi_zero(self):
        # S¹: f₀=3, f₁=3 → χ = 0
        assert euler_characteristic_simplicial([[0, 1], [1, 2], [2, 0]]) == 0

    def test_square_boundary_chi_zero(self):
        # S¹ with 4 vertices: f₀=4, f₁=4 → χ = 0
        sc = [[0, 1], [1, 2], [2, 3], [3, 0]]
        assert euler_characteristic_simplicial(sc) == 0

    # ------------------------------------------------------------------
    # Disks / contractible surfaces
    # ------------------------------------------------------------------

    def test_filled_triangle_chi_one(self):
        # Filled triangle: f₀=3, f₁=3, f₂=1 → χ = 3-3+1 = 1
        assert euler_characteristic_simplicial([[0, 1, 2]]) == 1

    def test_filled_square_chi_one(self):
        # Two filled triangles sharing diagonal: χ = 4 - 5 + 2 = 1
        sc = [[0, 1, 2], [0, 2, 3]]
        assert euler_characteristic_simplicial(sc) == 1

    # ------------------------------------------------------------------
    # Sphere S²
    # ------------------------------------------------------------------

    def test_tetrahedron_boundary_chi_two(self):
        # S²: f₀=4, f₁=6, f₂=4 → χ = 4-6+4 = 2
        sc = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
        assert euler_characteristic_simplicial(sc) == 2

    # ------------------------------------------------------------------
    # Torus T²
    # ------------------------------------------------------------------

    def test_torus_chi_zero(self):
        from pytop.simplicial_filtration import torus_filtration
        fc = torus_filtration()
        simplices = [list(s) for s in fc.simplices]
        assert euler_characteristic_simplicial(simplices) == 0

    # ------------------------------------------------------------------
    # Klein bottle
    # ------------------------------------------------------------------

    def test_klein_bottle_chi_zero(self):
        from pytop.simplicial_filtration import klein_bottle_filtration
        fc = klein_bottle_filtration()
        simplices = [list(s) for s in fc.simplices]
        assert euler_characteristic_simplicial(simplices) == 0

    # ------------------------------------------------------------------
    # RP²
    # ------------------------------------------------------------------

    def test_rp2_chi_one(self):
        from pytop.simplicial_filtration import rp2_filtration
        fc = rp2_filtration()
        simplices = [list(s) for s in fc.simplices]
        assert euler_characteristic_simplicial(simplices) == 1

    # ------------------------------------------------------------------
    # Maximal-simplices-only input (face-closure automatic)
    # ------------------------------------------------------------------

    def test_maximal_simplices_only_s2(self):
        # Pass only the four triangles; vertices and edges added automatically
        sc = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
        assert euler_characteristic_simplicial(sc) == 2

    def test_maximal_simplices_only_torus(self):
        from pytop.simplicial_filtration import torus_filtration
        fc = torus_filtration()
        # Take only 2-simplices as maximal faces
        top_simplices = [list(s) for s in fc.simplices if len(s) == 3]
        assert euler_characteristic_simplicial(top_simplices) == 0

    # ------------------------------------------------------------------
    # Empty and returns int
    # ------------------------------------------------------------------

    def test_empty_input_chi_zero(self):
        assert euler_characteristic_simplicial([]) == 0

    def test_returns_int(self):
        result = euler_characteristic_simplicial([[0]])
        assert isinstance(result, int)

    # ------------------------------------------------------------------
    # Additivity / consistency
    # ------------------------------------------------------------------

    def test_disjoint_union_chi_additive(self):
        # Two triangles (each χ=1): χ(A ⊔ B) = χ(A) + χ(B) = 2
        sc = [[0, 1, 2], [3, 4, 5]]
        assert euler_characteristic_simplicial(sc) == 2

    def test_circle_wedge_chi_minus_one(self):
        # S¹ ∨ S¹ (shared vertex 0): f₀=5, f₁=6 → χ = 5-6 = -1
        # (χ(A∨B) = χ(A) + χ(B) - χ(pt) = 0+0-1 = -1)
        sc = [
            [0, 1], [1, 2], [2, 0],  # first triangle boundary
            [0, 3], [3, 4], [4, 0],  # second triangle boundary
        ]
        assert euler_characteristic_simplicial(sc) == -1
