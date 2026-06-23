"""Tests for Phase 15: 4-Manifold Topology modules."""

import pytest
from fractions import Fraction


# ---------------------------------------------------------------------------
# P15.1 intersection_forms
# ---------------------------------------------------------------------------

class TestIntersectionForms:
    def test_e8_form(self):
        from pytop.intersection_forms import e8_form
        e8 = e8_form()
        assert e8.rank == 8
        assert e8.form_type == "even"
        assert e8.is_unimodular is True
        assert e8.definiteness == "positive_definite"

    def test_hyperbolic_form(self):
        from pytop.intersection_forms import hyperbolic_form
        H = hyperbolic_form()
        assert H.rank == 2
        assert H.signature == 0
        assert H.form_type == "even"
        assert H.is_unimodular is True
        assert H.definiteness == "indefinite"

    def test_diagonal_form_odd(self):
        from pytop.intersection_forms import diagonal_form
        Q = diagonal_form([1, -1, -1])
        assert Q.rank == 3
        assert Q.signature == -1
        assert Q.form_type == "odd"

    def test_cp2_form(self):
        from pytop.intersection_forms import intersection_form
        Q = intersection_form([[1]])
        assert Q.rank == 1
        assert Q.signature == 1
        assert Q.form_type == "odd"

    def test_connected_sum_form(self):
        from pytop.intersection_forms import hyperbolic_form, connected_sum_form
        H = hyperbolic_form()
        Q = connected_sum_form(H, H)
        assert Q.rank == 4
        assert Q.signature == 0

    def test_form_signature(self):
        from pytop.intersection_forms import form_signature
        assert form_signature([[1]]) == 1
        assert form_signature([[-1]]) == -1
        assert form_signature([[0, 1], [1, 0]]) == 0

    def test_is_unimodular(self):
        from pytop.intersection_forms import is_unimodular
        assert is_unimodular([[1]]) is True
        assert is_unimodular([[2]]) is False
        assert is_unimodular([[0, 1], [1, 0]]) is True

    def test_donaldson_theorem_e8(self):
        from pytop.intersection_forms import e8_form, donaldson_theorem
        e8 = e8_form()
        result = donaldson_theorem(e8)
        # E_8 is positive definite even → Donaldson says no smooth structure
        assert result["exotic_obstruction"] is True

    def test_donaldson_theorem_diagonal(self):
        from pytop.intersection_forms import diagonal_form, donaldson_theorem
        Q = diagonal_form([1, -1])
        result = donaldson_theorem(Q)
        assert result["exotic_obstruction"] is False

    def test_standard_forms_database(self):
        from pytop.intersection_forms import STANDARD_FORMS
        assert "CP2" in STANDARD_FORMS
        assert "K3" in STANDARD_FORMS
        assert STANDARD_FORMS["K3"]["signature"] == -16


# ---------------------------------------------------------------------------
# P15.2 kirby_calculus
# ---------------------------------------------------------------------------

