"""Coverage-targeted tests for proximity_spaces.py (v0.5.1)."""
import pytest
from pytop.proximity_spaces import (
    is_proximity_space,
    is_close,
    smirnov_compactification,
    _closeness_map,
)


# ---------------------------------------------------------------------------
# _closeness_map — line 57 (closeness_map in metadata, not top-level)
# ---------------------------------------------------------------------------

def test_closeness_map_from_metadata():
    # closeness_map is in metadata, not directly in the dict → line 57 fires
    space = {
        "metadata": {
            "closeness_map": {("A", "B"): True}
        }
    }
    result = _closeness_map(space)
    assert ("A", "B") in result
    assert result[("A", "B")] is True


# ---------------------------------------------------------------------------
# is_proximity_space — line 76 (is_proximity_space bool in metadata)
# ---------------------------------------------------------------------------

def test_is_proximity_space_from_metadata_bool():
    # top-level dict has no "is_proximity_space" key, but metadata does → line 76
    space = {"metadata": {"is_proximity_space": True}}
    assert is_proximity_space(space) is True


def test_is_proximity_space_from_metadata_false():
    space = {"metadata": {"is_proximity_space": False}}
    assert is_proximity_space(space) is False


# ---------------------------------------------------------------------------
# is_close — line 94 (space_type == "Metric Proximity" → return True)
# ---------------------------------------------------------------------------

def test_is_close_metric_proximity_space_type():
    space = {
        "is_proximity_space": True,
        "space_type": "Metric Proximity",
    }
    # No closeness_map → goes to line 92-94 check
    assert is_close("A", "B", space) is True


# ---------------------------------------------------------------------------
# is_close — line 95 (metric_proximity tag → return True)
# ---------------------------------------------------------------------------

def test_is_close_metric_proximity_tag():
    space = {
        "is_proximity_space": True,
        "tags": ["metric_proximity"],
    }
    assert is_close("A", "B", space) is True


# ---------------------------------------------------------------------------
# is_close — line 96 (no matching condition → return False)
# ---------------------------------------------------------------------------

def test_is_close_no_matching_condition_returns_false():
    # is_proximity_space=True but no closeness_map, not Metric Proximity, no metric_proximity tag
    space = {"is_proximity_space": True}
    assert is_close("A", "B", space) is False
