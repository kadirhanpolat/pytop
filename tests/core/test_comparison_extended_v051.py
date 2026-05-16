"""Coverage-targeted tests for comparison.py (v0.5.1)."""
import pytest
from pytop.comparison import (
    compare_spaces,
    invariant_profile,
    finite_homeomorphism_result,
    compare_invariants,
    _space_is_finite,
    _carrier_size,
    _representation_of,
    _extract_tags,
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
    return _space([1, 2], [set(), {1}, {2}, {1, 2}])


def _indiscrete2():
    return _space([1, 2], [set(), {1, 2}])


def _single():
    return _space([1], [set(), {1}])


# ---------------------------------------------------------------------------
# finite_homeomorphism_result — non-finite → unknown (line 55)
# ---------------------------------------------------------------------------

def test_homeomorphism_non_finite_left_unknown():
    from pytop.spaces import TopologicalSpace
    sym = TopologicalSpace.symbolic(description="test")
    r = finite_homeomorphism_result(sym, _discrete2())
    assert r.is_unknown


def test_homeomorphism_non_finite_both_unknown():
    from pytop.spaces import TopologicalSpace
    sym1 = TopologicalSpace.symbolic(description="a")
    sym2 = TopologicalSpace.symbolic(description="b")
    r = finite_homeomorphism_result(sym1, sym2)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# finite_homeomorphism_result — different cardinalities → false (line 65)
# ---------------------------------------------------------------------------

def test_homeomorphism_different_sizes_false():
    r = finite_homeomorphism_result(_single(), _discrete2())
    assert r.is_false
    assert r.mode == "exact"


# ---------------------------------------------------------------------------
# finite_homeomorphism_result — same structure → true / false
# ---------------------------------------------------------------------------

def test_homeomorphism_identical_topology_true():
    s1 = _discrete2()
    s2 = _discrete2()
    r = finite_homeomorphism_result(s1, s2)
    assert r.is_true
    assert r.mode == "exact"


def test_homeomorphism_different_topology_false():
    # discrete vs indiscrete, same carrier size
    r = finite_homeomorphism_result(_discrete2(), _indiscrete2())
    assert r.is_false
    assert r.mode == "exact"


# ---------------------------------------------------------------------------
# _space_is_finite — exception path (lines 132-133)
# ---------------------------------------------------------------------------

def test_space_is_finite_exception_returns_false():
    class Bad:
        def is_finite(self):
            raise RuntimeError("broken")
    assert _space_is_finite(Bad()) is False


def test_space_is_finite_no_method_returns_false():
    class NoMethod:
        pass
    assert _space_is_finite(NoMethod()) is False


def test_space_is_finite_true_for_finite_space():
    assert _space_is_finite(_discrete2()) is True


# ---------------------------------------------------------------------------
# _carrier_size — None/str carrier (line 140) and exception (lines 143-144)
# ---------------------------------------------------------------------------

def test_carrier_size_none_carrier():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test")
    assert _carrier_size(space) is None


def test_carrier_size_string_carrier():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace(carrier="omega")
    assert _carrier_size(space) is None


def test_carrier_size_exception():
    class BadCarrier:
        def __len__(self):
            raise TypeError("no size")
    class Sp:
        carrier = BadCarrier()
    assert _carrier_size(Sp()) is None


def test_carrier_size_finite():
    assert _carrier_size(_discrete2()) == 2


# ---------------------------------------------------------------------------
# _representation_of — fallback path (line 152)
# ---------------------------------------------------------------------------

def test_representation_of_finite_space():
    # FiniteTopologicalSpace has metadata["representation"] = "finite"
    assert _representation_of(_discrete2()) == "finite"


def test_representation_of_no_metadata_representation():
    class NoRep:
        metadata = {"description": "bare"}
        def is_finite(self):
            return False
    assert _representation_of(NoRep()) == "symbolic_general"


def test_representation_of_finite_is_finite():
    class FiniteLike:
        metadata = {}
        def is_finite(self):
            return True
    assert _representation_of(FiniteLike()) == "finite"


# ---------------------------------------------------------------------------
# compare_spaces — integration
# ---------------------------------------------------------------------------

def test_compare_spaces_identical():
    result = compare_spaces(_discrete2(), _discrete2())
    assert result["basic_property_match"] is True
    assert result["same_cardinality"] is True


def test_compare_spaces_different():
    result = compare_spaces(_discrete2(), _indiscrete2())
    assert "left_profile" in result
    assert "right_profile" in result
    assert result["same_cardinality"] is True


# ---------------------------------------------------------------------------
# compare_invariants
# ---------------------------------------------------------------------------

def test_compare_invariants_same_space():
    result = compare_invariants(_discrete2(), _discrete2())
    assert "compact" in result
    assert result["compact"][0] == result["compact"][1]


def test_compare_invariants_keys():
    result = compare_invariants(_single(), _discrete2())
    for key in ("compact", "connected", "t0", "hausdorff"):
        assert key in result
