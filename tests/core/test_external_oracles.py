"""Differential tests against independent external oracles (Phase 4 — P4.4).

Internal cross-checks (P4.1) are strong but share pytop's own code and
conventions, so they cannot catch a *shared* assumption. These tests pin pytop
against **truly independent** implementations:

* **sympy** — exact Smith normal form / determinant / rank, vs `exact_linalg`.
* **networkx** — Boyer–Myrvold planarity, vs `is_planar`.
* **numpy** — eigenvalue signature, vs the Sturm/Sylvester `signature` routine.

These are *test-only* oracles: pytop's runtime stays dependency-free. Each block
is skipped (not failed) when its oracle is not installed, so the suite is green
on a minimal install and exercises the agreement wherever the tools are present.
"""

from __future__ import annotations

import random
from itertools import combinations

import pytest

from pytop import (
    integer_determinant,
    integer_rank,
    is_planar,
    signature,
    smith_normal_form,
)
from pytop.knot_invariants import KnotDiagram
from pytop.seifert import _sylvester_signature

try:
    import sympy
    from sympy import Matrix as SympyMatrix
    from sympy.matrices.normalforms import smith_normal_form as sympy_snf

    HAVE_SYMPY = True
except ImportError:  # pragma: no cover
    HAVE_SYMPY = False

try:
    import networkx as nx

    HAVE_NETWORKX = True
except ImportError:  # pragma: no cover
    HAVE_NETWORKX = False

try:
    import numpy as np

    HAVE_NUMPY = True
except ImportError:  # pragma: no cover
    HAVE_NUMPY = False

try:
    import flint

    HAVE_FLINT = True
except ImportError:  # pragma: no cover
    HAVE_FLINT = False

try:
    import gudhi

    HAVE_GUDHI = True
except ImportError:  # pragma: no cover
    HAVE_GUDHI = False


def _random_matrix(rng, rows, cols, lo=-5, hi=5):
    return [[rng.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]


# ---------------------------------------------------------------------------
# sympy — exact linear algebra
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HAVE_SYMPY, reason="sympy not installed")
class TestSympyExactLinalg:
    def test_smith_normal_form_matches_sympy(self):
        rng = random.Random(1)
        for _ in range(40):
            rows, cols = rng.randint(1, 4), rng.randint(1, 4)
            matrix = _random_matrix(rng, rows, cols)
            normal = sympy_snf(SympyMatrix(matrix), domain=sympy.ZZ)
            sympy_factors = [
                abs(int(normal[i, i]))
                for i in range(min(rows, cols))
                if normal[i, i] != 0
            ]
            assert smith_normal_form(matrix) == sympy_factors

    def test_determinant_matches_sympy(self):
        rng = random.Random(2)
        for _ in range(50):
            n = rng.randint(1, 5)
            matrix = _random_matrix(rng, n, n)
            assert integer_determinant(matrix) == int(SympyMatrix(matrix).det())

    def test_rank_matches_sympy(self):
        rng = random.Random(3)
        for _ in range(50):
            rows, cols = rng.randint(1, 5), rng.randint(1, 5)
            matrix = _random_matrix(rng, rows, cols)
            assert integer_rank(matrix) == SympyMatrix(matrix).rank()


# ---------------------------------------------------------------------------
# networkx — planarity
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HAVE_NETWORKX, reason="networkx not installed")
class TestNetworkxPlanarity:
    def test_known_graphs(self):
        k5 = list(combinations(range(5), 2))
        k33 = [(i, j) for i in range(3) for j in range(3, 6)]
        k4 = list(combinations(range(4), 2))
        for edges in (k5, k33, k4):
            assert is_planar(edges) == nx.check_planarity(nx.Graph(edges))[0]

    def test_random_small_graphs_match_networkx(self):
        # pytop's exact genus search is exponential, so keep graphs small/sparse.
        rng = random.Random(4)
        for _ in range(40):
            n = rng.randint(3, 5)
            all_edges = list(combinations(range(n), 2))
            edges = [e for e in all_edges if rng.random() < 0.6]
            if not edges:
                continue
            graph = nx.Graph(edges)
            assert is_planar(edges) == nx.check_planarity(graph)[0]


