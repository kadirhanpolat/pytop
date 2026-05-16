"""Finite negative witness diagnostics.

v1.0.184 adds a unified diagnostic layer for negative examples used by the
finite engines.  The goal is to make failures teachable: every negative case
returns a stable code, a failure kind, and a concrete witness extracted from
the existing finite operator, basis, and map engines.

No external exercise text or solution is copied here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .finite_basis_engine import analyze_basis
from .finite_map_engine import FiniteMapEngineError, analyze_finite_map, normalize_finite_map_data
from .finite_operator_engine import validate_topology_candidate


@dataclass(frozen=True)
class NegativeWitnessCase:
    code: str
    label: str
    engine_area: str
    failure_kind: str
    learning_target: str
    expected_witness_key: str

    def __post_init__(self) -> None:
        if not self.code.startswith("NEG-"):
            raise ValueError("negative witness case codes must start with NEG-")
        if not self.engine_area:
            raise ValueError("engine_area must not be empty")
        if not self.expected_witness_key:
            raise ValueError("expected_witness_key must not be empty")


@dataclass(frozen=True)
class NegativeWitnessReport:
    code: str
    passed: bool
    engine_area: str
    failure_kind: str
    witness: dict[str, Any]
    teaching_note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "passed": self.passed,
            "engine_area": self.engine_area,
            "failure_kind": self.failure_kind,
            "witness": self.witness,
            "teaching_note": self.teaching_note,
        }


_CASES = (
    NegativeWitnessCase(
        code="NEG-TOPOLOGY-MISSING-EMPTY",
        label="Topology candidate missing the empty open",
        engine_area="finite_operator_engine",
        failure_kind="missing_required_open",
        learning_target="A topology must include the empty set and the carrier.",
        expected_witness_key="missing_required",
    ),
    NegativeWitnessCase(
        code="NEG-TOPOLOGY-UNION-FAILURE",
        label="Topology candidate closed under neither the required union witness nor generated union",
        engine_area="finite_operator_engine",
        failure_kind="union_closure_failure",
        learning_target="A finite open family must be closed under finite unions; the witness records the missing union.",
        expected_witness_key="union_failures",
    ),
    NegativeWitnessCase(
        code="NEG-BASIS-INTERSECTION-WITNESS",
        label="Basis candidate fails the pointwise intersection witness condition",
        engine_area="finite_basis_engine",
        failure_kind="basis_intersection_failure",
        learning_target="Covering the carrier is not enough; pairwise overlaps need local basis refinements.",
        expected_witness_key="intersection_failures",
    ),
    NegativeWitnessCase(
        code="NEG-MAP-MISSING-DOMAIN-POINT",
        label="Finite map is not total on the domain",
        engine_area="finite_map_engine",
        failure_kind="missing_domain_point",
        learning_target="A finite map contract must assign one codomain value to every domain point.",
        expected_witness_key="exception",
    ),
    NegativeWitnessCase(
        code="NEG-MAP-OUTSIDE-CODOMAIN",
        label="Finite map sends a point outside the declared codomain",
        engine_area="finite_map_engine",
        failure_kind="outside_codomain_value",
        learning_target="A well-defined map into Y must have all values in Y.",
        expected_witness_key="exception",
    ),
    NegativeWitnessCase(
        code="NEG-CONTINUITY-PREIMAGE-FAILURE",
        label="Bijective finite map that is not continuous",
        engine_area="finite_map_engine",
        failure_kind="continuity_preimage_failure",
        learning_target="Continuity is checked by preimages of codomain opens, not by image behavior.",
        expected_witness_key="failed_preimage_checks",
    ),
)


def build_negative_witness_cases() -> tuple[NegativeWitnessCase, ...]:
    return _CASES


def negative_witness_case_summary() -> dict[str, int]:
    cases = build_negative_witness_cases()
    return {
        "case_count": len(cases),
        "operator_case_count": sum(case.engine_area == "finite_operator_engine" for case in cases),
        "basis_case_count": sum(case.engine_area == "finite_basis_engine" for case in cases),
        "map_case_count": sum(case.engine_area == "finite_map_engine" for case in cases),
        "failure_kind_count": len({case.failure_kind for case in cases}),
    }


def run_negative_witness_case(code: str) -> NegativeWitnessReport:
    if code == "NEG-TOPOLOGY-MISSING-EMPTY":
        validation = validate_topology_candidate({0, 1}, [{0, 1}])
        return NegativeWitnessReport(
            code=code,
            passed=not validation.is_topology and frozenset() in validation.missing_required,
            engine_area="finite_operator_engine",
            failure_kind="missing_required_open",
            witness={
                "missing_required": validation.missing_required,
                "failure_count": validation.failure_count,
            },
            teaching_note="The family contains the carrier but omits the empty open.",
        )

    if code == "NEG-TOPOLOGY-UNION-FAILURE":
        validation = validate_topology_candidate({0, 1, 2}, [set(), {0}, {1}, {0, 1, 2}])
        union_witnesses = validation.union_failures
        return NegativeWitnessReport(
            code=code,
            passed=not validation.is_topology and any(item[2] == frozenset({0, 1}) for item in union_witnesses),
            engine_area="finite_operator_engine",
            failure_kind="union_closure_failure",
            witness={
                "union_failures": union_witnesses,
                "failure_count": validation.failure_count,
            },
            teaching_note="The opens {0} and {1} are present, but their union {0,1} is missing.",
        )

    if code == "NEG-BASIS-INTERSECTION-WITNESS":
        analysis = analyze_basis({0, 1, 2}, [{0, 1}, {1, 2}])
        return NegativeWitnessReport(
            code=code,
            passed=not analysis.is_basis and any(item[3] == frozenset({1}) for item in analysis.intersection_failures),
            engine_area="finite_basis_engine",
            failure_kind="basis_intersection_failure",
            witness={
                "coverage_missing": analysis.coverage_missing,
                "intersection_failures": analysis.intersection_failures,
                "failure_count": analysis.failure_count,
            },
            teaching_note="The two basis candidates overlap at {1}, but no basis member refines that overlap around point 1.",
        )

    if code == "NEG-MAP-MISSING-DOMAIN-POINT":
        try:
            normalize_finite_map_data({"a", "b"}, {0, 1}, {"a": 0})
        except FiniteMapEngineError as exc:
            return NegativeWitnessReport(
                code=code,
                passed="missing domain points" in str(exc),
                engine_area="finite_map_engine",
                failure_kind="missing_domain_point",
                witness={"exception": str(exc)},
                teaching_note="The mapping does not assign an image to every domain point.",
            )
        return _unexpected_success(code, "finite_map_engine", "missing_domain_point")

    if code == "NEG-MAP-OUTSIDE-CODOMAIN":
        try:
            normalize_finite_map_data({"a", "b"}, {0, 1}, {"a": 0, "b": 2})
        except FiniteMapEngineError as exc:
            return NegativeWitnessReport(
                code=code,
                passed="outside the codomain" in str(exc),
                engine_area="finite_map_engine",
                failure_kind="outside_codomain_value",
                witness={"exception": str(exc)},
                teaching_note="The mapping is total, but one value is not in the declared codomain.",
            )
        return _unexpected_success(code, "finite_map_engine", "outside_codomain_value")

    if code == "NEG-CONTINUITY-PREIMAGE-FAILURE":
        analysis = analyze_finite_map(
            {"a", "b"},
            [set(), {"a", "b"}],
            {0, 1},
            [set(), {1}, {0, 1}],
            {"a": 0, "b": 1},
        )
        failed = tuple(item for item in analysis.continuity_checks if not item[2])
        return NegativeWitnessReport(
            code=code,
            passed=analysis.is_bijective and not analysis.is_continuous and any(item[1] == frozenset({"b"}) for item in failed),
            engine_area="finite_map_engine",
            failure_kind="continuity_preimage_failure",
            witness={
                "is_bijective": analysis.is_bijective,
                "is_continuous": analysis.is_continuous,
                "failed_preimage_checks": failed,
            },
            teaching_note="The codomain open {1} has preimage {b}, which is not open in the indiscrete domain.",
        )

    raise KeyError(f"unknown negative witness case: {code}")


def run_all_negative_witness_cases() -> dict[str, NegativeWitnessReport]:
    return {case.code: run_negative_witness_case(case.code) for case in build_negative_witness_cases()}


def validate_negative_witness_diagnostics() -> dict[str, object]:
    diagnostics = []
    for case in build_negative_witness_cases():
        report = run_negative_witness_case(case.code)
        diagnostics.append({
            "code": case.code,
            "engine_area": case.engine_area,
            "failure_kind": case.failure_kind,
            "expected_witness_key": case.expected_witness_key,
            "has_expected_key": case.expected_witness_key in report.witness,
            "passed": report.passed and case.expected_witness_key in report.witness,
        })
    return {
        "passed": all(item["passed"] for item in diagnostics),
        "diagnostics": tuple(diagnostics),
        "summary": negative_witness_case_summary(),
    }


def render_negative_witness_diagnostics_report() -> str:
    lines = [
        "Finite negative witness diagnostics — v1.0.184",
        "Each case turns a failure into a stable, teachable witness.",
        "",
    ]
    for case in build_negative_witness_cases():
        report = run_negative_witness_case(case.code)
        lines.extend([
            f"- {case.code}: {case.label}",
            f"  engine: {case.engine_area}",
            f"  failure: {case.failure_kind}",
            f"  passed: {report.passed}",
            f"  learning target: {case.learning_target}",
        ])
    return "\n".join(lines)


def _unexpected_success(code: str, engine_area: str, failure_kind: str) -> NegativeWitnessReport:
    return NegativeWitnessReport(
        code=code,
        passed=False,
        engine_area=engine_area,
        failure_kind=failure_kind,
        witness={},
        teaching_note="The negative case unexpectedly succeeded.",
    )


__all__ = [
    "NegativeWitnessCase",
    "NegativeWitnessReport",
    "build_negative_witness_cases",
    "negative_witness_case_summary",
    "run_negative_witness_case",
    "run_all_negative_witness_cases",
    "validate_negative_witness_diagnostics",
    "render_negative_witness_diagnostics_report",
]
