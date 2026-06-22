"""Tests for computational 3-manifold engines: mapping_torus_h1, lens_space_pi1."""

from __future__ import annotations

import pytest

from pytop.exact_linalg import AbelianGroup
from pytop.three_manifolds import lens_space_pi1, mapping_torus_h1
from pytop.van_kampen import GroupPresentation


# ---------------------------------------------------------------------------
# mapping_torus_h1
# ---------------------------------------------------------------------------


class TestMappingTorusH1:
    def test_identity_monodromy_gives_torus_three(self):
        # T²_id = T³, H₁(T³) = ℤ³
        result = mapping_torus_h1([[1, 0], [0, 1]])
        assert isinstance(result, AbelianGroup)
        assert result.free_rank == 3
        assert result.torsion == ()

    def test_anosov_monodromy_gives_z(self):
        # M = [[2,1],[1,1]] (det=1, |tr|=3>2 → hyperbolic/Anosov)
        # M-I = [[1,1],[1,0]], SNF = diag(1,1), coker = 0
        # H₁ = ℤ
        result = mapping_torus_h1([[2, 1], [1, 1]])
        assert result.free_rank == 1
        assert result.torsion == ()

    def test_dehn_twist_monodromy_gives_z_squared(self):
        # M = [[1,1],[0,1]], M-I = [[0,1],[0,0]]
        # SNF = diag(1,0), coker = ℤ, H₁ = ℤ²
        result = mapping_torus_h1([[1, 1], [0, 1]])
        assert result.free_rank == 2
        assert result.torsion == ()

    def test_negative_dehn_twist(self):
        # M = [[1,-1],[0,1]], same H₁ as Dehn twist
        result = mapping_torus_h1([[1, -1], [0, 1]])
        assert result.free_rank == 2
        assert result.torsion == ()

    def test_order_4_rotation_gives_z_plus_z2(self):
        # M = [[0,1],[-1,0]] (rotation by π/2, order 4)
        # M-I = [[-1,1],[-1,-1]], SNF = diag(1,2), coker = ℤ/2
        # H₁ = ℤ ⊕ ℤ/2
        result = mapping_torus_h1([[0, 1], [-1, 0]])
        assert result.free_rank == 1
        assert result.torsion == (2,)

    def test_order_6_rotation(self):
        # M = [[1,1],[-1,0]] (order 6 monodromy)
        # M-I = [[0,1],[-1,-1]], det = 0*(-1) - 1*(-1) = 1 ≠ 0 → rank 2
        # SNF: check via hand computation
        # [[0,1],[-1,-1]] → swap rows: [[-1,-1],[0,1]] → multiply R0 by -1: [[1,1],[0,1]]
        # C1 -= C0: [[1,0],[0,1]] → SNF = I, coker = 0
        # H₁ = ℤ
        result = mapping_torus_h1([[1, 1], [-1, 0]])
        assert result.free_rank == 1
        assert result.torsion == ()

    def test_empty_monodromy_gives_z(self):
        # Empty fiber → H₁ = ℤ (just the base circle)
        result = mapping_torus_h1([])
        assert result.free_rank == 1
        assert result.torsion == ()

    def test_one_by_one_identity(self):
        # Fiber = S¹, monodromy = [1] (identity)
        # M-I = [0], coker = ℤ, H₁ = ℤ²
        result = mapping_torus_h1([[1]])
        assert result.free_rank == 2
        assert result.torsion == ()

    def test_one_by_one_minus_one(self):
        # Fiber = S¹, monodromy = [-1] (antipodal)
        # M-I = [-2], SNF = [2], coker = ℤ/2, H₁ = ℤ ⊕ ℤ/2
        result = mapping_torus_h1([[-1]])
        assert result.free_rank == 1
        assert result.torsion == (2,)

    def test_returns_abelian_group(self):
        result = mapping_torus_h1([[1, 0], [0, 1]])
        assert isinstance(result, AbelianGroup)

    def test_raises_on_non_square_matrix(self):
        with pytest.raises(ValueError, match="square"):
            mapping_torus_h1([[1, 0, 0], [0, 1]])

    def test_consistency_with_known_formula(self):
        # For any M with det(M-I) ≠ 0, H₁ is finite ⊕ ℤ (finite cokernel)
        # det(M-I) = 0 iff 1 is an eigenvalue of M
        # Identity has 1 as eigenvalue → ℤ factor in cokernel
        # Anosov has no eigenvalue 1 → cokernel is finite (0 here)
        anosov = mapping_torus_h1([[2, 1], [1, 1]])
        assert anosov.free_rank == 1  # only the S¹ factor


# ---------------------------------------------------------------------------
# lens_space_pi1
# ---------------------------------------------------------------------------


class TestLensSpacePi1:
    def test_p_zero_gives_infinite_cyclic(self):
        # L(0, q) = S¹ × S², π₁ = ℤ
        p = lens_space_pi1(0)
        assert isinstance(p, GroupPresentation)
        assert p.rank == 1
        assert p.is_free
        assert len(p.relators) == 0

    def test_p_one_gives_trivial_group(self):
        # L(1, q) = S³, π₁ = 1
        p = lens_space_pi1(1)
        assert isinstance(p, GroupPresentation)
        assert p.rank == 0
        assert len(p.relators) == 0

    def test_p_two_gives_z_mod_2(self):
        # L(2, 1) = RP³, π₁ = ℤ/2: 1 generator, 1 relator a^2=1
        p = lens_space_pi1(2)
        assert p.rank == 1   # rank = number of generators
        assert len(p.generators) == 1
        assert len(p.relators) == 1
        # Relator encodes total exponent 2
        assert sum(abs(e) for _, e in p.relators[0]) == 2

    def test_p_five_gives_z_mod_5(self):
        p = lens_space_pi1(5)
        assert p.rank == 1
        assert len(p.generators) == 1
        assert len(p.relators) == 1
        assert sum(abs(e) for _, e in p.relators[0]) == 5

    def test_p_large_prime(self):
        p = lens_space_pi1(13)
        assert len(p.generators) == 1
        assert len(p.relators) == 1
        assert sum(abs(e) for _, e in p.relators[0]) == 13

    def test_returns_group_presentation(self):
        assert isinstance(lens_space_pi1(3), GroupPresentation)

    def test_raises_on_negative_p(self):
        with pytest.raises(ValueError, match="non-negative"):
            lens_space_pi1(-1)
        with pytest.raises(ValueError):
            lens_space_pi1(-5)

    def test_pi1_depends_only_on_p(self):
        p1 = lens_space_pi1(5)
        p2 = lens_space_pi1(5)
        assert p1.rank == p2.rank
        assert len(p1.relators) == len(p2.relators)

    def test_p_three(self):
        p = lens_space_pi1(3)
        assert p.rank == 1
        assert len(p.generators) == 1
        assert sum(abs(e) for _, e in p.relators[0]) == 3
