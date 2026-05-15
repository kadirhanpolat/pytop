from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_volume6_audit_flags_incomplete_stub_band_v100():
    from pytop.volume6_audit import audit_volume_6_completeness, volume6_incomplete_milestones

    assert audit_volume_6_completeness() is True
    incomplete = set(volume6_incomplete_milestones())
    assert incomplete == set()
    assert "advanced_compactifications" not in incomplete
    assert "dimension_theory" not in incomplete
    assert "uniform_spaces" not in incomplete
    assert "proximity_spaces" not in incomplete
    assert "inverse_systems" not in incomplete


def test_volume6_audit_marks_fixed_surface_consistency_true_v100():
    from pytop.volume6_audit import volume6_audit_report

    report = volume6_audit_report()
    assert report["expected_version"] == "0.1.108"
    assert report["project_root"].endswith("pytop_v0_1_108")
    assert report["milestones"]["fixed_surface_consistency"]["status"] == "true"
    assert report["milestones"]["advanced_compactifications"]["status"] == "true"
    assert report["milestones"]["dimension_theory"]["status"] == "true"
    assert report["milestones"]["uniform_spaces"]["status"] == "true"
    assert report["milestones"]["proximity_spaces"]["status"] == "true"
    assert report["milestones"]["inverse_systems"]["status"] == "true"
    assert report["milestones"]["preservation_tables"]["status"] == "true"


def test_volume6_audit_render_mentions_incomplete_milestones_v100():
    from pytop.volume6_audit import render_volume6_audit_report

    text = render_volume6_audit_report()
    assert "COMPLETE" in text
    assert "advanced_compactifications: true" in text
    assert "dimension_theory: true" in text
    assert "uniform_spaces: true" in text
    assert "proximity_spaces: true" in text
    assert "inverse_systems: true" in text
    assert "preservation_tables: true" in text


def test_volume6_conclusion_no_longer_claims_programmatic_seal_v100():
    chapter = (
        ROOT
        / "manuscript"
        / "volume_6"
        / "chapters"
        / "36_volume6_conclusion.tex"
    )
    text = chapter.read_text(encoding="utf-8").lower()
    assert "programmatic seal of completion" not in text
    assert "conservative milestone gate" in text
