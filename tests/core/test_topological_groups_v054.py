"""Tests for topological_groups.py (v0.5.4)."""
import pytest

from pytop.result import Result
from pytop.spaces import TopologicalSpace
from pytop.topological_groups import (
    ABELIAN_TAGS,
    COMPACT_GROUP_TAGS,
    CONTINUOUS_OP_TAGS,
    DISCRETE_GROUP_TAGS,
    GROUP_NEGATIVE_TAGS,
    GROUP_POSITIVE_TAGS,
    LC_GROUP_TAGS,
    LIE_GROUP_TAGS,
    LOCALLY_COMPACT_TAGS,
    PROFINITE_TAGS,
    TopologicalGroupProfile,
    classify_topological_group,
    get_named_topological_group_profiles,
    is_topological_group,
    topological_group_layer_summary,
    topological_group_profile,
    topological_group_separation,
    topological_group_type_index,
)


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

class TestTagConstants:
    def test_group_positive_tags_contains_topological_group(self):
        assert "topological_group" in GROUP_POSITIVE_TAGS

    def test_group_positive_tags_contains_lie_group(self):
        assert "lie_group" in GROUP_POSITIVE_TAGS

    def test_group_negative_tags_contains_not_group(self):
        assert "not_group" in GROUP_NEGATIVE_TAGS

    def test_lie_group_tags_contains_lie(self):
        assert "lie" in LIE_GROUP_TAGS

    def test_profinite_tags_contains_profinite(self):
        assert "profinite" in PROFINITE_TAGS

    def test_compact_group_tags_contains_compact_group(self):
        assert "compact_group" in COMPACT_GROUP_TAGS

    def test_abelian_tags_contains_abelian(self):
        assert "abelian" in ABELIAN_TAGS

    def test_discrete_group_tags_contains_discrete_group(self):
        assert "discrete_group" in DISCRETE_GROUP_TAGS

    def test_continuous_op_tags_contains_continuous_group_ops(self):
        assert "continuous_group_ops" in CONTINUOUS_OP_TAGS

    def test_locally_compact_tags_contains_locally_compact(self):
        assert "locally_compact" in LOCALLY_COMPACT_TAGS

    def test_lc_group_tags_contains_lca_group(self):
        assert "lca_group" in LC_GROUP_TAGS


# ---------------------------------------------------------------------------
# TopologicalGroupProfile dataclass
# ---------------------------------------------------------------------------

