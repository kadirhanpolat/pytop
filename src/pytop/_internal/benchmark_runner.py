"""CLI tool to run benchmarks and generate baseline performance report.

Phase 17 P17.1: Profiling-driven benchmark runner.

Provides:
- main(): CLI entry point with argparse
- run_benchmarks(): Execute pytest benchmarks and collect output
- generate_baseline_report(): Run benchmarks and write Markdown report
"""

import argparse
import subprocess
import sys
from pathlib import Path

from pytop._internal.profiling import ProfileStats
from pytop._internal.profiling_report import ProfileReport, generate_markdown_report


def run_benchmarks(profile_type: str) -> tuple[str, int]:
    """Run pytest benchmarks and return the output and exit code.

    Executes pytest with benchmark markers for the specified profile type.
    Returns the raw pytest stdout output and the exit code (allowing for failures).

    Args:
        profile_type: Type of benchmarks to run.
            Options: "all", "homology", "persistence", "khovanov"

    Returns:
        Tuple of (pytest_output, exit_code). Exit code 0 means all tests passed.

    Raises:
        ValueError: If profile_type is invalid
    """
    # Map profile_type to pytest marker names
    marker_map = {
        "all": "benchmark",
        "homology": "benchmark_homology",
        "persistence": "benchmark_persistence",
        "khovanov": "benchmark_khovanov",
    }

    if profile_type not in marker_map:
        raise ValueError(
            f"Invalid profile_type: {profile_type}. "
            f"Valid options: {', '.join(marker_map.keys())}"
        )

    marker = marker_map[profile_type]

    # Construct pytest command
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/profiling/",
        "-v",
        f"-m {marker}",
        "--tb=short",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    # Return output and exit code (don't raise on failure)
    return result.stdout, result.returncode


def generate_baseline_report(
    output_path: str,
    profile_type: str = "all",
) -> int:
    """Run benchmarks and write baseline performance report.

    Executes benchmarks for the specified profile type, collects ProfileStats,
    and writes a Markdown report to the output file.

    Args:
        output_path: File path where the report should be written
        profile_type: Type of benchmarks to run (default "all")

    Returns:
        Exit code from pytest (0 if all benchmarks passed, non-zero otherwise)

    Raises:
        IOError: If output file cannot be written
    """
    # Run benchmarks
    print(f"Running {profile_type} benchmarks...", file=sys.stderr)
    pytest_output, exit_code = run_benchmarks(profile_type)

    # Parse pytest output and create ProfileStats entries
    # For baseline report, we'll create a simple report with metadata
    stats_list: list[ProfileStats] = []

    # TODO: Parse pytest output to extract actual performance data
    # For now, create a minimal report structure

    # Create ProfileReport
    report = ProfileReport(
        name=f"pytop Baseline Performance (Phase 17 P17.1 - {profile_type})",
        stats_list=stats_list,
        python_version=f"Python {sys.version.split()[0]}",
    )

    # Generate Markdown report
    report_markdown = generate_markdown_report(report)

    # Add metadata and pytest output to the report
    status_note = (
        "\n**Status:** [PASS] All benchmarks passed"
        if exit_code == 0
        else "\n**Status:** [WARNING] Some benchmarks failed or errored"
    )

    full_report = f"""{report_markdown}

## Benchmark Run Details

### Command
```
python -m pytest tests/profiling/ -v -m benchmark
```

### Status
{status_note}

### Raw Output
```
{pytest_output}
```
"""

    # Write to output file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(full_report)

    print(f"Baseline report written to {output_path}", file=sys.stderr)
    return exit_code


def main() -> int:
    """CLI entry point for benchmark runner.

    Parses command-line arguments and executes benchmark generation.

    Returns:
        Exit code (0 on success, 1 on error)
    """
    parser = argparse.ArgumentParser(
        description="Run pytop benchmarks and generate baseline performance report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m pytop._internal.benchmark_runner --profile all --output docs/PERFORMANCE.md
  python -m pytop._internal.benchmark_runner --profile homology
  python -m pytop._internal.benchmark_runner --help
        """.strip(),
    )

    parser.add_argument(
        "--profile",
        choices=["all", "homology", "persistence", "khovanov"],
        default="all",
        help="Type of benchmarks to run (default: all)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="docs/PERFORMANCE.md",
        help="Output file path for the report (default: docs/PERFORMANCE.md)",
    )

    args = parser.parse_args()

    try:
        generate_baseline_report(
            output_path=args.output,
            profile_type=args.profile,
        )
        # Return 0 if report generation succeeded (even if benchmarks had failures)
        return 0
    except OSError as e:
        print(f"Error writing report: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Invalid argument: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
