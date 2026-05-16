"""Tests for T3.5 / Tychonoff characterization additions (v0.5.4)."""
import pytest

from pytop.result import Result
from pytop.separation import (
    SEPARATION_CHAIN_ORDER,
    TYCHONOFF_POSITIVE_TAGS,
    check_tychonoff,
    separation_chain,
    tychonoff_characterization,
)
from pytop.spaces import TopologicalSpace


def _sp(*tags: str) -> TopologicalSpace:
    return TopologicalSpace(carrier=None, tags=set(tags))


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_tychonoff_positive_tags_contains_tychonoff(self):
        assert "tychonoff" in TYCHONOFF_POSITIVE_TAGS

    def test_tychonoff_positive_tags_contains_t3_5(self):
        assert "t3_5" in TYCHONOFF_POSITIVE_TAGS

    def test_tychonoff_positive_tags_contains_t3_half(self):
        assert "t3½" in TYCHONOFF_POSITIVE_TAGS

    def test_tychonoff_positive_tags_contains_cr_t1(self):
        assert "completely_regular_t1" in TYCHONOFF_POSITIVE_TAGS

    def test_separation_chain_order_is_tuple(self):
        assert isinstance(SEPARATION_CHAIN_ORDER, tuple)

    def test_separation_chain_order_contains_tychonoff(self):
        assert "tychonoff" in SEPARATION_CHAIN_ORDER

    def test_separation_chain_order_t0_first(self):
        assert SEPARATION_CHAIN_ORDER[0] == "t0"

    def test_separation_chain_order_perfectly_normal_last(self):
        assert SEPARATION_CHAIN_ORDER[-1] == "perfectly_normal"

    def test_separation_chain_order_tychonoff_after_t3(self):
        idx = list(SEPARATION_CHAIN_ORDER)
        assert idx.index("tychonoff") > idx.index("t3")

    def test_separation_chain_order_t4_after_tychonoff(self):
        idx = list(SEPARATION_CHAIN_ORDER)
        assert idx.index("t4") > idx.index("tychonoff")


# ---------------------------------------------------------------------------
# check_tychonoff — direct positive tags (Layer 3)
# ---------------------------------------------------------------------------

class TestCheckTychonoffDirectTags:
    def test_tychonoff_tag_is_true(self):
        assert check_tychonoff(_sp("tychonoff")).is_true

    def test_t3_5_tag_is_true(self):
        assert check_tychonoff(_sp("t3_5")).is_true

    def test_t3_half_tag_is_true(self):
        assert check_tychonoff(_sp("t3½")).is_true

    def test_completely_regular_t1_tag_is_true(self):
        assert check_tychonoff(_sp("completely_regular_t1")).is_true

    def test_direct_tag_criterion(self):
        r = check_tychonoff(_sp("tychonoff"))
        assert r.metadata.get("criterion") == "direct_tag"

    def test_returns_result_instance(self):
        assert isinstance(check_tychonoff(_sp("tychonoff")), Result)

    def test_mode_is_theorem(self):
        assert check_tychonoff(_sp("tychonoff")).mode == "theorem"


# ---------------------------------------------------------------------------
# check_tychonoff — Layer 2: metric
# ---------------------------------------------------------------------------

class TestCheckTychonoffMetric:
    def test_metric_tag_is_true(self):
        assert check_tychonoff(_sp("metric")).is_true

    def test_metric_criterion(self):
        r = check_tychonoff(_sp("metric"))
        assert r.metadata.get("criterion") == "metric"

    def test_metric_justification_mentions_metric(self):
        r = check_tychonoff(_sp("metric"))
        combined = " ".join(r.justification).lower()
        assert "metric" in combined


# ---------------------------------------------------------------------------
# check_tychonoff — Layer 4: T1 + completely_regular
# ---------------------------------------------------------------------------

