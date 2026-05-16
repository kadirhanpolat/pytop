"""Coverage-targeted tests for connectedness.py (v0.5.1)."""
import pytest
from pytop.connectedness import (
    ConnectednessError,
    normalize_connectedness_property,
    analyze_connectedness,
    is_connected,
    is_path_connected,
    is_locally_connected,
    is_arc_connected,
    is_totally_disconnected,
    is_scattered,
    _finite_t1_check,
    _finite_t0_check,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _space(carrier_list, opens_list):
    carrier = frozenset(carrier_list)
    topology = frozenset(frozenset(u) for u in opens_list)
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


def _discrete2():
    return _space(
        [1, 2],
        [set(), {1}, {2}, {1, 2}]
    )


def _indiscrete2():
    return _space([1, 2], [set(), {1, 2}])


def _single():
    return _space([1], [set(), {1}])


# ---------------------------------------------------------------------------
# ConnectednessError — line 47
# ---------------------------------------------------------------------------

def test_normalize_invalid_property():
    with pytest.raises(ConnectednessError):
        normalize_connectedness_property("foobar")


# ---------------------------------------------------------------------------
# is_arc_connected — finite exact logic  (lines 104-133)
# ---------------------------------------------------------------------------

def test_is_arc_connected_singleton_true():
    space = _single()
    r = is_arc_connected(space)
    assert r.is_true
    assert r.mode == "exact"


def test_is_arc_connected_indiscrete_true():
    space = _indiscrete2()
    r = is_arc_connected(space)
    assert r.is_true
    assert r.mode == "exact"


def test_is_arc_connected_discrete_false():
    space = _discrete2()
    r = is_arc_connected(space)
    assert r.is_false
    assert r.mode == "exact"


def test_is_arc_connected_nontrivial_non_indiscrete_false():
    # {1,2} with topology {∅, {1}, {1,2}} — T0 but not indiscrete
    space = _space([1, 2], [set(), {1}, {1, 2}])
    r = is_arc_connected(space)
    assert r.is_false


# ---------------------------------------------------------------------------
# is_totally_disconnected — finite exact logic  (lines 135-150)
# ---------------------------------------------------------------------------

def test_is_totally_disconnected_discrete_true():
    space = _discrete2()
    r = is_totally_disconnected(space)
    assert r.is_true
    assert r.mode == "exact"


def test_is_totally_disconnected_indiscrete_false():
    space = _indiscrete2()
    r = is_totally_disconnected(space)
    assert r.is_false
    assert r.mode == "exact"


def test_is_totally_disconnected_singleton_true():
    space = _single()
    r = is_totally_disconnected(space)
    assert r.is_true


# ---------------------------------------------------------------------------
# is_scattered — finite exact logic  (lines 152-173)
# ---------------------------------------------------------------------------

def test_is_scattered_discrete_true():
    # Discrete = T0, should be scattered
    space = _discrete2()
    r = is_scattered(space)
    assert r.is_true
    assert r.mode == "exact"


def test_is_scattered_indiscrete_false():
    # Indiscrete on 2 points is NOT T0
    space = _indiscrete2()
    r = is_scattered(space)
    assert r.is_false
    assert r.mode == "exact"


def test_is_scattered_t0_nontrivial_true():
    # {1,2} with topology {∅, {1}, {1,2}} — T0
    space = _space([1, 2], [set(), {1}, {1, 2}])
    r = is_scattered(space)
    assert r.is_true


# ---------------------------------------------------------------------------
# Shorthand aliases — lines 209, 213, 217
# ---------------------------------------------------------------------------

def test_is_arc_connected_alias():
    r = is_arc_connected(_single())
    assert r.is_true


def test_is_totally_disconnected_alias():
    r = is_totally_disconnected(_discrete2())
    assert r.is_true


def test_is_scattered_alias():
    r = is_scattered(_discrete2())
    assert r.is_true


# ---------------------------------------------------------------------------
# is_locally_connected  (line 224 neighborhood)
# ---------------------------------------------------------------------------

def test_is_locally_connected_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["locally_connected"])
    r = is_locally_connected(space)
    assert r.is_true


def test_is_locally_connected_finite():
    r = is_locally_connected(_discrete2())
    # discrete 2-point space — result is true or unknown (finite exact or tag)
    assert r.is_true or r.is_unknown


# ---------------------------------------------------------------------------
# _finite_t1_check  (lines 242-248)
# ---------------------------------------------------------------------------

def test_finite_t1_check_discrete_true():
    opens = [set(), {1}, {2}, {1, 2}]
    assert _finite_t1_check(opens, [1, 2]) is True


def test_finite_t1_check_indiscrete_false():
    opens = [set(), {1, 2}]
    assert _finite_t1_check(opens, [1, 2]) is False


def test_finite_t1_check_single_point_true():
    opens = [set(), {1}]
    assert _finite_t1_check(opens, [1]) is True


# ---------------------------------------------------------------------------
# _finite_t0_check  (lines 252-256)
# ---------------------------------------------------------------------------

def test_finite_t0_check_discrete_true():
    opens = [set(), {1}, {2}, {1, 2}]
    assert _finite_t0_check(opens, [1, 2]) is True


def test_finite_t0_check_indiscrete_false():
    opens = [set(), {1, 2}]
    assert _finite_t0_check(opens, [1, 2]) is False


def test_finite_t0_check_t0_not_t1():
    # {1,2} with {∅, {1}, {1,2}} — T0
    opens = [set(), {1}, {1, 2}]
    assert _finite_t0_check(opens, [1, 2]) is True


def test_finite_t0_check_single_true():
    assert _finite_t0_check([set(), {1}], [1]) is True


# ---------------------------------------------------------------------------
# analyze_connectedness — tag-based paths
# ---------------------------------------------------------------------------

def test_analyze_connectedness_not_connected_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["not_connected"])
    r = analyze_connectedness(space, "connected")
    assert r.is_false


def test_analyze_connectedness_arc_connected_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["arc_connected"])
    r = analyze_connectedness(space, "arc_connected")
    assert r.is_true


def test_analyze_connectedness_totally_disconnected_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["totally_disconnected"])
    r = analyze_connectedness(space, "totally_disconnected")
    assert r.is_true


def test_analyze_connectedness_scattered_tag():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["scattered"])
    r = analyze_connectedness(space, "scattered")
    assert r.is_true


# ---------------------------------------------------------------------------
# _finite_connected_from_topology — line 224 (None topology or None carrier)
# ---------------------------------------------------------------------------

from pytop.connectedness import _finite_connected_from_topology


class _NullTopoSpace:
    carrier = frozenset({1, 2})
    topology = None


class _NullCarrierSpace:
    carrier = None
    topology = frozenset([frozenset(), frozenset({1, 2})])


def test_finite_connected_from_topology_none_topology():
    result = _finite_connected_from_topology(_NullTopoSpace())
    assert result is None


def test_finite_connected_from_topology_none_carrier():
    result = _finite_connected_from_topology(_NullCarrierSpace())
    assert result is None
