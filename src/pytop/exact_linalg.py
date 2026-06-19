"""Exact integer linear algebra: Smith normal form, rank, determinant, cokernel.

Pure-Python and exact (no floating point). These primitives back pytop's
homology, Dehn-surgery and Alexander engines; exposing them as a small public
core lets you compute the homology of your own integer chain complexes, the
order of a presented abelian group, or an exact determinant directly — and keeps
a single, well-tested implementation behind all of them.

Two independent exact routes meet here as a built-in cross-check: the rank and
torsion come from the **Smith normal form**, while :func:`integer_determinant`
uses fraction-free **Bareiss** elimination; for a full-rank square matrix the
determinant equals ``± ∏`` of the invariant factors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .homology import _smith_normal_form

__all__ = [
    "AbelianGroup",
    "smith_normal_form",
    "smith_normal_form_extended",
    "integer_rank",
    "integer_determinant",
    "cokernel",
    "cokernel_generators",
]


# ---------------------------------------------------------------------------
# Finitely generated abelian group
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AbelianGroup:
    """A finitely generated abelian group ``ℤ^{free_rank} ⊕ ⊕ ℤ/dᵢ``.

    ``torsion`` lists the invariant factors ``dᵢ > 1`` with ``d₁ | d₂ | …``.
    """

    free_rank: int
    torsion: tuple[int, ...] = field(default=())

    @property
    def order(self) -> int | None:
        """``|G|`` if finite (``free_rank == 0``), else ``None``."""
        if self.free_rank > 0:
            return None
        product = 1
        for d in self.torsion:
            product *= d
        return product

    @property
    def is_trivial(self) -> bool:
        return self.free_rank == 0 and not self.torsion

    def __str__(self) -> str:
        parts: list[str] = []
        if self.free_rank == 1:
            parts.append("Z")
        elif self.free_rank > 1:
            parts.append(f"Z^{self.free_rank}")
        parts.extend(f"Z/{d}" for d in self.torsion)
        return " + ".join(parts) if parts else "0"


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------


def smith_normal_form(matrix: list[list[int]]) -> list[int]:
    """Return the positive invariant factors ``[d₁, …, d_r]`` of an integer matrix.

    They satisfy ``d₁ | d₂ | … | d_r`` and ``r`` equals the rank; entries equal
    to one are retained, so ``rank = len(result)`` and the torsion coefficients
    are ``[d for d in result if d > 1]``.
    """

    return _smith_normal_form([list(row) for row in matrix])


def smith_normal_form_extended(
    matrix: list[list[int]],
) -> tuple[list[int], list[list[int]], list[list[int]]]:
    """Return ``(factors, P, Q)`` such that ``P @ matrix @ Q`` is in Smith normal form.

    The unimodular integer matrices ``P`` (rows×rows) and ``Q`` (cols×cols) satisfy
    ``P @ matrix @ Q = diag(d₁, …, d_r, 0, …, 0)`` where ``[d₁, …, d_r]`` is
    exactly the output of :func:`smith_normal_form`.  Both ``P`` and ``Q`` have
    integer determinant ±1, so the decomposition is exact over ℤ.

    This extended form is needed to:

    - Express homology bases in terms of the original simplices.
    - Solve integer linear systems ``Ax = b`` over ℤ.
    - Lift cokernel generators to explicit group elements.
    """
    from .mayer_vietoris import _snf_ext

    m = [list(map(int, row)) for row in matrix]
    D, P, _Pinv, Q, _Qinv = _snf_ext(m)
    r = min(len(D), len(D[0]) if D else 0)
    factors = [D[i][i] for i in range(r) if D[i][i] != 0]
    return factors, P, Q


def integer_rank(matrix: list[list[int]]) -> int:
    """Return the rank of an integer matrix (the number of invariant factors)."""

    return len(smith_normal_form(matrix))


def integer_determinant(matrix: list[list[Any]]) -> int:
    """Return the determinant of a square integer matrix.

    Uses fraction-free **Bareiss** elimination — every intermediate quotient is
    exact, so the result is an exact integer with no overflow or rounding.
    """

    rows = [[int(value) for value in row] for row in matrix]
    n = len(rows)
    if any(len(row) != n for row in rows):
        raise ValueError("integer_determinant requires a square matrix.")
    if n == 0:
        return 1

    sign = 1
    previous = 1
    for k in range(n - 1):
        if rows[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if rows[i][k] != 0), None)
            if swap is None:
                return 0
            rows[k], rows[swap] = rows[swap], rows[k]
            sign = -sign
        pivot = rows[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                rows[i][j] = (rows[i][j] * pivot - rows[i][k] * rows[k][j]) // previous
        previous = pivot
    return sign * rows[n - 1][n - 1]


def cokernel(matrix: list[list[int]]) -> AbelianGroup:
    """Return the cokernel ``ℤ^{cols} / (row lattice)`` as an :class:`AbelianGroup`.

    The rows of ``matrix`` are read as relations among ``cols`` generators (the
    standard presentation of a finitely generated abelian group).
    """

    rows = [list(row) for row in matrix]
    n_cols = len(rows[0]) if rows else 0
    if n_cols == 0:
        return AbelianGroup(free_rank=0, torsion=())
    factors = smith_normal_form(rows)
    free_rank = n_cols - len(factors)
    torsion = tuple(d for d in factors if d > 1)
    return AbelianGroup(free_rank=free_rank, torsion=torsion)


def cokernel_generators(
    matrix: list[list[int]],
) -> tuple[AbelianGroup, list[list[int]]]:
    """Return ``(group, generators)`` for the cokernel ``ℤ^n / im(matrix)``.

    The rows of ``matrix`` present relations among ``n = cols`` generators.
    This function returns:

    - ``group``:      the same :class:`AbelianGroup` as :func:`cokernel`.
    - ``generators``: a list of integer vectors in ``ℤ^n``, one per summand of
      ``group``, ordered as ``[free generators…, torsion generators…]``.
      Each free generator ``g`` satisfies ``matrix @ g ≡ 0 (mod 1)`` (i.e. lies
      in the kernel of the map ``ℤ^n → ℤ^m`` encoded by ``matrix``).
      Each torsion generator ``g_i`` has order ``d_i`` in the cokernel (i.e.
      ``d_i · g_i`` is in the image of ``matrix``).

    The generators are the columns of ``Q⁻¹`` (the inverse right-transformation
    matrix from the extended Smith normal form) corresponding to the non-unit
    and zero diagonal positions.

    Example
    -------
    >>> group, gens = cokernel_generators([[2, 0], [0, 6]])
    >>> str(group)
    'Z/2 + Z/6'
    >>> len(gens)   # one torsion generator per summand
    2
    """
    from .mayer_vietoris import _snf_ext

    m = [list(map(int, row)) for row in matrix]
    n_cols = len(m[0]) if m else 0
    if n_cols == 0:
        return AbelianGroup(free_rank=0, torsion=()), []

    D, _P, _Pinv, _Q, Qinv = _snf_ext(m)
    r = min(len(D), n_cols)
    factors = [D[i][i] for i in range(r) if D[i][i] != 0]

    free_rank = n_cols - len(factors)
    torsion = tuple(d for d in factors if d > 1)
    group = AbelianGroup(free_rank=free_rank, torsion=torsion)

    # Columns of Qinv^T (= rows of Qinv) in SNF basis correspond to summands.
    # Columns of Q^{-1} that correspond to: free part (zero diagonal) first,
    # then torsion part (d_i > 1 diagonal positions), then trivial (d_i = 1).
    # We pick columns of Qinv (= Q^{-T}) matching the non-trivial summands.
    # Qinv rows give the coordinate change; column j of Q^{-1} = row j of Qinv^T.
    # Equivalently: the j-th column of Q^{-1} is the j-th column extracted from Qinv transposed.
    # Simpler: Qinv[j] is the j-th row of Q^{-1}, giving coordinates in ℤ^n for summand j.

    generators: list[list[int]] = []
    # Free generators (columns beyond rank)
    for j in range(len(factors), n_cols):
        generators.append(list(Qinv[j]))
    # Torsion generators (columns with d_i > 1)
    for j, d in enumerate(factors):
        if d > 1:
            generators.append(list(Qinv[j]))

    return group, generators
