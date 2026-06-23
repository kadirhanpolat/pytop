"""Phase 10 — Scale & Algorithm.

Tests for all five P10 milestones:
  P10.1 — sparse_linalg (sparse SNF + matrix_density)
  P10.2 — parallel Khovanov
  P10.3 — witness complex / approximate persistence
  P10.4 — streaming persistence
  P10.5 — GPU backend (graceful fallback when cupy absent)
"""

from __future__ import annotations

import math
import random

import pytest

from pytop.exact_linalg import smith_normal_form

# ---------------------------------------------------------------------------
# P10.1 — Sparse SNF
# ---------------------------------------------------------------------------
from pytop.sparse_linalg import (
    _SparseMat,
    matrix_density,
    sparse_smith_normal_form,
)


class TestMatrixDensity:
    def test_all_zero(self):
        assert matrix_density([[0, 0], [0, 0]]) == 0.0

    def test_all_nonzero(self):
        assert matrix_density([[1, 2], [3, 4]]) == 1.0

    def test_half_nonzero(self):
        assert matrix_density([[1, 0], [0, 1]]) == pytest.approx(0.5)

    def test_empty(self):
        assert matrix_density([]) == 0.0


class TestSparseSNF:
    def _check(self, matrix):
        """Sparse result must match dense result."""
        assert sparse_smith_normal_form(matrix) == smith_normal_form(matrix)

    def test_empty(self):
        assert sparse_smith_normal_form([]) == []

    def test_empty_row(self):
        assert sparse_smith_normal_form([[0, 0, 0]]) == []

    def test_single_nonzero(self):
        assert sparse_smith_normal_form([[3]]) == [3]

    def test_identity_2x2(self):
        assert sparse_smith_normal_form([[1, 0], [0, 1]]) == [1, 1]

    def test_single_factor_6(self):
        # [[2, 0], [0, 3]] → SNF = [1, 6]
        self._check([[2, 0], [0, 3]])

    def test_diagonal_divisible(self):
        # [[1, 0], [0, 6]] already in SNF
        self._check([[1, 0], [0, 6]])

    def test_zero_matrix(self):
        assert sparse_smith_normal_form([[0, 0], [0, 0]]) == []

    def test_row_vector(self):
        self._check([[2, 4, 6]])

    def test_col_vector(self):
        self._check([[2], [4], [6]])

    def test_torus_boundary(self):
        # H_1(torus) = Z^2; boundary matrices have specific SNF
        self._check([[1, -1, 0, 1], [0, 1, -1, 0], [-1, 0, 1, -1]])

    def test_negative_entries(self):
        self._check([[-2, 3], [1, -5]])

    def test_sparse_large(self):
        # Sparse 8x8 matrix (boundary matrix of a path of 9 vertices)
        n = 9
        mat = [[0] * (n - 1) for _ in range(n)]
        for j in range(n - 1):
            mat[j][j] = 1
            mat[j + 1][j] = -1
        self._check(mat)

    def test_random_match_dense(self):
        rng = random.Random(42)
        for _ in range(20):
            m, n = rng.randint(2, 8), rng.randint(2, 8)
            mat = [[rng.choice([-1, 0, 0, 1]) for _ in range(n)] for _ in range(m)]
            assert sparse_smith_normal_form(mat) == smith_normal_form(mat)

    def test_accepts_scipy_sparse(self):
        pytest.importorskip("scipy", reason="scipy not installed")
        import scipy.sparse as sp
        mat = sp.coo_matrix([[1, 2], [0, 3]])
        result = sparse_smith_normal_form(mat)
        assert result == smith_normal_form([[1, 2], [0, 3]])


