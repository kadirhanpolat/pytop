"""Pytest configuration and fixtures for profiling tests.

Phase 17 P17.1: Fixtures for auto-profiling functions in benchmarks.
"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from pytop._internal.profiling_fixtures import ProfileCollector, create_profile_benchmark


@pytest.fixture
def profile_collector() -> ProfileCollector:
    """Create a fresh ProfileCollector for test.

    Returns a new ProfileCollector instance. Automatically cleared
    between tests via fixture scope.

    Yields:
        ProfileCollector instance
    """
    return ProfileCollector()


@pytest.fixture
def profile_benchmark(
    profile_collector: ProfileCollector,
) -> Any:
    """Create a @profile_benchmark decorator bound to this test's ProfileCollector.

    The decorator automatically collects stats from each decorated function call.

    Args:
        profile_collector: ProfileCollector fixture from same test

    Returns:
        Decorator factory accepting (track_memory=False)

    Example:
        >>> def test_my_func(profile_benchmark):
        ...     @profile_benchmark(track_memory=False)
        ...     def my_func(x):
        ...         return x * 2
        ...     result, stats = my_func(10)
        ...     assert result == 20
    """
    return create_profile_benchmark(profile_collector)


@pytest.fixture(scope="session", autouse=True)
def setup_profiling_output_dir() -> Generator[None, None, None]:
    """Create a temporary output directory for profiling results.

    Session-scoped fixture that automatically runs at test session start.
    Creates a temporary directory that can be used by profiling tests
    to write reports and profile dumps.

    Yields:
        Temporary directory path (cleanup is automatic via tempfile)
    """
    with tempfile.TemporaryDirectory(prefix="pytop_profiling_") as tmpdir:
        profile_output_dir = Path(tmpdir)
        # Directory is available for test use during session
        _ = profile_output_dir
        yield
