"""Tests for Nagata-Smirnov and Bing metrization criteria (v0.5.4)."""
import pytest

from pytop.metrization_profiles import (
    BING_TAGS,
    NAGATA_SMIRNOV_TAGS,
    REGULAR_TAGS,
    check_bing_metrization,
    check_nagata_smirnov,
    get_named_metrization_profiles,
    is_metrizable,
    metrization_theorem_check,
)
from pytop.result import Result
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

class TestNewConstants:
    def test_regular_tags_contains_t3(self):
        assert "t3" in REGULAR_TAGS

    def test_regular_tags_contains_regular(self):
        assert "regular" in REGULAR_TAGS

    def test_nagata_smirnov_tags_contains_sigma_lf(self):
        assert "sigma_locally_finite_base" in NAGATA_SMIRNOV_TAGS

    def test_nagata_smirnov_tags_contains_alias(self):
        assert "sigma_lf_base" in NAGATA_SMIRNOV_TAGS

    def test_bing_tags_contains_sigma_discrete(self):
        assert "sigma_discrete_base" in BING_TAGS

    def test_bing_tags_contains_alias(self):
        assert "sigma_d_base" in BING_TAGS


# ---------------------------------------------------------------------------
# New named profiles in registry
# ---------------------------------------------------------------------------

class TestNewNamedProfiles:
    def test_at_least_five_profiles(self):
        assert len(get_named_metrization_profiles()) >= 5

    def test_nagata_smirnov_profile_present(self):
        keys = {p.key for p in get_named_metrization_profiles()}
        assert "nagata_smirnov_sigma_lf_base_route" in keys

    def test_bing_profile_present(self):
        keys = {p.key for p in get_named_metrization_profiles()}
        assert "bing_sigma_discrete_base_route" in keys

    def test_nagata_smirnov_criterion_family(self):
        profiles = {p.key: p for p in get_named_metrization_profiles()}
        assert profiles["nagata_smirnov_sigma_lf_base_route"].criterion_family == "sigma_locally_finite"

    def test_bing_criterion_family(self):
        profiles = {p.key: p for p in get_named_metrization_profiles()}
        assert profiles["bing_sigma_discrete_base_route"].criterion_family == "sigma_discrete"


# ---------------------------------------------------------------------------
# is_metrizable — Layer 5 (Nagata-Smirnov)
# ---------------------------------------------------------------------------

class TestIsMetrizableNagataSmirnov:
    def test_t3_plus_sigma_lf_base_is_true(self):
        r = is_metrizable(_sp("t3", "sigma_locally_finite_base"))
        assert r.is_true

    def test_regular_plus_sigma_lf_base_is_true(self):
        r = is_metrizable(_sp("regular", "sigma_locally_finite_base"))
        assert r.is_true

    def test_sigma_lf_base_alias_recognized(self):
        r = is_metrizable(_sp("t3", "sigma_lf_base"))
        assert r.is_true

    def test_nagata_smirnov_criterion_label(self):
        r = is_metrizable(_sp("t3", "sigma_locally_finite_base"))
        assert r.metadata.get("criterion") == "nagata_smirnov"

    def test_sigma_lf_base_alone_is_unknown(self):
        r = is_metrizable(_sp("sigma_locally_finite_base"))
        assert r.is_unknown

    def test_t3_alone_is_unknown(self):
        r = is_metrizable(_sp("t3"))
        assert r.is_unknown


# ---------------------------------------------------------------------------
# is_metrizable — Layer 6 (Bing)
# ---------------------------------------------------------------------------

class TestIsMetrizableBing:
    def test_t3_plus_sigma_discrete_base_is_true(self):
        r = is_metrizable(_sp("t3", "sigma_discrete_base"))
        assert r.is_true

    def test_regular_plus_sigma_discrete_base_is_true(self):
        r = is_metrizable(_sp("regular", "sigma_discrete_base"))
        assert r.is_true

    def test_sigma_d_base_alias_recognized(self):
        r = is_metrizable(_sp("t3", "sigma_d_base"))
        assert r.is_true

    def test_bing_criterion_label(self):
        r = is_metrizable(_sp("t3", "sigma_discrete_base"))
        assert r.metadata.get("criterion") == "bing_metrization"

    def test_sigma_discrete_base_alone_is_unknown(self):
        r = is_metrizable(_sp("sigma_discrete_base"))
        assert r.is_unknown


# ---------------------------------------------------------------------------
# check_nagata_smirnov
# ---------------------------------------------------------------------------

