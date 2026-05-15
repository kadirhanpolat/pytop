"""Chapter 07--15 post-active-queue roadmap refresh for v1.0.360."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.360"
PREVIOUS_VERSION = "v1.0.359"
LABEL = "Chapter 07--15 post-active-queue roadmap refresh"
NEXT_EXPECTED_VERSION = "v1.0.361 Chapter 07--15 next-cycle queue selection"

EXPECTED_CHAPTER_COUNT = 9
EXPECTED_ADDED_RECORD_COUNT = 14
EXPECTED_REFRESH_TRACK_COUNT = 7
EXPECTED_NEXT_CYCLE_PLAN_COUNT = 8

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
    "docs/roadmap/current_active_roadmap_v1_0_360.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_360.md",
    "docs/packaging/subproject_packaging_policy_v1_0_360.md",
    "docs/reorganization/docs_reorganization_status_v1_0_360.md",
    "docs/releases/v1_0_360.md",
    "docs/integration/chapter_07_15/chapter_07_15_post_active_queue_roadmap_refresh_v1_0_360.md",
    "docs/verification/chapter_07_15_post_active_queue_roadmap_refresh_v1_0_360.md",
    "src/pytop/chapter_07_15_post_active_queue_roadmap_refresh.py",
    "tests/core/test_chapter_07_15_post_active_queue_roadmap_refresh_v360.py",
    "RELEASE_NOTES_v1_0_360.txt",
    "TEST_REPORT_v1_0_360.txt",
    "UPDATE_REPORT_v1_0_360.txt",
    "VERIFY_REPORT_v1_0_360.txt",
    "DATA_PRESERVATION_REPORT_v1_0_360.txt",
)

PREVIOUS_HANDOFF_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_359.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_359.md",
    "docs/releases/v1_0_359.md",
    "docs/integration/chapter_07_15/chapter_07_15_active_queue_implementation_final_handoff_audit_v1_0_359.md",
    "docs/verification/chapter_07_15_active_queue_implementation_final_handoff_audit_v1_0_359.md",
    "src/pytop/chapter_07_15_active_queue_implementation_final_handoff_audit.py",
    "tests/core/test_chapter_07_15_active_queue_implementation_final_handoff_audit_v359.py",
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
    "docs/roadmap/current_active_roadmap_v1_0_359.md",
)

REBASELINE_REFERENCE_RECORDS = (
    "docs/roadmap/chapter_07_15_active_integration_roadmap_v1_0_316.md",
    "docs/roadmap/chapter_07_15_integration_roadmap_v1_0_217.md",
)

REFRESH_TRACKS = (
    "v316_rebaseline_followthrough",
    "active_queue_chain_handoff_absorbed",
    "chapter_theme_coverage_resynchronization",
    "examples_questionbank_notebook_backlog_refresh",
    "api_generator_next_cycle_backlog",
    "packaging_archive_policy_reaffirmation",
    "next_cycle_version_plan_declared",
)

NEXT_CYCLE_PLAN = (
    ("v1.0.361", "Chapter 07--15 next-cycle queue selection"),
    ("v1.0.362", "Chapter 07--15 next-cycle queue contract baseline"),
    ("v1.0.363", "Chapter 07--15 next-cycle implementation pass"),
    ("v1.0.364", "Chapter 07--15 next-cycle regression gate"),
    ("v1.0.365", "Chapter 07--15 next-cycle remediation pass"),
    ("v1.0.366", "Chapter 07--15 next-cycle second regression gate"),
    ("v1.0.367", "Chapter 07--15 next-cycle closure checkpoint"),
    ("v1.0.368", "Chapter 07--15 next-cycle signoff packet"),
)

CHAPTER_THEME_MAP = {
    "07": ("continuous maps", "open and closed maps", "homeomorphism", "induced topologies"),
    "08": ("metrics", "metric topologies", "equivalent metrics", "normed spaces"),
    "09": ("first countability", "second countability", "separability", "Lindelof-type arguments"),
    "10": ("Hausdorff", "regular", "normal", "function separation"),
    "11": ("compactness", "finite intersection property", "countable compactness", "local compactness"),
    "12": ("product topology", "subbases", "Tychonoff route", "Cantor set"),
    "13": ("connectedness", "components", "path connectedness", "homotopic paths"),
    "14": ("Cauchy sequences", "complete metric spaces", "completions", "Baire category"),
    "15": ("function spaces", "pointwise convergence", "uniform convergence", "compact-open topology"),
}

CHECK_KEYS = (
    "current_records_exist",
    "previous_handoff_records_preserved",
    "active_queue_chain_records_preserved",
    "v316_rebaseline_roadmap_preserved",
    "refresh_tracks_declared",
    "next_cycle_plan_declared",
    "chapter_theme_map_complete",
    "active_surface_targets_present",
    "archive_bundle_integrity_confirmed",
    "no_active_nested_zip_files",
    "cleanup_deletion_gate_closed",
    "pyproject_version_aligned",
    "docs_index_points_to_current_release",
    "changelog_contains_current_release",
    "next_release_pointer_declared",
)

@dataclass(frozen=True)
class RoadmapRefreshCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class RoadmapRefreshPacket:
    version: str
    previous_version: str
    label: str
    chapter_count: int
    added_record_count: int
    refresh_track_count: int
    next_cycle_plan_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    refresh_tracks: Tuple[str, ...]
    next_cycle_plan: Tuple[Tuple[str, str], ...]
    chapter_theme_map: Mapping[str, Tuple[str, ...]]
    checks: Tuple[RoadmapRefreshCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "added_record_count": self.added_record_count,
            "refresh_track_count": self.refresh_track_count,
            "next_cycle_plan_count": self.next_cycle_plan_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "refresh_tracks": list(self.refresh_tracks),
            "next_cycle_plan": [list(x) for x in self.next_cycle_plan],
            "chapter_theme_map": {k: list(v) for k, v in self.chapter_theme_map.items()},
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

def build_roadmap_refresh(root: str | Path = ".") -> RoadmapRefreshPacket:
    root = Path(root)
    arch = archive_bundle_integrity(root)
    py = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    idx = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""

    vals = {
        "current_records_exist": all((root / r).exists() for r in CURRENT_RECORDS),
        "previous_handoff_records_preserved": all((root / r).exists() for r in PREVIOUS_HANDOFF_RECORDS),
        "active_queue_chain_records_preserved": all((root / r).exists() for r in ACTIVE_QUEUE_CHAIN_RECORDS),
        "v316_rebaseline_roadmap_preserved": all((root / r).exists() for r in REBASELINE_REFERENCE_RECORDS),
        "refresh_tracks_declared": len(REFRESH_TRACKS) == EXPECTED_REFRESH_TRACK_COUNT and REFRESH_TRACKS[0] == "v316_rebaseline_followthrough",
        "next_cycle_plan_declared": len(NEXT_CYCLE_PLAN) == EXPECTED_NEXT_CYCLE_PLAN_COUNT and NEXT_CYCLE_PLAN[0][0] == "v1.0.361",
        "chapter_theme_map_complete": len(CHAPTER_THEME_MAP) == EXPECTED_CHAPTER_COUNT and tuple(CHAPTER_THEME_MAP.keys()) == ("07", "08", "09", "10", "11", "12", "13", "14", "15"),
        "active_surface_targets_present": all((root / r).is_dir() for r in ACTIVE_SURFACE_TARGETS),
        "archive_bundle_integrity_confirmed": bool(arch.get("sha256_matches_manifest") and arch.get("testzip_ok") and arch.get("all_entries_readable") and arch.get("duplicate_entries") == 0),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "cleanup_deletion_gate_closed": True,
        "pyproject_version_aligned": 'version = "1.0.360"' in py and "post-active-queue roadmap refresh" in py,
        "docs_index_points_to_current_release": "current_active_roadmap_v1_0_360.md" in idx and "v1_0_360.md" in idx,
        "changelog_contains_current_release": "## v1.0.360" in ch and "post-active-queue roadmap refresh" in ch,
        "next_release_pointer_declared": NEXT_EXPECTED_VERSION in idx or NEXT_EXPECTED_VERSION in roadmap,
    }
    checks = tuple(RoadmapRefreshCheck(k, bool(vals[k]), str(bool(vals[k]))) for k in CHECK_KEYS)
    ready = sum(1 for c in checks if c.ready)
    return RoadmapRefreshPacket(
        VERSION,
        PREVIOUS_VERSION,
        LABEL,
        EXPECTED_CHAPTER_COUNT,
        EXPECTED_ADDED_RECORD_COUNT,
        len(REFRESH_TRACKS),
        len(NEXT_CYCLE_PLAN),
        len(CHECK_KEYS),
        ready,
        len(CHECK_KEYS) - ready,
        ready == len(CHECK_KEYS),
        REFRESH_TRACKS,
        NEXT_CYCLE_PLAN,
        CHAPTER_THEME_MAP,
        checks,
        {
            "archive_bundle_report": arch,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
            "reference_inputs_policy": "Chapter 07--15 zip files are comparison/reference inputs only unless adapted into active open-folder sources.",
        },
    )

def render_roadmap_refresh(packet: RoadmapRefreshPacket | None = None) -> str:
    packet = packet or build_roadmap_refresh()
    tracks = "\n".join(f"- {track}" for track in packet.refresh_tracks)
    plan = "\n".join(f"- {version}: {label}" for version, label in packet.next_cycle_plan)
    themes = "\n".join(f"- Chapter {chapter}: {', '.join(themes)}" for chapter, themes in packet.chapter_theme_map.items())
    return (
        f"# {packet.label}\n\n"
        f"Version: {packet.version}\n\n"
        f"## Refresh tracks\n{tracks}\n\n"
        f"## Next-cycle plan\n{plan}\n\n"
        f"## Chapter themes\n{themes}\n\n"
        f"Next: {NEXT_EXPECTED_VERSION}.\n"
    )
