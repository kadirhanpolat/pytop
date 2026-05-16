"""Coverage-targeted tests for result.py and subbases.py (v0.5.1)."""
import pytest
from pytop.result import Result, merge_results
from pytop.subbases import (
    BasisConstructionError,
    is_basis_for_topology,
    is_local_base_at,
    _normalize_carrier,
)


# ===========================================================================
# result.py
# ===========================================================================

# ---------------------------------------------------------------------------
# Result.__post_init__ — invalid status (line 55)
# ---------------------------------------------------------------------------

def test_result_invalid_status_raises():
    with pytest.raises(ValueError, match="Invalid status"):
        Result(status="maybe", mode="exact")


# ---------------------------------------------------------------------------
# Result.__post_init__ — invalid mode (line 59)
# ---------------------------------------------------------------------------

def test_result_invalid_mode_raises():
    with pytest.raises(ValueError, match="Invalid mode"):
        Result(status="true", mode="guessed")


# ---------------------------------------------------------------------------
# Result.summary — with assumptions (line 97)
# ---------------------------------------------------------------------------

def test_summary_with_assumptions():
    r = Result.true(
        mode="theorem",
        assumptions=["X is metrizable."],
        justification=["Metrizable implies compact."],
    )
    text = r.summary()
    assert "assumptions" in text
    assert "justification" in text


def test_summary_no_assumptions():
    r = Result.true(mode="exact", justification=["trivial"])
    text = r.summary()
    assert "true" in text


# ---------------------------------------------------------------------------
# merge_results — no args raises (line 219)
# ---------------------------------------------------------------------------

def test_merge_results_no_args_raises():
    with pytest.raises(ValueError, match="at least one Result"):
        merge_results()


# ---------------------------------------------------------------------------
# merge_results — status "unknown" when any unknown (line 225)
# ---------------------------------------------------------------------------

def test_merge_results_unknown_wins():
    r1 = Result.true(mode="exact", justification=["a"])
    r2 = Result.unknown(mode="symbolic", justification=["b"])
    merged = merge_results(r1, r2)
    assert merged.is_unknown


# ---------------------------------------------------------------------------
# merge_results — status "true" when all true (line 227)
# ---------------------------------------------------------------------------

def test_merge_results_all_true():
    r1 = Result.true(mode="exact", justification=["a"])
    r2 = Result.true(mode="theorem", justification=["b"])
    merged = merge_results(r1, r2)
    assert merged.is_true


# ---------------------------------------------------------------------------
# merge_results — status "false" when all false (line 229)
# ---------------------------------------------------------------------------

def test_merge_results_all_false():
    r1 = Result.false(mode="exact", justification=["a"])
    r2 = Result.false(mode="theorem", justification=["b"])
    merged = merge_results(r1, r2)
    assert merged.is_false


# ---------------------------------------------------------------------------
# merge_results — status "conditional" for mixed
# ---------------------------------------------------------------------------

def test_merge_results_mixed_conditional():
    r1 = Result.true(mode="exact", justification=["a"])
    r2 = Result.false(mode="exact", justification=["b"])
    merged = merge_results(r1, r2)
    assert merged.is_conditional


# ===========================================================================
# subbases.py
# ===========================================================================

# ---------------------------------------------------------------------------
# is_basis_for_topology — _is_topology fails: missing ∅ (lines 65, 235)
# ---------------------------------------------------------------------------

def test_is_basis_for_topology_invalid_topo_no_empty():
    # topology = [[1,2]] — missing ∅ → _is_topology returns False (line 235)
    result = is_basis_for_topology([1, 2], [[1, 2]], topology=[[1, 2]])
    assert result is False


# ---------------------------------------------------------------------------
# is_basis_for_topology — _is_topology fails: not closed under union (lines 65, 239)
# ---------------------------------------------------------------------------

def test_is_basis_for_topology_invalid_topo_not_closed():
    # topology has ∅ and {1,2,3} but {1}∪{2}={1,2} not in it → line 239
    result = is_basis_for_topology(
        [1, 2, 3],
        [[1, 2, 3]],
        topology=[[], [1], [2], [1, 2, 3]],
    )
    assert result is False


# ---------------------------------------------------------------------------
# is_local_base — point not in carrier (line 173)
# ---------------------------------------------------------------------------

def test_is_local_base_point_not_in_carrier():
    result = is_local_base_at([1, 2], 99, [[1, 2]], topology=[[], [1, 2]])
    assert result is False


# ---------------------------------------------------------------------------
# is_local_base — invalid topology (line 176)
# ---------------------------------------------------------------------------

def test_is_local_base_invalid_topology():
    # topology missing ∅ → _is_topology returns False → line 176
    result = is_local_base_at([1, 2], 1, [[1, 2]], topology=[[1, 2]])
    assert result is False


# ---------------------------------------------------------------------------
# _resolve_space_inputs — no topology, not a space (line 196)
# ---------------------------------------------------------------------------

def test_is_basis_for_topology_no_topology_raises():
    with pytest.raises(BasisConstructionError, match="Topology data must be supplied"):
        is_basis_for_topology([1, 2], [[1, 2]])  # no topology= argument


# ---------------------------------------------------------------------------
# _normalize_carrier — TypeError (lines 204-205)
# ---------------------------------------------------------------------------

def test_normalize_carrier_none_raises():
    with pytest.raises(BasisConstructionError, match="finite iterable"):
        _normalize_carrier(None)


def test_is_basis_with_non_iterable_carrier_raises():
    # None as carrier → _normalize_carrier(None) → TypeError → lines 204-205
    with pytest.raises(BasisConstructionError, match="finite iterable"):
        is_basis_for_topology(None, [[]], topology=[[]])


# ---------------------------------------------------------------------------
# _normalize_subset_family — member not subset (line 218)
# ---------------------------------------------------------------------------

def test_is_basis_member_outside_carrier_raises():
    # basis member {1,2,3} is not subset of carrier {1,2} → line 218
    with pytest.raises(BasisConstructionError, match="subset of the carrier"):
        is_basis_for_topology([1, 2], [[1, 2, 3]], topology=[[], [1, 2]])
