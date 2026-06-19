"""Čech complex filtration for persistent homology.

The Čech complex C(X, r) at scale r contains a simplex {x_0, ..., x_k} iff
the k+1 balls of radius r centred at the x_i have a common point (equivalently,
iff the minimum enclosing ball of {x_0, ..., x_k} has radius ≤ r).  The birth
time of a simplex is therefore its *circumradius* — the radius of the minimum
enclosing ball of its vertices.

Key relations
-------------
C(X, r) ⊆ VR(X, 2r) ⊆ C(X, 2r)   (Rips–Čech sandwich lemma)
|C(X, r)| ≃ ∪_i B(x_i, r)         (Nerve theorem → homotopy equivalence)

Because every edge in Čech enters at half its length, the Čech filtration
produces smaller complexes for the same topological information than Rips at
the same scale.

Public API
----------
cech_filtration          — build FilteredComplex from a list of R^d points
persistent_homology_cech — convenience wrapper (filtration → pairs)

References
----------
Edelsbrunner, H. & Harer, J. (2010). *Computational Topology*, Ch. III.2.
Boissonnat, J.-D., Chazal, F., & Yvinec, M. (2018). *Geometric and Topological
    Inference*, Ch. 3.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from itertools import combinations

from .persistent_homology import FilteredComplex, PersistencePair, persistence_pairs

# ---------------------------------------------------------------------------
# Pure-Python linear algebra helpers (no numpy)
# ---------------------------------------------------------------------------

_Pt = tuple[float, ...]


def _dot(u: _Pt, v: _Pt) -> float:
    return sum(a * b for a, b in zip(u, v))


def _norm2(v: _Pt) -> float:
    return sum(a * a for a in v)


def _sub(u: _Pt, v: _Pt) -> _Pt:
    return tuple(a - b for a, b in zip(u, v))


def _add_scaled(base: list[float], scale: float, delta: _Pt) -> None:
    for j, d in enumerate(delta):
        base[j] += scale * d


def _gauss(A: list[list[float]], b: list[float]) -> list[float] | None:
    """Solve A x = b via Gaussian elimination with partial pivoting.

    Returns None if the system is singular (degenerate simplex).
    """
    n = len(b)
    # Augmented matrix
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        # Pivot
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < 1e-12:
            return None
        M[col], M[pivot_row] = M[pivot_row], M[col]
        inv = 1.0 / M[col][col]
        for row in range(col + 1, n):
            factor = M[row][col] * inv
            for k in range(col, n + 1):
                M[row][k] -= factor * M[col][k]
    # Back-substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n]
        for j in range(i + 1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]
    return x


# ---------------------------------------------------------------------------
# Circumsphere via least-squares (exact for affinely independent points)
# ---------------------------------------------------------------------------


def _circumsphere(boundary: list[_Pt]) -> tuple[_Pt | None, float]:
    """Return the (centre, radius) of the unique sphere through ``boundary``.

    - 0 points → (None, -1.0)  — empty ball sentinel
    - 1 point  → (p, 0.0)
    - 2 points → midpoint ball
    - k+1 points in R^d → solve the linear system from the circumscribed-
      sphere equations; falls back to (k)-point circumsphere if degenerate.
    """
    if not boundary:
        return None, -1.0
    if len(boundary) == 1:
        return boundary[0], 0.0
    if len(boundary) == 2:
        p0, p1 = boundary
        centre: _Pt = tuple((a + b) / 2.0 for a, b in zip(p0, p1))
        return centre, math.sqrt(max(0.0, _norm2(_sub(p0, centre))))

    p0 = boundary[0]
    k = len(boundary) - 1

    # A[i] = p_{i+1} - p_0
    A = [_sub(boundary[i + 1], p0) for i in range(k)]
    # b[i] = ||A[i]||² / 2  (from expanding ||c - p_i||² = ||c - p_0||²)
    rhs = [_norm2(A[i]) / 2.0 for i in range(k)]
    # Gram matrix G[i][j] = A[i]·A[j]
    G = [[_dot(A[i], A[j]) for j in range(k)] for i in range(k)]

    lam = _gauss(G, rhs)
    if lam is None:
        # Affinely dependent — fall back to one fewer point
        return _circumsphere(boundary[:-1])

    # centre = p0 + Σ λ_i * A[i]
    c = list(p0)
    for i in range(k):
        _add_scaled(c, lam[i], A[i])
    centre = tuple(c)
    radius = math.sqrt(max(0.0, _norm2(_sub(boundary[0], centre))))
    return centre, radius


# ---------------------------------------------------------------------------
# Welzl's minimum enclosing ball (randomised, in-place list slicing)
# ---------------------------------------------------------------------------


def _welzl(pts: list[_Pt], boundary: list[_Pt]) -> tuple[_Pt | None, float]:
    """Welzl's algorithm: minimum enclosing ball of ``pts`` with ``boundary``
    constrained to lie on the boundary sphere.

    The recursion terminates when:
    - pts is empty, or
    - |boundary| = d + 1 (a sphere in R^d is determined by d+1 points).
    """
    d = len(pts[0]) if pts else (len(boundary[0]) if boundary else 0)
    if not pts or len(boundary) == d + 1:
        return _circumsphere(boundary)

    pt = pts[0]
    centre, radius = _welzl(pts[1:], boundary)
    # Check if pt is already inside (with small tolerance for floating point)
    if centre is not None and _norm2(_sub(pt, centre)) <= (radius + 1e-10) ** 2:
        return centre, radius

    return _welzl(pts[1:], boundary + [pt])


def _circumradius(points: Sequence[_Pt]) -> float:
    """Minimum enclosing ball radius of a finite set of points in R^d."""
    pts = list(points)
    if not pts:
        return 0.0
    if len(pts) == 1:
        return 0.0
    # Randomise to achieve expected O(d! · n) time
    import random
    random.shuffle(pts)
    _, r = _welzl(pts, [])
    return r


# ---------------------------------------------------------------------------
# Čech filtration
# ---------------------------------------------------------------------------


def cech_filtration(
    points: Sequence[Sequence[float]],
    max_dimension: int = 1,
    max_scale: float | None = None,
) -> FilteredComplex:
    """Build the Čech filtration of a finite point cloud in R^d.

    Parameters
    ----------
    points:
        A finite sequence of R^d points, each a sequence of ``d`` floats.
        All points must have the same dimension.
    max_dimension:
        Maximum simplex dimension to include (default 1 = graph skeleton).
    max_scale:
        Upper bound on circumradius; simplices born later are dropped.

    Returns
    -------
    FilteredComplex
        Filtration compatible with :func:`.persistence_pairs` and all other
        pytop persistence pipelines.

    Notes
    -----
    Time complexity is O(n^{k+1}) for generating k-simplices.  For small
    point clouds (n ≤ 50) and max_dimension ≤ 2 this is fast; for larger
    inputs consider Rips or an alpha complex.

    The Rips–Čech sandwich: each edge enters Čech at *half* its Euclidean
    length (versus the full length in Rips).
    """
    if max_dimension < 0:
        raise ValueError("max_dimension must be nonneg.")
    pts: list[_Pt] = [tuple(float(x) for x in p) for p in points]
    n = len(pts)
    if n == 0:
        raise ValueError("cech_filtration requires at least one point.")

    # 0-simplices always enter at radius 0
    entries: list[tuple[float, int, tuple[int, ...]]] = [
        (0.0, 0, (i,)) for i in range(n)
    ]

    for k in range(1, max_dimension + 1):
        for combo in combinations(range(n), k + 1):
            verts = [pts[i] for i in combo]
            r = _circumradius(verts)
            if max_scale is not None and r > max_scale:
                continue
            entries.append((r, k, combo))

    entries.sort(key=lambda e: (e[0], e[1], e[2]))
    return FilteredComplex(
        simplices=tuple(e[2] for e in entries),
        births=tuple(e[0] for e in entries),
        dimensions=tuple(e[1] for e in entries),
    )


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------


def persistent_homology_cech(
    points: Sequence[Sequence[float]],
    max_dimension: int = 1,
    max_scale: float | None = None,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistent homology of a point cloud via the Čech filtration.

    A convenience wrapper around :func:`cech_filtration` and
    :func:`.persistence_pairs`.

    Parameters
    ----------
    points:
        Finite point cloud in R^d.
    max_dimension:
        Maximum homological degree to compute.
    max_scale:
        Truncate filtration at this circumradius.
    include_zero_persistence:
        Whether to include degenerate (birth == death) pairs.

    Returns
    -------
    tuple[PersistencePair, ...]
        Persistence pairs sorted by (dimension, birth, death).

    Examples
    --------
    Six points on the unit circle in R^2 — expect one essential H_0 bar and
    one long H_1 bar close to radius 0.5:

    >>> import math
    >>> pts = [(math.cos(2*math.pi*i/6), math.sin(2*math.pi*i/6)) for i in range(6)]
    >>> pairs = persistent_homology_cech(pts, max_dimension=2)
    >>> essential = [p for p in pairs if p.is_essential]
    >>> len(essential) >= 2  # one H_0, one H_1
    True
    """
    fc = cech_filtration(points, max_dimension=max_dimension, max_scale=max_scale)
    return persistence_pairs(fc, include_zero_persistence=include_zero_persistence)
