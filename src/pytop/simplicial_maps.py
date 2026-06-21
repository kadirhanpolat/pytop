"""Simplicial maps and induced chain-level homomorphisms.

P7.2 milestone — five public objects:

SimplicialMap          : validated dataclass for a simplicial map f: K → L
chain_map_matrix       : integer matrix of f#_k: C_k(K) → C_k(L)
induced_map_on_homology: InducedHomologyMap with f_*: H_k(K) → H_k(L)
cone_complex           : CK = K * {apex}, always contractible
suspension_complex     : ΣK = K * S⁰, satisfies Σ(Sⁿ) ≃ Sⁿ⁺¹

Mathematical background
-----------------------
A simplicial map f: K → L is a vertex map v ↦ f(v) such that for every simplex
σ = {v₀,...,vₖ} ∈ K the image {f(v₀),...,f(vₖ)} spans a simplex in L (vertices
may collapse when f(vᵢ) = f(vⱼ), producing a lower-dimensional image).

The chain-level map f#_k: C_k(K) → C_k(L) is:
    f#_k([v₀,...,vₖ]) = 0                     if any images coincide (degenerate)
    f#_k([v₀,...,vₖ]) = sign(π) · [f(v_π(0)),...,f(v_π(k))]   otherwise
where π is the permutation sorting {f(v₀),...,f(vₖ)} into canonical (repr) order.

f# commutes with boundary (∂_L ∘ f# = f# ∘ ∂_K), so it induces f_* on homology.

The induced map on H_k uses extended Smith Normal Form to obtain cycle
representatives (via the shared ``_compute_homology_data`` machinery from
``mayer_vietoris``) and expresses the chain-level image in H_k(L) coordinates.

Cone and suspension
-------------------
cone_complex(K, apex) adds an apex vertex and joins it to every simplex:
    CK = K ∪ {σ ∪ {apex} : σ ∈ K} ∪ {{apex}}
CK is contractible: H_0(CK) = Z, H_k(CK) = 0 for k > 0.

suspension_complex(K, s, n) is the double cone K * S⁰:
    ΣK = K ∪ {σ ∪ {s} : σ ∈ K} ∪ {σ ∪ {n} : σ ∈ K} ∪ {{s},{n}}
For Sⁿ triangulated as K:  Σ(Sⁿ) ≃ Sⁿ⁺¹.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .homology import HomologyResult, _simplices_of_dimension
from .mayer_vietoris import _compute_homology_data, _induced_on_hk
from .simplices import Simplex
from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]


class SimplicialMapError(ValueError):
    """Raised when a simplicial map fails validation."""


@dataclass
class SimplicialMap:
    """A simplicial map f: K → L between finite simplicial complexes.

    Parameters
    ----------
    domain : SimplicialComplex
        Source complex K.
    codomain : SimplicialComplex
        Target complex L.
    vertex_map : dict
        Maps every vertex of ``domain`` to a vertex of ``codomain``.
        The map is valid if for every simplex {v₀,...,vₖ} ∈ K the image
        {f(v₀),...,f(vₖ)} is a simplex in L (collapsing is allowed).

    Raises
    ------
    SimplicialMapError
        If any domain vertex lacks an image, any image is outside the codomain,
        or any simplex fails to map into a codomain simplex.
    """

    domain: SimplicialComplex
    codomain: SimplicialComplex
    vertex_map: dict[Any, Any]

    def __post_init__(self) -> None:
        for v in self.domain.vertices:
            if v not in self.vertex_map:
                raise SimplicialMapError(
                    f"Vertex {v!r} in domain has no entry in vertex_map."
                )
        codomain_verts = self.codomain.vertices
        for fv in self.vertex_map.values():
            if fv not in codomain_verts:
                raise SimplicialMapError(
                    f"Image vertex {fv!r} is not a vertex of codomain."
                )
        codomain_simplices = {s.vertices for s in self.codomain.simplexes}
        for s in self.domain.simplexes:
            image = frozenset(self.vertex_map[v] for v in s.vertices)
            if image not in codomain_simplices:
                raise SimplicialMapError(
                    f"Image {set(image)} of domain simplex {set(s.vertices)} "
                    "is not a simplex in codomain."
                )


@dataclass
class InducedHomologyMap:
    """The induced map f_*: H_k(K;Z) → H_k(L;Z) on integral homology.

    Attributes
    ----------
    degree : int
        Homological degree k.
    domain_homology : HomologyResult
        H_k(K;Z) summary.
    codomain_homology : HomologyResult
        H_k(L;Z) summary.
    matrix : Matrix
        Integer matrix (rows = L generators, columns = K generators).
        Entry (i, j) is the H_k(L) coordinate of f_*(gⱼ) along generator gᵢ.
        Torsion generators come first, then free generators (matching the
        ordering used by ``_HomologyData.cycle_rep``).
    chain_matrix : Matrix
        The chain-level map f#_k: C_k(K) → C_k(L) as an integer matrix
        (rows = L k-simplices, columns = K k-simplices, canonical order).
    """

    degree: int
    domain_homology: HomologyResult
    codomain_homology: HomologyResult
    matrix: Matrix
    chain_matrix: Matrix


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _sort_sign(images: list[Any]) -> int:
    """Sign of the permutation that sorts ``images`` into canonical (repr) order.

    Returns +1 or -1.  Caller must ensure all entries are distinct.
    """
    sorted_imgs = sorted(images, key=repr)
    pos = {v: i for i, v in enumerate(images)}
    perm = [pos[v] for v in sorted_imgs]
    n = len(perm)
    visited = [False] * n
    sign = 1
    for i in range(n):
        if not visited[i]:
            j, length = i, 0
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                length += 1
            if length % 2 == 0:
                sign = -sign
    return sign


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def chain_map_matrix(sim_map: SimplicialMap, degree: int) -> Matrix:
    """Integer matrix of the chain map f#_k: C_k(K) → C_k(L).

    Rows are indexed by ``codomain``'s k-simplices in canonical order;
    columns by ``domain``'s k-simplices in canonical order.

    For each domain k-simplex σ = (v₀,...,vₖ):
    - If any two images coincide (degenerate): column is all zeros.
    - Otherwise: entry ±1 in the row corresponding to the sorted image,
      where the sign is the parity of the sorting permutation.

    Parameters
    ----------
    sim_map : SimplicialMap
    degree : int
        Chain degree k (≥ 0).

    Returns
    -------
    Matrix
        ``len(L_k) × len(K_k)`` integer matrix, or an empty matrix when
        either complex has no k-simplices.
    """
    if degree < 0:
        return []

    k_simp = _simplices_of_dimension(sim_map.domain, degree)
    l_simp = _simplices_of_dimension(sim_map.codomain, degree)

    n_k, n_l = len(k_simp), len(l_simp)
    if n_k == 0 or n_l == 0:
        return [[0] * n_k for _ in range(n_l)]

    l_idx = {s: i for i, s in enumerate(l_simp)}
    vm = sim_map.vertex_map
    mat: Matrix = [[0] * n_k for _ in range(n_l)]

    for col, sigma in enumerate(k_simp):
        images = [vm[v] for v in sigma]
        if len(set(images)) < len(images):
            continue
        sorted_img = tuple(sorted(images, key=repr))
        if sorted_img not in l_idx:
            continue
        sign = _sort_sign(images)
        mat[l_idx[sorted_img]][col] = sign

    return mat


def induced_map_on_homology(sim_map: SimplicialMap, degree: int) -> InducedHomologyMap:
    """Compute f_*: H_k(K;Z) → H_k(L;Z) induced by a simplicial map.

    Uses extended Smith Normal Form (via the shared ``mayer_vietoris`` machinery)
    to obtain cycle representatives for H_k(K) and express their chain-level
    images in the H_k(L) coordinate system.

    Parameters
    ----------
    sim_map : SimplicialMap
        A valid simplicial map f: K → L.
    degree : int
        Homological degree k (≥ 0).

    Returns
    -------
    InducedHomologyMap
        Contains the homology summaries, the chain-level matrix, and the
        integer matrix of the induced map on integral homology generators.

    Examples
    --------
    Identity map on S¹ (boundary of triangle) induces the identity on H₁ = Z:

    >>> from pytop.simplicial_complexes import SimplicialComplex
    >>> from pytop.simplices import Simplex
    >>> S1 = SimplicialComplex([Simplex([i]) for i in range(3)] +
    ...                        [Simplex([i,j]) for i,j in [(0,1),(0,2),(1,2)]])
    >>> vm = {0: 0, 1: 1, 2: 2}
    >>> f = SimplicialMap(S1, S1, vm)
    >>> r = induced_map_on_homology(f, 1)
    >>> r.matrix
    [[1]]
    """
    hdata_K = _compute_homology_data(sim_map.domain, degree)
    hdata_L = _compute_homology_data(sim_map.codomain, degree)
    f_chain = chain_map_matrix(sim_map, degree)
    hom_mat = _induced_on_hk(f_chain, hdata_K, hdata_L)

    return InducedHomologyMap(
        degree=degree,
        domain_homology=hdata_K.group,
        codomain_homology=hdata_L.group,
        matrix=hom_mat,
        chain_matrix=f_chain,
    )


def cone_complex(K: SimplicialComplex, apex: Any = "c") -> SimplicialComplex:
    """Return the cone CK = K ∗ {apex} over K.

    For every simplex σ ∈ K, adds σ ∪ {apex}.  The result is always
    contractible: H₀(CK) = Z, H_k(CK) = 0 for k > 0.

    Parameters
    ----------
    K : SimplicialComplex
    apex : Any
        Label for the new apex vertex.  Must not already appear in K.

    Returns
    -------
    SimplicialComplex
        Face-closed complex with ``|K| + (|K| + 1)`` simplices
        (original + one cone simplex per original simplex + apex).

    Raises
    ------
    ValueError
        If ``apex`` is already a vertex of K.
    """
    if apex in K.vertices:
        raise ValueError(f"Apex {apex!r} is already a vertex of K.")

    new_vsets: set[frozenset[Any]] = set()
    new_vsets.add(frozenset({apex}))
    for s in K.simplexes:
        new_vsets.add(s.vertices)
        new_vsets.add(s.vertices | {apex})

    return SimplicialComplex([Simplex(vs) for vs in new_vsets])


def suspension_complex(
    K: SimplicialComplex,
    south: Any = "s",
    north: Any = "n",
) -> SimplicialComplex:
    """Return the unreduced suspension ΣK = K ∗ S⁰ (double cone).

    Adds two new vertices ``south`` (s) and ``north`` (n) and for every
    simplex σ ∈ K adds σ ∪ {s} and σ ∪ {n}.  The suspension satisfies
    Σ(Sⁿ) ≃ Sⁿ⁺¹.

    Parameters
    ----------
    K : SimplicialComplex
    south, north : Any
        Labels for the suspension vertices.  Both must be absent from K and
        must be distinct from each other.

    Returns
    -------
    SimplicialComplex
        Face-closed complex: original K plus two cone copies (south and
        north) plus the two suspension points.

    Raises
    ------
    ValueError
        If ``south`` or ``north`` already appear in K, or if they are equal.
    """
    existing = K.vertices
    if south in existing:
        raise ValueError(f"south vertex {south!r} is already in K.")
    if north in existing:
        raise ValueError(f"north vertex {north!r} is already in K.")
    if south == north:
        raise ValueError("south and north must be distinct vertices.")

    new_vsets: set[frozenset[Any]] = set()
    new_vsets.add(frozenset({south}))
    new_vsets.add(frozenset({north}))
    for s in K.simplexes:
        new_vsets.add(s.vertices)
        new_vsets.add(s.vertices | {south})
        new_vsets.add(s.vertices | {north})

    return SimplicialComplex([Simplex(vs) for vs in new_vsets])