# ---------------------------------------------------------------------------
# numpy — signature via eigenvalues
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HAVE_NUMPY, reason="numpy not installed")
class TestNumpySignature:
    @staticmethod
    def _numpy_signature(symmetric):
        eigenvalues = np.linalg.eigvalsh(np.array(symmetric, dtype=float))
        positive = int(sum(1 for e in eigenvalues if e > 1e-9))
        negative = int(sum(1 for e in eigenvalues if e < -1e-9))
        return positive - negative

    def test_sylvester_signature_matches_numpy(self):
        rng = random.Random(5)
        checked = 0
        for _ in range(60):
            n = rng.randint(1, 5)
            matrix = _random_matrix(rng, n, n, lo=-4, hi=4)
            symmetric = [
                [matrix[i][j] + matrix[j][i] for j in range(n)] for i in range(n)
            ]
            if integer_determinant(symmetric) == 0:
                continue  # skip singular: a zero eigenvalue is float-ambiguous
            as_float = [[float(x) for x in row] for row in symmetric]
            assert _sylvester_signature(as_float) == self._numpy_signature(symmetric)
            checked += 1
        assert checked >= 10

    def test_knot_signature_matches_numpy(self):
        # σ(K) = signature of M + Mᵀ; compare to numpy's eigenvalue count.
        trefoil = KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))
        figure_eight = KnotDiagram(
            [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)], signs=(1, -1, 1, -1)
        )
        from pytop.seifert import seifert_matrix

        for diagram in (trefoil, figure_eight):
            matrix = seifert_matrix(diagram)
            n = len(matrix)
            symmetric = [
                [matrix[i][j] + matrix[j][i] for j in range(n)] for i in range(n)
            ]
            assert signature(diagram) == self._numpy_signature(symmetric)


# ---------------------------------------------------------------------------
# python-flint — exact linear algebra (a second independent exact oracle)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HAVE_FLINT, reason="python-flint not installed")
class TestFlintExactLinalg:
    def test_determinant_and_rank_match_flint(self):
        rng = random.Random(6)
        for _ in range(50):
            n = rng.randint(1, 5)
            matrix = _random_matrix(rng, n, n)
            fm = flint.fmpz_mat(matrix)
            assert integer_determinant(matrix) == int(fm.det())
            assert integer_rank(matrix) == fm.rank()

    def test_smith_normal_form_matches_flint(self):
        rng = random.Random(7)
        for _ in range(40):
            n = rng.randint(1, 4)
            matrix = _random_matrix(rng, n, n)
            normal = flint.fmpz_mat(matrix).snf()
            factors = [
                abs(int(normal[i, i])) for i in range(n) if int(normal[i, i]) != 0
            ]
            assert smith_normal_form(matrix) == factors

    def test_snf_acceleration_paths_agree(self):
        # The optional flint-accelerated SNF backend must equal the pure-Python
        # routine on both square and rectangular matrices (boundary matrices are
        # rectangular), so the speed path is exact.
        from pytop.homology import _smith_normal_form_flint, _smith_normal_form_python

        rng = random.Random(11)
        for _ in range(40):
            rows, cols = rng.randint(1, 6), rng.randint(1, 6)
            matrix = _random_matrix(rng, rows, cols)
            assert _smith_normal_form_python(matrix) == _smith_normal_form_flint(matrix)


