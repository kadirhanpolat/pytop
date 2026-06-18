"""Tests for the Twist algorithm with Clearing Lemma.

Every test either:
  - Cross-validates against the standard left-to-right reduction, or
  - Checks a known mathematical answer (matching test_persistent_homology_engine.py).

The Twist algorithm must produce *identical* output to the standard algorithm.
"""

from __future__ import annotations

import math

import pytest

from pytop.persistent_homology import (
    FilteredComplex,
    PersistencePair,
    persistence_pairs,
    vietoris_rips_filtration,
    barcode,
    persistence_diagram,
)
from pytop.persistent_homology_optimized import (
    ReductionStats,
    persistence_pairs_twist,
    persistence_pairs_twist_with_stats,
    persistent_homology_optimized,
)
from pytop.metric_spaces import FiniteMetricSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _euclidean(a, b):
    return math.dist(a, b)


def _metric_space(points):
    return FiniteMetricSpace(carrier=tuple(points), distance=_euclidean)


def _circle_points(n):
    return [
        (math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]


def _two_cluster_space():
    return _metric_space([(0.0, 0.0), (0.0, 0.3), (5.0, 0.0), (5.0, 0.3)])


def _cross_validate(filtered: FilteredComplex, **kwargs) -> None:
    """Assert Twist output equals standard output on the same FilteredComplex."""
    expected = persistence_pairs(filtered, **kwargs)
    got = persistence_pairs_twist(filtered, **kwargs)
    assert got == expected, (
        f"Twist result differs from standard.\n"
        f"Standard: {expected}\n"
        f"Twist:    {got}"
    )


# ---------------------------------------------------------------------------
# ReductionStats
# ---------------------------------------------------------------------------

class TestReductionStats:
    def test_is_frozen_dataclass(self):
        stats = ReductionStats(
            n_simplices=10, n_cleared=3, n_column_additions=7,
            n_finite_pairs=2, n_essential=1,
        )
        with pytest.raises(Exception):
            stats.n_cleared = 999  # type: ignore[misc]

    def test_clearing_ratio_zero_simplices(self):
        stats = ReductionStats(0, 0, 0, 0, 0)
        assert stats.clearing_ratio == 0.0

    def test_clearing_ratio(self):
        stats = ReductionStats(
            n_simplices=10, n_cleared=4, n_column_additions=0,
            n_finite_pairs=2, n_essential=0,
        )
        assert stats.clearing_ratio == pytest.approx(0.4)

    def test_n_pairs_is_sum(self):
        stats = ReductionStats(
            n_simplices=10, n_cleared=3, n_column_additions=5,
            n_finite_pairs=3, n_essential=2,
        )
        assert stats.n_pairs == 5

    def test_n_pairs_zero(self):
        assert ReductionStats(0, 0, 0, 0, 0).n_pairs == 0

    def test_clearing_ratio_full_clearing(self):
        stats = ReductionStats(
            n_simplices=8, n_cleared=8, n_column_additions=0,
            n_finite_pairs=4, n_essential=0,
        )
        assert stats.clearing_ratio == pytest.approx(1.0)

    def test_all_fields_accessible(self):
        stats = ReductionStats(
            n_simplices=5, n_cleared=2, n_column_additions=3,
            n_finite_pairs=1, n_essential=1,
        )
        assert stats.n_simplices == 5
        assert stats.n_cleared == 2
        assert stats.n_column_additions == 3
        assert stats.n_finite_pairs == 1
        assert stats.n_essential == 1


# ---------------------------------------------------------------------------
# Empty and trivial filtrations
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_filtration_twist(self):
        f = FilteredComplex(simplices=(), births=(), dimensions=())
        assert persistence_pairs_twist(f) == ()

    def test_empty_filtration_with_stats(self):
        f = FilteredComplex(simplices=(), births=(), dimensions=())
        pairs, stats = persistence_pairs_twist_with_stats(f)
        assert pairs == ()
        assert stats.n_simplices == 0
        assert stats.n_cleared == 0
        assert stats.n_column_additions == 0
        assert stats.n_pairs == 0

    def test_single_vertex_essential(self):
        f = FilteredComplex(simplices=((0,),), births=(0.0,), dimensions=(0,))
        pairs = persistence_pairs_twist(f)
        assert len(pairs) == 1
        assert pairs[0].dimension == 0
        assert pairs[0].birth == 0.0
        assert pairs[0].is_essential

    def test_two_vertices_one_essential(self):
        f = FilteredComplex(
            simplices=((0,), (1,)),
            births=(0.0, 0.0),
            dimensions=(0, 0),
        )
        pairs = persistence_pairs_twist(f)
        essential = [p for p in pairs if p.is_essential]
        assert len(essential) == 2

    def test_single_edge_creates_pair(self):
        # Vertex 0, Vertex 1, Edge 0-1
        f = FilteredComplex(
            simplices=((0,), (1,), (0, 1)),
            births=(0.0, 0.0, 1.0),
            dimensions=(0, 1, 1),
        )
        # FilteredComplex doesn't enforce dim = simplex_size - 1, but our
        # algorithm uses the dimensions field.  Manually set dim for vertices = 0
        # and edge = 1.
        # Actually simplex (0,1) has dim=1 as per the tuple above.
        f2 = FilteredComplex(
            simplices=((0,), (1,), (0, 1)),
            births=(0.0, 0.0, 1.0),
            dimensions=(0, 0, 1),
        )
        pairs = persistence_pairs_twist(f2)
        finite = [p for p in pairs if not p.is_essential]
        essential = [p for p in pairs if p.is_essential]
        assert len(finite) == 1
        assert finite[0].birth == pytest.approx(0.0)
        assert finite[0].death == pytest.approx(1.0)
        assert len(essential) == 1


# ---------------------------------------------------------------------------
# Cross-validation against standard algorithm — dim 1
# ---------------------------------------------------------------------------

class TestCrossValidationDim1:
    def test_two_clusters(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=1)
        _cross_validate(filtered)

    def test_circle_n6(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(6)), max_dimension=1
        )
        _cross_validate(filtered)

    def test_circle_n12(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(12)), max_dimension=1
        )
        _cross_validate(filtered)

    def test_three_collinear_points(self):
        space = _metric_space([(0.0,), (1.0,), (3.0,)])
        filtered = vietoris_rips_filtration(space, max_dimension=1)
        _cross_validate(filtered)

    def test_four_points_square(self):
        space = _metric_space([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        filtered = vietoris_rips_filtration(space, max_dimension=1)
        _cross_validate(filtered)

    def test_single_cluster_five_points(self):
        import math as m
        pts = [(m.cos(2 * m.pi * k / 5), m.sin(2 * m.pi * k / 5)) for k in range(5)]
        filtered = vietoris_rips_filtration(_metric_space(pts), max_dimension=1)
        _cross_validate(filtered)

    def test_with_max_scale(self):
        filtered = vietoris_rips_filtration(
            _two_cluster_space(), max_dimension=1, max_scale=1.0
        )
        _cross_validate(filtered)

    def test_include_zero_persistence(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=1)
        _cross_validate(filtered, include_zero_persistence=True)


# ---------------------------------------------------------------------------
# Cross-validation — dim 2 (triangles)
# ---------------------------------------------------------------------------

class TestCrossValidationDim2:
    def test_circle_n8_dim2(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(8)), max_dimension=2
        )
        _cross_validate(filtered)

    def test_two_clusters_dim2(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=2)
        _cross_validate(filtered)

    def test_five_points_pentagon_dim2(self):
        import math as m
        pts = [(m.cos(2 * m.pi * k / 5), m.sin(2 * m.pi * k / 5)) for k in range(5)]
        filtered = vietoris_rips_filtration(_metric_space(pts), max_dimension=2)
        _cross_validate(filtered)

    def test_four_points_tetrahedron(self):
        # Regular tetrahedron inscribed in the unit sphere
        pts = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
        filtered = vietoris_rips_filtration(_metric_space(pts), max_dimension=2)
        _cross_validate(filtered)

    def test_circle_n12_dim2(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(12)), max_dimension=2
        )
        _cross_validate(filtered)


