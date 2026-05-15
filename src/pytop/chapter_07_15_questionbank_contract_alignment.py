"""Chapter 07--15 questionbank contract-alignment helpers.

The v1.0.319 alignment layer is a contract surface, not a new question
generator. It binds active Chapter 07--15 questionbank drafts to examples_bank
evidence, core/API references, and the v1.0.318 API matrix.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .chapter_07_15_api_matrix import ChapterApiMatrixRow, build_chapter_07_15_api_matrix
from .questionbank_bridge import QuestionbankBridgeItem, questionbank_bridge_report
from .result import Result

CONTRACT_ALIGNMENT_VERSION = "v1.0.319"


@dataclass(frozen=True, slots=True)
class ChapterQuestionbankContractRow:
    """One aligned Chapter 07--15 questionbank contract row."""

    bridge_item: QuestionbankBridgeItem
    api_row: ChapterApiMatrixRow
    present_required_paths: tuple[str, ...]
    missing_required_paths: tuple[str, ...]
    missing_core_references: tuple[str, ...] = ()

    @property
    def chapter(self) -> int:
        return int(self.bridge_item.chapter)

    @property
    def topic(self) -> str:
        return self.bridge_item.topic

    @property
    def questionbank_doc(self) -> str:
        return self.bridge_item.questionbank_doc

    @property
    def examples_bank_docs(self) -> tuple[str, ...]:
        return self.bridge_item.examples_bank_docs

    @property
    def core_references(self) -> tuple[str, ...]:
        return self.bridge_item.core_references

    @property
    def test_contract_tags(self) -> tuple[str, ...]:
        return self.bridge_item.test_contract_tags

    @property
    def planned_api_needs(self) -> tuple[dict[str, str], ...]:
        return tuple(need.to_dict() for need in self.api_row.planned_needs)

    @property
    def blocker_count(self) -> int:
        return len(self.missing_required_paths) + len(self.missing_core_references) + self.api_row.missing_count

    @property
    def priority(self) -> str:
        return self.api_row.priority

    @property
    def alignment_status(self) -> str:
        if self.blocker_count:
            return "blocked"
        if self.test_contract_tags and self.api_row.status == "ready_to_contractize":
            return "aligned"
        return "mapped"

    @property
    def next_contract_actions(self) -> tuple[str, ...]:
        actions = [
            f"make `{self.questionbank_doc}` reference explicit Result/contract outputs",
            "keep examples original and use examples_bank as the active source of reusable scenarios",
        ]
        for need in self.api_row.planned_needs:
            actions.append(f"{need.kind}: {need.description}")
        if self.test_contract_tags:
            actions.append("test tags: " + "; ".join(self.test_contract_tags))
        return tuple(actions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "topic": self.topic,
            "alignment_status": self.alignment_status,
            "priority": self.priority,
            "blocker_count": self.blocker_count,
            "questionbank_doc": self.questionbank_doc,
            "examples_bank_docs": list(self.examples_bank_docs),
            "core_references": list(self.core_references),
            "test_contract_tags": list(self.test_contract_tags),
            "api_matrix_status": self.api_row.status,
            "planned_api_needs": list(self.planned_api_needs),
            "present_required_paths": list(self.present_required_paths),
            "missing_required_paths": list(self.missing_required_paths),
            "missing_core_references": list(self.missing_core_references),
            "next_contract_actions": list(self.next_contract_actions),
        }


@dataclass(frozen=True, slots=True)
class ChapterQuestionbankContractAlignmentReport:
    """Aggregate v1.0.319 questionbank contract-alignment report."""

    version: str
    package_root: str
    rows: tuple[ChapterQuestionbankContractRow, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def chapters(self) -> tuple[int, ...]:
        return tuple(row.chapter for row in self.rows)

    @property
    def aligned_count(self) -> int:
        return sum(1 for row in self.rows if row.alignment_status == "aligned")

    @property
    def mapped_count(self) -> int:
        return sum(1 for row in self.rows if row.alignment_status == "mapped")

    @property
    def blocked_count(self) -> int:
        return sum(1 for row in self.rows if row.alignment_status == "blocked")

    @property
    def blocker_count(self) -> int:
        return sum(row.blocker_count for row in self.rows)

    @property
    def high_priority_row_count(self) -> int:
        return sum(1 for row in self.rows if row.priority == "high")

    @property
    def contract_tag_count(self) -> int:
        return sum(len(row.test_contract_tags) for row in self.rows)

    @property
    def planned_contract_action_count(self) -> int:
        return sum(len(row.next_contract_actions) for row in self.rows)

    @property
    def status(self) -> str:
        return "true" if self.blocker_count == 0 and self.aligned_count == len(self.rows) else "false"

    @property
    def next_actions(self) -> tuple[str, ...]:
        return tuple(
            f"Chapter {row.chapter:02d}: {action}"
            for row in self.rows
            for action in row.next_contract_actions
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "package_root": self.package_root,
            "status": self.status,
            "chapters": list(self.chapters),
            "aligned_count": self.aligned_count,
            "mapped_count": self.mapped_count,
            "blocked_count": self.blocked_count,
            "blocker_count": self.blocker_count,
            "high_priority_row_count": self.high_priority_row_count,
            "contract_tag_count": self.contract_tag_count,
            "planned_contract_action_count": self.planned_contract_action_count,
            "rows": [row.to_dict() for row in self.rows],
            "next_actions": list(self.next_actions),
            "metadata": dict(self.metadata),
        }

    def to_result(self) -> Result:
        return Result(
            status=self.status,
            mode="contract_alignment",
            value=self.to_dict(),
            justification=[
                "Chapter 07--15 questionbank contract alignment completed.",
                "Each active questionbank draft is bound to examples_bank, core/API references, and v1.0.318 API-matrix status.",
                "The alignment is a contract map; it does not copy wording or problems from uploaded reference zips.",
            ],
            metadata=self.to_dict(),
        )


def build_chapter_07_15_questionbank_contract_alignment(
    package_root: str | Path,
    *,
    version: str = CONTRACT_ALIGNMENT_VERSION,
    bridge_items: Iterable[QuestionbankBridgeItem] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ChapterQuestionbankContractAlignmentReport:
    """Build the active Chapter 07--15 questionbank contract alignment."""

    root = Path(package_root)
    bridge_report = questionbank_bridge_report(root)
    selected_items = tuple(bridge_items) if bridge_items is not None else tuple(
        item for item in bridge_report.bridge_items if 7 <= int(item.chapter) <= 15
    )
    api_report = build_chapter_07_15_api_matrix(root)
    api_rows = {row.chapter: row for row in api_report.rows}
    missing_core = set(bridge_report.missing_core_references)

    rows: list[ChapterQuestionbankContractRow] = []
    for item in selected_items:
        chapter = int(item.chapter)
        required = item.required_paths
        present = tuple(path for path in required if (root / path).exists())
        missing = tuple(path for path in required if path not in present)
        item_missing_core = tuple(ref for ref in item.core_references if ref in missing_core)
        rows.append(
            ChapterQuestionbankContractRow(
                bridge_item=item,
                api_row=api_rows[chapter],
                present_required_paths=present,
                missing_required_paths=missing,
                missing_core_references=item_missing_core,
            )
        )

    return ChapterQuestionbankContractAlignmentReport(
        version=version,
        package_root=str(root),
        rows=tuple(rows),
        metadata={
            "source_bridge_version": bridge_report.version,
            "source_api_matrix_version": api_report.version,
            **dict(metadata or {}),
        },
    )


def render_chapter_07_15_questionbank_contract_alignment(report: ChapterQuestionbankContractAlignmentReport) -> str:
    """Render the questionbank contract alignment report as Markdown."""

    lines = [
        f"# Chapter 07--15 Questionbank Contract Alignment - {report.version}",
        "",
        "This report is generated from active package files only. It aligns each",
        "Chapter 07--15 questionbank draft with examples_bank evidence, core/API",
        "references, and the v1.0.318 API matrix.",
        "",
        "## Summary",
        "",
        f"- Package root: `{report.package_root}`",
        f"- Aligned chapters: `{report.aligned_count}`",
        f"- Blocked chapters: `{report.blocked_count}`",
        f"- Blocker count: `{report.blocker_count}`",
        f"- High-priority rows: `{report.high_priority_row_count}`",
        f"- Test contract tags: `{report.contract_tag_count}`",
        f"- Planned contract actions: `{report.planned_contract_action_count}`",
        "",
        "## Alignment matrix",
        "",
        "| Chapter | Topic | Status | Priority | Questionbank draft | Examples bank | Core/API references | Contract tags |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for row in report.rows:
        examples = "<br>".join(f"`{path}`" for path in row.examples_bank_docs)
        core = "<br>".join(f"`{ref}`" for ref in row.core_references)
        tags = "<br>".join(row.test_contract_tags)
        lines.append(
            f"| {row.chapter:02d} | {row.topic} | {row.alignment_status} | {row.priority} | "
            f"`{row.questionbank_doc}` | {examples} | {core} | {tags} |"
        )

    lines.extend(["", "## Next contract actions", ""])
    for action in report.next_actions:
        lines.append(f"- {action}")

    lines.extend(["", "## Guardrails", ""])
    lines.append("- Keep active questionbank material in open folders, not nested active zips.")
    lines.append("- Use uploaded Chapter 07--15 zips only as reference/evidence; do not copy wording or problems directly.")
    lines.append("- Use this alignment as the input for v1.0.320 manuscript target mapping and v1.0.321 Chapter 07 opening work.")
    return "\n".join(lines) + "\n"


def chapter_07_15_questionbank_contract_alignment_summary(package_root: str | Path) -> dict[str, Any]:
    """Return the v1.0.319 questionbank contract-alignment summary."""

    return build_chapter_07_15_questionbank_contract_alignment(package_root).to_dict()
