"""Chapter 07--15 coverage audit helpers.

This v1.0.317 module is deliberately read-only.  It does not import or copy the
uploaded Chapter 07--15 reference zips.  Instead, it audits the active open-folder
package surfaces and reports which chapter-facing surfaces already exist for the
next integration phases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .result import Result


SURFACE_NAMES = (
    "manuscript",
    "examples_bank",
    "questionbank_docs",
    "questionbank_code",
    "api_docs",
    "core_api",
    "tests",
    "notebooks",
    "integration_docs",
)


@dataclass(frozen=True, slots=True)
class ChapterCoverageSpec:
    """Expected active-package surfaces for one Chapter 07--15 target."""

    chapter: int
    topic: str
    expected: Mapping[str, tuple[str, ...]]
    notes: tuple[str, ...] = ()

    @property
    def label(self) -> str:
        return f"Chapter {self.chapter:02d}"


@dataclass(frozen=True, slots=True)
class SurfaceCoverage:
    """Presence result for one chapter/surface pair."""

    surface: str
    expected_paths: tuple[str, ...]
    present_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]

    @property
    def status(self) -> str:
        if not self.expected_paths:
            return "not_applicable"
        if not self.missing_paths:
            return "present"
        if self.present_paths:
            return "partial"
        return "missing"

    @property
    def is_present_or_partial(self) -> bool:
        return self.status in {"present", "partial"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "surface": self.surface,
            "status": self.status,
            "expected_paths": list(self.expected_paths),
            "present_paths": list(self.present_paths),
            "missing_paths": list(self.missing_paths),
        }


@dataclass(frozen=True, slots=True)
class ChapterCoverageRow:
    """Coverage row for a single chapter."""

    spec: ChapterCoverageSpec
    surfaces: tuple[SurfaceCoverage, ...]

    @property
    def chapter(self) -> int:
        return self.spec.chapter

    @property
    def topic(self) -> str:
        return self.spec.topic

    @property
    def statuses(self) -> dict[str, str]:
        return {surface.surface: surface.status for surface in self.surfaces}

    @property
    def missing_surfaces(self) -> tuple[str, ...]:
        return tuple(surface.surface for surface in self.surfaces if surface.status == "missing")

    @property
    def partial_surfaces(self) -> tuple[str, ...]:
        return tuple(surface.surface for surface in self.surfaces if surface.status == "partial")

    @property
    def coverage_score(self) -> int:
        """Return a simple percentage over applicable surfaces."""

        applicable = [surface for surface in self.surfaces if surface.status != "not_applicable"]
        if not applicable:
            return 0
        weighted = 0.0
        for surface in applicable:
            if surface.status == "present":
                weighted += 1.0
            elif surface.status == "partial":
                weighted += 0.5
        return round(100 * weighted / len(applicable))

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "label": self.spec.label,
            "topic": self.topic,
            "coverage_score": self.coverage_score,
            "statuses": self.statuses,
            "missing_surfaces": list(self.missing_surfaces),
            "partial_surfaces": list(self.partial_surfaces),
            "notes": list(self.spec.notes),
            "surfaces": [surface.to_dict() for surface in self.surfaces],
        }


@dataclass(frozen=True, slots=True)
class ChapterCoverageAuditReport:
    """Aggregate Chapter 07--15 coverage audit result."""

    version: str
    package_root: str
    rows: tuple[ChapterCoverageRow, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def chapters(self) -> tuple[int, ...]:
        return tuple(row.chapter for row in self.rows)

    @property
    def complete_chapter_count(self) -> int:
        return sum(1 for row in self.rows if not row.missing_surfaces and not row.partial_surfaces)

    @property
    def blocker_count(self) -> int:
        return sum(len(row.missing_surfaces) for row in self.rows)

    @property
    def warning_count(self) -> int:
        return sum(len(row.partial_surfaces) for row in self.rows)

    @property
    def status(self) -> str:
        # v1.0.317 is an audit, not a readiness gate.  Missing surfaces are
        # therefore expected planning output and not a packaging blocker.
        return "audit"

    @property
    def next_actions(self) -> tuple[str, ...]:
        actions: list[str] = []
        for row in self.rows:
            if row.missing_surfaces or row.partial_surfaces:
                surfaces = ", ".join(row.missing_surfaces + row.partial_surfaces)
                actions.append(f"{row.spec.label}: strengthen {surfaces}.")
        return tuple(actions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "package_root": self.package_root,
            "status": self.status,
            "chapters": list(self.chapters),
            "complete_chapter_count": self.complete_chapter_count,
            "blocker_count": self.blocker_count,
            "warning_count": self.warning_count,
            "rows": [row.to_dict() for row in self.rows],
            "next_actions": list(self.next_actions),
            "metadata": dict(self.metadata),
        }

    def to_result(self) -> Result:
        return Result(
            status="true",
            mode="audit",
            value=self.to_dict(),
            justification=[
                "Chapter 07--15 active-package coverage audit completed.",
                "Missing and partial surfaces are recorded as integration work items, not packaging failures.",
                f"Audited chapters: {', '.join(str(ch) for ch in self.chapters)}.",
            ],
            metadata=self.to_dict(),
        )


def default_chapter_07_15_coverage_specs() -> tuple[ChapterCoverageSpec, ...]:
    """Return the v1.0.317 baseline coverage expectations."""

    def t(*paths: str) -> tuple[str, ...]:
        return tuple(paths)

    return (
        ChapterCoverageSpec(
            7,
            "continuity, map taxonomy, homeomorphism, initial topology",
            {
                "manuscript": t("manuscript/volume_1/chapters/07_subspaces.tex"),
                "examples_bank": t("examples_bank/continuity_map_taxonomy.md"),
                "questionbank_docs": t("docs/questionbank/chapter_07_continuity_homeomorphism_family_draft_v1_0_205.md"),
                "questionbank_code": t("src/pytop/questionbank_bridge.py"),
                "api_docs": t("docs/api/chapter_07_continuity_api_needs_v1_0_214.md"),
                "core_api": t("src/pytop/maps.py", "src/pytop/infinite_maps.py"),
                "tests": t("tests/core/test_maps.py", "tests/core/test_infinite_maps_and_constructions.py"),
                "notebooks": t("notebooks/exploration/04_continuity.ipynb", "notebooks/teaching/lesson_03_continuity.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_07_continuity_comparison_v1_0_187.md"),
            },
            ("Strong documentation trail exists; the next risk is making questionbank contracts executable by chapter.",),
        ),
        ChapterCoverageSpec(
            8,
            "metric spaces, equivalent metrics, isometry, norm-induced metrics",
            {
                "manuscript": t("manuscript/volume_1/chapters/15_metric_spaces.tex"),
                "examples_bank": t("examples_bank/metric_space_examples.md", "examples_bank/metric_topology_bridge_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_08_metric_normed_family_draft_v1_0_206.md"),
                "questionbank_code": t("src/pytop/metric_contracts.py"),
                "api_docs": t("docs/api/chapter_08_metric_normed_api_needs_v1_0_215.md"),
                "core_api": t("src/pytop/metric_spaces.py", "src/pytop/metric_contracts.py"),
                "tests": t("tests/core/test_metric_spaces.py", "tests/core/test_metric_contracts_v302.py"),
                "notebooks": t("notebooks/teaching/lesson_06a_metric_spaces.ipynb", "notebooks/exploration/09c_norms_function_metrics_hilbert_glimpse.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_08_metric_normed_comparison_v1_0_188.md"),
            },
        ),
        ChapterCoverageSpec(
            9,
            "local bases, countability, separability, Lindelof reductions",
            {
                "manuscript": t("manuscript/volume_1/chapters/12_countability_axioms.tex"),
                "examples_bank": t("examples_bank/countability_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_09_countability_family_draft_v1_0_207.md"),
                "questionbank_code": t("src/pytop/countability.py"),
                "api_docs": t("docs/api/chapter_09_countability_api_needs_v1_0_216.md"),
                "core_api": t("src/pytop/countability.py", "src/pytop/infinite_countability.py"),
                "tests": t("tests/core/test_countability.py", "tests/core/test_infinite_countability.py"),
                "notebooks": t("notebooks/teaching/lesson_05_countability.ipynb", "notebooks/exploration/09_countability_and_metric_examples.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_09_countability_comparison_v1_0_189.md"),
            },
        ),
        ChapterCoverageSpec(
            10,
            "separation axioms, finite examples, cofinite/co-countable warnings",
            {
                "manuscript": t("manuscript/volume_1/chapters/11_separation_axioms.tex"),
                "examples_bank": t("examples_bank/separation_axioms_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_10_separation_axioms_family_draft_v1_0_208.md"),
                "questionbank_code": t("src/pytop/infinite_separation.py"),
                "api_docs": t("docs/integration/chapter_07_15/chapter_10_separation_comparison_v1_0_190.md"),
                "core_api": t("src/pytop/infinite_separation.py", "src/pytop/predicates.py"),
                "tests": t("tests/core/test_infinite_separation.py", "tests/core/test_predicates.py"),
                "notebooks": t("notebooks/teaching/lesson_04_separation.ipynb", "notebooks/counterexamples/t1_not_hausdorff_cocountable.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_10_separation_comparison_v1_0_190.md"),
            },
        ),
        ChapterCoverageSpec(
            11,
            "compactness, FIP, continuous images, metric compactness variants",
            {
                "manuscript": t("manuscript/volume_1/chapters/14_compactness.tex"),
                "examples_bank": t("examples_bank/compactness_examples.md", "examples_bank/compactness_variants_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_11_compactness_family_draft_v1_0_209.md"),
                "questionbank_code": t("src/pytop/compactness.py", "src/pytop/compactness_bridges.py"),
                "api_docs": t("docs/integration/chapter_07_15/chapter_11_compactness_comparison_v1_0_191.md"),
                "core_api": t("src/pytop/compactness.py", "src/pytop/infinite_compactness.py"),
                "tests": t("tests/core/test_compactness.py", "tests/core/test_compactness_bridges.py"),
                "notebooks": t("notebooks/teaching/lesson_06_compactness_connectedness.ipynb", "notebooks/exploration/07_compactness.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_11_compactness_comparison_v1_0_191.md"),
            },
        ),
        ChapterCoverageSpec(
            12,
            "product topology, box topology, projections, coordinate convergence",
            {
                "manuscript": t("manuscript/volume_1/chapters/08_products.tex"),
                "examples_bank": t("examples_bank/product_space_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_12_product_spaces_family_draft_v1_0_210.md"),
                "questionbank_code": t("src/pytop/products.py", "src/pytop/infinite_constructions.py"),
                "api_docs": t("docs/integration/chapter_07_15/chapter_12_products_comparison_v1_0_192.md"),
                "core_api": t("src/pytop/products.py", "src/pytop/infinite_constructions.py"),
                "tests": t("tests/core/test_products.py", "tests/core/test_infinite_maps_and_constructions.py"),
                "notebooks": t("notebooks/exploration/05_subspaces_products_quotients.ipynb", "notebooks/teaching/lesson_03b_subspaces_products_quotients.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_12_products_comparison_v1_0_192.md"),
            },
        ),
        ChapterCoverageSpec(
            13,
            "connectedness, clopen sets, components, path connectedness",
            {
                "manuscript": t("manuscript/volume_1/chapters/13_connectedness.tex"),
                "examples_bank": t("examples_bank/connectedness_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_13_connectedness_family_draft_v1_0_211.md"),
                "questionbank_code": t("src/pytop/connectedness.py"),
                "api_docs": t("docs/integration/chapter_07_15/chapter_13_connectedness_comparison_v1_0_193.md"),
                "core_api": t("src/pytop/connectedness.py", "src/pytop/infinite_connectedness.py"),
                "tests": t("tests/core/test_connectedness.py", "tests/core/test_infinite_connectedness.py"),
                "notebooks": t("notebooks/teaching/lesson_06_compactness_connectedness.ipynb", "notebooks/exploration/06_connectedness.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_13_connectedness_comparison_v1_0_193.md"),
            },
        ),
        ChapterCoverageSpec(
            14,
            "complete metric spaces, Cauchy sequences, completion, fixed-point route",
            {
                "manuscript": t("manuscript/volume_1/chapters/15_metric_spaces.tex"),
                "examples_bank": t("examples_bank/complete_metric_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_14_complete_metric_family_draft_v1_0_212.md"),
                "questionbank_code": t("src/pytop/metric_contracts.py"),
                "api_docs": t("docs/integration/chapter_07_15/chapter_14_complete_metric_comparison_v1_0_194.md"),
                "core_api": t("src/pytop/metric_spaces.py", "src/pytop/metric_contracts.py"),
                "tests": t("tests/core/test_metric_spaces.py", "tests/core/test_metric_contracts_v302.py"),
                "notebooks": t("notebooks/teaching/lesson_06c_sequences_and_completeness.ipynb", "notebooks/exploration/09b_sequences_subsequences_completeness.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_14_complete_metric_comparison_v1_0_194.md"),
            },
        ),
        ChapterCoverageSpec(
            15,
            "function spaces, pointwise/uniform convergence, sup norm, compact-open topology",
            {
                "manuscript": t("manuscript/volume_1/chapters/15_metric_spaces.tex"),
                "examples_bank": t("examples_bank/function_space_examples.md"),
                "questionbank_docs": t("docs/questionbank/chapter_15_function_spaces_family_draft_v1_0_213.md"),
                "questionbank_code": t("src/pytop_questionbank/chapter_15_preview_routes.py", "src/pytop_questionbank/chapter_15_seeded_bundle.py"),
                "api_docs": t("docs/integration/chapter_07_15/chapter_15_function_spaces_comparison_v1_0_195.md"),
                "core_api": t("src/pytop/metric_spaces.py", "src/pytop/research_bridge_profiles.py"),
                "tests": t("tests/questionbank/test_chapter_15_preview_routes.py", "tests/questionbank/test_chapter_15_seeded_bundle.py"),
                "notebooks": t("notebooks/exploration/09c_norms_function_metrics_hilbert_glimpse.ipynb", "notebooks/research/advanced_examples.ipynb"),
                "integration_docs": t("docs/integration/chapter_07_15/chapter_15_function_spaces_comparison_v1_0_195.md"),
            },
            ("This is the strongest questionbank-code surface among Chapters 07--15.",),
        ),
    )


def _path_status(package_root: Path, paths: Iterable[str]) -> SurfaceCoverage:
    expected = tuple(paths)
    present = tuple(path for path in expected if (package_root / path).exists())
    missing = tuple(path for path in expected if path not in present)
    return SurfaceCoverage(
        surface="",
        expected_paths=expected,
        present_paths=present,
        missing_paths=missing,
    )


def audit_chapter_07_15_coverage(
    package_root: str | Path,
    *,
    version: str = "v1.0.317",
    specs: Iterable[ChapterCoverageSpec] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ChapterCoverageAuditReport:
    """Audit active package coverage for Chapters 07--15."""

    root = Path(package_root)
    rows: list[ChapterCoverageRow] = []
    active_specs = tuple(specs) if specs is not None else default_chapter_07_15_coverage_specs()

    for spec in active_specs:
        surfaces: list[SurfaceCoverage] = []
        for surface in SURFACE_NAMES:
            expected = tuple(spec.expected.get(surface, ()))
            present = tuple(path for path in expected if (root / path).exists())
            missing = tuple(path for path in expected if path not in present)
            surfaces.append(
                SurfaceCoverage(
                    surface=surface,
                    expected_paths=expected,
                    present_paths=present,
                    missing_paths=missing,
                )
            )
        rows.append(ChapterCoverageRow(spec=spec, surfaces=tuple(surfaces)))

    return ChapterCoverageAuditReport(
        version=version,
        package_root=str(root),
        rows=tuple(rows),
        metadata=dict(metadata or {}),
    )


def render_chapter_07_15_coverage_audit(report: ChapterCoverageAuditReport) -> str:
    """Render a compact Markdown table for the audit report."""

    header = [
        f"# Chapter 07--15 Coverage Audit - {report.version}",
        "",
        "This report is generated from the active open-folder package surfaces.",
        "It does not treat uploaded Chapter 07--15 reference zips as active nested packages.",
        "",
        "## Summary",
        "",
        f"- Package root: `{report.package_root}`",
        f"- Audited chapters: `{', '.join(f'{chapter:02d}' for chapter in report.chapters)}`",
        f"- Complete chapter rows: `{report.complete_chapter_count}`",
        f"- Missing surface count: `{report.blocker_count}`",
        f"- Partial surface count: `{report.warning_count}`",
        "",
        "## Matrix",
        "",
        "| Chapter | Topic | Score | Manuscript | Examples | QB docs | QB code | API docs | Core API | Tests | Notebooks | Integration docs |",
        "|---|---|---:|---|---|---|---|---|---|---|---|---|",
    ]
    lines = header[:]
    surface_labels = {
        "manuscript": "Manuscript",
        "examples_bank": "Examples",
        "questionbank_docs": "QB docs",
        "questionbank_code": "QB code",
        "api_docs": "API docs",
        "core_api": "Core API",
        "tests": "Tests",
        "notebooks": "Notebooks",
        "integration_docs": "Integration docs",
    }
    del surface_labels  # labels are retained in the table header; statuses use fixed order.
    for row in report.rows:
        s = row.statuses
        lines.append(
            "| "
            + f"{row.chapter:02d} | {row.topic} | {row.coverage_score} | "
            + " | ".join(s[surface] for surface in SURFACE_NAMES)
            + " |"
        )
    lines.extend(["", "## Next actions", ""])
    if report.next_actions:
        for action in report.next_actions:
            lines.append(f"- {action}")
    else:
        lines.append("- No missing or partial surfaces were detected.")
    lines.extend(["", "## Notes", ""])
    lines.append("- `present` means every expected path for that surface exists.")
    lines.append("- `partial` means at least one expected path exists but another expected path is missing.")
    lines.append("- `missing` means no expected path exists for that surface.")
    lines.append("- This audit is a planning instrument for v1.0.318--v1.0.320, not a mathematical correctness proof.")
    return "\n".join(lines) + "\n"


def chapter_07_15_coverage_audit_summary(package_root: str | Path) -> dict[str, Any]:
    """Return the v1.0.317 audit summary dictionary."""

    return audit_chapter_07_15_coverage(package_root).to_dict()
