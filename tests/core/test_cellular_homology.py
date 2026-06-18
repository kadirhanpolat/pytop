"""Tests for the cellular homology module.

Coverage:
  - CWComplex construction and validation
  - cellular_homology for all standard space constructors
  - cellular_homology_groups / cellular_betti_numbers
  - cellular_euler_characteristic consistency with cw.euler_characteristic()
  - cw_from_simplicial cross-validation against simplicial_homology
"""
from __future__ import annotations

import pytest

from pytop.cellular_homology import (
    CWComplex,
    CWComplexError,
    cellular_betti_numbers,
    cellular_euler_characteristic,
    cellular_homology,
    cellular_homology_groups,
    cw_complex_projective_space,
    cw_from_simplicial,
    cw_klein_bottle,
    cw_lens_space,
    cw_moore_space,
    cw_real_projective_space,
    cw_sphere,
    cw_torus,
)
from pytop.homology import HomologyResult, simplicial_homology
from pytop.simplicial_complexes import generated_subcomplex


# ── Simplicial fixtures (reused from test_homology.py) ────────────────────────

def _sc_circle():
    return generated_subcomplex([{1, 2}, {2, 3}, {1, 3}])


def _sc_sphere():
    return generated_subcomplex([{1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}])


def _sc_torus():
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


def _sc_rp2():
    return generated_subcomplex([
        {1, 2, 3}, {1, 3, 4}, {1, 4, 5}, {1, 5, 6}, {1, 2, 6},
        {2, 3, 5}, {2, 4, 5}, {2, 4, 6}, {3, 4, 6}, {3, 5, 6},
    ])


# ── CWComplex construction ────────────────────────────────────────────────────

class TestCWComplexConstruction:
    def test_zero_cell_counts_filtered(self):
        cw = CWComplex(cell_counts={0: 1, 1: 0, 2: 2}, boundary_maps={}, require_chain_complex=False)
        assert 1 not in cw.cell_counts

    def test_dimension(self):
        cw = CWComplex(cell_counts={0: 1, 2: 1, 4: 1}, boundary_maps={})
        assert cw.dimension == 4

    def test_euler_characteristic_point(self):
        cw = CWComplex(cell_counts={0: 1}, boundary_maps={})
        assert cw.euler_characteristic() == 1

    def test_euler_characteristic_sphere(self):
        assert cw_sphere(2).euler_characteristic() == 2
        assert cw_torus().euler_characteristic() == 0
        assert cw_klein_bottle().euler_characteristic() == 0

    def test_chain_complex_violation_raises(self):
        # d_1 ∘ d_2 ≠ 0 should raise
        with pytest.raises(CWComplexError):
            CWComplex(
                cell_counts={0: 1, 1: 1, 2: 1},
                boundary_maps={1: [[1]], 2: [[1]]},
            )

    def test_require_chain_complex_false_skips_check(self):
        # Should not raise even though composition is nonzero
        cw = CWComplex(
            cell_counts={0: 1, 1: 1, 2: 1},
            boundary_maps={1: [[1]], 2: [[1]]},
            require_chain_complex=False,
        )
        assert cw.verify_chain_complex()  # violations list is nonempty

    def test_verify_chain_complex_valid_returns_empty(self):
        cw = cw_torus()
        assert cw.verify_chain_complex() == []


# ── Spheres ──────────────────────────────────────────────────────────────────

class TestSpheres:
    def test_s0(self):
        cw = cw_sphere(0)
        h0 = cellular_homology(cw, 0)
        assert h0.betti == 2
        assert h0.torsion == ()

    def test_s1(self):
        cw = cw_sphere(1)
        assert cellular_homology(cw, 0).betti == 1
        h1 = cellular_homology(cw, 1)
        assert h1.betti == 1
        assert h1.torsion == ()

    def test_s2(self):
        cw = cw_sphere(2)
        assert cellular_homology(cw, 0).betti == 1
        assert cellular_homology(cw, 1).betti == 0
        h2 = cellular_homology(cw, 2)
        assert h2.betti == 1
        assert h2.torsion == ()

    @pytest.mark.parametrize("n", [3, 4, 5, 7])
    def test_sn_betti(self, n: int):
        cw = cw_sphere(n)
        betti = cellular_betti_numbers(cw)
        for k, b in enumerate(betti):
            expected = 1 if k in (0, n) else 0
            assert b == expected, f"S^{n}: b_{k} expected {expected}, got {b}"

    def test_sphere_no_torsion(self):
        for n in range(1, 6):
            for h in cellular_homology_groups(cw_sphere(n)):
                assert h.torsion == (), f"S^{n} has unexpected torsion at degree {h.degree}"

    @pytest.mark.parametrize("n", [1, 2, 3, 4])
    def test_sphere_euler(self, n: int):
        cw = cw_sphere(n)
        chi_betti = cellular_euler_characteristic(cw)
        chi_cells = cw.euler_characteristic()
        assert chi_betti == chi_cells


