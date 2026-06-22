"""Tests for computational covering-space engines in covering_spaces.py.

Covers: CoveringGraph, cyclic_voltage_cover, universal_covering_tree,
fundamental_group_rank_graph, is_graph_covering_map.
"""

from __future__ import annotations

import pytest

from pytop.covering_spaces import (
    CoveringGraph,
    cyclic_voltage_cover,
    fundamental_group_rank_graph,
    is_graph_covering_map,
    universal_covering_tree,
)


# ---------------------------------------------------------------------------
# fundamental_group_rank_graph
# ---------------------------------------------------------------------------


class TestFundamentalGroupRankGraph:
    def test_empty_graph_rank_zero(self):
        assert fundamental_group_rank_graph([], []) == 0

    def test_single_vertex_no_edges(self):
        assert fundamental_group_rank_graph([0], []) == 0

    def test_path_graph_is_tree_rank_zero(self):
        # 0-1-2  (tree: simply connected)
        assert fundamental_group_rank_graph([0, 1, 2], [(0, 1), (1, 2)]) == 0

    def test_triangle_rank_one(self):
        # Triangle = S^1, π₁ = ℤ
        assert fundamental_group_rank_graph([0, 1, 2], [(0, 1), (1, 2), (2, 0)]) == 1

    def test_loop_on_single_vertex_rank_one(self):
        assert fundamental_group_rank_graph([0], [(0, 0)]) == 1

    def test_two_loops_rank_two(self):
        assert fundamental_group_rank_graph([0], [(0, 0), (0, 0)]) == 2

    def test_theta_graph_rank_two(self):
        # Two vertices, three parallel edges → β₁ = 3 - 2 + 1 = 2
        verts = [0, 1]
        edges = [(0, 1), (0, 1), (0, 1)]
        assert fundamental_group_rank_graph(verts, edges) == 2

    def test_complete_k4_rank_three(self):
        # K₄: 4 vertices, 6 edges → β₁ = 6 - 4 + 1 = 3
        verts = [0, 1, 2, 3]
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        assert fundamental_group_rank_graph(verts, edges) == 3

    def test_two_disjoint_triangles(self):
        # Each component has β₁ = 1; total = 1 + 1 + (2-1) = ... let's compute.
        # |E| = 6, |V| = 6, components = 2 → β₁ = 6 - 6 + 2 = 2
        verts = [0, 1, 2, 3, 4, 5]
        edges = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
        assert fundamental_group_rank_graph(verts, edges) == 2

    def test_forest_two_components_rank_zero(self):
        # Two disjoint edges (trees) → β₁ = 2 - 4 + 2 = 0
        verts = [0, 1, 2, 3]
        edges = [(0, 1), (2, 3)]
        assert fundamental_group_rank_graph(verts, edges) == 0


# ---------------------------------------------------------------------------
# cyclic_voltage_cover
# ---------------------------------------------------------------------------


class TestCyclicVoltageCover:
    def test_basic_structure_triangle_two_sheets(self):
        # Triangle (0-1-2) with n=2: 6 cover vertices, 6 cover edges
        verts = [0, 1, 2]
        edges = [(0, 1), (1, 2), (2, 0)]
        cg = cyclic_voltage_cover(verts, edges, n=2)
        assert cg.n == 2
        assert cg.num_cover_vertices == 6
        assert cg.num_cover_edges == 6

    def test_cover_vertices_are_pairs(self):
        verts = [0, 1]
        edges = [(0, 1)]
        cg = cyclic_voltage_cover(verts, edges, n=3)
        cverts = cg.cover_vertices
        assert len(cverts) == 6
        for v, k in cverts:
            assert v in verts
            assert 0 <= k < 3

    def test_explicit_voltages_respected(self):
        verts = [0, 1, 2]
        edges = [(0, 1), (1, 2), (2, 0)]
        # Assign voltage 0 to all non-tree edges (trivial cover)
        cg = cyclic_voltage_cover(verts, edges, n=2, voltages=[0, 0, 0])
        # All edges lift with voltage 0: (u,k) → (v,k)
        for (u, ku), (v, kv) in cg.cover_edges:
            assert ku == kv

    def test_voltage_one_on_single_edge(self):
        # One-vertex loop with voltage 1 in Z/3: 3 sheets, forms a single cycle
        cg = cyclic_voltage_cover([0], [(0, 0)], n=3, voltages=[1])
        assert cg.num_cover_vertices == 3
        assert cg.num_cover_edges == 3
        # Each edge (0,k) → (0, (k+1) % 3)
        for (u, k_src), (v, k_tgt) in cg.cover_edges:
            assert u == 0 and v == 0
            assert k_tgt == (k_src + 1) % 3

    def test_default_voltage_assigns_one_to_first_non_tree_edge(self):
        # Path 0-1 (tree edge) + extra edge 0-1 (non-tree, gets voltage 1)
        verts = [0, 1]
        edges = [(0, 1), (0, 1)]  # first is tree, second non-tree
        cg = cyclic_voltage_cover(verts, edges, n=2)
        assert cg.voltages[0] == 0   # tree edge
        assert cg.voltages[1] == 1   # non-tree edge

    def test_raises_on_nonpositive_n(self):
        with pytest.raises(ValueError, match="positive"):
            cyclic_voltage_cover([0, 1], [(0, 1)], n=0)
        with pytest.raises(ValueError):
            cyclic_voltage_cover([0, 1], [(0, 1)], n=-2)

    def test_raises_on_empty_vertices(self):
        with pytest.raises(ValueError, match="vertex"):
            cyclic_voltage_cover([], [], n=2)

    def test_raises_on_wrong_voltage_count(self):
        with pytest.raises(ValueError, match="voltage"):
            cyclic_voltage_cover([0, 1], [(0, 1)], n=2, voltages=[0, 1])

    def test_voltages_reduced_mod_n(self):
        verts = [0, 1]
        edges = [(0, 1)]
        cg = cyclic_voltage_cover(verts, edges, n=3, voltages=[7])
        assert cg.voltages[0] == 1   # 7 mod 3 == 1

    def test_returns_covering_graph_dataclass(self):
        cg = cyclic_voltage_cover([0, 1, 2], [(0, 1), (1, 2), (2, 0)], n=4)
        assert isinstance(cg, CoveringGraph)


