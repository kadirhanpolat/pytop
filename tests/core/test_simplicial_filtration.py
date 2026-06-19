"""Tests for simplicial_filtration.py — static complexes and standard triangulations."""

from __future__ import annotations

from pytop.persistent_homology import FilteredComplex, persistence_pairs
from pytop.persistent_homology_fp import persistence_pairs_fp
from pytop.simplicial_filtration import (
    klein_bottle_filtration,
    rp2_filtration,
    simplicial_filtration,
    torus_filtration,
)

# ---------------------------------------------------------------------------
# simplicial_filtration — generic builder
# ---------------------------------------------------------------------------


class TestSimplicialFiltration:
    def test_single_triangle_size_7(self) -> None:
        # Triangle {0,1,2}: 3 vertices + 3 edges + 1 face = 7
        fc = simplicial_filtration([(0, 1, 2)])
        assert fc.size() == 7

    def test_single_edge_size_3(self) -> None:
        fc = simplicial_filtration([(0, 1)])
        assert fc.size() == 3  # 2 vertices + 1 edge

    def test_single_vertex_size_1(self) -> None:
        fc = simplicial_filtration([(0,)])
        assert fc.size() == 1

    def test_all_births_zero(self) -> None:
        fc = simplicial_filtration([(0, 1, 2)])
        assert all(b == 0.0 for b in fc.births)

    def test_faces_before_cofaces(self) -> None:
        # Triangle: all edges must appear before the triangle
        fc = simplicial_filtration([(0, 1, 2)])
        simplex_idx = {s: i for i, s in enumerate(fc.simplices)}
        tri = (0, 1, 2)
        for edge in [(0, 1), (0, 2), (1, 2)]:
            assert simplex_idx[edge] < simplex_idx[tri]

    def test_returns_filtered_complex(self) -> None:
        fc = simplicial_filtration([(0, 1, 2)])
        assert isinstance(fc, FilteredComplex)

    def test_multiple_maximal_simplices(self) -> None:
        # Two disjoint edges: {0,1} and {2,3}
        fc = simplicial_filtration([(0, 1), (2, 3)])
        assert fc.size() == 6  # 4 vertices + 2 edges

    def test_face_closure_completeness(self) -> None:
        # Give only tetrahedron; all faces should appear
        fc = simplicial_filtration([(0, 1, 2, 3)])
        dim_counts = {d: 0 for d in range(4)}
        for d in fc.dimensions:
            dim_counts[d] += 1
        assert dim_counts[0] == 4   # vertices
        assert dim_counts[1] == 6   # edges
        assert dim_counts[2] == 4   # faces
        assert dim_counts[3] == 1   # tetrahedron

    def test_duplicate_faces_collapsed(self) -> None:
        # Two triangles sharing an edge
        fc = simplicial_filtration([(0, 1, 2), (0, 1, 3)])
        assert (0, 1) in fc.simplices  # shared edge appears once
        edge_count = sum(1 for d in fc.dimensions if d == 1)
        assert edge_count == 5  # (0,1),(0,2),(1,2),(0,3),(1,3)

    def test_contractible_no_h1(self) -> None:
        # Filled tetrahedron: contractible, no H_1
        fc = simplicial_filtration([(0, 1, 2, 3)])
        pairs = persistence_pairs(fc)
        h1 = [p for p in pairs if p.dimension == 1]
        assert all(not p.is_essential for p in h1)

    def test_sorted_by_dimension_then_lex(self) -> None:
        fc = simplicial_filtration([(0, 1, 2)])
        dims = list(fc.dimensions)
        for i in range(len(dims) - 1):
            assert dims[i] <= dims[i + 1]


# ---------------------------------------------------------------------------
# torus_filtration
# ---------------------------------------------------------------------------