# ---------------------------------------------------------------------------
# Known-answer tests (matching test_persistent_homology_engine.py)
# ---------------------------------------------------------------------------

class TestKnownAnswers:
    def test_two_clusters_h0_deaths(self):
        pairs = persistent_homology_optimized(_two_cluster_space(), max_dimension=1)
        h0 = [p for p in pairs if p.dimension == 0]
        finite_deaths = sorted(p.death for p in h0 if not p.is_essential)
        essential = [p for p in h0 if p.is_essential]
        assert len(essential) == 1
        assert finite_deaths == pytest.approx([0.3, 0.3, 5.0])

    def test_circle_n12_has_long_h1_bar(self):
        n = 12
        pairs = persistent_homology_optimized(
            _metric_space(_circle_points(n)), max_dimension=2
        )
        h1 = [p for p in pairs if p.dimension == 1]
        assert len(h1) >= 1
        longest = max(h1, key=lambda p: p.persistence)
        nearest_neighbor = 2 * math.sin(math.pi / n)
        assert longest.birth == pytest.approx(nearest_neighbor, abs=0.05)
        assert longest.persistence > 0.3

    def test_circle_n12_h0_merges(self):
        n = 12
        pairs = persistent_homology_optimized(
            _metric_space(_circle_points(n)), max_dimension=2
        )
        h0 = [p for p in pairs if p.dimension == 0]
        essential = [p for p in h0 if p.is_essential]
        finite_deaths = [p.death for p in h0 if not p.is_essential]
        nearest_neighbor = 2 * math.sin(math.pi / n)
        assert len(essential) == 1
        assert len(finite_deaths) == n - 1
        assert finite_deaths == pytest.approx([nearest_neighbor] * (n - 1))

    def test_two_clusters_essential_h0_survives(self):
        pairs = persistent_homology_optimized(_two_cluster_space(), max_dimension=1)
        h0 = [p for p in pairs if p.dimension == 0]
        assert sum(1 for p in h0 if p.is_essential) == 1

    def test_three_isolated_points_all_essential(self):
        space = _metric_space([(0.0,), (10.0,), (20.0,)])
        pairs = persistent_homology_optimized(space, max_dimension=0, max_scale=0.0)
        essential = [p for p in pairs if p.is_essential]
        assert len(essential) == 3

    def test_barcode_output_compatible(self):
        """Twist pairs can be fed into the standard barcode() helper."""
        pairs = persistent_homology_optimized(_two_cluster_space(), max_dimension=1)
        h0_bars = barcode(pairs, dimension=0)
        assert (0.0, math.inf) in h0_bars
        assert any(death == pytest.approx(5.0) for _, death in h0_bars)

    def test_persistence_diagram_output_compatible(self):
        pairs = persistent_homology_optimized(_two_cluster_space(), max_dimension=1)
        diagram = persistence_diagram(pairs)
        assert 0 in diagram
        assert len(barcode(pairs)) == sum(len(bars) for bars in diagram.values())


