"""Chapter 10 separation axioms manuscript integration - v1.0.324.

Bridges the T0–T4 separation hierarchy, Urysohn's lemma, the Tietze extension
theorem, and the implications among separation axioms to the active manuscript
anchor and API surface.

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

CHAPTER_10_INTEGRATION_VERSION: str = "v1.0.324"

# ---------------------------------------------------------------------------
# Manuscript targets and insertion points
# ---------------------------------------------------------------------------

CHAPTER_10_MANUSCRIPT_TARGETS: List[str] = [
    "src/pytop/chapter_10_separation_axioms_integration.py",
    "src/pytop/separation.py",
    "src/pytop/base_theory.py",
    "src/pytop/metric_spaces.py",
    "src/pytop/countability.py",
    "tests/core/test_chapter_10_separation_axioms_integration_v324.py",
    "docs/integration/chapter_07_15/chapter_10_separation_axioms_integration_v1_0_324.md",
]

CHAPTER_10_INSERTION_POINTS: List[str] = [
    "separation hierarchy table (T0 through T4 with examples and implications)",
    "Urysohn lemma and metrisation warning box",
    "Tietze extension theorem bridge at the end of the normal-spaces section",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SeparationAxiomRow:
    """One row in the separation-axiom bridge table."""
    id: str            # "T0", "T1", "T2", "T3", "T3_5", "T4"
    label: str
    definition: str
    canonical_example: str
    canonical_non_example: str
    api_note: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SeparationImplicationRow:
    """One directed implication in the separation hierarchy."""
    id: str
    source: str
    target: str
    converse_holds: bool
    counterexample: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class SeparationTheoremRow:
    """A key theorem in Chapter 10."""
    id: str
    label: str
    statement: str
    proof_sketch: str
    api_note: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Separation axiom bridge
# ---------------------------------------------------------------------------

def build_separation_axiom_bridge() -> List[SeparationAxiomRow]:
    """Return the T0–T4 (+ T3½) separation axiom bridge (6 rows)."""
    return [
        SeparationAxiomRow(
            id="T0",
            label="Kolmogorov space",
            definition=(
                "A topological space X is T0 if for every pair of distinct "
                "points x, y ∈ X there exists an open set containing one "
                "but not the other."
            ),
            canonical_example="Any T1 space; the Sierpiński space {0,1}.",
            canonical_non_example=(
                "The indiscrete space on two or more points: no open set "
                "distinguishes the two points."
            ),
            api_note="pytop.separation.is_t0(space) checks point-distinguishability.",
        ),
        SeparationAxiomRow(
            id="T1",
            label="Fréchet space",
            definition=(
                "A topological space X is T1 if for every pair of distinct "
                "points x, y ∈ X there exist open sets U ∋ x and V ∋ y "
                "with y ∉ U and x ∉ V. Equivalently, every singleton {x} "
                "is closed."
            ),
            canonical_example="Any metric space; the cofinite topology on an infinite set.",
            canonical_non_example=(
                "The Sierpiński space: {1} is not closed."
            ),
            api_note=(
                "pytop.separation.is_t1(space) checks that all singletons are closed."
            ),
        ),
        SeparationAxiomRow(
            id="T2",
            label="Hausdorff space",
            definition=(
                "A topological space X is T2 (Hausdorff) if for every pair "
                "of distinct points x, y ∈ X there exist disjoint open sets "
                "U ∋ x and V ∋ y."
            ),
            canonical_example="Every metric space; every ordered topological space.",
            canonical_non_example=(
                "The cofinite topology on an infinite set: no two non-empty open "
                "sets are disjoint."
            ),
            api_note=(
                "pytop.separation.is_hausdorff(space) verifies T2; "
                "pytop.separation.is_t2(space) is an alias."
            ),
        ),
        SeparationAxiomRow(
            id="T3",
            label="Regular space (T1 + regular)",
            definition=(
                "A topological space X is regular if for every point x ∈ X "
                "and every closed set F not containing x there exist disjoint "
                "open sets U ∋ x and V ⊇ F. A T3 space is T1 + regular."
            ),
            canonical_example="Every metric space; every compact Hausdorff space.",
            canonical_non_example=(
                "The K-topology on ℝ (basis = usual intervals ∪ sets of the form "
                "(a,b) \\ K where K = {1/n}): T2 but not regular."
            ),
            api_note=(
                "pytop.separation.is_regular(space) and "
                "pytop.separation.is_t3(space) check T1 + regularity."
            ),
        ),
        SeparationAxiomRow(
            id="T3_5",
            label="Tychonoff / completely regular (T1 + completely regular)",
            definition=(
                "A topological space X is completely regular if for every "
                "point x ∈ X and closed set F not containing x there exists "
                "a continuous function f : X → [0,1] with f(x) = 0 and "
                "f|_F ≡ 1. A Tychonoff space is T1 + completely regular."
            ),
            canonical_example=(
                "Every T4 (normal T1) space (by Urysohn's lemma); "
                "every subspace of a Tychonoff space."
            ),
            canonical_non_example=(
                "A T3 space that is not T3½ exists (Mysior's example), "
                "though such examples are highly non-trivial."
            ),
            api_note=(
                "pytop.separation.is_completely_regular(space) and "
                "pytop.separation.is_tychonoff(space)."
            ),
        ),
        SeparationAxiomRow(
            id="T4",
            label="Normal space (T1 + normal)",
            definition=(
                "A topological space X is normal if for every pair of "
                "disjoint closed sets A, B ⊆ X there exist disjoint open "
                "sets U ⊇ A and V ⊇ B. A T4 space is T1 + normal."
            ),
            canonical_example=(
                "Every metric space (by the distance function construction); "
                "every compact Hausdorff space."
            ),
            canonical_non_example=(
                "The Sorgenfrey plane (product of two Sorgenfrey lines): "
                "T3 but not normal."
            ),
            api_note=(
                "pytop.separation.is_normal(space) and "
                "pytop.separation.is_t4(space) check T1 + normality."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Separation implication bridge
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SeparationHierarchyBridge:
    """Full implication chain T4 → T3½ → T3 → T2 → T1 → T0."""
    version: str
    rows: List[SeparationImplicationRow]
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


def build_separation_hierarchy_bridge() -> SeparationHierarchyBridge:
    """Build the T0–T4 separation hierarchy implication bridge."""
    rows = [
        SeparationImplicationRow(
            id="T4_implies_T3_5",
            source="T4",
            target="T3½",
            converse_holds=False,
            counterexample=(
                "A Tychonoff space that is not normal exists, e.g. "
                "ℝ^I (uncountable product of ℝ) is T3½ but not normal "
                "when I is uncountable."
            ),
        ),
        SeparationImplicationRow(
            id="T3_5_implies_T3",
            source="T3½",
            target="T3",
            converse_holds=False,
            counterexample=(
                "Mysior's example: a T3 space that is not completely regular."
            ),
        ),
        SeparationImplicationRow(
            id="T3_implies_T2",
            source="T3",
            target="T2",
            converse_holds=False,
            counterexample=(
                "The K-topology on ℝ is Hausdorff (T2) but not regular (T3)."
            ),
        ),
        SeparationImplicationRow(
            id="T2_implies_T1",
            source="T2",
            target="T1",
            converse_holds=False,
            counterexample=(
                "The cofinite topology on an infinite set is T1 but not T2: "
                "no two non-empty open sets are disjoint."
            ),
        ),
        SeparationImplicationRow(
            id="T1_implies_T0",
            source="T1",
            target="T0",
            converse_holds=False,
            counterexample=(
                "The Sierpiński space is T0 but not T1: {1} is not closed."
            ),
        ),
        SeparationImplicationRow(
            id="metric_implies_T4",
            source="metric space",
            target="T4",
            converse_holds=False,
            counterexample=(
                "Many normal T1 spaces are not metrisable, e.g. the "
                "long line is T4 but not second countable hence not metrisable."
            ),
        ),
    ]
    return SeparationHierarchyBridge(
        version=CHAPTER_10_INTEGRATION_VERSION,
        rows=rows,
        summary=(
            "The separation hierarchy is strict: "
            "T4 ⟹ T3½ ⟹ T3 ⟹ T2 ⟹ T1 ⟹ T0. "
            "Every metric space is T4. No converse holds in general."
        ),
        api_reference=(
            "pytop.separation: is_t0, is_t1, is_hausdorff, is_t2, "
            "is_regular, is_t3, is_completely_regular, is_tychonoff, "
            "is_normal, is_t4"
        ),
    )


# ---------------------------------------------------------------------------
# Theorem bridge
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SeparationTheoremBridge:
    """Bridge for key Chapter 10 theorems."""
    version: str
    rows: List[SeparationTheoremRow]

    @property
    def theorem_count(self) -> int:
        return len(self.rows)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "rows": [r.to_dict() for r in self.rows],
        }


def build_separation_theorem_bridge() -> SeparationTheoremBridge:
    """Return the Chapter 10 theorem bridge (5 theorems)."""
    rows = [
        SeparationTheoremRow(
            id="10.1",
            label="Urysohn's lemma",
            statement=(
                "Let X be a normal space and A, B ⊆ X disjoint closed sets. "
                "Then there exists a continuous function f : X → [0,1] "
                "such that f|_A ≡ 0 and f|_B ≡ 1."
            ),
            proof_sketch=(
                "Inductively assign open sets U_q to each dyadic rational q ∈ [0,1] "
                "with cl(U_q) ⊆ U_r whenever q < r, starting from U_0 ⊇ A and "
                "U_1 = X \\ B. Define f(x) = inf{q : x ∈ U_q}; continuity follows "
                "from the nested structure."
            ),
            api_note=(
                "pytop.separation.urysohn_function(space, A, B) constructs "
                "a continuous separating function for disjoint closed A, B."
            ),
        ),
        SeparationTheoremRow(
            id="10.2",
            label="Urysohn metrisation theorem",
            statement=(
                "Every second countable regular (T3) space is metrisable. "
                "Equivalently, a second countable T3 space embeds as a subspace "
                "of the Hilbert cube [0,1]^ℕ."
            ),
            proof_sketch=(
                "Use Urysohn's lemma on the countable base to construct a "
                "countable family of continuous functions separating points from "
                "closed sets; embed via the evaluation map into [0,1]^ℕ, "
                "which is metrisable."
            ),
            api_note=(
                "pytop.separation.urysohn_metrisation_check(space) verifies "
                "second countability and T3 as necessary conditions for "
                "Urysohn metrisability."
            ),
        ),
        SeparationTheoremRow(
            id="10.3",
            label="Tietze extension theorem",
            statement=(
                "Let X be a normal space, A ⊆ X a closed subspace, and "
                "f : A → [a,b] a continuous function. Then there exists a "
                "continuous extension F : X → [a,b] with F|_A = f. "
                "The result also holds for f : A → ℝ (unbounded)."
            ),
            proof_sketch=(
                "Apply Urysohn's lemma iteratively to construct a series of "
                "continuous functions whose partial sums converge uniformly "
                "to an extension of f; the limit F is continuous by uniform "
                "convergence."
            ),
            api_note=(
                "pytop.separation.tietze_extension(space, closed_sub, f) "
                "computes a continuous extension of f over X."
            ),
        ),
        SeparationTheoremRow(
            id="10.4",
            label="Compact Hausdorff ⟹ T4",
            statement=(
                "Every compact Hausdorff space is normal (T4). "
                "Disjoint closed sets in a compact Hausdorff space can be "
                "separated by disjoint open sets."
            ),
            proof_sketch=(
                "Given disjoint closed A, B in a compact Hausdorff space X, "
                "for each a ∈ A use Hausdorff to separate a from each b ∈ B; "
                "compactness of B yields finitely many open sets covering B "
                "disjoint from an open set around a; repeat for A."
            ),
            api_note=(
                "pytop.separation.compact_hausdorff_is_normal(space) asserts "
                "the compact Hausdorff → T4 implication."
            ),
        ),
        SeparationTheoremRow(
            id="10.5",
            label="T4 ⟹ T3½ (Urysohn consequence)",
            statement=(
                "Every T4 (normal T1) space is completely regular (T3½). "
                "For any point x and closed set F with x ∉ F, Urysohn's lemma "
                "provides a continuous function f : X → [0,1] with f(x) = 0 "
                "and f|_F ≡ 1."
            ),
            proof_sketch=(
                "Apply Urysohn's lemma to the disjoint closed sets {x} (T1 "
                "guarantees singletons are closed) and F."
            ),
            api_note=(
                "pytop.separation.t4_implies_completely_regular(space) checks "
                "Theorem 10.5."
            ),
        ),
    ]
    return SeparationTheoremBridge(version=CHAPTER_10_INTEGRATION_VERSION, rows=rows)


# ---------------------------------------------------------------------------
# Metric-implies-separation bridge
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class MetricSeparationRow:
    """How metric spaces satisfy each separation axiom."""
    id: str
    axiom: str
    satisfied: bool
    proof_idea: str

    def to_dict(self) -> dict:
        return asdict(self)


def build_metric_separation_bridge() -> List[MetricSeparationRow]:
    """Return 6 rows showing metric spaces satisfy T0–T4."""
    return [
        MetricSeparationRow(
            id="metric_T0",
            axiom="T0",
            satisfied=True,
            proof_idea=(
                "For distinct x ≠ y with d(x,y) = r > 0, the open ball "
                "B(x, r/2) contains x but not y."
            ),
        ),
        MetricSeparationRow(
            id="metric_T1",
            axiom="T1",
            satisfied=True,
            proof_idea=(
                "For x ≠ y, B(x, d(x,y)/2) contains x but not y and vice versa. "
                "Singletons are closed: {x} = ∩_{n≥1} B(x,1/n)^c in the closed sense, "
                "or directly from the Hausdorff property."
            ),
        ),
        MetricSeparationRow(
            id="metric_T2",
            axiom="T2",
            satisfied=True,
            proof_idea=(
                "For distinct x, y with d(x,y) = r, the balls B(x, r/2) and "
                "B(y, r/2) are disjoint open sets separating x and y."
            ),
        ),
        MetricSeparationRow(
            id="metric_T3",
            axiom="T3",
            satisfied=True,
            proof_idea=(
                "For closed F and x ∉ F, let r = d(x,F) > 0. Then "
                "B(x, r/2) and ∪_{y∈F} B(y, r/2) are disjoint open sets."
            ),
        ),
        MetricSeparationRow(
            id="metric_T3_5",
            axiom="T3½",
            satisfied=True,
            proof_idea=(
                "Use f(z) = d(z,A) / (d(z,A) + d(z,F)) for closed F and "
                "point x ∉ F (set A = {x}); this is continuous, equals 0 at x, "
                "and equals 1 on F."
            ),
        ),
        MetricSeparationRow(
            id="metric_T4",
            axiom="T4",
            satisfied=True,
            proof_idea=(
                "For disjoint closed A, B, set U = {x : d(x,A) < d(x,B)} and "
                "V = {x : d(x,B) < d(x,A)}; these are disjoint open sets with "
                "A ⊆ U and B ⊆ V."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Chapter 10 integration audit
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Chapter10IntegrationAudit:
    """Audit record for the Chapter 10 separation axioms integration."""
    version: str
    insertion_points: List[str]
    separation_axiom_count: int
    theorem_count: int
    implication_count: int
    metric_separation_count: int
    blocker_count: int
    blocker_notes: List[str]

    @property
    def status(self) -> str:
        return "ready" if self.blocker_count == 0 else "blocked"

    def to_result(self) -> Result:
        result_status = "true" if self.blocker_count == 0 else "conditional"
        justification = [
            "Chapter 10 separation axioms integration audit complete.",
            f"Separation axioms bridged: {self.separation_axiom_count}.",
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
            "separation_axiom_count": self.separation_axiom_count,
            "theorem_count": self.theorem_count,
            "implication_count": self.implication_count,
            "metric_separation_count": self.metric_separation_count,
            "blocker_count": self.blocker_count,
            "blocker_notes": self.blocker_notes,
            "status": self.status,
        }


def build_chapter_10_integration_audit(root: Path) -> Chapter10IntegrationAudit:
    """Build the Chapter 10 integration audit."""
    axioms = build_separation_axiom_bridge()
    theorems = build_separation_theorem_bridge()
    hierarchy = build_separation_hierarchy_bridge()
    metric_sep = build_metric_separation_bridge()

    blockers: List[str] = []

    return Chapter10IntegrationAudit(
        version=CHAPTER_10_INTEGRATION_VERSION,
        insertion_points=CHAPTER_10_INSERTION_POINTS,
        separation_axiom_count=len(axioms),
        theorem_count=theorems.theorem_count,
        implication_count=hierarchy.implication_count,
        metric_separation_count=len(metric_sep),
        blocker_count=len(blockers),
        blocker_notes=blockers,
    )


# ---------------------------------------------------------------------------
# Summary and render
# ---------------------------------------------------------------------------

def chapter_10_integration_summary(root: Path) -> dict:
    """Return a summary dict for the Chapter 10 integration."""
    audit = build_chapter_10_integration_audit(root)
    axioms = build_separation_axiom_bridge()
    theorems = build_separation_theorem_bridge()
    hierarchy = build_separation_hierarchy_bridge()
    metric_sep = build_metric_separation_bridge()

    return {
        "version": CHAPTER_10_INTEGRATION_VERSION,
        "audit": audit.to_dict(),
        "separation_axiom_bridge": [a.to_dict() for a in axioms],
        "separation_theorem_bridge": theorems.to_dict(),
        "separation_hierarchy_bridge": hierarchy.to_dict(),
        "metric_separation_bridge": [r.to_dict() for r in metric_sep],
    }


def render_chapter_10_integration_report(root: Path) -> str:
    """Render a Markdown integration report for Chapter 10."""
    audit = build_chapter_10_integration_audit(root)
    axioms = build_separation_axiom_bridge()
    theorems = build_separation_theorem_bridge()
    hierarchy = build_separation_hierarchy_bridge()
    metric_sep = build_metric_separation_bridge()

    lines: List[str] = []
    lines.append(
        f"# Chapter 10 Separation Axioms Integration Report - {CHAPTER_10_INTEGRATION_VERSION}"
    )
    lines.append("")

    # Audit
    lines.append("## Audit")
    lines.append(f"- Version: {audit.version}")
    lines.append(f"- Status: {audit.status}")
    lines.append(f"- Separation axioms: {audit.separation_axiom_count}")
    lines.append(f"- Theorems: {audit.theorem_count}")
    lines.append(f"- Implication rows: {audit.implication_count}")
    lines.append(f"- Metric-separation rows: {audit.metric_separation_count}")
    lines.append(f"- Blockers: {audit.blocker_count}")
    lines.append("")

    # Separation axiom bridge
    lines.append("## Separation axiom bridge")
    for a in axioms:
        lines.append(f"### {a.id} — {a.label}")
        lines.append(f"**Definition:** {a.definition}")
        lines.append(f"**Example:** {a.canonical_example}")
        lines.append(f"**Non-example:** {a.canonical_non_example}")
        lines.append(f"**API note:** {a.api_note}")
        lines.append("")

    # Separation hierarchy
    lines.append("## Separation hierarchy bridge")
    lines.append(f"*{hierarchy.summary}*")
    lines.append("")
    for r in hierarchy.rows:
        conv = "converse holds" if r.converse_holds else "converse fails"
        lines.append(f"- **{r.id}**: {r.source} ⟹ {r.target} ({conv})")
        lines.append(f"  Counterexample: {r.counterexample}")
    lines.append("")

    # Theorem bridge
    lines.append("## Theorem bridge")
    for t in theorems.rows:
        lines.append(f"### Theorem {t.id} — {t.label}")
        lines.append(f"**Statement:** {t.statement}")
        lines.append(f"**Proof sketch:** {t.proof_sketch}")
        lines.append(f"**API note:** {t.api_note}")
        lines.append("")

    # Metric-separation table
    lines.append("## Metric separation bridge")
    lines.append("| axiom | satisfied | proof idea |")
    lines.append("|-------|-----------|------------|")
    for row in metric_sep:
        sat = "yes" if row.satisfied else "no"
        lines.append(f"| {row.axiom} | {sat} | {row.proof_idea[:80]}… |")
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
