"""Manuscript integration checklist for the v1.0.307 bridge pass.

This module consumes the v1.0.306 questionbank bridge map and checks whether
each Chapter 07--15 row has an active manuscript target. It deliberately stays
as a traceability/checklist layer: it does not copy wording from external
chapter reference zips and it does not create an independent subproject.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .questionbank_bridge import QUESTIONBANK_BRIDGE_ITEMS, QuestionbankBridgeItem
from .result import Result


@dataclass(frozen=True, slots=True)
class ManuscriptIntegrationItem:
    """One manuscript-facing integration checklist row."""

    chapter: str
    topic: str
    questionbank_doc: str
    manuscript_targets: tuple[str, ...]
    examples_bank_docs: tuple[str, ...]
    core_references: tuple[str, ...]
    notebook_targets: tuple[str, ...] = ()
    status: str = "ready_for_manuscript_pass"
    notes: tuple[str, ...] = ()

    @classmethod
    def from_bridge_item(cls, item: QuestionbankBridgeItem) -> "ManuscriptIntegrationItem":
        notes: tuple[str, ...]
        if item.manuscript_targets:
            notes = ("active manuscript target declared by the bridge map",)
        else:
            notes = ("bridge row has no manuscript target and needs editorial assignment",)
        return cls(
            chapter=item.chapter,
            topic=item.topic,
            questionbank_doc=item.questionbank_doc,
            manuscript_targets=tuple(item.manuscript_targets),
            examples_bank_docs=tuple(item.examples_bank_docs),
            core_references=tuple(item.core_references),
            notebook_targets=tuple(item.notebook_targets),
            status="ready_for_manuscript_pass" if item.manuscript_targets else "needs_target_assignment",
            notes=notes,
        )

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
            "manuscript_targets": list(self.manuscript_targets),
            "examples_bank_docs": list(self.examples_bank_docs),
            "core_references": list(self.core_references),
            "notebook_targets": list(self.notebook_targets),
            "status": self.status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ManuscriptIntegrationReport:
    """Aggregate manuscript integration status for Chapter 07--15."""

    version: str
    phase_range: str
    items: tuple[ManuscriptIntegrationItem, ...]
    missing_paths: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def chapter_count(self) -> int:
        return len({item.chapter for item in self.items})

    @property
    def mapped_item_count(self) -> int:
        return len(self.items)

    @property
    def target_count(self) -> int:
        return sum(len(item.manuscript_targets) for item in self.items)

    @property
    def chapters_needing_assignment(self) -> tuple[str, ...]:
        return tuple(item.chapter for item in self.items if not item.manuscript_targets)

    @property
    def blocker_count(self) -> int:
        return len(self.chapters_needing_assignment) + sum(len(v) for v in self.missing_paths.values())

    @property
    def status(self) -> str:
        return "true" if self.blocker_count == 0 else "conditional"

    @property
    def is_ready(self) -> bool:
        return self.blocker_count == 0

    def to_result(self) -> Result:
        if self.is_ready:
            return Result.true(
                mode="exact",
                value="manuscript integration checklist ready",
                assumptions=(
                    "Chapter 07--15 external zips are reference inputs only",
                    "bridge wording is not copied into manuscript files",
                    "active manuscript targets remain open-folder TeX sources",
                ),
                justification=(
                    f"{self.mapped_item_count} bridge rows have manuscript targets.",
                    f"{self.target_count} manuscript target references were checked.",
                ),
                metadata={
                    "version": self.version,
                    "phase_range": self.phase_range,
                    "mapped_item_count": self.mapped_item_count,
                    "chapter_count": self.chapter_count,
                    "target_count": self.target_count,
                    "blocker_count": 0,
                },
            )
        return Result.conditional(
            mode="mixed",
            value="manuscript integration checklist has blockers",
            assumptions=("missing paths or target assignments must be resolved before writing pass",),
            justification=(
                f"chapters_needing_assignment={list(self.chapters_needing_assignment)}",
                f"missing_path_groups={len(self.missing_paths)}",
            ),
            metadata={
                "version": self.version,
                "phase_range": self.phase_range,
                "mapped_item_count": self.mapped_item_count,
                "chapter_count": self.chapter_count,
                "target_count": self.target_count,
                "blocker_count": self.blocker_count,
                "missing_paths": {k: list(v) for k, v in self.missing_paths.items()},
            },
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "phase_range": self.phase_range,
            "status": self.status,
            "is_ready": self.is_ready,
            "chapter_count": self.chapter_count,
            "mapped_item_count": self.mapped_item_count,
            "target_count": self.target_count,
            "chapters_needing_assignment": list(self.chapters_needing_assignment),
            "missing_paths": {k: list(v) for k, v in self.missing_paths.items()},
            "items": [item.to_dict() for item in self.items],
        }


def manuscript_integration_items() -> tuple[ManuscriptIntegrationItem, ...]:
    """Return checklist rows derived from the active questionbank bridge map."""

    return tuple(ManuscriptIntegrationItem.from_bridge_item(item) for item in QUESTIONBANK_BRIDGE_ITEMS)


def missing_manuscript_integration_paths(package_root: str | Path | None = None) -> dict[str, tuple[str, ...]]:
    """Return required active paths that are missing from the package root."""

    if package_root is None:
        return {}
    root = Path(package_root)
    missing: dict[str, tuple[str, ...]] = {}
    for item in manuscript_integration_items():
        absent = tuple(path for path in item.required_paths if not (root / path).exists())
        if absent:
            missing[item.chapter] = absent
    return missing


def manuscript_integration_report(package_root: str | Path | None = None) -> ManuscriptIntegrationReport:
    """Build the v1.0.307 manuscript integration checklist report."""

    return ManuscriptIntegrationReport(
        version="v1.0.307",
        phase_range="v1.0.306-v1.0.310",
        items=manuscript_integration_items(),
        missing_paths=missing_manuscript_integration_paths(package_root),
    )


def manuscript_integration_summary(package_root: str | Path | None = None) -> str:
    """Return a compact human-readable summary."""

    report = manuscript_integration_report(package_root)
    return (
        f"Manuscript integration: {report.version}; "
        f"phase: {report.phase_range}; "
        f"chapters: {report.chapter_count}; "
        f"targets: {report.target_count}; "
        f"blockers: {report.blocker_count}"
    )
