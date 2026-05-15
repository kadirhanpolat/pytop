"""Chapter 07--15 cross-chapter consolidation and quality gate - v1.0.330.

This module consolidates the Chapter 07--15 opening track after the individual
chapter bridges were introduced in v1.0.321--v1.0.329.  The gate is intentionally
diagnostic: it checks that the active package contains the expected code, test,
integration, verification, manuscript, examples-bank, questionbank, and notebook
surfaces for the cross-chapter chain.

Originality guardrails
----------------------
The uploaded Chapter 07--15 zips are treated as reference-only material.  This
quality gate records standard topology dependencies and active package targets;
it does not copy external prose, proof text, examples, exercises, or diagrams.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, List

from pytop.result import Result

CHAPTER_07_15_GATE_VERSION: str = "v1.0.330"

CHAPTER_07_15_MODULE_TARGETS: List[str] = [
    "src/pytop/chapter_07_continuity_integration.py",
    "src/pytop/chapter_08_metric_integration.py",
    "src/pytop/chapter_09_countability_integration.py",
    "src/pytop/chapter_10_separation_axioms_integration.py",
    "src/pytop/chapter_11_compactness_integration.py",
    "src/pytop/chapter_12_product_spaces_integration.py",
    "src/pytop/chapter_13_connectedness_integration.py",
    "src/pytop/chapter_14_complete_metric_integration.py",
    "src/pytop/chapter_15_function_spaces_integration.py",
    "src/pytop/chapter_07_15_cross_chapter_quality_gate.py",
]

CHAPTER_07_15_TEST_TARGETS: List[str] = [
    "tests/core/test_chapter_07_continuity_integration_v321.py",
    "tests/core/test_chapter_08_metric_integration_v322.py",
    "tests/core/test_chapter_09_countability_integration_v323.py",
    "tests/core/test_chapter_10_separation_axioms_integration_v324.py",
    "tests/core/test_chapter_11_compactness_integration_v325.py",
    "tests/core/test_chapter_12_product_spaces_integration_v326.py",
    "tests/core/test_chapter_13_connectedness_integration_v327.py",
    "tests/core/test_chapter_14_complete_metric_integration_v328.py",
    "tests/core/test_chapter_15_function_spaces_integration_v329.py",
    "tests/core/test_chapter_07_15_cross_chapter_quality_gate_v330.py",
]

CHAPTER_07_15_DOC_TARGETS: List[str] = [
    "docs/integration/chapter_07_15/chapter_07_continuity_integration_v1_0_321.md",
    "docs/integration/chapter_07_15/chapter_08_metric_integration_v1_0_322.md",
    "docs/integration/chapter_07_15/chapter_09_countability_integration_v1_0_323.md",
    "docs/integration/chapter_07_15/chapter_10_separation_axioms_integration_v1_0_324.md",
    "docs/integration/chapter_07_15/chapter_11_compactness_integration_v1_0_325.md",
    "docs/integration/chapter_07_15/chapter_12_product_spaces_integration_v1_0_326.md",
    "docs/integration/chapter_07_15/chapter_13_connectedness_integration_v1_0_327.md",
    "docs/integration/chapter_07_15/chapter_14_complete_metric_integration_v1_0_328.md",
    "docs/integration/chapter_07_15/chapter_15_function_spaces_integration_v1_0_329.md",
    "docs/integration/chapter_07_15/chapter_07_15_cross_chapter_consolidation_v1_0_330.md",
    "docs/verification/chapter_07_15_cross_chapter_quality_gate_v1_0_330.md",
]

CHAPTER_07_15_SURFACE_TARGETS: List[str] = [
    "examples_bank/function_space_examples.md",
    "examples_bank/quotient_space_examples.md",
    "examples_bank/convergence_examples.md",
    "examples_bank/local_properties_examples.md",
    "examples_bank/compactness_variants_examples.md",
    "examples_bank/metric_topology_bridge_examples.md",
    "docs/questionbank/chapter_07_continuity_homeomorphism_family_draft_v1_0_205.md",
    "docs/questionbank/chapter_08_metric_normed_family_draft_v1_0_206.md",
    "docs/questionbank/chapter_09_countability_family_draft_v1_0_207.md",
    "docs/questionbank/chapter_10_separation_axioms_family_draft_v1_0_208.md",
    "docs/questionbank/chapter_11_compactness_family_draft_v1_0_209.md",
    "docs/questionbank/chapter_12_product_spaces_family_draft_v1_0_210.md",
    "docs/questionbank/chapter_13_connectedness_family_draft_v1_0_211.md",
    "docs/questionbank/chapter_15_function_spaces_family_draft_v1_0_213.md",
    "notebooks/smoke/contract_to_result_rendering_smoke_v1_0_308.ipynb",
    "manuscript/volume_1/worksheets/07a_norms_function_metrics_forward_look.md",
    "manuscript/volume_1/quick_checks/07a_norms_function_metrics_forward_look.tex",
]

CHAPTER_07_15_ALL_TARGETS: List[str] = (
    CHAPTER_07_15_MODULE_TARGETS
    + CHAPTER_07_15_TEST_TARGETS
    + CHAPTER_07_15_DOC_TARGETS
    + CHAPTER_07_15_SURFACE_TARGETS
)


@dataclass(frozen=True)
class ChapterBridgeRecord:
    """One chapter-level bridge in the Chapter 07--15 chain."""

    chapter: str
    topic: str
    version: str
    module_path: str
    integration_doc: str
    dependency_from_previous: str
    handoff_to_next: str
    quality_question: str


@dataclass(frozen=True)
class CrossChapterConsistencyRule:
    """A consistency rule that must be kept visible across Chapters 07--15."""

    id: str
    scope: str
    rule: str
    risk_if_missing: str
    active_surface: str


@dataclass(frozen=True)
class CrossChapterQualityGate:
    """Computed readiness snapshot for the Chapter 07--15 consolidation gate."""

    version: str
    bridge_count: int
    rule_count: int
    module_targets: int
    test_targets: int
    doc_targets: int
    surface_targets: int
    missing_targets: List[str]
    originality_guardrail: str

    @property
    def blocker_count(self) -> int:
        return len(self.missing_targets)

    @property
    def ready(self) -> bool:
        return self.blocker_count == 0 and self.bridge_count == 9 and self.rule_count >= 8

    def to_result(self) -> Result:
        return Result(
            status="true" if self.ready else "conditional",
            mode="mixed",
            value={
                "version": self.version,
                "ready": self.ready,
                "bridge_count": self.bridge_count,
                "rule_count": self.rule_count,
                "missing_targets": list(self.missing_targets),
                "blocker_count": self.blocker_count,
            },
            assumptions=(
                "Chapter 07--15 uploaded zips are reference-only.",
                "Active package surfaces remain open folders in one full package.",
                "The historical archive bundle under docs/archive is not an active source.",
            ),
        )


def build_chapter_07_15_bridge_records() -> List[ChapterBridgeRecord]:
    """Return the nine chapter bridges opened in v1.0.321--v1.0.329."""
    return [
        ChapterBridgeRecord(
            chapter="07",
            topic="continuity and homeomorphism",
            version="v1.0.321",
            module_path="src/pytop/chapter_07_continuity_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_07_continuity_integration_v1_0_321.md",
            dependency_from_previous="basis/subbasis and open-set language from Chapters 05--06",
            handoff_to_next="metric continuity, metric examples, and normed-space diagnostics",
            quality_question="Are open-set, inverse-image, sequential, and homeomorphism readings separated?",
        ),
        ChapterBridgeRecord(
            chapter="08",
            topic="metric and normed examples",
            version="v1.0.322",
            module_path="src/pytop/chapter_08_metric_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_08_metric_integration_v1_0_322.md",
            dependency_from_previous="continuity bridge and metric-induced topology language",
            handoff_to_next="first/second countability and local base diagnostics",
            quality_question="Are metric topology, norm topology, and finite/real examples distinguished?",
        ),
        ChapterBridgeRecord(
            chapter="09",
            topic="countability axioms",
            version="v1.0.323",
            module_path="src/pytop/chapter_09_countability_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_09_countability_integration_v1_0_323.md",
            dependency_from_previous="basis and metric local-base constructions",
            handoff_to_next="separation axioms and countability-sensitive examples",
            quality_question="Are first countability, second countability, Lindelof-style, and separability claims kept distinct?",
        ),
        ChapterBridgeRecord(
            chapter="10",
            topic="separation axioms",
            version="v1.0.324",
            module_path="src/pytop/chapter_10_separation_axioms_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_10_separation_axioms_integration_v1_0_324.md",
            dependency_from_previous="countability and neighborhood language",
            handoff_to_next="compactness in Hausdorff and non-Hausdorff contexts",
            quality_question="Are T0/T1/T2/regular/normal distinctions represented without collapsing them?",
        ),
        ChapterBridgeRecord(
            chapter="11",
            topic="compactness variants",
            version="v1.0.325",
            module_path="src/pytop/chapter_11_compactness_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_11_compactness_integration_v1_0_325.md",
            dependency_from_previous="open covers, separation assumptions, and countability variants",
            handoff_to_next="product compactness and projection/product arguments",
            quality_question="Are compact, sequentially compact, countably compact, and Lindelof-type readings separated?",
        ),
        ChapterBridgeRecord(
            chapter="12",
            topic="product spaces",
            version="v1.0.326",
            module_path="src/pytop/chapter_12_product_spaces_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_12_product_spaces_integration_v1_0_326.md",
            dependency_from_previous="compactness and finite/infinite product cautions",
            handoff_to_next="connectedness preservation and coordinatewise arguments",
            quality_question="Are product topology, box topology, projection subbases, and coordinate convergence separated?",
        ),
        ChapterBridgeRecord(
            chapter="13",
            topic="connectedness and path connectedness",
            version="v1.0.327",
            module_path="src/pytop/chapter_13_connectedness_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_13_connectedness_integration_v1_0_327.md",
            dependency_from_previous="product and continuous-image preservation tools",
            handoff_to_next="complete metric examples, fixed-point forward pointers, and Baire reading",
            quality_question="Are connectedness, path connectedness, local connectedness, and components distinguished?",
        ),
        ChapterBridgeRecord(
            chapter="14",
            topic="complete metric spaces",
            version="v1.0.328",
            module_path="src/pytop/chapter_14_complete_metric_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_14_complete_metric_integration_v1_0_328.md",
            dependency_from_previous="metric, compactness, and connectedness examples",
            handoff_to_next="function-space sup metrics, compact convergence, and completeness of C[0,1]",
            quality_question="Are Cauchy, complete, totally bounded, compact, completion, and fixed-point claims separated?",
        ),
        ChapterBridgeRecord(
            chapter="15",
            topic="function spaces",
            version="v1.0.329",
            module_path="src/pytop/chapter_15_function_spaces_integration.py",
            integration_doc="docs/integration/chapter_07_15/chapter_15_function_spaces_integration_v1_0_329.md",
            dependency_from_previous="complete metric and compact convergence examples",
            handoff_to_next="post-opening consolidation, manuscript insertion planning, and cross-surface QA",
            quality_question="Are pointwise, uniform, compact-open, equicontinuity, and functional readings separated?",
        ),
    ]


def build_cross_chapter_consistency_rules() -> List[CrossChapterConsistencyRule]:
    """Return the consolidation rules used by the v1.0.330 quality gate."""
    return [
        CrossChapterConsistencyRule(
            id="continuous_image_chain",
            scope="Chapters 07, 11, 13",
            rule="Continuous images preserve selected properties only under the correct hypotheses.",
            risk_if_missing="The manuscript may overgeneralize compactness or connectedness transfer statements.",
            active_surface="docs/integration/chapter_07_15/",
        ),
        CrossChapterConsistencyRule(
            id="metric_vs_topological_language",
            scope="Chapters 07, 08, 14, 15",
            rule="Metric statements must be translated to open-set/topological statements before reuse outside metric spaces.",
            risk_if_missing="Metric-only arguments may be presented as general-topology arguments.",
            active_surface="examples_bank/metric_topology_bridge_examples.md",
        ),
        CrossChapterConsistencyRule(
            id="countability_separation_interaction",
            scope="Chapters 09, 10",
            rule="Countability axioms and separation axioms are independent axes unless a theorem explicitly links them.",
            risk_if_missing="Examples may incorrectly suggest that countability implies Hausdorff-type separation or conversely.",
            active_surface="docs/questionbank/",
        ),
        CrossChapterConsistencyRule(
            id="compactness_variant_names",
            scope="Chapter 11 with Chapters 09 and 14",
            rule="Compact, countably compact, sequentially compact, Lindelof, totally bounded, and complete must keep distinct diagnostics.",
            risk_if_missing="Question families may collapse non-equivalent compactness variants.",
            active_surface="examples_bank/compactness_variants_examples.md",
        ),
        CrossChapterConsistencyRule(
            id="product_box_warning",
            scope="Chapter 12 with Chapters 07, 11, 13, 15",
            rule="Product topology and box topology must not be interchanged in preservation or convergence statements.",
            risk_if_missing="Coordinatewise convergence and function-space product readings may become misleading.",
            active_surface="docs/integration/chapter_07_15/chapter_12_product_spaces_integration_v1_0_326.md",
        ),
        CrossChapterConsistencyRule(
            id="connected_path_connected_local_connected",
            scope="Chapter 13 with Chapters 07 and 12",
            rule="Connectedness, path connectedness, local connectedness, and component decompositions require separate witnesses.",
            risk_if_missing="Problem generators may accept path arguments for merely connected spaces.",
            active_surface="docs/integration/chapter_07_15/chapter_13_connectedness_integration_v1_0_327.md",
        ),
        CrossChapterConsistencyRule(
            id="complete_not_compact",
            scope="Chapter 14 with Chapters 08 and 11",
            rule="Completeness and compactness must be connected through additional hypotheses such as total boundedness when appropriate.",
            risk_if_missing="Complete metric examples may be falsely reported as compact.",
            active_surface="docs/integration/chapter_07_15/chapter_14_complete_metric_integration_v1_0_328.md",
        ),
        CrossChapterConsistencyRule(
            id="function_space_convergence_modes",
            scope="Chapter 15 with Chapters 07, 12, 14",
            rule="Pointwise, uniform, compact convergence, sup-metric topology, and compact-open topology must keep separate quantifier patterns.",
            risk_if_missing="Function-space exercises may silently replace one topology by another.",
            active_surface="docs/integration/chapter_07_15/chapter_15_function_spaces_integration_v1_0_329.md",
        ),
        CrossChapterConsistencyRule(
            id="originality_and_reference_only_policy",
            scope="All Chapter 07--15 integrations",
            rule="Uploaded chapter zips are reference-only; active prose, examples, tests, and docs must be original package material.",
            risk_if_missing="The ecosystem may drift into copied external examples or wording.",
            active_surface="docs/packaging/subproject_packaging_policy_v1_0_330.md",
        ),
    ]


def _missing_targets(package_root: str | Path | None, targets: Iterable[str]) -> List[str]:
    if package_root is None:
        return []
    root = Path(package_root)
    return [target for target in targets if not (root / target).exists()]


def build_chapter_07_15_quality_gate(package_root: str | Path | None = None) -> CrossChapterQualityGate:
    """Build the Chapter 07--15 cross-chapter quality-gate snapshot."""
    bridges = build_chapter_07_15_bridge_records()
    rules = build_cross_chapter_consistency_rules()
    return CrossChapterQualityGate(
        version=CHAPTER_07_15_GATE_VERSION,
        bridge_count=len(bridges),
        rule_count=len(rules),
        module_targets=len(CHAPTER_07_15_MODULE_TARGETS),
        test_targets=len(CHAPTER_07_15_TEST_TARGETS),
        doc_targets=len(CHAPTER_07_15_DOC_TARGETS),
        surface_targets=len(CHAPTER_07_15_SURFACE_TARGETS),
        missing_targets=_missing_targets(package_root, CHAPTER_07_15_ALL_TARGETS),
        originality_guardrail=(
            "Chapter 07--15 uploaded zips remain reference-only.  The consolidation "
            "gate records active-package dependencies and does not copy external "
            "prose, exercises, proof text, examples, or diagrams."
        ),
    )


def chapter_07_15_consolidation_summary(package_root: str | Path | None = None) -> dict[str, Any]:
    gate = build_chapter_07_15_quality_gate(package_root)
    return {
        "version": gate.version,
        "topic": "Chapter 07--15 cross-chapter consolidation",
        "ready": gate.ready,
        "bridge_count": gate.bridge_count,
        "rule_count": gate.rule_count,
        "target_count": (
            gate.module_targets + gate.test_targets + gate.doc_targets + gate.surface_targets
        ),
        "blocker_count": gate.blocker_count,
        "next": "v1.0.331: convert the consolidated Chapter 07--15 gate into a manuscript/examples/questionbank insertion queue",
    }


def render_chapter_07_15_quality_gate_report(package_root: str | Path | None = None) -> str:
    """Render a markdown report for the v1.0.330 cross-chapter quality gate."""
    gate = build_chapter_07_15_quality_gate(package_root)
    lines: list[str] = [
        "# Chapter 07--15 Cross-Chapter Quality Gate - v1.0.330",
        "",
        "## Consolidated chapter bridges",
    ]
    for row in build_chapter_07_15_bridge_records():
        lines.append(
            f"- Chapter {row.chapter} `{row.topic}` ({row.version}): "
            f"from {row.dependency_from_previous}; next={row.handoff_to_next}; "
            f"gate={row.quality_question}"
        )
    lines.extend(["", "## Cross-chapter consistency rules"])
    for rule in build_cross_chapter_consistency_rules():
        lines.append(f"- `{rule.id}` ({rule.scope}): {rule.rule} Risk: {rule.risk_if_missing}")
    lines.extend(
        [
            "",
            "## Gate counts",
            f"- Version: `{gate.version}`",
            f"- Bridge count: `{gate.bridge_count}`",
            f"- Rule count: `{gate.rule_count}`",
            f"- Module targets: `{gate.module_targets}`",
            f"- Test targets: `{gate.test_targets}`",
            f"- Documentation targets: `{gate.doc_targets}`",
            f"- Surface targets: `{gate.surface_targets}`",
            f"- Missing targets: `{gate.blocker_count}`",
            f"- Ready: `{gate.ready}`",
            "",
            "## Originality guardrail",
            gate.originality_guardrail,
        ]
    )
    if gate.missing_targets:
        lines.extend(["", "## Missing targets"])
        lines.extend(f"- `{target}`" for target in gate.missing_targets)
    return "\n".join(lines) + "\n"


def chapter_07_15_gate_payload(package_root: str | Path | None = None) -> dict[str, Any]:
    """Return a serializable payload useful for docs and release reports."""
    gate = build_chapter_07_15_quality_gate(package_root)
    return {
        "gate": asdict(gate),
        "bridges": [asdict(row) for row in build_chapter_07_15_bridge_records()],
        "rules": [asdict(row) for row in build_cross_chapter_consistency_rules()],
    }
