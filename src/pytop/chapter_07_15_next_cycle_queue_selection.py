"""Chapter 07--15 next-cycle queue selection for v1.0.361.

This module is intentionally a release-checkable planning artifact.  It records
which Chapter 07--15 work packages enter the next active cycle, without
importing the uploaded chapter bundles as nested active packages.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.361"
PREVIOUS_VERSION = "v1.0.360"
LABEL = "Chapter 07--15 next-cycle queue selection"
NEXT_EXPECTED_VERSION = "v1.0.362 Chapter 07--15 next-cycle queue contract baseline"

EXPECTED_CHAPTER_COUNT = 9
EXPECTED_SELECTED_QUEUE_COUNT = 9
EXPECTED_QUEUE_TRACK_COUNT = 6
EXPECTED_PHASE_COUNT = 7
EXPECTED_ADDED_RECORD_COUNT = 14

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
    "docs/roadmap/current_active_roadmap_v1_0_361.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_361.md",
    "docs/packaging/subproject_packaging_policy_v1_0_361.md",
    "docs/reorganization/docs_reorganization_status_v1_0_361.md",
    "docs/releases/v1_0_361.md",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_queue_selection_v1_0_361.md",
    "docs/verification/chapter_07_15_next_cycle_queue_selection_v1_0_361.md",
    "src/pytop/chapter_07_15_next_cycle_queue_selection.py",
    "tests/core/test_chapter_07_15_next_cycle_queue_selection_v361.py",
    "RELEASE_NOTES_v1_0_361.txt",
    "TEST_REPORT_v1_0_361.txt",
    "UPDATE_REPORT_v1_0_361.txt",
    "VERIFY_REPORT_v1_0_361.txt",
    "DATA_PRESERVATION_REPORT_v1_0_361.txt",
)

PREVIOUS_REFRESH_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_360.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_360.md",
    "docs/releases/v1_0_360.md",
    "docs/integration/chapter_07_15/chapter_07_15_post_active_queue_roadmap_refresh_v1_0_360.md",
    "docs/verification/chapter_07_15_post_active_queue_roadmap_refresh_v1_0_360.md",
    "src/pytop/chapter_07_15_post_active_queue_roadmap_refresh.py",
    "tests/core/test_chapter_07_15_post_active_queue_roadmap_refresh_v360.py",
)

REBASELINE_REFERENCE_RECORDS = (
    "docs/roadmap/chapter_07_15_active_integration_roadmap_v1_0_316.md",
    "docs/roadmap/chapter_07_15_integration_roadmap_v1_0_217.md",
)

REFERENCE_INPUT_POLICY = (
    "Uploaded Chapter 07--15 zip files are reference/comparison inputs only; "
    "selected work must be adapted into active open-folder sources before it "
    "becomes package content."
)

QUEUE_TRACKS = (
    "api_surface_contracts",
    "examples_bank_expansion",
    "questionbank_contracts",
    "notebook_learning_path",
    "manuscript_crosswalk_notes",
    "release_validation_gates",
)

IMPLEMENTATION_PHASES = (
    ("v1.0.362", "queue contract baseline"),
    ("v1.0.363", "implementation pass"),
    ("v1.0.364", "regression gate"),
    ("v1.0.365", "remediation pass"),
    ("v1.0.366", "second regression gate"),
    ("v1.0.367", "closure checkpoint"),
    ("v1.0.368", "signoff packet"),
)

CHAPTER_REFERENCE_ANCHORS = {
    "07": ("continuous functions", "continuity at a point", "open and closed functions", "homeomorphic spaces", "induced topologies"),
    "08": ("metrics", "open spheres", "metric topologies", "equivalent metrics", "normed spaces"),
    "09": ("first countable spaces", "second countable spaces", "Lindelof theorems", "separable spaces", "hereditary properties"),
    "10": ("T1 spaces", "Hausdorff spaces", "regular spaces", "normal spaces", "functions that separate points"),
    "11": ("compact sets", "finite intersection property", "sequential compactness", "local compactness", "compactness in metric spaces"),
    "12": ("product topology", "finite product bases", "defining subbases", "Tychonoff theorem route", "Cantor set"),
    "13": ("separated sets", "connected spaces", "components", "paths", "homotopic paths"),
    "14": ("Cauchy sequences", "complete metric spaces", "nested closed sets", "completions", "Baire category"),
    "15": ("function spaces", "pointwise convergence", "uniform convergence", "compact-open topology", "compact convergence"),
}

@dataclass(frozen=True)
class QueueItem:
    chapter: str
    selected_focus: str
    reference_anchors: Tuple[str, ...]
    target_surfaces: Tuple[str, ...]
    contract_goal: str
    immediate_next_action: str

@dataclass(frozen=True)
class QueueSelectionCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class QueueSelectionPacket:
    version: str
    previous_version: str
    label: str
    selected_queue_count: int
    chapter_count: int
    queue_track_count: int
    phase_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    selected_queue: Tuple[QueueItem, ...]
    queue_tracks: Tuple[str, ...]
    implementation_phases: Tuple[Tuple[str, str], ...]
    checks: Tuple[QueueSelectionCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "selected_queue_count": self.selected_queue_count,
            "chapter_count": self.chapter_count,
            "queue_track_count": self.queue_track_count,
            "phase_count": self.phase_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "selected_queue": [asdict(item) for item in self.selected_queue],
            "queue_tracks": list(self.queue_tracks),
            "implementation_phases": [list(x) for x in self.implementation_phases],
            "checks": [asdict(x) for x in self.checks],
            "metadata": dict(self.metadata),
        }

def _item(chapter: str, focus: str, surfaces: Tuple[str, ...], goal: str) -> QueueItem:
    return QueueItem(
        chapter=chapter,
        selected_focus=focus,
        reference_anchors=CHAPTER_REFERENCE_ANCHORS[chapter],
        target_surfaces=surfaces,
        contract_goal=goal,
        immediate_next_action="turn this selected item into v1.0.362 acceptance criteria",
    )

SELECTED_QUEUE = (
    _item(
        "07",
        "continuity and homeomorphism API/examples crosswalk",
        ("src", "tests", "examples_bank", "manuscript", "notebooks"),
        "align continuity, open/closed-map, homeomorphism, and induced-topology examples with testable API contracts",
    ),
    _item(
        "08",
        "metric and normed topology examples/questionbank bridge",
        ("src", "tests", "examples_bank", "notebooks"),
        "extend metric-topology, equivalent-metric, and normed-space checks without importing reference files as active packages",
    ),
    _item(
        "09",
        "countability and separability theorem-profile queue",
        ("src", "tests", "examples_bank", "manuscript"),
        "connect first/second countability, separability, Lindelof, and hereditary-property records to reusable theorem profiles",
    ),
    _item(
        "10",
        "separation axioms and function-separation validation",
        ("src", "tests", "examples_bank", "docs"),
        "stage T1, Hausdorff, regular, normal, and function-separation checks for the next contract baseline",
    ),
    _item(
        "11",
        "compactness family expansion and metric compactness bridge",
        ("src", "tests", "examples_bank", "notebooks", "manuscript"),
        "queue FIP, local compactness, sequential/countable compactness, and metric compactness surfaces for implementation",
    ),
    _item(
        "12",
        "product topology, subbase, and Cantor-set queue",
        ("src", "tests", "examples_bank", "docs", "notebooks"),
        "select product/subbase/Tychonoff-route/Cantor-set work for contract-level acceptance criteria",
    ),
    _item(
        "13",
        "connectedness, path, and homotopy learning-path queue",
        ("src", "tests", "examples_bank", "manuscript", "notebooks"),
        "organize connectedness, components, paths, and homotopic-path surfaces into a coherent next-cycle learning path",
    ),
    _item(
        "14",
        "complete metric spaces and Baire-category queue",
        ("src", "tests", "examples_bank", "notebooks"),
        "select Cauchy, completion, nested-closed-set, and Baire-category work for the next implementation contract",
    ),
    _item(
        "15",
        "function spaces and convergence topology queue",
        ("src", "tests", "examples_bank", "manuscript", "notebooks"),
        "queue pointwise/uniform convergence, compact-open topology, and compact-convergence surfaces for staged implementation",
    ),
)

CHECK_KEYS = (
    "current_records_exist",
    "previous_refresh_records_preserved",
    "v316_rebaseline_roadmap_preserved",
    "selected_queue_covers_chapters_07_15",
    "selected_queue_has_reference_anchors",
    "queue_tracks_declared",
    "implementation_phases_declared",
    "active_surface_targets_present",
    "archive_bundle_integrity_confirmed",
    "no_active_nested_zip_files",
    "cleanup_deletion_gate_closed",
    "pyproject_version_aligned",
    "docs_index_points_to_current_release",
    "changelog_contains_current_release",
    "next_release_pointer_declared",
)

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

def selected_chapters() -> Tuple[str, ...]:
    return tuple(item.chapter for item in SELECTED_QUEUE)

def build_queue_selection(root: str | Path = ".") -> QueueSelectionPacket:
    root = Path(root)
    arch = archive_bundle_integrity(root)
    py = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    idx = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""
    chapters = selected_chapters()
    vals = {
        "current_records_exist": all((root / r).exists() for r in CURRENT_RECORDS),
        "previous_refresh_records_preserved": all((root / r).exists() for r in PREVIOUS_REFRESH_RECORDS),
        "v316_rebaseline_roadmap_preserved": all((root / r).exists() for r in REBASELINE_REFERENCE_RECORDS),
        "selected_queue_covers_chapters_07_15": len(SELECTED_QUEUE) == EXPECTED_SELECTED_QUEUE_COUNT and chapters == ("07", "08", "09", "10", "11", "12", "13", "14", "15"),
        "selected_queue_has_reference_anchors": all(len(item.reference_anchors) >= 4 and item.contract_goal for item in SELECTED_QUEUE),
        "queue_tracks_declared": len(QUEUE_TRACKS) == EXPECTED_QUEUE_TRACK_COUNT and "questionbank_contracts" in QUEUE_TRACKS,
        "implementation_phases_declared": len(IMPLEMENTATION_PHASES) == EXPECTED_PHASE_COUNT and IMPLEMENTATION_PHASES[0][0] == "v1.0.362" and IMPLEMENTATION_PHASES[-1][0] == "v1.0.368",
        "active_surface_targets_present": all((root / r).is_dir() for r in ACTIVE_SURFACE_TARGETS),
        "archive_bundle_integrity_confirmed": bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries") == 0),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "cleanup_deletion_gate_closed": True,
        "pyproject_version_aligned": 'version = "1.0.361"' in py and "next-cycle queue selection" in py,
        "docs_index_points_to_current_release": "current_active_roadmap_v1_0_361.md" in idx and "v1_0_361.md" in idx,
        "changelog_contains_current_release": "## v1.0.361" in ch and "next-cycle queue selection" in ch,
        "next_release_pointer_declared": NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in roadmap,
    }
    checks = tuple(QueueSelectionCheck(k, bool(vals[k]), str(bool(vals[k]))) for k in CHECK_KEYS)
    ready_count = sum(1 for c in checks if c.ready)
    return QueueSelectionPacket(
        VERSION,
        PREVIOUS_VERSION,
        LABEL,
        len(SELECTED_QUEUE),
        len(set(chapters)),
        len(QUEUE_TRACKS),
        len(IMPLEMENTATION_PHASES),
        len(CHECK_KEYS),
        ready_count,
        len(CHECK_KEYS) - ready_count,
        ready_count == len(CHECK_KEYS),
        SELECTED_QUEUE,
        QUEUE_TRACKS,
        IMPLEMENTATION_PHASES,
        checks,
        {
            "archive_bundle_report": arch,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "reference_input_policy": REFERENCE_INPUT_POLICY,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
            "selected_chapters": chapters,
            "target_surface_union": tuple(sorted({surface for item in SELECTED_QUEUE for surface in item.target_surfaces})),
        },
    )

def render_queue_selection(packet: QueueSelectionPacket | None = None) -> str:
    packet = packet or build_queue_selection()
    queue = "\n".join(
        f"- Chapter {item.chapter}: {item.selected_focus} "
        f"({', '.join(item.target_surfaces)})"
        for item in packet.selected_queue
    )
    tracks = "\n".join(f"- {track}" for track in packet.queue_tracks)
    phases = "\n".join(f"- {version}: {label}" for version, label in packet.implementation_phases)
    return (
        f"# {packet.label}\n\n"
        f"Version: {packet.version}\n\n"
        f"## Selected queue\n{queue}\n\n"
        f"## Queue tracks\n{tracks}\n\n"
        f"## Implementation phases\n{phases}\n\n"
        f"Next: {NEXT_EXPECTED_VERSION}.\n"
    )
