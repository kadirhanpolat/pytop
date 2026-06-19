"""Known-answer and property tests for the exact integer linear algebra core.

`exact_linalg` exposes the Smith normal form, integer rank, fraction-free
(Bareiss) determinant, and abelian-group cokernel that back pytop's homology and
surgery engines.  The property tests pin the two independent exact routes
against each other: for a full-rank square matrix the Bareiss determinant equals
``± ∏`` of the Smith invariant factors.
"""

from __future__ import annotations

import random
from math import prod

import pytest

from pytop import (
    AbelianGroup,
    cokernel,
    integer_determinant,
    integer_rank,
    smith_normal_form,
    smith_normal_form_extended,
)


def _transpose(matrix):
    return [list(row) for row in zip(*matrix)]


# ---------------------------------------------------------------------------
# AbelianGroup
# ---------------------------------------------------------------------------


class TestAbelianGroup:
    def test_str(self):
        assert str(AbelianGroup(0, ())) == "0"
        assert str(AbelianGroup(1, ())) == "Z"
        assert str(AbelianGroup(2, (6,))) == "Z^2 + Z/6"
        assert str(AbelianGroup(0, (5,))) == "Z/5"

    def test_order_and_trivial(self):
        assert AbelianGroup(0, (2, 6)).order == 12
        assert AbelianGroup(0, ()).order == 1
        assert AbelianGroup(1, ()).order is None
        assert AbelianGroup(0, ()).is_trivial
        assert not AbelianGroup(0, (2,)).is_trivial


# ---------------------------------------------------------------------------
# Smith normal form / rank
# ---------------------------------------------------------------------------


class TestSmithNormalForm:
    def test_identity(self):
        assert smith_normal_form([[1, 0], [0, 1]]) == [1, 1]

    def test_diagonal_divisibility(self):
        # invariant factors are normalised so each divides the next
        assert smith_normal_form([[2, 0], [0, 3]]) == [1, 6]

    def test_rank_deficient(self):
        assert smith_normal_form([[1, 2], [2, 4]]) == [1]

    def test_integer_rank(self):
        assert integer_rank([[1, 0], [0, 1]]) == 2
        assert integer_rank([[1, 2], [2, 4]]) == 1
        assert integer_rank([[0, 0], [0, 0]]) == 0

    def test_rank_rectangular(self):
        assert integer_rank([[1, 0, 0], [0, 1, 0]]) == 2


# ---------------------------------------------------------------------------
# Integer determinant (Bareiss)
# ---------------------------------------------------------------------------


class TestIntegerDeterminant:
    def test_identity_and_empty(self):
        assert integer_determinant([[1, 0], [0, 1]]) == 1
        assert integer_determinant([]) == 1  # empty product

    def test_known_values(self):
        assert integer_determinant([[1, 2], [3, 4]]) == -2
        assert integer_determinant([[2, 0, 0], [0, 3, 0], [0, 0, 5]]) == 30
        assert integer_determinant([[6, 1, 1], [4, -2, 5], [2, 8, 7]]) == -306

    def test_singular_is_zero(self):
        assert integer_determinant([[1, 2], [2, 4]]) == 0

    def test_non_square_rejected(self):
        with pytest.raises(ValueError, match="square"):
            integer_determinant([[1, 2, 3], [4, 5, 6]])


# ---------------------------------------------------------------------------
# Cokernel
# ---------------------------------------------------------------------------


class TestCokernel:
    def test_torsion(self):
        assert cokernel([[2, 0], [0, 6]]) == AbelianGroup(0, (2, 6))

    def test_free_part(self):
        assert cokernel([[1, 0, 0], [0, 0, 0]]) == AbelianGroup(2, ())

    def test_unimodular_is_trivial(self):
        assert cokernel([[1, 0], [0, 1]]).is_trivial

    def test_empty(self):
        assert cokernel([]) == AbelianGroup(0, ())


# ---------------------------------------------------------------------------
# Properties — the two exact routes must agree
# ---------------------------------------------------------------------------


