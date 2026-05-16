"""Coverage-targeted tests for inverse_systems.py (v0.5.1)."""
from pytop.inverse_systems import (
    _tags_of,
    _any_space_has,
    compute_limit_properties,
    inverse_limit,
)


class _BadTags:
    tags = "compact"  # string, not list/tuple/set/frozenset


# ---------------------------------------------------------------------------
# _tags_of — line 105 (set input returns lowercase tag strings)
# ---------------------------------------------------------------------------

def test_tags_of_set_input():
    result = _tags_of({"compact", "hausdorff"})
    assert "compact" in result
    assert "hausdorff" in result


# ---------------------------------------------------------------------------
# _tags_of — line 110 (dict with non-collection 'tags' value returns set())
# ---------------------------------------------------------------------------

def test_tags_of_dict_non_list_tags_returns_empty():
    result = _tags_of({"tags": "compact"})
    assert result == set()


# ---------------------------------------------------------------------------
# _tags_of — line 114 (obj.tags is a string → return set())
# ---------------------------------------------------------------------------

def test_tags_of_object_string_tags_returns_empty():
    result = _tags_of(_BadTags())
    assert result == set()


# ---------------------------------------------------------------------------
# _any_space_has — line 122
# ---------------------------------------------------------------------------

def test_any_space_has_returns_true():
    spaces = [{"tags": ["hausdorff"]}, {"tags": ["compact"]}]
    result = _any_space_has(spaces, "compact")
    assert result is True


# ---------------------------------------------------------------------------
# compute_limit_properties — line 185 (non-surjective bonding map else branch)
# ---------------------------------------------------------------------------

def test_compute_limit_properties_non_surjective_compact_hausdorff():
    spaces = [{"tags": ["compact", "hausdorff"]}, {"tags": ["compact", "hausdorff"]}]
    maps = [{"tags": ["continuous"]}]  # no "surjective" tag
    props = compute_limit_properties(spaces, maps)
    assert "compact" in props["tags"]
    assert any("compact Hausdorff" in j for j in props["justifications"])


# ---------------------------------------------------------------------------
# inverse_limit — line 275 (spaces not list/tuple → return None)
# ---------------------------------------------------------------------------

def test_inverse_limit_non_list_spaces_returns_none():
    inv_sys = {"system_type": "inverse_system", "spaces": "XY", "bonding_maps": []}
    result = inverse_limit(inv_sys)
    assert result is None
