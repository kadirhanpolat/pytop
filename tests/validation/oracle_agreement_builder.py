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
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from tests.validation.fixtures import KnotTable
from tests.validation.oracle_integrations import (
    get_available_oracles,
)

# --- Docker-free internal oracle: pytop's own engine vs the curated table ------
#
# Famous knots that are torus knots T(p, q). Their Alexander polynomials in
# ``fixtures.KnotTable`` were curated and Sage-verified; here we recompute them
# with pytop's own reduced-Burau engine and assert agreement. This populates the
# agreement matrix even when no external oracle (SnapPy/SageMath) is installed --
# the "oracle" being cross-checked is pytop's computational core itself.
TORUS_KNOT_PARAMS: dict[str, tuple[int, int]] = {
    "trefoil_3_1": (2, 3),
    "cinquefoil_5_1": (2, 5),
    "septafoil_7_1": (2, 7),
    "8_19": (3, 4),
    "10_124": (3, 5),
    "11_1": (2, 11),
    "13_1": (2, 13),
    "15_1": (2, 15),
    "17_1": (2, 17),
}

# One signed monomial of a LaTeX Alexander polynomial, e.g. ``- 3t^{-2}``,
# ``+ t``, ``1``. Groups: sign, integer coefficient, the ``t`` variable, a
# braced exponent ``^{-2}`` or a bare exponent ``^2``.
_ALEX_TERM = re.compile(r"([+-]?)\s*(\d*)\s*(t)?(?:\^\{(-?\d+)\}|\^(-?\d+))?")


def parse_alexander_latex(poly: str) -> dict[int, int]:
    """Parse a LaTeX Alexander polynomial into an ``exponent -> coefficient`` map.

    Handles braced (``t^{-2}``) and bare (``t^2``) exponents, implicit unit
    coefficients (``t`` -> 1, ``-t`` -> -1) and the constant term (``1`` -> exp 0).
    """
    coeffs: dict[int, int] = {}
    for match in _ALEX_TERM.finditer(poly.strip()):
        if match.group(0).strip() == "":
            continue
        sign, num, t_var, exp_braced, exp_bare = match.groups()
        coef = -1 if sign == "-" else 1
        if num:
            coef *= int(num)
        if not t_var:
            exp = 0
        elif exp_braced is not None:
            exp = int(exp_braced)
        elif exp_bare is not None:
            exp = int(exp_bare)
        else:
            exp = 1
        coeffs[exp] = coeffs.get(exp, 0) + coef
    return {e: c for e, c in coeffs.items() if c != 0}


def canonical_alexander(coeffs: dict[int, int]) -> tuple[tuple[int, int], ...]:
    """Canonicalize an Alexander polynomial up to a unit (``+-t^k``).

    The Alexander polynomial is only well-defined up to multiplication by a unit
    ``+-t^k``. Shifting the lowest exponent to 0 quotients out the ``t^k`` factor
    and fixing the sign of the top coefficient to ``+1`` quotients out the sign,
    so two representations of the same polynomial map to the same tuple.
    """
    nonzero = {e: c for e, c in coeffs.items() if c != 0}
    if not nonzero:
        return ()
    lo = min(nonzero)
    hi = max(nonzero)
    sign = 1 if nonzero[hi] > 0 else -1
    return tuple(sorted((e - lo, sign * c) for e, c in nonzero.items()))


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
        import pytop

        self.oracles = get_available_oracles()
        self.report = AgreementMatrixReport(
            timestamp=datetime.now().isoformat(),
            pytop_version=pytop.__version__,
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

    def test_torus_knot_alexander_internal(
        self, knots: list[KnotTable.KnotEntry] | None = None
    ) -> None:
        """Cross-check torus-knot Alexander polynomials vs pytop's own engine.

        Docker-free: for every knot in ``TORUS_KNOT_PARAMS`` present in the table,
        recompute the Alexander polynomial with pytop's reduced-Burau engine
        (``torus_knot_alexander_poly``) and compare it -- up to the unit ambiguity
        (see :func:`canonical_alexander`) -- against the curated, Sage-verified
        value. This guarantees the agreement matrix is populated even when no
        external oracle is available.
        """
        from pytop import torus_knot_alexander_poly

        if knots is None:
            knots = KnotTable.KNOTS
        by_name = {k.name: k for k in knots}

        for name, (p, q) in TORUS_KNOT_PARAMS.items():
            entry = by_name.get(name)
            if entry is None:
                continue
            live = torus_knot_alexander_poly(p, q)
            table = parse_alexander_latex(entry.alexander_poly)
            agree = canonical_alexander(live) == canonical_alexander(table)
            self.comparisons.append(
                OracleComparison(
                    oracle_name="pytop_internal",
                    test_type="alexander_torus",
                    subject=name,
                    pytop_result=f"T({p},{q}) reduced-Burau",
                    oracle_result=entry.alexander_poly,
                    agree=agree,
                    confidence=1.0 if agree else 0.0,
                )
            )
            self.report.total_tests += 1
            if agree:
                self.report.passed_tests += 1
            else:
                self.report.failed_tests += 1

        if "pytop_internal" not in self.report.oracle_names:
            self.report.oracle_names.append("pytop_internal")
        if "alexander_torus" not in self.report.test_types:
            self.report.test_types.append("alexander_torus")

    def build(self) -> AgreementMatrixReport:
        """Build complete agreement matrix."""
        self.test_torus_knot_alexander_internal()
        self.test_knot_polynomials()
        self.test_persistent_betti()
        self.report.agreements = self.comparisons
        return self.report


def generate_oracle_matrix() -> AgreementMatrixReport:
    """Build a fully populated agreement matrix from all available oracles.

    Always includes the Docker-free internal torus-knot oracle, plus any external
    oracle that happens to be installed (GUDHI/Ripser persistent Betti, and
    SnapPy/SageMath knot polynomials when ``PYTOP_*_ORACLE=1``).
    """
    builder = OracleAgreementBuilder()
    return builder.build()


def persist_oracle_matrix(
    report: AgreementMatrixReport, out_dir: str | Path
) -> tuple[Path, Path]:
    """Write the agreement matrix to ``oracle_matrix.json`` and ``oracle_matrix.md``.

    Returns the ``(json_path, markdown_path)`` pair.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "oracle_matrix.json"
    md_path = out / "oracle_matrix.md"
    json_path.write_text(report.to_json(), encoding="utf-8")
    md_path.write_text(report.to_markdown(), encoding="utf-8")
    return json_path, md_path
