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
