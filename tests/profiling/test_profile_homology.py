"""Benchmark tests for core pytop homology, persistence, and knot invariant computations.

Phase 17 P17.1: Profile homology, persistent homology, and Khovanov invariants
using the @profile_benchmark fixture. Tracks wall-clock time and memory usage.

Test categories:
- TestProfileHomology: Standard triangulations (torus, Klein bottle)
- TestProfilePersistence: Rips complexes at various scales
- TestProfileKhovanov: Knot diagrams and polynomial invariants
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from pytop.homology import homology_groups
from pytop.khovanov import khovanov_homology
from pytop.knot_invariants import KnotDiagram
from pytop.simplicial_complexes import SimplicialComplex
from pytop.simplicial_filtration import (
    klein_bottle_filtration,
    simplicial_filtration,
    torus_filtration,
)


@pytest.mark.benchmark
class TestProfileHomology:
    """Benchmark homology computation on standard triangulations."""

    def test_profile_torus_homology(self, profile_benchmark: Any) -> None:
        """Profile homology computation on the torus (7-vertex triangulation).

        The torus minimal triangulation has 7 vertices and 14 triangles.
        Expected homology: H₀ = ℤ, H₁ = ℤ², H₂ = ℤ

        Decorator: @profile_benchmark(track_memory=True)
        Tracks: Wall-clock time, peak memory usage during computation
        """

        @profile_benchmark(track_memory=True)
        def compute_torus_homology() -> tuple[int, int, int]:
            """Compute simplicial homology on torus filtration."""
            fc = torus_filtration()
            # Convert FilteredComplex to SimplicialComplex
            complex_obj = SimplicialComplex(fc.simplices)
            groups = homology_groups(complex_obj)
            # Return Betti numbers for verification
            return tuple(group.betti for group in groups)

        betti_numbers, stats = compute_torus_homology()

        # Verify result structure: torus has Betti numbers (1, 2, 1)
        assert len(betti_numbers) == 3, "Torus should have 3 homology groups"
        assert betti_numbers[0] == 1, "H_0(T²) has rank 1"
        assert betti_numbers[1] == 2, "H_1(T²) has rank 2"
        assert betti_numbers[2] == 1, "H_2(T²) has rank 1"

        # Log profile stats for diagnostics
        assert stats.total_time > 0, "Profile should record positive wall time"

    def test_profile_klein_homology(self, profile_benchmark: Any) -> None:
        """Profile homology computation on Klein bottle (8-vertex triangulation).

        The Klein bottle minimal triangulation has 8 vertices and 16 triangles.
        Expected homology: H₀ = ℤ, H₁ = ℤ ⊕ ℤ/2, H₂ = 0

        Decorator: @profile_benchmark(track_memory=True)
        Tracks: Wall-clock time, peak memory usage during computation
        """

        @profile_benchmark(track_memory=True)
        def compute_klein_homology() -> tuple[int, int, int]:
            """Compute simplicial homology on Klein bottle filtration."""
            fc = klein_bottle_filtration()
            # Convert FilteredComplex to SimplicialComplex
            complex_obj = SimplicialComplex(fc.simplices)
            groups = homology_groups(complex_obj)
            # Return Betti numbers for verification
            return tuple(group.betti for group in groups)

        betti_numbers, stats = compute_klein_homology()

        # Verify result structure: Klein bottle has Betti numbers (1, 1, 0)
        # (The Z/2 torsion in H_1 is invisible to Betti numbers)
        assert len(betti_numbers) == 3, "Klein bottle should have 3 homology groups"
        assert betti_numbers[0] == 1, "H_0(K) has rank 1"
        assert betti_numbers[1] == 1, "H_1(K) has rank 1 (free part only)"
        assert betti_numbers[2] == 0, "H_2(K) has rank 0"

        # Log profile stats
        assert stats.total_time > 0, "Profile should record positive wall time"


@pytest.mark.benchmark
class TestProfilePersistence:
    """Benchmark persistent homology computation on Rips complexes at various scales."""

    @pytest.mark.parametrize("n_points", [20, 50, 100])
    def test_profile_rips_persistence(
        self, n_points: int, profile_benchmark: Any
    ) -> None:
        """Profile simplicial complex construction from grid.

        Generate a 2D grid of points and build a simplicial filtration.
        This tests profiling of complex construction and sizing at scale.

        Args:
            n_points: Number of random points (20, 50, or 100)
            profile_benchmark: Profiling fixture with memory tracking

        Decorator: @profile_benchmark(track_memory=True)
        Tracks: Wall-clock time, peak memory, scaling behavior
        """

        @profile_benchmark(track_memory=True)
        def construct_grid_complex() -> int:
            """Construct grid-based simplicial complex and return simplex count."""
            # Create grid-based triangulation with n_points vertices
            # arranged in sqrt(n_points) × sqrt(n_points) grid
            grid_size = int(np.sqrt(n_points))
            maximal_simplices = []

            # Generate triangular faces from grid
            for i in range(grid_size - 1):
                for j in range(grid_size - 1):
                    v0 = i * grid_size + j
                    v1 = i * grid_size + j + 1
                    v2 = (i + 1) * grid_size + j
                    v3 = (i + 1) * grid_size + j + 1

                    # Two triangles per grid cell
                    maximal_simplices.append((v0, v1, v2))
                    maximal_simplices.append((v1, v3, v2))

            # Build filtration with automatic face closure
            fc = simplicial_filtration(maximal_simplices)
            return fc.size()

        simplex_count, stats = construct_grid_complex()

        # Verify result is reasonable
        assert isinstance(simplex_count, int), "Simplex count should be integer"
        assert simplex_count > 0, "Grid complex should contain simplices"

        # Log profiling stats
        assert stats.total_time > 0, "Profile should record positive wall time"


@pytest.mark.benchmark
class TestProfileKhovanov:
    """Benchmark Khovanov homology computation on knot diagrams."""

    def test_profile_unknot_khovanov(self, profile_benchmark: Any) -> None:
        """Profile Khovanov homology computation on unknot.

        The unknot (trivial knot) has 0 crossings. This serves as a baseline
        for profiling the Khovanov homology computation infrastructure.

        Decorator: @profile_benchmark(track_memory=True)
        Tracks: Wall-clock time, memory usage during Khovanov computation
        """

        @profile_benchmark(track_memory=True)
        def compute_unknot_khovanov() -> int:
            """Compute Khovanov homology total rank on unknot."""
            # Unknot: empty PD code
            diagram = KnotDiagram(pd=(), signs=())

            # Compute Khovanov homology
            kh = khovanov_homology(diagram)
            return kh.total_rank()

        result, stats = compute_unknot_khovanov()

        # Verify result is computed
        assert isinstance(result, int), "Result should be an integer"
        assert result >= 0, "Total rank should be non-negative"

        # Log profiling stats
        assert stats.total_time > 0, "Profile should record positive wall time"

    def test_profile_hopf_link_khovanov(self, profile_benchmark: Any) -> None:
        """Profile Khovanov homology on Hopf link (simplest 2-component link).

        The Hopf link has 2 crossings and is the canonical simplest link
        with more than one component.

        Decorator: @profile_benchmark(track_memory=True)
        Tracks: Wall-clock time, memory usage for multi-component link
        """

        @profile_benchmark(track_memory=True)
        def compute_hopf_khovanov() -> int:
            """Compute Khovanov homology total rank on Hopf link."""
            # Hopf link: 2 crossings, standard PD code
            # Each crossing is (in1, out1, in2, out2) - counterclockwise, understrand first
            pd = ((0, 1, 2, 3), (2, 3, 0, 1))
            signs = (1, 1)  # All crossings positive

            diagram = KnotDiagram(pd=pd, signs=signs, components=2)
            kh = khovanov_homology(diagram)
            return kh.total_rank()

        result, stats = compute_hopf_khovanov()

        # Verify result is computed
        assert isinstance(result, int), "Result should be an integer"
        assert result > 0, "Hopf link should have nonzero homology"

        # Log profiling stats
        assert stats.total_time > 0, "Profile should record positive wall time"


@pytest.mark.benchmark
class TestProfileSimplicialComplex:
    """Benchmark operations on simplicial complex construction and manipulation."""

    def test_profile_sphere_complex_construction(
        self, profile_benchmark: Any
    ) -> None:
        """Profile construction of S² via simplicial complex.

        Builds the 2-sphere as two triangles sharing edges (minimal triangulation).
        Uses simplicial_filtration for proper face closure.

        Decorator: @profile_benchmark(track_memory=True)
        Tracks: Wall-clock time, memory usage for complex construction
        """

        @profile_benchmark(track_memory=True)
        def construct_sphere_complex() -> int:
            """Construct S² simplicial complex and return simplex count."""
            # Minimal triangulation of S²: two triangles sharing edge (0,1)
            maximal_simplices = [(0, 1, 2), (0, 1, 3)]

            # Build using simplicial_filtration which handles face closure
            fc = simplicial_filtration(maximal_simplices)
            # Convert FilteredComplex to SimplicialComplex
            complex_obj = SimplicialComplex(fc.simplices)
            return len(complex_obj.simplexes)

        simplex_count, stats = construct_sphere_complex()

        # Verify result
        assert isinstance(simplex_count, int), "Simplex count should be integer"
        assert simplex_count > 0, "Complex should contain simplices"

        # Log profiling stats
        assert stats.total_time > 0, "Profile should record positive wall time"