class TestCheckTychonoffCRT1:
    def test_t1_plus_cr_is_true(self):
        assert check_tychonoff(_sp("t1", "completely_regular")).is_true

    def test_t1_plus_functionally_regular_is_true(self):
        assert check_tychonoff(_sp("t1", "functionally_regular")).is_true

    def test_hausdorff_plus_cr_is_true(self):
        # hausdorff implies t1, so hausdorff + cr → Tychonoff
        assert check_tychonoff(_sp("hausdorff", "completely_regular")).is_true

    def test_cr_t1_criterion(self):
        r = check_tychonoff(_sp("t1", "completely_regular"))
        assert r.metadata.get("criterion") == "cr_t1"

    def test_cr_alone_is_unknown(self):
        assert check_tychonoff(_sp("completely_regular")).is_unknown

    def test_t1_alone_is_unknown(self):
        assert check_tychonoff(_sp("t1")).is_unknown

    def test_justification_mentions_characterisation(self):
        r = check_tychonoff(_sp("t1", "completely_regular"))
        combined = " ".join(r.justification).lower()
        assert "t1" in combined or "completely regular" in combined


# ---------------------------------------------------------------------------
# check_tychonoff — Layer 5: T4 / normal + T1
# ---------------------------------------------------------------------------

class TestCheckTychonoffNormalT1:
    def test_t4_tag_is_true(self):
        # t4 implies t1 and cr via _positive_tag_implies, caught by Layer 4
        assert check_tychonoff(_sp("t4")).is_true

    def test_normal_t1_tag_is_true(self):
        assert check_tychonoff(_sp("normal_t1")).is_true

    def test_normal_t1_tag_criterion(self):
        r = check_tychonoff(_sp("normal_t1"))
        assert r.metadata.get("criterion") == "normal_t1"

    def test_normal_plus_t1_tags_is_true(self):
        assert check_tychonoff(_sp("normal", "t1")).is_true

    def test_normal_plus_t1_criterion(self):
        r = check_tychonoff(_sp("normal", "t1"))
        assert r.metadata.get("criterion") == "normal_t1"

    def test_normal_alone_is_unknown(self):
        assert check_tychonoff(_sp("normal")).is_unknown

    def test_perfectly_normal_tag_is_true(self):
        assert check_tychonoff(_sp("perfectly_normal")).is_true


# ---------------------------------------------------------------------------
# check_tychonoff — Layer 1: blocking (negative) tags
# ---------------------------------------------------------------------------

class TestCheckTychonoffNegative:
    def test_not_tychonoff_is_false(self):
        assert check_tychonoff(_sp("not_tychonoff")).is_false

    def test_not_t3_5_is_false(self):
        assert check_tychonoff(_sp("not_t3_5")).is_false

    def test_not_completely_regular_is_false(self):
        assert check_tychonoff(_sp("not_completely_regular")).is_false

    def test_not_t1_is_false(self):
        assert check_tychonoff(_sp("not_t1")).is_false

    def test_negative_criterion_is_none(self):
        r = check_tychonoff(_sp("not_tychonoff"))
        assert r.metadata.get("criterion") is None


# ---------------------------------------------------------------------------
# check_tychonoff — unknown
# ---------------------------------------------------------------------------

class TestCheckTychonoffUnknown:
    def test_no_tags_is_unknown(self):
        assert check_tychonoff(_sp()).is_unknown

    def test_hausdorff_alone_is_unknown(self):
        assert check_tychonoff(_sp("hausdorff")).is_unknown

    def test_t3_alone_is_unknown(self):
        # T3 (regular Hausdorff) does not imply Tychonoff in general
        assert check_tychonoff(_sp("t3")).is_unknown

    def test_unknown_criterion_is_none(self):
        r = check_tychonoff(_sp())
        assert r.metadata.get("criterion") is None

    def test_unknown_metadata_has_tags_key(self):
        r = check_tychonoff(_sp())
        assert "tags" in r.metadata


# ---------------------------------------------------------------------------
# tychonoff_characterization
# ---------------------------------------------------------------------------