class TestTorusFiltration:
    def test_simplex_counts(self) -> None:
        fc = torus_filtration()
        dim_counts = {d: list(fc.dimensions).count(d) for d in range(3)}
        assert dim_counts[0] == 9    # 9 vertices
        assert dim_counts[1] == 27   # 27 edges
        assert dim_counts[2] == 18   # 18 triangles

    def test_euler_characteristic(self) -> None:
        fc = torus_filtration()
        dims = fc.dimensions
        chi = dims.count(0) - dims.count(1) + dims.count(2)
        assert chi == 0  # T² has χ = 0

    def test_betti_numbers_prime_2(self) -> None:
        fc = torus_filtration()
        pairs = persistence_pairs_fp(fc, prime=2)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1  # β_0 = 1
        assert sum(1 for p in ess if p.dimension == 1) == 2  # β_1 = 2
        assert sum(1 for p in ess if p.dimension == 2) == 1  # β_2 = 1

    def test_betti_numbers_prime_3(self) -> None:
        fc = torus_filtration()
        pairs = persistence_pairs_fp(fc, prime=3)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1
        assert sum(1 for p in ess if p.dimension == 1) == 2
        assert sum(1 for p in ess if p.dimension == 2) == 1

    def test_betti_numbers_prime_5(self) -> None:
        fc = torus_filtration()
        pairs = persistence_pairs_fp(fc, prime=5)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1
        assert sum(1 for p in ess if p.dimension == 1) == 2
        assert sum(1 for p in ess if p.dimension == 2) == 1

    def test_torsion_free_all_primes_agree(self) -> None:
        # T² has no torsion: Betti numbers same for all primes
        fc = torus_filtration()
        results: dict[int, tuple[int, int, int]] = {}
        for p in [2, 3, 5, 7]:
            pairs = persistence_pairs_fp(fc, prime=p)
            ess = [pp for pp in pairs if pp.is_essential]
            results[p] = (
                sum(1 for pp in ess if pp.dimension == 0),
                sum(1 for pp in ess if pp.dimension == 1),
                sum(1 for pp in ess if pp.dimension == 2),
            )
        values = list(results.values())
        assert all(v == values[0] for v in values), f"Differ: {results}"

    def test_total_essential_count(self) -> None:
        fc = torus_filtration()
        pairs = persistence_pairs_fp(fc, prime=2)
        ess = [p for p in pairs if p.is_essential]
        assert len(ess) == 4  # β_0 + β_1 + β_2 = 1 + 2 + 1


# ---------------------------------------------------------------------------
# klein_bottle_filtration
# ---------------------------------------------------------------------------


class TestKleinBottleFiltration:
    def test_simplex_counts(self) -> None:
        fc = klein_bottle_filtration()
        dim_counts = {d: list(fc.dimensions).count(d) for d in range(3)}
        assert dim_counts[0] == 9
        assert dim_counts[2] == 18  # 18 triangles

    def test_euler_characteristic(self) -> None:
        fc = klein_bottle_filtration()
        dims = fc.dimensions
        chi = dims.count(0) - dims.count(1) + dims.count(2)
        assert chi == 0  # Klein bottle has χ = 0

    def test_betti_numbers_prime_2(self) -> None:
        # Over F_2: H_*(K; F_2) = (F_2, F_2², F_2) by UCT
        # β_0=1, β_1=2, β_2=1
        fc = klein_bottle_filtration()
        pairs = persistence_pairs_fp(fc, prime=2)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1
        assert sum(1 for p in ess if p.dimension == 1) == 2
        assert sum(1 for p in ess if p.dimension == 2) == 1

    def test_betti_numbers_prime_3(self) -> None:
        # Over F_3: H_*(K; F_3) = (F_3, F_3, 0) — Z/2 torsion invisible
        # β_0=1, β_1=1, β_2=0
        fc = klein_bottle_filtration()
        pairs = persistence_pairs_fp(fc, prime=3)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1
        assert sum(1 for p in ess if p.dimension == 1) == 1
        assert sum(1 for p in ess if p.dimension == 2) == 0

    def test_betti_numbers_prime_5(self) -> None:
        fc = klein_bottle_filtration()
        pairs = persistence_pairs_fp(fc, prime=5)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 1) == 1
        assert sum(1 for p in ess if p.dimension == 2) == 0

    def test_torsion_detection_h1(self) -> None:
        # The Z/2 torsion in H_1(K;Z) is detected: β_1 differs between F_2 and F_3
        fc = klein_bottle_filtration()
        b1_f2 = sum(1 for p in persistence_pairs_fp(fc, 2) if p.is_essential and p.dimension == 1)
        b1_f3 = sum(1 for p in persistence_pairs_fp(fc, 3) if p.is_essential and p.dimension == 1)
        assert b1_f2 == 2
        assert b1_f3 == 1
        assert b1_f2 != b1_f3, "Torsion should cause F_2 and F_3 β_1 to differ"

    def test_torsion_detection_h2(self) -> None:
        # β_2 also differs: UCT gives β_2=1 over F_2, β_2=0 over F_3
        fc = klein_bottle_filtration()
        b2_f2 = sum(1 for p in persistence_pairs_fp(fc, 2) if p.is_essential and p.dimension == 2)
        b2_f3 = sum(1 for p in persistence_pairs_fp(fc, 3) if p.is_essential and p.dimension == 2)
        assert b2_f2 == 1
        assert b2_f3 == 0


