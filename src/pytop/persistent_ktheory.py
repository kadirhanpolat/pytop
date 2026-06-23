"""Persistent K-theory for filtrations of finite simplicial complexes (Phase 12.2).

Rational K-theory via the Atiyah-Hirzebruch spectral sequence (AHSS).
For a finite CW complex X, the AHSS degenerates rationally (Atiyah 1962),
giving:

    K⁰(X) ⊗ ℚ ≅ ⊕_{k even} H_k(X; ℚ)
    K¹(X) ⊗ ℚ ≅ ⊕_{k odd}  H_k(X; ℚ)

For integer K-theory the AHSS has potential differentials d_3, d_5, …
(all odd), but for all spaces in the test suite these vanish and the
integral Betti numbers of K⁰, K¹ coincide with the rational ranks above.

Persistent K-theory barcode:
Given a filtration K₀ ⊆ K₁ ⊆ … ⊆ Kₙ, we run the Twist persistent
homology algorithm to obtain all persistence pairs (b, d, dim), then
partition by dimension parity:

    K⁰-barcode = { (b, d) : dim even }
    K¹-barcode = { (b, d) : dim odd  }

The K⁰-barcode tracks when K-theory classes represented by even-dimensional
cycles are born and die across the filtration.  The virtual K-Euler
characteristic satisfies χ_K = rank K⁰ − rank K¹ = χ (the topological
Euler characteristic), consistent with the standard relation between K-theory
and homology via the Chern character.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .homology import SimplicialComplex, homology_groups
from .persistent_homology import FilteredComplex, PersistencePair
from .persistent_homology_optimized import persistence_pairs_twist

__all__ = [
    "KTheoryGroups",
    "KBarcode",
    "k0_simplicial",
    "k1_simplicial",
    "k_theory_groups",
    "k_barcode",
    "k_betti_numbers",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KTheoryGroups:
    """Rational K-theory groups of a finite simplicial complex.

    Attributes
    ----------
    k0_rank:
        Rank of K⁰(X) ⊗ ℚ = sum of even Betti numbers.
    k1_rank:
        Rank of K¹(X) ⊗ ℚ = sum of odd Betti numbers.
    k0_rational:
        Human-readable string for K⁰(X) ⊗ ℚ (e.g. ``"ℚ^2"``).
    k1_rational:
        Human-readable string for K¹(X) ⊗ ℚ.
    betti_numbers:
        Tuple (β₀, β₁, …, β_{dim}) of all Betti numbers of X.
    """

    k0_rank: int
    k1_rank: int
    k0_rational: str
    k1_rational: str
    betti_numbers: tuple[int, ...]


@dataclass(frozen=True)
class KBarcode:
    """Persistent K-theory barcode of a filtered simplicial complex.

    Attributes
    ----------
    k0_pairs:
        Persistence pairs from even-dimensional homology (the K⁰ barcode).
    k1_pairs:
        Persistence pairs from odd-dimensional homology (the K¹ barcode).
    all_pairs:
        All persistence pairs before parity filtering.
    """

    k0_pairs: tuple[PersistencePair, ...]
    k1_pairs: tuple[PersistencePair, ...]
    all_pairs: tuple[PersistencePair, ...]

    def k0_betti_at(self, scale: float) -> int:
        """Number of active K⁰ bars at *scale* (bars with birth ≤ scale < death)."""
        return sum(1 for p in self.k0_pairs if p.birth <= scale < p.death)

    def k1_betti_at(self, scale: float) -> int:
        """Number of active K¹ bars at *scale*."""
        return sum(1 for p in self.k1_pairs if p.birth <= scale < p.death)

    def euler_characteristic_at(self, scale: float) -> int:
        """Virtual K-Euler characteristic χ_K = rank K⁰ − rank K¹ at *scale*."""
        return self.k0_betti_at(scale) - self.k1_betti_at(scale)


# ---------------------------------------------------------------------------
# K-theory of a simplicial complex
# ---------------------------------------------------------------------------


def k_theory_groups(complex_obj: SimplicialComplex) -> KTheoryGroups:
    """Compute rational K-theory groups of a simplicial complex via AHSS.

    Parameters
    ----------
    complex_obj:
        A :class:`~pytop.homology.SimplicialComplex`.

    Returns
    -------
    :class:`KTheoryGroups` with ranks and human-readable descriptions.

    Examples
    --------
    Circle S¹ (β₀ = 1, β₁ = 1) → K⁰ rank = 1, K¹ rank = 1:

    >>> from pytop.homology import SimplicialComplex
    >>> S1 = SimplicialComplex([(0,), (1,), (2,), (0,1), (1,2), (0,2)])
    >>> g = k_theory_groups(S1)
    >>> g.k0_rank, g.k1_rank
    (1, 1)

    Point (β₀ = 1) → K⁰ rank = 1, K¹ rank = 0:

    >>> pt = SimplicialComplex([(0,)])
    >>> g = k_theory_groups(pt)
    >>> g.k0_rank, g.k1_rank
    (1, 0)
    """
    groups = homology_groups(complex_obj)
    betti = tuple(g.betti for g in groups)

    k0 = sum(b for i, b in enumerate(betti) if i % 2 == 0)
    k1 = sum(b for i, b in enumerate(betti) if i % 2 == 1)

    def _fmt(r: int) -> str:
        if r == 0:
            return "0"
        if r == 1:
            return "ℚ"
        return f"ℚ^{r}"

    return KTheoryGroups(
        k0_rank=k0,
        k1_rank=k1,
        k0_rational=_fmt(k0),
        k1_rational=_fmt(k1),
        betti_numbers=betti,
    )


def k0_simplicial(complex_obj: SimplicialComplex) -> int:
    """Return rank K⁰(X) ⊗ ℚ = sum of even Betti numbers of *complex_obj*.

    Examples
    --------
    >>> from pytop.homology import SimplicialComplex
    >>> k0_simplicial(SimplicialComplex([(0,)]))
    1
    """
    return k_theory_groups(complex_obj).k0_rank


def k1_simplicial(complex_obj: SimplicialComplex) -> int:
    """Return rank K¹(X) ⊗ ℚ = sum of odd Betti numbers of *complex_obj*.

    Examples
    --------
    >>> from pytop.homology import SimplicialComplex
    >>> S1 = SimplicialComplex([(0,), (1,), (2,), (0,1), (1,2), (0,2)])
    >>> k1_simplicial(S1)
    1
    """
    return k_theory_groups(complex_obj).k1_rank


def k_betti_numbers(complex_obj: SimplicialComplex) -> tuple[int, int]:
    """Return ``(rank K⁰, rank K¹)`` for *complex_obj*.

    The K-Euler characteristic satisfies χ_K = rank K⁰ − rank K¹ = χ(X).

    Examples
    --------
    Torus T² (β₀=1, β₁=2, β₂=1) → K⁰ rank = 2, K¹ rank = 2:

    >>> from pytop.homology import SimplicialComplex
    >>> # minimal 7-vertex torus triangulation via Heawood construction
    >>> from pytop.simplicial_filtration import torus_filtration
    >>> filt = torus_filtration()
    >>> torus = SimplicialComplex(filt.simplices)
    >>> k_betti_numbers(torus)
    (2, 2)
    """
    g = k_theory_groups(complex_obj)
    return g.k0_rank, g.k1_rank


# ---------------------------------------------------------------------------
# Persistent K-theory barcode
# ---------------------------------------------------------------------------


def k_barcode(
    filtered: FilteredComplex,
    max_dimension: int | None = None,
) -> KBarcode:
    """Compute the persistent K-theory barcode of a filtered simplicial complex.

    Runs the Twist persistent homology algorithm on *filtered* and partitions
    the resulting bars by their homological dimension parity:

    - **K⁰-barcode**: bars from H₀, H₂, H₄, …
    - **K¹-barcode**: bars from H₁, H₃, H₅, …

    Parameters
    ----------
    filtered:
        A :class:`~pytop.persistent_homology.FilteredComplex`.
    max_dimension:
        Highest homological dimension to include.  Defaults to the maximum
        simplex dimension in *filtered*.

    Returns
    -------
    :class:`KBarcode`.

    Notes
    -----
    The relation χ_K(scale) = rank K⁰(scale) − rank K¹(scale) equals the
    topological Euler characteristic of the sub-complex at *scale*.

    Examples
    --------
    Eight-point circle: one long K⁰ bar (from H₀), one long K¹ bar (from H₁):

    >>> from pytop.persistent_homology import vietoris_rips_filtration
    >>> import math
    >>> class _C:
    ...     carrier = [(math.cos(2*math.pi*i/8), math.sin(2*math.pi*i/8)) for i in range(8)]
    ...     def distance_between(self, a, b):
    ...         return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
    >>> kb = k_barcode(vietoris_rips_filtration(_C(), max_dimension=2))
    >>> len(kb.k0_pairs) >= 1
    True
    >>> len(kb.k1_pairs) >= 1
    True
    """
    pairs = persistence_pairs_twist(filtered)

    if max_dimension is not None:
        pairs = [p for p in pairs if p.dimension <= max_dimension]

    k0 = tuple(p for p in pairs if p.dimension % 2 == 0)
    k1 = tuple(p for p in pairs if p.dimension % 2 == 1)

    return KBarcode(
        k0_pairs=k0,
        k1_pairs=k1,
        all_pairs=tuple(pairs),
    )