# ---------------------------------------------------------------------------
# Clearing Lemma effect: cleared > 0 on non-trivial inputs
# ---------------------------------------------------------------------------

class TestClearingLemmaStats:
    def test_two_clusters_clears_some_columns(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=1)
        _, stats = persistence_pairs_twist_with_stats(filtered)
        # At minimum the 3 vertices killed by edges are cleared.
        assert stats.n_cleared >= 3

    def test_circle_n12_clears_some_columns(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(12)), max_dimension=2
        )
        _, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_cleared > 0

    def test_single_vertex_no_clearing(self):
        f = FilteredComplex(simplices=((0,),), births=(0.0,), dimensions=(0,))
        _, stats = persistence_pairs_twist_with_stats(f)
        assert stats.n_cleared == 0

    def test_stats_n_simplices_matches_filtered(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=1)
        _, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_simplices == filtered.size()

    def test_stats_n_finite_plus_essential_equals_n_pairs(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=1)
        pairs, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_finite_pairs + stats.n_essential == len(pairs)
        assert stats.n_pairs == len(pairs)

    def test_clearing_ratio_between_zero_and_one(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(8)), max_dimension=2
        )
        _, stats = persistence_pairs_twist_with_stats(filtered)
        assert 0.0 <= stats.clearing_ratio <= 1.0

    def test_dim2_has_more_clearing_than_dim1(self):
        """Higher max_dimension → more cross-dimensional clearing opportunities."""
        space = _metric_space(_circle_points(8))
        f1 = vietoris_rips_filtration(space, max_dimension=1)
        f2 = vietoris_rips_filtration(space, max_dimension=2)
        _, s1 = persistence_pairs_twist_with_stats(f1)
        _, s2 = persistence_pairs_twist_with_stats(f2)
        # dim-2 complex has strictly more simplices and more clearing chances.
        assert s2.n_simplices >= s1.n_simplices
        assert s2.n_cleared >= s1.n_cleared

    def test_column_additions_nonnegative(self):
        filtered = vietoris_rips_filtration(_two_cluster_space(), max_dimension=2)
        _, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_column_additions >= 0


# ---------------------------------------------------------------------------
# persistent_homology_optimized — interface tests
# ---------------------------------------------------------------------------

class TestPersistentHomologyOptimized:
    def test_returns_tuple_of_pairs(self):
        pairs = persistent_homology_optimized(_two_cluster_space(), max_dimension=1)
        assert isinstance(pairs, tuple)
        assert all(isinstance(p, PersistencePair) for p in pairs)

    def test_sorted_by_dimension_birth_death(self):
        pairs = persistent_homology_optimized(
            _metric_space(_circle_points(8)), max_dimension=2
        )
        keys = [(p.dimension, p.birth, p.death) for p in pairs]
        assert keys == sorted(keys)

    def test_max_scale_limits_simplices(self):
        pairs_no_limit = persistent_homology_optimized(
            _two_cluster_space(), max_dimension=1
        )
        pairs_limited = persistent_homology_optimized(
            _two_cluster_space(), max_dimension=1, max_scale=0.5
        )
        assert len(pairs_limited) <= len(pairs_no_limit)

    def test_max_dimension_zero_only_vertices(self):
        pairs = persistent_homology_optimized(_two_cluster_space(), max_dimension=0)
        assert all(p.dimension == 0 for p in pairs)

    def test_matches_standard_persistent_homology(self):
        from pytop.persistent_homology import persistent_homology as ph_std
        space = _metric_space(_circle_points(8))
        expected = ph_std(space, max_dimension=2)
        got = persistent_homology_optimized(space, max_dimension=2)
        assert got == expected

    def test_include_zero_persistence(self):
        pairs_with = persistent_homology_optimized(
            _two_cluster_space(), max_dimension=1, include_zero_persistence=True
        )
        pairs_without = persistent_homology_optimized(
            _two_cluster_space(), max_dimension=1, include_zero_persistence=False
        )
        assert len(pairs_with) >= len(pairs_without)
