"""Tests for Phase 13: Homotopy Theory modules."""

import pytest
from fractions import Fraction


# ---------------------------------------------------------------------------
# P13.1 chain_homotopy
# ---------------------------------------------------------------------------

class TestChainHomotopy:
    def _make_I(self, n: int):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def _make_zero(self, m: int, n: int):
        return [[0] * n for _ in range(m)]

    def test_identity_homotopic_to_itself(self):
        from pytop.chain_homotopy import is_chain_homotopy
        n = 2
        I = self._make_I(n)
        Z = self._make_zero(n, n)
        # f = g = I, homotopy h = 0: ∂0 + 0∂ = 0 = I - I ✓
        result = is_chain_homotopy(f=[I], g=[I], h=[Z], boundary_C=[Z], boundary_D=[Z])
        assert result.is_valid is True

    def test_non_homotopic_maps(self):
        from pytop.chain_homotopy import is_chain_homotopy
        n = 2
        I = self._make_I(n)
        Z = self._make_zero(n, n)
        g = self._make_zero(n, n)
        # f = I, g = 0, h = 0: ∂0 + 0∂ = 0 ≠ I - 0 = I → not valid
        result = is_chain_homotopy(f=[I], g=[g], h=[Z], boundary_C=[Z], boundary_D=[Z])
        assert result.is_valid is False

    def test_chain_homotopy_result_fields(self):
        from pytop.chain_homotopy import is_chain_homotopy, ChainHomotopyResult
        n = 1
        I = [[1]]
        Z = [[0]]
        result = is_chain_homotopy(f=[I], g=[I], h=[Z], boundary_C=[Z], boundary_D=[Z])
        assert isinstance(result, ChainHomotopyResult)
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'equation_errors')

    def test_find_chain_homotopy(self):
        from pytop.chain_homotopy import find_chain_homotopy
        n = 2
        I = self._make_I(n)
        Z = self._make_zero(n, n)
        result = find_chain_homotopy(f=[I], g=[I], boundary_C=[Z], boundary_D=[Z])
        # f = g: homotopy = 0 should work
        assert result is not None

    def test_chain_homotopy_equiv_same(self):
        from pytop.chain_homotopy import chain_homotopy_equiv
        result = chain_homotopy_equiv(
            betti_C=[1, 0], torsion_C=[(), ()],
            betti_D=[1, 0], torsion_D=[(), ()],
        )
        assert result.verdict == "equivalent"

    def test_chain_homotopy_equiv_different_betti(self):
        from pytop.chain_homotopy import chain_homotopy_equiv
        result = chain_homotopy_equiv(
            betti_C=[1, 0], torsion_C=[(), ()],
            betti_D=[1, 1], torsion_D=[(), ()],
        )
        assert result.verdict == "not_equivalent"

    def test_homotopy_equivalence_verdict_fields(self):
        from pytop.chain_homotopy import HomotopyEquivalenceVerdict
        v = HomotopyEquivalenceVerdict(
            verdict="equivalent", reason="test",
            betti_K=(1, 0), betti_L=(1, 0),
            euler_K=1, euler_L=1,
        )
        assert v.verdict == "equivalent"
        assert v.is_equivalent is True

    def test_homotopy_equivalence_simplicial(self):
        from pytop.chain_homotopy import homotopy_equivalence_simplicial
        from pytop.homology import SimplicialComplex
        K = SimplicialComplex([[0]])
        L = SimplicialComplex([[0]])
        result = homotopy_equivalence_simplicial(K, L)
        assert result.verdict in ("equivalent", "not_equivalent", "undecidable")


# ---------------------------------------------------------------------------
# P13.2 eilenberg_maclane
# ---------------------------------------------------------------------------

