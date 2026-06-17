"""Tests for the simplicial cohomology and cup product ring module.

Coverage
────────
1. coboundary_matrix — transpose of boundary_matrix; δ²=0
2. simplicial_cohomology — groups on standard spaces
3. UCT: betti^k = betti_k; torsion^k = torsion_{k-1}
4. cohomology_betti_numbers — equals simplicial betti_numbers
5. cup_product_cochain — cochain-level correctness
6. simplicial_cohomology_ring / CohomologyRing
   a. Standard spaces: point, circle, sphere, torus, RP²
   b. Torus H^1 ⊗ H^1 → H^2 is non-degenerate and antisymmetric
   c. Graded commutativity [f]∪[g] = (−1)^{pq}[g]∪[f]
   d. H^0 unit element acts as a scalar on higher cohomology
7. is_trivial_ring on spheres; non-trivial on torus
"""
from __future__ import annotations

import pytest

from pytop.cohomology import (
    CohomologyResult,
    coboundary_matrix,
    cohomology_betti_numbers,
    cohomology_groups,
    cup_product_cochain,
    simplicial_cohomology,
    simplicial_cohomology_ring,
    _compute_cohomology_data,
)
from pytop.homology import betti_numbers, boundary_matrix, simplicial_homology
from pytop.homology import _simplices_of_dimension
from pytop.mayer_vietoris import _mat_vec
from pytop.simplicial_complexes import generated_subcomplex


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _point():
    return generated_subcomplex([{1}])


def _circle():
    return generated_subcomplex([{1, 2}, {2, 3}, {1, 3}])


def _sphere():
    return generated_subcomplex([{1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}])


def _torus():
    triangles = []
    for i in range(3):
        for j in range(3):
            a = (i % 3, j % 3)
            b = ((i + 1) % 3, j % 3)
            c = (i % 3, (j + 1) % 3)
            d = ((i + 1) % 3, (j + 1) % 3)
            triangles.append({a, b, c})
            triangles.append({b, d, c})
    return generated_subcomplex(triangles)


def _rp2():
    return generated_subcomplex([
        {1, 2, 3}, {1, 3, 4}, {1, 4, 5}, {1, 5, 6}, {1, 2, 6},
        {2, 3, 5}, {2, 4, 5}, {2, 4, 6}, {3, 4, 6}, {3, 5, 6},
    ])


# ── coboundary_matrix ─────────────────────────────────────────────────────────

class TestCoboundaryMatrix:
    def test_is_transpose_of_boundary(self):
        K = _circle()
        # coboundary_matrix(K, 0) = (∂_1)^T
        delta0 = coboundary_matrix(K, 0)
        d1 = boundary_matrix(K, 1)
        assert len(delta0) == len(d1[0])
        assert len(delta0[0]) == len(d1)
        for i in range(len(delta0)):
            for j in range(len(delta0[0])):
                assert delta0[i][j] == d1[j][i]

    @pytest.mark.parametrize("builder", [_circle, _sphere, _torus, _rp2])
    def test_delta_squared_is_zero(self, builder):
        K = builder()
        for k in range(K.dimension):
            dk = coboundary_matrix(K, k)
            dk1 = coboundary_matrix(K, k + 1)
            if not dk or not dk[0] or not dk1 or not dk1[0]:
                continue
            # δ^{k+1} ∘ δ^k = 0
            n_mid = len(dk)
            for i in range(len(dk1)):
                for j in range(len(dk[0])):
                    val = sum(dk1[i][m] * dk[m][j] for m in range(n_mid))
                    assert val == 0

    def test_top_dimension_empty(self):
        assert coboundary_matrix(_sphere(), 2) == []

    def test_negative_degree_empty(self):
        assert coboundary_matrix(_circle(), -1) == []


# ── simplicial_cohomology ─────────────────────────────────────────────────────

class TestSimplicialCohomology:
    def test_point(self):
        h0 = simplicial_cohomology(_point(), 0)
        assert h0.betti == 1 and h0.torsion == ()

    def test_circle(self):
        K = _circle()
        assert simplicial_cohomology(K, 0).betti == 1
        h1 = simplicial_cohomology(K, 1)
        assert h1.betti == 1 and h1.torsion == ()

    def test_sphere(self):
        K = _sphere()
        assert simplicial_cohomology(K, 0).betti == 1
        assert simplicial_cohomology(K, 1).betti == 0
        h2 = simplicial_cohomology(K, 2)
        assert h2.betti == 1 and h2.torsion == ()

    def test_torus(self):
        K = _torus()
        assert simplicial_cohomology(K, 0).betti == 1
        assert simplicial_cohomology(K, 1).betti == 2
        assert simplicial_cohomology(K, 2).betti == 1
        for k in range(3):
            assert simplicial_cohomology(K, k).torsion == ()

    def test_rp2_uct(self):
        # UCT: H^0=Z, H^1=0, H^2=Z/2  (torsion of H_1 shifts to degree 2)
        K = _rp2()
        assert simplicial_cohomology(K, 0) == CohomologyResult(0, 1, ())
        assert simplicial_cohomology(K, 1) == CohomologyResult(1, 0, ())
        assert simplicial_cohomology(K, 2) == CohomologyResult(2, 0, (2,))

    def test_negative_and_out_of_range(self):
        K = _sphere()
        assert simplicial_cohomology(K, -1).betti == 0
        assert simplicial_cohomology(K, 5).betti == 0


