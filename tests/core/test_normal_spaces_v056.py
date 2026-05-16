"""Tests for normal_spaces.py (v0.5.6)."""

import pytest

from pytop.normal_spaces import (
    COMPACT_HAUSDORFF_TAGS,
    METRIZABLE_NORMAL_TAGS,
    NORMAL_NEGATIVE_TAGS,
    NORMAL_POSITIVE_TAGS,
    PARACOMPACT_HAUSDORFF_TAGS,
    PERFECTLY_NORMAL_TAGS,
    TIETZE_CONFIRMING_TAGS,
    URYSOHN_CONFIRMING_TAGS,
    NormalSpaceProfile,
    classify_normality,
    get_named_normal_space_profiles,
    normal_chapter_index,
    normal_layer_summary,
    normal_space_profile,
    normal_type_index,
    tietze_extension_applicable,
    urysohn_function_exists,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_normal_positive_contains_metric(self):
        assert "metric" in NORMAL_POSITIVE_TAGS

    def test_normal_positive_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in NORMAL_POSITIVE_TAGS

    def test_normal_positive_contains_t4(self):
        assert "t4" in NORMAL_POSITIVE_TAGS

    def test_normal_negative_contains_not_normal(self):
        assert "not_normal" in NORMAL_NEGATIVE_TAGS

    def test_normal_negative_contains_sorgenfrey_plane(self):
        assert "sorgenfrey_plane" in NORMAL_NEGATIVE_TAGS

    def test_perfectly_normal_contains_metric(self):
        assert "metric" in PERFECTLY_NORMAL_TAGS

    def test_perfectly_normal_contains_t6(self):
        assert "t6" in PERFECTLY_NORMAL_TAGS

    def test_metrizable_tags_contains_banach(self):
        assert "banach_space" in METRIZABLE_NORMAL_TAGS

    def test_compact_hausdorff_tags_contains_compact_t2(self):
        assert "compact_t2" in COMPACT_HAUSDORFF_TAGS

    def test_paracompact_hausdorff_tags_contains_cw_complex(self):
        assert "cw_complex" in PARACOMPACT_HAUSDORFF_TAGS

    def test_tietze_confirming_tags_contains_t4(self):
        assert "t4" in TIETZE_CONFIRMING_TAGS

    def test_urysohn_confirming_tags_nonempty(self):
        assert len(URYSOHN_CONFIRMING_TAGS) >= 5


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

class TestNamedNormalSpaceProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_normal_space_profiles(), tuple)

    def test_at_least_five_profiles(self):
        assert len(get_named_normal_space_profiles()) >= 5

    def test_all_are_normal_space_profile(self):
        for p in get_named_normal_space_profiles():
            assert isinstance(p, NormalSpaceProfile)

    def test_metrizable_profile_exists(self):
        keys = {p.key for p in get_named_normal_space_profiles()}
        assert "metrizable_space" in keys

    def test_compact_hausdorff_profile_exists(self):
        keys = {p.key for p in get_named_normal_space_profiles()}
        assert "compact_hausdorff_space" in keys

    def test_cw_complex_profile_exists(self):
        keys = {p.key for p in get_named_normal_space_profiles()}
        assert "cw_complex" in keys

    def test_niemytzki_profile_exists(self):
        keys = {p.key for p in get_named_normal_space_profiles()}
        assert "niemytzki_plane" in keys

    def test_sorgenfrey_plane_profile_exists(self):
        keys = {p.key for p in get_named_normal_space_profiles()}
        assert "sorgenfrey_plane" in keys

    def test_metrizable_is_perfectly_normal(self):
        profiles = {p.key: p for p in get_named_normal_space_profiles()}
        assert profiles["metrizable_space"].normality_type == "perfectly_normal"

    def test_compact_hausdorff_is_normal(self):
        profiles = {p.key: p for p in get_named_normal_space_profiles()}
        assert profiles["compact_hausdorff_space"].normality_type == "normal"

    def test_niemytzki_is_normal(self):
        profiles = {p.key: p for p in get_named_normal_space_profiles()}
        assert profiles["niemytzki_plane"].normality_type == "normal"

    def test_sorgenfrey_plane_is_not_normal(self):
        profiles = {p.key: p for p in get_named_normal_space_profiles()}
        assert profiles["sorgenfrey_plane"].normality_type == "not_normal"

    def test_profile_keys_unique(self):
        keys = [p.key for p in get_named_normal_space_profiles()]
        assert len(keys) == len(set(keys))

    def test_all_profiles_have_chapter_targets(self):
        for p in get_named_normal_space_profiles():
            assert len(p.chapter_targets) >= 1

    def test_all_profiles_have_nonempty_focus(self):
        for p in get_named_normal_space_profiles():
            assert p.focus.strip()


