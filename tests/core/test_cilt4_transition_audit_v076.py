"""Tests for the v0.1.76 Cilt IV transition audit surface."""

from __future__ import annotations

import pytop
from pytop._internal.cilt4_transition_audit import (
    cilt4_transition_audit,
    cilt4_transition_criteria,
    cilt4_transition_milestone_lookup,
    render_cilt4_transition_audit_report,
)


def test_v076_transition_audit_marks_cilt_iv_ready_for_cilt_v():
    result = cilt4_transition_audit()

    assert result.is_true
    assert result.value == "cilt_iv_transition_ready"
    assert result.metadata["audit_version"] == "v0.1.76"
    assert result.metadata["ready_for_cilt_v"] is True
    assert result.metadata["closed_corridor_count"] == 11
    assert result.metadata["next_open_version"] == "v0.1.77"
    assert result.metadata["chapters_covered"] == [24, 25, 26, 27, 28, 29, 30]



def test_v076_transition_criteria_are_explicit_and_ready():
    criteria = cilt4_transition_criteria()

    assert len(criteria) == 4
    assert all(item["status"] for item in criteria)
    assert {item["criterion_id"] for item in criteria} == {
        "set_theoretic_entry_language",
        "quantitative_invariant_language",
        "comparison_route_closure",
        "warning_line_honesty",
    }
    assert all(item["unlocks_versions"] for item in criteria)



def test_v076_transition_milestone_lookup_returns_v075_close_out_record():
    result = cilt4_transition_milestone_lookup("v0.1.75")

    assert result.is_true
    assert result.metadata["version"] == "v0.1.75"
    assert "notebook / worksheet route completion" in result.metadata["title"].lower()
    assert "Chapter 29 notebooks, the shared worksheet, Chapter 30 notebooks" in result.justification[0]


def test_v076_transition_milestone_lookup_unknown_version_is_honest():
    result = cilt4_transition_milestone_lookup("v0.1.99")

    assert result.is_unknown
    assert result.metadata["version"] == "v0.1.99"
    assert "v0.1.65" in result.justification[0]
    assert "v0.1.75" in result.justification[0]


def test_v076_transition_audit_report_is_human_readable():
    report = render_cilt4_transition_audit_report()

    assert "Cilt IV transition audit report" in report
    assert "closed corridors: 11" in report
    assert "questionbank route counts:" in report
    assert "next open version: v0.1.77" in report
    assert "v0.1.77: Tightness and network invariants entry split" in report