# ── UCT consistency ───────────────────────────────────────────────────────────

class TestUCT:
    @pytest.mark.parametrize("builder", [_point, _circle, _sphere, _torus, _rp2])
    def test_betti_equals_homology_betti(self, builder):
        K = builder()
        assert cohomology_betti_numbers(K) == betti_numbers(K)

    @pytest.mark.parametrize("builder", [_point, _circle, _sphere, _torus, _rp2])
    def test_torsion_shifts_by_one(self, builder):
        K = builder()
        for k in range(1, K.dimension + 1):
            assert simplicial_cohomology(K, k).torsion == simplicial_homology(K, k - 1).torsion

    def test_h0_always_torsion_free(self):
        for b in [_point, _circle, _sphere, _torus, _rp2]:
            assert simplicial_cohomology(b(), 0).torsion == ()


# ── CohomologyResult ──────────────────────────────────────────────────────────

class TestCohomologyResult:
    def test_describe_zero(self):
        assert CohomologyResult(1, 0, ()).describe() == "0"

    def test_describe_z(self):
        assert CohomologyResult(0, 1, ()).describe() == "Z"

    def test_describe_z2(self):
        assert CohomologyResult(2, 2, ()).describe() == "Z^2"

    def test_describe_torsion(self):
        assert CohomologyResult(2, 0, (2,)).describe() == "Z/2"

    def test_is_free(self):
        assert CohomologyResult(1, 1, ()).is_free
        assert not CohomologyResult(2, 0, (2,)).is_free


# ── cup_product_cochain ───────────────────────────────────────────────────────

class TestCupProductCochain:
    def test_cup_0_0_pointwise(self):
        K = _circle()
        verts = _simplices_of_dimension(K, 0)
        n = len(verts)
        f = list(range(1, n + 1))
        g = list(range(n, 0, -1))
        fg = cup_product_cochain(K, f, g, 0, 0)
        assert fg == [f[i] * g[i] for i in range(n)]

    def test_zero_cochain_gives_zero(self):
        K = _torus()
        n1 = len(_simplices_of_dimension(K, 1))
        f = [0] * n1
        g = [0] * n1
        assert all(v == 0 for v in cup_product_cochain(K, f, g, 1, 1))

    def test_cup_beyond_dimension_is_empty(self):
        K = _sphere()
        n2 = len(_simplices_of_dimension(K, 2))
        f, g = [1] * n2, [1] * n2
        assert cup_product_cochain(K, f, g, 2, 2) == []

    def test_cup_of_cocycles_is_cocycle(self):
        """δ(f ∪ g) = 0 whenever δf = δg = 0."""
        K = _torus()
        hd0 = _compute_cohomology_data(K, 0)
        hd1 = _compute_cohomology_data(K, 1)
        f0 = hd0.cocycle_rep(0)
        g1 = hd1.cocycle_rep(0)
        fg = cup_product_cochain(K, f0, g1, 0, 1)
        # δ^1(fg) = 0
        delta1 = coboundary_matrix(K, 1)
        if delta1 and delta1[0]:
            assert all(v == 0 for v in _mat_vec(delta1, fg))

    def test_cup_unit_with_1cochain(self):
        """The constant-1 cochain in C^0 acts as identity for ∪."""
        K = _circle()
        hd0 = _compute_cohomology_data(K, 0)
        # constant-1 cochain in C^0
        const1 = [1] * len(_simplices_of_dimension(K, 0))
        hd1 = _compute_cohomology_data(K, 1)
        g = hd1.cocycle_rep(0)
        fg = cup_product_cochain(K, const1, g, 0, 1)
        # (1 ∪ g)(e) = 1(front_0 e) · g(e) = g(e) since 1 evaluates to 1
        assert fg == g


# ── simplicial_cohomology_ring ────────────────────────────────────────────────

