"""Tests for persistent_ktheory.py — rational persistent K-theory."""

from __future__ import annotations

import math

import pytest

from pytop.homology import SimplicialComplex
from pytop.persistent_homology import vietoris_rips_filtration
from pytop.persistent_ktheory import (
    KBarcode,
    k0_simplicial,
    k1_simplicial,
    k_barcode,
    k_betti_numbers,
    k_theory_groups,
)
from pytop.simplicial_filtration import torus_filtration

# ---------------------------------------------------------------------------
# Small simplicial complexes
# ---------------------------------------------------------------------------

# Point
_PT = SimplicialComplex([(0,)])

# Circle S¹ (triangulated as triangle boundary): β₀=1, β₁=1
_S1 = SimplicialComplex([(0,), (1,), (2,), (0, 1), (1, 2), (0, 2)])

# Sphere S² (boundary of tetrahedron): β₀=1, β₁=0, β₂=1
_S2 = SimplicialComplex(
    [
        (0,), (1,), (2,), (3,),
        (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
        (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3),
    ]
)

# Filled triangle (disk D²): contractible, β₀=1, all others 0
_DISK = SimplicialComplex(
    [(0,), (1,), (2,), (0, 1), (1, 2), (0, 2), (0, 1, 2)]
)

# Two disjoint edges (two intervals): β₀=2, β₁=0
_TWO_EDGES = SimplicialComplex(
    [(0,), (1,), (2,), (3,), (0, 1), (2, 3)]
)


# ---------------------------------------------------------------------------
# k_theory_groups
# ---------------------------------------------------------------------------


class TestKTheoryGroups:
    def test_point_k0_rank_one(self) -> None:
        g = k_theory_groups(_PT)
        assert g.k0_rank == 1

    def test_point_k1_rank_zero(self) -> None:
        g = k_theory_groups(_PT)
        assert g.k1_rank == 0

    def test_circle_k0_rank_one(self) -> None:
        # S¹: β₀=1 (even) → K⁰ rank = 1
        g = k_theory_groups(_S1)
        assert g.k0_rank == 1

    def test_circle_k1_rank_one(self) -> None:
        # S¹: β₁=1 (odd) → K¹ rank = 1
        g = k_theory_groups(_S1)
        assert g.k1_rank == 1

    def test_sphere_s2_k0_rank_two(self) -> None:
        # S²: β₀=1, β₂=1 (both even) → K⁰ rank = 2
        g = k_theory_groups(_S2)
        assert g.k0_rank == 2

    def test_sphere_s2_k1_rank_zero(self) -> None:
        # S²: β₁=0 (no odd Betti) → K¹ rank = 0
        g = k_theory_groups(_S2)
        assert g.k1_rank == 0

    def test_disk_contractible_k0_one(self) -> None:
        g = k_theory_groups(_DISK)
        assert g.k0_rank == 1
        assert g.k1_rank == 0

    def test_two_disjoint_edges_k0_two(self) -> None:
        # Two components: β₀=2 → K⁰ rank = 2
        g = k_theory_groups(_TWO_EDGES)
        assert g.k0_rank == 2
        assert g.k1_rank == 0

    def test_betti_numbers_stored(self) -> None:
        g = k_theory_groups(_S1)
        assert len(g.betti_numbers) >= 2
        assert g.betti_numbers[0] == 1
        assert g.betti_numbers[1] == 1

    def test_rational_string_zero(self) -> None:
        g = k_theory_groups(_PT)
        assert g.k1_rational == "0"

    def test_rational_string_Q(self) -> None:
        g = k_theory_groups(_PT)
        assert g.k0_rational == "ℚ"

    def test_rational_string_Qn(self) -> None:
        g = k_theory_groups(_S2)
        assert "2" in g.k0_rational or g.k0_rank == 2

    def test_torus_k0_rank_two(self) -> None:
        # T²: β₀=1, β₁=2, β₂=1 → K⁰ rank = 1+1 = 2
        filt = torus_filtration()
        torus = SimplicialComplex(filt.simplices)
        g = k_theory_groups(torus)
        assert g.k0_rank == 2

    def test_torus_k1_rank_two(self) -> None:
        # T²: β₁=2 → K¹ rank = 2
        filt = torus_filtration()
        torus = SimplicialComplex(filt.simplices)
        g = k_theory_groups(torus)
        assert g.k1_rank == 2


# ---------------------------------------------------------------------------
# k0_simplicial and k1_simplicial
# ---------------------------------------------------------------------------


class TestKSimplicial:
    def test_k0_point(self) -> None:
        assert k0_simplicial(_PT) == 1

    def test_k1_point(self) -> None:
        assert k1_simplicial(_PT) == 0

    def test_k0_circle(self) -> None:
        assert k0_simplicial(_S1) == 1

    def test_k1_circle(self) -> None:
        assert k1_simplicial(_S1) == 1

    def test_k0_sphere(self) -> None:
        assert k0_simplicial(_S2) == 2

    def test_k1_sphere(self) -> None:
        assert k1_simplicial(_S2) == 0

    def test_k0_disk(self) -> None:
        assert k0_simplicial(_DISK) == 1

    def test_k1_disk(self) -> None:
        assert k1_simplicial(_DISK) == 0


# ---------------------------------------------------------------------------
# k_betti_numbers
# ---------------------------------------------------------------------------


class TestKBettiNumbers:
    def test_point_returns_1_0(self) -> None:
        assert k_betti_numbers(_PT) == (1, 0)

    def test_circle_returns_1_1(self) -> None:
        assert k_betti_numbers(_S1) == (1, 1)

    def test_sphere_returns_2_0(self) -> None:
        assert k_betti_numbers(_S2) == (2, 0)

    def test_k_euler_equals_topological_euler(self) -> None:
        # χ_K = rank K⁰ - rank K¹ = χ (topological)
        k0, k1 = k_betti_numbers(_S1)
        assert k0 - k1 == 0  # χ(S¹) = 0

        k0s, k1s = k_betti_numbers(_S2)
        assert k0s - k1s == 2  # χ(S²) = 2

        k0d, k1d = k_betti_numbers(_DISK)
        assert k0d - k1d == 1  # χ(D²) = 1


# ---------------------------------------------------------------------------
# k_barcode (persistent K-theory)
# ---------------------------------------------------------------------------


class _CircleCloud:
    """Eight evenly-spaced points on the unit circle."""

    carrier = [
        (math.cos(2 * math.pi * i / 8), math.sin(2 * math.pi * i / 8))
        for i in range(8)
    ]

    def distance_between(self, a: tuple, b: tuple) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class _LineCloud:
    """Three collinear points — contractible."""

    carrier = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]

    def distance_between(self, a: tuple, b: tuple) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class TestKBarcode:
    def _circle_barcode(self) -> KBarcode:
        filt = vietoris_rips_filtration(_CircleCloud(), max_dimension=2)
        return k_barcode(filt)

    def _line_barcode(self) -> KBarcode:
        # max_dimension=2 fills the triangle at scale 2, killing the spurious H₁
        filt = vietoris_rips_filtration(_LineCloud(), max_dimension=2)
        return k_barcode(filt)

    def test_circle_has_k0_pairs(self) -> None:
        kb = self._circle_barcode()
        assert len(kb.k0_pairs) >= 1

    def test_circle_has_k1_pairs(self) -> None:
        kb = self._circle_barcode()
        assert len(kb.k1_pairs) >= 1

    def test_k0_pairs_even_dimension(self) -> None:
        kb = self._circle_barcode()
        for p in kb.k0_pairs:
            assert p.dimension % 2 == 0

    def test_k1_pairs_odd_dimension(self) -> None:
        kb = self._circle_barcode()
        for p in kb.k1_pairs:
            assert p.dimension % 2 == 1

    def test_all_pairs_is_union(self) -> None:
        kb = self._circle_barcode()
        all_set = set(kb.all_pairs)
        assert set(kb.k0_pairs) <= all_set
        assert set(kb.k1_pairs) <= all_set
        assert len(kb.k0_pairs) + len(kb.k1_pairs) == len(kb.all_pairs)

    def test_line_k0_betti_at_large_scale(self) -> None:
        kb = self._line_barcode()
        # At large scale the line cloud is contractible → K⁰ rank = 1
        assert kb.k0_betti_at(1e9) == 1

    def test_line_k1_betti_zero_at_large_scale(self) -> None:
        kb = self._line_barcode()
        assert kb.k1_betti_at(1e9) == 0

    def test_euler_characteristic_at_scale_zero_circle(self) -> None:
        # At scale=0: 8 isolated points → K⁰=8, K¹=0, χ_K = 8
        kb = self._circle_barcode()
        chi = kb.euler_characteristic_at(0.0)
        assert chi == 8

    def test_euler_characteristic_at_large_scale_line(self) -> None:
        # Line with max_dim=2 fills the triangle at scale 2 → contractible → χ_K=1
        kb = self._line_barcode()
        chi = kb.euler_characteristic_at(1e9)
        assert chi == 1  # χ(pt) = 1

    def test_max_dimension_filter(self) -> None:
        filt = vietoris_rips_filtration(_CircleCloud(), max_dimension=2)
        kb_all = k_barcode(filt)
        kb_dim1 = k_barcode(filt, max_dimension=1)
        assert all(p.dimension <= 1 for p in kb_dim1.all_pairs)
        assert len(kb_dim1.all_pairs) <= len(kb_all.all_pairs)

    def test_circle_k0_betti_starts_at_8(self) -> None:
        kb = self._circle_barcode()
        # At scale 0, 8 isolated points → 8 active K⁰ bars from H₀
        assert kb.k0_betti_at(0.0) == 8

    def test_kbarcode_is_frozen(self) -> None:
        kb = self._circle_barcode()
        with pytest.raises((AttributeError, TypeError)):
            kb.k0_pairs = ()  # type: ignore[misc]
