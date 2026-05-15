"""Tests for metric_contracts.py."""

import pytest
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_contracts import (
    MetricContract,
    bounded_metric_transform_contract,
    equivalent_metric_contract,
    finite_metric_contract,
    finite_product_metric_contract,
    metric_contract_summary,
)


def _discrete_metric(x, y):
    return 0 if x == y else 1


MS2 = FiniteMetricSpace(carrier=(0, 1), distance=_discrete_metric)
MS3 = FiniteMetricSpace(carrier=(1, 2, 3), distance=_discrete_metric)
MS_ABC = FiniteMetricSpace(carrier=("a", "b", "c"), distance=_discrete_metric)


# ---------------------------------------------------------------------------
# MetricContract.to_result
# ---------------------------------------------------------------------------

class TestMetricContractToResult:
    def test_true_status_gives_true_result(self):
        c = MetricContract("test", "true", "exact", carrier_size=3, metric_kind="finite")
        r = c.to_result()
        assert r.is_true

    def test_false_status_gives_false_result(self):
        c = MetricContract("test", "false", "exact", warnings=("invalid",))
        r = c.to_result()
        assert r.is_false

    def test_conditional_status(self):
        c = MetricContract("test", "conditional", "symbolic")
        r = c.to_result()
        assert r.status == "conditional"

    def test_unknown_status(self):
        c = MetricContract("test", "unknown", "symbolic")
        r = c.to_result()
        assert r.is_unknown

    def test_metadata_forwarded(self):
        c = MetricContract("test", "true", "exact", carrier_size=2,
                           metadata={"extra": "data"})
        r = c.to_result()
        assert r.metadata["extra"] == "data"
        assert r.metadata["carrier_size"] == 2


# ---------------------------------------------------------------------------
# finite_metric_contract
# ---------------------------------------------------------------------------

class TestFiniteMetricContract:
    def test_valid_metric_gives_true(self):
        c = finite_metric_contract(MS3)
        assert c.status == "true"
        assert c.carrier_size == 3
        assert c.metric_kind == "finite"

    def test_to_result_is_true(self):
        c = finite_metric_contract(MS2)
        assert c.to_result().is_true

    def test_carrier_size_matches(self):
        c = finite_metric_contract(MS_ABC)
        assert c.carrier_size == 3

    def test_no_carrier_gives_unknown(self):
        from pytop.metric_spaces import MetricSpace
        sp = MetricSpace(carrier=None, distance=_discrete_metric)
        c = finite_metric_contract(sp)
        assert c.status == "unknown"

    def test_custom_name(self):
        c = finite_metric_contract(MS3, name="my_metric")
        assert c.name == "my_metric"


# ---------------------------------------------------------------------------
# bounded_metric_transform_contract
# ---------------------------------------------------------------------------

class TestBoundedMetricTransformContract:
    def test_normalized_transform_gives_true(self):
        c = bounded_metric_transform_contract(MS3, transform="normalized")
        assert c.status == "true"
        assert c.metric_kind == "bounded_transform"

    def test_capped_transform_gives_true(self):
        c = bounded_metric_transform_contract(MS2, transform="capped")
        assert c.status == "true"

    def test_invalid_transform_gives_false(self):
        c = bounded_metric_transform_contract(MS3, transform="unknown_transform")
        assert c.status == "false"

    def test_result_has_transform_metadata(self):
        c = bounded_metric_transform_contract(MS2, transform="normalized")
        assert c.to_result().is_true


# ---------------------------------------------------------------------------
# finite_product_metric_contract
# ---------------------------------------------------------------------------

class TestFiniteProductMetricContract:
    def test_two_factor_product(self):
        c = finite_product_metric_contract(MS2, MS3)
        assert c.status == "true"
        assert c.carrier_size == 6  # 2 * 3
        assert c.metadata["factor_count"] == 2

    def test_single_factor(self):
        c = finite_product_metric_contract(MS3)
        assert c.status == "true"
        assert c.carrier_size == 3

    def test_no_factors_gives_false(self):
        c = finite_product_metric_contract()
        assert c.status == "false"

    def test_three_factors(self):
        c = finite_product_metric_contract(MS2, MS2, MS_ABC)
        assert c.status == "true"
        assert c.carrier_size == 12  # 2 * 2 * 3

    def test_mode_max_is_default(self):
        c = finite_product_metric_contract(MS2, MS3)
        assert c.to_result().is_true


# ---------------------------------------------------------------------------
# equivalent_metric_contract
# ---------------------------------------------------------------------------

class TestEquivalentMetricContract:
    def test_none_inputs_give_unknown(self):
        c = equivalent_metric_contract(None, None)
        assert c.status == "unknown"

    def test_no_witness_gives_unknown(self):
        c = equivalent_metric_contract(MS2, MS3, witness=None)
        assert c.status == "unknown"

    def test_true_witness(self):
        c = equivalent_metric_contract(MS2, MS2, witness=lambda a, b: True)
        assert c.status == "true"

    def test_false_witness(self):
        c = equivalent_metric_contract(MS2, MS2, witness=lambda a, b: False)
        assert c.status == "false"


# ---------------------------------------------------------------------------
# metric_contract_summary
# ---------------------------------------------------------------------------

class TestMetricContractSummary:
    def test_summary_is_string(self):
        c = finite_metric_contract(MS3)
        s = metric_contract_summary(c)
        assert isinstance(s, str)

    def test_summary_contains_status(self):
        c = finite_metric_contract(MS3)
        assert "true" in metric_contract_summary(c)

    def test_summary_contains_name(self):
        c = finite_metric_contract(MS3, name="my_contract")
        assert "my_contract" in metric_contract_summary(c)
