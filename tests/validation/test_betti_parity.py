"""P16.2/P16.3: pytop vs GUDHI/Ripser persistent Betti parity.

These are the *wired* oracle cross-checks that were previously "pending": they
build the same Vietoris-Rips filtration on both sides and assert that the Betti
number at every filtration scale agrees, for the dimensions the truncated
skeleton can represent faithfully (``H_k`` for ``k <= max_betti_dim``, with
simplices built up to dimension ``max_betti_dim + 1``).

Skipped gracefully when the oracle is not installed (``importorskip``).

See ``betti_parity.py`` for the correctness rationale (Betti-at-scale, not
death-count; skeleton dimension governs trustworthy ``H_k``).
"""

from __future__ import annotations

import math

import pytest

from tests.validation.betti_parity import (
    betti_at_scale,
    compare_betti,
    pytop_rips_bars,
)

# --------------------------------------------------------------------------
# Deterministic point-cloud fixtures
# --------------------------------------------------------------------------


def circle(n: int, *, radius: float = 1.0, center: tuple[float, float] = (0.0, 0.0)):
    """``n`` evenly spaced points on a circle (S^1)."""
    cx, cy = center
    return [
        (cx + radius * math.cos(2 * math.pi * k / n), cy + radius * math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]


def two_circles(n: int = 12):
    """Two disjoint circles far enough apart not to merge (H0 = H1 = 2)."""
    return circle(n, center=(0.0, 0.0)) + circle(n, center=(6.0, 0.0))


def icosahedron():
    """12 icosahedron vertices on the unit sphere (S^2: H0=1, H1=0, H2=1)."""
    phi = (1.0 + 5.0**0.5) / 2.0
    raw = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            raw.append((0.0, s1 * 1.0, s2 * phi))
            raw.append((s1 * 1.0, s2 * phi, 0.0))
            raw.append((s2 * phi, 0.0, s1 * 1.0))
    out = []
    for v in raw:
        norm = math.sqrt(sum(c * c for c in v))
        out.append(tuple(c / norm for c in v))
    return out


# --------------------------------------------------------------------------
# Sanity: pytop alone recovers the expected topology at a plateau scale
# --------------------------------------------------------------------------


class TestPytopRecoversTopology:
    def test_circle_is_a_loop(self):
        bars = pytop_rips_bars(circle(12), max_scale=2.0, max_betti_dim=1)
        assert betti_at_scale(bars, 0.9, 1) == {0: 1, 1: 1}

    def test_two_circles(self):
        bars = pytop_rips_bars(two_circles(12), max_scale=2.0, max_betti_dim=1)
        assert betti_at_scale(bars, 0.9, 1) == {0: 2, 1: 2}

    def test_sphere_has_a_void(self):
        bars = pytop_rips_bars(icosahedron(), max_scale=2.2, max_betti_dim=2)
        assert betti_at_scale(bars, 1.7, 2) == {0: 1, 1: 0, 2: 1}


# --------------------------------------------------------------------------
# GUDHI parity
# --------------------------------------------------------------------------


class TestGudhiParity:
    @staticmethod
    def _assert_full_agreement(points, *, max_scale, max_betti_dim):
        pytest.importorskip("gudhi")
        result = compare_betti(
            points, oracle="gudhi", max_scale=max_scale, max_betti_dim=max_betti_dim
        )
        # The comparison must actually sample something non-trivial.
        assert result.scales, "no comparison scales were generated"
        assert result.agree, f"pytop vs GUDHI disagreements: {result.disagreements()[:10]}"

    def test_circle(self):
        self._assert_full_agreement(circle(12), max_scale=2.0, max_betti_dim=1)

    def test_circle_dense(self):
        self._assert_full_agreement(circle(24), max_scale=1.6, max_betti_dim=1)

    def test_two_circles(self):
        self._assert_full_agreement(two_circles(12), max_scale=2.0, max_betti_dim=1)

    def test_sphere_h2(self):
        self._assert_full_agreement(icosahedron(), max_scale=2.2, max_betti_dim=2)

    def test_random_cloud(self):
        # Reproducible pseudo-random cloud — exercises generic agreement, no
        # special structure. Uses a fixed seed for determinism.
        import random

        rng = random.Random(20260623)
        pts = [(rng.uniform(0, 3), rng.uniform(0, 3)) for _ in range(20)]
        self._assert_full_agreement(pts, max_scale=1.5, max_betti_dim=1)


# --------------------------------------------------------------------------
# Ripser parity (skipped unless ripser is installed)
# --------------------------------------------------------------------------


class TestRipserParity:
    @staticmethod
    def _assert_full_agreement(points, *, max_scale, max_betti_dim):
        pytest.importorskip("ripser")
        result = compare_betti(
            points, oracle="ripser", max_scale=max_scale, max_betti_dim=max_betti_dim
        )
        assert result.scales, "no comparison scales were generated"
        assert result.agree, f"pytop vs Ripser disagreements: {result.disagreements()[:10]}"

    def test_circle(self):
        self._assert_full_agreement(circle(12), max_scale=2.0, max_betti_dim=1)

    def test_two_circles(self):
        self._assert_full_agreement(two_circles(12), max_scale=2.0, max_betti_dim=1)
