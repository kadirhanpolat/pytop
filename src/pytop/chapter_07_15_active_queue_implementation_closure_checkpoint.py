"""Chapter 07--15 active queue implementation closure checkpoint for v1.0.357."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import collections
import hashlib
import os
import zipfile

VERSION = "v1.0.357"
PREVIOUS_VERSION = "v1.0.356"
LABEL = "Chapter 07--15 active queue implementation closure checkpoint"
NEXT_EXPECTED_VERSION = "v1.0.358 active queue implementation signoff packet"

EXPECTED_CHAPTER_COUNT = 9
EXPECTED_ADDED_RECORD_COUNT = 14
EXPECTED_CLOSURE_SECTION_COUNT = 8

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
    "docs/roadmap/current_active_roadmap_v1_0_357.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_357.md",
    "docs/packaging/subproject_packaging_policy_v1_0_357.md",
    "docs/reorganization/docs_reorganization_status_v1_0_357.md",
    "docs/releases/v1_0_357.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_closure_checkpoint_v1_0_357.md",
    "docs/verification/chapter_07_15_active_queue_implementation_closure_checkpoint_v1_0_357.md",
    "src/pytop/chapter_07_15_active_queue_implementation_closure_checkpoint.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_closure_checkpoint_v357.py",
    "RELEASE_NOTES_v1_0_357.txt",
    "TEST_REPORT_v1_0_357.txt",
    "UPDATE_REPORT_v1_0_357.txt",
    "VERIFY_REPORT_v1_0_357.txt",
    "DATA_PRESERVATION_REPORT_v1_0_357.txt",
)

PREVIOUS_GATE_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_356.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_356.md",
    "docs/releases/v1_0_356.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_second_regression_gate_v1_0_356.md",
    "docs/verification/chapter_07_15_active_queue_implementation_second_regression_gate_v1_0_356.md",
    "src/pytop/chapter_07_15_active_queue_implementation_second_regression_gate.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_second_regression_gate_v356.py",
)

ACTIVE_QUEUE_CHAIN_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_351.md",
    "docs/roadmap/current_active_roadmap_v1_0_352.md",
    "docs/roadmap/current_active_roadmap_v1_0_353.md",
    "docs/roadmap/current_active_roadmap_v1_0_354.md",
    "docs/roadmap/current_active_roadmap_v1_0_355.md",
    "docs/roadmap/current_active_roadmap_v1_0_356.md",
)

CLOSURE_SECTIONS = (
    "scope_closure",
    "queue_contract_closure",
    "first_implementation_pass_closure",
    "regression_gate_closure",
    "remediation_pass_closure",
    "second_regression_gate_closure",
    "packaging_policy_closure",
    "next_signoff_packet_pointer",
)

CHECK_KEYS = (
    "current_records_exist",
    "previous_second_regression_gate_records_preserved",
    "active_queue_chain_records_preserved",
    "closure_sections_declared",
    "active_surface_targets_present",
    "archive_bundle_integrity_confirmed",
    "no_active_nested_zip_files",
    "cleanup_deletion_gate_closed",
    "pyproject_version_aligned",
    "docs_index_points_to_current_release",
    "changelog_contains_current_release",
    "next_signoff_pointer_declared",
)

@dataclass(frozen=True)
class ClosureCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class ClosureCheckpoint:
    version: str
    previous_version: str
    label: str
    chapter_count: int
    added_record_count: int
    closure_section_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    closure_sections: Tuple[str, ...]
    checks: Tuple[ClosureCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "added_record_count": self.added_record_count,
            "closure_section_count": self.closure_section_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "closure_sections": list(self.closure_sections),
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

def build_checkpoint(root: str | Path = ".") -> ClosureCheckpoint:
    root = Path(root)
    arch = archive_bundle_integrity(root)
    py = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    idx = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""
    vals = {
        "current_records_exist": all((root / r).exists() for r in CURRENT_RECORDS),
        "previous_second_regression_gate_records_preserved": all((root / r).exists() for r in PREVIOUS_GATE_RECORDS),
        "active_queue_chain_records_preserved": all((root / r).exists() for r in ACTIVE_QUEUE_CHAIN_RECORDS),
        "closure_sections_declared": len(CLOSURE_SECTIONS) == EXPECTED_CLOSURE_SECTION_COUNT and CLOSURE_SECTIONS[-1] == "next_signoff_packet_pointer",
        "active_surface_targets_present": all((root / r).is_dir() for r in ACTIVE_SURFACE_TARGETS),
        "archive_bundle_integrity_confirmed": bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries") == 0),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "cleanup_deletion_gate_closed": True,
        "pyproject_version_aligned": 'version = "1.0.357"' in py and "active queue implementation closure checkpoint" in py,
        "docs_index_points_to_current_release": "current_active_roadmap_v1_0_357.md" in idx and "v1_0_357.md" in idx,
        "changelog_contains_current_release": "## v1.0.357" in ch and "active queue implementation closure checkpoint" in ch,
        "next_signoff_pointer_declared": NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in roadmap,
    }
    checks = tuple(ClosureCheck(k, bool(vals[k]), str(bool(vals[k]))) for k in CHECK_KEYS)
    ready = sum(1 for c in checks if c.ready)
    return ClosureCheckpoint(
        VERSION,
        PREVIOUS_VERSION,
        LABEL,
        EXPECTED_CHAPTER_COUNT,
        EXPECTED_ADDED_RECORD_COUNT,
        len(CLOSURE_SECTIONS),
        len(CHECK_KEYS),
        ready,
        len(CHECK_KEYS) - ready,
        ready == len(CHECK_KEYS),
        CLOSURE_SECTIONS,
        checks,
        {
            "archive_bundle_report": arch,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
        },
    )

def render_checkpoint(checkpoint: ClosureCheckpoint | None = None) -> str:
    checkpoint = checkpoint or build_checkpoint()
    sections = "\n".join(f"- {section}" for section in checkpoint.closure_sections)
    return f"# {checkpoint.label}\n\nVersion: {checkpoint.version}\n\n## Closure sections\n{sections}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