# ---------------------------------------------------------------------------
# normal_layer_summary
# ---------------------------------------------------------------------------

class TestNormalLayerSummary:
    def test_returns_dict(self):
        assert isinstance(normal_layer_summary(), dict)

    def test_total_matches_profile_count(self):
        assert sum(normal_layer_summary().values()) == len(get_named_normal_space_profiles())

    def test_main_text_at_least_one(self):
        assert normal_layer_summary().get("main_text", 0) >= 1

    def test_selected_block_at_least_one(self):
        assert normal_layer_summary().get("selected_block", 0) >= 1


# ---------------------------------------------------------------------------
# normal_chapter_index
# ---------------------------------------------------------------------------

class TestNormalChapterIndex:
    def test_returns_dict(self):
        assert isinstance(normal_chapter_index(), dict)

    def test_chapter_32_contains_metrizable(self):
        index = normal_chapter_index()
        assert "32" in index
        assert "metrizable_space" in index["32"]

    def test_chapter_36_contains_niemytzki(self):
        index = normal_chapter_index()
        assert "36" in index
        assert "niemytzki_plane" in index["36"]

    def test_values_are_tuples(self):
        for v in normal_chapter_index().values():
            assert isinstance(v, tuple)


# ---------------------------------------------------------------------------
# normal_type_index
# ---------------------------------------------------------------------------

class TestNormalTypeIndex:
    def test_returns_dict(self):
        assert isinstance(normal_type_index(), dict)

    def test_perfectly_normal_type_exists(self):
        assert "perfectly_normal" in normal_type_index()

    def test_normal_type_exists(self):
        assert "normal" in normal_type_index()

    def test_not_normal_type_exists(self):
        assert "not_normal" in normal_type_index()


# ---------------------------------------------------------------------------
# urysohn_function_exists — negative
# ---------------------------------------------------------------------------

class TestUrysohnNegative:
    def test_not_normal_tag_returns_false(self):
        assert urysohn_function_exists(_sp("not_normal")).is_false

    def test_sorgenfrey_plane_returns_false(self):
        assert urysohn_function_exists(_sp("sorgenfrey_plane")).is_false

    def test_moore_plane_full_returns_false(self):
        assert urysohn_function_exists(_sp("moore_plane_full")).is_false

    def test_false_result_has_theorem_mode(self):
        result = urysohn_function_exists(_sp("not_normal"))
        assert result.mode == "theorem"

    def test_false_result_value(self):
        result = urysohn_function_exists(_sp("not_normal"))
        assert result.value == "urysohn_function_exists"


# ---------------------------------------------------------------------------
# urysohn_function_exists — metrizable
# ---------------------------------------------------------------------------

class TestUrysohnMetrizable:
    def test_metric_tag_returns_true(self):
        assert urysohn_function_exists(_sp("metric")).is_true

    def test_metrizable_tag_returns_true(self):
        assert urysohn_function_exists(_sp("metrizable")).is_true

    def test_polish_space_returns_true(self):
        assert urysohn_function_exists(_sp("polish_space")).is_true

    def test_banach_space_returns_true(self):
        assert urysohn_function_exists(_sp("banach_space")).is_true

    def test_metrizable_criterion_in_metadata(self):
        result = urysohn_function_exists(_sp("metric"))
        assert result.metadata["criterion"] == "metrizable"

    def test_metrizable_justification_mentions_distance(self):
        result = urysohn_function_exists(_sp("metric"))
        assert any("d(x,A)" in j for j in result.justification)


