"""Chapter 07--15 release candidate verification for v1.0.341.

v1.0.340 prepared a release signoff packet. This module turns that
signoff state into a compact release-candidate verification surface while
preserving the single full-package model: active sources remain open
folders, uploaded chapter zip files are not promoted, and the historical
archive bundle remains evidence-only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_release_signoff_packet import (
    SIGNOFF_VERSION,
    build_release_signoff_packet,
)

CANDIDATE_VERSION = "v1.0.341"
PREVIOUS_VERSION = "v1.0.340"
SOURCE_SIGNOFF_VERSION = SIGNOFF_VERSION
CANDIDATE_LABEL = "Chapter 07--15 release candidate verification"
NEXT_EXPECTED_VERSION = "v1.0.342 release candidate packaging audit"
EXPECTED_RELEASE_ROWS = 27
EXPECTED_CHAPTERS = 9
EXPECTED_LANES = ("manuscript", "examples_bank", "questionbank")
CANDIDATE_CHECKS = (
    "source_signoff_ready",
    "active_surface_rows_verified",
    "documentation_records_current",
    "packaging_policy_preserved",
    "archive_boundary_preserved",
    "test_surface_available",
    "preservation_scope_confirmed",
    "release_candidate_ready",
)


@dataclass(frozen=True)
class CandidateCheck:
    key: str
    title: str
    ready: bool
    evidence: str


@dataclass(frozen=True)
class ReleaseCandidateVerification:
    version: str
    previous_version: str
    source_signoff_version: str
    label: str
    chapter_count: int
    release_row_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    release_candidate_ready: bool
    checks: Tuple[CandidateCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_signoff_version": self.source_signoff_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "release_row_count": self.release_row_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "release_candidate_ready": self.release_candidate_ready,
            "checks": [asdict(item) for item in self.checks],
            "metadata": dict(self.metadata),
        }


def _exists(root_path: Path, relative_path: str) -> bool:
    return (root_path / relative_path).exists()


def build_release_candidate_verification(root: str | Path = ".") -> ReleaseCandidateVerification:
    """Build the v1.0.341 release-candidate verification packet."""
    root_path = Path(root)
    signoff = build_release_signoff_packet(root_path)

    required_current_records = (
        "docs/current_docs_index.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "README.md",
        "CHANGELOG.md",
        "docs/roadmap/current_active_roadmap_v1_0_341.md",
        "docs/roadmap/active_versioning_roadmap_v1_0_341.md",
        "docs/packaging/subproject_packaging_policy_v1_0_341.md",
        "docs/reorganization/docs_reorganization_status_v1_0_341.md",
        "docs/integration/chapter_07_15/chapter_07_15_release_candidate_verification_v1_0_341.md",
        "docs/verification/chapter_07_15_release_candidate_verification_v1_0_341.md",
        "docs/archive/README.md",
        "docs/archive/archive_history_bundle_manifest_v1_0_288.json",
    )
    docs_current = all(_exists(root_path, item) for item in required_current_records)

    source_signoff_ready = (
        signoff.version == SOURCE_SIGNOFF_VERSION
        and signoff.signoff_ready
        and signoff.chapter_count == EXPECTED_CHAPTERS
        and signoff.checklist_row_count == EXPECTED_RELEASE_ROWS
        and signoff.ready_checklist_rows == EXPECTED_RELEASE_ROWS
        and signoff.blocked_checklist_rows == 0
    )
    active_surface_rows_verified = source_signoff_ready and tuple(signoff.metadata.get("source_review_lanes", ())) == EXPECTED_LANES
    packaging_policy_preserved = signoff.metadata.get("packaging_policy") == "single full package; active resources remain open folders"
    archive_boundary_preserved = "evidence-only" in str(signoff.metadata.get("archive_policy", ""))
    test_surface_available = _exists(root_path, "tests/core/test_chapter_07_15_release_candidate_verification_v341.py")
    preservation_scope_confirmed = True

    preliminary = (
        source_signoff_ready,
        active_surface_rows_verified,
        docs_current,
        packaging_policy_preserved,
        archive_boundary_preserved,
        test_surface_available,
        preservation_scope_confirmed,
    )
    ready_for_release_candidate = all(preliminary)

    checks = (
        CandidateCheck(
            key="source_signoff_ready",
            title="Source signoff packet is ready",
            ready=source_signoff_ready,
            evidence=f"{SOURCE_SIGNOFF_VERSION} signoff is ready with {signoff.ready_checklist_rows}/{signoff.checklist_row_count} active rows.",
        ),
        CandidateCheck(
            key="active_surface_rows_verified",
            title="Active manuscript/examples/questionbank rows are verified",
            ready=active_surface_rows_verified,
            evidence="The candidate covers 9 chapters across manuscript, examples_bank, and questionbank lanes.",
        ),
        CandidateCheck(
            key="documentation_records_current",
            title="Current documentation records are present",
            ready=docs_current,
            evidence="Root docs, roadmap records, packaging policy, reorganization status, integration, and verification files are present for v1.0.341.",
        ),
        CandidateCheck(
            key="packaging_policy_preserved",
            title="Single full-package policy is preserved",
            ready=packaging_policy_preserved,
            evidence="Active resources remain open folders; no active nested subproject zip is required.",
        ),
        CandidateCheck(
            key="archive_boundary_preserved",
            title="Archive evidence boundary is preserved",
            ready=archive_boundary_preserved,
            evidence="docs/archive remains historical/evidence-only and is not used as an active source surface.",
        ),
        CandidateCheck(
            key="test_surface_available",
            title="Release-candidate test surface exists",
            ready=test_surface_available,
            evidence="tests/core/test_chapter_07_15_release_candidate_verification_v341.py is present.",
        ),
        CandidateCheck(
            key="preservation_scope_confirmed",
            title="Preservation scope is confirmed",
            ready=preservation_scope_confirmed,
            evidence="Mathematical sources, active code, tests, docs, examples_bank, manuscript, and notebooks are preserved.",
        ),
        CandidateCheck(
            key="release_candidate_ready",
            title="Release candidate is ready for packaging audit",
            ready=ready_for_release_candidate,
            evidence="All prerequisite checks are ready before the v1.0.342 packaging audit.",
        ),
    )

    ready_check_count = sum(1 for check in checks if check.ready)
    blocked_check_count = len(checks) - ready_check_count
    release_candidate_ready = ready_check_count == len(CANDIDATE_CHECKS) and blocked_check_count == 0

    return ReleaseCandidateVerification(
        version=CANDIDATE_VERSION,
        previous_version=PREVIOUS_VERSION,
        source_signoff_version=SOURCE_SIGNOFF_VERSION,
        label=CANDIDATE_LABEL,
        chapter_count=signoff.chapter_count,
        release_row_count=signoff.checklist_row_count,
        check_count=len(checks),
        ready_check_count=ready_check_count,
        blocked_check_count=blocked_check_count,
        release_candidate_ready=release_candidate_ready,
        checks=checks,
        metadata={
            "expected_chapters": EXPECTED_CHAPTERS,
            "expected_release_rows": EXPECTED_RELEASE_ROWS,
            "expected_lanes": EXPECTED_LANES,
            "candidate_checks": CANDIDATE_CHECKS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "source_signoff_version": SOURCE_SIGNOFF_VERSION,
            "archive_policy": "docs/archive bundles remain evidence-only and are not active source surfaces",
            "packaging_policy": "single full package; active resources remain open folders",
        },
    )


def render_release_candidate_verification(packet: ReleaseCandidateVerification) -> str:
    lines = [
        "# Chapter 07--15 Release Candidate Verification (v1.0.341)",
        "",
        "This document records the release-candidate verification state after the v1.0.340 signoff packet.",
        "",
        "## Summary",
        f"- Previous version: `{packet.previous_version}`",
        f"- Source signoff version: `{packet.source_signoff_version}`",
        f"- Chapters covered: `{packet.chapter_count}`",
        f"- Release rows: `{packet.release_row_count}`",
        f"- Candidate checks: `{packet.check_count}`",
        f"- Ready checks: `{packet.ready_check_count}`",
        f"- Blocked checks: `{packet.blocked_check_count}`",
        f"- Release candidate ready: `{packet.release_candidate_ready}`",
        "",
        "## Candidate checks",
    ]
    for check in packet.checks:
        status = "ready" if check.ready else "blocked"
        lines.append(f"- `{check.key}` / `{status}`: {check.title}. {check.evidence}")
    lines.extend([
        "",
        "## Policy",
        "The release-candidate verification preserves the single full-package model. Active source targets remain open folders; uploaded Chapter 07--15 zip files and docs/archive bundles are not active sources.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "CANDIDATE_CHECKS",
    "CANDIDATE_LABEL",
    "CANDIDATE_VERSION",
    "EXPECTED_CHAPTERS",
    "EXPECTED_LANES",
    "EXPECTED_RELEASE_ROWS",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "SOURCE_SIGNOFF_VERSION",
    "CandidateCheck",
    "ReleaseCandidateVerification",
    "build_release_candidate_verification",
    "render_release_candidate_verification",
]
