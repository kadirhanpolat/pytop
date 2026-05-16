"""Coverage-targeted tests for infinite_countability.py (v0.5.1)."""
import pytest
from pytop.infinite_countability import (
    analyze_infinite_countability,
    infinite_countability_report,
)
from pytop.infinite_spaces import DiscreteInfiniteSpace


# ---------------------------------------------------------------------------
# analyze_infinite_countability — line 31 (non-InfiniteTopologicalSpace)
# ---------------------------------------------------------------------------

def test_analyze_non_infinite_space_delegates():
    # Not an InfiniteTopologicalSpace → line 31 fires (delegates to analyze_countability)
    class _FakeSpace:
        tags = {"first_countable"}
        metadata = {}

    result = analyze_infinite_countability(_FakeSpace(), "first_countable")
    assert result is not None


# ---------------------------------------------------------------------------
# analyze_infinite_countability — lines 41-42 (uncountable discrete space)
# ---------------------------------------------------------------------------

def test_analyze_uncountable_discrete_second_countable_returns_false():
    # carrier="R" → uncountable tag → lines 41-42 fire (returns False)
    space = DiscreteInfiniteSpace(carrier="R")
    result = analyze_infinite_countability(space, "second_countable")
    assert result.is_false


def test_analyze_uncountable_discrete_separable_returns_false():
    space = DiscreteInfiniteSpace(carrier="R")
    result = analyze_infinite_countability(space, "separable")
    assert result.is_false


def test_analyze_uncountable_discrete_lindelof_returns_false():
    space = DiscreteInfiniteSpace(carrier="R")
    result = analyze_infinite_countability(space, "lindelof")
    assert result.is_false