# ---------------------------------------------------------------------------
# rp2_filtration
# ---------------------------------------------------------------------------


class TestRP2Filtration:
    def test_simplex_counts(self) -> None:
        fc = rp2_filtration()
        dim_counts = {d: list(fc.dimensions).count(d) for d in range(3)}
        assert dim_counts[0] == 6    # 6 vertices
        assert dim_counts[1] == 15   # 15 edges
        assert dim_counts[2] == 10   # 10 triangles

    def test_euler_characteristic(self) -> None:
        fc = rp2_filtration()
        dims = fc.dimensions
        chi = dims.count(0) - dims.count(1) + dims.count(2)
        assert chi == 1  # RP² has χ = 1

    def test_betti_numbers_prime_2(self) -> None:
        # Over F_2: H_*(RP²; F_2) = (F_2, F_2, F_2) by UCT
        # β_0=1, β_1=1, β_2=1
        fc = rp2_filtration()
        pairs = persistence_pairs_fp(fc, prime=2)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1
        assert sum(1 for p in ess if p.dimension == 1) == 1
        assert sum(1 for p in ess if p.dimension == 2) == 1

    def test_betti_numbers_prime_3(self) -> None:
        # Over F_3: H_*(RP²; F_3) = (F_3, 0, 0) — Z/2 torsion invisible
        fc = rp2_filtration()
        pairs = persistence_pairs_fp(fc, prime=3)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 0) == 1
        assert sum(1 for p in ess if p.dimension == 1) == 0
        assert sum(1 for p in ess if p.dimension == 2) == 0

    def test_betti_numbers_prime_5(self) -> None:
        fc = rp2_filtration()
        pairs = persistence_pairs_fp(fc, prime=5)
        ess = [p for p in pairs if p.is_essential]
        assert sum(1 for p in ess if p.dimension == 1) == 0

    def test_torsion_detection_h1(self) -> None:
        # Z/2 torsion: β_1 = 1 over F_2, β_1 = 0 over F_3
        fc = rp2_filtration()
        b1_f2 = sum(1 for p in persistence_pairs_fp(fc, 2) if p.is_essential and p.dimension == 1)
        b1_f3 = sum(1 for p in persistence_pairs_fp(fc, 3) if p.is_essential and p.dimension == 1)
        assert b1_f2 == 1
        assert b1_f3 == 0
        assert b1_f2 != b1_f3, "Z/2 torsion must be detected"

    def test_all_births_zero(self) -> None:
        fc = rp2_filtration()
        assert all(b == 0.0 for b in fc.births)

    def test_total_simplices(self) -> None:
        fc = rp2_filtration()
        assert fc.size() == 31  # 6 + 15 + 10
