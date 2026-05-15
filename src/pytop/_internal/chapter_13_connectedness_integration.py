"""Chapter 13 connectedness manuscript integration - v1.0.327.

This module opens the Chapter 13 connectedness/path-connectedness integration
track from the active Chapter 07--15 target map.  It records separated-set
criteria, clopen diagnostics, connected components, path/local connectedness
distinctions, continuous-image preservation, and the intermediate value theorem
bridge in a machine-readable form.

Originality guardrails
----------------------
All wording is synthesised from standard topology and the active pytop API
surface.  Uploaded chapter zip files are treated as reference inputs only; no
external prose, example wording, exercise wording, or proof wording is copied.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List

from pytop.result import Result

# ---------------------------------------------------------------------------
# Version and active targets
# ---------------------------------------------------------------------------

CHAPTER_13_INTEGRATION_VERSION: str = "v1.0.327"

CHAPTER_13_MANUSCRIPT_TARGETS: List[str] = [
    "manuscript/volume_1/chapters/13_connectedness.tex",
    "src/pytop/connectedness.py",
    "src/pytop/infinite_connectedness.py",
    "examples_bank/connectedness_examples.md",
    "docs/questionbank/chapter_13_connectedness_family_draft_v1_0_211.md",
    "notebooks/exploration/06_connectedness.ipynb",
    "notebooks/counterexamples/connected_not_path_connected.ipynb",
    "docs/quality/chapter_13_separated_sets_bridge_quality_gate_v1_0_253.md",
    "docs/quality/chapter_13_clopen_characterization_bridge_quality_gate_v1_0_254.md",
    "tests/core/test_chapter_13_connectedness_integration_v327.py",
    "docs/integration/chapter_07_15/chapter_13_connectedness_integration_v1_0_327.md",
]

CHAPTER_13_INSERTION_POINTS: List[str] = [
    "separated sets and nontrivial clopen subsets as equivalent disconnection diagnostics",
    "connected components and path components as partition-level invariants",
    "path connectedness and local connectedness distinction table with counterexample pointers",
    "continuous images of connected spaces and the intermediate value theorem bridge",
]

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SeparatedSetDiagnosticRow:
    """One separated-set or clopen diagnostic row."""

    id: str
    criterion: str
    detects_disconnection: bool
    manuscript_note: str
    api_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ComponentBridgeRow:
    """One connected-component or path-component bridge row."""

    id: str
    object_name: str
    definition: str
    partition_role: str
    api_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PathLocalConnectednessRow:
    """One row distinguishing connected, path connected, and local variants."""

    id: str
    property_name: str
    implication: str
    converse_holds: bool
    caution: str
    example_pointer: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ContinuousImageIVTRow:
    """One row linking connectedness preservation to IVT-style arguments."""

    id: str
    theorem: str
    hypothesis: str
    conclusion: str
    manuscript_use: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ConnectednessCounterexampleRow:
    """One counterexample/warning row for Chapter 13."""

    id: str
    space: str
    connected: bool
    path_connected: bool | str
    locally_connected: bool | str
    lesson: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ConnectednessIntegrationAudit:
    """Audit summary for the Chapter 13 connectedness integration surface."""

    version: str
    separated_set_rows: int
    component_rows: int
    path_local_rows: int
    continuous_image_rows: int
    counterexample_rows: int
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
                "Chapter 13 is anchored in manuscript/volume_1/chapters/13_connectedness.tex.",
                "Uploaded Chapter 13 reference material is not copied verbatim.",
            ],
            justification=[
                f"Separated-set diagnostic rows: {self.separated_set_rows}.",
                f"Component bridge rows: {self.component_rows}.",
                f"Path/local connectedness rows: {self.path_local_rows}.",
                f"Continuous-image/IVT rows: {self.continuous_image_rows}.",
                f"Counterexample rows: {self.counterexample_rows}.",
                f"Missing active targets: {self.blocker_count}.",
            ],
            metadata=self.to_dict(),
        )


# ---------------------------------------------------------------------------
# Separated sets and clopen diagnostics
# ---------------------------------------------------------------------------

def build_separated_set_diagnostic_bridge() -> List[SeparatedSetDiagnosticRow]:
    """Return separated-set and clopen diagnostic bridge rows."""
    return [
        SeparatedSetDiagnosticRow(
            id="separated_union_definition",
            criterion="X is disconnected when it is the union of two nonempty separated subsets.",
            detects_disconnection=True,
            manuscript_note="Use this as the first geometric intuition for splitting a space.",
            api_note="connects to pytop.connectedness.analyze_connectedness and finite clopen checks",
        ),
        SeparatedSetDiagnosticRow(
            id="nontrivial_clopen_subset",
            criterion="A nonempty proper subset that is both open and closed gives a disconnection.",
            detects_disconnection=True,
            manuscript_note="State the clopen criterion immediately after separated-set definitions.",
            api_note="connects to pytop.predicates.is_clopen_subset and finite topology enumeration",
        ),
        SeparatedSetDiagnosticRow(
            id="finite_space_clopen_scan",
            criterion="In finite explicit spaces, connectedness can be tested by scanning all clopen subsets.",
            detects_disconnection=True,
            manuscript_note="Turn small finite spaces into table-based diagnostics for students.",
            api_note="implemented in pytop.connectedness._finite_connected_from_topology",
        ),
        SeparatedSetDiagnosticRow(
            id="interval_no_clopen_split",
            criterion="Intervals in the real line cannot be split by a nontrivial clopen subset in the subspace topology.",
            detects_disconnection=False,
            manuscript_note="Use as the intuitive bridge from order completeness to connectedness.",
            api_note="links to examples_bank/connectedness_examples.md and real-line examples",
        ),
    ]


# ---------------------------------------------------------------------------
# Components and path components
# ---------------------------------------------------------------------------

def build_component_bridge() -> List[ComponentBridgeRow]:
    """Return connected-component and path-component bridge rows."""
    return [
        ComponentBridgeRow(
            id="connected_component_maximality",
            object_name="connected component",
            definition="A maximal connected subset containing a given point.",
            partition_role="Connected components form a partition of the space.",
            api_note="future component enumeration can be layered over connectedness diagnostics",
        ),
        ComponentBridgeRow(
            id="path_component_maximality",
            object_name="path component",
            definition="A maximal subset in which any two points can be joined by a path.",
            partition_role="Path components partition the space and refine connected components in general.",
            api_note="connects to pytop.connectedness.is_path_connected",
        ),
        ComponentBridgeRow(
            id="component_invariant_transfer",
            object_name="component profile",
            definition="The number and qualitative type of components are homeomorphism invariants.",
            partition_role="Component data supports compare_spaces and invariant-profile discussion.",
            api_note="connects to pytop.comparison.compare_invariants and preservation layers",
        ),
        ComponentBridgeRow(
            id="locally_connected_component_openness",
            object_name="locally connected component behaviour",
            definition="In locally connected spaces, components of open sets are open.",
            partition_role="This explains why local hypotheses change component-level behaviour.",
            api_note="connects to pytop.connectedness.is_locally_connected",
        ),
    ]


# ---------------------------------------------------------------------------
# Path connectedness and local connectedness distinctions
# ---------------------------------------------------------------------------

def build_path_local_connectedness_bridge() -> List[PathLocalConnectednessRow]:
    """Return path/local connectedness distinction rows."""
    return [
        PathLocalConnectednessRow(
            id="path_connected_implies_connected",
            property_name="path connectedness",
            implication="path connected => connected",
            converse_holds=False,
            caution="The converse fails without additional hypotheses.",
            example_pointer="topologist sine curve / connected not path connected notebook",
        ),
        PathLocalConnectednessRow(
            id="locally_path_connected_components",
            property_name="local path connectedness",
            implication="locally path connected + connected => path connected on many standard domains",
            converse_holds=False,
            caution="Do not replace local hypotheses with global connectedness alone.",
            example_pointer="open subsets of Euclidean spaces versus pathological subspaces",
        ),
        PathLocalConnectednessRow(
            id="locally_connected_component_openness",
            property_name="local connectedness",
            implication="locally connected spaces have open components of open subsets",
            converse_holds=False,
            caution="A connected space need not be locally connected.",
            example_pointer="comb-style and sine-curve style warnings",
        ),
        PathLocalConnectednessRow(
            id="intervals_are_path_connected",
            property_name="interval path connectedness",
            implication="real intervals are path connected and therefore connected",
            converse_holds=True,
            caution="For subsets of R, connected subsets are exactly intervals; this is special to the line.",
            example_pointer="real-line interval examples",
        ),
        PathLocalConnectednessRow(
            id="product_connectedness_pointer",
            property_name="product connectedness",
            implication="products of connected spaces are connected under the product topology",
            converse_holds=False,
            caution="This is a forward/backward bridge to Chapter 12 product-space preservation rows.",
            example_pointer="Chapter 12 product preservation bridge",
        ),
    ]


# ---------------------------------------------------------------------------
# Continuous images and IVT
# ---------------------------------------------------------------------------

def build_continuous_image_ivt_bridge() -> List[ContinuousImageIVTRow]:
    """Return continuous-image and IVT bridge rows."""
    return [
        ContinuousImageIVTRow(
            id="continuous_image_connected",
            theorem="Continuous image of a connected space is connected.",
            hypothesis="f: X -> Y is continuous and X is connected.",
            conclusion="f(X) is connected in Y.",
            manuscript_use="Use as the preservation theorem before real-valued consequences.",
        ),
        ContinuousImageIVTRow(
            id="ivt_real_interval",
            theorem="Intermediate value theorem as connected-image theorem.",
            hypothesis="f: [a,b] -> R is continuous and y lies between f(a) and f(b).",
            conclusion="There exists c in [a,b] with f(c)=y.",
            manuscript_use="Present IVT as a connected-image consequence, not merely a calculus fact.",
        ),
        ContinuousImageIVTRow(
            id="homeomorphism_preserves_connectedness",
            theorem="Homeomorphisms preserve connectedness and path connectedness.",
            hypothesis="X and Y are homeomorphic.",
            conclusion="Connectedness data transfers both ways.",
            manuscript_use="Link Chapter 13 to the Chapter 07 homeomorphism-invariant transfer layer.",
        ),
        ContinuousImageIVTRow(
            id="quotient_connectedness_pointer",
            theorem="Quotient images of connected spaces are connected.",
            hypothesis="q: X -> X/~ is quotient and X is connected.",
            conclusion="The quotient space is connected.",
            manuscript_use="Use as a bridge to quotient and sum constructions without importing external text.",
        ),
    ]


# ---------------------------------------------------------------------------
# Counterexample and caution rows
# ---------------------------------------------------------------------------

def build_connectedness_counterexample_bridge() -> List[ConnectednessCounterexampleRow]:
    """Return counterexample/caution rows for Chapter 13."""
    return [
        ConnectednessCounterexampleRow(
            id="two_point_discrete",
            space="two-point discrete space",
            connected=False,
            path_connected=False,
            locally_connected=True,
            lesson="A nontrivial clopen singleton gives the smallest finite disconnection witness.",
        ),
        ConnectednessCounterexampleRow(
            id="indiscrete_space",
            space="nonempty indiscrete space",
            connected=True,
            path_connected="usually symbolic / context-dependent",
            locally_connected=True,
            lesson="Absence of nontrivial open sets can force connectedness in finite diagnostics.",
        ),
        ConnectednessCounterexampleRow(
            id="topologist_sine_curve_style",
            space="connected not path connected continuum-style example",
            connected=True,
            path_connected=False,
            locally_connected=False,
            lesson="Connectedness and path connectedness must be taught as distinct notions.",
        ),
        ConnectednessCounterexampleRow(
            id="rational_line",
            space="Q with the subspace topology from R",
            connected=False,
            path_connected=False,
            locally_connected="not treated as a positive local model here",
            lesson="Density alone does not imply connectedness.",
        ),
    ]


# ---------------------------------------------------------------------------
# Audit, summary, rendering
# ---------------------------------------------------------------------------

def build_chapter_13_integration_audit(root: Path | str | None = None) -> ConnectednessIntegrationAudit:
    """Build the Chapter 13 integration audit for an extracted package root."""
    root_path = Path(root) if root is not None else Path.cwd()
    missing = tuple(
        rel for rel in CHAPTER_13_MANUSCRIPT_TARGETS
        if not (root_path / rel).exists()
    )
    return ConnectednessIntegrationAudit(
        version=CHAPTER_13_INTEGRATION_VERSION,
        separated_set_rows=len(build_separated_set_diagnostic_bridge()),
        component_rows=len(build_component_bridge()),
        path_local_rows=len(build_path_local_connectedness_bridge()),
        continuous_image_rows=len(build_continuous_image_ivt_bridge()),
        counterexample_rows=len(build_connectedness_counterexample_bridge()),
        insertion_points=len(CHAPTER_13_INSERTION_POINTS),
        missing_targets=missing,
        originality_guardrail=(
            "Chapter 13 uses uploaded chapter zips as reference-only material; "
            "examples, proofs, and exercises must be rewritten in the project voice."
        ),
    )


def chapter_13_integration_summary(root: Path | str | None = None) -> dict[str, Any]:
    """Return a compact machine-readable summary of the v1.0.327 bridge."""
    audit = build_chapter_13_integration_audit(root)
    return {
        "version": CHAPTER_13_INTEGRATION_VERSION,
        "topic": "connectedness and path connectedness",
        "separated_set_rows": audit.separated_set_rows,
        "component_rows": audit.component_rows,
        "path_local_rows": audit.path_local_rows,
        "continuous_image_rows": audit.continuous_image_rows,
        "counterexample_rows": audit.counterexample_rows,
        "insertion_points": list(CHAPTER_13_INSERTION_POINTS),
        "blocker_count": audit.blocker_count,
        "ready": audit.ready,
        "next": "v1.0.328 Chapter 14 complete metric spaces integration",
    }


def render_chapter_13_integration_report(root: Path | str | None = None) -> str:
    """Render a human-readable Chapter 13 integration report."""
    audit = build_chapter_13_integration_audit(root)
    lines: list[str] = [
        f"# Chapter 13 Connectedness Integration Report - {CHAPTER_13_INTEGRATION_VERSION}",
        "",
        "## Separated sets and clopen diagnostics",
    ]
    for row in build_separated_set_diagnostic_bridge():
        lines.append(
            f"- **{row.id}**: {row.criterion} Manuscript: {row.manuscript_note} API: {row.api_note}."
        )
    lines.extend(["", "## Connected components and path components"])
    for row in build_component_bridge():
        lines.append(
            f"- **{row.object_name}** (`{row.id}`): {row.definition} {row.partition_role} API: {row.api_note}."
        )
    lines.extend(["", "## Path/local connectedness distinctions"])
    for row in build_path_local_connectedness_bridge():
        lines.append(
            f"- **{row.property_name}** (`{row.id}`): {row.implication}. Converse holds: `{row.converse_holds}`. Caution: {row.caution}"
        )
    lines.extend(["", "## Continuous images and IVT bridge"])
    for row in build_continuous_image_ivt_bridge():
        lines.append(
            f"- **{row.id}**: {row.theorem} Hypothesis: {row.hypothesis} Conclusion: {row.conclusion}"
        )
    lines.extend(["", "## Counterexample and caution bridge"])
    for row in build_connectedness_counterexample_bridge():
        lines.append(
            f"- **{row.space}** (`{row.id}`): connected=`{row.connected}`, path_connected=`{row.path_connected}`, locally_connected=`{row.locally_connected}`. Lesson: {row.lesson}"
        )
    lines.extend([
        "",
        "## Audit",
        f"- Separated-set diagnostic rows: `{audit.separated_set_rows}`",
        f"- Component rows: `{audit.component_rows}`",
        f"- Path/local connectedness rows: `{audit.path_local_rows}`",
        f"- Continuous-image/IVT rows: `{audit.continuous_image_rows}`",
        f"- Counterexample rows: `{audit.counterexample_rows}`",
        f"- Insertion points: `{audit.insertion_points}`",
        f"- Missing targets: `{audit.blocker_count}`",
        f"- Ready: `{audit.ready}`",
        "",
        "## Originality guardrail",
        audit.originality_guardrail,
    ])
    return "\n".join(lines) + "\n"


__all__ = [
    "CHAPTER_13_INTEGRATION_VERSION",
    "CHAPTER_13_MANUSCRIPT_TARGETS",
    "CHAPTER_13_INSERTION_POINTS",
    "SeparatedSetDiagnosticRow",
    "ComponentBridgeRow",
    "PathLocalConnectednessRow",
    "ContinuousImageIVTRow",
    "ConnectednessCounterexampleRow",
    "ConnectednessIntegrationAudit",
    "build_separated_set_diagnostic_bridge",
    "build_component_bridge",
    "build_path_local_connectedness_bridge",
    "build_continuous_image_ivt_bridge",
    "build_connectedness_counterexample_bridge",
    "build_chapter_13_integration_audit",
    "chapter_13_integration_summary",
    "render_chapter_13_integration_report",
]