class TestProperties:
    def test_determinant_equals_invariant_factor_product(self):
        rng = random.Random(99)
        for _ in range(150):
            n = rng.randint(1, 4)
            matrix = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
            determinant = integer_determinant(matrix)
            factors = smith_normal_form(matrix)
            if len(factors) == n:  # full rank
                assert abs(determinant) == prod(factors)
            else:
                assert determinant == 0

    def test_determinant_and_rank_transpose_invariant(self):
        rng = random.Random(123)
        for _ in range(120):
            rows = rng.randint(1, 4)
            cols = rng.randint(1, 4)
            matrix = [[rng.randint(-4, 4) for _ in range(cols)] for _ in range(rows)]
            assert integer_rank(matrix) == integer_rank(_transpose(matrix))
            if rows == cols:
                assert integer_determinant(matrix) == integer_determinant(_transpose(matrix))

    def test_cokernel_free_rank_matches_rank(self):
        rng = random.Random(456)
        for _ in range(120):
            rows = rng.randint(1, 4)
            cols = rng.randint(1, 4)
            matrix = [[rng.randint(-4, 4) for _ in range(cols)] for _ in range(rows)]
            group = cokernel(matrix)
            assert group.free_rank == cols - integer_rank(matrix)

    def test_square_cokernel_order_equals_abs_determinant(self):
        rng = random.Random(789)
        for _ in range(120):
            n = rng.randint(1, 4)
            matrix = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
            determinant = integer_determinant(matrix)
            group = cokernel(matrix)
            if determinant != 0:
                assert group.order == abs(determinant)
            else:
                assert group.free_rank > 0


# ---------------------------------------------------------------------------
# Formal invariants — pytopSNF_positive and pytopSNF_divisibilityChain
# ---------------------------------------------------------------------------


