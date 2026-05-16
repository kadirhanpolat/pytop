"""Coverage-targeted tests for order_lattice.py (v0.5.1)."""
import pytest
from pytop.order_lattice import (
    OrderLatticeError,
    leq,
    lower_bounds,
    upper_bounds,
    meet,
    join,
    is_lattice,
    linear_extension,
    _carrier_and_relation,
)


# ---------------------------------------------------------------------------
# _carrier_and_relation — raises for invalid input (line 31)
# ---------------------------------------------------------------------------

def test_carrier_and_relation_invalid_raises():
    with pytest.raises(OrderLatticeError, match="order-space object"):
        _carrier_and_relation("not_a_space")


def test_carrier_and_relation_invalid_number():
    with pytest.raises(OrderLatticeError):
        _carrier_and_relation(42)


# ---------------------------------------------------------------------------
# leq — full function body (lines 35-38)
# ---------------------------------------------------------------------------

def test_leq_true():
    carrier = (1, 2, 3)
    relation = {(1, 2), (2, 3)}
    assert leq((carrier, relation), 1, 2) is True


def test_leq_false():
    carrier = (1, 2, 3)
    relation = {(1, 2)}
    assert leq((carrier, relation), 2, 1) is False


def test_leq_element_not_in_carrier_raises():
    carrier = (1, 2)
    relation = {(1, 2)}
    with pytest.raises(OrderLatticeError, match="belong to the carrier"):
        leq((carrier, relation), 99, 1)


# ---------------------------------------------------------------------------
# meet — returns None for non-unique greatest lower bound (line 68)
# ---------------------------------------------------------------------------

def test_meet_returns_none():
    # Two incomparable lower bounds 3 and 4 for elements 1 and 2
    carrier = (1, 2, 3, 4)
    relation = {(3, 1), (3, 2), (4, 1), (4, 2)}
    result = meet((carrier, relation), 1, 2)
    assert result is None


def test_meet_returns_value():
    # Chain 1 ≤ 2 ≤ 3: meet(2, 3) = 2
    carrier = (1, 2, 3)
    relation = {(1, 2), (2, 3)}
    result = meet((carrier, relation), 2, 3)
    assert result == 2


# ---------------------------------------------------------------------------
# is_lattice — returns Result.false for non-partial-order (line 82)
# ---------------------------------------------------------------------------

def test_is_lattice_false_for_non_partial_order():
    # Symmetric non-trivial relation → not antisymmetric → not partial order
    carrier = (1, 2)
    relation = {(1, 2), (2, 1)}
    result = is_lattice((carrier, relation))
    assert result.is_false


def test_is_lattice_true_for_chain():
    carrier = (1, 2, 3)
    relation = {(1, 2), (2, 3)}
    result = is_lattice((carrier, relation))
    assert result.is_true


# ---------------------------------------------------------------------------
# linear_extension — raises for non-partial-order (line 140)
# ---------------------------------------------------------------------------

def test_linear_extension_raises_for_non_po():
    carrier = (1, 2)
    relation = {(1, 2), (2, 1)}
    with pytest.raises(OrderLatticeError, match="partial order"):
        linear_extension((carrier, relation))


def test_linear_extension_chain():
    carrier = (1, 2, 3)
    relation = {(1, 2), (2, 3)}
    ext = linear_extension((carrier, relation))
    assert ext.index(1) < ext.index(2) < ext.index(3)


# ---------------------------------------------------------------------------
# join and lower/upper bounds
# ---------------------------------------------------------------------------

def test_join_returns_none():
    # Two incomparable upper bounds
    carrier = (1, 2, 3, 4)
    relation = {(1, 3), (1, 4), (2, 3), (2, 4)}
    result = join((carrier, relation), 1, 2)
    assert result is None


def test_lower_bounds_chain():
    carrier = (1, 2, 3)
    relation = {(1, 2), (2, 3)}
    lbs = lower_bounds((carrier, relation), 2, 3)
    assert 1 in lbs
    assert 2 in lbs


def test_upper_bounds_chain():
    carrier = (1, 2, 3)
    relation = {(1, 2), (2, 3)}
    ubs = upper_bounds((carrier, relation), 1, 2)
    assert 2 in ubs
    assert 3 in ubs
