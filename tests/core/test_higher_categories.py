"""Tests for pytop.higher_categories."""

from __future__ import annotations

import pytest

from pytop.higher_categories import (
    ADJUNCTION_TAGS,
    ENRICHED_CATEGORY_TAGS,
    INFINITY_TOPOS_TAGS,
    KAN_COMPLEX_TAGS,
    MODEL_CATEGORY_TAGS,
    QUASI_CATEGORY_TAGS,
    SEGAL_SPACE_TAGS,
    STABLE_INFINITY_TAGS,
    HigherCategoryProfile,
    classify_higher_category,
    get_named_higher_category_profiles,
    has_all_limits_and_colimits,
    higher_category_chapter_index,
    higher_category_layer_summary,
    higher_category_profile,
    higher_category_type_index,
    is_infinity_categorical,
    is_presentable_infinity_category,
    is_stable_infinity_category,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

class _Space:
    def __init__(self, tags: set[str], representation: str = "test") -> None:
        self.tags = tags
        self.representation = representation


def _space(*tags: str, rep: str = "test") -> _Space:
    return _Space(set(tags), rep)


# ---------------------------------------------------------------------------
# TestTagConstants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_quasi_category_tags_nonempty(self):
        assert len(QUASI_CATEGORY_TAGS) >= 4

    def test_kan_complex_tags_nonempty(self):
        assert len(KAN_COMPLEX_TAGS) >= 4

    def test_segal_space_tags_nonempty(self):
        assert len(SEGAL_SPACE_TAGS) >= 4

    def test_stable_infinity_tags_nonempty(self):
        assert len(STABLE_INFINITY_TAGS) >= 4

    def test_infinity_topos_tags_nonempty(self):
        assert len(INFINITY_TOPOS_TAGS) >= 4

    def test_adjunction_tags_nonempty(self):
        assert len(ADJUNCTION_TAGS) >= 4

    def test_model_category_tags_nonempty(self):
        assert len(MODEL_CATEGORY_TAGS) >= 4

    def test_enriched_category_tags_nonempty(self):
        assert len(ENRICHED_CATEGORY_TAGS) >= 4

    # quasi_category
    def test_quasi_category_in_quasi_tags(self):
        assert "quasi_category" in QUASI_CATEGORY_TAGS

    def test_inner_horn_filling_in_quasi_tags(self):
        assert "inner_horn_filling" in QUASI_CATEGORY_TAGS

    def test_joyal_model_in_quasi_tags(self):
        assert "joyal_model" in QUASI_CATEGORY_TAGS

    def test_nerve_functor_in_quasi_tags(self):
        assert "nerve_functor" in QUASI_CATEGORY_TAGS

    def test_homotopy_coherent_in_quasi_tags(self):
        assert "homotopy_coherent" in QUASI_CATEGORY_TAGS

    # kan_complex
    def test_kan_complex_in_kan_tags(self):
        assert "kan_complex" in KAN_COMPLEX_TAGS

    def test_infinity_groupoid_in_kan_tags(self):
        assert "infinity_groupoid" in KAN_COMPLEX_TAGS

    def test_grothendieck_homotopy_in_kan_tags(self):
        assert "grothendieck_homotopy" in KAN_COMPLEX_TAGS

    def test_horn_filling_all_in_kan_tags(self):
        assert "horn_filling_all" in KAN_COMPLEX_TAGS

    # segal_space
    def test_complete_segal_space_in_segal_tags(self):
        assert "complete_segal_space" in SEGAL_SPACE_TAGS

    def test_rezk_model_in_segal_tags(self):
        assert "rezk_model" in SEGAL_SPACE_TAGS

    def test_segal_condition_in_segal_tags(self):
        assert "segal_condition" in SEGAL_SPACE_TAGS

    def test_bisimplicial_set_in_segal_tags(self):
        assert "bisimplicial_set" in SEGAL_SPACE_TAGS

    # stable_infinity
    def test_stable_infinity_category_in_stable_tags(self):
        assert "stable_infinity_category" in STABLE_INFINITY_TAGS

    def test_spectra_category_in_stable_tags(self):
        assert "spectra_category" in STABLE_INFINITY_TAGS

    def test_derived_infinity_category_in_stable_tags(self):
        assert "derived_infinity_category" in STABLE_INFINITY_TAGS

    def test_pushout_pullback_stable_in_stable_tags(self):
        assert "pushout_pullback_stable" in STABLE_INFINITY_TAGS

    # infinity_topos
    def test_infinity_topos_in_topos_tags(self):
        assert "infinity_topos" in INFINITY_TOPOS_TAGS

    def test_left_exact_localization_in_topos_tags(self):
        assert "left_exact_localization" in INFINITY_TOPOS_TAGS

    def test_presentable_infinity_in_topos_tags(self):
        assert "presentable_infinity" in INFINITY_TOPOS_TAGS

    def test_lurie_topos_in_topos_tags(self):
        assert "lurie_topos" in INFINITY_TOPOS_TAGS

    # adjunction
    def test_infinity_adjunction_in_adj_tags(self):
        assert "infinity_adjunction" in ADJUNCTION_TAGS

    def test_yoneda_infinity_in_adj_tags(self):
        assert "yoneda_infinity" in ADJUNCTION_TAGS

    def test_adjoint_functor_theorem_in_adj_tags(self):
        assert "adjoint_functor_theorem" in ADJUNCTION_TAGS

    # model_category
    def test_model_category_in_mc_tags(self):
        assert "model_category" in MODEL_CATEGORY_TAGS

    def test_quillen_model_in_mc_tags(self):
        assert "quillen_model" in MODEL_CATEGORY_TAGS

    def test_weak_equivalence_in_mc_tags(self):
        assert "weak_equivalence" in MODEL_CATEGORY_TAGS

    # enriched_category
    def test_enriched_category_in_enriched_tags(self):
        assert "enriched_category" in ENRICHED_CATEGORY_TAGS

    def test_dg_category_in_enriched_tags(self):
        assert "dg_category" in ENRICHED_CATEGORY_TAGS

    def test_bergner_model_in_enriched_tags(self):
        assert "bergner_model" in ENRICHED_CATEGORY_TAGS

    def test_dwyer_kan_in_enriched_tags(self):
        assert "dwyer_kan" in ENRICHED_CATEGORY_TAGS

    def test_all_tag_constants_are_frozensets(self):
        for tagset in [
            QUASI_CATEGORY_TAGS, KAN_COMPLEX_TAGS, SEGAL_SPACE_TAGS,
            STABLE_INFINITY_TAGS, INFINITY_TOPOS_TAGS, ADJUNCTION_TAGS,
            MODEL_CATEGORY_TAGS, ENRICHED_CATEGORY_TAGS,
        ]:
            assert isinstance(tagset, frozenset)

    def test_all_tags_contain_strings_only(self):
        for tagset in [QUASI_CATEGORY_TAGS, KAN_COMPLEX_TAGS, STABLE_INFINITY_TAGS]:
            for tag in tagset:
                assert isinstance(tag, str)

    def test_quasi_and_kan_disjoint(self):
        assert len(QUASI_CATEGORY_TAGS & KAN_COMPLEX_TAGS) == 0

    def test_stable_and_topos_disjoint(self):
        assert len(STABLE_INFINITY_TAGS & INFINITY_TOPOS_TAGS) == 0

    def test_model_and_enriched_disjoint(self):
        assert len(MODEL_CATEGORY_TAGS & ENRICHED_CATEGORY_TAGS) == 0

    def test_quasi_exactly_8_tags(self):
        assert len(QUASI_CATEGORY_TAGS) == 8

    def test_kan_exactly_8_tags(self):
        assert len(KAN_COMPLEX_TAGS) == 8

    def test_segal_exactly_8_tags(self):
        assert len(SEGAL_SPACE_TAGS) == 8

    def test_stable_exactly_8_tags(self):
        assert len(STABLE_INFINITY_TAGS) == 8


# ---------------------------------------------------------------------------
# TestNamedHigherCategoryProfiles
# ---------------------------------------------------------------------------

class TestNamedHigherCategoryProfiles:
    def setup_method(self):
        self.profiles = get_named_higher_category_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_exactly_eight_profiles(self):
        assert len(self.profiles) == 8

    def test_all_are_higher_category_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, HigherCategoryProfile)

    def test_all_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_all_keys_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.key, str) and len(p.key) > 0

    def test_all_display_names_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.display_name, str) and len(p.display_name) > 0

    def test_all_focus_strings_long(self):
        for p in self.profiles:
            assert isinstance(p.focus, str) and len(p.focus) >= 300

    def test_all_chapter_targets_nonempty(self):
        for p in self.profiles:
            assert isinstance(p.chapter_targets, tuple) and len(p.chapter_targets) >= 1

    def test_all_chapter_targets_contain_45_60_72(self):
        for p in self.profiles:
            assert "45" in p.chapter_targets
            assert "60" in p.chapter_targets
            assert "72" in p.chapter_targets

    def test_quasi_category_profile_exists(self):
        assert any(p.key == "quasi_category" for p in self.profiles)

    def test_kan_complex_groupoid_profile_exists(self):
        assert any(p.key == "kan_complex_groupoid" for p in self.profiles)

    def test_complete_segal_space_profile_exists(self):
        assert any(p.key == "complete_segal_space" for p in self.profiles)

    def test_stable_infinity_category_profile_exists(self):
        assert any(p.key == "stable_infinity_category" for p in self.profiles)

    def test_presentable_infinity_category_profile_exists(self):
        assert any(p.key == "presentable_infinity_category" for p in self.profiles)

    def test_infinity_topos_profile_exists(self):
        assert any(p.key == "infinity_topos" for p in self.profiles)

    def test_dg_category_profile_exists(self):
        assert any(p.key == "dg_category" for p in self.profiles)

    def test_model_category_quillen_profile_exists(self):
        assert any(p.key == "model_category_quillen" for p in self.profiles)

    def test_quasi_category_fields(self):
        p = next(x for x in self.profiles if x.key == "quasi_category")
        assert p.category_type == "quasi_category"
        assert p.model_type == "simplicial_set"
        assert p.is_stable is False
        assert p.has_all_limits is True
        assert p.has_all_colimits is True
        assert p.is_presentable is False
        assert p.has_t_structure is False

    def test_kan_complex_groupoid_fields(self):
        p = next(x for x in self.profiles if x.key == "kan_complex_groupoid")
        assert p.category_type == "kan_complex"
        assert p.model_type == "simplicial_set"
        assert p.is_stable is False
        assert p.is_presentable is False

    def test_complete_segal_space_fields(self):
        p = next(x for x in self.profiles if x.key == "complete_segal_space")
        assert p.category_type == "complete_segal_space"
        assert p.model_type == "bisimplicial_set"
        assert p.is_stable is False
        assert p.has_t_structure is False

    def test_stable_infinity_category_fields(self):
        p = next(x for x in self.profiles if x.key == "stable_infinity_category")
        assert p.category_type == "stable_infinity"
        assert p.is_stable is True
        assert p.has_t_structure is True
        assert p.model_type == "general"

    def test_presentable_infinity_category_fields(self):
        p = next(x for x in self.profiles if x.key == "presentable_infinity_category")
        assert p.is_presentable is True
        assert p.has_all_limits is True
        assert p.has_all_colimits is True
        assert p.is_stable is False

    def test_infinity_topos_fields(self):
        p = next(x for x in self.profiles if x.key == "infinity_topos")
        assert p.category_type == "infinity_topos"
        assert p.is_presentable is True
        assert p.has_all_limits is True
        assert p.has_all_colimits is True
        assert p.is_stable is False

    def test_dg_category_fields(self):
        p = next(x for x in self.profiles if x.key == "dg_category")
        assert p.category_type == "enriched_category"
        assert p.model_type == "enriched"
        assert p.is_stable is True
        assert p.has_t_structure is True
        assert p.has_all_limits is False
        assert p.has_all_colimits is False

    def test_model_category_quillen_fields(self):
        p = next(x for x in self.profiles if x.key == "model_category_quillen")
        assert p.category_type == "enriched_category"
        assert p.model_type == "general"
        assert p.has_all_limits is True
        assert p.has_all_colimits is True
        assert p.is_stable is False
        assert p.has_t_structure is False

    def test_profiles_are_frozen(self):
        p = self.profiles[0]
        with pytest.raises((AttributeError, TypeError)):
            p.key = "modified"  # type: ignore[misc]

    def test_category_types_valid(self):
        valid = {"quasi_category", "kan_complex", "segal_space", "complete_segal_space",
                 "simplicial_category", "stable_infinity", "infinity_topos", "enriched_category"}
        for p in self.profiles:
            assert p.category_type in valid

    def test_model_types_valid(self):
        valid = {"simplicial_set", "bisimplicial_set", "enriched", "general"}
        for p in self.profiles:
            assert p.model_type in valid


