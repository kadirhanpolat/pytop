"""Integration tests for benchmark_runner CLI (Phase 17 P17.1).

End-to-end tests verifying:
- CLI tool can be invoked via subprocess
- Report generation produces valid output structure
- Different profile types generate expected reports
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


class TestBenchmarkRunnerIntegration:
    """Integration tests for benchmark_runner as subprocess."""

    def test_cli_tool_invocation(self) -> None:
        """Test that CLI tool can be invoked as subprocess."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            # Run CLI tool as subprocess
            result = subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "all",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            # Should exit with 0
            assert result.returncode == 0, f"CLI should exit with 0. stderr: {result.stderr}"

            # Report should be created
            assert output_path.exists(), "Report file should be created"

    def test_cli_tool_with_homology_profile(self) -> None:
        """Test CLI tool with homology profile type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "homology_report.md"

            result = subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "homology",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, f"CLI should succeed. stderr: {result.stderr}"
            assert output_path.exists(), "Report should be created"

    def test_cli_tool_with_persistence_profile(self) -> None:
        """Test CLI tool with persistence profile type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "persistence_report.md"

            result = subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "persistence",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, f"CLI should succeed. stderr: {result.stderr}"
            assert output_path.exists(), "Report should be created"

    def test_cli_tool_with_khovanov_profile(self) -> None:
        """Test CLI tool with khovanov profile type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "khovanov_report.md"

            result = subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "khovanov",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0, f"CLI should succeed. stderr: {result.stderr}"
            assert output_path.exists(), "Report should be created"

    def test_cli_tool_default_output_path(self) -> None:
        """Test CLI tool creates report at default path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory to use default output path
            import os

            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create docs dir for default output
                docs_dir = Path(tmpdir) / "docs"
                docs_dir.mkdir()

                result = subprocess.run(
                    [
                        sys.executable,
                        str(Path(old_cwd) / "src/pytop/_internal/benchmark_runner.py"),
                        "--profile",
                        "all",
                    ],
                    capture_output=True,
                    text=True,
                )

                assert result.returncode == 0, f"CLI should succeed. stderr: {result.stderr}"

                # Check default output path
                default_output = docs_dir / "PERFORMANCE.md"
                assert default_output.exists(), "Report should be created at default path"

            finally:
                os.chdir(old_cwd)

    def test_cli_tool_help_option(self) -> None:
        """Test CLI tool --help option."""
        result = subprocess.run(
            [
                sys.executable,
                "src/pytop/_internal/benchmark_runner.py",
                "--help",
            ],
            capture_output=True,
            text=True,
        )

        # --help exits with 0
        assert result.returncode == 0, "Help should exit with 0"

        # Help text should contain usage information
        assert "usage:" in result.stdout, "Help should contain usage"
        assert "--profile" in result.stdout, "Help should document --profile"
        assert "--output" in result.stdout, "Help should document --output"

    def test_report_structure(self) -> None:
        """Test that generated report has expected structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "all",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
            )

            content = output_path.read_text()

            # Verify expected sections exist
            required_sections = [
                "# Profile Report:",
                "## Metadata",
                "## Function Breakdown",
                "## Top Bottlenecks",
                "## Benchmark Run Details",
                "Python Version:",
                "Generated:",
                "Total Runtime:",
            ]

            for section in required_sections:
                assert section in content, f"Report should contain '{section}' section"

            # Verify report includes pytest output
            assert "test session starts" in content, "Report should include pytest output"

    def test_report_file_not_empty(self) -> None:
        """Test that generated report is not empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "all",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
            )

            file_size = output_path.stat().st_size
            assert file_size > 1000, "Report should contain meaningful content (>1KB)"

    def test_multiple_runs_overwrite_report(self) -> None:
        """Test that multiple CLI runs overwrite the previous report."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            # First run
            subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "homology",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
            )

            first_mtime = output_path.stat().st_mtime

            # Second run with different profile
            import time

            time.sleep(0.1)  # Ensure mtime is different

            subprocess.run(
                [
                    sys.executable,
                    "src/pytop/_internal/benchmark_runner.py",
                    "--profile",
                    "khovanov",
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
            )

            second_size = output_path.stat().st_size
            second_mtime = output_path.stat().st_mtime

            # Second run should create a different report (might be different size)
            assert second_mtime > first_mtime, "Report should be updated on second run"

            # Report should still exist and have content
            assert output_path.exists(), "Report should still exist"
            assert second_size > 1000, "Report should have meaningful content"