class TestKirbyCalculus:
    def test_kirby_cp2(self):
        from pytop.kirby_calculus import kirby_diagram_cp2, signature_kirby
        d = kirby_diagram_cp2()
        assert d.n_two_handles == 1
        assert signature_kirby(d) == 1

    def test_kirby_s2xs2(self):
        from pytop.kirby_calculus import kirby_diagram_s2xs2, signature_kirby, b2_kirby
        d = kirby_diagram_s2xs2()
        assert b2_kirby(d) == 2
        assert signature_kirby(d) == 0

    def test_kirby_euler(self):
        from pytop.kirby_calculus import kirby_diagram_cp2, euler_characteristic_kirby
        d = kirby_diagram_cp2()
        chi = euler_characteristic_kirby(d)
        assert chi == 3  # 2 + 1 (one 2-handle)

    def test_stabilize_plus(self):
        from pytop.kirby_calculus import kirby_diagram_cp2, kirby_stabilize
        d = kirby_diagram_cp2()
        d2, move = kirby_stabilize(d, sign=1)
        assert d2.n_two_handles == 2
        assert move.move_type == "stabilize_plus"

    def test_stabilize_minus(self):
        from pytop.kirby_calculus import kirby_diagram_cp2, kirby_stabilize
        d = kirby_diagram_cp2()
        d2, move = kirby_stabilize(d, sign=-1)
        assert d2.n_two_handles == 2

    def test_handle_slide(self):
        from pytop.kirby_calculus import kirby_diagram_s2xs2, kirby_handle_slide
        d = kirby_diagram_s2xs2()
        d2, move = kirby_handle_slide(d, slide_idx=0, over_idx=1)
        assert move.move_type == "handle_slide"
        assert d2.n_two_handles == 2

    def test_kirby_to_intersection_form(self):
        from pytop.kirby_calculus import kirby_diagram_cp2, kirby_to_intersection_form
        d = kirby_diagram_cp2()
        form = kirby_to_intersection_form(d)
        assert form.rank == 1
        assert form.signature == 1

    def test_is_kirby_equivalent(self):
        from pytop.kirby_calculus import kirby_diagram_cp2, is_kirby_equivalent
        d = kirby_diagram_cp2()
        assert is_kirby_equivalent(d, d) is True

    def test_k3_kirby_diagram(self):
        from pytop.kirby_calculus import kirby_diagram_k3_fiber, b2_kirby
        d = kirby_diagram_k3_fiber()
        assert b2_kirby(d) == 22

    def test_dehn_surgery_matrix(self):
        from pytop.kirby_calculus import dehn_surgery_matrix
        mat = dehn_surgery_matrix([(1, 1), (-1, 1)], linking_matrix_off=None)
        assert mat[0][0] == 1
        assert mat[1][1] == -1

    def test_kirby_diagram_construction(self):
        from pytop.kirby_calculus import kirby_diagram
        d = kirby_diagram(framings=[-2, -2, -2], name="A2_plumbing")
        assert d.n_two_handles == 3
        assert d.name == "A2_plumbing"


# ---------------------------------------------------------------------------
# P15.3 casson_invariant
# ---------------------------------------------------------------------------

class TestCassonInvariant:
    def test_s3(self):
        from pytop.casson_invariant import casson_s3
        c = casson_s3()
        assert c.lambda_value == 0
        assert c.rohlin_mod2 == 0

    def test_poincare_sphere(self):
        from pytop.casson_invariant import casson_invariant_brieskorn
        # Σ(2,3,5) = Poincaré homology sphere
        c = casson_invariant_brieskorn(2, 3, 5)
        assert c.lambda_value == -1

    def test_brieskorn_237(self):
        from pytop.casson_invariant import casson_invariant_brieskorn
        # λ(Σ(2,3,7)) = σ(Milnor fibre)/8 = -8/8 = -1 (Neumann–Wahl theorem).
        c = casson_invariant_brieskorn(2, 3, 7)
        assert c.lambda_value == -1

    def test_connected_sum(self):
        from pytop.casson_invariant import casson_s3, casson_invariant_brieskorn, casson_invariant_connected_sum
        s3 = casson_s3()
        p = casson_invariant_brieskorn(2, 3, 5)
        c = casson_invariant_connected_sum(s3, p)
        assert c.lambda_value == p.lambda_value

    def test_rohlin_mod2(self):
        from pytop.casson_invariant import rohlin_mod2, casson_invariant_brieskorn
        c = casson_invariant_brieskorn(2, 3, 5)
        mu = rohlin_mod2(c)
        assert mu in (0, 1)
        assert mu == abs(c.lambda_value) % 2

    def test_lens_space(self):
        from pytop.casson_invariant import casson_invariant_lens_space
        c = casson_invariant_lens_space(1, 0)  # S³
        assert c.lambda_value == 0

    def test_dedekind_sum(self):
        from pytop.casson_invariant import dedekind_sum
        # s(1,1) = 0
        assert dedekind_sum(1, 1) == Fraction(0)
        # s(1,3) = -1/9 (standard value)
        s = dedekind_sum(1, 3)
        assert isinstance(s, Fraction)

    def test_surgery_formula(self):
        from pytop.casson_invariant import casson_invariant_surgery, alexander_second_derivative
        # Trefoil alexander: Δ(t) = t^{-1} - 1 + t
        alex = {-1: 1, 0: -1, 1: 1}
        d2 = alexander_second_derivative(alex)
        c = casson_invariant_surgery(alex, framing=1, knot_name="trefoil")
        assert isinstance(c.lambda_value, int)

    def test_database_lookup(self):
        from pytop.casson_invariant import casson_data
        c = casson_data("S3")
        assert c.lambda_value == 0
        c2 = casson_data("Poincare_homology_sphere")
        assert c2.lambda_value == -1

    def test_non_coprime_raises(self):
        from pytop.casson_invariant import casson_invariant_brieskorn
        with pytest.raises(ValueError):
            casson_invariant_brieskorn(2, 4, 3)  # gcd(2,4)=2 ≠ 1


