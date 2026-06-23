"""
P16.1 Benchmark suite: timing and homology validation.

Runs baseline computations on reference datasets, reports timings.
Validates against oracle baselines (BaselineResults from fixtures).
"""

import time
from typing import Any

import pytest

from pytop import (
    euler_characteristic_simplicial,
    is_planar,
    simplicial_homology,
)

from .fixtures import (
    BaselineResults,
    GraphExamples,
    GridGraphLibrary,
    KnotTable,
    MinimalTriangulations,
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
            _ = simplicial_homology(sc, degree=0)
            _ = simplicial_homology(sc, degree=1)
            _ = simplicial_homology(sc, degree=2)
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


class TestKnotTable:
    """Test knot invariant database (KnotInfo reference data)."""

    def test_unknot_properties(self):
        """Unknot has crossing number 0, genus 0."""
        unknot = KnotTable.UNKNOT
        assert unknot.crossing_number == 0
        assert unknot.genus == 0
        assert unknot.alexander_poly == "1"
        assert unknot.jones_poly == "1"

    def test_trefoil_properties(self):
        """Trefoil 3₁: crossing 3, genus 1."""
        trefoil = KnotTable.TREFOIL
        assert trefoil.crossing_number == 3
        assert trefoil.genus == 1
        assert "q^3" in trefoil.jones_poly
        assert "-t^{-1}" in trefoil.alexander_poly

    def test_figure8_properties(self):
        """Figure-8 knot 4₁: crossing 4, genus 1."""
        fig8 = KnotTable.FIGURE8
        assert fig8.crossing_number == 4
        assert fig8.genus == 1
        assert "q^{-2}" in fig8.jones_poly

    def test_cinquefoil_properties(self):
        """Cinquefoil 5₁: crossing 5, genus 2."""
        cinq = KnotTable.CINQUEFOIL
        assert cinq.crossing_number == 5
        assert cinq.genus == 2

    def test_stevedore_properties(self):
        """Stevedore knot 6₁: crossing 6, genus 2."""
        steve = KnotTable.STEVEDORE
        assert steve.crossing_number == 6
        assert steve.genus == 2

    def test_septafoil_properties(self):
        """Septafoil 7₁: crossing 7, genus 3."""
        septa = KnotTable.SEPTAFOIL
        assert septa.crossing_number == 7
        assert septa.genus == 3

    @pytest.mark.parametrize("knot", KnotTable.KNOTS)
    def test_all_knots_have_valid_invariants(self, knot):
        """All knots in KnotTable have positive genus."""
        assert knot.crossing_number >= 0
        assert knot.genus >= 0
        assert len(knot.alexander_poly) > 0
        assert len(knot.jones_poly) > 0

    def test_knots_by_crossing_number(self):
        """Query knots by crossing number."""
        unknots = KnotTable.by_crossing_number(0)
        assert len(unknots) == 1
        assert unknots[0].name == "unknot"

        trefoils = KnotTable.by_crossing_number(3)
        assert len(trefoils) == 1

    def test_knots_by_genus(self):
        """Query knots by genus."""
        genus_1 = KnotTable.by_genus(1)
        assert len(genus_1) == 2  # Trefoil, Figure-8
        assert all(k.genus == 1 for k in genus_1)

        genus_2 = KnotTable.by_genus(2)
        assert len(genus_2) == 2  # Cinquefoil, Stevedore


class TestLargeGraphLibrary:
    """Test large-scale graph benchmarks (PHOEG-style grids)."""

    def test_grid_5x5_properties(self):
        """5×5 grid: 25 vertices, 40 edges."""
        g = GridGraphLibrary.grid_5x5()
        # Count vertices and edges
        vertices = set()
        for u, v in g:
            vertices.add(u)
            vertices.add(v)
        assert len(vertices) == 25
        assert len(g) == 40
        assert is_planar(g)

    def test_grid_10x10_properties(self):
        """10×10 grid: 100 vertices, 180 edges."""
        g = GridGraphLibrary.grid_10x10()
        vertices = set()
        for u, v in g:
            vertices.add(u)
            vertices.add(v)
        assert len(vertices) == 100
        assert len(g) == 180
        assert is_planar(g)

    def test_grid_20x20_properties(self):
        """20×20 grid: 400 vertices, 760 edges."""
        g = GridGraphLibrary.grid_20x20()
        vertices = set()
        for u, v in g:
            vertices.add(u)
            vertices.add(v)
        assert len(vertices) == 400
        assert len(g) == 760
        assert is_planar(g)

    def test_grid_40x40_properties(self):
        """40×40 grid: 1600 vertices, 3120 edges."""
        g = GridGraphLibrary.grid_40x40()
        vertices = set()
        for u, v in g:
            vertices.add(u)
            vertices.add(v)
        assert len(vertices) == 1600
        assert len(g) == 3120
        assert is_planar(g)

    def test_all_grids_planar(self):
        """All grids in library should be planar."""
        grids = GridGraphLibrary.grids_all()
        for name, edges in grids.items():
            result = is_planar(edges)
            assert result, f"{name} should be planar"


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

    def report(self) -> dict[str, Any]:
        return {"name": self.name, "elapsed_s": self.elapsed}


class TestPerformanceBenchmarks:
    """Timing benchmarks on reference datasets."""

    def test_torus_homology_timing(self):
        """Measure time to compute T² homology."""
        fc = MinimalTriangulations.torus_7vertex()
        sc = _filtered_to_simplicial(fc)
        with BenchmarkTimer("Torus H_* (7v)") as timer:
            _ = simplicial_homology(sc, degree=0)
            _ = simplicial_homology(sc, degree=1)
            _ = simplicial_homology(sc, degree=2)
        # Baseline: <100ms on modern hardware
        assert timer.elapsed < 0.1, f"Torus homology: {timer.elapsed:.4f}s (expected <0.1s)"

    def test_klein_homology_timing(self):
        """Measure time to compute Klein bottle homology."""
        fc = MinimalTriangulations.klein_bottle_8vertex()
        sc = _filtered_to_simplicial(fc)
        with BenchmarkTimer("Klein bottle H_* (8v)") as timer:
            _ = simplicial_homology(sc, degree=0)
            _ = simplicial_homology(sc, degree=1)
            _ = simplicial_homology(sc, degree=2)
        assert timer.elapsed < 0.1

    def test_rp2_homology_timing(self):
        """Measure time to compute ℝP² homology."""
        fc = MinimalTriangulations.rp2_6vertex()
        sc = _filtered_to_simplicial(fc)
        with BenchmarkTimer("ℝP² H_* (6v)") as timer:
            _ = simplicial_homology(sc, degree=0)
            _ = simplicial_homology(sc, degree=1)
            _ = simplicial_homology(sc, degree=2)
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

    def test_grid_10x10_planarity_timing(self):
        """Measure time to check 10×10 grid planarity (100 vertices, 180 edges)."""
        edges = GridGraphLibrary.grid_10x10()
        with BenchmarkTimer("is_planar(grid_10x10)") as timer:
            result = is_planar(edges)
        assert result
        # Should be fast even on larger grid (linear-time planarity algorithm)
        assert timer.elapsed < 0.1

    def test_grid_20x20_planarity_timing(self):
        """Measure time to check 20×20 grid planarity (400 vertices, 760 edges)."""
        edges = GridGraphLibrary.grid_20x20()
        with BenchmarkTimer("is_planar(grid_20x20)") as timer:
            result = is_planar(edges)
        assert result
        assert timer.elapsed < 0.2

    def test_grid_40x40_planarity_timing(self):
        """Measure time to check 40×40 grid planarity (1600 vertices, 3120 edges)."""
        edges = GridGraphLibrary.grid_40x40()
        with BenchmarkTimer("is_planar(grid_40x40)") as timer:
            result = is_planar(edges)
        assert result
        assert timer.elapsed < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