# ---------------------------------------------------------------------------
# GUDHI — Vietoris–Rips persistent homology
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HAVE_GUDHI, reason="gudhi not installed")
class TestGudhiPersistence:
    @staticmethod
    def _pytop_finite_bars(points, max_dim, max_scale, tol=1e-6):
        import math

        from pytop import persistent_homology
        from pytop.metric_spaces import FiniteMetricSpace

        space = FiniteMetricSpace(carrier=tuple(points), distance=math.dist)
        pairs = persistent_homology(space, max_dimension=max_dim, max_scale=max_scale)
        bars: dict[int, list] = {}
        for p in pairs:
            if p.death < max_scale - tol and p.death - p.birth > tol:
                bars.setdefault(p.dimension, []).append((p.birth, p.death))
        return {d: sorted(v) for d, v in bars.items()}

    @staticmethod
    def _gudhi_finite_bars(points, max_dim, max_scale, tol=1e-6):
        rips = gudhi.RipsComplex(points=points, max_edge_length=max_scale)
        tree = rips.create_simplex_tree(max_dimension=max_dim)
        tree.compute_persistence()
        bars: dict[int, list] = {}
        for dim, (birth, death) in tree.persistence():
            if death != float("inf") and death < max_scale - tol and death - birth > tol:
                bars.setdefault(dim, []).append((birth, death))
        return {d: sorted(v) for d, v in bars.items()}

    def _assert_agree(self, points, max_dim=2, max_scale=1.9):
        pytop_bars = self._pytop_finite_bars(points, max_dim, max_scale)
        gudhi_bars = self._gudhi_finite_bars(points, max_dim, max_scale)
        assert set(pytop_bars) == set(gudhi_bars)
        for dim in pytop_bars:
            pytop_d = pytop_bars[dim]
            gudhi_d = gudhi_bars[dim]
            assert len(pytop_d) == len(gudhi_d), f"dim {dim}: {len(pytop_d)} vs {len(gudhi_d)}"
            for (b1, d1), (b2, d2) in zip(pytop_d, gudhi_d):
                assert abs(b1 - b2) < 1e-6 and abs(d1 - d2) < 1e-6

    def test_circle_h1(self):
        import math

        points = [(math.cos(2 * math.pi * k / 12), math.sin(2 * math.pi * k / 12)) for k in range(12)]
        self._assert_agree(points, max_dim=2, max_scale=1.9)

    def test_random_clouds(self):
        rng = random.Random(8)
        for _ in range(5):
            points = [(rng.uniform(0, 2), rng.uniform(0, 2)) for _ in range(9)]
            self._assert_agree(points, max_dim=2, max_scale=1.2)

    @staticmethod
    def _pytop_cohomology_finite_bars(points, max_dim, max_scale, tol=1e-6):
        import math

        from pytop.metric_spaces import FiniteMetricSpace
        from pytop.persistent_homology import vietoris_rips_filtration
        from pytop.persistent_homology_optimized import persistence_pairs_cohomology

        space = FiniteMetricSpace(carrier=tuple(points), distance=math.dist)
        filtered = vietoris_rips_filtration(space, max_dimension=max_dim, max_scale=max_scale)
        pairs = persistence_pairs_cohomology(filtered)
        bars: dict[int, list] = {}
        for p in pairs:
            if p.death < max_scale - tol and p.death - p.birth > tol:
                bars.setdefault(p.dimension, []).append((p.birth, p.death))
        return {d: sorted(v) for d, v in bars.items()}

    def test_cohomology_matches_gudhi(self):
        # The dual (persistent cohomology) engine must also agree with GUDHI.
        import math

        points = [(math.cos(2 * math.pi * k / 12), math.sin(2 * math.pi * k / 12)) for k in range(12)]
        coh_bars = self._pytop_cohomology_finite_bars(points, 2, 1.9)
        gudhi_bars = self._gudhi_finite_bars(points, 2, 1.9)
        assert set(coh_bars) == set(gudhi_bars)
        for dim in coh_bars:
            assert len(coh_bars[dim]) == len(gudhi_bars[dim])
            for (b1, d1), (b2, d2) in zip(coh_bars[dim], gudhi_bars[dim]):
                assert abs(b1 - b2) < 1e-6 and abs(d1 - d2) < 1e-6
