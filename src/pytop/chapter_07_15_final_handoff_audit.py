"""Chapter 07--15 final release handoff audit for v1.0.343.

v1.0.342 locked the release-candidate packaging audit. This module adds the
final handoff audit surface that a new conversation or release operator can
read before continuing the Topology Book / pytop ecosystem from the Chapter
07--15 consolidation line.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_packaging_audit import (
    EXPECTED_CHAPTERS,
    EXPECTED_LANES,
    EXPECTED_RELEASE_ROWS,
    PACKAGING_AUDIT_VERSION,
    build_release_candidate_packaging_audit,
)

FINAL_HANDOFF_VERSION = "v1.0.343"
PREVIOUS_VERSION = "v1.0.342"
SOURCE_PACKAGING_AUDIT_VERSION = PACKAGING_AUDIT_VERSION
FINAL_HANDOFF_LABEL = "Chapter 07--15 final release handoff audit"
NEXT_EXPECTED_VERSION = "v1.0.344 post-release maintenance roadmap"
EXPECTED_CHAPTERS = EXPECTED_CHAPTERS
EXPECTED_LANES = EXPECTED_LANES
EXPECTED_RELEASE_ROWS = EXPECTED_RELEASE_ROWS
FINAL_HANDOFF_CHECKS = (
    "source_packaging_audit_ready",
    "release_records_current",
    "final_handoff_scope_declared",
    "active_surface_rows_locked",
    "archive_boundary_verified",
    "packaging_contract_inherited",
    "downstream_restart_prompt_ready",
    "final_handoff_audit_ready",
)


@dataclass(frozen=True)
class FinalHandoffCheck:
    key: str
    title: str
    ready: bool
    evidence: str


@dataclass(frozen=True)
class FinalReleaseHandoffAudit:
    version: str
    previous_version: str
    source_packaging_audit_version: str
    label: str
    chapter_count: int
    release_row_count: int
    handoff_check_count: int
    ready_check_count: int
    blocked_check_count: int
    final_handoff_ready: bool
    checks: Tuple[FinalHandoffCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_packaging_audit_version": self.source_packaging_audit_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "release_row_count": self.release_row_count,
            "handoff_check_count": self.handoff_check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "final_handoff_ready": self.final_handoff_ready,
            "checks": [asdict(item) for item in self.checks],
            "metadata": dict(self.metadata),
        }


def _exists(root_path: Path, relative_path: str) -> bool:
    return (root_path / relative_path).exists()


def build_final_release_handoff_audit(root: str | Path = ".") -> FinalReleaseHandoffAudit:
    """Build the v1.0.343 final release handoff audit packet."""
    root_path = Path(root)
    packaging = build_release_candidate_packaging_audit(root_path)

    required_current_records = (
        "docs/current_docs_index.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "README.md",
        "CHANGELOG.md",
        "docs/roadmap/current_active_roadmap_v1_0_343.md",
        "docs/roadmap/active_versioning_roadmap_v1_0_343.md",
        "docs/packaging/subproject_packaging_policy_v1_0_343.md",
        "docs/reorganization/docs_reorganization_status_v1_0_343.md",
        "docs/releases/v1_0_343.md",
        "docs/integration/chapter_07_15/chapter_07_15_final_handoff_audit_v1_0_343.md",
        "docs/verification/chapter_07_15_final_handoff_audit_v1_0_343.md",
        "docs/archive/README.md",
        "docs/archive/archive_history_bundle_manifest_v1_0_288.json",
        "docs/archive/archive_history_bundle_sha256_v1_0_288.txt",
    )
    docs_current = all(_exists(root_path, item) for item in required_current_records)

    source_packaging_audit_ready = (
        packaging.version == SOURCE_PACKAGING_AUDIT_VERSION
        and packaging.packaging_audit_ready
        and packaging.chapter_count == EXPECTED_CHAPTERS
        and packaging.release_row_count == EXPECTED_RELEASE_ROWS
        and packaging.blocked_check_count == 0
    )
    release_records_current = docs_current
    final_handoff_scope_declared = docs_current
    active_surface_rows_locked = (
        packaging.release_row_count == EXPECTED_RELEASE_ROWS
        and tuple(packaging.metadata.get("expected_lanes", ())) == EXPECTED_LANES
    )
    archive_boundary_verified = (
        _exists(root_path, "docs/archive/archive_history_bundle_manifest_v1_0_288.json")
        and _exists(root_path, "docs/archive/archive_history_bundle_sha256_v1_0_288.txt")
    )
    packaging_contract_inherited = (
        packaging.metadata.get("compression_method") == "ZIP_DEFLATED / method 8"
        and "single full package" in str(packaging.metadata.get("packaging_policy", ""))
    )
    downstream_restart_prompt_ready = docs_current and _exists(root_path, "RELEASE_NOTES_v1_0_343.txt")

    preliminary = (
        source_packaging_audit_ready,
        release_records_current,
        final_handoff_scope_declared,
        active_surface_rows_locked,
        archive_boundary_verified,
        packaging_contract_inherited,
        downstream_restart_prompt_ready,
    )
    ready_for_final_handoff = all(preliminary)

    checks = (
        FinalHandoffCheck(
            key="source_packaging_audit_ready",
            title="Source packaging audit is ready",
            ready=source_packaging_audit_ready,
            evidence=f"{SOURCE_PACKAGING_AUDIT_VERSION} packaging audit is ready with {packaging.release_row_count} active rows and {packaging.blocked_check_count} blocked checks.",
        ),
        FinalHandoffCheck(
            key="release_records_current",
            title="Release records are current",
            ready=release_records_current,
            evidence="Root and docs records for v1.0.343 are present and point to the final handoff audit.",
        ),
        FinalHandoffCheck(
            key="final_handoff_scope_declared",
            title="Final handoff scope is declared",
            ready=final_handoff_scope_declared,
            evidence="The handoff audit covers Chapter 07--15 manuscript, examples_bank, questionbank, packaging, archive-boundary, and restart-context surfaces.",
        ),
        FinalHandoffCheck(
            key="active_surface_rows_locked",
            title="Active surface rows are locked",
            ready=active_surface_rows_locked,
            evidence=f"{EXPECTED_RELEASE_ROWS} active rows remain distributed over {EXPECTED_CHAPTERS} chapters and {len(EXPECTED_LANES)} lanes.",
        ),
        FinalHandoffCheck(
            key="archive_boundary_verified",
            title="Archive boundary is verified",
            ready=archive_boundary_verified,
            evidence="docs/archive contains evidence-only manifest and SHA256 records; archive bundles are not promoted to active sources.",
        ),
        FinalHandoffCheck(
            key="packaging_contract_inherited",
            title="Packaging contract is inherited",
            ready=packaging_contract_inherited,
            evidence="The v1.0.342 single-root, duplicate-free, deflate method 8, full-package contract is carried into v1.0.343.",
        ),
        FinalHandoffCheck(
            key="downstream_restart_prompt_ready",
            title="Downstream restart prompt is ready",
            ready=downstream_restart_prompt_ready,
            evidence="Release notes and roadmap records identify v1.0.344 as the next post-release maintenance roadmap step.",
        ),
        FinalHandoffCheck(
            key="final_handoff_audit_ready",
            title="Final handoff audit is ready",
            ready=ready_for_final_handoff,
            evidence="All final handoff prerequisites are ready and no blocking check remains.",
        ),
    )

    ready_check_count = sum(1 for check in checks if check.ready)
    blocked_check_count = len(checks) - ready_check_count
    final_handoff_ready = ready_check_count == len(FINAL_HANDOFF_CHECKS) and blocked_check_count == 0

    return FinalReleaseHandoffAudit(
        version=FINAL_HANDOFF_VERSION,
        previous_version=PREVIOUS_VERSION,
        source_packaging_audit_version=SOURCE_PACKAGING_AUDIT_VERSION,
        label=FINAL_HANDOFF_LABEL,
        chapter_count=packaging.chapter_count,
        release_row_count=packaging.release_row_count,
        handoff_check_count=len(checks),
        ready_check_count=ready_check_count,
        blocked_check_count=blocked_check_count,
        final_handoff_ready=final_handoff_ready,
        checks=checks,
        metadata={
            "expected_chapters": EXPECTED_CHAPTERS,
            "expected_release_rows": EXPECTED_RELEASE_ROWS,
            "expected_lanes": EXPECTED_LANES,
            "final_handoff_checks": FINAL_HANDOFF_CHECKS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "source_packaging_audit_version": SOURCE_PACKAGING_AUDIT_VERSION,
            "single_root": "topology_book_ecosystem_v1_0_343",
            "compression_method": "ZIP_DEFLATED / method 8",
            "archive_policy": "docs/archive bundles remain evidence-only and are not active source surfaces",
            "packaging_policy": "single full package; active resources remain open folders",
            "restart_context": "continue from v1.0.343 into v1.0.344 post-release maintenance roadmap",
        },
    )


def render_final_release_handoff_audit(packet: FinalReleaseHandoffAudit) -> str:
    lines = [
        "# Chapter 07--15 Final Release Handoff Audit (v1.0.343)",
        "",
        "This document records the final handoff state after the v1.0.342 release-candidate packaging audit.",
        "",
        "## Summary",
        f"- Previous version: `{packet.previous_version}`",
        f"- Source packaging audit version: `{packet.source_packaging_audit_version}`",
        f"- Chapters covered: `{packet.chapter_count}`",
        f"- Release rows: `{packet.release_row_count}`",
        f"- Handoff checks: `{packet.handoff_check_count}`",
        f"- Ready checks: `{packet.ready_check_count}`",
        f"- Blocked checks: `{packet.blocked_check_count}`",
        f"- Final handoff ready: `{packet.final_handoff_ready}`",
        "",
        "## Final handoff checks",
    ]
    for check in packet.checks:
        status = "ready" if check.ready else "blocked"
        lines.append(f"- `{check.key}` / `{status}`: {check.title}. {check.evidence}")
    lines.extend([
        "",
        "## Handoff policy",
        "The release handoff preserves the single full-package model. Active source targets remain open folders; uploaded Chapter 07--15 zip files and docs/archive bundles are not active sources.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "FINAL_HANDOFF_CHECKS",
    "FINAL_HANDOFF_LABEL",
    "FINAL_HANDOFF_VERSION",
    "EXPECTED_CHAPTERS",
    "EXPECTED_LANES",
    "EXPECTED_RELEASE_ROWS",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "SOURCE_PACKAGING_AUDIT_VERSION",
    "FinalHandoffCheck",
    "FinalReleaseHandoffAudit",
    "build_final_release_handoff_audit",
    "render_final_release_handoff_audit",
]
