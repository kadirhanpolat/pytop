"""Chapter 07 continuity and homeomorphism manuscript integration helpers.

v1.0.321 opens the Chapter 07 integration work described in the v1.0.320
manuscript target map.  The module provides:

- A continuity-criteria bridge that connects the four standard equivalent
  formulations of continuity (preimage-open, closed-set, closure-image,
  neighbourhood) to the active manuscript anchor.
- A homeomorphism invariant transfer contract that enumerates which topological
  properties are transferred under a homeomorphism and which are not.
- An initial-topology forward pointer that records the subbase/coarsest-topology
  characterisation as a bridge to later product and function-space chapters.
- A Chapter 07 integration audit helper that checks whether the active manuscript
  anchor files are present.

Originality guardrails
----------------------
All prose, examples, and exercise wording in this module is written in the
book voice and derived from the active API / examples_bank.  Nothing is copied
directly from the uploaded Chapter 07 zip reference files.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .result import Result

CHAPTER_07_INTEGRATION_VERSION = "v1.0.321"

# ---------------------------------------------------------------------------
# Continuity-criteria bridge
# ---------------------------------------------------------------------------

CONTINUITY_CRITERIA = (
    {
        "id": "preimage_open",
        "label": "Preimage-open criterion",
        "statement": (
            "f : X → Y is continuous iff for every open H ⊆ Y the preimage "
            "f⁻¹[H] is open in X."
        ),
        "manuscript_anchor": "continuity/homeomorphism route anchored in Volume 1 continuity material",
        "bridge_note": (
            "This is the definition used throughout the API (maps.py / infinite_maps.py). "
            "The bridge box should reference is_continuous_map and the exact tag 'continuous'."
        ),
    },
    {
        "id": "closed_set",
        "label": "Closed-set criterion",
        "statement": (
            "f : X → Y is continuous iff for every closed F ⊆ Y the preimage "
            "f⁻¹[F] is closed in X."
        ),
        "manuscript_anchor": "continuity/homeomorphism route anchored in Volume 1 continuity material",
        "bridge_note": (
            "Theorem 7.3 in the reference text. "
            "The exact finite map analyser in maps.py checks this via complement duality."
        ),
    },
    {
        "id": "closure_image",
        "label": "Closure-image criterion",
        "statement": (
            "f : X → Y is continuous iff f[Ā] ⊆ f[A]̄ for every A ⊆ X, "
            "i.e. f preserves arbitrary closeness."
        ),
        "manuscript_anchor": "continuity/homeomorphism route anchored in Volume 1 continuity material",
        "bridge_note": (
            "Theorem 7.4 in the reference text.  "
            "The satisfies_closure_image_inclusion helper in maps.py tests this directly."
        ),
    },
    {
        "id": "neighbourhood",
        "label": "Neighbourhood / pointwise criterion",
        "statement": (
            "f : X → Y is continuous at p iff for every neighbourhood N of f(p) "
            "the preimage f⁻¹[N] is a neighbourhood of p. "
            "f is globally continuous iff it is continuous at every point of X."
        ),
        "manuscript_anchor": "continuity/homeomorphism route anchored in Volume 1 continuity material",
        "bridge_note": (
            "Theorem 7.5 and the local continuity definition in the reference text. "
            "The is_continuous_at_point helper in maps.py implements this for finite spaces."
        ),
    },
)


@dataclass(frozen=True, slots=True)
class ContinuityCriterionRow:
    """One continuity criterion with its manuscript bridge note."""

    id: str
    label: str
    statement: str
    manuscript_anchor: str
    bridge_note: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "statement": self.statement,
            "manuscript_anchor": self.manuscript_anchor,
            "bridge_note": self.bridge_note,
        }


def build_continuity_criteria_bridge() -> tuple[ContinuityCriterionRow, ...]:
    """Return the four standard continuity criteria as bridge rows."""
    return tuple(ContinuityCriterionRow(**c) for c in CONTINUITY_CRITERIA)


# ---------------------------------------------------------------------------
# Homeomorphism invariant transfer contract
# ---------------------------------------------------------------------------

HOMEOMORPHISM_INVARIANTS = (
    {"property": "connectedness", "transferred": True,
     "note": "A homeomorphism maps connected spaces to connected spaces (Example 4.3 in reference)."},
    {"property": "compactness", "transferred": True,
     "note": "Continuous images of compact spaces are compact; homeomorphisms are bijective and continuous."},
    {"property": "separation axiom T0", "transferred": True,
     "note": "T0 is a topological invariant; a homeomorphism preserves the distinguishability of points."},
    {"property": "separation axiom T1", "transferred": True,
     "note": "Singleton-closed sets are preserved under homeomorphism."},
    {"property": "Hausdorff (T2)", "transferred": True,
     "note": "The ability to separate points by open sets is preserved."},
    {"property": "first countability", "transferred": True,
     "note": "Existence of a countable local base at each point is preserved."},
    {"property": "second countability", "transferred": True,
     "note": "Existence of a countable base for the whole topology is preserved."},
    {"property": "cardinality of the carrier set", "transferred": True,
     "note": "A homeomorphism is bijective, so carrier cardinalities agree."},
    {"property": "length / measure", "transferred": False,
     "note": "Example 4.1: R is homeomorphic to (-1,1); they have different lengths."},
    {"property": "boundedness", "transferred": False,
     "note": "Example 4.1: (-1,1) is bounded; R is not. They are homeomorphic."},
    {"property": "Cauchy-sequence property", "transferred": False,
     "note": "Example 4.2: the reciprocal homeomorphism on (0,∞) turns a Cauchy sequence into a non-Cauchy one."},
    {"property": "completeness", "transferred": False,
     "note": "Completeness is a metric property, not a topological invariant."},
    {"property": "area", "transferred": False,
     "note": "Problem 23 in reference: discs of different radii are homeomorphic."},
)


@dataclass(frozen=True, slots=True)
class HomeomorphismInvariantRow:
    """One property with its homeomorphism transfer status."""

    property: str
    transferred: bool
    note: str

    @property
    def status(self) -> str:
        return "topological_invariant" if self.transferred else "not_topological_invariant"

    def to_dict(self) -> dict[str, Any]:
        return {
            "property": self.property,
            "transferred": self.transferred,
            "status": self.status,
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class HomeomorphismInvariantContract:
    """Aggregate invariant transfer contract for the Chapter 07 bridge."""

    version: str
    rows: tuple[HomeomorphismInvariantRow, ...]

    @property
    def invariant_count(self) -> int:
        return sum(1 for r in self.rows if r.transferred)

    @property
    def non_invariant_count(self) -> int:
        return sum(1 for r in self.rows if not r.transferred)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "invariant_count": self.invariant_count,
            "non_invariant_count": self.non_invariant_count,
            "rows": [r.to_dict() for r in self.rows],
        }

    def to_result(self) -> Result:
        return Result(
            status="true",
            mode="exact",
            value=self.to_dict(),
            justification=[
                "Chapter 07 homeomorphism invariant transfer contract built.",
                f"{self.invariant_count} topological invariants listed.",
                f"{self.non_invariant_count} non-invariant metric/measure properties listed.",
            ],
            metadata=self.to_dict(),
        )


def build_homeomorphism_invariant_contract() -> HomeomorphismInvariantContract:
    """Build the Chapter 07 homeomorphism invariant transfer contract."""
    rows = tuple(HomeomorphismInvariantRow(**r) for r in HOMEOMORPHISM_INVARIANTS)
    return HomeomorphismInvariantContract(
        version=CHAPTER_07_INTEGRATION_VERSION,
        rows=rows,
    )


# ---------------------------------------------------------------------------
# Initial-topology forward pointer
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class InitialTopologyForwardPointer:
    """Bridge record linking the Chapter 07 initial-topology section to later chapters."""

    version: str
    statement: str
    subbase_characterisation: str
    coarsest_topology_note: str
    forward_pointers: tuple[str, ...]
    api_references: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "statement": self.statement,
            "subbase_characterisation": self.subbase_characterisation,
            "coarsest_topology_note": self.coarsest_topology_note,
            "forward_pointers": list(self.forward_pointers),
            "api_references": list(self.api_references),
        }


def build_initial_topology_forward_pointer() -> InitialTopologyForwardPointer:
    """Build the Chapter 07 initial-topology bridge forward pointer."""
    return InitialTopologyForwardPointer(
        version=CHAPTER_07_INTEGRATION_VERSION,
        statement=(
            "Given a family of functions {fᵢ : X → (Yᵢ, Tᵢ)}, the initial topology "
            "on X is the coarsest topology making every fᵢ continuous. "
            "Its defining subbase is ⋃ᵢ {fᵢ⁻¹[H] : H ∈ Tᵢ}."
        ),
        subbase_characterisation=(
            "Theorem 7.8: The collection δ = ⋃ᵢ {fᵢ⁻¹[H] : H ∈ Tᵢ} is a subbase for "
            "the initial topology.  A function g : Z → X is continuous with respect to "
            "the initial topology iff every fᵢ ∘ g is continuous."
        ),
        coarsest_topology_note=(
            "The initial topology is the intersection of all topologies on X making "
            "every fᵢ continuous.  This is Theorem 7.8(ii) and (iii) in the reference."
        ),
        forward_pointers=(
            "Chapter 12 product topology: the product topology on ∏Xᵢ is the initial topology "
            "induced by the projection maps πⱼ : ∏Xᵢ → Xⱼ.",
            "Chapter 15 function spaces: the pointwise-convergence topology on Yˣ is the "
            "initial topology induced by the evaluation maps evₓ : Yˣ → Y.",
        ),
        api_references=(
            "maps.initial_topology_from_maps",
            "subbases.generate_topology_from_subbasis",
            "infinite_maps.analyze_infinite_map_property",
        ),
    )


# ---------------------------------------------------------------------------
# Chapter 07 integration audit
# ---------------------------------------------------------------------------

CHAPTER_07_MANUSCRIPT_TARGETS = (
    "src/pytop/maps.py",
    "src/pytop/infinite_maps.py",
    "src/pytop/chapter_07_continuity_integration.py",
    "docs/integration/chapter_07_15/chapter_07_continuity_integration_v1_0_321.md",
    "docs/verification/chapter_07_continuity_integration_v1_0_321.md",
    "tests/core/test_chapter_07_continuity_integration_v321.py",
)

CHAPTER_07_INSERTION_POINTS = (
    "add a continuity criteria bridge box in the manuscript continuity section",
    "add a homeomorphism invariant transfer warning in the topological properties section",
    "add an initial-topology forward pointer at the end of the induced-topology section",
)


@dataclass(frozen=True, slots=True)
class Chapter07IntegrationAudit:
    """Audit result for the Chapter 07 v1.0.321 integration."""

    version: str
    present_targets: tuple[str, ...]
    missing_targets: tuple[str, ...]
    insertion_points: tuple[str, ...]
    continuity_criteria_count: int
    invariant_count: int
    non_invariant_count: int

    @property
    def blocker_count(self) -> int:
        return len(self.missing_targets)

    @property
    def status(self) -> str:
        return "ready" if self.blocker_count == 0 else "blocked"

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status,
            "blocker_count": self.blocker_count,
            "present_targets": list(self.present_targets),
            "missing_targets": list(self.missing_targets),
            "insertion_points": list(self.insertion_points),
            "continuity_criteria_count": self.continuity_criteria_count,
            "invariant_count": self.invariant_count,
            "non_invariant_count": self.non_invariant_count,
        }

    def to_result(self) -> Result:
        return Result(
            status=self.status,
            mode="exact",
            value=self.to_dict(),
            justification=[
                f"Chapter 07 v1.0.321 integration audit: {self.status}.",
                f"Manuscript targets present: {len(self.present_targets)}.",
                f"Manuscript targets missing: {self.blocker_count}.",
                f"Continuity criteria bridged: {self.continuity_criteria_count}.",
                f"Homeomorphism invariants: {self.invariant_count} invariant, "
                f"{self.non_invariant_count} non-invariant.",
            ],
            metadata=self.to_dict(),
        )


def build_chapter_07_integration_audit(package_root: str | Path) -> Chapter07IntegrationAudit:
    """Build the Chapter 07 v1.0.321 integration audit report."""
    root = Path(package_root)
    present = tuple(t for t in CHAPTER_07_MANUSCRIPT_TARGETS if (root / t).exists())
    missing = tuple(t for t in CHAPTER_07_MANUSCRIPT_TARGETS if t not in present)
    criteria = build_continuity_criteria_bridge()
    contract = build_homeomorphism_invariant_contract()
    return Chapter07IntegrationAudit(
        version=CHAPTER_07_INTEGRATION_VERSION,
        present_targets=present,
        missing_targets=missing,
        insertion_points=CHAPTER_07_INSERTION_POINTS,
        continuity_criteria_count=len(criteria),
        invariant_count=contract.invariant_count,
        non_invariant_count=contract.non_invariant_count,
    )


# ---------------------------------------------------------------------------
# Top-level summary
# ---------------------------------------------------------------------------

def chapter_07_integration_summary(package_root: str | Path) -> dict[str, Any]:
    """Return a combined Chapter 07 v1.0.321 integration summary dict."""
    audit = build_chapter_07_integration_audit(package_root)
    criteria = build_continuity_criteria_bridge()
    contract = build_homeomorphism_invariant_contract()
    pointer = build_initial_topology_forward_pointer()
    return {
        "version": CHAPTER_07_INTEGRATION_VERSION,
        "audit": audit.to_dict(),
        "continuity_criteria_bridge": [c.to_dict() for c in criteria],
        "homeomorphism_invariant_contract": contract.to_dict(),
        "initial_topology_forward_pointer": pointer.to_dict(),
    }


def render_chapter_07_integration_report(package_root: str | Path) -> str:
    """Render a Markdown integration report for Chapter 07 v1.0.321."""
    summary = chapter_07_integration_summary(package_root)
    audit = summary["audit"]
    contract = summary["homeomorphism_invariant_contract"]
    pointer = summary["initial_topology_forward_pointer"]
    criteria = summary["continuity_criteria_bridge"]

    lines = [
        f"# Chapter 07 Continuity Integration Report - {CHAPTER_07_INTEGRATION_VERSION}",
        "",
        "## Audit",
        "",
        f"- Status: `{audit['status']}`",
        f"- Blocker count: `{audit['blocker_count']}`",
        f"- Present manuscript targets: `{len(audit['present_targets'])}`",
        f"- Missing manuscript targets: `{audit['blocker_count']}`",
        "",
        "## Continuity criteria bridge",
        "",
        "| ID | Label | Manuscript anchor |",
        "|---|---|---|",
    ]
    for c in criteria:
        lines.append(f"| `{c['id']}` | {c['label']} | {c['manuscript_anchor']} |")

    lines.extend([
        "",
        "## Homeomorphism invariant transfer contract",
        "",
        f"- Topological invariants: `{contract['invariant_count']}`",
        f"- Non-invariants: `{contract['non_invariant_count']}`",
        "",
        "| Property | Status | Note |",
        "|---|---|---|",
    ])
    for r in contract["rows"]:
        lines.append(f"| {r['property']} | `{r['status']}` | {r['note']} |")

    lines.extend([
        "",
        "## Initial-topology forward pointer",
        "",
        pointer["statement"],
        "",
        f"**Subbase characterisation:** {pointer['subbase_characterisation']}",
        "",
        "**Forward pointers:**",
        "",
    ])
    for fp in pointer["forward_pointers"]:
        lines.append(f"- {fp}")

    lines.extend([
        "",
        "## Insertion points",
        "",
    ])
    for ip in audit["insertion_points"]:
        lines.append(f"- {ip}")

    lines.extend([
        "",
        "## Originality guardrails",
        "",
        "- Do not copy prose, examples, or exercises directly from uploaded chapter zips.",
        "- Rewrite examples in the book voice; keep examples_bank as the reusable source.",
        "- Use this report as the contract, not as prose to copy into the manuscript.",
    ])
    return "\n".join(lines) + "\n"
