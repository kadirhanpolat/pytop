"""Tests for v0.1.50 Cilt II undergraduate route close-out corridor.

Covers cilt2_route_summary.py: cilt2_route_summary, cilt2_corridor_lookup,
Result metadata, and integration with v0.1.47-v0.1.49 corridor modules.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from pytop._internal.cilt2_route_summary import cilt2_route_summary, cilt2_corridor_lookup
import pytop


# ---------------------------------------------------------------------------
# cilt2_route_summary
# ---------------------------------------------------------------------------

class TestCilt2RouteSummary:
    def test_is_true(self):
        r = cilt2_route_summary()
        assert r.is_true

    def test_value(self):
        r = cilt2_route_summary()
        assert r.value == "cilt_ii_close_out"

    def test_cilt_metadata(self):
        r = cilt2_route_summary()
        assert r.metadata["cilt"] == "II"

    def test_phase_metadata(self):
        r = cilt2_route_summary()
        assert "v0.1.41" in r.metadata["phase"]
        assert "v0.1.50" in r.metadata["phase"]

    def test_close_out_version(self):
        r = cilt2_route_summary()
        assert r.metadata["close_out_version"] == "v0.1.50"

    def test_total_corridors(self):
        r = cilt2_route_summary()
        assert r.metadata["total_corridors"] == 3

    def test_corridors_keys(self):
        r = cilt2_route_summary()
        assert "v0.1.47" in r.metadata["corridors"]
        assert "v0.1.48" in r.metadata["corridors"]
        assert "v0.1.49" in r.metadata["corridors"]

    def test_chapters_covered(self):
        r = cilt2_route_summary()
        chapters = r.metadata["chapters_covered"]
        assert 10 in chapters
        assert 16 in chapters

    def test_close_out_flag(self):
        r = cilt2_route_summary()
        assert r.metadata["cilt_ii_close_out"] is True

    def test_v0150_corridor_record(self):
        r = cilt2_route_summary()
        assert r.metadata["v0_1_50_corridor_record"] is True

    def test_worksheet_path(self):
        r = cilt2_route_summary()
        assert "08_cilt2_undergraduate_route" in r.metadata["worksheet"]

    def test_quick_check_path(self):
        r = cilt2_route_summary()
        assert "08_cilt2_undergraduate_route" in r.metadata["quick_check"]

    def test_notebook_path(self):
        r = cilt2_route_summary()
        assert "cilt2_undergraduate_route" in r.metadata["notebook"]

    def test_justification_nonempty(self):
        r = cilt2_route_summary()
        assert len(r.justification) > 0
        assert "Cilt II" in r.justification[0]

    def test_corridor_v047_api(self):
        r = cilt2_route_summary()
        api = r.metadata["corridors"]["v0.1.47"]["api"]
        assert "is_complete" in api
        assert "analyze_metric_completeness" in api

    def test_corridor_v048_api(self):
        r = cilt2_route_summary()
        api = r.metadata["corridors"]["v0.1.48"]["api"]
        assert "preservation_table_lookup" in api

    def test_corridor_v049_api(self):
        r = cilt2_route_summary()
        api = r.metadata["corridors"]["v0.1.49"]["api"]
        assert "counterexample_lookup" in api
        assert "ATLAS_IDS" in api


# ---------------------------------------------------------------------------
# cilt2_corridor_lookup
# ---------------------------------------------------------------------------

class TestCilt2CorridorLookup:
    def test_v047_true(self):
        r = cilt2_corridor_lookup("v0.1.47")
        assert r.is_true
        assert r.value == "v0.1.47"

    def test_v048_true(self):
        r = cilt2_corridor_lookup("v0.1.48")
        assert r.is_true
        assert r.value == "v0.1.48"

    def test_v049_true(self):
        r = cilt2_corridor_lookup("v0.1.49")
        assert r.is_true
        assert r.value == "v0.1.49"

    def test_v047_chapter(self):
        r = cilt2_corridor_lookup("v0.1.47")
        assert r.metadata["chapter"] == 15

    def test_v048_chapter(self):
        r = cilt2_corridor_lookup("v0.1.48")
        assert r.metadata["chapter"] == 10

    def test_v049_chapter(self):
        r = cilt2_corridor_lookup("v0.1.49")
        assert r.metadata["chapter"] == 10

    def test_v047_title(self):
        r = cilt2_corridor_lookup("v0.1.47")
        assert "completeness" in r.metadata["title"].lower()

    def test_v048_title(self):
        r = cilt2_corridor_lookup("v0.1.48")
        assert "preservation" in r.metadata["title"].lower()

    def test_v049_title(self):
        r = cilt2_corridor_lookup("v0.1.49")
        assert "counterexample" in r.metadata["title"].lower()

    def test_unknown_version(self):
        r = cilt2_corridor_lookup("v0.1.99")
        assert not r.is_true

    def test_v0150_flag(self):
        for ver in ["v0.1.47", "v0.1.48", "v0.1.49"]:
            r = cilt2_corridor_lookup(ver)
            assert r.metadata.get("v0_1_50_corridor_record") is True

    def test_cilt_ii_flag(self):
        for ver in ["v0.1.47", "v0.1.48", "v0.1.49"]:
            r = cilt2_corridor_lookup(ver)
            assert r.metadata.get("cilt_ii_close_out") is True


# ---------------------------------------------------------------------------
# pytop public API integration
# ---------------------------------------------------------------------------

class TestPytopPublicApi:
    def test_all_v047_exports(self):
        for name in ["is_complete", "is_totally_bounded",
                     "metric_compactness_check", "analyze_metric_completeness"]:
            assert hasattr(pytop, name), f"Missing: {name}"

    def test_all_v048_exports(self):
        for name in ["preservation_table_lookup", "preservation_table_row",
                     "preservation_table_column", "analyze_preservation_table"]:
            assert hasattr(pytop, name), f"Missing: {name}"

    def test_all_v049_exports(self):
        for name in ["counterexample_lookup", "counterexample_atlas_by_layer",
                     "counterexample_atlas_by_property",
                     "counterexample_atlas_by_construction",
                     "analyze_counterexample_atlas", "ATLAS_IDS"]:
            assert hasattr(pytop, name), f"Missing: {name}"