class TestCohomologyRing:
    def test_point_trivial(self):
        ring = simplicial_cohomology_ring(_point())
        assert ring.betti_numbers() == (1,)
        assert ring.is_trivial_ring()

    def test_sphere_trivial(self):
        ring = simplicial_cohomology_ring(_sphere())
        assert ring.betti_numbers() == (1, 0, 1)
        assert ring.is_trivial_ring()

    def test_circle_trivial(self):
        assert simplicial_cohomology_ring(_circle()).is_trivial_ring()

    def test_torus_betti(self):
        ring = simplicial_cohomology_ring(_torus())
        assert ring.betti_numbers() == (1, 2, 1)

    def test_torus_nontrivial_ring(self):
        assert not simplicial_cohomology_ring(_torus()).is_trivial_ring()

    def test_torus_cup_h1_h1_shape(self):
        # H^1=Z², H^2=Z → cup matrix is 1×4
        ring = simplicial_cohomology_ring(_torus())
        M = ring.cup((1, 1))
        assert M is not None and len(M) == 1 and len(M[0]) == 4

    def test_torus_cup_h1_h1_diagonal_zero(self):
        """α∪α = 0 for any α ∈ H^1(T²; Z)  (graded commutativity + Z free)."""
        ring = simplicial_cohomology_ring(_torus())
        M = ring.cup((1, 1))
        # col i*n_q+j with n_q=2: col 0=α_0∪α_0, col 3=α_1∪α_1
        assert M[0][0] == 0, "α_0∪α_0 must be 0"
        assert M[0][3] == 0, "α_1∪α_1 must be 0"

    def test_torus_cup_h1_h1_nondegenerate(self):
        """α_0 ∪ α_1 ≠ 0  (non-degenerate pairing on H^1(T²))."""
        ring = simplicial_cohomology_ring(_torus())
        M = ring.cup((1, 1))
        # col 1 = α_0∪α_1
        assert M[0][1] != 0

    def test_torus_graded_commutativity_h1_h1(self):
        """[f]∪[g] = (−1)^{1·1}[g]∪[f]  →  α_0∪α_1 = −α_1∪α_0."""
        ring = simplicial_cohomology_ring(_torus())
        M = ring.cup((1, 1))
        # col 1 = α_0∪α_1 (i=0,j=1 → 0*2+1), col 2 = α_1∪α_0 (i=1,j=0 → 1*2+0)
        assert M[0][1] == -M[0][2], (
            f"Graded commutativity: α_0∪α_1={M[0][1]} should equal −α_1∪α_0={-M[0][2]}"
        )

    def test_torus_cup_h0_h1_unit_action(self):
        """H^0 generator acts as scalar multiple of identity on H^1."""
        ring = simplicial_cohomology_ring(_torus())
        # M_01: (2 × 2),  cols: [unit∪α_0, unit∪α_1]
        M_01 = ring.cup((0, 1))
        assert len(M_01) == 2 and len(M_01[0]) == 2
        # Off-diagonal zero: [unit]∪[α_0] has no [α_1] component
        assert M_01[0][1] == 0
        assert M_01[1][0] == 0
        # Diagonal entries equal and nonzero
        assert M_01[0][0] != 0
        assert M_01[0][0] == M_01[1][1]

    def test_rp2_betti_and_torsion(self):
        ring = simplicial_cohomology_ring(_rp2())
        assert ring.betti_numbers() == (1, 0, 0)
        assert ring.h(2) is not None
        assert ring.h(2).torsion == (2,)

    def test_rp2_trivial_positive_cup(self):
        # H^1(RP²;Z)=0, so no nontrivial cup products for p,q≥1
        assert simplicial_cohomology_ring(_rp2()).is_trivial_ring()

    def test_h_accessor(self):
        ring = simplicial_cohomology_ring(_torus())
        assert ring.h(0).betti == 1
        assert ring.h(1).betti == 2
        assert ring.h(2).betti == 1
        assert ring.h(5) is None

    def test_cup_returns_empty_for_missing_key(self):
        ring = simplicial_cohomology_ring(_circle())
        # (1,1) is not in cup_table: dim=1 so p+q=2 > dim
        M = ring.cup((1, 1))
        assert M == []

    def test_describe_contains_groups(self):
        for builder in [_point, _circle, _sphere, _torus, _rp2]:
            ring = simplicial_cohomology_ring(builder())
            desc = ring.describe()
            assert "H^0" in desc


# ── Rank duality: rank(δ^k) = rank(∂_{k+1}) ──────────────────────────────────

class TestCoboundaryBoundaryRankDuality:
    @pytest.mark.parametrize("builder", [_circle, _sphere, _torus, _rp2])
    def test_rank_equality(self, builder):
        from pytop.homology import _smith_normal_form
        K = builder()
        for k in range(K.dimension):
            bm = boundary_matrix(K, k + 1)
            cm = coboundary_matrix(K, k)
            rank_b = len(_smith_normal_form(bm)) if bm and bm[0] else 0
            rank_c = len(_smith_normal_form(cm)) if cm and cm[0] else 0
            assert rank_b == rank_c, f"Rank mismatch at k={k} for {builder.__name__}"
