"""Milestone S4 — extended axioms (T3/T4, countability) and new representations."""

from __future__ import annotations

from pytop.experimental.spaces import (
    CofiniteSpace,
    Decidability,
    DiscreteCountableSpace,
    FiniteSpace,
    OrderTopologySpace,
    SorgenfreyLineSpace,
    discrete_finite_space,
    is_first_countable,
    is_lindelof,
    is_second_countable,
    is_separable,
    is_t3,
    is_t4,
    rational_metric_space,
)

SIERPINSKI = FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}])


# --------------------------------------------------------------------------
# Composite separation axioms T3 / T4
# --------------------------------------------------------------------------

def test_discrete_is_t3_and_t4():
    d = discrete_finite_space({0, 1, 2})
    assert is_t3(d).value is True
    assert is_t4(d).value is True


def test_sierpinski_is_not_t3_or_t4():
    # Sierpinski is not even T1, so not T3/T4
    assert is_t3(SIERPINSKI).value is False
    assert is_t4(SIERPINSKI).value is False


def test_cofinite_is_not_t3():
    # cofinite is T1 but not regular -> not T3
    assert is_t3(CofiniteSpace()).value is False


def test_order_topology_is_t4():
    assert is_t4(OrderTopologySpace()).value is True


# --------------------------------------------------------------------------
# Countability / covering on finite spaces (trivially all hold)
# --------------------------------------------------------------------------

def test_finite_space_has_all_countability_properties():
    d = discrete_finite_space({0, 1, 2})
    assert is_lindelof(d).value is True
    assert is_separable(d).value is True
    assert is_second_countable(d).value is True
    assert is_first_countable(d).value is True


# --------------------------------------------------------------------------
# Infinite representations via certificates
# --------------------------------------------------------------------------

def test_order_topology_countability():
    q = OrderTopologySpace()
    assert is_separable(q).value is True
    assert is_second_countable(q).value is True
    assert is_lindelof(q).value is True


def test_metric_first_countable_but_others_undecided():
    m = rational_metric_space()
    assert is_first_countable(m).value is True
    # a generic metric space's separability/second-countability is not determined
    assert is_separable(m).decidability is Decidability.UNDECIDABLE
    assert is_second_countable(m).decidability is Decidability.UNDECIDABLE


# --------------------------------------------------------------------------
# Sorgenfrey line — the separable, first-countable, NOT second-countable example
# --------------------------------------------------------------------------

def test_sorgenfrey_line_certificates():
    s = SorgenfreyLineSpace()
    assert is_separable(s).value is True
    assert is_first_countable(s).value is True
    assert is_lindelof(s).value is True
    assert is_second_countable(s).value is False     # the classic gap
    assert is_t4(s).value is True                     # Sorgenfrey is normal + T1


def test_discrete_countable_is_second_countable():
    d = DiscreteCountableSpace()
    assert is_second_countable(d).value is True
    assert is_separable(d).value is True
    assert is_t4(d).value is True
