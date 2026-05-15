"""Cilt IV interim audit and Cilt V transition criteria (v0.1.76).

This module closes the v0.1.65--v0.1.75 Cilt IV line with a durable audit
surface. It records the stabilized corridor milestones, summarizes the
comparison/assessment/worksheet support that now exists around the cardinal
function block, and makes the next Cilt V transition gates explicit.

Roadmap reference:
  v0.1.76 -- Write the Cilt IV interim audit and clarify the Cilt V transition
  criteria.
"""

from __future__ import annotations

from typing import Any

from .cardinal_function_examples import (
    cardinal_function_comparison_exercises,
    cardinal_function_notebook_route_alignment,
)
from .result import Result

__all__ = [
    "cilt4_transition_audit",
    "cilt4_transition_criteria",
    "cilt4_transition_milestone_lookup",
    "render_cilt4_transition_audit_report",
]

VERSION = "0.1.76"


_CILT4_MILESTONES: dict[str, dict[str, Any]] = {
    "v0.1.65": {
        "title": "Cardinal-number entry corridor",
        "chapter": 26,
        "durable_api": (
            "cardinality_class",
            "cardinal_number_profile",
            "analyze_cardinal_numbers",
        ),
        "summary": (
            "Cardinality tiers, countable/uncountable threshold language, Cantor "
            "and Schroeder-Bernstein bridge notes are stable."
        ),
        "readiness_signal": "Set-size language is available before topological cardinal functions.",
    },
    "v0.1.66": {
        "title": "Ordinal-number entry corridor",
        "chapter": 27,
        "durable_api": (
            "ordinal_class",
            "ordinal_profile",
            "analyze_ordinal_numbers",
        ),
        "summary": (
            "Successor/limit and order-type language is callable, so later "
            "ordinal-indexed examples have a stable reading layer."
        ),
        "readiness_signal": "Order-type vocabulary is separated from cardinal-size vocabulary.",
    },
    "v0.1.67": {
        "title": "Cofinality and regularity entry corridor",
        "chapter": 28,
        "durable_api": (
            "cofinality_class",
            "cofinality_profile",
            "analyze_cofinality",
        ),
        "summary": (
            "Regular/singular distinction and cofinality reading are stable "
            "enough for cardinal-topology warning language."
        ),
        "readiness_signal": "Regularity/cofinality language is available before advanced invariant growth.",
    },
    "v0.1.68": {
        "title": "Quantitative-topology positioning corridor",
        "chapter": 24,
        "durable_api": (
            "quantitative_profile",
            "analyze_quantitative_topology",
        ),
        "summary": (
            "Qualitative properties are restated as cardinal thresholds "
            "w(X), d(X), chi(X), and L(X)."
        ),
        "readiness_signal": "The package can explain why countability properties are threshold statements.",
    },
    "v0.1.69": {
        "title": "Basic topological invariants corridor",
        "chapter": 25,
        "durable_api": (
            "topological_invariants_profile",
            "analyze_topological_invariants",
        ),
        "summary": (
            "The invariant inventory now includes cellularity, spread, network "
            "weight, and tightness in addition to the threshold quartet."
        ),
        "readiness_signal": "The later Cilt V topics already have a named precursor vocabulary.",
    },
    "v0.1.70": {
        "title": "Cardinal-function framework corridor",
        "chapter": 29,
        "durable_api": (
            "cardinal_function_definition",
            "cardinal_function_comparison",
            "cardinal_functions_framework_profile",
            "analyze_cardinal_functions_framework",
        ),
        "summary": (
            "Definitions, comparison theorems, and example expectations are "
            "split into stable layers."
        ),
        "readiness_signal": "Definition/comparison/example responsibilities are no longer mixed together.",
    },
    "v0.1.71": {
        "title": "Cardinal-function example catalog expansion",
        "chapter": 29,
        "durable_api": (
            "cardinal_function_examples_catalog",
            "cardinal_function_example",
            "cardinal_function_examples_by_layer",
            "cardinal_function_workbook_tasks",
            "analyze_cardinal_function_examples",
        ),
        "summary": (
            "Finite, safe infinite, metric, and warning examples are stored as "
            "reusable records rather than prose-only notes."
        ),
        "readiness_signal": "Future transition work can reuse worked examples without reauthoring them.",
    },
    "v0.1.72": {
        "title": "Comparison exercises and notebook-route alignment",
        "chapter": 29,
        "durable_api": (
            "cardinal_function_comparison_exercises",
            "cardinal_function_notebook_route_alignment",
        ),
        "summary": (
            "Five durable comparison-route identifiers connect examples, Chapter 29, "
            "and the notebook pair."
        ),
        "readiness_signal": "The same route identifiers survive from examples into notebooks.",
    },
    "v0.1.73": {
        "title": "Comparison-route assessment/questionbank alignment",
        "chapter": 29,
        "durable_api": (
            "build_cilt4_cardinal_function_comparison_assessment_routes",
            "cilt4_cardinal_function_comparison_assessment_alignment",
            "cilt4_cardinal_function_comparison_assessment_summary",
        ),
        "summary": (
            "The five comparison routes now have generated-question-ready "
            "assessment route IDs and measurable prompts."
        ),
        "readiness_signal": "The corridor is no longer notebook-only; it has direct assessment handles.",
    },
    "v0.1.74": {
        "title": "Assessment feedback and answer-key/rubric alignment",
        "chapter": 29,
        "durable_api": (
            "cilt4_cardinal_function_comparison_feedback_alignment",
            "cilt4_cardinal_function_comparison_feedback_summary",
            "render_cilt4_cardinal_function_comparison_feedback_report",
        ),
        "summary": (
            "The same five assessment route IDs are tied to durable answer-key, "
            "rubric, and feedback-focus surfaces."
        ),
        "readiness_signal": "Teacher-side moderation uses the same route identifiers as student work.",
    },
    "v0.1.75": {
        "title": "Notebook / worksheet route completion",
        "chapter": 30,
        "durable_api": (
            "cilt4_cardinal_function_comparison_notebook_worksheet_alignment",
            "cilt4_cardinal_function_comparison_notebook_worksheet_summary",
            "render_cilt4_cardinal_function_comparison_notebook_worksheet_report",
        ),
        "summary": (
            "Chapter 29 notebooks, the shared worksheet, Chapter 30 notebooks, and "
            "teacher surfaces now share the same five route identifiers."
        ),
        "readiness_signal": "The comparison corridor is stable across student and teacher surfaces.",
    },
}

