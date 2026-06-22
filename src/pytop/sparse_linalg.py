"""Sparse integer linear algebra for large, sparse boundary matrices.

Provides a dict-based sparse integer matrix and a sparse-aware Smith normal
form that avoids O(m×n) dense allocation when most entries are zero — the
typical case for Khovanov and Vietoris–Rips boundary matrices.

Optional scipy.sparse integration: :func:`sparse_smith_normal_form` accepts a
``scipy.sparse`` matrix as input (any format) and converts it internally.
"""

from __future__ import annotations

from collections import defaultdict

__all__ = [
    "sparse_smith_normal_form",
    "matrix_density",
]

# Thresholds for automatic routing in homology._smith_normal_form.
# A matrix is routed through the sparse path when BOTH conditions hold:
#   min(rows, cols) >= _SPARSE_MIN_DIM  AND  density < _SPARSE_MAX_DENSITY
SPARSE_MIN_DIM: int = 30
SPARSE_MAX_DENSITY: float = 0.30


# ---------------------------------------------------------------------------
# Internal mutable sparse matrix (row + col adjacency dicts)
# ---------------------------------------------------------------------------


class _SparseMat:
    """Mutable sparse integer matrix with dual row/col adjacency dicts.

    Invariant: _r[i][j] == v iff _c[j][i] == v iff v != 0.
    """

    __slots__ = ("nrows", "ncols", "_r", "_c")

    def __init__(self, nrows: int, ncols: int) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self._r: dict[int, dict[int, int]] = defaultdict(dict)
        self._c: dict[int, dict[int, int]] = defaultdict(dict)

    @classmethod
    def from_dense(cls, matrix: list[list[int]]) -> "_SparseMat":
        m = len(matrix)
        n = len(matrix[0]) if m else 0
        mat = cls(m, n)
        for i, row in enumerate(matrix):
            for j, v in enumerate(row):
                if v != 0:
                    mat._r[i][j] = v
                    mat._c[j][i] = v
        return mat

    def get(self, i: int, j: int) -> int:
        ri = self._r.get(i)
        return ri[j] if ri is not None and j in ri else 0

    def _put(self, i: int, j: int, v: int) -> None:
        if v == 0:
            ri = self._r.get(i)
            if ri is not None:
                ri.pop(j, None)
                if not ri:
                    del self._r[i]
            ci = self._c.get(j)
            if ci is not None:
                ci.pop(i, None)
                if not ci:
                    del self._c[j]
        else:
            self._r.setdefault(i, {})[j] = v
            self._c.setdefault(j, {})[i] = v

    def swap_rows(self, a: int, b: int) -> None:
        if a == b:
            return
        ra = dict(self._r.get(a, {}))
        rb = dict(self._r.get(b, {}))
        # Remove a, b from all affected _c entries
        for j in ra:
            ci = self._c.get(j)
            if ci is not None:
                ci.pop(a, None)
                if not ci:
                    del self._c[j]
        for j in rb:
            ci = self._c.get(j)
            if ci is not None:
                ci.pop(b, None)
                if not ci:
                    del self._c[j]
        # Clear _r[a], _r[b]
        self._r.pop(a, None)
        self._r.pop(b, None)
        # Write ra → row b, rb → row a
        if ra:
            self._r[b] = ra
            for j, v in ra.items():
                self._c.setdefault(j, {})[b] = v
        if rb:
            self._r[a] = rb
            for j, v in rb.items():
                self._c.setdefault(j, {})[a] = v

    def swap_cols(self, a: int, b: int) -> None:
        if a == b:
            return
        ca = dict(self._c.get(a, {}))
        cb = dict(self._c.get(b, {}))
        for i in ca:
            ri = self._r.get(i)
            if ri is not None:
                ri.pop(a, None)
                if not ri:
                    del self._r[i]
        for i in cb:
            ri = self._r.get(i)
            if ri is not None:
                ri.pop(b, None)
                if not ri:
                    del self._r[i]
        self._c.pop(a, None)
        self._c.pop(b, None)
        if ca:
            self._c[b] = ca
            for i, v in ca.items():
                self._r.setdefault(i, {})[b] = v
        if cb:
            self._c[a] = cb
            for i, v in cb.items():
                self._r.setdefault(i, {})[a] = v

    def add_row(self, src: int, dst: int, factor: int) -> None:
        """``dst_row += factor * src_row`` (in-place)."""
        if factor == 0:
            return
        for j, v in list(self._r.get(src, {}).items()):
            self._put(dst, j, self.get(dst, j) + factor * v)

    def add_col(self, src: int, dst: int, factor: int) -> None:
        """``dst_col += factor * src_col`` (in-place)."""
        if factor == 0:
            return
        for i, v in list(self._c.get(src, {}).items()):
            self._put(i, dst, self.get(i, dst) + factor * v)


