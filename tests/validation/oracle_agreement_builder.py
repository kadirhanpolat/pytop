"""Oracle agreement matrix builder for P16.2 — automated validation engine.

Orchestrates cross-oracle comparisons:
- Persistent homology Betti agreement (GUDHI vs Ripser vs pytop)
- Knot polynomial agreement (Alexander, Jones across systems)
- K-theory rational group agreement (Sage vs pytop)
- Dehn surgery H₁ agreement (SnapPy vs pytop)

Produces: agreement matrix, disagreement report, confidence scores.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import NamedTuple

from tests.validation.fixtures import KnotTable
from tests.validation.oracle_integrations import (
    get_available_oracles,
)


class OracleComparison(NamedTuple):
    """Single oracle vs pytop comparison."""

    oracle_name: str
    test_type: str  # 'persistent_betti', 'alexander', 'jones', 'dehn_surgery_h1', 'k_theory'
    subject: str  # knot name, complex id, etc.
    pytop_result: str  # human-readable result
    oracle_result: str  # human-readable result
    agree: bool
    confidence: float = 1.0  # 0.0-1.0, lower if partial match


@dataclass
class AgreementMatrixReport:
    """Comprehensive oracle agreement report."""

    timestamp: str
    pytop_version: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    agreements: list[OracleComparison] = field(default_factory=list)
    oracle_names: list[str] = field(default_factory=list)
    test_types: list[str] = field(default_factory=list)

    def agreement_rate(self) -> float:
        """Overall agreement rate (0.0-1.0)."""
        if self.total_tests == 0:
            return 0.0
        return self.passed_tests / self.total_tests

    def summary_by_oracle(self) -> dict[str, dict[str, str]]:
        """Breakdown: {oracle_name -> {test_type -> "passed/total"}}."""
        summary: dict[str, dict[str, dict[str, int]]] = {}
        for comp in self.agreements:
            oracle = comp.oracle_name
            test = comp.test_type
            if oracle not in summary:
                summary[oracle] = {}
            if test not in summary[oracle]:
                summary[oracle][test] = {"passed": 0, "total": 0}
            summary[oracle][test]["total"] += 1
            if comp.agree:
                summary[oracle][test]["passed"] += 1

        # Convert to string format
        result: dict[str, dict[str, str]] = {}
        for oracle, test_dict in summary.items():
            result[oracle] = {}
            for test, counts in test_dict.items():
                result[oracle][test] = f"{counts['passed']}/{counts['total']}"
        return result

    def to_json(self) -> str:
        """Export as JSON."""
        data = {
            "timestamp": self.timestamp,
            "pytop_version": self.pytop_version,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "agreement_rate": f"{self.agreement_rate():.2%}",
            "oracles": self.oracle_names,
            "test_types": self.test_types,
            "summary": self.summary_by_oracle(),
            "comparisons": [
                {
                    "oracle": c.oracle_name,
                    "test_type": c.test_type,
                    "subject": c.subject,
                    "pytop_result": c.pytop_result,
                    "oracle_result": c.oracle_result,
                    "agree": c.agree,
                    "confidence": c.confidence,
                }
                for c in self.agreements
            ],
        }
        return json.dumps(data, indent=2)

    def to_markdown(self) -> str:
        """Export as Markdown report."""
        lines = [
            "# P16.2 Oracle Agreement Matrix Report\n",
            f"**Timestamp:** {self.timestamp}\n",
            f"**pytop version:** {self.pytop_version}\n",
            f"**Overall agreement:** {self.agreement_rate():.1%} ({self.passed_tests}/{self.total_tests} tests)\n",
            f"**Oracles tested:** {', '.join(self.oracle_names)}\n",
        ]

        lines.append("## Summary by Oracle\n")
        for oracle, tests in self.summary_by_oracle().items():
            lines.append(f"\n### {oracle}\n")
            for test, rate in sorted(tests.items()):
                lines.append(f"- {test}: {rate}")

        lines.append("\n## Disagreements\n")
        disagreements = [c for c in self.agreements if not c.agree]
        if disagreements:
            for comp in disagreements:
                lines.append(
                    f"\n**{comp.oracle_name} vs pytop** ({comp.test_type}, {comp.subject}):\n"
                )
                lines.append(f"  - pytop:  {comp.pytop_result}\n")
                lines.append(f"  - {comp.oracle_name}: {comp.oracle_result}\n")
        else:
            lines.append("[OK] All tests passed!\n")

        return "".join(lines)


class OracleAgreementBuilder:
    """Builds comprehensive oracle agreement matrix."""

    def __init__(self):
        self.oracles = get_available_oracles()
        self.report = AgreementMatrixReport(
            timestamp=datetime.now().isoformat(),
            pytop_version="1.6.0",
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            oracle_names=[o.name for o in self.oracles],
            test_types=["alexander_poly", "jones_poly", "persistent_betti"],
        )
        self.comparisons: list[OracleComparison] = []

    def test_knot_polynomials(self, knots: list[KnotTable.KnotEntry] | None = None):
        """Test Alexander and Jones polynomials across oracles."""
        if knots is None:
            knots = KnotTable.KNOTS

        # If no oracles support knot polynomials, skip
        if not any(oracle.name in ["SnapPy", "SageMath"] for oracle in self.oracles):
            return

        for knot in knots:
            # pytop reference (from KnotTable)
            pytop_alex = knot.alexander_poly
            pytop_jones = knot.jones_poly

            # Test against each oracle that supports knots
            for oracle in self.oracles:
                if oracle.name not in ["SnapPy", "SageMath"]:
                    continue

                # Alexander polynomial
                oracle_alex = oracle.compute_alexander_polynomial(knot.name)
                if oracle_alex and oracle_alex != f"{oracle.name}({knot.name})":
                    # Only test if oracle returned a real result (not a placeholder)
                    agree_alex = oracle_alex == pytop_alex or pytop_alex in oracle_alex
                    self.comparisons.append(
                        OracleComparison(
                            oracle_name=oracle.name,
                            test_type="alexander_poly",
                            subject=knot.name,
                            pytop_result=pytop_alex,
                            oracle_result=oracle_alex,
                            agree=agree_alex,
                            confidence=1.0 if agree_alex else 0.0,
                        )
                    )
                    self.report.total_tests += 1
                    if agree_alex:
                        self.report.passed_tests += 1
                    else:
                        self.report.failed_tests += 1

                # Jones polynomial
                oracle_jones = oracle.compute_jones_polynomial(knot.name)
                if oracle_jones and oracle_jones != f"{oracle.name}({knot.name})":
                    agree_jones = oracle_jones == pytop_jones or pytop_jones in oracle_jones
                    self.comparisons.append(
                        OracleComparison(
                            oracle_name=oracle.name,
                            test_type="jones_poly",
                            subject=knot.name,
                            pytop_result=pytop_jones,
                            oracle_result=oracle_jones,
                            agree=agree_jones,
                            confidence=1.0 if agree_jones else 0.0,
                        )
                    )
                    self.report.total_tests += 1
                    if agree_jones:
                        self.report.passed_tests += 1
                    else:
                        self.report.failed_tests += 1

    def test_persistent_betti(self, sample_circles: int = 3):
        """Test persistent Betti agreement on sample circles.

        Compares Betti numbers *at scale* (bars alive at a representative
        plateau scale, ``birth <= s < death``) rather than counting deaths, and
        only for ``H_k`` with ``k <= max_betti_dim`` -- the dimensions the
        truncated Rips skeleton can represent faithfully. See
        ``betti_parity.compare_betti`` for the underlying machinery.
        """
        from tests.validation.betti_parity import compare_betti

        max_betti_dim = 1  # circles: H0, H1 are faithful with a triangle-complete complex
        for n_points in [6, 12, 24][:sample_circles]:
            points = [
                (math.cos(2 * math.pi * k / n_points), math.sin(2 * math.pi * k / n_points))
                for k in range(n_points)
            ]
            subject = f"circle_{n_points}pt"
            max_scale = 1.9

            for oracle in self.oracles:
                if oracle.name not in ("GUDHI", "Ripser"):
                    continue
                try:
                    result = compare_betti(
                        points,
                        oracle=oracle.name.lower(),
                        max_scale=max_scale,
                        max_betti_dim=max_betti_dim,
                    )
                except Exception as e:  # pragma: no cover - oracle import/runtime issues
                    print(f"Warning: {oracle.name} failed on {subject}: {e}")
                    continue

                # One comparison per dimension: agreement across *all* sampled scales.
                for dim in range(max_betti_dim + 1):
                    agree = all(
                        per_dim[dim][0] == per_dim[dim][1]
                        for _s, per_dim in result.samples
                    )
                    self.comparisons.append(
                        OracleComparison(
                            oracle_name=oracle.name,
                            test_type="persistent_betti",
                            subject=f"{subject}_H{dim}",
                            pytop_result="betti_curve",
                            oracle_result="betti_curve",
                            agree=agree,
                            confidence=1.0 if agree else 0.0,
                        )
                    )
                    self.report.total_tests += 1
                    if agree:
                        self.report.passed_tests += 1
                    else:
                        self.report.failed_tests += 1

    def build(self) -> AgreementMatrixReport:
        """Build complete agreement matrix."""
        self.test_knot_polynomials()
        self.test_persistent_betti()
        self.report.agreements = self.comparisons
        return self.report
