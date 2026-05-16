"""Tests for topological_vector_spaces.py (v0.5.7)."""

import types

import pytest

from pytop.result import Result
from pytop.spaces import TopologicalSpace
from pytop.topological_vector_spaces import (
    BANACH_TAGS,
    FRECHET_TAGS,
    HAHN_BANACH_TAGS,
    HILBERT_TAGS,
    LOCALLY_CONVEX_TAGS,
    NOT_LOCALLY_CONVEX_TAGS,
    OPEN_MAPPING_TAGS,
    TVS_NEGATIVE_TAGS,
    TVS_POSITIVE_TAGS,
    TVSProfile,
    classify_tvs,
    get_named_tvs_profiles,
    hahn_banach_applicable,
    is_banach_space,
    is_frechet_space,
    is_locally_convex,
    open_mapping_theorem_holds,
    tvs_chapter_index,
    tvs_layer_summary,
    tvs_profile,
    tvs_type_index,
)


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_tvs_positive_contains_banach(self):
        assert "banach_space" in TVS_POSITIVE_TAGS

    def test_tvs_positive_contains_hilbert(self):
        assert "hilbert_space" in TVS_POSITIVE_TAGS

    def test_tvs_positive_contains_frechet(self):
        assert "frechet_space" in TVS_POSITIVE_TAGS

    def test_tvs_positive_contains_locally_convex(self):
        assert "locally_convex" in TVS_POSITIVE_TAGS

    def test_tvs_negative_contains_not_tvs(self):
        assert "not_tvs" in TVS_NEGATIVE_TAGS

    def test_locally_convex_contains_banach(self):
        assert "banach_space" in LOCALLY_CONVEX_TAGS

    def test_locally_convex_contains_nuclear(self):
        assert "nuclear_space" in LOCALLY_CONVEX_TAGS

    def test_not_locally_convex_contains_lp_quasi(self):
        assert "lp_space_0_p_1" in NOT_LOCALLY_CONVEX_TAGS

    def test_frechet_contains_smooth_functions(self):
        assert "smooth_functions_space" in FRECHET_TAGS

    def test_banach_contains_sobolev(self):
        assert "sobolev_space" in BANACH_TAGS

    def test_hilbert_contains_l2(self):
        assert "l2_space" in HILBERT_TAGS

    def test_hahn_banach_contains_locally_convex(self):
        assert "locally_convex" in HAHN_BANACH_TAGS

    def test_open_mapping_contains_frechet(self):
        assert "frechet_space" in OPEN_MAPPING_TAGS

    def test_hilbert_subset_of_banach(self):
        for tag in HILBERT_TAGS:
            assert tag in BANACH_TAGS

    def test_banach_subset_of_frechet(self):
        for tag in BANACH_TAGS:
            assert tag in FRECHET_TAGS


# ---------------------------------------------------------------------------
# TVSProfile dataclass
# ---------------------------------------------------------------------------

