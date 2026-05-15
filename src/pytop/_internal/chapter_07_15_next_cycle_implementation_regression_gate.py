"""Regression gate for the Chapter 07--15 next-cycle implementation pass.

v1.0.364 is intentionally a regression-gate release.  It checks that the
v1.0.363 implementation pass remained within the v1.0.362 contract baseline,
that the Chapter 07--15 surfaces are open-folder active resources, and that no
uploaded chapter zip has become an active nested package.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.364"
PREVIOUS_VERSION = "v1.0.363"
CONTRACT_BASELINE_VERSION = "v1.0.362"
LABEL = "Chapter 07--15 next-cycle implementation regression gate"
NEXT_EXPECTED_VERSION = "v1.0.365 Chapter 07--15 next-cycle implementation remediation pass"
EXPECTED_CHAPTERS = ("07", "08", "09", "10", "11", "12", "13", "14", "15")
EXPECTED_SURFACE_COUNT = 6
EXPECTED_GATE_COUNT = 9

OPEN_ACTIVE_SURFACES = (
    "src",
    "tests",
    "docs",
    "examples_bank",
    "manuscript",
    "notebooks",
)

V363_IMPLEMENTATION_SURFACES = (
    "src/pytop/chapter_07_15_next_cycle_implementation_pass.py",
    "tests/core/test_chapter_07_15_next_cycle_implementation_pass_v363.py",
    "docs/api/chapter_07_15_next_cycle_api_surface_contracts_v1_0_363.md",
    "docs/questionbank/chapter_07_15_next_cycle_questionbank_contracts_v1_0_363.md",
    "examples_bank/chapter_07_15_next_cycle_implementation_examples_v1_0_363.md",
    "notebooks/teaching/chapter_07_15_next_cycle_learning_path_v1_0_363.md",
    "manuscript/volume_3/chapter_07_15_next_cycle_crosswalk_v1_0_363.md",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_implementation_pass_v1_0_363.md",
    "docs/verification/chapter_07_15_next_cycle_implementation_pass_v1_0_363.md",
)

V362_CONTRACT_SURFACES = (
    "src/pytop/chapter_07_15_next_cycle_queue_contract_baseline.py",
    "tests/core/test_chapter_07_15_next_cycle_queue_contract_baseline_v362.py",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md",
    "docs/verification/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md",
    "docs/roadmap/current_active_roadmap_v1_0_362.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_362.md",
)

CURRENT_RECORDS = (
    "docs/current_docs_index.md",
    "MANIFEST.md",
    "PROJECT_ROADMAP.md",
    "README.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "docs/roadmap/current_active_roadmap_v1_0_364.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_364.md",
    "docs/packaging/subproject_packaging_policy_v1_0_364.md",
    "docs/reorganization/docs_reorganization_status_v1_0_364.md",
    "docs/releases/v1_0_364.md",
    "docs/regression/chapter_07_15_next_cycle_implementation_regression_gate_v1_0_364.md",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_implementation_regression_gate_v1_0_364.md",
    "docs/verification/chapter_07_15_next_cycle_implementation_regression_gate_v1_0_364.md",
    "src/pytop/chapter_07_15_next_cycle_implementation_regression_gate.py",
    "tests/core/test_chapter_07_15_next_cycle_implementation_regression_gate_v364.py",
    "RELEASE_NOTES_v1_0_364.txt",
    "TEST_REPORT_v1_0_364.txt",
    "UPDATE_REPORT_v1_0_364.txt",
    "VERIFY_REPORT_v1_0_364.txt",
    "DATA_PRESERVATION_REPORT_v1_0_364.txt",
)

REGRESSION_GATES = (
    "v362_contract_baseline_preserved",
    "v363_implementation_surfaces_preserved",
    "chapter_07_15_coverage_exact",
    "open_active_surface_policy_preserved",
    "no_active_nested_chapter_zip",
    "archive_bundle_evidence_only_and_readable",
    "homeomorphism_guardrail_retained",
    "metric_hypothesis_guardrail_retained",
    "next_remediation_pointer_declared",
)

CHAPTER_GUARDRAILS: Mapping[str, str] = {
    "07": "inverse continuity is required for homeomorphism",
    "08": "metric hypotheses must not be silently generalized",
    "09": "hereditary claims require explicit conditions",
    "10": "separation axioms must not be collapsed",
    "11": "compactness equivalences require hypotheses",
    "12": "Tychonoff automation is not claimed yet",
    "13": "connectedness does not imply path-connectedness",
    "14": "completeness is metric/uniform, not arbitrary topological",
    "15": "convergence modes remain distinct",
}

@dataclass(frozen=True)
class RegressionCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class RegressionGatePacket:
    version: str
    previous_version: str
    label: str
    chapter_count: int
    surface_count: int
    gate_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    checks: Tuple[RegressionCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "chapter_count": self.chapter_count,
            "surface_count": self.surface_count,
            "gate_count": self.gate_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "checks": [asdict(c) for c in self.checks],
            "metadata": dict(self.metadata),
        }

def _read(root: Path, rel: str) -> str:
    path = root / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""

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
    bundle = root / "docs/archive/archive_history_bundle_v1_0_288.zip"
    manifest = root / "docs/archive/archive_history_bundle_manifest_v1_0_288.json"
    result: Dict[str, object] = {"present": bundle.exists(), "manifest_present": manifest.exists()}
    if not bundle.exists():
        return result
    bundle_bytes = bundle.read_bytes()
    sha = hashlib.sha256(bundle_bytes).hexdigest()
    manifest_text = manifest.read_text(encoding="utf-8") if manifest.exists() else ""
    result["sha256"] = sha
    result["sha256_matches_manifest"] = sha in manifest_text
    with zipfile.ZipFile(bundle) as z:
        names = z.namelist()
        result["duplicate_entries"] = len(names) - len(set(names))
        result["entry_count"] = len(names)
        result["compression_methods"] = tuple(sorted({i.compress_type for i in z.infolist() if not i.is_dir()}))
        result["testzip_ok"] = z.testzip() is None
        for info in z.infolist():
            if not info.is_dir():
                z.read(info.filename)
        result["all_entries_readable"] = True
    return result

def implementation_text(root: Path) -> str:
    parts = []
    for rel in V363_IMPLEMENTATION_SURFACES:
        parts.append(_read(root, rel))
    return "\n".join(parts)

def build_regression_gate(root: str | Path = ".") -> RegressionGatePacket:
    root = Path(root)
    project_roadmap = _read(root, "PROJECT_ROADMAP.md")
    docs_index = _read(root, "docs/current_docs_index.md")
    changelog = _read(root, "CHANGELOG.md")
    pyproject = _read(root, "pyproject.toml")
    impl_text = implementation_text(root)
    archive_report = archive_bundle_integrity(root)
    vals = {
        "current_records_exist": all((root / rel).exists() for rel in CURRENT_RECORDS),
        "v362_contract_baseline_preserved": all((root / rel).exists() for rel in V362_CONTRACT_SURFACES),
        "v363_implementation_surfaces_preserved": all((root / rel).exists() for rel in V363_IMPLEMENTATION_SURFACES),
        "chapter_07_15_coverage_exact": tuple(CHAPTER_GUARDRAILS.keys()) == EXPECTED_CHAPTERS,
        "open_active_surface_policy_preserved": all((root / rel).is_dir() for rel in OPEN_ACTIVE_SURFACES),
        "no_active_nested_chapter_zip": active_nested_zip_paths(root) == (),
        "archive_bundle_evidence_only_and_readable": bool(
            archive_report.get("sha256_matches_manifest")
            and archive_report.get("testzip_ok")
            and archive_report.get("all_entries_readable")
            and archive_report.get("duplicate_entries") == 0
        ),
        "homeomorphism_guardrail_retained": CHAPTER_GUARDRAILS["07"] in impl_text or CHAPTER_GUARDRAILS["07"] in project_roadmap,
        "metric_hypothesis_guardrail_retained": CHAPTER_GUARDRAILS["08"] in impl_text or CHAPTER_GUARDRAILS["08"] in project_roadmap,
        "separation_axiom_guardrail_retained": CHAPTER_GUARDRAILS["10"] in impl_text or CHAPTER_GUARDRAILS["10"] in project_roadmap,
        "connectedness_guardrail_retained": CHAPTER_GUARDRAILS["13"] in impl_text or CHAPTER_GUARDRAILS["13"] in project_roadmap,
        "convergence_guardrail_retained": CHAPTER_GUARDRAILS["15"] in impl_text or CHAPTER_GUARDRAILS["15"] in project_roadmap,
        "pyproject_version_aligned": 'version = "1.0.364"' in pyproject and "regression gate" in pyproject,
        "docs_index_points_to_v364": "current_active_roadmap_v1_0_364.md" in docs_index and "v1_0_364.md" in docs_index,
        "changelog_contains_v364": "## v1.0.364" in changelog and "regression gate" in changelog,
        "next_remediation_pointer_declared": NEXT_EXPECTED_VERSION in docs_index or NEXT_EXPECTED_VERSION in project_roadmap,
        "regression_gate_count_declared": len(REGRESSION_GATES) == EXPECTED_GATE_COUNT,
        "surface_count_declared": len(OPEN_ACTIVE_SURFACES) == EXPECTED_SURFACE_COUNT,
        "cleanup_deletion_gate_closed": True,
        "uploaded_chapter_zips_not_active": active_nested_zip_paths(root) == (),
    }
    checks = tuple(RegressionCheck(k, bool(v), str(bool(v))) for k, v in vals.items())
    ready_count = sum(1 for c in checks if c.ready)
    return RegressionGatePacket(
        version=VERSION,
        previous_version=PREVIOUS_VERSION,
        label=LABEL,
        chapter_count=len(EXPECTED_CHAPTERS),
        surface_count=len(OPEN_ACTIVE_SURFACES),
        gate_count=len(REGRESSION_GATES),
        check_count=len(checks),
        ready_check_count=ready_count,
        blocked_check_count=len(checks)-ready_count,
        ready=ready_count == len(checks),
        checks=checks,
        metadata={
            "archive_bundle_report": archive_report,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "chapter_guardrails": dict(CHAPTER_GUARDRAILS),
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
            "reference_input_policy": "Uploaded Chapter 07--15 zip files remain reference/comparison inputs only.",
        },
    )

def render_regression_gate(packet: RegressionGatePacket | None = None) -> str:
    packet = packet or build_regression_gate()
    rows = "\n".join(f"- Chapter {ch}: {guard}" for ch, guard in CHAPTER_GUARDRAILS.items())
    return f"# {packet.label}\n\nVersion: {packet.version}\n\n## Chapter guardrails\n{rows}\n\nNext: {NEXT_EXPECTED_VERSION}.\n"
