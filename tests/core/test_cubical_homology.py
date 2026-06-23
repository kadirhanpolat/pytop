"""Tests for pytop.cubical_homology."""

from __future__ import annotations

import math

import pytest

from pytop.cubical_homology import (
    Cube,
    CubicalComplex,
    CubicalFiltration,
    bitmap_to_cubical_filtration,
    circle_cubical,
    cube_dim,
    cube_faces_signed,
    cube_faces_z2,
    cubical_boundary_matrix,
    cubical_homology,
    disk_cubical,
    interval_complex,
    make_cubical_complex,
    persistence_pairs_cubical,
    persistent_homology_bitmap,
    sphere_cubical_1d,
)
from pytop.homology import HomologyResult
from pytop.metric_spaces import FiniteMetricSpace
from pytop.persistent_homology import (
    FilteredComplex,
    PersistencePair,
    vietoris_rips_filtration,
)
from pytop.persistent_homology_optimized import persistence_pairs_twist_with_stats

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mat_mul(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """Integer matrix product A @ B."""
    if not A or not A[0] or not B or not B[0]:
        rows = len(A)
        cols = len(B[0]) if B and B[0] else 0
        return [[0] * cols for _ in range(rows)]
    rows, mid, cols = len(A), len(B), len(B[0])
    return [
        [sum(A[i][k] * B[k][j] for k in range(mid)) for j in range(cols)]
        for i in range(rows)
    ]


def _is_zero_matrix(M: list[list[int]]) -> bool:
    return all(v == 0 for row in M for v in row)


def _metric_space(points):
    return FiniteMetricSpace(carrier=tuple(points), distance=math.dist)


def _circle_points(n):
    return [
        (math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]


# ---------------------------------------------------------------------------
# cube_dim
# ---------------------------------------------------------------------------

class TestCubeDim:
    def test_vertex_0d(self):
        assert cube_dim(((0, 0),)) == 0

    def test_edge_1d(self):
        assert cube_dim(((0, 1),)) == 1

    def test_vertex_2d_embedding(self):
        assert cube_dim(((2, 2), (3, 3))) == 0

    def test_horizontal_edge_in_2d(self):
        assert cube_dim(((0, 1), (0, 0))) == 1

    def test_vertical_edge_in_2d(self):
        assert cube_dim(((0, 0), (0, 1))) == 1

    def test_square_2d(self):
        assert cube_dim(((0, 1), (0, 1))) == 2

    def test_cube_3d(self):
        assert cube_dim(((0, 1), (0, 1), (0, 1))) == 3

    def test_mixed_degenerate_nondegenerate(self):
        assert cube_dim(((0, 0), (0, 1), (2, 2))) == 1

    def test_all_degenerate(self):
        assert cube_dim(((5, 5), (3, 3), (1, 1))) == 0


# ---------------------------------------------------------------------------
# cube_faces_z2
# ---------------------------------------------------------------------------

class TestCubeFacesZ2:
    def test_vertex_has_no_faces(self):
        assert cube_faces_z2(((0, 0),)) == []

    def test_edge_has_two_endpoints(self):
        faces = cube_faces_z2(((0, 1),))
        assert sorted(faces) == sorted([((0, 0),), ((1, 1),)])

    def test_square_has_four_edges(self):
        faces = cube_faces_z2(((0, 1), (0, 1)))
        assert len(faces) == 4

    def test_square_faces_are_distinct(self):
        faces = cube_faces_z2(((0, 1), (0, 1)))
        assert len(set(faces)) == 4

    def test_square_faces_are_edges(self):
        faces = cube_faces_z2(((0, 1), (0, 1)))
        assert all(cube_dim(f) == 1 for f in faces)

    def test_square_faces_correct(self):
        faces = set(cube_faces_z2(((0, 1), (0, 1))))
        expected = {
            ((1, 1), (0, 1)),  # right vertical edge
            ((0, 0), (0, 1)),  # left vertical edge
            ((0, 1), (1, 1)),  # top horizontal edge
            ((0, 1), (0, 0)),  # bottom horizontal edge
        }
        assert faces == expected

    def test_3d_cube_has_six_faces(self):
        cube: Cube = ((0, 1), (0, 1), (0, 1))
        faces = cube_faces_z2(cube)
        assert len(faces) == 6
        assert all(cube_dim(f) == 2 for f in faces)


# ---------------------------------------------------------------------------
# cube_faces_signed — boundary squared = 0
# ---------------------------------------------------------------------------

class TestCubeFacesSigned:
    def test_vertex_no_faces(self):
        assert cube_faces_signed(((0, 0),)) == []

    def test_edge_signs(self):
        faces = cube_faces_signed(((0, 1),))
        coeffs_cubes = {c: coeff for coeff, c in faces}
        # ∂[0,1] = [1,1] - [0,0]
        assert coeffs_cubes.get(((1, 1),)) == 1
        assert coeffs_cubes.get(((0, 0),)) == -1

    def test_signs_sum_correctly_for_square(self):
        # For a 2-cube, the boundary has 4 faces with signs ±1.
        faces = cube_faces_signed(((0, 1), (0, 1)))
        coeffs = [c for c, _ in faces]
        assert all(c in (1, -1) for c in coeffs)
        assert sum(coeffs) == 0  # balanced cancellation

    def test_boundary_squared_zero_1d(self):
        # ∂∂[0,1] = ∂([1,1] - [0,0]) = 0 (vertices have no faces)
        chain: dict[Cube, int] = {}
        for coeff, face in cube_faces_signed(((0, 1),)):
            for c2, f2 in cube_faces_signed(face):
                chain[f2] = chain.get(f2, 0) + coeff * c2
        assert all(v == 0 for v in chain.values())

    def test_boundary_squared_zero_2d(self):
        chain: dict[Cube, int] = {}
        for coeff, face in cube_faces_signed(((0, 1), (0, 1))):
            for c2, f2 in cube_faces_signed(face):
                chain[f2] = chain.get(f2, 0) + coeff * c2
        assert all(v == 0 for v in chain.values())

    def test_boundary_squared_zero_3d(self):
        chain: dict[Cube, int] = {}
        for coeff, face in cube_faces_signed(((0, 1), (0, 1), (0, 1))):
            for c2, f2 in cube_faces_signed(face):
                chain[f2] = chain.get(f2, 0) + coeff * c2
        assert all(v == 0 for v in chain.values())


# ---------------------------------------------------------------------------
# make_cubical_complex
# ---------------------------------------------------------------------------

class TestMakeCubicalComplex:
    def test_single_vertex(self):
        cx = make_cubical_complex([((0, 0),)])
        assert len(cx.cubes) == 1
        assert cx.dimension == 0

    def test_single_edge_closure(self):
        cx = make_cubical_complex([((0, 1),)])
        # closure: edge + two vertices = 3
        assert len(cx.cubes) == 3
        assert cx.dimension == 1

    def test_unit_square_closure(self):
        cx = make_cubical_complex([((0, 1), (0, 1))])
        # 1 square + 4 edges + 4 vertices = 9
        assert len(cx.cubes) == 9
        assert cx.dimension == 2

    def test_empty_input(self):
        cx = make_cubical_complex([])
        assert len(cx.cubes) == 0
        assert cx.dimension == -1

    def test_two_edges_sharing_vertex(self):
        cx = make_cubical_complex([((0, 1),), ((1, 2),)])
        # edges: (0,1), (1,2); vertices: (0,), (1,), (2,) → 5 total
        assert len(cx.cubes) == 5


# ---------------------------------------------------------------------------
# cubical_boundary_matrix — ∂² = 0
# ---------------------------------------------------------------------------

class TestCubicalBoundaryMatrix:
    def _check_boundary_sq_zero(self, cx: CubicalComplex, k: int) -> None:
        dk = cubical_boundary_matrix(cx, k)
        dk1 = cubical_boundary_matrix(cx, k + 1)
        if not dk or not dk[0] or not dk1 or not dk1[0]:
            return
        product = _mat_mul(dk, dk1)
        assert _is_zero_matrix(product), f"∂_{k} ∘ ∂_{k+1} ≠ 0"

    def test_boundary_sq_zero_circle_k0(self):
        self._check_boundary_sq_zero(circle_cubical(4), 0)

    def test_boundary_sq_zero_circle_k1(self):
        self._check_boundary_sq_zero(circle_cubical(4), 1)

    def test_boundary_sq_zero_disk_k0(self):
        self._check_boundary_sq_zero(disk_cubical(), 0)

    def test_boundary_sq_zero_disk_k1(self):
        self._check_boundary_sq_zero(disk_cubical(), 1)

    def test_boundary_matrix_dimensions_circle(self):
        cx = circle_cubical(4)
        # 4 vertices, 4 edges
        d0 = cubical_boundary_matrix(cx, 0)
        d1 = cubical_boundary_matrix(cx, 1)
        # d0 maps into C_{-1} = 0 → no rows
        assert d0 == []
        # d1: rows = #vertices = 4, cols = #edges = 4
        assert len(d1) == 4
        assert len(d1[0]) == 4

    def test_boundary_matrix_dimensions_disk(self):
        cx = disk_cubical()
        d2 = cubical_boundary_matrix(cx, 2)
        # 4 edges, 1 square → rows=4, cols=1
        assert len(d2) == 4
        assert len(d2[0]) == 1

    def test_k_beyond_dimension_empty(self):
        cx = circle_cubical(4)
        d3 = cubical_boundary_matrix(cx, 3)
        assert d3 == [] or all(len(row) == 0 for row in d3)


# ---------------------------------------------------------------------------
# cubical_homology — known answers
# ---------------------------------------------------------------------------

class TestCubicalHomology:
    def _h(self, cx: CubicalComplex, k: int) -> HomologyResult:
        groups = cubical_homology(cx)
        return groups[k]

    def test_circle_h0(self):
        assert self._h(circle_cubical(4), 0).describe() == "Z"

    def test_circle_h1(self):
        assert self._h(circle_cubical(4), 1).describe() == "Z"

    def test_circle_no_torsion(self):
        h1 = self._h(circle_cubical(4), 1)
        assert h1.torsion == ()

    def test_disk_h0(self):
        assert self._h(disk_cubical(), 0).describe() == "Z"

    def test_disk_h1_zero(self):
        assert self._h(disk_cubical(), 1).describe() == "0"

    def test_disk_h2_zero(self):
        assert self._h(disk_cubical(), 2).describe() == "0"

    def test_interval_h0(self):
        assert self._h(interval_complex(3), 0).describe() == "Z"

    def test_interval_h1_zero(self):
        assert self._h(interval_complex(3), 1).describe() == "0"

    def test_single_vertex_h0(self):
        cx = make_cubical_complex([((0, 0), (0, 0))])
        groups = cubical_homology(cx)
        assert groups[0].describe() == "Z"

    def test_two_disjoint_vertices_h0(self):
        cx = make_cubical_complex([((0, 0), (0, 0)), ((5, 5), (5, 5))])
        groups = cubical_homology(cx)
        assert groups[0].betti == 2

    def test_two_disjoint_circles_h0(self):
        c1 = circle_cubical(4)
        shifted: list[Cube] = [tuple((a + 10, b + 10) for a, b in cube) for cube in c1.cubes]  # type: ignore[arg-type]
        c2 = make_cubical_complex(shifted)
        cx = CubicalComplex(c1.cubes | c2.cubes)
        groups = cubical_homology(cx)
        assert groups[0].betti == 2
        assert groups[1].betti == 2

    def test_circle_n6_h1(self):
        cx = circle_cubical(6)
        groups = cubical_homology(cx)
        assert groups[1].describe() == "Z"

    def test_empty_complex(self):
        cx = CubicalComplex(frozenset())
        assert cubical_homology(cx) == ()

    def test_sphere_cubical_1d_alias(self):
        cx = sphere_cubical_1d()
        groups = cubical_homology(cx)
        assert groups[1].describe() == "Z"

    def test_degrees_match_dimension(self):
        cx = disk_cubical()
        groups = cubical_homology(cx)
        assert len(groups) == cx.dimension + 1
        for i, g in enumerate(groups):
            assert g.degree == i

    def test_euler_characteristic_circle(self):
        cx = circle_cubical(4)
        chi = cx.euler_characteristic()
        betti_sum = sum((-1) ** g.degree * g.betti for g in cubical_homology(cx))
        assert chi == betti_sum == 0

    def test_euler_characteristic_disk(self):
        cx = disk_cubical()
        chi = cx.euler_characteristic()
        betti_sum = sum((-1) ** g.degree * g.betti for g in cubical_homology(cx))
        assert chi == betti_sum == 1


# ---------------------------------------------------------------------------
# bitmap_to_cubical_filtration
# ---------------------------------------------------------------------------

class TestBitmapToCubicalFiltration:
    def test_1x1_image_cube_count(self):
        f = bitmap_to_cubical_filtration([[0.0]])
        # 4 vertices + 2 H-edges + 2 V-edges + 1 pixel = 9
        assert f.size() == 9

    def test_2x2_image_cube_count(self):
        f = bitmap_to_cubical_filtration([[0.0, 1.0], [1.0, 0.0]])
        # 9 vertices + 6 H-edges + 6 V-edges + 4 pixels = 25
        assert f.size() == 25

    def test_mxn_cube_count(self):
        m, n = 3, 4
        f = bitmap_to_cubical_filtration([[0.0] * n for _ in range(m)])
        # vertices: (m+1)(n+1), H-edges: m(n+1), V-edges: (m+1)n, pixels: mn
        expected = (m + 1) * (n + 1) + m * (n + 1) + (m + 1) * n + m * n
        assert f.size() == expected

    def test_filtration_valid_faces_before_cofaces(self):
        # For every cube in the filtration, all its faces must appear earlier.
        img = [[1.0, 3.0], [2.0, 4.0]]
        f = bitmap_to_cubical_filtration(img)
        index_of = {c: i for i, c in enumerate(f.cubes)}
        for idx, cube in enumerate(f.cubes):
            for face in cube_faces_z2(cube):
                assert index_of[face] < idx or f.births[index_of[face]] <= f.births[idx]

    def test_1x1_pixel_birth(self):
        f = bitmap_to_cubical_filtration([[7.0]])
        pixel: Cube = ((0, 1), (0, 1))
        idx = list(f.cubes).index(pixel)
        assert f.births[idx] == pytest.approx(7.0)

    def test_births_nondecreasing(self):
        f = bitmap_to_cubical_filtration([[1.0, 5.0, 2.0], [3.0, 4.0, 0.0]])
        for i in range(f.size() - 1):
            assert f.births[i] <= f.births[i + 1]

    def test_dimensions_correct(self):
        f = bitmap_to_cubical_filtration([[0.0, 1.0], [2.0, 3.0]])
        for cube, dim in zip(f.cubes, f.dimensions):
            assert cube_dim(cube) == dim

    def test_empty_image_raises(self):
        with pytest.raises(ValueError):
            bitmap_to_cubical_filtration([])

    def test_empty_row_raises(self):
        with pytest.raises(ValueError):
            bitmap_to_cubical_filtration([[]])


# ---------------------------------------------------------------------------
# persistence_pairs_cubical and persistent_homology_bitmap
# ---------------------------------------------------------------------------

class TestCubicalPersistence:
    def test_1x1_essential_h0(self):
        pairs = persistent_homology_bitmap([[3.0]])
        essential = [p for p in pairs if p.is_essential]
        assert len(essential) == 1
        assert essential[0].dimension == 0
        assert essential[0].birth == pytest.approx(3.0)

    def test_1x1_no_h1(self):
        pairs = persistent_homology_bitmap([[3.0]])
        assert not any(p.dimension == 1 for p in pairs)

    def test_annular_h0_essential(self):
        img = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        pairs = persistent_homology_bitmap(img)
        h0_essential = [p for p in pairs if p.dimension == 0 and p.is_essential]
        assert len(h0_essential) == 1

    def test_annular_h1_finite_bar(self):
        img = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        pairs = persistent_homology_bitmap(img)
        h1 = [p for p in pairs if p.dimension == 1]
        assert len(h1) >= 1

    def test_annular_h1_bar_birth_death(self):
        img = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        pairs = persistent_homology_bitmap(img)
        h1 = [p for p in pairs if p.dimension == 1 and not p.is_essential]
        assert len(h1) >= 1
        bar = max(h1, key=lambda p: p.persistence)
        assert bar.birth == pytest.approx(0.0)
        assert bar.death == pytest.approx(1.0)

    def test_flat_image_no_h1(self):
        img = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        pairs = persistent_homology_bitmap(img)
        h1 = [p for p in pairs if p.dimension == 1]
        assert len(h1) == 0

    def test_uniform_image_one_essential_h0(self):
        img = [[5.0, 5.0], [5.0, 5.0]]
        pairs = persistent_homology_bitmap(img)
        h0_essential = [p for p in pairs if p.dimension == 0 and p.is_essential]
        assert len(h0_essential) == 1

    def test_two_components_h0(self):
        # 1×3 image with a large gap in the middle
        img = [[0.0, 100.0, 0.0]]
        pairs = persistent_homology_bitmap(img)
        h0 = [p for p in pairs if p.dimension == 0]
        essential = [p for p in h0 if p.is_essential]
        finite = [p for p in h0 if not p.is_essential]
        assert len(essential) == 1
        # The gap causes a finite H0 bar
        assert len(finite) >= 1
        assert max(p.death for p in finite) == pytest.approx(100.0)

    def test_sorted_output(self):
        img = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        pairs = persistent_homology_bitmap(img)
        keys = [(p.dimension, p.birth, p.death) for p in pairs]
        assert keys == sorted(keys)

    def test_returns_persistence_pairs(self):
        pairs = persistent_homology_bitmap([[1.0, 2.0], [3.0, 4.0]])
        assert isinstance(pairs, tuple)
        assert all(isinstance(p, PersistencePair) for p in pairs)

    def test_persistence_pairs_cubical_matches_bitmap(self):
        img = [[0.0, 1.0], [1.0, 0.0]]
        f = bitmap_to_cubical_filtration(img)
        pairs1 = persistence_pairs_cubical(f)
        pairs2 = persistent_homology_bitmap(img)
        assert pairs1 == pairs2

    def test_empty_filtration(self):
        f = CubicalFiltration(cubes=(), births=(), dimensions=())
        assert persistence_pairs_cubical(f) == ()

    def test_include_zero_persistence(self):
        img = [[0.0, 0.0], [0.0, 0.0]]
        p_with = persistent_homology_bitmap(img, include_zero_persistence=True)
        p_without = persistent_homology_bitmap(img, include_zero_persistence=False)
        assert len(p_with) >= len(p_without)

    def test_deeper_annulus_h1(self):
        # 5x5 image: border=0, inner ring=1, center=2
        img = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 2, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
        pairs = persistent_homology_bitmap(img)
        h1 = [p for p in pairs if p.dimension == 1 and not p.is_essential]
        assert len(h1) >= 1


# ---------------------------------------------------------------------------
# 1D cubical complexes via interval_complex
# ---------------------------------------------------------------------------

class TestIntervalCubicalComplex:
    def test_interval_n2_is_path(self):
        cx = interval_complex(2)
        # path [0,1,2]: 2 edges + 3 vertices = 5 cubes
        assert len(cx.cubes) == 5
        assert cx.dimension == 1

    def test_interval_n2_h0_connected(self):
        cx = interval_complex(2)
        groups = cubical_homology(cx)
        assert groups[0].betti == 1

    def test_interval_n2_h1_zero(self):
        cx = interval_complex(2)
        groups = cubical_homology(cx)
        assert groups[1].betti == 0

    def test_interval_n1_single_edge(self):
        cx = interval_complex(1)
        assert cx.dimension == 1
        groups = cubical_homology(cx)
        assert groups[0].betti == 1   # connected
        assert groups[1].betti == 0   # no loop

    def test_interval_euler_characteristic(self):
        cx = interval_complex(4)
        chi = cx.euler_characteristic()
        betti = sum((-1) ** g.degree * g.betti for g in cubical_homology(cx))
        assert chi == betti == 1   # contractible

    def test_interval_n5_cube_count(self):
        # n segments → n edges + (n+1) vertices
        n = 5
        cx = interval_complex(n)
        assert len(cx.cubes) == n + (n + 1)


# ---------------------------------------------------------------------------
# 3D cubical complexes
# ---------------------------------------------------------------------------

class TestCubical3D:
    def _unit_cube_3d(self) -> CubicalComplex:
        return make_cubical_complex([((0, 1), (0, 1), (0, 1))])

    def _hollow_cube_3d(self) -> CubicalComplex:
        """Shell of the unit cube: 6 faces but no interior 3-cell."""
        faces_3d: list[Cube] = [
            # six square faces of [0,1]³
            ((0, 0), (0, 1), (0, 1)),   # x=0 face
            ((1, 1), (0, 1), (0, 1)),   # x=1 face
            ((0, 1), (0, 0), (0, 1)),   # y=0 face
            ((0, 1), (1, 1), (0, 1)),   # y=1 face
            ((0, 1), (0, 1), (0, 0)),   # z=0 face
            ((0, 1), (0, 1), (1, 1)),   # z=1 face
        ]
        return make_cubical_complex(faces_3d)

    def test_unit_cube_3d_dimension(self):
        cx = self._unit_cube_3d()
        assert cx.dimension == 3

    def test_unit_cube_3d_h0_connected(self):
        groups = cubical_homology(self._unit_cube_3d())
        assert groups[0].betti == 1

    def test_unit_cube_3d_h1_zero(self):
        groups = cubical_homology(self._unit_cube_3d())
        assert groups[1].betti == 0

    def test_unit_cube_3d_h2_zero(self):
        groups = cubical_homology(self._unit_cube_3d())
        assert groups[2].betti == 0

    def test_unit_cube_3d_h3_zero(self):
        # Solid cube is contractible → H_3 = 0
        groups = cubical_homology(self._unit_cube_3d())
        assert groups[3].betti == 0

    def test_unit_cube_3d_euler(self):
        cx = self._unit_cube_3d()
        chi_cx = cx.euler_characteristic()
        chi_h = sum((-1) ** g.degree * g.betti for g in cubical_homology(cx))
        assert chi_cx == chi_h == 1  # contractible

    def test_boundary_sq_zero_3d_cube_k1(self):
        cx = self._unit_cube_3d()
        d1 = cubical_boundary_matrix(cx, 1)
        d2 = cubical_boundary_matrix(cx, 2)
        if d1 and d1[0] and d2 and d2[0]:
            product = _mat_mul(d1, d2)
            assert _is_zero_matrix(product)

    def test_boundary_sq_zero_3d_cube_k2(self):
        cx = self._unit_cube_3d()
        d2 = cubical_boundary_matrix(cx, 2)
        d3 = cubical_boundary_matrix(cx, 3)
        if d2 and d2[0] and d3 and d3[0]:
            product = _mat_mul(d2, d3)
            assert _is_zero_matrix(product)

    def test_hollow_cube_h2_is_z(self):
        # The surface of the cube ≃ S², so H₂ = Z
        cx = self._hollow_cube_3d()
        groups = cubical_homology(cx)
        assert groups[0].betti == 1   # connected
        assert groups[1].betti == 0   # no 1-loops
        assert groups[2].betti == 1   # one 2-sphere


# ---------------------------------------------------------------------------
# bitmap_to_cubical_filtration: 1D degenerate image
# ---------------------------------------------------------------------------

class TestBitmapFiltration1D:
    def test_1xn_row_image_cube_count(self):
        # 1×3 row: trivially 2D but with 1 row
        img = [[1.0, 2.0, 3.0]]
        f = bitmap_to_cubical_filtration(img)
        # m=1, n=3: (1+1)(3+1) + 1(3+1) + (1+1)*3 + 1*3 = 8 + 4 + 6 + 3 = 21
        expected = (1 + 1) * (3 + 1) + 1 * (3 + 1) + (1 + 1) * 3 + 1 * 3
        assert f.size() == expected

    def test_nx1_column_image_cube_count(self):
        img = [[1.0], [2.0], [3.0]]
        f = bitmap_to_cubical_filtration(img)
        m, n = 3, 1
        expected = (m + 1) * (n + 1) + m * (n + 1) + (m + 1) * n + m * n
        assert f.size() == expected

    def test_monotone_row_no_h1(self):
        pairs = persistent_homology_bitmap([[0.0, 1.0, 2.0, 3.0]])
        h1 = [p for p in pairs if p.dimension == 1]
        assert len(h1) == 0

    def test_monotone_row_one_essential_h0(self):
        pairs = persistent_homology_bitmap([[0.0, 1.0, 2.0, 3.0]])
        h0_essential = [p for p in pairs if p.dimension == 0 and p.is_essential]
        assert len(h0_essential) == 1


# ---------------------------------------------------------------------------
# ReductionStats value-range invariants
# ---------------------------------------------------------------------------

class TestReductionStatsInvariants:
    def _stats_for_space(self, points, max_dim=1):
        filtered = vietoris_rips_filtration(
            _metric_space(points), max_dimension=max_dim
        )
        _, stats = persistence_pairs_twist_with_stats(filtered)
        return stats, filtered

    def test_n_cleared_le_n_simplices(self):
        stats, filtered = self._stats_for_space(_circle_points(8), max_dim=2)
        assert stats.n_cleared <= stats.n_simplices

    def test_n_column_additions_nonneg_circle(self):
        stats, _ = self._stats_for_space(_circle_points(6), max_dim=2)
        assert stats.n_column_additions >= 0

    def test_clearing_ratio_in_unit_interval_circle(self):
        stats, _ = self._stats_for_space(_circle_points(8), max_dim=2)
        assert 0.0 <= stats.clearing_ratio <= 1.0

    def test_n_pairs_equals_len_output(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(6)), max_dimension=2
        )
        pairs, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_pairs == len(pairs)

    def test_n_finite_plus_essential_equals_total(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(6)), max_dimension=2
        )
        pairs, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_finite_pairs + stats.n_essential == stats.n_pairs

    def test_n_simplices_equals_filtered_size(self):
        filtered = vietoris_rips_filtration(
            _metric_space(_circle_points(6)), max_dimension=1
        )
        _, stats = persistence_pairs_twist_with_stats(filtered)
        assert stats.n_simplices == filtered.size()

    def test_two_isolated_points_no_clearing(self):
        # Two points far apart at dim=0 only: no edges → no clearing possible
        f = FilteredComplex(
            simplices=((0,), (1,)),
            births=(0.0, 0.0),
            dimensions=(0, 0),
        )
        _, stats = persistence_pairs_twist_with_stats(f)
        assert stats.n_cleared == 0
        assert stats.n_column_additions == 0
