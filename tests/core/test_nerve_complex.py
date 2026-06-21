"""Tests for P7.3 — nerve_complex module.

Covers:
  nerve_of_cover   : basic nerve, intersection logic, max_dim, errors
  good_cover_check : covers/misses space, all-nonempty, pairwise
  cech_nerve       : 1-D and 2-D point clouds, radius sensitivity, errors
"""

from __future__ import annotations

import math
import pytest

from pytop.homology import simplicial_homology
from pytop.nerve_complex import cech_nerve, good_cover_check, nerve_of_cover
from pytop.simplicial_complexes import SimplicialComplex


# ---------------------------------------------------------------------------
# nerve_of_cover
# ---------------------------------------------------------------------------

class TestNerveOfCover:
    def test_three_sets_path(self) -> None:
        # U0={0,1}, U1={1,2}, U2={2,3} — nerve is a path: 0-1-2
        U = [{0, 1}, {1, 2}, {2, 3}]
        N = nerve_of_cover(U)
        assert N.dimension == 1
        # H_0 = Z (connected), H_1 = 0 (contractible path)
        assert simplicial_homology(N, 0).betti == 1
        assert simplicial_homology(N, 1).betti == 0

    def test_three_sets_triangle(self) -> None:
        # Pairwise intersections but empty triple intersection
        U = [{0, 1}, {1, 2}, {0, 2}]
        N = nerve_of_cover(U)
        # All pairs intersect → 3 edges; triple intersection = {∅} → no 2-simplex
        assert N.dimension == 1
        assert simplicial_homology(N, 1).betti == 1  # S¹

    def test_three_sets_filled(self) -> None:
        # All three share a point → triangle + all faces
        U = [{0, 1, 2}, {1, 2, 3}, {0, 2, 3}]
        N = nerve_of_cover(U)
        assert N.dimension == 2
        assert simplicial_homology(N, 2).betti == 0  # contractible nerve

    def test_single_set(self) -> None:
        U = [{0, 1, 2}]
        N = nerve_of_cover(U)
        assert N.dimension == 0

    def test_two_disjoint_sets(self) -> None:
        U = [{0, 1}, {2, 3}]
        N = nerve_of_cover(U)
        assert N.dimension == 0
        assert simplicial_homology(N, 0).betti == 2  # two components

    def test_max_dim_truncates(self) -> None:
        U = [{0, 1, 2}, {1, 2, 3}, {0, 2, 3}]
        N0 = nerve_of_cover(U, max_dim=0)
        assert N0.dimension == 0
        N1 = nerve_of_cover(U, max_dim=1)
        assert N1.dimension == 1

    def test_error_empty_cover(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            nerve_of_cover([])

    def test_error_empty_set_in_cover(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            nerve_of_cover([{1, 2}, set()])

    def test_vertex_indices_are_integers(self) -> None:
        U = [{0}, {1}, {0, 1}]
        N = nerve_of_cover(U)
        for s in N.simplexes:
            for v in s.vertices:
                assert isinstance(v, int)

    def test_nerve_face_closed(self) -> None:
        U = [{0, 1, 2}, {1, 2, 3}, {0, 2, 3}]
        N = nerve_of_cover(U)
        from pytop.simplicial_complexes import face_closure_diagnostic
        diag = face_closure_diagnostic(N.simplexes)
        assert diag.is_face_closed

    def test_four_sets_with_quad_intersection(self) -> None:
        # All 4 sets share point 0 → tetrahedron nerve
        U = [{0, 1}, {0, 2}, {0, 3}, {0, 4}]
        N = nerve_of_cover(U)
        assert N.dimension == 3
        # Tetrahedron is contractible
        assert simplicial_homology(N, 0).betti == 1
        assert simplicial_homology(N, 1).betti == 0
        assert simplicial_homology(N, 2).betti == 0
        assert simplicial_homology(N, 3).betti == 0


# ---------------------------------------------------------------------------
# good_cover_check
# ---------------------------------------------------------------------------

class TestGoodCoverCheck:
    def test_covers_space(self) -> None:
        space = {0, 1, 2}
        cover = [{0, 1}, {1, 2}]
        result = good_cover_check(cover, space)
        assert result["covers_space"] is True
        assert result["all_nonempty"] is True
        assert result["is_good_cover"] is True

    def test_does_not_cover_space(self) -> None:
        space = {0, 1, 2, 3}
        cover = [{0, 1}, {1, 2}]
        result = good_cover_check(cover, space)
        assert result["covers_space"] is False
        assert result["is_good_cover"] is False

    def test_no_space_given(self) -> None:
        cover = [{0, 1}, {1, 2}]
        result = good_cover_check(cover)
        assert result["covers_space"] is None
        assert result["all_nonempty"] is True
        assert result["is_good_cover"] is True

    def test_empty_set_in_cover(self) -> None:
        cover = [{0, 1}, set()]
        result = good_cover_check(cover)
        assert result["all_nonempty"] is False
        assert result["is_good_cover"] is False

    def test_empty_cover(self) -> None:
        result = good_cover_check([])
        assert result["is_good_cover"] is False

    def test_pairwise_intersections(self) -> None:
        cover = [{0, 1}, {1, 2}, {3, 4}]
        result = good_cover_check(cover)
        pairs = result["pairwise_intersections"]
        assert (0, 1) in pairs
        assert (0, 2) not in pairs  # {0,1} ∩ {3,4} = ∅
        assert (1, 2) not in pairs  # {1,2} ∩ {3,4} = ∅

    def test_nerve_dimension_reported(self) -> None:
        cover = [{0, 1}, {1, 2}, {0, 2}]
        result = good_cover_check(cover)
        assert result["nerve_dimension"] == 1  # path of 3 vertices


# ---------------------------------------------------------------------------
# cech_nerve
# ---------------------------------------------------------------------------

class TestCechNerve:
    def test_three_collinear_points_radius_small(self) -> None:
        # Points at 0, 1, 2 with r=0.6: only adjacent pairs intersect
        pts = [(0.0,), (1.0,), (2.0,)]
        C = cech_nerve(pts, radius=0.6)
        assert C.dimension == 1
        # Two segments 0-1 and 1-2 but not 0-2 (dist=2 > 2r=1.2)
        assert simplicial_homology(C, 0).betti == 1
        assert simplicial_homology(C, 1).betti == 0

    def test_three_collinear_points_radius_large(self) -> None:
        # r=1.1 so B(0,r)∩B(2,r) is nonempty at 1.0: all three intersect
        pts = [(0.0,), (1.0,), (2.0,)]
        C = cech_nerve(pts, radius=1.1)
        assert C.dimension == 2

    def test_circle_points_small_radius(self) -> None:
        # 4 points on unit circle at 0°, 90°, 180°, 270°
        # Adjacent pairs at distance √2 ≈ 1.414; edge circumradius = √2/2 ≈ 0.707
        import math
        pts = [(math.cos(k * math.pi / 2), math.sin(k * math.pi / 2)) for k in range(4)]
        # r=0.6 < √2/2 ≈ 0.707: all pairwise circumradii exceed r → only 0-skeleton
        C = cech_nerve(pts, radius=0.6)
        assert C.dimension == 0

    def test_circle_points_medium_radius(self) -> None:
        import math
        pts = [(math.cos(k * math.pi / 2), math.sin(k * math.pi / 2)) for k in range(4)]
        # r=0.8 too small; r=0.8 > √2/2 ≈ 0.707 so adjacent balls intersect
        C = cech_nerve(pts, radius=0.75)
        # Adjacent pairs: dist = √2 ≈ 1.414, circumradius of edge = dist/2 ≈ 0.707
        assert C.dimension >= 1

    def test_max_dim_truncation(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
        C0 = cech_nerve(pts, radius=10.0, max_dim=0)
        assert C0.dimension == 0
        C1 = cech_nerve(pts, radius=10.0, max_dim=1)
        assert C1.dimension == 1
        C2 = cech_nerve(pts, radius=10.0, max_dim=2)
        assert C2.dimension == 2

    def test_error_empty_points(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            cech_nerve([], radius=1.0)

    def test_error_non_positive_radius(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            cech_nerve([(0.0,), (1.0,)], radius=0.0)
        with pytest.raises(ValueError, match="positive"):
            cech_nerve([(0.0,), (1.0,)], radius=-1.0)

    def test_error_inconsistent_dimension(self) -> None:
        with pytest.raises(ValueError, match="dimension"):
            cech_nerve([(0.0,), (1.0, 2.0)], radius=1.0)

    def test_single_point(self) -> None:
        C = cech_nerve([(0.0, 0.0)], radius=1.0)
        assert C.dimension == 0

    def test_two_points_intersecting(self) -> None:
        # Two points at distance 1, radius 0.6: balls intersect
        C = cech_nerve([(0.0,), (1.0,)], radius=0.6)
        assert C.dimension == 1

    def test_two_points_disjoint(self) -> None:
        # Two points at distance 1, radius 0.4: balls disjoint
        C = cech_nerve([(0.0,), (1.0,)], radius=0.4)
        assert C.dimension == 0

    def test_result_face_closed(self) -> None:
        pts = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
        C = cech_nerve(pts, radius=5.0)
        from pytop.simplicial_complexes import face_closure_diagnostic
        diag = face_closure_diagnostic(C.simplexes)
        assert diag.is_face_closed
