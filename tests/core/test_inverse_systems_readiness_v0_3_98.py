import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_inverse_systems_release_readiness_manifest_passes() -> None:
    data = json.loads((ROOT / "exports/inverse_systems_release_readiness_manifest_v0_3_98.json").read_text(encoding="utf-8"))
    assert data["route"] == "INV-05"
    assert data["support_files_present"] == data["support_files_required"] == 12
    assert data["source_hash_matches_mirror_front_matter"] is True
    assert data["manifest_source_hash_matches_actual_source"] is True
    assert data["manifest_generated_hash_matches_actual_mirror"] is True
    assert data["lane_closure_decision"] == "closed"
    assert data["passed"] is True

def test_inverse_systems_release_readiness_report_names_next_lane() -> None:
    report = (ROOT / "docs/qa/inverse_systems_mirror_release_readiness_checkpoint_report.md").read_text(encoding="utf-8")
    assert "INV-05" in report
    assert "v0.3.99" in report
    assert "canonical TeX" in report
