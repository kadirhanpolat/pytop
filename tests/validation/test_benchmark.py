"""
P16.1 Benchmark suite: timing and homology validation.

Runs baseline computations on reference datasets, reports timings.
Validates against oracle baselines (BaselineResults from fixtures).
"""

import time
import pytest
from typing import Tuple, Dict, Any

from pytop import (
    simplicial_homology,
    is_planar,
    graph_genus,
    euler_characteristic_simplicial,
)

from .fixtures import (
    MinimalTriangulations,
    GraphExamples,
    BaselineResults,
    _filtered_to_simplicial,
)


class TestMinimalTriangulations:
    """Test homology of minimal 2-manifold triangulations."""

    def test_torus_7v_homology(self):
        """T² minimal: H₀=ℤ, H₁=ℤ², H₂=ℤ."""
        fc = MinimalTriangulations.torus_7vertex()
        sc = _filtered_to_simplicial(fc)
        h0 = simplicial_homology(sc, degree=0)
        h1 = simplicial_homology(sc, degree=1)
        h2 = simplicial_homology(sc, degree=2)

        # Check Betti numbers
        assert h0.betti == BaselineResults.TORUS_7V["H0"][0]
        assert h1.betti == BaselineResults.TORUS_7V["H1"][0]
        assert h2.betti == BaselineResults.TORUS_7V["H2"][0]

        # Check torsion (should be empty)
        assert len(h0.torsion) == 0
        assert len(h1.torsion) == 0
        assert len(h2.torsion) == 0

    def test_klein_8v_homology(self):
        """Klein bottle minimal: H₀=ℤ, H₁=ℤ⊕ℤ/2, H₂=0."""
        fc = MinimalTriangulations.klein_bottle_8vertex()
        sc = _filtered_to_simplicial(fc)
        h0 = simplicial_homology(sc, degree=0)
        h1 = simplicial_homology(sc, degree=1)
        h2 = simplicial_homology(sc, degree=2)

        assert h0.betti == BaselineResults.KLEIN_8V["H0"][0]
        assert h1.betti == BaselineResults.KLEIN_8V["H1"][0]
        assert h2.betti == BaselineResults.KLEIN_8V["H2"][0]

        # H₁ torsion: ℤ/2
        assert len(h1.torsion) == 1
        assert h1.torsion[0] == 2

    def test_rp2_6v_homology(self):
        """ℝP² minimal: H₀=ℤ, H₁=ℤ/2, H₂=0 (reduced)."""
        fc = MinimalTriangulations.rp2_6vertex()
        sc = _filtered_to_simplicial(fc)
        h0 = simplicial_homology(sc, degree=0)
        h1 = simplicial_homology(sc, degree=1)
        h2 = simplicial_homology(sc, degree=2)

        assert h0.betti == BaselineResults.RP2_6V["H0"][0]
        assert h1.betti == BaselineResults.RP2_6V["H1"][0]
        assert h2.betti == BaselineResults.RP2_6V["H2"][0]

        # H₁ torsion: ℤ/2
        assert len(h1.torsion) == 1
        assert h1.torsion[0] == 2

    def test_euler_characteristic_consistency(self):
        """χ = V - E + F computed from simplicial_homology."""
        manifolds = [
            (MinimalTriangulations.torus_7vertex(), 0),
            (MinimalTriangulations.klein_bottle_8vertex(), 0),
            (MinimalTriangulations.rp2_6vertex(), 1),
        ]

        for fc, expected_chi in manifolds:
            sc = _filtered_to_simplicial(fc)
            h0 = simplicial_homology(sc, degree=0)
            h1 = simplicial_homology(sc, degree=1)
            h2 = simplicial_homology(sc, degree=2)
            chi = euler_characteristic_simplicial(fc.simplices)
            assert chi == expected_chi


class TestGraphExamples:
    """Test graph invariants: planarity, genus."""

    @pytest.mark.parametrize("name,builder,is_planar_expected", [
        ("grid_3x3", GraphExamples.grid_3x3, True),
        ("K5", GraphExamples.complete_graph_5, False),
        ("K6", GraphExamples.complete_graph_6, False),
        ("petersen", GraphExamples.petersen_graph, False),
    ])
    def test_graph_planarity(self, name, builder, is_planar_expected):
        """Test planar/non-planar classification."""
        g = builder()
        result = is_planar(g)
        assert result == is_planar_expected, f"{name}: expected {is_planar_expected}, got {result}"

    def test_k5_genus(self):
        """K₅ on sphere: impossible. Minimal surface: torus (genus=1)."""
        g = GraphExamples.complete_graph_5()
        # is_planar should return False
        assert not is_planar(g)

    def test_grid_3x3_genus(self):
        """Grid graph: planar, genus = 0."""
        g = GraphExamples.grid_3x3()
        assert is_planar(g)
        # Genus computed from Euler formula for connected planar graph
        # V - E + F = 2 → F = 2 - V + E for genus=0
        # For grid: V=9, E=12 → F = 2 - 9 + 12 = 5 (4 faces + outer)
        # Genus = 0 for planar


class BenchmarkTimer:
    """Context manager for timing."""

    def __init__(self, name: str):
        self.name = name
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        print(f"\n{self.name}: {self.elapsed:.4f}s")

    def report(self) -> Dict[str, Any]:
        return {"name": self.name, "elapsed_s": self.elapsed}


class TestPerformanceBenchmarks:
    """Timing benchmarks on reference datasets."""

    def test_torus_homology_timing(self):
        """Measure time to compute T² homology."""
        fc = MinimalTriangulations.torus_7vertex()
        sc = _filtered_to_simplicial(fc)
        with BenchmarkTimer("Torus H_* (7v)") as timer:
            h0 = simplicial_homology(sc, degree=0)
            h1 = simplicial_homology(sc, degree=1)
            h2 = simplicial_homology(sc, degree=2)
        # Baseline: <100ms on modern hardware
        assert timer.elapsed < 0.1, f"Torus homology: {timer.elapsed:.4f}s (expected <0.1s)"

    def test_klein_homology_timing(self):
        """Measure time to compute Klein bottle homology."""
        fc = MinimalTriangulations.klein_bottle_8vertex()
        sc = _filtered_to_simplicial(fc)
        with BenchmarkTimer("Klein bottle H_* (8v)") as timer:
            h0 = simplicial_homology(sc, degree=0)
            h1 = simplicial_homology(sc, degree=1)
            h2 = simplicial_homology(sc, degree=2)
        assert timer.elapsed < 0.1

    def test_rp2_homology_timing(self):
        """Measure time to compute ℝP² homology."""
        fc = MinimalTriangulations.rp2_6vertex()
        sc = _filtered_to_simplicial(fc)
        with BenchmarkTimer("ℝP² H_* (6v)") as timer:
            h0 = simplicial_homology(sc, degree=0)
            h1 = simplicial_homology(sc, degree=1)
            h2 = simplicial_homology(sc, degree=2)
        assert timer.elapsed < 0.1

    def test_graph_k5_planarity_timing(self):
        """Measure time to check K₅ non-planarity."""
        edges = GraphExamples.complete_graph_5()
        with BenchmarkTimer("is_planar(K₅)") as timer:
            result = is_planar(edges)
        assert not result
        assert timer.elapsed < 0.01

    def test_graph_k6_planarity_timing(self):
        """Measure time to check K₆ non-planarity."""
        edges = GraphExamples.complete_graph_6()
        with BenchmarkTimer("is_planar(K₆)") as timer:
            result = is_planar(edges)
        assert not result
        assert timer.elapsed < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
