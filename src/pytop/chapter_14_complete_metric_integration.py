"""Chapter 14 complete metric-spaces manuscript integration - v1.0.328.

This module opens the Chapter 14 complete metric-spaces integration track from
Chapter 07--15.  It records Cauchy-sequence diagnostics, completeness examples,
closed-subspace/completion routes, compactness-vs-completeness distinctions,
contraction/fixed-point cautions, and Baire-reading boundaries in a
machine-readable form.

Originality guardrails
----------------------
The uploaded Chapter 14 zip is treated as reference-only material.  The bridge
below uses standard topology terminology and active ``pytop`` surfaces; it does
not copy external prose, proof text, examples, exercises, or diagram wording.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List

from pytop.result import Result

# ---------------------------------------------------------------------------
# Version and active targets
# ---------------------------------------------------------------------------

CHAPTER_14_INTEGRATION_VERSION: str = "v1.0.328"

CHAPTER_14_MANUSCRIPT_TARGETS: List[str] = [
    "manuscript/volume_1/chapters/16_sequences_and_convergence.tex",
    "manuscript/volume_1/quick_checks/07_sequences_completeness.tex",
    "src/pytop/metric_contracts.py",
    "src/pytop/metric_spaces.py",
    "examples_bank/complete_metric_examples.md",
    "examples_bank/convergence_examples.md",
    "docs/questionbank/chapter_14_complete_metric_family_draft_v1_0_212.md",
    "notebooks/exploration/09b_sequences_subsequences_completeness.ipynb",
    "docs/integration/chapter_07_15/chapter_14_cauchy_completeness_bridge_note_v1_0_259.md",
    "docs/integration/chapter_07_15/chapter_14_closed_subspace_completeness_bridge_note_v1_0_260.md",
    "docs/integration/chapter_07_15/chapter_14_nested_closed_sets_bridge_note_v1_0_261.md",
    "docs/integration/chapter_07_15/chapter_14_complete_totally_bounded_compactness_bridge_note_v1_0_262.md",
    "docs/integration/chapter_07_15/chapter_14_banach_fixed_point_forward_bridge_note_v1_0_263.md",
    "docs/integration/chapter_07_15/chapter_14_completion_forward_bridge_note_v1_0_264.md",
    "docs/integration/chapter_07_15/chapter_14_baire_category_forward_bridge_note_v1_0_265.md",
    "docs/quality/chapter_14_cauchy_completeness_bridge_quality_gate_v1_0_259.md",
    "tests/core/test_chapter_14_complete_metric_integration_v328.py",
    "docs/integration/chapter_07_15/chapter_14_complete_metric_integration_v1_0_328.md",
]

CHAPTER_14_INSERTION_POINTS: List[str] = [
    "Cauchy versus convergent sequence status table",
    "complete subspace and closed-subspace theorem warning box",
    "complete plus totally bounded versus compact comparison table",
    "completion, contraction mapping, and Baire theorem forward-pointer boxes",
]

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CauchyCompletenessRow:
    """One Cauchy/completeness diagnostic row."""

    id: str
    concept: str
    criterion: str
    positive_model: str
    caution: str
    api_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ClosedSubspaceCompletionRow:
    """One closed-subspace, completion, or nested-set route row."""

    id: str
    route: str
    hypothesis: str
    conclusion: str
    failure_warning: str
    manuscript_use: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MetricCompactnessComparisonRow:
    """One metric compactness/completeness comparison row."""

    id: str
    space: str
    complete: bool | str
    totally_bounded: bool | str
    compact: bool | str
    lesson: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FixedPointCompletionBridgeRow:
    """One forward bridge row for contractions, completions, or Banach spaces."""

    id: str
    theorem_or_route: str
    completeness_role: str
    safe_chapter_14_scope: str
    future_bridge: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class BaireReadingBridgeRow:
    """One Baire-category reading scaffold row."""

    id: str
    term: str
    reading_task: str
    allowed_output: str
    overreach_warning: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CompleteMetricIntegrationAudit:
    """Audit summary for the Chapter 14 complete metric-spaces integration surface."""

    version: str
    cauchy_rows: int
    subspace_completion_rows: int
    compactness_rows: int
    fixed_point_completion_rows: int
    baire_reading_rows: int
    insertion_points: int
    missing_targets: tuple[str, ...]
    originality_guardrail: str

    @property
    def blocker_count(self) -> int:
        return len(self.missing_targets)

    @property
    def ready(self) -> bool:
        return self.blocker_count == 0

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["blocker_count"] = self.blocker_count
        data["ready"] = self.ready
        return data

    def to_result(self) -> Result:
        return Result(
            status="true" if self.ready else "conditional",
            mode="mixed",
            value=self.to_dict(),
            assumptions=[
                "Chapter 14 is anchored in metric-sequence and completeness material.",
                "Uploaded Chapter 14 material is not copied verbatim.",
            ],
            justification=[
                f"Cauchy/completeness rows: {self.cauchy_rows}.",
                f"Closed-subspace/completion rows: {self.subspace_completion_rows}.",
                f"Metric compactness comparison rows: {self.compactness_rows}.",
                f"Fixed-point/completion bridge rows: {self.fixed_point_completion_rows}.",
                f"Baire reading rows: {self.baire_reading_rows}.",
                f"Missing active targets: {self.blocker_count}.",
            ],
            metadata=self.to_dict(),
        )


# ---------------------------------------------------------------------------
# Cauchy sequences and completeness
# ---------------------------------------------------------------------------

def build_cauchy_completeness_bridge() -> List[CauchyCompletenessRow]:
    """Return Chapter 14 Cauchy/completeness diagnostic rows."""
    return [
        CauchyCompletenessRow(
            id="convergent_implies_cauchy",
            concept="convergent sequence",
            criterion="Every convergent sequence in a metric space is Cauchy.",
            positive_model="eventual epsilon control by the limit point",
            caution="The converse is a completeness statement, not a general metric-space fact.",
            api_note="binds to convergence_examples and Result-based explanation output",
        ),
        CauchyCompletenessRow(
            id="cauchy_missing_limit",
            concept="Cauchy but not convergent in the ambient space",
            criterion="A Cauchy sequence can fail to converge when its natural limit is outside the space.",
            positive_model="boundary-approaching sequence in an open interval or rational approximations to an irrational",
            caution="Do not call the ambient space complete when the limit point has been removed.",
            api_note="binds to examples_bank/complete_metric_examples.md warning lines",
        ),
        CauchyCompletenessRow(
            id="eventually_constant_discrete_metric",
            concept="discrete/trivial metric Cauchy behaviour",
            criterion="For a unit discrete metric, a Cauchy sequence is eventually constant.",
            positive_model="finite or discrete carrier where epsilon below one forces equality",
            caution="This is metric-specific and should not be generalized to all metrics on the same set.",
            api_note="binds to finite metric examples and finite_metric_contract",
        ),
        CauchyCompletenessRow(
            id="coordinatewise_cauchy_euclidean",
            concept="Euclidean coordinate control",
            criterion="A Cauchy sequence in finite-dimensional Euclidean space is coordinatewise Cauchy.",
            positive_model="projection to finitely many real coordinates",
            caution="Keep this finite-dimensional; infinite products need separate topology/metric hypotheses.",
            api_note="bridges Chapter 12 product/convergence rows to metric examples",
        ),
        CauchyCompletenessRow(
            id="complete_space_definition",
            concept="complete metric space",
            criterion="A metric space is complete when every Cauchy sequence converges inside the space.",
            positive_model="R, closed intervals, finite metric spaces, and standard Euclidean spaces",
            caution="Completeness is not purely topological; equivalent-looking spaces may differ metrically.",
            api_note="binds to metric_contracts and complete_metric_examples benchmark tags",
        ),
    ]


# ---------------------------------------------------------------------------
# Closed subspaces, nested sets, and completion
# ---------------------------------------------------------------------------

def build_closed_subspace_completion_bridge() -> List[ClosedSubspaceCompletionRow]:
    """Return closed-subspace, nested-set, and completion route rows."""
    return [
        ClosedSubspaceCompletionRow(
            id="closed_subspace_of_complete_space",
            route="closed-subspace completeness theorem",
            hypothesis="Y is closed in a complete metric space X with the inherited metric.",
            conclusion="Y is complete.",
            failure_warning="Without closedness, a Cauchy sequence in Y can converge in X to a point outside Y.",
            manuscript_use="place after the definition of completeness as the first structural permanence result",
        ),
        ClosedSubspaceCompletionRow(
            id="complete_subspace_closed_in_metric_space",
            route="complete subspace closedness theorem",
            hypothesis="Y is a complete subspace of a metric space X.",
            conclusion="Y is closed in X.",
            failure_warning="The metric inherited by Y must be explicit; avoid topological-only phrasing.",
            manuscript_use="use as the reverse direction warning for subspace exercises",
        ),
        ClosedSubspaceCompletionRow(
            id="nested_closed_sets_diameter_zero",
            route="nested closed sets principle",
            hypothesis="Nonempty closed sets are nested and diameters tend to zero in a complete metric space.",
            conclusion="Their intersection is nonempty, and often a single point under the diameter condition.",
            failure_warning="Closedness and the diameter-zero condition are both essential hypotheses.",
            manuscript_use="turn into a theorem-reading table rather than a black-box theorem prover",
        ),
        ClosedSubspaceCompletionRow(
            id="completion_by_cauchy_classes",
            route="completion construction forward pointer",
            hypothesis="Cauchy sequences are identified when their pairwise distances tend to zero.",
            conclusion="The quotient model supplies a complete space containing a dense isometric copy of the original space.",
            failure_warning="Do not expose this as executable construction until equivalence-class contracts are stable.",
            manuscript_use="give a guided overview and send formal generator work to a later version",
        ),
    ]


# ---------------------------------------------------------------------------
# Complete, totally bounded, compact
# ---------------------------------------------------------------------------

def build_metric_compactness_comparison_bridge() -> List[MetricCompactnessComparisonRow]:
    """Return metric compactness/completeness comparison rows."""
    return [
        MetricCompactnessComparisonRow(
            id="closed_unit_interval",
            space="closed unit interval with the usual metric",
            complete=True,
            totally_bounded=True,
            compact=True,
            lesson="This is the positive benchmark for compact metric spaces.",
        ),
        MetricCompactnessComparisonRow(
            id="real_line",
            space="real line with the usual metric",
            complete=True,
            totally_bounded=False,
            compact=False,
            lesson="Completeness alone does not imply compactness.",
        ),
        MetricCompactnessComparisonRow(
            id="open_unit_interval",
            space="open unit interval with the inherited usual metric",
            complete=False,
            totally_bounded=True,
            compact=False,
            lesson="Total boundedness without completeness is not compactness.",
        ),
        MetricCompactnessComparisonRow(
            id="finite_metric_space",
            space="finite metric space",
            complete=True,
            totally_bounded=True,
            compact=True,
            lesson="Finite metric spaces are safe test fixtures but should not hide infinite-space distinctions.",
        ),
    ]


# ---------------------------------------------------------------------------
# Fixed-point and completion bridges
# ---------------------------------------------------------------------------

def build_fixed_point_completion_bridge() -> List[FixedPointCompletionBridgeRow]:
    """Return fixed-point/completion forward bridge rows."""
    return [
        FixedPointCompletionBridgeRow(
            id="contraction_mapping_definition",
            theorem_or_route="contraction mapping route",
            completeness_role="A contraction theorem needs the Picard sequence to have its Cauchy limit in the space.",
            safe_chapter_14_scope="verify a supplied contraction constant and explain why completeness is named",
            future_bridge="later numerical iteration notebooks and fixed-point problem generators",
        ),
        FixedPointCompletionBridgeRow(
            id="banach_fixed_point_theorem",
            theorem_or_route="Banach fixed-point theorem",
            completeness_role="Completeness converts the constructed Cauchy orbit into an actual fixed point.",
            safe_chapter_14_scope="theorem statement, hypothesis checklist, and short proof skeleton only",
            future_bridge="analysis-facing applications outside the basic topology package",
        ),
        FixedPointCompletionBridgeRow(
            id="completion_uniqueness_route",
            theorem_or_route="uniqueness of completion up to isometry",
            completeness_role="Any completion is a complete host for the same Cauchy-limit data.",
            safe_chapter_14_scope="guided reading plus route map; no automatic quotient construction yet",
            future_bridge="equivalence-relation and quotient-metric construction contracts",
        ),
        FixedPointCompletionBridgeRow(
            id="banach_space_forward_pointer",
            theorem_or_route="Banach-space forward pointer",
            completeness_role="A complete normed vector space is a metric-completeness refinement of normed-space material.",
            safe_chapter_14_scope="terminology pointer and examples, not a functional-analysis chapter",
            future_bridge="Chapter 15 function-space metrics and sup-norm completeness",
        ),
    ]


# ---------------------------------------------------------------------------
# Baire category reading scaffold
# ---------------------------------------------------------------------------

def build_baire_reading_bridge() -> List[BaireReadingBridgeRow]:
    """Return Baire category theorem reading-scaffold rows."""
    return [
        BaireReadingBridgeRow(
            id="nowhere_dense_term",
            term="nowhere dense subset",
            reading_task="identify closure, interior, and the empty-interior conclusion",
            allowed_output="hypothesis/conclusion matching and short examples",
            overreach_warning="do not turn this into an unrestricted category-theory generator",
        ),
        BaireReadingBridgeRow(
            id="meagre_union_term",
            term="countable union of nowhere dense sets",
            reading_task="separate finite, countable, dense, and nowhere-dense language",
            allowed_output="terminology table and localized proof-step prompts",
            overreach_warning="avoid analytic applications not already supported by the manuscript",
        ),
        BaireReadingBridgeRow(
            id="baire_complete_metric_statement",
            term="Baire theorem for complete metric spaces",
            reading_task="locate the completeness hypothesis and state the conclusion in plain language",
            allowed_output="guided theorem-reading family",
            overreach_warning="keep this as reading scaffold until a stable Baire section exists",
        ),
    ]


# ---------------------------------------------------------------------------
# Audit and rendering
# ---------------------------------------------------------------------------

def build_chapter_14_integration_audit(package_root: str | Path) -> CompleteMetricIntegrationAudit:
    """Build an audit for the Chapter 14 complete metric-spaces integration."""
    root = Path(package_root)
    missing = tuple(path for path in CHAPTER_14_MANUSCRIPT_TARGETS if not (root / path).exists())
    return CompleteMetricIntegrationAudit(
        version=CHAPTER_14_INTEGRATION_VERSION,
        cauchy_rows=len(build_cauchy_completeness_bridge()),
        subspace_completion_rows=len(build_closed_subspace_completion_bridge()),
        compactness_rows=len(build_metric_compactness_comparison_bridge()),
        fixed_point_completion_rows=len(build_fixed_point_completion_bridge()),
        baire_reading_rows=len(build_baire_reading_bridge()),
        insertion_points=len(CHAPTER_14_INSERTION_POINTS),
        missing_targets=missing,
        originality_guardrail=(
            "Chapter 14 reference zips are used only to identify coverage themes; "
            "all examples, reports, and tests are freshly written."
        ),
    )


def chapter_14_integration_summary(package_root: str | Path) -> dict[str, Any]:
    """Return a compact dictionary summary for release records."""
    audit = build_chapter_14_integration_audit(package_root)
    return {
        "version": audit.version,
        "topic": "complete metric spaces",
        "ready": audit.ready,
        "blocker_count": audit.blocker_count,
        "cauchy_rows": audit.cauchy_rows,
        "subspace_completion_rows": audit.subspace_completion_rows,
        "compactness_rows": audit.compactness_rows,
        "fixed_point_completion_rows": audit.fixed_point_completion_rows,
        "baire_reading_rows": audit.baire_reading_rows,
        "next": "v1.0.329 Chapter 15 function spaces integration",
    }


def render_chapter_14_integration_report(package_root: str | Path) -> str:
    """Render the Chapter 14 integration report as Markdown."""
    audit = build_chapter_14_integration_audit(package_root)
    lines: list[str] = [
        "# Chapter 14 Complete Metric Spaces Integration Report - v1.0.328",
        "",
        "## Cauchy sequences and completeness",
    ]
    for row in build_cauchy_completeness_bridge():
        lines.append(
            f"- **{row.id}** ({row.concept}): {row.criterion} Model: {row.positive_model}. "
            f"Caution: {row.caution} API: {row.api_note}."
        )

    lines.extend(["", "## Closed subspaces, nested sets, and completions"])
    for row in build_closed_subspace_completion_bridge():
        lines.append(
            f"- **{row.id}** ({row.route}): if {row.hypothesis} then {row.conclusion} "
            f"Warning: {row.failure_warning} Manuscript: {row.manuscript_use}."
        )

    lines.extend(["", "## Complete, totally bounded, compact comparison"])
    for row in build_metric_compactness_comparison_bridge():
        lines.append(
            f"- **{row.id}**: {row.space}; complete=`{row.complete}`, "
            f"totally_bounded=`{row.totally_bounded}`, compact=`{row.compact}`. Lesson: {row.lesson}"
        )

    lines.extend(["", "## Contraction, fixed-point, and completion forward bridge"])
    for row in build_fixed_point_completion_bridge():
        lines.append(
            f"- **{row.id}** ({row.theorem_or_route}): {row.completeness_role} "
            f"Scope: {row.safe_chapter_14_scope}. Future: {row.future_bridge}."
        )

    lines.extend(["", "## Baire reading scaffold"])
    for row in build_baire_reading_bridge():
        lines.append(
            f"- **{row.id}** ({row.term}): task={row.reading_task}. "
            f"Allowed output: {row.allowed_output}. Warning: {row.overreach_warning}."
        )

    lines.extend([
        "",
        "## Audit",
        f"- Cauchy/completeness rows: `{audit.cauchy_rows}`",
        f"- Closed-subspace/completion rows: `{audit.subspace_completion_rows}`",
        f"- Compactness comparison rows: `{audit.compactness_rows}`",
        f"- Fixed-point/completion rows: `{audit.fixed_point_completion_rows}`",
        f"- Baire reading rows: `{audit.baire_reading_rows}`",
        f"- Insertion points: `{audit.insertion_points}`",
        f"- Missing targets: `{audit.blocker_count}`",
        f"- Ready: `{audit.ready}`",
        "",
        "## Originality guardrail",
        audit.originality_guardrail,
    ])
    return "\n".join(lines) + "\n"
