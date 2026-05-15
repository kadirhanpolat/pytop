"""Tests for metrization_profiles.py."""

import pytest
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.metrization_profiles import (
    MetrizationProfile,
    MetrizationError,
    analyze_metrization,
    get_named_metrization_profiles,
    is_metrizable,
    metrization_chapter_index,
    metrization_layer_summary,
    metrization_profile,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace

X3 = [1, 2, 3]
DISCRETE_TOP = [set(), {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}]
SIER_TOP = [set(), {1}, {1,2}, {1,2,3}]


def _fsp(carrier, topology):
    return FiniteTopologicalSpace(
        carrier=frozenset(carrier),
        topology=tuple(frozenset(s) for s in topology),
    )


def _symbolic(**tags):
    return TopologicalSpace(carrier=None, tags=set(tags.keys()) if tags else set())


# ---------------------------------------------------------------------------
# MetrizationProfile
# ---------------------------------------------------------------------------

class TestMetrizationProfile:
    def test_is_frozen_dataclass(self):
        p = MetrizationProfile(
            key="test",
            display_name="Test",
            criterion_family="classical",
            presentation_layer="main_text",
            focus="testing",
            chapter_targets=("1",),
        )
        assert p.key == "test"

    def test_immutable(self):
        p = MetrizationProfile(
            key="test", display_name="T", criterion_family="c",
            presentation_layer="p", focus="f", chapter_targets=(),
        )
        with pytest.raises((AttributeError, TypeError)):
            p.key = "changed"


# ---------------------------------------------------------------------------
# get_named_metrization_profiles
# ---------------------------------------------------------------------------

class TestGetNamedMetrizationProfiles:
    def test_returns_tuple(self):
        profiles = get_named_metrization_profiles()
        assert isinstance(profiles, tuple)

    def test_at_least_three_profiles(self):
        assert len(get_named_metrization_profiles()) >= 3

    def test_all_are_metrization_profile(self):
        for p in get_named_metrization_profiles():
            assert isinstance(p, MetrizationProfile)

    def test_urysohn_route_present(self):
        keys = {p.key for p in get_named_metrization_profiles()}
        assert "urysohn_second_countable_regular_route" in keys

    def test_compact_hausdorff_route_present(self):
        keys = {p.key for p in get_named_metrization_profiles()}
        assert "compact_hausdorff_second_countable_route" in keys


# ---------------------------------------------------------------------------
# metrization_layer_summary
# ---------------------------------------------------------------------------

class TestMetrizationLayerSummary:
    def test_returns_dict(self):
        s = metrization_layer_summary()
        assert isinstance(s, dict)

    def test_counts_are_positive(self):
        for v in metrization_layer_summary().values():
            assert v > 0


# ---------------------------------------------------------------------------
# metrization_chapter_index
# ---------------------------------------------------------------------------

class TestMetrizationChapterIndex:
    def test_returns_dict(self):
        idx = metrization_chapter_index()
        assert isinstance(idx, dict)

    def test_chapter_23_present(self):
        idx = metrization_chapter_index()
        assert "23" in idx

    def test_values_are_tuples(self):
        for v in metrization_chapter_index().values():
            assert isinstance(v, tuple)


# ---------------------------------------------------------------------------
# is_metrizable — finite spaces
# ---------------------------------------------------------------------------

class TestIsMetrizableFinite:
    def test_discrete_space_is_metrizable(self):
        r = is_metrizable(_fsp(X3, DISCRETE_TOP))
        assert r.is_true

    def test_discrete_mode_is_exact(self):
        r = is_metrizable(_fsp(X3, DISCRETE_TOP))
        assert r.mode == "exact"

    def test_sierpinski_space_not_metrizable(self):
        r = is_metrizable(_fsp(X3, SIER_TOP))
        assert r.is_false

    def test_returns_result_instance(self):
        r = is_metrizable(_fsp(X3, DISCRETE_TOP))
        assert isinstance(r, Result)


# ---------------------------------------------------------------------------
# is_metrizable — symbolic spaces via tags
# ---------------------------------------------------------------------------

class TestIsMetrizableSymbolic:
    def test_metrizable_tag_gives_true(self):
        sp = TopologicalSpace(carrier=None, tags={"metrizable"})
        assert is_metrizable(sp).is_true

    def test_not_metrizable_tag_gives_false(self):
        sp = TopologicalSpace(carrier=None, tags={"not_metrizable"})
        assert is_metrizable(sp).is_false

    def test_not_hausdorff_tag_gives_false(self):
        sp = TopologicalSpace(carrier=None, tags={"not_hausdorff"})
        assert is_metrizable(sp).is_false

    def test_second_countable_plus_regular_gives_true(self):
        sp = TopologicalSpace(carrier=None, tags={"second_countable", "regular"})
        assert is_metrizable(sp).is_true

    def test_second_countable_plus_t3_gives_true(self):
        sp = TopologicalSpace(carrier=None, tags={"second_countable", "t3"})
        assert is_metrizable(sp).is_true

    def test_second_countable_alone_gives_unknown(self):
        sp = TopologicalSpace(carrier=None, tags={"second_countable"})
        assert is_metrizable(sp).is_unknown

    def test_no_tags_gives_unknown(self):
        sp = TopologicalSpace(carrier=None, tags=set())
        assert is_metrizable(sp).is_unknown

    def test_metric_tag_gives_true(self):
        sp = TopologicalSpace(carrier=None, tags={"metric"})
        assert is_metrizable(sp).is_true


# ---------------------------------------------------------------------------
# metrization_profile
# ---------------------------------------------------------------------------

class TestMetrizationProfileFn:
    def test_returns_dict(self):
        p = metrization_profile(_fsp(X3, DISCRETE_TOP))
        assert isinstance(p, dict)

    def test_has_is_metrizable_key(self):
        p = metrization_profile(_fsp(X3, DISCRETE_TOP))
        assert "is_metrizable" in p

    def test_has_criterion_key(self):
        p = metrization_profile(_fsp(X3, DISCRETE_TOP))
        assert "criterion" in p

    def test_has_named_profiles_key(self):
        p = metrization_profile(_fsp(X3, DISCRETE_TOP))
        assert "named_profiles" in p
        assert len(p["named_profiles"]) >= 3

    def test_urysohn_criterion_detected(self):
        sp = TopologicalSpace(carrier=None, tags={"second_countable", "t3"})
        p = metrization_profile(sp)
        assert p["criterion"] == "urysohn_metrization"


# ---------------------------------------------------------------------------
# analyze_metrization
# ---------------------------------------------------------------------------

class TestAnalyzeMetrization:
    def test_returns_result(self):
        r = analyze_metrization(_fsp(X3, DISCRETE_TOP))
        assert isinstance(r, Result)

    def test_discrete_space_is_true(self):
        r = analyze_metrization(_fsp(X3, DISCRETE_TOP))
        assert r.is_true

    def test_sierpinski_is_false(self):
        r = analyze_metrization(_fsp(X3, SIER_TOP))
        assert r.is_false

    def test_result_value_is_metrization_analysis(self):
        r = analyze_metrization(_fsp(X3, DISCRETE_TOP))
        assert r.value == "metrization_analysis"

    def test_metadata_has_is_metrizable(self):
        r = analyze_metrization(_fsp(X3, DISCRETE_TOP))
        assert "is_metrizable" in r.metadata

    def test_metadata_has_named_profile_keys(self):
        r = analyze_metrization(_fsp(X3, DISCRETE_TOP))
        assert "named_profile_keys" in r.metadata
        assert len(r.metadata["named_profile_keys"]) >= 3
