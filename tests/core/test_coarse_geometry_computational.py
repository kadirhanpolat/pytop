"""Tests for coarse_geometry.py computational engines (growth, geodesic, tree, classification)."""

from __future__ import annotations

from pytop.coarse_geometry import (
    classify_graph_coarse_growth,
    geodesic_distance_graph,
    growth_function_graph,
    is_tree_graph,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _path(n: int) -> dict[int, list[int]]:
    """Path graph P_n on vertices 0..n-1."""
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for i in range(n - 1):
        adj[i].append(i + 1)
        adj[i + 1].append(i)
    return adj


def _cycle(n: int) -> dict[int, list[int]]:
    """Cycle graph C_n."""
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for i in range(n):
        j = (i + 1) % n
        adj[i].append(j)
        adj[j].append(i)
    return adj


def _complete(n: int) -> dict[int, list[int]]:
    """Complete graph K_n."""
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                adj[i].append(j)
    return adj


def _star(k: int) -> dict[int, list[int]]:
    """Star graph K_{1,k}: center 0, leaves 1..k."""
    adj: dict[int, list[int]] = {0: list(range(1, k + 1))}
    for i in range(1, k + 1):
        adj[i] = [0]
    return adj


def _grid(m: int, n: int) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """m×n grid graph."""
    adj: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for i in range(m):
        for j in range(n):
            v = (i, j)
            adj[v] = []
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    adj[v].append((ni, nj))
    return adj


# ---------------------------------------------------------------------------
# growth_function_graph
# ---------------------------------------------------------------------------

class TestGrowthFunctionGraph:
    def test_single_vertex(self):
        adj = {0: []}
        g = growth_function_graph(adj, 0, 3)
        assert g == {0: 1, 1: 1, 2: 1, 3: 1}

    def test_path_growth_linear(self):
        adj = _path(10)
        g = growth_function_graph(adj, 4, 5)
        assert g[0] == 1
        assert g[1] == 3   # center + 2 neighbors
        assert g[2] == 5
        assert g[5] == 10  # full path covered

    def test_star_growth(self):
        adj = _star(4)
        g = growth_function_graph(adj, 0, 3)
        assert g[0] == 1   # center only
        assert g[1] == 5   # center + 4 leaves
        assert g[2] == 5   # no further vertices
        assert g[3] == 5

    def test_grid_growth_approx_quadratic(self):
        adj = _grid(11, 11)
        g = growth_function_graph(adj, (5, 5), 5)
        # At radius r in Z^2, b(r) ≈ 2r^2 + 2r + 1
        assert g[1] == 5
        assert g[2] == 13

    def test_radius_zero(self):
        adj = _path(5)
        g = growth_function_graph(adj, 2, 0)
        assert g[0] == 1

    def test_returns_all_radii(self):
        adj = _path(5)
        g = growth_function_graph(adj, 0, 4)
        assert set(g.keys()) == {0, 1, 2, 3, 4}


# ---------------------------------------------------------------------------
# geodesic_distance_graph
# ---------------------------------------------------------------------------

class TestGeodesicDistanceGraph:
    def test_self_distance_zero(self):
        adj = _path(5)
        assert geodesic_distance_graph(adj, 2, 2) == 0

    def test_adjacent_distance_one(self):
        adj = _path(5)
        assert geodesic_distance_graph(adj, 0, 1) == 1

    def test_path_distance(self):
        adj = _path(10)
        assert geodesic_distance_graph(adj, 0, 9) == 9

    def test_unreachable_returns_minus_one(self):
        adj = {0: [], 1: []}  # two isolated vertices
        assert geodesic_distance_graph(adj, 0, 1) == -1

    def test_cycle_distance(self):
        adj = _cycle(8)
        d = geodesic_distance_graph(adj, 0, 4)
        assert d == 4  # diametrically opposite

    def test_complete_graph_all_distance_one(self):
        adj = _complete(5)
        for v in range(1, 5):
            assert geodesic_distance_graph(adj, 0, v) == 1

    def test_star_center_to_leaf(self):
        adj = _star(5)
        assert geodesic_distance_graph(adj, 0, 3) == 1

    def test_star_leaf_to_leaf(self):
        adj = _star(5)
        assert geodesic_distance_graph(adj, 1, 5) == 2


# ---------------------------------------------------------------------------
# is_tree_graph
# ---------------------------------------------------------------------------

class TestIsTreeGraph:
    def test_path_is_tree(self):
        assert is_tree_graph(_path(5)) is True

    def test_star_is_tree(self):
        assert is_tree_graph(_star(4)) is True

    def test_single_vertex_is_tree(self):
        assert is_tree_graph({0: []}) is True

    def test_edge_is_tree(self):
        assert is_tree_graph({0: [1], 1: [0]}) is True

    def test_cycle_is_not_tree(self):
        assert is_tree_graph(_cycle(4)) is False

    def test_complete_k4_is_not_tree(self):
        assert is_tree_graph(_complete(4)) is False

    def test_disconnected_is_not_tree(self):
        adj = {0: [1], 1: [0], 2: [], 3: []}
        assert is_tree_graph(adj) is False

    def test_empty_is_not_tree(self):
        assert is_tree_graph({}) is False

    def test_binary_tree_depth3(self):
        adj = {
            0: [1, 2],
            1: [0, 3, 4],
            2: [0, 5, 6],
            3: [1], 4: [1], 5: [2], 6: [2],
        }
        assert is_tree_graph(adj) is True

    def test_tree_with_cycle_added_is_not_tree(self):
        adj = dict(_path(5))
        adj[0].append(4)
        adj[4].append(0)
        assert is_tree_graph(adj) is False


# ---------------------------------------------------------------------------
# classify_graph_coarse_growth
# ---------------------------------------------------------------------------

class TestClassifyGraphCoarseGrowth:
    def test_path_polynomial_degree_1(self):
        adj = _path(20)
        r = classify_graph_coarse_growth(adj, 9, max_radius=8)
        assert r["growth_type"] == "polynomial"
        assert r["polynomial_degree"] == 1

    def test_grid_polynomial_degree_2(self):
        adj = _grid(11, 11)
        r = classify_graph_coarse_growth(adj, (5, 5), max_radius=5)
        assert r["growth_type"] == "polynomial"
        assert r["polynomial_degree"] == 2

    def test_path_is_tree(self):
        adj = _path(10)
        r = classify_graph_coarse_growth(adj, 4)
        assert r["is_tree"] is True

    def test_cycle_not_tree(self):
        adj = _cycle(10)
        r = classify_graph_coarse_growth(adj, 0)
        assert r["is_tree"] is False

    def test_vertex_and_edge_counts(self):
        adj = _path(5)
        r = classify_graph_coarse_growth(adj, 0)
        assert r["vertex_count"] == 5
        assert r["edge_count"] == 4

    def test_star_vertex_count(self):
        adj = _star(4)
        r = classify_graph_coarse_growth(adj, 0)
        assert r["vertex_count"] == 5
        assert r["edge_count"] == 4

    def test_growth_dict_present(self):
        adj = _path(10)
        r = classify_graph_coarse_growth(adj, 0, max_radius=5)
        assert "growth" in r
        assert 0 in r["growth"]

    def test_connected_path(self):
        adj = _path(10)
        r = classify_graph_coarse_growth(adj, 0)
        assert r["connected"] is True

    def test_disconnected_graph(self):
        adj = {0: [1], 1: [0], 2: [], 3: []}
        r = classify_graph_coarse_growth(adj, 0)
        assert r["connected"] is False
