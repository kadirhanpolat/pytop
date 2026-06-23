"""Tests for benchmark_runner CLI tool (Phase 17 P17.1).

Tests for:
- run_benchmarks(): Subprocess execution and output capture
- generate_baseline_report(): Report generation and file I/O
- main(): CLI argument parsing and entry point
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest

from pytop._internal.benchmark_runner import (
    generate_baseline_report,
    main,
    run_benchmarks,
)


class TestRunBenchmarks:
    """Test run_benchmarks() function."""

    def test_run_benchmarks_returns_tuple(self) -> None:
        """Test that run_benchmarks returns (output, exit_code) tuple."""
        output, exit_code = run_benchmarks("all")

        assert isinstance(output, str), "Output should be a string"
        assert isinstance(exit_code, int), "Exit code should be an integer"

    def test_run_benchmarks_captures_output(self) -> None:
        """Test that run_benchmarks captures pytest output."""
        output, exit_code = run_benchmarks("all")

        # pytest output should contain session info
        assert "test session starts" in output, "Should contain pytest session info"
        assert "platform" in output, "Should contain platform info"

    def test_run_benchmarks_invalid_profile_type(self) -> None:
        """Test that run_benchmarks raises ValueError for invalid profile_type."""
        with pytest.raises(ValueError, match="Invalid profile_type"):
            run_benchmarks("invalid_profile")

    def test_run_benchmarks_valid_profile_types(self) -> None:
        """Test that all valid profile types are accepted."""
        valid_types = ["all", "homology", "persistence", "khovanov"]

        for profile_type in valid_types:
            output, exit_code = run_benchmarks(profile_type)
            assert isinstance(output, str), f"Should accept {profile_type}"
            assert isinstance(exit_code, int), f"Exit code should be int for {profile_type}"


class TestGenerateBaselineReport:
    """Test generate_baseline_report() function."""

    def test_generate_baseline_report_creates_file(self) -> None:
        """Test that generate_baseline_report creates output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            generate_baseline_report(str(output_path), profile_type="all")

            assert output_path.exists(), "Report file should be created"
            assert output_path.stat().st_size > 0, "Report file should not be empty"

    def test_generate_baseline_report_returns_exit_code(self) -> None:
        """Test that generate_baseline_report returns pytest exit code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            result = generate_baseline_report(str(output_path), profile_type="all")

            # Exit code could be 0 (all passed) or non-zero (some failed)
            assert isinstance(result, int), "Should return an integer exit code"

    def test_generate_baseline_report_contains_metadata(self) -> None:
        """Test that report contains expected metadata sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            generate_baseline_report(str(output_path), profile_type="all")

            content = output_path.read_text()

            # Check for expected sections
            assert "# Profile Report:" in content, "Should have title"
            assert "## Metadata" in content, "Should have metadata section"
            assert "## Function Breakdown" in content, "Should have breakdown section"
            assert "## Top Bottlenecks" in content, "Should have bottlenecks section"
            assert "## Benchmark Run Details" in content, "Should have run details"
            assert "Python Version:" in content, "Should have Python version"

    def test_generate_baseline_report_contains_pytest_output(self) -> None:
        """Test that report includes raw pytest output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            generate_baseline_report(str(output_path), profile_type="all")

            content = output_path.read_text()

            # Should include raw pytest output
            assert "test session starts" in content, "Should contain pytest output"

    def test_generate_baseline_report_creates_parent_dirs(self) -> None:
        """Test that generate_baseline_report creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "nested" / "report.md"

            # Parent dirs don't exist yet
            assert not output_path.parent.exists(), "Parent should not exist yet"

            generate_baseline_report(str(output_path), profile_type="all")

            # Parent dirs should be created
            assert output_path.parent.exists(), "Parent dirs should be created"
            assert output_path.exists(), "Report file should be created"

    def test_generate_baseline_report_all_profile_types(self) -> None:
        """Test that all profile types can generate reports."""
        profile_types = ["all", "homology", "persistence", "khovanov"]

        for profile_type in profile_types:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / f"{profile_type}_report.md"

                exit_code = generate_baseline_report(
                    str(output_path), profile_type=profile_type
                )

                assert output_path.exists(), f"Should create report for {profile_type}"
                assert isinstance(exit_code, int), f"Should return exit code for {profile_type}"


class TestMainCLI:
    """Test main() CLI function."""

    def test_main_with_default_args(self, monkeypatch: Any) -> None:
        """Test main() with default arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"
            monkeypatch.setattr(
                sys,
                "argv",
                [
                    "benchmark_runner.py",
                    "--output",
                    str(output_path),
                ],
            )

            exit_code = main()

            assert exit_code == 0, "Should return 0 on success"
            assert output_path.exists(), "Report should be created"

    def test_main_with_profile_arg(self, monkeypatch: Any) -> None:
        """Test main() with --profile argument."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"
            monkeypatch.setattr(
                sys,
                "argv",
                [
                    "benchmark_runner.py",
                    "--profile",
                    "homology",
                    "--output",
                    str(output_path),
                ],
            )

            exit_code = main()

            assert exit_code == 0, "Should return 0 on success"
            assert output_path.exists(), "Report should be created"

    def test_main_help_message(self, monkeypatch: Any, capsys: Any) -> None:
        """Test that --help displays usage information."""
        monkeypatch.setattr(sys, "argv", ["benchmark_runner.py", "--help"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        # argparse exits with 0 for --help
        assert exc_info.value.code == 0

    def test_main_invalid_profile_type(self, monkeypatch: Any) -> None:
        """Test main() with invalid --profile argument."""
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "benchmark_runner.py",
                "--profile",
                "invalid",
            ],
        )

        with pytest.raises(SystemExit) as exc_info:
            main()

        # argparse exits with 2 for invalid argument
        assert exc_info.value.code == 2

    def test_main_creates_report_with_all_profile_types(self, monkeypatch: Any) -> None:
        """Test main() creates reports for each profile type."""
        profile_types = ["all", "homology", "persistence", "khovanov"]

        for profile_type in profile_types:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "report.md"
                monkeypatch.setattr(
                    sys,
                    "argv",
                    [
                        "benchmark_runner.py",
                        "--profile",
                        profile_type,
                        "--output",
                        str(output_path),
                    ],
                )

                exit_code = main()

                assert exit_code == 0, f"Should return 0 for {profile_type}"
                assert output_path.exists(), f"Should create report for {profile_type}"
