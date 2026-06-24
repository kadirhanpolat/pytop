"""Optimized persistent homology: Twist algorithm with the Clearing Lemma.

Standard column reduction (left-to-right sweep over Z/2) runs in O(n³) worst
case.  The Twist algorithm (Chen–Kerber 2011) processes boundary columns
dimension by dimension from highest to lowest.  As each finite persistence
pair (creator σ, destroyer τ) is discovered, the creator's column is
immediately *cleared* — the Clearing Lemma guarantees it reduces to zero so
no column operations on it are ever needed.

Clearing Lemma  (Chen–Kerber 2011, Lemma 1)
--------------------------------------------
Let D be the boundary matrix and R = D·V its column-reduced form (over Z/2).
If low(R[j]) = i — meaning simplex j kills the class born at simplex i — then
column R[i] reduces to zero without any column operations.

Consequence: processing dimensions top-down lets us identify creators
*before* we would normally reduce them, so we skip those reductions entirely.
On Vietoris–Rips filtrations of circle- or torus-like data, this eliminates
a large fraction of column additions.

Correctness guarantee: `persistence_pairs_twist` produces results identical to
`persistence_pairs` (the standard left-to-right reduction) on every input.
The unit tests enforce this via cross-validation.

Public API
----------
ReductionStats                    — statistics from one reduction run
persistence_pairs_twist           — Twist reduction (same signature / output as
                                    persistence_pairs)
persistence_pairs_twist_with_stats — same but also returns ReductionStats
persistent_homology_optimized     — convenience: VR filtration → Twist reduction
                                    (soft-deprecation candidate — see below)

Deprecation note
----------------
``persistent_homology_optimized`` is a **soft-deprecation candidate**
(``DEPRECATIONS.md`` → *Candidates*; ``docs/API_DESIGN.md`` finding #3). It is a
historical alias for ``persistent_homology(space, method="auto")`` and produces
identical barcodes. New code should prefer the latter. No ``DeprecationWarning``
is emitted yet.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations
from typing import Any

from .persistent_homology import (
    FilteredComplex,
    PersistencePair,
    vietoris_rips_filtration,
)

# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ReductionStats:
    """Statistics from one run of the Twist reduction.

    Attributes
    ----------
    n_simplices : int
        Total number of simplices in the filtered complex.
    n_cleared : int
        Columns skipped thanks to the Clearing Lemma.
    n_column_additions : int
        Number of XOR operations (column additions over Z/2) performed.
    n_finite_pairs : int
        Finite persistence pairs (b < d < ∞) found.
    n_essential : int
        Essential (infinite) persistence pairs found.
    """

    n_simplices: int
    n_cleared: int
    n_column_additions: int
    n_finite_pairs: int
    n_essential: int

    @property
    def clearing_ratio(self) -> float:
        """Fraction of columns skipped by clearing (0.0 – 1.0)."""
        return self.n_cleared / self.n_simplices if self.n_simplices > 0 else 0.0

    @property
    def n_pairs(self) -> int:
        """Total persistence pairs (finite + essential)."""
        return self.n_finite_pairs + self.n_essential


# ---------------------------------------------------------------------------
# Core: Twist algorithm with Clearing Lemma
# ---------------------------------------------------------------------------

def _build_columns(
    filtered: FilteredComplex,
) -> tuple[list[int], dict[tuple[int, ...], int]]:
    """Build the Z/2 boundary columns and the simplex→index map.

    Each column is represented as a Python ``int`` used as a bigint bitmask:
    bit *r* is set when row *r* contains a 1.  This lets the hot-path XOR and
    pivot operations use native integer arithmetic instead of Python set
    operations (~5× faster on typical inputs).
    """
    index_of: dict[tuple[int, ...], int] = {
        s: idx for idx, s in enumerate(filtered.simplices)
    }
    columns: list[int] = []
    for simplex, dim in zip(filtered.simplices, filtered.dimensions):
        if dim == 0:
            columns.append(0)
        else:
            mask = 0
            for face in combinations(simplex, len(simplex) - 1):
                mask |= 1 << index_of[face]
            columns.append(mask)
    return columns, index_of


def _twist_reduce(
    columns: list[int],
    dimensions: tuple[int, ...],
    births: tuple[float, ...],
    *,
    include_zero_persistence: bool = False,
) -> tuple[tuple[PersistencePair, ...], ReductionStats]:
    """Core Twist+Clearing reduction over pre-built Z/2 boundary columns.

    This is the shared kernel used by both the simplicial and cubical
    persistence interfaces.  ``columns[j]`` is a Python bigint bitmask where
    bit *r* is set iff row *r* has a 1 in column *j* of the boundary matrix
    (over Z/2).  Columns are mutated in place.

    Using ``int`` bitmasks instead of ``set[int]`` gives roughly 5× speed-up
    on the hot path:

    * pivot  → ``col.bit_length() - 1``  (no Python max() call)
    * empty? → ``col == 0``
    * XOR    → ``col ^= other``          (identical syntax, native integer op)

    Returns
    -------
    pairs : tuple[PersistencePair, ...]
    stats : ReductionStats
    """
    n = len(columns)
    if n == 0:
        return (), ReductionStats(0, 0, 0, 0, 0)

    by_dim: dict[int, list[int]] = {}
    for j, d in enumerate(dimensions):
        by_dim.setdefault(d, []).append(j)

    max_dim = max(dimensions)
    low_inverse: dict[int, int] = {}
    cleared: set[int] = set()
    col_additions = 0

    for d in range(max_dim, -1, -1):
        for j in by_dim.get(d, []):
            if j in cleared:
                continue
            while columns[j]:
                pivot = columns[j].bit_length() - 1
                if pivot in low_inverse:
                    columns[j] ^= columns[low_inverse[pivot]]
                    col_additions += 1
                else:
                    low_inverse[pivot] = j
                    cleared.add(pivot)
                    break

    pairs: list[PersistencePair] = []
    for creator, destroyer in low_inverse.items():
        birth = births[creator]
        death = births[destroyer]
        if not include_zero_persistence and death == birth:
            continue
        pairs.append(PersistencePair(dimensions[creator], birth, death))

    paired_creators = set(low_inverse)
    for i in range(n):
        if i in cleared:
            continue
        if not columns[i] and i not in paired_creators:
            pairs.append(PersistencePair(dimensions[i], births[i], math.inf))

    result = tuple(sorted(pairs, key=lambda p: (p.dimension, p.birth, p.death)))
    finite = sum(1 for p in result if not p.is_essential)
    essential = len(result) - finite
    stats = ReductionStats(
        n_simplices=n,
        n_cleared=len(cleared),
        n_column_additions=col_additions,
        n_finite_pairs=finite,
        n_essential=essential,
    )
    return result, stats


def persistence_pairs_twist_with_stats(
    filtered: FilteredComplex,
    *,
    include_zero_persistence: bool = False,
) -> tuple[tuple[PersistencePair, ...], ReductionStats]:
    """Twist reduction with Clearing; also returns :class:`ReductionStats`.

    Same output as :func:`persistence_pairs_twist` plus a :class:`ReductionStats`
    instance reporting how many columns were cleared and how many column
    additions were performed.
    """
    n = filtered.size()
    if n == 0:
        return (), ReductionStats(0, 0, 0, 0, 0)

    columns, _ = _build_columns(filtered)
    return _twist_reduce(
        columns,
        filtered.dimensions,
        filtered.births,
        include_zero_persistence=include_zero_persistence,
    )


def persistence_pairs_twist(
    filtered: FilteredComplex,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistence pairs via the Twist algorithm (Chen–Kerber 2011).

    Produces results identical to :func:`~pytop.persistent_homology.persistence_pairs`
    but processes dimensions from high to low and applies the Clearing Lemma to
    skip creator columns whose reduction is guaranteed to be zero.

    Parameters
    ----------
    filtered:
        Output of :func:`~pytop.persistent_homology.vietoris_rips_filtration`
        or any :class:`~pytop.persistent_homology.FilteredComplex`.
    include_zero_persistence:
        If ``True``, include pairs with ``birth == death``.

    Returns
    -------
    tuple[PersistencePair, ...]
        Sorted by ``(dimension, birth, death)``.
    """
    pairs, _ = persistence_pairs_twist_with_stats(
        filtered, include_zero_persistence=include_zero_persistence
    )
    return pairs


