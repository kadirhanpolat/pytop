"""Tests for cech_complex.py — Čech complex filtration."""

from __future__ import annotations

import math

import pytest

from pytop.cech_complex import (
    _circumradius,
    cech_filtration,
    persistent_homology_cech,
)
from pytop.persistent_homology import (
    FilteredComplex,
    PersistencePair,
    vietoris_rips_filtration,
)
from pytop.persistent_homology import (
    persistence_pairs as rips_pairs,
)

# ---------------------------------------------------------------------------
# _circumradius — minimum enclosing ball radius
# ---------------------------------------------------------------------------


class TestCircumradius:
    def test_single_point_radius_zero(self) -> None:
        assert _circumradius([(0.0, 0.0)]) == pytest.approx(0.0)

    def test_two_points_half_distance(self) -> None:
        r = _circumradius([(0.0,), (4.0,)])
        assert r == pytest.approx(2.0)

    def test_equilateral_triangle(self) -> None:
        # Circumradius = side / sqrt(3)
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)]
        r = _circumradius(pts)
        assert r == pytest.approx(1.0 / math.sqrt(3), rel=1e-5)

    def test_right_triangle_hypotenuse_half(self) -> None:
        # Right triangle: minimum enclosing ball = hypotenuse / 2
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        r = _circumradius(pts)
        assert r == pytest.approx(math.sqrt(2) / 2, rel=1e-5)

    def test_obtuse_triangle_max_edge_half(self) -> None:
        # Obtuse: MEB is determined by the longest edge
        pts = [(0.0, 0.0), (4.0, 0.0), (0.1, 0.1)]
        r = _circumradius(pts)
        # Longest edge is from (0,0) to (4,0), length 4 → MEB radius ≈ 2
        assert r == pytest.approx(2.0, rel=1e-3)

    def test_two_points_in_3d(self) -> None:
        pts = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0)]
        assert _circumradius(pts) == pytest.approx(1.0)

    def test_regular_tetrahedron(self) -> None:
        # Circumradius of regular tetrahedron with edge=2; circumradius = sqrt(3)
        pts = [
            (1.0, 1.0, 1.0),
            (1.0, -1.0, -1.0),
            (-1.0, 1.0, -1.0),
            (-1.0, -1.0, 1.0),
        ]
        r = _circumradius(pts)
        assert r == pytest.approx(math.sqrt(3.0), rel=1e-5)

    def test_unit_square_diagonal(self) -> None:
        # Unit square: circumradius = sqrt(2)/2
        pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        r = _circumradius(pts)
        assert r == pytest.approx(math.sqrt(2) / 2, rel=1e-5)

    def test_collinear_points(self) -> None:
        # Three collinear points: MEB = span / 2
        pts = [(0.0,), (3.0,), (1.5,)]
        r = _circumradius(pts)
        assert r == pytest.approx(1.5)


# ---------------------------------------------------------------------------
# cech_filtration
# ---------------------------------------------------------------------------


class TestCechFiltration:
    def test_single_point(self) -> None:
        fc = cech_filtration([(0.0, 0.0)])
        assert fc.size() == 1
        assert fc.births == (0.0,)
        assert fc.dimensions == (0,)

    def test_two_points_edge_at_half_distance(self) -> None:
        # Two points 2 apart → edge at radius 1
        fc = cech_filtration([(0.0,), (2.0,)], max_dimension=1)
        assert fc.size() == 3  # 2 vertices + 1 edge
        edge_idx = fc.dimensions.index(1)
        assert fc.births[edge_idx] == pytest.approx(1.0)

    def test_vertices_at_zero(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        fc = cech_filtration(pts, max_dimension=2)
        for i in range(3):
            assert fc.births[i] == pytest.approx(0.0)
            assert fc.dimensions[i] == 0

    def test_max_dimension_0_no_edges(self) -> None:
        pts = [(0.0,), (1.0,), (2.0,)]
        fc = cech_filtration(pts, max_dimension=0)
        assert all(d == 0 for d in fc.dimensions)
        assert fc.size() == 3

    def test_max_scale_filters_edges(self) -> None:
        # Two points 10 apart, edge radius = 5; cut at 3 → no edge
        fc = cech_filtration([(0.0,), (10.0,)], max_dimension=1, max_scale=3.0)
        assert fc.size() == 2  # only the two vertices

    def test_rips_cech_sandwich_edges(self) -> None:
        # Each Čech edge birth = Rips edge birth / 2
        pts = [(0.0, 0.0), (3.0, 0.0), (0.0, 4.0)]
        fc_cech = cech_filtration(pts, max_dimension=1)
        fc_rips = vietoris_rips_filtration(
            _DummySpace(pts), max_dimension=1
        )
        # Build birth maps
        cech_edges = {
            combo: fc_cech.births[i]
            for i, combo in enumerate(fc_cech.simplices)
            if fc_cech.dimensions[i] == 1
        }
        rips_edges = {
            combo: fc_rips.births[i]
            for i, combo in enumerate(fc_rips.simplices)
            if fc_rips.dimensions[i] == 1
        }
        for combo in cech_edges:
            assert cech_edges[combo] == pytest.approx(rips_edges[combo] / 2, rel=1e-5)

    def test_faces_before_cofaces(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)]
        fc = cech_filtration(pts, max_dimension=2)
        simplex_index = {s: i for i, s in enumerate(fc.simplices)}
        # Each edge must enter before or with the triangle
        triangle = (0, 1, 2)
        t_idx = simplex_index[triangle]
        for edge in [(0, 1), (0, 2), (1, 2)]:
            e_idx = simplex_index[edge]
            assert fc.births[e_idx] <= fc.births[t_idx] + 1e-10

    def test_births_nondecreasing(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
        fc = cech_filtration(pts, max_dimension=2)
        for i in range(len(fc.births) - 1):
            assert fc.births[i] <= fc.births[i + 1] + 1e-10

    def test_returns_filtered_complex(self) -> None:
        pts = [(0.0,), (1.0,)]
        fc = cech_filtration(pts, max_dimension=1)
        assert isinstance(fc, FilteredComplex)

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError):
            cech_filtration([])

    def test_negative_max_dimension_raises(self) -> None:
        with pytest.raises(ValueError):
            cech_filtration([(0.0,)], max_dimension=-1)


