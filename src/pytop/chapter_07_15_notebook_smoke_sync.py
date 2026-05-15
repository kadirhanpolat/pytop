"""Chapter 07--15 notebook and smoke-demo synchronization for v1.0.332.

The module records which active notebook surfaces and shared smoke notebook should
be used for each Chapter 07--15 insertion queue item. It intentionally stores
paths to open-folder active resources, never nested archive files.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping, Tuple

NOTEBOOK_SMOKE_SYNC_VERSION = "v1.0.332"
NOTEBOOK_SMOKE_SOURCE_QUEUE_VERSION = "v1.0.331"
SHARED_SMOKE_NOTEBOOK = "notebooks/smoke/contract_to_result_rendering_smoke_v1_0_308.ipynb"
ACTIVE_NOTEBOOK_SURFACES = ("teaching", "exploration", "smoke")


@dataclass(frozen=True)
class NotebookSmokeSyncSpec:
    chapter: int
    chapter_label: str
    teaching_notebook: str
    exploration_notebook: str
    smoke_notebook: str
    smoke_goal: str
    depends_on: Tuple[str, ...]
    open_folder_guardrail: str


@dataclass(frozen=True)
class NotebookSmokeSyncItem:
    spec: NotebookSmokeSyncSpec
    teaching_exists: bool
    exploration_exists: bool
    smoke_exists: bool
    ready: bool
    notes: Tuple[str, ...]


@dataclass(frozen=True)
class NotebookSmokeSyncReport:
    version: str
    source_queue_version: str
    chapter_count: int
    ready_count: int
    missing_count: int
    shared_smoke_notebook: str
    all_open_folder_targets: bool
    status: bool
    items: Tuple[NotebookSmokeSyncItem, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "source_queue_version": self.source_queue_version,
            "chapter_count": self.chapter_count,
            "ready_count": self.ready_count,
            "missing_count": self.missing_count,
            "shared_smoke_notebook": self.shared_smoke_notebook,
            "all_open_folder_targets": self.all_open_folder_targets,
            "status": self.status,
            "items": [asdict(item) for item in self.items],
            "metadata": dict(self.metadata),
        }


def _guardrail(chapter: int) -> str:
    return (
        f"Chapter {chapter:02d} notebook/smoke work must point to active open-folder "
        "resources. Uploaded chapter zips and docs/archive bundles remain evidence only."
    )


def default_chapter_07_15_notebook_smoke_specs() -> Tuple[NotebookSmokeSyncSpec, ...]:
    rows = {
        7: (
            "Continuity and homeomorphisms",
            "notebooks/teaching/lesson_03_continuity.ipynb",
            "notebooks/exploration/04_continuity.ipynb",
            "validate continuity/homeomorphism examples from the insertion queue",
        ),
        8: (
            "Metric spaces",
            "notebooks/teaching/lesson_06a_metric_spaces.ipynb",
            "notebooks/exploration/09_countability_and_metric_examples.ipynb",
            "validate metric-space example and report rendering hooks",
        ),
        9: (
            "Countability axioms",
            "notebooks/teaching/lesson_05_countability.ipynb",
            "notebooks/exploration/09_countability_and_metric_examples.ipynb",
            "validate countability report examples and smoke-demo captions",
        ),
        10: (
            "Separation axioms",
            "notebooks/teaching/lesson_04_separation.ipynb",
            "notebooks/counterexamples/t1_not_hausdorff_cocountable.ipynb",
            "validate separation counterexample rendering without copying chapter text",
        ),
        11: (
            "Compactness variants",
            "notebooks/teaching/lesson_06_compactness_connectedness.ipynb",
            "notebooks/exploration/07_compactness.ipynb",
            "validate compactness/variant distinction in smoke examples",
        ),
        12: (
            "Product spaces",
            "notebooks/teaching/lesson_03b_subspaces_products_quotients.ipynb",
            "notebooks/exploration/05_subspaces_products_quotients.ipynb",
            "validate product-space insertion queue examples",
        ),
        13: (
            "Connectedness",
            "notebooks/teaching/lesson_06_compactness_connectedness.ipynb",
            "notebooks/exploration/06_connectedness.ipynb",
            "validate connected/path-connected examples and nonexamples",
        ),
        14: (
            "Complete metric spaces",
            "notebooks/teaching/lesson_06c_sequences_and_completeness.ipynb",
            "notebooks/exploration/09b_sequences_subsequences_completeness.ipynb",
            "validate Cauchy/completeness examples through notebook smoke links",
        ),
        15: (
            "Function spaces",
            "notebooks/teaching/lesson_06a_metric_spaces.ipynb",
            "notebooks/exploration/09c_norms_function_metrics_hilbert_glimpse.ipynb",
            "validate function-metric and compact-open preview examples",
        ),
    }
    return tuple(
        NotebookSmokeSyncSpec(
            chapter=chapter,
            chapter_label=label,
            teaching_notebook=teaching,
            exploration_notebook=exploration,
            smoke_notebook=SHARED_SMOKE_NOTEBOOK,
            smoke_goal=goal,
            depends_on=(NOTEBOOK_SMOKE_SOURCE_QUEUE_VERSION, "notebook_smoke_examples_v1_0_308"),
            open_folder_guardrail=_guardrail(chapter),
        )
        for chapter, (label, teaching, exploration, goal) in rows.items()
    )


def _is_open_folder_target(path: str) -> bool:
    return not path.endswith(".zip") and "/docs/archive/" not in f"/{path}"


def build_chapter_07_15_notebook_smoke_sync(root: str | Path = ".") -> NotebookSmokeSyncReport:
    root_path = Path(root)
    items = []
    for spec in default_chapter_07_15_notebook_smoke_specs():
        teaching_exists = (root_path / spec.teaching_notebook).exists()
        exploration_exists = (root_path / spec.exploration_notebook).exists()
        smoke_exists = (root_path / spec.smoke_notebook).exists()
        ready = teaching_exists and exploration_exists and smoke_exists
        items.append(
            NotebookSmokeSyncItem(
                spec=spec,
                teaching_exists=teaching_exists,
                exploration_exists=exploration_exists,
                smoke_exists=smoke_exists,
                ready=ready,
                notes=(
                    f"teaching={teaching_exists}",
                    f"exploration={exploration_exists}",
                    f"smoke={smoke_exists}",
                    spec.smoke_goal,
                ),
            )
        )
    ready_count = sum(1 for item in items if item.ready)
    missing_count = len(items) - ready_count
    all_open = all(
        _is_open_folder_target(path)
        for spec in (item.spec for item in items)
        for path in (spec.teaching_notebook, spec.exploration_notebook, spec.smoke_notebook)
    )
    metadata = {
        "active_surfaces": ACTIVE_NOTEBOOK_SURFACES,
        "source_queue": {"version": NOTEBOOK_SMOKE_SOURCE_QUEUE_VERSION, "ready_items": 27},
        "next_expected_version": "v1.0.333 post-consolidation release checkpoint",
    }
    return NotebookSmokeSyncReport(
        version=NOTEBOOK_SMOKE_SYNC_VERSION,
        source_queue_version=NOTEBOOK_SMOKE_SOURCE_QUEUE_VERSION,
        chapter_count=len(items),
        ready_count=ready_count,
        missing_count=missing_count,
        shared_smoke_notebook=SHARED_SMOKE_NOTEBOOK,
        all_open_folder_targets=all_open,
        status=(missing_count == 0 and all_open),
        items=tuple(items),
        metadata=metadata,
    )


def render_chapter_07_15_notebook_smoke_sync(report: NotebookSmokeSyncReport) -> str:
    lines = [
        f"# Chapter 07--15 Notebook and Smoke-Demo Synchronization ({report.version})",
        "",
        "This report links the v1.0.331 insertion queue to active notebook and smoke-demo surfaces.",
        "It does not add nested zip dependencies and it does not treat uploaded chapter zips as active sources.",
        "",
        "## Summary",
        f"- Chapters: `{report.chapter_count}`",
        f"- Ready chapters: `{report.ready_count}`",
        f"- Missing chapters: `{report.missing_count}`",
        f"- Shared smoke notebook: `{report.shared_smoke_notebook}`",
        f"- Open-folder targets only: `{report.all_open_folder_targets}`",
        f"- Status: `{report.status}`",
        "",
        "## Chapter notebook links",
    ]
    for item in report.items:
        lines.append(
            f"- Chapter {item.spec.chapter:02d}: teaching `{item.spec.teaching_notebook}`; "
            f"exploration `{item.spec.exploration_notebook}`; smoke `{item.spec.smoke_notebook}`."
        )
    lines += [
        "",
        "## Guardrail",
        "Notebook/smoke synchronization is a routing layer only; mathematical prose, examples, and exercises must remain original project-native content.",
    ]
    return "\n".join(lines)
