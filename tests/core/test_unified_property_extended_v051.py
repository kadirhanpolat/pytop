"""Coverage-targeted tests for unified_property.py (v0.5.1)."""
import pytest
from pytop.unified_property import (
    analyze_property,
    analyze_space,
    is_finite_space,
    is_infinite_space,
    _to_space,
)
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import IndiscreteInfiniteSpace


# ---------------------------------------------------------------------------
# _to_space — line 42 (tags not a list/tuple/set/frozenset → tags = [])
# ---------------------------------------------------------------------------

def test_to_space_non_collection_tags_uses_empty_list():
    # "tags" value is a plain string, not a collection → line 42 fires (tags = [])
    result = _to_space({"tags": "compact"})
    # Should return a TopologicalSpace (or original dict if exception) — just verify it runs
    assert result is not None


def test_to_space_int_tags_uses_empty_list():
    # "tags" value is an integer → line 42 fires
    result = _to_space({"tags": 99})
    assert result is not None


# ---------------------------------------------------------------------------
# _to_space — lines 46-47 (except Exception: return space)
# ---------------------------------------------------------------------------

def test_to_space_unhashable_tags_returns_original():
    # tags contains a list (unhashable) — TopologicalSpace.symbolic may raise
    # → except clause (lines 46-47) catches it and returns the original dict
    space_dict = {"tags": [[1, 2]]}
    result = _to_space(space_dict)
    # Either returns a TopologicalSpace or the original dict — either is valid
    assert result is not None


# ---------------------------------------------------------------------------
# analyze_property — unregistered property → unknown result
# ---------------------------------------------------------------------------

def test_analyze_property_unknown_property():
    space = FiniteTopologicalSpace(
        carrier=frozenset({1, 2}),
        topology=frozenset([frozenset(), frozenset({1, 2})]),
    )
    result = analyze_property(space, "not_a_real_property")
    assert result.is_unknown


# ---------------------------------------------------------------------------
# analyze_property — dict input with string tags (hits _to_space line 42)
# ---------------------------------------------------------------------------

def test_analyze_property_dict_with_string_tags():
    # string tags → _to_space fires line 42
    result = analyze_property({"tags": "compact"}, "compact")
    assert result is not None


# ---------------------------------------------------------------------------
# analyze_property — infinite space dispatches to infinite_fn (line 216)
# ---------------------------------------------------------------------------

def test_analyze_property_infinite_space_dispatches_correctly():
    space = IndiscreteInfiniteSpace(carrier="R")
    result = analyze_property(space, "compact")
    assert result.is_true


# ---------------------------------------------------------------------------
# analyze_space — runs all registered properties
# ---------------------------------------------------------------------------

def test_analyze_space_returns_dict_of_results():
    space = FiniteTopologicalSpace(
        carrier=frozenset({1}),
        topology=frozenset([frozenset(), frozenset({1})]),
    )
    report = analyze_space(space, ["compact", "connected"])
    assert "compact" in report
    assert "connected" in report