# ── Real projective spaces ────────────────────────────────────────────────────

class TestRealProjectiveSpace:
    def test_rp0_is_point(self):
        assert cellular_betti_numbers(cw_real_projective_space(0)) == (1,)

    def test_rp1_is_circle(self):
        cw = cw_real_projective_space(1)
        assert cellular_betti_numbers(cw) == (1, 1)

    def test_rp2(self):
        cw = cw_real_projective_space(2)
        assert cellular_betti_numbers(cw) == (1, 0, 0)
        assert cellular_homology(cw, 1).torsion == (2,)
        assert cellular_homology(cw, 2).torsion == ()

    def test_rp3(self):
        cw = cw_real_projective_space(3)
        assert cellular_betti_numbers(cw) == (1, 0, 0, 1)
        assert cellular_homology(cw, 1).torsion == (2,)
        assert cellular_homology(cw, 3).torsion == ()

    def test_rp4(self):
        cw = cw_real_projective_space(4)
        assert cellular_betti_numbers(cw) == (1, 0, 0, 0, 0)
        assert cellular_homology(cw, 1).torsion == (2,)
        assert cellular_homology(cw, 3).torsion == (2,)

    def test_rp5(self):
        cw = cw_real_projective_space(5)
        assert cellular_betti_numbers(cw) == (1, 0, 0, 0, 0, 1)
        for k in [1, 3]:
            assert cellular_homology(cw, k).torsion == (2,)

    def test_rpn_euler_characteristic(self):
        # χ(RP^n) = 1 if n even, 0 if n odd
        for n in range(1, 7):
            cw = cw_real_projective_space(n)
            expected_chi = 1 if n % 2 == 0 else 0
            assert cellular_euler_characteristic(cw) == expected_chi, (
                f"RP^{n}: χ expected {expected_chi}"
            )


# ── Complex projective spaces ─────────────────────────────────────────────────

class TestComplexProjectiveSpace:
    def test_cp0_is_point(self):
        cw = cw_complex_projective_space(0)
        assert cellular_betti_numbers(cw) == (1,)

    def test_cp1_is_s2(self):
        cw = cw_complex_projective_space(1)
        assert cellular_betti_numbers(cw) == (1, 0, 1)
        for h in cellular_homology_groups(cw):
            assert h.torsion == ()

    def test_cp2(self):
        cw = cw_complex_projective_space(2)
        betti = cellular_betti_numbers(cw)
        assert betti == (1, 0, 1, 0, 1)

    def test_cp3(self):
        cw = cw_complex_projective_space(3)
        betti = cellular_betti_numbers(cw)
        assert betti == (1, 0, 1, 0, 1, 0, 1)

    def test_cpn_no_torsion(self):
        for n in range(1, 5):
            for h in cellular_homology_groups(cw_complex_projective_space(n)):
                assert h.torsion == (), f"CP^{n} has torsion at degree {h.degree}"

    def test_cpn_euler(self):
        for n in range(1, 5):
            cw = cw_complex_projective_space(n)
            assert cellular_euler_characteristic(cw) == n + 1


# ── Torus and Klein bottle ────────────────────────────────────────────────────

class TestSurfaces:
    def test_torus_homology(self):
        cw = cw_torus()
        groups = {h.degree: h for h in cellular_homology_groups(cw)}
        assert groups[0].betti == 1 and groups[0].torsion == ()
        assert groups[1].betti == 2 and groups[1].torsion == ()
        assert groups[2].betti == 1 and groups[2].torsion == ()

    def test_torus_euler(self):
        cw = cw_torus()
        assert cellular_euler_characteristic(cw) == 0
        assert cw.euler_characteristic() == 0

    def test_klein_bottle_homology(self):
        cw = cw_klein_bottle()
        h0 = cellular_homology(cw, 0)
        h1 = cellular_homology(cw, 1)
        h2 = cellular_homology(cw, 2)
        assert h0.betti == 1 and h0.torsion == ()
        assert h1.betti == 1 and h1.torsion == (2,)
        assert h2.betti == 0 and h2.torsion == ()

    def test_klein_bottle_euler(self):
        cw = cw_klein_bottle()
        assert cellular_euler_characteristic(cw) == 0


