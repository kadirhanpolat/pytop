
"""Chapter 07--15 release candidate packaging audit for v1.0.342.

v1.0.341 verified the release-candidate state. This module turns that
candidate state into a release packaging audit surface: single root,
deflate-only file entries, duplicate-entry prevention, archive bundle
boundary checks, and open-folder active source preservation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_release_candidate_verification import (
    CANDIDATE_VERSION,
    EXPECTED_CHAPTERS,
    EXPECTED_LANES,
    EXPECTED_RELEASE_ROWS,
    build_release_candidate_verification,
)

PACKAGING_AUDIT_VERSION = "v1.0.342"
PREVIOUS_VERSION = "v1.0.341"
SOURCE_CANDIDATE_VERSION = CANDIDATE_VERSION
PACKAGING_AUDIT_LABEL = "Chapter 07--15 release candidate packaging audit"
NEXT_EXPECTED_VERSION = "v1.0.343 final release handoff audit"
EXPECTED_RELEASE_ROWS = EXPECTED_RELEASE_ROWS
EXPECTED_CHAPTERS = EXPECTED_CHAPTERS
EXPECTED_LANES = EXPECTED_LANES
PACKAGING_AUDIT_CHECKS = (
    "source_candidate_ready",
    "single_root_contract_declared",
    "deflate_contract_declared",
    "duplicate_entry_contract_declared",
    "archive_bundle_boundary_declared",
    "active_open_folder_contract_preserved",
    "test_surface_available",
    "packaging_audit_ready",
)


@dataclass(frozen=True)
class PackagingAuditCheck:
    key: str
    title: str
    ready: bool
    evidence: str


@dataclass(frozen=True)
class ReleaseCandidatePackagingAudit:
    version: str
    previous_version: str
    source_candidate_version: str
    label: str
    chapter_count: int
    release_row_count: int
    audit_check_count: int
    ready_check_count: int
    blocked_check_count: int
    packaging_audit_ready: bool
    checks: Tuple[PackagingAuditCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_candidate_version": self.source_candidate_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "release_row_count": self.release_row_count,
            "audit_check_count": self.audit_check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "packaging_audit_ready": self.packaging_audit_ready,
            "checks": [asdict(item) for item in self.checks],
            "metadata": dict(self.metadata),
        }


def _exists(root_path: Path, relative_path: str) -> bool:
    return (root_path / relative_path).exists()


def build_release_candidate_packaging_audit(root: str | Path = ".") -> ReleaseCandidatePackagingAudit:
    """Build the v1.0.342 release-candidate packaging audit packet."""
    root_path = Path(root)
    candidate = build_release_candidate_verification(root_path)

    required_current_records = (
        "docs/current_docs_index.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "README.md",
        "CHANGELOG.md",
        "docs/roadmap/current_active_roadmap_v1_0_342.md",
        "docs/roadmap/active_versioning_roadmap_v1_0_342.md",
        "docs/packaging/subproject_packaging_policy_v1_0_342.md",
        "docs/reorganization/docs_reorganization_status_v1_0_342.md",
        "docs/releases/v1_0_342.md",
        "docs/integration/chapter_07_15/chapter_07_15_packaging_audit_v1_0_342.md",
        "docs/verification/chapter_07_15_packaging_audit_v1_0_342.md",
        "docs/archive/README.md",
        "docs/archive/archive_history_bundle_manifest_v1_0_288.json",
    )
    docs_current = all(_exists(root_path, item) for item in required_current_records)

    source_candidate_ready = (
        candidate.version == SOURCE_CANDIDATE_VERSION
        and candidate.release_candidate_ready
        and candidate.chapter_count == EXPECTED_CHAPTERS
        and candidate.release_row_count == EXPECTED_RELEASE_ROWS
        and candidate.blocked_check_count == 0
    )
    single_root_contract_declared = docs_current
    deflate_contract_declared = docs_current
    duplicate_entry_contract_declared = docs_current
    archive_bundle_boundary_declared = _exists(root_path, "docs/archive/archive_history_bundle_manifest_v1_0_288.json")
    active_open_folder_contract_preserved = tuple(candidate.metadata.get("expected_lanes", ())) == EXPECTED_LANES
    test_surface_available = _exists(root_path, "tests/core/test_chapter_07_15_packaging_audit_v342.py")

    preliminary = (
        source_candidate_ready,
        single_root_contract_declared,
        deflate_contract_declared,
        duplicate_entry_contract_declared,
        archive_bundle_boundary_declared,
        active_open_folder_contract_preserved,
        test_surface_available,
    )
    ready_for_packaging_audit = all(preliminary)

    checks = (
        PackagingAuditCheck(
            key="source_candidate_ready",
            title="Source release candidate is ready",
            ready=source_candidate_ready,
            evidence=f"{SOURCE_CANDIDATE_VERSION} candidate is ready with {candidate.release_row_count} active rows and {candidate.blocked_check_count} blocked checks.",
        ),
        PackagingAuditCheck(
            key="single_root_contract_declared",
            title="Single internal root contract is declared",
            ready=single_root_contract_declared,
            evidence="The v1.0.342 records require exactly one internal root named topology_book_ecosystem_v1_0_342.",
        ),
        PackagingAuditCheck(
            key="deflate_contract_declared",
            title="Deflate compression contract is declared",
            ready=deflate_contract_declared,
            evidence="All delivered file entries must use ZIP_DEFLATED / method 8.",
        ),
        PackagingAuditCheck(
            key="duplicate_entry_contract_declared",
            title="Duplicate-entry rejection contract is declared",
            ready=duplicate_entry_contract_declared,
            evidence="The release zip must contain zero duplicate entries before the sandbox link is reported.",
        ),
        PackagingAuditCheck(
            key="archive_bundle_boundary_declared",
            title="Archive bundle boundary is declared",
            ready=archive_bundle_boundary_declared,
            evidence="docs/archive remains evidence-only and any archive_history_bundle zip must be independently readable and SHA256-verified.",
        ),
        PackagingAuditCheck(
            key="active_open_folder_contract_preserved",
            title="Active open-folder source contract is preserved",
            ready=active_open_folder_contract_preserved,
            evidence="manuscript, examples_bank, and questionbank active lanes remain open-folder resources.",
        ),
        PackagingAuditCheck(
            key="test_surface_available",
            title="Packaging-audit test surface exists",
            ready=test_surface_available,
            evidence="tests/core/test_chapter_07_15_packaging_audit_v342.py is present.",
        ),
        PackagingAuditCheck(
            key="packaging_audit_ready",
            title="Packaging audit is ready for final release handoff audit",
            ready=ready_for_packaging_audit,
            evidence="All packaging prerequisites are ready before the v1.0.343 final release handoff audit.",
        ),
    )

    ready_check_count = sum(1 for check in checks if check.ready)
    blocked_check_count = len(checks) - ready_check_count
    packaging_audit_ready = ready_check_count == len(PACKAGING_AUDIT_CHECKS) and blocked_check_count == 0

    return ReleaseCandidatePackagingAudit(
        version=PACKAGING_AUDIT_VERSION,
        previous_version=PREVIOUS_VERSION,
        source_candidate_version=SOURCE_CANDIDATE_VERSION,
        label=PACKAGING_AUDIT_LABEL,
        chapter_count=candidate.chapter_count,
        release_row_count=candidate.release_row_count,
        audit_check_count=len(checks),
        ready_check_count=ready_check_count,
        blocked_check_count=blocked_check_count,
        packaging_audit_ready=packaging_audit_ready,
        checks=checks,
        metadata={
            "expected_chapters": EXPECTED_CHAPTERS,
            "expected_release_rows": EXPECTED_RELEASE_ROWS,
            "expected_lanes": EXPECTED_LANES,
            "packaging_audit_checks": PACKAGING_AUDIT_CHECKS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "source_candidate_version": SOURCE_CANDIDATE_VERSION,
            "single_root": "topology_book_ecosystem_v1_0_342",
            "compression_method": "ZIP_DEFLATED / method 8",
            "archive_policy": "docs/archive bundles remain evidence-only and are not active source surfaces",
            "packaging_policy": "single full package; active resources remain open folders",
        },
    )


def render_release_candidate_packaging_audit(packet: ReleaseCandidatePackagingAudit) -> str:
    lines = [
        "# Chapter 07--15 Release Candidate Packaging Audit (v1.0.342)",
        "",
        "This document records the packaging-audit state after the v1.0.341 release-candidate verification.",
        "",
        "## Summary",
        f"- Previous version: `{packet.previous_version}`",
        f"- Source candidate version: `{packet.source_candidate_version}`",
        f"- Chapters covered: `{packet.chapter_count}`",
        f"- Release rows: `{packet.release_row_count}`",
        f"- Packaging audit checks: `{packet.audit_check_count}`",
        f"- Ready checks: `{packet.ready_check_count}`",
        f"- Blocked checks: `{packet.blocked_check_count}`",
        f"- Packaging audit ready: `{packet.packaging_audit_ready}`",
        "",
        "## Packaging audit checks",
    ]
    for check in packet.checks:
        status = "ready" if check.ready else "blocked"
        lines.append(f"- `{check.key}` / `{status}`: {check.title}. {check.evidence}")
    lines.extend([
        "",
        "## Policy",
        "The packaging audit preserves the single full-package model. Active source targets remain open folders; uploaded Chapter 07--15 zip files and docs/archive bundles are not active sources.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "PACKAGING_AUDIT_CHECKS",
    "PACKAGING_AUDIT_LABEL",
    "PACKAGING_AUDIT_VERSION",
    "EXPECTED_CHAPTERS",
    "EXPECTED_LANES",
    "EXPECTED_RELEASE_ROWS",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "SOURCE_CANDIDATE_VERSION",
    "PackagingAuditCheck",
    "ReleaseCandidatePackagingAudit",
    "build_release_candidate_packaging_audit",
    "render_release_candidate_packaging_audit",
]
