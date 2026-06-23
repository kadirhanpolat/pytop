"""Tests for the computational pi1_graph engine in fundamental_group.py."""

from __future__ import annotations

import pytest

from pytop.fundamental_group import pi1_graph
from pytop.van_kampen import GroupPresentation

# ---------------------------------------------------------------------------
# pi1_graph — basic correctness
# ---------------------------------------------------------------------------


class TestPi1Graph:
    def test_single_vertex_no_edges_trivial(self):
        p = pi1_graph([0], [])
        assert isinstance(p, GroupPresentation)
        assert p.rank == 0
        assert p.is_free

    def test_path_graph_trivial(self):
        # 0-1-2: tree, simply connected
        p = pi1_graph([0, 1, 2], [(0, 1), (1, 2)])
        assert p.rank == 0

    def test_triangle_rank_one(self):
        # Triangle = S^1, π₁(S^1) = ℤ (free of rank 1)
        p = pi1_graph([0, 1, 2], [(0, 1), (1, 2), (2, 0)])
        assert p.rank == 1
        assert p.is_free
        assert len(p.relators) == 0

    def test_loop_on_single_vertex_rank_one(self):
        p = pi1_graph([0], [(0, 0)])
        assert p.rank == 1

    def test_theta_graph_rank_two(self):
        # Two vertices, three parallel edges
        p = pi1_graph([0, 1], [(0, 1), (0, 1), (0, 1)])
        assert p.rank == 2

    def test_wedge_of_three_circles(self):
        # Star graph with 3 extra loops = 3 non-tree edges
        # One central vertex 0, three loops: rank 3
        p = pi1_graph([0], [(0, 0), (0, 0), (0, 0)])
        assert p.rank == 3

    def test_complete_k4_rank_three(self):
        # K₄: β₁ = 6 - 4 + 1 = 3
        verts = [0, 1, 2, 3]
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        p = pi1_graph(verts, edges)
        assert p.rank == 3

    def test_graph_with_string_vertices(self):
        p = pi1_graph(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
        assert p.rank == 1

    def test_result_is_free_group(self):
        # For any graph, π₁ is free (no 2-cells = no relators)
        for verts, edges in [
            ([0, 1, 2], [(0, 1), (1, 2), (2, 0)]),
            ([0, 1], [(0, 1), (0, 1)]),
            ([0, 1, 2, 3], [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]),
        ]:
            p = pi1_graph(verts, edges)
            assert p.is_free
            assert len(p.relators) == 0

    def test_rank_matches_beta1(self):
        from pytop.covering_spaces import fundamental_group_rank_graph

        test_cases = [
            ([0], []),
            ([0, 1, 2], [(0, 1), (1, 2), (2, 0)]),
            ([0, 1], [(0, 1), (0, 1), (0, 1)]),
            ([0, 1, 2, 3], [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
        ]
        for verts, edges in test_cases:
            p = pi1_graph(verts, edges)
            expected = fundamental_group_rank_graph(verts, edges)
            assert p.rank == expected, f"rank mismatch for {verts}, {edges}"

    def test_custom_basepoint(self):
        # Basepoint shouldn't change the group isomorphism class
        p0 = pi1_graph([0, 1, 2], [(0, 1), (1, 2), (2, 0)], basepoint=0)
        p1 = pi1_graph([0, 1, 2], [(0, 1), (1, 2), (2, 0)], basepoint=1)
        assert p0.rank == p1.rank

    def test_raises_on_empty_vertices(self):
        with pytest.raises(ValueError):
            pi1_graph([], [])

    def test_raises_on_invalid_basepoint(self):
        with pytest.raises(ValueError, match="[Bb]asepoint"):
            pi1_graph([0, 1], [(0, 1)], basepoint=99)

    def test_generators_named_for_non_tree_edges(self):
        # Triangle: one non-tree edge = one generator
        p = pi1_graph([0, 1, 2], [(0, 1), (1, 2), (2, 0)])
        assert len(p.generators) == 1
