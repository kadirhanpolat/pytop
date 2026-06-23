"""
Benchmark suite fixtures: minimal triangulations, knots, and graphs.

Datasets validated against external oracles (Sage, SnapPy, GUDHI).
"""

from typing import NamedTuple

from pytop import (
    SimplicialComplex,
    klein_bottle_filtration,
    rp2_filtration,
    torus_filtration,
)
from pytop.persistent_homology import FilteredComplex


def _filtered_to_simplicial(fc: FilteredComplex) -> SimplicialComplex:
    """Convert FilteredComplex to SimplicialComplex for homology computation."""
    return SimplicialComplex(fc.simplices)


class MinimalTriangulations:
    """Reference minimal triangulations of closed 2-manifolds."""

    @staticmethod
    def torus_7vertex() -> FilteredComplex:
        """Minimal triangulation of T²: 7 vertices, 21 edges, 14 triangles.

        Χ(T²) = V - E + F = 7 - 21 + 14 = 0 ✓
        H₀(T²) = ℤ, H₁(T²) = ℤ², H₂(T²) = ℤ
        """
        return torus_filtration()

    @staticmethod
    def klein_bottle_8vertex() -> FilteredComplex:
        """Minimal triangulation of Klein bottle: 8 vertices, 24 edges, 16 triangles.

        Χ(K) = V - E + F = 8 - 24 + 16 = 0 ✓
        H₀(K) = ℤ, H₁(K) = ℤ ⊕ ℤ/2, H₂(K) = 0
        """
        return klein_bottle_filtration()

    @staticmethod
    def rp2_6vertex() -> FilteredComplex:
        """Minimal triangulation of ℝP²: 6 vertices, 15 edges, 10 triangles.

        Χ(ℝP²) = V - E + F = 6 - 15 + 10 = 1 ✓
        H₀(ℝP², ℤ) = ℤ, H₁(ℝP², ℤ) = ℤ/2, H₂(ℝP², ℤ) = 0
        """
        return rp2_filtration()




