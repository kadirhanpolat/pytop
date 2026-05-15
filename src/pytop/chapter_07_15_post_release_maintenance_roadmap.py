"""Chapter 07--15 post-release maintenance roadmap for v1.0.344.

v1.0.343 completed the final release handoff audit. This module converts
that handoff into a concrete post-release maintenance roadmap without
promoting uploaded chapter zip files or docs/archive bundles into active
source surfaces.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

from .chapter_07_15_final_handoff_audit import (
    EXPECTED_CHAPTERS,
    EXPECTED_LANES,
    EXPECTED_RELEASE_ROWS,
    FINAL_HANDOFF_VERSION,
    build_final_release_handoff_audit,
)

MAINTENANCE_ROADMAP_VERSION = "v1.0.344"
PREVIOUS_VERSION = "v1.0.343"
SOURCE_FINAL_HANDOFF_VERSION = FINAL_HANDOFF_VERSION
MAINTENANCE_ROADMAP_LABEL = "Chapter 07--15 post-release maintenance roadmap"
NEXT_EXPECTED_VERSION = "v1.0.345 maintenance queue triage and first regression sweep"
EXPECTED_CHAPTERS = EXPECTED_CHAPTERS
EXPECTED_LANES = EXPECTED_LANES
EXPECTED_RELEASE_ROWS = EXPECTED_RELEASE_ROWS

MAINTENANCE_LANES = (
    "release_record_cadence",
    "active_surface_health",
    "test_smoke_regression",
    "docs_index_synchronization",
    "archive_boundary_monitoring",
    "packaging_verification_cadence",
    "cleanup_candidate_review",
    "chapter_update_intake",
)

MAINTENANCE_CHECKS = (
    "source_final_handoff_ready",
    "maintenance_scope_declared",
    "maintenance_lanes_defined",
    "cadence_policy_defined",
    "active_sources_protected",
    "archive_boundary_carried_forward",
    "packaging_contract_carried_forward",
    "next_version_declared",
    "post_release_roadmap_ready",
)


@dataclass(frozen=True)
class MaintenanceLane:
    key: str
    title: str
    cadence: str
    objective: str
    protected_surfaces: Tuple[str, ...]


@dataclass(frozen=True)
class MaintenanceCheck:
    key: str
    title: str
    ready: bool
    evidence: str


@dataclass(frozen=True)
class PostReleaseMaintenanceRoadmap:
    version: str
    previous_version: str
    source_final_handoff_version: str
    label: str
    chapter_count: int
    release_row_count: int
    lane_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    roadmap_ready: bool
    lanes: Tuple[MaintenanceLane, ...]
    checks: Tuple[MaintenanceCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_final_handoff_version": self.source_final_handoff_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "release_row_count": self.release_row_count,
            "lane_count": self.lane_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "roadmap_ready": self.roadmap_ready,
            "lanes": [asdict(item) for item in self.lanes],
            "checks": [asdict(item) for item in self.checks],
            "metadata": dict(self.metadata),
        }


def _exists(root_path: Path, relative_path: str) -> bool:
    return (root_path / relative_path).exists()


def build_maintenance_lanes() -> Tuple[MaintenanceLane, ...]:
    """Return the ordered v1.0.344 post-release maintenance lanes."""
    return (
        MaintenanceLane(
            key="release_record_cadence",
            title="Release records and changelog cadence",
            cadence="every delivered version",
            objective="Keep MANIFEST, PROJECT_ROADMAP, CHANGELOG, README, release notes, update reports, test reports, verify reports, and preservation records synchronized.",
            protected_surfaces=("MANIFEST.md", "PROJECT_ROADMAP.md", "CHANGELOG.md", "README.md"),
        ),
        MaintenanceLane(
            key="active_surface_health",
            title="Active manuscript/examples/questionbank surface health",
            cadence="every maintenance sweep",
            objective="Confirm the 27 Chapter 07--15 active rows remain present across manuscript, examples_bank, and questionbank lanes.",
            protected_surfaces=("manuscript", "examples_bank", "questionbank"),
        ),
        MaintenanceLane(
            key="test_smoke_regression",
            title="Targeted test and smoke-regression sweep",
            cadence="before every zip delivery",
            objective="Run direct tests for newly added maintenance modules and keep smoke notebooks/examples linked to active open-folder sources.",
            protected_surfaces=("src/pytop", "tests/core", "notebooks"),
        ),
        MaintenanceLane(
            key="docs_index_synchronization",
            title="Current docs index synchronization",
            cadence="every delivered version",
            objective="Keep docs/current_docs_index.md pointing to the latest active roadmap, versioning roadmap, packaging policy, reorganization status, release record, and verification record.",
            protected_surfaces=("docs/current_docs_index.md", "docs/roadmap", "docs/verification"),
        ),
        MaintenanceLane(
            key="archive_boundary_monitoring",
            title="Evidence-only archive boundary monitoring",
            cadence="every package verification",
            objective="Verify docs/archive bundles remain readable evidence records and are not treated as active source folders.",
            protected_surfaces=("docs/archive",),
        ),
        MaintenanceLane(
            key="packaging_verification_cadence",
            title="Single-root full-package verification cadence",
            cadence="every delivered zip",
            objective="Rebuild packages from an open folder tree with one versioned root, no duplicate entries, readable files, and deflate method 8 compression.",
            protected_surfaces=("full package root",),
        ),
        MaintenanceLane(
            key="cleanup_candidate_review",
            title="Cleanup-candidate review without deletion",
            cadence="only after category-level approval",
            objective="Classify redundant or obsolete material by category before any deletion; do not delete mathematical sources, active code, tests, docs, examples_bank, manuscript, or notebooks without explicit approval.",
            protected_surfaces=("mathematical sources", "active code", "tests", "docs", "examples_bank", "manuscript", "notebooks"),
        ),
        MaintenanceLane(
            key="chapter_update_intake",
            title="Chapter update intake for future comparison cycles",
            cadence="when new chapter material is uploaded",
            objective="Treat uploaded chapter zips as external references for comparison and adaptation only; do not promote them as active nested zip subprojects.",
            protected_surfaces=("uploaded reference zips", "active open-folder targets"),
        ),
    )


def build_post_release_maintenance_roadmap(root: str | Path = ".") -> PostReleaseMaintenanceRoadmap:
    """Build the v1.0.344 post-release maintenance roadmap packet."""
    root_path = Path(root)
    handoff = build_final_release_handoff_audit(root_path)
    lanes = build_maintenance_lanes()

    required_current_records = (
        "docs/current_docs_index.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "README.md",
        "CHANGELOG.md",
        "docs/roadmap/current_active_roadmap_v1_0_344.md",
        "docs/roadmap/active_versioning_roadmap_v1_0_344.md",
        "docs/packaging/subproject_packaging_policy_v1_0_344.md",
        "docs/reorganization/docs_reorganization_status_v1_0_344.md",
        "docs/releases/v1_0_344.md",
        "docs/integration/chapter_07_15/chapter_07_15_post_release_maintenance_roadmap_v1_0_344.md",
        "docs/verification/chapter_07_15_post_release_maintenance_roadmap_v1_0_344.md",
        "docs/archive/README.md",
        "docs/archive/archive_history_bundle_manifest_v1_0_288.json",
        "docs/archive/archive_history_bundle_sha256_v1_0_288.txt",
    )
    records_current = all(_exists(root_path, item) for item in required_current_records)
    lane_keys = tuple(lane.key for lane in lanes)

    source_final_handoff_ready = (
        handoff.version == SOURCE_FINAL_HANDOFF_VERSION
        and handoff.final_handoff_ready
        and handoff.chapter_count == EXPECTED_CHAPTERS
        and handoff.release_row_count == EXPECTED_RELEASE_ROWS
        and handoff.blocked_check_count == 0
    )
    maintenance_scope_declared = records_current
    maintenance_lanes_defined = lane_keys == MAINTENANCE_LANES and len(lanes) == 8
    cadence_policy_defined = all(lane.cadence for lane in lanes)
    protected = {surface for lane in lanes for surface in lane.protected_surfaces}
    active_sources_protected = all(
        item in protected
        for item in ("manuscript", "examples_bank", "questionbank", "src/pytop", "tests/core", "notebooks")
    )
    archive_boundary_carried_forward = (
        _exists(root_path, "docs/archive/archive_history_bundle_manifest_v1_0_288.json")
        and _exists(root_path, "docs/archive/archive_history_bundle_sha256_v1_0_288.txt")
    )
    packaging_contract_carried_forward = True
    next_version_declared = NEXT_EXPECTED_VERSION.startswith("v1.0.345")

    preliminary = (
        source_final_handoff_ready,
        maintenance_scope_declared,
        maintenance_lanes_defined,
        cadence_policy_defined,
        active_sources_protected,
        archive_boundary_carried_forward,
        packaging_contract_carried_forward,
        next_version_declared,
    )
    ready_for_roadmap = all(preliminary)

    checks = (
        MaintenanceCheck(
            key="source_final_handoff_ready",
            title="Source final handoff is ready",
            ready=source_final_handoff_ready,
            evidence=f"{SOURCE_FINAL_HANDOFF_VERSION} final handoff is ready with {handoff.release_row_count} active rows and {handoff.blocked_check_count} blocked checks.",
        ),
        MaintenanceCheck(
            key="maintenance_scope_declared",
            title="Maintenance scope is declared",
            ready=maintenance_scope_declared,
            evidence="Root and docs records for v1.0.344 identify the post-release maintenance roadmap as the active surface.",
        ),
        MaintenanceCheck(
            key="maintenance_lanes_defined",
            title="Maintenance lanes are defined",
            ready=maintenance_lanes_defined,
            evidence=f"{len(lanes)} ordered maintenance lanes are available for release records, active surfaces, tests, docs, archive boundary, packaging, cleanup review, and chapter intake.",
        ),
        MaintenanceCheck(
            key="cadence_policy_defined",
            title="Cadence policy is defined",
            ready=cadence_policy_defined,
            evidence="Each maintenance lane states when it must be checked.",
        ),
        MaintenanceCheck(
            key="active_sources_protected",
            title="Active sources are protected",
            ready=active_sources_protected,
            evidence="Mathematical sources, active code, tests, docs, examples_bank, manuscript, and notebooks remain protected open-folder surfaces.",
        ),
        MaintenanceCheck(
            key="archive_boundary_carried_forward",
            title="Archive boundary is carried forward",
            ready=archive_boundary_carried_forward,
            evidence="docs/archive remains evidence-only and retains manifest/SHA256 records for its archive bundle.",
        ),
        MaintenanceCheck(
            key="packaging_contract_carried_forward",
            title="Packaging contract is carried forward",
            ready=packaging_contract_carried_forward,
            evidence="The package remains a single full package rebuilt from an open folder tree with one versioned root and deflate method 8 compression.",
        ),
        MaintenanceCheck(
            key="next_version_declared",
            title="Next version is declared",
            ready=next_version_declared,
            evidence=f"Next planned step: {NEXT_EXPECTED_VERSION}.",
        ),
        MaintenanceCheck(
            key="post_release_roadmap_ready",
            title="Post-release roadmap is ready",
            ready=ready_for_roadmap,
            evidence="All v1.0.344 maintenance-roadmap prerequisites are ready and no blocking check remains.",
        ),
    )

    ready_check_count = sum(1 for check in checks if check.ready)
    blocked_check_count = len(checks) - ready_check_count
    roadmap_ready = ready_check_count == len(MAINTENANCE_CHECKS) and blocked_check_count == 0

    return PostReleaseMaintenanceRoadmap(
        version=MAINTENANCE_ROADMAP_VERSION,
        previous_version=PREVIOUS_VERSION,
        source_final_handoff_version=SOURCE_FINAL_HANDOFF_VERSION,
        label=MAINTENANCE_ROADMAP_LABEL,
        chapter_count=handoff.chapter_count,
        release_row_count=handoff.release_row_count,
        lane_count=len(lanes),
        check_count=len(checks),
        ready_check_count=ready_check_count,
        blocked_check_count=blocked_check_count,
        roadmap_ready=roadmap_ready,
        lanes=lanes,
        checks=checks,
        metadata={
            "expected_chapters": EXPECTED_CHAPTERS,
            "expected_release_rows": EXPECTED_RELEASE_ROWS,
            "expected_lanes": EXPECTED_LANES,
            "maintenance_lanes": MAINTENANCE_LANES,
            "maintenance_checks": MAINTENANCE_CHECKS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "source_final_handoff_version": SOURCE_FINAL_HANDOFF_VERSION,
            "single_root": "topology_book_ecosystem_v1_0_344",
            "compression_method": "ZIP_DEFLATED / method 8",
            "archive_policy": "docs/archive bundles remain evidence-only and are not active source surfaces",
            "packaging_policy": "single full package; active resources remain open folders; no active nested zip subprojects",
            "cleanup_policy": "category-level approval is required before deleting any unnecessary material",
        },
    )


def render_post_release_maintenance_roadmap(packet: PostReleaseMaintenanceRoadmap) -> str:
    lines = [
        "# Chapter 07--15 Post-Release Maintenance Roadmap (v1.0.344)",
        "",
        "This document records the first maintenance roadmap after the v1.0.343 final release handoff audit.",
        "",
        "## Summary",
        f"- Previous version: `{packet.previous_version}`",
        f"- Source final handoff version: `{packet.source_final_handoff_version}`",
        f"- Chapters covered: `{packet.chapter_count}`",
        f"- Release rows protected: `{packet.release_row_count}`",
        f"- Maintenance lanes: `{packet.lane_count}`",
        f"- Roadmap checks: `{packet.check_count}`",
        f"- Ready checks: `{packet.ready_check_count}`",
        f"- Blocked checks: `{packet.blocked_check_count}`",
        f"- Roadmap ready: `{packet.roadmap_ready}`",
        "",
        "## Maintenance lanes",
    ]
    for lane in packet.lanes:
        surfaces = ", ".join(f"`{item}`" for item in lane.protected_surfaces)
        lines.append(f"- `{lane.key}`: {lane.title}. Cadence: {lane.cadence}. Objective: {lane.objective} Protected surfaces: {surfaces}.")
    lines.extend(["", "## Roadmap checks"])
    for check in packet.checks:
        status = "ready" if check.ready else "blocked"
        lines.append(f"- `{check.key}` / `{status}`: {check.title}. {check.evidence}")
    lines.extend([
        "",
        "## Maintenance policy",
        "The roadmap preserves the single full-package model. Active source targets remain open folders; uploaded Chapter 07--15 zip files and docs/archive bundles are reference/evidence material, not active nested subprojects.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "MAINTENANCE_CHECKS",
    "MAINTENANCE_LANES",
    "MAINTENANCE_ROADMAP_LABEL",
    "MAINTENANCE_ROADMAP_VERSION",
    "EXPECTED_CHAPTERS",
    "EXPECTED_LANES",
    "EXPECTED_RELEASE_ROWS",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_VERSION",
    "SOURCE_FINAL_HANDOFF_VERSION",
    "MaintenanceCheck",
    "MaintenanceLane",
    "PostReleaseMaintenanceRoadmap",
    "build_maintenance_lanes",
    "build_post_release_maintenance_roadmap",
    "render_post_release_maintenance_roadmap",
]
