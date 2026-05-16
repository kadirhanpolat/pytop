"""Tests for zero_dimensionality.py (v0.5.9)."""

import types

import pytest

from pytop.zero_dimensionality import (
    COMPACT_HAUSDORFF_TAGS,
    COMPACT_ZD_TAGS,
    EMBEDS_IN_CANTOR_TAGS,
    NOT_ZERO_DIMENSIONAL_TAGS,
    PROFINITE_TAGS,
    SCATTERED_TAGS,
    STONE_DUALITY_TAGS,
    TOTALLY_DISCONNECTED_TAGS,
    ZERO_DIMENSIONAL_TAGS,
    ZeroDimensionalProfile,
    cantor_universality,
    classify_zero_dimensionality,
    get_named_zero_dimensional_profiles,
    has_clopen_base,
    is_profinite,
    is_zero_dimensional,
    stone_duality_applicable,
    zero_dimensional_chapter_index,
    zero_dimensional_layer_summary,
    zero_dimensional_type_index,
    zero_dimensionality_profile,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_zero_dimensional_contains_zero_dimensional(self):
        assert "zero_dimensional" in ZERO_DIMENSIONAL_TAGS

    def test_zero_dimensional_contains_cantor_set(self):
        assert "cantor_set" in ZERO_DIMENSIONAL_TAGS

    def test_zero_dimensional_contains_profinite(self):
        assert "profinite" in ZERO_DIMENSIONAL_TAGS

    def test_zero_dimensional_contains_discrete(self):
        assert "discrete" in ZERO_DIMENSIONAL_TAGS

    def test_zero_dimensional_contains_scattered(self):
        assert "scattered" in ZERO_DIMENSIONAL_TAGS

    def test_zero_dimensional_contains_rationals(self):
        assert "rationals" in ZERO_DIMENSIONAL_TAGS

    def test_zero_dimensional_contains_baire_space(self):
        assert "baire_space" in ZERO_DIMENSIONAL_TAGS

    def test_totally_disconnected_contains_totally_disconnected(self):
        assert "totally_disconnected" in TOTALLY_DISCONNECTED_TAGS

    def test_totally_disconnected_contains_cantor_set(self):
        assert "cantor_set" in TOTALLY_DISCONNECTED_TAGS

    def test_totally_disconnected_contains_profinite(self):
        assert "profinite" in TOTALLY_DISCONNECTED_TAGS

    def test_profinite_contains_profinite(self):
        assert "profinite" in PROFINITE_TAGS

    def test_profinite_contains_p_adic_integers(self):
        assert "p_adic_integers" in PROFINITE_TAGS

    def test_profinite_contains_cantor_space(self):
        assert "cantor_space" in PROFINITE_TAGS

    def test_profinite_contains_stone_space(self):
        assert "stone_space" in PROFINITE_TAGS

    def test_compact_zd_contains_cantor_set(self):
        assert "cantor_set" in COMPACT_ZD_TAGS

    def test_compact_zd_contains_profinite(self):
        assert "profinite" in COMPACT_ZD_TAGS

    def test_compact_zd_contains_finite_space(self):
        assert "finite_space" in COMPACT_ZD_TAGS

    def test_scattered_contains_scattered(self):
        assert "scattered" in SCATTERED_TAGS

    def test_scattered_contains_discrete(self):
        assert "discrete" in SCATTERED_TAGS

    def test_not_zero_dimensional_contains_connected(self):
        assert "connected" in NOT_ZERO_DIMENSIONAL_TAGS

    def test_not_zero_dimensional_contains_real_line(self):
        assert "real_line" in NOT_ZERO_DIMENSIONAL_TAGS

    def test_not_zero_dimensional_contains_continuum(self):
        assert "continuum" in NOT_ZERO_DIMENSIONAL_TAGS

    def test_compact_hausdorff_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in COMPACT_HAUSDORFF_TAGS

    def test_compact_hausdorff_contains_profinite(self):
        assert "profinite" in COMPACT_HAUSDORFF_TAGS

    def test_stone_duality_contains_stone_space(self):
        assert "stone_space" in STONE_DUALITY_TAGS

    def test_stone_duality_contains_profinite(self):
        assert "profinite" in STONE_DUALITY_TAGS

    def test_embeds_in_cantor_contains_compact_metrizable(self):
        assert "compact_metrizable" in EMBEDS_IN_CANTOR_TAGS

    def test_embeds_in_cantor_contains_cantor_set(self):
        assert "cantor_set" in EMBEDS_IN_CANTOR_TAGS

    def test_embeds_in_cantor_contains_profinite(self):
        assert "profinite" in EMBEDS_IN_CANTOR_TAGS


# ---------------------------------------------------------------------------
# ZeroDimensionalProfile dataclass
# ---------------------------------------------------------------------------

class TestZeroDimensionalProfileDataclass:
    def test_profile_is_frozen(self):
        p = ZeroDimensionalProfile(
            key="test",
            display_name="Test",
            space_type="test_type",
            is_compact=True,
            is_metrizable=True,
            is_profinite=False,
            is_scattered=False,
            presentation_layer="main_text",
            focus="test focus",
            chapter_targets=("4",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields(self):
        p = ZeroDimensionalProfile(
            key="cantor",
            display_name="Cantor",
            space_type="compact_metrizable_perfect",
            is_compact=True,
            is_metrizable=True,
            is_profinite=True,
            is_scattered=False,
            presentation_layer="main_text",
            focus="focus text",
            chapter_targets=("4", "6"),
        )
        assert p.key == "cantor"
        assert p.is_compact is True
        assert p.is_profinite is True
        assert p.is_scattered is False
        assert "4" in p.chapter_targets


# ---------------------------------------------------------------------------
# Named profiles registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        profiles = get_named_zero_dimensional_profiles()
        assert isinstance(profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(get_named_zero_dimensional_profiles()) >= 5

    def test_cantor_space_present(self):
        keys = {p.key for p in get_named_zero_dimensional_profiles()}
        assert "cantor_space" in keys

    def test_cantor_set_present(self):
        keys = {p.key for p in get_named_zero_dimensional_profiles()}
        assert "cantor_set" in keys

    def test_p_adic_integers_present(self):
        keys = {p.key for p in get_named_zero_dimensional_profiles()}
        assert "p_adic_integers" in keys

    def test_rational_numbers_present(self):
        keys = {p.key for p in get_named_zero_dimensional_profiles()}
        assert "rational_numbers" in keys

    def test_baire_space_present(self):
        keys = {p.key for p in get_named_zero_dimensional_profiles()}
        assert "baire_space" in keys

    def test_cantor_space_is_compact(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["cantor_space"].is_compact is True

    def test_cantor_space_is_profinite(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["cantor_space"].is_profinite is True

    def test_rational_numbers_not_compact(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["rational_numbers"].is_compact is False

    def test_rational_numbers_not_profinite(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["rational_numbers"].is_profinite is False

    def test_baire_space_not_compact(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["baire_space"].is_compact is False

    def test_p_adic_is_profinite(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["p_adic_integers"].is_profinite is True

    def test_discrete_countable_is_scattered(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["discrete_countable"].is_scattered is True

    def test_cantor_space_not_scattered(self):
        profiles = {p.key: p for p in get_named_zero_dimensional_profiles()}
        assert profiles["cantor_space"].is_scattered is False

    def test_all_profiles_have_chapter_targets(self):
        for p in get_named_zero_dimensional_profiles():
            assert len(p.chapter_targets) >= 1

    def test_all_profiles_have_focus(self):
        for p in get_named_zero_dimensional_profiles():
            assert len(p.focus) > 20

    def test_all_profiles_have_display_name(self):
        for p in get_named_zero_dimensional_profiles():
            assert len(p.display_name) > 3

    def test_all_keys_are_unique(self):
        keys = [p.key for p in get_named_zero_dimensional_profiles()]
        assert len(keys) == len(set(keys))


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        result = zero_dimensional_layer_summary()
        assert isinstance(result, dict)

    def test_layer_summary_has_main_text(self):
        summary = zero_dimensional_layer_summary()
        assert "main_text" in summary

    def test_layer_summary_values_are_positive(self):
        summary = zero_dimensional_layer_summary()
        assert all(v > 0 for v in summary.values())

    def test_chapter_index_returns_dict(self):
        index = zero_dimensional_chapter_index()
        assert isinstance(index, dict)

    def test_chapter_index_chapter_4_exists(self):
        index = zero_dimensional_chapter_index()
        assert "4" in index

    def test_chapter_index_chapter_4_has_cantor(self):
        index = zero_dimensional_chapter_index()
        assert "cantor_space" in index["4"]

    def test_chapter_index_values_are_tuples(self):
        for val in zero_dimensional_chapter_index().values():
            assert isinstance(val, tuple)

    def test_type_index_returns_dict(self):
        index = zero_dimensional_type_index()
        assert isinstance(index, dict)

    def test_type_index_has_compact_metrizable_perfect(self):
        index = zero_dimensional_type_index()
        assert "compact_metrizable_perfect" in index

    def test_type_index_values_are_tuples(self):
        for val in zero_dimensional_type_index().values():
            assert isinstance(val, tuple)


# ---------------------------------------------------------------------------
# has_clopen_base
# ---------------------------------------------------------------------------

class TestHasClopenBase:
    def test_explicit_zero_dimensional_true(self):
        sp = _sp("zero_dimensional")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_clopen_base_tag_true(self):
        sp = _sp("clopen_base")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_cantor_set_true(self):
        sp = _sp("cantor_set")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_cantor_space_true(self):
        sp = _sp("cantor_space")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_discrete_true(self):
        sp = _sp("discrete")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_p_adic_integers_true(self):
        sp = _sp("p_adic_integers")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_rationals_true(self):
        sp = _sp("rationals")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_baire_space_true(self):
        sp = _sp("baire_space")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_profinite_true(self):
        sp = _sp("profinite")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_stone_space_true(self):
        sp = _sp("stone_space")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_totally_disconnected_compact_hausdorff_true(self):
        sp = _sp("totally_disconnected", "compact_hausdorff")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_totally_disconnected_metrizable_true(self):
        sp = _sp("totally_disconnected", "metrizable")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_totally_disconnected_metric_true(self):
        sp = _sp("totally_disconnected", "metric")
        r = has_clopen_base(sp)
        assert r.is_true

    def test_connected_false(self):
        sp = _sp("connected")
        r = has_clopen_base(sp)
        assert r.is_false

    def test_real_line_false(self):
        sp = _sp("real_line")
        r = has_clopen_base(sp)
        assert r.is_false

    def test_interval_false(self):
        sp = _sp("closed_interval")
        r = has_clopen_base(sp)
        assert r.is_false

    def test_continuum_false(self):
        sp = _sp("continuum")
        r = has_clopen_base(sp)
        assert r.is_false

    def test_unknown_empty(self):
        sp = _sp()
        r = has_clopen_base(sp)
        assert r.is_unknown

    def test_unknown_generic(self):
        sp = _sp("hausdorff", "separable")
        r = has_clopen_base(sp)
        assert r.is_unknown

    def test_returns_result_instance(self):
        sp = _sp("cantor_set")
        assert isinstance(has_clopen_base(sp), Result)

    def test_true_result_has_justification(self):
        sp = _sp("profinite")
        r = has_clopen_base(sp)
        assert r.justification

    def test_false_result_has_justification(self):
        sp = _sp("connected")
        r = has_clopen_base(sp)
        assert r.justification


# ---------------------------------------------------------------------------
# is_zero_dimensional
# ---------------------------------------------------------------------------

class TestIsZeroDimensional:
    def test_zero_dimensional_tag_true(self):
        sp = _sp("zero_dimensional")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_cantor_space_true(self):
        sp = _sp("cantor_space")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_cantor_set_true(self):
        sp = _sp("cantor_set")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_profinite_true(self):
        sp = _sp("profinite")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_p_adic_integers_true(self):
        sp = _sp("p_adic_integers")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_discrete_true(self):
        sp = _sp("discrete")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_baire_space_true(self):
        sp = _sp("baire_space")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_scattered_true(self):
        sp = _sp("scattered")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_totally_disconnected_compact_hausdorff_true(self):
        sp = _sp("totally_disconnected", "compact_hausdorff")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_totally_disconnected_metrizable_true(self):
        sp = _sp("totally_disconnected", "metrizable")
        r = is_zero_dimensional(sp)
        assert r.is_true

    def test_connected_false(self):
        sp = _sp("connected")
        r = is_zero_dimensional(sp)
        assert r.is_false

    def test_path_connected_false(self):
        sp = _sp("path_connected")
        r = is_zero_dimensional(sp)
        assert r.is_false

    def test_real_line_false(self):
        sp = _sp("real_line")
        r = is_zero_dimensional(sp)
        assert r.is_false

    def test_manifold_false(self):
        sp = _sp("manifold")
        r = is_zero_dimensional(sp)
        assert r.is_false

    def test_unknown_empty(self):
        sp = _sp()
        r = is_zero_dimensional(sp)
        assert r.is_unknown

    def test_returns_result(self):
        sp = _sp("discrete")
        assert isinstance(is_zero_dimensional(sp), Result)


# ---------------------------------------------------------------------------
# is_profinite
# ---------------------------------------------------------------------------

class TestIsProfinite:
    def test_explicit_profinite_tag_true(self):
        sp = _sp("profinite")
        r = is_profinite(sp)
        assert r.is_true

    def test_profinite_space_tag_true(self):
        sp = _sp("profinite_space")
        r = is_profinite(sp)
        assert r.is_true

    def test_cantor_space_compact_hausdorff_true(self):
        sp = _sp("cantor_space", "compact_hausdorff")
        r = is_profinite(sp)
        assert r.is_true

    def test_cantor_set_compact_metrizable_true(self):
        sp = _sp("cantor_set", "compact_metrizable")
        r = is_profinite(sp)
        assert r.is_true

    def test_p_adic_integers_compact_metrizable_true(self):
        sp = _sp("p_adic_integers", "compact_metrizable")
        r = is_profinite(sp)
        assert r.is_true

    def test_stone_space_compact_hausdorff_true(self):
        sp = _sp("stone_space", "compact_hausdorff")
        r = is_profinite(sp)
        assert r.is_true

    def test_totally_disconnected_compact_true(self):
        sp = _sp("totally_disconnected", "compact_hausdorff")
        r = is_profinite(sp)
        assert r.is_true

    def test_totally_disconnected_compact_metrizable_true(self):
        sp = _sp("totally_disconnected", "compact_metrizable")
        r = is_profinite(sp)
        assert r.is_true

    def test_rationals_not_compact_false(self):
        sp = _sp("rationals")
        r = is_profinite(sp)
        assert r.is_false

    def test_baire_space_not_compact_false(self):
        sp = _sp("baire_space")
        r = is_profinite(sp)
        assert r.is_false

    def test_real_line_not_compact_false(self):
        sp = _sp("real_line")
        r = is_profinite(sp)
        assert r.is_false

    def test_irrationals_not_compact_false(self):
        sp = _sp("irrationals")
        r = is_profinite(sp)
        assert r.is_false

    def test_unknown_empty(self):
        sp = _sp()
        r = is_profinite(sp)
        assert r.is_unknown

    def test_unknown_compact_without_hausdorff_zd(self):
        sp = _sp("compact")
        r = is_profinite(sp)
        assert r.is_unknown

    def test_returns_result(self):
        sp = _sp("profinite")
        assert isinstance(is_profinite(sp), Result)

    def test_true_has_justification(self):
        sp = _sp("profinite")
        r = is_profinite(sp)
        assert r.justification

    def test_false_has_justification(self):
        sp = _sp("rationals")
        r = is_profinite(sp)
        assert r.justification


# ---------------------------------------------------------------------------
# stone_duality_applicable
# ---------------------------------------------------------------------------

class TestStoneDualityApplicable:
    def test_stone_space_tag_true(self):
        sp = _sp("stone_space")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_boolean_space_tag_true(self):
        sp = _sp("boolean_space")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_profinite_true(self):
        sp = _sp("profinite")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_cantor_space_true(self):
        sp = _sp("cantor_space")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_cantor_set_true(self):
        sp = _sp("cantor_set")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_p_adic_integers_true(self):
        sp = _sp("p_adic_integers")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_compact_metrizable_zero_dimensional_true(self):
        sp = _sp("compact_metrizable", "zero_dimensional")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_compact_hausdorff_zero_dimensional_true(self):
        sp = _sp("compact_hausdorff", "zero_dimensional")
        r = stone_duality_applicable(sp)
        assert r.is_true

    def test_connected_false(self):
        sp = _sp("connected")
        r = stone_duality_applicable(sp)
        assert r.is_false

    def test_real_line_false(self):
        sp = _sp("real_line")
        r = stone_duality_applicable(sp)
        assert r.is_false

    def test_rationals_not_compact_false(self):
        sp = _sp("rationals")
        r = stone_duality_applicable(sp)
        assert r.is_false

    def test_baire_space_not_compact_false(self):
        sp = _sp("baire_space")
        r = stone_duality_applicable(sp)
        assert r.is_false

    def test_unknown_empty(self):
        sp = _sp()
        r = stone_duality_applicable(sp)
        assert r.is_unknown

    def test_returns_result(self):
        sp = _sp("stone_space")
        assert isinstance(stone_duality_applicable(sp), Result)


# ---------------------------------------------------------------------------
# cantor_universality
# ---------------------------------------------------------------------------

class TestCantorUniversality:
    def test_cantor_set_itself_true(self):
        sp = _sp("cantor_set")
        r = cantor_universality(sp)
        assert r.is_true

    def test_cantor_space_itself_true(self):
        sp = _sp("cantor_space")
        r = cantor_universality(sp)
        assert r.is_true

    def test_compact_metrizable_zero_dimensional_true(self):
        sp = _sp("compact_metrizable", "zero_dimensional", "metrizable")
        r = cantor_universality(sp)
        assert r.is_true

    def test_compact_metrizable_totally_disconnected_true(self):
        sp = _sp("compact_metrizable", "totally_disconnected", "metrizable")
        r = cantor_universality(sp)
        assert r.is_true

    def test_profinite_metrizable_true(self):
        sp = _sp("profinite", "compact_metrizable")
        r = cantor_universality(sp)
        assert r.is_true

    def test_p_adic_integers_metrizable_true(self):
        sp = _sp("p_adic_integers", "compact_metrizable")
        r = cantor_universality(sp)
        assert r.is_true

    def test_finite_discrete_compact_metrizable_true(self):
        sp = _sp("finite_space", "compact_metrizable", "zero_dimensional", "metrizable")
        r = cantor_universality(sp)
        assert r.is_true

    def test_non_metrizable_compact_false(self):
        sp = _sp("compact", "not_metrizable")
        r = cantor_universality(sp)
        assert r.is_false

    def test_uncountable_weight_compact_false(self):
        sp = _sp("compact", "uncountable_weight")
        r = cantor_universality(sp)
        assert r.is_false

    def test_rationals_not_compact_false(self):
        sp = _sp("rationals")
        r = cantor_universality(sp)
        assert r.is_false

    def test_real_line_not_compact_false(self):
        sp = _sp("real_line")
        r = cantor_universality(sp)
        assert r.is_false

    def test_baire_space_not_compact_false(self):
        sp = _sp("baire_space")
        r = cantor_universality(sp)
        assert r.is_false

    def test_irrationals_not_compact_false(self):
        sp = _sp("irrationals")
        r = cantor_universality(sp)
        assert r.is_false

    def test_unknown_empty(self):
        sp = _sp()
        r = cantor_universality(sp)
        assert r.is_unknown

    def test_unknown_compact_no_zd(self):
        sp = _sp("compact_metrizable")
        r = cantor_universality(sp)
        assert r.is_unknown

    def test_returns_result(self):
        sp = _sp("cantor_set")
        assert isinstance(cantor_universality(sp), Result)

    def test_true_has_justification(self):
        sp = _sp("cantor_set")
        r = cantor_universality(sp)
        assert r.justification

    def test_false_has_justification(self):
        sp = _sp("rationals")
        r = cantor_universality(sp)
        assert r.justification


# ---------------------------------------------------------------------------
# classify_zero_dimensionality
# ---------------------------------------------------------------------------

class TestClassifyZeroDimensionality:
    def test_returns_dict(self):
        sp = _sp("cantor_space")
        result = classify_zero_dimensionality(sp)
        assert isinstance(result, dict)

    def test_profinite_type_for_profinite_space(self):
        sp = _sp("profinite")
        result = classify_zero_dimensionality(sp)
        assert result["zero_dim_type"] == "profinite"

    def test_cantor_space_is_profinite_type(self):
        sp = _sp("cantor_space", "compact_hausdorff")
        result = classify_zero_dimensionality(sp)
        assert result["zero_dim_type"] == "profinite"

    def test_connected_is_not_zero_dimensional_type(self):
        sp = _sp("connected", "real_line")
        result = classify_zero_dimensionality(sp)
        assert result["zero_dim_type"] == "not_zero_dimensional"

    def test_zero_dimensional_type_for_zd_space(self):
        sp = _sp("zero_dimensional")
        result = classify_zero_dimensionality(sp)
        assert result["zero_dim_type"] in {"zero_dimensional", "profinite",
                                            "compact_metrizable_zd", "polish_zd",
                                            "scattered"}

    def test_scattered_type(self):
        sp = _sp("scattered", "discrete")
        result = classify_zero_dimensionality(sp)
        assert result["zero_dim_type"] in {"scattered", "zero_dimensional"}

    def test_has_all_required_keys(self):
        sp = _sp("cantor_space")
        result = classify_zero_dimensionality(sp)
        for key in ("zero_dim_type", "has_clopen_base", "is_zero_dimensional",
                    "is_profinite", "stone_duality", "embeds_in_cantor",
                    "key_properties", "representation", "tags"):
            assert key in result

    def test_key_properties_is_list(self):
        sp = _sp("profinite")
        result = classify_zero_dimensionality(sp)
        assert isinstance(result["key_properties"], list)

    def test_profinite_has_profinite_in_properties(self):
        sp = _sp("profinite")
        result = classify_zero_dimensionality(sp)
        assert "profinite" in result["key_properties"]

    def test_clopen_base_in_properties_for_zd(self):
        sp = _sp("zero_dimensional")
        result = classify_zero_dimensionality(sp)
        assert "clopen_base" in result["key_properties"]

    def test_not_zero_dimensional_in_properties_for_connected(self):
        sp = _sp("connected")
        result = classify_zero_dimensionality(sp)
        assert "not_zero_dimensional" in result["key_properties"]

    def test_sub_results_are_result_instances(self):
        sp = _sp("cantor_set")
        result = classify_zero_dimensionality(sp)
        for key in ("has_clopen_base", "is_zero_dimensional", "is_profinite",
                    "stone_duality", "embeds_in_cantor"):
            assert isinstance(result[key], Result)

    def test_tags_field_is_sorted_list(self):
        sp = _sp("profinite", "compact_hausdorff", "cantor_space")
        result = classify_zero_dimensionality(sp)
        assert isinstance(result["tags"], list)
        assert result["tags"] == sorted(result["tags"])


# ---------------------------------------------------------------------------
# zero_dimensionality_profile
# ---------------------------------------------------------------------------

class TestZeroDimensionalityProfile:
    def test_returns_dict(self):
        sp = _sp("cantor_set")
        result = zero_dimensionality_profile(sp)
        assert isinstance(result, dict)

    def test_has_classification_key(self):
        sp = _sp("profinite")
        result = zero_dimensionality_profile(sp)
        assert "classification" in result

    def test_has_named_profiles_key(self):
        sp = _sp("profinite")
        result = zero_dimensionality_profile(sp)
        assert "named_profiles" in result

    def test_has_layer_summary_key(self):
        sp = _sp("profinite")
        result = zero_dimensionality_profile(sp)
        assert "layer_summary" in result

    def test_named_profiles_is_tuple(self):
        sp = _sp("discrete")
        result = zero_dimensionality_profile(sp)
        assert isinstance(result["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        sp = _sp("cantor_space")
        result = zero_dimensionality_profile(sp)
        assert isinstance(result["layer_summary"], dict)

    def test_classification_is_dict(self):
        sp = _sp("cantor_space")
        result = zero_dimensionality_profile(sp)
        assert isinstance(result["classification"], dict)


# ---------------------------------------------------------------------------
# __all__ and module structure
# ---------------------------------------------------------------------------

class TestModuleStructure:
    def test_all_is_defined(self):
        import pytop.zero_dimensionality as m
        assert hasattr(m, "__all__")

    def test_all_is_list(self):
        import pytop.zero_dimensionality as m
        assert isinstance(m.__all__, list)

    def test_profile_class_in_all(self):
        import pytop.zero_dimensionality as m
        assert "ZeroDimensionalProfile" in m.__all__

    def test_classify_in_all(self):
        import pytop.zero_dimensionality as m
        assert "classify_zero_dimensionality" in m.__all__

    def test_all_names_are_importable(self):
        import pytop.zero_dimensionality as m
        for name in m.__all__:
            assert hasattr(m, name), f"{name} is in __all__ but not defined"

    def test_module_is_importable_from_pytop(self):
        from pytop import zero_dimensionality_profile as _  # noqa: F401

    def test_zero_dimensional_profile_importable_from_pytop(self):
        from pytop import ZeroDimensionalProfile as _  # noqa: F401
