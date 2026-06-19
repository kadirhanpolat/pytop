"""Simplicial filtration builders: static complexes and standard triangulations.

Provides two related utilities:

1. **Static filtration** — convert any simplicial complex (given as a set of
   maximal simplices or as an explicit face-closed list) into a
   :class:`.FilteredComplex` where all simplices enter at birth=0.  The
   resulting filtration is valid (faces before cofaces, births nondecreasing)
   because sorting by dimension is sufficient when all births are 0.

2. **Standard triangulations** — minimal triangulations of well-known closed
   surfaces as :class:`.FilteredComplex` objects.  These are useful for
   cross-validating persistence algorithms against known homology groups, and
   for demonstrating torsion detection via :func:`.persistence_pairs_fp`::

       from pytop.simplicial_filtration import torus_filtration, klein_bottle_filtration
       from pytop.persistent_homology_fp import persistence_pairs_fp

       # Torus: H_0 = Z, H_1 = Z², H_2 = Z  (same for all primes)
       fc = torus_filtration()
       for p in [2, 3, 5]:
           pairs = persistence_pairs_fp(fc, prime=p)
           assert sum(1 for pp in pairs if pp.is_essential) == 4  # β_0+β_1+β_2

       # Klein bottle: H_1(K; Z) = Z ⊕ Z/2
       # Over F_2: β_1 = 2; over F_3: β_1 = 1 (torsion invisible)
       fc = klein_bottle_filtration()
       b1_f2 = sum(1 for pp in persistence_pairs_fp(fc, 2)
                   if pp.is_essential and pp.dimension == 1)
       b1_f3 = sum(1 for pp in persistence_pairs_fp(fc, 3)
                   if pp.is_essential and pp.dimension == 1)
       assert b1_f2 == 2 and b1_f3 == 1

Public API
----------
simplicial_filtration      — build FilteredComplex from explicit simplex list
torus_filtration           — 3×3 grid triangulation of T² (18 triangles)
klein_bottle_filtration    — 3×3 grid triangulation of K (18 triangles)
rp2_filtration             — minimal 6-vertex triangulation of RP² (10 triangles)
"""

from __future__ import annotations

from itertools import combinations

from .persistent_homology import FilteredComplex

# ---------------------------------------------------------------------------
# Generic static-complex builder
# ---------------------------------------------------------------------------


def simplicial_filtration(
    maximal_simplices: list[tuple[int, ...]],
) -> FilteredComplex:
    """Build a :class:`.FilteredComplex` from a list of maximal simplices.

    Parameters
    ----------
    maximal_simplices :
        A list of simplices (each a sorted tuple of non-negative integer
        vertex indices).  All faces are automatically included via closure.

    Returns
    -------
    FilteredComplex
        A static filtration (all births = 0.0) in which simplices are ordered
        by dimension (0 → 1 → 2 → ...) and then lexicographically.  This
        satisfies the ``FilteredComplex`` invariant: every face appears before
        every coface.

    Examples
    --------
    >>> fc = simplicial_filtration([(0, 1, 2)])
    >>> fc.size()
    7
    """
    face_set: set[tuple[int, ...]] = set()
    for simplex in maximal_simplices:
        for k in range(len(simplex) + 1):
            for face in combinations(sorted(simplex), k):
                if face:
                    face_set.add(face)

    all_faces = sorted(face_set, key=lambda f: (len(f) - 1, f))
    n = len(all_faces)
    return FilteredComplex(
        simplices=tuple(all_faces),
        births=tuple(0.0 for _ in range(n)),
        dimensions=tuple(len(f) - 1 for f in all_faces),
    )


# ---------------------------------------------------------------------------
# Standard triangulations
# ---------------------------------------------------------------------------


def _grid_torus_triangles(n: int = 3) -> list[tuple[int, ...]]:
    """Return 2n² triangles for the n×n flat torus triangulation.

    Vertices are (i, j) → n*i + j for i,j in {0,...,n-1}.
    The identification is (i, n) = (i, 0) and (n, j) = (0, j) (standard
    toroidal identification).
    """
    triangles: list[tuple[int, ...]] = []
    for i in range(n):
        for j in range(n):
            a = n * i + j
            b = n * ((i + 1) % n) + j
            c = n * i + (j + 1) % n
            d = n * ((i + 1) % n) + (j + 1) % n
            # Each grid cell → 2 triangles
            triangles.append(tuple(sorted((a, b, c))))
            triangles.append(tuple(sorted((b, c, d))))
    return triangles


