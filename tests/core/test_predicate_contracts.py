"""Tests for predicate_contracts.py."""

import pytest
from pytop.predicate_contracts import (
    SubsetPredicateContract,
    finite_subset_predicate_contract,
    subset_predicate_contract,
    subset_predicate_summary,
    symbolic_subset_predicate_contract,
)
from pytop.result import Result


def _is_nonempty(carrier, subset):
    return len(subset) > 0


def _is_open_in_discrete(carrier, subset):
    return True


# ---------------------------------------------------------------------------
# SubsetPredicateContract.to_result
# ---------------------------------------------------------------------------

class TestSubsetPredicateContractToResult:
    def test_true_status_returns_true_result(self):
        c = SubsetPredicateContract("my_pred", "true", "exact")
        r = c.to_result()
        assert r.is_true
        assert r.mode == "exact"

    def test_false_status_returns_false_result(self):
        c = SubsetPredicateContract("my_pred", "false", "exact")
        r = c.to_result()
        assert r.is_false

    def test_conditional_status(self):
        c = SubsetPredicateContract("cond_pred", "conditional", "theorem",
                                     assumptions=("assumption A",))
        r = c.to_result()
        assert r.status == "conditional"

    def test_unknown_status_returns_unknown(self):
        c = SubsetPredicateContract("unknown_pred", "unknown", "symbolic")
        r = c.to_result()
        assert r.is_unknown

    def test_metadata_forwarded(self):
        c = SubsetPredicateContract("p", "true", "exact",
                                     metadata={"extra": "val"})
        r = c.to_result()
        assert r.metadata["extra"] == "val"

    def test_predicate_name_in_result_metadata(self):
        c = SubsetPredicateContract("p", "true", "exact", carrier_size=5, subset_size=2)
        r = c.to_result()
        assert r.metadata["predicate_name"] == "p"
        assert r.metadata["carrier_size"] == 5
        assert r.metadata["subset_size"] == 2


# ---------------------------------------------------------------------------
# finite_subset_predicate_contract
# ---------------------------------------------------------------------------

class TestFiniteSubsetPredicateContract:
    def test_truthy_predicate_returns_true(self):
        c = finite_subset_predicate_contract([1, 2, 3], [1, 2], _is_nonempty,
                                              predicate_name="nonempty")
        assert c.status == "true"
        assert c.mode == "exact"

    def test_falsy_predicate_returns_false(self):
        def always_false(c, s): return False
        c = finite_subset_predicate_contract([1, 2], [1], always_false)
        assert c.status == "false"

    def test_subset_not_in_carrier_returns_false(self):
        c = finite_subset_predicate_contract([1, 2], [1, 5], _is_nonempty)
        assert c.status == "false"
        assert "not contained" in c.warnings[0]

    def test_sizes_recorded(self):
        c = finite_subset_predicate_contract([1, 2, 3], [1, 2], _is_nonempty)
        assert c.carrier_size == 3
        assert c.subset_size == 2

    def test_subset_recorded_in_metadata(self):
        c = finite_subset_predicate_contract([1, 2, 3], [2, 3], _is_nonempty)
        assert set(c.metadata["subset"]) == {2, 3}

    def test_empty_subset_and_nonempty_check_returns_false(self):
        c = finite_subset_predicate_contract([1, 2, 3], [], _is_nonempty)
        assert c.status == "false"

    def test_predicate_name_recorded(self):
        c = finite_subset_predicate_contract([1], [1], _is_open_in_discrete,
                                              predicate_name="is_open")
        assert c.predicate_name == "is_open"


# ---------------------------------------------------------------------------
# symbolic_subset_predicate_contract
# ---------------------------------------------------------------------------

class TestSymbolicSubsetPredicateContract:
    def test_returns_unknown_symbolic(self):
        c = symbolic_subset_predicate_contract("sym_pred")
        assert c.status == "unknown"
        assert c.mode == "symbolic"

    def test_reason_in_warnings(self):
        c = symbolic_subset_predicate_contract("p", reason="not enough data")
        assert "not enough data" in c.warnings

    def test_assumptions_forwarded(self):
        c = symbolic_subset_predicate_contract("p", assumptions=["assume X"])
        assert "assume X" in c.assumptions


# ---------------------------------------------------------------------------
# subset_predicate_contract (dispatcher)
# ---------------------------------------------------------------------------

class TestSubsetPredicateContract:
    def test_none_carrier_returns_symbolic_unknown(self):
        c = subset_predicate_contract(None, [1], _is_nonempty)
        assert c.status == "unknown"
        assert c.mode == "symbolic"

    def test_none_subset_returns_symbolic_unknown(self):
        c = subset_predicate_contract([1, 2], None, _is_nonempty)
        assert c.status == "unknown"

    def test_none_predicate_returns_symbolic_unknown(self):
        c = subset_predicate_contract([1, 2], [1], None)
        assert c.status == "unknown"

    def test_all_provided_delegates_to_finite(self):
        c = subset_predicate_contract([1, 2, 3], [1, 2], _is_nonempty)
        assert c.status == "true"
        assert c.mode == "exact"


# ---------------------------------------------------------------------------
# subset_predicate_summary
# ---------------------------------------------------------------------------

class TestSubsetPredicateSummary:
    def test_summary_contains_expected_fields(self):
        c = SubsetPredicateContract("my_pred", "true", "exact",
                                     subset_size=2)
        s = subset_predicate_summary(c)
        assert "my_pred" in s
        assert "true" in s
        assert "exact" in s
        assert "2" in s