# ---------------------------------------------------------------------------
# urysohn_function_exists — compact Hausdorff
# ---------------------------------------------------------------------------

class TestUrysohnCompactHausdorff:
    def test_compact_hausdorff_returns_true(self):
        assert urysohn_function_exists(_sp("compact_hausdorff")).is_true

    def test_compact_t2_returns_true(self):
        assert urysohn_function_exists(_sp("compact_t2")).is_true

    def test_profinite_returns_true(self):
        assert urysohn_function_exists(_sp("profinite")).is_true

    def test_compact_hausdorff_criterion_in_metadata(self):
        result = urysohn_function_exists(_sp("compact_hausdorff"))
        assert result.metadata["criterion"] == "compact_hausdorff"


# ---------------------------------------------------------------------------
# urysohn_function_exists — paracompact Hausdorff
# ---------------------------------------------------------------------------

class TestUrysohnParacompactHausdorff:
    def test_paracompact_hausdorff_returns_true(self):
        assert urysohn_function_exists(_sp("paracompact_hausdorff")).is_true

    def test_cw_complex_returns_true(self):
        assert urysohn_function_exists(_sp("cw_complex")).is_true

    def test_manifold_returns_true(self):
        assert urysohn_function_exists(_sp("manifold")).is_true

    def test_paracompact_criterion_in_metadata(self):
        result = urysohn_function_exists(_sp("paracompact_hausdorff"))
        assert result.metadata["criterion"] == "paracompact_hausdorff"

    def test_justification_mentions_dieudonne(self):
        result = urysohn_function_exists(_sp("paracompact_hausdorff"))
        assert any("Dieudonné" in j for j in result.justification)


# ---------------------------------------------------------------------------
# urysohn_function_exists — normal tag
# ---------------------------------------------------------------------------

class TestUrysohnNormalTag:
    def test_normal_tag_returns_true(self):
        assert urysohn_function_exists(_sp("normal")).is_true

    def test_t4_tag_returns_true(self):
        assert urysohn_function_exists(_sp("t4")).is_true

    def test_normal_t1_tag_returns_true(self):
        assert urysohn_function_exists(_sp("normal_t1")).is_true

    def test_normal_criterion_in_metadata(self):
        result = urysohn_function_exists(_sp("normal"))
        assert result.metadata["criterion"] == "normal_tag"


# ---------------------------------------------------------------------------
# urysohn_function_exists — unknown
# ---------------------------------------------------------------------------

class TestUrysohnUnknown:
    def test_empty_tags_returns_unknown(self):
        result = urysohn_function_exists(_sp())
        assert not result.is_true and not result.is_false

    def test_t2_alone_returns_unknown(self):
        result = urysohn_function_exists(_sp("hausdorff"))
        assert not result.is_true and not result.is_false

    def test_unknown_mode_is_symbolic(self):
        result = urysohn_function_exists(_sp())
        assert result.mode == "symbolic"


# ---------------------------------------------------------------------------
# tietze_extension_applicable — negative
# ---------------------------------------------------------------------------

class TestTietzeNegative:
    def test_not_normal_tag_returns_false(self):
        assert tietze_extension_applicable(_sp("not_normal")).is_false

    def test_sorgenfrey_plane_returns_false(self):
        assert tietze_extension_applicable(_sp("sorgenfrey_plane")).is_false

    def test_false_result_mode_is_theorem(self):
        result = tietze_extension_applicable(_sp("not_normal"))
        assert result.mode == "theorem"


# ---------------------------------------------------------------------------
# tietze_extension_applicable — metrizable
# ---------------------------------------------------------------------------

class TestTietzeMetrizable:
    def test_metric_tag_returns_true(self):
        assert tietze_extension_applicable(_sp("metric")).is_true

    def test_metrizable_tag_returns_true(self):
        assert tietze_extension_applicable(_sp("metrizable")).is_true

    def test_completely_metrizable_returns_true(self):
        assert tietze_extension_applicable(_sp("completely_metrizable")).is_true

    def test_metrizable_criterion_in_metadata(self):
        result = tietze_extension_applicable(_sp("metric"))
        assert result.metadata["criterion"] == "metrizable"

    def test_justification_mentions_closed_subspace(self):
        result = tietze_extension_applicable(_sp("metric"))
        assert any("closed" in j.lower() for j in result.justification)


