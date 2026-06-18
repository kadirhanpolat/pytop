"""Cubical homology and persistent homology for cubical complexes.

Mathematical background
-----------------------
A **cubical complex** in ℤⁿ is a finite collection of *elementary cubes*
(products of elementary intervals) that is closed under taking faces.  An
*elementary interval* is either a degenerate point [k, k] or a unit segment
[k, k+1] for some integer k.  An *elementary cube* of dimension d is a
product I₁ × ⋯ × Iₙ where exactly d of the Iᵢ are non-degenerate.

Boundary operator (over ℤ, with signs)
---------------------------------------
For Q = I₁ × ⋯ × Iₙ with non-degenerate intervals at positions p₁ < ⋯ < pₖ:

    ∂Q = Σⱼ₌₀^{k-1} (-1)^j  ×  [right-face at pⱼ  −  left-face at pⱼ]

where the right/left face at position p replaces Iₚ = [a, a+1] with [a+1, a+1]
/ [a, a] respectively.  This satisfies ∂² = 0.

Cubical homology
----------------
``cubical_homology(cx)`` computes H₀, H₁, …, Hₙ of a static
``CubicalComplex`` using the same Smith Normal Form engine as simplicial
homology.

Image persistence (lower-star cubical filtration)
-------------------------------------------------
Given a 2-D array of pixel values ``values[i][j]``:

* Each pixel (i, j) is a 2-cube [i, i+1] × [j, j+1] with birth = values[i][j].
* Faces (edges / vertices) are assigned birth = min of all adjacent pixel
  values.  This guarantees f(face) ≤ f(coface) — a valid filtration — and
  means that a face enters the filtration as soon as the *cheapest* pixel
  adjacent to it enters.

``bitmap_to_cubical_filtration(values)`` builds a ``CubicalFiltration``.
``persistent_homology_bitmap(values)`` is a one-call convenience that returns
the persistence pairs using the Twist+Clearing algorithm.

Public API
----------
Interval                        type alias for tuple[int, int]
Cube                            type alias for tuple[Interval, ...]
cube_dim(cube)                  → int
cube_faces_z2(cube)             → list[Cube]
cube_faces_signed(cube)         → list[tuple[int, Cube]]
CubicalComplex                  dataclass (cubes, dimension, k_cubes, …)
make_cubical_complex(top_cubes) → CubicalComplex  (closure under faces)
cubical_boundary_matrix(cx, k)  → list[list[int]]
cubical_homology(cx)            → tuple[HomologyResult, ...]
interval_complex(n)             → [0, n] as a cubical complex
circle_cubical(n)               → S¹ as n-square loop
disk_cubical()                  → D² = unit square
CubicalFiltration               dataclass
bitmap_to_cubical_filtration    → CubicalFiltration from 2-D image
persistence_pairs_cubical       → tuple[PersistencePair, ...]
persistent_homology_bitmap      → tuple[PersistencePair, ...]
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

from .homology import HomologyResult, _smith_normal_form
from .persistent_homology import PersistencePair
from .persistent_homology_optimized import ReductionStats, _twist_reduce


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

#: An elementary interval: (k, k) degenerate or (k, k+1) non-degenerate.
Interval = tuple[int, int]

#: An elementary cube: product of elementary intervals, one per axis.
Cube = tuple[Interval, ...]


# ---------------------------------------------------------------------------
# Elementary cube operations
# ---------------------------------------------------------------------------

def cube_dim(cube: Cube) -> int:
    """Return the dimension of *cube* (number of non-degenerate intervals)."""
    return sum(1 for left, right in cube if right != left)


def cube_faces_signed(cube: Cube) -> list[tuple[int, Cube]]:
    """Return ``(coefficient, face)`` pairs for all faces of *cube* (over ℤ).

    Uses the sign convention ∂Q = Σⱼ (-1)ʲ [right_face - left_face] where j
    counts non-degenerate intervals to the left of the current one.
    """
    result: list[tuple[int, Cube]] = []
    nd_count = 0  # number of non-degenerate intervals processed so far
    for i, (left, right) in enumerate(cube):
        if right == left:
            continue
        face_right: Cube = cube[:i] + ((right, right),) + cube[i + 1:]
        face_left: Cube = cube[:i] + ((left, left),) + cube[i + 1:]
        sign = (-1) ** nd_count
        result.append((sign, face_right))
        result.append((-sign, face_left))
        nd_count += 1
    return result


def cube_faces_z2(cube: Cube) -> list[Cube]:
    """Return all faces of *cube* as a list (over Z/2, no signs)."""
    result: list[Cube] = []
    for i, (left, right) in enumerate(cube):
        if right == left:
            continue
        result.append(cube[:i] + ((right, right),) + cube[i + 1:])
        result.append(cube[:i] + ((left, left),) + cube[i + 1:])
    return result


def _all_faces(cube: Cube) -> frozenset[Cube]:
    """Return the closure of *cube* under the face operator (including itself)."""
    result: set[Cube] = {cube}
    frontier = [cube]
    while frontier:
        next_frontier: list[Cube] = []
        for c in frontier:
            for face in cube_faces_z2(c):
                if face not in result:
                    result.add(face)
                    next_frontier.append(face)
        frontier = next_frontier
    return frozenset(result)


# ---------------------------------------------------------------------------
# CubicalComplex
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CubicalComplex:
    """A finite cubical complex: a set of elementary cubes closed under faces.

    Construct via :func:`make_cubical_complex`.
    """

    cubes: frozenset[Cube]

    @property
    def dimension(self) -> int:
        """Maximum dimension of any cube in the complex (−1 if empty)."""
        if not self.cubes:
            return -1
        return max(cube_dim(c) for c in self.cubes)

    def k_cubes(self, k: int) -> list[Cube]:
        """Return the k-dimensional cubes in canonical (sorted) order."""
        return sorted(
            (c for c in self.cubes if cube_dim(c) == k),
            key=lambda c: tuple(x for pair in c for x in pair),
        )

    def euler_characteristic(self) -> int:
        """Alternating sum of cube counts by dimension."""
        chi = 0
        for k in range(self.dimension + 1):
            chi += (-1) ** k * len(self.k_cubes(k))
        return chi


def make_cubical_complex(top_cubes: Iterable[Cube]) -> CubicalComplex:
    """Build a :class:`CubicalComplex` as the face-closure of *top_cubes*."""
    all_cubes: set[Cube] = set()
    for c in top_cubes:
        all_cubes |= _all_faces(c)
    return CubicalComplex(frozenset(all_cubes))


# ---------------------------------------------------------------------------
# Boundary matrix and homology (over ℤ via Smith Normal Form)
# ---------------------------------------------------------------------------

def cubical_boundary_matrix(cx: CubicalComplex, k: int) -> list[list[int]]:
    """Return the integer boundary matrix ∂_k of *cx*.

    Rows are indexed by (k−1)-cubes, columns by k-cubes, both in canonical
    order.  Returns an empty matrix when k ≤ 0 or no k-cubes exist.

    .. warning::
        This function allocates a dense integer matrix of size
        ``#(k−1)-cubes × #k-cubes``.  For large cubical complexes derived
        from images (m×n > ~50×50 pixels), this can require hundreds of
        millions of entries and exhaust available memory.  For large images,
        consider using ``persistence_pairs_cubical`` (or
        ``persistent_homology_bitmap``) which avoids the full boundary matrix
        and runs the Twist+Clearing algorithm on sparse Z/2 columns instead.
    """
    if k <= 0:
        return []
    faces_k = cx.k_cubes(k - 1)
    cubes_k = cx.k_cubes(k)
    if not cubes_k:
        return [[0] * 0 for _ in faces_k]
    face_index = {c: idx for idx, c in enumerate(faces_k)}
    mat: list[list[int]] = [[0] * len(cubes_k) for _ in faces_k]
    for col, cube in enumerate(cubes_k):
        for coeff, face in cube_faces_signed(cube):
            row = face_index[face]
            mat[row][col] += coeff
    return mat


def cubical_homology(cx: CubicalComplex) -> tuple[HomologyResult, ...]:
    """Compute H₀, H₁, …, H_d of *cx* over ℤ using Smith Normal Form.

    Returns one :class:`~pytop.homology.HomologyResult` per degree from 0 to
    ``cx.dimension``.  The algorithm is identical to simplicial homology: SNF
    of ∂_k and ∂_{k+1} determines rank and torsion of H_k.

    .. warning::
        Internally calls :func:`cubical_boundary_matrix`, which allocates
        dense integer matrices.  For cubical complexes built from images larger
        than approximately 50×50 pixels, memory usage can become prohibitive
        (on the order of hundreds of millions of entries).  For large images,
        prefer ``persistence_pairs_cubical`` or ``persistent_homology_bitmap``
        which use a sparse Twist+Clearing algorithm and avoid the full boundary
        matrix.
    """
    if cx.dimension < 0:
        return ()

    def _rank(mat: list[list[int]]) -> int:
        return len(_smith_normal_form(mat)) if (mat and mat[0]) else 0

    results: list[HomologyResult] = []
    for k in range(cx.dimension + 1):
        dk = cubical_boundary_matrix(cx, k)
        dk1 = cubical_boundary_matrix(cx, k + 1)

        rank_dk = _rank(dk)
        ck_size = len(cx.k_cubes(k))
        kernel_dim = ck_size - rank_dk

        factors_dk1 = _smith_normal_form(dk1) if (dk1 and dk1[0]) else []
        image_rank = len(factors_dk1)
        torsion = tuple(d for d in factors_dk1 if d > 1)
        betti = kernel_dim - image_rank

        results.append(HomologyResult(degree=k, betti=betti, torsion=torsion))
    return tuple(results)


# ---------------------------------------------------------------------------
# Standard cubical spaces
# ---------------------------------------------------------------------------

def interval_complex(n: int = 1) -> CubicalComplex:
    """Return the interval [0, n] as a 1D cubical complex.

    H₀ = ℤ, H₁ = 0 (contractible).
    """
    if n < 0:
        raise ValueError("n must be nonnegative.")
    top_cubes: list[Cube] = [((i, i + 1),) for i in range(n)]
    return make_cubical_complex(top_cubes)


def circle_cubical(n: int = 4) -> CubicalComplex:
    """Return S¹ as an axis-aligned rectangular loop in the cubical grid.

    Builds the boundary of the rectangle [0, h] × [0, 1] where
    h = max(1, (n − 2) // 2).  This gives 2h + 2 unit edges.  For n = 4 this
    is the unit square; for larger n the rectangle grows horizontally.  In all
    cases the result is homeomorphic to S¹, so H₀ = ℤ, H₁ = ℤ.

    Parameters
    ----------
    n : int
        Approximate number of edges (n ≥ 4).  The actual edge count is
        2 * max(1, (n − 2) // 2) + 2, equal to n for even n ≥ 4.
    """
    if n < 4:
        raise ValueError("circle_cubical requires n ≥ 4.")
    h = max(1, (n - 2) // 2)
    top: list[Cube] = []
    # Bottom horizontal edges: [x, x+1] × [0, 0] for x in 0..h-1
    for x in range(h):
        top.append(((x, x + 1), (0, 0)))
    # Right vertical edge: [h, h] × [0, 1]
    top.append(((h, h), (0, 1)))
    # Top horizontal edges: [x, x+1] × [1, 1] for x in h-1..0
    for x in range(h - 1, -1, -1):
        top.append(((x, x + 1), (1, 1)))
    # Left vertical edge: [0, 0] × [0, 1]
    top.append(((0, 0), (0, 1)))
    return make_cubical_complex(top)


def disk_cubical() -> CubicalComplex:
    """Return D² as the filled unit square [0,1] × [0,1].

    H₀ = ℤ, H₁ = 0, H₂ = 0 (contractible).
    """
    return make_cubical_complex([((0, 1), (0, 1))])


def sphere_cubical_1d() -> CubicalComplex:
    """Alias for :func:`circle_cubical`."""
    return circle_cubical(4)


# ---------------------------------------------------------------------------
# Cubical filtration for persistent homology
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CubicalFiltration:
    """A filtration of elementary cubes ordered by birth value.

    Constructed by :func:`bitmap_to_cubical_filtration`.  Passed to
    :func:`persistence_pairs_cubical`.

    Attributes
    ----------
    cubes : tuple[Cube, ...]
        Cubes in filtration order (birth non-decreasing, faces before cofaces
        at equal birth).
    births : tuple[float, ...]
        Filtration value (birth time) of each cube.
    dimensions : tuple[int, ...]
        Dimension of each cube.
    """

    cubes: tuple[Cube, ...]
    births: tuple[float, ...]
    dimensions: tuple[int, ...]

    def size(self) -> int:
        return len(self.cubes)


def bitmap_to_cubical_filtration(
    values: Sequence[Sequence[float]],
) -> CubicalFiltration:
    """Build the lower-star cubical filtration of a 2-D pixel array.

    Each pixel ``values[i][j]`` becomes the 2-cube [i, i+1] × [j, j+1].
    The filtration value of any face Q is the *minimum* value among all pixels
    of which Q is a face.  This ensures f(face) ≤ f(coface) and means Q
    enters as soon as its cheapest adjacent pixel enters.

    Parameters
    ----------
    values:
        A 2-D sequence of shape (m, n) with m ≥ 1, n ≥ 1.

    Returns
    -------
    CubicalFiltration
        Cubes sorted by (birth, dimension) so faces always precede cofaces at
        equal birth.
    """
    m = len(values)
    if m == 0:
        raise ValueError("values must be nonempty.")
    n = len(values[0])
    if n == 0:
        raise ValueError("values rows must be nonempty.")

    def _adj_range(lo: int, hi: int, size: int) -> list[int]:
        """Pixel indices (along one axis) for which interval [lo, hi] is a face."""
        if lo == hi:  # degenerate point k
            return [i for i in (lo - 1, lo) if 0 <= i < size]
        else:         # non-degenerate [k, k+1]
            return [lo] if 0 <= lo < size else []

    def _birth(cube: Cube) -> float:
        rows = _adj_range(cube[0][0], cube[0][1], m)
        cols = _adj_range(cube[1][0], cube[1][1], n)
        adj = [values[r][c] for r in rows for c in cols]
        return float(min(adj)) if adj else 0.0

    # Build all cubes: vertices, horizontal edges, vertical edges, pixels.
    all_cubes: list[Cube] = []
    # Vertices
    for i in range(m + 1):
        for j in range(n + 1):
            all_cubes.append(((i, i), (j, j)))
    # Horizontal edges [i, i+1] × [j, j]
    for i in range(m):
        for j in range(n + 1):
            all_cubes.append(((i, i + 1), (j, j)))
    # Vertical edges [i, i] × [j, j+1]
    for i in range(m + 1):
        for j in range(n):
            all_cubes.append(((i, i), (j, j + 1)))
    # Pixels (2-cubes) [i, i+1] × [j, j+1]
    for i in range(m):
        for j in range(n):
            all_cubes.append(((i, i + 1), (j, j + 1)))

    # Assign birth values.
    cube_birth = [(_birth(c), cube_dim(c), c) for c in all_cubes]
    # Sort: birth ascending, then dimension ascending (faces before cofaces).
    cube_birth.sort(key=lambda x: (x[0], x[1]))

    cubes = tuple(x[2] for x in cube_birth)
    births = tuple(x[0] for x in cube_birth)
    dims = tuple(x[1] for x in cube_birth)
    return CubicalFiltration(cubes=cubes, births=births, dimensions=dims)


# ---------------------------------------------------------------------------
# Cubical persistent homology (Twist+Clearing over Z/2)
# ---------------------------------------------------------------------------

def _cubical_boundary_columns(
    filtration: CubicalFiltration,
) -> list[set[int]]:
    """Build Z/2 boundary columns for the cubical filtration."""
    index_of: dict[Cube, int] = {c: idx for idx, c in enumerate(filtration.cubes)}
    columns: list[set[int]] = []
    for cube, d in zip(filtration.cubes, filtration.dimensions):
        if d == 0:
            columns.append(set())
        else:
            columns.append({index_of[f] for f in cube_faces_z2(cube)})
    return columns


def persistence_pairs_cubical(
    filtration: CubicalFiltration,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistence pairs of a :class:`CubicalFiltration` over Z/2.

    Uses the Twist+Clearing algorithm — the same shared kernel as
    :func:`~pytop.persistent_homology_optimized.persistence_pairs_twist`.

    Parameters
    ----------
    filtration:
        Output of :func:`bitmap_to_cubical_filtration` or a custom
        :class:`CubicalFiltration`.
    include_zero_persistence:
        Whether to include bars with birth = death.

    Returns
    -------
    tuple[PersistencePair, ...]
        Sorted by ``(dimension, birth, death)``.
    """
    if filtration.size() == 0:
        return ()
    columns = _cubical_boundary_columns(filtration)
    pairs, _ = _twist_reduce(
        columns,
        filtration.dimensions,
        filtration.births,
        include_zero_persistence=include_zero_persistence,
    )
    return pairs


def persistent_homology_bitmap(
    values: Sequence[Sequence[float]],
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """One-call convenience: 2-D bitmap → cubical filtration → Twist persistence.

    Parameters
    ----------
    values:
        A 2-D array of pixel values with shape (m, n), m ≥ 1, n ≥ 1.
    include_zero_persistence:
        Whether to include zero-length bars.

    Returns
    -------
    tuple[PersistencePair, ...]
        Persistence pairs sorted by ``(dimension, birth, death)``.

    Examples
    --------
    >>> img = [[0.0, 1.0], [1.0, 2.0]]
    >>> pairs = persistent_homology_bitmap(img)
    >>> any(p.dimension == 0 and p.is_essential for p in pairs)
    True
    """
    filtration = bitmap_to_cubical_filtration(values)
    return persistence_pairs_cubical(filtration, include_zero_persistence=include_zero_persistence)


__all__ = [
    "Interval",
    "Cube",
    "cube_dim",
    "cube_faces_signed",
    "cube_faces_z2",
    "CubicalComplex",
    "make_cubical_complex",
    "cubical_boundary_matrix",
    "cubical_homology",
    "interval_complex",
    "circle_cubical",
    "disk_cubical",
    "sphere_cubical_1d",
    "CubicalFiltration",
    "bitmap_to_cubical_filtration",
    "persistence_pairs_cubical",
    "persistent_homology_bitmap",
]
