"""Coverage patches for v0.5.7 — 4 previously-uncovered lines."""

import types

from pytop.baire_category import is_baire_space
from pytop.descriptive_set_theory import is_g_delta
from pytop.normal_spaces import urysohn_function_exists
from pytop.topological_vector_spaces import is_locally_convex


# ---------------------------------------------------------------------------
# descriptive_set_theory.py:104 — _extract_tags returns set() for tagless object
# ---------------------------------------------------------------------------

class TestDescriptiveSetTheoryExtractTagsFallback:
    def test_extract_tags_returns_empty_for_int(self):
        # An int has no 'tags' or '_tags' attribute → _extract_tags returns set()
        r = is_g_delta(42)
        assert r.is_unknown
        assert r.metadata["tags"] == []

    def test_extract_tags_returns_empty_for_bare_namespace(self):
        sp = types.SimpleNamespace()  # no tags attr at all
        r = is_g_delta(sp)
        assert r.is_unknown
        assert r.metadata["tags"] == []

    def test_extract_tags_returns_empty_for_string(self):
        r = is_g_delta("open_interval")
        assert r.is_unknown


# ---------------------------------------------------------------------------
# normal_spaces.py:97 — _representation_of attribute path
# ---------------------------------------------------------------------------

class TestNormalSpacesRepresentationAttributePath:
    def test_attribute_path_returns_representation(self):
        sp = types.SimpleNamespace(
            tags={"metric"},
            metadata={},
            representation="euclidean_r3",
        )
        r = urysohn_function_exists(sp)
        assert r.is_true
        assert "euclidean_r3" in r.metadata.get("representation", "")

    def test_attribute_path_lowercases_representation(self):
        sp = types.SimpleNamespace(
            tags={"compact_hausdorff"},
            metadata={},
            representation="CompactHausdorff",
        )
        r = urysohn_function_exists(sp)
        assert r.metadata.get("representation") == "compacthausdorff"


# ---------------------------------------------------------------------------
# baire_category.py:97 — _representation_of attribute path
# ---------------------------------------------------------------------------

class TestBaireCategoryRepresentationAttributePath:
    def test_attribute_path_returns_representation(self):
        sp = types.SimpleNamespace(
            tags={"complete_metric", "polish_space"},
            metadata={},
            representation="cantor_space_2_omega",
        )
        r = is_baire_space(sp)
        assert r.is_true
        assert "cantor_space_2_omega" in r.metadata.get("representation", "")

    def test_attribute_path_used_when_no_metadata_representation(self):
        sp = types.SimpleNamespace(
            tags={"locally_compact_hausdorff"},
            metadata={},
            representation="stone_cech_corona",
        )
        r = is_baire_space(sp)
        assert r.is_true
        assert r.metadata.get("representation") == "stone_cech_corona"


# ---------------------------------------------------------------------------
# topological_vector_spaces.py:121 — _extract_tags returns set() for tagless object
# ---------------------------------------------------------------------------

class TestTVSExtractTagsFallback:
    def test_extract_tags_returns_empty_for_int(self):
        r = is_locally_convex(42)
        assert r.is_unknown
        assert r.metadata["tags"] == []

    def test_extract_tags_returns_empty_for_bare_namespace(self):
        sp = types.SimpleNamespace()
        r = is_locally_convex(sp)
        assert r.is_unknown