class TestCheckNagataSmirnov:
    def test_returns_result(self):
        r = check_nagata_smirnov(_sp("t3", "sigma_locally_finite_base"))
        assert isinstance(r, Result)

    def test_full_criterion_is_true(self):
        r = check_nagata_smirnov(_sp("t3", "sigma_locally_finite_base"))
        assert r.is_true

    def test_mode_is_theorem(self):
        r = check_nagata_smirnov(_sp("t3", "sigma_locally_finite_base"))
        assert r.mode == "theorem"

    def test_criterion_key_in_metadata(self):
        r = check_nagata_smirnov(_sp("t3", "sigma_locally_finite_base"))
        assert r.metadata.get("criterion") == "nagata_smirnov"

    def test_justification_mentions_nagata(self):
        r = check_nagata_smirnov(_sp("t3", "sigma_locally_finite_base"))
        combined = " ".join(r.justification).lower()
        assert "nagata" in combined

    def test_missing_t3_gives_unknown(self):
        r = check_nagata_smirnov(_sp("sigma_locally_finite_base"))
        assert r.is_unknown

    def test_missing_base_gives_unknown(self):
        r = check_nagata_smirnov(_sp("t3"))
        assert r.is_unknown

    def test_no_tags_gives_unknown(self):
        r = check_nagata_smirnov(_sp())
        assert r.is_unknown

    def test_unknown_criterion_is_none(self):
        r = check_nagata_smirnov(_sp("t3"))
        assert r.metadata.get("criterion") is None

    def test_tychonoff_tag_counts_as_regular(self):
        r = check_nagata_smirnov(_sp("tychonoff", "sigma_locally_finite_base"))
        assert r.is_true

    def test_sigma_lf_base_alias_works(self):
        r = check_nagata_smirnov(_sp("regular", "sigma_lf_base"))
        assert r.is_true

    def test_not_metrizable_tag_does_not_block_criterion_directly(self):
        # check_nagata_smirnov looks at positive criteria only, not negative tags
        r = check_nagata_smirnov(_sp("not_metrizable", "t3", "sigma_locally_finite_base"))
        # The criterion sees t3+sigma_lf_base so it still returns true
        assert r.is_true


# ---------------------------------------------------------------------------
# check_bing_metrization
# ---------------------------------------------------------------------------

class TestCheckBingMetrization:
    def test_returns_result(self):
        r = check_bing_metrization(_sp("t3", "sigma_discrete_base"))
        assert isinstance(r, Result)

    def test_full_criterion_is_true(self):
        r = check_bing_metrization(_sp("t3", "sigma_discrete_base"))
        assert r.is_true

    def test_mode_is_theorem(self):
        r = check_bing_metrization(_sp("t3", "sigma_discrete_base"))
        assert r.mode == "theorem"

    def test_criterion_key_in_metadata(self):
        r = check_bing_metrization(_sp("t3", "sigma_discrete_base"))
        assert r.metadata.get("criterion") == "bing_metrization"

    def test_justification_mentions_bing(self):
        r = check_bing_metrization(_sp("t3", "sigma_discrete_base"))
        combined = " ".join(r.justification).lower()
        assert "bing" in combined

    def test_missing_t3_gives_unknown(self):
        r = check_bing_metrization(_sp("sigma_discrete_base"))
        assert r.is_unknown

    def test_missing_base_gives_unknown(self):
        r = check_bing_metrization(_sp("regular"))
        assert r.is_unknown

    def test_no_tags_gives_unknown(self):
        r = check_bing_metrization(_sp())
        assert r.is_unknown

    def test_unknown_criterion_is_none(self):
        r = check_bing_metrization(_sp("regular"))
        assert r.metadata.get("criterion") is None

    def test_sigma_d_base_alias_works(self):
        r = check_bing_metrization(_sp("t3", "sigma_d_base"))
        assert r.is_true

    def test_regular_t1_tag_counts_as_regular(self):
        r = check_bing_metrization(_sp("regular_t1", "sigma_discrete_base"))
        assert r.is_true


# ---------------------------------------------------------------------------
# metrization_theorem_check
# ---------------------------------------------------------------------------

class TestMetrizationTheoremCheck:
    def test_returns_dict(self):
        d = metrization_theorem_check(_sp("t3", "sigma_locally_finite_base"))
        assert isinstance(d, dict)

    def test_has_all_keys(self):
        d = metrization_theorem_check(_sp())
        assert set(d.keys()) == {"urysohn", "nagata_smirnov", "bing", "verdict"}

    def test_urysohn_criterion_populates_verdict(self):
        d = metrization_theorem_check(_sp("second_countable", "t3"))
        assert d["verdict"].is_true
        assert d["verdict"].metadata.get("criterion") == "urysohn_metrization"

    def test_nagata_smirnov_criterion_populates_verdict(self):
        d = metrization_theorem_check(_sp("t3", "sigma_locally_finite_base"))
        assert d["verdict"].is_true
        assert d["verdict"].metadata.get("criterion") == "nagata_smirnov"

    def test_bing_criterion_populates_verdict(self):
        d = metrization_theorem_check(_sp("t3", "sigma_discrete_base"))
        assert d["verdict"].is_true
        assert d["verdict"].metadata.get("criterion") == "bing_metrization"

    def test_not_metrizable_tag_verdict_is_false(self):
        d = metrization_theorem_check(_sp("not_metrizable"))
        assert d["verdict"].is_false

    def test_no_info_verdict_is_unknown(self):
        d = metrization_theorem_check(_sp())
        assert d["verdict"].is_unknown

    def test_individual_results_are_result_instances(self):
        d = metrization_theorem_check(_sp("t3", "sigma_locally_finite_base"))
        for key in ("urysohn", "nagata_smirnov", "bing"):
            assert isinstance(d[key], Result)

    def test_verdict_is_result_instance(self):
        d = metrization_theorem_check(_sp())
        assert isinstance(d["verdict"], Result)

    def test_metrizable_tag_urysohn_true_wins(self):
        # metrizable tag → is_metrizable returns true via Layer 3
        d = metrization_theorem_check(_sp("metrizable"))
        assert d["verdict"].is_true

    def test_not_hausdorff_tag_verdict_false(self):
        d = metrization_theorem_check(_sp("not_hausdorff"))
        assert d["verdict"].is_false
