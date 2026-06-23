"""Known-answer tests for the constructive persistent-homology engine."""

from __future__ import annotations

import math

import pytest

from pytop import (
    betti_numbers,
    euler_characteristic_curve,
    persistent_homology,
    vietoris_rips_filtration,
)
from pytop.metric_spaces import FiniteMetricSpace
from pytop.persistent_homology import barcode, persistence_diagram
from pytop.simplicial_complexes import generated_subcomplex


def _euclidean(a, b):
    return math.dist(a, b)


def _metric_space(points):
    return FiniteMetricSpace(carrier=tuple(points), distance=_euclidean)


def _circle_points(n):
    return [
        (math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]


# --------------------------------------------------------------------------
# Two well-separated clusters -> H0 shows the inter-cluster gap
# --------------------------------------------------------------------------

def test_two_clusters_h0():
    points = [(0.0, 0.0), (0.0, 0.3), (5.0, 0.0), (5.0, 0.3)]
    pairs = persistent_homology(_metric_space(points), max_dimension=1)

    h0 = [p for p in pairs if p.dimension == 0]
    essential = [p for p in h0 if p.is_essential]
    finite_deaths = sorted(p.death for p in h0 if not p.is_essential)

    # one connected component survives forever
    assert len(essential) == 1
    # three merges: two intra-cluster at 0.3, one inter-cluster at 5.0
    assert finite_deaths == pytest.approx([0.3, 0.3, 5.0])


# --------------------------------------------------------------------------
# Points sampled on a circle -> a single dominant H1 bar
# --------------------------------------------------------------------------

def test_circle_has_one_long_h1_bar():
    n = 12
    pairs = persistent_homology(_metric_space(_circle_points(n)), max_dimension=2)

    h1 = [p for p in pairs if p.dimension == 1]
    assert len(h1) >= 1

    longest = max(h1, key=lambda p: p.persistence)
    nearest_neighbor = 2 * math.sin(math.pi / n)  # birth scale of the loop
    assert longest.birth == pytest.approx(nearest_neighbor, abs=0.05)
    assert longest.persistence > 0.3


def test_circle_h0_merges_at_nearest_neighbor():
    n = 12
    pairs = persistent_homology(_metric_space(_circle_points(n)), max_dimension=2)

    h0 = [p for p in pairs if p.dimension == 0]
    essential = [p for p in h0 if p.is_essential]
    finite_deaths = [p.death for p in h0 if not p.is_essential]

    nearest_neighbor = 2 * math.sin(math.pi / n)
    assert len(essential) == 1
    assert len(finite_deaths) == n - 1
    assert finite_deaths == pytest.approx([nearest_neighbor] * (n - 1))


# --------------------------------------------------------------------------
# Cross-check with the homology engine (Faz 1): essential bars at the top of a
# dimension-capped filtration equal the Betti numbers of the resulting complex.
# --------------------------------------------------------------------------

def test_essential_bars_match_homology_engine():
    # 4 points, 1-skeleton only (no triangles): the filtration tops out at K4's
    # 1-skeleton, whose homology is H0 = Z, H1 = Z^3.
    points = [(0.0, 0.0), (0.0, 0.3), (5.0, 0.0), (5.0, 0.3)]
    pairs = persistent_homology(_metric_space(points), max_dimension=1)

    essential_h0 = sum(1 for p in pairs if p.dimension == 0 and p.is_essential)
    essential_h1 = sum(1 for p in pairs if p.dimension == 1 and p.is_essential)

    edges = [{i, j} for i in range(4) for j in range(i + 1, 4)]
    k4_skeleton = generated_subcomplex(edges)
    betti = betti_numbers(k4_skeleton)

    assert essential_h0 == betti[0] == 1
    assert essential_h1 == betti[1] == 3


# --------------------------------------------------------------------------
# Euler characteristic curve sanity
# --------------------------------------------------------------------------

def test_barcode_and_diagram():
    points = [(0.0, 0.0), (0.0, 0.3), (5.0, 0.0), (5.0, 0.3)]
    pairs = persistent_homology(_metric_space(points), max_dimension=1)

    h0_bars = barcode(pairs, dimension=0)
    # the connected component lives forever, and the clusters merge at 5.0
    assert (0.0, math.inf) in h0_bars
    assert any(death == pytest.approx(5.0) for _, death in h0_bars)

    diagram = persistence_diagram(pairs)
    assert 0 in diagram
    # every bar in the diagram appears in the flat barcode too
    assert len(barcode(pairs)) == sum(len(bars) for bars in diagram.values())


def test_euler_characteristic_curve_starts_at_vertex_count():
    points = [(0.0, 0.0), (0.0, 0.3), (5.0, 0.0), (5.0, 0.3)]
    filtered = vietoris_rips_filtration(_metric_space(points), max_dimension=1)
    curve = euler_characteristic_curve(filtered, scales=(0.0, 10.0))

    # at scale 0 only the four vertices exist -> chi = 4
    assert curve[0] == (0.0, 4)
    # at a large scale all 4 vertices and 6 edges are present -> chi = 4 - 6 = -2
    assert curve[1] == (10.0, -2)


# ---------------------------------------------------------------------------
# Inductive Vietoris-Rips construction (P17.3): correctness invariants.
#
# The filtration is built by inductive clique expansion over the neighborhood
# graph rather than exhaustive C(n, k+1) enumeration. These tests lock in the
# invariants the optimization must preserve.
# ---------------------------------------------------------------------------


def _brute_force_rips(points, max_dimension, max_scale):
    """Reference filtration via exhaustive subset enumeration (O(n^(k+2)))."""
    from itertools import combinations

    n = len(points)
    entries = [(0.0, 0, (i,)) for i in range(n)]
    for k in range(1, max_dimension + 1):
        for combo in combinations(range(n), k + 1):
            birth = max(math.dist(points[a], points[b]) for a, b in combinations(combo, 2))
            if max_scale is not None and birth > max_scale:
                continue
            entries.append((birth, k, combo))
    entries.sort(key=lambda e: (e[0], e[1], e[2]))
    return (
        tuple(e[2] for e in entries),
        tuple(e[0] for e in entries),
        tuple(e[1] for e in entries),
    )


@pytest.mark.parametrize("max_dimension", [0, 1, 2, 3])
@pytest.mark.parametrize("max_scale", [0.8, 1.5, None])
def test_inductive_rips_matches_brute_force(max_dimension, max_scale):
    points = _circle_points(13) + [(0.2, 0.1), (-0.3, 0.4), (0.5, -0.2)]
    filtered = vietoris_rips_filtration(
        _metric_space(points), max_dimension=max_dimension, max_scale=max_scale
    )
    bf_simplices, bf_births, bf_dims = _brute_force_rips(
        points, max_dimension, max_scale
    )
    assert filtered.simplices == bf_simplices
    assert filtered.births == bf_births
    assert filtered.dimensions == bf_dims


def test_inductive_rips_respects_max_scale_and_diameters():
    points = _circle_points(20)
    max_scale = 1.0
    filtered = vietoris_rips_filtration(
        _metric_space(points), max_dimension=2, max_scale=max_scale
    )
    for simplex, birth in zip(filtered.simplices, filtered.births):
        # birth is exactly the simplex diameter (max pairwise distance)...
        if len(simplex) >= 2:
            from itertools import combinations

            diameter = max(
                math.dist(points[a], points[b]) for a, b in combinations(simplex, 2)
            )
            assert birth == pytest.approx(diameter)
        # ...and no simplex exceeds the truncation scale.
        assert birth <= max_scale + 1e-12


def test_inductive_rips_vertices_only_for_dim_zero():
    points = _circle_points(8)
    filtered = vietoris_rips_filtration(
        _metric_space(points), max_dimension=0, max_scale=2.0
    )
    assert all(d == 0 for d in filtered.dimensions)
    assert len(filtered.simplices) == len(points)
