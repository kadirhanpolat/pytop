"""Tests for dimension_theory.py computational engines (covering_dimension_simplicial, ind_finite_space)."""

from __future__ import annotations

from pytop.dimension_theory import covering_dimension_simplicial, ind_finite_space

# ---------------------------------------------------------------------------
# covering_dimension_simplicial
# ---------------------------------------------------------------------------

class TestCoveringDimensionSimplicial:
    def test_point_dim_zero(self):
        assert covering_dimension_simplicial([[0]]) == 0

    def test_edge_dim_one(self):
        assert covering_dimension_simplicial([[0, 1], [0], [1]]) == 1

    def test_circle_dim_one(self):
        assert covering_dimension_simplicial([[0, 1], [1, 2], [2, 0], [0], [1], [2]]) == 1

    def test_triangle_dim_two(self):
        assert covering_dimension_simplicial([[0, 1, 2], [0, 1], [0, 2], [1, 2], [0], [1], [2]]) == 2

    def test_sphere_s2_dim_two(self):
        bdry = [[0,1,2],[0,1,3],[0,2,3],[1,2,3],[0,1],[0,2],[0,3],[1,2],[1,3],[2,3],[0],[1],[2],[3]]
        assert covering_dimension_simplicial(bdry) == 2

    def test_tetrahedron_3_simplex_dim_three(self):
        assert covering_dimension_simplicial([[0, 1, 2, 3]]) == 3

    def test_empty_returns_minus_one(self):
        assert covering_dimension_simplicial([]) == -1

    def test_two_points_dim_zero(self):
        assert covering_dimension_simplicial([[0], [1]]) == 0

    def test_torus_7_vertex_dim_two(self):
        torus = [
            [0,1,2],[0,2,6],[0,3,4],[0,4,1],[0,5,3],[0,6,5],
            [1,4,5],[1,5,6],[1,6,2],[2,3,6],[2,4,3],[2,5,4],
            [3,5,6],[4,6,3],
        ]
        assert covering_dimension_simplicial(torus) == 2

    def test_max_dim_from_mixed_simplices(self):
        # Complex with simplices of various dimensions
        mixed = [[0], [0, 1], [0, 1, 2]]
        assert covering_dimension_simplicial(mixed) == 2


# ---------------------------------------------------------------------------
# ind_finite_space
# ---------------------------------------------------------------------------

class TestIndFiniteSpace:
    def test_empty_space_minus_one(self):
        assert ind_finite_space([]) == -1

    def test_single_point_zero(self):
        assert ind_finite_space([frozenset(), frozenset({0})]) == 0

    def test_discrete_2pt_zero(self):
        # Discrete space: specialization = identity, no non-trivial chain
        tau = [frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})]
        assert ind_finite_space(tau) == 0

    def test_sierpinski_space_one(self):
        # Sierpinski: 0 specializes to 1 (every open containing 0 contains 1)
        tau = [frozenset(), frozenset({1}), frozenset({0, 1})]
        assert ind_finite_space(tau) == 1

    def test_trivial_topology_zero(self):
        # Indiscrete on {0,1}: 0 ≤ 1 and 1 ≤ 0, so same equivalence class
        # Longest strict chain = 0
        tau = [frozenset(), frozenset({0, 1})]
        assert ind_finite_space(tau) == 0

    def test_three_point_chain_two(self):
        # Three-point chain: τ = {∅, {2}, {1,2}, {0,1,2}}
        # Specialization order: 0 < 1 < 2 (chain of length 2)
        tau = [frozenset(), frozenset({2}), frozenset({1, 2}), frozenset({0, 1, 2})]
        assert ind_finite_space(tau) == 2

    def test_discrete_3pt_zero(self):
        tau = [
            frozenset(), frozenset({0}), frozenset({1}), frozenset({2}),
            frozenset({0, 1}), frozenset({0, 2}), frozenset({1, 2}), frozenset({0, 1, 2}),
        ]
        assert ind_finite_space(tau) == 0

    def test_two_point_sierpinski_chain_length_one(self):
        # 0 specializes to 1 but not vice versa
        tau = [frozenset(), frozenset({1}), frozenset({0, 1})]
        result = ind_finite_space(tau)
        assert result == 1

    def test_ind_nonnegative_for_nonempty(self):
        tau = [frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})]
        assert ind_finite_space(tau) >= 0

    def test_nontrivial_3pt_topology(self):
        # τ = {∅, {0}, {0,1}, {0,2}, {0,1,2}}
        tau = [
            frozenset(), frozenset({0}), frozenset({0, 1}),
            frozenset({0, 2}), frozenset({0, 1, 2}),
        ]
        result = ind_finite_space(tau)
        assert isinstance(result, int)
        assert result >= 0
