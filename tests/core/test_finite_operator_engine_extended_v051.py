"""Coverage-targeted tests for finite_operator_engine.py (v0.5.1)."""
import pytest
from pytop.finite_operator_engine import (
    FiniteOperatorEngineError,
    validate_topology_candidate,
    _normalize_carrier,
    _normalize_family,
    _normalize_subset,
)


# ---------------------------------------------------------------------------
# validate_topology_candidate — line 97 (intersection_failures)
# ---------------------------------------------------------------------------

def test_validate_intersection_failure_recorded():
    # {1,2} ∩ {1,3} = {1} NOT in the family → line 97 fires
    v = validate_topology_candidate(
        [1, 2, 3],
        [set(), {1, 2}, {1, 3}, {1, 2, 3}],
    )
    assert not v.is_topology
    assert len(v.intersection_failures) > 0


# ---------------------------------------------------------------------------
# _normalize_carrier — lines 251-252 (frozenset raises TypeError on unhashable)
# ---------------------------------------------------------------------------

def test_normalize_carrier_unhashable_elements_raises():
    # lists are unhashable → frozenset([[1,2]]) raises TypeError → lines 251-252
    with pytest.raises(FiniteOperatorEngineError, match="hashable"):
        _normalize_carrier([[1, 2], [3, 4]])


# ---------------------------------------------------------------------------
# _normalize_family — line 262 (family is None)
# ---------------------------------------------------------------------------

def test_normalize_family_none_raises():
    with pytest.raises(FiniteOperatorEngineError):
        _normalize_family(None, frozenset({1, 2}))


# ---------------------------------------------------------------------------
# _normalize_family — lines 266-267 (family is non-iterable)
# ---------------------------------------------------------------------------

def test_normalize_family_non_iterable_raises():
    # iter(42) raises TypeError → lines 266-267
    with pytest.raises(FiniteOperatorEngineError):
        _normalize_family(42, frozenset({1, 2}))


# ---------------------------------------------------------------------------
# _normalize_family — lines 271-272 (member is non-iterable)
# ---------------------------------------------------------------------------

def test_normalize_family_member_non_iterable_raises():
    # frozenset(42) raises TypeError → lines 271-272
    with pytest.raises(FiniteOperatorEngineError):
        _normalize_family([42], frozenset({1, 2}))


# ---------------------------------------------------------------------------
# _normalize_family — line 274 (member not subset of carrier)
# ---------------------------------------------------------------------------

def test_normalize_family_member_outside_carrier_raises():
    # {99} ⊄ {1,2}, allow_external=False → line 274
    with pytest.raises(FiniteOperatorEngineError, match="subset of the carrier"):
        _normalize_family([{99}], frozenset({1, 2}), allow_external=False)


# ---------------------------------------------------------------------------
# _normalize_subset — lines 282-283 (frozenset raises TypeError on unhashable)
# ---------------------------------------------------------------------------

def test_normalize_subset_unhashable_raises():
    # frozenset([[1,2]]) raises TypeError → lines 282-283
    with pytest.raises(FiniteOperatorEngineError, match="hashable"):
        _normalize_subset([[1, 2]], frozenset({1, 2}))


# ---------------------------------------------------------------------------
# _normalize_subset — line 285 (subset not contained in carrier)
# ---------------------------------------------------------------------------

def test_normalize_subset_outside_carrier_raises():
    # {99} ⊄ {1,2} → line 285
    with pytest.raises(FiniteOperatorEngineError, match="contained in the carrier"):
        _normalize_subset({99}, frozenset({1, 2}))
