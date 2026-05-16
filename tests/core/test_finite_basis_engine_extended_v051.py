"""Coverage-targeted tests for finite_basis_engine.py (v0.5.1)."""
import pytest
from pytop.finite_basis_engine import (
    FiniteBasisEngineError,
    generated_topology_from_basis,
    local_base_report,
    continuity_via_basis_preimage,
    minimal_basis,
    minimal_basis_report,
    _normalize_carrier,
    _normalize_family,
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


def _t0_space():
    return _space([1, 2], [set(), {1}, {1, 2}])


# ---------------------------------------------------------------------------
# _normalize_carrier errors  (line 327-328)
# ---------------------------------------------------------------------------

def test_normalize_carrier_string_raises():
    with pytest.raises(FiniteBasisEngineError):
        _normalize_carrier("abc")


def test_normalize_carrier_none_raises():
    with pytest.raises(FiniteBasisEngineError):
        _normalize_carrier(None)


def test_normalize_carrier_unhashable():
    with pytest.raises(FiniteBasisEngineError):
        _normalize_carrier([[1, 2]])  # list is not hashable


# ---------------------------------------------------------------------------
# _normalize_family errors  (lines 340-343)
# ---------------------------------------------------------------------------

def test_normalize_family_member_not_subset_of_carrier():
    carrier = frozenset({1, 2})
    with pytest.raises(FiniteBasisEngineError, match="not a subset"):
        _normalize_family([[1, 3]], carrier)


def test_normalize_family_unhashable_member():
    with pytest.raises(FiniteBasisEngineError, match="hashable"):
        _normalize_family([[[1, 2]]], None)  # inner list is unhashable


# ---------------------------------------------------------------------------
# local_base_report with FiniteTopologicalSpace  (lines 200-201)
# ---------------------------------------------------------------------------

def test_local_base_report_with_finite_space_object():
    space = _discrete2()
    # basis: all singletons
    candidate = [{1}, {2}]
    report = local_base_report(space, 1, candidate)
    assert "point" in report
    assert report["point"] == 1
    assert "is_local_base" in report


def test_local_base_report_with_finite_space_topology():
    space = _t0_space()
    # {1} is the minimal open neighborhood of 1
    candidate = [{1}]
    report = local_base_report(space, 1, candidate)
    assert report["is_local_base"] is True


# ---------------------------------------------------------------------------
# continuity_via_basis_preimage errors  (lines 228, 231)
# ---------------------------------------------------------------------------

def test_continuity_via_basis_preimage_not_a_topology():
    # Missing empty set → not a valid topology
    with pytest.raises(FiniteBasisEngineError, match="topology"):
        continuity_via_basis_preimage(
            [1, 2],
            [{1, 2}],          # missing ∅ → invalid
            [{1}, {2}],
            {1: 1, 2: 2},
        )


def test_continuity_via_basis_preimage_missing_domain_point():
    with pytest.raises(FiniteBasisEngineError, match="missing domain points"):
        continuity_via_basis_preimage(
            [1, 2],
            [set(), {1}, {2}, {1, 2}],
            [{1}],
            {1: 1},  # 2 is missing
        )


def test_continuity_via_basis_preimage_identity_is_continuous():
    result = continuity_via_basis_preimage(
        [1, 2],
        [set(), {1}, {2}, {1, 2}],
        [{1}, {2}],
        {1: 1, 2: 2},
    )
    assert result["is_continuous_via_basis"] is True


# ---------------------------------------------------------------------------
# minimal_basis  (lines 259-275)
# ---------------------------------------------------------------------------

def test_minimal_basis_discrete():
    space = _discrete2()
    basis = minimal_basis(space)
    # Discrete topology: minimal basis = singletons
    assert frozenset({1}) in basis
    assert frozenset({2}) in basis


def test_minimal_basis_indiscrete():
    space = _indiscrete2()
    basis = minimal_basis(space)
    # Indiscrete: only non-empty open set is {1,2}
    assert frozenset({1, 2}) in basis


def test_minimal_basis_t0():
    # {1,2} with opens {∅, {1}, {1,2}}
    space = _t0_space()
    basis = minimal_basis(space)
    # Minimal nbhd of 1 is {1}; minimal nbhd of 2 is {1,2}
    assert frozenset({1}) in basis
    assert frozenset({1, 2}) in basis


def test_minimal_basis_three_point_chain():
    # 1 <= 2 <= 3 order topology: opens {∅, {3}, {2,3}, {1,2,3}}
    carrier = frozenset({1, 2, 3})
    topology = frozenset([
        frozenset(), frozenset({3}), frozenset({2, 3}), frozenset({1, 2, 3})
    ])
    space = FiniteTopologicalSpace(carrier=carrier, topology=topology)
    basis = minimal_basis(space)
    assert frozenset({3}) in basis
    assert frozenset({2, 3}) in basis
    assert frozenset({1, 2, 3}) in basis


def test_minimal_basis_returns_tuple():
    space = _discrete2()
    basis = minimal_basis(space)
    assert isinstance(basis, tuple)


def test_minimal_basis_no_duplicates():
    space = _discrete2()
    basis = minimal_basis(space)
    assert len(basis) == len(set(basis))


# ---------------------------------------------------------------------------
# minimal_basis_report  (lines 284-287)
# ---------------------------------------------------------------------------

def test_minimal_basis_report_discrete():
    space = _discrete2()
    report = minimal_basis_report(space)
    assert report["carrier"] == frozenset({1, 2})
    assert report["minimal_basis_size"] == 2
    assert report["topology_size"] == 4
    assert "reduction_ratio" in report
    assert report["reduction_ratio"] == round(4 / 2, 3)


def test_minimal_basis_report_keys():
    space = _t0_space()
    report = minimal_basis_report(space)
    for key in ("carrier", "topology_size", "minimal_basis",
                "minimal_basis_size", "reduction_ratio"):
        assert key in report


def test_minimal_basis_report_indiscrete():
    space = _indiscrete2()
    report = minimal_basis_report(space)
    # Only one non-trivial open set in basis
    assert report["minimal_basis_size"] == 1
    assert report["reduction_ratio"] is not None
