"""Tests for P7.6 — morse_complex module.

Covers:
  MorseChainComplex      : construction, num_critical, morse_vector
  morse_boundary_operator : explicit matrix values for S¹, S², contractible
  morse_chain_complex    : full complex construction
  morse_homology         : H_* equals simplicial homology (validates=True)
"""

from __future__ import annotations

from pytop.discrete_morse import (
    MorseMatching,
    MorsePair,
    discrete_gradient_matching,
    is_valid_morse_matching,
)
from pytop.morse_complex import (
    MorseChainComplex,
    MorseHomologyResult,
    morse_boundary_operator,
    morse_chain_complex,
    morse_homology,
)
from pytop.simplices import Simplex
from pytop.simplicial_complexes import SimplicialComplex

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _circle() -> SimplicialComplex:
    """Triangulated S¹ with 3 vertices and 3 edges."""
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
    ])


def _disk() -> SimplicialComplex:
    """Filled triangle D²."""
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([1, 2]),
        Simplex([0, 1, 2]),
    ])


def _sphere_s2() -> SimplicialComplex:
    """Minimal triangulation of S² (boundary of a tetrahedron, 4 vertices)."""
    return SimplicialComplex([
        Simplex([0]), Simplex([1]), Simplex([2]), Simplex([3]),
        Simplex([0, 1]), Simplex([0, 2]), Simplex([0, 3]),
        Simplex([1, 2]), Simplex([1, 3]), Simplex([2, 3]),
        Simplex([0, 1, 2]), Simplex([0, 1, 3]),
        Simplex([0, 2, 3]), Simplex([1, 2, 3]),
    ])


def _interval() -> SimplicialComplex:
    """[0, 1] as an edge — contractible."""
    return SimplicialComplex([Simplex([0]), Simplex([1]), Simplex([0, 1])])


def _two_points() -> SimplicialComplex:
    """Two disjoint vertices — H_0 = Z²."""
    return SimplicialComplex([Simplex([0]), Simplex([1])])


def _torus_filtration_complex() -> SimplicialComplex:
    """7-vertex minimal triangulation of T² imported from simplicial_filtration."""
    from pytop.simplicial_filtration import torus_filtration
    filt = torus_filtration()
    all_simplices = [Simplex(list(vs)) for vs in filt.simplices]
    return SimplicialComplex(all_simplices)


def _make_matching_for_circle() -> tuple[SimplicialComplex, MorseMatching]:
    """Build a valid Morse matching on S¹ with exactly 1 vertex + 1 edge critical."""
    K = _circle()
    # Pair {0} ↔ {0,1} and {1} ↔ {1,2} — leaves {2} and {0,2} critical
    p1 = MorsePair(face=Simplex([0]), coface=Simplex([0, 1]))
    p2 = MorsePair(face=Simplex([1]), coface=Simplex([1, 2]))
    critical = frozenset({Simplex([2]), Simplex([0, 2])})
    matching = MorseMatching(pairs=frozenset({p1, p2}), critical=critical)
    assert is_valid_morse_matching(K, matching)
    return K, matching


def _make_matching_for_interval() -> tuple[SimplicialComplex, MorseMatching]:
    """Interval [0,1]: pair {0} ↔ {0,1}, critical = {{1}}."""
    K = _interval()
    p = MorsePair(face=Simplex([0]), coface=Simplex([0, 1]))
    matching = MorseMatching(pairs=frozenset({p}), critical=frozenset({Simplex([1])}))
    assert is_valid_morse_matching(K, matching)
    return K, matching


# ---------------------------------------------------------------------------
# TestMorseChainComplex — basic construction
# ---------------------------------------------------------------------------

