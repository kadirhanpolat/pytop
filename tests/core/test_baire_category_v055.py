"""Tests for baire_category.py (v0.5.5)."""

import pytest

from pytop.baire_category import (
    BAIRE_NEGATIVE_TAGS,
    BAIRE_POSITIVE_TAGS,
    COMEAGER_TAGS,
    COMPLETE_METRIC_TAGS,
    LCH_TAGS,
    MEAGER_SPACE_TAGS,
    OPEN_DENSE_TAGS,
    POLISH_TAGS,
    BaireCategoryProfile,
    baire_category_profile,
    baire_category_theorem_check,
    baire_chapter_index,
    baire_layer_summary,
    baire_type_index,
    classify_baire_category,
    get_named_baire_examples,
    is_baire_space,
    is_meager_space,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_baire_positive_contains_complete_metric(self):
        assert "complete_metric" in BAIRE_POSITIVE_TAGS

    def test_baire_positive_contains_polish(self):
        assert "polish_space" in BAIRE_POSITIVE_TAGS

    def test_baire_positive_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in BAIRE_POSITIVE_TAGS

    def test_baire_negative_contains_not_baire(self):
        assert "not_baire" in BAIRE_NEGATIVE_TAGS

    def test_baire_negative_contains_meager_space(self):
        assert "meager_space" in BAIRE_NEGATIVE_TAGS

    def test_complete_metric_tags_contains_polish(self):
        assert "polish" in COMPLETE_METRIC_TAGS

    def test_complete_metric_tags_contains_banach(self):
        assert "banach_space" in COMPLETE_METRIC_TAGS

    def test_lch_tags_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in LCH_TAGS

    def test_meager_space_tags_contains_countable_no_isolated(self):
        assert "countable_no_isolated_points" in MEAGER_SPACE_TAGS

    def test_comeager_tags_contains_residual(self):
        assert "residual" in COMEAGER_TAGS

    def test_open_dense_tags_nonempty(self):
        assert len(OPEN_DENSE_TAGS) >= 1


# ---------------------------------------------------------------------------
# Named examples registry
# ---------------------------------------------------------------------------

class TestNamedBaireExamples:
    def test_returns_tuple(self):
        examples = get_named_baire_examples()
        assert isinstance(examples, tuple)

    def test_at_least_five_examples(self):
        assert len(get_named_baire_examples()) >= 5

    def test_all_are_baire_category_profile(self):
        for p in get_named_baire_examples():
            assert isinstance(p, BaireCategoryProfile)

    def test_real_line_example_exists(self):
        keys = {p.key for p in get_named_baire_examples()}
        assert "real_line_complete_metric" in keys

    def test_rationals_example_exists(self):
        keys = {p.key for p in get_named_baire_examples()}
        assert "rationals_not_baire" in keys

    def test_cantor_set_example_exists(self):
        keys = {p.key for p in get_named_baire_examples()}
        assert "cantor_set" in keys

    def test_baire_space_omega_exists(self):
        keys = {p.key for p in get_named_baire_examples()}
        assert "baire_space_omega_omega" in keys

    def test_rationals_example_is_not_baire(self):
        examples = {p.key: p for p in get_named_baire_examples()}
        assert examples["rationals_not_baire"].is_baire is False

    def test_real_line_example_is_baire(self):
        examples = {p.key: p for p in get_named_baire_examples()}
        assert examples["real_line_complete_metric"].is_baire is True

    def test_cantor_set_is_baire(self):
        examples = {p.key: p for p in get_named_baire_examples()}
        assert examples["cantor_set"].is_baire is True

    def test_all_examples_have_nonempty_keys(self):
        for p in get_named_baire_examples():
            assert p.key.strip()

    def test_all_examples_have_chapter_targets(self):
        for p in get_named_baire_examples():
            assert len(p.chapter_targets) >= 1

    def test_all_examples_have_nonempty_focus(self):
        for p in get_named_baire_examples():
            assert p.focus.strip()

    def test_profile_keys_are_unique(self):
        keys = [p.key for p in get_named_baire_examples()]
        assert len(keys) == len(set(keys))


# ---------------------------------------------------------------------------
# baire_layer_summary
# ---------------------------------------------------------------------------

class TestBaireLayerSummary:
    def test_returns_dict(self):
        assert isinstance(baire_layer_summary(), dict)

    def test_main_text_count_at_least_one(self):
        summary = baire_layer_summary()
        assert summary.get("main_text", 0) >= 1

    def test_selected_block_count_at_least_one(self):
        summary = baire_layer_summary()
        assert summary.get("selected_block", 0) >= 1

    def test_advanced_note_count_at_least_one(self):
        summary = baire_layer_summary()
        assert summary.get("advanced_note", 0) >= 1

    def test_total_matches_example_count(self):
        summary = baire_layer_summary()
        assert sum(summary.values()) == len(get_named_baire_examples())


# ---------------------------------------------------------------------------
# baire_chapter_index
# ---------------------------------------------------------------------------

class TestBaireChapterIndex:
    def test_returns_dict(self):
        assert isinstance(baire_chapter_index(), dict)

    def test_chapter_27_contains_real_line(self):
        index = baire_chapter_index()
        assert "27" in index
        assert "real_line_complete_metric" in index["27"]

    def test_chapter_48_contains_rationals(self):
        index = baire_chapter_index()
        assert "48" in index
        assert "rationals_not_baire" in index["48"]

    def test_values_are_tuples(self):
        for v in baire_chapter_index().values():
            assert isinstance(v, tuple)


# ---------------------------------------------------------------------------
# baire_type_index
# ---------------------------------------------------------------------------

class TestBaireTypeIndex:
    def test_returns_dict(self):
        assert isinstance(baire_type_index(), dict)

    def test_complete_metric_type_exists(self):
        assert "complete_metric" in baire_type_index()

    def test_not_baire_type_exists(self):
        assert "not_baire" in baire_type_index()


# ---------------------------------------------------------------------------
# is_baire_space — negative cases
# ---------------------------------------------------------------------------

class TestIsBaireSpaceNegative:
    def test_not_baire_tag_returns_false(self):
        sp = _sp("not_baire")
        result = is_baire_space(sp)
        assert result.is_false

    def test_meager_space_tag_returns_false(self):
        sp = _sp("meager_space")
        result = is_baire_space(sp)
        assert result.is_false

    def test_countable_t1_no_isolated_returns_false(self):
        sp = _sp("countable", "t1", "no_isolated_points")
        result = is_baire_space(sp)
        assert result.is_false

    def test_rationals_like_combination_returns_false(self):
        sp = _sp("countably_infinite", "hausdorff", "perfect_space")
        result = is_baire_space(sp)
        assert result.is_false

    def test_negative_result_has_theorem_mode(self):
        sp = _sp("not_baire")
        result = is_baire_space(sp)
        assert result.mode == "theorem"

    def test_negative_result_value_is_baire_space(self):
        sp = _sp("not_baire")
        result = is_baire_space(sp)
        assert result.value == "baire_space"


# ---------------------------------------------------------------------------
# is_baire_space — positive cases (complete metric)
# ---------------------------------------------------------------------------

class TestIsBaireSpaceCompleteMetric:
    def test_complete_metric_tag_returns_true(self):
        assert is_baire_space(_sp("complete_metric")).is_true

    def test_completely_metrizable_returns_true(self):
        assert is_baire_space(_sp("completely_metrizable")).is_true

    def test_polish_space_returns_true(self):
        assert is_baire_space(_sp("polish_space")).is_true

    def test_banach_space_returns_true(self):
        assert is_baire_space(_sp("banach_space")).is_true

    def test_hilbert_space_returns_true(self):
        assert is_baire_space(_sp("hilbert_space")).is_true

    def test_polish_criterion_in_metadata(self):
        result = is_baire_space(_sp("polish"))
        assert result.metadata["criterion"] == "complete_metric"

    def test_complete_metric_mode_is_theorem(self):
        result = is_baire_space(_sp("complete_metric"))
        assert result.mode == "theorem"

    def test_complete_metric_justification_mentions_bct(self):
        result = is_baire_space(_sp("complete_metric"))
        assert any("Baire Category Theorem" in j for j in result.justification)


# ---------------------------------------------------------------------------
# is_baire_space — positive cases (locally compact Hausdorff)
# ---------------------------------------------------------------------------

class TestIsBaireSpaceLocallyCompactHausdorff:
    def test_compact_hausdorff_returns_true(self):
        assert is_baire_space(_sp("compact_hausdorff")).is_true

    def test_lch_tag_returns_true(self):
        assert is_baire_space(_sp("locally_compact_hausdorff")).is_true

    def test_compact_t2_returns_true(self):
        assert is_baire_space(_sp("compact_t2")).is_true

    def test_lch_criterion_in_metadata(self):
        result = is_baire_space(_sp("compact_hausdorff"))
        assert result.metadata["criterion"] == "locally_compact_hausdorff"

    def test_lch_justification_mentions_bct(self):
        result = is_baire_space(_sp("locally_compact_hausdorff"))
        assert any("Baire Category Theorem" in j for j in result.justification)


# ---------------------------------------------------------------------------
# is_baire_space — open dense subspace layer
# ---------------------------------------------------------------------------

class TestIsBaireSpaceOpenDense:
    def test_open_dense_subspace_of_baire_is_baire(self):
        sp = _sp("open_dense_subspace", "compact_hausdorff")
        result = is_baire_space(sp)
        assert result.is_true

    def test_open_dense_criterion_in_metadata(self):
        sp = _sp("open_baire_subspace", "baire")
        result = is_baire_space(sp)
        assert result.is_true
        assert result.metadata["criterion"] == "open_subspace_of_baire"


# ---------------------------------------------------------------------------
# is_baire_space — direct tag layer
# ---------------------------------------------------------------------------

class TestIsBaireSpaceDirectTag:
    def test_baire_tag_returns_true(self):
        assert is_baire_space(_sp("baire")).is_true

    def test_baire_space_tag_returns_true(self):
        assert is_baire_space(_sp("baire_space")).is_true

    def test_cantor_set_tag_returns_true(self):
        assert is_baire_space(_sp("cantor_set")).is_true

    def test_direct_tag_criterion_in_metadata(self):
        result = is_baire_space(_sp("baire"))
        assert result.metadata["criterion"] == "direct_tag"


# ---------------------------------------------------------------------------
# is_baire_space — unknown
# ---------------------------------------------------------------------------

class TestIsBaireSpaceUnknown:
    def test_empty_tags_returns_unknown(self):
        result = is_baire_space(_sp())
        assert not result.is_true and not result.is_false

    def test_unknown_mode_is_symbolic(self):
        result = is_baire_space(_sp())
        assert result.mode == "symbolic"

    def test_t1_alone_returns_unknown(self):
        result = is_baire_space(_sp("t1"))
        assert not result.is_true and not result.is_false


# ---------------------------------------------------------------------------
# is_meager_space
# ---------------------------------------------------------------------------

class TestIsMeagerSpace:
    def test_meager_space_tag_returns_true(self):
        assert is_meager_space(_sp("meager_space")).is_true

    def test_countable_no_isolated_points_meager(self):
        sp = _sp("countable", "t1", "no_isolated_points")
        assert is_meager_space(sp).is_true

    def test_rationals_like_is_meager(self):
        sp = _sp("omega", "t2", "perfect_space")
        assert is_meager_space(sp).is_true

    def test_complete_metric_is_not_meager(self):
        result = is_meager_space(_sp("complete_metric"))
        assert result.is_false

    def test_compact_hausdorff_is_not_meager(self):
        result = is_meager_space(_sp("compact_hausdorff"))
        assert result.is_false

    def test_baire_space_is_not_meager(self):
        result = is_meager_space(_sp("baire"))
        assert result.is_false

    def test_unknown_for_untagged(self):
        result = is_meager_space(_sp("t2"))
        assert not result.is_true and not result.is_false

    def test_meager_criterion_in_metadata(self):
        result = is_meager_space(_sp("meager_space"))
        assert result.metadata["criterion"] == "direct_tag"

    def test_baire_contradiction_criterion(self):
        result = is_meager_space(_sp("complete_metric"))
        assert result.metadata["criterion"] == "baire_not_meager"


# ---------------------------------------------------------------------------
# baire_category_theorem_check
# ---------------------------------------------------------------------------

class TestBaireCategoryTheoremCheck:
    def test_complete_metric_bct_applies(self):
        result = baire_category_theorem_check(_sp("complete_metric"))
        assert result.is_true
        assert result.metadata["bct_form"] == "metric"

    def test_lch_bct_applies(self):
        result = baire_category_theorem_check(_sp("locally_compact_hausdorff"))
        assert result.is_true
        assert result.metadata["bct_form"] == "topological"

    def test_polish_bct_form(self):
        result = baire_category_theorem_check(_sp("polish_space"))
        assert result.is_true
        assert result.metadata["bct_form"] == "polish"

    def test_complete_metric_plus_second_countable_gives_polish_form(self):
        result = baire_category_theorem_check(_sp("complete_metric", "second_countable"))
        assert result.is_true
        assert result.metadata["bct_form"] == "polish"

    def test_not_baire_returns_false(self):
        result = baire_category_theorem_check(_sp("not_baire"))
        assert result.is_false
        assert result.metadata["bct_form"] is None

    def test_untagged_returns_unknown(self):
        result = baire_category_theorem_check(_sp("t1", "hausdorff"))
        assert not result.is_true and not result.is_false
        assert result.metadata["bct_form"] is None

    def test_compact_hausdorff_bct_topological_form(self):
        result = baire_category_theorem_check(_sp("compact_hausdorff"))
        assert result.is_true
        assert result.metadata["bct_form"] == "topological"


# ---------------------------------------------------------------------------
# classify_baire_category
# ---------------------------------------------------------------------------

class TestClassifyBaireCategory:
    def test_complete_metric_baire_type(self):
        result = classify_baire_category(_sp("complete_metric"))
        assert result["baire_type"] == "complete_metric"

    def test_lch_baire_type(self):
        result = classify_baire_category(_sp("locally_compact_hausdorff"))
        assert result["baire_type"] == "locally_compact_hausdorff"

    def test_polish_baire_type(self):
        result = classify_baire_category(_sp("polish_space", "second_countable"))
        assert result["baire_type"] == "polish"

    def test_not_baire_type(self):
        result = classify_baire_category(_sp("not_baire"))
        assert result["baire_type"] == "not_baire"

    def test_unknown_baire_type_for_untagged(self):
        result = classify_baire_category(_sp())
        assert result["baire_type"] == "unknown"

    def test_complete_metric_key_properties(self):
        result = classify_baire_category(_sp("complete_metric"))
        assert "baire_space" in result["key_properties"]
        assert "complete_metric" in result["key_properties"]

    def test_lch_key_properties(self):
        result = classify_baire_category(_sp("compact_hausdorff"))
        assert "locally_compact_hausdorff" in result["key_properties"]

    def test_meager_space_in_key_properties(self):
        result = classify_baire_category(_sp("countable", "t1", "no_isolated_points"))
        assert "meager_in_itself" in result["key_properties"]

    def test_result_has_is_baire_key(self):
        result = classify_baire_category(_sp("baire"))
        assert "is_baire" in result
        assert isinstance(result["is_baire"], Result)

    def test_result_has_representation(self):
        result = classify_baire_category(_sp("complete_metric"))
        assert "representation" in result

    def test_result_has_tags(self):
        result = classify_baire_category(_sp("complete_metric"))
        assert "tags" in result
        assert "complete_metric" in result["tags"]

    def test_result_has_bct_applies(self):
        result = classify_baire_category(_sp("complete_metric"))
        assert "bct_applies" in result

    def test_baire_direct_tag_type(self):
        result = classify_baire_category(_sp("baire"))
        assert result["baire_type"] == "baire"


# ---------------------------------------------------------------------------
# baire_category_profile
# ---------------------------------------------------------------------------

class TestBaireCategoryProfile:
    def test_profile_has_classification(self):
        result = baire_category_profile(_sp("complete_metric"))
        assert "classification" in result

    def test_profile_has_named_examples(self):
        result = baire_category_profile(_sp("complete_metric"))
        assert "named_examples" in result
        assert len(result["named_examples"]) >= 5

    def test_profile_has_layer_summary(self):
        result = baire_category_profile(_sp())
        assert "layer_summary" in result

    def test_profile_classification_is_dict(self):
        result = baire_category_profile(_sp("baire"))
        assert isinstance(result["classification"], dict)

    def test_profile_named_examples_are_baire_profiles(self):
        result = baire_category_profile(_sp())
        for p in result["named_examples"]:
            assert isinstance(p, BaireCategoryProfile)


# ---------------------------------------------------------------------------
# Metadata representation paths (for coverage)
# ---------------------------------------------------------------------------

class TestBaireRepresentationPaths:
    def test_symbolic_representation_propagates(self):
        sp = TopologicalSpace.symbolic(
            description="Real line",
            representation="real_line",
            tags={"complete_metric"},
        )
        result = is_baire_space(sp)
        assert result.metadata["representation"] == "real_line"

    def test_lch_representation_propagates(self):
        sp = TopologicalSpace.symbolic(
            description="Closed interval",
            representation="closed_interval",
            tags={"compact_hausdorff"},
        )
        result = is_baire_space(sp)
        assert result.metadata["representation"] == "closed_interval"

    def test_unknown_space_representation_default(self):
        sp = _sp("t1")
        result = is_baire_space(sp)
        assert result.metadata["representation"] == "symbolic_general"


# ---------------------------------------------------------------------------
# Cross-module smoke tests
# ---------------------------------------------------------------------------

class TestBaireCrossModule:
    def test_real_line_profile_matches_complete_metric(self):
        sp = TopologicalSpace.symbolic(
            description="Real line",
            representation="real_line",
            tags={"complete_metric", "second_countable"},
        )
        profile = baire_category_profile(sp)
        cls = profile["classification"]
        assert cls["baire_type"] == "polish"
        assert cls["is_baire"].is_true

    def test_rationals_profile_not_baire(self):
        sp = TopologicalSpace.symbolic(
            description="Rationals",
            representation="rationals",
            tags={"countably_infinite", "hausdorff", "no_isolated_points"},
        )
        profile = baire_category_profile(sp)
        cls = profile["classification"]
        assert cls["baire_type"] == "not_baire"
        assert cls["is_baire"].is_false

    def test_cantor_set_is_baire(self):
        sp = _sp("cantor_set")
        assert is_baire_space(sp).is_true

    def test_baire_omega_omega_is_baire(self):
        sp = _sp("baire_space_omega")
        assert is_baire_space(sp).is_true

    def test_complete_metric_and_meager_contradiction(self):
        sp = _sp("complete_metric")
        baire_r = is_baire_space(sp)
        meager_r = is_meager_space(sp)
        assert baire_r.is_true
        assert meager_r.is_false

    def test_not_baire_and_not_baire_theorem(self):
        sp = _sp("not_baire")
        baire_r = is_baire_space(sp)
        bct_r = baire_category_theorem_check(sp)
        assert baire_r.is_false
        assert bct_r.is_false
