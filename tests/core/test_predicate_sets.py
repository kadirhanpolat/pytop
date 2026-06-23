"""Tests for src/pytop/predicate_sets.py."""

from fractions import Fraction

import pytest

from pytop.predicate_sets import (
    C,
    MathSet,
    N,
    N_plus,
    PredicateSetError,
    Q,
    R,
    R_plus,
    Sigma,
    Z,
    Z_plus,
    alphabet,
    complex_numbers,
    integers,
    natural_numbers,
    positive_integers,
    positive_naturals,
    positive_reals,
    rationals,
    reals,
    set_of,
)

# ===========================================================================
# Membership: base sets
# ===========================================================================

class TestNContains:
    def test_zero_in_N(self):
        assert 0 in N

    def test_positive_int_in_N(self):
        assert 5 in N

    def test_negative_int_not_in_N(self):
        assert -1 not in N

    def test_float_not_in_N(self):
        assert 2.0 not in N

    def test_bool_not_in_N(self):
        assert True not in N
        assert False not in N

    def test_string_not_in_N(self):
        assert "1" not in N


class TestZContains:
    def test_negative_in_Z(self):
        assert -5 in Z

    def test_zero_in_Z(self):
        assert 0 in Z

    def test_positive_in_Z(self):
        assert 7 in Z

    def test_float_not_in_Z(self):
        assert 1.5 not in Z

    def test_bool_not_in_Z(self):
        assert True not in Z


class TestQContains:
    def test_fraction_in_Q(self):
        assert Fraction(1, 3) in Q

    def test_integer_in_Q(self):
        assert 5 in Q

    def test_float_not_in_Q(self):
        assert 1.5 not in Q


class TestRContains:
    def test_float_in_R(self):
        assert 3.14 in R

    def test_int_in_R(self):
        assert 2 in R

    def test_fraction_in_R(self):
        assert Fraction(1, 2) in R

    def test_complex_not_in_R(self):
        assert complex(1, 1) not in R

    def test_bool_not_in_R(self):
        assert True not in R


class TestCContains:
    def test_complex_in_C(self):
        assert complex(1, 2) in C

    def test_real_in_C(self):
        assert 3.14 in C

    def test_int_in_C(self):
        assert 5 in C

    def test_string_not_in_C(self):
        assert "1" not in C


class TestSigmaContains:
    def test_lowercase_in_Sigma(self):
        assert "a" in Sigma
        assert "z" in Sigma

    def test_uppercase_not_in_Sigma(self):
        assert "A" not in Sigma

    def test_digit_not_in_Sigma(self):
        assert "1" not in Sigma

    def test_multi_char_not_in_Sigma(self):
        assert "ab" not in Sigma


# ===========================================================================
# Comprehension: where
# ===========================================================================

class TestMathSetWhere:
    def test_evens_contain_even(self):
        evens = N.where(lambda n: n % 2 == 0, name="Even ℕ")
        assert 4 in evens
        assert 100 in evens

    def test_evens_exclude_odd(self):
        evens = N.where(lambda n: n % 2 == 0, name="Even ℕ")
        assert 3 not in evens
        assert 7 not in evens

    def test_base_excluded(self):
        # negative integers excluded by base set N even if pred says True
        large = N.where(lambda n: n > 1000)
        assert -5 not in large

    def test_chained_where(self):
        # {n ∈ ℕ : n even and n > 10}
        evens = N.where(lambda n: n % 2 == 0)
        large_evens = evens.where(lambda n: n > 10)
        assert 12 in large_evens
        assert 8 not in large_evens
        assert 11 not in large_evens

    def test_name_auto_generated(self):
        evens = N.where(lambda n: n % 2 == 0)
        assert "ℕ" in repr(evens)

    def test_name_custom(self):
        evens = N.where(lambda n: n % 2 == 0, name="2ℕ")
        assert repr(evens) == "2ℕ"


# ===========================================================================
# Set operations
# ===========================================================================

class TestMathSetOperations:
    def test_intersection(self):
        A = N.where(lambda n: n % 2 == 0)   # even naturals
        B = N.where(lambda n: n % 3 == 0)   # multiples of 3
        AB = A.intersection(B)
        assert 6 in AB
        assert 4 not in AB
        assert 9 not in AB

    def test_union(self):
        A = N.where(lambda n: n % 2 == 0)
        B = N.where(lambda n: n == 1)
        AuB = A.union(B)
        assert 1 in AuB
        assert 4 in AuB
        assert 3 not in AuB

    def test_complement_in(self):
        evens = N.where(lambda n: n % 2 == 0)
        odds = evens.complement_in(N)
        assert 1 in odds
        assert 3 in odds
        assert 2 not in odds
        assert -1 not in odds  # not in universe

    def test_and_operator(self):
        A = N.where(lambda n: n > 5)
        B = N.where(lambda n: n < 10)
        AB = A & B
        assert 7 in AB
        assert 3 not in AB
        assert 11 not in AB

    def test_or_operator(self):
        A = N.where(lambda n: n == 0)
        B = N.where(lambda n: n == 1)
        AuB = A | B
        assert 0 in AuB
        assert 1 in AuB
        assert 2 not in AuB


