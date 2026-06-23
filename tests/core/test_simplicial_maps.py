"""Tests for P7.2 — simplicial_maps module.

Covers:
  SimplicialMap      : construction, validation, error cases
  chain_map_matrix   : identity, inclusion, constant, sign
  induced_map_on_homology : known H_k results on S¹, D², S², trivial cases
  cone_complex       : contractibility, vertex count, error
  suspension_complex : Σ(S⁰)≃S¹, Σ(S¹)≃S², errors
"""

from __future__ import annotations

import pytest

from pytop.homology import simplicial_homology
from pytop.simplices import Simplex
from pytop.simplicial_complexes import SimplicialComplex
from pytop.simplicial_maps import (
    InducedHomologyMap,
    SimplicialMap,
    SimplicialMapError,
    chain_map_matrix,
    cone_complex,
    induced_map_on_homology,
    suspension_complex,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_circle() -> SimplicialComplex:
    """Boundary of triangle = S¹ triangulation (3 vertices, 3 edges)."""
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
    ])


def _make_disk() -> SimplicialComplex:
    """Filled triangle = D² (3 vertices, 3 edges, 1 triangle)."""
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        Simplex([0, 1, 2]),
    ])


def _make_two_points() -> SimplicialComplex:
    """S⁰ = two disjoint points {0} and {1}."""
    return SimplicialComplex([Simplex([0]), Simplex([1])])


def _make_point() -> SimplicialComplex:
    return SimplicialComplex([Simplex([0])])


def _identity_map(K: SimplicialComplex) -> SimplicialMap:
    return SimplicialMap(K, K, {v: v for v in K.vertices})


# ---------------------------------------------------------------------------
# SimplicialMap — construction & validation
# ---------------------------------------------------------------------------

