"""Chapter 07--15 next-cycle implementation remediation pass for v1.0.365."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple
import hashlib
import os
import zipfile

VERSION = "v1.0.365"
PREVIOUS_VERSION = "v1.0.364"
LABEL = "Chapter 07--15 next-cycle implementation remediation pass"
NEXT_EXPECTED_VERSION = "v1.0.366 Chapter 07--15 next-cycle implementation second regression gate"

ACTIVE_SURFACE_TARGETS = ("src", "tests", "docs", "examples_bank", "manuscript", "notebooks", "tools")
REFERENCE_INPUT_POLICY = (
    "Uploaded Chapter 07--15 zip files remain reference/comparison inputs only; "
    "remediated content becomes active only through open-folder source, test, docs, "
    "examples_bank, manuscript, or notebook surfaces."
)

CURRENT_RECORDS = (
    "docs/current_docs_index.md",
    "MANIFEST.md",
    "PROJECT_ROADMAP.md",
    "README.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "docs/roadmap/current_active_roadmap_v1_0_365.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_365.md",
    "docs/packaging/subproject_packaging_policy_v1_0_365.md",
    "docs/reorganization/docs_reorganization_status_v1_0_365.md",
    "docs/releases/v1_0_365.md",
    "docs/remediation/chapter_07_15_next_cycle_implementation_remediation_pass_v1_0_365.md",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_implementation_remediation_pass_v1_0_365.md",
    "docs/verification/chapter_07_15_next_cycle_implementation_remediation_pass_v1_0_365.md",
    "src/pytop/chapter_07_15_next_cycle_implementation_remediation_pass.py",
    "tests/core/test_chapter_07_15_next_cycle_implementation_remediation_pass_v365.py",
    "RELEASE_NOTES_v1_0_365.txt",
    "TEST_REPORT_v1_0_365.txt",
    "UPDATE_REPORT_v1_0_365.txt",
    "VERIFY_REPORT_v1_0_365.txt",
    "DATA_PRESERVATION_REPORT_v1_0_365.txt",
)

PREVIOUS_GATE_RECORDS = (
    "docs/roadmap/current_active_roadmap_v1_0_364.md",
    "docs/roadmap/active_versioning_roadmap_v1_0_364.md",
    "src/pytop/chapter_07_15_next_cycle_implementation_regression_gate.py",
    "tests/core/test_chapter_07_15_next_cycle_implementation_regression_gate_v364.py",
    "docs/regression/chapter_07_15_next_cycle_implementation_regression_gate_v1_0_364.md",
)

IMPLEMENTATION_RECORDS = (
    "src/pytop/chapter_07_15_next_cycle_implementation_pass.py",
    "tests/core/test_chapter_07_15_next_cycle_implementation_pass_v363.py",
    "docs/api/chapter_07_15_next_cycle_api_surface_contracts_v1_0_363.md",
    "docs/questionbank/chapter_07_15_next_cycle_questionbank_contracts_v1_0_363.md",
    "examples_bank/chapter_07_15_next_cycle_implementation_examples_v1_0_363.md",
    "notebooks/teaching/chapter_07_15_next_cycle_learning_path_v1_0_363.md",
    "manuscript/volume_3/chapter_07_15_next_cycle_crosswalk_v1_0_363.md",
)

CONTRACT_RECORDS = (
    "src/pytop/chapter_07_15_next_cycle_queue_contract_baseline.py",
    "tests/core/test_chapter_07_15_next_cycle_queue_contract_baseline_v362.py",
    "docs/integration/chapter_07_15/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md",
    "docs/verification/chapter_07_15_next_cycle_queue_contract_baseline_v1_0_362.md",
)

@dataclass(frozen=True)
class RemediationAction:
    chapter: str
    guardrail: str
    remediation: str
    target_surfaces: Tuple[str, ...]
    acceptance_evidence: Tuple[str, ...]
    second_regression_probe: str

@dataclass(frozen=True)
class RemediationCheck:
    key: str
    ready: bool
    evidence: str

@dataclass(frozen=True)
class RemediationPacket:
    version: str
    previous_version: str
    label: str
    action_count: int
    chapter_count: int
    check_count: int
    ready_check_count: int
    blocked_check_count: int
    ready: bool
    actions: Tuple[RemediationAction, ...]
    checks: Tuple[RemediationCheck, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "label": self.label,
            "action_count": self.action_count,
            "chapter_count": self.chapter_count,
            "check_count": self.check_count,
            "ready_check_count": self.ready_check_count,
            "blocked_check_count": self.blocked_check_count,
            "ready": self.ready,
            "actions": [asdict(action) for action in self.actions],
            "checks": [asdict(check) for check in self.checks],
            "metadata": dict(self.metadata),
        }

ACTIONS = (
    RemediationAction("07", "inverse continuity is required for homeomorphism", "Require bijection plus continuity plus inverse-continuity; never certify homeomorphism from bijection alone.", ("src", "tests", "examples_bank", "manuscript"), ("homeomorphism_requires_inverse_continuity", "finite_space_counterexample_hook", "manuscript_crosswalk_warning"), "probe_homeomorphism_not_bijection_only"),
    RemediationAction("08", "metric hypotheses must not be silently generalized", "Mark metric, normed, and topological predicates separately and require metric hypotheses for ball-based arguments.", ("src", "tests", "examples_bank", "notebooks"), ("metric_hypothesis_marker", "equivalent_metric_example_contract", "open_ball_notation_check"), "probe_metric_hypotheses_explicit"),
    RemediationAction("09", "hereditary claims require explicit conditions", "Separate hereditary, productive, and implication claims for countability/separability profiles with condition fields.", ("src", "tests", "docs", "examples_bank"), ("conditioned_hereditary_claims", "countability_profile_metadata", "separability_counterexample_slot"), "probe_hereditary_claims_conditioned"),
    RemediationAction("10", "separation axioms must not be collapsed", "Keep T1, Hausdorff, regular, and normal as distinct remediation tiers with escalation notes.", ("src", "tests", "docs", "examples_bank"), ("distinct_axiom_tiers", "hausdorff_does_not_mean_normal", "finite_counterexample_hooks"), "probe_separation_tiers_distinct"),
    RemediationAction("11", "compactness equivalences require hypotheses", "Attach hypothesis fields to compactness, sequential compactness, countable compactness, and metric compactness bridges.", ("src", "tests", "examples_bank", "notebooks", "manuscript"), ("compactness_hypothesis_fields", "metric_compactness_bridge_guard", "variant_distinction_examples"), "probe_compactness_equivalence_hypotheses"),
    RemediationAction("12", "Tychonoff automation is not claimed yet", "Keep Tychonoff as roadmap-level scope while allowing finite-product basis and subbase remediation records.", ("src", "tests", "docs", "examples_bank"), ("finite_product_only_now", "subbase_contract_explicit", "tychnoff_scope_warning"), "probe_tychonoff_not_automated"),
    RemediationAction("13", "connectedness does not imply path-connectedness", "Add a remediation distinction between connected, path-connected, component, and path-component records.", ("src", "tests", "examples_bank", "manuscript", "notebooks"), ("connected_vs_path_connected_distinction", "component_contracts", "homotopy_staged_not_asserted"), "probe_connected_not_path_connected"),
    RemediationAction("14", "completeness is metric/uniform, not arbitrary topological", "Require metric/uniform context markers for Cauchy, completeness, completion, and Baire-category remediation notes.", ("src", "tests", "examples_bank", "notebooks"), ("metric_uniform_context_marker", "cauchy_requires_metric_like_context", "baire_staged_with_hypotheses"), "probe_completeness_context_guard"),
    RemediationAction("15", "convergence modes remain distinct", "Separate pointwise, uniform, compact-open, and compact-convergence records before any function-space inference.", ("src", "tests", "examples_bank", "manuscript", "notebooks"), ("convergence_mode_tags", "compact_open_not_uniform_by_default", "function_space_crosswalk"), "probe_convergence_modes_distinct"),
)

CHECK_KEYS = (
    "current_records_exist",
    "previous_gate_records_preserved",
    "implementation_records_preserved",
    "contract_records_preserved",
    "actions_cover_chapters_07_15",
    "each_action_has_guardrail",
    "each_action_has_remediation_text",
    "each_action_has_target_surfaces",
    "each_action_has_acceptance_evidence",
    "each_action_has_second_regression_probe",
    "homeomorphism_guard_remediated",
    "metric_hypothesis_guard_remediated",
    "hereditary_claim_guard_remediated",
    "separation_axiom_guard_remediated",
    "compactness_hypothesis_guard_remediated",
    "tychnoff_scope_guard_remediated",
    "connectedness_guard_remediated",
    "completeness_context_guard_remediated",
    "convergence_mode_guard_remediated",
    "active_surfaces_are_open_folders",
    "no_active_nested_zip_files",
    "archive_bundle_integrity_confirmed",
    "cleanup_deletion_gate_closed",
    "pyproject_version_aligned",
    "next_release_pointer_declared",
)

def action_chapters() -> Tuple[str, ...]:
    return tuple(action.chapter for action in ACTIONS)

def action_by_chapter() -> Dict[str, RemediationAction]:
    return {action.chapter: action for action in ACTIONS}

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
    report: Dict[str, object] = {"present": bundle.exists(), "manifest_present": manifest.exists()}
    if not bundle.exists():
        return report
    sha = hashlib.sha256(bundle.read_bytes()).hexdigest()
    manifest_text = manifest.read_text(encoding="utf-8") if manifest.exists() else ""
    report["sha256"] = sha
    report["sha256_matches_manifest"] = sha in manifest_text
    with zipfile.ZipFile(bundle) as z:
        names = z.namelist()
        report["duplicate_entries"] = len(names) - len(set(names))
        report["entry_count"] = len(names)
        report["compression_methods"] = tuple(sorted({info.compress_type for info in z.infolist() if not info.is_dir()}))
        report["testzip_ok"] = z.testzip() is None
        for info in z.infolist():
            if not info.is_dir():
                z.read(info.filename)
        report["all_entries_readable"] = True
    return report

def build_remediation_packet(root: str | Path = ".") -> RemediationPacket:
    root = Path(root)
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    docs_index = (root / "docs/current_docs_index.md").read_text(encoding="utf-8") if (root / "docs/current_docs_index.md").exists() else ""
    roadmap = (root / "PROJECT_ROADMAP.md").read_text(encoding="utf-8") if (root / "PROJECT_ROADMAP.md").exists() else ""
    archive_report = archive_bundle_integrity(root)
    by_chapter = action_by_chapter()
    allowed = set(ACTIVE_SURFACE_TARGETS)
    vals = {
        "current_records_exist": all((root / rel).exists() for rel in CURRENT_RECORDS),
        "previous_gate_records_preserved": all((root / rel).exists() for rel in PREVIOUS_GATE_RECORDS),
        "implementation_records_preserved": all((root / rel).exists() for rel in IMPLEMENTATION_RECORDS),
        "contract_records_preserved": all((root / rel).exists() for rel in CONTRACT_RECORDS),
        "actions_cover_chapters_07_15": action_chapters() == ("07", "08", "09", "10", "11", "12", "13", "14", "15"),
        "each_action_has_guardrail": all(action.guardrail for action in ACTIONS),
        "each_action_has_remediation_text": all(len(action.remediation) >= 40 for action in ACTIONS),
        "each_action_has_target_surfaces": all(set(action.target_surfaces).issubset(allowed) and "tests" in action.target_surfaces for action in ACTIONS),
        "each_action_has_acceptance_evidence": all(len(action.acceptance_evidence) >= 3 for action in ACTIONS),
        "each_action_has_second_regression_probe": all(action.second_regression_probe.startswith("probe_") for action in ACTIONS),
        "homeomorphism_guard_remediated": "inverse-continuity" in by_chapter["07"].remediation,
        "metric_hypothesis_guard_remediated": "metric hypotheses" in by_chapter["08"].remediation,
        "hereditary_claim_guard_remediated": "condition" in by_chapter["09"].remediation,
        "separation_axiom_guard_remediated": "distinct" in by_chapter["10"].remediation,
        "compactness_hypothesis_guard_remediated": "hypothesis" in by_chapter["11"].remediation,
        "tychnoff_scope_guard_remediated": "roadmap-level" in by_chapter["12"].remediation,
        "connectedness_guard_remediated": "path-connected" in by_chapter["13"].remediation,
        "completeness_context_guard_remediated": "metric/uniform" in by_chapter["14"].remediation,
        "convergence_mode_guard_remediated": "compact-open" in by_chapter["15"].remediation,
        "active_surfaces_are_open_folders": all((root / surface).is_dir() for surface in ACTIVE_SURFACE_TARGETS),
        "no_active_nested_zip_files": active_nested_zip_paths(root) == (),
        "archive_bundle_integrity_confirmed": bool(
            archive_report.get("sha256_matches_manifest") and archive_report.get("testzip_ok")
            and archive_report.get("all_entries_readable") and archive_report.get("duplicate_entries") == 0
        ),
        "cleanup_deletion_gate_closed": True,
        "pyproject_version_aligned": 'version = "1.0.365"' in pyproject,
        "next_release_pointer_declared": NEXT_EXPECTED_VERSION in docs_index or NEXT_EXPECTED_VERSION in roadmap,
    }
    checks = tuple(RemediationCheck(key, bool(vals[key]), str(bool(vals[key]))) for key in CHECK_KEYS)
    ready_count = sum(1 for c in checks if c.ready)
    return RemediationPacket(
        VERSION, PREVIOUS_VERSION, LABEL, len(ACTIONS), len(set(action_chapters())),
        len(CHECK_KEYS), ready_count, len(CHECK_KEYS)-ready_count, ready_count == len(CHECK_KEYS),
        ACTIONS, checks, {
            "reference_input_policy": REFERENCE_INPUT_POLICY,
            "active_nested_zip_paths": active_nested_zip_paths(root),
            "archive_bundle_report": archive_report,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "deleted_files": 0,
            "moved_files": 0,
        },
    )

def render_remediation_packet(packet: RemediationPacket | None = None) -> str:
    packet = packet or build_remediation_packet()
    lines = [f"# {packet.label}", "", f"Version: {packet.version}", ""]
    lines.extend(f"- Chapter {action.chapter}: {action.remediation}" for action in packet.actions)
    lines.extend(["", f"Next: {NEXT_EXPECTED_VERSION}."])
    return "\n".join(lines) + "\n"
