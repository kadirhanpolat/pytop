"""Tests for solenoid_profiles.py (v0.5.9)."""

import pytest

from pytop.solenoid_profiles import (
    COMPACT_FACTOR_TAGS,
    CONNECTED_FACTOR_TAGS,
    HOMOGENEOUS_TAGS,
    INDECOMPOSABLE_TAGS,
    INVERSE_LIMIT_TAGS,
    LOCALLY_DISCONNECTED_TAGS,
    METRIZABLE_INVERSE_LIMIT_TAGS,
    NOT_SOLENOID_TAGS,
    SOLENOID_TAGS,
    SolenoidProfile,
    classify_solenoid,
    get_named_solenoid_profiles,
    inverse_limit_is_compact,
    inverse_limit_is_connected,
    is_indecomposable_continuum,
    is_solenoid,
    solenoid_chapter_index,
    solenoid_is_homogeneous,
    solenoid_layer_summary,
    solenoid_profile,
    solenoid_type_index,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_solenoid_tags_contains_solenoid(self):
        assert "solenoid" in SOLENOID_TAGS

    def test_solenoid_tags_contains_dyadic_solenoid(self):
        assert "dyadic_solenoid" in SOLENOID_TAGS

    def test_solenoid_tags_contains_p_adic_solenoid(self):
        assert "p_adic_solenoid" in SOLENOID_TAGS

    def test_solenoid_tags_contains_generalized_solenoid(self):
        assert "generalized_solenoid" in SOLENOID_TAGS

    def test_inverse_limit_tags_contains_solenoid(self):
        assert "solenoid" in INVERSE_LIMIT_TAGS

    def test_inverse_limit_tags_contains_profinite(self):
        assert "profinite" in INVERSE_LIMIT_TAGS

    def test_inverse_limit_tags_contains_cantor_set(self):
        assert "cantor_set" in INVERSE_LIMIT_TAGS

    def test_inverse_limit_tags_contains_hilbert_cube(self):
        assert "hilbert_cube" in INVERSE_LIMIT_TAGS

    def test_indecomposable_tags_contains_solenoid(self):
        assert "solenoid" in INDECOMPOSABLE_TAGS

    def test_indecomposable_tags_contains_pseudo_arc(self):
        assert "pseudo_arc" in INDECOMPOSABLE_TAGS

    def test_compact_factor_tags_contains_solenoid(self):
        assert "solenoid" in COMPACT_FACTOR_TAGS

    def test_compact_factor_tags_contains_profinite(self):
        assert "profinite" in COMPACT_FACTOR_TAGS

    def test_compact_factor_tags_contains_hilbert_cube(self):
        assert "hilbert_cube" in COMPACT_FACTOR_TAGS

    def test_connected_factor_tags_contains_solenoid(self):
        assert "solenoid" in CONNECTED_FACTOR_TAGS

    def test_connected_factor_tags_contains_hilbert_cube(self):
        assert "hilbert_cube" in CONNECTED_FACTOR_TAGS

    def test_homogeneous_tags_contains_solenoid(self):
        assert "solenoid" in HOMOGENEOUS_TAGS

    def test_homogeneous_tags_contains_topological_group(self):
        assert "topological_group" in HOMOGENEOUS_TAGS

    def test_homogeneous_tags_contains_cantor_space(self):
        assert "cantor_space" in HOMOGENEOUS_TAGS

    def test_not_solenoid_contains_locally_connected(self):
        assert "locally_connected" in NOT_SOLENOID_TAGS

    def test_not_solenoid_contains_manifold(self):
        assert "manifold" in NOT_SOLENOID_TAGS

    def test_not_solenoid_contains_discrete(self):
        assert "discrete" in NOT_SOLENOID_TAGS

    def test_locally_disconnected_contains_solenoid(self):
        assert "solenoid" in LOCALLY_DISCONNECTED_TAGS

    def test_locally_disconnected_contains_cantor_set(self):
        assert "cantor_set" in LOCALLY_DISCONNECTED_TAGS

    def test_metrizable_lim_contains_solenoid(self):
        assert "solenoid" in METRIZABLE_INVERSE_LIMIT_TAGS

    def test_metrizable_lim_contains_hilbert_cube(self):
        assert "hilbert_cube" in METRIZABLE_INVERSE_LIMIT_TAGS


# ---------------------------------------------------------------------------
# SolenoidProfile dataclass
# ---------------------------------------------------------------------------

class TestSolenoidProfileDataclass:
    def test_profile_is_frozen(self):
        p = SolenoidProfile(
            key="test",
            display_name="Test",
            space_type="test_type",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=True,
            is_homogeneous=True,
            presentation_layer="main_text",
            focus="test focus",
            chapter_targets=("6",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = SolenoidProfile(
            key="dyadic",
            display_name="Dyadic Solenoid",
            space_type="solenoid_group",
            is_compact=True,
            is_connected=True,
            is_metrizable=True,
            is_indecomposable=True,
            is_homogeneous=True,
            presentation_layer="main_text",
            focus="focus",
            chapter_targets=("6", "28"),
        )
        assert p.key == "dyadic"
        assert p.is_compact is True
        assert p.is_indecomposable is True
        assert p.is_homogeneous is True
        assert "6" in p.chapter_targets


# ---------------------------------------------------------------------------
# Named profiles registry
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        profiles = get_named_solenoid_profiles()
        assert isinstance(profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(get_named_solenoid_profiles()) >= 5

    def test_dyadic_solenoid_present(self):
        keys = {p.key for p in get_named_solenoid_profiles()}
        assert "dyadic_solenoid" in keys

    def test_p_adic_solenoid_present(self):
        keys = {p.key for p in get_named_solenoid_profiles()}
        assert "p_adic_solenoid" in keys

    def test_p_adic_integers_lim_present(self):
        keys = {p.key for p in get_named_solenoid_profiles()}
        assert "p_adic_integers_lim" in keys

    def test_hilbert_cube_lim_present(self):
        keys = {p.key for p in get_named_solenoid_profiles()}
        assert "hilbert_cube_lim" in keys

    def test_cantor_set_lim_present(self):
        keys = {p.key for p in get_named_solenoid_profiles()}
        assert "cantor_set_lim" in keys

    def test_dyadic_solenoid_is_compact(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["dyadic_solenoid"].is_compact is True

    def test_dyadic_solenoid_is_connected(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["dyadic_solenoid"].is_connected is True

    def test_dyadic_solenoid_is_indecomposable(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["dyadic_solenoid"].is_indecomposable is True

    def test_dyadic_solenoid_is_homogeneous(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["dyadic_solenoid"].is_homogeneous is True

    def test_p_adic_solenoid_is_indecomposable(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["p_adic_solenoid"].is_indecomposable is True

    def test_p_adic_integers_not_connected(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["p_adic_integers_lim"].is_connected is False

    def test_cantor_set_lim_not_connected(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["cantor_set_lim"].is_connected is False

    def test_hilbert_cube_not_homogeneous(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["hilbert_cube_lim"].is_homogeneous is False

    def test_hilbert_cube_not_indecomposable(self):
        profiles = {p.key: p for p in get_named_solenoid_profiles()}
        assert profiles["hilbert_cube_lim"].is_indecomposable is False

    def test_all_keys_unique(self):
        keys = [p.key for p in get_named_solenoid_profiles()]
        assert len(keys) == len(set(keys))

    def test_all_profiles_have_chapter_targets(self):
        for p in get_named_solenoid_profiles():
            assert len(p.chapter_targets) >= 1

    def test_all_profiles_have_focus(self):
        for p in get_named_solenoid_profiles():
            assert len(p.focus) > 20

    def test_all_profiles_have_display_name(self):
        for p in get_named_solenoid_profiles():
            assert len(p.display_name) > 3


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(solenoid_layer_summary(), dict)

    def test_layer_summary_has_main_text(self):
        assert "main_text" in solenoid_layer_summary()

    def test_layer_summary_values_positive(self):
        assert all(v > 0 for v in solenoid_layer_summary().values())

    def test_chapter_index_returns_dict(self):
        assert isinstance(solenoid_chapter_index(), dict)

    def test_chapter_index_chapter_6_exists(self):
        assert "6" in solenoid_chapter_index()

    def test_chapter_index_chapter_6_has_dyadic(self):
        assert "dyadic_solenoid" in solenoid_chapter_index()["6"]

    def test_chapter_index_values_are_tuples(self):
        for val in solenoid_chapter_index().values():
            assert isinstance(val, tuple)

    def test_type_index_returns_dict(self):
        assert isinstance(solenoid_type_index(), dict)

    def test_type_index_has_solenoid_group(self):
        assert "solenoid_group" in solenoid_type_index()

    def test_type_index_solenoid_group_has_dyadic(self):
        assert "dyadic_solenoid" in solenoid_type_index()["solenoid_group"]

    def test_type_index_values_are_tuples(self):
        for val in solenoid_type_index().values():
            assert isinstance(val, tuple)


# ---------------------------------------------------------------------------
# is_solenoid
# ---------------------------------------------------------------------------

class TestIsSolenoid:
    def test_solenoid_tag_true(self):
        sp = _sp("solenoid")
        assert is_solenoid(sp).is_true

    def test_dyadic_solenoid_tag_true(self):
        sp = _sp("dyadic_solenoid")
        assert is_solenoid(sp).is_true

    def test_p_adic_solenoid_tag_true(self):
        sp = _sp("p_adic_solenoid")
        assert is_solenoid(sp).is_true

    def test_generalized_solenoid_tag_true(self):
        sp = _sp("generalized_solenoid")
        assert is_solenoid(sp).is_true

    def test_solenoid_group_tag_true(self):
        sp = _sp("solenoid_group")
        assert is_solenoid(sp).is_true

    def test_inverse_limit_circles_true(self):
        sp = _sp("inverse_limit_circles")
        assert is_solenoid(sp).is_true

    def test_locally_connected_false(self):
        sp = _sp("locally_connected")
        assert is_solenoid(sp).is_false

    def test_locally_path_connected_false(self):
        sp = _sp("locally_path_connected")
        assert is_solenoid(sp).is_false

    def test_manifold_false(self):
        sp = _sp("manifold")
        assert is_solenoid(sp).is_false

    def test_disk_false(self):
        sp = _sp("disk")
        assert is_solenoid(sp).is_false

    def test_sphere_false(self):
        sp = _sp("sphere")
        assert is_solenoid(sp).is_false

    def test_discrete_false(self):
        sp = _sp("discrete")
        assert is_solenoid(sp).is_false

    def test_zero_dimensional_false(self):
        sp = _sp("zero_dimensional")
        assert is_solenoid(sp).is_false

    def test_unknown_empty(self):
        sp = _sp()
        assert is_solenoid(sp).is_unknown

    def test_unknown_compact_connected(self):
        sp = _sp("compact", "connected")
        assert is_solenoid(sp).is_unknown

    def test_returns_result(self):
        assert isinstance(is_solenoid(_sp("solenoid")), Result)

    def test_true_has_justification(self):
        r = is_solenoid(_sp("dyadic_solenoid"))
        assert r.justification

    def test_false_has_justification(self):
        r = is_solenoid(_sp("locally_connected"))
        assert r.justification


# ---------------------------------------------------------------------------
# inverse_limit_is_compact
# ---------------------------------------------------------------------------

class TestInverseLimitIsCompact:
    def test_solenoid_compact_true(self):
        sp = _sp("solenoid")
        assert inverse_limit_is_compact(sp).is_true

    def test_dyadic_solenoid_compact_true(self):
        sp = _sp("dyadic_solenoid")
        assert inverse_limit_is_compact(sp).is_true

    def test_p_adic_solenoid_compact_true(self):
        sp = _sp("p_adic_solenoid")
        assert inverse_limit_is_compact(sp).is_true

    def test_compact_factors_true(self):
        sp = _sp("compact_factors")
        assert inverse_limit_is_compact(sp).is_true

    def test_compact_metrizable_factors_true(self):
        sp = _sp("compact_metrizable_factors")
        assert inverse_limit_is_compact(sp).is_true

    def test_profinite_compact_true(self):
        sp = _sp("profinite")
        assert inverse_limit_is_compact(sp).is_true

    def test_cantor_set_compact_true(self):
        sp = _sp("cantor_set")
        assert inverse_limit_is_compact(sp).is_true

    def test_hilbert_cube_compact_true(self):
        sp = _sp("hilbert_cube")
        assert inverse_limit_is_compact(sp).is_true

    def test_compact_inverse_limit_true(self):
        sp = _sp("compact_inverse_limit")
        assert inverse_limit_is_compact(sp).is_true

    def test_non_compact_factors_false(self):
        sp = _sp("non_compact_factors")
        assert inverse_limit_is_compact(sp).is_false

    def test_real_line_factors_false(self):
        sp = _sp("real_line_factors")
        assert inverse_limit_is_compact(sp).is_false

    def test_open_interval_factors_false(self):
        sp = _sp("open_interval_factors")
        assert inverse_limit_is_compact(sp).is_false

    def test_unknown_empty(self):
        assert inverse_limit_is_compact(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(inverse_limit_is_compact(_sp("solenoid")), Result)


# ---------------------------------------------------------------------------
# inverse_limit_is_connected
# ---------------------------------------------------------------------------

class TestInverseLimitIsConnected:
    def test_solenoid_connected_true(self):
        sp = _sp("solenoid")
        assert inverse_limit_is_connected(sp).is_true

    def test_dyadic_solenoid_connected_true(self):
        sp = _sp("dyadic_solenoid")
        assert inverse_limit_is_connected(sp).is_true

    def test_p_adic_solenoid_connected_true(self):
        sp = _sp("p_adic_solenoid")
        assert inverse_limit_is_connected(sp).is_true

    def test_connected_factors_surjective_true(self):
        sp = _sp("connected_factors", "surjective_bonding_maps")
        assert inverse_limit_is_connected(sp).is_true

    def test_hilbert_cube_connected_true(self):
        sp = _sp("hilbert_cube", "connected_factors")
        assert inverse_limit_is_connected(sp).is_true

    def test_connected_inverse_limit_true(self):
        sp = _sp("connected_inverse_limit")
        assert inverse_limit_is_connected(sp).is_true

    def test_profinite_disconnected_false(self):
        sp = _sp("profinite")
        assert inverse_limit_is_connected(sp).is_false

    def test_cantor_set_disconnected_false(self):
        sp = _sp("cantor_set")
        assert inverse_limit_is_connected(sp).is_false

    def test_p_adic_integers_disconnected_false(self):
        sp = _sp("p_adic_integers")
        assert inverse_limit_is_connected(sp).is_false

    def test_totally_disconnected_false(self):
        sp = _sp("totally_disconnected")
        assert inverse_limit_is_connected(sp).is_false

    def test_discrete_factors_false(self):
        sp = _sp("discrete_factors")
        assert inverse_limit_is_connected(sp).is_false

    def test_disconnected_factors_false(self):
        sp = _sp("disconnected_factors")
        assert inverse_limit_is_connected(sp).is_false

    def test_unknown_empty(self):
        assert inverse_limit_is_connected(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(inverse_limit_is_connected(_sp("solenoid")), Result)

    def test_true_has_justification(self):
        r = inverse_limit_is_connected(_sp("solenoid"))
        assert r.justification

    def test_false_has_justification(self):
        r = inverse_limit_is_connected(_sp("profinite"))
        assert r.justification


# ---------------------------------------------------------------------------
# is_indecomposable_continuum
# ---------------------------------------------------------------------------

class TestIsIndecomposableContinuum:
    def test_solenoid_indecomposable_true(self):
        sp = _sp("solenoid")
        assert is_indecomposable_continuum(sp).is_true

    def test_dyadic_solenoid_true(self):
        sp = _sp("dyadic_solenoid")
        assert is_indecomposable_continuum(sp).is_true

    def test_p_adic_solenoid_true(self):
        sp = _sp("p_adic_solenoid")
        assert is_indecomposable_continuum(sp).is_true

    def test_generalized_solenoid_true(self):
        sp = _sp("generalized_solenoid")
        assert is_indecomposable_continuum(sp).is_true

    def test_indecomposable_tag_true(self):
        sp = _sp("indecomposable")
        assert is_indecomposable_continuum(sp).is_true

    def test_pseudo_arc_true(self):
        sp = _sp("pseudo_arc")
        assert is_indecomposable_continuum(sp).is_true

    def test_locally_connected_false(self):
        sp = _sp("locally_connected")
        assert is_indecomposable_continuum(sp).is_false

    def test_locally_path_connected_false(self):
        sp = _sp("locally_path_connected")
        assert is_indecomposable_continuum(sp).is_false

    def test_arc_false(self):
        sp = _sp("arc")
        assert is_indecomposable_continuum(sp).is_false

    def test_interval_false(self):
        sp = _sp("interval")
        assert is_indecomposable_continuum(sp).is_false

    def test_sphere_false(self):
        sp = _sp("sphere")
        assert is_indecomposable_continuum(sp).is_false

    def test_torus_false(self):
        sp = _sp("torus")
        assert is_indecomposable_continuum(sp).is_false

    def test_manifold_false(self):
        sp = _sp("manifold")
        assert is_indecomposable_continuum(sp).is_false

    def test_hilbert_cube_false(self):
        sp = _sp("hilbert_cube")
        assert is_indecomposable_continuum(sp).is_false

    def test_cantor_set_false(self):
        sp = _sp("cantor_set")
        assert is_indecomposable_continuum(sp).is_false

    def test_discrete_false(self):
        sp = _sp("discrete")
        assert is_indecomposable_continuum(sp).is_false

    def test_profinite_false(self):
        sp = _sp("profinite")
        assert is_indecomposable_continuum(sp).is_false

    def test_zero_dimensional_false(self):
        sp = _sp("zero_dimensional")
        assert is_indecomposable_continuum(sp).is_false

    def test_unknown_empty(self):
        assert is_indecomposable_continuum(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_indecomposable_continuum(_sp("solenoid")), Result)

    def test_true_has_justification(self):
        assert is_indecomposable_continuum(_sp("solenoid")).justification

    def test_false_has_justification(self):
        assert is_indecomposable_continuum(_sp("locally_connected")).justification


# ---------------------------------------------------------------------------
# solenoid_is_homogeneous
# ---------------------------------------------------------------------------

class TestSolenoidIsHomogeneous:
    def test_solenoid_homogeneous_true(self):
        sp = _sp("solenoid")
        assert solenoid_is_homogeneous(sp).is_true

    def test_dyadic_solenoid_homogeneous_true(self):
        sp = _sp("dyadic_solenoid")
        assert solenoid_is_homogeneous(sp).is_true

    def test_topological_group_homogeneous_true(self):
        sp = _sp("topological_group")
        assert solenoid_is_homogeneous(sp).is_true

    def test_homogeneous_tag_true(self):
        sp = _sp("homogeneous")
        assert solenoid_is_homogeneous(sp).is_true

    def test_cantor_space_homogeneous_true(self):
        sp = _sp("cantor_space")
        assert solenoid_is_homogeneous(sp).is_true

    def test_cantor_set_homogeneous_true(self):
        sp = _sp("cantor_set")
        assert solenoid_is_homogeneous(sp).is_true

    def test_circle_homogeneous_true(self):
        sp = _sp("circle")
        assert solenoid_is_homogeneous(sp).is_true

    def test_torus_homogeneous_true(self):
        sp = _sp("torus")
        assert solenoid_is_homogeneous(sp).is_true

    def test_hilbert_cube_not_homogeneous_false(self):
        sp = _sp("hilbert_cube")
        assert solenoid_is_homogeneous(sp).is_false

    def test_arc_not_homogeneous_false(self):
        sp = _sp("arc")
        assert solenoid_is_homogeneous(sp).is_false

    def test_interval_not_homogeneous_false(self):
        sp = _sp("interval")
        assert solenoid_is_homogeneous(sp).is_false

    def test_closed_interval_not_homogeneous_false(self):
        sp = _sp("closed_interval")
        assert solenoid_is_homogeneous(sp).is_false

    def test_warsaw_circle_not_homogeneous_false(self):
        sp = _sp("warsaw_circle")
        assert solenoid_is_homogeneous(sp).is_false

    def test_not_homogeneous_tag_false(self):
        sp = _sp("not_homogeneous")
        assert solenoid_is_homogeneous(sp).is_false

    def test_unknown_empty(self):
        assert solenoid_is_homogeneous(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(solenoid_is_homogeneous(_sp("solenoid")), Result)

    def test_true_has_justification(self):
        assert solenoid_is_homogeneous(_sp("solenoid")).justification

    def test_false_has_justification(self):
        assert solenoid_is_homogeneous(_sp("hilbert_cube")).justification


# ---------------------------------------------------------------------------
# classify_solenoid
# ---------------------------------------------------------------------------

class TestClassifySolenoid:
    def test_returns_dict(self):
        sp = _sp("solenoid")
        assert isinstance(classify_solenoid(sp), dict)

    def test_solenoid_type_for_solenoid(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert result["solenoid_type"] == "solenoid"

    def test_dyadic_solenoid_type(self):
        sp = _sp("dyadic_solenoid")
        result = classify_solenoid(sp)
        assert result["solenoid_type"] == "solenoid"

    def test_profinite_inverse_limit_type(self):
        sp = _sp("profinite", "cantor_set")
        result = classify_solenoid(sp)
        assert result["solenoid_type"] == "profinite_inverse_limit"

    def test_locally_connected_not_solenoid_type(self):
        sp = _sp("locally_connected")
        result = classify_solenoid(sp)
        assert result["solenoid_type"] == "not_solenoid"

    def test_has_all_required_keys(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        for key in ("solenoid_type", "is_solenoid", "is_compact", "is_connected",
                    "is_indecomposable", "is_homogeneous", "key_properties",
                    "representation", "tags"):
            assert key in result

    def test_key_properties_is_list(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert isinstance(result["key_properties"], list)

    def test_solenoid_in_properties(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert "solenoid" in result["key_properties"]

    def test_compact_in_properties_for_solenoid(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert "compact" in result["key_properties"]

    def test_connected_in_properties_for_solenoid(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert "connected" in result["key_properties"]

    def test_indecomposable_in_properties_for_solenoid(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert "indecomposable" in result["key_properties"]

    def test_homogeneous_in_properties_for_solenoid(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        assert "homogeneous" in result["key_properties"]

    def test_sub_results_are_result_instances(self):
        sp = _sp("solenoid")
        result = classify_solenoid(sp)
        for key in ("is_solenoid", "is_compact", "is_connected",
                    "is_indecomposable", "is_homogeneous"):
            assert isinstance(result[key], Result)

    def test_tags_sorted(self):
        sp = _sp("solenoid", "compact", "connected")
        result = classify_solenoid(sp)
        assert result["tags"] == sorted(result["tags"])


# ---------------------------------------------------------------------------
# solenoid_profile
# ---------------------------------------------------------------------------

class TestSolenoidProfile:
    def test_returns_dict(self):
        sp = _sp("solenoid")
        assert isinstance(solenoid_profile(sp), dict)

    def test_has_classification_key(self):
        sp = _sp("dyadic_solenoid")
        assert "classification" in solenoid_profile(sp)

    def test_has_named_profiles_key(self):
        sp = _sp("dyadic_solenoid")
        assert "named_profiles" in solenoid_profile(sp)

    def test_has_layer_summary_key(self):
        sp = _sp("dyadic_solenoid")
        assert "layer_summary" in solenoid_profile(sp)

    def test_named_profiles_is_tuple(self):
        sp = _sp("solenoid")
        assert isinstance(solenoid_profile(sp)["named_profiles"], tuple)

    def test_layer_summary_is_dict(self):
        sp = _sp("solenoid")
        assert isinstance(solenoid_profile(sp)["layer_summary"], dict)

    def test_classification_is_dict(self):
        sp = _sp("solenoid")
        assert isinstance(solenoid_profile(sp)["classification"], dict)


# ---------------------------------------------------------------------------
# __all__ and module structure
# ---------------------------------------------------------------------------

class TestModuleStructure:
    def test_all_is_defined(self):
        import pytop.solenoid_profiles as m
        assert hasattr(m, "__all__")

    def test_all_is_list(self):
        import pytop.solenoid_profiles as m
        assert isinstance(m.__all__, list)

    def test_profile_class_in_all(self):
        import pytop.solenoid_profiles as m
        assert "SolenoidProfile" in m.__all__

    def test_classify_in_all(self):
        import pytop.solenoid_profiles as m
        assert "classify_solenoid" in m.__all__

    def test_all_names_importable(self):
        import pytop.solenoid_profiles as m
        for name in m.__all__:
            assert hasattr(m, name), f"{name} in __all__ but not defined"

    def test_module_importable_from_pytop(self):
        from pytop import solenoid_profile as _  # noqa: F401

    def test_solenoid_profile_class_importable_from_pytop(self):
        from pytop import SolenoidProfile as _  # noqa: F401
