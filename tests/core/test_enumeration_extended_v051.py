"""Coverage-targeted tests for enumeration.py (v0.5.1)."""
import pytest
from pytop.enumeration import (
    enumerate_topologies,
    enumerate_topologies_on_n_points,
    enumerate_t0_topologies,
    enumerate_t1_topologies,
    enumerate_hausdorff_topologies,
    count_topologies_on_n_points,
    _is_topology,
)


# ---------------------------------------------------------------------------
# enumerate_topologies_on_n_points — n<0 raises ValueError (line 46)
# ---------------------------------------------------------------------------

def test_enumerate_negative_n_raises():
    with pytest.raises(ValueError, match="nonnegative"):
        enumerate_topologies_on_n_points(-1)


def test_enumerate_zero_points():
    spaces = enumerate_topologies_on_n_points(0)
    # Only topology on empty set: {∅}
    assert len(spaces) == 1


def test_enumerate_one_point():
    spaces = enumerate_topologies_on_n_points(1)
    assert len(spaces) == 1


def test_enumerate_two_points():
    spaces = enumerate_topologies_on_n_points(2)
    assert len(spaces) == 4  # known: 4 topologies on 2 points


# ---------------------------------------------------------------------------
# enumerate_t1_topologies — direct call (line 57)
# ---------------------------------------------------------------------------

def test_enumerate_t1_topologies_two_points():
    # On 2 points: only discrete topology is T1
    t1_spaces = enumerate_t1_topologies([1, 2])
    assert len(t1_spaces) == 1


def test_enumerate_t1_topologies_one_point():
    t1_spaces = enumerate_t1_topologies([1])
    assert len(t1_spaces) == 1


def test_enumerate_t1_topologies_empty():
    t1_spaces = enumerate_t1_topologies([])
    assert isinstance(t1_spaces, list)


# ---------------------------------------------------------------------------
# enumerate_t0_topologies and enumerate_hausdorff_topologies
# ---------------------------------------------------------------------------

def test_enumerate_t0_topologies_two_points():
    t0_spaces = enumerate_t0_topologies([1, 2])
    # On 2 points: discrete + one T0 non-discrete
    assert len(t0_spaces) >= 1


def test_enumerate_hausdorff_topologies_two_points():
    h_spaces = enumerate_hausdorff_topologies([1, 2])
    # Only discrete is Hausdorff on 2 points
    assert len(h_spaces) == 1


# ---------------------------------------------------------------------------
# _is_topology — no empty set (line 83), bad intersection (87), bad union (89)
# ---------------------------------------------------------------------------

def test_is_topology_missing_empty_set():
    # No empty set → line 83: return False
    family = {frozenset({1}), frozenset({1, 2})}
    assert _is_topology(family) is False


def test_is_topology_not_closed_under_intersection():
    # Has ∅ and {1,2,3}, but {1}∩{2}=∅ is in family,
    # {1}∩{1,2}={1} which IS in family...
    # Need: {1}∩{2}=∅ ✓, but what about {1,2}∩{1,3}={1}?
    # family = {∅, {1,2}, {1,3}, {1,2,3}}: {1,2}∩{1,3}={1} NOT in family → line 87
    family = {frozenset(), frozenset({1, 2}), frozenset({1, 3}), frozenset({1, 2, 3})}
    assert _is_topology(family) is False


def test_is_topology_not_closed_under_union():
    # family with ∅ and {1,2,3} but {1}∪{2}={1,2} NOT in family
    family = {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2, 3})}
    assert _is_topology(family) is False


def test_is_topology_valid_discrete():
    family = {frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})}
    assert _is_topology(family) is True


def test_is_topology_valid_indiscrete():
    family = {frozenset(), frozenset({1, 2})}
    assert _is_topology(family) is True


def test_is_topology_empty_family():
    # No empty set → False
    assert _is_topology(set()) is False


# ---------------------------------------------------------------------------
# count_topologies_on_n_points
# ---------------------------------------------------------------------------

def test_count_topologies_two_points():
    assert count_topologies_on_n_points(2) == 4


def test_count_topologies_one_point():
    assert count_topologies_on_n_points(1) == 1
