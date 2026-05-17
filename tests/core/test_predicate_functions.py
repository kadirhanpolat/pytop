"""Tests for src/pytop/predicate_functions.py."""

import pytest

from pytop.predicate_functions import (
    MathFunction,
    PredicateFunctionError,
    abs_value,
    double,
    function_from,
    negate_fn,
    square,
    successor,
)
from pytop.predicate_sets import N, R, Z


# ===========================================================================
# Pre-built: successor, square, double, abs_value, negate_fn
# ===========================================================================

class TestSuccessor:
    def test_basic_values(self):
        assert successor(0) == 1
        assert successor(9) == 10

    def test_out_of_domain_raises(self):
        with pytest.raises(PredicateFunctionError):
            successor(-1)   # -1 not in N

    def test_repr_contains_arrow(self):
        assert "→" in repr(successor)

    def test_name(self):
        assert successor.name == "succ"


class TestSquare:
    def test_basic_values(self):
        assert square(0) == 0
        assert square(3) == 9
        assert square(10) == 100

    def test_out_of_domain_raises(self):
        with pytest.raises(PredicateFunctionError):
            square(-1)

    def test_float_not_in_domain(self):
        with pytest.raises(PredicateFunctionError):
            square(2.5)


class TestDouble:
    def test_positive(self):
        assert double(5) == 10

    def test_negative(self):
        assert double(-3) == -6

    def test_zero(self):
        assert double(0) == 0

    def test_float_not_in_domain(self):
        with pytest.raises(PredicateFunctionError):
            double(1.5)


class TestAbsValue:
    def test_positive(self):
        assert abs_value(3.5) == 3.5

    def test_negative(self):
        assert abs_value(-2.7) == 2.7

    def test_zero(self):
        assert abs_value(0.0) == 0.0

    def test_int_in_R(self):
        assert abs_value(-5) == 5


class TestNegateFn:
    def test_positive_becomes_negative(self):
        assert negate_fn(3.0) == -3.0

    def test_negative_becomes_positive(self):
        assert negate_fn(-7.0) == 7.0

    def test_zero(self):
        assert negate_fn(0.0) == 0.0


# ===========================================================================
# apply / __call__
# ===========================================================================

class TestApply:
    def test_apply_is_call(self):
        assert square.apply(4) == square(4) == 16

    def test_out_of_domain_raises(self):
        with pytest.raises(PredicateFunctionError):
            successor(-3)

    def test_out_of_codomain_raises(self):
        # Function that maps N → N but rule produces negative
        bad = function_from(N, N, lambda x: -x - 1, name="bad")
        with pytest.raises(PredicateFunctionError):
            bad(0)


# ===========================================================================
# restrict_to
# ===========================================================================

class TestRestrictTo:
    def test_square_restrict(self):
        result = square.restrict_to(range(5))
        assert result == {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

    def test_successor_restrict(self):
        result = successor.restrict_to(range(3))
        assert result == {0: 1, 1: 2, 2: 3}

    def test_out_of_domain_skipped(self):
        result = square.restrict_to([-1, 0, 1, 2])
        assert -1 not in result
        assert result == {0: 0, 1: 1, 2: 4}

    def test_empty_elements(self):
        assert square.restrict_to([]) == {}


# ===========================================================================
# compose
# ===========================================================================

class TestCompose:
    def test_square_compose_successor(self):
        # (square ∘ successor)(3) = square(successor(3)) = square(4) = 16
        ss = square.compose(successor)
        assert ss(3) == 16

    def test_successor_compose_double(self):
        # (successor ∘ double)(3) = successor(double(3)) = successor(6) = 7
        # Note: double is Z→Z and successor is N→N; codomain mismatch by name
        # Test composition that IS valid: square ∘ successor (both N→N)
        sq_succ = square.compose(successor)
        # (square ∘ successor)(3) = square(successor(3)) = square(4) = 16
        assert sq_succ(3) == 16

    def test_composition_name(self):
        comp = square.compose(successor)
        assert "∘" in comp.name

    def test_domain_mismatch_raises(self):
        # double: Z→Z, square: N→N; codomain of square (N) != domain of double (Z)
        with pytest.raises(PredicateFunctionError):
            double.compose(square)

    def test_abs_compose_negate(self):
        # (abs ∘ negate)(x) = |−x| = |x|  (both R→R, valid)
        abs_neg = abs_value.compose(negate_fn)
        assert abs_neg(3.0) == 3.0
        assert abs_neg(-5.0) == 5.0


# ===========================================================================
# Structural tests
# ===========================================================================

class TestStructuralChecks:
    def test_successor_injective(self):
        assert successor.is_injective_on(range(10))

    def test_constant_not_injective(self):
        const = function_from(N, N, lambda x: 0, name="0")
        assert not const.is_injective_on(range(5))

    def test_square_not_surjective_on_0_1_2_3_4(self):
        # square(N) does not hit every value in {0,1,2,3,4}
        assert not square.is_surjective_on(range(5), range(5))

    def test_identity_bijective(self):
        ident = function_from(N, N, lambda x: x, name="id")
        elems = list(range(5))
        assert ident.is_bijective_on(elems, elems)

    def test_double_not_bijective_on_0_4(self):
        # double maps {0,1,2} → {0,2,4} which is not all of {0,1,2,3,4}
        assert not double.is_bijective_on([0, 1, 2], [0, 1, 2, 3, 4])


# ===========================================================================
# function_from constructor
# ===========================================================================

class TestFunctionFrom:
    def test_custom_rule(self):
        cube = function_from(N, N, lambda x: x ** 3, name="x³")
        assert cube(3) == 27

    def test_auto_name(self):
        f = function_from(N, N, lambda x: x + 2)
        assert "ℕ" in repr(f)

    def test_custom_name_in_repr(self):
        cube = function_from(N, N, lambda x: x ** 3, name="x³")
        assert "x³" in repr(cube)

    def test_domain_codomain_stored(self):
        f = function_from(R, R, lambda x: x * 2, name="2x")
        assert f.domain is R
        assert f.codomain is R
