"""Tests for hyperspaces.py (v0.5.8)."""

import types

import pytest

from pytop.hyperspaces import (
    COMPACT_METRIZABLE_TAGS,
    CONNECTED_BASE_TAGS,
    HAUSDORFF_METRIC_TAGS,
    LOCALLY_COMPACT_METRIZABLE_TAGS,
    METRIZABLE_BASE_TAGS,
    NOT_HYPERSPACE_COMPACT_TAGS,
    POLISH_BASE_TAGS,
    VIETORIS_COMPACT_TAGS,
    HyperspaceProfile,
    classify_hyperspace,
    get_named_hyperspace_profiles,
    hausdorff_metric_applicable,
    hyperspace_chapter_index,
    hyperspace_is_compact,
    hyperspace_is_connected,
    hyperspace_is_polish,
    hyperspace_layer_summary,
    hyperspace_profile,
    hyperspace_type_index,
    vietoris_topology_hausdorff,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_compact_metrizable_contains_cantor(self):
        assert "cantor_set" in COMPACT_METRIZABLE_TAGS

    def test_compact_metrizable_contains_closed_interval(self):
        assert "closed_interval" in COMPACT_METRIZABLE_TAGS

    def test_compact_metrizable_contains_compact(self):
        assert "compact" in COMPACT_METRIZABLE_TAGS

    def test_polish_base_contains_polish_space(self):
        assert "polish_space" in POLISH_BASE_TAGS

    def test_polish_base_contains_completely_metrizable(self):
        assert "completely_metrizable" in POLISH_BASE_TAGS

    def test_polish_base_contains_banach(self):
        assert "banach_space" in POLISH_BASE_TAGS

    def test_locally_compact_contains_real_line(self):
        assert "real_line" in LOCALLY_COMPACT_METRIZABLE_TAGS

    def test_locally_compact_contains_euclidean(self):
        assert "euclidean" in LOCALLY_COMPACT_METRIZABLE_TAGS

    def test_connected_base_contains_connected(self):
        assert "connected" in CONNECTED_BASE_TAGS

    def test_connected_base_contains_real_line(self):
        assert "real_line" in CONNECTED_BASE_TAGS

    def test_hausdorff_metric_contains_metric(self):
        assert "metric" in HAUSDORFF_METRIC_TAGS

    def test_not_compact_contains_real_line(self):
        assert "real_line" in NOT_HYPERSPACE_COMPACT_TAGS

    def test_not_compact_contains_irrationals(self):
        assert "irrationals" in NOT_HYPERSPACE_COMPACT_TAGS

    def test_vietoris_compact_contains_compact(self):
        assert "compact" in VIETORIS_COMPACT_TAGS

    def test_metrizable_base_contains_metric(self):
        assert "metric" in METRIZABLE_BASE_TAGS


# ---------------------------------------------------------------------------
# HyperspaceProfile dataclass
# ---------------------------------------------------------------------------

class TestHyperspaceProfileDataclass:
    def test_profile_is_frozen(self):
        p = HyperspaceProfile(
            key="test",
            display_name="Test",
            hyperspace_type="compact_polish",
            base_space_class="compact_metrizable",
            is_compact=True,
            is_polish=True,
            presentation_layer="main_text",
            focus="test focus",
            chapter_targets=("4",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields(self):
        p = HyperspaceProfile(
            key="k_closed_interval",
            display_name="K([0,1])",
            hyperspace_type="compact_polish",
            base_space_class="compact_metrizable",
            is_compact=True,
            is_polish=True,
            presentation_layer="main_text",
            focus="K([0,1]) focus",
            chapter_targets=("4", "27"),
        )
        assert p.is_compact is True
        assert p.is_polish is True
        assert "4" in p.chapter_targets


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

class TestNamedHyperspaceProfiles:
    def setup_method(self):
        self.profiles = get_named_hyperspace_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_has_five_profiles(self):
        assert len(self.profiles) == 5

    def test_all_are_hyperspace_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, HyperspaceProfile)

    def test_k_closed_interval_present(self):
        keys = {p.key for p in self.profiles}
        assert "k_closed_interval" in keys

    def test_k_cantor_present(self):
        keys = {p.key for p in self.profiles}
        assert "k_cantor" in keys

    def test_k_real_line_present(self):
        keys = {p.key for p in self.profiles}
        assert "k_real_line" in keys

    def test_vietoris_compact_present(self):
        keys = {p.key for p in self.profiles}
        assert "vietoris_compact" in keys

    def test_k_polish_space_present(self):
        keys = {p.key for p in self.profiles}
        assert "k_polish_space" in keys

    def test_k_closed_interval_is_compact(self):
        p = next(x for x in self.profiles if x.key == "k_closed_interval")
        assert p.is_compact is True

    def test_k_real_line_not_compact(self):
        p = next(x for x in self.profiles if x.key == "k_real_line")
        assert p.is_compact is False

    def test_k_real_line_is_polish(self):
        p = next(x for x in self.profiles if x.key == "k_real_line")
        assert p.is_polish is True

    def test_k_cantor_compact_polish(self):
        p = next(x for x in self.profiles if x.key == "k_cantor")
        assert p.is_compact is True
        assert p.is_polish is True

    def test_vietoris_compact_type(self):
        p = next(x for x in self.profiles if x.key == "vietoris_compact")
        assert p.hyperspace_type == "compact_vietoris"

    def test_k_polish_space_type(self):
        p = next(x for x in self.profiles if x.key == "k_polish_space")
        assert p.hyperspace_type == "polish"


# ---------------------------------------------------------------------------
# Layer / chapter / type index helpers
# ---------------------------------------------------------------------------

class TestIndexHelpers:
    def test_layer_summary_is_dict(self):
        ls = hyperspace_layer_summary()
        assert isinstance(ls, dict)

    def test_layer_summary_has_main_text(self):
        ls = hyperspace_layer_summary()
        assert "main_text" in ls

    def test_layer_summary_counts_correct(self):
        ls = hyperspace_layer_summary()
        assert ls.get("main_text", 0) == 2
        assert ls.get("selected_block", 0) == 2
        assert ls.get("advanced_note", 0) == 1

    def test_chapter_index_is_dict(self):
        ci = hyperspace_chapter_index()
        assert isinstance(ci, dict)

    def test_chapter_4_has_profiles(self):
        ci = hyperspace_chapter_index()
        assert "4" in ci
        assert len(ci["4"]) >= 4

    def test_chapter_27_has_profiles(self):
        ci = hyperspace_chapter_index()
        assert "27" in ci

    def test_chapter_index_values_are_tuples(self):
        ci = hyperspace_chapter_index()
        for v in ci.values():
            assert isinstance(v, tuple)

    def test_type_index_is_dict(self):
        ti = hyperspace_type_index()
        assert isinstance(ti, dict)

    def test_type_index_has_compact_polish(self):
        ti = hyperspace_type_index()
        assert "compact_polish" in ti

    def test_type_index_compact_polish_has_closed_interval(self):
        ti = hyperspace_type_index()
        assert "k_closed_interval" in ti["compact_polish"]


# ---------------------------------------------------------------------------
# hausdorff_metric_applicable
# ---------------------------------------------------------------------------

class TestHausdorffMetricApplicable:
    def test_polish_space_applicable(self):
        sp = _sp("polish_space")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "polish"

    def test_completely_metrizable_applicable(self):
        sp = _sp("completely_metrizable")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true

    def test_cantor_set_applicable(self):
        sp = _sp("cantor_set")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true

    def test_compact_metrizable_applicable(self):
        sp = _sp("compact_metrizable", "metric")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true
        # compact_metrizable is in POLISH_BASE_TAGS → hits polish layer first
        assert r.metadata["criterion"] in ("polish", "compact_metrizable")

    def test_compact_with_metric_applicable(self):
        sp = _sp("compact", "metrizable")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true

    def test_locally_compact_metrizable_applicable(self):
        sp = _sp("real_line")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "locally_compact_metrizable"

    def test_metric_space_applicable(self):
        sp = _sp("metric")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "metrizable"

    def test_metrizable_applicable(self):
        sp = _sp("metrizable")
        r = hausdorff_metric_applicable(sp)
        assert r.is_true

    def test_unknown_no_tags(self):
        sp = _sp("connected", "compact")
        r = hausdorff_metric_applicable(sp)
        assert r.is_unknown

    def test_result_has_representation(self):
        sp = _sp("polish_space")
        r = hausdorff_metric_applicable(sp)
        assert "representation" in r.metadata


# ---------------------------------------------------------------------------
# hyperspace_is_compact
# ---------------------------------------------------------------------------

class TestHyperspaceIsCompact:
    def test_real_line_not_compact(self):
        sp = _sp("real_line")
        r = hyperspace_is_compact(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "not_compact_base"

    def test_not_compact_tag(self):
        sp = _sp("non_compact")
        r = hyperspace_is_compact(sp)
        assert r.is_false

    def test_irrationals_not_compact(self):
        sp = _sp("irrationals")
        r = hyperspace_is_compact(sp)
        assert r.is_false

    def test_compact_metrizable_compact(self):
        sp = _sp("compact_metrizable")
        r = hyperspace_is_compact(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "blaschke"

    def test_cantor_set_compact(self):
        sp = _sp("cantor_set")
        r = hyperspace_is_compact(sp)
        assert r.is_true

    def test_closed_interval_compact(self):
        sp = _sp("closed_interval")
        r = hyperspace_is_compact(sp)
        assert r.is_true

    def test_compact_with_metrizable_compact(self):
        sp = _sp("compact", "metrizable")
        r = hyperspace_is_compact(sp)
        assert r.is_true

    def test_polish_not_compact_is_false(self):
        sp = _sp("polish_space", "completely_metrizable")
        r = hyperspace_is_compact(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "polish_not_compact"

    def test_unknown_no_tags(self):
        sp = _sp("connected", "t2")
        r = hyperspace_is_compact(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# hyperspace_is_polish
# ---------------------------------------------------------------------------

class TestHyperspaceIsPolish:
    def test_compact_metrizable_polish(self):
        sp = _sp("compact_metrizable")
        r = hyperspace_is_polish(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "compact_metrizable"

    def test_cantor_set_polish(self):
        sp = _sp("cantor_set")
        r = hyperspace_is_polish(sp)
        assert r.is_true

    def test_closed_interval_polish(self):
        sp = _sp("closed_interval")
        r = hyperspace_is_polish(sp)
        assert r.is_true

    def test_polish_space_tag_polish(self):
        sp = _sp("polish_space")
        r = hyperspace_is_polish(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "polish"

    def test_completely_metrizable_polish(self):
        sp = _sp("completely_metrizable")
        r = hyperspace_is_polish(sp)
        assert r.is_true

    def test_real_line_polish(self):
        sp = _sp("real_line")
        r = hyperspace_is_polish(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "locally_compact_polish"

    def test_banach_space_polish(self):
        sp = _sp("banach_space")
        r = hyperspace_is_polish(sp)
        assert r.is_true

    def test_unknown_no_metrizable_tags(self):
        sp = _sp("compact", "connected")
        r = hyperspace_is_polish(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# vietoris_topology_hausdorff
# ---------------------------------------------------------------------------

class TestVietorisTopologyHausdorff:
    def test_hausdorff_base_hausdorff_vietoris(self):
        sp = _sp("hausdorff")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "hausdorff_base"

    def test_t2_base_hausdorff(self):
        sp = _sp("t2")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_true

    def test_metric_base_hausdorff(self):
        sp = _sp("metric")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_true

    def test_compact_hausdorff_hausdorff(self):
        sp = _sp("compact_hausdorff")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_true

    def test_polish_space_hausdorff(self):
        sp = _sp("polish_space")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_true

    def test_t1_not_t2_not_hausdorff(self):
        sp = _sp("t1")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "t1_not_t2"

    def test_unknown_no_separation_tags(self):
        sp = _sp("connected", "compact")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_unknown

    def test_normal_implies_hausdorff(self):
        sp = _sp("normal")
        r = vietoris_topology_hausdorff(sp)
        assert r.is_true


# ---------------------------------------------------------------------------
# hyperspace_is_connected
# ---------------------------------------------------------------------------

class TestHyperspaceIsConnected:
    def test_connected_base_connected(self):
        sp = _sp("connected")
        r = hyperspace_is_connected(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "connected_base"

    def test_path_connected_base_connected(self):
        sp = _sp("path_connected")
        r = hyperspace_is_connected(sp)
        assert r.is_true

    def test_real_line_connected(self):
        sp = _sp("real_line")
        r = hyperspace_is_connected(sp)
        assert r.is_true

    def test_closed_interval_connected(self):
        sp = _sp("closed_interval")
        r = hyperspace_is_connected(sp)
        assert r.is_true

    def test_cantor_set_disconnected(self):
        sp = _sp("cantor_set")
        r = hyperspace_is_connected(sp)
        assert r.is_false

    def test_totally_disconnected_disconnected(self):
        sp = _sp("totally_disconnected")
        r = hyperspace_is_connected(sp)
        assert r.is_false

    def test_zero_dimensional_disconnected(self):
        sp = _sp("zero_dimensional")
        r = hyperspace_is_connected(sp)
        assert r.is_false

    def test_discrete_disconnected(self):
        sp = _sp("discrete")
        r = hyperspace_is_connected(sp)
        assert r.is_false

    def test_disconnected_tag(self):
        sp = _sp("disconnected")
        r = hyperspace_is_connected(sp)
        assert r.is_false

    def test_unknown_no_connectedness_tags(self):
        sp = _sp("compact", "hausdorff")
        r = hyperspace_is_connected(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# classify_hyperspace
# ---------------------------------------------------------------------------

class TestClassifyHyperspace:
    def test_returns_dict(self):
        sp = _sp("compact_metrizable")
        result = classify_hyperspace(sp)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        sp = _sp("compact_metrizable")
        result = classify_hyperspace(sp)
        for key in ("hyperspace_type", "hausdorff_metric", "is_compact",
                    "is_polish", "vietoris_hausdorff", "is_connected",
                    "key_properties", "representation", "tags"):
            assert key in result

    def test_compact_metrizable_type(self):
        sp = _sp("compact_metrizable", "metric")
        result = classify_hyperspace(sp)
        assert result["hyperspace_type"] == "compact_polish"

    def test_cantor_set_compact_polish(self):
        sp = _sp("cantor_set")
        result = classify_hyperspace(sp)
        assert result["hyperspace_type"] == "compact_polish"

    def test_real_line_polish_not_compact(self):
        sp = _sp("real_line")
        result = classify_hyperspace(sp)
        assert result["hyperspace_type"] == "polish"

    def test_polish_space_polish_type(self):
        sp = _sp("polish_space")
        result = classify_hyperspace(sp)
        assert result["hyperspace_type"] in ("compact_polish", "polish")

    def test_metric_space_metrizable_type(self):
        sp = _sp("metric")
        result = classify_hyperspace(sp)
        assert result["hyperspace_type"] == "metrizable"

    def test_key_properties_compact_metrizable(self):
        sp = _sp("cantor_set")
        result = classify_hyperspace(sp)
        assert "compact" in result["key_properties"]
        assert "polish" in result["key_properties"]

    def test_key_properties_connected_real_line(self):
        sp = _sp("real_line")
        result = classify_hyperspace(sp)
        assert "connected" in result["key_properties"]

    def test_disconnected_in_key_properties_for_cantor(self):
        sp = _sp("cantor_set")
        result = classify_hyperspace(sp)
        assert "disconnected" in result["key_properties"]

    def test_results_are_result_instances(self):
        sp = _sp("compact_metrizable")
        result = classify_hyperspace(sp)
        assert isinstance(result["is_compact"], Result)
        assert isinstance(result["is_polish"], Result)
        assert isinstance(result["hausdorff_metric"], Result)

    def test_unknown_no_tags(self):
        sp = _sp()
        result = classify_hyperspace(sp)
        assert result["hyperspace_type"] == "unknown"


# ---------------------------------------------------------------------------
# hyperspace_profile (facade)
# ---------------------------------------------------------------------------

class TestHyperspaceProfileFacade:
    def test_returns_dict(self):
        sp = _sp("compact_metrizable")
        result = hyperspace_profile(sp)
        assert isinstance(result, dict)

    def test_has_classification_key(self):
        sp = _sp("compact_metrizable")
        result = hyperspace_profile(sp)
        assert "classification" in result

    def test_has_named_profiles_key(self):
        sp = _sp("compact_metrizable")
        result = hyperspace_profile(sp)
        assert "named_profiles" in result

    def test_has_layer_summary_key(self):
        sp = _sp("compact_metrizable")
        result = hyperspace_profile(sp)
        assert "layer_summary" in result

    def test_named_profiles_is_tuple(self):
        sp = _sp("compact_metrizable")
        result = hyperspace_profile(sp)
        assert isinstance(result["named_profiles"], tuple)

    def test_classification_is_dict(self):
        sp = _sp("compact_metrizable")
        result = hyperspace_profile(sp)
        assert isinstance(result["classification"], dict)


# ---------------------------------------------------------------------------
# Representation routing
# ---------------------------------------------------------------------------

class TestRepresentationRouting:
    def test_metadata_dict_path(self):
        sp = TopologicalSpace.symbolic(
            description="Hilbert cube hyperspace",
            representation="k_closed_interval_hilbert_cube",
            tags={"compact_metrizable"},
        )
        r = hyperspace_is_compact(sp)
        assert r.is_true
        assert "k_closed_interval_hilbert_cube" in r.metadata.get("representation", "")

    def test_attribute_path(self):
        sp = types.SimpleNamespace(tags={"polish_space"}, metadata={}, representation="k_reals")
        r = hyperspace_is_polish(sp)
        assert r.is_true
        assert "k_reals" in r.metadata.get("representation", "")

    def test_no_tags_fallback_to_set(self):
        r = hausdorff_metric_applicable(42)
        assert r.is_unknown
        assert r.metadata["tags"] == []


# ---------------------------------------------------------------------------
# Cross-theorem consistency
# ---------------------------------------------------------------------------

class TestCrossTheoremConsistency:
    def test_compact_metrizable_compact_and_polish(self):
        sp = _sp("compact_metrizable")
        assert hyperspace_is_compact(sp).is_true
        assert hyperspace_is_polish(sp).is_true

    def test_real_line_polish_not_compact(self):
        sp = _sp("real_line")
        assert hyperspace_is_compact(sp).is_false
        assert hyperspace_is_polish(sp).is_true

    def test_cantor_compact_disconnected(self):
        sp = _sp("cantor_set")
        assert hyperspace_is_compact(sp).is_true
        assert hyperspace_is_connected(sp).is_false

    def test_interval_compact_connected(self):
        sp = _sp("closed_interval")
        assert hyperspace_is_compact(sp).is_true
        assert hyperspace_is_connected(sp).is_true

    def test_hausdorff_metric_consistent_with_polish(self):
        sp = _sp("polish_space")
        hm = hausdorff_metric_applicable(sp)
        pol = hyperspace_is_polish(sp)
        assert hm.is_true
        assert pol.is_true

    def test_non_compact_not_compact_hyperspace(self):
        sp = _sp("non_compact", "metrizable")
        assert hyperspace_is_compact(sp).is_false
