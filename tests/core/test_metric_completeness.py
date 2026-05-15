"""Tests for metric_completeness.py — is_complete, is_totally_bounded,
metric_compactness_check, analyze_metric_completeness."""

import pytest
from pytop.metric_spaces import FiniteMetricSpace
from pytop.metric_completeness import (
    MetricCompletenessError,
    analyze_metric_completeness,
    is_complete,
    is_totally_bounded,
    metric_compactness_check,
)


def _discrete(n):
    pts = set(range(n))
    return FiniteMetricSpace(pts, lambda x, y: 0.0 if x == y else 1.0)


def _line(pts):
    return FiniteMetricSpace(set(pts), lambda x, y: abs(x - y))


# ---------------------------------------------------------------------------
# is_complete
# ---------------------------------------------------------------------------

class TestIsComplete:
    def test_finite_metric_space_is_complete(self):
        r = is_complete(_discrete(3))
        assert r.is_true
        assert r.mode == "exact"

    def test_carrier_size_in_metadata(self):
        r = is_complete(_discrete(5))
        assert r.metadata["carrier_size"] == 5

    def test_operator_name_in_metadata(self):
        r = is_complete(_discrete(2))
        assert r.metadata["operator"] == "is_complete"

    def test_non_metric_object_returns_unknown(self):
        r = is_complete("not a space")
        assert r.is_unknown

    def test_object_without_carrier_returns_unknown(self):
        class NoCarrier:
            pass
        r = is_complete(NoCarrier())
        assert r.is_unknown

    def test_justification_mentions_cauchy(self):
        r = is_complete(_discrete(2))
        assert any("Cauchy" in j for j in r.justification)


# ---------------------------------------------------------------------------
# is_totally_bounded
# ---------------------------------------------------------------------------

class TestIsTotallyBounded:
    def test_finite_space_is_totally_bounded(self):
        r = is_totally_bounded(_line([0, 1, 2]))
        assert r.is_true
        assert r.mode == "exact"

    def test_epsilon_witness_recorded_in_metadata(self):
        r = is_totally_bounded(_line([0, 1, 2]), epsilon=0.5)
        assert r.metadata["epsilon"] == 0.5
        assert r.metadata["net_size"] == 3

    def test_zero_epsilon_returns_false(self):
        r = is_totally_bounded(_line([0, 1, 2]), epsilon=0.0)
        assert r.is_false

    def test_negative_epsilon_returns_false(self):
        r = is_totally_bounded(_line([0, 1, 2]), epsilon=-1.0)
        assert r.is_false

    def test_non_metric_object_returns_unknown(self):
        r = is_totally_bounded(object())
        assert r.is_unknown

    def test_no_epsilon_still_returns_true(self):
        r = is_totally_bounded(_discrete(4))
        assert r.is_true
        assert r.metadata["epsilon"] is None


# ---------------------------------------------------------------------------
# metric_compactness_check
# ---------------------------------------------------------------------------

class TestMetricCompactnessCheck:
    def test_finite_space_is_compact(self):
        r = metric_compactness_check(_discrete(3))
        assert r.is_true
        assert r.metadata["compact"] is True
        assert r.metadata["complete"] is True
        assert r.metadata["totally_bounded"] is True

    def test_cilt_ii_corridor_in_metadata(self):
        r = metric_compactness_check(_discrete(2))
        assert "cilt_ii_corridor" in r.metadata

    def test_non_metric_returns_unknown(self):
        r = metric_compactness_check(42)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# analyze_metric_completeness
# ---------------------------------------------------------------------------

class TestAnalyzeMetricCompleteness:
    def test_returns_all_true_for_finite_space(self):
        r = analyze_metric_completeness(_line([0, 1, 2, 3]))
        assert r.is_true
        assert r.value["is_complete"] is True
        assert r.value["is_totally_bounded"] is True
        assert r.value["metric_compact"] is True

    def test_mode_is_exact_for_finite_space(self):
        r = analyze_metric_completeness(_discrete(3))
        assert r.mode == "exact"

    def test_v0147_corridor_record_in_metadata(self):
        r = analyze_metric_completeness(_discrete(3))
        assert r.metadata.get("v0_1_47_corridor_record") is True

    def test_epsilon_forwarded(self):
        r = analyze_metric_completeness(_line([0, 1, 2]), epsilon=0.5)
        tb_meta = r.metadata["totally_bounded"]
        assert tb_meta["metadata"]["epsilon"] == 0.5

    def test_complete_and_totally_bounded_nested(self):
        r = analyze_metric_completeness(_discrete(2))
        assert r.metadata["complete"]["status"] == "true"
        assert r.metadata["totally_bounded"]["status"] == "true"