_CILT5_TRANSITION_CRITERIA: tuple[dict[str, Any], ...] = (
    {
        "criterion_id": "set_theoretic_entry_language",
        "label": "Set-theoretic entry language is stable",
        "status": True,
        "evidence_versions": ("v0.1.65", "v0.1.66", "v0.1.67"),
        "supports": (
            "cardinality tiers",
            "successor/limit ordinal reading",
            "cofinality and regular/singular distinction",
        ),
        "transition_use": (
            "Cilt V can refer to regularity, cofinality, and threshold hierarchy "
            "without reopening the entry corridor."
        ),
        "unlocks_versions": ("v0.1.77", "v0.1.78"),
    },
    {
        "criterion_id": "quantitative_invariant_language",
        "label": "Quantitative and invariant language is stable",
        "status": True,
        "evidence_versions": ("v0.1.68", "v0.1.69", "v0.1.70"),
        "supports": (
            "w/d/chi/L threshold reading",
            "network weight and tightness precursor vocabulary",
            "definition/comparison/example separation",
        ),
        "transition_use": (
            "Cilt V can start with tighter invariant families rather than re-explaining "
            "why cardinal functions are topological."
        ),
        "unlocks_versions": ("v0.1.77", "v0.1.79", "v0.1.80"),
    },
    {
        "criterion_id": "comparison_route_closure",
        "label": "Comparison routes are closed across student and teacher surfaces",
        "status": True,
        "evidence_versions": ("v0.1.71", "v0.1.72", "v0.1.73", "v0.1.74", "v0.1.75"),
        "supports": (
            "worked examples",
            "notebook-route identifiers",
            "assessment route IDs",
            "answer-key/rubric linkage",
            "worksheet completion",
        ),
        "transition_use": (
            "The package can advance into Cilt V while preserving the same corridor "
            "discipline from examples through evaluation."
        ),
        "unlocks_versions": ("v0.1.77", "v0.1.78"),
    },
    {
        "criterion_id": "warning_line_honesty",
        "label": "Blocked shortcuts are explicit before the Cilt V jump",
        "status": True,
        "evidence_versions": ("v0.1.70", "v0.1.71", "v0.1.72", "v0.1.74", "v0.1.75"),
        "supports": (
            "metric is not blindly second-countable",
            "compact is not blindly small-cardinal",
            "local smallness is not global smallness",
        ),
        "transition_use": (
            "Cilt V may widen the invariant vocabulary without flattening the guard "
            "lines that keep examples mathematically honest."
        ),
        "unlocks_versions": ("v0.1.77", "v0.1.80"),
    },
)

