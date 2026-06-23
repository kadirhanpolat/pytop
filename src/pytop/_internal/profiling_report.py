"""Profiling report generation module (Phase 17 P17.1).

Converts ProfileStats collections into human-readable Markdown and machine-readable
JSON reports for analysis and documentation.

Provides:
- ProfileReport: immutable dataclass for aggregated profiling results
- generate_markdown_report(): produces formatted Markdown report
- generate_json_report(): produces JSON report
"""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pytop._internal.profiling import ProfileStats


@dataclass(frozen=True)
class ProfileReport:
    """Immutable profiling report container.

    Aggregates multiple ProfileStats objects into a single report with
    computed totals and bottleneck analysis.

    Attributes:
        name: Name/title of the report
        stats_list: List of ProfileStats objects to aggregate
        timestamp: ISO format timestamp (auto-generated)
        python_version: Optional Python version info
    """

    name: str
    stats_list: list[ProfileStats]
    timestamp: str = ""
    python_version: str | None = None

    def __post_init__(self) -> None:
        """Initialize default timestamp if not provided."""
        # dataclass(frozen=True) prevents normal __init__ modification,
        # so we use object.__setattr__ to set the timestamp
        if not self.timestamp:
            object.__setattr__(self, "timestamp", datetime.now().isoformat())

    @property
    def total_runtime(self) -> float:
        """Total runtime across all stats.

        Returns:
            Sum of all total_time values in stats_list
        """
        return sum(stat.total_time for stat in self.stats_list)

    @property
    def peak_memory_mb(self) -> float:
        """Maximum peak memory usage across all stats.

        Returns:
            Maximum peak_memory_mb value in stats_list, or 0.0 if empty
        """
        if not self.stats_list:
            return 0.0
        return max(stat.peak_memory_mb for stat in self.stats_list)

    def bottleneck_functions(
        self, top_n: int = 5
    ) -> list[tuple[str, float, float]]:
        """Return top N bottleneck functions sorted by total time.

        Args:
            top_n: Number of top functions to return (default 5)

        Returns:
            List of (function_name, total_time, peak_memory_mb) tuples
            sorted by total_time descending
        """
        # Create tuples of (name, time, memory)
        bottlenecks = [
            (stat.function_name, stat.total_time, stat.peak_memory_mb)
            for stat in self.stats_list
        ]

        # Sort by total_time descending
        sorted_bottlenecks = sorted(bottlenecks, key=lambda x: x[1], reverse=True)

        # Return top_n
        return sorted_bottlenecks[:top_n]


def generate_markdown_report(report: ProfileReport) -> str:
    """Generate a formatted Markdown report from ProfileReport.

    Args:
        report: ProfileReport object to convert

    Returns:
        Formatted Markdown string with report structure
    """
    lines: list[str] = []

    # Title
    lines.append(f"# Profile Report: {report.name}")
    lines.append("")

    # Metadata section
    lines.append("## Metadata")
    lines.append(f"- **Generated:** {report.timestamp}")
    lines.append(f"- **Total Runtime:** {report.total_runtime:.4f} seconds")
    lines.append(f"- **Peak Memory:** {report.peak_memory_mb:.2f} MB")
    if report.python_version:
        lines.append(f"- **Python Version:** {report.python_version}")
    lines.append("")

    # Function breakdown table
    lines.append("## Function Breakdown")
    lines.append("")
    lines.append("| Name | Time (s) | Calls | Memory (MB) |")
    lines.append("|------|----------|-------|------------|")

    for stat in report.stats_list:
        lines.append(
            f"| {stat.function_name} | {stat.total_time:.4f} | "
            f"{stat.call_count} | {stat.peak_memory_mb:.2f} |"
        )

    lines.append("")

    # Top bottlenecks section
    lines.append("## Top Bottlenecks")
    lines.append("")

    bottlenecks = report.bottleneck_functions(top_n=5)
    if bottlenecks:
        for i, (name, time, memory) in enumerate(bottlenecks, 1):
            lines.append(f"{i}. **{name}** — {time:.4f}s ({memory:.2f} MB)")
    else:
        lines.append("(No functions to report)")

    lines.append("")

    return "\n".join(lines)


def generate_json_report(report: ProfileReport) -> str:
    """Generate a JSON report from ProfileReport.

    Args:
        report: ProfileReport object to convert

    Returns:
        JSON formatted string with report data
    """
    # Build stats array
    stats_array: list[dict[str, Any]] = []
    for stat in report.stats_list:
        stats_array.append(
            {
                "function_name": stat.function_name,
                "total_time": stat.total_time,
                "call_count": stat.call_count,
                "peak_memory_mb": stat.peak_memory_mb,
                "top_5_callers": stat.top_5_callers,
            }
        )

    # Build report object
    report_data: dict[str, Any] = {
        "name": report.name,
        "timestamp": report.timestamp,
        "total_runtime": report.total_runtime,
        "peak_memory_mb": report.peak_memory_mb,
        "function_count": len(report.stats_list),
        "stats": stats_array,
    }

    if report.python_version:
        report_data["python_version"] = report.python_version

    return json.dumps(report_data, indent=2)
