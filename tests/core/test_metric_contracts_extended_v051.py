"""Coverage-targeted tests for metric_contracts.py (v0.5.1)."""
import pytest
from pytop.metric_spaces import FiniteMetricSpace, MetricSpace
from pytop.metric_contracts import (
    bounded_metric_transform_contract,
    equivalent_metric_contract,
    finite_metric_contract,
    finite_product_metric_contract,
)


def _discrete(x, y):
    return 0.0 if x == y else 1.0


_MS2 = FiniteMetricSpace(carrier=(0, 1), distance=_discrete)


class _BadCarrierSpace:
    """carrier is not None but not iterable → tuple(carrier) raises TypeError."""
    carrier = 42
    distance = None


class _NullCarrierSpace:
    """carrier attribute is None → finite_metric_contract returns 'unknown'."""
    carrier = None
    distance = None


# ---------------------------------------------------------------------------
# finite_metric_contract — lines 48-49 (TypeError on tuple(carrier))
# ---------------------------------------------------------------------------

def test_finite_metric_contract_non_iterable_carrier_returns_unknown():
    result = finite_metric_contract(_BadCarrierSpace())
    assert result.status == "unknown"
    assert any("not an explicit finite iterable" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# bounded_metric_transform_contract — line 57 (base.status != "true")
# ---------------------------------------------------------------------------

def test_bounded_metric_transform_base_fails_early_return():
    # carrier=None → base.status="unknown" → line 57 triggers early return
    result = bounded_metric_transform_contract(_NullCarrierSpace())
    assert result.status == "unknown"
    assert result.metric_kind == "bounded_transform"


def test_bounded_metric_transform_unknown_transform_false():
    # valid base but unknown transform name → line 63
    result = bounded_metric_transform_contract(_MS2, transform="logarithmic")
    assert result.status == "false"


# ---------------------------------------------------------------------------
# finite_product_metric_contract — lines 74-75 (factor with status != "true")
# ---------------------------------------------------------------------------

def test_finite_product_metric_contract_invalid_factor():
    # _NullCarrierSpace has carrier=None → factor_contract.status="unknown" → lines 74-75
    result = finite_product_metric_contract(_NullCarrierSpace())
    assert result.status == "unknown"
    assert result.metric_kind == "product"


# ---------------------------------------------------------------------------
# equivalent_metric_contract — line 86 (not both valid metrics)
# ---------------------------------------------------------------------------

def test_equivalent_metric_contract_left_invalid():
    # left has carrier=None → left_contract.status="unknown" → line 86
    result = equivalent_metric_contract(
        _NullCarrierSpace(), _MS2, witness=lambda a, b: True
    )
    assert result.status == "unknown"
    assert result.mode == "mixed"
