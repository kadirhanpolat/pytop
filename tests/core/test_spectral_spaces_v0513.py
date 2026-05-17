"""Tests for spectral_spaces.py (v0.5.13)."""

import pytest

from pytop.spectral_spaces import (
    GENERIC_POINT_TAGS,
    NOT_SOBER_TAGS,
    NOT_STONE_TAGS,
    NOT_T1_TAGS,
    SOBER_POSITIVE_TAGS,
    SPATIAL_FRAME_TAGS,
    SPECTRAL_TAGS,
    STONE_SPACE_TAGS,
    SpectralSpaceProfile,
    classify_spectral_space,
    frame_is_spatial,
    get_named_spectral_space_profiles,
    is_sober,
    is_spectral,
    is_stone_space,
    spectral_space_chapter_index,
    spectral_space_layer_summary,
    spectral_space_profile,
    spectral_space_type_index,
    stone_duality_applies,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_sober_tags_contains_sober(self):
        assert "sober" in SOBER_POSITIVE_TAGS

    def test_sober_tags_contains_hausdorff(self):
        assert "hausdorff" in SOBER_POSITIVE_TAGS

    def test_sober_tags_contains_stone_space(self):
        assert "stone_space" in SOBER_POSITIVE_TAGS

    def test_sober_tags_contains_spec_ring(self):
        assert "spec_ring" in SOBER_POSITIVE_TAGS

    def test_sober_tags_contains_sierpinski(self):
        assert "sierpinski_space" in SOBER_POSITIVE_TAGS

    def test_spectral_tags_contains_spectral_space(self):
        assert "spectral_space" in SPECTRAL_TAGS

    def test_spectral_tags_contains_spec_ring(self):
        assert "spec_ring" in SPECTRAL_TAGS

    def test_spectral_tags_contains_stone_space(self):
        assert "stone_space" in SPECTRAL_TAGS

    def test_spectral_tags_contains_zariski(self):
        assert "zariski_spectrum" in SPECTRAL_TAGS

    def test_stone_tags_contains_stone_space(self):
        assert "stone_space" in STONE_SPACE_TAGS

    def test_stone_tags_contains_profinite(self):
        assert "profinite" in STONE_SPACE_TAGS

    def test_stone_tags_contains_boolean_space(self):
        assert "boolean_space" in STONE_SPACE_TAGS

    def test_stone_tags_contains_cantor_space(self):
        assert "cantor_space" in STONE_SPACE_TAGS

    def test_stone_tags_contains_p_adic(self):
        assert "p_adic_integers" in STONE_SPACE_TAGS

    def test_spatial_frame_contains_sober(self):
        assert "sober" in SPATIAL_FRAME_TAGS

    def test_spatial_frame_contains_stone_space(self):
        assert "stone_space" in SPATIAL_FRAME_TAGS

    def test_generic_point_contains_generic_point(self):
        assert "generic_point" in GENERIC_POINT_TAGS

    def test_generic_point_contains_sierpinski(self):
        assert "sierpinski_space" in GENERIC_POINT_TAGS

    def test_not_sober_contains_not_sober(self):
        assert "not_sober" in NOT_SOBER_TAGS

    def test_not_sober_contains_alexandrov_no_maximum(self):
        assert "alexandrov_no_maximum" in NOT_SOBER_TAGS

    def test_not_t1_contains_spec_ring(self):
        assert "spec_ring" in NOT_T1_TAGS

    def test_not_t1_contains_sierpinski(self):
        assert "sierpinski_space" in NOT_T1_TAGS

    def test_not_stone_contains_sierpinski(self):
        assert "sierpinski_space" in NOT_STONE_TAGS

    def test_not_stone_contains_spec_ring(self):
        assert "spec_ring" in NOT_STONE_TAGS

    def test_tag_sets_are_sets(self):
        for s in [SOBER_POSITIVE_TAGS, SPECTRAL_TAGS, STONE_SPACE_TAGS,
                  SPATIAL_FRAME_TAGS, GENERIC_POINT_TAGS,
                  NOT_SOBER_TAGS, NOT_T1_TAGS, NOT_STONE_TAGS]:
            assert isinstance(s, set)

    def test_stone_space_not_in_not_sober(self):
        assert "stone_space" not in NOT_SOBER_TAGS

    def test_hausdorff_not_in_not_stone(self):
        # hausdorff is needed for stone, not a negative tag
        assert "hausdorff" not in NOT_STONE_TAGS


# ---------------------------------------------------------------------------
# SpectralSpaceProfile dataclass
# ---------------------------------------------------------------------------

class TestSpectralSpaceProfileDataclass:
    def test_profile_is_frozen(self):
        p = SpectralSpaceProfile(
            key="t", display_name="T", space_type="sober_t0",
            is_sober=True, is_spectral=True, is_stone_space=False,
            is_t0=True, is_t1=False, has_generic_point=True,
            presentation_layer="main_text", focus="f",
            chapter_targets=("8",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields_accessible(self):
        p = SpectralSpaceProfile(
            key="k", display_name="D", space_type="stone",
            is_sober=True, is_spectral=True, is_stone_space=True,
            is_t0=True, is_t1=True, has_generic_point=False,
            presentation_layer="main_text", focus="f",
            chapter_targets=("8", "26"),
        )
        assert p.key == "k"
        assert p.is_stone_space is True
        assert p.is_t1 is True
        assert p.chapter_targets == ("8", "26")

    def test_profile_equality(self):
        kwargs = dict(
            key="a", display_name="A", space_type="spectral",
            is_sober=True, is_spectral=True, is_stone_space=False,
            is_t0=True, is_t1=False, has_generic_point=True,
            presentation_layer="main_text", focus="f",
            chapter_targets=("8",),
        )
        assert SpectralSpaceProfile(**kwargs) == SpectralSpaceProfile(**kwargs)


# ---------------------------------------------------------------------------
# Named profiles
# ---------------------------------------------------------------------------

class TestNamedSpectralSpaceProfiles:
    def setup_method(self):
        self.profiles = get_named_spectral_space_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_at_least_five_profiles(self):
        assert len(self.profiles) >= 5

    def test_all_are_spectral_profiles(self):
        for p in self.profiles:
            assert isinstance(p, SpectralSpaceProfile)

    def test_keys_unique(self):
        keys = [p.key for p in self.profiles]
        assert len(keys) == len(set(keys))

    def test_sierpinski_exists(self):
        assert "sierpinski_space" in {p.key for p in self.profiles}

    def test_spec_integral_domain_exists(self):
        assert "spec_integral_domain" in {p.key for p in self.profiles}

    def test_stone_space_exists(self):
        assert "stone_space" in {p.key for p in self.profiles}

    def test_zariski_affine_line_exists(self):
        assert "zariski_affine_line" in {p.key for p in self.profiles}

    def test_alexandrov_dcpo_exists(self):
        assert "alexandrov_dcpo" in {p.key for p in self.profiles}

    def test_alexandrov_no_max_exists(self):
        assert "alexandrov_no_max" in {p.key for p in self.profiles}

    def test_sierpinski_is_sober(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_space")
        assert p.is_sober is True

    def test_sierpinski_is_spectral(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_space")
        assert p.is_spectral is True

    def test_sierpinski_not_stone(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_space")
        assert p.is_stone_space is False

    def test_sierpinski_t0_not_t1(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_space")
        assert p.is_t0 is True
        assert p.is_t1 is False

    def test_sierpinski_has_generic_point(self):
        p = next(x for x in self.profiles if x.key == "sierpinski_space")
        assert p.has_generic_point is True

    def test_spec_domain_is_sober(self):
        p = next(x for x in self.profiles if x.key == "spec_integral_domain")
        assert p.is_sober is True

    def test_spec_domain_is_spectral(self):
        p = next(x for x in self.profiles if x.key == "spec_integral_domain")
        assert p.is_spectral is True

    def test_spec_domain_not_t1(self):
        p = next(x for x in self.profiles if x.key == "spec_integral_domain")
        assert p.is_t1 is False

    def test_spec_domain_has_generic_point(self):
        p = next(x for x in self.profiles if x.key == "spec_integral_domain")
        assert p.has_generic_point is True

    def test_stone_is_sober(self):
        p = next(x for x in self.profiles if x.key == "stone_space")
        assert p.is_sober is True

    def test_stone_is_spectral(self):
        p = next(x for x in self.profiles if x.key == "stone_space")
        assert p.is_spectral is True

    def test_stone_is_stone(self):
        p = next(x for x in self.profiles if x.key == "stone_space")
        assert p.is_stone_space is True

    def test_stone_is_t1(self):
        p = next(x for x in self.profiles if x.key == "stone_space")
        assert p.is_t1 is True

    def test_stone_no_generic_point(self):
        p = next(x for x in self.profiles if x.key == "stone_space")
        assert p.has_generic_point is False

    def test_zariski_not_t1(self):
        p = next(x for x in self.profiles if x.key == "zariski_affine_line")
        assert p.is_t1 is False

    def test_zariski_is_spectral(self):
        p = next(x for x in self.profiles if x.key == "zariski_affine_line")
        assert p.is_spectral is True

    def test_alexandrov_dcpo_sober(self):
        p = next(x for x in self.profiles if x.key == "alexandrov_dcpo")
        assert p.is_sober is True

    def test_alexandrov_no_max_not_sober(self):
        p = next(x for x in self.profiles if x.key == "alexandrov_no_max")
        assert p.is_sober is False

    def test_alexandrov_no_max_not_spectral(self):
        p = next(x for x in self.profiles if x.key == "alexandrov_no_max")
        assert p.is_spectral is False

    def test_alexandrov_no_max_t0(self):
        p = next(x for x in self.profiles if x.key == "alexandrov_no_max")
        assert p.is_t0 is True

    def test_alexandrov_no_max_no_generic_point(self):
        p = next(x for x in self.profiles if x.key == "alexandrov_no_max")
        assert p.has_generic_point is False

    def test_sober_implies_t0_in_profiles(self):
        for p in self.profiles:
            if p.is_sober:
                assert p.is_t0

    def test_stone_implies_spectral_in_profiles(self):
        for p in self.profiles:
            if p.is_stone_space:
                assert p.is_spectral

    def test_spectral_implies_sober_in_profiles(self):
        for p in self.profiles:
            if p.is_spectral:
                assert p.is_sober

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


# ---------------------------------------------------------------------------
# Index functions
# ---------------------------------------------------------------------------

class TestIndexFunctions:
    def test_layer_summary_returns_dict(self):
        assert isinstance(spectral_space_layer_summary(), dict)

    def test_layer_summary_sum_equals_profile_count(self):
        total = sum(spectral_space_layer_summary().values())
        assert total == len(get_named_spectral_space_profiles())

    def test_layer_summary_has_main_text(self):
        assert "main_text" in spectral_space_layer_summary()

    def test_chapter_index_returns_dict(self):
        assert isinstance(spectral_space_chapter_index(), dict)

    def test_chapter_index_values_are_tuples(self):
        for v in spectral_space_chapter_index().values():
            assert isinstance(v, tuple)

    def test_chapter_index_contains_chapter_8(self):
        assert "8" in spectral_space_chapter_index()

    def test_chapter_index_contains_chapter_26(self):
        assert "26" in spectral_space_chapter_index()

    def test_sierpinski_in_chapter_8(self):
        assert "sierpinski_space" in spectral_space_chapter_index()["8"]

    def test_type_index_returns_dict(self):
        assert isinstance(spectral_space_type_index(), dict)

    def test_type_index_has_spectral(self):
        assert "spectral" in spectral_space_type_index()

    def test_type_index_has_stone(self):
        assert "stone" in spectral_space_type_index()

    def test_type_index_has_t0_not_sober(self):
        assert "t0_not_sober" in spectral_space_type_index()

    def test_type_index_all_types_in_profiles(self):
        all_types = {p.space_type for p in get_named_spectral_space_profiles()}
        assert set(spectral_space_type_index().keys()) == all_types


# ---------------------------------------------------------------------------
# is_sober
# ---------------------------------------------------------------------------

class TestIsSober:
    def test_sober_tag_true(self):
        assert is_sober(_sp("sober")).is_true

    def test_hausdorff_true(self):
        assert is_sober(_sp("hausdorff")).is_true

    def test_t2_true(self):
        assert is_sober(_sp("t2")).is_true

    def test_compact_hausdorff_true(self):
        assert is_sober(_sp("compact_hausdorff")).is_true

    def test_metrizable_true(self):
        assert is_sober(_sp("metrizable")).is_true

    def test_stone_space_true(self):
        assert is_sober(_sp("stone_space")).is_true

    def test_profinite_true(self):
        assert is_sober(_sp("profinite")).is_true

    def test_spectral_space_true(self):
        assert is_sober(_sp("spectral_space")).is_true

    def test_spec_ring_true(self):
        assert is_sober(_sp("spec_ring")).is_true

    def test_zariski_true(self):
        assert is_sober(_sp("zariski_spectrum")).is_true

    def test_sierpinski_true(self):
        assert is_sober(_sp("sierpinski_space")).is_true

    def test_alexandrov_dcpo_true(self):
        assert is_sober(_sp("alexandrov_dcpo")).is_true

    def test_not_sober_tag_false(self):
        assert is_sober(_sp("not_sober")).is_false

    def test_alexandrov_no_maximum_false(self):
        assert is_sober(_sp("alexandrov_no_maximum")).is_false

    def test_empty_unknown(self):
        assert is_sober(_sp()).is_unknown

    def test_irrelevant_tags_unknown(self):
        assert is_sober(_sp("compact", "connected")).is_unknown

    def test_returns_result(self):
        assert isinstance(is_sober(_sp("sober")), Result)

    def test_true_has_justification(self):
        r = is_sober(_sp("spec_ring"))
        assert len(r.justification) > 0

    def test_false_has_justification(self):
        r = is_sober(_sp("not_sober"))
        assert len(r.justification) > 0

    def test_spatial_locale_true(self):
        assert is_sober(_sp("spatial_locale")).is_true


# ---------------------------------------------------------------------------
# is_spectral
# ---------------------------------------------------------------------------

class TestIsSpectral:
    def test_spectral_space_tag_true(self):
        assert is_spectral(_sp("spectral_space")).is_true

    def test_coherent_space_true(self):
        assert is_spectral(_sp("coherent_space")).is_true

    def test_spec_ring_true(self):
        assert is_spectral(_sp("spec_ring")).is_true

    def test_zariski_true(self):
        assert is_spectral(_sp("zariski_spectrum")).is_true

    def test_stone_space_true(self):
        assert is_spectral(_sp("stone_space")).is_true

    def test_profinite_true(self):
        assert is_spectral(_sp("profinite")).is_true

    def test_sierpinski_true(self):
        assert is_spectral(_sp("sierpinski_space")).is_true

    def test_not_sober_false(self):
        assert is_spectral(_sp("not_sober")).is_false

    def test_alexandrov_no_maximum_false(self):
        assert is_spectral(_sp("alexandrov_no_maximum")).is_false

    def test_empty_unknown(self):
        assert is_spectral(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_spectral(_sp("spectral_space")), Result)

    def test_alexandrov_finite_poset_true(self):
        assert is_spectral(_sp("alexandrov_finite_poset")).is_true


# ---------------------------------------------------------------------------
# is_stone_space
# ---------------------------------------------------------------------------

class TestIsStoneSpace:
    def test_stone_space_tag_true(self):
        assert is_stone_space(_sp("stone_space")).is_true

    def test_boolean_space_true(self):
        assert is_stone_space(_sp("boolean_space")).is_true

    def test_profinite_true(self):
        assert is_stone_space(_sp("profinite")).is_true

    def test_cantor_space_true(self):
        assert is_stone_space(_sp("cantor_space")).is_true

    def test_cantor_set_true(self):
        assert is_stone_space(_sp("cantor_set")).is_true

    def test_p_adic_integers_true(self):
        assert is_stone_space(_sp("p_adic_integers")).is_true

    def test_profinite_group_true(self):
        assert is_stone_space(_sp("profinite_group")).is_true

    def test_compact_totally_disconnected_hausdorff_true(self):
        assert is_stone_space(_sp("compact_totally_disconnected_hausdorff")).is_true

    def test_sierpinski_false(self):
        assert is_stone_space(_sp("sierpinski_space")).is_false

    def test_spec_ring_false(self):
        assert is_stone_space(_sp("spec_ring")).is_false

    def test_not_hausdorff_false(self):
        assert is_stone_space(_sp("not_hausdorff")).is_false

    def test_connected_nontrivial_false(self):
        assert is_stone_space(_sp("connected_nontrivial")).is_false

    def test_empty_unknown(self):
        assert is_stone_space(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(is_stone_space(_sp("stone_space")), Result)


# ---------------------------------------------------------------------------
# frame_is_spatial
# ---------------------------------------------------------------------------

class TestFrameIsSpatial:
    def test_spatial_frame_tag_true(self):
        assert frame_is_spatial(_sp("spatial_frame")).is_true

    def test_sober_tag_true(self):
        assert frame_is_spatial(_sp("sober")).is_true

    def test_hausdorff_true(self):
        assert frame_is_spatial(_sp("hausdorff")).is_true

    def test_spectral_space_true(self):
        assert frame_is_spatial(_sp("spectral_space")).is_true

    def test_stone_space_true(self):
        assert frame_is_spatial(_sp("stone_space")).is_true

    def test_not_sober_false(self):
        assert frame_is_spatial(_sp("not_sober")).is_false

    def test_alexandrov_no_maximum_false(self):
        assert frame_is_spatial(_sp("alexandrov_no_maximum")).is_false

    def test_empty_unknown(self):
        assert frame_is_spatial(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(frame_is_spatial(_sp("sober")), Result)

    def test_true_has_justification(self):
        r = frame_is_spatial(_sp("sober"))
        assert len(r.justification) > 0


# ---------------------------------------------------------------------------
# stone_duality_applies
# ---------------------------------------------------------------------------

class TestStoneDualityApplies:
    def test_stone_space_true(self):
        assert stone_duality_applies(_sp("stone_space")).is_true

    def test_profinite_true(self):
        assert stone_duality_applies(_sp("profinite")).is_true

    def test_boolean_space_true(self):
        assert stone_duality_applies(_sp("boolean_space")).is_true

    def test_cantor_space_true(self):
        assert stone_duality_applies(_sp("cantor_space")).is_true

    def test_p_adic_integers_true(self):
        assert stone_duality_applies(_sp("p_adic_integers")).is_true

    def test_sierpinski_false(self):
        assert stone_duality_applies(_sp("sierpinski_space")).is_false

    def test_spec_ring_false(self):
        assert stone_duality_applies(_sp("spec_ring")).is_false

    def test_not_hausdorff_false(self):
        assert stone_duality_applies(_sp("not_hausdorff")).is_false

    def test_t0_not_t1_false(self):
        assert stone_duality_applies(_sp("t0_not_t1")).is_false

    def test_generic_point_not_closed_false(self):
        assert stone_duality_applies(_sp("generic_point_not_closed")).is_false

    def test_empty_unknown(self):
        assert stone_duality_applies(_sp()).is_unknown

    def test_returns_result(self):
        assert isinstance(stone_duality_applies(_sp("stone_space")), Result)


# ---------------------------------------------------------------------------
# classify_spectral_space
# ---------------------------------------------------------------------------

class TestClassifySpectralSpace:
    def test_returns_dict(self):
        assert isinstance(classify_spectral_space(_sp()), dict)

    def test_has_space_class_key(self):
        assert "space_class" in classify_spectral_space(_sp())

    def test_has_is_sober_key(self):
        assert "is_sober" in classify_spectral_space(_sp())

    def test_has_is_spectral_key(self):
        assert "is_spectral" in classify_spectral_space(_sp())

    def test_has_is_stone_space_key(self):
        assert "is_stone_space" in classify_spectral_space(_sp())

    def test_has_frame_is_spatial_key(self):
        assert "frame_is_spatial" in classify_spectral_space(_sp())

    def test_has_stone_duality_key(self):
        assert "stone_duality" in classify_spectral_space(_sp())

    def test_has_key_properties_key(self):
        assert "key_properties" in classify_spectral_space(_sp())

    def test_key_properties_is_list(self):
        assert isinstance(classify_spectral_space(_sp())["key_properties"], list)

    def test_stone_space_class(self):
        r = classify_spectral_space(_sp("stone_space"))
        assert r["space_class"] == "stone"

    def test_spec_ring_class_spectral(self):
        r = classify_spectral_space(_sp("spec_ring"))
        assert r["space_class"] == "spectral"

    def test_sober_not_spectral_class(self):
        r = classify_spectral_space(_sp("sober"))
        assert r["space_class"] == "sober"

    def test_not_sober_class(self):
        r = classify_spectral_space(_sp("not_sober"))
        assert r["space_class"] == "t0_not_sober"

    def test_unknown_class_empty(self):
        r = classify_spectral_space(_sp())
        assert r["space_class"] == "unknown"

    def test_stone_key_properties_contains_stone_space(self):
        r = classify_spectral_space(_sp("stone_space"))
        assert "stone_space" in r["key_properties"]

    def test_stone_key_properties_contains_sober(self):
        r = classify_spectral_space(_sp("stone_space"))
        assert "sober" in r["key_properties"]

    def test_not_sober_key_properties_contains_not_sober(self):
        r = classify_spectral_space(_sp("not_sober"))
        assert "not_sober" in r["key_properties"]

    def test_sierpinski_t0_not_t1_in_key_props(self):
        r = classify_spectral_space(_sp("sierpinski_space"))
        assert "t0_not_t1" in r["key_properties"]

    def test_spec_ring_t0_not_t1_in_key_props(self):
        r = classify_spectral_space(_sp("spec_ring"))
        assert "t0_not_t1" in r["key_properties"]

    def test_representation_in_output(self):
        assert "representation" in classify_spectral_space(_sp())

    def test_tags_is_list(self):
        assert isinstance(classify_spectral_space(_sp("sober"))["tags"], list)

    def test_stone_duality_in_key_props_for_stone(self):
        r = classify_spectral_space(_sp("stone_space"))
        assert "stone_duality" in r["key_properties"]


# ---------------------------------------------------------------------------
# spectral_space_profile
# ---------------------------------------------------------------------------

class TestSpectralSpaceProfile:
    def test_returns_dict(self):
        assert isinstance(spectral_space_profile(_sp()), dict)

    def test_has_classification_key(self):
        assert "classification" in spectral_space_profile(_sp())

    def test_has_named_profiles_key(self):
        assert "named_profiles" in spectral_space_profile(_sp())

    def test_has_layer_summary_key(self):
        assert "layer_summary" in spectral_space_profile(_sp())

    def test_named_profiles_is_tuple(self):
        assert isinstance(spectral_space_profile(_sp())["named_profiles"], tuple)

    def test_classification_has_space_class(self):
        p = spectral_space_profile(_sp("spectral_space"))
        assert "space_class" in p["classification"]

    def test_layer_summary_is_dict(self):
        assert isinstance(spectral_space_profile(_sp())["layer_summary"], dict)

    def test_stone_classification_correct(self):
        p = spectral_space_profile(_sp("stone_space"))
        assert p["classification"]["space_class"] == "stone"

    def test_not_sober_classification_correct(self):
        p = spectral_space_profile(_sp("not_sober"))
        assert p["classification"]["space_class"] == "t0_not_sober"