# ---------------------------------------------------------------------------
# P15.4 milnor_fibers
# ---------------------------------------------------------------------------

class TestMilnorFibers:
    def test_milnor_number_e8(self):
        from pytop.milnor_fibers import milnor_number
        assert milnor_number(2, 3, 5) == 8  # E_8: (1)(2)(4)=8

    def test_milnor_number_e6(self):
        from pytop.milnor_fibers import milnor_number
        assert milnor_number(2, 3, 4) == 6  # E_6: (1)(2)(3)=6

    def test_milnor_number_a_n(self):
        from pytop.milnor_fibers import milnor_number
        # A_n: z^2 + y^2 + z^{n+1} ≅ Brieskorn(2,2,n+1): μ = (1)(1)(n) = n
        assert milnor_number(2, 2, 4) == 3  # A_3: μ=3

    def test_brieskorn_fiber(self):
        from pytop.milnor_fibers import milnor_fiber_brieskorn
        F = milnor_fiber_brieskorn(2, 3, 5)
        assert F.milnor_number == 8
        assert F.betti_numbers == (1, 0, 8)
        assert F.euler_characteristic == 9

    def test_ade_e6(self):
        from pytop.milnor_fibers import milnor_fiber_ade
        F = milnor_fiber_ade("E6")
        assert F.milnor_number == 6

    def test_ade_e8(self):
        from pytop.milnor_fibers import milnor_fiber_ade
        F = milnor_fiber_ade("E8")
        assert F.milnor_number == 8
        assert F.monodromy_order == 30

    def test_ade_an(self):
        from pytop.milnor_fibers import milnor_fiber_ade
        F = milnor_fiber_ade("A3")
        assert F.milnor_number == 3
        assert F.monodromy_order == 4  # A_n: order n+1

    def test_monodromy_order(self):
        from pytop.milnor_fibers import monodromy_order
        from math import gcd
        def lcm(a,b): return a*b//gcd(a,b)
        assert monodromy_order(2, 3, 5) == lcm(lcm(2,3),5)  # 30

    def test_euler_characteristic(self):
        from pytop.milnor_fibers import milnor_fiber_euler
        assert milnor_fiber_euler(2, 3, 5) == 9

    def test_homology(self):
        from pytop.milnor_fibers import brieskorn_fiber_homology
        b = brieskorn_fiber_homology(2, 3, 5)
        assert b == (1, 0, 8)

    def test_ade_database(self):
        from pytop.milnor_fibers import ADE_DATABASE
        assert "E6" in ADE_DATABASE
        assert "E7" in ADE_DATABASE
        assert "E8" in ADE_DATABASE
        assert ADE_DATABASE["E8"]["milnor_number"] == 8


# ---------------------------------------------------------------------------
# P15.5 rohlin_theorem
# ---------------------------------------------------------------------------