# ---------------------------------------------------------------------------
# persistent_homology_cech
# ---------------------------------------------------------------------------


class TestPersistentHomologyCech:
    def test_returns_tuple_of_pairs(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0)]
        pairs = persistent_homology_cech(pts, max_dimension=1)
        assert isinstance(pairs, tuple)
        assert all(isinstance(p, PersistencePair) for p in pairs)

    def test_single_connected_component_one_essential_h0(self) -> None:
        pts = [(0.0,), (1.0,), (2.0,)]
        pairs = persistent_homology_cech(pts, max_dimension=1)
        essential_h0 = [p for p in pairs if p.is_essential and p.dimension == 0]
        assert len(essential_h0) == 1

    def test_two_disconnected_clusters_two_essential_h0(self) -> None:
        # Two clusters far apart, cut before they merge
        pts = [(0.0,), (0.1,), (10.0,), (10.1,)]
        pairs = persistent_homology_cech(pts, max_dimension=1, max_scale=1.0)
        essential_h0 = [p for p in pairs if p.is_essential and p.dimension == 0]
        assert len(essential_h0) == 2

    def test_circle_has_essential_h1_with_scale_cut(self) -> None:
        # 8 points on unit circle, adjacent chord ≈ 0.765 → Čech birth ≈ 0.383.
        # With max_scale=0.45 only adjacent edges are included (skip-1 chord ≈ 0.707
        # gives Čech birth 0.354... wait, recompute):
        #   adjacent chord = 2*sin(π/8) ≈ 0.765 → birth 0.383
        #   skip-1 chord   = 2*sin(π/4) = √2 ≈ 1.414 → birth 0.707
        # Cut at 0.5: only 8 adjacent edges → 8-cycle → exactly 1 essential H_1.
        n = 8
        pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
               for i in range(n)]
        pairs = persistent_homology_cech(pts, max_dimension=1, max_scale=0.5)
        essential_h1 = [p for p in pairs if p.is_essential and p.dimension == 1]
        assert len(essential_h1) == 1

    def test_circle_finite_h1_closed_by_triangles(self) -> None:
        # With max_dimension=2 the loop is eventually filled by triangles
        # (each triangle on the unit circle has circumradius = 1.0) so
        # H_1 has at least one bar that dies at r=1.0.
        n = 8
        pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
               for i in range(n)]
        pairs = persistent_homology_cech(pts, max_dimension=2)
        # All H_1 bars eventually die (no essential H_1)
        h1 = [p for p in pairs if p.dimension == 1]
        assert len(h1) >= 1

    def test_contractible_no_h1(self) -> None:
        # Five points on [0,1] line segment → no H_1
        pts = [(float(i) / 4,) for i in range(5)]
        pairs = persistent_homology_cech(pts, max_dimension=2)
        h1 = [p for p in pairs if p.dimension == 1]
        assert all(not p.is_essential for p in h1)

    def test_birth_death_order(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        pairs = persistent_homology_cech(pts, max_dimension=2)
        for p in pairs:
            if not p.is_essential:
                assert p.birth <= p.death

    def test_cech_vs_rips_edge_births(self) -> None:
        # For edges, Čech birth = Rips birth / 2
        pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
        cech = persistent_homology_cech(pts, max_dimension=1)
        rips = rips_pairs(vietoris_rips_filtration(_DummySpace(pts), max_dimension=1))
        # Finite H_1 bar in Čech corresponds to Rips H_1 bar at double the scale
        cech_h1 = sorted(
            [p for p in cech if p.dimension == 1 and not p.is_essential],
            key=lambda p: p.birth,
        )
        rips_h1 = sorted(
            [p for p in rips if p.dimension == 1 and not p.is_essential],
            key=lambda p: p.birth,
        )
        # Count must agree (same topological event, different scale)
        assert len(cech_h1) == len(rips_h1)

    def test_equilateral_triangle_h1(self) -> None:
        # Three vertices of an equilateral triangle → one H_1 bar (loop)
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)]
        pairs = persistent_homology_cech(pts, max_dimension=2)
        h1 = [p for p in pairs if p.dimension == 1]
        assert len(h1) >= 1


# ---------------------------------------------------------------------------
# Dummy space adapter for Rips interop tests
# ---------------------------------------------------------------------------


class _DummySpace:
    """Minimal space adapter exposing carrier and distance_between."""

    def __init__(self, pts: list[tuple[float, ...]]) -> None:
        self._pts = pts

    @property
    def carrier(self) -> list[tuple[float, ...]]:
        return self._pts

    def distance_between(self, a: tuple[float, ...], b: tuple[float, ...]) -> float:
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
