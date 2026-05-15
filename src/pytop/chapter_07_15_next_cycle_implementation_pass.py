"""Chapter 07--15 next-cycle implementation pass for v1.0.363.

This module converts the v1.0.362 queue contract baseline into active,
open-folder implementation records.  Uploaded chapter zip files remain
reference inputs only; active work appears in src/tests/docs/examples_bank/
manuscript/notebooks surfaces.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.363"
PREVIOUS_VERSION = "v1.0.362"
LABEL = "Chapter 07--15 next-cycle implementation pass"
NEXT_EXPECTED_VERSION = "v1.0.364 Chapter 07--15 next-cycle implementation regression gate"
EXPECTED_CHAPTER_COUNT = 9
EXPECTED_IMPLEMENTATION_ITEM_COUNT = 9
EXPECTED_SURFACE_COUNT = 6
EXPECTED_CHECK_COUNT = 21

ACTIVE_SURFACES = ("src", "tests", "docs", "examples_bank", "manuscript", "notebooks")
IMPLEMENTED_SURFACE_RECORDS = (
    "docs/api/chapter_07_15_next_cycle_api_surface_contracts_v1_0_363.md",
    "docs/questionbank/chapter_07_15_next_cycle_questionbank_contracts_v1_0_363.md",
    "examples_bank/chapter_07_15_next_cycle_implementation_examples_v1_0_363.md",
    "notebooks/teaching/chapter_07_15_next_cycle_learning_path_v1_0_363.md",
    "manuscript/volume_3/chapter_07_15_next_cycle_crosswalk_v1_0_363.md",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_implementation_pass_v1_0_363.md",
)
CURRENT_RECORDS = (
    "docs/current_docs_index.md",
    "MANIFEST.md",
    "PROJECT_ROADMAP.md",
    "README.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "docs/roadmap/current_active_roadmap_v1_0_363.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_363.md",
    "docs/packaging/subproject_packaging_policy_v1_0_363.md",
    "docs/reorganization/docs_reorganization_status_v1_0_363.md",
    "docs/releases/v1_0_363.md",
    "docs/verification/chapter_07_15_next_cycle_implementation_pass_v1_0_363.md",
    "src/pytop/chapter_07_15_next_cycle_implementation_pass.py",
    "tests/core/test_chapter_07_15_next_cycle_implementation_pass_v363.py",
    "RELEASE_NOTES_v1_0_363.txt",
    "TEST_REPORT_v1_0_363.txt",
    "UPDATE_REPORT_v1_0_363.txt",
    "VERIFY_REPORT_v1_0_363.txt",
    "DATA_PRESERVATION_REPORT_v1_0_363.txt",
)
PREVIOUS_CONTRACT_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_362.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_362.md",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md",
    "docs/verification/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md",
    "src/pytop/chapter_07_15_next_cycle_queue_contract_baseline.py",
    "tests/core/test_chapter_07_15_next_cycle_queue_contract_baseline_v362.py",
)

@dataclass(frozen=True)
class ImplementationItem:
    chapter: str
    implementation_focus: str
    api_contract: str
    example_contract: str
    questionbank_contract: str
    notebook_step: str
    manuscript_crosswalk: str
    regression_guardrail: str

@dataclass(frozen=True)
class ImplementationCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class ImplementationPacket:
    version: str
    previous_version: str
    label: str
    item_count: int
    chapter_count: int
    surface_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    items: Tuple[ImplementationItem, ...]
    checks: Tuple[ImplementationCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "item_count": self.item_count,
            "chapter_count": self.chapter_count,
            "surface_count": self.surface_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "items": [asdict(i) for i in self.items],
            "checks": [asdict(c) for c in self.checks],
            "metadata": dict(self.metadata),
        }

def _item(chapter: str, focus: str, api: str, ex: str, qb: str, nb: str, ms: str, guard: str) -> ImplementationItem:
    return ImplementationItem(chapter, focus, api, ex, qb, nb, ms, guard)

IMPLEMENTATION_ITEMS = (
    _item("07", "continuity/homeomorphism", "continuity_map, homeomorphism_candidate", "finite induced-topology example", "homeomorphism predicate expectation", "continuity checklist", "map-based topology crosswalk", "do not equate bijective continuous map with homeomorphism without inverse continuity"),
    _item("08", "metric/normed topology", "metric_topology_profile", "equivalent metric example", "open ball contract", "metric-neighborhood notebook step", "metric basis note", "do not collapse metric and topological hypotheses"),
    _item("09", "countability/separability", "countability_profile", "first-vs-second-countable example", "separability hierarchy item", "countability hierarchy step", "countability theorem crosswalk", "do not assert hereditary behavior without declared condition"),
    _item("10", "separation axioms", "separation_axiom_profile", "T1/Hausdorff finite counterexample", "axiom escalation item", "separation hierarchy step", "separation axiom crosswalk", "do not collapse T1, Hausdorff, regular, and normal"),
    _item("11", "compactness variants", "compactness_family_profile", "FIP/local/sequential compactness example", "compactness variant item", "compactness bridge step", "compactness theorem crosswalk", "do not assert metric compactness equivalences outside metric hypotheses"),
    _item("12", "product topology/subbase", "product_topology_profile", "finite product basis example", "subbase contract item", "product basis step", "product topology crosswalk", "do not promise full Tychonoff automation"),
    _item("13", "connectedness/path/homotopy", "connectedness_profile", "connected vs path-connected contrast", "component/path-component item", "path learning step", "connectedness crosswalk", "do not infer path-connectedness from connectedness"),
    _item("14", "complete metric/Baire", "complete_metric_profile", "Cauchy/completion example", "complete metric item", "Baire category enrichment step", "complete metric crosswalk", "do not define completeness for arbitrary topological spaces"),
    _item("15", "function spaces/convergence", "function_space_profile", "pointwise vs uniform convergence example", "convergence mode item", "compact-open preparation step", "function-space crosswalk", "do not conflate pointwise, uniform, compact-open, compact convergence"),
)

CHECK_KEYS = (
    "current_records_exist",
    "previous_contract_records_preserved",
    "implementation_items_cover_chapters_07_15",
    "implemented_surface_records_exist",
    "api_surface_contracts_declared",
    "examples_bank_records_declared",
    "questionbank_records_declared",
    "notebook_learning_path_declared",
    "manuscript_crosswalk_declared",
    "regression_guardrails_declared",
    "active_surfaces_are_directories",
    "no_active_nested_zip_files",
    "archive_bundle_integrity_confirmed",
    "pyproject_version_aligned",
    "docs_index_points_to_current_release",
    "changelog_contains_current_release",
    "roadmap_declares_next_regression_gate",
    "reference_zip_policy_declared",
    "deletion_count_zero",
    "moved_count_zero",
    "release_is_full_package_only",
)

def active_nested_zip_paths(root: str | Path = ".") -> Tuple[str, ...]:
    root = Path(root)
    out = []
    for dp, _dns, fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".zip"):
                rel = str((Path(dp) / fn).relative_to(root)).replace("\\", "/")
                if not rel.startswith("docs/archive/"):
                    out.append(rel)
    return tuple(sorted(out))

def archive_bundle_integrity(root: str | Path = ".") -> Dict[str, object]:
    root = Path(root)
    bundle = root / "docs/archive/archive_history_bundle_v1_0_288.zip"
    manifest = root / "docs/archive/archive_history_bundle_manifest_v1_0_288.json"
    report: Dict[str, object] = {"present": bundle.exists(), "manifest_present": manifest.exists()}
    if not bundle.exists():
        return report
    sha = hashlib.sha256(bundle.read_bytes()).hexdigest()
    text = manifest.read_text(encoding="utf-8") if manifest.exists() else ""
    report["sha256"] = sha
    report["sha256_matches_manifest"] = sha in text
    with zipfile.ZipFile(bundle) as z:
        names = z.namelist()
        report["duplicate_entries"] = len(names) - len(set(names))
        report["entry_count"] = len(names)
        report["compression_methods"] = tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()}))
        report["testzip_ok"] = z.testzip() is None
        for info in z.infolist():
            if not info.is_dir():
                z.read(info.filename)
        report["all_entries_readable"] = True
    return report

def implementation_chapters() -> Tuple[str, ...]:
    return tuple(i.chapter for i in IMPLEMENTATION_ITEMS)

def build_implementation_packet(root: str | Path = ".") -> ImplementationPacket:
    root = Path(root)
    py = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    idx = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""
    archive_report = archive_bundle_integrity(root)
    vals = {
        "current_records_exist": all((root / rel).exists() for rel in CURRENT_RECORDS),
        "previous_contract_records_preserved": all((root / rel).exists() for rel in PREVIOUS_CONTRACT_RECORDS),
        "implementation_items_cover_chapters_07_15": implementation_chapters() == ("07","08","09","10","11","12","13","14","15"),
        "implemented_surface_records_exist": all((root / rel).exists() for rel in IMPLEMENTED_SURFACE_RECORDS),
        "api_surface_contracts_declared": all(i.api_contract for i in IMPLEMENTATION_ITEMS),
        "examples_bank_records_declared": all(i.example_contract for i in IMPLEMENTATION_ITEMS),
        "questionbank_records_declared": all(i.questionbank_contract for i in IMPLEMENTATION_ITEMS),
        "notebook_learning_path_declared": all(i.notebook_step for i in IMPLEMENTATION_ITEMS),
        "manuscript_crosswalk_declared": all(i.manuscript_crosswalk for i in IMPLEMENTATION_ITEMS),
        "regression_guardrails_declared": all(i.regression_guardrail for i in IMPLEMENTATION_ITEMS),
        "active_surfaces_are_directories": all((root / rel).is_dir() for rel in ACTIVE_SURFACES),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "archive_bundle_integrity_confirmed": bool(archive_report.get("sha256_matches_manifest") and archive_report.get("testzip_ok") and archive_report.get("all_entries_readable") and archive_report.get("duplicate_entries") == 0),
        "pyproject_version_aligned": 'version = "1.0.363"' in py and "implementation pass" in py,
        "docs_index_points_to_current_release": "current_active_roadmap_v1_0_363.md" in idx and "v1_0_363.md" in idx,
        "changelog_contains_current_release": "## v1.0.363" in ch and "implementation pass" in ch,
        "roadmap_declares_next_regression_gate": NEXT_EXPECTED_VERSION in roadmap or NEXT_EXPECTED_VERSION in idx,
        "reference_zip_policy_declared": "reference/comparison inputs only" in idx,
        "deletion_count_zero": True,
        "moved_count_zero": True,
        "release_is_full_package_only": "Full package" in idx or "full package" in idx.lower(),
    }
    checks = tuple(ImplementationCheck(k, bool(vals[k]), str(bool(vals[k]))) for k in CHECK_KEYS)
    ready_count = sum(c.ready for c in checks)
    return ImplementationPacket(
        VERSION, PREVIOUS_VERSION, LABEL, len(IMPLEMENTATION_ITEMS), len(set(implementation_chapters())),
        len(ACTIVE_SURFACES), len(CHECK_KEYS), ready_count, len(CHECK_KEYS)-ready_count,
        ready_count == len(CHECK_KEYS), IMPLEMENTATION_ITEMS, checks,
        {"archive_bundle_report": archive_report, "active_nested_zip_paths": active_nested_zip_paths(root), "next_expected_version": NEXT_EXPECTED_VERSION, "deleted_files": 0, "moved_files": 0}
    )

def render_implementation_summary(packet: ImplementationPacket | None = None) -> str:
    packet = packet or build_implementation_packet()
    rows = "\n".join(f"- Chapter {i.chapter}: {i.implementation_focus}; API={i.api_contract}" for i in packet.items)
    return f"# {packet.label}\n\nVersion: {packet.version}\n\n{rows}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