def _grid_klein_triangles(n: int = 3) -> list[tuple[int, ...]]:
    """Return 2n² triangles for an n×n Klein bottle triangulation.

    Identification: j wraps normally (j mod n); when i wraps (i mod n), j is
    reflected to (n-1-j mod n) — this produces the Klein bottle's orientation
    reversal on the horizontal circle.
    """
    def klein_vid(i: int, j: int) -> int:
        j_norm = j % n
        if (i // n) % 2 == 0:
            return n * (i % n) + j_norm
        else:
            return n * (i % n) + (n - 1 - j_norm) % n

    triangles: list[tuple[int, ...]] = []
    for i in range(n):
        for j in range(n):
            a = klein_vid(i, j)
            b = klein_vid(i + 1, j)
            c = klein_vid(i, j + 1)
            d = klein_vid(i + 1, j + 1)
            triangles.append(tuple(sorted((a, b, c))))
            triangles.append(tuple(sorted((b, c, d))))
    return triangles


def torus_filtration() -> FilteredComplex:
    """Return a :class:`.FilteredComplex` for the torus T².

    Uses a 3×3 grid triangulation with 9 vertices, 27 edges, and 18 triangles.
    The identification is (i, j) ∼ (i mod 3, j mod 3).

    Known homology::

        H_0(T²; Z) = Z        (β_0 = 1)
        H_1(T²; Z) = Z ⊕ Z   (β_1 = 2)
        H_2(T²; Z) = Z        (β_2 = 1)

    For all primes p, the F_p Betti numbers are (1, 2, 1), as T² has no torsion.

    Returns
    -------
    FilteredComplex
        54 simplices total (9 vertices + 27 edges + 18 triangles).
    """
    triangles = _grid_torus_triangles(3)
    return simplicial_filtration(triangles)


def klein_bottle_filtration() -> FilteredComplex:
    """Return a :class:`.FilteredComplex` for the Klein bottle K.

    Uses a 3×3 grid triangulation with 9 vertices and 18 triangles.

    Known homology::

        H_0(K; Z) = Z
        H_1(K; Z) = Z ⊕ Z/2   (free part ⊕ torsion)
        H_2(K; Z) = 0

    F_p Betti numbers:
        p = 2: (1, 2, 0) — Z/2 torsion is visible
        p ≥ 3: (1, 1, 0) — torsion invisible

    Returns
    -------
    FilteredComplex
        Static simplicial filtration of the Klein bottle.

    Notes
    -----
    The triangulation uses the identification: horizontal wrap is orientation-
    preserving, vertical wrap reverses the horizontal coordinate.
    """
    triangles = _grid_klein_triangles(3)
    return simplicial_filtration(triangles)


def rp2_filtration() -> FilteredComplex:
    """Return a :class:`.FilteredComplex` for the real projective plane RP².

    Uses the minimal 6-vertex triangulation (10 triangles, 15 edges).

    Known homology::

        H_0(RP²; Z) = Z
        H_1(RP²; Z) = Z/2      (pure torsion)
        H_2(RP²; Z) = 0

    F_p Betti numbers:
        p = 2: (1, 1, 0) — Z/2 torsion is visible
        p ≥ 3: (1, 0, 0) — torsion invisible (H_1 vanishes)

    Returns
    -------
    FilteredComplex
        31 simplices (6 vertices + 15 edges + 10 triangles).

    Notes
    -----
    The triangulation is the classical 6-vertex triangulation of RP² from
    Banchoff & Kühnel (1992).  Vertices are 0–5; the 10 maximal triangles are:

        (0,1,3), (0,1,5), (0,2,3), (0,2,4), (0,4,5),
        (1,2,4), (1,2,5), (1,3,4), (2,3,5), (3,4,5).

    One can verify χ = 6 − 15 + 10 = 1 (correct for RP²).
    """
    triangles: list[tuple[int, ...]] = [
        (0, 1, 3), (0, 1, 5), (0, 2, 3), (0, 2, 4), (0, 4, 5),
        (1, 2, 4), (1, 2, 5), (1, 3, 4), (2, 3, 5), (3, 4, 5),
    ]
    return simplicial_filtration(triangles)
