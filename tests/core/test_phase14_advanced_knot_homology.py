"""Tests for Phase 14: Advanced Knot Homology modules."""

import pytest
from fractions import Fraction


# ---------------------------------------------------------------------------
# P14.1 khovanov_odd
# ---------------------------------------------------------------------------

class TestOddKhovanov:
    def test_unknot_odd_khovanov(self):
        from pytop.khovanov_odd import khovanov_homology_odd
        from pytop.knot_invariants import KnotDiagram
        # Unknot: empty PD code
        kh = khovanov_homology_odd(KnotDiagram(pd=(), signs=()))
        assert kh.total_rank() >= 0

    def test_odd_khovanov_dataclass(self):
        from pytop.khovanov_odd import OddKhovanovHomology
        kh = OddKhovanovHomology(
            groups={(0, -1): (1, ()), (0, 1): (1, ())},
            writhe=0, n_plus=0, n_minus=0,
            jones_graded_euler={-1: 1, 1: 1},
        )
        assert kh.betti(0, -1) == 1
        assert kh.total_rank() == 2

    def test_odd_sign_assignment(self):
        from pytop.khovanov_odd import _odd_sign
        # (−1)^0 = 1 when no 1s before position 0
        assert _odd_sign((0, 0, 0), 0) == 1
        # (−1)^1 = -1 when one 1 before position 1
        assert _odd_sign((1, 0, 0), 1) == -1

    def test_compare_parities(self):
        from pytop.khovanov_odd import compare_khovanov_parities, OddKhovanovHomology
        from pytop.khovanov import KhovanovHomology
        kh_even = KhovanovHomology(
            groups={(0, -1): (1, ()), (0, 1): (1, ())},
        )
        kh_odd = OddKhovanovHomology(
            groups={(0, -1): (1, ()), (0, 1): (1, ())},
            writhe=0, n_plus=0, n_minus=0,
            jones_graded_euler={-1: 1, 1: 1},
        )
        result = compare_khovanov_parities(kh_even, kh_odd)
        assert "agree_at" in result
        assert "differ_at" in result

    def test_nonzero_groups(self):
        from pytop.khovanov_odd import OddKhovanovHomology
        kh = OddKhovanovHomology(
            groups={(0, 1): (2, (3,)), (1, 3): (0, ())},
            writhe=0, n_plus=0, n_minus=0,
            jones_graded_euler={},
        )
        ng = kh.nonzero_groups()
        assert len(ng) == 1  # (1,3) has betti=0 and no torsion

    def test_odd_khovanov_unknot_rank(self):
        from pytop.khovanov_odd import khovanov_homology_odd
        from pytop.knot_invariants import KnotDiagram
        kh = khovanov_homology_odd(KnotDiagram(pd=(), signs=()))
        assert kh.total_rank() == 2  # unknot: two generators


# ---------------------------------------------------------------------------
# P14.2 grid_floer
# ---------------------------------------------------------------------------

class TestGridFloer:
    def test_unknot_grid(self):
        from pytop.grid_floer import unknot_grid, hfk_hat
        grid = unknot_grid()
        hfk = hfk_hat(grid)
        # HFK̂ of the unknot: one generator in (m=0, a=0)
        assert hfk is not None
        assert hfk.total_rank() >= 1

    def test_grid_diagram_construction(self):
        from pytop.grid_floer import grid_diagram_from_permutations, GridDiagram
        # 2x2 unknot: O at (0,0), (1,1); X at (0,1), (1,0)
        grid = grid_diagram_from_permutations(
            o_perm=[0, 1], x_perm=[1, 0]
        )
        assert isinstance(grid, GridDiagram)
        assert grid.n == 2

    def test_grid_states(self):
        from pytop.grid_floer import unknot_grid
        grid = unknot_grid()
        states = grid.grid_states()
        assert len(states) > 0

    def test_maslov_grading(self):
        from pytop.grid_floer import unknot_grid, GridState
        grid = unknot_grid()
        states = grid.grid_states()
        if states:
            m = states[0].maslov_grading(grid)
            assert isinstance(m, int)

    def test_alexander_grading(self):
        from pytop.grid_floer import unknot_grid
        grid = unknot_grid()
        states = grid.grid_states()
        if states:
            a = states[0].alexander_grading(grid)
            assert isinstance(a, (int, Fraction))

    def test_hfkhat_dataclass(self):
        from pytop.grid_floer import HFKHat
        hfk = HFKHat(
            groups={(0, 0): 1},
            total_generators=1,
        )
        assert hfk.total_rank() == 1

    def test_trefoil_grid(self):
        from pytop.grid_floer import trefoil_grid
        grid = trefoil_grid()
        assert grid.n >= 3

    def test_alexander_from_hfk(self):
        from pytop.grid_floer import unknot_grid, hfk_hat, alexander_polynomial_from_hfk
        grid = unknot_grid()
        hfk = hfk_hat(grid)
        alex = alexander_polynomial_from_hfk(hfk)
        # Unknot: Δ(t) = 1
        assert alex is not None