# ===========================================================================
# to_frozenset
# ===========================================================================

class TestToFrozenset:
    def test_evens_in_range(self):
        evens = N.where(lambda n: n % 2 == 0)
        result = evens.to_frozenset(range(10))
        assert result == frozenset({0, 2, 4, 6, 8})

    def test_full_N_in_range(self):
        result = N.to_frozenset(range(5))
        assert result == frozenset({0, 1, 2, 3, 4})

    def test_filters_negatives(self):
        result = N.to_frozenset(range(-3, 4))
        assert result == frozenset({0, 1, 2, 3})

    def test_empty_elements(self):
        assert N.to_frozenset([]) == frozenset()

    def test_sigma_filter(self):
        chars = list("aB1cD")
        result = Sigma.to_frozenset(chars)
        assert result == frozenset({"a", "c"})


# ===========================================================================
# sample
# ===========================================================================

class TestSample:
    def test_N_sample_in_N(self):
        samples = N.sample(10)
        assert all(x in N for x in samples)
        assert len(samples) == 10

    def test_N_sample_deterministic(self):
        assert N.sample(5) == [0, 1, 2, 3, 4]

    def test_R_sample_in_R(self):
        samples = R.sample(5, seed=0)
        assert all(x in R for x in samples)

    def test_Sigma_sample_in_Sigma(self):
        samples = Sigma.sample(5)
        assert all(x in Sigma for x in samples)
        assert len(samples) == 5

    def test_no_sampler_raises(self):
        S = MathSet(name="?", predicate=lambda x: True)
        with pytest.raises(PredicateSetError):
            S.sample(5)

    def test_comprehension_sample_in_set(self):
        evens = N.where(lambda n: n % 2 == 0)
        samples = evens.sample(5, seed=0)
        assert all(x in evens for x in samples)


# ===========================================================================
# Aliases
# ===========================================================================

class TestAliases:
    def test_natural_numbers_is_N(self):
        assert natural_numbers is N

    def test_integers_is_Z(self):
        assert integers is Z

    def test_rationals_is_Q(self):
        assert rationals is Q

    def test_reals_is_R(self):
        assert reals is R

    def test_complex_numbers_is_C(self):
        assert complex_numbers is C

    def test_alphabet_is_Sigma(self):
        assert alphabet is Sigma

    def test_positive_naturals_is_N_plus(self):
        assert positive_naturals is N_plus

    def test_positive_integers_is_Z_plus(self):
        assert positive_integers is Z_plus

    def test_positive_reals_is_R_plus(self):
        assert positive_reals is R_plus


# ===========================================================================
# Derived sets: N_plus, Z_plus, R_plus
# ===========================================================================

class TestDerivedSets:
    def test_N_plus_excludes_zero(self):
        assert 0 not in N_plus

    def test_N_plus_includes_positive(self):
        assert 1 in N_plus
        assert 5 in N_plus

    def test_N_plus_excludes_negative(self):
        assert -1 not in N_plus

    def test_Z_plus_includes_positive(self):
        assert 3 in Z_plus

    def test_Z_plus_excludes_zero_and_negative(self):
        assert 0 not in Z_plus
        assert -2 not in Z_plus

    def test_R_plus_includes_positive_float(self):
        assert 0.001 in R_plus

    def test_R_plus_excludes_zero(self):
        assert 0 not in R_plus
        assert 0.0 not in R_plus


# ===========================================================================
# set_of convenience function
# ===========================================================================

class TestSetOf:
    def test_set_of_equivalence(self):
        evens_where = N.where(lambda n: n % 2 == 0, name="E")
        evens_set_of = set_of(N, lambda n: n % 2 == 0, name="E")
        # same membership
        for x in range(20):
            assert (x in evens_where) == (x in evens_set_of)

    def test_set_of_name(self):
        s = set_of(R, lambda x: x > 0, name="ℝ⁺")
        assert repr(s) == "ℝ⁺"


# ===========================================================================
# repr
# ===========================================================================

class TestRepr:
    def test_N_repr(self):
        assert repr(N) == "ℕ"

    def test_R_repr(self):
        assert repr(R) == "ℝ"

    def test_Sigma_repr(self):
        assert repr(Sigma) == "Σ"
