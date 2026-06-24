"""Tests for persistence_distances.py — bottleneck, Wasserstein, entropy, landscape."""

from __future__ import annotations

import math

import pytest

from pytop.persistence_distances import (
    bottleneck_distance,
    persistence_entropy,
    persistence_landscape,
    wasserstein_distance,
)
from pytop.persistent_homology import PersistencePair

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def pp(dim: int, birth: float, death: float) -> PersistencePair:
    return PersistencePair(dimension=dim, birth=birth, death=death)


def ppe(dim: int, birth: float) -> PersistencePair:
    """Essential persistence pair (infinite death)."""
    return PersistencePair(dimension=dim, birth=birth, death=math.inf)


EMPTY: tuple[PersistencePair, ...] = ()


# ---------------------------------------------------------------------------
# bottleneck_distance
# ---------------------------------------------------------------------------


class TestBottleneckDistance:
    def test_identical_diagrams(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(1, 0.5, 1.5))
        assert bottleneck_distance(d, d) == pytest.approx(0.0, abs=1e-9)

    def test_empty_vs_empty(self) -> None:
        assert bottleneck_distance(EMPTY, EMPTY) == pytest.approx(0.0)

    def test_empty_vs_single(self) -> None:
        # D2 has one point (0.2, 0.6); best match = diagonal → cost = 0.2
        d2 = (pp(0, 0.2, 0.6),)
        assert bottleneck_distance(EMPTY, d2) == pytest.approx(0.2)

    def test_single_vs_empty(self) -> None:
        d1 = (pp(0, 0.2, 0.6),)
        assert bottleneck_distance(d1, EMPTY) == pytest.approx(0.2)

    def test_close_points(self) -> None:
        # D1 = {(0,1)}, D2 = {(0.1, 0.9)} → optimal match costs L∞ = max(0.1,0.1) = 0.1
        d1 = (pp(0, 0.0, 1.0),)
        d2 = (pp(0, 0.1, 0.9),)
        assert bottleneck_distance(d1, d2) == pytest.approx(0.1, abs=1e-9)

    def test_symmetry(self) -> None:
        d1 = (pp(0, 0.0, 1.0), pp(1, 0.2, 0.8))
        d2 = (pp(0, 0.1, 0.9),)
        assert bottleneck_distance(d1, d2) == pytest.approx(bottleneck_distance(d2, d1))

    def test_triangle_inequality(self) -> None:
        d1 = (pp(0, 0.0, 1.0),)
        d2 = (pp(0, 0.1, 0.9),)
        d3 = (pp(0, 0.2, 0.8),)
        d_13 = bottleneck_distance(d1, d3)
        d_12 = bottleneck_distance(d1, d2)
        d_23 = bottleneck_distance(d2, d3)
        assert d_13 <= d_12 + d_23 + 1e-12

    def test_essential_bars_excluded(self) -> None:
        d1 = (pp(0, 0.0, 1.0), ppe(0, 0.0))
        d2 = (pp(0, 0.1, 0.9), ppe(0, 2.0))
        # Essential bars should be ignored → only finite bars matter
        assert bottleneck_distance(d1, d2) == pytest.approx(0.1, abs=1e-9)

    def test_degree_filter(self) -> None:
        d1 = (pp(0, 0.0, 2.0), pp(1, 0.0, 1.0))
        d2 = (pp(0, 0.0, 2.0), pp(1, 0.3, 0.7))
        # Only degree 1: (0,1) vs (0.3,0.7) → L∞ = max(0.3,0.3) = 0.3
        assert bottleneck_distance(d1, d2, degree=1) == pytest.approx(0.3, abs=1e-9)
        # Only degree 0: identical → 0
        assert bottleneck_distance(d1, d2, degree=0) == pytest.approx(0.0)

    def test_non_negative(self) -> None:
        d1 = (pp(0, 0.5, 1.5), pp(1, 0.1, 0.9))
        d2 = (pp(0, 0.0, 2.0),)
        assert bottleneck_distance(d1, d2) >= 0.0

    def test_two_vs_two_optimal(self) -> None:
        # Both diagrams have same two points → distance 0
        d = (pp(0, 0.0, 1.0), pp(0, 0.5, 1.5))
        assert bottleneck_distance(d, d) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# wasserstein_distance
# ---------------------------------------------------------------------------