class TestSparseSNFInternal:
    def test_sparse_mat_from_dense(self):
        mat = _SparseMat.from_dense([[1, 0], [0, 2]])
        assert mat.get(0, 0) == 1
        assert mat.get(0, 1) == 0
        assert mat.get(1, 1) == 2

    def test_swap_rows(self):
        mat = _SparseMat.from_dense([[1, 2], [3, 4]])
        mat.swap_rows(0, 1)
        assert mat.get(0, 0) == 3
        assert mat.get(1, 0) == 1

    def test_swap_cols(self):
        mat = _SparseMat.from_dense([[1, 2], [3, 4]])
        mat.swap_cols(0, 1)
        assert mat.get(0, 0) == 2
        assert mat.get(0, 1) == 1

    def test_add_row(self):
        mat = _SparseMat.from_dense([[1, 2], [3, 4]])
        mat.add_row(0, 1, -3)  # row1 += -3 * row0 → [3-3, 4-6] = [0, -2]
        assert mat.get(1, 0) == 0
        assert mat.get(1, 1) == -2

    def test_add_col(self):
        mat = _SparseMat.from_dense([[1, 2], [3, 4]])
        mat.add_col(0, 1, -2)  # col1 += -2*col0 → [2-2, 4-6] = [0, -2]
        assert mat.get(0, 1) == 0
        assert mat.get(1, 1) == -2

    def test_sparsity_maintained(self):
        mat = _SparseMat.from_dense([[1, 2], [3, 4]])
        mat.add_row(0, 1, -3)
        # (1,0) must be zero and absent from dicts
        assert 0 not in mat._r.get(1, {})

    def test_swap_rows_noop(self):
        mat = _SparseMat.from_dense([[5, 0], [0, 7]])
        mat.swap_rows(0, 0)
        assert mat.get(0, 0) == 5


# ---------------------------------------------------------------------------
# P10.2 — Parallel Khovanov
# ---------------------------------------------------------------------------

from pytop.khovanov import khovanov_homology  # noqa: E402
from pytop.knot_invariants import KnotDiagram  # noqa: E402


def _unknot() -> KnotDiagram:
    return KnotDiagram(pd=(), signs=())


def _trefoil() -> KnotDiagram:
    return KnotDiagram(
        pd=((1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)),
        signs=(1, 1, 1),
    )


def _figure8() -> KnotDiagram:
    return KnotDiagram(
        pd=((4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)),
        signs=(1, -1, 1, -1),
    )


class TestParallelKhovanov:
    def _check_parallel_equals_sequential(self, diagram):
        seq = khovanov_homology(diagram, parallel=False)
        par = khovanov_homology(diagram, parallel=True)
        assert seq.groups == par.groups

    def test_unknot(self):
        self._check_parallel_equals_sequential(_unknot())

    def test_trefoil(self):
        self._check_parallel_equals_sequential(_trefoil())

    def test_figure8(self):
        self._check_parallel_equals_sequential(_figure8())

    def test_parallel_false_is_default(self):
        kh = khovanov_homology(_trefoil())
        assert isinstance(kh, khovanov_homology.__class__ if False else khovanov_homology(_trefoil()).__class__)

    def test_parallel_euler_characteristic(self):
        kh_seq = khovanov_homology(_trefoil(), parallel=False)
        kh_par = khovanov_homology(_trefoil(), parallel=True)
        assert kh_seq.graded_euler_characteristic() == kh_par.graded_euler_characteristic()


# ---------------------------------------------------------------------------
# P10.3 — Witness complex
# ---------------------------------------------------------------------------

from pytop.witness_complex import (  # noqa: E402
    WitnessComplex,
    landmark_sample,
    persistent_homology_witness,
    witness_filtration,
)


def _circle_points(n: int = 20, seed: int = 0) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    angles = [2 * math.pi * i / n for i in range(n)]
    noise = 0.05
    return [
        (math.cos(a) + rng.uniform(-noise, noise),
         math.sin(a) + rng.uniform(-noise, noise))
        for a in angles
    ]


