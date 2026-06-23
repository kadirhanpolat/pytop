"""Phase 17 P17.2: Algorithm Optimization Benchmarks.

Compares performance of different reduction methods (standard, twist, cohomology)
on realistic datasets to measure optimization speedup from P17.1→P17.2.

Tests:
- Method comparison on varying dataset sizes
- Clearing Lemma effectiveness measurement
- Memory profiling across methods
"""

from __future__ import annotations

from typing import Any

import pytest

from pytop.metric_spaces import FiniteMetricSpace
from pytop.persistent_homology import (
    persistent_homology,
    vietoris_rips_filtration,
)
from pytop.persistent_homology_optimized import (
    ReductionStats,
    persistence_pairs_twist_with_stats,
)

# numpy is an optional (test-only) dependency — see the [oracles] extra. Skip the
# whole module gracefully when it is absent instead of failing collection.
np = pytest.importorskip("numpy")


@pytest.mark.benchmark
class TestMethodComparison:
    """Benchmark and compare reduction methods on Rips complexes."""

    def _create_point_cloud(self, n_points: int, seed: int = 42) -> FiniteMetricSpace:
        """Create a random 2D point cloud."""
        np.random.seed(seed)
        points = np.random.rand(n_points, 2)
        import math

        return FiniteMetricSpace(
            carrier=tuple(map(tuple, points)), distance=math.dist
        )

    @pytest.mark.parametrize("n_points", [30, 60, 100])
    def test_method_consistency(self, n_points: int, profile_benchmark: Any) -> None:
        """Verify all methods produce identical results.

        Tests that 'twist', 'cohomology', and 'standard' methods
        produce the same persistence pairs (within tolerance).
        """
        space = self._create_point_cloud(n_points)

        @profile_benchmark(track_memory=False)
        def get_results() -> tuple[tuple, tuple, tuple]:
            """Compute persistence pairs with all three methods."""
            pairs_standard = persistent_homology(space, method="standard")
            pairs_twist = persistent_homology(space, method="twist")
            pairs_cohomology = persistent_homology(space, method="cohomology")
            return pairs_standard, pairs_twist, pairs_cohomology

        (pairs_std, pairs_twist, pairs_coh), stats = get_results()

        # Verify all methods produce identical results
        assert (
            pairs_std == pairs_twist
        ), f"Standard and Twist differ for n={n_points}"
        assert (
            pairs_std == pairs_coh
        ), f"Standard and Cohomology differ for n={n_points}"
        assert len(pairs_std) > 0, f"No pairs computed for n={n_points}"

        # Log profiling stats
        assert stats.total_time > 0, "Profile should record positive wall time"

    @pytest.mark.parametrize("n_points", [40, 80])
    def test_twist_clearing_effectiveness(
        self, n_points: int, profile_benchmark: Any
    ) -> None:
        """Profile Twist algorithm and measure Clearing Lemma effectiveness.

        Computes ReductionStats to report:
        - Number of columns cleared
        - Number of column additions performed
        - Clearing ratio (fraction of columns skipped)
        """
        space = self._create_point_cloud(n_points)

        @profile_benchmark(track_memory=True)
        def profile_twist_stats() -> ReductionStats:
            """Profile Twist reduction and extract ReductionStats."""
            filtered = vietoris_rips_filtration(space, max_dimension=1)
            _, stats_obj = persistence_pairs_twist_with_stats(filtered)
            return stats_obj

        stats_obj, prof_stats = profile_twist_stats()

        # Verify stats are populated
        assert stats_obj.n_simplices > 0, "Should have simplices"
        assert (
            stats_obj.n_cleared >= 0
        ), "Cleared count should be non-negative"
        assert (
            0 <= stats_obj.clearing_ratio <= 1
        ), "Clearing ratio should be in [0, 1]"

        # Log performance metrics
        assert prof_stats.total_time > 0, "Profile should record positive wall time"


@pytest.mark.benchmark
class TestLargeDatasetOptimization:
    """Benchmark optimizations on larger realistic datasets."""

    def test_profile_large_rips(self, profile_benchmark: Any) -> None:
        """Profile Rips complex on 150-point cloud (realistic TDA size).

        Tests the optimized pipeline on a dataset large enough to show
        non-trivial reduction time.
        """

        @profile_benchmark(track_memory=True)
        def compute_large_rips() -> int:
            """Compute persistent homology on 150 random points."""
            np.random.seed(42)
            points = np.random.rand(150, 2)
            import math

            space = FiniteMetricSpace(
                carrier=tuple(map(tuple, points)), distance=math.dist
            )

            # Use default (optimized) method
            pairs = persistent_homology(space, max_dimension=1)
            return len(pairs)

        pair_count, stats = compute_large_rips()

        # Verify result
        assert isinstance(pair_count, int), "Pair count should be integer"
        assert pair_count > 0, "Should have persistence pairs"

        # Log profiling stats
        assert stats.total_time > 0, "Profile should record positive wall time"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
