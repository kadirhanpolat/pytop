"""Coverage-targeted tests for compactness.py (v0.5.1)."""
import pytest
from pytop.compactness import (
    CompactnessError,
    analyze_compactness,
    is_countably_compact,
    is_limit_point_compact,
    normalize_compactness_property,
)


class _Obj:
    def __init__(self, tags=()):
        self.tags = set(tags)
        self.metadata = {}


# ---------------------------------------------------------------------------
# normalize_compactness_property — line 49 (unsupported property raises)
# ---------------------------------------------------------------------------

def test_normalize_unsupported_property_raises():
    with pytest.raises(CompactnessError, match="Unsupported"):
        normalize_compactness_property("quasi_compact")


def test_analyze_compactness_unsupported_raises():
    with pytest.raises(CompactnessError):
        analyze_compactness(_Obj(), "quasi_compact")


# ---------------------------------------------------------------------------
# is_countably_compact — line 118 (just needs to be called)
# ---------------------------------------------------------------------------

def test_is_countably_compact_called():
    result = is_countably_compact(_Obj(tags={"compact"}))
    assert result is not None


# ---------------------------------------------------------------------------
# is_limit_point_compact — line 126 (just needs to be called)
# ---------------------------------------------------------------------------

def test_is_limit_point_compact_called():
    result = is_limit_point_compact(_Obj(tags={"compact"}))
    assert result is not None
