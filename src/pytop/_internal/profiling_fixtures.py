"""Pytest fixtures for auto-profiling functions in benchmarks.

Phase 17 P17.1: Immutable ProfileCollector and decorator factory for test-based
profiling with automatic stat collection across test runs.

Provides:
- ProfileCollector: Immutable collection for ProfileStats across test runs
- create_profile_benchmark: Decorator factory that auto-collects stats
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from pytop._internal.profiling import ProfileStats, _ProfileContext

T = TypeVar("T")


class ProfileCollector:
    """Immutable-style collector for ProfileStats across test runs.

    Maintains an ordered list of ProfileStats from decorated function calls.
    Thread-safe via internal list operations.

    Attributes:
        _stats: Ordered list of collected ProfileStats
    """

    def __init__(self) -> None:
        """Initialize empty ProfileCollector."""
        self._stats: list[ProfileStats] = []

    def record(self, stat: ProfileStats) -> None:
        """Record a ProfileStats measurement.

        Args:
            stat: ProfileStats instance to store
        """
        self._stats.append(stat)

    def collected_stats(self) -> list[ProfileStats]:
        """Retrieve all collected ProfileStats.

        Returns:
            List of ProfileStats in collection order
        """
        return list(self._stats)

    def clear(self) -> None:
        """Clear all collected ProfileStats.

        Used for test isolation between test runs.
        """
        self._stats.clear()


def create_profile_benchmark(
    collector: ProfileCollector,
) -> Callable[
    [bool],
    Callable[[Callable[..., T]], Callable[..., tuple[T, ProfileStats]]],
]:
    """Create a @profile_benchmark decorator factory for a given ProfileCollector.

    This decorator wraps functions with profiling instrumentation, collecting
    cProfile and optional memory stats, then auto-recording in the collector.

    Args:
        collector: ProfileCollector instance to accumulate stats

    Returns:
        Decorator factory that accepts (track_memory=False) and returns
        a decorator for functions returning (result, ProfileStats)

    Example:
        >>> collector = ProfileCollector()
        >>> benchmark = create_profile_benchmark(collector)
        >>> @benchmark(track_memory=False)
        ... def expensive_func(n):
        ...     return sum(range(n))
        ... result, stats = expensive_func(1000)
        >>> print(len(collector.collected_stats()), stats.total_time)
    """

    def profile_benchmark(
        track_memory: bool = False,
    ) -> Callable[[Callable[..., T]], Callable[..., tuple[T, ProfileStats]]]:
        """Decorator that profiles a function and auto-collects stats.

        Args:
            track_memory: Whether to track peak memory usage via tracemalloc

        Returns:
            Decorator function that wraps target function
        """

        def decorator(
            func: Callable[..., T],
        ) -> Callable[..., tuple[T, ProfileStats]]:
            """Apply profiling instrumentation to a function.

            Args:
                func: Function to be profiled

            Returns:
                Wrapped function that returns (result, ProfileStats) tuple
                and auto-records stats in collector
            """

            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> tuple[T, ProfileStats]:
                """Execute profiled function and return result with auto-collected stats.

                Collects cProfile statistics and optional memory tracking via
                _ProfileContext, then auto-records the stats in the collector
                before returning (result, ProfileStats).

                Args:
                    *args: Positional arguments to pass to wrapped function
                    **kwargs: Keyword arguments to pass to wrapped function

                Returns:
                    Tuple of (result, ProfileStats) where result is the wrapped
                    function's return value; stats are auto-recorded in collector
                """
                ctx: _ProfileContext[T] = _ProfileContext(
                    func.__name__, track_memory=track_memory
                )
                with ctx:
                    result = func(*args, **kwargs)

                if ctx.stats is None:
                    raise RuntimeError(
                        "ProfileStats was not initialized by context manager"
                    )

                # Auto-record stats in collector
                collector.record(ctx.stats)

                return (result, ctx.stats)

            return wrapper

        return decorator

    return profile_benchmark
