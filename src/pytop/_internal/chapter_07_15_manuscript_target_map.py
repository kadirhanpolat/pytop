"""Chapter 07--15 manuscript integration target-map helpers.

The v1.0.320 target map is a planning and contract surface.  It connects the
v1.0.319 questionbank contract alignment to active manuscript anchors and marks
where chapter-by-chapter integration should start in v1.0.321--v1.0.329.  It
uses active open-folder package paths only; uploaded Chapter 07--15 zip files are
reference inputs, not active nested sources.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .chapter_07_15_questionbank_contract_alignment import (
    ChapterQuestionbankContractRow,
    build_chapter_07_15_questionbank_contract_alignment,
)
from .result import Result

MANUSCRIPT_TARGET_MAP_VERSION = "v1.0.320"


@dataclass(frozen=True, slots=True)
class ChapterManuscriptTargetSpec:
    """Static manuscript-target specification for one Chapter 07--15 row."""

    chapter: int
    manuscript_route: str
    insertion_points: tuple[str, ...]
    teaching_targets: tuple[str, ...]
    originality_guardrails: tuple[str, ...]
    chapter_opening_version: str
    notes: tuple[str, ...] = ()

    @property
    def label(self) -> str:
        return f"Chapter {self.chapter:02d}"


@dataclass(frozen=True, slots=True)
class ChapterManuscriptTargetRow:
    """Resolved manuscript target-map row."""

    spec: ChapterManuscriptTargetSpec
    contract_row: ChapterQuestionbankContractRow
    manuscript_targets: tuple[str, ...]
    present_manuscript_targets: tuple[str, ...]
    missing_manuscript_targets: tuple[str, ...]

    @property
    def chapter(self) -> int:
        return self.spec.chapter

    @property
    def topic(self) -> str:
        return self.contract_row.topic

    @property
    def priority(self) -> str:
        return self.contract_row.priority

    @property
    def chapter_opening_version(self) -> str:
        return self.spec.chapter_opening_version

    @property
    def insertion_points(self) -> tuple[str, ...]:
        return self.spec.insertion_points

    @property
    def teaching_targets(self) -> tuple[str, ...]:
        return self.spec.teaching_targets

    @property
    def originality_guardrails(self) -> tuple[str, ...]:
        return self.spec.originality_guardrails

    @property
    def blocker_count(self) -> int:
        return len(self.missing_manuscript_targets) + self.contract_row.blocker_count

    @property
    def status(self) -> str:
        if self.blocker_count:
            return "blocked"
        if self.contract_row.alignment_status == "aligned":
            return "ready_for_chapter_opening"
        return "mapped"

    @property
    def next_manuscript_actions(self) -> tuple[str, ...]:
        return (
            f"open {self.spec.manuscript_route}",
            f"use `{self.contract_row.questionbank_doc}` as the contract source, not as prose to copy",
            "attach examples_bank references as reusable scenario anchors",
            *self.insertion_points,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "label": self.spec.label,
            "topic": self.topic,
            "status": self.status,
            "priority": self.priority,
            "chapter_opening_version": self.chapter_opening_version,
            "manuscript_route": self.spec.manuscript_route,
            "manuscript_targets": list(self.manuscript_targets),
            "present_manuscript_targets": list(self.present_manuscript_targets),
            "missing_manuscript_targets": list(self.missing_manuscript_targets),
            "questionbank_doc": self.contract_row.questionbank_doc,
            "examples_bank_docs": list(self.contract_row.examples_bank_docs),
            "api_matrix_status": self.contract_row.api_row.status,
            "contract_alignment_status": self.contract_row.alignment_status,
            "insertion_points": list(self.insertion_points),
            "teaching_targets": list(self.teaching_targets),
            "originality_guardrails": list(self.originality_guardrails),
            "notes": list(self.spec.notes),
            "next_manuscript_actions": list(self.next_manuscript_actions),
        }


@dataclass(frozen=True, slots=True)
class ChapterManuscriptTargetMapReport:
    """Aggregate v1.0.320 manuscript target-map report."""

    version: str
    package_root: str
    rows: tuple[ChapterManuscriptTargetRow, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def chapters(self) -> tuple[int, ...]:
        return tuple(row.chapter for row in self.rows)

    @property
    def ready_count(self) -> int:
        return sum(1 for row in self.rows if row.status == "ready_for_chapter_opening")

    @property
    def blocked_count(self) -> int:
        return sum(1 for row in self.rows if row.status == "blocked")

    @property
    def blocker_count(self) -> int:
        return sum(row.blocker_count for row in self.rows)

    @property
    def manuscript_target_count(self) -> int:
        return sum(len(row.manuscript_targets) for row in self.rows)

    @property
    def insertion_point_count(self) -> int:
        return sum(len(row.insertion_points) for row in self.rows)

    @property
    def originality_guardrail_count(self) -> int:
        return sum(len(row.originality_guardrails) for row in self.rows)

    @property
    def status(self) -> str:
        return "true" if self.blocker_count == 0 and self.ready_count == len(self.rows) else "false"

    @property
    def chapter_opening_versions(self) -> dict[int, str]:
        return {row.chapter: row.chapter_opening_version for row in self.rows}

    @property
    def next_actions(self) -> tuple[str, ...]:
        return tuple(
            f"Chapter {row.chapter:02d}: {action}"
            for row in self.rows
            for action in row.next_manuscript_actions
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "package_root": self.package_root,
            "status": self.status,
            "chapters": list(self.chapters),
            "ready_count": self.ready_count,
            "blocked_count": self.blocked_count,
            "blocker_count": self.blocker_count,
            "manuscript_target_count": self.manuscript_target_count,
            "insertion_point_count": self.insertion_point_count,
            "originality_guardrail_count": self.originality_guardrail_count,
            "chapter_opening_versions": {str(k): v for k, v in self.chapter_opening_versions.items()},
            "rows": [row.to_dict() for row in self.rows],
            "next_actions": list(self.next_actions),
            "metadata": dict(self.metadata),
        }

    def to_result(self) -> Result:
        return Result(
            status=self.status,
            mode="manuscript_target_map",
            value=self.to_dict(),
            justification=[
                "Chapter 07--15 manuscript integration target map completed.",
                "Each manuscript target is bound to the v1.0.319 questionbank contract alignment and v1.0.318 API matrix.",
                "The map is a planning surface and keeps originality guardrails explicit.",
            ],
            metadata=self.to_dict(),
        )


def default_chapter_07_15_manuscript_target_specs() -> tuple[ChapterManuscriptTargetSpec, ...]:
    """Return the default v1.0.320 manuscript target-map specifications."""

    common_guardrails = (
        "do not copy prose, examples, or exercises directly from uploaded chapter zips",
        "rewrite examples in the book voice and keep examples_bank as the reusable source",
    )
    return (
        ChapterManuscriptTargetSpec(
            chapter=7,
            manuscript_route="continuity/homeomorphism route anchored in Volume 1 continuity material",
            insertion_points=(
                "add a continuity criteria bridge box",
                "add a homeomorphism invariant transfer warning",
                "add an initial-topology forward pointer",
            ),
            teaching_targets=("preimage-open language", "closed-set language", "invariant transfer"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.321",
            notes=("Chapter 07 topic numbering is external-reference numbering; the active manuscript anchor is Volume 1 Chapter 06.",),
        ),
        ChapterManuscriptTargetSpec(
            chapter=8,
            manuscript_route="metric-space route anchored in Volume 1 metric material",
            insertion_points=(
                "add metric-validation output boxes",
                "separate equivalent-metric and isometry examples",
            ),
            teaching_targets=("metric axioms", "equivalent metrics", "norm-induced metrics"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.322",
        ),
        ChapterManuscriptTargetSpec(
            chapter=9,
            manuscript_route="countability/local-base route anchored in Volume 1 countability material",
            insertion_points=(
                "add local-base diagnostic table",
                "add separability/Lindelof comparison warning",
            ),
            teaching_targets=("first countability", "second countability", "separability", "Lindelof reductions"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.323",
        ),
        ChapterManuscriptTargetSpec(
            chapter=10,
            manuscript_route="separation-axiom route anchored in Volume 1 separation material",
            insertion_points=(
                "add finite negative-witness classification block",
                "add cofinite/co-countable caution line",
            ),
            teaching_targets=("T0/T1/Hausdorff distinctions", "closed-singleton checks", "counterexample routes"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.324",
        ),
        ChapterManuscriptTargetSpec(
            chapter=11,
            manuscript_route="compactness route anchored in Volume 1 compactness material",
            insertion_points=(
                "add FIP/open-cover route comparison",
                "add continuous-image preservation contract box",
            ),
            teaching_targets=("finite subcovers", "FIP", "metric compactness variants"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.325",
        ),
        ChapterManuscriptTargetSpec(
            chapter=12,
            manuscript_route="product and box topology route anchored in Volume 1 product material",
            insertion_points=(
                "add product-versus-box topology distinction",
                "add projection/subbase bridge example",
            ),
            teaching_targets=("product carriers", "box topology", "coordinate convergence", "projection maps"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.326",
        ),
        ChapterManuscriptTargetSpec(
            chapter=13,
            manuscript_route="connectedness route anchored in Volume 1 connectedness material",
            insertion_points=(
                "add clopen-separation diagnostic block",
                "add component/path-connectedness distinction warning",
            ),
            teaching_targets=("connectedness", "components", "path connectedness", "local connectedness"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.327",
        ),
        ChapterManuscriptTargetSpec(
            chapter=14,
            manuscript_route="complete metric route anchored in Volume 1 sequences/completeness material",
            insertion_points=(
                "add Cauchy/completeness status table",
                "add completion and fixed-point forward pointer",
            ),
            teaching_targets=("Cauchy sequences", "complete subspaces", "completion", "Banach fixed-point route"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.328",
        ),
        ChapterManuscriptTargetSpec(
            chapter=15,
            manuscript_route="function-space route anchored in Volume 2 function-space bridge material",
            insertion_points=(
                "add point-open versus compact-open topology comparison",
                "add equicontinuity/Ascoli forward pointer",
                "add finite function-carrier smoke example",
            ),
            teaching_targets=("pointwise convergence", "uniform convergence", "compact-open topology", "function-space metrics"),
            originality_guardrails=common_guardrails,
            chapter_opening_version="v1.0.329",
            notes=("Function-space material is an advanced bridge; keep the first pass as a scaffold, not a full replacement chapter.",),
        ),
    )


def _unique(paths: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            ordered.append(path)
    return tuple(ordered)


def build_chapter_07_15_manuscript_target_map(
    package_root: str | Path,
    *,
    version: str = MANUSCRIPT_TARGET_MAP_VERSION,
    specs: Iterable[ChapterManuscriptTargetSpec] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ChapterManuscriptTargetMapReport:
    """Build the active Chapter 07--15 manuscript target map."""

    root = Path(package_root)
    alignment = build_chapter_07_15_questionbank_contract_alignment(root)
    contract_rows = {row.chapter: row for row in alignment.rows}
    rows: list[ChapterManuscriptTargetRow] = []
    for spec in tuple(specs) if specs is not None else default_chapter_07_15_manuscript_target_specs():
        contract_row = contract_rows[spec.chapter]
        targets = _unique(contract_row.bridge_item.manuscript_targets)
        present = tuple(path for path in targets if (root / path).exists())
        missing = tuple(path for path in targets if path not in present)
        rows.append(
            ChapterManuscriptTargetRow(
                spec=spec,
                contract_row=contract_row,
                manuscript_targets=targets,
                present_manuscript_targets=present,
                missing_manuscript_targets=missing,
            )
        )

    return ChapterManuscriptTargetMapReport(
        version=version,
        package_root=str(root),
        rows=tuple(rows),
        metadata={
            "source_contract_alignment_version": alignment.version,
            "source_api_matrix_version": alignment.metadata.get("source_api_matrix_version", "v1.0.318"),
            "numbering_note": "External Chapter 07--15 topic numbering is mapped to active manuscript anchors; manuscript volume/chapter numbers are not assumed to match one-to-one.",
            **dict(metadata or {}),
        },
    )


def render_chapter_07_15_manuscript_target_map(report: ChapterManuscriptTargetMapReport) -> str:
    """Render the manuscript target map as Markdown."""

    lines = [
        f"# Chapter 07--15 Manuscript Integration Target Map - {report.version}",
        "",
        "This report is generated from active package files only. It connects the",
        "v1.0.319 questionbank contract alignment to manuscript anchors, examples_bank",
        "surfaces, and the v1.0.318 API matrix before chapter-by-chapter integration.",
        "",
        "## Summary",
        "",
        f"- Package root: `{report.package_root}`",
        f"- Ready chapters: `{report.ready_count}`",
        f"- Blocked chapters: `{report.blocked_count}`",
        f"- Blocker count: `{report.blocker_count}`",
        f"- Manuscript target count: `{report.manuscript_target_count}`",
        f"- Insertion point count: `{report.insertion_point_count}`",
        f"- Originality guardrail count: `{report.originality_guardrail_count}`",
        "",
        "## Numbering note",
        "",
        str(report.metadata.get("numbering_note", "")),
        "",
        "## Target matrix",
        "",
        "| Chapter | Topic | Status | Opening version | Manuscript targets | Insertion points | Teaching targets |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in report.rows:
        manuscript_targets = "<br>".join(f"`{path}`" for path in row.manuscript_targets)
        insertion_points = "<br>".join(row.insertion_points)
        teaching_targets = "<br>".join(row.teaching_targets)
        lines.append(
            f"| {row.chapter:02d} | {row.topic} | {row.status} | {row.chapter_opening_version} | "
            f"{manuscript_targets} | {insertion_points} | {teaching_targets} |"
        )

    lines.extend(["", "## Next manuscript actions", ""])
    for action in report.next_actions:
        lines.append(f"- {action}")

    lines.extend(["", "## Guardrails", ""])
    lines.append("- Keep active manuscript, questionbank, examples_bank, code, tests, and notebooks in open folders.")
    lines.append("- Uploaded Chapter 07--15 zips remain reference inputs; avoid direct copying of prose, examples, and exercises.")
    lines.append("- Use this map as the input for v1.0.321 Chapter 07 opening work and the v1.0.321--v1.0.329 chapter track.")
    return "\n".join(lines) + "\n"


def chapter_07_15_manuscript_target_map_summary(package_root: str | Path) -> dict[str, Any]:
    """Return the v1.0.320 manuscript target-map summary."""

    return build_chapter_07_15_manuscript_target_map(package_root).to_dict()