class TestSNFFormalInvariants:
    """Property tests corresponding to the two main formal theorems in formal/Formal/SNF/.

    - pytopSNF_positive:          every factor d_i > 0
    - pytopSNF_divisibilityChain: d_1 | d_2 | ... | d_k
    """

    # --- Known-answer spot checks ---

    def test_positive_identity(self):
        factors = smith_normal_form([[1, 0], [0, 1]])
        assert all(d > 0 for d in factors)

    def test_divisibility_chain_known(self):
        # [[6,4],[3,2]] → SNF factors should satisfy d_1 | d_2
        factors = smith_normal_form([[6, 4], [3, 2]])
        for i in range(len(factors) - 1):
            assert factors[i + 1] % factors[i] == 0, factors

    def test_positive_rectangular(self):
        factors = smith_normal_form([[2, 4, 6], [1, 3, 5]])
        assert all(d > 0 for d in factors)

    def test_divisibility_after_elimination(self):
        # Matrix that requires row/col operations to achieve SNF
        factors = smith_normal_form([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        for i in range(len(factors) - 1):
            assert factors[i + 1] % factors[i] == 0, factors

    # --- Random property tests (pytopSNF_positive) ---

    def test_all_factors_positive_random(self):
        rng = random.Random(2024)
        for _ in range(300):
            rows = rng.randint(1, 5)
            cols = rng.randint(1, 5)
            matrix = [[rng.randint(-10, 10) for _ in range(cols)] for _ in range(rows)]
            factors = smith_normal_form(matrix)
            assert all(d > 0 for d in factors), f"non-positive factor in {factors}"

    # --- Random property tests (pytopSNF_divisibilityChain) ---

    def test_divisibility_chain_random_square(self):
        rng = random.Random(2025)
        for _ in range(300):
            n = rng.randint(1, 5)
            matrix = [[rng.randint(-8, 8) for _ in range(n)] for _ in range(n)]
            factors = smith_normal_form(matrix)
            for i in range(len(factors) - 1):
                assert factors[i + 1] % factors[i] == 0, (
                    f"divisibility broken at index {i}: "
                    f"{factors[i]} ∤ {factors[i + 1]}, factors={factors}"
                )

    def test_divisibility_chain_random_rectangular(self):
        rng = random.Random(2026)
        for _ in range(300):
            rows = rng.randint(1, 5)
            cols = rng.randint(1, 5)
            matrix = [[rng.randint(-8, 8) for _ in range(cols)] for _ in range(rows)]
            factors = smith_normal_form(matrix)
            for i in range(len(factors) - 1):
                assert factors[i + 1] % factors[i] == 0, (
                    f"divisibility broken at index {i}: "
                    f"{factors[i]} ∤ {factors[i + 1]}, factors={factors}"
                )

    def test_divisibility_chain_large_entries(self):
        rng = random.Random(2027)
        for _ in range(100):
            rows = rng.randint(2, 4)
            cols = rng.randint(2, 4)
            matrix = [[rng.randint(-100, 100) for _ in range(cols)] for _ in range(rows)]
            factors = smith_normal_form(matrix)
            assert all(d > 0 for d in factors)
            for i in range(len(factors) - 1):
                assert factors[i + 1] % factors[i] == 0, factors


# ---------------------------------------------------------------------------
# smith_normal_form_extended: transformation matrices P, Q
# ---------------------------------------------------------------------------


def _mat_mul(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """Integer matrix product A @ B."""
    rows, mid, cols = len(A), len(B), len(B[0]) if B else 0
    return [
        [sum(A[i][k] * B[k][j] for k in range(mid)) for j in range(cols)]
        for i in range(rows)
    ]


def _abs_det(M: list[list[int]]) -> int:
    """Absolute value of determinant (Bareiss), for square matrices only."""
    from pytop import integer_determinant
    return abs(integer_determinant(M))


class TestSNFExtended:
    """Tests for smith_normal_form_extended: (factors, P, Q) decomposition."""

    def _check_decomposition(self, matrix: list[list[int]]) -> None:
        factors, P, Q = smith_normal_form_extended(matrix)
        rows, cols = len(matrix), len(matrix[0]) if matrix else 0

        # factors must match smith_normal_form
        assert factors == smith_normal_form(matrix)

        # P, Q must be square with the right dimensions
        assert len(P) == rows and all(len(row) == rows for row in P)
        assert len(Q) == cols and all(len(row) == cols for row in Q)

        # P and Q must be unimodular (det = ±1)
        if rows > 0:
            assert _abs_det(P) == 1, f"|det(P)| = {_abs_det(P)}, not 1"
        if cols > 0:
            assert _abs_det(Q) == 1, f"|det(Q)| = {_abs_det(Q)}, not 1"

        # P @ matrix @ Q must be diagonal with the invariant factors on the diagonal
        D = _mat_mul(_mat_mul(P, matrix), Q)
        r = len(factors)
        for i in range(rows):
            for j in range(cols):
                if i == j and i < r:
                    assert D[i][j] == factors[i], f"D[{i}][{j}] = {D[i][j]}, expected {factors[i]}"
                else:
                    assert D[i][j] == 0, f"D[{i}][{j}] = {D[i][j]}, expected 0"

    def test_identity_2x2(self):
        self._check_decomposition([[1, 0], [0, 1]])

    def test_diagonal_non_snf(self):
        # [[2, 0], [0, 3]] → SNF = [[1, 0], [0, 6]]
        self._check_decomposition([[2, 0], [0, 3]])

    def test_rank_deficient(self):
        self._check_decomposition([[1, 2], [2, 4]])

    def test_single_row(self):
        self._check_decomposition([[4, 6, 10]])

    def test_single_col(self):
        self._check_decomposition([[6], [4], [10]])

    def test_rectangular_wide(self):
        self._check_decomposition([[1, 2, 3], [4, 5, 6]])

    def test_rectangular_tall(self):
        self._check_decomposition([[1, 4], [2, 5], [3, 6]])

    def test_zero_matrix(self):
        factors, P, Q = smith_normal_form_extended([[0, 0], [0, 0]])
        assert factors == []
        assert _abs_det(P) == 1
        assert _abs_det(Q) == 1

    def test_random_property(self):
        rng = random.Random(3141)
        for _ in range(150):
            rows = rng.randint(1, 4)
            cols = rng.randint(1, 4)
            matrix = [[rng.randint(-6, 6) for _ in range(cols)] for _ in range(rows)]
            self._check_decomposition(matrix)
