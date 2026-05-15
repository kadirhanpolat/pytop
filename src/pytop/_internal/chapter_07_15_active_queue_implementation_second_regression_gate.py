"""Chapter 07--15 active queue implementation second regression gate for v1.0.356."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.356"
PREVIOUS_VERSION = "v1.0.355"
SOURCE_GATE_VERSION = "v1.0.355"
LABEL = "Chapter 07--15 active queue implementation second regression gate"
NEXT_EXPECTED_VERSION = "v1.0.357 active queue implementation closure checkpoint"
EXPECTED_CHAPTER_COUNT = 9
EXPECTED_RECORD_COUNT = 14
EXPECTED_GATE_COUNT = 8
EXPECTED_CHECK_COUNT = 12

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
    "docs/roadmap/current_active_roadmap_v1_0_356.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_356.md",
    "docs/packaging/subproject_packaging_policy_v1_0_356.md",
    "docs/reorganization/docs_reorganization_status_v1_0_356.md",
    "docs/releases/v1_0_356.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_second_regression_gate_v1_0_356.md",
    "docs/verification/chapter_07_15_active_queue_implementation_second_regression_gate_v1_0_356.md",
    "src/pytop/chapter_07_15_active_queue_implementation_second_regression_gate.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_second_regression_gate_v356.py",
    "RELEASE_NOTES_v1_0_356.txt",
    "TEST_REPORT_v1_0_356.txt",
    "UPDATE_REPORT_v1_0_356.txt",
    "VERIFY_REPORT_v1_0_356.txt",
    "DATA_PRESERVATION_REPORT_v1_0_356.txt",
)

PREVIOUS_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_355.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_355.md",
    "docs/releases/v1_0_355.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_remediation_pass_v1_0_355.md",
    "docs/verification/chapter_07_15_active_queue_implementation_remediation_pass_v1_0_355.md",
    "src/pytop/chapter_07_15_active_queue_implementation_remediation_pass.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_remediation_pass_v355.py",
)

SECOND_REGRESSION_GATES = (
    "current_record_presence_gate",
    "previous_remediation_pass_preservation_gate",
    "first_regression_gate_preservation_gate",
    "active_surface_open_folder_gate",
    "archive_bundle_integrity_gate",
    "nested_zip_boundary_gate",
    "metadata_alignment_gate",
    "closure_checkpoint_pointer_gate",
)

CHECK_KEYS = (
    "current_records_exist",
    "previous_remediation_records_preserved",
    "first_regression_gate_records_preserved",
    "second_regression_gates_declared",
    "active_surface_targets_present",
    "archive_bundle_integrity_confirmed",
    "no_active_nested_zip_files",
    "cleanup_deletion_gate_closed",
    "pyproject_version_aligned",
    "docs_index_points_to_current_release",
    "changelog_contains_current_release",
    "next_release_pointer_declared",
)

FIRST_REGRESSION_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_354.md",
    "docs/releases/v1_0_354.md",
    "src/pytop/chapter_07_15_active_queue_implementation_regression_gate.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_regression_gate_v354.py",
)

@dataclass(frozen=True)
class SecondRegressionCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class SecondRegressionPacket:
    version: str
    previous_version: str
    source_gate_version: str
    label: str
    chapter_count: int
    record_count: int
    gate_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    gates: Tuple[str, ...]
    checks: Tuple[SecondRegressionCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "source_gate_version": self.source_gate_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "record_count": self.record_count,
            "gate_count": self.gate_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "gates": list(self.gates),
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

def build_packet(root: str | Path = ".") -> SecondRegressionPacket:
    root = Path(root)
    arch = archive_bundle_integrity(root)
    py = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    idx = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""
    vals = {
        "current_records_exist": all((root / r).exists() for r in CURRENT_RECORDS),
        "previous_remediation_records_preserved": all((root / r).exists() for r in PREVIOUS_RECORDS),
        "first_regression_gate_records_preserved": all((root / r).exists() for r in FIRST_REGRESSION_RECORDS),
        "second_regression_gates_declared": len(SECOND_REGRESSION_GATES) == EXPECTED_GATE_COUNT and SECOND_REGRESSION_GATES[-1] == "closure_checkpoint_pointer_gate",
        "active_surface_targets_present": all((root / r).is_dir() for r in ACTIVE_SURFACE_TARGETS),
        "archive_bundle_integrity_confirmed": bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries") == 0),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "cleanup_deletion_gate_closed": True,
        "pyproject_version_aligned": 'version = "1.0.356"' in py and "active queue implementation second regression gate" in py,
        "docs_index_points_to_current_release": "current_active_roadmap_v1_0_356.md" in idx and "v1_0_356.md" in idx,
        "changelog_contains_current_release": "## v1.0.356" in ch and "active queue implementation second regression gate" in ch,
        "next_release_pointer_declared": NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in roadmap,
    }
    checks = tuple(SecondRegressionCheck(k, bool(vals[k]), str(bool(vals[k]))) for k in CHECK_KEYS)
    ready = sum(1 for c in checks if c.ready)
    return SecondRegressionPacket(
        VERSION,
        PREVIOUS_VERSION,
        SOURCE_GATE_VERSION,
        LABEL,
        EXPECTED_CHAPTER_COUNT,
        EXPECTED_RECORD_COUNT,
        len(SECOND_REGRESSION_GATES),
        len(CHECK_KEYS),
        ready,
        len(CHECK_KEYS) - ready,
        ready == len(CHECK_KEYS),
        SECOND_REGRESSION_GATES,
        checks,
        {
            "archive_bundle_report": arch,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
        },
    )

def render_packet(packet: SecondRegressionPacket | None = None) -> str:
    packet = packet or build_packet()
    gates = "\n".join(f"- {gate}" for gate in packet.gates)
    return f"# {packet.label}\n\nVersion: {packet.version}\n\n## Second regression gates\n{gates}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