class TestTVSProfileDataclass:
    def test_profile_is_frozen(self):
        p = TVSProfile(
            key="test",
            display_name="Test",
            tvs_type="banach",
            is_locally_convex=True,
            is_complete=True,
            presentation_layer="main_text",
            focus="test focus",
            chapter_targets=("5",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields(self):
        p = TVSProfile(
            key="hilbert_l2",
            display_name="L2",
            tvs_type="hilbert",
            is_locally_convex=True,
            is_complete=True,
            presentation_layer="main_text",
            focus="hilbert focus",
            chapter_targets=("5", "28"),
        )
        assert p.tvs_type == "hilbert"
        assert p.is_locally_convex is True
        assert p.is_complete is True
        assert "5" in p.chapter_targets


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

class TestNamedTVSProfiles:
    def setup_method(self):
        self.profiles = get_named_tvs_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_has_five_profiles(self):
        assert len(self.profiles) == 5

    def test_all_are_tvs_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, TVSProfile)

    def test_hilbert_l2_present(self):
        keys = {p.key for p in self.profiles}
        assert "hilbert_l2" in keys

    def test_banach_lp_present(self):
        keys = {p.key for p in self.profiles}
        assert "banach_lp" in keys

    def test_frechet_smooth_present(self):
        keys = {p.key for p in self.profiles}
        assert "frechet_smooth" in keys

    def test_locally_convex_distributions_present(self):
        keys = {p.key for p in self.profiles}
        assert "locally_convex_distributions" in keys

    def test_quasi_banach_lp_present(self):
        keys = {p.key for p in self.profiles}
        assert "quasi_banach_lp" in keys

    def test_hilbert_is_locally_convex(self):
        p = next(x for x in self.profiles if x.key == "hilbert_l2")
        assert p.is_locally_convex is True

    def test_hilbert_is_complete(self):
        p = next(x for x in self.profiles if x.key == "hilbert_l2")
        assert p.is_complete is True

    def test_quasi_banach_not_locally_convex(self):
        p = next(x for x in self.profiles if x.key == "quasi_banach_lp")
        assert p.is_locally_convex is False

    def test_frechet_smooth_is_frechet_type(self):
        p = next(x for x in self.profiles if x.key == "frechet_smooth")
        assert p.tvs_type == "frechet"

    def test_hilbert_type(self):
        p = next(x for x in self.profiles if x.key == "hilbert_l2")
        assert p.tvs_type == "hilbert"

    def test_banach_lp_is_locally_convex(self):
        p = next(x for x in self.profiles if x.key == "banach_lp")
        assert p.is_locally_convex is True

    def test_distributions_type_is_locally_convex(self):
        p = next(x for x in self.profiles if x.key == "locally_convex_distributions")
        assert p.tvs_type == "locally_convex"

    def test_quasi_banach_type_is_tvs(self):
        p = next(x for x in self.profiles if x.key == "quasi_banach_lp")
        assert p.tvs_type == "tvs"


# ---------------------------------------------------------------------------
# Layer / chapter / type index helpers
# ---------------------------------------------------------------------------

class TestIndexHelpers:
    def test_layer_summary_is_dict(self):
        ls = tvs_layer_summary()
        assert isinstance(ls, dict)

    def test_layer_summary_has_main_text(self):
        ls = tvs_layer_summary()
        assert "main_text" in ls

    def test_layer_summary_counts_correct(self):
        ls = tvs_layer_summary()
        assert ls.get("main_text", 0) == 2
        assert ls.get("selected_block", 0) == 1
        assert ls.get("advanced_note", 0) == 2

    def test_chapter_index_is_dict(self):
        ci = tvs_chapter_index()
        assert isinstance(ci, dict)

    def test_chapter_5_has_profiles(self):
        ci = tvs_chapter_index()
        assert "5" in ci
        assert len(ci["5"]) >= 3

    def test_chapter_index_values_are_tuples(self):
        ci = tvs_chapter_index()
        for v in ci.values():
            assert isinstance(v, tuple)

    def test_type_index_is_dict(self):
        ti = tvs_type_index()
        assert isinstance(ti, dict)

    def test_type_index_has_hilbert_and_banach(self):
        ti = tvs_type_index()
        assert "hilbert" in ti
        assert "banach" in ti

    def test_type_index_hilbert_has_l2(self):
        ti = tvs_type_index()
        assert "hilbert_l2" in ti["hilbert"]

    def test_type_index_frechet_has_smooth(self):
        ti = tvs_type_index()
        assert "frechet_smooth" in ti["frechet"]


# ---------------------------------------------------------------------------
# is_locally_convex
# ---------------------------------------------------------------------------

class TestIsLocallyConvex:
    def test_not_locally_convex_tag(self):
        sp = _sp("not_locally_convex")
        r = is_locally_convex(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_locally_convex"

    def test_lp_quasi_banach_not_locally_convex(self):
        sp = _sp("lp_space_0_p_1")
        r = is_locally_convex(sp)
        assert r.is_false

    def test_hilbert_is_locally_convex(self):
        sp = _sp("hilbert_space")
        r = is_locally_convex(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "hilbert"

    def test_l2_is_locally_convex(self):
        sp = _sp("l2_space")
        r = is_locally_convex(sp)
        assert r.is_true

    def test_banach_is_locally_convex(self):
        sp = _sp("banach_space")
        r = is_locally_convex(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "banach"

    def test_sobolev_is_locally_convex(self):
        sp = _sp("sobolev_space")
        r = is_locally_convex(sp)
        assert r.is_true

    def test_frechet_is_locally_convex(self):
        sp = _sp("frechet_space")
        r = is_locally_convex(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "frechet"

    def test_smooth_functions_is_locally_convex(self):
        sp = _sp("smooth_functions_space")
        r = is_locally_convex(sp)
        assert r.is_true

    def test_locally_convex_direct_tag(self):
        sp = _sp("locally_convex")
        r = is_locally_convex(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "direct_tag"

    def test_normed_space_is_locally_convex(self):
        sp = _sp("normed_space")
        r = is_locally_convex(sp)
        assert r.is_true

    def test_nuclear_space_is_locally_convex(self):
        sp = _sp("nuclear_space")
        r = is_locally_convex(sp)
        assert r.is_true

    def test_unknown_no_relevant_tags(self):
        sp = _sp("compact", "connected")
        r = is_locally_convex(sp)
        assert r.is_unknown

    def test_result_has_representation(self):
        sp = _sp("banach_space")
        r = is_locally_convex(sp)
        assert "representation" in r.metadata

    def test_result_has_tags(self):
        sp = _sp("banach_space")
        r = is_locally_convex(sp)
        assert "tags" in r.metadata


# ---------------------------------------------------------------------------
# is_frechet_space
# ---------------------------------------------------------------------------

class TestIsFrechetSpace:
    def test_not_locally_convex_not_frechet(self):
        sp = _sp("not_locally_convex")
        r = is_frechet_space(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_locally_convex"

    def test_lp_quasi_not_frechet(self):
        sp = _sp("lp_space_0_p_1")
        r = is_frechet_space(sp)
        assert r.is_false

    def test_hilbert_is_frechet(self):
        sp = _sp("hilbert_space")
        r = is_frechet_space(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "hilbert"

    def test_banach_is_frechet(self):
        sp = _sp("banach_space")
        r = is_frechet_space(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "banach"

    def test_lp_space_is_frechet(self):
        sp = _sp("lp_space")
        r = is_frechet_space(sp)
        assert r.is_true

    def test_frechet_tag_direct(self):
        sp = _sp("frechet_space")
        r = is_frechet_space(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "direct_tag"

    def test_smooth_functions_is_frechet(self):
        sp = _sp("smooth_functions_space")
        r = is_frechet_space(sp)
        assert r.is_true

    def test_distribution_space_not_frechet(self):
        sp = _sp("distribution_space")
        r = is_frechet_space(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_metrizable"

    def test_lf_space_not_frechet(self):
        sp = _sp("lf_space")
        r = is_frechet_space(sp)
        assert r.is_false

    def test_unknown_no_tags(self):
        sp = _sp("compact", "connected")
        r = is_frechet_space(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# is_banach_space
# ---------------------------------------------------------------------------

class TestIsBanachSpace:
    def test_not_banach_tag(self):
        sp = _sp("not_banach")
        r = is_banach_space(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_banach"

    def test_not_normable_not_banach(self):
        sp = _sp("not_normable")
        r = is_banach_space(sp)
        assert r.is_false

    def test_hilbert_is_banach(self):
        sp = _sp("hilbert_space")
        r = is_banach_space(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "hilbert"

    def test_l2_is_banach(self):
        sp = _sp("l2")
        r = is_banach_space(sp)
        assert r.is_true

    def test_banach_tag_direct(self):
        sp = _sp("banach_space")
        r = is_banach_space(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "direct_tag"

    def test_lp_space_is_banach(self):
        sp = _sp("lp_space")
        r = is_banach_space(sp)
        assert r.is_true

    def test_sobolev_is_banach(self):
        sp = _sp("sobolev_space")
        r = is_banach_space(sp)
        assert r.is_true

    def test_smooth_functions_not_banach(self):
        sp = _sp("smooth_functions_space")
        r = is_banach_space(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "frechet_not_banach"

    def test_schwartz_not_banach(self):
        sp = _sp("schwartz_space")
        r = is_banach_space(sp)
        assert r.is_false

    def test_not_locally_convex_not_banach(self):
        sp = _sp("not_locally_convex")
        r = is_banach_space(sp)
        assert r.is_false

    def test_unknown_no_tags(self):
        sp = _sp("compact", "connected")
        r = is_banach_space(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# hahn_banach_applicable
# ---------------------------------------------------------------------------

class TestHahnBanachApplicable:
    def test_not_locally_convex_hb_fails(self):
        sp = _sp("not_locally_convex")
        r = hahn_banach_applicable(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_locally_convex"

    def test_lp_quasi_hb_fails(self):
        sp = _sp("lp_space_0_p_1")
        r = hahn_banach_applicable(sp)
        assert r.is_false

    def test_hilbert_hb_applies(self):
        sp = _sp("hilbert_space")
        r = hahn_banach_applicable(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "hilbert"

    def test_banach_hb_applies(self):
        sp = _sp("banach_space")
        r = hahn_banach_applicable(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "locally_convex"

    def test_frechet_hb_applies(self):
        sp = _sp("frechet_space")
        r = hahn_banach_applicable(sp)
        assert r.is_true

    def test_locally_convex_hb_applies(self):
        sp = _sp("locally_convex")
        r = hahn_banach_applicable(sp)
        assert r.is_true

    def test_normed_space_hb_applies(self):
        sp = _sp("normed_space")
        r = hahn_banach_applicable(sp)
        assert r.is_true

    def test_nuclear_space_hb_applies(self):
        sp = _sp("nuclear_space")
        r = hahn_banach_applicable(sp)
        assert r.is_true

    def test_unknown_no_tags(self):
        sp = _sp("compact", "connected")
        r = hahn_banach_applicable(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# open_mapping_theorem_holds
# ---------------------------------------------------------------------------

class TestOpenMappingTheoremHolds:
    def test_not_metrizable_om_fails(self):
        sp = _sp("not_metrizable")
        r = open_mapping_theorem_holds(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_frechet"

    def test_distribution_space_om_fails(self):
        sp = _sp("distribution_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_false

    def test_lf_space_om_fails(self):
        sp = _sp("lf_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_false

    def test_not_locally_convex_om_fails(self):
        sp = _sp("not_locally_convex")
        r = open_mapping_theorem_holds(sp)
        assert r.is_false

    def test_hilbert_om_holds(self):
        sp = _sp("hilbert_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "hilbert"

    def test_banach_om_holds(self):
        sp = _sp("banach_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "banach"

    def test_lp_space_om_holds(self):
        sp = _sp("lp_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_true

    def test_frechet_om_holds(self):
        sp = _sp("frechet_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "frechet"

    def test_smooth_functions_om_holds(self):
        sp = _sp("smooth_functions_space")
        r = open_mapping_theorem_holds(sp)
        assert r.is_true

    def test_unknown_no_tags(self):
        sp = _sp("compact", "connected")
        r = open_mapping_theorem_holds(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# classify_tvs
# ---------------------------------------------------------------------------

class TestClassifyTVS:
    def test_returns_dict(self):
        sp = _sp("hilbert_space")
        result = classify_tvs(sp)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        sp = _sp("hilbert_space")
        result = classify_tvs(sp)
        for key in ("tvs_type", "is_locally_convex", "is_frechet", "is_banach",
                    "hahn_banach", "open_mapping", "key_properties", "representation", "tags"):
            assert key in result

    def test_hilbert_tvs_type(self):
        sp = _sp("hilbert_space")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "hilbert"

    def test_banach_tvs_type(self):
        sp = _sp("banach_space")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "banach"

    def test_frechet_tvs_type(self):
        sp = _sp("frechet_space")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "frechet"

    def test_locally_convex_tvs_type(self):
        sp = _sp("locally_convex")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "locally_convex"

    def test_tvs_positive_tag_gives_tvs_type(self):
        sp = _sp("lp_space_0_p_1")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "tvs"

    def test_unknown_tvs_type(self):
        sp = _sp("compact", "connected")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "unknown"

    def test_hilbert_key_properties(self):
        sp = _sp("hilbert_space")
        result = classify_tvs(sp)
        assert "locally_convex" in result["key_properties"]
        assert "frechet" in result["key_properties"]
        assert "banach" in result["key_properties"]
        assert "hilbert" in result["key_properties"]
        assert "hahn_banach" in result["key_properties"]
        assert "open_mapping" in result["key_properties"]

    def test_not_locally_convex_in_key_properties(self):
        sp = _sp("not_locally_convex")
        result = classify_tvs(sp)
        assert "not_locally_convex" in result["key_properties"]

    def test_results_are_result_instances(self):
        sp = _sp("banach_space")
        result = classify_tvs(sp)
        assert isinstance(result["is_locally_convex"], Result)
        assert isinstance(result["is_frechet"], Result)
        assert isinstance(result["is_banach"], Result)

    def test_representation_in_result(self):
        sp = _sp("hilbert_space")
        result = classify_tvs(sp)
        assert isinstance(result["representation"], str)

    def test_schwartz_space_tvs_type(self):
        sp = _sp("schwartz_space")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "frechet"


# ---------------------------------------------------------------------------
# tvs_profile (facade)
# ---------------------------------------------------------------------------

class TestTVSProfileFacade:
    def test_returns_dict(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert isinstance(result, dict)

    def test_has_classification_key(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert "classification" in result

    def test_has_named_profiles_key(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert "named_profiles" in result

    def test_has_layer_summary_key(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert "layer_summary" in result

    def test_named_profiles_is_tuple(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert isinstance(result["named_profiles"], tuple)

    def test_classification_is_dict(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert isinstance(result["classification"], dict)

    def test_layer_summary_is_dict(self):
        sp = _sp("banach_space")
        result = tvs_profile(sp)
        assert isinstance(result["layer_summary"], dict)


# ---------------------------------------------------------------------------
# Representation routing
# ---------------------------------------------------------------------------

class TestRepresentationRouting:
    def test_metadata_dict_path(self):
        sp = TopologicalSpace.symbolic(
            description="L2 space",
            representation="hilbert_l2_space",
            tags={"hilbert_space"},
        )
        r = is_locally_convex(sp)
        assert r.is_true
        assert "hilbert_l2_space" in r.metadata.get("representation", "")

    def test_attribute_path(self):
        sp = types.SimpleNamespace(tags={"banach_space"}, metadata={}, representation="lp_banach")
        r = is_banach_space(sp)
        assert r.is_true
        assert "lp_banach" in r.metadata.get("representation", "")

    def test_no_representation_fallback(self):
        sp = types.SimpleNamespace(tags={"frechet_space"}, metadata={})
        r = is_frechet_space(sp)
        assert r.is_true
        assert r.metadata.get("representation") == "symbolic_general"


# ---------------------------------------------------------------------------
# Cross-theorem consistency (TVS hierarchy)
# ---------------------------------------------------------------------------

class TestTVSHierarchyConsistency:
    def test_hilbert_implies_banach(self):
        sp = _sp("hilbert_space")
        assert is_banach_space(sp).is_true
        assert is_frechet_space(sp).is_true
        assert is_locally_convex(sp).is_true

    def test_banach_implies_frechet(self):
        sp = _sp("banach_space")
        assert is_frechet_space(sp).is_true
        assert is_locally_convex(sp).is_true

    def test_frechet_implies_locally_convex(self):
        sp = _sp("frechet_space")
        assert is_locally_convex(sp).is_true

    def test_not_locally_convex_implies_not_frechet_not_banach(self):
        sp = _sp("not_locally_convex")
        assert is_locally_convex(sp).is_false
        assert is_frechet_space(sp).is_false
        assert is_banach_space(sp).is_false

    def test_smooth_functions_frechet_not_banach(self):
        sp = _sp("smooth_functions_space")
        assert is_frechet_space(sp).is_true
        assert is_banach_space(sp).is_false
        assert is_locally_convex(sp).is_true

    def test_distribution_space_not_frechet(self):
        sp = _sp("distribution_space")
        assert is_frechet_space(sp).is_false
        assert is_locally_convex(sp).is_true

    def test_hahn_banach_requires_local_convexity(self):
        sp = _sp("lp_space_0_p_1")
        assert hahn_banach_applicable(sp).is_false
        assert is_locally_convex(sp).is_false

    def test_open_mapping_requires_frechet(self):
        sp = _sp("lf_space")
        assert open_mapping_theorem_holds(sp).is_false
        assert is_frechet_space(sp).is_false

    def test_hilbert_satisfies_all_theorems(self):
        sp = _sp("hilbert")
        assert hahn_banach_applicable(sp).is_true
        assert open_mapping_theorem_holds(sp).is_true

    def test_lp_space_0_p_1_tvs_but_not_locally_convex(self):
        sp = _sp("lp_space_0_p_1")
        result = classify_tvs(sp)
        assert result["tvs_type"] == "tvs"
        assert result["is_locally_convex"].is_false
