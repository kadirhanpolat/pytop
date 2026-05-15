from __future__ import annotations

from pathlib import Path

from pytop_questionbank.cilt4_entry_assessment_routes import (
    build_cilt4_entry_assessment_routes,
    cilt4_entry_assessment_route_summary,
    measured_concepts_for_cilt4_entry_assessment,
    render_cilt4_entry_assessment_route_report,
    route_ids_for_cilt4_entry_assessment,
)

ROOT = Path(__file__).resolve().parents[2]


def test_cilt4_entry_assessment_routes_close_objective_only_gap():
    routes = build_cilt4_entry_assessment_routes()
    assert len(routes) == 4
    assert cilt4_entry_assessment_route_summary()["generated_question_route_ready_count"] == 4
    assert set(route_ids_for_cilt4_entry_assessment()) == {
        "CILT4-MS-IV-35-ORDINALS-ASSESSMENT",
        "CILT4-MS-IV-36-COFINALITY-REGULARITY-ASSESSMENT",
        "CILT4-MS-IV-38-BASIC-INVARIANTS-ASSESSMENT",
        "CILT4-MS-IV-39-CARDINAL-FUNCTION-FRAMEWORK-ASSESSMENT",
    }
    assert sum(len(route.items) for route in routes) >= 16


def test_cilt4_entry_assessment_routes_measure_required_concepts():
    concepts = set(measured_concepts_for_cilt4_entry_assessment())
    for concept in (
        "ordinal reading",
        "successor/limit ordinal",
        "order type vs cardinality",
        "cofinality reading",
        "regular cardinal",
        "singular cardinal",
        "weight",
        "density",
        "character",
        "Lindelof number",
        "cellularity",
        "invariant comparison",
        "cardinal-function framework reading",
    ):
        assert concept in concepts


def test_cilt4_entry_assessment_map_points_to_direct_route_file():
    text = (ROOT / "docs/roadmap/pedagogical_volume_reorganization_map.md").read_text(encoding="utf-8")
    assert "v0.1.70-fix2 -- Cilt IV direct questionbank/assessment route closure" in text
    assert "src/pytop_questionbank/cilt4_entry_assessment_routes.py#CILT4-MS-IV-35-ORDINALS-ASSESSMENT" in text
    assert "src/pytop_questionbank/cilt4_entry_assessment_routes.py#CILT4-MS-IV-36-COFINALITY-REGULARITY-ASSESSMENT" in text
    assert "src/pytop_questionbank/cilt4_entry_assessment_routes.py#CILT4-MS-IV-38-BASIC-INVARIANTS-ASSESSMENT" in text
    assert "src/pytop_questionbank/cilt4_entry_assessment_routes.py#CILT4-MS-IV-39-CARDINAL-FUNCTION-FRAMEWORK-ASSESSMENT" in text


def test_cilt4_entry_assessment_report_is_human_readable():
    report = render_cilt4_entry_assessment_route_report()
    assert "Cilt IV entry assessment route report" in report
    assert "assessment items" in report
    assert "CILT4-MS-IV-39-CARDINAL-FUNCTION-FRAMEWORK-ASSESSMENT" in report