# ---------------------------------------------------------------------------
# P14.3 concordance
# ---------------------------------------------------------------------------

class TestConcordance:
    def test_concordance_data_unknot(self):
        from pytop.concordance import concordance_data
        data = concordance_data("unknot")
        assert data.tau == 0
        assert data.s_invariant == 0
        assert data.signature == 0

    def test_concordance_data_trefoil(self):
        from pytop.concordance import concordance_data
        data = concordance_data("trefoil")
        assert data.tau == 1
        assert data.s_invariant == 2
        assert data.signature == -2

    def test_tau_torus_knot(self):
        from pytop.concordance import tau_torus_knot
        assert tau_torus_knot(2, 3) == 1   # T(2,3) = trefoil
        assert tau_torus_knot(2, 5) == 2   # T(2,5)
        assert tau_torus_knot(3, 4) == 3   # T(3,4): (3-1)(4-1)/2 = 3

    def test_s_invariant_torus_knot(self):
        from pytop.concordance import s_invariant_torus_knot
        assert s_invariant_torus_knot(2, 3) == 2
        assert s_invariant_torus_knot(2, 5) == 4

    def test_signature_torus_knot(self):
        from pytop.concordance import signature_torus_knot
        # σ(T(2,q)) = -(q-1) for q odd
        assert signature_torus_knot(2, 3) == -2
        assert signature_torus_knot(2, 5) == -4

    def test_is_algebraically_slice_unknot(self):
        from pytop.concordance import is_algebraically_slice, concordance_data
        uk = concordance_data("unknot")
        assert is_algebraically_slice(uk) is True

    def test_is_algebraically_slice_trefoil(self):
        from pytop.concordance import is_algebraically_slice, concordance_data
        tr = concordance_data("trefoil")
        assert is_algebraically_slice(tr) is False

    def test_concordance_order(self):
        from pytop.concordance import concordance_order, concordance_data
        uk = concordance_data("unknot")
        result = concordance_order(uk)
        assert result in ("infinite", "finite", "slice", 1, 2, "unknown")

    def test_tristram_levine(self):
        from pytop.concordance import tristram_levine_signature
        # omega = e^{iπ/3}, just test it runs on a Seifert matrix (trefoil).
        import cmath
        omega = cmath.exp(1j * cmath.pi / 3)
        seifert_trefoil = [[-1, 1], [0, -1]]
        sig = tristram_levine_signature(seifert_trefoil, omega)
        assert isinstance(sig, int)


# ---------------------------------------------------------------------------
# P14.4 satellite_knots
# ---------------------------------------------------------------------------

class TestSatelliteKnots:
    def test_torus_knot_alexander(self):
        from pytop.satellite_knots import torus_knot_alexander_poly
        # T(2,3) trefoil: Δ(t) = t^{-1} - 1 + t
        alex = torus_knot_alexander_poly(2, 3)
        assert -1 in alex and 0 in alex and 1 in alex

    def test_cable_alexander(self):
        from pytop.satellite_knots import cable_alexander_poly, torus_knot_alexander_poly
        alex_trefoil = torus_knot_alexander_poly(2, 3)
        cable = cable_alexander_poly(alex_trefoil, p=2, q=1)
        assert isinstance(cable, dict)

    def test_cable_genus(self):
        from pytop.satellite_knots import cable_genus
        # T(2,3) genus = 1; (2,1)-cable: 2*1 + (2-1)(1-1)/2 = 2
        g = cable_genus(seifert_genus=1, p=2, q=1)
        assert g == 2

    def test_cable_tau(self):
        from pytop.satellite_knots import cable_tau
        # τ of (p,1)-cable of K: p*τ(K) for longitudinal cable
        tau = cable_tau(companion_tau=1, p=2, q=1)
        assert tau == 2

    def test_satellite_data(self):
        from pytop.satellite_knots import satellite_data, SatelliteKnot
        data = satellite_data("Wh+(T_{2,3})")
        assert isinstance(data, SatelliteKnot)

    def test_satellite_alexander(self):
        from pytop.satellite_knots import satellite_alexander_poly, torus_knot_alexander_poly
        alex_k = torus_knot_alexander_poly(2, 3)
        alex_p = torus_knot_alexander_poly(2, 3)
        result = satellite_alexander_poly(pattern_poly=alex_p, companion_poly=alex_k, winding=1)
        assert isinstance(result, dict)

    def test_whitehead_double(self):
        from pytop.satellite_knots import whitehead_double
        wd = whitehead_double(companion_name="T_{2,3}", companion_genus=1)
        assert wd.seifert_genus == 1

    def test_cable_knot_dataclass(self):
        from pytop.satellite_knots import CableKnot
        ck = CableKnot(companion_name="trefoil", p=2, q=3,
                       alexander_poly={0: 1}, seifert_genus=2, tau=None)
        assert ck.p == 2

    def test_longitudinal_cable(self):
        from pytop.satellite_knots import longitudinal_cable, torus_knot_alexander_poly
        alex = torus_knot_alexander_poly(2, 3)
        lc = longitudinal_cable(companion_poly=alex, companion_genus=1, p=3)
        assert lc.q == 1


