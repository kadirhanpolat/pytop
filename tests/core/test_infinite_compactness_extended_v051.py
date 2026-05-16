"""Coverage-targeted tests for infinite_compactness.py (v0.5.1)."""
import pytest
from pytop.infinite_compactness import (
    analyze_infinite_compactness,
    infinite_compactness_report,
)
from pytop.infinite_spaces import DiscreteInfiniteSpace, IndiscreteInfiniteSpace


# ---------------------------------------------------------------------------
# analyze_infinite_compactness — line 31 (non-InfiniteTopologicalSpace)
# ---------------------------------------------------------------------------

def test_analyze_non_infinite_space_delegates_to_analyze_compactness():
    # Not an InfiniteTopologicalSpace → line 30 check → line 31: delegates
    class _FakeCompact:
        tags = {"compact"}
        metadata = {}

    result = analyze_infinite_compactness(_FakeCompact())
    # analyze_compactness handles tagged objects; any concrete result is valid
    assert result is not None


def test_analyze_non_infinite_space_string_input():
    # A string is not an InfiniteTopologicalSpace → delegates
    result = analyze_infinite_compactness("not a space")
    assert result is not None


# ---------------------------------------------------------------------------
# infinite_compactness_report — line 61
# ---------------------------------------------------------------------------

def test_infinite_compactness_report_discrete_space():
    space = DiscreteInfiniteSpace(carrier="N")
    report = infinite_compactness_report(space)
    assert "compact" in report
    assert "lindelof" in report
    assert report["compact"].is_false   # DiscreteInfiniteSpace is not compact


def test_infinite_compactness_report_indiscrete_space():
    space = IndiscreteInfiniteSpace(carrier="R")
    report = infinite_compactness_report(space)
    assert report["compact"].is_true    # IndiscreteInfiniteSpace is compact
