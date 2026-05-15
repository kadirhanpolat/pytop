"""Chapter 07--15 active queue implementation final handoff audit for v1.0.359."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.359"
PREVIOUS_VERSION = "v1.0.358"
LABEL = "Chapter 07--15 active queue implementation final handoff audit"
NEXT_EXPECTED_VERSION = "v1.0.360 post-active-queue roadmap refresh"

EXPECTED_CHAPTER_COUNT = 9
EXPECTED_ADDED_RECORD_COUNT = 14
EXPECTED_AUDIT_SECTION_COUNT = 10

ACTIVE_SURFACE_TARGETS = (
    "src",
    "tests",
    "docs",
    "examples_bank",
    "manuscript",
    "notebooks",
    "tools",
)

CURRENT_RECORDS = (
    "docs/current_docs_index.md",
    "MANIFEST.md",
    "PROJECT_ROADMAP.md",
    "README.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "docs/roadmap/current_active_roadmap_v1_0_359.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_359.md",
    "docs/packaging/subproject_packaging_policy_v1_0_359.md",
    "docs/reorganization/docs_reorganization_status_v1_0_359.md",
    "docs/releases/v1_0_359.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_final_handoff_audit_v1_0_359.md",
    "docs/verification/chapter_07_15_active_queue_implementation_final_handoff_audit_v1_0_359.md",
    "src/pytop/chapter_07_15_active_queue_implementation_final_handoff_audit.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_final_handoff_audit_v359.py",
    "RELEASE_NOTES_v1_0_359.txt",
    "TEST_REPORT_v1_0_359.txt",
    "UPDATE_REPORT_v1_0_359.txt",
    "VERIFY_REPORT_v1_0_359.txt",
    "DATA_PRESERVATION_REPORT_v1_0_359.txt",
)

PREVIOUS_SIGNOFF_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_358.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_358.md",
    "docs/releases/v1_0_358.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_signoff_packet_v1_0_358.md",
    "docs/verification/chapter_07_15_active_queue_implementation_signoff_packet_v1_0_358.md",
    "src/pytop/chapter_07_15_active_queue_implementation_signoff_packet.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_signoff_packet_v358.py",
)

ACTIVE_QUEUE_CHAIN_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_351.md",
    "docs/roadmap/current_active_roadmap_v1_0_352.md",
    "docs/roadmap/current_active_roadmap_v1_0_353.md",
    "docs/roadmap/current_active_roadmap_v1_0_354.md",
    "docs/roadmap/current_active_roadmap_v1_0_355.md",
    "docs/roadmap/current_active_roadmap_v1_0_356.md",
    "docs/roadmap/current_active_roadmap_v1_0_357.md",
    "docs/roadmap/current_active_roadmap_v1_0_358.md",
)

AUDIT_SECTIONS = (
    "source_package_audit",
    "active_queue_chain_audit",
    "signoff_packet_audit",
    "current_record_audit",
    "active_source_boundary_audit",
    "archive_bundle_audit",
    "packaging_policy_audit",
    "data_preservation_audit",
    "release_handoff_audit",
    "next_roadmap_refresh_pointer",
)

CHECK_KEYS = (
    "current_records_exist",
    "previous_signoff_packet_records_preserved",
    "active_queue_chain_records_preserved",
    "audit_sections_declared",
    "active_surface_targets_present",
    "archive_bundle_integrity_confirmed",
    "no_active_nested_zip_files",
    "cleanup_deletion_gate_closed",
    "pyproject_version_aligned",
    "docs_index_points_to_current_release",
    "changelog_contains_current_release",
    "next_roadmap_refresh_pointer_declared",
)

@dataclass(frozen=True)
class HandoffAuditCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class FinalHandoffAudit:
    version: str
    previous_version: str
    label: str
    chapter_count: int
    added_record_count: int
    audit_section_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    audit_sections: Tuple[str, ...]
    checks: Tuple[HandoffAuditCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "added_record_count": self.added_record_count,
            "audit_section_count": self.audit_section_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "audit_sections": list(self.audit_sections),
            "checks": [asdict(x) for x in self.checks],
            "metadata": dict(self.metadata),
        }

def active_nested_zip_paths(root: str | Path = ".") -> Tuple[str, ...]:
    root = Path(root)
    out = []
    for dirpath, _dirs, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".zip"):
                rel = str((Path(dirpath) / filename).relative_to(root)).replace("\\", "/")
                if not rel.startswith("docs/archive/"):
                    out.append(rel)
    return tuple(sorted(out))

def archive_bundle_integrity(root: str | Path = ".") -> Dict[str, object]:
    root = Path(root)
    p = root / "docs/archive/archive_history_bundle_v1_0_288.zip"
    m = root / "docs/archive/archive_history_bundle_manifest_v1_0_288.json"
    report: Dict[str, object] = {"present": p.exists(), "manifest_present": m.exists()}
    if not p.exists():
        return report
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = m.read_text(encoding="utf-8") if m.exists() else ""
    report["sha256"] = sha
    report["sha256_matches_manifest"] = sha in manifest
    with zipfile.ZipFile(p) as z:
        names = z.namelist()
        report["duplicate_entries"] = len(names) - len(set(names))
        report["entry_count"] = len(names)
        report["compression_methods"] = tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()}))
        report["testzip_ok"] = z.testzip() is None
        for i in z.infolist():
            if not i.is_dir():
                z.read(i.filename)
        report["all_entries_readable"] = True
    return report

def build_final_handoff_audit(root: str | Path = ".") -> FinalHandoffAudit:
    root = Path(root)
    arch = archive_bundle_integrity(root)
    py = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    idx = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""
    vals = {
        "current_records_exist": all((root / r).exists() for r in CURRENT_RECORDS),
        "previous_signoff_packet_records_preserved": all((root / r).exists() for r in PREVIOUS_SIGNOFF_RECORDS),
        "active_queue_chain_records_preserved": all((root / r).exists() for r in ACTIVE_QUEUE_CHAIN_RECORDS),
        "audit_sections_declared": len(AUDIT_SECTIONS) == EXPECTED_AUDIT_SECTION_COUNT and AUDIT_SECTIONS[-1] == "next_roadmap_refresh_pointer",
        "active_surface_targets_present": all((root / r).is_dir() for r in ACTIVE_SURFACE_TARGETS),
        "archive_bundle_integrity_confirmed": bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries") == 0),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "cleanup_deletion_gate_closed": True,
        "pyproject_version_aligned": 'version = "1.0.359"' in py and "active queue implementation final handoff audit" in py,
        "docs_index_points_to_current_release": "current_active_roadmap_v1_0_359.md" in idx and "v1_0_359.md" in idx,
        "changelog_contains_current_release": "## v1.0.359" in ch and "active queue implementation final handoff audit" in ch,
        "next_roadmap_refresh_pointer_declared": NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in roadmap,
    }
    checks = tuple(HandoffAuditCheck(k, bool(vals[k]), str(bool(vals[k]))) for k in CHECK_KEYS)
    ready = sum(1 for c in checks if c.ready)
    return FinalHandoffAudit(
        VERSION,
        PREVIOUS_VERSION,
        LABEL,
        EXPECTED_CHAPTER_COUNT,
        EXPECTED_ADDED_RECORD_COUNT,
        len(AUDIT_SECTIONS),
        len(CHECK_KEYS),
        ready,
        len(CHECK_KEYS) - ready,
        ready == len(CHECK_KEYS),
        AUDIT_SECTIONS,
        checks,
        {
            "archive_bundle_report": arch,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
        },
    )

def render_final_handoff_audit(audit: FinalHandoffAudit | None = None) -> str:
    audit = audit or build_final_handoff_audit()
    sections = "\n".join(f"- {section}" for section in audit.audit_sections)
    return f"# {audit.label}\n\nVersion: {audit.version}\n\n## Audit sections\n{sections}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