class TestWassersteinDistance:
    def test_identical_diagrams(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(1, 0.5, 1.5))
        assert wasserstein_distance(d, d) == pytest.approx(0.0, abs=1e-9)

    def test_empty_vs_empty(self) -> None:
        assert wasserstein_distance(EMPTY, EMPTY) == pytest.approx(0.0)

    def test_empty_vs_single_p1(self) -> None:
        # D2 = {(0.2, 0.6)}: diagonal cost = 0.2; d_W^1 = 0.2
        d2 = (pp(0, 0.2, 0.6),)
        assert wasserstein_distance(EMPTY, d2, p=1) == pytest.approx(0.2, abs=1e-9)

    def test_close_points_p1(self) -> None:
        # D1 = {(0,1)}, D2 = {(0.1,0.9)}: optimal = match directly, cost = 0.1
        d1 = (pp(0, 0.0, 1.0),)
        d2 = (pp(0, 0.1, 0.9),)
        assert wasserstein_distance(d1, d2, p=1) == pytest.approx(0.1, abs=1e-9)

    def test_p2_close_points(self) -> None:
        d1 = (pp(0, 0.0, 1.0),)
        d2 = (pp(0, 0.1, 0.9),)
        # L∞ distance = 0.1, so d_W^2 = 0.1^2^(1/2) = 0.1
        assert wasserstein_distance(d1, d2, p=2) == pytest.approx(0.1, abs=1e-9)

    def test_p_less_than_1_raises(self) -> None:
        with pytest.raises(ValueError, match="p must be ≥ 1"):
            wasserstein_distance(EMPTY, EMPTY, p=0.5)

    def test_symmetry(self) -> None:
        d1 = (pp(0, 0.0, 1.0), pp(1, 0.2, 0.8))
        d2 = (pp(0, 0.1, 0.9),)
        assert wasserstein_distance(d1, d2, p=1) == pytest.approx(
            wasserstein_distance(d2, d1, p=1), abs=1e-9
        )

    def test_wasserstein_ge_zero(self) -> None:
        d1 = (pp(0, 0.5, 1.5), pp(1, 0.1, 0.9))
        d2 = (pp(0, 0.0, 2.0),)
        assert wasserstein_distance(d1, d2, p=1) >= 0.0

    def test_degree_filter(self) -> None:
        d1 = (pp(0, 0.0, 2.0), pp(1, 0.0, 1.0))
        d2 = (pp(0, 0.0, 2.0), pp(1, 0.5, 1.5))
        # Degree 0: identical → 0
        assert wasserstein_distance(d1, d2, p=1, degree=0) == pytest.approx(0.0)
        # Degree 1: (0,1) vs (0.5,1.5) → L∞ = max(0.5,0.5) = 0.5
        assert wasserstein_distance(d1, d2, p=1, degree=1) == pytest.approx(0.5, abs=1e-9)

    def test_wasserstein_vs_bottleneck_single_point(self) -> None:
        # For a single pair of points, Wasserstein-1 equals bottleneck
        d1 = (pp(0, 0.0, 1.0),)
        d2 = (pp(0, 0.2, 0.8),)
        assert wasserstein_distance(d1, d2, p=1) == pytest.approx(
            bottleneck_distance(d1, d2), abs=1e-9
        )


# ---------------------------------------------------------------------------
# persistence_entropy
# ---------------------------------------------------------------------------


class TestPersistenceEntropy:
    def test_empty_diagram(self) -> None:
        assert persistence_entropy(EMPTY) == pytest.approx(0.0)

    def test_single_bar(self) -> None:
        # Single bar: ratio = 1, entropy = -1*log(1) = 0
        d = (pp(0, 0.0, 1.0),)
        assert persistence_entropy(d) == pytest.approx(0.0, abs=1e-12)

    def test_two_equal_bars(self) -> None:
        # Two equal-length bars: p1 = p2 = 0.5, entropy = log(2)
        d = (pp(0, 0.0, 1.0), pp(0, 0.0, 1.0))
        assert persistence_entropy(d) == pytest.approx(math.log(2), abs=1e-9)

    def test_entropy_non_negative(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(1, 0.2, 0.8), pp(1, 0.1, 0.5))
        assert persistence_entropy(d) >= 0.0

    def test_essential_bars_excluded(self) -> None:
        d_finite = (pp(0, 0.0, 1.0), pp(0, 0.0, 1.0))
        d_with_essential = (pp(0, 0.0, 1.0), pp(0, 0.0, 1.0), ppe(0, 0.0))
        # Essential bar should not affect entropy
        assert persistence_entropy(d_with_essential) == pytest.approx(
            persistence_entropy(d_finite), abs=1e-12
        )

    def test_degree_filter(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(1, 0.0, 2.0), pp(1, 0.0, 2.0))
        # Degree 1 only: two equal-length bars → entropy = log(2)
        assert persistence_entropy(d, degree=1) == pytest.approx(math.log(2), abs=1e-9)

    def test_unequal_bars_entropy(self) -> None:
        # Bars of length 1, 1, 2: p = [0.25, 0.25, 0.5], L = 4
        # H = -2*(0.25*log(0.25)) - 0.5*log(0.5) = 2*0.25*log(4) + 0.5*log(2)
        d = (pp(0, 0.0, 1.0), pp(0, 0.0, 1.0), pp(0, 0.0, 2.0))
        expected = -2 * 0.25 * math.log(0.25) - 0.5 * math.log(0.5)
        assert persistence_entropy(d) == pytest.approx(expected, abs=1e-9)


