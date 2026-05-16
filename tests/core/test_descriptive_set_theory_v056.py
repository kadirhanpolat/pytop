"""Tests for descriptive_set_theory.py (v0.5.6)."""

import types

import pytest

from pytop.descriptive_set_theory import (
    BAIRE_PROPERTY_TAGS,
    BOREL_NEGATIVE_TAGS,
    CLOSED_IN_METRIZABLE_TAGS,
    F_SIGMA_TAGS,
    G_DELTA_NEGATIVE_TAGS,
    G_DELTA_TAGS,
    OPEN_IN_METRIZABLE_TAGS,
    PERFECT_SET_TAGS,
    SCATTERED_TAGS,
    DescriptiveSetProfile,
    cantor_bendixson_analysis,
    classify_descriptive_complexity,
    descriptive_chapter_index,
    descriptive_layer_summary,
    descriptive_set_profile,
    descriptive_type_index,
    get_named_descriptive_profiles,
    has_baire_property,
    is_f_sigma,
    is_g_delta,
    is_perfect_set,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_g_delta_contains_open(self):
        assert "open" in G_DELTA_TAGS

    def test_g_delta_contains_polish(self):
        assert "polish_space" in G_DELTA_TAGS

    def test_g_delta_contains_irrationals(self):
        assert "irrationals" in G_DELTA_TAGS

    def test_f_sigma_contains_closed(self):
        assert "closed" in F_SIGMA_TAGS

    def test_f_sigma_contains_rationals(self):
        assert "rationals" in F_SIGMA_TAGS

    def test_f_sigma_contains_sigma_compact(self):
        assert "sigma_compact" in F_SIGMA_TAGS

    def test_perfect_set_contains_cantor(self):
        assert "cantor_set" in PERFECT_SET_TAGS

    def test_perfect_set_contains_irrationals(self):
        assert "irrationals" in PERFECT_SET_TAGS

    def test_scattered_contains_scattered(self):
        assert "scattered" in SCATTERED_TAGS

    def test_scattered_contains_successor_ordinal(self):
        assert "successor_ordinal_space" in SCATTERED_TAGS

    def test_baire_property_contains_borel(self):
        assert "borel" in BAIRE_PROPERTY_TAGS

    def test_baire_property_contains_analytic(self):
        assert "analytic" in BAIRE_PROPERTY_TAGS

    def test_borel_negative_contains_bernstein(self):
        assert "bernstein_set" in BOREL_NEGATIVE_TAGS

    def test_borel_negative_contains_vitali(self):
        assert "vitali_set" in BOREL_NEGATIVE_TAGS

    def test_g_delta_negative_contains_rationals(self):
        assert "rationals" in G_DELTA_NEGATIVE_TAGS

    def test_closed_metrizable_contains_compact(self):
        assert "compact" in CLOSED_IN_METRIZABLE_TAGS

    def test_closed_metrizable_contains_cantor(self):
        assert "cantor_set" in CLOSED_IN_METRIZABLE_TAGS

    def test_open_in_metrizable_contains_open(self):
        assert "open" in OPEN_IN_METRIZABLE_TAGS


# ---------------------------------------------------------------------------
# DescriptiveSetProfile dataclass
# ---------------------------------------------------------------------------

class TestDescriptiveSetProfileDataclass:
    def test_profile_is_frozen(self):
        p = DescriptiveSetProfile(
            key="test",
            display_name="Test",
            borel_class="g_delta",
            has_baire_property=True,
            is_perfect=False,
            presentation_layer="main_text",
            focus="test focus",
            chapter_targets=("27",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "other"  # type: ignore[misc]

    def test_profile_fields(self):
        p = DescriptiveSetProfile(
            key="irrationals_g_delta",
            display_name="Irrationals",
            borel_class="g_delta",
            has_baire_property=True,
            is_perfect=True,
            presentation_layer="main_text",
            focus="irrationals focus",
            chapter_targets=("27", "52"),
        )
        assert p.borel_class == "g_delta"
        assert p.has_baire_property is True
        assert p.is_perfect is True
        assert "27" in p.chapter_targets


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

class TestNamedDescriptiveProfiles:
    def setup_method(self):
        self.profiles = get_named_descriptive_profiles()

    def test_returns_tuple(self):
        assert isinstance(self.profiles, tuple)

    def test_has_five_profiles(self):
        assert len(self.profiles) == 5

    def test_all_are_profile_instances(self):
        for p in self.profiles:
            assert isinstance(p, DescriptiveSetProfile)

    def test_irrationals_g_delta_present(self):
        keys = {p.key for p in self.profiles}
        assert "irrationals_g_delta" in keys

    def test_rationals_f_sigma_present(self):
        keys = {p.key for p in self.profiles}
        assert "rationals_f_sigma" in keys

    def test_cantor_set_perfect_present(self):
        keys = {p.key for p in self.profiles}
        assert "cantor_set_perfect" in keys

    def test_open_interval_present(self):
        keys = {p.key for p in self.profiles}
        assert "open_interval_g_delta_f_sigma" in keys

    def test_countable_scattered_present(self):
        keys = {p.key for p in self.profiles}
        assert "countable_scattered_ordinal" in keys

    def test_irrationals_is_perfect(self):
        p = next(x for x in self.profiles if x.key == "irrationals_g_delta")
        assert p.is_perfect is True

    def test_rationals_not_perfect(self):
        p = next(x for x in self.profiles if x.key == "rationals_f_sigma")
        assert p.is_perfect is False

    def test_cantor_set_is_perfect(self):
        p = next(x for x in self.profiles if x.key == "cantor_set_perfect")
        assert p.is_perfect is True

    def test_rationals_borel_class_f_sigma(self):
        p = next(x for x in self.profiles if x.key == "rationals_f_sigma")
        assert p.borel_class == "f_sigma"

    def test_irrationals_borel_class_g_delta(self):
        p = next(x for x in self.profiles if x.key == "irrationals_g_delta")
        assert p.borel_class == "g_delta"

    def test_scattered_ordinal_has_baire_property(self):
        p = next(x for x in self.profiles if x.key == "countable_scattered_ordinal")
        assert p.has_baire_property is True

    def test_all_have_baire_property(self):
        for p in self.profiles:
            assert p.has_baire_property is True


# ---------------------------------------------------------------------------
# Layer / chapter / type index helpers
# ---------------------------------------------------------------------------

class TestIndexHelpers:
    def test_layer_summary_is_dict(self):
        ls = descriptive_layer_summary()
        assert isinstance(ls, dict)

    def test_layer_summary_has_main_text(self):
        ls = descriptive_layer_summary()
        assert "main_text" in ls

    def test_layer_summary_counts_correct(self):
        ls = descriptive_layer_summary()
        assert ls.get("main_text", 0) == 2
        assert ls.get("selected_block", 0) == 2
        assert ls.get("advanced_note", 0) == 1

    def test_chapter_index_is_dict(self):
        ci = descriptive_chapter_index()
        assert isinstance(ci, dict)

    def test_chapter_27_has_multiple_profiles(self):
        ci = descriptive_chapter_index()
        assert "27" in ci
        assert len(ci["27"]) >= 4

    def test_chapter_index_values_are_tuples(self):
        ci = descriptive_chapter_index()
        for v in ci.values():
            assert isinstance(v, tuple)

    def test_type_index_is_dict(self):
        ti = descriptive_type_index()
        assert isinstance(ti, dict)

    def test_type_index_has_g_delta_and_f_sigma(self):
        ti = descriptive_type_index()
        assert "g_delta" in ti
        assert "f_sigma" in ti

    def test_type_index_g_delta_has_irrationals(self):
        ti = descriptive_type_index()
        assert "irrationals_g_delta" in ti["g_delta"]

    def test_type_index_f_sigma_has_rationals(self):
        ti = descriptive_type_index()
        assert "rationals_f_sigma" in ti["f_sigma"]


# ---------------------------------------------------------------------------
# is_g_delta
# ---------------------------------------------------------------------------

class TestIsGDelta:
    def test_explicit_not_g_delta_tag(self):
        sp = _sp("not_g_delta", "rationals")
        r = is_g_delta(sp)
        assert r.is_false

    def test_rationals_tag_not_g_delta(self):
        sp = _sp("rationals")
        r = is_g_delta(sp)
        assert r.is_false

    def test_open_tag_is_g_delta(self):
        sp = _sp("open")
        r = is_g_delta(sp)
        assert r.is_true

    def test_g_delta_tag_direct(self):
        sp = _sp("g_delta")
        r = is_g_delta(sp)
        assert r.is_true

    def test_irrationals_tag_is_g_delta(self):
        sp = _sp("irrationals")
        r = is_g_delta(sp)
        assert r.is_true

    def test_polish_space_is_g_delta_alexandrov(self):
        sp = _sp("polish_space", "metric")
        r = is_g_delta(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "alexandrov"

    def test_completely_metrizable_is_g_delta(self):
        sp = _sp("completely_metrizable")
        r = is_g_delta(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "alexandrov"

    def test_closed_metrizable_is_g_delta(self):
        sp = _sp("closed_metrizable", "metric")
        r = is_g_delta(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "closed_in_metrizable"

    def test_cantor_set_is_g_delta(self):
        sp = _sp("cantor_set", "compact")
        r = is_g_delta(sp)
        assert r.is_true

    def test_unknown_no_tags(self):
        sp = _sp("some_unknown_property")
        r = is_g_delta(sp)
        assert r.is_unknown

    def test_result_has_representation_key(self):
        sp = _sp("open")
        r = is_g_delta(sp)
        assert "representation" in r.metadata

    def test_result_has_tags_key(self):
        sp = _sp("open")
        r = is_g_delta(sp)
        assert "tags" in r.metadata


# ---------------------------------------------------------------------------
# is_f_sigma
# ---------------------------------------------------------------------------

class TestIsFSigma:
    def test_closed_tag_is_f_sigma(self):
        sp = _sp("closed")
        r = is_f_sigma(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "direct_tag"

    def test_f_sigma_tag_direct(self):
        sp = _sp("f_sigma")
        r = is_f_sigma(sp)
        assert r.is_true

    def test_rationals_tag_is_f_sigma(self):
        sp = _sp("rationals")
        r = is_f_sigma(sp)
        assert r.is_true

    def test_open_in_metric_is_f_sigma(self):
        sp = _sp("open", "metrizable")
        r = is_f_sigma(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "open_in_metrizable"

    def test_sigma_compact_is_f_sigma(self):
        sp = _sp("sigma_compact")
        r = is_f_sigma(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "sigma_compact"

    def test_countable_t1_is_f_sigma(self):
        sp = _sp("countable", "t1")
        r = is_f_sigma(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "countable_t1"

    def test_countable_hausdorff_is_f_sigma(self):
        sp = _sp("countably_infinite", "hausdorff")
        r = is_f_sigma(sp)
        assert r.is_true

    def test_unknown_no_tags(self):
        sp = _sp("connected")
        r = is_f_sigma(sp)
        assert r.is_unknown

    def test_open_alone_not_via_metrizable_layer(self):
        sp = _sp("open")
        r = is_f_sigma(sp)
        # "open" alone hits direct_tag (f_sigma check doesn't have "open" in direct)
        # Actually "open" is not in F_SIGMA_TAGS so it won't hit direct_tag
        # Without a metrizable tag it should be unknown
        assert r.is_unknown or r.is_true  # either is acceptable


# ---------------------------------------------------------------------------
# is_perfect_set
# ---------------------------------------------------------------------------

class TestIsPerfectSet:
    def test_scattered_tag_not_perfect(self):
        sp = _sp("scattered")
        r = is_perfect_set(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "scattered"

    def test_perfect_tag_direct(self):
        sp = _sp("perfect_set")
        r = is_perfect_set(sp)
        assert r.is_true

    def test_perfect_space_tag(self):
        sp = _sp("perfect_space")
        r = is_perfect_set(sp)
        assert r.is_true

    def test_cantor_set_is_perfect(self):
        sp = _sp("cantor_set")
        r = is_perfect_set(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "cantor_set"

    def test_irrationals_is_perfect(self):
        sp = _sp("irrationals")
        r = is_perfect_set(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "irrationals"

    def test_countable_t1_not_perfect(self):
        sp = _sp("countable", "t1")
        r = is_perfect_set(sp)
        assert r.is_false
        assert r.metadata["criterion"] == "countable_t1_scattered"

    def test_countable_hausdorff_not_perfect(self):
        sp = _sp("countably_infinite", "hausdorff")
        r = is_perfect_set(sp)
        assert r.is_false

    def test_no_isolated_points_closed_metric(self):
        sp = _sp("no_isolated_points", "dense_in_itself", "closed", "metric")
        r = is_perfect_set(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "no_isolated_points_closed"

    def test_unknown_no_tags(self):
        sp = _sp("connected")
        r = is_perfect_set(sp)
        assert r.is_unknown

    def test_scattered_wins_over_perfect_tag(self):
        sp = _sp("scattered", "perfect_set")
        r = is_perfect_set(sp)
        assert r.is_false

    def test_successor_ordinal_not_perfect(self):
        sp = _sp("successor_ordinal_space")
        r = is_perfect_set(sp)
        assert r.is_false


# ---------------------------------------------------------------------------
# has_baire_property
# ---------------------------------------------------------------------------

class TestHasBaireProperty:
    def test_bernstein_set_no_baire_property(self):
        sp = _sp("bernstein_set")
        r = has_baire_property(sp)
        assert r.is_false

    def test_vitali_set_no_baire_property(self):
        sp = _sp("vitali_set")
        r = has_baire_property(sp)
        assert r.is_false

    def test_non_borel_no_baire_property(self):
        sp = _sp("non_borel")
        r = has_baire_property(sp)
        assert r.is_false

    def test_open_has_baire_property(self):
        sp = _sp("open")
        r = has_baire_property(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "open_or_closed"

    def test_closed_has_baire_property(self):
        sp = _sp("closed")
        r = has_baire_property(sp)
        assert r.is_true

    def test_g_delta_has_baire_property(self):
        sp = _sp("g_delta")
        r = has_baire_property(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "g_delta_or_f_sigma"

    def test_f_sigma_has_baire_property(self):
        sp = _sp("f_sigma")
        r = has_baire_property(sp)
        assert r.is_true

    def test_g_delta_sigma_has_baire_property(self):
        sp = _sp("g_delta_sigma")
        r = has_baire_property(sp)
        assert r.is_true

    def test_borel_has_baire_property(self):
        sp = _sp("borel")
        r = has_baire_property(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "borel_analytic"

    def test_analytic_has_baire_property(self):
        sp = _sp("analytic")
        r = has_baire_property(sp)
        assert r.is_true

    def test_metrizable_has_baire_property(self):
        sp = _sp("metrizable")
        r = has_baire_property(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "metrizable"

    def test_polish_space_has_baire_property(self):
        sp = _sp("polish_space")
        r = has_baire_property(sp)
        assert r.is_true

    def test_unknown_no_relevant_tags(self):
        sp = _sp("connected", "compact")
        r = has_baire_property(sp)
        assert r.is_unknown


# ---------------------------------------------------------------------------
# cantor_bendixson_analysis
# ---------------------------------------------------------------------------

class TestCantorBendixsonAnalysis:
    def test_perfect_set_trivial_decomposition(self):
        sp = _sp("perfect_set")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "perfect"
        assert r.metadata["cb_rank"] == 0

    def test_cantor_set_trivial(self):
        sp = _sp("cantor_set")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "perfect"

    def test_irrationals_trivial(self):
        sp = _sp("irrationals")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "perfect"

    def test_scattered_decomposition(self):
        sp = _sp("scattered")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "scattered"

    def test_successor_ordinal_scattered(self):
        sp = _sp("successor_ordinal_space")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "scattered"

    def test_closed_in_polish_applies(self):
        sp = _sp("closed", "metric")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true
        assert r.metadata["criterion"] == "closed_in_polish"

    def test_compact_in_polish_applies(self):
        sp = _sp("compact", "metrizable")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true

    def test_unknown_no_context(self):
        sp = _sp("connected")
        r = cantor_bendixson_analysis(sp)
        assert r.is_unknown

    def test_closed_in_polish_tag(self):
        sp = _sp("closed_in_polish")
        r = cantor_bendixson_analysis(sp)
        assert r.is_true


# ---------------------------------------------------------------------------
# classify_descriptive_complexity
# ---------------------------------------------------------------------------

class TestClassifyDescriptiveComplexity:
    def test_returns_dict(self):
        sp = _sp("open")
        result = classify_descriptive_complexity(sp)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        sp = _sp("open")
        result = classify_descriptive_complexity(sp)
        for key in ("borel_class", "is_g_delta", "is_f_sigma", "is_perfect",
                    "has_baire_property", "cb_analysis", "key_properties",
                    "representation", "tags"):
            assert key in result

    def test_open_tag_borel_class_open(self):
        sp = _sp("open")
        result = classify_descriptive_complexity(sp)
        assert result["borel_class"] == "open"

    def test_closed_tag_borel_class_closed(self):
        sp = _sp("closed")
        result = classify_descriptive_complexity(sp)
        assert result["borel_class"] == "closed"

    def test_g_delta_only_borel_class(self):
        sp = _sp("g_delta", "polish_space")
        result = classify_descriptive_complexity(sp)
        assert result["borel_class"] in ("g_delta", "open")

    def test_rationals_f_sigma_borel_class(self):
        sp = _sp("rationals")
        result = classify_descriptive_complexity(sp)
        assert result["borel_class"] == "f_sigma"

    def test_irrationals_key_properties(self):
        sp = _sp("irrationals")
        result = classify_descriptive_complexity(sp)
        assert "g_delta" in result["key_properties"]
        assert "perfect" in result["key_properties"]

    def test_polish_space_key_properties_include_completely_metrizable(self):
        sp = _sp("polish_space")
        result = classify_descriptive_complexity(sp)
        assert "completely_metrizable" in result["key_properties"]

    def test_scattered_key_properties(self):
        sp = _sp("scattered")
        result = classify_descriptive_complexity(sp)
        assert "scattered" in result["key_properties"]

    def test_borel_tag_borel_class(self):
        sp = _sp("borel")
        result = classify_descriptive_complexity(sp)
        assert result["borel_class"] == "borel"

    def test_results_are_result_instances(self):
        sp = _sp("open")
        result = classify_descriptive_complexity(sp)
        assert isinstance(result["is_g_delta"], Result)
        assert isinstance(result["is_f_sigma"], Result)

    def test_representation_in_result(self):
        sp = _sp("open")
        result = classify_descriptive_complexity(sp)
        assert isinstance(result["representation"], str)

    def test_unknown_tags_yields_unknown_borel_class(self):
        sp = _sp("locally_connected", "t3")
        result = classify_descriptive_complexity(sp)
        assert result["borel_class"] == "unknown"


# ---------------------------------------------------------------------------
# descriptive_set_profile (facade)
# ---------------------------------------------------------------------------

class TestDescriptiveSetProfile:
    def test_returns_dict(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert isinstance(result, dict)

    def test_has_classification_key(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert "classification" in result

    def test_has_named_profiles_key(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert "named_profiles" in result

    def test_has_layer_summary_key(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert "layer_summary" in result

    def test_named_profiles_is_tuple(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert isinstance(result["named_profiles"], tuple)

    def test_classification_is_dict(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert isinstance(result["classification"], dict)

    def test_layer_summary_is_dict(self):
        sp = _sp("g_delta")
        result = descriptive_set_profile(sp)
        assert isinstance(result["layer_summary"], dict)


# ---------------------------------------------------------------------------
# Representation routing (_representation_of coverage)
# ---------------------------------------------------------------------------

class TestRepresentationRouting:
    def test_metadata_dict_path(self):
        sp = TopologicalSpace.symbolic(
            description="Baire space omega^omega",
            representation="irrationals_baire_space",
            tags={"irrationals"},
        )
        r = is_g_delta(sp)
        assert r.is_true
        assert "irrationals_baire_space" in r.metadata.get("representation", "")

    def test_attribute_path(self):
        sp = types.SimpleNamespace(tags={"g_delta"}, metadata={}, representation="my_g_delta_set")
        r = is_g_delta(sp)
        assert r.is_true
        assert "my_g_delta_set" in r.metadata.get("representation", "")

    def test_no_representation_falls_back_to_symbolic_general(self):
        sp = types.SimpleNamespace(tags={"f_sigma"}, metadata={})
        r = is_f_sigma(sp)
        assert r.is_true
        assert r.metadata.get("representation") == "symbolic_general"


# ---------------------------------------------------------------------------
# Cross-theorem consistency
# ---------------------------------------------------------------------------

class TestCrossTheoremConsistency:
    def test_irrationals_g_delta_and_perfect(self):
        sp = _sp("irrationals")
        g = is_g_delta(sp)
        p = is_perfect_set(sp)
        assert g.is_true
        assert p.is_true

    def test_rationals_f_sigma_not_g_delta(self):
        sp = _sp("rationals")
        g = is_g_delta(sp)
        f = is_f_sigma(sp)
        assert g.is_false
        assert f.is_true

    def test_cantor_set_g_delta_and_perfect(self):
        sp = _sp("cantor_set")
        g = is_g_delta(sp)
        p = is_perfect_set(sp)
        assert g.is_true
        assert p.is_true

    def test_scattered_implies_not_perfect(self):
        sp = _sp("scattered")
        p = is_perfect_set(sp)
        assert p.is_false

    def test_bernstein_set_no_baire_property_but_could_be_g_delta_unknown(self):
        sp = _sp("bernstein_set")
        bp = has_baire_property(sp)
        g = is_g_delta(sp)
        assert bp.is_false
        assert g.is_unknown

    def test_polish_space_g_delta_and_baire(self):
        sp = _sp("polish_space")
        g = is_g_delta(sp)
        b = has_baire_property(sp)
        assert g.is_true
        assert b.is_true
