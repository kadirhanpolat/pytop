"""Chapter 10--12 second post-checkpoint insertion pass for v1.0.335.

This module continues the post-checkpoint insertion sequence after the Chapter
07--09 pass.  It records active open-folder targets for separation axioms,
compactness, and product spaces.  Uploaded chapter zips and ``docs/archive``
bundles remain historical/evidence inputs; this module never treats them as
active project sources.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

SECOND_INSERTION_PASS_VERSION = "v1.0.335"
PREVIOUS_INSERTION_PASS_VERSION = "v1.0.334"
SOURCE_CHECKPOINT_VERSION = "v1.0.333"
INSERTION_PASS_LABEL = "Chapter 10--12 second post-checkpoint insertion pass"
NEXT_EXPECTED_VERSION = "v1.0.336 third post-checkpoint insertion pass"
TARGET_CHAPTERS = (10, 11, 12)
ACTIVE_SURFACES = ("manuscript", "examples_bank", "questionbank")


@dataclass(frozen=True)
class SecondInsertionTarget:
    surface: str
    path: str
    objective: str
    exists: bool
    open_folder_target: bool


@dataclass(frozen=True)
class SecondInsertionItem:
    chapter: int
    chapter_label: str
    pass_role: str
    targets: Tuple[SecondInsertionTarget, ...]
    local_objective: str
    cross_link_objective: str
    originality_guardrail: str
    ready: bool


@dataclass(frozen=True)
class SecondInsertionReport:
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
    items: Tuple[SecondInsertionItem, ...]
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


def _target(root: Path, surface: str, path: str, objective: str) -> SecondInsertionTarget:
    return SecondInsertionTarget(
        surface=surface,
        path=path,
        objective=objective,
        exists=(root / path).exists(),
        open_folder_target=_is_open_folder_target(path),
    )


def default_second_insertion_specs() -> Tuple[Mapping[str, object], ...]:
    """Return the Chapter 10--12 second insertion-pass target specification."""
    return (
        {
            "chapter": 10,
            "label": "Separation axioms",
            "pass_role": "stabilize T0/T1/Hausdorff/regular/normal examples before compactness links",
            "local_objective": "add original separation-axiom insertion routes and finite/cofinite diagnostics",
            "cross_link_objective": "connect separation examples to compact-Hausdorff and product-space preservation notes",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/11_separation_axioms.tex", "separation-axiom manuscript anchor"),
                ("examples_bank", "examples_bank/separation_axioms_examples.md", "separation examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_10_separation_axioms_family_draft_v1_0_208.md", "separation question-family draft anchor"),
            ),
        },
        {
            "chapter": 11,
            "label": "Compactness variants",
            "pass_role": "align open-cover compactness with FIP, continuous images, and metric compactness variants",
            "local_objective": "add original compactness insertion routes and counterexample prompts",
            "cross_link_objective": "connect compactness to separation, total-bounded/complete, and later function-space topics",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/14_compactness.tex", "compactness manuscript anchor"),
                ("examples_bank", "examples_bank/compactness_examples.md", "compactness examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_11_compactness_family_draft_v1_0_209.md", "compactness question-family draft anchor"),
            ),
        },
        {
            "chapter": 12,
            "label": "Product spaces",
            "pass_role": "stabilize box/product topology distinctions and projection-subbase vocabulary",
            "local_objective": "add original product-space insertion routes and coordinatewise convergence prompts",
            "cross_link_objective": "connect product spaces to Tychonoff forward notes and later function-space topologies",
            "targets": (
                ("manuscript", "manuscript/volume_1/chapters/08_products.tex", "product-space manuscript anchor"),
                ("examples_bank", "examples_bank/product_space_examples.md", "product-space examples-bank anchor"),
                ("questionbank", "docs/questionbank/chapter_12_product_spaces_family_draft_v1_0_210.md", "product-spaces question-family draft anchor"),
            ),
        },
    )


def build_chapter_10_12_second_insertion_pass(root: Path) -> SecondInsertionReport:
    items = []
    for spec in default_second_insertion_specs():
        targets = tuple(
            _target(root, surface, path, objective)
            for surface, path, objective in spec["targets"]
        )
        ready = all(target.exists and target.open_folder_target for target in targets)
        items.append(
            SecondInsertionItem(
                chapter=int(spec["chapter"]),
                chapter_label=str(spec["label"]),
                pass_role=str(spec["pass_role"]),
                targets=targets,
                local_objective=str(spec["local_objective"]),
                cross_link_objective=str(spec["cross_link_objective"]),
                originality_guardrail=(
                    "Use uploaded Chapter 10--12 zips as evidence only; rewrite every insertion "
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
    return SecondInsertionReport(
        version=SECOND_INSERTION_PASS_VERSION,
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
            "evidence_policy": "uploaded chapter zips and docs/archive bundles are not active sources",
        },
    )


def render_chapter_10_12_second_insertion_pass(report: SecondInsertionReport) -> str:
    lines = [
        "# Chapter 10--12 Second Post-Checkpoint Insertion Pass (v1.0.335)",
        "",
        "This pass continues the post-checkpoint insertion sequence for Chapter 07--15.",
        "It records active open-folder targets for separation axioms, compactness, and product spaces.",
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
        "No direct copying from uploaded Chapter 10--12 source zips is permitted. Each insertion must be rewritten as project-native manuscript prose, examples-bank material, or questionbank contract content.",
        "",
        "## Next",
        "v1.0.336 third post-checkpoint insertion pass for Chapter 13--15.",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "ACTIVE_SURFACES",
    "INSERTION_PASS_LABEL",
    "NEXT_EXPECTED_VERSION",
    "PREVIOUS_INSERTION_PASS_VERSION",
    "SECOND_INSERTION_PASS_VERSION",
    "SOURCE_CHECKPOINT_VERSION",
    "TARGET_CHAPTERS",
    "SecondInsertionItem",
    "SecondInsertionReport",
    "SecondInsertionTarget",
    "build_chapter_10_12_second_insertion_pass",
    "default_second_insertion_specs",
    "render_chapter_10_12_second_insertion_pass",
]
