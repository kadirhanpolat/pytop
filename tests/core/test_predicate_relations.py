"""Tests for src/pytop/predicate_relations.py."""

import pytest

from pytop.predicate_relations import (
    MathRelation,
    PredicateRelationError,
    divides,
    geq,
    gt,
    leq,
    lt,
    relation_between,
    relation_on,
)
from pytop.predicate_sets import N, N_plus, R, Z


# ===========================================================================
# Pre-built: leq, lt, geq, gt
# ===========================================================================

class TestLeq:
    def test_holds_less(self):
        assert leq.holds(2, 5)

    def test_holds_equal(self):
        assert leq.holds(3, 3)

    def test_not_holds_greater(self):
        assert not leq.holds(5, 2)

    def test_call_syntax(self):
        assert leq(1, 10)
        assert not leq(10, 1)

    def test_float_comparison(self):
        assert leq.holds(1.5, 2.7)

    def test_out_of_domain_returns_false(self):
        assert not leq.holds("a", "b")  # strings not in R


class TestLt:
    def test_strict_less(self):
        assert lt.holds(2, 3)

    def test_equal_not_strict(self):
        assert not lt.holds(3, 3)


class TestGeqGt:
    def test_geq(self):
        assert geq.holds(5, 2)
        assert geq.holds(3, 3)
        assert not geq.holds(2, 5)

    def test_gt(self):
        assert gt.holds(5, 2)
        assert not gt.holds(3, 3)


# ===========================================================================
# Pre-built: divides
# ===========================================================================

class TestDivides:
    def test_divides_true(self):
        assert divides.holds(3, 12)
        assert divides.holds(1, 7)
        assert divides.holds(5, 5)

    def test_divides_false(self):
        assert not divides.holds(3, 7)
        assert not divides.holds(4, 6)

    def test_zero_not_in_N_plus(self):
        assert not divides.holds(0, 10)  # 0 not in N_plus

    def test_repr_contains_symbol(self):
        assert "∣" in repr(divides)


# ===========================================================================
# restrict_to / restrict_between
# ===========================================================================

class TestRestrictTo:
    def test_leq_on_1_2_3(self):
        result = leq.restrict_to([1, 2, 3])
        expected = {(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)}
        assert result == expected

    def test_lt_on_1_2_3(self):
        result = lt.restrict_to([1, 2, 3])
        expected = {(1,2),(1,3),(2,3)}
        assert result == expected

    def test_divides_on_1_2_3_6(self):
        result = divides.restrict_to([1, 2, 3, 6])
        assert (1, 6) in result
        assert (2, 6) in result
        assert (3, 6) in result
        assert (4, 6) not in result  # 4 not in carrier

    def test_restrict_between(self):
        R_custom = relation_between(N, N, lambda x, y: x + y == 5, name="sum=5")
        result = R_custom.restrict_between([1, 2, 3], [2, 3, 4])
        assert (1, 4) in result
        assert (2, 3) in result
        assert (3, 2) in result
        assert (1, 2) not in result


# ===========================================================================
# Inverse
# ===========================================================================

class TestInverse:
    def test_leq_inverse_is_geq(self):
        inv = leq.inverse()
        assert inv.holds(5, 2)     # 5 geq 2
        assert not inv.holds(2, 5) # 2 not geq 5

    def test_lt_inverse_is_gt(self):
        inv = lt.inverse()
        assert inv.holds(5, 2)
        assert not inv.holds(2, 5)
        assert not inv.holds(3, 3)

    def test_inverse_name(self):
        inv = leq.inverse()
        assert "⁻¹" in inv.name

    def test_divides_inverse(self):
        inv = divides.inverse()
        assert inv.holds(12, 3)   # 3 divides 12 → (12,3) in inverse
        assert not inv.holds(7, 3)


# ===========================================================================
# Structural tests
# ===========================================================================

class TestStructuralChecks:
    def test_leq_reflexive(self):
        assert leq.is_reflexive_on([1, 2, 3, 4, 5])

    def test_leq_antisymmetric(self):
        assert leq.is_antisymmetric_on([1, 2, 3, 4, 5])

    def test_leq_transitive(self):
        assert leq.is_transitive_on([1, 2, 3, 4, 5])

    def test_leq_is_partial_order(self):
        assert leq.is_partial_order_on([1, 2, 3])

    def test_leq_is_total_order(self):
        assert leq.is_total_order_on([1, 2, 3])

    def test_lt_not_reflexive(self):
        assert not lt.is_reflexive_on([1, 2, 3])

    def test_divides_is_partial_order_on_divisors_of_12(self):
        # {1, 2, 3, 4, 6, 12} forms a partial order under divisibility
        assert divides.is_partial_order_on([1, 2, 3, 4, 6, 12])

    def test_equivalence_mod2(self):
        mod2 = relation_on(N, lambda x, y: (x - y) % 2 == 0, name="≡₂")
        assert mod2.is_equivalence_on(range(6))

    def test_lt_not_symmetric(self):
        assert not lt.is_symmetric_on([1, 2, 3])


# ===========================================================================
# relation_on / relation_between
# ===========================================================================

class TestRelationOn:
    def test_custom_relation_holds(self):
        same_parity = relation_on(Z, lambda x, y: (x - y) % 2 == 0, name="≡₂")
        assert same_parity.holds(4, 8)
        assert same_parity.holds(3, 7)
        assert not same_parity.holds(3, 8)

    def test_domain_equals_codomain(self):
        R_custom = relation_on(N, lambda x, y: x == y, name="=")
        assert R_custom.domain is R_custom.codomain

    def test_auto_name(self):
        R_custom = relation_on(N, lambda x, y: x < y)
        assert "ℕ" in R_custom.name


class TestRelationBetween:
    def test_heterogeneous_holds(self):
        f_rel = relation_between(N, Sigma, lambda n, c: n == ord(c) - 97, name="ord")
        assert f_rel.holds(0, "a")
        assert f_rel.holds(25, "z")
        assert not f_rel.holds(1, "a")

    def test_out_of_domain_false(self):
        f_rel = relation_between(N, Sigma, lambda n, c: True, name="all")
        assert not f_rel.holds(-1, "a")   # -1 not in N
        assert not f_rel.holds(1, "A")    # "A" not in Sigma

    def test_repr_contains_times(self):
        f_rel = relation_between(N, R, lambda n, x: n < x, name="<")
        assert "×" in repr(f_rel)


from pytop.predicate_sets import Sigma  # noqa: E402
