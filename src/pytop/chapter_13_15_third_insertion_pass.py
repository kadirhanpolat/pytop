"""Chapter 13--15 third post-checkpoint insertion pass for v1.0.336.

This module completes the three-pass post-checkpoint insertion sequence that
started with Chapter 07--09 and continued with Chapter 10--12.  It records
active open-folder targets for connectedness, complete metric spaces, and
function spaces.  Uploaded chapter zips and ``docs/archive`` bundles remain
historical/evidence inputs; they are never treated as active project sources.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

THIRD_INSERTION_PASS_VERSION = "v1.0.336"
PREVIOUS_INSERTION_PASS_VERSION = "v1.0.335"
SOURCE_CHECKPOINT_VERSION = "v1.0.333"
INSERTION_PASS_LABEL = "Chapter 13--15 third post-checkpoint insertion pass"
NEXT_EXPECTED_VERSION = "v1.0.337 post-insertion audit and release stabilization"
TARGET_CHAPTERS = (13, 14, 15)
ACTIVE_SURFACES = ("manuscript", "examples_bank", "questionbank")


@dataclass(frozen=True)
class ThirdInsertionTarget:
    surface: str
    path: str
    objective: str
    exists: bool
    open_folder_target: bool


@dataclass(frozen=True)
class ThirdInsertionItem:
    chapter: int
    chapter_label: str
    pass_role: str
    targets: Tuple[ThirdInsertionTarget, ...]
    local_objective: str
    cross_link_objective: str
    originality_guardrail: str
    ready: bool


@dataclass(frozen=True)
class ThirdInsertionReport:
    version: str
    previous_insertion_pass_version: str
    source_checkpoint_version: str
    pass_label: str
    chapter_count: int
    target_count: int
    ready_chapter_count: int
    missing_target_count: int
    all_open_folder_targets: bool
    status: bool
    items: Tuple[ThirdInsertionItem, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_insertion_pass_version": self.previous_insertion_pass_version,
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


def _target(root: Path, surface: str, path: str, objective: str) -> ThirdInsertionTarget:
    return ThirdInsertionTarget(
        surface=surface,
        path=path,
        objective=objective,
        exists=(root / path).exists(),
        open_folder_target=_is_open_folder_target(path),
    )


def default_third_insertion_specs() -> Tuple[Mapping[str, object], ...]:
    """Return the Chapter 13--15 third insertion-pass target specification."""
    return (
        {
            "chapter": 13,
            "label": "Connectedness and path connectedness",
            "pass_role": "stabilize separated-set, clopen, component, and path-component insertion routes",
            "local_objective": "add original connectedness insertion routes and component-level diagnostic prompts",
            "cross_link_objective": "connect continuous-image preservation to compact intervals and IVT-style reading tasks",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/13_connectedness.tex", "connectedness manuscript anchor"),
                ("examples_bank", "examples_bank/connectedness_examples.md", "connectedness examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_13_connectedness_family_draft_v1_0_211.md", "connectedness question-family draft anchor"),
            ),
        },
        {
            "chapter": 14,
            "label": "Complete metric spaces",
            "pass_role": "stabilize Cauchy, completeness, contraction, completion, and Baire forward bridges",
            "local_objective": "add original complete-metric insertion routes and theorem dependency prompts",
            "cross_link_objective": "connect compactness variants to complete/totally bounded criteria and function-space metrics",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/16_sequences_and_convergence.tex", "complete-metric manuscript anchor"),
                ("examples_bank", "examples_bank/complete_metric_examples.md", "complete-metric examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_14_complete_metric_family_draft_v1_0_212.md", "complete-metric question-family draft anchor"),
            ),
        },
        {
            "chapter": 15,
            "label": "Function spaces",
            "pass_role": "stabilize pointwise/uniform convergence, compact-open topology, and Ascoli preview routes",
            "local_objective": "add original function-space insertion routes and topology-selection prompts",
            "cross_link_objective": "connect product topology, sup metrics, compact-open topology, and bounded-functional previews",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/15_metric_spaces.tex", "function-space manuscript anchor"),
                ("examples_bank", "examples_bank/function_space_examples.md", "function-space examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_15_function_spaces_family_draft_v1_0_213.md", "function-spaces question-family draft anchor"),
            ),
        },
    )


def build_chapter_13_15_third_insertion_pass(root: Path) -> ThirdInsertionReport:
    items = []
    for spec in default_third_insertion_specs():
        targets = tuple(
            _target(root, surface, path, objective)
            for surface, path, objective in spec["targets"]
        )
        ready = all(target.exists and target.open_folder_target for target in targets)
        items.append(
            ThirdInsertionItem(
                chapter=int(spec["chapter"]),
                chapter_label=str(spec["label"]),
                pass_role=str(spec["pass_role"]),
                targets=targets,
                local_objective=str(spec["local_objective"]),
                cross_link_objective=str(spec["cross_link_objective"]),
                originality_guardrail=(
                    "Use uploaded Chapter 13--15 zips as evidence only; rewrite every insertion "
                    "as project-native prose, examples, or questionbank contracts without direct copy."
                ),
                ready=ready,
            )
        )

    target_count = sum(len(item.targets) for item in items)
    missing_target_count = sum(
        1 for item in items for target in item.targets if not target.exists
    )
    all_open_folder_targets = all(
        target.open_folder_target for item in items for target in item.targets
    )
    ready_chapter_count = sum(1 for item in items if item.ready)
    status = (
        len(items) == len(TARGET_CHAPTERS)
        and tuple(item.chapter for item in items) == TARGET_CHAPTERS
        and ready_chapter_count == len(TARGET_CHAPTERS)
        and missing_target_count == 0
        and all_open_folder_targets
    )
    return ThirdInsertionReport(
        version=THIRD_INSERTION_PASS_VERSION,
        previous_insertion_pass_version=PREVIOUS_INSERTION_PASS_VERSION,
        source_checkpoint_version=SOURCE_CHECKPOINT_VERSION,
        pass_label=INSERTION_PASS_LABEL,
        chapter_count=len(items),
        target_count=target_count,
        ready_chapter_count=ready_chapter_count,
        missing_target_count=missing_target_count,
        all_open_folder_targets=all_open_folder_targets,
        status=status,
        items=tuple(items),
        metadata={
            "active_surfaces": ACTIVE_SURFACES,
            "target_chapters": TARGET_CHAPTERS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "completed_post_checkpoint_sequence": ("v1.0.334", "v1.0.335", "v1.0.336"),
            "evidence_policy": "uploaded chapter zips and docs/archive bundles are not active sources",
        },
    )


def render_chapter_13_15_third_insertion_pass(report: ThirdInsertionReport) -> str:
    lines = [
        "# Chapter 13--15 Third Post-Checkpoint Insertion Pass (v1.0.336)",
        "",
        "This pass completes the Chapter 07--15 post-checkpoint insertion sequence.",
        "It records active open-folder targets for connectedness, complete metric spaces, and function spaces.",
        "",
        "## Summary",
        f"- Previous insertion pass: `{report.previous_insertion_pass_version}`",
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
        lines.append(
            f"- Chapter {item.chapter:02d} -- {item.chapter_label}: {item.local_objective}."
        )
        lines.append(f"  - Cross-link objective: {item.cross_link_objective}.")
        for target in item.targets:
            state = "ready" if target.exists and target.open_folder_target else "missing-or-blocked"
            lines.append(f"  - `{target.surface}`: `{target.path}` ({state})")
    lines.extend([
        "",
        "## Originality guardrail",
        "No direct copying from uploaded Chapter 13--15 source zips is permitted. Each insertion must be rewritten as project-native manuscript prose, examples-bank material, or questionbank contract content.",
        "",
        "## Next",
        "v1.0.337 post-insertion audit and release stabilization.",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "ACTIVE_SURFACES",
    "INSERTION_PASS_LABEL",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_INSERTION_PASS_VERSION",
    "SOURCE_CHECKPOINT_VERSION",
    "TARGET_CHAPTERS",
    "THIRD_INSERTION_PASS_VERSION",
    "ThirdInsertionItem",
    "ThirdInsertionReport",
    "ThirdInsertionTarget",
    "build_chapter_13_15_third_insertion_pass",
    "default_third_insertion_specs",
    "render_chapter_13_15_third_insertion_pass",
]