# ---------------------------------------------------------------------------
# tietze_extension_applicable — compact Hausdorff
# ---------------------------------------------------------------------------

class TestTietzeCompactHausdorff:
    def test_compact_hausdorff_returns_true(self):
        assert tietze_extension_applicable(_sp("compact_hausdorff")).is_true

    def test_compact_t2_returns_true(self):
        assert tietze_extension_applicable(_sp("compact_t2")).is_true

    def test_compact_hausdorff_criterion(self):
        result = tietze_extension_applicable(_sp("compact_hausdorff"))
        assert result.metadata["criterion"] == "compact_hausdorff"


# ---------------------------------------------------------------------------
# tietze_extension_applicable — paracompact Hausdorff
# ---------------------------------------------------------------------------

class TestTietzeParacompactHausdorff:
    def test_paracompact_hausdorff_returns_true(self):
        assert tietze_extension_applicable(_sp("paracompact_hausdorff")).is_true

    def test_cw_complex_returns_true(self):
        assert tietze_extension_applicable(_sp("cw_complex")).is_true

    def test_paracompact_criterion(self):
        result = tietze_extension_applicable(_sp("paracompact_hausdorff"))
        assert result.metadata["criterion"] == "paracompact_hausdorff"


# ---------------------------------------------------------------------------
# tietze_extension_applicable — T4 tag
# ---------------------------------------------------------------------------

class TestTietzeT4Tag:
    def test_t4_tag_returns_true(self):
        assert tietze_extension_applicable(_sp("t4")).is_true

    def test_normal_t1_tag_returns_true(self):
        assert tietze_extension_applicable(_sp("normal_t1")).is_true

    def test_perfectly_normal_returns_true(self):
        assert tietze_extension_applicable(_sp("perfectly_normal")).is_true

    def test_t4_criterion_in_metadata(self):
        result = tietze_extension_applicable(_sp("t4"))
        assert result.metadata["criterion"] == "t4_tag"


# ---------------------------------------------------------------------------
# tietze_extension_applicable — unknown
# ---------------------------------------------------------------------------

class TestTietzeUnknown:
    def test_empty_tags_returns_unknown(self):
        result = tietze_extension_applicable(_sp())
        assert not result.is_true and not result.is_false

    def test_hausdorff_alone_returns_unknown(self):
        result = tietze_extension_applicable(_sp("hausdorff"))
        assert not result.is_true and not result.is_false


# ---------------------------------------------------------------------------
# classify_normality
# ---------------------------------------------------------------------------

class TestClassifyNormality:
    def test_metrizable_is_perfectly_normal(self):
        result = classify_normality(_sp("metric"))
        assert result["normality_type"] == "perfectly_normal"

    def test_compact_hausdorff_is_normal(self):
        result = classify_normality(_sp("compact_hausdorff"))
        assert result["normality_type"] == "normal"

    def test_not_normal_type(self):
        result = classify_normality(_sp("not_normal"))
        assert result["normality_type"] == "not_normal"

    def test_unknown_type_for_untagged(self):
        result = classify_normality(_sp("hausdorff"))
        assert result["normality_type"] == "unknown"

    def test_metric_key_properties_include_normal(self):
        result = classify_normality(_sp("metric"))
        assert "normal" in result["key_properties"]

    def test_metric_key_properties_include_perfectly_normal(self):
        result = classify_normality(_sp("metric"))
        assert "perfectly_normal" in result["key_properties"]

    def test_metric_key_properties_include_tietze(self):
        result = classify_normality(_sp("metric"))
        assert "tietze_extension" in result["key_properties"]

    def test_compact_hausdorff_in_key_properties(self):
        result = classify_normality(_sp("compact_hausdorff"))
        assert "compact_hausdorff" in result["key_properties"]

    def test_result_has_urysohn_key(self):
        result = classify_normality(_sp("metric"))
        assert "urysohn" in result
        assert isinstance(result["urysohn"], Result)

    def test_result_has_tietze_key(self):
        result = classify_normality(_sp("metric"))
        assert "tietze" in result
        assert isinstance(result["tietze"], Result)

    def test_result_has_representation(self):
        result = classify_normality(_sp("metric"))
        assert "representation" in result

    def test_result_has_tags(self):
        result = classify_normality(_sp("metric"))
        assert "tags" in result
        assert "metric" in result["tags"]

    def test_sorgenfrey_plane_not_normal(self):
        result = classify_normality(_sp("sorgenfrey_plane"))
        assert result["normality_type"] == "not_normal"

    def test_t4_is_normal(self):
        result = classify_normality(_sp("t4"))
        assert result["normality_type"] == "normal"

    def test_paracompact_hausdorff_is_normal(self):
        result = classify_normality(_sp("paracompact_hausdorff"))
        assert result["normality_type"] == "normal"


