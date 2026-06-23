"""Tests for discrete_morse.py — discrete Morse theory on simplicial complexes."""

from __future__ import annotations

from itertools import combinations

import pytest

from pytop.discrete_morse import (
    MorseMatching,
    MorsePair,
    check_morse_inequalities,
    discrete_gradient_matching,
    is_valid_morse_matching,
)
from pytop.simplices import Simplex
from pytop.simplicial_complexes import SimplicialComplex

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _from_faces(faces: list[list[int]]) -> SimplicialComplex:
    """Build a face-closed SimplicialComplex from a list of maximal faces."""
    all_simplexes: list[list[int]] = []
    seen: set[frozenset[int]] = set()
    for face in faces:
        for r in range(1, len(face) + 1):
            for sub in combinations(face, r):
                key = frozenset(sub)
                if key not in seen:
                    seen.add(key)
                    all_simplexes.append(list(sub))
    return SimplicialComplex(all_simplexes)


def interval_complex() -> SimplicialComplex:
    """[0,1] as a simplicial complex: two vertices and one edge."""
    return SimplicialComplex([[0], [1], [0, 1]])


def triangle_complex() -> SimplicialComplex:
    """Filled triangle: 3 vertices, 3 edges, 1 face (contractible)."""
    return _from_faces([[0, 1, 2]])


def circle_complex() -> SimplicialComplex:
    """Triangulated S^1: 3 vertices, 3 edges (no 2-face)."""
    return SimplicialComplex([[0], [1], [2], [0, 1], [1, 2], [0, 2]])


def tetrahedron_complex() -> SimplicialComplex:
    """Filled 3-simplex (contractible)."""
    return _from_faces([[0, 1, 2, 3]])


def sphere_s2_complex() -> SimplicialComplex:
    """Hollow tetrahedron = minimal S^2 triangulation: 4V, 6E, 4F."""
    return _from_faces([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])


def torus_complex() -> SimplicialComplex:
    """9-vertex torus triangulation (flat square with identified boundary).

    Grid: vertex (i,j) → 3i+j for i,j in {0,1,2}.
    Triangles come from subdividing each unit square with a diagonal.
    χ = 9 - 27 + 18 = 0; Betti numbers (1,2,1).
    """
    def v(i: int, j: int) -> int:
        return 3 * (i % 3) + (j % 3)

    faces: list[list[int]] = []
    for i in range(3):
        for j in range(3):
            faces.append([v(i, j), v(i + 1, j), v(i, j + 1)])
            faces.append([v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)])
    return _from_faces(faces)


# ---------------------------------------------------------------------------
# MorsePair construction
# ---------------------------------------------------------------------------


class TestMorsePair:
    def test_valid_pair(self) -> None:
        sigma = Simplex([0])
        tau = Simplex([0, 1])
        pair = MorsePair(face=sigma, coface=tau)
        assert pair.face == sigma
        assert pair.coface == tau

    def test_wrong_dimension_raises(self) -> None:
        sigma = Simplex([0])
        tau = Simplex([0, 1, 2])
        with pytest.raises(ValueError, match="dimension"):
            MorsePair(face=sigma, coface=tau)

    def test_not_a_face_raises(self) -> None:
        sigma = Simplex([5])
        tau = Simplex([0, 1])
        with pytest.raises(ValueError, match="subset"):
            MorsePair(face=sigma, coface=tau)


# ---------------------------------------------------------------------------
# MorseMatching methods
# ---------------------------------------------------------------------------


class TestMorseMatching:
    def test_morse_vector_single_critical(self) -> None:
        sigma = Simplex([0])
        matching = MorseMatching(pairs=frozenset(), critical=frozenset([sigma]))
        assert matching.morse_vector() == (1,)

    def test_morse_vector_empty_critical(self) -> None:
        matching = MorseMatching(pairs=frozenset(), critical=frozenset())
        assert matching.morse_vector() == ()

    def test_euler_characteristic(self) -> None:
        # 2 critical 0-cells, 1 critical 1-cell → χ = 2 - 1 = 1
        v0 = Simplex([0])
        v1 = Simplex([1])
        e = Simplex([0, 1])
        matching = MorseMatching(pairs=frozenset(), critical=frozenset([v0, v1, e]))
        assert matching.euler_characteristic() == 2 - 1

    def test_critical_by_dimension(self) -> None:
        v = Simplex([0])
        e = Simplex([0, 1])
        matching = MorseMatching(pairs=frozenset(), critical=frozenset([v, e]))
        assert matching.critical_by_dimension(0) == frozenset([v])
        assert matching.critical_by_dimension(1) == frozenset([e])
        assert matching.critical_by_dimension(2) == frozenset()


# ---------------------------------------------------------------------------
# discrete_gradient_matching — structural correctness
# ---------------------------------------------------------------------------


