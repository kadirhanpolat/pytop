"""Chapter 07--15 API coverage matrix helpers.

The v1.0.318 matrix is a planning surface built from the active open-folder
package.  It does not import uploaded Chapter 07--15 zips and it does not treat
historical archive material as active source.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .chapter_07_15_coverage_audit import default_chapter_07_15_coverage_specs
from .result import Result


API_MATRIX_VERSION = "v1.0.318"


@dataclass(frozen=True, slots=True)
class ChapterApiNeed:
    """One planned API or contract need for a chapter."""

    kind: str
    description: str
    priority: str = "normal"

    def to_dict(self) -> dict[str, str]:
        return {
            "kind": self.kind,
            "description": self.description,
            "priority": self.priority,
        }


@dataclass(frozen=True, slots=True)
class ChapterApiMatrixSpec:
    """Static v1.0.318 API-matrix planning specification for one chapter."""

    chapter: int
    topic: str
    concept_groups: tuple[str, ...]
    expected_core_api: tuple[str, ...]
    expected_bridge_docs: tuple[str, ...]
    planned_needs: tuple[ChapterApiNeed, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def label(self) -> str:
        return f"Chapter {self.chapter:02d}"


@dataclass(frozen=True, slots=True)
class ChapterApiMatrixRow:
    """Resolved API-matrix row for one chapter."""

    spec: ChapterApiMatrixSpec
    present_core_api: tuple[str, ...]
    missing_core_api: tuple[str, ...]
    present_bridge_docs: tuple[str, ...]
    missing_bridge_docs: tuple[str, ...]

    @property
    def chapter(self) -> int:
        return self.spec.chapter

    @property
    def topic(self) -> str:
        return self.spec.topic

    @property
    def concept_groups(self) -> tuple[str, ...]:
        return self.spec.concept_groups

    @property
    def planned_needs(self) -> tuple[ChapterApiNeed, ...]:
        return self.spec.planned_needs

    @property
    def missing_count(self) -> int:
        return len(self.missing_core_api) + len(self.missing_bridge_docs)

    @property
    def status(self) -> str:
        """Return the matrix status.

        `ready_to_contractize` means current API and bridge-doc surfaces exist
        and the remaining work is making those surfaces more explicit in
        questionbank/manuscript contracts.  `needs_surface` is reserved for
        genuinely missing active API or bridge-doc paths.
        """

        if self.missing_count:
            return "needs_surface"
        if self.planned_needs:
            return "ready_to_contractize"
        return "covered"

    @property
    def priority(self) -> str:
        priorities = {need.priority for need in self.planned_needs}
        if "high" in priorities:
            return "high"
        if "normal" in priorities:
            return "normal"
        return "low"

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "label": self.spec.label,
            "topic": self.topic,
            "concept_groups": list(self.concept_groups),
            "status": self.status,
            "priority": self.priority,
            "expected_core_api": list(self.spec.expected_core_api),
            "present_core_api": list(self.present_core_api),
            "missing_core_api": list(self.missing_core_api),
            "expected_bridge_docs": list(self.spec.expected_bridge_docs),
            "present_bridge_docs": list(self.present_bridge_docs),
            "missing_bridge_docs": list(self.missing_bridge_docs),
            "planned_needs": [need.to_dict() for need in self.planned_needs],
            "notes": list(self.spec.notes),
        }


@dataclass(frozen=True, slots=True)
class ChapterApiMatrixReport:
    """Aggregate v1.0.318 API coverage matrix report."""

    version: str
    package_root: str
    rows: tuple[ChapterApiMatrixRow, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def chapters(self) -> tuple[int, ...]:
        return tuple(row.chapter for row in self.rows)

    @property
    def status(self) -> str:
        return "matrix"

    @property
    def blocker_count(self) -> int:
        return sum(row.missing_count for row in self.rows)

    @property
    def high_priority_need_count(self) -> int:
        return sum(1 for row in self.rows for need in row.planned_needs if need.priority == "high")

    @property
    def planned_need_count(self) -> int:
        return sum(len(row.planned_needs) for row in self.rows)

    @property
    def rows_needing_surface_count(self) -> int:
        return sum(1 for row in self.rows if row.status == "needs_surface")

    @property
    def rows_ready_to_contractize_count(self) -> int:
        return sum(1 for row in self.rows if row.status == "ready_to_contractize")

    @property
    def next_actions(self) -> tuple[str, ...]:
        actions: list[str] = []
        for row in self.rows:
            if row.missing_count:
                missing = ", ".join(row.missing_core_api + row.missing_bridge_docs)
                actions.append(f"{row.spec.label}: restore or create missing API surface(s): {missing}.")
            for need in row.planned_needs:
                prefix = "high-priority" if need.priority == "high" else need.priority
                actions.append(f"{row.spec.label}: {prefix} {need.kind} — {need.description}")
        return tuple(actions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "package_root": self.package_root,
            "status": self.status,
            "chapters": list(self.chapters),
            "blocker_count": self.blocker_count,
            "planned_need_count": self.planned_need_count,
            "high_priority_need_count": self.high_priority_need_count,
            "rows_needing_surface_count": self.rows_needing_surface_count,
            "rows_ready_to_contractize_count": self.rows_ready_to_contractize_count,
            "rows": [row.to_dict() for row in self.rows],
            "next_actions": list(self.next_actions),
            "metadata": dict(self.metadata),
        }

    def to_result(self) -> Result:
        return Result(
            status="true",
            mode="matrix",
            value=self.to_dict(),
            justification=[
                "Chapter 07--15 API coverage matrix completed.",
                "Existing API files and bridge documentation are separated from planned API skeleton needs.",
                "The matrix is a planning input for v1.0.319 and v1.0.320, not a packaging blocker.",
            ],
            metadata=self.to_dict(),
        )


def default_chapter_07_15_api_matrix_specs() -> tuple[ChapterApiMatrixSpec, ...]:
    """Return the v1.0.318 API-matrix baseline."""

    coverage_specs = {spec.chapter: spec for spec in default_chapter_07_15_coverage_specs()}

    def core(chapter: int) -> tuple[str, ...]:
        return tuple(coverage_specs[chapter].expected.get("core_api", ()))

    def docs(chapter: int) -> tuple[str, ...]:
        return tuple(coverage_specs[chapter].expected.get("api_docs", ()))

    need = ChapterApiNeed

    return (
        ChapterApiMatrixSpec(7, coverage_specs[7].topic, ("continuity", "open/closed maps", "homeomorphism", "initial topology"), core(7), docs(7), (need("contract", "turn finite/infinite continuity checks into chapter-facing questionbank contracts", "high"), need("skeleton", "name initial-topology and homeomorphism checks as stable API capabilities", "normal")), ("Chapter 07 is the first chapter-by-chapter opening target after v1.0.320.",)),
        ChapterApiMatrixSpec(8, coverage_specs[8].topic, ("metric spaces", "equivalent metrics", "isometry", "norm-induced metrics"), core(8), docs(8), (need("contract", "bind metric examples to explicit metric-contract validation outputs", "normal"), need("skeleton", "separate isometry/equivalent-metric teaching helpers from generic metric validation", "normal"))),
        ChapterApiMatrixSpec(9, coverage_specs[9].topic, ("local bases", "first/second countability", "separability", "Lindelof reductions"), core(9), docs(9), (need("test", "add chapter-facing countability/local-base tests named for Chapter 09", "high"), need("contract", "convert local-base and separability examples into executable questionbank contracts", "high")), ("v1.0.317 marked Chapter 09 tests as partial.",)),
        ChapterApiMatrixSpec(10, coverage_specs[10].topic, ("T0/T1/T2 separation", "finite counterexamples", "cofinite/co-countable warnings"), core(10), docs(10), (need("test", "add Chapter 10 separation-axiom tests over finite and infinite examples", "high"), need("skeleton", "name cofinite/co-countable warning checks as explicit API capabilities", "normal")), ("v1.0.317 marked Chapter 10 tests as partial.",)),
        ChapterApiMatrixSpec(11, coverage_specs[11].topic, ("open-cover compactness", "FIP", "continuous images", "metric compactness variants"), core(11), docs(11), (need("contract", "tie compactness variants to examples_bank and preservation outputs", "normal"), need("skeleton", "make FIP and metric compactness routes visible in a chapter-facing API map", "normal"))),
        ChapterApiMatrixSpec(12, coverage_specs[12].topic, ("product topology", "box topology", "projections", "coordinate convergence"), core(12), docs(12), (need("contract", "separate product and box topology questionbank contracts", "normal"), need("skeleton", "make projection/coordinate-convergence checks discoverable from products", "normal"))),
        ChapterApiMatrixSpec(13, coverage_specs[13].topic, ("connectedness", "clopen sets", "components", "path connectedness"), core(13), docs(13), (need("test", "add Chapter 13 connectedness/component/path-connectedness tests", "high"), need("contract", "turn clopen/component examples into executable questionbank contracts", "high")), ("v1.0.317 marked Chapter 13 tests as partial.",)),
        ChapterApiMatrixSpec(14, coverage_specs[14].topic, ("Cauchy sequences", "complete metric spaces", "completion", "fixed-point route"), core(14), docs(14), (need("contract", "bind completeness examples to metric-contract outputs", "normal"), need("skeleton", "make Cauchy/completion route names explicit without overpromising theorem proving", "normal"))),
        ChapterApiMatrixSpec(15, coverage_specs[15].topic, ("function spaces", "pointwise convergence", "uniform convergence", "compact-open topology"), core(15), docs(15), (need("contract", "connect existing Chapter 15 questionbank routes to API matrix rows", "normal"), need("skeleton", "separate compact-open and point-open topology preview surfaces", "normal")), ("Chapter 15 has the strongest existing questionbank-code surface.",)),
    )


def build_chapter_07_15_api_matrix(package_root: str | Path, *, version: str = API_MATRIX_VERSION, specs: Iterable[ChapterApiMatrixSpec] | None = None, metadata: Mapping[str, Any] | None = None) -> ChapterApiMatrixReport:
    """Build the Chapter 07--15 API coverage matrix for the active package."""

    root = Path(package_root)
    active_specs = tuple(specs) if specs is not None else default_chapter_07_15_api_matrix_specs()
    rows: list[ChapterApiMatrixRow] = []

    for spec in active_specs:
        present_core = tuple(path for path in spec.expected_core_api if (root / path).exists())
        missing_core = tuple(path for path in spec.expected_core_api if path not in present_core)
        present_docs = tuple(path for path in spec.expected_bridge_docs if (root / path).exists())
        missing_docs = tuple(path for path in spec.expected_bridge_docs if path not in present_docs)
        rows.append(ChapterApiMatrixRow(spec=spec, present_core_api=present_core, missing_core_api=missing_core, present_bridge_docs=present_docs, missing_bridge_docs=missing_docs))

    return ChapterApiMatrixReport(version=version, package_root=str(root), rows=tuple(rows), metadata=dict(metadata or {}))


def render_chapter_07_15_api_matrix(report: ChapterApiMatrixReport) -> str:
    """Render the API coverage matrix as Markdown."""

    lines = [
        f"# Chapter 07--15 API Coverage Matrix - {report.version}",
        "",
        "This matrix is generated from active package files only.  It separates",
        "current API surfaces, API/bridge documentation, and planned API-skeleton",
        "or contract needs.",
        "",
        "## Summary",
        "",
        f"- Package root: `{report.package_root}`",
        f"- Audited chapters: `{', '.join(f'{chapter:02d}' for chapter in report.chapters)}`",
        f"- Missing active API/doc surfaces: `{report.blocker_count}`",
        f"- Planned API/contract/test needs: `{report.planned_need_count}`",
        f"- High-priority planned needs: `{report.high_priority_need_count}`",
        f"- Rows ready to contractize: `{report.rows_ready_to_contractize_count}`",
        "",
        "## Matrix",
        "",
        "| Chapter | Topic | Status | Priority | Current core API | API/bridge docs | Planned skeleton/contract needs |",
        "|---|---|---|---|---|---|---|",
    ]

    for row in report.rows:
        current_api = "<br>".join(f"`{path}`" for path in row.present_core_api) or "missing"
        bridge_docs = "<br>".join(f"`{path}`" for path in row.present_bridge_docs) or "missing"
        needs = "<br>".join(f"{need.kind}: {need.description}" for need in row.planned_needs) or "none"
        lines.append(f"| {row.chapter:02d} | {row.topic} | {row.status} | {row.priority} | {current_api} | {bridge_docs} | {needs} |")

    lines.extend(["", "## Next actions", ""])
    for action in report.next_actions:
        lines.append(f"- {action}")

    lines.extend(["", "## Guardrails", ""])
    lines.append("- Do not turn uploaded Chapter 07--15 zips into active nested packages.")
    lines.append("- Do not treat `docs/archive/` history bundles as active source.")
    lines.append("- Use this matrix as the input for v1.0.319 questionbank-contract alignment and v1.0.320 manuscript target mapping.")
    return "\n".join(lines) + "\n"


def chapter_07_15_api_matrix_summary(package_root: str | Path) -> dict[str, Any]:
    """Return the v1.0.318 API-matrix summary dictionary."""

    return build_chapter_07_15_api_matrix(package_root).to_dict()