# ---------------------------------------------------------------------------
# persistence_landscape
# ---------------------------------------------------------------------------


class TestPersistenceLandscape:
    def test_empty_diagram(self) -> None:
        ls = persistence_landscape(EMPTY, num_layers=2, num_grid_points=10)
        assert ls.num_layers == 2
        assert ls.grid_size == 10
        assert all(v == 0.0 for v in ls.layer(1))
        assert all(v == 0.0 for v in ls.layer(2))

    def test_single_bar_landscape(self) -> None:
        # Bar (0, 2): tent function peaks at t=1 with value 1.0
        d = (pp(0, 0.0, 2.0),)
        ls = persistence_landscape(d, num_layers=1, num_grid_points=5, t_min=0.0, t_max=2.0)
        layer = ls.layer(1)
        # Find the peak
        peak_idx = max(range(len(layer)), key=lambda i: layer[i])
        assert layer[peak_idx] == pytest.approx(1.0, abs=0.1)

    def test_layer_count(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(0, 0.2, 0.8), pp(0, 0.4, 0.6))
        ls = persistence_landscape(d, num_layers=3)
        assert ls.num_layers == 3

    def test_more_layers_than_bars_padded_with_zeros(self) -> None:
        d = (pp(0, 0.0, 1.0),)
        ls = persistence_landscape(d, num_layers=3, num_grid_points=20)
        assert ls.num_layers == 3
        assert all(v == 0.0 for v in ls.layer(2))
        assert all(v == 0.0 for v in ls.layer(3))

    def test_landscape_non_negative(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(1, 0.5, 1.5))
        ls = persistence_landscape(d, num_layers=2)
        for k in range(1, ls.num_layers + 1):
            assert all(v >= 0.0 for v in ls.layer(k))

    def test_layer_index_out_of_range(self) -> None:
        d = (pp(0, 0.0, 1.0),)
        ls = persistence_landscape(d, num_layers=1)
        with pytest.raises(IndexError):
            ls.layer(0)
        with pytest.raises(IndexError):
            ls.layer(2)

    def test_layer1_ge_layer2(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(0, 0.3, 0.7))
        ls = persistence_landscape(d, num_layers=2, num_grid_points=50)
        for v1, v2 in zip(ls.layer(1), ls.layer(2)):
            assert v1 >= v2 - 1e-12

    def test_invalid_num_layers_raises(self) -> None:
        with pytest.raises(ValueError, match="num_layers"):
            persistence_landscape(EMPTY, num_layers=0)

    def test_invalid_grid_points_raises(self) -> None:
        with pytest.raises(ValueError, match="num_grid_points"):
            persistence_landscape(EMPTY, num_grid_points=1)

    def test_grid_size_matches(self) -> None:
        d = (pp(0, 0.0, 1.0),)
        ls = persistence_landscape(d, num_grid_points=42)
        assert ls.grid_size == 42
        for k in range(1, ls.num_layers + 1):
            assert len(ls.layer(k)) == 42

    def test_degree_filter(self) -> None:
        d = (pp(0, 0.0, 1.0), pp(1, 0.0, 3.0))
        # Only degree 1 bar: peak should be larger (longer bar)
        ls1 = persistence_landscape(d, degree=1, num_layers=1, num_grid_points=50)
        ls0 = persistence_landscape(d, degree=0, num_layers=1, num_grid_points=50)
        assert max(ls1.layer(1)) > max(ls0.layer(1))


def test_persistence_entropy_hand_computed():
    """Lock the Shannon formula against a hand-computed 3-bar value (issue #6).

    Three bars with lifetimes 1, 1, 2 -> total length L = 4, so the normalized
    probabilities are p = [1/4, 1/4, 1/2]. With natural log,
        H = -(1/4 ln 1/4 + 1/4 ln 1/4 + 1/2 ln 1/2)
          = -(1/2 ln 1/4 + 1/2 ln 1/2)
          = (3/2) ln 2
          = 1.0397207708...
    """
    pairs = (
        PersistencePair(0, 0.0, 1.0),
        PersistencePair(0, 0.0, 1.0),
        PersistencePair(1, 0.0, 2.0),
    )
    assert persistence_entropy(pairs) == pytest.approx(1.5 * math.log(2))