def persistent_homology_optimized(
    space: Any,
    max_dimension: int = 1,
    max_scale: float | None = None,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Vietoris–Rips filtration followed by Twist reduction.

    Convenience wrapper equivalent to calling
    :func:`~pytop.persistent_homology.vietoris_rips_filtration` then
    :func:`persistence_pairs_twist`.

    .. note::
       Soft-deprecation candidate (see ``DEPRECATIONS.md`` and
       ``docs/API_DESIGN.md`` finding #3). Since :func:`persistent_homology`
       already routes to the twist method by default — and to the size-aware
       ``"auto"`` router as of P17.3 — this wrapper is effectively a historical
       alias. Prefer ``persistent_homology(space, method="auto")`` in new code.
       No behavior change and no ``DeprecationWarning`` yet; both produce
       identical barcodes.

    Parameters
    ----------
    space:
        Any object exposing ``carrier`` and ``distance_between``.
    max_dimension:
        Maximum simplex dimension to include (default 1 → edges only).
    max_scale:
        If given, simplices with birth > max_scale are excluded.
    include_zero_persistence:
        Whether to include zero-length bars.
    """
    filtered = vietoris_rips_filtration(
        space, max_dimension=max_dimension, max_scale=max_scale
    )
    return persistence_pairs_twist(
        filtered, include_zero_persistence=include_zero_persistence
    )


# ---------------------------------------------------------------------------
# Persistent cohomology — de Silva–Morozov–Vejdemo-Johansson (2011)
# ---------------------------------------------------------------------------

def persistence_pairs_cohomology_with_stats(
    filtered: FilteredComplex,
    *,
    include_zero_persistence: bool = False,
) -> tuple[tuple[PersistencePair, ...], ReductionStats]:
    """Persistent **cohomology** via the incremental algorithm; also returns stats.

    The dual algorithm of de Silva–Morozov–Vejdemo-Johansson (2011): instead of
    reducing the boundary matrix column by column, it processes the simplices in
    filtration order while maintaining the live **cocycles** (Z/2 cochains).  When
    a new simplex ``σ`` is added, the cocycles ``z`` with ``⟨z, ∂σ⟩ = 1`` are
    exactly those whose class ``σ`` cobounds; the youngest of them dies (a finite
    pair) and the rest are updated by adding the dying cochain.  Cocycles that are
    never killed are the essential classes.

    An inverted index ``containing[s]`` (the live cocycles whose cochain contains
    simplex ``s``) means each new simplex is only compared against the cocycles
    sharing one of its facets — so on Vietoris–Rips filtrations, where almost all
    pairs are *apparent*, the number of cochain additions is tiny compared with the
    boundary reduction (often hundreds vs hundreds of thousands), giving the same
    barcode faster.

    Returns the persistence pairs (identical to
    :func:`~pytop.persistent_homology.persistence_pairs`) and a
    :class:`ReductionStats` whose ``n_column_additions`` counts the cochain
    additions performed (``n_cleared`` is not applicable here and is ``0``).

    Complexity
    ----------
    Output-sensitive: dominated by the cochain additions, which is small on
    structured (Rips-like) inputs. See ``docs/COMPLEXITY.md``.
    """

    n = filtered.size()
    if n == 0:
        return (), ReductionStats(0, 0, 0, 0, 0)

    simplices, dims, births = filtered.simplices, filtered.dimensions, filtered.births
    index_of = {simplex: idx for idx, simplex in enumerate(simplices)}

    def facets(idx: int) -> list[int]:
        simplex = simplices[idx]
        if len(simplex) <= 1:
            return []
        return [index_of[face] for face in combinations(simplex, len(simplex) - 1)]

    birth_of: dict[int, int] = {}        # cocycle id -> birth simplex index
    cochain_of: dict[int, set[int]] = {}  # cocycle id -> set of simplex indices
    containing: dict[int, set[int]] = {}  # simplex index -> cocycle ids containing it
    pairs: list[PersistencePair] = []
    xor_ops = 0
    next_id = 0

    for i in range(n):
        # Parity of each live cocycle over the facets of simplex i = ⟨z, ∂σ_i⟩.
        parity: dict[int, int] = {}
        for f in facets(i):
            for cid in containing.get(f, ()):
                parity[cid] = parity.get(cid, 0) ^ 1
        hit = [cid for cid, p in parity.items() if p]

        if not hit:  # σ_i creates a new cocycle (positive simplex)
            cid = next_id
            next_id += 1
            birth_of[cid] = i
            cochain_of[cid] = {i}
            containing.setdefault(i, set()).add(cid)
            continue

        # σ_i kills the youngest cocycle it cobounds (elder rule), pairing it.
        pivot = max(hit, key=lambda cid: birth_of[cid])
        creator = birth_of[pivot]
        if include_zero_persistence or births[creator] != births[i]:
            pairs.append(PersistencePair(dims[creator], births[creator], births[i]))
        pivot_cochain = cochain_of[pivot]
        for cid in hit:
            if cid == pivot:
                continue
            xor_ops += 1
            target = cochain_of[cid]
            for s in pivot_cochain:  # target ^= pivot_cochain, keeping the index
                if s in target:
                    target.discard(s)
                    containing[s].discard(cid)
                else:
                    target.add(s)
                    containing.setdefault(s, set()).add(cid)
        for s in pivot_cochain:
            containing[s].discard(pivot)
        del cochain_of[pivot]
        del birth_of[pivot]

    for cid, b in birth_of.items():  # unkilled cocycles are essential
        pairs.append(PersistencePair(dims[b], births[b], math.inf))

    result = tuple(sorted(pairs, key=lambda p: (p.dimension, p.birth, p.death)))
    finite = sum(1 for p in result if not p.is_essential)
    stats = ReductionStats(
        n_simplices=n,
        n_cleared=0,
        n_column_additions=xor_ops,
        n_finite_pairs=finite,
        n_essential=len(result) - finite,
    )
    return result, stats


def persistence_pairs_cohomology(
    filtered: FilteredComplex,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistence pairs via the dual (persistent cohomology) algorithm.

    Produces results identical to
    :func:`~pytop.persistent_homology.persistence_pairs` and
    :func:`persistence_pairs_twist`, but via persistent cohomology (de Silva–
    Morozov–Vejdemo-Johansson 2011) — far fewer column operations on Vietoris–Rips
    filtrations.  See :func:`persistence_pairs_cohomology_with_stats`.
    """

    pairs, _ = persistence_pairs_cohomology_with_stats(
        filtered, include_zero_persistence=include_zero_persistence
    )
    return pairs


# ---------------------------------------------------------------------------
# Size-aware auto routing (P17.3)
# ---------------------------------------------------------------------------

AUTO_COHOMOLOGY_THRESHOLD = 1024
"""Simplex count at/above which :func:`persistence_pairs_auto` uses cohomology.

Empirically (P17.3 benchmarks, see ``docs/P17_3_PARALLEL_SCALING.md``) the de
Silva–Morozov–Vejdemo-Johansson dual algorithm overtakes Twist+Clearing on
Vietoris–Rips filtrations once the *materialized* complex exceeds ~1k simplices,
after which its lead grows super-linearly (≈1.5× at m≈7k, ≈2.8× at m≈55k, ≈3.8×
at m≈108k) because it performs hundreds of cochain additions where Twist
performs millions of column XORs. Below the threshold Twist's lower constant
factor wins, so tiny complexes stay on Twist. The crossover is broad and flat,
so the exact value is not sensitive — 1024 sits safely inside the gap measured
between m≈520 (Twist faster) and m≈2850 (cohomology faster).
"""


def select_reduction_method(n_simplices: int) -> str:
    """Return the reduction method auto-routing picks for a complex of this size.

    ``"cohomology"`` when ``n_simplices >= AUTO_COHOMOLOGY_THRESHOLD``, else
    ``"twist"``. Exposed separately so callers (and tests) can inspect the routing
    decision without running a reduction.
    """
    return "cohomology" if n_simplices >= AUTO_COHOMOLOGY_THRESHOLD else "twist"


def persistence_pairs_auto(
    filtered: FilteredComplex,
    *,
    include_zero_persistence: bool = False,
) -> tuple[PersistencePair, ...]:
    """Compute persistence pairs via the faster reduction for the input size.

    Routes small complexes (``< AUTO_COHOMOLOGY_THRESHOLD`` simplices) to the
    Twist algorithm and larger ones to persistent cohomology, which scales far
    better on Vietoris–Rips filtrations. The output is **identical** to
    :func:`persistence_pairs_twist`, :func:`persistence_pairs_cohomology`, and the
    standard reduction on every input — only the wall-clock time differs. This is
    the routing used by :func:`~pytop.persistent_homology.persistent_homology`'s
    default ``method="auto"``.
    """
    if select_reduction_method(filtered.size()) == "cohomology":
        return persistence_pairs_cohomology(
            filtered, include_zero_persistence=include_zero_persistence
        )
    return persistence_pairs_twist(
        filtered, include_zero_persistence=include_zero_persistence
    )


__all__ = [
    "ReductionStats",
    "AUTO_COHOMOLOGY_THRESHOLD",
    "select_reduction_method",
    "persistence_pairs_auto",
    "persistence_pairs_twist",
    "persistence_pairs_twist_with_stats",
    "persistence_pairs_cohomology",
    "persistence_pairs_cohomology_with_stats",
    "persistent_homology_optimized",
]