_CILT5_TARGET_LINE: tuple[dict[str, Any], ...] = (
    {
        "version": "v0.1.77",
        "title": "Tightness and network invariants entry split",
        "focus": (
            "Separate introductory and advanced lanes before the cardinal-topology "
            "vocabulary becomes too dense."
        ),
    },
    {
        "version": "v0.1.78",
        "title": "Hereditary and local cardinal functions strengthening",
        "focus": (
            "Promote local/hereditary behavior now that the witness discipline is stable."
        ),
    },
    {
        "version": "v0.1.79",
        "title": "Classical cardinal inequalities reinforcement",
        "focus": (
            "Use the comparison corridor to support the main inequality block with "
            "examples, tests, and questionbank surfaces."
        ),
    },
    {
        "version": "v0.1.80",
        "title": "Compactness and cardinal functions reassessment",
        "focus": (
            "Revisit compactness only after the warning-line discipline and the small-cardinal "
            "guard rails are explicit."
        ),
    },
)

_CILT4_CHAPTERS_COVERED = (24, 25, 26, 27, 28, 29, 30)


def _questionbank_support_summary() -> dict[str, Any]:
    from pytop_questionbank.cilt4_entry_assessment_routes import (
        cilt4_cardinal_function_comparison_assessment_route_ids,
        cilt4_cardinal_function_comparison_assessment_summary,
        cilt4_cardinal_function_comparison_feedback_summary,
        cilt4_cardinal_function_comparison_notebook_worksheet_summary,
        cilt4_cardinal_function_comparison_route_ids,
        cilt4_entry_assessment_route_summary,
        route_ids_for_cilt4_entry_assessment,
    )

    return {
        "entry_assessment_summary": cilt4_entry_assessment_route_summary(),
        "entry_assessment_route_ids": route_ids_for_cilt4_entry_assessment(),
        "comparison_route_ids": cilt4_cardinal_function_comparison_route_ids(),
        "comparison_assessment_route_ids": cilt4_cardinal_function_comparison_assessment_route_ids(),
        "comparison_assessment_summary": cilt4_cardinal_function_comparison_assessment_summary(),
        "comparison_feedback_summary": cilt4_cardinal_function_comparison_feedback_summary(),
        "comparison_notebook_worksheet_summary": cilt4_cardinal_function_comparison_notebook_worksheet_summary(),
    }


def _milestone_records() -> dict[str, dict[str, Any]]:
    return {
        version: {
            "title": data["title"],
            "chapter": data["chapter"],
            "durable_api": list(data["durable_api"]),
            "summary": data["summary"],
            "readiness_signal": data["readiness_signal"],
        }
        for version, data in _CILT4_MILESTONES.items()
    }


def cilt4_transition_criteria() -> tuple[dict[str, Any], ...]:
    """Return the explicit readiness criteria for the Cilt IV -> Cilt V transition."""
    return tuple(
        {
            "criterion_id": item["criterion_id"],
            "label": item["label"],
            "status": item["status"],
            "evidence_versions": list(item["evidence_versions"]),
            "supports": list(item["supports"]),
            "transition_use": item["transition_use"],
            "unlocks_versions": list(item["unlocks_versions"]),
        }
        for item in _CILT5_TRANSITION_CRITERIA
    )