# ---------------------------------------------------------------------------
# universal_covering_tree
# ---------------------------------------------------------------------------


class TestUniversalCoveringTree:
    def test_single_vertex_no_edges_only_root(self):
        verts, edges = universal_covering_tree([0], [], max_depth=3)
        assert len(verts) == 1
        assert len(edges) == 0
        assert verts[0] == (0,)

    def test_path_graph_same_as_itself(self):
        # A path is already a tree; its universal cover is itself
        cverts, cedges = universal_covering_tree([0, 1, 2], [(0, 1), (1, 2)], max_depth=4)
        # Should not duplicate any vertex
        assert len(cverts) == len(set(cverts))

    def test_triangle_cover_is_infinite_line(self):
        # Triangle has π₁ = ℤ; its universal cover is ℝ (infinite path)
        # With max_depth=4, we get a finite portion
        cverts, cedges = universal_covering_tree([0, 1, 2], [(0, 1), (1, 2), (2, 0)], max_depth=4)
        # Tree condition: no cycles
        assert len(cedges) == len(cverts) - 1

    def test_cover_is_a_tree(self):
        # Any universal cover of a connected graph is a tree
        for verts, edges in [
            ([0, 1, 2], [(0, 1), (1, 2), (2, 0)]),
            ([0], [(0, 0)]),
            ([0, 1, 2, 3], [(0, 1), (0, 2), (1, 2), (2, 3)]),
        ]:
            cverts, cedges = universal_covering_tree(verts, edges, max_depth=4)
            # Tree: |edges| == |vertices| - 1
            assert len(cedges) == len(cverts) - 1

    def test_max_depth_limits_output(self):
        cverts_2, _ = universal_covering_tree([0, 1, 2], [(0, 1), (1, 2), (2, 0)], max_depth=2)
        cverts_4, _ = universal_covering_tree([0, 1, 2], [(0, 1), (1, 2), (2, 0)], max_depth=4)
        assert len(cverts_2) <= len(cverts_4)

    def test_empty_graph_returns_empty(self):
        cverts, cedges = universal_covering_tree([], [], max_depth=3)
        assert cverts == []
        assert cedges == []

    def test_vertices_are_tuples_of_base_labels(self):
        cverts, _ = universal_covering_tree([0, 1], [(0, 1)], max_depth=3)
        for path in cverts:
            assert isinstance(path, tuple)
            for v in path:
                assert v in (0, 1)


# ---------------------------------------------------------------------------
# is_graph_covering_map
# ---------------------------------------------------------------------------


class TestIsGraphCoveringMap:
    def _build_cyclic_cover_projection(
        self,
        base_verts: list[int],
        base_edges: list[tuple[int, int]],
        n: int,
    ) -> tuple[list[tuple[int, int]], list[tuple[tuple[int, int], tuple[int, int]]], dict]:
        """Helper: project (v,k) → v for the trivial n-sheeted cover."""
        cg = cyclic_voltage_cover(base_verts, base_edges, n, voltages=[0] * len(base_edges))
        total_v = cg.cover_vertices
        total_e = cg.cover_edges
        proj = {(v, k): v for v, k in total_v}
        return total_v, total_e, proj

    def test_trivial_two_sheet_cover_of_triangle(self):
        bv = [0, 1, 2]
        be = [(0, 1), (1, 2), (2, 0)]
        tv, te, proj = self._build_cyclic_cover_projection(bv, be, 2)
        assert is_graph_covering_map(tv, te, bv, be, proj)

    def test_trivial_three_sheet_cover_of_edge(self):
        bv = [0, 1]
        be = [(0, 1)]
        tv, te, proj = self._build_cyclic_cover_projection(bv, be, 3)
        assert is_graph_covering_map(tv, te, bv, be, proj)

    def test_non_covering_map_rejected(self):
        # Map that sends all cover vertices to vertex 0 is not a covering map
        # (unless base has one vertex with self-loops of appropriate degree)
        bv = [0, 1]
        be = [(0, 1)]
        tv = [(0, 0), (0, 1), (1, 0), (1, 1)]
        te = [((0, 0), (1, 0)), ((0, 1), (1, 1))]
        proj: dict = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
        assert not is_graph_covering_map(tv, te, bv, be, proj)

    def test_missing_projection_entry_returns_false(self):
        bv = [0, 1]
        be = [(0, 1)]
        tv = [(0, 0), (1, 0)]
        te = [((0, 0), (1, 0))]
        proj: dict = {(0, 0): 0}   # (1,0) missing
        assert not is_graph_covering_map(tv, te, bv, be, proj)

    def test_base_not_fully_covered_returns_false(self):
        bv = [0, 1, 2]
        be = [(0, 1), (1, 2), (2, 0)]
        # Projection only covers vertex 0 and 1
        tv = [(0, 0), (1, 0)]
        te = [((0, 0), (1, 0))]
        proj: dict = {(0, 0): 0, (1, 0): 1}
        assert not is_graph_covering_map(tv, te, bv, be, proj)
