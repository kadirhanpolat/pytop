"""Tests for src/pytop/logic.py."""

import pytest

from pytop.logic import (
    Proposition,
    conjunction,
    disjunction,
    for_all,
    iff,
    implies,
    negate,
    there_exists,
    unique_exists,
)

# ---------------------------------------------------------------------------
# Proposition
# ---------------------------------------------------------------------------

class TestProposition:
    def test_truth_value_true(self):
        p = Proposition("p", True)
        assert bool(p) is True

    def test_truth_value_false(self):
        p = Proposition("p", False)
        assert bool(p) is False

    def test_repr_true(self):
        p = Proposition("raining", True)
        assert repr(p) == "raining=T"

    def test_repr_false(self):
        p = Proposition("sunny", False)
        assert repr(p) == "sunny=F"

    def test_frozen(self):
        p = Proposition("x", True)
        with pytest.raises((AttributeError, TypeError)):
            p.truth_value = False  # type: ignore[misc]

    def test_equality(self):
        assert Proposition("p", True) == Proposition("p", True)
        assert Proposition("p", True) != Proposition("p", False)


# ---------------------------------------------------------------------------
# Connectives
# ---------------------------------------------------------------------------

class TestNegate:
    def test_negate_true(self):
        p = Proposition("p", True)
        assert not negate(p)

    def test_negate_false(self):
        p = Proposition("p", False)
        assert negate(p)

    def test_double_negation(self):
        p = Proposition("p", True)
        assert bool(negate(negate(p))) is True


class TestConjunction:
    def test_all_true(self):
        ps = [Proposition(f"p{i}", True) for i in range(3)]
        assert conjunction(*ps)

    def test_one_false(self):
        ps = [Proposition("p", True), Proposition("q", False)]
        assert not conjunction(*ps)

    def test_single(self):
        assert conjunction(Proposition("p", True))
        assert not conjunction(Proposition("p", False))

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            conjunction()


class TestDisjunction:
    def test_all_false(self):
        ps = [Proposition(f"p{i}", False) for i in range(3)]
        assert not disjunction(*ps)

    def test_one_true(self):
        ps = [Proposition("p", False), Proposition("q", True)]
        assert disjunction(*ps)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            disjunction()


class TestImplies:
    # Truth table: T→T=T, T→F=F, F→T=T, F→F=T
    def test_tt(self):
        assert implies(Proposition("p", True), Proposition("q", True))

    def test_tf(self):
        assert not implies(Proposition("p", True), Proposition("q", False))

    def test_ft(self):
        assert implies(Proposition("p", False), Proposition("q", True))

    def test_ff(self):
        assert implies(Proposition("p", False), Proposition("q", False))


class TestIff:
    def test_tt(self):
        assert iff(Proposition("p", True), Proposition("q", True))

    def test_ff(self):
        assert iff(Proposition("p", False), Proposition("q", False))

    def test_tf(self):
        assert not iff(Proposition("p", True), Proposition("q", False))

    def test_ft(self):
        assert not iff(Proposition("p", False), Proposition("q", True))


# ---------------------------------------------------------------------------
# Quantifiers
# ---------------------------------------------------------------------------

class TestForAll:
    def test_all_even(self):
        assert for_all([2, 4, 6], lambda x: x % 2 == 0)

    def test_not_all_even(self):
        assert not for_all([2, 3, 6], lambda x: x % 2 == 0)

    def test_empty_carrier(self):
        assert for_all([], lambda x: False)  # vacuously true

    def test_singleton_true(self):
        assert for_all([5], lambda x: x > 0)

    def test_singleton_false(self):
        assert not for_all([0], lambda x: x > 0)


class TestThereExists:
    def test_exists(self):
        assert there_exists([1, 2, 3], lambda x: x == 2)

    def test_not_exists(self):
        assert not there_exists([1, 3, 5], lambda x: x % 2 == 0)

    def test_empty_carrier(self):
        assert not there_exists([], lambda x: True)


class TestUniqueExists:
    def test_unique(self):
        assert unique_exists([1, 2, 3, 4], lambda x: x == 3)

    def test_none(self):
        assert not unique_exists([1, 2, 3], lambda x: x > 10)

    def test_two(self):
        assert not unique_exists([1, 2, 3, 4], lambda x: x > 2)

    def test_empty(self):
        assert not unique_exists([], lambda x: True)