class TestEilenbergMaclane:
    def test_k_z3_cyclic_h1(self):
        from pytop.eilenberg_maclane import km_homology_cyclic, KGnHomology
        H = km_homology_cyclic(m=3, max_degree=4)
        assert isinstance(H, KGnHomology)
        # H_1(K(ℤ/3,1)) = ℤ/3 (torsion)
        assert 3 in H.torsion[1]

    def test_k_cyclic_even_degrees_zero(self):
        from pytop.eilenberg_maclane import km_homology_cyclic
        H = km_homology_cyclic(m=5, max_degree=4)
        # H_0 = ℤ, H_2k = 0 for k ≥ 1
        assert H.betti[0] == 1
        assert H.betti[2] == 0

    def test_k_z1_free_rank(self):
        from pytop.eilenberg_maclane import km_homology_free
        H = km_homology_free(rank=3, max_degree=3)
        # K(F_3,1) = ∨S^1: H_0=ℤ, H_1=ℤ^3, H_k=0 k>=2
        assert H.betti[0] == 1
        assert H.betti[1] == 3
        assert H.betti[2] == 0

    def test_k_free_abelian_torus(self):
        from pytop.eilenberg_maclane import km_homology_free_abelian
        H = km_homology_free_abelian(rank=2, max_degree=3)
        # K(ℤ^2,1) = T^2: H_0=ℤ, H_1=ℤ^2, H_2=ℤ
        assert H.betti[0] == 1
        assert H.betti[1] == 2
        assert H.betti[2] == 1

    def test_k_z1_circle(self):
        from pytop.eilenberg_maclane import km_homology_z
        H = km_homology_z(n=1, max_degree=3)
        # K(ℤ,1) = S^1: H_0=ℤ, H_1=ℤ, H_k=0 k>=2
        assert H.betti[0] == 1
        assert H.betti[1] == 1
        assert H.betti[2] == 0

    def test_k_z2_cp_inf(self):
        from pytop.eilenberg_maclane import km_homology_z
        H = km_homology_z(n=2, max_degree=5)
        # K(ℤ,2) = CP^∞: H_0=ℤ, H_2=ℤ, H_4=ℤ, odd=0
        assert H.betti[0] == 1
        assert H.betti[2] == 1

    def test_k_z2_cyclic(self):
        from pytop.eilenberg_maclane import km_homology_z2
        H = km_homology_z2(n=1, max_degree=5)
        assert H is not None

    def test_km_rational(self):
        from pytop.eilenberg_maclane import km_homology_rational
        result = km_homology_rational(group_name="Z", n=1, max_degree=3)
        assert isinstance(result, dict)

    def test_is_aspherical(self):
        from pytop.eilenberg_maclane import is_aspherical_by_homology
        from pytop.homology import SimplicialComplex
        # The circle (aspherical K(ℤ,1)): need face-closed complex
        K = SimplicialComplex([[0], [1], [2], [0, 1], [1, 2], [0, 2]])
        result = is_aspherical_by_homology(K)
        assert isinstance(result, bool)

    def test_euler_characteristic(self):
        from pytop.eilenberg_maclane import km_euler_characteristic
        chi = km_euler_characteristic(group_name="free_abelian", n=1, truncation=4)
        assert isinstance(chi, int)


# ---------------------------------------------------------------------------
# P13.3 massey_products
# ---------------------------------------------------------------------------

class TestMasseyProducts:
    def test_massey_product_dataclass(self):
        from pytop.massey_products import MasseyProduct
        mp = MasseyProduct(
            is_defined=True,
            is_trivial=True,
            product_degree=1,
            cochain=None,
            null_homotopy_x=None,
            null_homotopy_y=None,
            obstruction="",
        )
        assert mp.is_defined is True
        assert mp.is_trivial is True

    def test_massey_vanishes_on_trivial(self):
        from pytop.massey_products import massey_vanishes, MasseyProduct
        mp = MasseyProduct(
            is_defined=True, is_trivial=True, product_degree=2,
            cochain=(0,), null_homotopy_x=(0,), null_homotopy_y=(0,), obstruction="",
        )
        assert massey_vanishes(mp) is True

    def test_massey_not_defined(self):
        from pytop.massey_products import massey_vanishes, MasseyProduct
        mp = MasseyProduct(
            is_defined=False, is_trivial=False, product_degree=2,
            cochain=None, null_homotopy_x=None, null_homotopy_y=None,
            obstruction="cup product non-zero",
        )
        assert massey_vanishes(mp) is False

    def test_is_formal_simplicial_point(self):
        from pytop.massey_products import is_formal_simplicial
        from pytop.homology import SimplicialComplex
        K = SimplicialComplex([[0]])
        result, reason = is_formal_simplicial(K)
        assert result in (True, False)
        assert isinstance(reason, str)

    def test_triple_massey_interval(self):
        from pytop.massey_products import triple_massey_product
        from pytop.homology import SimplicialComplex
        K = SimplicialComplex([[0], [1], [0, 1]])
        n0 = len([s for s in K.simplexes if s.dimension == 0])
        result = triple_massey_product([1] + [0]*(n0-1), [1] + [0]*(n0-1),
                                        [1] + [0]*(n0-1), (0, 0, 0), K)
        assert hasattr(result, 'is_defined')

    def test_all_triple_massey(self):
        from pytop.massey_products import all_triple_massey_products
        from pytop.homology import SimplicialComplex
        K = SimplicialComplex([[0], [1], [0, 1]])
        result = all_triple_massey_products(K, max_total_degree=3)
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# P13.4 hopf_invariant
# ---------------------------------------------------------------------------

