"""Chapter 09 countability / local-base manuscript integration - v1.0.323.

Bridges first countability (C1), second countability (C2), separability,
and Lindelöf spaces to the active manuscript anchor and API surface.

Originality guardrails
----------------------
All content is synthesised from standard topology knowledge.
Do **not** copy verbatim from any uploaded chapter zip.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

from pytop.result import Result

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

CHAPTER_09_INTEGRATION_VERSION: str = "v1.0.323"

# ---------------------------------------------------------------------------
# Manuscript targets and insertion points
# ---------------------------------------------------------------------------

CHAPTER_09_MANUSCRIPT_TARGETS: List[str] = [
    "src/pytop/chapter_09_countability_integration.py",
    "src/pytop/countability.py",
    "src/pytop/metric_spaces.py",
    "src/pytop/base_theory.py",
    "src/pytop/separation.py",
    "tests/core/test_chapter_09_countability_integration_v323.py",
    "docs/integration/chapter_07_15/chapter_09_countability_integration_v1_0_323.md",
]

CHAPTER_09_INSERTION_POINTS: List[str] = [
    "local-base diagnostic table (C1 vs C2 comparison)",
    "separability / Lindelöf comparison warning box",
    "implication-chain diagram (C2 → C1, C2 → S, S+metric → C2)",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CountabilityAxiomRow:
    """One row in the countability-axiom bridge table."""
    id: str           # e.g. "C1", "C2"
    label: str
    definition: str
    api_note: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ImplicationRow:
    """One directed implication between countability properties."""
    id: str
    source: str
    target: str
    direction: str          # "=>" or "<=>"
    converse_holds: bool
    counterexample: str     # counterexample when converse fails

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CountabilityTheoremRow:
    """A key theorem in Chapter 09."""
    id: str           # e.g. "9.1", "9.3"
    label: str
    statement: str
    proof_sketch: str
    api_note: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HereditaryRow:
    """Whether a property is hereditary (preserved by subspaces)."""
    id: str
    property_name: str
    hereditary: bool
    note: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Bridges
# ---------------------------------------------------------------------------

def build_countability_axiom_bridge() -> List[CountabilityAxiomRow]:
    """Return the C1 / C2 / S / L countability-axiom bridge (4 rows)."""
    return [
        CountabilityAxiomRow(
            id="C1",
            label="First countability",
            definition=(
                "A topological space X is first countable (C1) if every point "
                "x ∈ X has a countable neighbourhood base {Bₙ(x) : n ∈ ℕ}."
            ),
            api_note=(
                "pytop.countability.is_first_countable(space) returns True when "
                "every point has a countable local base."
            ),
        ),
        CountabilityAxiomRow(
            id="C2",
            label="Second countability",
            definition=(
                "A topological space X is second countable (C2) if its topology "
                "has a countable base ℬ (a single countable collection of open "
                "sets that generates all open sets)."
            ),
            api_note=(
                "pytop.countability.is_second_countable(space) checks for a "
                "countable global base."
            ),
        ),
        CountabilityAxiomRow(
            id="S",
            label="Separability",
            definition=(
                "A topological space X is separable if it contains a countable "
                "dense subset D ⊆ X (i.e. cl(D) = X)."
            ),
            api_note=(
                "pytop.countability.is_separable(space) returns True when a "
                "countable dense subset exists."
            ),
        ),
        CountabilityAxiomRow(
            id="L",
            label="Lindelöf property",
            definition=(
                "A topological space X is Lindelöf if every open cover of X "
                "has a countable subcover."
            ),
            api_note=(
                "pytop.countability.is_lindelof(space) verifies every open cover "
                "reduces to a countable one."
            ),
        ),
    ]


@dataclass(frozen=True, slots=True)
class ImplicationChainBridge:
    """Full implication chain among C1, C2, S, L."""
    version: str
    rows: List[ImplicationRow]
    summary: str
    api_reference: str

    @property
    def implication_count(self) -> int:
        return len(self.rows)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "rows": [r.to_dict() for r in self.rows],
            "summary": self.summary,
            "api_reference": self.api_reference,
        }


def build_implication_chain_bridge() -> ImplicationChainBridge:
    """Build the countability implication-chain bridge."""
    rows = [
        ImplicationRow(
            id="C2_implies_C1",
            source="C2",
            target="C1",
            direction="=>",
            converse_holds=False,
            counterexample=(
                "The uncountable discrete space is C1 (singleton local bases) "
                "but not C2 (no countable global base)."
            ),
        ),
        ImplicationRow(
            id="C2_implies_S",
            source="C2",
            target="S",
            direction="=>",
            converse_holds=False,
            counterexample=(
                "The Sorgenfrey line is separable (ℚ is dense) but not C2."
            ),
        ),
        ImplicationRow(
            id="C2_implies_L",
            source="C2",
            target="L",
            direction="=>",
            converse_holds=False,
            counterexample=(
                "The Sorgenfrey line is Lindelöf but not C2."
            ),
        ),
        ImplicationRow(
            id="S_metric_implies_C2",
            source="S (metric)",
            target="C2",
            direction="=>",
            converse_holds=True,
            counterexample="N/A — converse holds for metric spaces (Theorem 9.6).",
        ),
    ]
    return ImplicationChainBridge(
        version=CHAPTER_09_INTEGRATION_VERSION,
        rows=rows,
        summary=(
            "Second countable ⟹ first countable, separable, and Lindelöf. "
            "In metric spaces, separable ⟺ second countable (Theorem 9.6). "
            "None of the other converses hold in general."
        ),
        api_reference=(
            "pytop.countability: is_first_countable, is_second_countable, "
            "is_separable, is_lindelof"
        ),
    )


@dataclass(frozen=True, slots=True)
class TheoremBridge:
    """Bridge for key Chapter 09 theorems."""
    version: str
    rows: List[CountabilityTheoremRow]

    @property
    def theorem_count(self) -> int:
        return len(self.rows)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "rows": [r.to_dict() for r in self.rows],
        }


def build_theorem_bridge() -> TheoremBridge:
    """Return the Chapter 09 theorem bridge (5 theorems)."""
    rows = [
        CountabilityTheoremRow(
            id="9.1",
            label="C1 and sequential continuity",
            statement=(
                "Let X be a C1 topological space and f : X → Y. "
                "Then f is continuous at x₀ ∈ X if and only if "
                "f is sequentially continuous at x₀ (i.e. xₙ → x₀ implies "
                "f(xₙ) → f(x₀))."
            ),
            proof_sketch=(
                "Forward: standard ε–δ argument using the countable nested "
                "local base at x₀. Backward: if f is not continuous choose "
                "xₙ ∈ Bₙ(x₀) \\ f⁻¹(V) to contradict sequential continuity."
            ),
            api_note=(
                "pytop.countability.c1_sequential_continuity_equiv(f, space) "
                "verifies Theorem 9.1 for a given map."
            ),
        ),
        CountabilityTheoremRow(
            id="9.2",
            label="C2 implies C1",
            statement=(
                "Every second countable (C2) space is first countable (C1). "
                "If ℬ is a countable global base for X, then "
                "{B ∈ ℬ : x ∈ B} is a countable local base at each x ∈ X."
            ),
            proof_sketch=(
                "For any x ∈ X and open U ∋ x, some B ∈ ℬ satisfies "
                "x ∈ B ⊆ U; so {B ∈ ℬ : x ∈ B} is the required local base."
            ),
            api_note=(
                "pytop.countability.c2_implies_c1(space) asserts the implication."
            ),
        ),
        CountabilityTheoremRow(
            id="9.3",
            label="C2 implies Lindelöf",
            statement=(
                "Every second countable space is Lindelöf: given a countable "
                "base ℬ = {B₁, B₂, …} and an open cover {Uα}, select for each "
                "Bₙ ⊆ Uα a single Uα; the selected subfamily is countable and "
                "still covers X."
            ),
            proof_sketch=(
                "For each x ∈ X pick Bₙ(x) ⊆ Uα(x); the set of distinct "
                "Bₙ used is countable, yielding a countable subcover."
            ),
            api_note=(
                "pytop.countability.c2_implies_lindelof(space) asserts C2 → L."
            ),
        ),
        CountabilityTheoremRow(
            id="9.4",
            label="Lindelöf + regular ⟹ normal",
            statement=(
                "A regular Lindelöf space is normal. "
                "(Used to lift Lindelöf to separation axioms in Chapter 10.)"
            ),
            proof_sketch=(
                "Standard transfinite-induction argument using the countable "
                "subcover property to separate disjoint closed sets."
            ),
            api_note=(
                "pytop.separation.lindelof_regular_is_normal(space) checks "
                "Theorem 9.4."
            ),
        ),
        CountabilityTheoremRow(
            id="9.5",
            label="C2 implies separable",
            statement=(
                "Every second countable space X is separable: if ℬ = {Bₙ} is "
                "a countable base, pick xₙ ∈ Bₙ for each n; then {xₙ} is a "
                "countable dense subset."
            ),
            proof_sketch=(
                "For any non-empty open U there exists Bₙ ⊆ U, so xₙ ∈ U; "
                "hence {xₙ} meets every open set, proving density."
            ),
            api_note=(
                "pytop.countability.c2_implies_separable(space) asserts C2 → S."
            ),
        ),
        CountabilityTheoremRow(
            id="9.6",
            label="Separable metric ⟹ C2",
            statement=(
                "A separable metric space is second countable. "
                "If D = {dₙ} is a countable dense set, then "
                "ℬ = {B(dₙ, 1/m) : n, m ∈ ℕ} is a countable base."
            ),
            proof_sketch=(
                "For any open U and x ∈ U pick r > 0 with B(x,r) ⊆ U; "
                "choose dₙ ∈ B(x, r/2) and m with 1/m < r/2; then "
                "x ∈ B(dₙ, 1/m) ⊆ U."
            ),
            api_note=(
                "pytop.countability.separable_metric_is_c2(space) verifies "
                "Theorem 9.6."
            ),
        ),
    ]
    return TheoremBridge(version=CHAPTER_09_INTEGRATION_VERSION, rows=rows)


@dataclass(frozen=True, slots=True)
class HereditaryBridge:
    """Bridge for hereditary (subspace-preservation) properties in Chapter 09."""
    version: str
    rows: List[HereditaryRow]

    @property
    def hereditary_count(self) -> int:
        return sum(1 for r in self.rows if r.hereditary)

    @property
    def non_hereditary_count(self) -> int:
        return sum(1 for r in self.rows if not r.hereditary)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "rows": [r.to_dict() for r in self.rows],
            "hereditary_count": self.hereditary_count,
            "non_hereditary_count": self.non_hereditary_count,
        }


def build_hereditary_bridge() -> HereditaryBridge:
    """Return the Chapter 09 hereditary-property bridge."""
    rows = [
        HereditaryRow(
            id="C1_hereditary",
            property_name="First countability (C1)",
            hereditary=True,
            note=(
                "Every subspace of a C1 space is C1: the restrictions of "
                "the countable local bases form local bases in the subspace."
            ),
        ),
        HereditaryRow(
            id="C2_hereditary",
            property_name="Second countability (C2)",
            hereditary=True,
            note=(
                "Every subspace of a C2 space is C2: intersect the global "
                "base with the subspace to get a countable base."
            ),
        ),
        HereditaryRow(
            id="S_not_hereditary",
            property_name="Separability",
            hereditary=False,
            note=(
                "Separability is NOT hereditary. The Niemytzki (Moore) plane "
                "is separable but its closed subspace — the x-axis with "
                "tangent-disc topology — is not separable."
            ),
        ),
        HereditaryRow(
            id="L_not_hereditary",
            property_name="Lindelöf",
            hereditary=False,
            note=(
                "Lindelöf is NOT hereditary. The Sorgenfrey plane is the "
                "product of two Sorgenfrey lines (each Lindelöf) but is not "
                "Lindelöf; its closed discrete subspace {(x, −x)} witnesses "
                "the failure."
            ),
        ),
    ]
    return HereditaryBridge(version=CHAPTER_09_INTEGRATION_VERSION, rows=rows)


# ---------------------------------------------------------------------------
# Local-base diagnostic table
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class LocalBaseDiagnosticRow:
    """One row in the local-base diagnostic table."""
    id: str
    space_name: str
    is_c1: bool
    is_c2: bool
    local_base_note: str

    def to_dict(self) -> dict:
        return asdict(self)


def build_local_base_diagnostic_table() -> List[LocalBaseDiagnosticRow]:
    """Return five canonical examples for the local-base diagnostic table."""
    return [
        LocalBaseDiagnosticRow(
            id="R_usual",
            space_name="ℝ (usual topology)",
            is_c1=True,
            is_c2=True,
            local_base_note=(
                "Countable base {(p, q) : p, q ∈ ℚ}; intervals (x−1/n, x+1/n) "
                "give a countable local base at each x."
            ),
        ),
        LocalBaseDiagnosticRow(
            id="R_discrete_uncountable",
            space_name="Uncountable set with discrete topology",
            is_c1=True,
            is_c2=False,
            local_base_note=(
                "{{x}} is a local base at each x (C1), but no countable "
                "global base exists (not C2)."
            ),
        ),
        LocalBaseDiagnosticRow(
            id="sorgenfrey_line",
            space_name="Sorgenfrey line (lower-limit topology on ℝ)",
            is_c1=True,
            is_c2=False,
            local_base_note=(
                "{[x, x+1/n) : n ∈ ℕ} is a countable local base at x (C1), "
                "but the space is not C2; it is however separable (ℚ is dense)."
            ),
        ),
        LocalBaseDiagnosticRow(
            id="R_indiscrete",
            space_name="ℝ with indiscrete topology",
            is_c1=True,
            is_c2=True,
            local_base_note=(
                "Only one open set beyond ∅; {ℝ} is a countable base. "
                "Trivially C1 and C2, but very few open sets."
            ),
        ),
        LocalBaseDiagnosticRow(
            id="niemytzki_plane",
            space_name="Niemytzki (Moore) plane",
            is_c1=True,
            is_c2=False,
            local_base_note=(
                "C1 (tangent-disc neighbourhoods form a local base) but not C2. "
                "The x-axis subspace is an uncountable discrete space."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Chapter 09 integration audit
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Chapter09IntegrationAudit:
    """Audit record for the Chapter 09 countability integration."""
    version: str
    insertion_points: List[str]
    countability_axiom_count: int
    theorem_count: int
    hereditary_count: int
    non_hereditary_count: int
    local_base_example_count: int
    implication_count: int
    blocker_count: int
    blocker_notes: List[str]

    @property
    def status(self) -> str:
        return "ready" if self.blocker_count == 0 else "blocked"

    def to_result(self) -> Result:
        result_status = "true" if self.blocker_count == 0 else "conditional"
        justification = [
            "Chapter 09 countability integration audit complete.",
            f"Countability axioms bridged: {self.countability_axiom_count}.",
            f"Theorems bridged: {self.theorem_count}.",
            f"Insertion points: {len(self.insertion_points)}.",
            f"Blockers: {self.blocker_count}.",
        ]
        return Result(
            status=result_status,
            mode="exact",
            justification=justification,
        )

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "insertion_points": self.insertion_points,
            "countability_axiom_count": self.countability_axiom_count,
            "theorem_count": self.theorem_count,
            "hereditary_count": self.hereditary_count,
            "non_hereditary_count": self.non_hereditary_count,
            "local_base_example_count": self.local_base_example_count,
            "implication_count": self.implication_count,
            "blocker_count": self.blocker_count,
            "blocker_notes": self.blocker_notes,
            "status": self.status,
        }


def build_chapter_09_integration_audit(root: Path) -> Chapter09IntegrationAudit:
    """Build the Chapter 09 integration audit."""
    axioms = build_countability_axiom_bridge()
    theorems = build_theorem_bridge()
    hereditary = build_hereditary_bridge()
    local_base = build_local_base_diagnostic_table()
    chain = build_implication_chain_bridge()

    blockers: List[str] = []

    return Chapter09IntegrationAudit(
        version=CHAPTER_09_INTEGRATION_VERSION,
        insertion_points=CHAPTER_09_INSERTION_POINTS,
        countability_axiom_count=len(axioms),
        theorem_count=theorems.theorem_count,
        hereditary_count=hereditary.hereditary_count,
        non_hereditary_count=hereditary.non_hereditary_count,
        local_base_example_count=len(local_base),
        implication_count=chain.implication_count,
        blocker_count=len(blockers),
        blocker_notes=blockers,
    )


# ---------------------------------------------------------------------------
# Summary and render
# ---------------------------------------------------------------------------

def chapter_09_integration_summary(root: Path) -> dict:
    """Return a summary dict for the Chapter 09 integration."""
    audit = build_chapter_09_integration_audit(root)
    axioms = build_countability_axiom_bridge()
    theorems = build_theorem_bridge()
    hereditary = build_hereditary_bridge()
    local_base = build_local_base_diagnostic_table()
    chain = build_implication_chain_bridge()

    return {
        "version": CHAPTER_09_INTEGRATION_VERSION,
        "audit": audit.to_dict(),
        "countability_axiom_bridge": [a.to_dict() for a in axioms],
        "theorem_bridge": theorems.to_dict(),
        "hereditary_bridge": hereditary.to_dict(),
        "local_base_diagnostic": [r.to_dict() for r in local_base],
        "implication_chain_bridge": chain.to_dict(),
    }


def render_chapter_09_integration_report(root: Path) -> str:
    """Render a Markdown integration report for Chapter 09."""
    audit = build_chapter_09_integration_audit(root)
    axioms = build_countability_axiom_bridge()
    theorems = build_theorem_bridge()
    hereditary = build_hereditary_bridge()
    local_base = build_local_base_diagnostic_table()
    chain = build_implication_chain_bridge()

    lines: List[str] = []
    lines.append(
        f"# Chapter 09 Countability Integration Report - {CHAPTER_09_INTEGRATION_VERSION}"
    )
    lines.append("")

    # Audit section
    lines.append("## Audit")
    lines.append(f"- Version: {audit.version}")
    lines.append(f"- Status: {audit.status}")
    lines.append(f"- Countability axioms: {audit.countability_axiom_count}")
    lines.append(f"- Theorems: {audit.theorem_count}")
    lines.append(f"- Hereditary: {audit.hereditary_count}, Non-hereditary: {audit.non_hereditary_count}")
    lines.append(f"- Local-base examples: {audit.local_base_example_count}")
    lines.append(f"- Implication rows: {audit.implication_count}")
    lines.append(f"- Blockers: {audit.blocker_count}")
    lines.append("")

    # Countability axiom bridge
    lines.append("## Countability axiom bridge")
    for a in axioms:
        lines.append(f"### {a.id} — {a.label}")
        lines.append(f"**Definition:** {a.definition}")
        lines.append(f"**API note:** {a.api_note}")
        lines.append("")

    # Theorem bridge
    lines.append("## Theorem bridge")
    for t in theorems.rows:
        lines.append(f"### Theorem {t.id} — {t.label}")
        lines.append(f"**Statement:** {t.statement}")
        lines.append(f"**Proof sketch:** {t.proof_sketch}")
        lines.append(f"**API note:** {t.api_note}")
        lines.append("")

    # Implication chain
    lines.append("## Implication chain bridge")
    lines.append(f"*{chain.summary}*")
    lines.append("")
    for r in chain.rows:
        conv = "converse holds" if r.converse_holds else "converse fails"
        lines.append(f"- **{r.id}**: {r.source} ⟹ {r.target} ({conv})")
        if not r.converse_holds:
            lines.append(f"  Counterexample: {r.counterexample}")
    lines.append("")

    # Hereditary bridge
    lines.append("## Hereditary property bridge")
    for h in hereditary.rows:
        marker = "✓ hereditary" if h.hereditary else "✗ not hereditary"
        lines.append(f"- **{h.property_name}** — {marker}: {h.note}")
    lines.append("")

    # Local-base diagnostic table
    lines.append("## Local-base diagnostic table")
    lines.append("| id | space | C1 | C2 | note |")
    lines.append("|----|-------|----|----|------|")
    for row in local_base:
        c1 = "yes" if row.is_c1 else "no"
        c2 = "yes" if row.is_c2 else "no"
        lines.append(f"| {row.id} | {row.space_name} | {c1} | {c2} | {row.local_base_note} |")
    lines.append("")

    # Insertion points
    lines.append("## Insertion points")
    for ip in audit.insertion_points:
        lines.append(f"1. {ip}")
    lines.append("")

    # Originality guardrails
    lines.append("## Originality guardrails")
    lines.append(
        "Do not copy verbatim from any uploaded chapter zip. "
        "All definitions, theorem statements, and proof sketches above are "
        "synthesised from standard topology knowledge and must be reworded "
        "before manuscript insertion."
    )
    lines.append("")

    return "\n".join(lines)