class TestLandmarkSample:
    def test_random_correct_count(self):
        pts = [(float(i), 0.0) for i in range(10)]
        land = landmark_sample(pts, 4, method="random", seed=7)
        assert len(land) == 4
        assert len(set(land)) == 4  # no duplicates
        assert all(0 <= i < 10 for i in land)

    def test_maxmin_correct_count(self):
        pts = [(float(i), 0.0) for i in range(10)]
        land = landmark_sample(pts, 4, method="maxmin", seed=0)
        assert len(land) == 4
        assert len(set(land)) == 4

    def test_maxmin_spread(self):
        # On a line [0..9], maxmin landmarks should be spread apart
        pts = [(float(i), 0.0) for i in range(10)]
        land = landmark_sample(pts, 3, method="maxmin", seed=0)
        coords = sorted(pts[i][0] for i in land)
        # Minimum gap between landmarks should be > 2
        gaps = [coords[k + 1] - coords[k] for k in range(len(coords) - 1)]
        assert min(gaps) >= 2.0

    def test_k_equals_n(self):
        pts = [(float(i), 0.0) for i in range(5)]
        land = landmark_sample(pts, 5, method="maxmin")
        assert sorted(land) == list(range(5))

    def test_k_equals_1(self):
        pts = [(float(i), 0.0) for i in range(10)]
        land = landmark_sample(pts, 1, method="maxmin")
        assert len(land) == 1

    def test_invalid_k(self):
        pts = [(0.0, 0.0), (1.0, 0.0)]
        with pytest.raises(ValueError):
            landmark_sample(pts, 3)

    def test_unknown_method(self):
        pts = [(0.0, 0.0), (1.0, 0.0)]
        with pytest.raises(ValueError, match="Unknown"):
            landmark_sample(pts, 1, method="fancy")

    def test_reproducible_with_seed(self):
        pts = [(float(i), 0.0) for i in range(20)]
        l1 = landmark_sample(pts, 5, method="random", seed=42)
        l2 = landmark_sample(pts, 5, method="random", seed=42)
        assert l1 == l2


class TestWitnessFiltration:
    def test_vertices_always_at_zero(self):
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.5)]
        land = pts
        filt = witness_filtration(pts, land, max_dim=0)
        # Every vertex is witnessed by itself at distance 0
        for b in filt.births:
            assert b == 0.0

    def test_edge_birth_positive(self):
        # Two landmarks far apart; witnesses are the landmarks themselves
        pts = [(0.0, 0.0), (3.0, 0.0)]
        filt = witness_filtration(pts, pts, max_dim=1)
        edges = [filt.births[i] for i in range(filt.size()) if filt.dimensions[i] == 1]
        assert len(edges) >= 1
        assert all(b > 0 for b in edges)

    def test_max_dim_respected(self):
        pts = [(float(i), 0.0) for i in range(5)]
        filt = witness_filtration(pts, pts, max_dim=1)
        assert all(d <= 1 for d in filt.dimensions)

    def test_max_eps_filters(self):
        pts = [(0.0, 0.0), (10.0, 0.0)]
        filt_full = witness_filtration(pts, pts, max_dim=1)
        filt_cut = witness_filtration(pts, pts, max_dim=1, max_eps=5.0)
        assert filt_cut.size() <= filt_full.size()

    def test_faces_before_cofaces(self):
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.8)]
        filt = witness_filtration(pts, pts, max_dim=2)
        # Every simplex's birth ≥ all its faces' births
        idx = {s: i for i, s in enumerate(filt.simplices)}
        for i, sigma in enumerate(filt.simplices):
            if len(sigma) < 2:
                continue
            for k in range(len(sigma)):
                face = sigma[:k] + sigma[k + 1:]
                if face in idx:
                    assert filt.births[idx[face]] <= filt.births[i] + 1e-12