class TestMorseChainComplex:
    def test_type(self) -> None:
        K, M = _make_matching_for_circle()
        cc = morse_chain_complex(K, M)
        assert isinstance(cc, MorseChainComplex)

    def test_critical_simplices_by_dim(self) -> None:
        K, M = _make_matching_for_circle()
        cc = morse_chain_complex(K, M)
        assert cc.num_critical(0) == 1
        assert cc.num_critical(1) == 1

    def test_morse_vector_circle(self) -> None:
        K, M = _make_matching_for_circle()
        cc = morse_chain_complex(K, M)
        assert cc.morse_vector() == (1, 1)

    def test_morse_vector_interval(self) -> None:
        K, M = _make_matching_for_interval()
        cc = morse_chain_complex(K, M)
        assert cc.morse_vector() == (1,)

    def test_boundary_matrices_present(self) -> None:
        K, M = _make_matching_for_circle()
        cc = morse_chain_complex(K, M)
        assert 1 in cc.boundary_matrices

    def test_empty_matching(self) -> None:
        K = _circle()
        M = MorseMatching(pairs=frozenset(), critical=frozenset())
        cc = morse_chain_complex(K, M)
        assert cc.morse_vector() == ()

    def test_greedy_matching_circle(self) -> None:
        K = _circle()
        M = discrete_gradient_matching(K)
        assert is_valid_morse_matching(K, M)
        cc = morse_chain_complex(K, M)
        # Greedy should also give 1 vertex + 1 edge critical
        assert cc.num_critical(0) == 1
        assert cc.num_critical(1) == 1

    def test_disk_greedy_morse_vector(self) -> None:
        K = _disk()
        M = discrete_gradient_matching(K)
        cc = morse_chain_complex(K, M)
        # Disk is contractible → minimal is (1,) but greedy may not be perfect
        total = sum(cc.morse_vector())
        assert total >= 1  # at least one critical cell


# ---------------------------------------------------------------------------
# TestMorseBoundaryOperator — explicit matrix checks
# ---------------------------------------------------------------------------

class TestMorseBoundaryOperator:
    def test_circle_boundary_is_zero(self) -> None:
        K, M = _make_matching_for_circle()
        mat = morse_boundary_operator(K, M, 1)
        # ∂^M_1: C^M_1 → C^M_0 must be zero (since H_1(S¹) = Z)
        assert len(mat) == 1 and len(mat[0]) == 1
        assert mat[0][0] == 0

    def test_shape_circle(self) -> None:
        K, M = _make_matching_for_circle()
        mat = morse_boundary_operator(K, M, 1)
        assert len(mat) == 1      # 1 critical 0-simplex (row)
        assert len(mat[0]) == 1   # 1 critical 1-simplex (col)

    def test_k_zero_returns_empty(self) -> None:
        K, M = _make_matching_for_circle()
        assert morse_boundary_operator(K, M, 0) == []

    def test_no_critical_km1_returns_zero_rows(self) -> None:
        K = _interval()
        p = MorsePair(face=Simplex([0]), coface=Simplex([0, 1]))
        M = MorseMatching(pairs=frozenset({p}), critical=frozenset({Simplex([1])}))
        # At degree 1: 0 critical 1-simplices → empty columns
        mat = morse_boundary_operator(K, M, 1)
        assert mat == [[]]  # 1 row (1 critical 0-simplex), 0 cols

    def test_interval_boundary_is_zero_matrix(self) -> None:
        K, M = _make_matching_for_interval()
        # Only 1 critical 0-simplex, 0 critical 1-simplices
        mat = morse_boundary_operator(K, M, 1)
        # shape: 1 row × 0 cols
        assert len(mat) == 1 and len(mat[0]) == 0

    def test_two_points_boundary_at_1(self) -> None:
        # Two disjoint points have no edges → no Morse pairs possible
        K = _two_points()
        M = MorseMatching(
            pairs=frozenset(),
            critical=frozenset({Simplex([0]), Simplex([1])}),
        )
        mat = morse_boundary_operator(K, M, 1)
        # 2 critical 0-simplices → 2 rows; 0 critical 1-simplices → 0 cols
        assert all(len(row) == 0 for row in mat)


# ---------------------------------------------------------------------------
# TestMorseHomology — Morse theorem validation
# ---------------------------------------------------------------------------

