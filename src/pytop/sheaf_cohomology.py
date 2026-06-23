"""Čech sheaf cohomology on finite topological spaces (Phase 12.1).

For a finite topological space X with topology τ and a sheaf F of
finitely generated free ℤ-modules, the Čech cohomology

    H^p(X; F)  (p = 0, 1, 2, …)

is computed from the Čech cochain complex with respect to an explicit
open cover U = {U₀, …, Uₙ}:

    C^p(U, F) = ⊕_{i₀ < … < iₚ, ∩U_{iₖ} ≠ ∅} F(∩U_{iₖ})

    δ^p: C^p → C^{p+1},  (δ^p s)_J = ∑_k (−1)^k res_{∩U_I → ∩U_J}(s_I)

    H^p = ker δ^p / im δ^{p−1}  (computed via Smith normal form)

Key results encoded in this module:
- Constant sheaf ℤ, cover = all non-empty opens: H^0 = ℤ^c where c is the
  number of connected components.  For acyclic covers (Leray's theorem),
  the Čech cohomology equals the derived-functor sheaf cohomology.
- Skyscraper sheaf at a point: H^0 = ℤ (the stalk), H^p = 0 for p > 0.
- The coboundary formula is the standard alternating-sum formula for Čech
  cochains; signs are (−1)^k where k is the position of the omitted index
  in the ordered multi-index.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any

from .exact_linalg import AbelianGroup
from .homology import _rank, _smith_normal_form

__all__ = [
    "FiniteSheaf",
    "constant_sheaf",
    "skyscraper_sheaf",
    "cech_cohomology",
    "sheaf_cohomology",
]


# ---------------------------------------------------------------------------
# FiniteSheaf
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FiniteSheaf:
    """A sheaf of finitely generated free ℤ-modules on a finite topological space.

    Attributes
    ----------
    open_sets:
        All open sets of the space (tuple of frozensets, ordered canonically).
    sections:
        Maps each open set U to its ℤ-rank, i.e. rank of F(U).
        By convention sections[frozenset()] = 0 (empty stalk).
    restrictions:
        Maps each pair (U, V) with V ⊊ U (V ≠ U) to the integer matrix
        res_{U→V}: ℤ^{rank U} → ℤ^{rank V} stored as a list of rows, each
        of length rank U, giving a matrix of shape rank(V) × rank(U).
    name:
        Human-readable label (e.g. ``"ℤ"`` for the constant sheaf).
    """

    open_sets: tuple[frozenset, ...]
    sections: dict[frozenset, int]
    restrictions: dict[tuple[frozenset, frozenset], list[list[int]]]
    name: str = "F"

    def section_rank(self, u: frozenset) -> int:
        return self.sections.get(frozenset(u), 0)

    def restrict(self, big: frozenset, small: frozenset) -> list[list[int]]:
        """Restriction matrix res_{big → small}.  Returns identity if big == small."""
        big = frozenset(big)
        small = frozenset(small)
        if big == small:
            r = self.section_rank(big)
            return [[int(i == j) for j in range(r)] for i in range(r)]
        return list(self.restrictions.get((big, small), []))


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def constant_sheaf(open_sets: list[frozenset], name: str = "ℤ") -> FiniteSheaf:
    """The constant sheaf ℤ: F(U) = ℤ for U ≠ ∅, F(∅) = 0.

    Restriction maps are all the identity map ℤ → ℤ (constant sections restrict
    to constant sections).

    Parameters
    ----------
    open_sets:
        All open sets of the finite topological space, including ∅.
    name:
        Label for the sheaf (default ``"ℤ"``).

    Returns
    -------
    :class:`FiniteSheaf` representing the constant ℤ-sheaf.

    Examples
    --------
    >>> opens = [frozenset(), frozenset({0}), frozenset({0, 1})]
    >>> F = constant_sheaf(opens)
    >>> F.section_rank(frozenset({0}))
    1
    >>> F.section_rank(frozenset())
    0
    """
    empty = frozenset()
    opens = [frozenset(u) for u in open_sets]
    sections: dict[frozenset, int] = {u: (0 if u == empty else 1) for u in opens}
    restrictions: dict[tuple[frozenset, frozenset], list[list[int]]] = {}
    for u in opens:
        for v in opens:
            if v < u and v != empty:
                restrictions[(u, v)] = [[1]]
    return FiniteSheaf(
        open_sets=tuple(sorted(opens, key=lambda x: (len(x), sorted(x)))),
        sections=sections,
        restrictions=restrictions,
        name=name,
    )


def skyscraper_sheaf(
    open_sets: list[frozenset],
    stalk_open: frozenset,
    rank: int = 1,
    name: str = "sky",
) -> FiniteSheaf:
    """The skyscraper sheaf with stalk ℤ^rank supported at *stalk_open*.

    F(U) = ℤ^rank if stalk_open ⊆ U, else 0.  Restriction maps are the
    identity on ℤ^rank between open sets that both contain the stalk point.

    Parameters
    ----------
    open_sets:
        All open sets of the finite topological space.
    stalk_open:
        The open set on which the sheaf is concentrated (its stalk).
    rank:
        ℤ-rank of the stalk (default 1).
    name:
        Label for the sheaf.

    Returns
    -------
    :class:`FiniteSheaf`.

    Examples
    --------
    >>> opens = [frozenset(), frozenset({1}), frozenset({0, 1})]
    >>> F = skyscraper_sheaf(opens, frozenset({1}))
    >>> F.section_rank(frozenset({1}))
    1
    >>> F.section_rank(frozenset({0, 1}))
    1
    """
    stk = frozenset(stalk_open)
    opens = [frozenset(u) for u in open_sets]
    sections: dict[frozenset, int] = {u: (rank if stk <= u else 0) for u in opens}
    restrictions: dict[tuple[frozenset, frozenset], list[list[int]]] = {}
    for u in opens:
        for v in opens:
            if v < u and sections[u] > 0 and sections[v] > 0:
                restrictions[(u, v)] = [[int(i == j) for j in range(rank)] for i in range(rank)]
    return FiniteSheaf(
        open_sets=tuple(sorted(opens, key=lambda x: (len(x), sorted(x)))),
        sections=sections,
        restrictions=restrictions,
        name=name,
    )


# ---------------------------------------------------------------------------
# Čech cochain complex
# ---------------------------------------------------------------------------


def _intersect_cover(cover: list[frozenset], indices: tuple[int, ...]) -> frozenset:
    result = cover[indices[0]]
    for i in indices[1:]:
        result = result & cover[i]
    return result


def _cech_coboundary(
    cover: list[frozenset],
    sheaf: FiniteSheaf,
    p: int,
) -> list[list[int]]:
    """Build the coboundary matrix δ^p: C^p(cover, F) → C^{p+1}(cover, F).

    Returns a dense integer matrix of shape (rank C^{p+1}) × (rank C^p).
    Multi-indices with empty intersection are excluded (they contribute rank 0).
    """
    n = len(cover)

    mids_p: list[tuple[int, ...]] = [
        idx
        for idx in combinations(range(n), p + 1)
        if bool(_intersect_cover(cover, idx))
    ]
    mids_p1: list[tuple[int, ...]] = [
        idx
        for idx in combinations(range(n), p + 2)
        if bool(_intersect_cover(cover, idx))
    ]

    ranks_p = [sheaf.section_rank(_intersect_cover(cover, idx)) for idx in mids_p]
    ranks_p1 = [sheaf.section_rank(_intersect_cover(cover, idx)) for idx in mids_p1]

    row_total = sum(ranks_p1)
    col_total = sum(ranks_p)

    mat: list[list[int]] = [[0] * col_total for _ in range(row_total)]
    if row_total == 0 or col_total == 0:
        return mat

    # Precompute column offsets
    col_off: dict[tuple[int, ...], int] = {}
    offset = 0
    for idx, r in zip(mids_p, ranks_p):
        col_off[idx] = offset
        offset += r

    row_offset = 0
    for j_idx, J in enumerate(mids_p1):
        inter_J = _intersect_cover(cover, J)
        r_J = ranks_p1[j_idx]
        J_set = set(J)

        for i_idx, I in enumerate(mids_p):
            r_I = ranks_p[i_idx]
            if r_I == 0:
                continue
            I_set = set(I)
            if not (I_set < J_set):
                continue

            removed = next(iter(J_set - I_set))
            face_k = list(J).index(removed)
            sign = 1 if face_k % 2 == 0 else -1

            inter_I = _intersect_cover(cover, I)
            res_mat = sheaf.restrict(inter_I, inter_J)
            if not res_mat:
                continue

            c_off = col_off[I]
            for ri in range(min(r_J, len(res_mat))):
                row_vals = res_mat[ri]
                for ci in range(min(r_I, len(row_vals))):
                    mat[row_offset + ri][c_off + ci] += sign * row_vals[ci]

        row_offset += r_J

    return mat


# ---------------------------------------------------------------------------
# Čech cohomology
# ---------------------------------------------------------------------------


def cech_cohomology(
    cover: list[frozenset],
    sheaf: FiniteSheaf,
    max_degree: int | None = None,
) -> dict[int, AbelianGroup]:
    """Compute Čech cohomology H^p(cover, F) for p = 0, …, max_degree.

    Parameters
    ----------
    cover:
        Non-empty open sets forming an open cover of X.  Intersections are
        computed automatically.  The empty set is silently dropped.
    sheaf:
        A :class:`FiniteSheaf` on the same topological space.
    max_degree:
        Highest cohomology degree to compute.  Defaults to ``len(cover) − 1``.

    Returns
    -------
    dict mapping p → :class:`AbelianGroup`.

    Notes
    -----
    The Betti number formula is:

        β^p = (rank C^p − rank δ^p) − rank δ^{p−1}

    Torsion is extracted from the invariant factors of δ^{p−1} via SNF.

    Examples
    --------
    Sierpiński space (contractible) with constant sheaf ℤ:

    >>> opens = [frozenset(), frozenset({1}), frozenset({0, 1})]
    >>> F = constant_sheaf(opens)
    >>> cover = [frozenset({1}), frozenset({0, 1})]
    >>> H = cech_cohomology(cover, F)
    >>> str(H[0])
    'Z'
    >>> H[1].free_rank
    0
    """
    cover = [frozenset(u) for u in cover if u]
    if not cover:
        return {}

    if max_degree is None:
        max_degree = len(cover) - 1

    coboundaries: dict[int, list[list[int]]] = {
        p: _cech_coboundary(cover, sheaf, p)
        for p in range(max_degree)
    }

    result: dict[int, AbelianGroup] = {}
    for p in range(max_degree + 1):
        n_p = sum(
            sheaf.section_rank(_intersect_cover(cover, idx))
            for idx in combinations(range(len(cover)), p + 1)
            if bool(_intersect_cover(cover, idx))
        )

        rank_curr = _rank(coboundaries[p]) if p in coboundaries else 0
        rank_prev = _rank(coboundaries[p - 1]) if p > 0 and (p - 1) in coboundaries else 0

        betti = max((n_p - rank_curr) - rank_prev, 0)

        if p > 0 and (p - 1) in coboundaries:
            factors = _smith_normal_form(coboundaries[p - 1])
            torsion = tuple(f for f in factors if f > 1)
        else:
            torsion = ()

        result[p] = AbelianGroup(free_rank=betti, torsion=torsion)

    return result


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------


def _minimal_open_cover(
    open_sets: list[frozenset], universe: frozenset
) -> list[frozenset]:
    """Return the minimal open neighborhood cover {U_x : x ∈ X}.

    For each point x, U_x = ∩{U ∈ τ : x ∈ U} is the smallest open set
    containing x.  The collection {U_x} is a Leray cover for the constant
    sheaf on any finite T₀ space (McCord 1966): Čech cohomology with this
    cover equals the singular cohomology of the geometric realisation of
    the order complex.
    """
    pts = sorted(universe)
    nbhds: list[frozenset] = []
    for p in pts:
        containing = [frozenset(u) for u in open_sets if p in u]
        if not containing:
            continue
        mn: frozenset = containing[0]
        for u in containing[1:]:
            mn = mn & u
        if mn:
            nbhds.append(mn)
    return list({u for u in nbhds})


def sheaf_cohomology(
    open_sets: list[frozenset],
    universe: frozenset,
    sheaf: FiniteSheaf,
    max_degree: int | None = None,
) -> dict[str, Any]:
    """Compute Čech sheaf cohomology on a finite topological space.

    Uses the **minimal open neighborhood cover** {U_x : x ∈ X} as the
    Čech cover.  This is a Leray cover for the constant sheaf on any finite
    T₀ space (McCord 1966), so the result equals the sheaf-theoretic
    (derived-functor) cohomology in that case.

    Parameters
    ----------
    open_sets:
        All open sets of X (should include ∅ and *universe*).
    universe:
        The total space X (a frozenset of points).
    sheaf:
        A :class:`FiniteSheaf` on X.
    max_degree:
        Highest degree to compute.  Defaults to ``|X| − 1``.

    Returns
    -------
    dict with keys:

    - ``"cohomology"`` : dict[int, :class:`AbelianGroup`]
    - ``"betti_numbers"`` : list[int]
    - ``"euler_characteristic"`` : int  (alternating sum of Betti numbers)
    - ``"cover_size"`` : int  (number of minimal open neighborhoods used)
    - ``"sheaf"`` : str  (name of the sheaf)

    Examples
    --------
    Constant sheaf ℤ on a 2-point discrete space (two connected components):

    >>> opens = [frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})]
    >>> F = constant_sheaf(opens)
    >>> r = sheaf_cohomology(opens, frozenset({0, 1}), F)
    >>> r["betti_numbers"][0]
    2

    Constant sheaf on the Sierpiński space (contractible):

    >>> opens2 = [frozenset(), frozenset({1}), frozenset({0, 1})]
    >>> F2 = constant_sheaf(opens2)
    >>> r2 = sheaf_cohomology(opens2, frozenset({0, 1}), F2)
    >>> r2["betti_numbers"][0]
    1
    """
    cover = _minimal_open_cover(open_sets, frozenset(universe))
    if not cover:
        cover = [frozenset(u) for u in open_sets if u]

    if max_degree is None:
        max_degree = max(len(frozenset(universe)) - 1, 0)

    H = cech_cohomology(cover, sheaf, max_degree=max_degree)

    betti = [H[p].free_rank for p in range(max_degree + 1)]
    chi = sum((-1) ** p * b for p, b in enumerate(betti))

    return {
        "cohomology": H,
        "betti_numbers": betti,
        "euler_characteristic": chi,
        "cover_size": len(cover),
        "sheaf": sheaf.name,
    }
