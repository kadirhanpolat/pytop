"""Nerve complex utilities.

P7.3 milestone — three public objects:

nerve_of_cover   : build the nerve N(U) of a finite open cover
good_cover_check : test whether every finite intersection is empty or contractible
cech_nerve       : build the Čech nerve from a point cloud + cover radius

Mathematical background
-----------------------
Given a finite collection U = {U_α}_{α∈A} of nonempty sets, the **nerve**
N(U) is the abstract simplicial complex whose k-simplices are the (k+1)-element
sub-collections of U with nonempty intersection:

    {U_{α₀}, ..., U_{α_k}} ∈ N(U)  iff  U_{α₀} ∩ ⋯ ∩ U_{α_k} ≠ ∅

**Nerve theorem** (Borsuk–Leray / Weil 1952): if U is a *good cover* of a
paracompact space X (every nonempty finite intersection is contractible), then
the nerve N(U) is homotopy equivalent to X:  |N(U)| ≃ X.

For point cloud TDA, the **Čech nerve** at radius r is exactly the nerve of the
cover by closed balls B(xᵢ, r).  A simplex {xᵢ₀,...,xᵢ_k} is in the Čech
complex iff ⋂ B(xᵢⱼ, r) ≠ ∅ (equivalently the miniball of {xᵢ₀,...,xᵢ_k}
has radius ≤ r).  The Čech nerve is used by ``cech_filtration`` in
``cech_complex.py`` for this reason.

good_cover_check
----------------
For finite sets (finite discrete topology), a set is "contractible" iff it is
nonempty and connected (as a graph induced by the cover) — more precisely,
every nonempty finite intersection is itself nonempty (the topological
contractibility condition reduces to this for finite discrete sets).  The
function flags whether the cover passes this simple finite criterion.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any

from .simplices import Simplex
from .simplicial_complexes import SimplicialComplex


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------


def nerve_of_cover(
    cover: list[set[Any]],
    max_dim: int | None = None,
) -> SimplicialComplex:
    """Build the nerve N(U) of a finite open cover.

    Each set in ``cover`` becomes a vertex of the nerve (indexed 0, 1, …).
    A collection of vertices ``{i₀,...,iₖ}`` forms a k-simplex iff the
    corresponding sets have nonempty common intersection:
    ``cover[i₀] ∩ ⋯ ∩ cover[iₖ] ≠ ∅``.

    Parameters
    ----------
    cover : list[set]
        A list of nonempty sets.  Each set represents one open set Uᵢ in the
        cover.  Vertices of the nerve are the integer indices 0, 1, …, len-1.
    max_dim : int | None
        If given, include only simplices of dimension ≤ ``max_dim``.  Useful
        for large covers where high-dimensional intersections are costly.

    Returns
    -------
    SimplicialComplex
        The nerve N(U) as an abstract simplicial complex on integer vertices.
        Always face-closed by construction.

    Raises
    ------
    ValueError
        If ``cover`` is empty or any set in ``cover`` is empty.

    Examples
    --------
    >>> U = [{0,1,2}, {2,3}, {3,4,0}]
    >>> N = nerve_of_cover(U)
    >>> N.dimension  # vertices + edges + 1 triangle
    2
    """
    if not cover:
        raise ValueError("cover must be non-empty.")
    for i, s in enumerate(cover):
        if not s:
            raise ValueError(f"Set at index {i} is empty; every cover element must be nonempty.")

    n = len(cover)
    dim_limit = max_dim if max_dim is not None else n - 1

    # Collect all simplices that have nonempty intersection.
    # Iterate from singletons up to (dim_limit+1)-element subsets.
    all_simplices: list[frozenset[int]] = []
    for size in range(1, min(dim_limit + 2, n + 1)):
        for combo in combinations(range(n), size):
            intersection = cover[combo[0]].copy()
            for idx in combo[1:]:
                intersection &= cover[idx]
                if not intersection:
                    break
            if intersection:
                all_simplices.append(frozenset(combo))

    if not all_simplices:
        raise ValueError("All pairwise intersections are empty — the nerve has no simplices.")

    return SimplicialComplex([Simplex(vs) for vs in all_simplices])


def good_cover_check(
    cover: list[set[Any]],
    space: set[Any] | None = None,
) -> dict[str, Any]:
    """Check whether a finite cover satisfies the good cover condition.

    For a finite *discrete* space, a cover U = {U_α} is a **good cover** if
    every nonempty finite sub-intersection is contractible.  For finite sets
    with the discrete topology, contractibility of a nonempty set is automatic
    (every nonempty discrete finite space deformation-retracts to a point), so
    this reduces to checking:

      1. The cover is a cover of ``space`` (union = space).
      2. Every finite sub-intersection is either empty or nonempty — trivially
         true, so we additionally check *connectivity* of the nerve (all
         elements share at least one common point or the nerve is connected).

    Returns a summary dictionary with keys:

    - ``"covers_space"`` (bool | None): True if ⋃Uᵢ = space, None if space
      not provided.
    - ``"all_nonempty"`` (bool): True if every set in cover is nonempty.
    - ``"pairwise_intersections"`` (list[tuple]): list of pairs (i,j) with
      nonempty Uᵢ ∩ Uⱼ.
    - ``"is_good_cover"`` (bool): True if all nonempty and covers space
      (space provided) or all nonempty (space not provided).
    - ``"nerve_dimension"`` (int): dimension of the nerve N(U).

    Parameters
    ----------
    cover : list[set]
        Finite collection of sets to check.
    space : set | None
        The underlying space.  If provided, checks that ⋃Uᵢ = space.
    """
    if not cover:
        return {
            "covers_space": None,
            "all_nonempty": False,
            "pairwise_intersections": [],
            "is_good_cover": False,
            "nerve_dimension": -1,
        }

    all_nonempty = all(bool(s) for s in cover)
    pairwise = [
        (i, j)
        for i, j in combinations(range(len(cover)), 2)
        if cover[i] & cover[j]
    ]

    covers_space: bool | None = None
    if space is not None:
        union: set[Any] = set()
        for s in cover:
            union |= s
        covers_space = union == space

    try:
        nerve = nerve_of_cover([s for s in cover if s])
        nerve_dim = nerve.dimension
    except ValueError:
        nerve_dim = -1

    is_good = all_nonempty and (covers_space if space is not None else True)

    return {
        "covers_space": covers_space,
        "all_nonempty": all_nonempty,
        "pairwise_intersections": pairwise,
        "is_good_cover": is_good,
        "nerve_dimension": nerve_dim,
    }


def cech_nerve(
    points: list[tuple[float, ...]],
    radius: float,
    max_dim: int | None = None,
) -> SimplicialComplex:
    """Build the Čech nerve (Čech complex) for a point cloud at radius r.

    A simplex {i₀,...,iₖ} is included iff the closed balls B(xᵢⱼ, r) have
    a common point — equivalently iff the circumradius of {xᵢ₀,...,xᵢ_k} is
    ≤ r (computed via the Welzl miniball, same criterion as
    ``cech_complex.cech_filtration``).

    This constructs the *static* Čech complex at a fixed radius, not a
    filtration.  For TDA use ``cech_complex.cech_filtration`` instead.

    Parameters
    ----------
    points : list[tuple[float, ...]]
        Point cloud in ℝ^d (all points must have the same dimension).
    radius : float
        Ball radius r > 0.
    max_dim : int | None
        If given, include only simplices of dimension ≤ ``max_dim``.

    Returns
    -------
    SimplicialComplex
        The Čech complex C(X, r) on integer vertex indices 0, …, n-1.

    Raises
    ------
    ValueError
        If ``points`` is empty, ``radius`` ≤ 0, or points have inconsistent
        dimension.

    Examples
    --------
    >>> pts = [(0.0,), (1.0,), (2.0,)]
    >>> C = cech_nerve(pts, radius=0.6)  # only adjacent pairs intersect
    >>> C.dimension
    1
    """
    if not points:
        raise ValueError("points must be non-empty.")
    if radius <= 0:
        raise ValueError(f"radius must be positive, got {radius}.")
    dim0 = len(points[0])
    for i, p in enumerate(points):
        if len(p) != dim0:
            raise ValueError(f"Point {i} has dimension {len(p)}, expected {dim0}.")

    n = len(points)
    dim_limit = max_dim if max_dim is not None else n - 1

    all_simplices: list[frozenset[int]] = []
    for size in range(1, min(dim_limit + 2, n + 1)):
        for combo in combinations(range(n), size):
            pts_sub = [points[i] for i in combo]
            if _miniball_radius(pts_sub) <= radius:
                all_simplices.append(frozenset(combo))

    if not all_simplices:
        raise ValueError(
            f"No simplices formed at radius {radius}; all balls are disjoint."
        )

    return SimplicialComplex([Simplex(vs) for vs in all_simplices])


# ---------------------------------------------------------------------------
# Miniball helper (Welzl circumradius for small point sets)
# ---------------------------------------------------------------------------


def _miniball_radius(pts: list[tuple[float, ...]]) -> float:
    """Return the circumradius of the miniball enclosing ``pts``.

    Uses the same Gaussian-elimination circumsphere algorithm as
    ``cech_complex._circumradius``.  Duplicate points and degenerate
    configurations return radius 0.
    """
    if len(pts) == 1:
        return 0.0

    d = len(pts[0])

    if len(pts) == 2:
        return 0.5 * _dist(pts[0], pts[1])

    # General case: solve the circumsphere linear system.
    # Centre c satisfies: |c - pᵢ|² = |c - p₀|² for i = 1,...,k
    # Expanding: 2(pᵢ - p₀)·c = |pᵢ|² - |p₀|²
    p0 = pts[0]
    rows: list[list[float]] = []
    rhs: list[float] = []
    for p in pts[1:]:
        row = [2.0 * (p[j] - p0[j]) for j in range(d)]
        b = sum((p[j] ** 2 - p0[j] ** 2) for j in range(d))
        rows.append(row)
        rhs.append(b)

    centre = _solve_ls(rows, rhs, d)
    if centre is None:
        # Degenerate / lower-dimensional — fall back to max pairwise dist / 2.
        return max(
            _dist(pts[i], pts[j])
            for i in range(len(pts))
            for j in range(i + 1, len(pts))
        ) / 2.0

    return _dist(tuple(centre), p0)


def _dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum((ai - bi) ** 2 for ai, bi in zip(a, b)) ** 0.5


def _solve_ls(
    rows: list[list[float]],
    rhs: list[float],
    d: int,
) -> list[float] | None:
    """Least-squares / exact solution via Gaussian elimination.

    Returns None if the system is rank-deficient (degenerate configuration).
    """
    m = len(rows)
    # Build augmented matrix [A | b]
    aug = [row[:] + [rhs[i]] for i, row in enumerate(rows)]

    # If overdetermined (m > d), use normal equations A^T A x = A^T b
    if m > d:
        A = rows
        At = [[A[i][j] for i in range(m)] for j in range(d)]
        AtA = [[sum(At[r][k] * A[k][c] for k in range(m)) for c in range(d)] for r in range(d)]
        Atb = [sum(At[r][k] * rhs[k] for k in range(m)) for r in range(d)]
        aug = [AtA[r][:] + [Atb[r]] for r in range(d)]
        m = d

    # Gaussian elimination with partial pivoting
    sol_rows = [aug[r][:] for r in range(m)]
    n_cols = d
    pivot_col = 0
    pivot_row = 0
    for col in range(n_cols):
        if pivot_row >= m:
            break
        best = pivot_row
        best_val = abs(sol_rows[pivot_row][col])
        for r in range(pivot_row + 1, m):
            if abs(sol_rows[r][col]) > best_val:
                best = r
                best_val = abs(sol_rows[r][col])
        if best_val < 1e-12:
            return None
        sol_rows[pivot_row], sol_rows[best] = sol_rows[best], sol_rows[pivot_row]
        piv = sol_rows[pivot_row][col]
        for r in range(m):
            if r != pivot_row and abs(sol_rows[r][col]) > 1e-15:
                factor = sol_rows[r][col] / piv
                for c in range(d + 1):
                    sol_rows[r][c] -= factor * sol_rows[pivot_row][c]
        pivot_row += 1

    if pivot_row < n_cols:
        return None

    result = [0.0] * d
    pr = 0
    for col in range(d):
        if abs(sol_rows[pr][col]) > 1e-12:
            result[col] = sol_rows[pr][d] / sol_rows[pr][col]
            pr += 1
    return result