class TestTychonoffCharacterization:
    def test_returns_dict(self):
        d = tychonoff_characterization(_sp("tychonoff"))
        assert isinstance(d, dict)

    def test_has_required_keys(self):
        d = tychonoff_characterization(_sp())
        assert set(d.keys()) == {"is_tychonoff", "criterion", "is_completely_regular", "is_t1", "note"}

    def test_is_tychonoff_is_result(self):
        d = tychonoff_characterization(_sp("t1", "completely_regular"))
        assert isinstance(d["is_tychonoff"], Result)

    def test_is_completely_regular_is_result(self):
        d = tychonoff_characterization(_sp("t1", "completely_regular"))
        assert isinstance(d["is_completely_regular"], Result)

    def test_is_t1_is_result(self):
        d = tychonoff_characterization(_sp("t1", "completely_regular"))
        assert isinstance(d["is_t1"], Result)

    def test_tychonoff_space_note_positive(self):
        d = tychonoff_characterization(_sp("tychonoff"))
        assert "tychonoff" in d["note"].lower()

    def test_not_tychonoff_note_negative(self):
        d = tychonoff_characterization(_sp("not_tychonoff"))
        assert "fail" in d["note"].lower()

    def test_unknown_note(self):
        d = tychonoff_characterization(_sp())
        assert "undetermined" in d["note"].lower()

    def test_criterion_matches_check_tychonoff(self):
        d = tychonoff_characterization(_sp("t1", "completely_regular"))
        assert d["criterion"] == "cr_t1"

    def test_criterion_none_when_unknown(self):
        d = tychonoff_characterization(_sp())
        assert d["criterion"] is None

    def test_tychonoff_tag_gives_true_verdict(self):
        d = tychonoff_characterization(_sp("tychonoff"))
        assert d["is_tychonoff"].is_true

    def test_metric_tag_gives_true_verdict(self):
        d = tychonoff_characterization(_sp("metric"))
        assert d["is_tychonoff"].is_true


# ---------------------------------------------------------------------------
# separation_chain
# ---------------------------------------------------------------------------

class TestSeparationChain:
    def test_returns_dict(self):
        d = separation_chain(_sp("tychonoff"))
        assert isinstance(d, dict)

    def test_has_all_chain_keys(self):
        d = separation_chain(_sp())
        assert set(d.keys()) == set(SEPARATION_CHAIN_ORDER)

    def test_all_values_are_results(self):
        d = separation_chain(_sp("metric"))
        for v in d.values():
            assert isinstance(v, Result)

    def test_metric_space_all_true(self):
        d = separation_chain(_sp("metric"))
        for key, r in d.items():
            assert r.is_true, f"Expected true for {key}, got {r.status}"

    def test_no_tags_all_unknown(self):
        d = separation_chain(_sp())
        for key, r in d.items():
            assert r.is_unknown, f"Expected unknown for {key}, got {r.status}"

    def test_tychonoff_entry_uses_check_tychonoff(self):
        # t4 tag: check_tychonoff returns true (Layer 4 or 5); analyze_separation
        # would also return true via tag implication — but we verify the result is true
        d = separation_chain(_sp("t4"))
        assert d["tychonoff"].is_true

    def test_not_t1_makes_t1_entry_false(self):
        d = separation_chain(_sp("not_t1"))
        assert d["t1"].is_false

    def test_t3_tag_t3_entry_true(self):
        d = separation_chain(_sp("t3"))
        assert d["t3"].is_true

    def test_tychonoff_entry_is_result(self):
        d = separation_chain(_sp("tychonoff"))
        assert isinstance(d["tychonoff"], Result)

    def test_chain_keys_match_separation_chain_order(self):
        d = separation_chain(_sp())
        assert list(d.keys()) == list(SEPARATION_CHAIN_ORDER)

    def test_t1_plus_cr_tychonoff_entry_true(self):
        d = separation_chain(_sp("t1", "completely_regular"))
        assert d["tychonoff"].is_true

    def test_not_tychonoff_tag_tychonoff_entry_false(self):
        d = separation_chain(_sp("not_tychonoff"))
        assert d["tychonoff"].is_false