class TestTopologicalGroupProfile:
    def test_is_frozen(self):
        p = TopologicalGroupProfile(
            key="test", display_name="T", group_type="lie",
            presentation_layer="main_text", focus="test focus",
            separation_level="T3.5", chapter_targets=("1",),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "changed"

    def test_fields_accessible(self):
        p = TopologicalGroupProfile(
            key="k", display_name="D", group_type="compact",
            presentation_layer="advanced_note", focus="f",
            separation_level="T3.5", chapter_targets=("20",),
        )
        assert p.key == "k"
        assert p.separation_level == "T3.5"


# ---------------------------------------------------------------------------
# get_named_topological_group_profiles
# ---------------------------------------------------------------------------

class TestNamedProfiles:
    def test_returns_tuple(self):
        assert isinstance(get_named_topological_group_profiles(), tuple)

    def test_at_least_five_profiles(self):
        assert len(get_named_topological_group_profiles()) >= 5

    def test_all_are_profile_instances(self):
        for p in get_named_topological_group_profiles():
            assert isinstance(p, TopologicalGroupProfile)

    def test_real_lie_group_present(self):
        keys = {p.key for p in get_named_topological_group_profiles()}
        assert "real_lie_group" in keys

    def test_compact_lie_group_present(self):
        keys = {p.key for p in get_named_topological_group_profiles()}
        assert "compact_lie_group" in keys

    def test_profinite_group_present(self):
        keys = {p.key for p in get_named_topological_group_profiles()}
        assert "profinite_group" in keys

    def test_lca_group_present(self):
        keys = {p.key for p in get_named_topological_group_profiles()}
        assert "locally_compact_abelian_group" in keys

    def test_discrete_group_present(self):
        keys = {p.key for p in get_named_topological_group_profiles()}
        assert "discrete_group" in keys

    def test_all_separation_levels_are_t35(self):
        for p in get_named_topological_group_profiles():
            assert p.separation_level == "T3.5"


# ---------------------------------------------------------------------------
# topological_group_layer_summary
# ---------------------------------------------------------------------------

class TestLayerSummary:
    def test_returns_dict(self):
        assert isinstance(topological_group_layer_summary(), dict)

    def test_main_text_present(self):
        s = topological_group_layer_summary()
        assert s.get("main_text", 0) >= 1

    def test_advanced_note_present(self):
        s = topological_group_layer_summary()
        assert s.get("advanced_note", 0) >= 1

    def test_counts_are_positive(self):
        for v in topological_group_layer_summary().values():
            assert v > 0


# ---------------------------------------------------------------------------
# topological_group_type_index
# ---------------------------------------------------------------------------

class TestTypeIndex:
    def test_returns_dict(self):
        assert isinstance(topological_group_type_index(), dict)

    def test_lie_key_present(self):
        idx = topological_group_type_index()
        assert "lie" in idx or "compact_lie" in idx

    def test_values_are_tuples(self):
        for v in topological_group_type_index().values():
            assert isinstance(v, tuple)


# ---------------------------------------------------------------------------
# is_topological_group — positive cases
# ---------------------------------------------------------------------------

class TestIsTopologicalGroupPositive:
    def test_lie_group_tag_is_true(self):
        assert is_topological_group(_sp("lie_group")).is_true

    def test_lie_tag_is_true(self):
        assert is_topological_group(_sp("lie")).is_true

    def test_smooth_manifold_group_tag_is_true(self):
        assert is_topological_group(_sp("smooth_manifold_group")).is_true

    def test_profinite_tag_is_true(self):
        assert is_topological_group(_sp("profinite")).is_true

    def test_profinite_group_tag_is_true(self):
        assert is_topological_group(_sp("profinite_group")).is_true

    def test_compact_group_tag_is_true(self):
        assert is_topological_group(_sp("compact_group")).is_true

    def test_locally_compact_group_tag_is_true(self):
        assert is_topological_group(_sp("locally_compact_group")).is_true

    def test_lca_group_tag_is_true(self):
        assert is_topological_group(_sp("lca_group")).is_true

    def test_topological_group_tag_is_true(self):
        assert is_topological_group(_sp("topological_group")).is_true

    def test_abelian_tag_is_true(self):
        assert is_topological_group(_sp("abelian")).is_true

    def test_abelian_group_tag_is_true(self):
        assert is_topological_group(_sp("abelian_group")).is_true

    def test_discrete_group_tag_is_true(self):
        assert is_topological_group(_sp("discrete_group")).is_true

    def test_t0_plus_continuous_ops_is_true(self):
        assert is_topological_group(_sp("t0", "continuous_group_ops")).is_true

    def test_hausdorff_plus_continuous_multiplication_is_true(self):
        assert is_topological_group(_sp("hausdorff", "continuous_multiplication")).is_true

    def test_t4_plus_continuous_inversion_is_true(self):
        assert is_topological_group(_sp("t4", "continuous_inversion")).is_true

    def test_returns_result_instance(self):
        assert isinstance(is_topological_group(_sp("lie_group")), Result)

    def test_mode_is_theorem(self):
        assert is_topological_group(_sp("lie_group")).mode == "theorem"


# ---------------------------------------------------------------------------
# is_topological_group — criteria labels
# ---------------------------------------------------------------------------

class TestIsTopologicalGroupCriteria:
    def test_lie_criterion(self):
        r = is_topological_group(_sp("lie_group"))
        assert r.metadata.get("criterion") == "lie_group"

    def test_profinite_criterion(self):
        r = is_topological_group(_sp("profinite"))
        assert r.metadata.get("criterion") == "profinite"

    def test_compact_group_criterion(self):
        r = is_topological_group(_sp("compact_group"))
        assert r.metadata.get("criterion") == "compact_or_lc_group"

    def test_lca_group_criterion(self):
        r = is_topological_group(_sp("lca_group"))
        assert r.metadata.get("criterion") == "compact_or_lc_group"

    def test_direct_tag_criterion(self):
        r = is_topological_group(_sp("topological_group"))
        assert r.metadata.get("criterion") == "direct_tag"

    def test_axioms_via_tags_criterion(self):
        r = is_topological_group(_sp("t0", "continuous_group_ops"))
        assert r.metadata.get("criterion") == "axioms_via_tags"


# ---------------------------------------------------------------------------
# is_topological_group — negative / unknown
# ---------------------------------------------------------------------------

class TestIsTopologicalGroupNegativeUnknown:
    def test_not_group_is_false(self):
        assert is_topological_group(_sp("not_group")).is_false

    def test_not_topological_group_is_false(self):
        assert is_topological_group(_sp("not_topological_group")).is_false

    def test_semigroup_only_is_false(self):
        assert is_topological_group(_sp("semigroup_only")).is_false

    def test_no_tags_is_unknown(self):
        assert is_topological_group(_sp()).is_unknown

    def test_metric_alone_is_unknown(self):
        # metric space is not necessarily a group
        assert is_topological_group(_sp("metric")).is_unknown

    def test_compact_alone_is_unknown(self):
        # compact space is not necessarily a group
        assert is_topological_group(_sp("compact")).is_unknown

    def test_t0_alone_is_unknown(self):
        # T0 alone without continuous ops is unknown
        assert is_topological_group(_sp("t0")).is_unknown

    def test_continuous_ops_alone_is_unknown(self):
        # continuous ops without separation is unknown
        assert is_topological_group(_sp("continuous_group_ops")).is_unknown

    def test_criterion_none_when_false(self):
        r = is_topological_group(_sp("not_group"))
        assert r.metadata.get("criterion") is None

    def test_criterion_none_when_unknown(self):
        r = is_topological_group(_sp())
        assert r.metadata.get("criterion") is None


# ---------------------------------------------------------------------------
# topological_group_separation
# ---------------------------------------------------------------------------

class TestTopologicalGroupSeparation:
    def test_lie_group_is_tychonoff(self):
        r = topological_group_separation(_sp("lie_group"))
        assert r.is_true

    def test_lie_group_criterion(self):
        r = topological_group_separation(_sp("lie_group"))
        assert r.metadata.get("criterion") == "lie_group_metrizable"

    def test_profinite_is_tychonoff(self):
        r = topological_group_separation(_sp("profinite"))
        assert r.is_true

    def test_profinite_criterion(self):
        r = topological_group_separation(_sp("profinite"))
        assert r.metadata.get("criterion") == "profinite_compact_hausdorff"

    def test_compact_group_is_tychonoff(self):
        r = topological_group_separation(_sp("compact_group"))
        assert r.is_true

    def test_compact_group_criterion(self):
        r = topological_group_separation(_sp("compact_group"))
        assert r.metadata.get("criterion") == "compact_group_hausdorff"

    def test_discrete_group_is_tychonoff(self):
        r = topological_group_separation(_sp("discrete_group"))
        assert r.is_true

    def test_discrete_group_criterion(self):
        r = topological_group_separation(_sp("discrete_group"))
        assert r.metadata.get("criterion") == "discrete_group_metrizable"

    def test_topological_group_plus_t0_is_tychonoff(self):
        r = topological_group_separation(_sp("topological_group", "t0"))
        assert r.is_true

    def test_t0_group_criterion(self):
        r = topological_group_separation(_sp("topological_group", "t0"))
        assert r.metadata.get("criterion") == "t0_group_is_tychonoff"

    def test_topological_group_plus_hausdorff_is_tychonoff(self):
        r = topological_group_separation(_sp("topological_group", "hausdorff"))
        assert r.is_true

    def test_topological_group_plus_locally_compact_is_tychonoff(self):
        r = topological_group_separation(_sp("topological_group", "locally_compact"))
        assert r.is_true

    def test_topological_group_alone_is_unknown(self):
        # No separation tag → cannot apply T0-group theorem
        r = topological_group_separation(_sp("topological_group"))
        assert r.is_unknown

    def test_not_group_gives_unknown(self):
        r = topological_group_separation(_sp("not_group"))
        assert r.is_unknown

    def test_no_tags_gives_unknown(self):
        r = topological_group_separation(_sp())
        assert r.is_unknown

    def test_returns_result(self):
        r = topological_group_separation(_sp("lie_group"))
        assert isinstance(r, Result)

    def test_group_confirmed_true_in_metadata(self):
        r = topological_group_separation(_sp("lie_group"))
        assert r.metadata.get("group_confirmed") is True

    def test_group_confirmed_false_when_not_group(self):
        r = topological_group_separation(_sp("not_group"))
        assert r.metadata.get("group_confirmed") is False

    def test_value_is_tychonoff(self):
        r = topological_group_separation(_sp("lie_group"))
        assert r.value == "tychonoff"

    def test_mode_is_theorem_when_true(self):
        r = topological_group_separation(_sp("lie_group"))
        assert r.mode == "theorem"

    def test_justification_nonempty(self):
        r = topological_group_separation(_sp("profinite"))
        assert len(r.justification) >= 1


# ---------------------------------------------------------------------------
# classify_topological_group
# ---------------------------------------------------------------------------

class TestClassifyTopologicalGroup:
    def test_returns_dict(self):
        assert isinstance(classify_topological_group(_sp("lie_group")), dict)

    def test_has_required_keys(self):
        d = classify_topological_group(_sp("lie_group"))
        assert set(d.keys()) == {
            "group_type", "is_topological_group", "is_compact",
            "is_abelian", "is_discrete", "separation", "key_properties",
        }

    def test_lie_group_type(self):
        d = classify_topological_group(_sp("lie_group"))
        assert d["group_type"] == "lie"

    def test_compact_lie_type(self):
        d = classify_topological_group(_sp("lie_group", "compact"))
        assert d["group_type"] == "compact_lie"

    def test_profinite_type(self):
        d = classify_topological_group(_sp("profinite"))
        assert d["group_type"] == "profinite"

    def test_discrete_type(self):
        d = classify_topological_group(_sp("discrete_group"))
        assert d["group_type"] == "discrete"

    def test_compact_abelian_type(self):
        d = classify_topological_group(_sp("compact_group", "abelian", "compact"))
        assert d["group_type"] == "compact_abelian"

    def test_lca_type(self):
        d = classify_topological_group(_sp("lca_group", "abelian"))
        assert d["group_type"] == "locally_compact_abelian"

    def test_general_type(self):
        d = classify_topological_group(_sp("topological_group"))
        assert d["group_type"] == "general"

    def test_unknown_type_when_not_confirmed(self):
        d = classify_topological_group(_sp())
        assert d["group_type"] == "unknown"

    def test_is_compact_true_when_compact_tag(self):
        d = classify_topological_group(_sp("profinite"))
        assert d["is_compact"] is True

    def test_is_compact_none_when_unknown(self):
        d = classify_topological_group(_sp("topological_group"))
        assert d["is_compact"] is None

    def test_is_abelian_true(self):
        d = classify_topological_group(_sp("abelian_group"))
        assert d["is_abelian"] is True

    def test_is_abelian_false(self):
        d = classify_topological_group(_sp("topological_group", "not_abelian"))
        assert d["is_abelian"] is False

    def test_is_abelian_none_when_unknown(self):
        d = classify_topological_group(_sp("topological_group"))
        assert d["is_abelian"] is None

    def test_key_properties_contains_topological_group_when_true(self):
        d = classify_topological_group(_sp("lie_group"))
        assert "topological_group" in d["key_properties"]

    def test_key_properties_contains_tychonoff_for_lie(self):
        d = classify_topological_group(_sp("lie_group"))
        assert "tychonoff" in d["key_properties"]

    def test_key_properties_contains_lie_for_lie_group(self):
        d = classify_topological_group(_sp("lie_group"))
        assert "lie" in d["key_properties"]

    def test_key_properties_contains_profinite_for_profinite(self):
        d = classify_topological_group(_sp("profinite"))
        assert "profinite" in d["key_properties"]

    def test_key_properties_empty_when_unknown(self):
        d = classify_topological_group(_sp())
        assert d["key_properties"] == []

    def test_separation_is_result(self):
        d = classify_topological_group(_sp("lie_group"))
        assert isinstance(d["separation"], Result)

    def test_is_topological_group_is_result(self):
        d = classify_topological_group(_sp("lie_group"))
        assert isinstance(d["is_topological_group"], Result)


# ---------------------------------------------------------------------------
# topological_group_profile
# ---------------------------------------------------------------------------

class TestTopologicalGroupProfile:
    def test_returns_dict(self):
        d = topological_group_profile(_sp("lie_group"))
        assert isinstance(d, dict)

    def test_has_required_keys(self):
        d = topological_group_profile(_sp())
        assert set(d.keys()) == {"classification", "named_profiles", "layer_summary"}

    def test_classification_is_dict(self):
        d = topological_group_profile(_sp("lie_group"))
        assert isinstance(d["classification"], dict)

    def test_named_profiles_is_tuple(self):
        d = topological_group_profile(_sp())
        assert isinstance(d["named_profiles"], tuple)

    def test_named_profiles_at_least_five(self):
        d = topological_group_profile(_sp())
        assert len(d["named_profiles"]) >= 5

    def test_layer_summary_is_dict(self):
        d = topological_group_profile(_sp())
        assert isinstance(d["layer_summary"], dict)

    def test_layer_summary_positive_counts(self):
        d = topological_group_profile(_sp())
        for v in d["layer_summary"].values():
            assert v > 0

    def test_lie_group_classification_type(self):
        d = topological_group_profile(_sp("lie_group"))
        assert d["classification"]["group_type"] == "lie"
