"""Smith normal form dispatch: sparse matrices take the sparse path even with FLINT.

python-flint's ``fmpz_mat.snf()`` falls back to Kannan–Bachem on singular or
non-square input. On the 443×476 even-Khovanov differential of ``7_2`` it ran past
60 s and 5 GB, while the sparse pure-Python path finishes in 0.13 s — so with
python-flint installed (the ``[fast]`` and ``[oracles]`` extras), Khovanov homology
of a 7-crossing knot hung. Khovanov differentials and simplicial boundary matrices
are sparse and rank-deficient by nature. FLINT stays the route for dense matrices,
where it is much faster than either pure-Python path.
"""

from __future__ import annotations

import pytest

import pytop.homology as hom


def _sparse_boundary_like(n: int) -> list[list[int]]:
    return [[1 if c == r else -1 if c == r + 1 else 0 for c in range(n)] for r in range(n - 1)]


@pytest.fixture
def fake_flint(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Pretend python-flint is installed; record the sizes it is asked to reduce."""

    calls: list[int] = []

    def record(matrix: list[list[int]]) -> list[int]:
        calls.append(len(matrix))
        return hom._smith_normal_form_python(matrix)

    monkeypatch.setattr(hom, "_flint", object())
    monkeypatch.setattr(hom, "_smith_normal_form_flint", record)
    return calls


def test_sparse_matrix_skips_flint(fake_flint: list[int]) -> None:
    matrix = _sparse_boundary_like(60)
    assert hom._smith_normal_form(matrix) == [1] * 59
    assert fake_flint == []


def test_dense_matrix_still_uses_flint(fake_flint: list[int]) -> None:
    matrix = [[(3 * r + 5 * c) % 7 + 1 for c in range(40)] for r in range(40)]
    hom._smith_normal_form(matrix)
    assert fake_flint == [40]


def test_small_matrix_uses_flint_below_the_sparse_threshold(fake_flint: list[int]) -> None:
    matrix = _sparse_boundary_like(20)  # min-dim 19 < SPARSE_MIN_DIM: not worth the sparse path
    hom._smith_normal_form(matrix)
    assert fake_flint == [19]
