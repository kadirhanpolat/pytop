"""Tests for v0.1.49 basic counterexample atlas corridor.

Covers counterexample_atlas.py: lookup, layer/property/construction queries,
Result metadata, and ATLAS_IDS.
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from pytop.counterexample_atlas import (
    counterexample_lookup,
    counterexample_atlas_by_layer,
    counterexample_atlas_by_property,
    counterexample_atlas_by_construction,
    analyze_counterexample_atlas,
    ATLAS_IDS,
)


# ---------------------------------------------------------------------------
# ATLAS_IDS
# ---------------------------------------------------------------------------

class TestAtlasIds:
    def test_is_tuple(self):
        assert isinstance(ATLAS_IDS, tuple)

    def test_contains_all_separation(self):
        for i in range(1, 7):
            assert f"CE-S-{i:02d}" in ATLAS_IDS

    def test_contains_all_preservation(self):
        for i in range(1, 11):
            assert f"CE-P-{i:02d}" in ATLAS_IDS

    def test_total_count(self):
        assert len(ATLAS_IDS) == 16

    def test_sorted(self):
        assert list(ATLAS_IDS) == sorted(ATLAS_IDS)


# ---------------------------------------------------------------------------
# counterexample_lookup
# ---------------------------------------------------------------------------

class TestCounterexampleLookup:
    def test_ce_s_01_true(self):
        r = counterexample_lookup("CE-S-01")
        assert r.is_true

    def test_ce_s_01_value(self):
        r = counterexample_lookup("CE-S-01")
        assert r.value == "CE-S-01"

    def test_ce_s_01_layer(self):
        r = counterexample_lookup("CE-S-01")
        assert r.metadata["layer"] == "separation"

    def test_ce_s_01_property(self):
        r = counterexample_lookup("CE-S-01")
        assert r.metadata["property_failed"] == "t0"

    def test_ce_s_02_t0_not_t1(self):
        r = counterexample_lookup("CE-S-02")
        assert r.is_true
        assert r.metadata["counterexample_class"] == "t0_not_t1"

    def test_ce_s_03_t1_not_hausdorff(self):
        r = counterexample_lookup("CE-S-03")
        assert r.metadata["counterexample_class"] == "t1_not_hausdorff"

    def test_ce_s_04_t1_not_hausdorff(self):
        r = counterexample_lookup("CE-S-04")
        assert r.metadata["counterexample_class"] == "t1_not_hausdorff"

    def test_ce_s_05_finite_t1(self):
        r = counterexample_lookup("CE-S-05")
        assert r.metadata["counterexample_class"] == "finite_t1_forces_discrete"

    def test_ce_s_06_positive_anchor(self):
        r = counterexample_lookup("CE-S-06")
        assert r.is_true
        assert r.metadata["counterexample_class"] == "metric_hausdorff_anchor"
        assert r.metadata["property_failed"] is None

    def test_ce_p_01_connectedness(self):
        r = counterexample_lookup("CE-P-01")
        assert r.is_true
        assert r.metadata["property_failed"] == "connectedness"
        assert r.metadata["construction"] == "subspace"

    def test_ce_p_02_compactness_subspace(self):
        r = counterexample_lookup("CE-P-02")
        assert r.metadata["property_failed"] == "compactness"
        assert r.metadata["construction"] == "subspace"

    def test_ce_p_03_hausdorff_quotient(self):
        r = counterexample_lookup("CE-P-03")
        assert r.metadata["property_failed"] == "hausdorff"
        assert r.metadata["construction"] == "quotient"

    def test_ce_p_04_hausdorff_continuous_image(self):
        r = counterexample_lookup("CE-P-04")
        assert r.metadata["construction"] == "continuous_image"

    def test_ce_p_05_t1_quotient(self):
        r = counterexample_lookup("CE-P-05")
        assert r.metadata["property_failed"] == "t1"
        assert r.metadata["construction"] == "quotient"

    def test_ce_p_06_t1_continuous_image(self):
        r = counterexample_lookup("CE-P-06")
        assert r.metadata["property_failed"] == "t1"
        assert r.metadata["construction"] == "continuous_image"

    def test_ce_p_07_second_countability_quotient(self):
        r = counterexample_lookup("CE-P-07")
        assert r.metadata["property_failed"] == "second_countability"
        assert r.metadata["construction"] == "quotient"

    def test_ce_p_08_second_countability_image(self):
        r = counterexample_lookup("CE-P-08")
        assert r.metadata["property_failed"] == "second_countability"
        assert r.metadata["construction"] == "continuous_image"

    def test_ce_p_09_uncountable_product(self):
        r = counterexample_lookup("CE-P-09")
        assert r.metadata["construction"] == "countable_product"
        assert r.metadata["counterexample_class"] == "second_countability_uncountable_product"

    def test_ce_p_10_path_connectedness(self):
        r = counterexample_lookup("CE-P-10")
        assert r.metadata["property_failed"] == "path_connectedness"
        assert r.metadata["counterexample_class"] == "connected_not_path_connected"

    def test_lowercase_id_normalised(self):
        r = counterexample_lookup("ce-s-01")
        assert r.is_true
        assert r.value == "CE-S-01"

    def test_unknown_id_returns_unknown(self):
        r = counterexample_lookup("CE-X-99")
        assert not r.is_true

    def test_justification_nonempty(self):
        r = counterexample_lookup("CE-P-01")
        assert len(r.justification) > 0
        assert len(r.justification[0]) > 10

    def test_cilt_ii_corridor_metadata(self):
        r = counterexample_lookup("CE-S-03")
        assert r.metadata.get("cilt_ii_corridor") == "basic-counterexample-atlas"

    def test_v0149_corridor_record_flag(self):
        for aid in ATLAS_IDS:
            r = counterexample_lookup(aid)
            assert r.metadata.get("v0_1_49_corridor_record") is True


# ---------------------------------------------------------------------------
# counterexample_atlas_by_layer
# ---------------------------------------------------------------------------

class TestAtlasByLayer:
    def test_separation_layer_count(self):
        r = counterexample_atlas_by_layer("separation")
        assert r.is_true
        assert len(r.value) == 6

    def test_preservation_layer_count(self):
        r = counterexample_atlas_by_layer("preservation")
        assert r.is_true
        assert len(r.value) == 10

    def test_separation_contains_ce_s_01(self):
        r = counterexample_atlas_by_layer("separation")
        assert "CE-S-01" in r.value

    def test_preservation_contains_ce_p_10(self):
        r = counterexample_atlas_by_layer("preservation")
        assert "CE-P-10" in r.value

    def test_invalid_layer_unknown(self):
        r = counterexample_atlas_by_layer("metric")
        assert not r.is_true

    def test_metadata_entry_count(self):
        r = counterexample_atlas_by_layer("separation")
        assert r.metadata["entry_count"] == 6


# ---------------------------------------------------------------------------
# counterexample_atlas_by_property
# ---------------------------------------------------------------------------

class TestAtlasByProperty:
    def test_hausdorff_failures(self):
        r = counterexample_atlas_by_property("hausdorff")
        assert r.is_true
        # CE-S-03, CE-S-04, CE-P-03, CE-P-04
        assert len(r.value) >= 2

    def test_t1_failures(self):
        r = counterexample_atlas_by_property("t1")
        assert r.is_true
        assert len(r.value) >= 2

    def test_second_countability_failures(self):
        r = counterexample_atlas_by_property("second_countability")
        assert r.is_true
        # CE-P-07, CE-P-08, CE-P-09
        assert len(r.value) >= 3

    def test_connectedness_failure(self):
        r = counterexample_atlas_by_property("connectedness")
        assert r.is_true
        assert "CE-P-01" in r.value

    def test_unknown_property_returns_unknown(self):
        r = counterexample_atlas_by_property("normality")
        assert not r.is_true


# ---------------------------------------------------------------------------
# counterexample_atlas_by_construction
# ---------------------------------------------------------------------------

class TestAtlasByConstruction:
    def test_subspace_failures(self):
        r = counterexample_atlas_by_construction("subspace")
        assert r.is_true
        # CE-P-01, CE-P-02, CE-P-10
        assert len(r.value) >= 3

    def test_quotient_failures(self):
        r = counterexample_atlas_by_construction("quotient")
        assert r.is_true
        # CE-P-03, CE-P-05, CE-P-07
        assert len(r.value) >= 3

    def test_continuous_image_failures(self):
        r = counterexample_atlas_by_construction("continuous_image")
        assert r.is_true
        # CE-P-04, CE-P-06, CE-P-08
        assert len(r.value) >= 3

    def test_unknown_construction(self):
        r = counterexample_atlas_by_construction("direct_sum")
        assert not r.is_true


# ---------------------------------------------------------------------------
# analyze_counterexample_atlas (corridor entry-point)
# ---------------------------------------------------------------------------

class TestAnalyzeCounterexampleAtlas:
    def test_full_summary(self):
        r = analyze_counterexample_atlas()
        assert r.is_true
        assert r.metadata["total_entries"] == 16
        assert r.metadata["separation_entries"] == 6
        assert r.metadata["preservation_entries"] == 10

    def test_with_atlas_id(self):
        r = analyze_counterexample_atlas(atlas_id="CE-P-10")
        assert r.is_true
        assert r.value == "CE-P-10"

    def test_with_layer(self):
        r = analyze_counterexample_atlas(layer="preservation")
        assert r.is_true
        assert len(r.value) == 10

    def test_with_property_name(self):
        r = analyze_counterexample_atlas(property_name="hausdorff")
        assert r.is_true

    def test_with_construction(self):
        r = analyze_counterexample_atlas(construction="quotient")
        assert r.is_true

    def test_cilt_ii_metadata(self):
        r = analyze_counterexample_atlas()
        assert r.metadata["cilt_ii_corridor"] == "basic-counterexample-atlas"
