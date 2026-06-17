"""Tests for the Mayer–Vietoris long exact sequence module.

We use concrete simplicial models where the expected homology groups
and LES maps are known from topology.

S^1 (circle) decomposition
──────────────────────────
A = path 0─1─2      (contractible)
B = edge 0─2         (contractible)
A ∩ B = {0, 2}      (two isolated vertices, H_0 = Z²)
K = A ∪ B = ∂Δ²    (triangle boundary = S^1)

Expected LES:
  0 → H_1(K)=Z ─δ→ H_0(A∩B)=Z² ─φ→ H_0(A)⊕H_0(B)=Z⊕Z ─ψ→ H_0(K)=Z → 0

S^2 (sphere) decomposition
───────────────────────────
Take the boundary of the tetrahedron [0,1,2,3] and split it into
two "hemispheres":
  A = faces containing vertex 3: {[0,1,3],[0,2,3],[1,2,3], edges, vertices}
  B = faces of the equatorial disc {[0,1,2], edges, vertices}
  A ∩ B = the equatorial triangle boundary {[0,1],[0,2],[1,2],[0],[1],[2]} ≅ S^1
  K = A ∪ B = ∂Δ³ ≅ S^2

Expected: H_0=Z, H_1=0, H_2=Z.
"""
import pytest
from pytop.simplicial_complexes import SimplicialComplex
from pytop.mayer_vietoris import (
    sc_intersection,
    sc_union,
    mayer_vietoris,
    _snf_ext,
    _mat_mul,
    _imat,
    _compute_homology_data,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def circle_mv():
    """A ∪ B = S^1 decomposition."""
    A = SimplicialComplex([[0, 1], [1, 2], [0], [1], [2]])
    B = SimplicialComplex([[0, 2], [0], [2]])
    return A, B


@pytest.fixture
def sphere_mv():
    """A ∪ B = S^2 decomposition via ∂Δ³."""
    # A: three triangular faces containing vertex 3
    A = SimplicialComplex([
        [0, 1, 3], [0, 2, 3], [1, 2, 3],
        [0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3],
        [0], [1], [2], [3],
    ])
    # B: the equatorial triangle filled in as a disc
    B = SimplicialComplex([
        [0, 1, 2],
        [0, 1], [0, 2], [1, 2],
        [0], [1], [2],
    ])
    return A, B


# ── _snf_ext sanity checks ────────────────────────────────────────────────────

class TestSnfExt:
    def test_identity_preserved(self):
        M = [[1, 2], [3, 4]]
        D, P, Pinv, Q, Qinv = _snf_ext(M)
        # P @ M @ Q = D
        PD = _mat_mul(P, M)
        PDQ = _mat_mul(PD, Q)
        assert PDQ == D

    def test_inverses(self):
        M = [[1, 2], [3, 4]]
        _, P, Pinv, Q, Qinv = _snf_ext(M)
        n = len(P)
        m = len(Q)
        assert _mat_mul(P, Pinv) == _imat(n)
        assert _mat_mul(Q, Qinv) == _imat(m)

    def test_diagonal_nonneg(self):
        M = [[0, 2, 1], [1, 3, 0]]
        D, *_ = _snf_ext(M)
        for i in range(min(len(D), len(D[0]) if D else 0)):
            assert D[i][i] >= 0

    def test_rank_preserved(self):
        M = [[1, 0, 0], [0, 2, 0], [0, 0, 0]]
        D, *_ = _snf_ext(M)
        non_zero = sum(1 for i in range(min(len(D), len(D[0]))) if D[i][i] != 0)
        assert non_zero == 2

    def test_torsion_divisibility(self):
        # SNF diagonal entries must satisfy d_1 | d_2 | ... | d_r
        M = [[2, 0], [0, 6]]
        D, P, Pinv, Q, Qinv = _snf_ext(M)
        diag = [D[i][i] for i in range(min(len(D), len(D[0]))) if D[i][i] != 0]
        for k in range(len(diag) - 1):
            assert diag[k + 1] % diag[k] == 0


# ── sc_intersection / sc_union ────────────────────────────────────────────────

class TestScOps:
    def test_intersection_circle(self, circle_mv):
        A, B = circle_mv
        AB = sc_intersection(A, B)
        from pytop.simplices import Simplex
        verts = {frozenset(s.vertices) for s in AB.simplexes}
        assert frozenset({0}) in verts
        assert frozenset({2}) in verts
        assert frozenset({0, 2}) not in verts  # edge not in A

    def test_union_circle(self, circle_mv):
        A, B = circle_mv
        K = sc_union(A, B)
        from pytop.simplices import Simplex
        edges = {frozenset(s.vertices) for s in K.simplexes if len(s.vertices) == 2}
        assert frozenset({0, 1}) in edges
        assert frozenset({1, 2}) in edges
        assert frozenset({0, 2}) in edges

    def test_union_is_face_closed(self, circle_mv):
        A, B = circle_mv
        K = sc_union(A, B)
        assert K is not None  # SimplicialComplex validates face-closure

    def test_intersection_empty_raises(self):
        A = SimplicialComplex([[0], [1]])
        B = SimplicialComplex([[2], [3]])
        with pytest.raises(ValueError, match="empty"):
            sc_intersection(A, B)


# ── _compute_homology_data ────────────────────────────────────────────────────

class TestHomologyData:
    def test_s1_path_h0(self, circle_mv):
        A, _ = circle_mv
        hd = _compute_homology_data(A, 0)
        assert hd.group.betti == 1
        assert hd.group.torsion == ()

    def test_s1_path_h1_zero(self, circle_mv):
        A, _ = circle_mv
        hd = _compute_homology_data(A, 1)
        assert hd.group.betti == 0
        assert hd.group.torsion == ()

    def test_cycle_rep_roundtrip(self, circle_mv):
        A, B = circle_mv
        AB = sc_intersection(A, B)
        K = sc_union(A, B)
        hd = _compute_homology_data(K, 1)  # H_1(S^1) = Z
        assert hd.group.betti == 1
        rep = hd.cycle_rep(0)
        # rep should be a non-zero cycle
        assert any(c != 0 for c in rep)
        # coords_in_hk of the rep must give the generator
        coords = hd.coords_in_hk(rep)
        assert coords == [1] or coords == [-1]

    def test_zero_degree_two_component(self, circle_mv):
        A, B = circle_mv
        AB = sc_intersection(A, B)
        hd = _compute_homology_data(AB, 0)
        assert hd.group.betti == 2  # two connected components


# ── mayer_vietoris: circle S^1 ────────────────────────────────────────────────

class TestMVCircle:
    def test_groups_at_degree_0(self, circle_mv):
        A, B = circle_mv
        mv = mayer_vietoris(A, B)
        d0 = next(d for d in mv.degrees if d.degree == 0)
        assert d0.h_intersection.betti == 2   # A∩B = two points
        assert d0.h_A.betti == 1              # A contractible
        assert d0.h_B.betti == 1              # B contractible
        assert d0.h_union.betti == 1          # S^1 connected

    def test_groups_at_degree_1(self, circle_mv):
        A, B = circle_mv
        mv = mayer_vietoris(A, B)
        d1 = next(d for d in mv.degrees if d.degree == 1)
        assert d1.h_intersection.betti == 0   # A∩B has no loops
        assert d1.h_A.betti == 0              # A contractible
        assert d1.h_B.betti == 0              # B contractible
        assert d1.h_union.betti == 1          # S^1 has one loop

    def test_euler_characteristic(self, circle_mv):
        A, B = circle_mv
        mv = mayer_vietoris(A, B)
        assert mv.euler_check_passed

    def test_sequence_is_exact(self, circle_mv):
        A, B = circle_mv
        mv = mayer_vietoris(A, B)
        assert mv.is_exact

    def test_describe_runs(self, circle_mv):
        A, B = circle_mv
        mv = mayer_vietoris(A, B)
        desc = mv.describe()
        assert "Mayer" in desc
        assert "✓" in desc

    def test_union_is_triangle_boundary(self, circle_mv):
        A, B = circle_mv
        mv = mayer_vietoris(A, B)
        K = mv.union
        assert K.dimension == 1
        assert K.euler_characteristic() == 0  # χ(S^1) = 0


# ── mayer_vietoris: sphere S^2 ────────────────────────────────────────────────

class TestMVSphere:
    def test_groups_h0(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        d0 = next(d for d in mv.degrees if d.degree == 0)
        assert d0.h_union.betti == 1

    def test_groups_h1_zero(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        d1 = next(d for d in mv.degrees if d.degree == 1)
        assert d1.h_union.betti == 0
        assert d1.h_union.torsion == ()

    def test_groups_h2(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        d2 = next(d for d in mv.degrees if d.degree == 2)
        assert d2.h_union.betti == 1   # H_2(S^2) = Z

    def test_euler_characteristic(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        assert mv.euler_check_passed

    def test_sequence_is_exact(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        assert mv.is_exact

    def test_a_is_contractible(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        # A is a cone (contractible): all H_k = 0 for k > 0
        for d in mv.degrees:
            if d.degree > 0:
                assert d.h_A.betti == 0, f"A should be contractible at degree {d.degree}"

    def test_b_is_disc(self, sphere_mv):
        A, B = sphere_mv
        mv = mayer_vietoris(A, B)
        for d in mv.degrees:
            if d.degree > 0:
                assert d.h_B.betti == 0, f"B (disc) should have trivial H_{d.degree}"


# ── MV for a disjoint-union sanity check ─────────────────────────────────────

class TestMVInterval:
    """A ∪ B = segment [0,1,2] with A=[0,1] B=[1,2] A∩B={1}."""

    @pytest.fixture
    def interval_mv(self):
        A = SimplicialComplex([[0, 1], [0], [1]])
        B = SimplicialComplex([[1, 2], [1], [2]])
        return A, B

    def test_union_is_path(self, interval_mv):
        A, B = interval_mv
        mv = mayer_vietoris(A, B)
        assert mv.union.dimension == 1

    def test_h0_union_is_z(self, interval_mv):
        A, B = interval_mv
        mv = mayer_vietoris(A, B)
        d0 = next(d for d in mv.degrees if d.degree == 0)
        assert d0.h_union.betti == 1

    def test_euler_check(self, interval_mv):
        A, B = interval_mv
        mv = mayer_vietoris(A, B)
        assert mv.euler_check_passed

    def test_is_exact(self, interval_mv):
        A, B = interval_mv
        mv = mayer_vietoris(A, B)
        assert mv.is_exact