class TestHopfInvariant:
    def test_hopf_fibration_valid(self):
        from pytop.hopf_invariant import hopf_fibration
        for n in [1, 2, 4, 8]:
            hf = hopf_fibration(n)
            assert hf.hopf_invariant == 1

    def test_hopf_fibration_invalid(self):
        from pytop.hopf_invariant import hopf_fibration
        with pytest.raises(ValueError):
            hopf_fibration(3)

    def test_all_hopf_fibrations(self):
        from pytop.hopf_invariant import all_hopf_fibrations
        fibrations = all_hopf_fibrations()
        ns = [hf.target_sphere for hf in fibrations]
        assert set(ns) == {1, 2, 4, 8}

    def test_adams_theorem_valid(self):
        from pytop.hopf_invariant import adams_hopf_invariant_one
        assert adams_hopf_invariant_one(1) is True
        assert adams_hopf_invariant_one(2) is True
        assert adams_hopf_invariant_one(4) is True
        assert adams_hopf_invariant_one(8) is True

    def test_adams_theorem_invalid(self):
        from pytop.hopf_invariant import adams_hopf_invariant_one
        assert adams_hopf_invariant_one(3) is False
        assert adams_hopf_invariant_one(5) is False

    def test_pi3_s2(self):
        from pytop.hopf_invariant import pi3_s2
        result = pi3_s2()
        assert "group" in result

    def test_hopf_invariant_sum(self):
        from pytop.hopf_invariant import hopf_invariant_sum
        result = hopf_invariant_sum(3, 5)
        assert result == 8

    def test_hopf_from_cup(self):
        from pytop.hopf_invariant import hopf_invariant_from_cup
        result = hopf_invariant_from_cup(cup_coefficient=1)
        assert isinstance(result, int)

    def test_hopf_degree_map(self):
        from pytop.hopf_invariant import hopf_invariant_degree_map
        result = hopf_invariant_degree_map(n=2, degree=3)
        assert result == 9  # 3^2

    def test_hopf_invariant_dataclass(self):
        from pytop.hopf_invariant import HopfInvariant
        hf = HopfInvariant(
            source_sphere=3,
            target_sphere=2,
            hopf_invariant=1,
            name="eta_2",
            mapping_cone="CP2",
            cup_product="i2 cup i2 = i4",
        )
        assert hf.hopf_invariant == 1
        assert hf.target_sphere == 2


# ---------------------------------------------------------------------------
# P13.5 sullivan_models
# ---------------------------------------------------------------------------

class TestSullivanModels:
    def test_sullivan_sphere_odd(self):
        from pytop.sullivan_models import sullivan_sphere
        m = sullivan_sphere(3)
        assert m.is_formal is True
        assert len(m.generators) == 1

    def test_sullivan_sphere_even(self):
        from pytop.sullivan_models import sullivan_sphere
        m = sullivan_sphere(2)
        assert len(m.generators) == 2

    def test_sullivan_torus(self):
        from pytop.sullivan_models import sullivan_torus
        m = sullivan_torus(r=2)
        assert m.is_formal is True
        assert len(m.generators) == 2

    def test_sullivan_cp(self):
        from pytop.sullivan_models import sullivan_complex_projective
        m = sullivan_complex_projective(2)
        assert len(m.generators) == 2

    def test_pi_rational_s3(self):
        from pytop.sullivan_models import pi_rational, sullivan_sphere
        s3 = sullivan_sphere(3)
        # π_3(S^3) ⊗ Q = Q (rank 1)
        r3 = pi_rational(s3, 3)
        assert r3 == 1
        # π_4(S^3) ⊗ Q = 0
        r4 = pi_rational(s3, 4)
        assert r4 == 0

    def test_euler_characteristic_torus(self):
        from pytop.sullivan_models import euler_characteristic_sullivan, sullivan_torus
        m = sullivan_torus(r=2)
        chi = euler_characteristic_sullivan(m, max_degree=4)
        assert chi == 0  # T^2 has χ = 0

    def test_is_pure_sullivan(self):
        from pytop.sullivan_models import is_pure_sullivan, sullivan_sphere
        m = sullivan_sphere(4)
        result = is_pure_sullivan(m)
        assert isinstance(result, bool)

    def test_sullivan_product(self):
        from pytop.sullivan_models import sullivan_product, sullivan_sphere
        s3 = sullivan_sphere(3)
        s5 = sullivan_sphere(5)
        prod = sullivan_product(s3, s5)
        assert len(prod.generators) == len(s3.generators) + len(s5.generators)

    def test_sullivan_from_betti(self):
        from pytop.sullivan_models import sullivan_from_betti
        # Torus: b_0=1, b_1=2, b_2=1
        m = sullivan_from_betti([1, 2, 1])
        assert m is not None
