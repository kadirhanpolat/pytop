"""Tests for locale_theory.py (v0.5.15)."""

import pytest

from pytop.locale_theory import (
    COMPACT_LOCALE_TAGS,
    COMPLETELY_REGULAR_LOCALE_TAGS,
    LOCALIC_GROUP_TAGS,
    NON_SPATIAL_LOCALE_TAGS,
    NOT_REGULAR_LOCALE_TAGS,
    REGULAR_LOCALE_TAGS,
    SPATIAL_LOCALE_TAGS,
    ZERO_DIMENSIONAL_LOCALE_TAGS,
    LocaleProfile,
    classify_locale,
    get_named_locale_profiles,
    is_compact_locale,
    is_localic_group,
    is_regular_locale,
    is_spatial_locale,
    is_stone_locale,
    locale_chapter_index,
    locale_layer_summary,
    locale_profile,
    locale_type_index,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_spatial_contains_sober(self):
        assert "sober" in SPATIAL_LOCALE_TAGS

    def test_spatial_contains_hausdorff(self):
        assert "hausdorff" in SPATIAL_LOCALE_TAGS

    def test_spatial_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in SPATIAL_LOCALE_TAGS

    def test_spatial_contains_metrizable(self):
        assert "metrizable" in SPATIAL_LOCALE_TAGS

    def test_spatial_contains_stone_space(self):
        assert "stone_space" in SPATIAL_LOCALE_TAGS

    def test_spatial_contains_profinite(self):
        assert "profinite" in SPATIAL_LOCALE_TAGS

    def test_spatial_contains_localic_group(self):
        assert "localic_group" in SPATIAL_LOCALE_TAGS

    def test_compact_contains_compact(self):
        assert "compact" in COMPACT_LOCALE_TAGS

    def test_compact_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in COMPACT_LOCALE_TAGS

    def test_compact_contains_stone_locale(self):
        assert "stone_locale" in COMPACT_LOCALE_TAGS

    def test_compact_contains_profinite(self):
        assert "profinite" in COMPACT_LOCALE_TAGS

    def test_regular_contains_regular_locale(self):
        assert "regular_locale" in REGULAR_LOCALE_TAGS

    def test_regular_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in REGULAR_LOCALE_TAGS

    def test_regular_contains_stone_locale(self):
        assert "stone_locale" in REGULAR_LOCALE_TAGS

    def test_regular_contains_metrizable(self):
        assert "metrizable" in REGULAR_LOCALE_TAGS

    def test_completely_regular_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in COMPLETELY_REGULAR_LOCALE_TAGS

    def test_completely_regular_contains_stone_locale(self):
        assert "stone_locale" in COMPLETELY_REGULAR_LOCALE_TAGS

    def test_zero_dim_contains_stone_locale(self):
        assert "stone_locale" in ZERO_DIMENSIONAL_LOCALE_TAGS

    def test_zero_dim_contains_boolean_locale(self):
        assert "boolean_locale" in ZERO_DIMENSIONAL_LOCALE_TAGS

    def test_zero_dim_contains_profinite(self):
        assert "profinite" in ZERO_DIMENSIONAL_LOCALE_TAGS

    def test_non_spatial_contains_non_spatial_locale(self):
        assert "non_spatial_locale" in NON_SPATIAL_LOCALE_TAGS

    def test_non_spatial_contains_measure_algebra(self):
        assert "measure_algebra_locale" in NON_SPATIAL_LOCALE_TAGS

    def test_non_spatial_contains_no_classical_points(self):
        assert "no_classical_points" in NON_SPATIAL_LOCALE_TAGS

    def test_localic_group_contains_localic_group(self):
        assert "localic_group" in LOCALIC_GROUP_TAGS

    def test_localic_group_contains_group_object_in_loc(self):
        assert "group_object_in_loc" in LOCALIC_GROUP_TAGS

    def test_not_regular_contains_t0_not_t1(self):
        assert "t0_not_t1" in NOT_REGULAR_LOCALE_TAGS

    def test_not_regular_contains_sierpinski_locale(self):
        assert "sierpinski_locale" in NOT_REGULAR_LOCALE_TAGS

    def test_all_tag_constants_are_sets(self):
        for s in [SPATIAL_LOCALE_TAGS, COMPACT_LOCALE_TAGS, REGULAR_LOCALE_TAGS,
                  COMPLETELY_REGULAR_LOCALE_TAGS, ZERO_DIMENSIONAL_LOCALE_TAGS,
                  NON_SPATIAL_LOCALE_TAGS, LOCALIC_GROUP_TAGS, NOT_REGULAR_LOCALE_TAGS]:
            assert isinstance(s, frozenset)

    def test_non_spatial_and_spatial_no_common_key_tag(self):
        # measure_algebra_locale is in NON_SPATIAL but not in SPATIAL
        assert "measure_algebra_locale" not in SPATIAL_LOCALE_TAGS


# ---------------------------------------------------------------------------
# LocaleProfile dataclass
# ---------------------------------------------------------------------------

class TestLocaleProfileDataclass:
    def test_profile_is_frozen(self):
        p = LocaleProfile(
            key="t", display_name="T", locale_type="spatial_locale",
            is_spatial=True, is_compact=True, is_regular=True,
            is_completely_regular=True, is_zero_dimensional=False,
            is_localic_group=False,
            presentation_layer="main_text", focus="test",
            chapter_targets=("10",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = LocaleProfile(
            key="k", display_name="K", locale_type="stone_locale",
            is_spatial=True, is_compact=True, is_regular=True,
            is_completely_regular=True, is_zero_dimensional=True,
            is_localic_group=False,
            presentation_layer="main_text", focus="stone",
            chapter_targets=("10", "28"),
        )
        assert p.key == "k"
        assert p.locale_type == "stone_locale"
        assert p.is_zero_dimensional is True
        assert p.is_localic_group is False
        assert p.chapter_targets == ("10", "28")

    def test_profile_equality(self):
        kwargs = dict(
            key="a", display_name="A", locale_type="spatial_locale",
            is_spatial=True, is_compact=False, is_regular=True,
            is_completely_regular=True, is_zero_dimensional=False,
            is_localic_group=True,
            presentation_layer="main_text", focus="f",
            chapter_targets=("10",),
        )
        assert LocaleProfile(**kwargs) == LocaleProfile(**kwargs)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedLocaleProfiles:
    def setup_method(self):
        self.profiles = get_named_locale_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(self.profiles) >= 5

    def test_all_are_locale_profiles(self):
        for p in self.profiles:
            assert isinstance(p, LocaleProfile)

    def test_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_localic_real_line_exists(self):
        assert "localic_real_line" in {p.key for p in self.profiles}

    def test_random_real_locale_exists(self):
        assert "random_real_locale" in {p.key for p in self.profiles}

    def test_stone_locale_profinite_exists(self):
        assert "stone_locale_profinite" in {p.key for p in self.profiles}

    def test_unit_interval_locale_exists(self):
        assert "unit_interval_locale" in {p.key for p in self.profiles}

    def test_sierpinski_locale_exists(self):
        assert "sierpinski_locale" in {p.key for p in self.profiles}

    def test_localic_torus_exists(self):
        assert "localic_torus" in {p.key for p in self.profiles}

    def test_localic_real_line_is_spatial(self):
        p = next(x for x in self.profiles if x.key == "localic_real_line")
        assert p.is_spatial is True

    def test_localic_real_line_not_compact(self):
        p = next(x for x in self.profiles if x.key == "localic_real_line")
        assert p.is_compact is False

    def test_localic_real_line_is_regular(self):
        p = next(x for x in self.profiles if x.key == "localic_real_line")
        assert p.is_regular is True

    def test_localic_real_line_is_localic_group(self):
        p = next(x for x in self.profiles if x.key == "localic_real_line")
        assert p.is_localic_group is True

    def test_localic_real_line_not_zero_dimensional(self):
        p = next(x for x in self.profiles if x.key == "localic_real_line")
        assert p.is_zero_dimensional is False

    def test_random_real_not_spatial(self):
        p = next(x for x in self.profiles if x.key == "random_real_locale")
        assert p.is_spatial is False

    def test_random_real_is_compact(self):
        p = next(x for x in self.profiles if x.key == "random_real_locale")
        assert p.is_compact is True

    def test_random_real_is_regular(self):
        p = next(x for x in self.profiles if x.key == "random_real_locale")
        assert p.is_regular is True

    def test_random_real_is_zero_dimensional(self):
        p = next(x for x in self.profiles if x.key == "random_real_locale")
        assert p.is_zero_dimensional is True

    def test_random_real_not_localic_group(self):
        p = next(x for x in self.profiles if x.key == "random_real_locale")
        assert p.is_localic_group is False

    def test_stone_profinite_is_spatial(self):
        p = next(x for x in self.profiles if x.key == "stone_locale_profinite")
        assert p.is_spatial is True

    def test_stone_profinite_is_compact(self):
        p = next(x for x in self.profiles if x.key == "stone_locale_profinite")
        assert p.is_compact is True

    def test_stone_profinite_is_zero_dimensional(self):
        p = next(x for x in self.profiles if x.key == "stone_locale_profinite")
        assert p.is_zero_dimensional is True

    def test_stone_profinite_locale_type(self):
        p = next(x for x in self.profiles if x.key == "stone_locale_profinite")
        assert p.locale_type == "stone_locale"

    def test_unit_interval_is_compact(self):
        p = next(x for x in self.profiles if x.key == "unit_interval_locale")
        assert p.is_compact is True

    def test_unit_interval_not_zero_dimensional(self):
        p = next(x for x in self.profiles if x.key == "unit_interval_locale")
        assert p.is_zero_dimensional is False

    def test_unit_interval_is_spatial(self):
        p = next(x for x in self.profiles if x.key == "unit_interval_locale")
        assert p.is_spatial is True

    def test_unit_interval_is_regular(self):
        p = next(x for x in self.profiles if x.key == "unit_interval_locale")
        assert p.is_regular is True

    def test_sierpinski_is_spatial(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_locale")
        assert p.is_spatial is True

    def test_sierpinski_is_compact(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_locale")
        assert p.is_compact is True

    def test_sierpinski_not_regular(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_locale")
        assert p.is_regular is False

    def test_sierpinski_not_completely_regular(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_locale")
        assert p.is_completely_regular is False

    def test_sierpinski_not_zero_dimensional(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_locale")
        assert p.is_zero_dimensional is False

    def test_localic_torus_is_localic_group(self):
        p = next(x for x in self.profiles if x.key == "localic_torus")
        assert p.is_localic_group is True

    def test_localic_torus_is_spatial(self):
        p = next(x for x in self.profiles if x.key == "localic_torus")
        assert p.is_spatial is True

    def test_localic_torus_is_compact(self):
        p = next(x for x in self.profiles if x.key == "localic_torus")
        assert p.is_compact is True

    def test_localic_torus_not_zero_dimensional(self):
        p = next(x for x in self.profiles if x.key == "localic_torus")
        assert p.is_zero_dimensional is False

    def test_all_have_nonempty_focus(self):
        for p in self.profiles:
            assert len(p.focus) > 30

    def test_all_have_chapter_targets(self):
        for p in self.profiles:
            assert len(p.chapter_targets) >= 1

    def test_all_presentation_layers_valid(self):
        valid = {"main_text", "selected_block", "appendix", "exercise"}
        for p in self.profiles:
            assert p.presentation_layer in valid

    def test_non_spatial_implies_no_localic_group(self):
        for p in self.profiles:
            if not p.is_spatial:
                assert p.is_localic_group is False

    def test_stone_locale_is_compact_and_regular(self):
        for p in self.profiles:
            if p.locale_type == "stone_locale":
                assert p.is_compact is True
                assert p.is_regular is True


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(locale_layer_summary(), dict)

    def test_layer_summary_sum_equals_profile_count(self):
        total = sum(locale_layer_summary().values())
        assert total == len(get_named_locale_profiles())

    def test_layer_summary_has_main_text(self):
        assert "main_text" in locale_layer_summary()

    def test_layer_summary_has_selected_block(self):
        assert "selected_block" in locale_layer_summary()

    def test_chapter_index_returns_dict(self):
        assert isinstance(locale_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in locale_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_contains_chapter_10(self):
        assert "10" in locale_chapter_index()

    def test_chapter_index_contains_chapter_28(self):
        assert "28" in locale_chapter_index()

    def test_localic_real_line_in_chapter_10(self):
        assert "localic_real_line" in locale_chapter_index()["10"]

    def test_random_real_in_chapter_52(self):
        assert "random_real_locale" in locale_chapter_index()["52"]

    def test_type_index_returns_dict(self):
        assert isinstance(locale_type_index(), dict)

    def test_type_index_has_spatial_locale(self):
        assert "spatial_locale" in locale_type_index()

    def test_type_index_has_non_spatial_locale(self):
        assert "non_spatial_locale" in locale_type_index()

    def test_type_index_has_stone_locale(self):
        assert "stone_locale" in locale_type_index()

    def test_type_index_has_localic_group(self):
        assert "localic_group" in locale_type_index()

    def test_type_index_all_types_in_profiles(self):
        all_types = {p.locale_type for p in get_named_locale_profiles()}
        assert set(locale_type_index().keys()) == all_types


# ---------------------------------------------------------------------------
# is_spatial_locale
# ---------------------------------------------------------------------------

class TestIsSpatialLocale:
    def test_spatial_locale_tag_true(self):
        assert is_spatial_locale(_sp("spatial_locale")).is_true

    def test_sober_true(self):
        assert is_spatial_locale(_sp("sober")).is_true

    def test_sober_space_true(self):
        assert is_spatial_locale(_sp("sober_space")).is_true

    def test_hausdorff_true(self):
        assert is_spatial_locale(_sp("hausdorff")).is_true

    def test_t2_true(self):
        assert is_spatial_locale(_sp("t2")).is_true

    def test_compact_hausdorff_true(self):
        assert is_spatial_locale(_sp("compact_hausdorff")).is_true

    def test_metrizable_true(self):
        assert is_spatial_locale(_sp("metrizable")).is_true

    def test_stone_space_true(self):
        assert is_spatial_locale(_sp("stone_space")).is_true

    def test_profinite_true(self):
        assert is_spatial_locale(_sp("profinite")).is_true

    def test_localic_group_true(self):
        assert is_spatial_locale(_sp("localic_group")).is_true

    def test_group_object_in_loc_true(self):
        assert is_spatial_locale(_sp("group_object_in_loc")).is_true

    def test_measure_algebra_false(self):
        assert is_spatial_locale(_sp("measure_algebra_locale")).is_false

    def test_non_spatial_locale_false(self):
        assert is_spatial_locale(_sp("non_spatial_locale")).is_false

    def test_no_classical_points_false(self):
        assert is_spatial_locale(_sp("no_classical_points")).is_false

    def test_random_real_locale_false(self):
        assert is_spatial_locale(_sp("random_real_locale")).is_false

    def test_empty_unknown(self):
        assert is_spatial_locale(_sp()).is_unknown

    def test_irrelevant_tags_unknown(self):
        assert is_spatial_locale(_sp("compact", "connected")).is_unknown

    def test_returns_result(self):
        assert isinstance(is_spatial_locale(_sp("sober")), Result)

    def test_true_has_justification(self):
        r = is_spatial_locale(_sp("hausdorff"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_spatial_locale(_sp("non_spatial_locale"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_compact_locale
# ---------------------------------------------------------------------------

class TestIsCompactLocale:
    def test_compact_tag_true(self):
        assert is_compact_locale(_sp("compact")).is_true

    def test_compact_locale_true(self):
        assert is_compact_locale(_sp("compact_locale")).is_true

    def test_compact_hausdorff_true(self):
        assert is_compact_locale(_sp("compact_hausdorff")).is_true

    def test_stone_locale_true(self):
        assert is_compact_locale(_sp("stone_locale")).is_true

    def test_profinite_true(self):
        assert is_compact_locale(_sp("profinite")).is_true

    def test_stone_space_true(self):
        assert is_compact_locale(_sp("stone_space")).is_true

    def test_boolean_locale_true(self):
        assert is_compact_locale(_sp("boolean_locale")).is_true

    def test_measure_algebra_true(self):
        assert is_compact_locale(_sp("measure_algebra_locale")).is_true

    def test_complete_boolean_algebra_true(self):
        assert is_compact_locale(_sp("complete_boolean_algebra")).is_true

    def test_non_compact_locale_false(self):
        assert is_compact_locale(_sp("non_compact_locale")).is_false

    def test_empty_unknown(self):
        assert is_compact_locale(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_compact_locale(_sp("compact")), Result)

    def test_true_has_justification(self):
        r = is_compact_locale(_sp("stone_locale"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_regular_locale
# ---------------------------------------------------------------------------

class TestIsRegularLocale:
    def test_regular_locale_tag_true(self):
        assert is_regular_locale(_sp("regular_locale")).is_true

    def test_completely_regular_true(self):
        assert is_regular_locale(_sp("completely_regular_locale")).is_true

    def test_compact_hausdorff_true(self):
        assert is_regular_locale(_sp("compact_hausdorff")).is_true

    def test_metrizable_true(self):
        assert is_regular_locale(_sp("metrizable")).is_true

    def test_stone_locale_true(self):
        assert is_regular_locale(_sp("stone_locale")).is_true

    def test_boolean_locale_true(self):
        assert is_regular_locale(_sp("boolean_locale")).is_true

    def test_measure_algebra_true(self):
        assert is_regular_locale(_sp("measure_algebra_locale")).is_true

    def test_complete_boolean_algebra_true(self):
        assert is_regular_locale(_sp("complete_boolean_algebra")).is_true

    def test_t0_not_t1_false(self):
        assert is_regular_locale(_sp("t0_not_t1")).is_false

    def test_sierpinski_locale_false(self):
        assert is_regular_locale(_sp("sierpinski_locale")).is_false

    def test_not_regular_locale_false(self):
        assert is_regular_locale(_sp("not_regular_locale")).is_false

    def test_empty_unknown(self):
        assert is_regular_locale(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_regular_locale(_sp("regular_locale")), Result)

    def test_true_has_justification(self):
        r = is_regular_locale(_sp("compact_hausdorff"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_regular_locale(_sp("sierpinski_locale"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_stone_locale
# ---------------------------------------------------------------------------

class TestIsStoneLocale:
    def test_stone_locale_tag_true(self):
        assert is_stone_locale(_sp("stone_locale")).is_true

    def test_boolean_locale_true(self):
        assert is_stone_locale(_sp("boolean_locale")).is_true

    def test_stone_space_true(self):
        assert is_stone_locale(_sp("stone_space")).is_true

    def test_profinite_true(self):
        assert is_stone_locale(_sp("profinite")).is_true

    def test_complete_boolean_algebra_true(self):
        assert is_stone_locale(_sp("complete_boolean_algebra")).is_true

    def test_measure_algebra_true(self):
        assert is_stone_locale(_sp("measure_algebra_locale")).is_true

    def test_clopen_base_locale_true(self):
        assert is_stone_locale(_sp("clopen_base_locale")).is_true

    def test_connected_nontrivial_false(self):
        assert is_stone_locale(_sp("connected_nontrivial")).is_false

    def test_not_zero_dimensional_false(self):
        assert is_stone_locale(_sp("not_zero_dimensional")).is_false

    def test_path_connected_false(self):
        assert is_stone_locale(_sp("path_connected")).is_false

    def test_empty_unknown(self):
        assert is_stone_locale(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_stone_locale(_sp("stone_locale")), Result)

    def test_true_has_justification(self):
        r = is_stone_locale(_sp("stone_space"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_stone_locale(_sp("connected_nontrivial"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# is_localic_group
# ---------------------------------------------------------------------------

class TestIsLocalicGroup:
    def test_localic_group_tag_true(self):
        assert is_localic_group(_sp("localic_group")).is_true

    def test_group_object_in_loc_true(self):
        assert is_localic_group(_sp("group_object_in_loc")).is_true

    def test_localic_abelian_group_true(self):
        assert is_localic_group(_sp("localic_abelian_group")).is_true

    def test_localic_compact_group_true(self):
        assert is_localic_group(_sp("localic_compact_group")).is_true

    def test_topological_group_plus_sober_true(self):
        assert is_localic_group(_sp("topological_group", "sober")).is_true

    def test_topological_group_plus_hausdorff_true(self):
        assert is_localic_group(_sp("topological_group", "hausdorff")).is_true

    def test_topological_group_plus_metrizable_true(self):
        assert is_localic_group(_sp("topological_group", "metrizable")).is_true

    def test_topological_group_alone_unknown(self):
        assert is_localic_group(_sp("topological_group")).is_unknown

    def test_empty_unknown(self):
        assert is_localic_group(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_localic_group(_sp("localic_group")), Result)

    def test_true_has_justification(self):
        r = is_localic_group(_sp("localic_group"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# classify_locale
# ---------------------------------------------------------------------------

class TestClassifyLocale:
    def test_returns_dict(self):
        assert isinstance(classify_locale(_sp()), dict)

    def test_has_locale_class_key(self):
        assert "locale_class" in classify_locale(_sp())

    def test_has_is_spatial_key(self):
        assert "is_spatial_locale" in classify_locale(_sp())

    def test_has_is_compact_key(self):
        assert "is_compact_locale" in classify_locale(_sp())

    def test_has_is_regular_key(self):
        assert "is_regular_locale" in classify_locale(_sp())

    def test_has_is_stone_key(self):
        assert "is_stone_locale" in classify_locale(_sp())

    def test_has_is_localic_group_key(self):
        assert "is_localic_group" in classify_locale(_sp())

    def test_has_key_properties_key(self):
        assert "key_properties" in classify_locale(_sp())

    def test_key_properties_is_list(self):
        assert isinstance(classify_locale(_sp())["key_properties"], list)

    def test_non_spatial_class(self):
        r = classify_locale(_sp("measure_algebra_locale"))
        assert r["locale_class"] == "non_spatial"

    def test_stone_class(self):
        r = classify_locale(_sp("stone_space", "profinite"))
        assert r["locale_class"] == "stone"

    def test_localic_group_class(self):
        r = classify_locale(_sp("localic_group"))
        assert r["locale_class"] == "localic_group"

    def test_compact_regular_class(self):
        r = classify_locale(_sp("compact_hausdorff"))
        assert r["locale_class"] == "compact_regular"

    def test_spatial_class(self):
        r = classify_locale(_sp("sober"))
        assert r["locale_class"] == "spatial"

    def test_unknown_class_empty(self):
        r = classify_locale(_sp())
        assert r["locale_class"] == "unknown"

    def test_non_spatial_in_key_props_for_non_spatial(self):
        r = classify_locale(_sp("non_spatial_locale"))
        assert "non_spatial" in r["key_properties"]

    def test_compact_in_key_props_for_compact(self):
        r = classify_locale(_sp("compact_hausdorff"))
        assert "compact" in r["key_properties"]

    def test_regular_in_key_props_for_regular(self):
        r = classify_locale(_sp("regular_locale"))
        assert "regular" in r["key_properties"]

    def test_stone_locale_in_key_props_for_stone(self):
        r = classify_locale(_sp("stone_space", "profinite"))
        assert "stone_locale" in r["key_properties"]

    def test_localic_group_in_key_props(self):
        r = classify_locale(_sp("localic_group"))
        assert "localic_group" in r["key_properties"]

    def test_zero_dimensional_in_key_props(self):
        r = classify_locale(_sp("stone_locale"))
        assert "zero_dimensional" in r["key_properties"]

    def test_not_regular_in_key_props_for_sierpinski(self):
        r = classify_locale(_sp("sierpinski_locale"))
        assert "not_regular" in r["key_properties"]

    def test_representation_in_output(self):
        assert "representation" in classify_locale(_sp())

    def test_tags_is_list(self):
        assert isinstance(classify_locale(_sp("sober"))["tags"], list)

    def test_spatial_in_key_props_for_hausdorff(self):
        r = classify_locale(_sp("hausdorff"))
        assert "spatial" in r["key_properties"]


# ---------------------------------------------------------------------------
# locale_profile
# ---------------------------------------------------------------------------

class TestLocaleProfile:
    def test_returns_dict(self):
        assert isinstance(locale_profile(_sp()), dict)

    def test_has_classification_key(self):
        assert "classification" in locale_profile(_sp())

    def test_has_named_profiles_key(self):
        assert "named_profiles" in locale_profile(_sp())

    def test_has_layer_summary_key(self):
        assert "layer_summary" in locale_profile(_sp())

    def test_named_profiles_is_tuple(self):
        assert isinstance(locale_profile(_sp())["named_profiles"], tuple)

    def test_classification_has_locale_class(self):
        p = locale_profile(_sp("sober"))
        assert "locale_class" in p["classification"]

    def test_layer_summary_is_dict(self):
        assert isinstance(locale_profile(_sp())["layer_summary"], dict)

    def test_non_spatial_classification_correct(self):
        p = locale_profile(_sp("measure_algebra_locale"))
        assert p["classification"]["locale_class"] == "non_spatial"

    def test_stone_classification_correct(self):
        p = locale_profile(_sp("stone_space", "profinite"))
        assert p["classification"]["locale_class"] == "stone"
