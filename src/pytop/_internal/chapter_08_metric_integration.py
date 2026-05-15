"""Chapter 08 metric-space manuscript integration helpers.

v1.0.322 opens the Chapter 08 integration work described in the v1.0.320
manuscript target map.  The module provides:

- A metric axiom validation bridge (M1-M4) with API notes.
- An equivalent-metrics bridge recording the same-topology characterisation.
- An isometry-vs-homeomorphism contract (Theorem 8.10 + non-converse example).
- A norm-induced-metric bridge (Theorem 8.13, N1-N3, four norm examples).
- A Chapter 08 integration audit helper.

Originality guardrails
----------------------
All prose and wording is written in the book voice and derived from the active
API / examples_bank.  Nothing is copied from uploaded Chapter 08 zip files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .result import Result

CHAPTER_08_INTEGRATION_VERSION = "v1.0.322"

# ---------------------------------------------------------------------------
# Metric axiom bridge
# ---------------------------------------------------------------------------

METRIC_AXIOMS = (
    {"id": "M1", "label": "Non-negativity and self-distance zero",
     "statement": "d(a, b) >= 0 and d(a, a) = 0 for all a, b in X.",
     "api_note": "The metric_spaces.py axiom checker verifies M1 by testing all (a,a) pairs."},
    {"id": "M2", "label": "Symmetry",
     "statement": "d(a, b) = d(b, a) for all a, b in X.",
     "api_note": "Symmetry is checked pair-wise over the finite carrier in metric_spaces.py."},
    {"id": "M3", "label": "Triangle inequality",
     "statement": "d(a, c) <= d(a, b) + d(b, c) for all a, b, c in X.",
     "api_note": "Checked over all triples. The weaker M3* (distinct triples only) suffices -- M1 fills the rest."},
    {"id": "M4", "label": "Positive definiteness",
     "statement": "If a != b then d(a, b) > 0.",
     "api_note": "M4 checked by confirming d(a,b) > 0 whenever a != b. Pseudometrics satisfy M1-M3 but not M4."},
)

STANDARD_METRIC_TRANSFORMS = (
    {"id": "truncated", "label": "Truncated metric",
     "formula": "e(a, b) = min(1, d(a, b))", "preserves_topology": True,
     "note": "Bounded by 1; induces the same topology as d."},
    {"id": "standard_bounded", "label": "Standard bounded metric",
     "formula": "e(a, b) = d(a, b) / (1 + d(a, b))", "preserves_topology": True,
     "note": "Values in [0, 1). Triangle inequality via monotone-ratio argument."},
)


@dataclass(frozen=True, slots=True)
class MetricAxiomRow:
    id: str
    label: str
    statement: str
    api_note: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "statement": self.statement, "api_note": self.api_note}


@dataclass(frozen=True, slots=True)
class MetricTransformRow:
    id: str
    label: str
    formula: str
    preserves_topology: bool
    note: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "formula": self.formula,
                "preserves_topology": self.preserves_topology, "note": self.note}


def build_metric_axiom_bridge() -> tuple[MetricAxiomRow, ...]:
    return tuple(MetricAxiomRow(**a) for a in METRIC_AXIOMS)


def build_metric_transform_bridge() -> tuple[MetricTransformRow, ...]:
    return tuple(MetricTransformRow(**t) for t in STANDARD_METRIC_TRANSFORMS)


# ---------------------------------------------------------------------------
# Equivalent-metrics bridge
# ---------------------------------------------------------------------------

EQUIVALENT_METRICS_EXAMPLES = (
    {"id": "R2_usual_d1_d2", "label": "Euclidean, max, and taxicab metrics on R^2",
     "description": "All three induce the usual topology on R^2 (Example 6.1).",
     "equivalent": True},
    {"id": "trivial_vs_d2_discrete", "label": "Trivial metric vs d(a,b)=2 (a!=b)",
     "description": "Both induce the discrete topology; S(p,1/2)={p} in both cases.",
     "equivalent": True},
    {"id": "usual_vs_indiscrete_R", "label": "Usual metric vs indiscrete topology on R",
     "description": "The indiscrete topology on R is not metrizable; not equivalent to the usual metric.",
     "equivalent": False},
)


@dataclass(frozen=True, slots=True)
class EquivalentMetricsRow:
    id: str
    label: str
    description: str
    equivalent: bool

    @property
    def status(self) -> str:
        return "equivalent" if self.equivalent else "not_equivalent"

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "description": self.description,
                "equivalent": self.equivalent, "status": self.status}


@dataclass(frozen=True, slots=True)
class EquivalentMetricsBridge:
    version: str
    rows: tuple[EquivalentMetricsRow, ...]
    same_topology_criterion: str
    api_reference: str

    @property
    def equivalent_count(self) -> int:
        return sum(1 for r in self.rows if r.equivalent)

    @property
    def non_equivalent_count(self) -> int:
        return sum(1 for r in self.rows if not r.equivalent)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "same_topology_criterion": self.same_topology_criterion,
            "api_reference": self.api_reference,
            "equivalent_count": self.equivalent_count,
            "non_equivalent_count": self.non_equivalent_count,
            "rows": [r.to_dict() for r in self.rows],
        }


def build_equivalent_metrics_bridge() -> EquivalentMetricsBridge:
    rows = tuple(EquivalentMetricsRow(**r) for r in EQUIVALENT_METRICS_EXAMPLES)
    return EquivalentMetricsBridge(
        version=CHAPTER_08_INTEGRATION_VERSION,
        rows=rows,
        same_topology_criterion=(
            "Two metrics d and d* on X are equivalent iff their open-sphere families "
            "are bases for the same topology on X."
        ),
        api_reference="metric_spaces.are_equivalent_metrics / metric_contracts.py",
    )


# ---------------------------------------------------------------------------
# Isometry vs homeomorphism contract
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class IsometryHomeomorphismContract:
    version: str
    isometry_definition: str
    homeomorphism_note: str
    theorem_8_10: str
    non_converse_example: str
    direction: str
    api_references: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "isometry_definition": self.isometry_definition,
            "homeomorphism_note": self.homeomorphism_note,
            "theorem_8_10": self.theorem_8_10,
            "non_converse_example": self.non_converse_example,
            "direction": self.direction,
            "api_references": list(self.api_references),
        }


def build_isometry_homeomorphism_contract() -> IsometryHomeomorphismContract:
    return IsometryHomeomorphismContract(
        version=CHAPTER_08_INTEGRATION_VERSION,
        isometry_definition=(
            "A metric space (X, d) is isometric to (Y, e) iff there exists a bijection "
            "f : X -> Y such that d(p, q) = e(f(p), f(q)) for all p, q in X."
        ),
        homeomorphism_note=(
            "Every isometry is a homeomorphism (bijective, continuous, open), "
            "but the converse fails."
        ),
        theorem_8_10=(
            "Theorem 8.10: If (X, d) is isometric to (Y, e), then (X, d) is homeomorphic "
            "to (Y, e). The isometry relation is an equivalence relation on metric spaces."
        ),
        non_converse_example=(
            "Counter-example (Example 8.1): Let d be the trivial metric on X and "
            "e(a,b)=2 (a!=b) on Y with |X|=|Y|>1. Both induce the discrete topology, "
            "so the spaces are homeomorphic but not isometric (d(a,b)=1 != 2=e(f(a),f(b)))."
        ),
        direction="isometry => homeomorphism (converse fails in general)",
        api_references=(
            "maps.is_homeomorphism_map",
            "metric_spaces.are_isometric",
            "metric_contracts.py",
        ),
    )


# ---------------------------------------------------------------------------
# Norm-induced metric bridge
# ---------------------------------------------------------------------------

NORM_AXIOMS = (
    {"id": "N1", "label": "Zero norm iff zero vector",
     "statement": "||v|| >= 0 and ||v|| = 0 iff v = 0.",
     "induced_metric_note": "N1 implies M1 and M4 for the induced metric d(v,w) = ||v-w||."},
    {"id": "N2", "label": "Subadditivity (triangle inequality for norms)",
     "statement": "||v + w|| <= ||v|| + ||w||.",
     "induced_metric_note": (
         "N2 gives M3 for the induced metric: "
         "d(v,u) = ||v-u|| = ||(v-w)+(w-u)|| <= ||v-w||+||w-u|| = d(v,w)+d(w,u)."
     )},
    {"id": "N3", "label": "Homogeneity",
     "statement": "||kv|| = |k| ||v|| for all k in R.",
     "induced_metric_note": "N3 is a scaling axiom for norms; no direct metric-axiom analogue."},
)

NORM_EXAMPLES = (
    {"id": "euclidean_norm_Rm", "label": "Euclidean norm on R^m",
     "formula": "||<a1,...,am>|| = sqrt(sum ai^2)",
     "induced_metric": "Euclidean metric on R^m",
     "note": "Induces the usual topology on R^m."},
    {"id": "sup_norm_C01", "label": "Sup-norm on C[0,1]",
     "formula": "||f|| = sup{|f(x)| : x in [0,1]}",
     "induced_metric": "d*(f,g) = sup{|f(x)-g(x)| : x in [0,1]}",
     "note": "Example 1.4 / 10.4 in the reference."},
    {"id": "L1_norm_C01", "label": "L1-norm on C[0,1]",
     "formula": "||f|| = integral_0^1 |f(x)| dx",
     "induced_metric": "d(f,g) = integral_0^1 |f(x)-g(x)| dx",
     "note": "Example 1.3 / 10.3 in the reference; measures area between functions."},
    {"id": "l2_norm_Hilbert", "label": "l2-norm on R^inf (Hilbert space)",
     "formula": "||<an>|| = sqrt(sum |an|^2)",
     "induced_metric": "l2-metric: d(p,q) = sqrt(sum |an-bn|^2)",
     "note": "Induces the l2-metric on Hilbert space H."},
)


@dataclass(frozen=True, slots=True)
class NormAxiomRow:
    id: str
    label: str
    statement: str
    induced_metric_note: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "statement": self.statement,
                "induced_metric_note": self.induced_metric_note}


@dataclass(frozen=True, slots=True)
class NormExampleRow:
    id: str
    label: str
    formula: str
    induced_metric: str
    note: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "formula": self.formula,
                "induced_metric": self.induced_metric, "note": self.note}


@dataclass(frozen=True, slots=True)
class NormInducedMetricBridge:
    version: str
    theorem_8_13: str
    axiom_rows: tuple[NormAxiomRow, ...]
    example_rows: tuple[NormExampleRow, ...]
    api_reference: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "theorem_8_13": self.theorem_8_13,
            "axiom_rows": [r.to_dict() for r in self.axiom_rows],
            "example_rows": [r.to_dict() for r in self.example_rows],
            "api_reference": self.api_reference,
        }


def build_norm_induced_metric_bridge() -> NormInducedMetricBridge:
    return NormInducedMetricBridge(
        version=CHAPTER_08_INTEGRATION_VERSION,
        theorem_8_13=(
            "Theorem 8.13: Let V be a normed space with norm ||.||. "
            "The function d(v, w) = ||v - w|| is a metric on V, called the induced metric."
        ),
        axiom_rows=tuple(NormAxiomRow(**a) for a in NORM_AXIOMS),
        example_rows=tuple(NormExampleRow(**e) for e in NORM_EXAMPLES),
        api_reference="metric_spaces.metric_from_norm / metric_contracts.py",
    )


# ---------------------------------------------------------------------------
# Chapter 08 integration audit
# ---------------------------------------------------------------------------

CHAPTER_08_MANUSCRIPT_TARGETS = (
    "src/pytop/metric_spaces.py",
    "src/pytop/metric_contracts.py",
    "src/pytop/chapter_08_metric_integration.py",
    "docs/integration/chapter_07_15/chapter_08_metric_integration_v1_0_322.md",
    "docs/verification/chapter_08_metric_integration_v1_0_322.md",
    "tests/core/test_chapter_08_metric_integration_v322.py",
)

CHAPTER_08_INSERTION_POINTS = (
    "add metric-validation output boxes (axioms M1-M4 with API references)",
    "separate equivalent-metric and isometry examples with a distinction box",
    "add norm-induced metric bridge at the end of the normed-spaces section",
)


@dataclass(frozen=True, slots=True)
class Chapter08IntegrationAudit:
    version: str
    present_targets: tuple[str, ...]
    missing_targets: tuple[str, ...]
    insertion_points: tuple[str, ...]
    metric_axiom_count: int
    equivalent_metrics_example_count: int
    norm_axiom_count: int
    norm_example_count: int

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
            "metric_axiom_count": self.metric_axiom_count,
            "equivalent_metrics_example_count": self.equivalent_metrics_example_count,
            "norm_axiom_count": self.norm_axiom_count,
            "norm_example_count": self.norm_example_count,
        }

    def to_result(self) -> Result:
        result_status = "true" if self.blocker_count == 0 else "conditional"
        return Result(
            status=result_status,
            mode="exact",
            value=self.to_dict(),
            justification=[
                "Chapter 08 v1.0.322 integration audit: " + self.status + ".",
                "Metric axioms bridged: " + str(self.metric_axiom_count) + ".",
                "Equivalent-metrics examples: " + str(self.equivalent_metrics_example_count) + ".",
                "Norm axioms bridged: " + str(self.norm_axiom_count) + ".",
                "Norm-induced metric examples: " + str(self.norm_example_count) + ".",
                "Blockers: " + str(self.blocker_count) + ".",
            ],
            metadata=self.to_dict(),
        )


def build_chapter_08_integration_audit(package_root: str) -> Chapter08IntegrationAudit:
    root = Path(package_root)
    present = tuple(t for t in CHAPTER_08_MANUSCRIPT_TARGETS if (root / t).exists())
    missing = tuple(t for t in CHAPTER_08_MANUSCRIPT_TARGETS if t not in present)
    axioms = build_metric_axiom_bridge()
    eq_bridge = build_equivalent_metrics_bridge()
    norm_bridge = build_norm_induced_metric_bridge()
    return Chapter08IntegrationAudit(
        version=CHAPTER_08_INTEGRATION_VERSION,
        present_targets=present,
        missing_targets=missing,
        insertion_points=CHAPTER_08_INSERTION_POINTS,
        metric_axiom_count=len(axioms),
        equivalent_metrics_example_count=len(eq_bridge.rows),
        norm_axiom_count=len(norm_bridge.axiom_rows),
        norm_example_count=len(norm_bridge.example_rows),
    )


# ---------------------------------------------------------------------------
# Top-level summary and render
# ---------------------------------------------------------------------------

def chapter_08_integration_summary(package_root: str) -> dict[str, Any]:
    audit = build_chapter_08_integration_audit(package_root)
    axioms = build_metric_axiom_bridge()
    transforms = build_metric_transform_bridge()
    eq_bridge = build_equivalent_metrics_bridge()
    iso_contract = build_isometry_homeomorphism_contract()
    norm_bridge = build_norm_induced_metric_bridge()
    return {
        "version": CHAPTER_08_INTEGRATION_VERSION,
        "audit": audit.to_dict(),
        "metric_axiom_bridge": [a.to_dict() for a in axioms],
        "metric_transform_bridge": [t.to_dict() for t in transforms],
        "equivalent_metrics_bridge": eq_bridge.to_dict(),
        "isometry_homeomorphism_contract": iso_contract.to_dict(),
        "norm_induced_metric_bridge": norm_bridge.to_dict(),
    }


def render_chapter_08_integration_report(package_root: str) -> str:
    summary = chapter_08_integration_summary(package_root)
    audit = summary["audit"]
    eq_bridge = summary["equivalent_metrics_bridge"]
    iso = summary["isometry_homeomorphism_contract"]
    norm = summary["norm_induced_metric_bridge"]

    lines = [
        "# Chapter 08 Metric-Space Integration Report - " + CHAPTER_08_INTEGRATION_VERSION,
        "",
        "## Audit",
        "",
        "- Status: `" + audit["status"] + "`",
        "- Blocker count: `" + str(audit["blocker_count"]) + "`",
        "- Metric axioms bridged: `" + str(audit["metric_axiom_count"]) + "`",
        "- Equivalent-metrics examples: `" + str(audit["equivalent_metrics_example_count"]) + "`",
        "- Norm axioms bridged: `" + str(audit["norm_axiom_count"]) + "`",
        "- Norm-induced metric examples: `" + str(audit["norm_example_count"]) + "`",
        "",
        "## Metric axiom bridge (M1-M4)",
        "",
        "| ID | Label | Statement |",
        "|---|---|---|",
    ]
    for a in summary["metric_axiom_bridge"]:
        lines.append("| `" + a["id"] + "` | " + a["label"] + " | " + a["statement"] + " |")

    lines.extend([
        "",
        "## Metric transform bridge",
        "",
        "| ID | Label | Formula | Preserves topology |",
        "|---|---|---|---|",
    ])
    for t in summary["metric_transform_bridge"]:
        lines.append("| `" + t["id"] + "` | " + t["label"] + " | `" + t["formula"] + "` | `" + str(t["preserves_topology"]) + "` |")

    lines.extend([
        "",
        "## Equivalent-metrics bridge",
        "",
        "**Criterion:** " + eq_bridge["same_topology_criterion"],
        "",
        "| ID | Label | Status |",
        "|---|---|---|",
    ])
    for r in eq_bridge["rows"]:
        lines.append("| `" + r["id"] + "` | " + r["label"] + " | `" + r["status"] + "` |")

    lines.extend([
        "",
        "## Isometry vs homeomorphism contract",
        "",
        "**Theorem 8.10:** " + iso["theorem_8_10"],
        "",
        "**Direction:** `" + iso["direction"] + "`",
        "",
        "**Non-converse example:** " + iso["non_converse_example"],
        "",
        "## Norm-induced metric bridge",
        "",
        "**Theorem 8.13:** " + norm["theorem_8_13"],
        "",
        "### Norm axioms",
        "",
        "| ID | Label | Statement |",
        "|---|---|---|",
    ])
    for a in norm["axiom_rows"]:
        lines.append("| `" + a["id"] + "` | " + a["label"] + " | " + a["statement"] + " |")

    lines.extend([
        "",
        "### Norm-induced metric examples",
        "",
        "| ID | Label | Induced metric |",
        "|---|---|---|",
    ])
    for e in norm["example_rows"]:
        lines.append("| `" + e["id"] + "` | " + e["label"] + " | " + e["induced_metric"] + " |")

    lines.extend([
        "",
        "## Insertion points",
        "",
    ])
    for ip in audit["insertion_points"]:
        lines.append("- " + ip)

    lines.extend([
        "",
        "## Originality guardrails",
        "",
        "- Do not copy prose, examples, or exercises directly from uploaded chapter zips.",
        "- Rewrite examples in the book voice; keep examples_bank as the reusable source.",
        "- Use this report as the contract, not as prose to copy into the manuscript.",
    ])
    return "\n".join(lines) + "\n"
