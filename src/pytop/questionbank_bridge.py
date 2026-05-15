"""Questionbank bridge map for the v1.0.306 integration phase.

The bridge maps active questionbank drafts to existing package surfaces. It does
not copy wording from external Chapter 07--15 reference zips. Its purpose is to
make the next integration work testable: every mapped question-family surface
points to examples_bank material and to at least one core contract/result helper.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import Any, Iterable, Mapping

from .result import Result


CoreReference = str


@dataclass(frozen=True, slots=True)
class QuestionbankBridgeItem:
    """One questionbank-to-core bridge row."""

    chapter: str
    topic: str
    questionbank_doc: str
    examples_bank_docs: tuple[str, ...]
    core_references: tuple[CoreReference, ...]
    test_contract_tags: tuple[str, ...]
    manuscript_targets: tuple[str, ...] = ()
    notebook_targets: tuple[str, ...] = ()
    status: str = "mapped"

    @property
    def required_paths(self) -> tuple[str, ...]:
        return (
            self.questionbank_doc,
            *self.examples_bank_docs,
            *self.manuscript_targets,
            *self.notebook_targets,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "topic": self.topic,
            "questionbank_doc": self.questionbank_doc,
            "examples_bank_docs": list(self.examples_bank_docs),
            "core_references": list(self.core_references),
            "test_contract_tags": list(self.test_contract_tags),
            "manuscript_targets": list(self.manuscript_targets),
            "notebook_targets": list(self.notebook_targets),
            "status": self.status,
        }


QUESTIONBANK_BRIDGE_ITEMS: tuple[QuestionbankBridgeItem, ...] = (
    QuestionbankBridgeItem(
        chapter="07",
        topic="continuity and homeomorphism",
        questionbank_doc="docs/questionbank/chapter_07_continuity_homeomorphism_family_draft_v1_0_205.md",
        examples_bank_docs=("examples_bank/continuity_map_taxonomy.md", "examples_bank/construction_bridge_examples.md"),
        core_references=("pytop.result_rendering:render_result", "pytop.predicate_contracts:subset_predicate_contract"),
        test_contract_tags=("preimage-open check", "homeomorphism invariant transfer", "rendered Result explanation"),
        manuscript_targets=("manuscript/volume_1/chapters/06_continuity_homeomorphism.tex",),
    ),
    QuestionbankBridgeItem(
        chapter="08",
        topic="metric and normed examples",
        questionbank_doc="docs/questionbank/chapter_08_metric_normed_family_draft_v1_0_206.md",
        examples_bank_docs=("examples_bank/metric_space_examples.md", "examples_bank/metric_topology_bridge_examples.md"),
        core_references=("pytop.metric_contracts:finite_metric_contract", "pytop.metric_contracts:equivalent_metric_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("metric validation", "equivalent metric comparison", "bounded metric transform"),
        manuscript_targets=("manuscript/volume_1/chapters/15_metric_spaces.tex",),
        notebook_targets=("notebooks/exploration/09_countability_and_metric_examples.ipynb",),
    ),
    QuestionbankBridgeItem(
        chapter="09",
        topic="countability axioms",
        questionbank_doc="docs/questionbank/chapter_09_countability_family_draft_v1_0_207.md",
        examples_bank_docs=("examples_bank/countability_examples.md", "examples_bank/metric_topology_bridge_examples.md"),
        core_references=("pytop.predicate_contracts:symbolic_subset_predicate_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("finite/symbolic predicate status", "assumption-aware explanation"),
        manuscript_targets=("manuscript/volume_1/chapters/12_countability_axioms.tex",),
        notebook_targets=("notebooks/exploration/09_countability_and_metric_examples.ipynb",),
    ),
    QuestionbankBridgeItem(
        chapter="10",
        topic="separation axioms",
        questionbank_doc="docs/questionbank/chapter_10_separation_axioms_family_draft_v1_0_208.md",
        examples_bank_docs=("examples_bank/separation_axioms_examples.md", "examples_bank/standard_spaces.md"),
        core_references=("pytop.predicate_contracts:finite_subset_predicate_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("negative witness classification", "closed singleton check", "separation counterexample route"),
        manuscript_targets=("manuscript/volume_1/chapters/11_separation_axioms.tex",),
    ),
    QuestionbankBridgeItem(
        chapter="11",
        topic="compactness variants",
        questionbank_doc="docs/questionbank/chapter_11_compactness_family_draft_v1_0_209.md",
        examples_bank_docs=("examples_bank/compactness_examples.md", "examples_bank/compactness_variants_examples.md"),
        core_references=("pytop.predicate_contracts:symbolic_subset_predicate_contract", "pytop.metric_contracts:finite_metric_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("open cover finite subcover route", "metric compactness comparison", "conditional theorem rendering"),
        manuscript_targets=("manuscript/volume_1/chapters/14_compactness.tex",),
        notebook_targets=("notebooks/exploration/07_compactness.ipynb",),
    ),
    QuestionbankBridgeItem(
        chapter="12",
        topic="product spaces",
        questionbank_doc="docs/questionbank/chapter_12_product_spaces_family_draft_v1_0_210.md",
        examples_bank_docs=("examples_bank/product_space_examples.md", "examples_bank/construction_bridge_examples.md"),
        core_references=("pytop.construction_contracts:finite_product_contract", "pytop.metric_contracts:finite_product_metric_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("finite product carrier", "product metric contract", "projection/subbase bridge"),
        manuscript_targets=("manuscript/volume_1/chapters/08_products.tex",),
    ),
    QuestionbankBridgeItem(
        chapter="13",
        topic="connectedness and path connectedness",
        questionbank_doc="docs/questionbank/chapter_13_connectedness_family_draft_v1_0_211.md",
        examples_bank_docs=("examples_bank/connectedness_examples.md", "examples_bank/local_properties_examples.md"),
        core_references=("pytop.predicate_contracts:subset_predicate_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("separation by clopen subsets", "image preservation route", "local/global distinction"),
        manuscript_targets=("manuscript/volume_1/chapters/13_connectedness.tex",),
    ),
    QuestionbankBridgeItem(
        chapter="14",
        topic="complete metric spaces",
        questionbank_doc="docs/questionbank/chapter_14_complete_metric_family_draft_v1_0_212.md",
        examples_bank_docs=("examples_bank/complete_metric_examples.md", "examples_bank/convergence_examples.md"),
        core_references=("pytop.metric_contracts:finite_metric_contract", "pytop.result_rendering:render_result"),
        test_contract_tags=("metric contract status", "sequence/Cauchy warning line", "completion-route note"),
        manuscript_targets=("manuscript/volume_1/chapters/16_sequences_and_convergence.tex",),
        notebook_targets=("notebooks/exploration/09b_sequences_subsequences_completeness.ipynb",),
    ),
    QuestionbankBridgeItem(
        chapter="15",
        topic="function spaces",
        questionbank_doc="docs/questionbank/function_space_topology_family_draft_v0_1_83.md",
        examples_bank_docs=("examples_bank/function_space_examples.md",),
        core_references=(
            "pytop.function_spaces:function_space_topology_families",
            "pytop.function_spaces:function_space_topology_selector",
            "pytop.function_spaces:render_function_space_topology_report",
        ),
        test_contract_tags=("pointwise entry lane", "compact-open bridge", "uniform advanced line"),
        manuscript_targets=("manuscript/volume_2/chapters/23a_function_spaces_and_compact_open_topology.tex",),
        notebook_targets=("notebooks/exploration/09c_norms_function_metrics_hilbert_glimpse.ipynb",),
    ),
)


@dataclass(frozen=True, slots=True)
class QuestionbankBridgeReport:
    """Machine-readable v1.0.306 bridge report."""

    version: str
    phase_range: str
    bridge_items: tuple[QuestionbankBridgeItem, ...]
    missing_paths: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    missing_core_references: tuple[CoreReference, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def mapped_chapter_count(self) -> int:
        return len({item.chapter for item in self.bridge_items})

    @property
    def mapped_item_count(self) -> int:
        return len(self.bridge_items)

    @property
    def blocker_count(self) -> int:
        return sum(len(values) for values in self.missing_paths.values()) + len(self.missing_core_references)

    @property
    def status(self) -> str:
        return "true" if self.blocker_count == 0 else "false"

    @property
    def is_ready(self) -> bool:
        return self.status == "true"

    def to_result(self) -> Result:
        metadata = {
            "phase_range": self.phase_range,
            "mapped_chapter_count": self.mapped_chapter_count,
            "mapped_item_count": self.mapped_item_count,
            "blocker_count": self.blocker_count,
            "missing_paths": {chapter: list(paths) for chapter, paths in self.missing_paths.items()},
            "missing_core_references": list(self.missing_core_references),
            "bridge_items": [item.to_dict() for item in self.bridge_items],
        }
        justification = [
            f"Mapped {self.mapped_item_count} questionbank families across {self.mapped_chapter_count} chapters.",
            "Each bridge row connects an active questionbank draft to examples_bank and core contract/rendering surfaces.",
            "External Chapter 07--15 zip wording is not copied into the active package.",
        ]
        justification.extend(self.notes)
        factory = Result.true if self.is_ready else Result.false
        value = f"questionbank bridge {'ready' if self.is_ready else 'has blockers'} at {self.version}"
        return factory(mode="exact", value=value, justification=justification, metadata=metadata)

    def summary_lines(self) -> list[str]:
        lines = [
            f"Questionbank bridge: {self.version}",
            f"phase: {self.phase_range}",
            f"status: {self.status}",
            f"mapped chapters: {self.mapped_chapter_count}",
            f"mapped bridge items: {self.mapped_item_count}",
            f"blockers: {self.blocker_count}",
        ]
        for item in self.bridge_items:
            lines.append(f"- Chapter {item.chapter}: {item.topic} -> {item.questionbank_doc}")
        if self.missing_core_references:
            lines.append("missing core references: " + ", ".join(self.missing_core_references))
        for chapter, paths in self.missing_paths.items():
            lines.append(f"missing paths for chapter {chapter}: " + ", ".join(paths))
        return lines


def default_package_root() -> Path:
    """Return the source-tree package root when available."""
    return Path(__file__).resolve().parents[2]


def _missing_paths(package_root: Path, items: Iterable[QuestionbankBridgeItem]) -> dict[str, tuple[str, ...]]:
    missing: dict[str, tuple[str, ...]] = {}
    for item in items:
        absent = tuple(path for path in item.required_paths if not (package_root / path).exists())
        if absent:
            missing[item.chapter] = absent
    return missing


def _core_reference_exists(reference: CoreReference) -> bool:
    module_name, _, attr = reference.partition(":")
    if not module_name or not attr:
        return False
    try:
        module = import_module(module_name)
    except Exception:
        return False
    return hasattr(module, attr)


def missing_core_references(items: Iterable[QuestionbankBridgeItem]) -> tuple[CoreReference, ...]:
    """Return missing ``module:attribute`` references for bridge rows."""
    refs = tuple(dict.fromkeys(ref for item in items for ref in item.core_references))
    return tuple(ref for ref in refs if not _core_reference_exists(ref))


def questionbank_bridge_report(package_root: str | Path | None = None) -> QuestionbankBridgeReport:
    """Build the v1.0.306 questionbank bridge report."""
    root = Path(package_root) if package_root is not None else default_package_root()
    items = QUESTIONBANK_BRIDGE_ITEMS
    return QuestionbankBridgeReport(
        version="v1.0.306",
        phase_range="v1.0.306-v1.0.310",
        bridge_items=items,
        missing_paths=_missing_paths(root, items),
        missing_core_references=missing_core_references(items),
        notes=(
            "This is a bridge map, not a new independent questionbank subproject.",
            "Question family content remains in open-folder docs/questionbank and examples_bank surfaces.",
        ),
    )


def questionbank_bridge_summary(package_root: str | Path | None = None) -> str:
    """Return a compact human-readable bridge summary."""
    return "\n".join(questionbank_bridge_report(package_root).summary_lines())


def bridge_items_by_chapter() -> dict[str, QuestionbankBridgeItem]:
    """Return bridge items keyed by chapter number."""
    return {item.chapter: item for item in QUESTIONBANK_BRIDGE_ITEMS}


def bridge_contract_tags() -> dict[str, tuple[str, ...]]:
    """Return test-contract tags keyed by chapter number."""
    return {item.chapter: item.test_contract_tags for item in QUESTIONBANK_BRIDGE_ITEMS}
