"""Test suite for profiling infrastructure (Phase 17 P17.1).

Tests for:
- ProfileStats dataclass
- @profile_call decorator
- context_profile context manager
"""

import pytest
from pytop._internal.profiling import ProfileStats, profile_call, context_profile


def fibonacci(n: int) -> int:
    """Simple fibonacci for testing profiling."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


class TestProfileStats:
    """Test ProfileStats dataclass."""

    def test_profile_stats_creation(self):
        """Test that ProfileStats dataclass can be created."""
        stats = ProfileStats(
            function_name="test_func",
            total_time=0.5,
            call_count=100,
            peak_memory_mb=10.5,
            top_5_callers=["caller1", "caller2"],
            raw_profile_data={"key": "value"},
        )
        assert stats.function_name == "test_func"
        assert stats.total_time == 0.5
        assert stats.call_count == 100
        assert stats.peak_memory_mb == 10.5
        assert stats.top_5_callers == ["caller1", "caller2"]
        assert stats.raw_profile_data == {"key": "value"}


class TestProfileCallDecorator:
    """Test @profile_call decorator."""

    def test_profile_call_basic(self):
        """Test basic @profile_call decorator functionality.

        Decorator should:
        - Execute the wrapped function
        - Return (result, ProfileStats) tuple
        - Have positive total_time
        - Have call_count > 0
        """
        @profile_call(track_memory=False, track_caller=False)
        def add(a: int, b: int) -> int:
            return a + b

        result, stats = add(5, 3)

        assert result == 8
        assert isinstance(stats, ProfileStats)
        assert stats.function_name == "add"
        assert stats.total_time > 0
        assert stats.call_count > 0

    def test_profile_call_with_fibonacci(self):
        """Test @profile_call with fibonacci(10)."""
        @profile_call(track_memory=False, track_caller=False)
        def fib_profiled(n: int) -> int:
            return fibonacci(n)

        result, stats = fib_profiled(10)

        assert result == 55
        assert isinstance(stats, ProfileStats)
        assert stats.total_time > 0
        assert stats.call_count > 1  # Multiple recursive calls

    def test_profile_call_memory_tracking(self):
        """Test @profile_call with memory tracking enabled.

        When track_memory=True, stats.peak_memory_mb should be > 0.
        """
        @profile_call(track_memory=True, track_caller=False)
        def allocate_memory() -> list:
            # Allocate ~1 MB of memory
            return [i for i in range(100000)]

        result, stats = allocate_memory()

        assert isinstance(result, list)
        assert len(result) == 100000
        assert isinstance(stats, ProfileStats)
        assert stats.peak_memory_mb > 0

    def test_profile_call_memory_tracking_disabled(self):
        """Test @profile_call with memory tracking disabled.

        When track_memory=False, stats.peak_memory_mb should be 0.
        """
        @profile_call(track_memory=False, track_caller=False)
        def allocate_memory() -> list:
            return [i for i in range(100000)]

        result, stats = allocate_memory()

        assert isinstance(result, list)
        assert stats.peak_memory_mb == 0

    def test_profile_call_with_exception(self):
        """Test @profile_call preserves exceptions."""
        @profile_call(track_memory=False, track_caller=False)
        def raise_error() -> None:
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            raise_error()

    def test_profile_call_with_args_kwargs(self):
        """Test @profile_call preserves function arguments."""
        @profile_call(track_memory=False, track_caller=False)
        def func(a: int, b: int, c: int = 0) -> int:
            return a + b + c

        result, stats = func(1, 2, c=3)
        assert result == 6
        assert stats.call_count > 0

    def test_profile_call_enable_by_default_true(self):
        """Test @profile_call with enable_by_default=True."""
        @profile_call(enable_by_default=True)
        def simple_func() -> str:
            return "hello"

        result, stats = simple_func()
        assert result == "hello"
        assert stats.total_time >= 0

    def test_profile_call_enable_by_default_false(self):
        """Test @profile_call with enable_by_default=False.

        When profiling is disabled, the function should still execute
        correctly but return ProfileStats with all zeros/empty.
        """
        @profile_call(enable_by_default=False)
        def simple_func(x: int) -> int:
            return x * 2

        result, stats = simple_func(5)
        assert result == 10
        assert stats.total_time == 0.0
        assert stats.call_count == 0
        assert stats.peak_memory_mb == 0.0
        assert stats.top_5_callers == []
        assert stats.raw_profile_data == {}

    def test_profile_call_multiple_invocations(self):
        """Test calling a decorated function multiple times."""
        @profile_call(track_memory=False, track_caller=False)
        def increment(x: int) -> int:
            return x + 1

        result1, stats1 = increment(1)
        result2, stats2 = increment(2)

        assert result1 == 2
        assert result2 == 3
        assert isinstance(stats1, ProfileStats)
        assert isinstance(stats2, ProfileStats)


class TestContextProfile:
    """Test context_profile context manager."""

    def test_context_profile_basic(self):
        """Test basic context_profile context manager.

        Should:
        - Execute code in context
        - Collect ProfileStats
        - Have positive total_time
        - Have call_count > 0
        """
        with context_profile("test_block", track_memory=False) as prof:
            fibonacci(10)

        assert prof.stats is not None
        assert isinstance(prof.stats, ProfileStats)
        assert prof.stats.total_time > 0
        assert prof.stats.call_count > 0

    def test_context_profile_memory_tracking(self):
        """Test context_profile with memory tracking."""
        with context_profile("memory_block", track_memory=True) as prof:
            data = [i for i in range(100000)]
            assert len(data) == 100000

        assert prof.stats is not None
        assert prof.stats.peak_memory_mb > 0

    def test_context_profile_memory_tracking_disabled(self):
        """Test context_profile with memory tracking disabled."""
        with context_profile("no_memory_block", track_memory=False) as prof:
            data = [i for i in range(100000)]
            assert len(data) == 100000

        assert prof.stats is not None
        assert prof.stats.peak_memory_mb == 0

    def test_context_profile_with_exception(self):
        """Test context_profile propagates exceptions."""
        with pytest.raises(ValueError, match="Test error"):
            with context_profile("error_block", track_memory=False) as prof:
                raise ValueError("Test error")

    def test_context_profile_name(self):
        """Test context_profile stores function name."""
        with context_profile("my_operation", track_memory=False) as prof:
            pass

        assert prof.stats.function_name == "my_operation"

    def test_context_profile_sequential(self):
        """Test sequential (non-nested) context_profile calls."""
        with context_profile("first", track_memory=False) as prof1:
            fibonacci(5)

        with context_profile("second", track_memory=False) as prof2:
            fibonacci(5)

        assert prof1.stats is not None
        assert prof2.stats is not None
        assert prof1.stats.function_name == "first"
        assert prof2.stats.function_name == "second"