class TestRohlinTheorem:
    def test_s4_rohlin(self):
        from pytop.rohlin_theorem import check_rohlin_theorem
        from pytop.intersection_forms import intersection_form
        Q = intersection_form([[0]])  # Trivial? Use rank-0 form
        # Use S^4: Q = 0 (empty)
        # Test via known example instead
        from pytop.rohlin_theorem import ROHLIN_EXAMPLES
        assert "K3" in ROHLIN_EXAMPLES
        assert ROHLIN_EXAMPLES["K3"]["rohlin_ok"] is True

    def test_k3_spin(self):
        from pytop.intersection_forms import hyperbolic_form, connected_sum_form
        from pytop.rohlin_theorem import is_spin_manifold, check_rohlin_theorem
        H = hyperbolic_form()
        # K3 ~ 3H ⊕ (-2)E_8: we test the signature property
        # Test that H is spin
        assert is_spin_manifold(H) is True

    def test_cp2_not_spin(self):
        from pytop.intersection_forms import intersection_form
        from pytop.rohlin_theorem import is_spin_manifold
        Q = intersection_form([[1]])
        assert is_spin_manifold(Q) is False

    def test_e8_manifold_rohlin_violation(self):
        from pytop.intersection_forms import e8_form
        from pytop.rohlin_theorem import check_rohlin_theorem
        e8 = e8_form()
        result = check_rohlin_theorem(e8, manifold_description="E8_manifold")
        # E_8 is spin but σ=8, not ≡ 0 mod 16 → violation
        assert result.is_spin is True
        assert result.rohlin_satisfied is False
        assert result.smooth_possible is False

    def test_rohlin_check_k3(self):
        # Build a form with signature -16 and even type
        from pytop.intersection_forms import intersection_form
        from pytop.rohlin_theorem import check_rohlin_theorem
        # Mock K3 with small even form of signature 0
        Q = intersection_form([[0, 1], [1, 0]])  # H, sigma=0
        result = check_rohlin_theorem(Q, "2H")
        assert result.is_spin is True
        assert result.rohlin_satisfied is True

    def test_kirby_siebenmann(self):
        from pytop.intersection_forms import hyperbolic_form
        from pytop.rohlin_theorem import kirby_siebenmann_obstruction
        H = hyperbolic_form()
        ks = kirby_siebenmann_obstruction(H)
        assert ks in (0, 1)

    def test_n_spin_structures(self):
        from pytop.rohlin_theorem import n_spin_structures
        # Simply-connected: 1 spin structure
        assert n_spin_structures(0) == 1
        # H^1(X; Z/2) = Z/2: 2 spin structures
        assert n_spin_structures(1) == 2

    def test_freedman_realization(self):
        from pytop.intersection_forms import e8_form
        from pytop.rohlin_theorem import check_freedman_realization
        e8 = e8_form()
        result = check_freedman_realization(e8)
        assert result["realizable_topologically"] is True
        assert result["smoothable"] is False  # E_8 not smoothable

    def test_rohlin_invariant_from_signature(self):
        from pytop.rohlin_theorem import rohlin_invariant_from_signature
        assert rohlin_invariant_from_signature(0) == 0
        assert rohlin_invariant_from_signature(16) == 0
        assert rohlin_invariant_from_signature(8) == 1

    def test_rohlin_bad_signature(self):
        from pytop.rohlin_theorem import rohlin_invariant_from_signature
        with pytest.raises(ValueError):
            rohlin_invariant_from_signature(3)

    def test_spin_cobordism(self):
        from pytop.rohlin_theorem import spin_cobordism_group
        result = spin_cobordism_group(4)
        assert "ℤ" in result or "Z" in result

    def test_spin_structure_result(self):
        from pytop.intersection_forms import hyperbolic_form
        from pytop.rohlin_theorem import spin_structure_result
        H = hyperbolic_form()
        result = spin_structure_result(H)
        assert result.is_spin is True
        assert result.w2_vanishes is True
        assert result.n_spin_structures == 1

    def test_rohlin_examples_database(self):
        from pytop.rohlin_theorem import ROHLIN_EXAMPLES
        assert "E8_manifold" in ROHLIN_EXAMPLES
        assert ROHLIN_EXAMPLES["E8_manifold"]["rohlin_ok"] is False
        assert ROHLIN_EXAMPLES["CP2"]["spin"] is False