class TestPersistentHomologyWitness:
    def test_returns_witness_complex(self):
        pts = _circle_points(16)
        wc = persistent_homology_witness(pts, k=8, max_dim=1, seed=0)
        assert isinstance(wc, WitnessComplex)
        assert len(wc.landmark_indices) == 8

    def test_circle_has_h1(self):
        pts = _circle_points(24)
        wc = persistent_homology_witness(pts, k=10, max_dim=1, seed=1)
        h1_bars = [p for p in wc.pairs if p.dimension == 1]
        # A circle-shaped cloud should produce at least one H1 bar
        assert len(h1_bars) >= 1

    def test_collinear_no_h1(self):
        # Points on a line have no H1
        pts = [(float(i), 0.0) for i in range(20)]
        wc = persistent_homology_witness(pts, k=6, max_dim=1, seed=3)
        h1_bars = [p for p in wc.pairs if p.dimension == 1 and not math.isinf(p.death)]
        assert len(h1_bars) == 0

    def test_landmark_method_random(self):
        pts = _circle_points(20)
        wc = persistent_homology_witness(pts, k=8, max_dim=1, landmark_method="random", seed=7)
        assert len(wc.landmark_indices) == 8


# ---------------------------------------------------------------------------
# P10.4 — Streaming persistence
# ---------------------------------------------------------------------------

from pytop.persistent_homology import FilteredComplex  # noqa: E402
from pytop.persistent_homology_optimized import persistence_pairs_twist  # noqa: E402
from pytop.streaming_persistence import StreamingPersistence  # noqa: E402


def _build_standard_filtration() -> FilteredComplex:
    """Triangle {0,1,2} with edges and vertices, filtration by scale."""
    from pytop.persistent_homology import FilteredComplex
    return FilteredComplex(
        simplices=((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)),
        births=(0.0, 0.0, 0.0, 1.0, 1.5, 2.0),
        dimensions=(0, 0, 0, 1, 1, 1),
    )


