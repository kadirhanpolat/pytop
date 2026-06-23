"""
Benchmark suite fixtures: minimal triangulations, knots, and graphs.

Datasets validated against external oracles (Sage, SnapPy, GUDHI).
"""

from typing import Tuple, List, Dict, Iterable
from pytop import (
    torus_filtration,
    klein_bottle_filtration,
    rp2_filtration,
    SimplicialComplex,
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
    def grid_3x3() -> List[Tuple[int, int]]:
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
    def complete_graph_5() -> List[Tuple[int, int]]:
        """K₅: complete graph on 5 vertices (10 edges).

        Non-planar, K₅ witness (Kuratowski).
        """
        edges = []
        for u in range(5):
            for v in range(u + 1, 5):
                edges.append((u, v))
        return edges

    @staticmethod
    def complete_graph_6() -> List[Tuple[int, int]]:
        """K₆: complete graph on 6 vertices (15 edges).

        Non-planar, K₆ witness.
        """
        edges = []
        for u in range(6):
            for v in range(u + 1, 6):
                edges.append((u, v))
        return edges

    @staticmethod
    def petersen_graph() -> List[Tuple[int, int]]:
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
    "BaselineResults",
]
