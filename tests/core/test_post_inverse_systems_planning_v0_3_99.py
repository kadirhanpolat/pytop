import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_post_inverse_planning_selects_advanced_function_spaces() -> None:
    data = json.loads((ROOT / "exports/post_inverse_systems_lane_planning_manifest_v0_3_99.json").read_text(encoding="utf-8"))
    assert data["route"] == "PLAN-07"
    assert data["inverse_closure_surface_present"] == data["inverse_closure_surface_required"] == 9
    assert data["selected_next_lane"] == "advanced-function-spaces"
    assert data["next_lane_anchor_present"] == data["next_lane_anchor_required"] == 5
    assert data["planned_micro_lane"][0].startswith("v0.4.00")
    assert data["passed"] is True

def test_post_inverse_planning_doc_has_guardrails() -> None:
    text = (ROOT / "docs/roadmap/post_inverse_systems_maturity_lane_planning.md").read_text(encoding="utf-8")
    assert "AFS-01" in text
    assert "Generated AI-MD hand edits: `0`" in text
    assert "advanced-function-spaces" in text