# ── Lens spaces ───────────────────────────────────────────────────────────────

class TestLensSpaces:
    @pytest.mark.parametrize("p", [2, 3, 5, 7])
    def test_lens_space_h1_torsion(self, p: int):
        cw = cw_lens_space(p)
        h1 = cellular_homology(cw, 1)
        assert h1.betti == 0
        assert h1.torsion == (p,)

    def test_lens_space_h0_and_h3(self):
        for p in [2, 3, 5]:
            cw = cw_lens_space(p)
            assert cellular_homology(cw, 0).betti == 1
            assert cellular_homology(cw, 3).betti == 1
            assert cellular_homology(cw, 2).betti == 0

    def test_lens_space_p0(self):
        # L(0,1): d_2 = [[0]] so H_1 = Z
        cw = cw_lens_space(0)
        h1 = cellular_homology(cw, 1)
        assert h1.betti == 1
        assert h1.torsion == ()

    def test_lens_space_euler(self):
        for p in [2, 3, 5]:
            cw = cw_lens_space(p)
            assert cellular_euler_characteristic(cw) == 0


# ── Moore spaces ──────────────────────────────────────────────────────────────

class TestMooreSpaces:
    @pytest.mark.parametrize("n,k", [(2, 1), (3, 1), (5, 2), (4, 3), (6, 2)])
    def test_hk_equals_zn(self, n: int, k: int):
        cw = cw_moore_space(n, k)
        hk = cellular_homology(cw, k)
        assert hk.betti == 0
        assert hk.torsion == (n,)

    @pytest.mark.parametrize("n,k", [(2, 1), (3, 2), (5, 3)])
    def test_other_degrees_trivial(self, n: int, k: int):
        cw = cw_moore_space(n, k)
        for h in cellular_homology_groups(cw):
            if h.degree == 0:
                assert h.betti == 1
            elif h.degree == k:
                pass  # tested separately
            else:
                assert h.betti == 0 and h.torsion == ()

    def test_moore_space_bad_n(self):
        with pytest.raises(ValueError):
            cw_moore_space(1, 2)

    def test_moore_space_bad_k(self):
        with pytest.raises(ValueError):
            cw_moore_space(3, 0)


# ── cw_from_simplicial cross-validation ──────────────────────────────────────

class TestCwFromSimplicial:
    @pytest.mark.parametrize("builder,dim", [
        (_sc_circle, 1),
        (_sc_sphere, 2),
        (_sc_torus, 2),
        (_sc_rp2, 2),
    ])
    def test_betti_matches_simplicial(self, builder, dim: int):
        K = builder()
        cw = cw_from_simplicial(K)
        for k in range(dim + 1):
            cellular = cellular_homology(cw, k)
            simplicial = simplicial_homology(K, k)
            assert cellular.betti == simplicial.betti, (
                f"Betti mismatch at degree {k}: cellular={cellular.betti}, "
                f"simplicial={simplicial.betti}"
            )
            assert cellular.torsion == simplicial.torsion, (
                f"Torsion mismatch at degree {k}: cellular={cellular.torsion}, "
                f"simplicial={simplicial.torsion}"
            )

    def test_from_simplicial_is_valid_chain_complex(self):
        for builder in [_sc_circle, _sc_sphere, _sc_torus, _sc_rp2]:
            K = builder()
            cw = cw_from_simplicial(K)
            assert cw.verify_chain_complex() == []

    def test_from_simplicial_cell_counts(self):
        K = _sc_circle()   # 3 vertices, 3 edges
        cw = cw_from_simplicial(K)
        assert cw.cell_counts[0] == 3
        assert cw.cell_counts[1] == 3


# ── Negative degree and out-of-range degrees ─────────────────────────────────

class TestEdgeCases:
    def test_negative_degree_returns_zero(self):
        cw = cw_sphere(2)
        h = cellular_homology(cw, -1)
        assert h.betti == 0 and h.torsion == ()

    def test_degree_beyond_dimension_returns_zero(self):
        cw = cw_sphere(2)
        h = cellular_homology(cw, 5)
        assert h.betti == 0 and h.torsion == ()

    def test_cw_sphere_invalid_n(self):
        with pytest.raises(ValueError):
            cw_sphere(-1)

    def test_rpn_invalid_n(self):
        with pytest.raises(ValueError):
            cw_real_projective_space(-1)

    def test_cpn_invalid_n(self):
        with pytest.raises(ValueError):
            cw_complex_projective_space(-1)

    def test_lens_space_invalid_p(self):
        with pytest.raises(ValueError):
            cw_lens_space(-1)
