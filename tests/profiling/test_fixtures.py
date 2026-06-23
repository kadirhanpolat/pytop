"""Tests for pytest profiling fixtures with stat collection.

Phase 17 P17.1: Fixture-based profiling decorator that auto-collects stats.
"""

# mypy: ignore-errors

from __future__ import annotations

import pytest

from pytop._internal.profiling import ProfileStats
from pytop._internal.profiling_fixtures import ProfileCollector, create_profile_benchmark


class TestProfileCollector:
    """Tests for ProfileCollector immutable collection class."""

    def test_profile_collector_initialization(self) -> None:
        """ProfileCollector initializes as empty."""
        collector = ProfileCollector()
        assert collector.collected_stats() == []

    def test_profile_collector_record_single_stat(self) -> None:
        """ProfileCollector.record() stores a stat and retrieved via collected_stats()."""
        collector = ProfileCollector()
        stat = ProfileStats(
            function_name="test_func",
            total_time=0.1,
            call_count=1,
            peak_memory_mb=5.0,
            top_5_callers=["caller1"],
            raw_profile_data={},
        )
        collector.record(stat)
        assert len(collector.collected_stats()) == 1
        assert collector.collected_stats()[0] == stat

    def test_profile_collector_record_multiple_stats(self) -> None:
        """ProfileCollector stores multiple stats in order."""
        collector = ProfileCollector()
        stats = [
            ProfileStats(
                function_name=f"func_{i}",
                total_time=float(i) * 0.1,
                call_count=i,
                peak_memory_mb=float(i),
                top_5_callers=[],
                raw_profile_data={},
            )
            for i in range(3)
        ]
        for stat in stats:
            collector.record(stat)

        collected = collector.collected_stats()
        assert len(collected) == 3
        assert all(collected[i] == stats[i] for i in range(3))

    def test_profile_collector_clear(self) -> None:
        """ProfileCollector.clear() resets all collected stats."""
        collector = ProfileCollector()
        stat = ProfileStats(
            function_name="test",
            total_time=0.1,
            call_count=1,
            peak_memory_mb=5.0,
            top_5_callers=[],
            raw_profile_data={},
        )
        collector.record(stat)
        assert len(collector.collected_stats()) == 1

        collector.clear()
        assert collector.collected_stats() == []

    def test_profile_collector_collected_stats_returns_list(self) -> None:
        """ProfileCollector.collected_stats() returns a list."""
        collector = ProfileCollector()
        result = collector.collected_stats()
        assert isinstance(result, list)


class TestCreateProfileBenchmark:
    """Tests for create_profile_benchmark decorator factory."""

    def test_profile_benchmark_decorator_wraps_function(self) -> None:
        """@profile_benchmark wraps function and preserves behavior."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def simple_func(x: int) -> int:
            return x * 2

        result, stats = simple_func(5)
        assert result == 10
        assert isinstance(stats, ProfileStats)
        assert stats.function_name == "simple_func"

    def test_profile_benchmark_auto_collects_stats(self) -> None:
        """@profile_benchmark auto-records stats in collector."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def test_func(x: int) -> int:
            return x + 1

        # Before call, collector is empty
        assert len(collector.collected_stats()) == 0

        # After call, stat is recorded
        result, stats = test_func(10)
        assert len(collector.collected_stats()) == 1
        assert collector.collected_stats()[0] == stats

    def test_profile_benchmark_multiple_calls_accumulate(self) -> None:
        """Multiple @profile_benchmark calls accumulate stats in collector."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def func1(x: int) -> int:
            return x

        @benchmark(track_memory=False)
        def func2(x: int) -> int:
            return x * 2

        # Call both functions multiple times
        func1(1)
        func1(2)
        func2(3)

        # All 3 calls should be collected
        stats_list = collector.collected_stats()
        assert len(stats_list) == 3
        # First two should be func1, third should be func2
        assert stats_list[0].function_name == "func1"
        assert stats_list[1].function_name == "func1"
        assert stats_list[2].function_name == "func2"

    def test_profile_benchmark_returns_tuple(self) -> None:
        """@profile_benchmark returns (result, ProfileStats) tuple."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def test_func() -> str:
            return "hello"

        result = test_func()
        assert isinstance(result, tuple)
        assert len(result) == 2
        value, stats = result
        assert value == "hello"
        assert isinstance(stats, ProfileStats)

    def test_profile_benchmark_preserves_function_name(self) -> None:
        """@profile_benchmark preserves wrapped function name."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def my_special_function() -> None:
            pass

        my_special_function()
        stats = collector.collected_stats()[0]
        assert stats.function_name == "my_special_function"

    def test_profile_benchmark_with_memory_tracking(self) -> None:
        """@profile_benchmark(track_memory=True) collects memory stats."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=True)
        def memory_func() -> list[int]:
            return list(range(10000))

        result, stats = memory_func()
        assert len(result) == 10000
        assert stats.peak_memory_mb >= 0.0

    def test_profile_benchmark_exception_propagates(self) -> None:
        """@profile_benchmark propagates exceptions from wrapped function."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def failing_func() -> None:
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            failing_func()

    def test_profile_benchmark_with_multiple_arguments(self) -> None:
        """@profile_benchmark handles functions with multiple arguments."""
        collector = ProfileCollector()
        benchmark = create_profile_benchmark(collector)

        @benchmark(track_memory=False)
        def multi_arg_func(a: int, b: str, c: float = 1.0) -> str:
            return f"{a}:{b}:{c}"

        result, stats = multi_arg_func(1, "test", c=2.5)
        assert result == "1:test:2.5"
        assert len(collector.collected_stats()) == 1

    def test_profile_benchmark_collection_isolation(self) -> None:
        """Different ProfileCollectors maintain separate collections."""
        collector1 = ProfileCollector()
        collector2 = ProfileCollector()

        bench1 = create_profile_benchmark(collector1)
        bench2 = create_profile_benchmark(collector2)

        @bench1(track_memory=False)
        def func1() -> int:
            return 1

        @bench2(track_memory=False)
        def func2() -> int:
            return 2

        func1()
        func1()
        func2()

        assert len(collector1.collected_stats()) == 2
        assert len(collector2.collected_stats()) == 1
