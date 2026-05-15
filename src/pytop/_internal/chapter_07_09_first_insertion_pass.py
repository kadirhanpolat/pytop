"""Chapter 07--09 first post-checkpoint insertion pass for v1.0.334.

This module starts the first concrete insertion pass after the Chapter 07--15
post-consolidation checkpoint. The pass intentionally targets active open-folder
surfaces only: manuscript chapter files, examples_bank files, and questionbank
family-draft documents. Uploaded chapter zips and ``docs/archive`` bundles remain
historical/evidence inputs, not active project sources.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

FIRST_INSERTION_PASS_VERSION = "v1.0.334"
SOURCE_CHECKPOINT_VERSION = "v1.0.333"
INSERTION_PASS_LABEL = "Chapter 07--09 first post-checkpoint insertion pass"
NEXT_EXPECTED_VERSION = "v1.0.335 second post-checkpoint insertion pass"
TARGET_CHAPTERS = (7, 8, 9)
ACTIVE_SURFACES = ("manuscript", "examples_bank", "questionbank")


@dataclass(frozen=True)
class FirstInsertionTarget:
    surface: str
    path: str
    objective: str
    exists: bool
    open_folder_target: bool


@dataclass(frozen=True)
class FirstInsertionItem:
    chapter: int
    chapter_label: str
    pass_role: str
    targets: Tuple[FirstInsertionTarget, ...]
    local_objective: str
    originality_guardrail: str
    ready: bool


@dataclass(frozen=True)
class FirstInsertionReport:
    version: str
    source_checkpoint_version: str
    pass_label: str
    chapter_count: int
    target_count: int
    ready_chapter_count: int
    missing_target_count: int
    all_open_folder_targets: bool
    status: bool
    items: Tuple[FirstInsertionItem, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "source_checkpoint_version": self.source_checkpoint_version,
            "pass_label": self.pass_label,
            "chapter_count": self.chapter_count,
            "target_count": self.target_count,
            "ready_chapter_count": self.ready_chapter_count,
            "missing_target_count": self.missing_target_count,
            "all_open_folder_targets": self.all_open_folder_targets,
            "status": self.status,
            "items": [asdict(item) for item in self.items],
            "metadata": dict(self.metadata),
        }


def _is_open_folder_target(path: str) -> bool:
    normalized = f"/{path}"
    return not path.endswith(".zip") and "/docs/archive/" not in normalized


def _target(root: Path, surface: str, path: str, objective: str) -> FirstInsertionTarget:
    return FirstInsertionTarget(
        surface=surface,
        path=path,
        objective=objective,
        exists=(root / path).exists(),
        open_folder_target=_is_open_folder_target(path),
    )


def default_first_insertion_specs() -> Tuple[Mapping[str, object], ...]:
    """Return the first post-checkpoint insertion-pass target specification.

    The chapter numbers follow the uploaded Chapter 07--15 reference sequence;
    manuscript paths point to the existing project-native volume structure.
    """
    return (
        {
            "chapter": 7,
            "label": "Continuity and homeomorphisms",
            "pass_role": "stabilize continuity examples before later metric/countability links",
            "local_objective": "add original continuity/homeomorphism reading routes and reusable example prompts",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/06_continuity_homeomorphism.tex", "chapter-facing continuity insertion anchor"),
                ("examples_bank", "examples_bank/continuity_map_taxonomy.md", "example bank continuity taxonomy anchor"),
                ("questionbank", "docs/questionbank/chapter_07_continuity_homeomorphism_family_draft_v1_0_205.md", "question family draft anchor"),
            ),
        },
        {
            "chapter": 8,
            "label": "Metric spaces",
            "pass_role": "connect metric intuition to topology without copying external prose",
            "local_objective": "add original metric/open-ball and induced-topology insertion routes",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/15_metric_spaces.tex", "project-native metric-space manuscript anchor"),
                ("examples_bank", "examples_bank/metric_space_examples.md", "metric examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_08_metric_normed_family_draft_v1_0_206.md", "metric/normed question family draft anchor"),
            ),
        },
        {
            "chapter": 9,
            "label": "Countability axioms",
            "pass_role": "align first/second countability examples with tested package reports",
            "local_objective": "add original countability insertion routes and diagnostic cross-links",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/12_countability_axioms.tex", "countability manuscript anchor"),
                ("examples_bank", "examples_bank/countability_examples.md", "countability examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_09_countability_family_draft_v1_0_207.md", "countability question family draft anchor"),
            ),
        },
    )


def build_chapter_07_09_first_insertion_pass(root: str | Path = ".") -> FirstInsertionReport:
    root_path = Path(root)
    items = []
    for spec in default_first_insertion_specs():
        targets = tuple(
            _target(root_path, surface, path, objective)
            for surface, path, objective in spec["targets"]  # type: ignore[index]
        )
        ready = all(target.exists and target.open_folder_target for target in targets)
        items.append(
            FirstInsertionItem(
                chapter=int(spec["chapter"]),
                chapter_label=str(spec["label"]),
                pass_role=str(spec["pass_role"]),
                targets=targets,
                local_objective=str(spec["local_objective"]),
                originality_guardrail=(
                    "Use uploaded Chapter 07--09 material only as comparison/evidence; "
                    "write project-native explanations, examples, and questions instead of copying."
                ),
                ready=ready,
            )
        )
    target_count = sum(len(item.targets) for item in items)
    missing = sum(1 for item in items for target in item.targets if not target.exists)
    all_open = all(target.open_folder_target for item in items for target in item.targets)
    ready_count = sum(1 for item in items if item.ready)
    metadata = {
        "source_checkpoint": SOURCE_CHECKPOINT_VERSION,
        "first_pass_chapters": TARGET_CHAPTERS,
        "active_surfaces": ACTIVE_SURFACES,
        "pass_sequence": {
            "v1.0.334": "Chapter 07--09 first post-checkpoint insertion pass",
            "v1.0.335": "Chapter 10--12 second post-checkpoint insertion pass",
            "v1.0.336": "Chapter 13--15 third post-checkpoint insertion pass",
        },
        "next_expected_version": NEXT_EXPECTED_VERSION,
    }
    return FirstInsertionReport(
        version=FIRST_INSERTION_PASS_VERSION,
        source_checkpoint_version=SOURCE_CHECKPOINT_VERSION,
        pass_label=INSERTION_PASS_LABEL,
        chapter_count=len(items),
        target_count=target_count,
        ready_chapter_count=ready_count,
        missing_target_count=missing,
        all_open_folder_targets=all_open,
        status=(ready_count == len(items) and missing == 0 and all_open),
        items=tuple(items),
        metadata=metadata,
    )


def render_chapter_07_09_first_insertion_pass(report: FirstInsertionReport) -> str:
    lines = [
        f"# Chapter 07--09 First Post-Checkpoint Insertion Pass ({report.version})",
        "",
        "This pass starts the post-checkpoint insertion sequence for Chapter 07--15.",
        "It records active open-folder targets for the first three chapters and keeps uploaded chapter zips as evidence only.",
        "",
        "## Summary",
        f"- Source checkpoint: `{report.source_checkpoint_version}`",
        f"- Chapters: `{report.chapter_count}`",
        f"- Targets: `{report.target_count}`",
        f"- Ready chapters: `{report.ready_chapter_count}`",
        f"- Missing targets: `{report.missing_target_count}`",
        f"- Open-folder targets only: `{report.all_open_folder_targets}`",
        f"- Status: `{report.status}`",
        "",
        "## Chapter targets",
    ]
    for item in report.items:
        lines.append(f"- Chapter {item.chapter:02d} -- {item.chapter_label}: {item.local_objective}.")
        for target in item.targets:
            state = "ready" if target.exists and target.open_folder_target else "missing"
            lines.append(f"  - `{target.surface}`: `{target.path}` ({state})")
    lines.extend([
        "",
        "## Originality guardrail",
        "No direct copying from uploaded Chapter 07--09 source zips is permitted. Each insertion must be rewritten as project-native manuscript prose, example-bank material, or questionbank contract content.",
        "",
        "## Next",
        NEXT_EXPECTED_VERSION + ".",
    ])
    return "\n".join(lines) + "\n"


__all__ = [
    "ACTIVE_SURFACES",
    "FIRST_INSERTION_PASS_VERSION",
    "INSERTION_PASS_LABEL",
    "NEXT_EXPECTED_VERSION",
    "SOURCE_CHECKPOINT_VERSION",
    "TARGET_CHAPTERS",
    "FirstInsertionItem",
    "FirstInsertionReport",
    "FirstInsertionTarget",
    "build_chapter_07_09_first_insertion_pass",
    "default_first_insertion_specs",
    "render_chapter_07_09_first_insertion_pass",
]