# ---------------------------------------------------------------------------
# Sparse Smith Normal Form
# ---------------------------------------------------------------------------


def _sparse_snf_inner(mat: _SparseMat) -> list[int]:
    """Core SNF algorithm on a _SparseMat; mirrors _smith_normal_form_python."""
    nrows, ncols = mat.nrows, mat.ncols
    invariants: list[int] = []
    t = 0

    while t < min(nrows, ncols):
        # Find smallest-magnitude nonzero in the active submatrix [t:, t:].
        pivot: tuple[int, int] | None = None
        best = 0
        for i, row in mat._r.items():
            if i < t:
                continue
            for j, v in row.items():
                if j < t:
                    continue
                if pivot is None or abs(v) < best:
                    pivot = (i, j)
                    best = abs(v)

        if pivot is None:
            break

        mat.swap_rows(t, pivot[0])
        mat.swap_cols(t, pivot[1])

        # Clear pivot row and column; retry when a swap is forced.
        cleared = False
        while not cleared:
            cleared = True
            pv = mat.get(t, t)

            # Eliminate col t (all rows i ≠ t).
            for i in list(mat._c.get(t, {}).keys()):
                if i == t:
                    continue
                v = mat.get(i, t)
                if v == 0:
                    continue
                mat.add_row(t, i, -(v // pv))
                if mat.get(i, t) != 0:
                    mat.swap_rows(t, i)
                    pv = mat.get(t, t)
                    cleared = False

            # Eliminate row t (all cols j ≠ t).
            for j in list(mat._r.get(t, {}).keys()):
                if j == t:
                    continue
                v = mat.get(t, j)
                if v == 0:
                    continue
                mat.add_col(t, j, -(v // pv))
                if mat.get(t, j) != 0:
                    mat.swap_cols(t, j)
                    pv = mat.get(t, t)
                    cleared = False

        # Enforce divisibility: d_t must divide every entry of the submatrix.
        pv = mat.get(t, t)
        if pv == 0:
            break

        needs_restart = False
        for i, row in mat._r.items():
            if i <= t:
                continue
            for j, v in row.items():
                if j <= t:
                    continue
                if v % pv != 0:
                    mat.add_row(i, t, 1)
                    needs_restart = True
                    break
            if needs_restart:
                break

        if needs_restart:
            continue  # restart without incrementing t

        invariants.append(abs(pv))
        t += 1

    return invariants


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def matrix_density(matrix: list[list[int]]) -> float:
    """Return the fraction of nonzero entries in an integer matrix.

    Returns 0.0 for an empty matrix.
    """
    if not matrix or not matrix[0]:
        return 0.0
    total = len(matrix) * len(matrix[0])
    nonzero = sum(1 for row in matrix for v in row if v != 0)
    return nonzero / total


def sparse_smith_normal_form(matrix: object) -> list[int]:
    """Smith normal form invariant factors using a sparse integer representation.

    Accepts a dense ``list[list[int]]`` or any ``scipy.sparse`` matrix
    (converted to COO internally).  Equivalent in output to
    :func:`pytop.exact_linalg.smith_normal_form` but avoids O(m×n) work
    when most entries are zero.

    Returns a list ``[d₁, …, d_r]`` with ``d₁ | … | d_r`` and ``r = rank``;
    every invariant factor (including those equal to 1) is listed.
    """
    # Accept scipy sparse matrices.
    if hasattr(matrix, "toarray"):
        matrix = matrix.toarray().tolist()  # type: ignore[union-attr]

    rows: list[list[int]] = list(matrix)  # type: ignore[arg-type]
    if not rows or not rows[0]:
        return []

    mat = _SparseMat.from_dense([[int(v) for v in row] for row in rows])
    return _sparse_snf_inner(mat)
