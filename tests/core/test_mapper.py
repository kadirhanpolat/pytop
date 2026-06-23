"""Tests for mapper.py — Mapper algorithm for topological data analysis."""

from __future__ import annotations

import math

import pytest

from pytop.mapper import (
    IntervalCover,
    MapperComplex,
    MapperNode,
    mapper,
    single_linkage_labels,
)

# ---------------------------------------------------------------------------
# IntervalCover
# ---------------------------------------------------------------------------


class TestIntervalCover:
    def test_intervals_cover_range(self) -> None:
        cover = IntervalCover(low=0.0, high=1.0, num_intervals=5, overlap_fraction=0.5)
        intervals = cover.intervals()
        # First interval starts at or before 0.0, last ends at or after 1.0
        assert intervals[0][0] <= 0.0
        assert intervals[-1][1] >= 1.0

    def test_num_intervals(self) -> None:
        cover = IntervalCover(low=0.0, high=1.0, num_intervals=4, overlap_fraction=0.25)
        assert len(cover.intervals()) == 4

    def test_overlap_means_adjacent_intervals_intersect(self) -> None:
        cover = IntervalCover(low=0.0, high=1.0, num_intervals=4, overlap_fraction=0.3)
        intervals = cover.intervals()
        for i in range(len(intervals) - 1):
            a_next, _ = intervals[i + 1]
            _, b_curr = intervals[i]
            assert b_curr > a_next, "Adjacent intervals should overlap"

    def test_interval_for_returns_correct_indices(self) -> None:
        cover = IntervalCover(low=0.0, high=1.0, num_intervals=2, overlap_fraction=0.5)
        # Midpoint of the range should be in both intervals
        mid = 0.5
        indices = cover.interval_for(mid)
        assert len(indices) >= 1

    def test_invalid_num_intervals_raises(self) -> None:
        with pytest.raises(ValueError, match="num_intervals"):
            IntervalCover(low=0.0, high=1.0, num_intervals=0, overlap_fraction=0.5)

    def test_invalid_overlap_raises(self) -> None:
        with pytest.raises(ValueError, match="overlap_fraction"):
            IntervalCover(low=0.0, high=1.0, num_intervals=5, overlap_fraction=0.0)
        with pytest.raises(ValueError, match="overlap_fraction"):
            IntervalCover(low=0.0, high=1.0, num_intervals=5, overlap_fraction=1.0)

    def test_low_ge_high_raises(self) -> None:
        with pytest.raises(ValueError, match="low must be"):
            IntervalCover(low=1.0, high=0.0, num_intervals=5, overlap_fraction=0.5)


# ---------------------------------------------------------------------------
# single_linkage_labels
# ---------------------------------------------------------------------------


class TestSingleLinkageLabels:
    def test_empty(self) -> None:
        assert single_linkage_labels([], gap_threshold=1.0) == []

    def test_single_point(self) -> None:
        labels = single_linkage_labels([0.5], gap_threshold=1.0)
        assert labels == [0]

    def test_two_close_points_one_cluster(self) -> None:
        labels = single_linkage_labels([0.0, 0.1], gap_threshold=1.0)
        assert labels[0] == labels[1]

    def test_two_distant_points_two_clusters(self) -> None:
        labels = single_linkage_labels([0.0, 5.0], gap_threshold=1.0)
        assert labels[0] != labels[1]

    def test_three_points_two_clusters(self) -> None:
        # 0.0, 0.1 close; 5.0 separate
        labels = single_linkage_labels([0.0, 0.1, 5.0], gap_threshold=1.0)
        assert labels[0] == labels[1]
        assert labels[0] != labels[2]

    def test_inf_gap_all_one_cluster(self) -> None:
        labels = single_linkage_labels([1.0, 2.0, 100.0], gap_threshold=math.inf)
        assert len(set(labels)) == 1


# ---------------------------------------------------------------------------
# MapperNode
# ---------------------------------------------------------------------------


class TestMapperNode:
    def test_len(self) -> None:
        node = MapperNode(interval_index=0, cluster_index=0, members=frozenset([0, 1, 2]))
        assert len(node) == 3


# ---------------------------------------------------------------------------
# MapperComplex
# ---------------------------------------------------------------------------


class TestMapperComplex:
    def _simple_complex(self) -> MapperComplex:
        n0 = MapperNode(0, 0, frozenset([0, 1]))
        n1 = MapperNode(1, 0, frozenset([1, 2]))
        simplices = frozenset([frozenset([0]), frozenset([1]), frozenset([0, 1])])
        return MapperComplex(nodes=(n0, n1), simplices=simplices, filter_values=(0.0, 1.0, 2.0))

    def test_num_nodes(self) -> None:
        mc = self._simple_complex()
        assert mc.num_nodes == 2

    def test_num_edges(self) -> None:
        mc = self._simple_complex()
        assert mc.num_edges == 1

    def test_edges(self) -> None:
        mc = self._simple_complex()
        assert mc.edges() == [(0, 1)]

    def test_connected_components_one_component(self) -> None:
        mc = self._simple_complex()
        components = mc.connected_components()
        assert len(components) == 1
        assert components[0] == frozenset([0, 1])

    def test_connected_components_two_components(self) -> None:
        n0 = MapperNode(0, 0, frozenset([0]))
        n1 = MapperNode(1, 0, frozenset([1]))
        simplices = frozenset([frozenset([0]), frozenset([1])])
        mc = MapperComplex(nodes=(n0, n1), simplices=simplices, filter_values=(0.0, 1.0))
        components = mc.connected_components()
        assert len(components) == 2