class TestSimplicialMap:
    def test_identity_map_valid(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        assert f.domain is K
        assert f.codomain is K

    def test_inclusion_valid(self) -> None:
        circle = _make_circle()
        disk = _make_disk()
        vm = {0: 0, 1: 1, 2: 2}
        f = SimplicialMap(circle, disk, vm)
        assert f.vertex_map == vm

    def test_constant_map_to_point_valid(self) -> None:
        circle = _make_circle()
        pt = _make_point()
        vm = {0: 0, 1: 0, 2: 0}
        f = SimplicialMap(circle, pt, vm)
        assert all(v == 0 for v in f.vertex_map.values())

    def test_error_missing_vertex(self) -> None:
        K = _make_circle()
        with pytest.raises(SimplicialMapError, match="has no entry"):
            SimplicialMap(K, K, {0: 0, 1: 1})  # vertex 2 missing

    def test_error_image_not_in_codomain(self) -> None:
        circle = _make_circle()
        with pytest.raises(SimplicialMapError, match="not a vertex"):
            SimplicialMap(circle, circle, {0: 0, 1: 1, 2: 99})

    def test_error_simplex_not_mapped_to_simplex(self) -> None:
        # Map edge {0,1} to {0,2} which is in codomain, but edge {0,2}→{0,2}
        # OK; however if we map {0,1}→{0} and {0,2}→{0,2} but target
        # edge {1,2} goes to {0,1} which must be in codomain.
        # Simpler: K has edge {0,1}, L has only isolated vertices 0,1 — no edge.
        K = SimplicialComplex([Simplex([0]), Simplex([1]), Simplex([0, 1])])
        L = SimplicialComplex([Simplex([0]), Simplex([1])])
        with pytest.raises(SimplicialMapError, match="not a simplex"):
            SimplicialMap(K, L, {0: 0, 1: 1})

    def test_collapsing_map_valid(self) -> None:
        # Collapse an edge: map both endpoints to the same vertex.
        # Image of edge {0,1} = {0,0} → just {0}, which is a 0-simplex in L.
        K = SimplicialComplex([
            Simplex([0]), Simplex([1]), Simplex([2]),
            Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        ])
        L = SimplicialComplex([
            Simplex([0]), Simplex([2]),
            Simplex([0, 2]),
        ])
        vm = {0: 0, 1: 0, 2: 2}
        f = SimplicialMap(K, L, vm)
        assert f.vertex_map[1] == 0


# ---------------------------------------------------------------------------
# chain_map_matrix
# ---------------------------------------------------------------------------

class TestChainMapMatrix:
    def test_identity_degree_0(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        M = chain_map_matrix(f, 0)
        assert len(M) == 3
        assert len(M[0]) == 3
        assert all(M[i][i] == 1 for i in range(3))
        assert sum(abs(M[i][j]) for i in range(3) for j in range(3)) == 3

    def test_identity_degree_1(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        M = chain_map_matrix(f, 1)
        assert len(M) == 3 and len(M[0]) == 3
        assert all(M[i][i] == 1 for i in range(3))
        assert sum(abs(M[i][j]) for i in range(3) for j in range(3)) == 3

    def test_identity_degree_2(self) -> None:
        disk = _make_disk()
        f = _identity_map(disk)
        M = chain_map_matrix(f, 2)
        assert M == [[1]]

    def test_inclusion_degree_1(self) -> None:
        circle = _make_circle()
        disk = _make_disk()
        f = SimplicialMap(circle, disk, {0: 0, 1: 1, 2: 2})
        M = chain_map_matrix(f, 1)
        # 3 edges in circle, 3 edges in disk — inclusion is ±identity
        assert len(M) == 3 and len(M[0]) == 3
        # Every column has exactly one nonzero ±1 entry
        for col in range(3):
            col_vals = [M[row][col] for row in range(3)]
            assert sum(abs(v) for v in col_vals) == 1

    def test_constant_map_degree_0(self) -> None:
        circle = _make_circle()
        pt = _make_point()
        f = SimplicialMap(circle, pt, {0: 0, 1: 0, 2: 0})
        M = chain_map_matrix(f, 0)
        # 1 row (codomain vertex), 3 cols (domain vertices) — all ones
        assert M == [[1, 1, 1]]

    def test_constant_map_degree_1_zero(self) -> None:
        circle = _make_circle()
        pt = _make_point()
        f = SimplicialMap(circle, pt, {0: 0, 1: 0, 2: 0})
        M = chain_map_matrix(f, 1)
        # No 1-simplices in codomain → zero matrix (0 rows, 3 cols)
        assert len(M) == 0

    def test_transposition_sign(self) -> None:
        # Map 0↦1, 1↦0, 2↦2 on the circle — swaps edge {0,1}→{0,1} with sign -1.
        K = _make_circle()
        f = SimplicialMap(K, K, {0: 1, 1: 0, 2: 2})
        M = chain_map_matrix(f, 1)
        # The simplices (0,1),(0,2),(1,2) map to (0,1) with -1, (1,2) with sign, (0,2) with -1
        # edge (0,1) → (1,0) = -(0,1): sign -1
        from pytop.homology import _simplices_of_dimension
        simp = _simplices_of_dimension(K, 1)
        edge_01 = simp.index((0, 1))
        col = [M[row][edge_01] for row in range(len(M))]
        # The column for (0,1) should be -1 in the row for (0,1)
        assert col[edge_01] == -1

    def test_negative_degree_empty(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        M = chain_map_matrix(f, -1)
        assert M == []

    def test_degree_too_high_empty(self) -> None:
        circle = _make_circle()
        f = _identity_map(circle)
        M = chain_map_matrix(f, 5)
        # No 5-simplices in either complex
        assert all(v == 0 for row in M for v in row) or len(M) == 0


# ---------------------------------------------------------------------------
# induced_map_on_homology
# ---------------------------------------------------------------------------

class TestInducedMapOnHomology:
    def test_identity_circle_h1(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        r = induced_map_on_homology(f, 1)
        assert isinstance(r, InducedHomologyMap)
        assert r.degree == 1
        assert r.domain_homology.betti == 1
        assert r.codomain_homology.betti == 1
        assert r.matrix == [[1]]

    def test_identity_circle_h0(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        r = induced_map_on_homology(f, 0)
        assert r.domain_homology.betti == 1
        assert r.matrix == [[1]]

    def test_inclusion_h1_zero(self) -> None:
        circle = _make_circle()
        disk = _make_disk()
        f = SimplicialMap(circle, disk, {0: 0, 1: 1, 2: 2})
        r = induced_map_on_homology(f, 1)
        # H_1(S¹) = Z, H_1(D²) = 0  → induced map has no codomain generators
        assert r.domain_homology.betti == 1
        assert r.codomain_homology.betti == 0
        assert r.matrix == []

    def test_constant_map_h1_trivial(self) -> None:
        circle = _make_circle()
        pt = _make_point()
        f = SimplicialMap(circle, pt, {0: 0, 1: 0, 2: 0})
        r = induced_map_on_homology(f, 1)
        assert r.codomain_homology.betti == 0
        assert r.matrix == []

    def test_inclusion_h0(self) -> None:
        circle = _make_circle()
        disk = _make_disk()
        f = SimplicialMap(circle, disk, {0: 0, 1: 1, 2: 2})
        r = induced_map_on_homology(f, 0)
        assert r.domain_homology.betti == 1
        assert r.codomain_homology.betti == 1
        assert r.matrix == [[1]]

    def test_identity_disk_h1(self) -> None:
        disk = _make_disk()
        f = _identity_map(disk)
        r = induced_map_on_homology(f, 1)
        assert r.domain_homology.betti == 0
        assert r.codomain_homology.betti == 0

    def test_identity_point_h0(self) -> None:
        pt = _make_point()
        f = _identity_map(pt)
        r = induced_map_on_homology(f, 0)
        assert r.matrix == [[1]]

    def test_returns_induced_homology_map_type(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        r = induced_map_on_homology(f, 1)
        assert isinstance(r.domain_homology.torsion, tuple)
        assert isinstance(r.chain_matrix, list)

    def test_chain_matrix_shape(self) -> None:
        circle = _make_circle()
        disk = _make_disk()
        f = SimplicialMap(circle, disk, {0: 0, 1: 1, 2: 2})
        r = induced_map_on_homology(f, 1)
        assert len(r.chain_matrix) == 3        # 3 edges in disk
        assert len(r.chain_matrix[0]) == 3    # 3 edges in circle

    def test_high_degree_trivial(self) -> None:
        K = _make_circle()
        f = _identity_map(K)
        r = induced_map_on_homology(f, 5)
        assert r.domain_homology.betti == 0
        assert r.codomain_homology.betti == 0


# ---------------------------------------------------------------------------
# cone_complex
# ---------------------------------------------------------------------------

class TestConeComplex:
    def test_cone_of_point_is_segment(self) -> None:
        pt = _make_point()
        CK = cone_complex(pt)
        # Should have vertices {0, c} and edge {0, c}
        verts = CK.vertices
        assert "c" in verts
        assert 0 in verts
        assert any(len(s.vertices) == 2 for s in CK.simplexes)

    def test_cone_of_circle_contractible_h0(self) -> None:
        circle = _make_circle()
        CK = cone_complex(circle)
        h0 = simplicial_homology(CK, 0)
        assert h0.betti == 1

    def test_cone_of_circle_contractible_h1(self) -> None:
        circle = _make_circle()
        CK = cone_complex(circle)
        h1 = simplicial_homology(CK, 1)
        assert h1.betti == 0
        assert h1.torsion == ()

    def test_cone_adds_one_apex(self) -> None:
        circle = _make_circle()
        n_before = len(circle.vertices)
        CK = cone_complex(circle)
        assert len(CK.vertices) == n_before + 1

    def test_cone_custom_apex(self) -> None:
        circle = _make_circle()
        CK = cone_complex(circle, apex=99)
        assert 99 in CK.vertices

    def test_cone_error_apex_exists(self) -> None:
        circle = _make_circle()
        with pytest.raises(ValueError, match="already a vertex"):
            cone_complex(circle, apex=0)

    def test_cone_of_two_points_connected(self) -> None:
        K = _make_two_points()
        CK = cone_complex(K)
        assert simplicial_homology(CK, 0).betti == 1
        assert simplicial_homology(CK, 1).betti == 0


# ---------------------------------------------------------------------------
# suspension_complex
# ---------------------------------------------------------------------------

class TestSuspensionComplex:
    def test_suspension_two_points_is_circle(self) -> None:
        # Σ(S⁰) ≃ S¹: H₀=Z, H₁=Z
        K = _make_two_points()
        SK = suspension_complex(K)
        assert simplicial_homology(SK, 0).betti == 1
        assert simplicial_homology(SK, 1).betti == 1
        assert simplicial_homology(SK, 1).torsion == ()

    def test_suspension_circle_is_sphere(self) -> None:
        # Σ(S¹) ≃ S²: H₀=Z, H₁=0, H₂=Z
        circle = _make_circle()
        SK = suspension_complex(circle)
        assert simplicial_homology(SK, 0).betti == 1
        assert simplicial_homology(SK, 1).betti == 0
        assert simplicial_homology(SK, 2).betti == 1
        assert simplicial_homology(SK, 2).torsion == ()

    def test_suspension_adds_two_vertices(self) -> None:
        K = _make_circle()
        n_before = len(K.vertices)
        SK = suspension_complex(K)
        assert len(SK.vertices) == n_before + 2

    def test_suspension_custom_poles(self) -> None:
        K = _make_two_points()
        SK = suspension_complex(K, south=10, north=20)
        assert 10 in SK.vertices
        assert 20 in SK.vertices

    def test_suspension_error_south_exists(self) -> None:
        K = _make_circle()
        with pytest.raises(ValueError, match="south vertex.*already"):
            suspension_complex(K, south=0)

    def test_suspension_error_north_exists(self) -> None:
        K = _make_circle()
        with pytest.raises(ValueError, match="north vertex.*already"):
            suspension_complex(K, north=1)

    def test_suspension_error_poles_equal(self) -> None:
        K = _make_circle()
        with pytest.raises(ValueError, match="distinct"):
            suspension_complex(K, south="x", north="x")

    def test_suspension_point_is_segment(self) -> None:
        # Σ(point) = segment [s, n]: H₀=Z, H₁=0
        pt = _make_point()
        SK = suspension_complex(pt)
        assert simplicial_homology(SK, 0).betti == 1
        assert simplicial_homology(SK, 1).betti == 0

    def test_suspension_face_closed(self) -> None:
        circle = _make_circle()
        SK = suspension_complex(circle)
        from pytop.simplicial_complexes import face_closure_diagnostic
        diag = face_closure_diagnostic(SK.simplexes)
        assert diag.is_face_closed
