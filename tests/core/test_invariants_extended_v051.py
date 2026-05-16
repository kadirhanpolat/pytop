"""Coverage-targeted tests for invariants.py (v0.5.1)."""
import pytest
from pytop.invariants import (
    InvariantError,
    normalize_invariant_name,
    invariants_summary,
    _finite_invariant,
    _finite_lindelof_number,
    _local_character,
)


class _Obj:
    def __init__(self, tags=()):
        self.tags = set(tags)
        self.metadata = {}


class _NullTopoSpace:
    topology = None
    carrier = [1, 2]


class _WithTopoSpace:
    def __init__(self):
        self.topology = [frozenset(), frozenset({1, 2})]
        self.carrier = [1, 2]


# ---------------------------------------------------------------------------
# normalize_invariant_name — line 41 (unsupported invariant raises)
# ---------------------------------------------------------------------------

def test_normalize_invariant_name_unsupported_raises():
    with pytest.raises(InvariantError, match="Unsupported"):
        normalize_invariant_name("bad_invariant_name")


# ---------------------------------------------------------------------------
# invariants_summary — line 113 (called for all FINITE_INVARIANTS)
# ---------------------------------------------------------------------------

def test_invariants_summary_returns_dict():
    result = invariants_summary(_Obj())
    assert isinstance(result, dict)
    assert "weight" in result


# ---------------------------------------------------------------------------
# _finite_invariant — line 122 (topology is None → return None)
# ---------------------------------------------------------------------------

def test_finite_invariant_none_topology_returns_none():
    result = _finite_invariant(_NullTopoSpace(), "weight")
    assert result is None


# ---------------------------------------------------------------------------
# _finite_invariant — line 136 (unknown name → return None, dead via public API)
# ---------------------------------------------------------------------------

def test_finite_invariant_unknown_name_returns_none():
    result = _finite_invariant(_WithTopoSpace(), "unknown_foo")
    assert result is None


# ---------------------------------------------------------------------------
# _finite_lindelof_number — line 165 (empty points → return 0)
# ---------------------------------------------------------------------------

def test_finite_lindelof_number_empty_points_returns_zero():
    result = _finite_lindelof_number((), [])
    assert result == 0


# ---------------------------------------------------------------------------
# _local_character — line 214 (point not in any open set → return 0)
# ---------------------------------------------------------------------------

def test_local_character_point_not_in_any_open_returns_zero():
    # 99 is not in set() or {1, 2}, so neighborhoods = [] → line 214
    result = _local_character(99, [set(), {1, 2}])
    assert result == 0
