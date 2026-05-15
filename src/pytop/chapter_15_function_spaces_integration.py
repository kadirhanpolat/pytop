"""Chapter 15 function-spaces manuscript integration - v1.0.329.

This module opens the Chapter 15 function-spaces integration track from
Chapter 07--15.  It records point-open/product-function identifications,
pointwise versus uniform convergence, sup-metric and compact-open topology
bridges, Arzela--Ascoli-style equicontinuity cautions, and bounded-linear-
functional forward pointers in a machine-readable form.

Originality guardrails
----------------------
The uploaded Chapter 15 zip is treated as reference-only material.  The bridge
below uses standard topology terminology and active ``pytop`` surfaces; it does
not copy external prose, proof text, examples, exercises, or diagram wording.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List

from pytop.result import Result

CHAPTER_15_INTEGRATION_VERSION: str = "v1.0.329"

CHAPTER_15_MANUSCRIPT_TARGETS: List[str] = [
    "manuscript/volume_1/chapters/01_sets_functions_families.tex",
    "manuscript/volume_1/quick_checks/07a_norms_function_metrics_forward_look.tex",
    "manuscript/volume_1/worksheets/07a_norms_function_metrics_forward_look.md",
    "examples_bank/function_space_examples.md",
    "docs/manuscript/function_spaces_bridge_v1_0_204.md",
    "docs/questionbank/chapter_15_function_spaces_family_draft_v1_0_213.md",
    "src/pytop_questionbank/chapter_15_preview_routes.py",
    "src/pytop_questionbank/chapter_15_seeded_bundle.py",
    "docs/integration/chapter_07_15/chapter_15_function_spaces_traceability_note_v1_0_266.md",
    "docs/integration/chapter_07_15/chapter_15_pointwise_uniform_convergence_bridge_note_v1_0_267.md",
    "docs/integration/chapter_07_15/chapter_15_sup_norm_function_space_metric_bridge_note_v1_0_268.md",
    "docs/integration/chapter_07_15/chapter_15_point_open_topology_bridge_note_v1_0_269.md",
    "docs/integration/chapter_07_15/chapter_15_compact_open_topology_bridge_note_v1_0_270.md",
    "docs/integration/chapter_07_15/chapter_15_equicontinuity_ascoli_bridge_note_v1_0_271.md",
    "docs/integration/chapter_07_15/chapter_15_function_space_examples_surface_v1_0_292.md",
    "docs/quality/chapter_15_function_spaces_traceability_quality_gate_v1_0_266.md",
    "docs/quality/chapter_15_pointwise_uniform_convergence_bridge_quality_gate_v1_0_267.md",
    "docs/quality/chapter_15_sup_norm_function_space_metric_bridge_quality_gate_v1_0_268.md",
    "docs/quality/chapter_15_point_open_topology_bridge_quality_gate_v1_0_269.md",
    "docs/quality/chapter_15_compact_open_topology_bridge_quality_gate_v1_0_270.md",
    "docs/quality/chapter_15_equicontinuity_ascoli_bridge_quality_gate_v1_0_271.md",
    "tests/core/test_chapter_15_function_spaces_integration_v329.py",
    "docs/integration/chapter_07_15/chapter_15_function_spaces_integration_v1_0_329.md",
]

CHAPTER_15_INSERTION_POINTS: List[str] = [
    "function space as product-indexed coordinate model",
    "point-open topology and evaluation-map subbase table",
    "pointwise versus uniform convergence warning block",
    "sup-metric and compact-open topology comparison panel",
    "equicontinuity, Ascoli, and bounded-functional forward bridge",
]


@dataclass(frozen=True, slots=True)
class FunctionSpaceTopologyRow:
    """One row for function-space topology selection."""

    id: str
    topology: str
    generating_data: str
    convergence_reading: str
    active_surface: str
    caution: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FunctionConvergenceRow:
    """One pointwise/uniform/compact convergence comparison row."""

    id: str
    mode: str
    quantifier_pattern: str
    stronger_than: str
    preserves_continuity: bool | str
    diagnostic: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SupMetricCompactOpenRow:
    """One sup-metric or compact-open topology bridge row."""

    id: str
    construction: str
    domain_condition: str
    topology_output: str
    comparison: str
    implementation_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AscoliEquicontinuityRow:
    """One equicontinuity/Ascoli forward row."""

    id: str
    property: str
    uniform_parameter: str
    compactness_role: str
    failure_warning: str
    manuscript_use: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FunctionalForwardBridgeRow:
    """One bounded-linear-functional and dual-space forward row."""

    id: str
    object_name: str
    algebraic_condition: str
    boundedness_condition: str
    norm_or_output: str
    scope_warning: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FunctionSpacesIntegrationAudit:
    """Audit summary for the Chapter 15 function-spaces integration surface."""

    version: str
    topology_rows: int
    convergence_rows: int
    sup_compact_open_rows: int
    ascoli_rows: int
    functional_rows: int
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
                "Chapter 15 is anchored in function-space and convergence material.",
                "Uploaded Chapter 15 material is used only as reference, not copied verbatim.",
            ],
            justification=[
                f"Function-space topology rows: {self.topology_rows}.",
                f"Convergence comparison rows: {self.convergence_rows}.",
                f"Sup-metric/compact-open rows: {self.sup_compact_open_rows}.",
                f"Ascoli/equicontinuity rows: {self.ascoli_rows}.",
                f"Functional forward rows: {self.functional_rows}.",
                f"Missing active targets: {self.blocker_count}.",
            ],
            metadata=self.to_dict(),
        )


def build_function_space_topology_bridge() -> List[FunctionSpaceTopologyRow]:
    """Return point-open/product/function-space topology rows."""
    return [
        FunctionSpaceTopologyRow(
            id="function_space_as_product",
            topology="coordinate product model",
            generating_data="identify functions X -> Y with product coordinates indexed by X",
            convergence_reading="coordinatewise statements become pointwise statements",
            active_surface="docs/integration/chapter_07_15/chapter_15_function_spaces_traceability_note_v1_0_266.md",
            caution="Use as a model bridge; do not silently replace arbitrary function-space topologies by product topology.",
        ),
        FunctionSpaceTopologyRow(
            id="evaluation_map_subbase",
            topology="point-open topology",
            generating_data="sets of functions constrained at a chosen point into an open set of Y",
            convergence_reading="evaluation maps are continuous by construction",
            active_surface="docs/integration/chapter_07_15/chapter_15_point_open_topology_bridge_note_v1_0_269.md",
            caution="Finite point constraints are not uniform control on the whole domain.",
        ),
        FunctionSpaceTopologyRow(
            id="bounded_function_sup_metric",
            topology="uniform-convergence metric topology",
            generating_data="supremum distance on bounded functions into a metric codomain",
            convergence_reading="metric convergence equals uniform convergence when the sup is finite",
            active_surface="docs/integration/chapter_07_15/chapter_15_sup_norm_function_space_metric_bridge_note_v1_0_268.md",
            caution="The sup-metric requires boundedness or a convention for infinite suprema.",
        ),
        FunctionSpaceTopologyRow(
            id="compact_open_subbase",
            topology="compact-open topology",
            generating_data="subbasic sets F(K,U) with compact K in the domain and open U in the codomain",
            convergence_reading="metric targets support uniform convergence on compact subsets",
            active_surface="docs/integration/chapter_07_15/chapter_15_compact_open_topology_bridge_note_v1_0_270.md",
            caution="It is generally finer than the point-open topology, but comparison needs hypotheses.",
        ),
        FunctionSpaceTopologyRow(
            id="continuous_function_subspace",
            topology="continuous-function subspace",
            generating_data="restrict the ambient function-space topology to C(X,Y)",
            convergence_reading="continuity of limits depends on the chosen topology and convergence mode",
            active_surface="examples_bank/function_space_examples.md",
            caution="Pointwise limits of continuous functions need not be continuous.",
        ),
    ]


def build_function_convergence_bridge() -> List[FunctionConvergenceRow]:
    """Return pointwise, uniform, and compact convergence rows."""
    return [
        FunctionConvergenceRow(
            id="pointwise_convergence",
            mode="pointwise convergence",
            quantifier_pattern="for each x and epsilon, an index threshold may depend on x",
            stronger_than="none in this bridge",
            preserves_continuity="not in general",
            diagnostic="matches convergence in the point-open topology",
        ),
        FunctionConvergenceRow(
            id="uniform_convergence",
            mode="uniform convergence",
            quantifier_pattern="for each epsilon, one index threshold works for every x",
            stronger_than="pointwise convergence",
            preserves_continuity=True,
            diagnostic="matches sup-metric convergence on bounded function families",
        ),
        FunctionConvergenceRow(
            id="compact_convergence",
            mode="uniform convergence on compacta",
            quantifier_pattern="for each compact K and epsilon, one threshold works for all x in K",
            stronger_than="pointwise convergence",
            preserves_continuity="under standard compact-open metric-target hypotheses",
            diagnostic="matches compact-open topology for suitable metric codomains",
        ),
        FunctionConvergenceRow(
            id="pointwise_not_uniform_warning",
            mode="non-uniform pointwise limit warning",
            quantifier_pattern="thresholds escape near moving witness points",
            stronger_than="counterexample row",
            preserves_continuity=False,
            diagnostic="use as a warning before any limit-continuity claim",
        ),
        FunctionConvergenceRow(
            id="uniform_limit_continuity",
            mode="uniform limit theorem",
            quantifier_pattern="continuity epsilon split plus uniform tail control",
            stronger_than="pointwise convergence",
            preserves_continuity=True,
            diagnostic="bridge to C[0,1] and sup-norm completeness examples",
        ),
    ]


def build_sup_metric_compact_open_bridge() -> List[SupMetricCompactOpenRow]:
    """Return rows comparing sup-metric, point-open, and compact-open topologies."""
    return [
        SupMetricCompactOpenRow(
            id="sup_metric_on_bounded_functions",
            construction="e(f,g)=sup_x d(f(x),g(x))",
            domain_condition="bounded function family or finite supremum",
            topology_output="uniform convergence topology",
            comparison="stronger than pointwise control",
            implementation_note="link to quick-check norms/function metrics forward look",
        ),
        SupMetricCompactOpenRow(
            id="compact_open_contains_point_open",
            construction="F(K,U) subbase with singleton K allowed",
            domain_condition="singletons compact in the domain",
            topology_output="compact-open topology",
            comparison="point-open subbasic constraints appear as singleton compact constraints",
            implementation_note="link to compact-open bridge quality gate",
        ),
        SupMetricCompactOpenRow(
            id="compact_convergence_metric_target",
            construction="uniform convergence on every compact subset",
            domain_condition="topological domain and metric codomain",
            topology_output="compact convergence reading",
            comparison="between pointwise and global uniform convergence in many examples",
            implementation_note="link to function_space_examples FS compact witness tests",
        ),
        SupMetricCompactOpenRow(
            id="c_zero_one_sup_norm",
            construction="continuous functions on a compact interval with sup norm",
            domain_condition="compact interval and real-valued continuous functions",
            topology_output="complete normed function space bridge",
            comparison="feeds Chapter 14 completeness and Chapter 15 function spaces together",
            implementation_note="link to notebooks/exploration/09c_norms_function_metrics_hilbert_glimpse.ipynb",
        ),
    ]


def build_ascoli_equicontinuity_bridge() -> List[AscoliEquicontinuityRow]:
    """Return equicontinuity, uniform boundedness, and Ascoli forward rows."""
    return [
        AscoliEquicontinuityRow(
            id="uniform_boundedness_family",
            property="uniform boundedness",
            uniform_parameter="one bound works for every function and every domain point",
            compactness_role="necessary compactness-side control in C[0,1] examples",
            failure_warning="pointwise boundedness is weaker and should not be substituted without proof",
            manuscript_use="place before equicontinuity as a separate family-level condition",
        ),
        AscoliEquicontinuityRow(
            id="equicontinuity_family",
            property="equicontinuity",
            uniform_parameter="one delta works for every function in the family",
            compactness_role="controls oscillation and supports Ascoli-style compactness statements",
            failure_warning="individual continuity or uniform continuity of each member is not enough by itself",
            manuscript_use="use a common-modulus table rather than a single-function continuity proof",
        ),
        AscoliEquicontinuityRow(
            id="ascoli_forward_pointer",
            property="Ascoli compactness criterion",
            uniform_parameter="closedness plus uniform boundedness plus equicontinuity in the intended setting",
            compactness_role="compactness characterization for selected continuous-function spaces",
            failure_warning="state hypotheses explicitly; do not present a hypothesis-free theorem",
            manuscript_use="keep as forward theorem scaffold with active quality-gate cross-reference",
        ),
        AscoliEquicontinuityRow(
            id="compactness_requires_family_level_control",
            property="family-level compactness diagnostics",
            uniform_parameter="common bounds and common continuity modulus",
            compactness_role="explains why compactness in function spaces is stronger than pointwise examples suggest",
            failure_warning="avoid checking only finitely many sample functions when claiming compactness",
            manuscript_use="attach to examples_bank/function_space_examples.md as a checklist",
        ),
    ]


def build_functional_forward_bridge() -> List[FunctionalForwardBridgeRow]:
    """Return bounded-linear-functional and dual-space forward rows."""
    return [
        FunctionalForwardBridgeRow(
            id="linear_functional_definition",
            object_name="linear functional",
            algebraic_condition="additivity and homogeneity on a normed vector space",
            boundedness_condition="not part of linearity; boundedness is an extra analytic condition",
            norm_or_output="real-valued linear output",
            scope_warning="do not conflate algebraic linearity with continuity",
        ),
        FunctionalForwardBridgeRow(
            id="bounded_functional_continuity_bridge",
            object_name="bounded linear functional",
            algebraic_condition="linear functional on a normed space",
            boundedness_condition="absolute value controlled by a constant times the norm",
            norm_or_output="continuous functional bridge",
            scope_warning="requires normed-space context, not arbitrary topological spaces",
        ),
        FunctionalForwardBridgeRow(
            id="dual_space_norm",
            object_name="dual space preview",
            algebraic_condition="bounded linear functionals form a vector space",
            boundedness_condition="operator norm is the least valid global bound",
            norm_or_output="dual norm and forward Banach-space vocabulary",
            scope_warning="keep as a preview unless the surrounding linear analysis material is present",
        ),
    ]


def build_chapter_15_integration_audit(package_root: str | Path | None = None) -> FunctionSpacesIntegrationAudit:
    """Build an audit summary, optionally checking that active targets exist."""
    root = Path(package_root) if package_root is not None else None
    missing: list[str] = []
    if root is not None:
        missing = [target for target in CHAPTER_15_MANUSCRIPT_TARGETS if not (root / target).exists()]
    return FunctionSpacesIntegrationAudit(
        version=CHAPTER_15_INTEGRATION_VERSION,
        topology_rows=len(build_function_space_topology_bridge()),
        convergence_rows=len(build_function_convergence_bridge()),
        sup_compact_open_rows=len(build_sup_metric_compact_open_bridge()),
        ascoli_rows=len(build_ascoli_equicontinuity_bridge()),
        functional_rows=len(build_functional_forward_bridge()),
        insertion_points=len(CHAPTER_15_INSERTION_POINTS),
        missing_targets=tuple(missing),
        originality_guardrail=(
            "Reference Chapter 15 material is used only for scope calibration; prose, examples, "
            "proofs, exercises, and diagrams are not copied into this module."
        ),
    )


def chapter_15_integration_summary(package_root: str | Path | None = None) -> dict[str, Any]:
    audit = build_chapter_15_integration_audit(package_root)
    return {
        "version": audit.version,
        "topic": "function spaces",
        "ready": audit.ready,
        "blocker_count": audit.blocker_count,
        "topology_rows": audit.topology_rows,
        "convergence_rows": audit.convergence_rows,
        "sup_compact_open_rows": audit.sup_compact_open_rows,
        "ascoli_rows": audit.ascoli_rows,
        "functional_rows": audit.functional_rows,
        "next": "v1.0.330: consolidate Chapter 07--15 integration audit and cross-chapter quality gates",
    }


def render_chapter_15_integration_report(package_root: str | Path | None = None) -> str:
    """Render the Chapter 15 integration bridge as a markdown report."""
    audit = build_chapter_15_integration_audit(package_root)
    lines: list[str] = [
        "# Chapter 15 Function Spaces Integration - v1.0.329",
        "",
        "## Function-space topology bridge",
    ]
    for row in build_function_space_topology_bridge():
        lines.append(f"- `{row.id}`: {row.topology}; data={row.generating_data}; caution={row.caution}")
    lines.extend(["", "## Pointwise, uniform, and compact convergence bridge"])
    for row in build_function_convergence_bridge():
        lines.append(f"- `{row.id}`: {row.mode}; quantifiers={row.quantifier_pattern}; diagnostic={row.diagnostic}")
    lines.extend(["", "## Sup-metric and compact-open topology bridge"])
    for row in build_sup_metric_compact_open_bridge():
        lines.append(f"- `{row.id}`: {row.construction}; comparison={row.comparison}")
    lines.extend(["", "## Equicontinuity and Ascoli forward bridge"])
    for row in build_ascoli_equicontinuity_bridge():
        lines.append(f"- `{row.id}`: {row.property}; warning={row.failure_warning}")
    lines.extend(["", "## Bounded functionals and dual-space preview"])
    for row in build_functional_forward_bridge():
        lines.append(f"- `{row.id}`: {row.object_name}; scope={row.scope_warning}")
    lines.extend([
        "",
        "## Audit",
        f"- Version: `{audit.version}`",
        f"- Topology rows: `{audit.topology_rows}`",
        f"- Convergence rows: `{audit.convergence_rows}`",
        f"- Sup/compact-open rows: `{audit.sup_compact_open_rows}`",
        f"- Ascoli rows: `{audit.ascoli_rows}`",
        f"- Functional rows: `{audit.functional_rows}`",
        f"- Insertion points: `{audit.insertion_points}`",
        f"- Missing targets: `{audit.blocker_count}`",
        f"- Ready: `{audit.ready}`",
        "",
        "## Originality guardrail",
        audit.originality_guardrail,
    ])
    if audit.missing_targets:
        lines.extend(["", "## Missing targets"])
        lines.extend(f"- `{target}`" for target in audit.missing_targets)
    return "\n".join(lines) + "\n"
