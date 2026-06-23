"""Core profiling infrastructure for pytop.

Phase 17 P17.1: Profiling decorator and context manager using stdlib cProfile
and tracemalloc.

Provides:
- ProfileStats: immutable dataclass for profile results
- @profile_call: decorator that wraps functions and returns (result, ProfileStats)
- context_profile: context manager for profiling code blocks
"""

import cProfile
import pstats
import tracemalloc
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from io import StringIO
from typing import Any, Callable, Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass(frozen=False)
class ProfileStats:
    """Immutable profile statistics container.

    Attributes:
        function_name: Name of the profiled function or code block
        total_time: Total wall-clock time in seconds
        call_count: Number of function calls
        peak_memory_mb: Peak memory usage in MB (0.0 if not tracked)
        top_5_callers: List of top 5 caller functions
        raw_profile_data: Raw pstats data dictionary
    """

    function_name: str
    total_time: float
    call_count: int
    peak_memory_mb: float
    top_5_callers: list[str]
    raw_profile_data: dict[str, Any]


class _ProfileContext(Generic[T]):
    """Context manager wrapper for profile collection."""

    def __init__(
        self,
        func_name: str,
        track_memory: bool = False,
    ) -> None:
        """Initialize profiling context.

        Args:
            func_name: Name of the profiled function/block
            track_memory: Whether to track memory usage
        """
        self.func_name = func_name
        self.track_memory = track_memory
        self.profiler: Optional[cProfile.Profile] = None
        self.stats: Optional[ProfileStats] = None
        self._memory_snapshot: Optional[tracemalloc.Snapshot] = None

    def __enter__(self) -> "_ProfileContext[T]":
        """Enter profiling context."""
        self.profiler = cProfile.Profile()
        self.profiler.enable()

        if self.track_memory:
            tracemalloc.start()

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit profiling context and collect statistics."""
        self.profiler.disable()

        if self.track_memory:
            self._memory_snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()

        # Collect profile statistics
        stream = StringIO()
        ps = pstats.Stats(self.profiler, stream=stream)
        ps.sort_stats("cumulative")

        # Extract stats from pstats
        total_time = 0.0
        call_count = 0
        top_5_callers: list[str] = []

        if ps.stats:
            # Calculate total time as sum of all call times
            for func_info, func_stats in ps.stats.items():
                if func_stats:
                    # func_stats = (primitive calls, calls, total time, cumulative time, callers)
                    call_count += func_stats[1]  # Total calls
                    total_time = max(total_time, func_stats[3])  # Use max cumulative time

            # Extract top 5 callers
            callers_list = []
            for func_info, func_stats in ps.stats.items():
                if func_stats and func_info:
                    callers_list.append(str(func_info))

            top_5_callers = sorted(callers_list)[:5]

        # Get peak memory
        peak_memory_mb = 0.0
        if self.track_memory and self._memory_snapshot:
            stats_list = self._memory_snapshot.statistics("lineno")
            if stats_list:
                peak_memory_mb = stats_list[0].size / (1024 * 1024)

        self.stats = ProfileStats(
            function_name=self.func_name,
            total_time=total_time,
            call_count=call_count,
            peak_memory_mb=peak_memory_mb,
            top_5_callers=top_5_callers,
            raw_profile_data=dict(ps.stats) if ps.stats else {},
        )


def profile_call(
    track_memory: bool = False,
    track_caller: bool = False,
    enable_by_default: bool = True,
) -> Callable[[Callable[..., T]], Callable[..., tuple[T, ProfileStats]]]:
    """Decorator for profiling function calls.

    Wraps a function to collect cProfile statistics and optional memory tracking.
    Returns (result, ProfileStats) tuple.

    Args:
        track_memory: Whether to track peak memory usage via tracemalloc
        track_caller: Whether to track caller information (currently unused)
        enable_by_default: Whether profiling is enabled by default

    Returns:
        Decorated function that returns (result, ProfileStats)

    Example:
        >>> @profile_call(track_memory=True)
        ... def expensive_function(n):
        ...     return sum(range(n))
        ...
        >>> result, stats = expensive_function(1000)
        >>> print(stats.total_time, stats.peak_memory_mb)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., tuple[T, ProfileStats]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> tuple[T, ProfileStats]:
            if not enable_by_default:
                # If profiling disabled, just call function
                result = func(*args, **kwargs)
                return (
                    result,
                    ProfileStats(
                        function_name=func.__name__,
                        total_time=0.0,
                        call_count=0,
                        peak_memory_mb=0.0,
                        top_5_callers=[],
                        raw_profile_data={},
                    ),
                )

            with _ProfileContext(func.__name__, track_memory=track_memory) as ctx:
                result = func(*args, **kwargs)

            assert ctx.stats is not None
            return (result, ctx.stats)

        return wrapper

    return decorator


@contextmanager
def context_profile(
    func_name: str,
    track_memory: bool = False,
) -> Any:
    """Context manager for profiling code blocks.

    Collects cProfile statistics and optional memory tracking for code
    executed within the context.

    Args:
        func_name: Name to associate with this profiling context
        track_memory: Whether to track peak memory usage via tracemalloc

    Yields:
        _ProfileContext with .stats attribute set after exit

    Example:
        >>> with context_profile("my_operation", track_memory=True) as prof:
        ...     result = expensive_operation()
        >>> print(prof.stats.total_time, prof.stats.peak_memory_mb)
    """
    ctx = _ProfileContext(func_name, track_memory=track_memory)
    with ctx:
        yield ctx