# ---------------------------------------------------------------------------
# mapper — integration tests
# ---------------------------------------------------------------------------


class TestMapper:
    def test_empty_data(self) -> None:
        mc = mapper([], filter_fn=lambda x: float(x))
        assert mc.num_nodes == 0
        assert mc.num_edges == 0

    def test_single_point(self) -> None:
        mc = mapper([1.0], filter_fn=lambda x: x)
        assert mc.num_nodes >= 1

    def test_line_data_linear_filter(self) -> None:
        # Points evenly spaced on [0, 1]; filter = identity
        data = [i / 9 for i in range(10)]
        mc = mapper(data, filter_fn=lambda x: x, num_intervals=3, overlap_fraction=0.3)
        assert mc.num_nodes >= 3  # at least one cluster per interval

    def test_two_clusters_produce_disconnected_graph(self) -> None:
        # Two clearly separated groups: [0..0.1] and [0.9..1.0]
        data = [0.0, 0.05, 0.1, 0.9, 0.95, 1.0]
        mc = mapper(data, filter_fn=lambda x: x, num_intervals=5, overlap_fraction=0.3)
        # Should produce at least 2 connected components
        components = mc.connected_components()
        assert len(components) >= 2

    def test_circle_x_filter_produces_nodes_with_edges(self) -> None:
        """Points on a circle with x-coordinate filter produce a connected Mapper graph.

        The x-filter f(x,y)=x collapses the top/bottom arc into each bin.
        With gap_threshold=inf (one cluster per bin), adjacent bins overlap
        and share points, producing a simple path graph.
        """
        import math
        n = 20
        data = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]
        mc = mapper(
            data, filter_fn=lambda xy: xy[0],
            num_intervals=4, overlap_fraction=0.4,
            gap_threshold=math.inf,
        )
        # With one cluster per interval and sufficient overlap, Mapper graph is connected
        assert mc.num_nodes >= 2
        assert mc.num_edges >= 1
        components = mc.connected_components()
        assert len(components) == 1

    def test_filter_values_stored(self) -> None:
        data = [1.0, 2.0, 3.0]
        mc = mapper(data, filter_fn=lambda x: x)
        assert len(mc.filter_values) == 3

    def test_custom_cover(self) -> None:
        data = [float(i) for i in range(10)]
        cover = IntervalCover(low=0.0, high=9.0, num_intervals=3, overlap_fraction=0.3)
        mc = mapper(data, filter_fn=lambda x: x, cover=cover)
        assert mc.num_nodes >= 3

    def test_max_simplex_dim_1_no_triangles(self) -> None:
        # Generate three mutually overlapping clusters
        data = [0.0, 0.5, 1.0, 1.5, 2.0]
        mc = mapper(data, filter_fn=lambda x: x, num_intervals=4, overlap_fraction=0.6,
                    max_simplex_dim=1)
        # No 2-simplex (triangle) should exist
        triangles = [s for s in mc.simplices if len(s) == 3]
        assert triangles == []

    def test_gap_threshold_override(self) -> None:
        # Large gap_threshold → all points in each bin form one cluster
        data = [0.0, 0.05, 0.1, 0.5, 0.9, 1.0]
        mc = mapper(data, filter_fn=lambda x: x, num_intervals=3, overlap_fraction=0.3,
                    gap_threshold=math.inf)
        # Each non-empty interval should produce exactly 1 cluster
        for node in mc.nodes:
            assert node.cluster_index == 0

    def test_custom_cluster_fn(self) -> None:
        # Cluster function that always puts everything in one cluster
        def all_one_cluster(fvals: list[float], indices: list[int]) -> list[int]:
            return [0] * len(fvals)

        data = [float(i) for i in range(6)]
        mc = mapper(data, filter_fn=lambda x: x, num_intervals=3, overlap_fraction=0.3,
                    cluster_fn=all_one_cluster)
        for node in mc.nodes:
            assert node.cluster_index == 0

    def test_all_nodes_are_zero_simplices(self) -> None:
        data = [float(i) for i in range(5)]
        mc = mapper(data, filter_fn=lambda x: x, num_intervals=3, overlap_fraction=0.4)
        zero_simplices = {next(iter(s)) for s in mc.simplices if len(s) == 1}
        assert zero_simplices == set(range(mc.num_nodes))

    def test_edge_exists_iff_shared_member(self) -> None:
        data = list(range(10))
        mc = mapper(data, filter_fn=float, num_intervals=3, overlap_fraction=0.3)
        for i, j in mc.edges():
            shared = mc.nodes[i].members & mc.nodes[j].members
            assert shared, f"Edge ({i},{j}) but no shared members"
