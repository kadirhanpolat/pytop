"""Chapter 07--15 release-facing manuscript/examples/questionbank stabilization for v1.0.338.

v1.0.331 created the insertion queue, v1.0.334--v1.0.336 executed the
three post-checkpoint insertion passes, and v1.0.337 audited the completed
sequence. This module turns that state into a release-facing stabilization
surface: manuscript, examples_bank, and questionbank targets are checked as
active open-folder resources with no nested zip promotion and with explicit
originality guardrails.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_insertion_queue import (
    ACTIVE_SURFACES,
    default_chapter_07_15_insertion_specs,
)

RELEASE_STABILIZATION_VERSION = "v1.0.338"
PREVIOUS_VERSION = "v1.0.337"
SOURCE_QUEUE_VERSION = "v1.0.331"
SOURCE_AUDIT_VERSION = "v1.0.337"
STABILIZATION_LABEL = "Chapter 07--15 release-facing manuscript/examples/questionbank stabilization"
NEXT_EXPECTED_VERSION = "v1.0.339 manuscript/examples/questionbank release dry-run checklist"
EXPECTED_CHAPTERS = tuple(range(7, 16))
EXPECTED_SURFACES = ACTIVE_SURFACES


@dataclass(frozen=True)
class StabilizationTarget:
    chapter: int
    chapter_label: str
    surface: str
    path: str
    exists: bool
    open_folder_resource: bool
    originality_guardrail: bool
    release_ready: bool


@dataclass(frozen=True)
class SurfaceStabilizationSummary:
    surface: str
    target_count: int
    ready_count: int
    missing_count: int


@dataclass(frozen=True)
class ReleaseStabilizationReport:
    version: str
    previous_version: str
    label: str
    source_queue_version: str
    source_audit_version: str
    chapter_count: int
    target_count: int
    ready_count: int
    missing_count: int
    all_open_folder_resources: bool
    all_originality_guardrails: bool
    release_ready: bool
    surface_summaries: Tuple[SurfaceStabilizationSummary, ...]
    targets: Tuple[StabilizationTarget, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "source_queue_version": self.source_queue_version,
            "source_audit_version": self.source_audit_version,
            "chapter_count": self.chapter_count,
            "target_count": self.target_count,
            "ready_count": self.ready_count,
            "missing_count": self.missing_count,
            "all_open_folder_resources": self.all_open_folder_resources,
            "all_originality_guardrails": self.all_originality_guardrails,
            "release_ready": self.release_ready,
            "surface_summaries": [asdict(item) for item in self.surface_summaries],
            "targets": [asdict(item) for item in self.targets],
            "metadata": dict(self.metadata),
        }


def _is_open_folder_resource(path: str) -> bool:
    normalized = f"/{path}"
    return not path.endswith(".zip") and "/docs/archive/" not in normalized


def _has_originality_guardrail(text: str) -> bool:
    lowered = text.lower()
    return "do not copy" in lowered and "verbatim" in lowered


def build_release_stabilization_report(root: str | Path = ".") -> ReleaseStabilizationReport:
    root_path = Path(root)
    targets = []
    for spec in default_chapter_07_15_insertion_specs():
        path = spec.target_path
        exists = (root_path / path).exists()
        open_folder = _is_open_folder_resource(path)
        guardrail = _has_originality_guardrail(spec.originality_guardrail)
        targets.append(
            StabilizationTarget(
                chapter=spec.chapter,
                chapter_label=spec.chapter_label,
                surface=spec.surface,
                path=path,
                exists=exists,
                open_folder_resource=open_folder,
                originality_guardrail=guardrail,
                release_ready=exists and open_folder and guardrail,
            )
        )

    surface_summaries = []
    for surface in EXPECTED_SURFACES:
        surface_targets = tuple(target for target in targets if target.surface == surface)
        ready_count = sum(1 for target in surface_targets if target.release_ready)
        surface_summaries.append(
            SurfaceStabilizationSummary(
                surface=surface,
                target_count=len(surface_targets),
                ready_count=ready_count,
                missing_count=sum(1 for target in surface_targets if not target.exists),
            )
        )

    missing_count = sum(1 for target in targets if not target.exists)
    ready_count = sum(1 for target in targets if target.release_ready)
    all_open = all(target.open_folder_resource for target in targets)
    all_guardrails = all(target.originality_guardrail for target in targets)
    chapters = tuple(sorted({target.chapter for target in targets}))
    release_ready = (
        chapters == EXPECTED_CHAPTERS
        and len(targets) == 27
        and missing_count == 0
        and ready_count == len(targets)
        and all_open
        and all_guardrails
        and tuple(summary.target_count for summary in surface_summaries) == (9, 9, 9)
    )
    return ReleaseStabilizationReport(
        version=RELEASE_STABILIZATION_VERSION,
        previous_version=PREVIOUS_VERSION,
        label=STABILIZATION_LABEL,
        source_queue_version=SOURCE_QUEUE_VERSION,
        source_audit_version=SOURCE_AUDIT_VERSION,
        chapter_count=len(chapters),
        target_count=len(targets),
        ready_count=ready_count,
        missing_count=missing_count,
        all_open_folder_resources=all_open,
        all_originality_guardrails=all_guardrails,
        release_ready=release_ready,
        surface_summaries=tuple(surface_summaries),
        targets=tuple(targets),
        metadata={
            "active_surfaces": EXPECTED_SURFACES,
            "expected_chapters": EXPECTED_CHAPTERS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "archive_policy": "docs/archive bundles are evidence-only and excluded from active release targets",
            "packaging_policy": "single full package; no active nested subproject zips",
            "stabilization_scope": "release-facing manuscript/examples_bank/questionbank readiness",
        },
    )


def render_release_stabilization_report(report: ReleaseStabilizationReport) -> str:
    lines = [
        "# Chapter 07--15 Release-Facing Stabilization (v1.0.338)",
        "",
        "This report checks whether the Chapter 07--15 manuscript, examples_bank, and questionbank targets are ready for release-facing dry-run work.",
        "",
        "## Summary",
        f"- Previous version: `{report.previous_version}`",
        f"- Source queue: `{report.source_queue_version}`",
        f"- Source audit: `{report.source_audit_version}`",
        f"- Chapters covered: `{report.chapter_count}`",
        f"- Targets: `{report.target_count}`",
        f"- Ready targets: `{report.ready_count}`",
        f"- Missing targets: `{report.missing_count}`",
        f"- Open-folder resources only: `{report.all_open_folder_resources}`",
        f"- Originality guardrails present: `{report.all_originality_guardrails}`",
        f"- Release ready: `{report.release_ready}`",
        "",
        "## Surface summaries",
    ]
    for summary in report.surface_summaries:
        lines.append(
            f"- `{summary.surface}`: `{summary.ready_count}` ready / `{summary.target_count}` total / `{summary.missing_count}` missing"
        )
    lines.extend(["", "## Stabilized targets"])
    for target in report.targets:
        state = "ready" if target.release_ready else "blocked"
        lines.append(
            f"- Chapter {target.chapter:02d} / `{target.surface}` / `{state}`: `{target.path}`"
        )
    lines.extend([
        "",
        "## Policy",
        "No uploaded chapter zip or archive bundle is promoted into an active source. Stabilization remains on open-folder manuscript, examples_bank, and questionbank targets, with originality guardrails preserved.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "EXPECTED_CHAPTERS",
    "EXPECTED_SURFACES",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "RELEASE_STABILIZATION_VERSION",
    "SOURCE_AUDIT_VERSION",
    "SOURCE_QUEUE_VERSION",
    "STABILIZATION_LABEL",
    "ReleaseStabilizationReport",
    "StabilizationTarget",
    "SurfaceStabilizationSummary",
    "build_release_stabilization_report",
    "render_release_stabilization_report",
]
