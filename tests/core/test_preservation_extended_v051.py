"""Coverage-targeted tests for preservation.py (v0.5.1)."""
import pytest
from pytop.preservation import (
    analyze_preservation,
    closure_image_behavior,
    _extract_tags,
    _representation_of,
)


class _MapObj:
    """Minimal symbolic map object."""
    def __init__(self, tags=(), metadata=None):
        self.tags = set(tags)
        self.metadata = metadata or {}


# ---------------------------------------------------------------------------
# closure_image_behavior — lines 190-192 (just call it)
# ---------------------------------------------------------------------------

def test_closure_image_behavior_returns_result():
    map_obj = _MapObj(tags={"continuous"})
    result = closure_image_behavior(map_obj, subset=None)
    assert result is not None
    assert "preservation" in result.metadata


# ---------------------------------------------------------------------------
# analyze_preservation — line 207 ("closure_image_behavior" context)
# ---------------------------------------------------------------------------

def test_analyze_preservation_closure_image_behavior():
    map_obj = _MapObj(tags={"continuous"})
    result = analyze_preservation("closure_image_behavior", map_obj)
    assert result is not None


def test_analyze_preservation_closure_preservation_alias():
    map_obj = _MapObj(tags={"continuous"})
    result = analyze_preservation("closure_preservation", map_obj)
    assert result is not None


# ---------------------------------------------------------------------------
# _extract_tags — line 221 (obj is a dict → fires dict branch)
# ---------------------------------------------------------------------------

def test_extract_tags_from_dict():
    tags = _extract_tags({"tags": ["compact", "hausdorff"]})
    assert "compact" in tags
    assert "hausdorff" in tags


def test_extract_tags_dict_empty():
    tags = _extract_tags({})
    assert isinstance(tags, set)


# ---------------------------------------------------------------------------
# _representation_of — line 229 (metadata with "representation" key)
# ---------------------------------------------------------------------------

def test_representation_of_from_metadata():
    obj = _MapObj(metadata={"representation": "finite"})
    assert _representation_of(obj) == "finite"


def test_representation_of_fallback():
    obj = _MapObj()
    assert _representation_of(obj) == "symbolic_general"
