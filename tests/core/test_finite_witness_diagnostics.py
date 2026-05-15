"""Tests for finite_witness_diagnostics.py."""

import pytest
from pytop.finite_witness_diagnostics import (
    NegativeWitnessCase,
    NegativeWitnessReport,
    build_negative_witness_cases,
    negative_witness_case_summary,
    render_negative_witness_diagnostics_report,
    run_all_negative_witness_cases,
    run_negative_witness_case,
    validate_negative_witness_diagnostics,
)

ALL_CODES = [
    "NEG-TOPOLOGY-MISSING-EMPTY",
    "NEG-TOPOLOGY-UNION-FAILURE",
    "NEG-BASIS-INTERSECTION-WITNESS",
    "NEG-MAP-MISSING-DOMAIN-POINT",
    "NEG-MAP-OUTSIDE-CODOMAIN",
    "NEG-CONTINUITY-PREIMAGE-FAILURE",
]


# ---------------------------------------------------------------------------
# NegativeWitnessCase
# ---------------------------------------------------------------------------

class TestNegativeWitnessCase:
    def test_valid_case_created(self):
        c = NegativeWitnessCase(
            code="NEG-TEST",
            label="test case",
            engine_area="finite_operator_engine",
            failure_kind="test_failure",
            learning_target="test target",
            expected_witness_key="test_key",
        )
        assert c.code == "NEG-TEST"

    def test_code_must_start_with_neg(self):
        with pytest.raises(ValueError):
            NegativeWitnessCase(
                code="BAD-CODE",
                label="x",
                engine_area="e",
                failure_kind="f",
                learning_target="l",
                expected_witness_key="k",
            )

    def test_empty_engine_area_raises(self):
        with pytest.raises(ValueError):
            NegativeWitnessCase(
                code="NEG-X",
                label="x",
                engine_area="",
                failure_kind="f",
                learning_target="l",
                expected_witness_key="k",
            )

    def test_empty_witness_key_raises(self):
        with pytest.raises(ValueError):
            NegativeWitnessCase(
                code="NEG-X",
                label="x",
                engine_area="e",
                failure_kind="f",
                learning_target="l",
                expected_witness_key="",
            )


# ---------------------------------------------------------------------------
# build_negative_witness_cases
# ---------------------------------------------------------------------------

class TestBuildNegativeWitnessCases:
    def test_returns_tuple(self):
        cases = build_negative_witness_cases()
        assert isinstance(cases, tuple)

    def test_six_cases(self):
        cases = build_negative_witness_cases()
        assert len(cases) == 6

    def test_all_instances_are_negative_witness_case(self):
        for case in build_negative_witness_cases():
            assert isinstance(case, NegativeWitnessCase)

    def test_all_codes_present(self):
        codes = {c.code for c in build_negative_witness_cases()}
        for code in ALL_CODES:
            assert code in codes


# ---------------------------------------------------------------------------
# negative_witness_case_summary
# ---------------------------------------------------------------------------

class TestNegativeWitnessCaseSummary:
    def test_returns_dict(self):
        s = negative_witness_case_summary()
        assert isinstance(s, dict)

    def test_case_count_is_six(self):
        s = negative_witness_case_summary()
        assert s["case_count"] == 6

    def test_operator_cases_present(self):
        s = negative_witness_case_summary()
        assert s["operator_case_count"] >= 1

    def test_map_cases_present(self):
        s = negative_witness_case_summary()
        assert s["map_case_count"] >= 1

    def test_basis_cases_present(self):
        s = negative_witness_case_summary()
        assert s["basis_case_count"] >= 1


# ---------------------------------------------------------------------------
# run_negative_witness_case — individual codes
# ---------------------------------------------------------------------------

class TestRunNegativeWitnessCase:
    @pytest.mark.parametrize("code", ALL_CODES)
    def test_each_code_returns_report(self, code):
        report = run_negative_witness_case(code)
        assert isinstance(report, NegativeWitnessReport)

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_each_code_passes(self, code):
        report = run_negative_witness_case(code)
        assert report.passed, f"{code} did not pass: witness={report.witness}"

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_report_has_code(self, code):
        report = run_negative_witness_case(code)
        assert report.code == code

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_report_witness_is_dict(self, code):
        report = run_negative_witness_case(code)
        assert isinstance(report.witness, dict)

    def test_topology_missing_empty_witness_key(self):
        report = run_negative_witness_case("NEG-TOPOLOGY-MISSING-EMPTY")
        assert "missing_required" in report.witness

    def test_topology_union_failure_witness_key(self):
        report = run_negative_witness_case("NEG-TOPOLOGY-UNION-FAILURE")
        assert "union_failures" in report.witness

    def test_basis_intersection_witness_key(self):
        report = run_negative_witness_case("NEG-BASIS-INTERSECTION-WITNESS")
        assert "intersection_failures" in report.witness

    def test_map_missing_domain_witness_key(self):
        report = run_negative_witness_case("NEG-MAP-MISSING-DOMAIN-POINT")
        assert "exception" in report.witness

    def test_unknown_code_raises(self):
        with pytest.raises(KeyError):
            run_negative_witness_case("NEG-NONEXISTENT-CODE")

    def test_as_dict_keys(self):
        report = run_negative_witness_case("NEG-TOPOLOGY-MISSING-EMPTY")
        d = report.as_dict()
        for key in ("code", "passed", "engine_area", "failure_kind", "witness", "teaching_note"):
            assert key in d


# ---------------------------------------------------------------------------
# run_all_negative_witness_cases
# ---------------------------------------------------------------------------

class TestRunAllNegativeWitnessCases:
    def test_returns_dict(self):
        results = run_all_negative_witness_cases()
        assert isinstance(results, dict)

    def test_all_codes_in_result(self):
        results = run_all_negative_witness_cases()
        for code in ALL_CODES:
            assert code in results

    def test_all_pass(self):
        results = run_all_negative_witness_cases()
        for code, report in results.items():
            assert report.passed, f"{code} did not pass"


# ---------------------------------------------------------------------------
# validate_negative_witness_diagnostics
# ---------------------------------------------------------------------------

class TestValidateNegativeWitnessDiagnostics:
    def test_returns_dict(self):
        result = validate_negative_witness_diagnostics()
        assert isinstance(result, dict)

    def test_overall_passed(self):
        result = validate_negative_witness_diagnostics()
        assert result["passed"] is True

    def test_has_diagnostics(self):
        result = validate_negative_witness_diagnostics()
        assert "diagnostics" in result
        assert len(result["diagnostics"]) == 6

    def test_has_summary(self):
        result = validate_negative_witness_diagnostics()
        assert "summary" in result


# ---------------------------------------------------------------------------
# render_negative_witness_diagnostics_report
# ---------------------------------------------------------------------------

class TestRenderReport:
    def test_returns_string(self):
        s = render_negative_witness_diagnostics_report()
        assert isinstance(s, str)

    def test_contains_all_codes(self):
        s = render_negative_witness_diagnostics_report()
        for code in ALL_CODES:
            assert code in s

    def test_contains_version(self):
        s = render_negative_witness_diagnostics_report()
        assert "v1.0.184" in s
