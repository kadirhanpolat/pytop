"""Integration quality gate for v1.0.309.

This gate joins the three open-folder integration surfaces produced in
v1.0.306--v1.0.308:

- questionbank bridge rows,
- manuscript target checklist rows,
- notebook smoke examples.

It is intentionally a verification layer. It does not copy external
Chapter 07--15 reference zip wording, it does not create a nested active
subproject, and it keeps the ecosystem in the single full-package model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .manuscript_integration import manuscript_integration_report
from .notebook_smoke_examples import notebook_smoke_report
from .questionbank_bridge import questionbank_bridge_report
from .result import Result


EXPECTED_INTEGRATION_CHAPTERS: tuple[str, ...] = tuple(f"{n:02d}" for n in range(7, 16))


@dataclass(frozen=True, slots=True)
class IntegrationQualitySection:
    """One upstream integration surface checked by the v1.0.309 gate."""

    name: str
    version: str
    status: str
    blocker_count: int
    evidence_paths: tuple[str, ...]
    summary: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_ready(self) -> bool:
        return self.status == "true" and self.blocker_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "blocker_count": self.blocker_count,
            "is_ready": self.is_ready,
            "evidence_paths": list(self.evidence_paths),
            "summary": self.summary,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class IntegrationQualityGateReport:
    """Aggregate gate across questionbank, manuscript, and notebook surfaces."""

    version: str
    phase_range: str
    sections: tuple[IntegrationQualitySection, ...]
    expected_chapters: tuple[str, ...]
    questionbank_chapters: tuple[str, ...]
    manuscript_chapters: tuple[str, ...]
    active_nested_zip_violations: tuple[str, ...] = ()
    missing_evidence_paths: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def ready_section_count(self) -> int:
        return sum(1 for section in self.sections if section.is_ready)

    @property
    def chapter_alignment_issues(self) -> tuple[str, ...]:
        issues: list[str] = []
        if self.questionbank_chapters != self.expected_chapters:
            issues.append(
                "questionbank chapters "
                f"{list(self.questionbank_chapters)} do not match {list(self.expected_chapters)}"
            )
        if self.manuscript_chapters != self.expected_chapters:
            issues.append(
                "manuscript chapters "
                f"{list(self.manuscript_chapters)} do not match {list(self.expected_chapters)}"
            )
        return tuple(issues)

    @property
    def blocker_count(self) -> int:
        return (
            sum(section.blocker_count for section in self.sections)
            + len(self.chapter_alignment_issues)
            + len(self.active_nested_zip_violations)
            + len(self.missing_evidence_paths)
        )

    @property
    def status(self) -> str:
        return "true" if self.is_ready else "conditional"

    @property
    def is_ready(self) -> bool:
        return (
            self.ready_section_count == self.section_count
            and self.blocker_count == 0
        )

    def to_result(self) -> Result:
        if self.is_ready:
            return Result.true(
                mode="exact",
                value="integration quality gate ready",
                assumptions=(
                    "Chapter 07--15 external zips remain reference inputs only",
                    "questionbank, manuscript, and notebook surfaces remain open-folder artifacts",
                    "active nested zips are not introduced outside the frozen docs/archive evidence bundle",
                ),
                justification=(
                    f"{self.section_count} integration sections are ready.",
                    f"chapters {self.expected_chapters[0]}--{self.expected_chapters[-1]} align across bridge and manuscript rows.",
                    "notebook smoke evidence is present and passing.",
                ),
                metadata={
                    "version": self.version,
                    "phase_range": self.phase_range,
                    "section_count": self.section_count,
                    "ready_section_count": self.ready_section_count,
                    "expected_chapters": list(self.expected_chapters),
                    "blocker_count": 0,
                },
            )
        return Result.conditional(
            mode="mixed",
            value="integration quality gate has blockers",
            assumptions=("all integration blockers must be resolved before the v1.0.310 checkpoint",),
            justification=(
                f"ready_sections={self.ready_section_count}/{self.section_count}",
                f"chapter_alignment_issues={list(self.chapter_alignment_issues)}",
                f"active_nested_zip_violations={list(self.active_nested_zip_violations)}",
                f"missing_evidence_paths={list(self.missing_evidence_paths)}",
            ),
            metadata={
                "version": self.version,
                "phase_range": self.phase_range,
                "section_count": self.section_count,
                "ready_section_count": self.ready_section_count,
                "blocker_count": self.blocker_count,
                "chapter_alignment_issues": list(self.chapter_alignment_issues),
                "active_nested_zip_violations": list(self.active_nested_zip_violations),
                "missing_evidence_paths": list(self.missing_evidence_paths),
            },
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "phase_range": self.phase_range,
            "status": self.status,
            "is_ready": self.is_ready,
            "section_count": self.section_count,
            "ready_section_count": self.ready_section_count,
            "blocker_count": self.blocker_count,
            "expected_chapters": list(self.expected_chapters),
            "questionbank_chapters": list(self.questionbank_chapters),
            "manuscript_chapters": list(self.manuscript_chapters),
            "chapter_alignment_issues": list(self.chapter_alignment_issues),
            "active_nested_zip_violations": list(self.active_nested_zip_violations),
            "missing_evidence_paths": list(self.missing_evidence_paths),
            "sections": [section.to_dict() for section in self.sections],
            "notes": list(self.notes),
        }


def _section_from_report(
    *,
    name: str,
    version: str,
    status: str,
    blocker_count: int,
    evidence_paths: tuple[str, ...],
    summary: str,
    metadata: Mapping[str, Any] | None = None,
) -> IntegrationQualitySection:
    return IntegrationQualitySection(
        name=name,
        version=version,
        status=status,
        blocker_count=blocker_count,
        evidence_paths=evidence_paths,
        summary=summary,
        metadata=dict(metadata or {}),
    )


def _active_nested_zip_violations(package_root: Path | None) -> tuple[str, ...]:
    if package_root is None:
        return ()
    violations: list[str] = []
    for path in package_root.rglob("*.zip"):
        rel = path.relative_to(package_root).as_posix()
        allowed_archive_bundle = (
            rel.startswith("docs/archive/archive_history_bundle_")
            and rel.endswith(".zip")
        )
        if not allowed_archive_bundle:
            violations.append(rel)
    return tuple(sorted(violations))


def _missing_evidence_paths(package_root: Path | None, sections: tuple[IntegrationQualitySection, ...]) -> tuple[str, ...]:
    if package_root is None:
        return ()
    required = tuple(dict.fromkeys(path for section in sections for path in section.evidence_paths))
    return tuple(path for path in required if not (package_root / path).exists())


def integration_quality_gate_report(package_root: str | Path | None = None) -> IntegrationQualityGateReport:
    """Build the v1.0.309 cross-surface integration quality gate."""

    root = Path(package_root) if package_root is not None else None

    q_report = questionbank_bridge_report(root)
    m_report = manuscript_integration_report(root)
    n_report = notebook_smoke_report(root)

    questionbank_chapters = tuple(sorted({item.chapter for item in q_report.bridge_items}))
    manuscript_chapters = tuple(sorted({item.chapter for item in m_report.items}))

    sections = (
        _section_from_report(
            name="questionbank_bridge",
            version=q_report.version,
            status=q_report.status,
            blocker_count=q_report.blocker_count,
            evidence_paths=(
                "docs/questionbank/questionbank_bridge_map_v1_0_306.md",
                "docs/quality/questionbank_bridge_quality_gate_v1_0_306.md",
                "tests/core/test_questionbank_bridge_v306.py",
            ),
            summary=f"{q_report.mapped_item_count} bridge rows over {q_report.mapped_chapter_count} chapters",
            metadata={
                "mapped_item_count": q_report.mapped_item_count,
                "mapped_chapter_count": q_report.mapped_chapter_count,
                "missing_core_references": list(q_report.missing_core_references),
            },
        ),
        _section_from_report(
            name="manuscript_integration",
            version=m_report.version,
            status=m_report.status,
            blocker_count=m_report.blocker_count,
            evidence_paths=(
                "docs/manuscript/manuscript_integration_checklist_v1_0_307.md",
                "docs/quality/manuscript_integration_quality_gate_v1_0_307.md",
                "tests/core/test_manuscript_integration_v307.py",
            ),
            summary=f"{m_report.target_count} manuscript target references for {m_report.chapter_count} chapters",
            metadata={
                "mapped_item_count": m_report.mapped_item_count,
                "target_count": m_report.target_count,
                "chapters_needing_assignment": list(m_report.chapters_needing_assignment),
            },
        ),
        _section_from_report(
            name="notebook_smoke_examples",
            version=n_report.version,
            status=n_report.status,
            blocker_count=n_report.blocker_count,
            evidence_paths=(
                "docs/notebooks/notebook_smoke_examples_v1_0_308.md",
                "docs/quality/notebook_smoke_quality_gate_v1_0_308.md",
                "notebooks/smoke/contract_to_result_rendering_smoke_v1_0_308.ipynb",
                "tests/core/test_notebook_smoke_examples_v308.py",
            ),
            summary=f"{n_report.passing_count}/{n_report.example_count} smoke examples passing",
            metadata={
                "example_count": n_report.example_count,
                "passing_count": n_report.passing_count,
                "failing_examples": list(n_report.failing_examples),
            },
        ),
    )

    return IntegrationQualityGateReport(
        version="v1.0.309",
        phase_range="v1.0.306-v1.0.310",
        sections=sections,
        expected_chapters=EXPECTED_INTEGRATION_CHAPTERS,
        questionbank_chapters=questionbank_chapters,
        manuscript_chapters=manuscript_chapters,
        active_nested_zip_violations=_active_nested_zip_violations(root),
        missing_evidence_paths=_missing_evidence_paths(root, sections),
        notes=(
            "This gate verifies integration traceability; it does not import external chapter wording.",
            "The only allowed nested zip is the frozen archive bundle under docs/archive.",
        ),
    )


def integration_quality_gate_summary(package_root: str | Path | None = None) -> str:
    """Return a compact human-readable v1.0.309 gate summary."""

    report = integration_quality_gate_report(package_root)
    return (
        f"Integration quality gate: {report.version}; "
        f"phase: {report.phase_range}; "
        f"sections: {report.ready_section_count}/{report.section_count}; "
        f"chapters: {report.expected_chapters[0]}--{report.expected_chapters[-1]}; "
        f"blockers: {report.blocker_count}"
    )