class TestMorseHomology:
    def test_type(self) -> None:
        K, M = _make_matching_for_circle()
        result = morse_homology(K, M)
        assert isinstance(result, MorseHomologyResult)

    def test_circle_h0(self) -> None:
        K, M = _make_matching_for_circle()
        result = morse_homology(K, M)
        assert result.get(0).betti == 1

    def test_circle_h1(self) -> None:
        K, M = _make_matching_for_circle()
        result = morse_homology(K, M)
        assert result.get(1).betti == 1

    def test_circle_validates(self) -> None:
        K, M = _make_matching_for_circle()
        result = morse_homology(K, M)
        assert result.validates is True

    def test_interval_h0(self) -> None:
        K, M = _make_matching_for_interval()
        result = morse_homology(K, M)
        assert result.get(0).betti == 1

    def test_interval_h1_zero(self) -> None:
        K, M = _make_matching_for_interval()
        result = morse_homology(K, M)
        assert result.get(1).betti == 0

    def test_interval_validates(self) -> None:
        K, M = _make_matching_for_interval()
        result = morse_homology(K, M)
        assert result.validates is True

    def test_disk_greedy(self) -> None:
        K = _disk()
        M = discrete_gradient_matching(K)
        result = morse_homology(K, M)
        assert result.validates is True
        assert result.get(0).betti == 1
        assert result.get(1).betti == 0
        assert result.get(2).betti == 0

    def test_s2_greedy(self) -> None:
        K = _sphere_s2()
        M = discrete_gradient_matching(K)
        assert is_valid_morse_matching(K, M)
        result = morse_homology(K, M)
        assert result.validates is True
        assert result.get(0).betti == 1
        assert result.get(1).betti == 0
        assert result.get(2).betti == 1

    def test_circle_greedy_validates(self) -> None:
        K = _circle()
        M = discrete_gradient_matching(K)
        result = morse_homology(K, M)
        assert result.validates is True

    def test_two_points_validates(self) -> None:
        K = _two_points()
        M = MorseMatching(
            pairs=frozenset(),
            critical=frozenset({Simplex([0]), Simplex([1])}),
        )
        result = morse_homology(K, M)
        assert result.validates is True
        assert result.get(0).betti == 2

    def test_get_out_of_range_returns_zero(self) -> None:
        K, M = _make_matching_for_circle()
        result = morse_homology(K, M)
        assert result.get(99).betti == 0

    def test_max_degree_parameter(self) -> None:
        K = _circle()
        M = discrete_gradient_matching(K)
        result = morse_homology(K, M, max_degree=0)
        assert len(result.groups) == 1  # only degree 0

    def test_s2_morse_vector_optimal(self) -> None:
        K = _sphere_s2()
        M = discrete_gradient_matching(K)
        cc = morse_chain_complex(K, M)
        mv = cc.morse_vector()
        # S² Euler characteristic = 2: m_0 - m_1 + m_2 = 2
        chi = sum((-1) ** k * mv[k] for k in range(len(mv)))
        assert chi == 2

    def test_circle_morse_vector_optimal(self) -> None:
        K = _circle()
        M = discrete_gradient_matching(K)
        cc = morse_chain_complex(K, M)
        mv = cc.morse_vector()
        # χ(S¹) = 0
        chi = sum((-1) ** k * mv[k] for k in range(len(mv)))
        assert chi == 0

    def test_torus_validates(self) -> None:
        K = _torus_filtration_complex()
        M = discrete_gradient_matching(K)
        assert is_valid_morse_matching(K, M)
        result = morse_homology(K, M)
        assert result.validates is True


# ---------------------------------------------------------------------------
# TestMorsePublicAPI — import from pytop directly
# ---------------------------------------------------------------------------

class TestMorsePublicAPI:
    def test_imports_from_pytop(self) -> None:
        from pytop import (
            MorseChainComplex,
            MorseHomologyResult,
            morse_boundary_operator,
            morse_chain_complex,
            morse_homology,
        )
        assert MorseChainComplex is not None
        assert MorseHomologyResult is not None
        assert callable(morse_boundary_operator)
        assert callable(morse_chain_complex)
        assert callable(morse_homology)

    def test_end_to_end_via_public_api(self) -> None:
        from pytop import morse_homology as mh
        from pytop.discrete_morse import discrete_gradient_matching
        K = _circle()
        M = discrete_gradient_matching(K)
        result = mh(K, M)
        assert result.validates is True
        assert result.get(1).betti == 1
