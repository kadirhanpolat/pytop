"""Tests for borel_measures.py (v0.5.10)."""

import pytest

from pytop.borel_measures import (
    ATOMIC_MEASURE_TAGS,
    COMPACT_HAUSDORFF_SPACE_TAGS,
    COMPACT_SUPPORT_TAGS,
    HAAR_MEASURE_TAGS,
    LOCALLY_COMPACT_HAUSDORFF_TAGS,
    NON_ATOMIC_TAGS,
    NOT_HAAR_TAGS,
    NOT_RADON_TAGS,
    RADON_MEASURE_TAGS,
    REGULAR_MEASURE_TAGS,
    SIGMA_FINITE_TAGS,
    BorelMeasureProfile,
    borel_measure_chapter_index,
    borel_measure_layer_summary,
    borel_measure_profile,
    borel_measure_type_index,
    classify_borel_measure,
    get_named_borel_measure_profiles,
    has_haar_measure,
    is_radon_measure,
    is_regular_measure,
    measure_support_is_compact,
    riesz_representation_applies,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_radon_tags_contains_radon_measure(self):
        assert "radon_measure" in RADON_MEASURE_TAGS

    def test_radon_tags_contains_dirac(self):
        assert "dirac_measure" in RADON_MEASURE_TAGS

    def test_radon_tags_contains_lebesgue(self):
        assert "lebesgue_measure" in RADON_MEASURE_TAGS

    def test_radon_tags_contains_haar(self):
        assert "haar_measure" in RADON_MEASURE_TAGS

    def test_radon_tags_contains_gaussian(self):
        assert "gaussian_measure" in RADON_MEASURE_TAGS

    def test_radon_tags_contains_probability(self):
        assert "probability_measure" in RADON_MEASURE_TAGS

    def test_regular_tags_contains_regular_measure(self):
        assert "regular_measure" in REGULAR_MEASURE_TAGS

    def test_regular_tags_contains_radon(self):
        assert "radon_measure" in REGULAR_MEASURE_TAGS

    def test_regular_tags_contains_lebesgue(self):
        assert "lebesgue_measure" in REGULAR_MEASURE_TAGS

    def test_compact_hausdorff_tags_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in COMPACT_HAUSDORFF_SPACE_TAGS

    def test_compact_hausdorff_tags_contains_compact_metrizable(self):
        assert "compact_metrizable" in COMPACT_HAUSDORFF_SPACE_TAGS

    def test_compact_hausdorff_tags_contains_cantor_set(self):
        assert "cantor_set" in COMPACT_HAUSDORFF_SPACE_TAGS

    def test_lc_hausdorff_tags_contains_real_line(self):
        assert "real_line" in LOCALLY_COMPACT_HAUSDORFF_TAGS

    def test_lc_hausdorff_tags_contains_compact_hausdorff(self):
        assert "compact_hausdorff" in LOCALLY_COMPACT_HAUSDORFF_TAGS

    def test_haar_tags_contains_topological_group(self):
        assert "topological_group" in HAAR_MEASURE_TAGS

    def test_haar_tags_contains_real_line(self):
        assert "real_line" in HAAR_MEASURE_TAGS

    def test_haar_tags_contains_torus(self):
        assert "torus" in HAAR_MEASURE_TAGS

    def test_atomic_tags_contains_dirac(self):
        assert "dirac_measure" in ATOMIC_MEASURE_TAGS

    def test_atomic_tags_contains_counting(self):
        assert "counting_measure" in ATOMIC_MEASURE_TAGS

    def test_non_atomic_tags_contains_lebesgue(self):
        assert "lebesgue_measure" in NON_ATOMIC_TAGS

    def test_non_atomic_tags_contains_gaussian(self):
        assert "gaussian_measure" in NON_ATOMIC_TAGS

    def test_compact_support_tags_contains_dirac(self):
        assert "dirac_measure" in COMPACT_SUPPORT_TAGS

    def test_not_radon_tags_contains_not_radon(self):
        assert "not_radon" in NOT_RADON_TAGS

    def test_not_haar_tags_contains_infinite_dim_banach(self):
        assert "infinite_dimensional_banach" in NOT_HAAR_TAGS

    def test_sigma_finite_tags_contains_lebesgue(self):
        assert "lebesgue_measure" in SIGMA_FINITE_TAGS

    def test_sigma_finite_tags_contains_probability(self):
        assert "probability_measure" in SIGMA_FINITE_TAGS


# ---------------------------------------------------------------------------
# BorelMeasureProfile dataclass
# ---------------------------------------------------------------------------

class TestBorelMeasureProfileDataclass:
    def test_profile_is_frozen(self):
        p = BorelMeasureProfile(
            key="test",
            display_name="Test",
            measure_type="test_type",
            is_radon=True,
            is_regular=True,
            is_atomic=False,
            is_sigma_finite=True,
            support_type="whole_space",
            presentation_layer="main_text",
            focus="test focus",
            chapter_targets=("5",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = BorelMeasureProfile(
            key="lebesgue",
            display_name="Lebesgue",
            measure_type="translation_invariant",
            is_radon=True,
            is_regular=True,
            is_atomic=False,
            is_sigma_finite=True,
            support_type="whole_space",
            presentation_layer="main_text",
            focus="focus",
            chapter_targets=("5", "17"),
        )
        assert p.key == "lebesgue"
        assert p.is_radon is True
        assert p.is_atomic is False
        assert "5" in p.chapter_targets


# ---------------------------------------------------------------------------
# Named profiles registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_borel_measure_profiles(), tuple)

    def test_at_least_five_profiles(self):
        assert len(get_named_borel_measure_profiles()) >= 5

    def test_lebesgue_present(self):
        keys = {p.key for p in get_named_borel_measure_profiles()}
        assert "lebesgue_measure" in keys

    def test_dirac_present(self):
        keys = {p.key for p in get_named_borel_measure_profiles()}
        assert "dirac_measure" in keys

    def test_haar_compact_present(self):
        keys = {p.key for p in get_named_borel_measure_profiles()}
        assert "haar_measure_compact" in keys

    def test_counting_measure_present(self):
        keys = {p.key for p in get_named_borel_measure_profiles()}
        assert "counting_measure" in keys

    def test_cantor_measure_present(self):
        keys = {p.key for p in get_named_borel_measure_profiles()}
        assert "cantor_measure" in keys

    def test_gaussian_measure_present(self):
        keys = {p.key for p in get_named_borel_measure_profiles()}
        assert "gaussian_measure" in keys

    def test_lebesgue_is_radon(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["lebesgue_measure"].is_radon is True

    def test_lebesgue_is_regular(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["lebesgue_measure"].is_regular is True

    def test_lebesgue_not_atomic(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["lebesgue_measure"].is_atomic is False

    def test_dirac_is_atomic(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["dirac_measure"].is_atomic is True

    def test_dirac_is_radon(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["dirac_measure"].is_radon is True

    def test_counting_measure_not_radon(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["counting_measure"].is_radon is False

    def test_counting_measure_is_atomic(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["counting_measure"].is_atomic is True

    def test_cantor_measure_not_atomic(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["cantor_measure"].is_atomic is False

    def test_cantor_measure_is_radon(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["cantor_measure"].is_radon is True

    def test_cantor_measure_support_is_cantor(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["cantor_measure"].support_type == "cantor_set"

    def test_dirac_support_is_singleton(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["dirac_measure"].support_type == "singleton"

    def test_haar_compact_is_sigma_finite(self):
        profiles = {p.key: p for p in get_named_borel_measure_profiles()}
        assert profiles["haar_measure_compact"].is_sigma_finite is True

    def test_all_keys_unique(self):
        keys = [p.key for p in get_named_borel_measure_profiles()]
        assert len(keys) == len(set(keys))

    def test_all_profiles_have_chapter_targets(self):
        for p in get_named_borel_measure_profiles():
            assert len(p.chapter_targets) >= 1

    def test_all_profiles_have_focus(self):
        for p in get_named_borel_measure_profiles():
            assert len(p.focus) > 20


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(borel_measure_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in borel_measure_layer_summary()

    def test_layer_summary_values_positive(self):
        assert all(v > 0 for v in borel_measure_layer_summary().values())

    def test_chapter_index_returns_dict(self):
        assert isinstance(borel_measure_chapter_index(), dict)

    def test_chapter_index_chapter_5_exists(self):
        assert "5" in borel_measure_chapter_index()

    def test_chapter_index_chapter_5_has_lebesgue(self):
        assert "lebesgue_measure" in borel_measure_chapter_index()["5"]

    def test_chapter_index_values_are_tuples(self):
        for val in borel_measure_chapter_index().values():
            assert isinstance(val, tuple)

    def test_type_index_returns_dict(self):
        assert isinstance(borel_measure_type_index(), dict)

    def test_type_index_has_point_mass(self):
        assert "point_mass" in borel_measure_type_index()

    def test_type_index_has_translation_invariant(self):
        assert "translation_invariant" in borel_measure_type_index()

    def test_type_index_values_are_tuples(self):
        for val in borel_measure_type_index().values():
            assert isinstance(val, tuple)


# ---------------------------------------------------------------------------
# is_radon_measure
# ---------------------------------------------------------------------------

class TestIsRadonMeasure:
    def test_radon_measure_tag_true(self):
        assert is_radon_measure(_sp("radon_measure")).is_true

    def test_radon_tag_true(self):
        assert is_radon_measure(_sp("radon")).is_true

    def test_dirac_measure_true(self):
        assert is_radon_measure(_sp("dirac_measure")).is_true

    def test_lebesgue_measure_true(self):
        assert is_radon_measure(_sp("lebesgue_measure")).is_true

    def test_haar_measure_true(self):
        assert is_radon_measure(_sp("haar_measure")).is_true

    def test_gaussian_measure_true(self):
        assert is_radon_measure(_sp("gaussian_measure")).is_true

    def test_probability_measure_true(self):
        assert is_radon_measure(_sp("probability_measure")).is_true

    def test_finite_measure_true(self):
        assert is_radon_measure(_sp("finite_measure")).is_true

    def test_compact_hausdorff_true(self):
        assert is_radon_measure(_sp("compact_hausdorff")).is_true

    def test_compact_metrizable_true(self):
        assert is_radon_measure(_sp("compact_metrizable")).is_true

    def test_cantor_set_true(self):
        assert is_radon_measure(_sp("cantor_set")).is_true

    def test_lc_hausdorff_plus_regular_true(self):
        sp = _sp("locally_compact_hausdorff", "regular_measure")
        assert is_radon_measure(sp).is_true

    def test_real_line_plus_regular_true(self):
        sp = _sp("real_line", "regular_measure")
        assert is_radon_measure(sp).is_true

    def test_counting_measure_uncountable_false(self):
        assert is_radon_measure(_sp("counting_measure_uncountable")).is_false

    def test_not_radon_tag_false(self):
        assert is_radon_measure(_sp("not_radon")).is_false

    def test_non_locally_finite_false(self):
        assert is_radon_measure(_sp("non_locally_finite")).is_false

    def test_unknown_empty(self):
        assert is_radon_measure(_sp()).is_unknown

    def test_unknown_generic_space(self):
        assert is_radon_measure(_sp("hausdorff", "separable")).is_unknown

    def test_returns_result(self):
        assert isinstance(is_radon_measure(_sp("radon_measure")), Result)

    def test_true_has_justification(self):
        assert is_radon_measure(_sp("lebesgue_measure")).justification

    def test_false_has_justification(self):
        assert is_radon_measure(_sp("not_radon")).justification


# ---------------------------------------------------------------------------
# is_regular_measure
# ---------------------------------------------------------------------------

class TestIsRegularMeasure:
    def test_regular_measure_tag_true(self):
        assert is_regular_measure(_sp("regular_measure")).is_true

    def test_outer_regular_tag_true(self):
        assert is_regular_measure(_sp("outer_regular")).is_true

    def test_inner_regular_tag_true(self):
        assert is_regular_measure(_sp("inner_regular")).is_true

    def test_radon_measure_tag_true(self):
        assert is_regular_measure(_sp("radon_measure")).is_true

    def test_lebesgue_measure_true(self):
        assert is_regular_measure(_sp("lebesgue_measure")).is_true

    def test_haar_measure_true(self):
        assert is_regular_measure(_sp("haar_measure")).is_true

    def test_dirac_measure_true(self):
        assert is_regular_measure(_sp("dirac_measure")).is_true

    def test_radon_plus_lc_hausdorff_true(self):
        sp = _sp("radon_measure", "locally_compact_hausdorff")
        assert is_regular_measure(sp).is_true

    def test_radon_plus_real_line_true(self):
        sp = _sp("radon_measure", "real_line")
        assert is_regular_measure(sp).is_true

    def test_compact_metrizable_probability_true(self):
        sp = _sp("compact_metrizable", "probability_measure")
        assert is_regular_measure(sp).is_true

    def test_compact_metric_borel_true(self):
        sp = _sp("compact_metric", "borel_measure")
        assert is_regular_measure(sp).is_true

    def test_not_regular_false(self):
        assert is_regular_measure(_sp("not_regular")).is_false

    def test_not_regular_measure_false(self):
        assert is_regular_measure(_sp("not_regular_measure")).is_false

    def test_unknown_empty(self):
        assert is_regular_measure(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_regular_measure(_sp("regular_measure")), Result)


# ---------------------------------------------------------------------------
# riesz_representation_applies
# ---------------------------------------------------------------------------

class TestRieszRepresentationApplies:
    def test_compact_hausdorff_true(self):
        assert riesz_representation_applies(_sp("compact_hausdorff")).is_true

    def test_compact_t2_true(self):
        assert riesz_representation_applies(_sp("compact_t2")).is_true

    def test_compact_metrizable_true(self):
        assert riesz_representation_applies(_sp("compact_metrizable")).is_true

    def test_cantor_set_true(self):
        assert riesz_representation_applies(_sp("cantor_set")).is_true

    def test_closed_interval_true(self):
        assert riesz_representation_applies(_sp("closed_interval")).is_true

    def test_sphere_true(self):
        assert riesz_representation_applies(_sp("sphere")).is_true

    def test_locally_compact_hausdorff_true(self):
        assert riesz_representation_applies(_sp("locally_compact_hausdorff")).is_true

    def test_real_line_true(self):
        assert riesz_representation_applies(_sp("real_line")).is_true

    def test_euclidean_true(self):
        assert riesz_representation_applies(_sp("euclidean")).is_true

    def test_not_hausdorff_false(self):
        assert riesz_representation_applies(_sp("not_hausdorff")).is_false

    def test_non_hausdorff_false(self):
        assert riesz_representation_applies(_sp("non_hausdorff")).is_false

    def test_infinite_dim_banach_false(self):
        assert riesz_representation_applies(_sp("infinite_dimensional_banach")).is_false

    def test_hilbert_space_infinite_false(self):
        assert riesz_representation_applies(_sp("hilbert_space_infinite_dim")).is_false

    def test_unknown_empty(self):
        assert riesz_representation_applies(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(riesz_representation_applies(_sp("compact_hausdorff")), Result)

    def test_true_has_justification(self):
        assert riesz_representation_applies(_sp("compact_hausdorff")).justification

    def test_false_has_justification(self):
        assert riesz_representation_applies(_sp("not_hausdorff")).justification


# ---------------------------------------------------------------------------
# has_haar_measure
# ---------------------------------------------------------------------------

class TestHasHaarMeasure:
    def test_explicit_haar_true(self):
        assert has_haar_measure(_sp("haar_measure")).is_true

    def test_topological_group_true(self):
        assert has_haar_measure(_sp("topological_group")).is_true

    def test_locally_compact_group_true(self):
        assert has_haar_measure(_sp("locally_compact_group")).is_true

    def test_compact_group_true(self):
        assert has_haar_measure(_sp("compact_group")).is_true

    def test_abelian_group_true(self):
        assert has_haar_measure(_sp("abelian_group")).is_true

    def test_lie_group_true(self):
        assert has_haar_measure(_sp("lie_group")).is_true

    def test_real_line_true(self):
        assert has_haar_measure(_sp("real_line")).is_true

    def test_torus_true(self):
        assert has_haar_measure(_sp("torus")).is_true

    def test_circle_true(self):
        assert has_haar_measure(_sp("circle")).is_true

    def test_p_adic_integers_true(self):
        assert has_haar_measure(_sp("p_adic_integers")).is_true

    def test_discrete_group_true(self):
        assert has_haar_measure(_sp("discrete_group")).is_true

    def test_discrete_true(self):
        assert has_haar_measure(_sp("discrete")).is_true

    def test_countable_discrete_true(self):
        assert has_haar_measure(_sp("countable_discrete")).is_true

    def test_infinite_dim_banach_false(self):
        assert has_haar_measure(_sp("infinite_dimensional_banach")).is_false

    def test_hilbert_space_infinite_false(self):
        assert has_haar_measure(_sp("hilbert_space_infinite_dim")).is_false

    def test_frechet_non_lc_false(self):
        assert has_haar_measure(_sp("frechet_space_non_lc")).is_false

    def test_unknown_empty(self):
        assert has_haar_measure(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(has_haar_measure(_sp("topological_group")), Result)

    def test_true_has_justification(self):
        assert has_haar_measure(_sp("topological_group")).justification

    def test_false_has_justification(self):
        assert has_haar_measure(_sp("infinite_dimensional_banach")).justification


# ---------------------------------------------------------------------------
# measure_support_is_compact
# ---------------------------------------------------------------------------

class TestMeasureSupportIsCompact:
    def test_dirac_measure_true(self):
        assert measure_support_is_compact(_sp("dirac_measure")).is_true

    def test_dirac_tag_true(self):
        assert measure_support_is_compact(_sp("dirac")).is_true

    def test_point_mass_true(self):
        assert measure_support_is_compact(_sp("point_mass")).is_true

    def test_compact_support_tag_true(self):
        assert measure_support_is_compact(_sp("compact_support")).is_true

    def test_compactly_supported_true(self):
        assert measure_support_is_compact(_sp("compactly_supported")).is_true

    def test_compact_hausdorff_true(self):
        assert measure_support_is_compact(_sp("compact_hausdorff")).is_true

    def test_compact_metrizable_true(self):
        assert measure_support_is_compact(_sp("compact_metrizable")).is_true

    def test_cantor_set_true(self):
        assert measure_support_is_compact(_sp("cantor_set")).is_true

    def test_cantor_measure_true(self):
        assert measure_support_is_compact(_sp("cantor_measure")).is_true

    def test_measure_on_compact_true(self):
        assert measure_support_is_compact(_sp("measure_on_compact")).is_true

    def test_lebesgue_measure_false(self):
        assert measure_support_is_compact(_sp("lebesgue_measure")).is_false

    def test_gaussian_measure_false(self):
        assert measure_support_is_compact(_sp("gaussian_measure")).is_false

    def test_counting_measure_false(self):
        assert measure_support_is_compact(_sp("counting_measure")).is_false

    def test_haar_measure_lc_false(self):
        assert measure_support_is_compact(_sp("haar_measure_lc")).is_false

    def test_unknown_empty(self):
        assert measure_support_is_compact(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(measure_support_is_compact(_sp("dirac_measure")), Result)

    def test_true_has_justification(self):
        assert measure_support_is_compact(_sp("dirac_measure")).justification

    def test_false_has_justification(self):
        assert measure_support_is_compact(_sp("lebesgue_measure")).justification


# ---------------------------------------------------------------------------
# classify_borel_measure
# ---------------------------------------------------------------------------

class TestClassifyBorelMeasure:
    def test_returns_dict(self):
        assert isinstance(classify_borel_measure(_sp("lebesgue_measure")), dict)

    def test_radon_regular_class(self):
        sp = _sp("lebesgue_measure")
        result = classify_borel_measure(sp)
        assert result["measure_class"] == "radon_regular"

    def test_radon_regular_for_dirac(self):
        sp = _sp("dirac_measure")
        result = classify_borel_measure(sp)
        assert result["measure_class"] == "radon_regular"

    def test_not_radon_for_uncountable_counting(self):
        sp = _sp("counting_measure_uncountable")
        result = classify_borel_measure(sp)
        assert result["measure_class"] == "not_radon"

    def test_has_all_required_keys(self):
        sp = _sp("lebesgue_measure")
        result = classify_borel_measure(sp)
        for key in ("measure_class", "is_radon", "is_regular", "riesz_applicable",
                    "has_haar", "support_compact", "key_properties",
                    "representation", "tags"):
            assert key in result

    def test_key_properties_is_list(self):
        sp = _sp("lebesgue_measure")
        assert isinstance(classify_borel_measure(sp)["key_properties"], list)

    def test_radon_in_properties_for_lebesgue(self):
        sp = _sp("lebesgue_measure")
        result = classify_borel_measure(sp)
        assert "radon" in result["key_properties"]

    def test_regular_in_properties_for_lebesgue(self):
        sp = _sp("lebesgue_measure")
        result = classify_borel_measure(sp)
        assert "regular" in result["key_properties"]

    def test_atomic_in_properties_for_dirac(self):
        sp = _sp("dirac_measure")
        result = classify_borel_measure(sp)
        assert "atomic" in result["key_properties"]

    def test_compact_support_in_properties_for_dirac(self):
        sp = _sp("dirac_measure")
        result = classify_borel_measure(sp)
        assert "compact_support" in result["key_properties"]

    def test_not_radon_in_properties_for_uncountable(self):
        sp = _sp("counting_measure_uncountable")
        result = classify_borel_measure(sp)
        assert "not_radon" in result["key_properties"]

    def test_sub_results_are_result_instances(self):
        sp = _sp("lebesgue_measure")
        result = classify_borel_measure(sp)
        for key in ("is_radon", "is_regular", "riesz_applicable",
                    "has_haar", "support_compact"):
            assert isinstance(result[key], Result)

    def test_tags_sorted(self):
        sp = _sp("lebesgue_measure", "radon_measure", "regular_measure")
        result = classify_borel_measure(sp)
        assert result["tags"] == sorted(result["tags"])


# ---------------------------------------------------------------------------
# borel_measure_profile
# ---------------------------------------------------------------------------

class TestBorelMeasureProfile:
    def test_returns_dict(self):
        assert isinstance(borel_measure_profile(_sp("lebesgue_measure")), dict)

    def test_has_classification_key(self):
        assert "classification" in borel_measure_profile(_sp("dirac_measure"))

    def test_has_named_profiles_key(self):
        assert "named_profiles" in borel_measure_profile(_sp("dirac_measure"))

    def test_has_layer_summary_key(self):
        assert "layer_summary" in borel_measure_profile(_sp("dirac_measure"))

    def test_named_profiles_is_tuple(self):
        assert isinstance(borel_measure_profile(_sp("lebesgue_measure"))["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        assert isinstance(borel_measure_profile(_sp("lebesgue_measure"))["layer_summary"], dict)

    def test_classification_is_dict(self):
        assert isinstance(borel_measure_profile(_sp("lebesgue_measure"))["classification"], dict)


# ---------------------------------------------------------------------------
# __all__ and module structure
# ---------------------------------------------------------------------------

class TestModuleStructure:
    def test_all_is_defined(self):
        import pytop.borel_measures as m
        assert hasattr(m, "__all__")

    def test_all_is_list(self):
        import pytop.borel_measures as m
        assert isinstance(m.__all__, list)

    def test_profile_class_in_all(self):
        import pytop.borel_measures as m
        assert "BorelMeasureProfile" in m.__all__

    def test_classify_in_all(self):
        import pytop.borel_measures as m
        assert "classify_borel_measure" in m.__all__

    def test_all_names_importable(self):
        import pytop.borel_measures as m
        for name in m.__all__:
            assert hasattr(m, name), f"{name} in __all__ but not defined"

    def test_module_importable_from_pytop(self):
        from pytop import borel_measure_profile as _  # noqa: F401

    def test_profile_class_importable_from_pytop(self):
        from pytop import BorelMeasureProfile as _  # noqa: F401
