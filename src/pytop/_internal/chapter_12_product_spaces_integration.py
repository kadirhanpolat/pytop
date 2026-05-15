"""Chapter 12 product-spaces manuscript integration - v1.0.326.

This module opens the Chapter 12 product-spaces integration track described
in the active Chapter 07--15 target map.  It records product topology, box
topology, projection/subbase, coordinate convergence, and preservation bridges
in a machine-readable form that can be consumed by tests, documentation, and
future manuscript edits.

Roadmap correction
------------------
The v1.0.320 target map assigns v1.0.326 to Chapter 12 product spaces and
v1.0.327 to Chapter 13 connectedness.  A later v1.0.325 roadmap line used
"Chapter 12 connectedness" by mistake.  This module follows the target map:
Chapter 12 = product spaces; connectedness remains the Chapter 13/v1.0.327
track.

Originality guardrails
----------------------
All wording is synthesised from standard topology and the active pytop API
surface.  Uploaded chapter zip files are used only as reference inputs; no
external prose, problem text, exercise wording, or proof wording is copied.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, List

from pytop.result import Result

# ---------------------------------------------------------------------------
# Version and active targets
# ---------------------------------------------------------------------------

CHAPTER_12_INTEGRATION_VERSION: str = "v1.0.326"

CHAPTER_12_MANUSCRIPT_TARGETS: List[str] = [
    "manuscript/volume_1/chapters/08_products.tex",
    "src/pytop/products.py",
    "src/pytop/construction_contracts.py",
    "src/pytop/metric_contracts.py",
    "examples_bank/product_space_examples.md",
    "examples_bank/construction_bridge_examples.md",
    "docs/questionbank/chapter_12_product_spaces_family_draft_v1_0_210.md",
    "tests/core/test_chapter_12_product_spaces_integration_v326.py",
    "docs/integration/chapter_07_15/chapter_12_product_spaces_integration_v1_0_326.md",
]

CHAPTER_12_INSERTION_POINTS: List[str] = [
    "product topology as the initial topology induced by the projections",
    "product topology versus box topology distinction table",
    "coordinatewise convergence and Tychonoff forward-pointer box",
]

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ProductTopologyRow:
    """One construction row in the product-topology bridge."""

    id: str
    label: str
    construction: str
    universal_property: str
    api_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProductBoxDistinctionRow:
    """One row contrasting product and box topology behaviour."""

    id: str
    construction: str
    basis_description: str
    projection_maps_continuous: bool
    agrees_with_product_for_finite_families: bool
    warning: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProjectionSubbaseRow:
    """One projection preimage/subbase bridge row."""

    id: str
    projection: str
    inverse_image_form: str
    role: str
    contract_reference: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProductPreservationRow:
    """One property-preservation row for product spaces."""

    property: str
    finite_product_status: str
    arbitrary_product_status: str
    caveat: str
    api_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CoordinateConvergenceRow:
    """One coordinate-convergence bridge row."""

    id: str
    setting: str
    criterion: str
    product_topology_valid: bool
    box_topology_warning: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProductSpacesIntegrationAudit:
    """Audit summary for the Chapter 12 product-spaces integration surface."""

    version: str
    product_topology_rows: int
    box_distinction_rows: int
    projection_subbase_rows: int
    preservation_rows: int
    coordinate_convergence_rows: int
    insertion_points: int
    missing_targets: tuple[str, ...]
    roadmap_correction: str

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
                "Chapter 12 follows the v1.0.320 target map: product spaces.",
                "Uploaded Chapter 12 reference material is not copied verbatim.",
            ],
            justification=[
                f"Product topology bridge rows: {self.product_topology_rows}.",
                f"Product/box distinction rows: {self.box_distinction_rows}.",
                f"Projection/subbase rows: {self.projection_subbase_rows}.",
                f"Preservation rows: {self.preservation_rows}.",
                f"Coordinate-convergence rows: {self.coordinate_convergence_rows}.",
                f"Missing active targets: {self.blocker_count}.",
            ],
            metadata=self.to_dict(),
        )


# ---------------------------------------------------------------------------
# Product topology bridge
# ---------------------------------------------------------------------------

def build_product_topology_bridge() -> List[ProductTopologyRow]:
    """Return the core product-topology construction bridge rows."""
    return [
        ProductTopologyRow(
            id="finite_product_basis",
            label="Finite product topology",
            construction=(
                "For finitely many spaces X1,...,Xn, basic open sets are finite "
                "rectangles U1×...×Un with each Ui open in Xi."
            ),
            universal_property=(
                "A map g: Z → X1×...×Xn is continuous exactly when all coordinate "
                "maps pi_i∘g are continuous."
            ),
            api_note="pytop.products.binary_product and pytop.products.product compute finite products exactly.",
        ),
        ProductTopologyRow(
            id="arbitrary_product_initial",
            label="Arbitrary product topology",
            construction=(
                "For a family (Xi)i∈I, the product topology is generated by the "
                "subbase pi_i^{-1}(Ui), where Ui is open in Xi and i ranges over I."
            ),
            universal_property=(
                "It is the coarsest topology on ∏Xi making every projection pi_i continuous."
            ),
            api_note="pytop.infinite_constructions.product records symbolic arbitrary products.",
        ),
        ProductTopologyRow(
            id="projection_subbase",
            label="Projection subbase viewpoint",
            construction=(
                "Finite intersections of projection preimages give cylinders; arbitrary "
                "unions of cylinders give product-open sets."
            ),
            universal_property=(
                "The subbase formulation is the bridge between continuity criteria and product construction."
            ),
            api_note="pytop.construction_contracts.finite_product_contract supplies finite carrier contracts.",
        ),
        ProductTopologyRow(
            id="metric_product_bridge",
            label="Metric product bridge",
            construction=(
                "For finite metric factors, a max, sum, or Euclidean-style product metric "
                "can induce the same finite product topology."
            ),
            universal_property=(
                "Metric validation should be separated from the purely topological product carrier."
            ),
            api_note="pytop.metric_contracts.finite_product_metric_contract validates finite product metrics.",
        ),
    ]


# ---------------------------------------------------------------------------
# Product topology versus box topology
# ---------------------------------------------------------------------------

def build_product_box_distinction_bridge() -> List[ProductBoxDistinctionRow]:
    """Return rows distinguishing product topology and box topology."""
    return [
        ProductBoxDistinctionRow(
            id="finite_family_agreement",
            construction="finite products",
            basis_description="All rectangle bases use only finitely many factors, so product and box bases agree.",
            projection_maps_continuous=True,
            agrees_with_product_for_finite_families=True,
            warning="For finite products there is no product/box discrepancy, so examples must use infinite families.",
        ),
        ProductBoxDistinctionRow(
            id="product_topology_cylinders",
            construction="product topology on an infinite family",
            basis_description="Basic opens restrict only finitely many coordinates and leave all other factors unrestricted.",
            projection_maps_continuous=True,
            agrees_with_product_for_finite_families=True,
            warning="This topology is intentionally coarse enough for coordinatewise continuity and convergence.",
        ),
        ProductBoxDistinctionRow(
            id="box_topology_rectangles",
            construction="box topology on an infinite family",
            basis_description="Basic opens are full boxes ∏Ui, allowing every coordinate to be restricted at once.",
            projection_maps_continuous=True,
            agrees_with_product_for_finite_families=True,
            warning="The box topology is usually strictly finer and may break coordinatewise convergence intuition.",
        ),
        ProductBoxDistinctionRow(
            id="sequence_space_warning",
            construction="sequence-space example family",
            basis_description="In countable products, box-neighbourhoods can require simultaneous control in every coordinate.",
            projection_maps_continuous=True,
            agrees_with_product_for_finite_families=False,
            warning="A sequence may converge coordinatewise in the product topology but fail in the box topology.",
        ),
    ]


# ---------------------------------------------------------------------------
# Projection/subbase bridge
# ---------------------------------------------------------------------------

def build_projection_subbase_bridge() -> List[ProjectionSubbaseRow]:
    """Return projection preimage rows for manuscript and contract alignment."""
    return [
        ProjectionSubbaseRow(
            id="left_projection",
            projection="pi_1 : X×Y → X",
            inverse_image_form="pi_1^{-1}(U) = U×Y",
            role="Generates left cylinders in the finite binary product topology.",
            contract_reference="pytop.products.binary_product",
        ),
        ProjectionSubbaseRow(
            id="right_projection",
            projection="pi_2 : X×Y → Y",
            inverse_image_form="pi_2^{-1}(V) = X×V",
            role="Generates right cylinders in the finite binary product topology.",
            contract_reference="pytop.products.binary_product",
        ),
        ProjectionSubbaseRow(
            id="indexed_projection",
            projection="pi_j : ∏_{i∈I} Xi → Xj",
            inverse_image_form="pi_j^{-1}(Uj) = ∏Wi, with Wj=Uj and Wi=Xi for i≠j",
            role="Defines the standard subbase for the arbitrary product topology.",
            contract_reference="pytop.infinite_constructions.product",
        ),
        ProjectionSubbaseRow(
            id="coordinate_test",
            projection="coordinate maps of g: Z → ∏Xi",
            inverse_image_form="(pi_j∘g)^{-1}(Uj) = g^{-1}(pi_j^{-1}(Uj))",
            role="Converts continuity into coordinatewise continuity checks.",
            contract_reference="pytop.result_rendering.render_result",
        ),
    ]


# ---------------------------------------------------------------------------
# Preservation bridge
# ---------------------------------------------------------------------------

def build_product_preservation_bridge() -> List[ProductPreservationRow]:
    """Return preservation rows used by Chapter 12 product-space exposition."""
    return [
        ProductPreservationRow(
            property="Hausdorff / T2",
            finite_product_status="preserved",
            arbitrary_product_status="preserved",
            caveat="All factors must be Hausdorff; the conclusion is for the product topology.",
            api_note="links to src/pytop/separation.py and finite negative-witness surfaces",
        ),
        ProductPreservationRow(
            property="T0 and T1 separation",
            finite_product_status="preserved",
            arbitrary_product_status="preserved",
            caveat="The proof is coordinatewise and uses projections to separate unequal coordinates.",
            api_note="links to src/pytop/separation.py",
        ),
        ProductPreservationRow(
            property="connectedness",
            finite_product_status="preserved",
            arbitrary_product_status="preserved",
            caveat="Connectedness of all factors is required; empty-factor edge cases must be handled separately.",
            api_note="links to src/pytop/connectedness.py and future Chapter 13 work",
        ),
        ProductPreservationRow(
            property="compactness",
            finite_product_status="preserved",
            arbitrary_product_status="preserved by Tychonoff",
            caveat="The arbitrary-product statement uses Tychonoff's theorem and therefore belongs in a forward-pointer box.",
            api_note="links to src/pytop/compactness.py and Chapter 11 compactness bridge",
        ),
        ProductPreservationRow(
            property="second countability",
            finite_product_status="preserved",
            arbitrary_product_status="not preserved in general",
            caveat="Countable products of second-countable spaces are second countable; arbitrary products can fail.",
            api_note="links to src/pytop/countability.py",
        ),
        ProductPreservationRow(
            property="metrizability",
            finite_product_status="preserved for metric factors",
            arbitrary_product_status="not preserved in general",
            caveat="Countable products of metrizable spaces are metrizable under standard product metrics; arbitrary products require caution.",
            api_note="links to src/pytop/metric_contracts.py and src/pytop/metric_spaces.py",
        ),
    ]


# ---------------------------------------------------------------------------
# Coordinate convergence bridge
# ---------------------------------------------------------------------------

def build_coordinate_convergence_bridge() -> List[CoordinateConvergenceRow]:
    """Return coordinate-convergence bridge rows."""
    return [
        CoordinateConvergenceRow(
            id="net_product_topology",
            setting="nets in arbitrary products",
            criterion="A net converges in the product topology iff every coordinate net converges in its factor.",
            product_topology_valid=True,
            box_topology_warning="The coordinatewise criterion does not characterise box-topology convergence in general.",
        ),
        CoordinateConvergenceRow(
            id="sequence_countable_metric",
            setting="sequences in countable metric products",
            criterion="For common countable metric products, sequence convergence is checked coordinate by coordinate.",
            product_topology_valid=True,
            box_topology_warning="Box neighbourhoods may demand uniform control over infinitely many coordinates.",
        ),
        CoordinateConvergenceRow(
            id="finite_metric_product",
            setting="finite product metric spaces",
            criterion="Convergence under max/sum product metrics agrees with coordinatewise convergence.",
            product_topology_valid=True,
            box_topology_warning="Finite products have no product/box distinction.",
        ),
        CoordinateConvergenceRow(
            id="tychonoff_pointer",
            setting="compact product families",
            criterion="Coordinate projections are the natural language for stating compactness of arbitrary products.",
            product_topology_valid=True,
            box_topology_warning="Tychonoff is a product-topology theorem, not a box-topology theorem.",
        ),
    ]


# ---------------------------------------------------------------------------
# Audit, summary, rendering
# ---------------------------------------------------------------------------

def build_chapter_12_integration_audit(root: Path | str | None = None) -> ProductSpacesIntegrationAudit:
    """Build the Chapter 12 integration audit for an extracted package root."""
    root_path = Path(root) if root is not None else Path.cwd()
    missing = tuple(
        rel for rel in CHAPTER_12_MANUSCRIPT_TARGETS
        if not (root_path / rel).exists()
    )
    return ProductSpacesIntegrationAudit(
        version=CHAPTER_12_INTEGRATION_VERSION,
        product_topology_rows=len(build_product_topology_bridge()),
        box_distinction_rows=len(build_product_box_distinction_bridge()),
        projection_subbase_rows=len(build_projection_subbase_bridge()),
        preservation_rows=len(build_product_preservation_bridge()),
        coordinate_convergence_rows=len(build_coordinate_convergence_bridge()),
        insertion_points=len(CHAPTER_12_INSERTION_POINTS),
        missing_targets=missing,
        roadmap_correction=(
            "v1.0.326 follows the v1.0.320 target map: Chapter 12 product spaces. "
            "The connectedness item belongs to Chapter 13/v1.0.327."
        ),
    )


def chapter_12_integration_summary(root: Path | str | None = None) -> dict[str, Any]:
    """Return a compact machine-readable summary of the v1.0.326 bridge."""
    audit = build_chapter_12_integration_audit(root)
    return {
        "version": CHAPTER_12_INTEGRATION_VERSION,
        "topic": "product spaces",
        "product_topology_rows": audit.product_topology_rows,
        "box_distinction_rows": audit.box_distinction_rows,
        "projection_subbase_rows": audit.projection_subbase_rows,
        "preservation_rows": audit.preservation_rows,
        "coordinate_convergence_rows": audit.coordinate_convergence_rows,
        "insertion_points": list(CHAPTER_12_INSERTION_POINTS),
        "blocker_count": audit.blocker_count,
        "ready": audit.ready,
        "next": "v1.0.327 Chapter 13 connectedness and path-connectedness integration",
    }


def render_chapter_12_integration_report(root: Path | str | None = None) -> str:
    """Render a human-readable Chapter 12 integration report."""
    audit = build_chapter_12_integration_audit(root)
    lines: list[str] = [
        f"# Chapter 12 Product-Spaces Integration Report - {CHAPTER_12_INTEGRATION_VERSION}",
        "",
        "## Roadmap correction",
        audit.roadmap_correction,
        "",
        "## Product topology bridge",
    ]
    for row in build_product_topology_bridge():
        lines.append(f"- **{row.label}** (`{row.id}`): {row.construction} API: {row.api_note}")
    lines.extend(["", "## Product/box distinction"])
    for row in build_product_box_distinction_bridge():
        lines.append(f"- **{row.construction}**: {row.basis_description} Warning: {row.warning}")
    lines.extend(["", "## Projection/subbase bridge"])
    for row in build_projection_subbase_bridge():
        lines.append(f"- `{row.projection}`: `{row.inverse_image_form}` — {row.role}")
    lines.extend(["", "## Preservation bridge"])
    for row in build_product_preservation_bridge():
        lines.append(f"- **{row.property}**: finite={row.finite_product_status}; arbitrary={row.arbitrary_product_status}. {row.caveat}")
    lines.extend(["", "## Coordinate convergence"])
    for row in build_coordinate_convergence_bridge():
        lines.append(f"- **{row.setting}**: {row.criterion} Box warning: {row.box_topology_warning}")
    lines.extend([
        "",
        "## Audit",
        f"- Product topology rows: `{audit.product_topology_rows}`",
        f"- Product/box distinction rows: `{audit.box_distinction_rows}`",
        f"- Projection/subbase rows: `{audit.projection_subbase_rows}`",
        f"- Preservation rows: `{audit.preservation_rows}`",
        f"- Coordinate-convergence rows: `{audit.coordinate_convergence_rows}`",
        f"- Insertion points: `{audit.insertion_points}`",
        f"- Missing targets: `{audit.blocker_count}`",
        f"- Ready: `{audit.ready}`",
        "",
        "## Originality guardrail",
        "Uploaded Chapter 12 zip material remains reference-only; manuscript prose, examples, and exercises must be written in the project voice.",
    ])
    if audit.missing_targets:
        lines.extend(["", "## Missing targets"])
        lines.extend(f"- `{p}`" for p in audit.missing_targets)
    return "\n".join(lines) + "\n"


__all__ = [
    "CHAPTER_12_INTEGRATION_VERSION",
    "CHAPTER_12_MANUSCRIPT_TARGETS",
    "CHAPTER_12_INSERTION_POINTS",
    "ProductTopologyRow",
    "ProductBoxDistinctionRow",
    "ProjectionSubbaseRow",
    "ProductPreservationRow",
    "CoordinateConvergenceRow",
    "ProductSpacesIntegrationAudit",
    "build_product_topology_bridge",
    "build_product_box_distinction_bridge",
    "build_projection_subbase_bridge",
    "build_product_preservation_bridge",
    "build_coordinate_convergence_bridge",
    "build_chapter_12_integration_audit",
    "chapter_12_integration_summary",
    "render_chapter_12_integration_report",
]
