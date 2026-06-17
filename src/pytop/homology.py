"""Constructive integer simplicial homology for finite complexes.

This module turns a finite :class:`~pytop.simplicial_complexes.SimplicialComplex`
into genuine homological invariants computed from its combinatorial data:

* oriented boundary matrices ``partial_k : C_k -> C_{k-1}`` over the integers,
* the Smith normal form of those matrices,
* the integral homology groups ``H_k(K; Z) = ker(partial_k) / im(partial_{k+1})``,
  decomposed into a free part (the Betti number ``b_k``) and a torsion part
  (the invariant factors greater than one).

Unlike the descriptive profiles elsewhere in the package, nothing here is
hardcoded: the Betti numbers and torsion coefficients are derived from the
boundary operators. The implementation is dependency-free and follows the
package convention of consistent vertex ordering by ``repr``.

Orientation convention
-----------------------
For a ``k``-simplex with vertices ordered ``v_0 < v_1 < ... < v_k`` (by
``repr``), the boundary is the alternating sum

    partial(sigma) = sum_i (-1)^i (v_0, ..., hat(v_i), ..., v_k)

so ``partial_{k-1} . partial_k = 0`` holds matrix-wise.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]


@dataclass(frozen=True)
class HomologyResult:
    """The integral homology group ``H_k(K; Z)`` in degree ``degree``.

    ``betti`` is the rank of the free part; ``torsion`` is the tuple of
    invariant factors greater than one (so ``H_k = Z^betti (+) (+)_d Z/d``).
    """

    degree: int
    betti: int
    torsion: tuple[int, ...] = ()

    @property
    def is_free(self) -> bool:
        return not self.torsion

    def describe(self) -> str:
        parts: list[str] = []
        if self.betti == 1:
            parts.append("Z")
        elif self.betti > 1:
            parts.append(f"Z^{self.betti}")
        parts.extend(f"Z/{factor}" for factor in self.torsion)
        return " (+) ".join(parts) if parts else "0"


def _ordered(vertices: frozenset[Any]) -> tuple[Any, ...]:
    """Order vertices consistently with the rest of the package (by repr)."""

    return tuple(sorted(vertices, key=repr))


def _simplices_of_dimension(complex_obj: SimplicialComplex, k: int) -> list[tuple[Any, ...]]:
    """Return the ordered ``k``-simplices as canonically ordered vertex tuples."""

    members = [
        _ordered(simplex.vertices)
        for simplex in complex_obj.simplexes
        if simplex.dimension == k
    ]
    return sorted(members, key=lambda vs: tuple(repr(v) for v in vs))


def boundary_matrix(complex_obj: SimplicialComplex, k: int) -> Matrix:
    """Return the integer boundary matrix ``partial_k`` of ``complex_obj``.

    Rows are indexed by the ``(k-1)``-simplices and columns by the
    ``k``-simplices, both in canonical order. For ``k <= 0`` or out-of-range
    degrees the matrix has no rows (``partial_0`` is the zero map to ``C_{-1}``).
    """

    if k <= 0:
        # partial_0 maps into C_{-1} = 0, so there are no rows.
        return []
    faces = _simplices_of_dimension(complex_obj, k - 1)
    simplices = _simplices_of_dimension(complex_obj, k)
    if not simplices:
        return [[0] * 0 for _ in range(len(faces))]
    face_index = {face: idx for idx, face in enumerate(faces)}
    matrix: Matrix = [[0] * len(simplices) for _ in range(len(faces))]
    for col, simplex in enumerate(simplices):
        for i in range(len(simplex)):
            face = simplex[:i] + simplex[i + 1 :]
            row = face_index[face]
            matrix[row][col] += (-1) ** i
    return matrix


def _smith_normal_form(matrix: Matrix) -> list[int]:
    """Return the positive invariant factors of ``matrix`` over the integers.

    The returned list ``[d_1, ..., d_r]`` satisfies ``d_1 | d_2 | ... | d_r`` and
    ``r`` equals the rank of the matrix. Entries equal to one are retained, so
    the rank is ``len(result)`` and torsion is ``[d for d in result if d > 1]``.
    """

    rows = [list(map(int, row)) for row in matrix]
    m = len(rows)
    n = len(rows[0]) if m else 0
    if m == 0 or n == 0:
        return []

    def swap_rows(i: int, j: int) -> None:
        rows[i], rows[j] = rows[j], rows[i]

    def swap_cols(i: int, j: int) -> None:
        for r in rows:
            r[i], r[j] = r[j], r[i]

    def add_row(src: int, dst: int, factor: int) -> None:
        source = rows[src]
        target = rows[dst]
        for c in range(n):
            target[c] += factor * source[c]

    def add_col(src: int, dst: int, factor: int) -> None:
        for r in rows:
            r[dst] += factor * r[src]

    invariants: list[int] = []
    t = 0
    while t < min(m, n):
        # Choose a pivot: the smallest-magnitude nonzero entry in the t-submatrix.
        pivot: tuple[int, int] | None = None
        best = 0
        for i in range(t, m):
            for j in range(t, n):
                value = rows[i][j]
                if value != 0 and (pivot is None or abs(value) < best):
                    pivot = (i, j)
                    best = abs(value)
        if pivot is None:
            break
        swap_rows(t, pivot[0])
        swap_cols(t, pivot[1])

        # Clear the pivot row and column; repeat until the pivot divides them.
        cleared = False
        while not cleared:
            cleared = True
            for i in range(m):
                if i != t and rows[i][t] != 0:
                    add_row(t, i, -(rows[i][t] // rows[t][t]))
                    if rows[i][t] != 0:
                        swap_rows(t, i)
                        cleared = False
            for j in range(n):
                if j != t and rows[t][j] != 0:
                    add_col(t, j, -(rows[t][j] // rows[t][t]))
                    if rows[t][j] != 0:
                        swap_cols(t, j)
                        cleared = False

        # Enforce the divisibility condition d_t | (remaining submatrix).
        pivot_value = rows[t][t]
        needs_restart = False
        for i in range(t + 1, m):
            for j in range(t + 1, n):
                if rows[i][j] % pivot_value != 0:
                    add_row(i, t, 1)
                    needs_restart = True
                    break
            if needs_restart:
                break
        if needs_restart:
            continue

        invariants.append(abs(rows[t][t]))
        t += 1

    return invariants


def _rank(matrix: Matrix) -> int:
    return len(_smith_normal_form(matrix))


def simplicial_homology(complex_obj: SimplicialComplex, degree: int) -> HomologyResult:
    """Return ``H_degree(complex_obj; Z)`` as a :class:`HomologyResult`.

    ``betti = nullity(partial_degree) - rank(partial_{degree+1})`` and the
    torsion coefficients are the invariant factors greater than one of
    ``partial_{degree+1}``.
    """

    if degree < 0:
        return HomologyResult(degree=degree, betti=0, torsion=())

    n_k = len(_simplices_of_dimension(complex_obj, degree))
    if n_k == 0:
        return HomologyResult(degree=degree, betti=0, torsion=())

    rank_k = _rank(boundary_matrix(complex_obj, degree))
    next_factors = _smith_normal_form(boundary_matrix(complex_obj, degree + 1))
    rank_k_plus_1 = len(next_factors)
    betti = (n_k - rank_k) - rank_k_plus_1
    torsion = tuple(factor for factor in next_factors if factor > 1)
    return HomologyResult(degree=degree, betti=betti, torsion=torsion)


def homology_groups(complex_obj: SimplicialComplex) -> tuple[HomologyResult, ...]:
    """Return ``H_0, ..., H_dim`` of ``complex_obj``."""

    return tuple(
        simplicial_homology(complex_obj, degree)
        for degree in range(complex_obj.dimension + 1)
    )


def betti_numbers(complex_obj: SimplicialComplex) -> tuple[int, ...]:
    """Return ``(b_0, ..., b_dim)``, the ranks of the integral homology groups."""

    return tuple(group.betti for group in homology_groups(complex_obj))


def reduced_homology(complex_obj: SimplicialComplex, degree: int) -> HomologyResult:
    """Return reduced homology ``tilde H_degree(complex_obj; Z)``.

    This agrees with ordinary homology except in degree zero, where the rank is
    reduced by one (so a connected complex has ``tilde H_0 = 0``).
    """

    ordinary = simplicial_homology(complex_obj, degree)
    if degree != 0:
        return ordinary
    return HomologyResult(degree=0, betti=max(ordinary.betti - 1, 0), torsion=ordinary.torsion)


def euler_characteristic_via_homology(complex_obj: SimplicialComplex) -> int:
    """Return the Euler characteristic as the alternating sum of Betti numbers.

    By the Euler-Poincare theorem this equals the combinatorial alternating sum
    of face counts (``SimplicialComplex.euler_characteristic``); the equality is
    a useful cross-check that the homology computation is consistent.
    """

    return sum(((-1) ** degree) * betti for degree, betti in enumerate(betti_numbers(complex_obj)))


__all__ = [
    "HomologyResult",
    "boundary_matrix",
    "simplicial_homology",
    "homology_groups",
    "betti_numbers",
    "reduced_homology",
    "euler_characteristic_via_homology",
]