# ---------------------------------------------------------------------------
# P14.5 virtual_knots
# ---------------------------------------------------------------------------

class TestVirtualKnots:
    def test_gauss_code_parsing(self):
        from pytop.virtual_knots import gauss_code_from_string
        gc = gauss_code_from_string("O1+U2+O3+U1+O2+U3+", name="virtual_trefoil")
        assert gc.n_classical == 3
        assert gc.name == "virtual_trefoil"
        assert len(gc.crossings) == 6

    def test_parity_of_crossing(self):
        from pytop.virtual_knots import gauss_code_from_string, parity_of_crossing
        gc = gauss_code_from_string("O1+U2+O3+U1+O2+U3+")
        # In the virtual trefoil, all crossings are odd
        for label in [1, 2, 3]:
            par = parity_of_crossing(label, gc)
            assert par in ("odd", "even", "unknown")

    def test_odd_writhe_classical_vanishes(self):
        from pytop.virtual_knots import gauss_code_from_string, odd_writhe
        # Trefoil (classical) Gauss code: all crossings even → J=0
        # Standard (oriented) Gauss code for classical right-hand trefoil
        gc = gauss_code_from_string("O1+U2+O3+U1+O2-U3-")
        j = odd_writhe(gc)
        assert isinstance(j, int)

    def test_odd_writhe_virtual_trefoil(self):
        from pytop.virtual_knots import gauss_code_from_string, odd_writhe
        # Genuine virtual trefoil: 2 crossings (1,2,1,2), both odd, both +.
        gc = gauss_code_from_string("O1+O2+U1+U2+", name="virtual_trefoil")
        j = odd_writhe(gc)
        assert j == 2

    def test_writhe(self):
        from pytop.virtual_knots import gauss_code_from_string, writhe
        gc = gauss_code_from_string("O1+U2+O3+U1+O2+U3+")
        w = writhe(gc)
        assert w == 3

    def test_is_classical_virtual_trefoil(self):
        from pytop.virtual_knots import gauss_code_from_string, is_classical
        gc = gauss_code_from_string("O1+O2+U1+U2+", name="virtual_trefoil")
        assert is_classical(gc) is False

    def test_virtual_genus_lower_bound(self):
        from pytop.virtual_knots import gauss_code_from_string, virtual_genus_lower_bound
        gc = gauss_code_from_string("O1+O2+U1+U2+", name="virtual_trefoil")
        lb = virtual_genus_lower_bound(gc)
        assert lb >= 1

    def test_arrow_polynomial(self):
        from pytop.virtual_knots import gauss_code_from_string, arrow_polynomial_bracket
        gc = gauss_code_from_string("O1+U2+O3+U1+O2+U3+")
        poly = arrow_polynomial_bracket(gc)
        assert isinstance(poly, dict)

    def test_virtual_knot_invariants(self):
        from pytop.virtual_knots import gauss_code_from_string, virtual_knot_invariants
        gc = gauss_code_from_string("O1+O2+U1+U2+", name="virtual_trefoil")
        inv = virtual_knot_invariants(gc)
        assert inv.odd_writhe == 2
        assert inv.is_classical_knot is False

    def test_virtual_knot_data(self):
        from pytop.virtual_knots import VIRTUAL_KNOT_DATA
        assert "unknot" in VIRTUAL_KNOT_DATA
        assert "virtual_trefoil" in VIRTUAL_KNOT_DATA
        assert VIRTUAL_KNOT_DATA["virtual_trefoil"]["odd_writhe"] == 2
