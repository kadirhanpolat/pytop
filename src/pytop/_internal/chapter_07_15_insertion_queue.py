"""Chapter 07--15 manuscript/examples/questionbank insertion queue for v1.0.331."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple

INSERTION_QUEUE_VERSION = "v1.0.331"
INSERTION_QUEUE_SOURCE_GATE_VERSION = "v1.0.330"
INSERTION_QUEUE_SOURCE_TARGET_MAP_VERSION = "v1.0.320"
ACTIVE_SURFACES = ("manuscript", "examples_bank", "questionbank")

@dataclass(frozen=True)
class ChapterInsertionSpec:
    chapter: int
    chapter_label: str
    surface: str
    target_path: str
    insertion_action: str
    priority: str
    depends_on: Tuple[str, ...]
    originality_guardrail: str

@dataclass(frozen=True)
class ChapterInsertionQueueItem:
    spec: ChapterInsertionSpec
    target_exists: bool
    status: str
    notes: Tuple[str, ...]

@dataclass(frozen=True)
class ChapterInsertionQueueReport:
    version: str
    source_gate_version: str
    source_target_map_version: str
    item_count: int
    ready_count: int
    missing_count: int
    surface_counts: Dict[str, int]
    high_priority_count: int
    originality_guardrail_count: int
    status: bool
    items: Tuple[ChapterInsertionQueueItem, ...]
    metadata: Mapping[str, object]
    def to_dict(self) -> Dict[str, object]:
        return {"version": self.version, "source_gate_version": self.source_gate_version, "source_target_map_version": self.source_target_map_version, "item_count": self.item_count, "ready_count": self.ready_count, "missing_count": self.missing_count, "surface_counts": dict(self.surface_counts), "high_priority_count": self.high_priority_count, "originality_guardrail_count": self.originality_guardrail_count, "status": self.status, "items": [asdict(item) for item in self.items], "metadata": dict(self.metadata)}

def _guardrail(chapter: int) -> str:
    return f"Use uploaded Chapter {chapter:02d} only as comparison/evidence; do not copy sentences, examples, exercises, proofs, or ordering verbatim. Create project-native manuscript prose, examples, and questionbank contracts."

def default_chapter_07_15_insertion_specs() -> Tuple[ChapterInsertionSpec, ...]:
    data = {
        7: ("Continuity and homeomorphisms", "manuscript/volume_1/chapters/06_continuity_homeomorphism.tex", "examples_bank/continuity_map_taxonomy.md", "docs/questionbank/chapter_07_continuity_homeomorphism_family_draft_v1_0_205.md"),
        8: ("Metric spaces", "manuscript/volume_1/chapters/15_metric_spaces.tex", "examples_bank/metric_space_examples.md", "docs/questionbank/chapter_08_metric_normed_family_draft_v1_0_206.md"),
        9: ("Countability axioms", "manuscript/volume_1/chapters/12_countability_axioms.tex", "examples_bank/countability_examples.md", "docs/questionbank/chapter_09_countability_family_draft_v1_0_207.md"),
        10: ("Separation axioms", "manuscript/volume_1/chapters/11_separation_axioms.tex", "examples_bank/separation_axioms_examples.md", "docs/questionbank/chapter_10_separation_axioms_family_draft_v1_0_208.md"),
        11: ("Compactness variants", "manuscript/volume_1/chapters/14_compactness.tex", "examples_bank/compactness_variants_examples.md", "docs/questionbank/chapter_11_compactness_family_draft_v1_0_209.md"),
        12: ("Product spaces", "manuscript/volume_1/chapters/08_products.tex", "examples_bank/product_space_examples.md", "docs/questionbank/chapter_12_product_spaces_family_draft_v1_0_210.md"),
        13: ("Connectedness", "manuscript/volume_1/chapters/13_connectedness.tex", "examples_bank/connectedness_examples.md", "docs/questionbank/chapter_13_connectedness_family_draft_v1_0_211.md"),
        14: ("Complete metric spaces", "manuscript/volume_1/chapters/16_sequences_and_convergence.tex", "examples_bank/complete_metric_examples.md", "docs/questionbank/chapter_14_complete_metric_family_draft_v1_0_212.md"),
        15: ("Function spaces", "manuscript/volume_1/chapters/15_metric_spaces.tex", "examples_bank/function_space_examples.md", "docs/questionbank/chapter_15_function_spaces_family_draft_v1_0_213.md"),
    }
    specs=[]
    for ch,(label,man,ex,qb) in data.items():
        specs.append(ChapterInsertionSpec(ch,label,"manuscript",man,"insert compact original bridge prose and theorem/proof placement TODOs","high",("v1.0.330 quality gate","v1.0.320 target map"),_guardrail(ch)))
        specs.append(ChapterInsertionSpec(ch,label,"examples_bank",ex,"attach original example-family prompt and nonexample warning","high",("examples_bank preservation policy",),_guardrail(ch)))
        specs.append(ChapterInsertionSpec(ch,label,"questionbank",qb,"turn comparison notes into parameterized question-family contracts","medium",("questionbank contract alignment",),_guardrail(ch)))
    return tuple(specs)

def _surface_counts(items: Iterable[ChapterInsertionQueueItem]) -> Dict[str,int]:
    counts={surface:0 for surface in ACTIVE_SURFACES}
    for item in items:
        counts[item.spec.surface]=counts.get(item.spec.surface,0)+1
    return counts

def build_chapter_07_15_insertion_queue(root: str | Path = ".") -> ChapterInsertionQueueReport:
    root_path=Path(root)
    items=[]
    for spec in default_chapter_07_15_insertion_specs():
        exists=(root_path/spec.target_path).exists()
        items.append(ChapterInsertionQueueItem(spec, exists, "ready" if exists else "missing", (f"surface={spec.surface}", f"priority={spec.priority}", "active open-folder target" if exists else "missing active target")))
    ready=sum(1 for item in items if item.target_exists)
    missing=len(items)-ready
    high=sum(1 for item in items if item.spec.priority=="high")
    guard=sum(1 for item in items if "do not copy" in item.spec.originality_guardrail.lower())
    metadata={"source_quality_gate":{"version":INSERTION_QUEUE_SOURCE_GATE_VERSION,"ready":True,"missing_targets":0}, "source_target_map":{"version":INSERTION_QUEUE_SOURCE_TARGET_MAP_VERSION,"status":True}, "next_expected_version":"v1.0.332 notebook and smoke-demo synchronization"}
    return ChapterInsertionQueueReport(INSERTION_QUEUE_VERSION, INSERTION_QUEUE_SOURCE_GATE_VERSION, INSERTION_QUEUE_SOURCE_TARGET_MAP_VERSION, len(items), ready, missing, _surface_counts(items), high, guard, missing==0, tuple(items), metadata)

def render_chapter_07_15_insertion_queue(report: ChapterInsertionQueueReport) -> str:
    lines=[f"# Chapter 07--15 Manuscript / Examples / Questionbank Insertion Queue ({report.version})", "", "This queue converts the consolidated quality gate into active insertion work. It is not copied chapter prose.", "", "## Summary", f"- Items: `{report.item_count}`", f"- Ready items: `{report.ready_count}`", f"- Missing targets: `{report.missing_count}`", f"- Status: `{report.status}`", "", "## Surface counts"]
    for surface in ACTIVE_SURFACES:
        lines.append(f"- `{surface}`: `{report.surface_counts.get(surface,0)}`")
    lines += ["", "## Queue items"]
    for item in report.items:
        lines.append(f"- Chapter {item.spec.chapter:02d} / `{item.spec.surface}` / `{item.status}`: `{item.spec.target_path}` -- {item.spec.insertion_action}")
    lines += ["", "## Originality guardrail", "Uploaded Chapter 07--15 sources are evidence/comparison material only; no verbatim transfer into active sources."]
    return "\n".join(lines)