# ---------------------------------------------------------------------------
# normal_space_profile
# ---------------------------------------------------------------------------

class TestNormalSpaceProfile:
    def test_profile_has_classification(self):
        result = normal_space_profile(_sp("metric"))
        assert "classification" in result

    def test_profile_has_named_profiles(self):
        result = normal_space_profile(_sp("metric"))
        assert "named_profiles" in result
        assert len(result["named_profiles"]) >= 5

    def test_profile_has_layer_summary(self):
        result = normal_space_profile(_sp())
        assert "layer_summary" in result

    def test_named_profiles_are_correct_type(self):
        result = normal_space_profile(_sp())
        for p in result["named_profiles"]:
            assert isinstance(p, NormalSpaceProfile)

    def test_classification_is_dict(self):
        result = normal_space_profile(_sp("compact_hausdorff"))
        assert isinstance(result["classification"], dict)


# ---------------------------------------------------------------------------
# Representation paths (coverage)
# ---------------------------------------------------------------------------

class TestNormalRepresentationPaths:
    def test_symbolic_representation_propagates_urysohn(self):
        sp = TopologicalSpace.symbolic(
            description="Real line",
            representation="real_line",
            tags={"metric"},
        )
        result = urysohn_function_exists(sp)
        assert result.metadata["representation"] == "real_line"

    def test_symbolic_representation_propagates_tietze(self):
        sp = TopologicalSpace.symbolic(
            description="Unit ball",
            representation="closed_ball",
            tags={"compact_hausdorff"},
        )
        result = tietze_extension_applicable(sp)
        assert result.metadata["representation"] == "closed_ball"

    def test_default_representation_for_untagged(self):
        result = urysohn_function_exists(_sp())
        assert result.metadata["representation"] == "symbolic_general"


# ---------------------------------------------------------------------------
# Cross-theorem consistency
# ---------------------------------------------------------------------------

class TestCrossTheoremConsistency:
    def test_metric_urysohn_and_tietze_both_true(self):
        sp = _sp("metric")
        assert urysohn_function_exists(sp).is_true
        assert tietze_extension_applicable(sp).is_true

    def test_compact_hausdorff_both_true(self):
        sp = _sp("compact_hausdorff")
        assert urysohn_function_exists(sp).is_true
        assert tietze_extension_applicable(sp).is_true

    def test_not_normal_urysohn_and_tietze_both_false(self):
        sp = _sp("not_normal")
        assert urysohn_function_exists(sp).is_false
        assert tietze_extension_applicable(sp).is_false

    def test_cw_complex_both_true(self):
        sp = _sp("cw_complex")
        assert urysohn_function_exists(sp).is_true
        assert tietze_extension_applicable(sp).is_true

    def test_t4_urysohn_true(self):
        assert urysohn_function_exists(_sp("t4")).is_true

    def test_perfectly_normal_is_stronger_than_normal(self):
        sp = _sp("perfectly_normal")
        assert urysohn_function_exists(sp).is_true
        cls = classify_normality(sp)
        assert cls["normality_type"] == "perfectly_normal"
