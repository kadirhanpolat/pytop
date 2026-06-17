"""Simplicial homology with field coefficients and relative homology.

This extends the integer engine in :mod:`pytop.homology` (boundary matrices →
Smith normal form → Betti + torsion over Z) toward research grade:

* **field coefficients** (`Q` and `Z/p`): the homology vector-space dimension is
  ``dim H_k(K; F) = nullity_F(∂_k) - rank_F(∂_{k+1})``, computed by Gaussian
  elimination over the field. Fields have no torsion, so this is just a Betti
  number — but it is *coefficient dependent*: the real projective plane has
  ``H_1(RP^2; Q) = 0`` yet ``H_1(RP^2; Z/2) = Z/2`` (the torsion becomes visible).
* **relative homology** ``H_*(K, L; Z)`` for a subcomplex ``L``: the homology of
  the relative chain complex ``C_*(K)/C_*(L)`` via Smith normal form, giving
  e.g. ``H_2(D^2, ∂D^2) = Z``.

All exact and dependency-free.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from .homology import HomologyResult, _simplices_of_dimension, _smith_normal_form, betti_numbers
from .homology import boundary_matrix as _integer_boundary_matrix
from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]


def _field_rank(matrix: Matrix, modulus: int | None) -> int:
    """Rank of an integer matrix over a field: Q if ``modulus`` is None, else Z/modulus."""

    if not matrix or not matrix[0]:
        return 0
    if modulus is None:
        rows: list[list[Any]] = [[Fraction(v) for v in row] for row in matrix]
    else:
        rows = [[v % modulus for v in row] for row in matrix]
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = next((r for r in range(rank, row_count) if rows[r][col] != 0), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        if modulus is None:
            inverse = Fraction(1) / rows[rank][col]
        else:
            inverse = pow(rows[rank][col], -1, modulus)
        for r in range(row_count):
            if r != rank and rows[r][col] != 0:
                factor = rows[r][col] * inverse
                if modulus is None:
                    rows[r] = [a - factor * b for a, b in zip(rows[r], rows[rank])]
                else:
                    rows[r] = [(a - factor * b) % modulus for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def _normalize_coefficients(coefficients: Any) -> int | None:
    """Return the field modulus: None for Q, the prime p for Z/p. 'Z' is handled elsewhere."""

    if coefficients in ("Q", "q", 0):
        return None
    if isinstance(coefficients, int) and coefficients >= 2:
        return coefficients
    raise ValueError(f"Unsupported field coefficients: {coefficients!r} (use 'Q' or a prime p).")


def homology_with_coefficients(
    complex_obj: SimplicialComplex, degree: int, coefficients: Any = "Q"
) -> HomologyResult:
    """Return ``H_degree(complex_obj; F)`` for field coefficients ``F``.

    ``coefficients`` is ``"Q"`` (rationals) or a prime ``p`` (the field ``Z/p``).
    For integer coefficients use :func:`pytop.simplicial_homology`.
    """

    if coefficients in ("Z", "z"):
        from .homology import simplicial_homology

        return simplicial_homology(complex_obj, degree)
    if degree < 0:
        return HomologyResult(degree=degree, betti=0, torsion=())
    modulus = _normalize_coefficients(coefficients)
    n_k = len(_simplices_of_dimension(complex_obj, degree))
    if n_k == 0:
        return HomologyResult(degree=degree, betti=0, torsion=())
    rank_k = _field_rank(_integer_boundary_matrix(complex_obj, degree), modulus)
    rank_k_plus_1 = _field_rank(_integer_boundary_matrix(complex_obj, degree + 1), modulus)
    return HomologyResult(degree=degree, betti=(n_k - rank_k) - rank_k_plus_1, torsion=())


def betti_numbers_over(complex_obj: SimplicialComplex, coefficients: Any = "Q") -> tuple[int, ...]:
    """Return the Betti numbers of ``complex_obj`` over the given coefficients.

    ``coefficients`` is ``"Z"`` (free ranks of integral homology), ``"Q"``, or a
    prime ``p``.
    """

    if coefficients in ("Z", "z"):
        return betti_numbers(complex_obj)
    return tuple(
        homology_with_coefficients(complex_obj, degree, coefficients).betti
        for degree in range(complex_obj.dimension + 1)
    )


def _vertex_sets(complex_obj: SimplicialComplex) -> set[frozenset[Any]]:
    return {simplex.vertices for simplex in complex_obj.simplexes}


def _relative_boundary_matrix(
    complex_obj: SimplicialComplex, sub: SimplicialComplex, degree: int
) -> tuple[Matrix, int]:
    """Boundary matrix of the relative chain complex ``C_*(K)/C_*(L)`` in degree ``degree``.

    Returns the matrix and the number of relative ``degree``-chains (columns).
    """

    in_sub = _vertex_sets(sub)
    cols = [s for s in _simplices_of_dimension(complex_obj, degree) if frozenset(s) not in in_sub]
    if degree <= 0:
        return [], len(cols)
    rows = [s for s in _simplices_of_dimension(complex_obj, degree - 1) if frozenset(s) not in in_sub]
    row_index = {simplex: i for i, simplex in enumerate(rows)}
    matrix: Matrix = [[0] * len(cols) for _ in rows]
    for col, simplex in enumerate(cols):
        for i in range(len(simplex)):
            face = simplex[:i] + simplex[i + 1 :]
            if frozenset(face) in in_sub:
                continue  # quotient out faces lying in L
            matrix[row_index[face]][col] += (-1) ** i
    return matrix, len(cols)


def relative_homology(
    complex_obj: SimplicialComplex, sub: SimplicialComplex, degree: int
) -> HomologyResult:
    """Return relative integral homology ``H_degree(complex_obj, sub; Z)``.

    ``sub`` must be a subcomplex of ``complex_obj``. Example:
    ``H_2(filled triangle, its boundary) = Z``.
    """

    if not _vertex_sets(sub) <= _vertex_sets(complex_obj):
        raise ValueError("sub must be a subcomplex of complex_obj.")
    if degree < 0:
        return HomologyResult(degree=degree, betti=0, torsion=())
    _, n_k = _relative_boundary_matrix(complex_obj, sub, degree)
    if n_k == 0:
        return HomologyResult(degree=degree, betti=0, torsion=())
    boundary_k, _ = _relative_boundary_matrix(complex_obj, sub, degree)
    rank_k = len(_smith_normal_form(boundary_k))
    next_factors = _smith_normal_form(_relative_boundary_matrix(complex_obj, sub, degree + 1)[0])
    rank_k_plus_1 = len(next_factors)
    betti = (n_k - rank_k) - rank_k_plus_1
    torsion = tuple(factor for factor in next_factors if factor > 1)
    return HomologyResult(degree=degree, betti=betti, torsion=torsion)


def relative_betti_numbers(
    complex_obj: SimplicialComplex, sub: SimplicialComplex
) -> tuple[int, ...]:
    """Return the relative Betti numbers ``(b_0, ..., b_dim)`` of ``(complex_obj, sub)``."""

    return tuple(
        relative_homology(complex_obj, sub, degree).betti
        for degree in range(complex_obj.dimension + 1)
    )


__all__ = [
    "homology_with_coefficients",
    "betti_numbers_over",
    "relative_homology",
    "relative_betti_numbers",
]
