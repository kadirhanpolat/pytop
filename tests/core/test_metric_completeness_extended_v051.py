"""Coverage-targeted tests for metric_completeness.py (v0.5.1)."""
import pytest
from pytop.metric_completeness import (
    MetricCompletenessError,
    is_complete,
    is_totally_bounded,
    metric_compactness_check,
    _finite_metric_data,
)


class _NonIterableCarrier:
    """carrier is not None but not iterable — tuple(carrier) raises Exception (line 254-255)."""
    carrier = 42
    distance = None


class _EmptyCarrier:
    """carrier is an empty iterable — points is empty (line 258)."""
    carrier = ()
    distance = None


class _NoDistance:
    """Valid carrier, distance=None, no distance_between attribute (line 265)."""
    carrier = (1, 2)
    distance = None


# ---------------------------------------------------------------------------
# _finite_metric_data — lines 254-255 (non-iterable carrier)
# ---------------------------------------------------------------------------

def test_finite_metric_data_non_iterable_carrier_raises():
    with pytest.raises(TypeError):
        _finite_metric_data(_NonIterableCarrier())


def test_is_complete_non_iterable_carrier_returns_unknown():
    result = is_complete(_NonIterableCarrier())
    assert result.is_unknown


# ---------------------------------------------------------------------------
# _finite_metric_data — line 258 (empty carrier)
# ---------------------------------------------------------------------------

def test_finite_metric_data_empty_carrier_raises():
    with pytest.raises(MetricCompletenessError):
        _finite_metric_data(_EmptyCarrier())


def test_is_complete_empty_carrier_returns_unknown():
    result = is_complete(_EmptyCarrier())
    assert result.is_unknown


def test_is_totally_bounded_empty_carrier_returns_unknown():
    result = is_totally_bounded(_EmptyCarrier())
    assert result.is_unknown


def test_metric_compactness_check_empty_carrier_returns_unknown():
    result = metric_compactness_check(_EmptyCarrier())
    assert result.is_unknown


# ---------------------------------------------------------------------------
# _finite_metric_data — line 265 (no distance and no distance_between)
# ---------------------------------------------------------------------------

def test_finite_metric_data_no_distance_raises():
    with pytest.raises(TypeError, match="distance specification"):
        _finite_metric_data(_NoDistance())


def test_is_complete_no_distance_returns_unknown():
    result = is_complete(_NoDistance())
    assert result.is_unknown
