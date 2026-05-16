"""Coverage-targeted tests for infinite_connectedness.py (v0.5.1)."""
import pytest
from pytop.infinite_connectedness import (
    KNOWN_TRUE,
    KNOWN_FALSE,
    analyze_infinite_connectedness,
    is_connected_infinite,
    is_path_connected_infinite,
    infinite_connectedness_report,
)
from pytop.infinite_spaces import (
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
    CofiniteSpace,
    CocountableSpace,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete():
    return DiscreteInfiniteSpace(carrier="N")


def _indiscrete():
    return IndiscreteInfiniteSpace(carrier="R")


def _cofinite():
    return CofiniteSpace(carrier="R")


def _cocountable():
    return CocountableSpace(carrier="R")


# ---------------------------------------------------------------------------
# KNOWN_TRUE paths — IndiscreteInfiniteSpace, CofiniteSpace, CocountableSpace
# ---------------------------------------------------------------------------

def test_analyze_indiscrete_connected_true():
    r = analyze_infinite_connectedness(_indiscrete(), "connected")
    assert r.is_true
    assert r.mode == "exact"


def test_analyze_indiscrete_path_connected_true():
    r = analyze_infinite_connectedness(_indiscrete(), "path_connected")
    assert r.is_true


def test_analyze_cofinite_connected_true():
    r = analyze_infinite_connectedness(_cofinite(), "connected")
    assert r.is_true


def test_analyze_cocountable_connected_true():
    r = analyze_infinite_connectedness(_cocountable(), "connected")
    assert r.is_true


# ---------------------------------------------------------------------------
# KNOWN_FALSE paths — DiscreteInfiniteSpace  (line 43)
# ---------------------------------------------------------------------------

def test_analyze_discrete_connected_false():
    r = analyze_infinite_connectedness(_discrete(), "connected")
    assert r.is_false
    assert r.mode == "exact"


def test_analyze_discrete_path_connected_false():
    r = analyze_infinite_connectedness(_discrete(), "path_connected")
    assert r.is_false


# ---------------------------------------------------------------------------
# Non-InfiniteTopologicalSpace fallback  (line 31)
# ---------------------------------------------------------------------------

def test_analyze_finite_space_falls_to_connectedness():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1, 2})])
    space = FiniteTopologicalSpace(carrier=carrier, topology=topology)
    r = analyze_infinite_connectedness(space, "connected")
    # FiniteTopologicalSpace is not InfiniteTopologicalSpace → falls to analyze_connectedness
    assert r is not None


def test_analyze_symbolic_falls_to_connectedness():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="test", tags=["connected"])
    r = analyze_infinite_connectedness(space, "connected")
    assert r.is_true


def test_analyze_non_infinite_unknown_property():
    from pytop.spaces import TopologicalSpace
    space = TopologicalSpace.symbolic(description="bare")
    r = analyze_infinite_connectedness(space, "connected")
    # Unknown symbolic space
    assert r is not None


# ---------------------------------------------------------------------------
# infinite_connectedness_report  (line 61)
# ---------------------------------------------------------------------------

def test_infinite_connectedness_report_discrete():
    report = infinite_connectedness_report(_discrete())
    assert "connected" in report
    assert "path_connected" in report
    assert report["connected"].is_false
    assert report["path_connected"].is_false


def test_infinite_connectedness_report_indiscrete():
    report = infinite_connectedness_report(_indiscrete())
    assert report["connected"].is_true
    assert report["path_connected"].is_true


def test_infinite_connectedness_report_cofinite():
    report = infinite_connectedness_report(_cofinite())
    assert report["connected"].is_true


# ---------------------------------------------------------------------------
# is_connected_infinite / is_path_connected_infinite convenience wrappers
# ---------------------------------------------------------------------------

def test_is_connected_infinite_discrete():
    r = is_connected_infinite(_discrete())
    assert r.is_false


def test_is_connected_infinite_indiscrete():
    r = is_connected_infinite(_indiscrete())
    assert r.is_true


def test_is_path_connected_infinite_indiscrete():
    r = is_path_connected_infinite(_indiscrete())
    assert r.is_true


def test_is_path_connected_infinite_discrete():
    r = is_path_connected_infinite(_discrete())
    assert r.is_false


# ---------------------------------------------------------------------------
# Property normalization — spaces with unknown variant properties
# ---------------------------------------------------------------------------

def test_discrete_unknown_property_falls_through():
    # DiscreteInfiniteSpace, "locally_connected" is not in KNOWN_TRUE/KNOWN_FALSE
    r = analyze_infinite_connectedness(_discrete(), "locally_connected")
    assert r is not None  # falls through to analyze_connectedness
