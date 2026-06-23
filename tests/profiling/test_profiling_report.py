"""Test suite for profiling report generation (Phase 17 P17.1).

Tests for:
- ProfileReport dataclass
- generate_markdown_report function
- generate_json_report function
"""

import json
from datetime import datetime

import pytest

from pytop._internal.profiling import ProfileStats
from pytop._internal.profiling_report import (
    ProfileReport,
    generate_json_report,
    generate_markdown_report,
)


class TestProfileReport:
    """Test ProfileReport dataclass."""

    def test_profile_report_creation(self):
        """Test that ProfileReport dataclass can be created."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=["caller1", "caller2"],
            raw_profile_data={"key": "value"},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=2.5,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=["caller3"],
            raw_profile_data={"key2": "value2"},
        )

        report = ProfileReport(
            name="test_report",
            stats_list=[stats1, stats2],
        )

        assert report.name == "test_report"
        assert len(report.stats_list) == 2
        assert report.stats_list[0].function_name == "func1"
        assert report.stats_list[1].function_name == "func2"

    def test_profile_report_immutable(self):
        """Test that ProfileReport is frozen (immutable)."""
        stats = ProfileStats(
            function_name="func",
            total_time=1.0,
            call_count=10,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        report = ProfileReport(name="test", stats_list=[stats])

        with pytest.raises(AttributeError):
            report.name = "modified"

    def test_profile_report_timestamp_generation(self):
        """Test that ProfileReport auto-generates timestamp."""
        stats = ProfileStats(
            function_name="func",
            total_time=1.0,
            call_count=10,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        report = ProfileReport(name="test", stats_list=[stats])

        # Timestamp should be set and be ISO format
        assert report.timestamp is not None
        assert isinstance(report.timestamp, str)
        # Should be parseable as ISO format
        datetime.fromisoformat(report.timestamp)

    def test_profile_report_total_runtime(self):
        """Test that total_runtime property sums all stats times."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=2.5,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats1, stats2])
        assert report.total_runtime == 4.0

    def test_profile_report_total_runtime_empty(self):
        """Test that total_runtime with empty stats_list is 0."""
        report = ProfileReport(name="test", stats_list=[])
        assert report.total_runtime == 0.0

    def test_profile_report_peak_memory_mb(self):
        """Test that peak_memory_mb property returns max of all peaks."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=2.5,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats3 = ProfileStats(
            function_name="func3",
            total_time=0.5,
            call_count=5,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats1, stats2, stats3])
        assert report.peak_memory_mb == 20.0

    def test_profile_report_peak_memory_mb_empty(self):
        """Test that peak_memory_mb with empty stats_list is 0."""
        report = ProfileReport(name="test", stats_list=[])
        assert report.peak_memory_mb == 0.0

    def test_profile_report_bottleneck_functions(self):
        """Test that bottleneck_functions returns top N sorted by time."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=5.0,
            call_count=100,
            peak_memory_mb=10.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=3.0,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats3 = ProfileStats(
            function_name="func3",
            total_time=1.0,
            call_count=5,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats1, stats2, stats3])
        bottlenecks = report.bottleneck_functions(top_n=2)

        assert len(bottlenecks) == 2
        # Should be sorted by total_time descending
        assert bottlenecks[0][0] == "func1"
        assert bottlenecks[0][1] == 5.0
        assert bottlenecks[0][2] == 10.0
        assert bottlenecks[1][0] == "func2"
        assert bottlenecks[1][1] == 3.0
        assert bottlenecks[1][2] == 20.0

    def test_profile_report_bottleneck_functions_all(self):
        """Test that bottleneck_functions(top_n=5) returns all if fewer than 5."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=2.0,
            call_count=100,
            peak_memory_mb=10.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=1.0,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats1, stats2])
        bottlenecks = report.bottleneck_functions(top_n=5)

        assert len(bottlenecks) == 2


class TestGenerateMarkdownReport:
    """Test markdown report generation."""

    def test_generate_markdown_report_structure(self):
        """Test that markdown report contains expected structure."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=2.5,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test_report", stats_list=[stats1, stats2])
        markdown = generate_markdown_report(report)

        # Check for expected sections
        assert "# Profile Report: test_report" in markdown
        assert "Generated:" in markdown
        assert "Total Runtime:" in markdown
        assert "Peak Memory:" in markdown
        assert "## Function Breakdown" in markdown
        assert "func1" in markdown
        assert "func2" in markdown

    def test_generate_markdown_report_table_format(self):
        """Test that markdown report contains table with proper format."""
        stats = ProfileStats(
            function_name="test_func",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats])
        markdown = generate_markdown_report(report)

        # Check for table headers
        assert "| Name |" in markdown
        assert "| Time (s) |" in markdown
        assert "| Calls |" in markdown
        assert "| Memory (MB) |" in markdown

    def test_generate_markdown_report_bottleneck_section(self):
        """Test that markdown report contains bottleneck functions section."""
        stats1 = ProfileStats(
            function_name="slow_func",
            total_time=10.0,
            call_count=100,
            peak_memory_mb=50.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="fast_func",
            total_time=0.5,
            call_count=10,
            peak_memory_mb=1.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats1, stats2])
        markdown = generate_markdown_report(report)

        assert "## Top Bottlenecks" in markdown
        assert "slow_func" in markdown

    def test_generate_markdown_report_returns_string(self):
        """Test that markdown report returns a string."""
        stats = ProfileStats(
            function_name="func",
            total_time=1.0,
            call_count=10,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats])
        markdown = generate_markdown_report(report)

        assert isinstance(markdown, str)
        assert len(markdown) > 0

    def test_generate_markdown_report_empty_stats(self):
        """Test that markdown report handles empty stats list."""
        report = ProfileReport(name="empty_report", stats_list=[])
        markdown = generate_markdown_report(report)

        assert "# Profile Report: empty_report" in markdown
        assert isinstance(markdown, str)