def cilt4_transition_audit(include_support_details: bool = False) -> Result:
    """Return a structured interim audit for the full Cilt IV line."""
    questionbank = _questionbank_support_summary()
    comparison_routes = cardinal_function_comparison_exercises()
    notebook_routes = cardinal_function_notebook_route_alignment()
    criteria = cilt4_transition_criteria()
    completion_summary = questionbank["comparison_notebook_worksheet_summary"]
    ready_for_cilt_v = all(item["status"] for item in criteria) and (
        completion_summary["route_completion_ready_count"] == len(comparison_routes)
    )

    metadata: dict[str, Any] = {
        "operator": "cilt4_transition_audit",
        "cilt": "IV",
        "phase": "v0.1.65--v0.1.76",
        "audit_version": "v0.1.76",
        "closed_corridor_count": len(_CILT4_MILESTONES),
        "corridors": _milestone_records(),
        "chapters_covered": list(_CILT4_CHAPTERS_COVERED),
        "comparison_route_count": len(comparison_routes),
        "notebook_alignment_count": len(notebook_routes),
        "entry_assessment_summary": questionbank["entry_assessment_summary"],
        "comparison_assessment_summary": questionbank["comparison_assessment_summary"],
        "comparison_feedback_summary": questionbank["comparison_feedback_summary"],
        "comparison_notebook_worksheet_summary": completion_summary,
        "transition_criteria": list(criteria),
        "next_cilt_v_targets": list(_CILT5_TARGET_LINE),
        "next_open_version": "v0.1.77",
        "ready_for_cilt_v": ready_for_cilt_v,
        "blocked_shortcuts": [
            "metric does not automatically imply second-countable",
            "compactness does not automatically imply small cardinal values",
            "local witness smallness does not automatically imply global witness smallness",
        ],
    }

    if include_support_details:
        metadata["entry_assessment_route_ids"] = list(questionbank["entry_assessment_route_ids"])
        metadata["comparison_route_ids"] = list(questionbank["comparison_route_ids"])
        metadata["comparison_assessment_route_ids"] = list(
            questionbank["comparison_assessment_route_ids"]
        )
        metadata["notebook_alignment_route_ids"] = [
            row["route_id"] for row in notebook_routes
        ]

    return Result.true(
        mode="exact",
        value="cilt_iv_transition_ready",
        justification=[
            "Cilt IV (v0.1.65--v0.1.75) is stable enough for a transition audit: "
            "set-theoretic entry language, quantitative invariant language, "
            "comparison routes, teacher feedback, and notebook/worksheet closure "
            "now coexist under durable APIs.",
            "The next open work no longer needs another Cilt IV closure pass; it can "
            "move into the Cilt V line beginning with the tighter network/tightness split "
            "while preserving the same warning-line discipline.",
        ],
        metadata=metadata,
    )


def cilt4_transition_milestone_lookup(version: str) -> Result:
    """Return the audit record for one Cilt IV milestone version."""
    key = str(version).strip()
    if key not in _CILT4_MILESTONES:
        return Result.unknown(
            mode="symbolic",
            value="cilt4_transition_milestone_lookup",
            justification=[
                f"No Cilt IV transition-audit milestone record for {version!r}. "
                f"Available: {', '.join(sorted(_CILT4_MILESTONES))}."
            ],
            metadata={
                "operator": "cilt4_transition_milestone_lookup",
                "version": version,
            },
        )

    data = _CILT4_MILESTONES[key]
    return Result.true(
        mode="exact",
        value=key,
        justification=[data["summary"]],
        metadata={
            "operator": "cilt4_transition_milestone_lookup",
            "version": key,
            "title": data["title"],
            "chapter": data["chapter"],
            "durable_api": list(data["durable_api"]),
            "readiness_signal": data["readiness_signal"],
            "audit_version": "v0.1.76",
            "cilt_iv_transition_audit": True,
        },
    )


def render_cilt4_transition_audit_report() -> str:
    """Return a human-readable report for the Cilt IV interim audit."""
    audit = cilt4_transition_audit()
    metadata = audit.metadata
    criteria = metadata["transition_criteria"]
    lines = [
        "Cilt IV transition audit report",
        "",
        f"- closed corridors: {metadata['closed_corridor_count']}",
        f"- chapters covered: {', '.join(str(ch) for ch in metadata['chapters_covered'])}",
        f"- comparison routes: {metadata['comparison_route_count']}",
        (
            "- questionbank route counts: "
            f"entry={metadata['entry_assessment_summary']['route_count']}; "
            f"assessment={metadata['comparison_assessment_summary']['route_count']}; "
            f"feedback-ready={metadata['comparison_feedback_summary']['feedback_ready_count']}; "
            f"notebook/worksheet-ready="
            f"{metadata['comparison_notebook_worksheet_summary']['route_completion_ready_count']}"
        ),
        f"- ready for Cilt V: {metadata['ready_for_cilt_v']}",
        f"- next open version: {metadata['next_open_version']}",
        "",
        "Transition criteria:",
    ]
    for criterion in criteria:
        lines.append(
            f"- {criterion['criterion_id']}: ready={criterion['status']}; "
            f"evidence={', '.join(criterion['evidence_versions'])}; "
            f"unlocks={', '.join(criterion['unlocks_versions'])}"
        )
    lines.extend(["", "Next Cilt V targets:"])
    for target in metadata["next_cilt_v_targets"]:
        lines.append(f"- {target['version']}: {target['title']}")
    return "\n".join(lines)