# ---------------------------------------------------------------------------
# TestSummaryFunctions
# ---------------------------------------------------------------------------

class TestSummaryFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(higher_category_layer_summary(), dict)

    def test_layer_summary_positive_counts(self):
        for v in higher_category_layer_summary().values():
            assert v > 0

    def test_layer_summary_total_matches_profiles(self):
        assert sum(higher_category_layer_summary().values()) == len(
            get_named_higher_category_profiles()
        )

    def test_chapter_index_returns_dict(self):
        assert isinstance(higher_category_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in higher_category_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_keys_sorted(self):
        keys = list(higher_category_chapter_index().keys())
        assert keys == sorted(keys)

    def test_chapter_index_contains_chapter_45(self):
        assert "45" in higher_category_chapter_index()

    def test_chapter_index_contains_chapter_60(self):
        assert "60" in higher_category_chapter_index()

    def test_chapter_index_contains_chapter_72(self):
        assert "72" in higher_category_chapter_index()

    def test_type_index_returns_dict(self):
        assert isinstance(higher_category_type_index(), dict)

    def test_type_index_values_are_tuples(self):
        for v in higher_category_type_index().values():
            assert isinstance(v, tuple)

    def test_type_index_keys_sorted(self):
        keys = list(higher_category_type_index().keys())
        assert keys == sorted(keys)

    def test_type_index_contains_quasi_category(self):
        assert "quasi_category" in higher_category_type_index()

    def test_type_index_contains_stable_infinity(self):
        assert "stable_infinity" in higher_category_type_index()

    def test_type_index_total_matches_profiles(self):
        assert sum(len(v) for v in higher_category_type_index().values()) == len(
            get_named_higher_category_profiles()
        )


# ---------------------------------------------------------------------------
# TestIsInfinityCategorical
# ---------------------------------------------------------------------------

class TestIsInfinityCategorical:
    # Layer 1 — quasi_category tags
    def test_quasi_category_tag(self):
        s = _space("quasi_category")
        assert is_infinity_categorical(s).is_true

    def test_inner_horn_filling_tag(self):
        s = _space("inner_horn_filling")
        assert is_infinity_categorical(s).is_true

    def test_joyal_model_tag(self):
        s = _space("joyal_model")
        assert is_infinity_categorical(s).is_true

    def test_nerve_functor_tag(self):
        s = _space("nerve_functor")
        assert is_infinity_categorical(s).is_true

    # Layer 1 — kan_complex tags
    def test_kan_complex_tag(self):
        s = _space("kan_complex")
        assert is_infinity_categorical(s).is_true

    def test_infinity_groupoid_tag(self):
        s = _space("infinity_groupoid")
        assert is_infinity_categorical(s).is_true

    def test_grothendieck_homotopy_tag(self):
        s = _space("grothendieck_homotopy")
        assert is_infinity_categorical(s).is_true

    def test_horn_filling_all_tag(self):
        s = _space("horn_filling_all")
        assert is_infinity_categorical(s).is_true

    # Layer 2 — segal_space tags
    def test_complete_segal_space_tag(self):
        s = _space("complete_segal_space")
        assert is_infinity_categorical(s).is_true

    def test_rezk_model_tag(self):
        s = _space("rezk_model")
        assert is_infinity_categorical(s).is_true

    # Layer 2 — stable_infinity tags
    def test_stable_infinity_category_tag(self):
        s = _space("stable_infinity_category")
        assert is_infinity_categorical(s).is_true

    def test_spectra_category_tag(self):
        s = _space("spectra_category")
        assert is_infinity_categorical(s).is_true

    # Layer 2 — infinity_topos tags
    def test_infinity_topos_tag(self):
        s = _space("infinity_topos")
        assert is_infinity_categorical(s).is_true

    def test_lurie_topos_tag(self):
        s = _space("lurie_topos")
        assert is_infinity_categorical(s).is_true

    # Layer 3 — model_category / enriched
    def test_model_category_tag(self):
        s = _space("model_category")
        assert is_infinity_categorical(s).is_true

    def test_dg_category_tag(self):
        s = _space("dg_category")
        assert is_infinity_categorical(s).is_true

    def test_bergner_model_tag(self):
        s = _space("bergner_model")
        assert is_infinity_categorical(s).is_true

    def test_dwyer_kan_tag(self):
        s = _space("dwyer_kan")
        assert is_infinity_categorical(s).is_true

    # Layer 4 — strict categories
    def test_strict_1_category_false(self):
        s = _space("strict_1_category")
        assert is_infinity_categorical(s).is_false

    def test_ordinary_category_false(self):
        s = _space("ordinary_category")
        assert is_infinity_categorical(s).is_false

    def test_set_category_false(self):
        s = _space("set_category")
        assert is_infinity_categorical(s).is_false

    # Layer 5 — unknown
    def test_empty_tags_unknown(self):
        s = _space()
        r = is_infinity_categorical(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("compact_manifold")
        r = is_infinity_categorical(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("quasi_category")
        r = is_infinity_categorical(s)
        assert len(r.justification) >= 1

    def test_result_metadata_has_criterion(self):
        s = _space("kan_complex")
        r = is_infinity_categorical(s)
        assert "criterion" in r.metadata

    def test_homotopy_coherent_tag(self):
        s = _space("homotopy_coherent")
        assert is_infinity_categorical(s).is_true

    def test_simplicial_localization_tag(self):
        s = _space("simplicial_localization")
        assert is_infinity_categorical(s).is_true


# ---------------------------------------------------------------------------
# TestIsStableInfinityCategory
# ---------------------------------------------------------------------------

class TestIsStableInfinityCategory:
    # Layer 1 — STABLE_INFINITY_TAGS
    def test_stable_infinity_category_tag(self):
        s = _space("stable_infinity_category")
        assert is_stable_infinity_category(s).is_true

    def test_stable_category_tag(self):
        s = _space("stable_category")
        assert is_stable_infinity_category(s).is_true

    def test_spectra_category_tag(self):
        s = _space("spectra_category")
        assert is_stable_infinity_category(s).is_true

    def test_triangulated_infinity_tag(self):
        s = _space("triangulated_infinity")
        assert is_stable_infinity_category(s).is_true

    def test_zero_object_infinity_tag(self):
        s = _space("zero_object_infinity")
        assert is_stable_infinity_category(s).is_true

    def test_pushout_pullback_stable_tag(self):
        s = _space("pushout_pullback_stable")
        assert is_stable_infinity_category(s).is_true

    def test_exact_triangle_infinity_tag(self):
        s = _space("exact_triangle_infinity")
        assert is_stable_infinity_category(s).is_true

    def test_derived_infinity_category_tag(self):
        s = _space("derived_infinity_category")
        assert is_stable_infinity_category(s).is_true

    # Layer 2 — explicit stable
    def test_dg_category_tag_stable(self):
        s = _space("dg_category")
        assert is_stable_infinity_category(s).is_true

    def test_stable_category_explicit(self):
        s = _space("stable_category")
        assert is_stable_infinity_category(s).is_true

    # Layer 3 — not stable
    def test_infinity_topos_not_stable(self):
        s = _space("infinity_topos")
        assert is_stable_infinity_category(s).is_false

    def test_segal_space_not_stable(self):
        s = _space("segal_space")
        assert is_stable_infinity_category(s).is_false

    def test_kan_complex_not_stable(self):
        s = _space("kan_complex")
        assert is_stable_infinity_category(s).is_false

    # Layer 4 — unknown
    def test_empty_tags_unknown(self):
        s = _space()
        r = is_stable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("smooth_manifold")
        r = is_stable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("stable_infinity_category")
        r = is_stable_infinity_category(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("spectra_category")
        r = is_stable_infinity_category(s)
        assert "criterion" in r.metadata

    def test_quasi_category_unknown_stability(self):
        s = _space("quasi_category")
        r = is_stable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_joyal_model_unknown_stability(self):
        s = _space("joyal_model")
        r = is_stable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_complete_segal_space_not_stable(self):
        s = _space("segal_space", "complete_segal_space")
        assert is_stable_infinity_category(s).is_false


# ---------------------------------------------------------------------------
# TestHasAllLimitsAndColimits
# ---------------------------------------------------------------------------

class TestHasAllLimitsAndColimits:
    # Layer 1 — INFINITY_TOPOS_TAGS
    def test_infinity_topos_tag(self):
        s = _space("infinity_topos")
        assert has_all_limits_and_colimits(s).is_true

    def test_left_exact_localization_tag(self):
        s = _space("left_exact_localization")
        assert has_all_limits_and_colimits(s).is_true

    def test_higher_topos_tag(self):
        s = _space("higher_topos")
        assert has_all_limits_and_colimits(s).is_true

    def test_infinity_sheaf_topos_tag(self):
        s = _space("infinity_sheaf_topos")
        assert has_all_limits_and_colimits(s).is_true

    # Layer 1 — ADJUNCTION_TAGS
    def test_infinity_adjunction_tag(self):
        s = _space("infinity_adjunction")
        assert has_all_limits_and_colimits(s).is_true

    def test_yoneda_infinity_tag(self):
        s = _space("yoneda_infinity")
        assert has_all_limits_and_colimits(s).is_true

    def test_adjoint_functor_theorem_tag(self):
        s = _space("adjoint_functor_theorem")
        assert has_all_limits_and_colimits(s).is_true

    def test_infinity_limit_colimit_tag(self):
        s = _space("infinity_limit_colimit")
        assert has_all_limits_and_colimits(s).is_true

    # Layer 2 — presentable / quasi_category
    def test_presentable_infinity_tag(self):
        s = _space("presentable_infinity")
        assert has_all_limits_and_colimits(s).is_true

    def test_accessible_infinity_tag(self):
        s = _space("accessible_infinity")
        assert has_all_limits_and_colimits(s).is_true

    def test_quasi_category_tag(self):
        s = _space("quasi_category")
        assert has_all_limits_and_colimits(s).is_true

    # Layer 3 — dg / incomplete
    def test_dg_category_no_all_limits(self):
        s = _space("dg_category")
        assert has_all_limits_and_colimits(s).is_false

    def test_not_complete_tag(self):
        s = _space("not_complete")
        assert has_all_limits_and_colimits(s).is_false

    def test_no_limits_tag(self):
        s = _space("no_limits")
        assert has_all_limits_and_colimits(s).is_false

    # Layer 4 — unknown
    def test_empty_tags_unknown(self):
        s = _space()
        r = has_all_limits_and_colimits(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("borsuk_ulam")
        r = has_all_limits_and_colimits(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("infinity_topos")
        r = has_all_limits_and_colimits(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("adjoint_functor_theorem")
        r = has_all_limits_and_colimits(s)
        assert "criterion" in r.metadata

    def test_lurie_topos_has_limits(self):
        s = _space("lurie_topos")
        assert has_all_limits_and_colimits(s).is_true

    def test_infinity_giraud_has_limits(self):
        s = _space("infinity_giraud")
        assert has_all_limits_and_colimits(s).is_true


# ---------------------------------------------------------------------------
# TestIsPresentableInfinityCategory
# ---------------------------------------------------------------------------

class TestIsPresentableInfinityCategory:
    # Layer 1 — INFINITY_TOPOS_TAGS
    def test_infinity_topos_is_presentable(self):
        s = _space("infinity_topos")
        assert is_presentable_infinity_category(s).is_true

    def test_lurie_topos_is_presentable(self):
        s = _space("lurie_topos")
        assert is_presentable_infinity_category(s).is_true

    def test_infinity_giraud_is_presentable(self):
        s = _space("infinity_giraud")
        assert is_presentable_infinity_category(s).is_true

    def test_higher_topos_is_presentable(self):
        s = _space("higher_topos")
        assert is_presentable_infinity_category(s).is_true

    def test_left_exact_localization_is_presentable(self):
        s = _space("left_exact_localization")
        assert is_presentable_infinity_category(s).is_true

    # Layer 2 — explicit presentable / adjunction
    def test_presentable_infinity_tag(self):
        s = _space("presentable_infinity")
        assert is_presentable_infinity_category(s).is_true

    def test_accessible_infinity_tag(self):
        s = _space("accessible_infinity")
        assert is_presentable_infinity_category(s).is_true

    def test_infinity_adjunction_tag(self):
        s = _space("infinity_adjunction")
        assert is_presentable_infinity_category(s).is_true

    def test_adjoint_functor_theorem_tag(self):
        s = _space("adjoint_functor_theorem")
        assert is_presentable_infinity_category(s).is_true

    def test_yoneda_infinity_tag(self):
        s = _space("yoneda_infinity")
        assert is_presentable_infinity_category(s).is_true

    # Layer 3 — not presentable
    def test_dg_category_not_presentable(self):
        s = _space("dg_category")
        assert is_presentable_infinity_category(s).is_false

    def test_not_presentable_tag(self):
        s = _space("not_presentable")
        assert is_presentable_infinity_category(s).is_false

    def test_small_category_not_presentable(self):
        s = _space("small_category")
        assert is_presentable_infinity_category(s).is_false

    # Layer 4 — unknown
    def test_empty_tags_unknown(self):
        s = _space()
        r = is_presentable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_unrelated_tag_unknown(self):
        s = _space("knot_invariant")
        r = is_presentable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_stable_infinity_unknown_presentable(self):
        s = _space("stable_infinity_category")
        r = is_presentable_infinity_category(s)
        assert not r.is_true and not r.is_false

    def test_result_has_justification(self):
        s = _space("infinity_topos")
        r = is_presentable_infinity_category(s)
        assert len(r.justification) >= 1

    def test_result_metadata_criterion(self):
        s = _space("presentable_infinity")
        r = is_presentable_infinity_category(s)
        assert "criterion" in r.metadata

    def test_infinity_sheaf_topos_is_presentable(self):
        s = _space("infinity_sheaf_topos")
        assert is_presentable_infinity_category(s).is_true

    def test_unit_counit_infinity_is_presentable(self):
        s = _space("unit_counit_infinity")
        assert is_presentable_infinity_category(s).is_true


# ---------------------------------------------------------------------------
# TestClassifyHigherCategory
# ---------------------------------------------------------------------------

class TestClassifyHigherCategory:
    def test_returns_dict(self):
        assert isinstance(classify_higher_category(_space()), dict)

    def test_has_four_keys(self):
        assert len(classify_higher_category(_space())) == 4

    def test_has_is_infinity_categorical_key(self):
        assert "is_infinity_categorical" in classify_higher_category(_space())

    def test_has_is_stable_infinity_category_key(self):
        assert "is_stable_infinity_category" in classify_higher_category(_space())

    def test_has_limits_colimits_key(self):
        assert "has_all_limits_and_colimits" in classify_higher_category(_space())

    def test_has_presentable_key(self):
        assert "is_presentable_infinity_category" in classify_higher_category(_space())

    def test_quasi_category_full_classification(self):
        s = _space("quasi_category", "presentable_infinity")
        r = classify_higher_category(s)
        assert r["is_infinity_categorical"].is_true
        assert r["has_all_limits_and_colimits"].is_true

    def test_stable_infinity_category_classification(self):
        s = _space("stable_infinity_category")
        r = classify_higher_category(s)
        assert r["is_infinity_categorical"].is_true
        assert r["is_stable_infinity_category"].is_true

    def test_infinity_topos_full_classification(self):
        s = _space("infinity_topos")
        r = classify_higher_category(s)
        assert r["is_infinity_categorical"].is_true
        assert r["has_all_limits_and_colimits"].is_true
        assert r["is_presentable_infinity_category"].is_true

    def test_strict_1_category_false_infinity(self):
        s = _space("strict_1_category")
        r = classify_higher_category(s)
        assert r["is_infinity_categorical"].is_false

    def test_empty_space_all_unknown(self):
        s = _space()
        for r in classify_higher_category(s).values():
            assert not r.is_true and not r.is_false

    def test_kan_complex_not_stable(self):
        s = _space("kan_complex")
        r = classify_higher_category(s)
        assert r["is_infinity_categorical"].is_true
        assert r["is_stable_infinity_category"].is_false


# ---------------------------------------------------------------------------
# TestHigherCategoryProfile
# ---------------------------------------------------------------------------

class TestHigherCategoryProfile:
    def test_returns_dict(self):
        assert isinstance(higher_category_profile(_space()), dict)

    def test_has_space_key(self):
        assert "space" in higher_category_profile(_space())

    def test_has_tags_key(self):
        assert "tags" in higher_category_profile(_space("quasi_category"))

    def test_has_representation_key(self):
        assert "representation" in higher_category_profile(_space())

    def test_has_classification_key(self):
        assert "classification" in higher_category_profile(_space())

    def test_has_summary_key(self):
        assert "summary" in higher_category_profile(_space())

    def test_tags_is_sorted_list(self):
        s = _space("quasi_category", "infinity_topos")
        result = higher_category_profile(s)
        tags = result["tags"]
        assert isinstance(tags, list) and tags == sorted(tags)

    def test_summary_has_four_entries(self):
        assert len(higher_category_profile(_space())["summary"]) == 4

    def test_summary_values_are_strings(self):
        s = _space("quasi_category")
        for v in higher_category_profile(s)["summary"].values():
            assert isinstance(v, str)

    def test_space_attribute_preserved(self):
        s = _space("infinity_topos")
        result = higher_category_profile(s)
        assert result["space"] is s
