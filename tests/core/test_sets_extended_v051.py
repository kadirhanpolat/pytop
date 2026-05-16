"""Coverage-targeted tests for sets.py (v0.5.1)."""
import pytest
from pytop.sets import (
    normalize_universe,
    set_union,
    set_intersection,
)


# ---------------------------------------------------------------------------
# normalize_universe — line 32 (just needs to be called)
# ---------------------------------------------------------------------------

def test_normalize_universe_returns_frozenset():
    result = normalize_universe([1, 2, 3])
    assert result == frozenset({1, 2, 3})


def test_normalize_universe_empty():
    result = normalize_universe([])
    assert result == frozenset()


# ---------------------------------------------------------------------------
# set_union — line 74 (no args → return empty set)
# ---------------------------------------------------------------------------

def test_set_union_no_args_returns_empty():
    result = set_union()
    assert result == set()


# ---------------------------------------------------------------------------
# set_intersection — line 86 (no args → return empty set)
# ---------------------------------------------------------------------------

def test_set_intersection_no_args_returns_empty():
    result = set_intersection()
    assert result == set()
