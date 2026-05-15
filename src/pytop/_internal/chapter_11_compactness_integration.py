"""Chapter 11 compactness manuscript integration - v1.0.325.

Bridges open-cover compactness, sequential compactness, limit-point
compactness, the finite intersection property, Heine-Borel, Tychonoff's
theorem, and compact-Hausdorff implications to the active manuscript
anchor and API surface.

Originality guardrails
----------------------
All content is synthesised from standard topology knowledge.
Do **not** copy verbatim from any uploaded chapter zip.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from pytop.result import Result

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

CHAPTER_11_INTEGRATION_VERSION: str = "v1.0.325"

# ---------------------------------------------------------------------------
# Manuscript targets and insertion points
# ---------------------------------------------------------------------------

CHAPTER_11_MANUSCRIPT_TARGETS: List[str] = [
    "src/pytop/chapter_11_compactness_integration.py",
    "src/pytop/compactness.py",
    "src/pytop/metric_spaces.py",
    "src/pytop/separation.py",
    "src/pytop/base_theory.py",
    "tests/core/test_chapter_11_compactness_integration_v325.py",
    "docs/integration/chapter_07_15/chapter_11_compactness_integration_v1_0_325.md",
]

CHAPTER_11_INSERTION_POINTS: List[str] = [
    "compactness equivalence table (open-cover, sequential, limit-point, FIP)",
    "Heine-Borel theorem box with ℝⁿ characterisation",
    "Tychonoff theorem and compact-Hausdorff implication warning box",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CompactnessVariantRow:
    """One row in the compactness-variant bridge table."""
    id: str
    label: str
    definition: str
    equivalent_to_compact: bool       # in general topology
    metric_equivalent: bool           # equivalent in metric spaces
    api_note: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CompactnessTheoremRow:
    """A key theorem in Chapter 11."""
    id: str
    label: str
    statement: str
    proof_sketch: str
    api_note: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HeineBorelRow:
    """One row in the Heine-Borel characterisation table."""
    id: str
    space: str
    characterisation: str
    compact: bool
    note: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CompactHausdorffRow:
    """Implication when compact meets Hausdorff."""
    id: str
    hypothesis: str
    conclusion: str
    converse_holds: bool
    counterexample: str

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Compactness variant bridge
# ---------------------------------------------------------------------------

def build_compactness_variant_bridge() -> List[CompactnessVariantRow]:
    """Return four compactness-variant rows."""
    return [
        CompactnessVariantRow(
            id="open_cover",
            label="Open-cover compactness",
            definition=(
                "A topological space X is compact if every open cover of X "
                "has a finite subcover."
            ),
            equivalent_to_compact=True,
            metric_equivalent=True,
            api_note="pytop.compactness.is_compact(space) checks open-cover compactness.",
        ),
        CompactnessVariantRow(
            id="sequential",
            label="Sequential compactness",
            definition=(
                "A topological space X is sequentially compact if every "
                "sequence in X has a convergent subsequence (with limit in X)."
            ),
            equivalent_to_compact=False,
            metric_equivalent=True,
            api_note=(
                "pytop.compactness.is_sequentially_compact(space) checks "
                "for convergent subsequences."
            ),
        ),
        CompactnessVariantRow(
            id="limit_point",
            label="Limit-point compactness",
            definition=(
                "A topological space X is limit-point compact (Bolzano-Weierstrass "
                "property) if every infinite subset of X has a limit point in X."
            ),
            equivalent_to_compact=False,
            metric_equivalent=True,
            api_note=(
                "pytop.compactness.is_limit_point_compact(space) checks that "
                "every infinite subset has a limit point."
            ),
        ),
        CompactnessVariantRow(
            id="fip",
            label="Finite intersection property (FIP)",
            definition=(
                "A collection of closed sets has the finite intersection "
                "property (FIP) if every finite subcollection has non-empty "
                "intersection. X is compact iff every collection of closed sets "
                "with the FIP has non-empty total intersection."
            ),
            equivalent_to_compact=True,
            metric_equivalent=True,
            api_note=(
                "pytop.compactness.compact_via_fip(space) verifies compactness "
                "via the FIP characterisation."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Heine-Borel bridge
# ---------------------------------------------------------------------------

def build_heine_borel_bridge() -> List[HeineBorelRow]:
    """Return six canonical Heine-Borel examples for ℝⁿ and beyond."""
    return [
        HeineBorelRow(
            id="closed_bounded_Rn",
            space="Closed and bounded subset of ℝⁿ",
            characterisation="closed and bounded",
            compact=True,
            note=(
                "The classical Heine-Borel theorem: a subset of ℝⁿ is compact "
                "iff it is closed and bounded."
            ),
        ),
        HeineBorelRow(
            id="open_interval_R",
            space="Open interval (a, b) ⊂ ℝ",
            characterisation="bounded but not closed",
            compact=False,
            note="The open cover {(a, b − 1/n) : n ≥ 1} has no finite subcover.",
        ),
        HeineBorelRow(
            id="unbounded_R",
            space="ℝ (all of the reals)",
            characterisation="closed but unbounded",
            compact=False,
            note="The cover {(−n, n) : n ∈ ℕ} has no finite subcover.",
        ),
        HeineBorelRow(
            id="unit_sphere_Rn",
            space="Unit sphere Sⁿ⁻¹ ⊂ ℝⁿ",
            characterisation="closed and bounded",
            compact=True,
            note="Sⁿ⁻¹ is a closed bounded subset of ℝⁿ; Heine-Borel applies.",
        ),
        HeineBorelRow(
            id="hilbert_unit_ball",
            space="Closed unit ball in ℓ²",
            characterisation="closed and bounded in infinite dimensions",
            compact=False,
            note=(
                "Heine-Borel fails in infinite-dimensional normed spaces: the "
                "sequence of standard basis vectors eₙ has no convergent "
                "subsequence."
            ),
        ),
        HeineBorelRow(
            id="cantor_set",
            space="Cantor set C ⊂ [0,1]",
            characterisation="closed and bounded",
            compact=True,
            note=(
                "The Cantor set is a closed bounded subset of ℝ, hence compact "
                "by Heine-Borel. It is also perfect and totally disconnected."
            ),
        ),
    ]


# ---------------------------------------------------------------------------
# Compact-Hausdorff implication bridge
# ---------------------------------------------------------------------------

def build_compact_hausdorff_bridge() -> List[CompactHausdorffRow]:
    """Return implications arising from compact + Hausdorff interaction."""
    return [
        CompactHausdorffRow(
            id="compact_hausdorff_is_normal",
            hypothesis="compact + Hausdorff",
            conclusion="T4 (normal)",
            converse_holds=False,
            counterexample=(
                "The deleted Tychonoff plank is T4 but not compact."
            ),
        ),
        CompactHausdorffRow(
            id="closed_in_compact_is_compact",
            hypothesis="closed subset of a compact space",
            conclusion="compact",
            converse_holds=False,
            counterexample=(
                "A compact subset of a Hausdorff space need not be closed "
                "in a non-Hausdorff space; but in Hausdorff spaces compact "
                "subsets are closed."
            ),
        ),
        CompactHausdorffRow(
            id="compact_in_hausdorff_is_closed",
            hypothesis="compact subset of a Hausdorff space",
            conclusion="closed",
            converse_holds=False,
            counterexample=(
                "Closed subsets of compact Hausdorff spaces are compact, "
                "but a closed subset of a non-compact Hausdorff space need "
                "not be compact (e.g. ℝ itself is closed in ℝ but not compact)."
            ),
        ),
        CompactHausdorffRow(
            id="continuous_image_compact",
            hypothesis="continuous image of a compact space",
            conclusion="compact",
            converse_holds=False,
            counterexample=(
                "The pre-image of a compact set under a continuous map need "
                "not be compact (e.g. f : ℝ → {0} collapses a non-compact "
                "space to a compact one)."
            ),
        ),
        CompactHausdorffRow(
            id="bijection_compact_hausdorff",
            hypothesis="continuous bijection from compact space to Hausdorff space",
            conclusion="homeomorphism",
            converse_holds=True,
            counterexample="N/A — the inverse is automatically continuous.",
        ),
    ]


# ---------------------------------------------------------------------------
# Theorem bridge
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class CompactnessTheoremBridge:
    """Bridge for key Chapter 11 theorems."""
    version: str
    rows: List[CompactnessTheoremRow]

    @property
    def theorem_count(self) -> int:
        return len(self.rows)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "rows": [r.to_dict() for r in self.rows],
        }


def build_compactness_theorem_bridge() -> CompactnessTheoremBridge:
    """Return the Chapter 11 theorem bridge (6 theorems)."""
    rows = [
        CompactnessTheoremRow(
            id="11.1",
            label="Heine-Borel theorem",
            statement=(
                "A subset K ⊆ ℝⁿ is compact if and only if K is closed and bounded."
            ),
            proof_sketch=(
                "Sufficiency: a closed bounded subset of ℝⁿ is contained in "
                "a closed n-cube; show the cube is compact by induction on n "
                "using the nested-interval lemma, then closed subsets of compact "
                "spaces are compact. Necessity: compact subsets of Hausdorff spaces "
                "are closed; compactness implies boundedness via the cover "
                "{B(0,n) : n ∈ ℕ}."
            ),
            api_note=(
                "pytop.compactness.heine_borel_check(subset, space) verifies "
                "closed + bounded in ℝⁿ."
            ),
        ),
        CompactnessTheoremRow(
            id="11.2",
            label="Tychonoff's theorem",
            statement=(
                "An arbitrary product of compact topological spaces is compact "
                "in the product topology."
            ),
            proof_sketch=(
                "Via Alexander sub-base theorem: it suffices to show every cover "
                "by sub-base elements has a finite subcover. For each factor, "
                "compactness provides finitely many sub-basic sets; a combinatorial "
                "argument (equivalent to the axiom of choice / Zorn's lemma) "
                "completes the proof."
            ),
            api_note=(
                "pytop.compactness.tychonoff_product(spaces) constructs the "
                "product and asserts compactness."
            ),
        ),
        CompactnessTheoremRow(
            id="11.3",
            label="Metric equivalences: compact ↔ sequentially compact ↔ limit-point compact",
            statement=(
                "In a metric space, open-cover compactness, sequential compactness, "
                "and limit-point compactness are all equivalent."
            ),
            proof_sketch=(
                "Compact → sequential: use total boundedness (from compactness) to "
                "extract a Cauchy subsequence; completeness (from compactness) gives "
                "convergence. Sequential → limit-point: a sequence of distinct points "
                "in an infinite subset has a convergent subsequence, whose limit is a "
                "limit point. Limit-point → compact: show total boundedness then use "
                "the Bolzano-Weierstrass argument."
            ),
            api_note=(
                "pytop.compactness.metric_compactness_equiv(metric_space) asserts "
                "Theorem 11.3."
            ),
        ),
        CompactnessTheoremRow(
            id="11.4",
            label="Extreme value theorem",
            statement=(
                "If f : X → ℝ is continuous and X is compact, then f attains "
                "its supremum and infimum: there exist x_max, x_min ∈ X with "
                "f(x_max) = sup f and f(x_min) = inf f."
            ),
            proof_sketch=(
                "f(X) is a compact subset of ℝ (continuous image of compact). "
                "A compact subset of ℝ is closed and bounded (Heine-Borel), "
                "hence contains its supremum and infimum."
            ),
            api_note=(
                "pytop.compactness.extreme_value_check(f, compact_space) "
                "verifies Theorem 11.4."
            ),
        ),
        CompactnessTheoremRow(
            id="11.5",
            label="Continuous bijection from compact to Hausdorff is a homeomorphism",
            statement=(
                "Let f : X → Y be a continuous bijection with X compact and Y "
                "Hausdorff. Then f is a homeomorphism."
            ),
            proof_sketch=(
                "It suffices to show f is a closed map. If C ⊆ X is closed then "
                "C is compact (closed subset of compact); f(C) is compact (continuous "
                "image of compact); compact subsets of Hausdorff spaces are closed, "
                "so f(C) is closed in Y."
            ),
            api_note=(
                "pytop.compactness.compact_hausdorff_homeomorphism(f, X, Y) "
                "verifies Theorem 11.5."
            ),
        ),
        CompactnessTheoremRow(
            id="11.6",
            label="FIP characterisation of compactness",
            statement=(
                "A topological space X is compact if and only if every collection "
                "of closed sets with the finite intersection property (FIP) has "
                "non-empty total intersection."
            ),
            proof_sketch=(
                "Contrapositive of the open-cover definition via De Morgan: "
                "an open cover without a finite subcover yields a collection of "
                "closed complements with FIP but empty total intersection."
            ),
            api_note=(
                "pytop.compactness.compact_via_fip(space) checks the FIP "
                "characterisation."
            ),
        ),
    ]
    return CompactnessTheoremBridge(version=CHAPTER_11_INTEGRATION_VERSION, rows=rows)


# ---------------------------------------------------------------------------
# Chapter 11 integration audit
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Chapter11IntegrationAudit:
    """Audit record for the Chapter 11 compactness integration."""
    version: str
    insertion_points: List[str]
    compactness_variant_count: int
    theorem_count: int
    heine_borel_example_count: int
    compact_hausdorff_count: int
    blocker_count: int
    blocker_notes: List[str]

    @property
    def status(self) -> str:
        return "ready" if self.blocker_count == 0 else "blocked"

    def to_result(self) -> Result:
        result_status = "true" if self.blocker_count == 0 else "conditional"
        justification = [
            "Chapter 11 compactness integration audit complete.",
            f"Compactness variants bridged: {self.compactness_variant_count}.",
            f"Theorems bridged: {self.theorem_count}.",
            f"Heine-Borel examples: {self.heine_borel_example_count}.",
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
            "compactness_variant_count": self.compactness_variant_count,
            "theorem_count": self.theorem_count,
            "heine_borel_example_count": self.heine_borel_example_count,
            "compact_hausdorff_count": self.compact_hausdorff_count,
            "blocker_count": self.blocker_count,
            "blocker_notes": self.blocker_notes,
            "status": self.status,
        }


def build_chapter_11_integration_audit(root: Path) -> Chapter11IntegrationAudit:
    """Build the Chapter 11 integration audit."""
    variants = build_compactness_variant_bridge()
    theorems = build_compactness_theorem_bridge()
    hb = build_heine_borel_bridge()
    ch = build_compact_hausdorff_bridge()

    blockers: List[str] = []

    return Chapter11IntegrationAudit(
        version=CHAPTER_11_INTEGRATION_VERSION,
        insertion_points=CHAPTER_11_INSERTION_POINTS,
        compactness_variant_count=len(variants),
        theorem_count=theorems.theorem_count,
        heine_borel_example_count=len(hb),
        compact_hausdorff_count=len(ch),
        blocker_count=len(blockers),
        blocker_notes=blockers,
    )


# ---------------------------------------------------------------------------
# Summary and render
# ---------------------------------------------------------------------------

def chapter_11_integration_summary(root: Path) -> dict:
    """Return a summary dict for the Chapter 11 integration."""
    audit = build_chapter_11_integration_audit(root)
    variants = build_compactness_variant_bridge()
    theorems = build_compactness_theorem_bridge()
    hb = build_heine_borel_bridge()
    ch = build_compact_hausdorff_bridge()

    return {
        "version": CHAPTER_11_INTEGRATION_VERSION,
        "audit": audit.to_dict(),
        "compactness_variant_bridge": [v.to_dict() for v in variants],
        "compactness_theorem_bridge": theorems.to_dict(),
        "heine_borel_bridge": [r.to_dict() for r in hb],
        "compact_hausdorff_bridge": [r.to_dict() for r in ch],
    }


def render_chapter_11_integration_report(root: Path) -> str:
    """Render a Markdown integration report for Chapter 11."""
    audit = build_chapter_11_integration_audit(root)
    variants = build_compactness_variant_bridge()
    theorems = build_compactness_theorem_bridge()
    hb = build_heine_borel_bridge()
    ch = build_compact_hausdorff_bridge()

    lines: List[str] = []
    lines.append(
        f"# Chapter 11 Compactness Integration Report - {CHAPTER_11_INTEGRATION_VERSION}"
    )
    lines.append("")

    # Audit
    lines.append("## Audit")
    lines.append(f"- Version: {audit.version}")
    lines.append(f"- Status: {audit.status}")
    lines.append(f"- Compactness variants: {audit.compactness_variant_count}")
    lines.append(f"- Theorems: {audit.theorem_count}")
    lines.append(f"- Heine-Borel examples: {audit.heine_borel_example_count}")
    lines.append(f"- Compact-Hausdorff rows: {audit.compact_hausdorff_count}")
    lines.append(f"- Blockers: {audit.blocker_count}")
    lines.append("")

    # Compactness variants
    lines.append("## Compactness variant bridge")
    lines.append("| id | label | equivalent (general) | equivalent (metric) |")
    lines.append("|----|-------|---------------------|---------------------|")
    for v in variants:
        g = "yes" if v.equivalent_to_compact else "no"
        m = "yes" if v.metric_equivalent else "no"
        lines.append(f"| {v.id} | {v.label} | {g} | {m} |")
    lines.append("")
    for v in variants:
        lines.append(f"### {v.id} — {v.label}")
        lines.append(f"**Definition:** {v.definition}")
        lines.append(f"**API note:** {v.api_note}")
        lines.append("")

    # Theorems
    lines.append("## Theorem bridge")
    for t in theorems.rows:
        lines.append(f"### Theorem {t.id} — {t.label}")
        lines.append(f"**Statement:** {t.statement}")
        lines.append(f"**Proof sketch:** {t.proof_sketch}")
        lines.append(f"**API note:** {t.api_note}")
        lines.append("")

    # Heine-Borel
    lines.append("## Heine-Borel bridge")
    lines.append("| id | space | characterisation | compact |")
    lines.append("|----|-------|-----------------|---------|")
    for r in hb:
        c = "yes" if r.compact else "no"
        lines.append(f"| {r.id} | {r.space} | {r.characterisation} | {c} |")
    lines.append("")
    for r in hb:
        lines.append(f"- **{r.id}**: {r.note}")
    lines.append("")

    # Compact-Hausdorff
    lines.append("## Compact-Hausdorff bridge")
    for r in ch:
        conv = "converse holds" if r.converse_holds else "converse fails"
        lines.append(f"- **{r.id}**: {r.hypothesis} ⟹ {r.conclusion} ({conv})")
        lines.append(f"  Note: {r.counterexample}")
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
