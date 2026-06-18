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