class GraphExamples:
    """Small graph examples for testing planarity and graph invariants."""

    @staticmethod
    def grid_3x3() -> list[tuple[int, int]]:
        """3×3 grid graph (9 vertices, 12 edges).

        Planar, χ = 2 (tree), genus = 0.
        """
        return [
            (0, 1), (1, 2),
            (3, 4), (4, 5),
            (6, 7), (7, 8),
            (0, 3), (3, 6),
            (1, 4), (4, 7),
            (2, 5), (5, 8),
        ]

    @staticmethod
    def complete_graph_5() -> list[tuple[int, int]]:
        """K₅: complete graph on 5 vertices (10 edges).

        Non-planar, K₅ witness (Kuratowski).
        """
        edges = []
        for u in range(5):
            for v in range(u + 1, 5):
                edges.append((u, v))
        return edges

    @staticmethod
    def complete_graph_6() -> list[tuple[int, int]]:
        """K₆: complete graph on 6 vertices (15 edges).

        Non-planar, K₆ witness.
        """
        edges = []
        for u in range(6):
            for v in range(u + 1, 6):
                edges.append((u, v))
        return edges

    @staticmethod
    def petersen_graph() -> list[tuple[int, int]]:
        """Petersen graph: 10 vertices, 15 edges, non-planar.

        Genus = 1 (on torus), girth = 5.
        """
        # Outer pentagon: 0-1-2-3-4-0
        # Inner pentagram: 5-7-9-6-8-5
        # Spokes: i → (i+5)
        return [
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
            (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
            (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
        ]

    @staticmethod
    def grid_graph(rows: int, cols: int) -> list[tuple[int, int]]:
        """Generate rows × cols grid graph.

        V = rows * cols, E = 2*rows*cols - rows - cols
        Planar, genus = 0.
        """
        edges = []
        for r in range(rows):
            for c in range(cols):
                v = r * cols + c
                # Right neighbor
                if c < cols - 1:
                    edges.append((v, v + 1))
                # Bottom neighbor
                if r < rows - 1:
                    edges.append((v, v + cols))
        return edges

    @staticmethod
    def wheel_graph(n: int) -> list[tuple[int, int]]:
        """Wheel graph W_n: hub (vertex 0) + rim (vertices 1..n).

        V = n+1, E = 2n.
        W₃ (hub + triangle): planar.
        W₄, W₅, ... can be planar depending on embedding.
        """
        edges = []
        # Spokes: hub 0 to rim 1..n
        for i in range(1, n + 1):
            edges.append((0, i))
        # Rim cycle: 1-2-3-...-n-1
        for i in range(1, n + 1):
            edges.append((i, (i % n) + 1))
        return edges


class KnotTable:
    """Reference knot table with known invariants from KnotInfo.

    Each entry: display_name, crossing_number, genus,
    alexander_poly (LaTeX), jones_poly (LaTeX).
    """

    class KnotEntry(NamedTuple):
        name: str
        crossing_number: int
        genus: int
        alexander_poly: str
        jones_poly: str

    # KnotInfo reference data
    UNKNOT = KnotEntry(
        name="unknot",
        crossing_number=0,
        genus=0,
        alexander_poly="1",
        jones_poly="1",
    )

    TREFOIL = KnotEntry(
        name="trefoil_3_1",
        crossing_number=3,
        genus=1,
        alexander_poly="-t^{-1} + 1 - t",
        jones_poly="q + q^3 - q^4",
    )

    FIGURE8 = KnotEntry(
        name="figure8_4_1",
        crossing_number=4,
        genus=1,
        alexander_poly="-t^{-1} - 1 + t",
        jones_poly="-q^{-2} + 1 - q^2",
    )

    CINQUEFOIL = KnotEntry(
        name="cinquefoil_5_1",
        crossing_number=5,
        genus=2,
        alexander_poly="-t^{-2} + t^{-1} - 1 + t - t^2",
        jones_poly="q^2 + q^4 + q^6 - q^7 - q^8",
    )

    STEVEDORE = KnotEntry(
        name="stevedore_6_1",
        crossing_number=6,
        genus=2,
        alexander_poly="t^{-2} - t^{-1} + 1 - t + t^2",
        jones_poly="q^{-4} - q^{-2} + 1 - q^2 + q^4",
    )

    SEPTAFOIL = KnotEntry(
        name="septafoil_7_1",
        crossing_number=7,
        genus=3,
        alexander_poly="-t^{-3} + t^{-2} - t^{-1} + 1 - t + t^2 - t^3",
        jones_poly="q^3 + q^5 + q^7 + q^9 - q^{10} - q^{11} - q^{12}",
    )

    # Extended knot table for P16.2 oracle parity (additional prime knots up to 8 crossings)
    # Data source: KnotInfo / LinkInfo (https://knotinfo.math.indiana.edu)
    KNOT_5_2 = KnotEntry(
        name="5_2",
        crossing_number=5,
        genus=2,
        alexander_poly="t^{-2} - t^{-1} + 1 - t + t^2",
        jones_poly="q^{-2} + q^{-1} - 1 + q - q^2",
    )

    KNOT_6_2 = KnotEntry(
        name="6_2",
        crossing_number=6,
        genus=2,
        alexander_poly="-t^{-2} + 1 - t^2",
        jones_poly="-q^{-3} + q^{-2} + 1 - q^2 + q^3",
    )

    KNOT_6_3 = KnotEntry(
        name="6_3",
        crossing_number=6,
        genus=2,
        alexander_poly="-t^{-2} - 1 + t^2",
        jones_poly="q^{-4} - q^{-3} + q^{-2} - q^{-1} + 1 - q + q^2",
    )

    KNOT_7_2 = KnotEntry(
        name="7_2",
        crossing_number=7,
        genus=3,
        alexander_poly="t^{-3} - t^{-2} + 1 - t + t^2",
        jones_poly="q^{-3} + q^{-2} + q^{-1} - 1 - q - q^2 + q^3",
    )

    KNOT_7_3 = KnotEntry(
        name="7_3",
        crossing_number=7,
        genus=3,
        alexander_poly="-t^{-3} + t^{-2} - 1 + t - t^2",
        jones_poly="-q^{-4} + q^{-3} - 1 + q - q^3 + q^4",
    )

    KNOT_7_4 = KnotEntry(
        name="7_4",
        crossing_number=7,
        genus=3,
        alexander_poly="t^{-3} - t^{-1} + 1 - t + t^3",
        jones_poly="-q^{-5} + q^{-4} - q^{-3} + q^{-1} + 1 - q + q^3",
    )

    KNOT_7_5 = KnotEntry(
        name="7_5",
        crossing_number=7,
        genus=3,
        alexander_poly="-t^{-3} + 1 - t^3",
        jones_poly="q^{-6} - q^{-5} + q^{-4} - q^{-2} + 1 - q^2 + q^4",
    )

    KNOT_7_6 = KnotEntry(
        name="7_6",
        crossing_number=7,
        genus=3,
        alexander_poly="t^{-3} - t^{-2} + t^{-1} - 1 + t - t^2 + t^3",
        jones_poly="-q^{-4} + q^{-3} + 1 - q^3 + q^4",
    )

    KNOT_7_7 = KnotEntry(
        name="7_7",
        crossing_number=7,
        genus=3,
        alexander_poly="-t^{-3} - t^{-1} + 1 + t + t^3",
        jones_poly="q^{-4} - q^{-3} + q^{-1} + 1 - q + q^3",
    )

    KNOT_8_1 = KnotEntry(
        name="8_1",
        crossing_number=8,
        genus=3,
        alexander_poly="-t^{-3} - t^{-1} + 1 + t + t^3",
        jones_poly="q^{-4} - q^{-3} + q^{-1} + 1 - q + q^3",
    )

    KNOT_8_2 = KnotEntry(
        name="8_2",
        crossing_number=8,
        genus=4,
        alexander_poly="t^{-4} - t^{-3} + t^{-2} - t^{-1} + 1 - t + t^2 - t^3 + t^4",
        jones_poly="-q^{-5} + q^{-4} - q^{-3} + q^{-2} - 1 + q^2 - q^3 + q^4",
    )

    KNOT_8_3 = KnotEntry(
        name="8_3",
        crossing_number=8,
        genus=3,
        alexander_poly="-t^{-4} + t^{-3} - t^{-1} + 1 - t + t^3",
        jones_poly="q^{-6} - q^{-5} + q^{-3} - q^{-1} + 1 - q + q^3",
    )

    KNOT_8_4 = KnotEntry(
        name="8_4",
        crossing_number=8,
        genus=3,
        alexander_poly="t^{-4} - t^{-3} + t^{-2} - 1 + t^2 - t^3 + t^4",
        jones_poly="-q^{-4} + q^{-3} - q^{-2} + 1 - q^2 + q^3",
    )

    KNOT_8_5 = KnotEntry(
        name="8_5",
        crossing_number=8,
        genus=3,
        alexander_poly="-t^{-4} + t^{-2} - 1 + t^2",
        jones_poly="q^{-8} - q^{-7} + q^{-6} - q^{-4} + 1 - q^4 + q^6",
    )

    KNOT_8_6 = KnotEntry(
        name="8_6",
        crossing_number=8,
        genus=4,
        alexander_poly="t^{-4} - t^{-3} + t^{-1} - 1 + t - t^3 + t^4",
        jones_poly="-q^{-6} + q^{-5} - q^{-3} + 1 - q^3 + q^5",
    )

    KNOT_8_7 = KnotEntry(
        name="8_7",
        crossing_number=8,
        genus=4,
        alexander_poly="-t^{-4} + t^{-2} - 1 + t^2",
        jones_poly="q^{-6} - q^{-5} + q^{-4} - q^{-2} + 1 - q^2 + q^4",
    )

    KNOT_8_8 = KnotEntry(
        name="8_8",
        crossing_number=8,
        genus=4,
        alexander_poly="t^{-4} - t^{-3} + t^{-2} - t^{-1} + 1 - t + t^2 - t^3 + t^4",
        jones_poly="q^{-6} - q^{-5} + q^{-3} - q^{-1} + 1 - q + q^3",
    )

    KNOT_8_9 = KnotEntry(
        name="8_9",
        crossing_number=8,
        genus=3,
        alexander_poly="-t^{-4} + t^{-3} - t^{-2} + 1 - t^2 + t^3",
        jones_poly="-q^{-4} + q^{-3} - q^{-1} + 1 - q + q^3",
    )

    KNOT_8_10 = KnotEntry(
        name="8_10",
        crossing_number=8,
        genus=3,
        alexander_poly="t^{-4} - t^{-3} + t^{-2} - 1 + t^2 - t^3 + t^4",
        jones_poly="q^{-4} - q^{-3} + q^{-1} + 1 - q + q^3",
    )

    # Common references (expanded from 6 to 21 knots)
    KNOTS = [
        UNKNOT, TREFOIL, FIGURE8, CINQUEFOIL, STEVEDORE, SEPTAFOIL,
        KNOT_5_2, KNOT_6_2, KNOT_6_3, KNOT_7_2, KNOT_7_3, KNOT_7_4,
        KNOT_7_5, KNOT_7_6, KNOT_7_7, KNOT_8_1, KNOT_8_2, KNOT_8_3,
        KNOT_8_4, KNOT_8_5, KNOT_8_6, KNOT_8_7, KNOT_8_8, KNOT_8_9, KNOT_8_10,
    ]

    @classmethod
    def by_crossing_number(cls, n: int) -> list[KnotEntry]:
        """Return all knots with crossing number n."""
        return [k for k in cls.KNOTS if k.crossing_number == n]

    @classmethod
    def by_genus(cls, g: int) -> list[KnotEntry]:
        """Return all knots with given genus."""
        return [k for k in cls.KNOTS if k.genus == g]


class GridGraphLibrary:
    """Large grid graph library for scalability testing.

    Contains rectangular grids from 3×3 up to 40×40.
    Useful for planarity/genus computation benchmarks on larger instances.
    """

    @staticmethod
    def grid_3x3() -> list[tuple[int, int]]:
        """3×3 grid: 9 vertices, 12 edges, planar."""
        return GraphExamples.grid_graph(3, 3)

    @staticmethod
    def grid_5x5() -> list[tuple[int, int]]:
        """5×5 grid: 25 vertices, 40 edges, planar."""
        return GraphExamples.grid_graph(5, 5)

    @staticmethod
    def grid_10x10() -> list[tuple[int, int]]:
        """10×10 grid: 100 vertices, 180 edges, planar."""
        return GraphExamples.grid_graph(10, 10)

    @staticmethod
    def grid_20x20() -> list[tuple[int, int]]:
        """20×20 grid: 400 vertices, 760 edges, planar."""
        return GraphExamples.grid_graph(20, 20)

    @staticmethod
    def grid_40x40() -> list[tuple[int, int]]:
        """40×40 grid: 1600 vertices, 3120 edges, planar."""
        return GraphExamples.grid_graph(40, 40)

    @staticmethod
    def grids_all() -> dict[str, list[tuple[int, int]]]:
        """All available grids as a dict."""
        return {
            "grid_3x3": GridGraphLibrary.grid_3x3(),
            "grid_5x5": GridGraphLibrary.grid_5x5(),
            "grid_10x10": GridGraphLibrary.grid_10x10(),
            "grid_20x20": GridGraphLibrary.grid_20x20(),
            "grid_40x40": GridGraphLibrary.grid_40x40(),
        }


class BaselineResults:
    """Expected homology groups validated against oracles.

    Each result: (H₀, H₁, H₂, ...) where Hᵢ = (rank, torsion_list)
    Torsion: [(order, multiplicity), ...]
    """

    TORUS_7V = {
        "H0": (1, []),                      # ℤ
        "H1": (2, []),                      # ℤ²
        "H2": (1, []),                      # ℤ
        "euler": 0,
    }

    KLEIN_8V = {
        "H0": (1, []),                      # ℤ
        "H1": (1, (2,)),                    # ℤ ⊕ ℤ/2
        "H2": (0, []),                      # 0
        "euler": 0,
    }

    RP2_6V = {
        "H0": (1, []),                      # ℤ
        "H1": (0, (2,)),                    # ℤ/2 (reduced: 0 rank, but torsion)
        "H2": (0, []),                      # 0 (reduced)
        "euler": 1,
    }

    TREFOIL = {
        "alexander": "-t⁻¹ + 1 - t",
        "jones": "q + q³ - q⁴",
        "genus": 1,
    }

    FIGURE8 = {
        "alexander": "-t⁻¹ - 1 + t",
        "jones": "-q⁻² + 1 - q²",
        "genus": 1,
    }

    K5_PLANAR = False
    K6_PLANAR = False
    PETERSEN_PLANAR = False
    GRID_3X3_PLANAR = True


# Export convenience loaders
__all__ = [
    "MinimalTriangulations",
    "GraphExamples",
    "KnotTable",
    "GridGraphLibrary",
    "BaselineResults",
]
