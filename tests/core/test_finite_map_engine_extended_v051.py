"""Coverage-targeted tests for finite_map_engine.py (v0.5.1)."""
import pytest
from pytop.finite_map_engine import (
    FiniteMapEngineError,
    normalize_finite_map_data,
    continuity_checks_by_opens,
    _normalize_carrier,
    _normalize_subset,
    _normalize_topology,
)


_D2 = frozenset({1, 2})
_INDISCRETE2 = [frozenset(), frozenset({1, 2})]
_DISCRETE2 = [frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2})]


# ---------------------------------------------------------------------------
# _normalize_carrier — line 213 (None or string carrier raises)
# ---------------------------------------------------------------------------

def test_normalize_carrier_none_raises():
    with pytest.raises(FiniteMapEngineError, match="finite iterable"):
        _normalize_carrier(None, "domain")


def test_normalize_carrier_string_raises():
    with pytest.raises(FiniteMapEngineError, match="finite iterable"):
        _normalize_carrier("abc", "domain")


# ---------------------------------------------------------------------------
# _normalize_carrier — lines 216-217 (unhashable elements raises TypeError)
# ---------------------------------------------------------------------------

def test_normalize_carrier_unhashable_raises():
    with pytest.raises(FiniteMapEngineError, match="hashable"):
        _normalize_carrier([[1, 2], [3, 4]], "domain")


# ---------------------------------------------------------------------------
# _normalize_subset — lines 223-224 (unhashable subset raises TypeError)
# ---------------------------------------------------------------------------

def test_normalize_subset_unhashable_raises():
    with pytest.raises(FiniteMapEngineError, match="hashable"):
        _normalize_subset([[1, 2]], _D2, "subset")


# ---------------------------------------------------------------------------
# _normalize_topology — line 236 (None topology raises)
# ---------------------------------------------------------------------------

def test_normalize_topology_none_raises():
    with pytest.raises(FiniteMapEngineError, match="iterable of subsets"):
        _normalize_topology(None, _D2, "domain_topology")


# ---------------------------------------------------------------------------
# _normalize_topology — line 241 (member outside carrier raises)
# ---------------------------------------------------------------------------

def test_normalize_topology_member_outside_carrier_raises():
    # {99} ⊄ {1,2} → line 241
    with pytest.raises(FiniteMapEngineError, match="subset of the carrier"):
        _normalize_topology([frozenset(), {99}], _D2, "domain_topology")


# ---------------------------------------------------------------------------
# continuity_checks_by_opens — line 146 (invalid codomain topology raises)
# ---------------------------------------------------------------------------

def test_continuity_checks_invalid_codomain_topology_raises():
    # domain discrete (valid), codomain topology missing {1}∪{2}={1,2}... actually
    # use a minimal invalid: topology missing ∅
    invalid_codomain_topo = [frozenset({1, 2})]   # missing ∅ → not a topology
    with pytest.raises(FiniteMapEngineError, match="codomain_topology"):
        continuity_checks_by_opens(
            [1, 2], _DISCRETE2,
            [1, 2], invalid_codomain_topo,
            {1: 1, 2: 2},
        )
