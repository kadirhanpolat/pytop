"""Chapter 07--15 release signoff packet preparation for v1.0.340.

v1.0.339 established a release dry-run checklist for manuscript,
examples_bank, and questionbank targets. This module prepares a compact,
testable signoff packet from that dry-run state without promoting uploaded
chapter zip files or archive bundles into active sources.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_release_dry_run_checklist import (
    DRY_RUN_VERSION,
    EXPECTED_CHECKLIST_ROWS,
    REVIEW_LANES,
    build_release_dry_run_checklist,
)

SIGNOFF_VERSION = "v1.0.340"
PREVIOUS_VERSION = "v1.0.339"
SOURCE_DRY_RUN_VERSION = DRY_RUN_VERSION
SIGNOFF_LABEL = "Chapter 07--15 release signoff packet preparation"
NEXT_EXPECTED_VERSION = "v1.0.341 release candidate verification"
SIGNOFF_SECTIONS = (
    "dry_run_readiness",
    "active_surface_coverage",
    "documentation_index",
    "packaging_policy",
    "archive_evidence_boundary",
    "preservation_statement",
    "test_surface",
)


@dataclass(frozen=True)
class SignoffSection:
    key: str
    title: str
    ready: bool
    evidence: str


@dataclass(frozen=True)
class ReleaseSignoffPacket:
    version: str
    previous_version: str
    source_dry_run_version: str
    label: str
    chapter_count: int
    checklist_row_count: int
    ready_checklist_rows: int
    blocked_checklist_rows: int
    section_count: int
    ready_section_count: int
    blocked_section_count: int
    signoff_ready: bool
    sections: Tuple[SignoffSection, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_dry_run_version": self.source_dry_run_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "checklist_row_count": self.checklist_row_count,
            "ready_checklist_rows": self.ready_checklist_rows,
            "blocked_checklist_rows": self.blocked_checklist_rows,
            "section_count": self.section_count,
            "ready_section_count": self.ready_section_count,
            "blocked_section_count": self.blocked_section_count,
            "signoff_ready": self.signoff_ready,
            "sections": [asdict(item) for item in self.sections],
            "metadata": dict(self.metadata),
        }


def _exists(root_path: Path, relative_path: str) -> bool:
    return (root_path / relative_path).exists()


def build_release_signoff_packet(root: str | Path = ".") -> ReleaseSignoffPacket:
    root_path = Path(root)
    dry_run = build_release_dry_run_checklist(root_path)

    required_docs = (
        "docs/current_docs_index.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "README.md",
        "CHANGELOG.md",
        "docs/roadmap/current_active_roadmap_v1_0_339.md",
        "docs/roadmap/active_versioning_roadmap_v1_0_339.md",
        "docs/packaging/subproject_packaging_policy_v1_0_339.md",
        "docs/reorganization/docs_reorganization_status_v1_0_339.md",
        "docs/archive/README.md",
        "docs/archive/archive_history_bundle_manifest_v1_0_288.json",
    )
    docs_ready = all(_exists(root_path, item) for item in required_docs)

    surface_rows_ready = (
        dry_run.row_count == EXPECTED_CHECKLIST_ROWS
        and dry_run.ready_count == EXPECTED_CHECKLIST_ROWS
        and dry_run.blocked_count == 0
    )
    no_archive_promotion = all("/docs/archive/" not in f"/{row.path}" for row in dry_run.rows)
    no_nested_active_zip = all(not row.path.endswith(".zip") for row in dry_run.rows)
    all_paths_exist = all(_exists(root_path, row.path) for row in dry_run.rows)

    sections = (
        SignoffSection(
            key="dry_run_readiness",
            title="Dry-run checklist is ready",
            ready=dry_run.dry_run_ready,
            evidence=f"{dry_run.ready_count}/{dry_run.row_count} dry-run rows are ready.",
        ),
        SignoffSection(
            key="active_surface_coverage",
            title="Chapter 07--15 active surfaces are covered",
            ready=surface_rows_ready and all_paths_exist and set(REVIEW_LANES) == {"manuscript", "examples_bank", "questionbank"},
            evidence="The packet covers 9 chapters across manuscript, examples_bank, and questionbank surfaces.",
        ),
        SignoffSection(
            key="documentation_index",
            title="Release documentation index is present",
            ready=docs_ready,
            evidence="Root docs, roadmap docs, packaging policy, reorganization status, and archive policy files are present.",
        ),
        SignoffSection(
            key="packaging_policy",
            title="Single full-package packaging policy is preserved",
            ready=no_nested_active_zip,
            evidence="Active rows point to open-folder resources and no active row ends with .zip.",
        ),
        SignoffSection(
            key="archive_evidence_boundary",
            title="Archive bundle remains evidence-only",
            ready=no_archive_promotion,
            evidence="No signoff row promotes docs/archive content into an active source surface.",
        ),
        SignoffSection(
            key="preservation_statement",
            title="Preservation statement is explicit",
            ready=True,
            evidence="No deletion or move is requested by this packet; mathematical sources, code, tests, docs, examples_bank, manuscript, and notebooks are preserved.",
        ),
        SignoffSection(
            key="test_surface",
            title="Test surface is defined for signoff packet",
            ready=True,
            evidence="This module has a direct test surface at tests/core/test_chapter_07_15_release_signoff_packet_v340.py.",
        ),
    )

    ready_section_count = sum(1 for section in sections if section.ready)
    blocked_section_count = len(sections) - ready_section_count
    signoff_ready = (
        dry_run.dry_run_ready
        and surface_rows_ready
        and all_paths_exist
        and ready_section_count == len(SIGNOFF_SECTIONS)
        and blocked_section_count == 0
    )

    return ReleaseSignoffPacket(
        version=SIGNOFF_VERSION,
        previous_version=PREVIOUS_VERSION,
        source_dry_run_version=SOURCE_DRY_RUN_VERSION,
        label=SIGNOFF_LABEL,
        chapter_count=dry_run.chapter_count,
        checklist_row_count=dry_run.row_count,
        ready_checklist_rows=dry_run.ready_count,
        blocked_checklist_rows=dry_run.blocked_count,
        section_count=len(sections),
        ready_section_count=ready_section_count,
        blocked_section_count=blocked_section_count,
        signoff_ready=signoff_ready,
        sections=sections,
        metadata={
            "expected_checklist_rows": EXPECTED_CHECKLIST_ROWS,
            "expected_sections": SIGNOFF_SECTIONS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "source_review_lanes": REVIEW_LANES,
            "archive_policy": "docs/archive bundles remain evidence-only and are not active source surfaces",
            "packaging_policy": "single full package; active resources remain open folders",
            "signoff_scope": "release-facing Chapter 07--15 manuscript/examples_bank/questionbank signoff preparation",
        },
    )


def render_release_signoff_packet(packet: ReleaseSignoffPacket) -> str:
    lines = [
        "# Chapter 07--15 Release Signoff Packet (v1.0.340)",
        "",
        "This packet prepares Chapter 07--15 manuscript, examples_bank, and questionbank targets for release candidate verification.",
        "",
        "## Summary",
        f"- Previous version: `{packet.previous_version}`",
        f"- Source dry-run version: `{packet.source_dry_run_version}`",
        f"- Chapters covered: `{packet.chapter_count}`",
        f"- Checklist rows: `{packet.checklist_row_count}`",
        f"- Ready checklist rows: `{packet.ready_checklist_rows}`",
        f"- Blocked checklist rows: `{packet.blocked_checklist_rows}`",
        f"- Signoff sections: `{packet.section_count}`",
        f"- Ready sections: `{packet.ready_section_count}`",
        f"- Blocked sections: `{packet.blocked_section_count}`",
        f"- Signoff ready: `{packet.signoff_ready}`",
        "",
        "## Signoff sections",
    ]
    for section in packet.sections:
        status = "ready" if section.ready else "blocked"
        lines.append(f"- `{section.key}` / `{status}`: {section.title}. {section.evidence}")
    lines.extend([
        "",
        "## Policy",
        "The signoff packet preserves the single full-package model. Active source targets remain open folders; uploaded Chapter 07--15 zips and docs/archive bundles are not treated as active sources.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "SIGNOFF_LABEL",
    "SIGNOFF_SECTIONS",
    "SIGNOFF_VERSION",
    "SOURCE_DRY_RUN_VERSION",
    "ReleaseSignoffPacket",
    "SignoffSection",
    "build_release_signoff_packet",
    "render_release_signoff_packet",
]
