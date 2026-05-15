"""Tests for construction_contracts.py."""

import pytest
from pytop.construction_contracts import (
    FiniteConstructionContract,
    finite_partition_contract,
    finite_product_contract,
    finite_product_summary,
    finite_quotient_contract,
    finite_quotient_summary,
)
from pytop.result import Result


# ---------------------------------------------------------------------------
# FiniteConstructionContract.to_result
# ---------------------------------------------------------------------------

class TestFiniteConstructionContractToResult:
    def test_true_status_returns_true_result(self):
        c = FiniteConstructionContract(kind="product", status="true",
                                       carrier_size=6, factor_count=2)
        r = c.to_result()
        assert r.is_true
        assert r.mode == "exact"

    def test_false_status_returns_false_result(self):
        c = FiniteConstructionContract(kind="product", status="false",
                                       warnings=("no factors",))
        r = c.to_result()
        assert r.is_false

    def test_unknown_status_returns_unknown(self):
        c = FiniteConstructionContract(kind="product", status="unknown")
        r = c.to_result()
        assert r.is_unknown

    def test_metadata_forwarded(self):
        c = FiniteConstructionContract(kind="product", status="true",
                                       carrier_size=4, metadata={"factor_sizes": [2, 2]})
        r = c.to_result()
        assert r.metadata["factor_sizes"] == [2, 2]
        assert r.metadata["carrier_size"] == 4

    def test_kind_in_result_value(self):
        c = FiniteConstructionContract(kind="quotient", status="true",
                                       carrier_size=3, block_count=2)
        r = c.to_result()
        assert r.value == "quotient"


# ---------------------------------------------------------------------------
# finite_product_contract
# ---------------------------------------------------------------------------

class TestFiniteProductContract:
    def test_two_factors(self):
        c = finite_product_contract([1, 2], [3, 4])
        assert c.status == "true"
        assert c.carrier_size == 4
        assert c.factor_count == 2

    def test_three_factors(self):
        c = finite_product_contract([1, 2], [3, 4], [5])
        assert c.status == "true"
        assert c.carrier_size == 4
        assert c.factor_count == 3

    def test_single_factor(self):
        c = finite_product_contract([[1, 2, 3]])
        assert c.status == "true"
        assert c.carrier_size == 3

    def test_empty_factors_list_returns_false(self):
        c = finite_product_contract()
        assert c.status == "false"

    def test_empty_factor_returns_false(self):
        c = finite_product_contract([1, 2], [])
        assert c.status == "false"

    def test_sample_in_metadata(self):
        c = finite_product_contract([1, 2], [3, 4])
        assert "sample" in c.metadata
        assert len(c.metadata["sample"]) > 0

    def test_factor_sizes_in_metadata(self):
        c = finite_product_contract([1, 2], [3, 4, 5])
        assert c.metadata["factor_sizes"] == [2, 3]

    def test_list_of_factors_variant(self):
        c = finite_product_contract([[1, 2], [3, 4]])
        assert c.status == "true"
        assert c.carrier_size == 4


# ---------------------------------------------------------------------------
# finite_product_summary
# ---------------------------------------------------------------------------

class TestFiniteProductSummary:
    def test_summary_is_string(self):
        s = finite_product_summary([1, 2], [3, 4])
        assert isinstance(s, str)

    def test_summary_contains_status(self):
        s = finite_product_summary([1, 2], [3, 4])
        assert "true" in s

    def test_summary_contains_factor_count(self):
        s = finite_product_summary([1, 2], [3, 4])
        assert "2" in s


# ---------------------------------------------------------------------------
# finite_partition_contract
# ---------------------------------------------------------------------------

class TestFinitePartitionContract:
    def test_valid_partition(self):
        c = finite_partition_contract([1, 2, 3], [[1], [2, 3]])
        assert c.status == "true"
        assert c.carrier_size == 3
        assert c.block_count == 2

    def test_trivial_partition(self):
        c = finite_partition_contract([1, 2, 3], [[1, 2, 3]])
        assert c.status == "true"
        assert c.block_count == 1

    def test_singleton_partition(self):
        c = finite_partition_contract([1, 2, 3], [[1], [2], [3]])
        assert c.status == "true"
        assert c.block_count == 3

    def test_empty_block_fails(self):
        c = finite_partition_contract([1, 2, 3], [[], [1, 2, 3]])
        assert c.status == "false"

    def test_block_outside_carrier_fails(self):
        c = finite_partition_contract([1, 2, 3], [[1, 99], [2, 3]])
        assert c.status == "false"

    def test_overlapping_blocks_fail(self):
        c = finite_partition_contract([1, 2, 3], [[1, 2], [2, 3]])
        assert c.status == "false"

    def test_partition_not_covering_carrier_fails(self):
        c = finite_partition_contract([1, 2, 3], [[1], [2]])
        assert c.status == "false"

    def test_block_sizes_in_metadata(self):
        c = finite_partition_contract([1, 2, 3], [[1], [2, 3]])
        assert "block_sizes" in c.metadata
        assert sorted(c.metadata["block_sizes"]) == [1, 2]


# ---------------------------------------------------------------------------
# finite_quotient_contract
# ---------------------------------------------------------------------------

class TestFiniteQuotientContract:
    def test_valid_partition_gives_quotient(self):
        c = finite_quotient_contract([1, 2, 3], [[1], [2, 3]])
        assert c.status == "true"
        assert c.kind == "quotient"
        assert c.block_count == 2

    def test_invalid_partition_gives_false_quotient(self):
        c = finite_quotient_contract([1, 2, 3], [[1, 2], [2, 3]])  # overlap
        assert c.status == "false"

    def test_quotient_to_result(self):
        c = finite_quotient_contract([1, 2, 3], [[1], [2, 3]])
        r = c.to_result()
        assert r.is_true


# ---------------------------------------------------------------------------
# finite_quotient_summary
# ---------------------------------------------------------------------------

class TestFiniteQuotientSummary:
    def test_summary_is_string(self):
        s = finite_quotient_summary([1, 2, 3], [[1], [2, 3]])
        assert isinstance(s, str)

    def test_summary_contains_quotient(self):
        s = finite_quotient_summary([1, 2, 3], [[1], [2, 3]])
        assert "quotient" in s

    def test_summary_contains_block_count(self):
        s = finite_quotient_summary([1, 2, 3], [[1], [2, 3]])
        assert "2" in s
