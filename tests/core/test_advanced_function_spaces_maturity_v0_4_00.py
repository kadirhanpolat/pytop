import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_advanced_function_spaces_maturity_matrix_passes() -> None:
    data = json.loads((ROOT / "exports/advanced_function_spaces_maturity_matrix_v0_4_00.json").read_text(encoding="utf-8"))
    assert data["route"] == "AFS-01"
    assert data["support_files_present"] == data["support_files_required"] == 7
    assert data["generated_mirror_hash_current"] is True
    assert data["generated_manifest_target_hash_current"] is True
    assert data["api_markers_present"] == data["api_markers_required"] == 4
    assert data["band_counts"] == {"A": 0, "B": 4, "C": 3, "D": 3}
    assert data["dedicated_examples_gap_declared"] is True
    assert data["dedicated_questionbank_gap_declared"] is True
    assert data["dedicated_notebook_gap_declared"] is True
    assert data["passed"] is True

def test_advanced_function_spaces_maturity_report_declares_next_step() -> None:
    text = (ROOT / "docs/qa/advanced_function_spaces_maturity_matrix_checkpoint_report.md").read_text(encoding="utf-8")
    assert "AFS-01" in text
    assert "AFS-02" in text
    assert "dedicated examples" in text
