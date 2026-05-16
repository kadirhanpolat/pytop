"""Coverage-targeted tests for uniform_spaces.py (v0.5.1)."""
from pytop.uniform_spaces import is_uniform_space, entourage_system, uniform_topology_tags


class _BoolAttrSpace:
    is_uniform_space = True
    is_uniformly_complete = True
    tags: set = {"metric"}
    metadata: dict = {}


class _MetaEntourageSpace:
    tags: set = set()
    metadata: dict = {"entourages": ["diagonal", "epsilon_balls"]}


# ---------------------------------------------------------------------------
# _explicit_bool — line 69 (bool attribute on object)
# ---------------------------------------------------------------------------

def test_is_uniform_space_bool_attr_triggers_line69():
    # is_uniform_space=True as bool attr → _explicit_bool line 69 fires
    result = is_uniform_space(_BoolAttrSpace())
    assert result is True


# ---------------------------------------------------------------------------
# _entourage_payload — line 78 (metadata has "entourages" key)
# ---------------------------------------------------------------------------

def test_entourage_system_metadata_entourages_triggers_line78():
    # metadata["entourages"] exists → _entourage_payload line 78 fires
    result = entourage_system(_MetaEntourageSpace())
    assert result is not None


# ---------------------------------------------------------------------------
# uniform_topology_tags — line 406 (uniformly_complete + metric → complete_metric)
# ---------------------------------------------------------------------------

def test_uniform_topology_tags_complete_metric():
    # is_uniform_space=True, is_uniformly_complete=True, "metric" in tags → line 406
    tags = uniform_topology_tags(_BoolAttrSpace())
    assert "complete_metric" in tags