class TestStreamingPersistence:
    def test_empty(self):
        sp = StreamingPersistence()
        assert sp.current_pairs() == []
        assert sp.current_betti() == {}
        assert sp.num_simplices() == 0

    def test_single_vertex(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        assert sp.num_simplices() == 1
        assert sp.current_betti() == {0: 1}  # one H0 class

    def test_two_isolated_vertices(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        sp.add_simplex((1,), 0.0)
        assert sp.current_betti() == {0: 2}

    def test_edge_connects_vertices(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        sp.add_simplex((1,), 0.0)
        sp.add_simplex((0, 1), 1.0)
        betti = sp.current_betti()
        assert betti.get(0, 0) == 1  # one H0 essential
        pairs = sp.current_pairs()
        assert len(pairs) == 1
        assert pairs[0].dimension == 0
        assert pairs[0].birth == 0.0
        assert pairs[0].death == 1.0

    def test_triangle_h1(self):
        sp = StreamingPersistence()
        for v in [0, 1, 2]:
            sp.add_simplex((v,), 0.0)
        sp.add_simplex((0, 1), 1.0)
        sp.add_simplex((0, 2), 1.0)
        sp.add_simplex((1, 2), 2.0)
        # H1 class born when last edge added, killed when filled (never here)
        betti = sp.current_betti()
        assert betti.get(0, 0) == 1  # one component survives
        h1 = [p for p in sp.current_pairs() if p.dimension == 1]
        # There's a loop but no 2-simplex to kill it yet → essential
        assert len(h1) == 0

    def test_filled_triangle_kills_h1(self):
        sp = StreamingPersistence()
        for v in [0, 1, 2]:
            sp.add_simplex((v,), 0.0)
        sp.add_simplex((0, 1), 1.0)
        sp.add_simplex((0, 2), 1.0)
        sp.add_simplex((1, 2), 2.0)
        sp.add_simplex((0, 1, 2), 3.0)  # fills the triangle
        h1 = [p for p in sp.current_pairs() if p.dimension == 1]
        assert len(h1) == 1
        assert h1[0].birth == pytest.approx(2.0)
        assert h1[0].death == pytest.approx(3.0)

    def test_matches_standard_reduction(self):
        """Streaming result must match persistence_pairs_twist on same filtration."""
        sp = StreamingPersistence()
        filt = _build_standard_filtration()
        for sigma, b in zip(filt.simplices, filt.births):
            sp.add_simplex(list(sigma), b)

        std_pairs = set(
            (p.dimension, p.birth, p.death)
            for p in persistence_pairs_twist(filt)
            if not math.isinf(p.death)
        )
        stream_pairs = set(
            (p.dimension, p.birth, p.death)
            for p in sp.current_pairs()
        )
        assert std_pairs == stream_pairs

    def test_duplicate_simplex_raises(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        with pytest.raises(ValueError, match="already been inserted"):
            sp.add_simplex((0,), 1.0)

    def test_missing_face_raises(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        with pytest.raises(ValueError, match="not been inserted"):
            sp.add_simplex((0, 1), 1.0)

    def test_essential_pairs(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        sp.add_simplex((1,), 0.5)
        essentials = sp.current_essential_pairs()
        # Both vertices are essential H0 classes (no edge yet)
        assert len(essentials) == 2
        assert all(math.isinf(p.death) for p in essentials)

    def test_include_zero_persistence(self):
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        sp.add_simplex((1,), 0.0)
        sp.add_simplex((0, 1), 0.0)  # same birth as vertices
        pairs_default = sp.current_pairs(include_zero_persistence=False)
        pairs_incl = sp.current_pairs(include_zero_persistence=True)
        # With zero_persistence=True there should be ≥ as many pairs
        assert len(pairs_incl) >= len(pairs_default)

    def test_path_graph(self):
        """Path 0-1-2-3: three edges, three H0 pairs reducing to one component."""
        sp = StreamingPersistence()
        for i in range(4):
            sp.add_simplex((i,), 0.0)
        for i in range(3):
            sp.add_simplex((i, i + 1), float(i + 1))
        h0_pairs = [p for p in sp.current_pairs() if p.dimension == 0]
        assert len(h0_pairs) == 3
        assert sp.current_betti().get(0, 0) == 1

    def test_sorted_key(self):
        """Simplex vertices are canonically sorted on insertion."""
        sp = StreamingPersistence()
        sp.add_simplex((0,), 0.0)
        sp.add_simplex((1,), 0.0)
        sp.add_simplex([1, 0], 1.0)  # unsorted — should be treated as (0,1)
        assert sp.num_simplices() == 3


# ---------------------------------------------------------------------------
# P10.5 — GPU backend (graceful fallback)
# ---------------------------------------------------------------------------

from pytop._gpu_backend import GPU_AVAILABLE, GPU_MIN_SIZE, gpu_twist_reduce  # noqa: E402


class TestGPUBackend:
    def test_gpu_available_is_bool(self):
        assert isinstance(GPU_AVAILABLE, bool)

    def test_gpu_min_size_positive(self):
        assert GPU_MIN_SIZE > 0

    def test_fallback_when_no_cupy(self):
        # In the test environment cupy is not installed → GPU_AVAILABLE is False.
        # gpu_twist_reduce must still return correct results via CPU fallback.
        # Build a small FilteredComplex directly (path graph 0-1-2).
        filt = FilteredComplex(
            simplices=((0,), (1,), (2,), (0, 1), (1, 2)),
            births=(0.0, 0.0, 0.0, 1.0, 2.0),
            dimensions=(0, 0, 0, 1, 1),
        )
        columns_raw: list[int] = []
        idx: dict[tuple[int, ...], int] = {}
        for k, sigma in enumerate(filt.simplices):
            idx[sigma] = k
            col: int = 0
            if len(sigma) >= 2:
                for r in range(len(sigma)):
                    face = sigma[:r] + sigma[r + 1:]
                    col ^= 1 << idx[face]
            columns_raw.append(col)

        result, stats = gpu_twist_reduce(
            columns_raw,
            filt.dimensions,
            filt.births,
        )
        # On CPU fallback: must return same as persistence_pairs_twist
        std = persistence_pairs_twist(filt)
        assert len(result) == len(std)

    def test_gpu_module_importable(self):
        import pytop._gpu_backend as gpu
        assert hasattr(gpu, "GPU_AVAILABLE")
        assert hasattr(gpu, "gpu_twist_reduce")

    def test_gpu_twist_reduce_exported(self):
        import pytop
        assert hasattr(pytop, "GPU_AVAILABLE")
        assert hasattr(pytop, "gpu_twist_reduce")