class TestGenerateJsonReport:
    """Test JSON report generation."""

    def test_generate_json_report_structure(self):
        """Test that JSON report contains expected fields."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=2.5,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test_report", stats_list=[stats1, stats2])
        json_str = generate_json_report(report)

        # Parse JSON
        data = json.loads(json_str)

        assert data["name"] == "test_report"
        assert data["timestamp"] is not None
        assert data["total_runtime"] == 4.0
        assert data["peak_memory_mb"] == 20.0
        assert data["function_count"] == 2

    def test_generate_json_report_stats_array(self):
        """Test that JSON report contains stats array."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats1])
        json_str = generate_json_report(report)

        data = json.loads(json_str)

        assert "stats" in data
        assert isinstance(data["stats"], list)
        assert len(data["stats"]) == 1
        assert data["stats"][0]["function_name"] == "func1"
        assert data["stats"][0]["total_time"] == 1.5

    def test_generate_json_report_returns_string(self):
        """Test that JSON report returns a string."""
        stats = ProfileStats(
            function_name="func",
            total_time=1.0,
            call_count=10,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats])
        json_str = generate_json_report(report)

        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_generate_json_report_valid_json(self):
        """Test that JSON report is valid JSON."""
        stats = ProfileStats(
            function_name="func",
            total_time=1.0,
            call_count=10,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats])
        json_str = generate_json_report(report)

        # Should not raise
        data = json.loads(json_str)
        assert data is not None

    def test_generate_json_report_empty_stats(self):
        """Test that JSON report handles empty stats list."""
        report = ProfileReport(name="empty_report", stats_list=[])
        json_str = generate_json_report(report)

        data = json.loads(json_str)

        assert data["name"] == "empty_report"
        assert data["function_count"] == 0
        assert data["stats"] == []

    def test_generate_json_report_formatting(self):
        """Test that JSON report is properly indented."""
        stats = ProfileStats(
            function_name="func",
            total_time=1.0,
            call_count=10,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test", stats_list=[stats])
        json_str = generate_json_report(report)

        # Should have newlines (indicates indent=2)
        assert "\n" in json_str


class TestIntegrationReportGeneration:
    """Integration tests for report generation."""

    def test_markdown_and_json_consistency(self):
        """Test that markdown and JSON reports contain consistent data."""
        stats1 = ProfileStats(
            function_name="func1",
            total_time=1.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=[],
            raw_profile_data={},
        )
        stats2 = ProfileStats(
            function_name="func2",
            total_time=2.5,
            call_count=50,
            peak_memory_mb=20.0,
            top_5_callers=[],
            raw_profile_data={},
        )

        report = ProfileReport(name="test_report", stats_list=[stats1, stats2])

        markdown = generate_markdown_report(report)
        json_str = generate_json_report(report)
        json_data = json.loads(json_str)

        # Both should mention the same functions
        assert "func1" in markdown
        assert "func2" in markdown
        assert json_data["function_count"] == 2

        # Total runtime should match
        assert "4.0" in markdown or "4" in markdown
        assert json_data["total_runtime"] == 4.0

    def test_report_generation_with_profile_call_integration(self, tmp_path):
        """Test report generation with real ProfileStats from @profile_call."""
        from pytop._internal.profiling import profile_call

        @profile_call(track_memory=False, track_caller=False)
        def sample_function(n: int) -> int:
            return sum(range(n))

        result, stats = sample_function(1000)

        report = ProfileReport(name="integration_test", stats_list=[stats])

        markdown = generate_markdown_report(report)
        json_str = generate_json_report(report)

        assert isinstance(markdown, str)
        assert len(markdown) > 0
        assert isinstance(json_str, str)

        # Should be valid JSON
        json_data = json.loads(json_str)
        assert json_data["name"] == "integration_test"