class TestDiscreteGradientMatching:
    def test_interval_is_contractible(self) -> None:
        K = interval_complex()
        matching = discrete_gradient_matching(K)
        assert len(matching.critical) == 1
        assert all(s.dimension == 0 for s in matching.critical)

    def test_triangle_is_contractible(self) -> None:
        K = triangle_complex()
        matching = discrete_gradient_matching(K)
        # Filled triangle is contractible → exactly 1 critical cell
        assert len(matching.critical) == 1

    def test_circle_has_correct_critical_cells(self) -> None:
        K = circle_complex()
        matching = discrete_gradient_matching(K)
        mv = matching.morse_vector()
        # S^1 requires ≥ 1 critical 0-cell and ≥ 1 critical 1-cell
        assert mv[0] >= 1
        assert len(mv) >= 2 and mv[1] >= 1

    def test_tetrahedron_is_contractible(self) -> None:
        K = tetrahedron_complex()
        matching = discrete_gradient_matching(K)
        assert len(matching.critical) == 1

    def test_sphere_s2_has_critical_0_and_2_cells(self) -> None:
        K = sphere_s2_complex()
        matching = discrete_gradient_matching(K)
        mv = matching.morse_vector()
        # S^2 → β_0=1, β_2=1 → ≥ 1 critical 0-cell and ≥ 1 critical 2-cell
        assert mv[0] >= 1
        assert len(mv) >= 3 and mv[2] >= 1

    def test_unknown_strategy_raises(self) -> None:
        K = interval_complex()
        with pytest.raises(ValueError, match="strategy"):
            discrete_gradient_matching(K, strategy="optimal")

    def test_matching_covers_all_simplices(self) -> None:
        for K in [interval_complex(), triangle_complex(), circle_complex()]:
            matching = discrete_gradient_matching(K)
            used = {p.face for p in matching.pairs} | {p.coface for p in matching.pairs}
            assert (used | matching.critical) == K.simplexes

    def test_pairs_are_disjoint(self) -> None:
        for K in [interval_complex(), circle_complex(), tetrahedron_complex()]:
            matching = discrete_gradient_matching(K)
            used_faces = {p.face for p in matching.pairs}
            used_cofaces = {p.coface for p in matching.pairs}
            assert used_faces & used_cofaces == set()
            assert (used_faces | used_cofaces) & matching.critical == set()

    def test_euler_characteristic_matches_complex(self) -> None:
        for K in [interval_complex(), triangle_complex(), circle_complex(),
                  sphere_s2_complex()]:
            matching = discrete_gradient_matching(K)
            assert matching.euler_characteristic() == K.euler_characteristic()


# ---------------------------------------------------------------------------
# is_valid_morse_matching
# ---------------------------------------------------------------------------


class TestIsValidMorseMatching:
    def test_greedy_output_is_valid(self) -> None:
        for K in [interval_complex(), triangle_complex(), circle_complex(),
                  tetrahedron_complex(), sphere_s2_complex()]:
            matching = discrete_gradient_matching(K)
            assert is_valid_morse_matching(K, matching), (
                f"Invalid matching on complex with f-vector {K.f_vector()}"
            )

    def test_trivial_matching_all_critical_is_valid(self) -> None:
        K = interval_complex()
        matching = MorseMatching(pairs=frozenset(), critical=K.simplexes)
        assert is_valid_morse_matching(K, matching)

    def test_invalid_overlap_detected(self) -> None:
        K = interval_complex()
        v0 = Simplex([0])
        v1 = Simplex([1])
        e = Simplex([0, 1])
        pair = MorsePair(face=v0, coface=e)
        # v0 appears in both pairs and critical → invalid partition
        matching = MorseMatching(pairs=frozenset([pair]), critical=frozenset([v0, v1]))
        assert not is_valid_morse_matching(K, matching)

    def test_incomplete_cover_detected(self) -> None:
        K = interval_complex()
        v0 = Simplex([0])
        # Only v0 declared critical — missing v1 and the edge
        matching = MorseMatching(pairs=frozenset(), critical=frozenset([v0]))
        assert not is_valid_morse_matching(K, matching)

    def test_cyclic_matching_is_invalid(self) -> None:
        # S^1 with the cyclic matching (0,01),(1,12),(2,02) — creates a V-cycle
        K = circle_complex()
        v0, v1, v2 = Simplex([0]), Simplex([1]), Simplex([2])
        e01 = Simplex([0, 1])
        e12 = Simplex([1, 2])
        e02 = Simplex([0, 2])
        pairs = frozenset([
            MorsePair(face=v0, coface=e01),
            MorsePair(face=v1, coface=e12),
            MorsePair(face=v2, coface=e02),
        ])
        matching = MorseMatching(pairs=pairs, critical=frozenset())
        assert not is_valid_morse_matching(K, matching)


# ---------------------------------------------------------------------------
# check_morse_inequalities
# ---------------------------------------------------------------------------


class TestCheckMorseInequalities:
    def test_interval_all_satisfied(self) -> None:
        K = interval_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        assert ineq.all_satisfied

    def test_circle_all_satisfied(self) -> None:
        K = circle_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        assert ineq.all_satisfied

    def test_triangle_all_satisfied(self) -> None:
        K = triangle_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        assert ineq.all_satisfied

    def test_sphere_s2_all_satisfied(self) -> None:
        K = sphere_s2_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        assert ineq.all_satisfied

    def test_euler_identity_holds(self) -> None:
        for K in [interval_complex(), triangle_complex(), circle_complex(),
                  sphere_s2_complex()]:
            matching = discrete_gradient_matching(K)
            ineq = check_morse_inequalities(K, matching)
            assert ineq.euler_identity_satisfied, (
                f"Euler identity failed: morse={ineq.euler_from_morse}, "
                f"complex={ineq.euler_from_complex}"
            )

    def test_describe_returns_string(self) -> None:
        K = circle_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        s = ineq.describe()
        assert "Morse vector" in s
        assert "Betti" in s

    def test_torus_euler_identity(self) -> None:
        K = torus_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        assert ineq.euler_identity_satisfied
        assert ineq.weak_inequalities_satisfied

    def test_tetrahedron_one_critical_cell_is_optimal(self) -> None:
        K = tetrahedron_complex()
        matching = discrete_gradient_matching(K)
        ineq = check_morse_inequalities(K, matching)
        # Contractible → optimal matching has exactly 1 critical cell
        assert sum(ineq.morse_vector) == 1
        assert ineq.all_satisfied
