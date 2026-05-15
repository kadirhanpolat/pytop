"""Chapter 07--15 manuscript/examples/questionbank release dry-run checklist for v1.0.339.

v1.0.338 stabilized the release-facing manuscript, examples_bank, and
questionbank surfaces. This module turns that stabilized state into a dry-run
checklist: each chapter/surface target receives a preflight row, a review lane,
and a no-nested-zip/originality guardrail status before a later release signoff
can be attempted.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_release_stabilization import (
    EXPECTED_CHAPTERS,
    EXPECTED_SURFACES,
    build_release_stabilization_report,
)

DRY_RUN_VERSION = "v1.0.339"
PREVIOUS_VERSION = "v1.0.338"
SOURCE_STABILIZATION_VERSION = "v1.0.338"
DRY_RUN_LABEL = "Chapter 07--15 manuscript/examples/questionbank release dry-run checklist"
NEXT_EXPECTED_VERSION = "v1.0.340 release signoff packet preparation"
REVIEW_LANES = {
    "manuscript": "mathematical narrative and notation review",
    "examples_bank": "worked-example coverage and originality review",
    "questionbank": "question-family coverage and assessment-route review",
}
EXPECTED_CHECKLIST_ROWS = len(EXPECTED_CHAPTERS) * len(EXPECTED_SURFACES)


@dataclass(frozen=True)
class DryRunChecklistRow:
    chapter: int
    chapter_label: str
    surface: str
    path: str
    review_lane: str
    exists: bool
    open_folder_resource: bool
    originality_guardrail: bool
    dry_run_ready: bool


@dataclass(frozen=True)
class DryRunSurfaceSummary:
    surface: str
    review_lane: str
    row_count: int
    ready_count: int
    blocked_count: int


@dataclass(frozen=True)
class ReleaseDryRunChecklistReport:
    version: str
    previous_version: str
    source_stabilization_version: str
    label: str
    chapter_count: int
    row_count: int
    ready_count: int
    blocked_count: int
    dry_run_ready: bool
    surface_summaries: Tuple[DryRunSurfaceSummary, ...]
    rows: Tuple[DryRunChecklistRow, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_stabilization_version": self.source_stabilization_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "row_count": self.row_count,
            "ready_count": self.ready_count,
            "blocked_count": self.blocked_count,
            "dry_run_ready": self.dry_run_ready,
            "surface_summaries": [asdict(item) for item in self.surface_summaries],
            "rows": [asdict(item) for item in self.rows],
            "metadata": dict(self.metadata),
        }


def build_release_dry_run_checklist(root: str | Path = ".") -> ReleaseDryRunChecklistReport:
    root_path = Path(root)
    stabilized = build_release_stabilization_report(root_path)
    rows = []
    for target in stabilized.targets:
        review_lane = REVIEW_LANES[target.surface]
        dry_run_ready = (
            target.exists
            and target.open_folder_resource
            and target.originality_guardrail
            and (root_path / target.path).exists()
        )
        rows.append(
            DryRunChecklistRow(
                chapter=target.chapter,
                chapter_label=target.chapter_label,
                surface=target.surface,
                path=target.path,
                review_lane=review_lane,
                exists=target.exists,
                open_folder_resource=target.open_folder_resource,
                originality_guardrail=target.originality_guardrail,
                dry_run_ready=dry_run_ready,
            )
        )

    surface_summaries = []
    for surface in EXPECTED_SURFACES:
        surface_rows = tuple(row for row in rows if row.surface == surface)
        ready_count = sum(1 for row in surface_rows if row.dry_run_ready)
        surface_summaries.append(
            DryRunSurfaceSummary(
                surface=surface,
                review_lane=REVIEW_LANES[surface],
                row_count=len(surface_rows),
                ready_count=ready_count,
                blocked_count=len(surface_rows) - ready_count,
            )
        )

    chapters = tuple(sorted({row.chapter for row in rows}))
    ready_count = sum(1 for row in rows if row.dry_run_ready)
    blocked_count = len(rows) - ready_count
    dry_run_ready = (
        stabilized.release_ready
        and chapters == EXPECTED_CHAPTERS
        and len(rows) == EXPECTED_CHECKLIST_ROWS
        and ready_count == EXPECTED_CHECKLIST_ROWS
        and blocked_count == 0
        and tuple(summary.row_count for summary in surface_summaries) == (9, 9, 9)
    )
    return ReleaseDryRunChecklistReport(
        version=DRY_RUN_VERSION,
        previous_version=PREVIOUS_VERSION,
        source_stabilization_version=SOURCE_STABILIZATION_VERSION,
        label=DRY_RUN_LABEL,
        chapter_count=len(chapters),
        row_count=len(rows),
        ready_count=ready_count,
        blocked_count=blocked_count,
        dry_run_ready=dry_run_ready,
        surface_summaries=tuple(surface_summaries),
        rows=tuple(rows),
        metadata={
            "expected_chapters": EXPECTED_CHAPTERS,
            "expected_surfaces": EXPECTED_SURFACES,
            "expected_checklist_rows": EXPECTED_CHECKLIST_ROWS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "archive_policy": "docs/archive bundles remain evidence-only and are excluded from dry-run rows",
            "packaging_policy": "single full package; active resources remain open folders",
            "dry_run_scope": "release-facing manuscript/examples_bank/questionbank checklist before signoff packet preparation",
        },
    )


def render_release_dry_run_checklist(report: ReleaseDryRunChecklistReport) -> str:
    lines = [
        "# Chapter 07--15 Release Dry-Run Checklist (v1.0.339)",
        "",
        "This checklist prepares the stabilized Chapter 07--15 manuscript, examples_bank, and questionbank surfaces for a later release signoff packet.",
        "",
        "## Summary",
        f"- Previous version: `{report.previous_version}`",
        f"- Source stabilization: `{report.source_stabilization_version}`",
        f"- Chapters covered: `{report.chapter_count}`",
        f"- Checklist rows: `{report.row_count}`",
        f"- Ready rows: `{report.ready_count}`",
        f"- Blocked rows: `{report.blocked_count}`",
        f"- Dry-run ready: `{report.dry_run_ready}`",
        "",
        "## Surface lanes",
    ]
    for summary in report.surface_summaries:
        lines.append(
            f"- `{summary.surface}`: `{summary.ready_count}` ready / `{summary.row_count}` total / `{summary.blocked_count}` blocked — {summary.review_lane}"
        )
    lines.extend(["", "## Checklist rows"])
    for row in report.rows:
        state = "ready" if row.dry_run_ready else "blocked"
        lines.append(
            f"- Chapter {row.chapter:02d} / `{row.surface}` / `{state}` / {row.review_lane}: `{row.path}`"
        )
    lines.extend([
        "",
        "## Policy",
        "No uploaded Chapter 07--15 zip and no archive bundle is promoted into an active source. The dry-run checklist points only to active open-folder targets and retains originality guardrails.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "DRY_RUN_LABEL",
    "DRY_RUN_VERSION",
    "EXPECTED_CHECKLIST_ROWS",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "REVIEW_LANES",
    "SOURCE_STABILIZATION_VERSION",
    "DryRunChecklistRow",
    "DryRunSurfaceSummary",
    "ReleaseDryRunChecklistReport",
    "build_release_dry_run_checklist",
    "render_release_dry_run_checklist",
]
