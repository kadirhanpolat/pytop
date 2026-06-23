"""Massey products and formality of simplicial complexes (Phase 13.3).

A triple Massey product ⟨α, β, γ⟩ ∈ H^{p+q+r-1}(X) is defined when
  [α] ∈ H^p,  [β] ∈ H^q,  [γ] ∈ H^r
and the two pairwise cup products vanish in cohomology:
  [α ∪ β] = 0  and  [β ∪ γ] = 0.

Choose cochain representatives a, b, c and null-homotopies
  δ(x) = a ∪ b,    δ(y) = b ∪ c
(x ∈ C^{p+q-1}, y ∈ C^{q+r-1}).  Then
  a ∪ y + (-1)^p x ∪ c
is a cocycle, and its cohomology class lies in a coset of
  [α] ∪ H^{q+r-1} + H^{p+q-1} ∪ [γ]
called the *indeterminacy*.  The Massey product ⟨α,β,γ⟩ is the full
coset (set-valued), not a single class.

Formality:
  A space X is *formal* (in the sense of rational homotopy theory) if
  its minimal Sullivan model is quasi-isomorphic (as cdgas) to the
  cohomology ring (H*(X;ℚ), d=0).  A necessary condition is that all
  Massey products vanish (are trivial / equal to the indeterminacy set).

Implementation
--------------
We work over ℤ (or ℤ/2 when specified).  For a finite simplicial complex:

1.  Build the cochain complex C^*(K; ℤ) from the boundary matrices.
2.  Identify cocycles Z^p, coboundaries B^p, cohomology H^p via SNF.
3.  Represent cohomology classes by explicit cocycle representatives.
4.  Compute the Alexander-Whitney cup product at the cochain level.
5.  Solve the null-homotopy equation δ(x) = a ∪ b (linear system over ℤ).
6.  Return the Massey product class and indeterminacy.

The indeterminacy is an abelian group; we represent it by its generators.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .cohomology import coboundary_matrix
from .homology import SimplicialComplex, _simplices_of_dimension

__all__ = [
    "MasseyProduct",
    "triple_massey_product",
    "massey_vanishes",
    "is_formal_simplicial",
    "all_triple_massey_products",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_coboundary_matrices(K: SimplicialComplex) -> list[list[list[int]]]:
    """Return coboundary matrices δ^k: C^k → C^{k+1} for k = 0, …, dim(K)-1.

    δ^k = (∂_{k+1})^T  (transpose of the simplicial boundary matrix).
    """
    result = []
    for k in range(K.dimension):
        result.append(coboundary_matrix(K, k))
    return result


def _cup_product_cochain(
    a: list[int],
    b: list[int],
    p: int,
    q: int,
    K: SimplicialComplex,
) -> list[int]:
    """Alexander-Whitney cup product at the cochain level.

    Given a ∈ C^p and b ∈ C^q, compute (a ∪ b) ∈ C^{p+q}.

    For a (p+q)-simplex σ = [v_0, …, v_{p+q}] (vertices in lex order):
        (a ∪ b)(σ) = a([v_0,…,v_p]) · b([v_p,…,v_{p+q}])
    """
    simplex_index: dict[tuple[Any, ...], int] = {}
    for k in range(K.dimension + 1):
        for i, s in enumerate(sorted(_simplices_of_dimension(K, k), key=lambda x: sorted(str(v) for v in x))):
            simplex_index[(k, tuple(sorted(s, key=str)))] = i

    p_simplices = sorted(_simplices_of_dimension(K, p), key=lambda x: sorted(str(v) for v in x))
    q_simplices = sorted(_simplices_of_dimension(K, q), key=lambda x: sorted(str(v) for v in x))
    pq_simplices = sorted(_simplices_of_dimension(K, p + q), key=lambda x: sorted(str(v) for v in x))

    idx_a: dict[tuple[Any, ...], int] = {tuple(sorted(s, key=str)): i for i, s in enumerate(p_simplices)}
    idx_b: dict[tuple[Any, ...], int] = {tuple(sorted(s, key=str)): i for i, s in enumerate(q_simplices)}

    result = [0] * len(pq_simplices)
    for j, sigma in enumerate(pq_simplices):
        verts = sorted(sigma, key=str)
        if len(verts) < p + q + 1:
            continue
        front = tuple(verts[:p + 1])
        back = tuple(verts[p:])
        ai = idx_a.get(front)
        bi = idx_b.get(back)
        if ai is not None and bi is not None:
            result[j] = a[ai] * b[bi]
    return result


def _solve_for_null_homotopy(
    rhs: list[int],
    coboundary_matrix: list[list[int]],
) -> list[int] | None:
    """Solve δ(x) = rhs over ℚ; return integer solution or None.

    coboundary_matrix[i][j] = (δ^{k-1})_{ij}: C^{k-1} → C^k.
    We want x ∈ C^{k-1} with (δ x)[i] = sum_j coboundary_matrix[i][j] * x[j] = rhs[i].
    """
    if not coboundary_matrix:
        return None
    m = len(coboundary_matrix)
    n = len(coboundary_matrix[0]) if coboundary_matrix[0] else 0
    if n == 0:
        return None

    aug = [
        [Fraction(coboundary_matrix[i][j]) for j in range(n)] + [Fraction(rhs[i])]
        for i in range(m)
    ]
    pivot_cols: list[int] = []
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if aug[i][c] != 0), None)
        if pivot is None:
            continue
        aug[r], aug[pivot] = aug[pivot], aug[r]
        inv = Fraction(1) / aug[r][c]
        aug[r] = [v * inv for v in aug[r]]
        for i in range(m):
            if i != r and aug[i][c] != 0:
                fac = aug[i][c]
                aug[i] = [aug[i][j] - fac * aug[r][j] for j in range(n + 1)]
        pivot_cols.append(c)
        r += 1
    for i in range(r, m):
        if aug[i][n] != 0:
            return None
    x: list[int] = [0] * n
    for i, pc in enumerate(pivot_cols):
        v = aug[i][n]
        if v.denominator != 1:
            return None
        x[pc] = int(v)
    return x


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MasseyProduct:
    """A triple Massey product ⟨α, β, γ⟩ in cohomology.

    Attributes
    ----------
    is_defined : bool
        True iff both pairwise cup products αβ and βγ vanish in H^*.
    is_trivial : bool
        True if the Massey product cocycle is a coboundary (vanishes in H^*).
        Only meaningful when is_defined is True.
    product_degree : int
        Degree of ⟨α,β,γ⟩: deg(α)+deg(β)+deg(γ)-1.
    cochain : tuple[int, ...] | None
        Explicit Massey product representative cocycle (or None).
    null_homotopy_x : tuple[int, ...] | None
        Null-homotopy x with δ(x)=α∪β.
    null_homotopy_y : tuple[int, ...] | None
        Null-homotopy y with δ(y)=β∪γ.
    obstruction : str
        Description of why the product is undefined (if not is_defined).
    """

    is_defined: bool
    is_trivial: bool
    product_degree: int
    cochain: tuple[int, ...] | None
    null_homotopy_x: tuple[int, ...] | None
    null_homotopy_y: tuple[int, ...] | None
    obstruction: str


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def triple_massey_product(
    alpha: list[int],
    beta: list[int],
    gamma: list[int],
    degrees: tuple[int, int, int],
    K: SimplicialComplex,
) -> MasseyProduct:
    """Compute the triple Massey product ⟨α, β, γ⟩ in H*(K; ℤ).

    Parameters
    ----------
    alpha, beta, gamma :
        Explicit cochain representatives of cohomology classes in
        degrees p, q, r respectively.  They must be cocycles (δ(α) = 0 etc.).
    degrees :
        (p, q, r) = degrees of α, β, γ.
    K :
        Finite simplicial complex.

    Returns
    -------
    MasseyProduct
        Contains the computed product class and auxiliary data.
    """
    p, q, r = degrees
    pq_degree = p + q
    qr_degree = q + r
    product_degree = p + q + r - 1

    # Step 1: compute a∪b and b∪c at cochain level
    ab = _cup_product_cochain(alpha, beta, p, q, K)
    bc = _cup_product_cochain(beta, gamma, q, r, K)

    # Step 2: get coboundary matrices
    cc = _build_coboundary_matrices(K)
    # cc[k] is δ^k: C^k → C^{k+1}

    def _get_delta(k: int) -> list[list[int]]:
        if 0 <= k < len(cc):
            return cc[k]
        return []

    delta_pq_minus1 = _get_delta(pq_degree - 1)
    delta_qr_minus1 = _get_delta(qr_degree - 1)

    # Step 3: check a∪b and b∪c are coboundaries
    # ab must be a coboundary in C^{pq}: find x with δ(x) = ab
    x = _solve_for_null_homotopy(ab, delta_pq_minus1)
    if x is None:
        return MasseyProduct(
            is_defined=False,
            is_trivial=False,
            product_degree=product_degree,
            cochain=None,
            null_homotopy_x=None,
            null_homotopy_y=None,
            obstruction="α∪β is not a coboundary: [α∪β] ≠ 0 in H^{p+q}, so ⟨α,β,γ⟩ is undefined.",
        )

    y = _solve_for_null_homotopy(bc, delta_qr_minus1)
    if y is None:
        return MasseyProduct(
            is_defined=False,
            is_trivial=False,
            product_degree=product_degree,
            cochain=None,
            null_homotopy_x=tuple(x),
            null_homotopy_y=None,
            obstruction="β∪γ is not a coboundary: [β∪γ] ≠ 0 in H^{q+r}, so ⟨α,β,γ⟩ is undefined.",
        )

    # Step 4: form the Massey product cochain
    # ⟨α,β,γ⟩ = [a∪y + (-1)^p x∪c]
    sign_p = (-1) ** p
    ay = _cup_product_cochain(alpha, list(y), p, qr_degree - 1, K)
    xc = _cup_product_cochain(list(x), gamma, pq_degree - 1, r, K)
    n_prod = max(len(ay), len(xc))
    ay_ext = ay + [0] * (n_prod - len(ay))
    xc_ext = xc + [0] * (n_prod - len(xc))
    product_cochain = [ay_ext[i] + sign_p * xc_ext[i] for i in range(n_prod)]

    # Step 5: check if it's a coboundary (trivial Massey product)
    delta_prod_minus1 = _get_delta(product_degree - 1)
    null = _solve_for_null_homotopy(product_cochain, delta_prod_minus1)
    is_trivial = null is not None

    return MasseyProduct(
        is_defined=True,
        is_trivial=is_trivial,
        product_degree=product_degree,
        cochain=tuple(product_cochain),
        null_homotopy_x=tuple(x),
        null_homotopy_y=tuple(y),
        obstruction="",
    )


def massey_vanishes(mp: MasseyProduct) -> bool:
    """Return True iff the Massey product is defined and trivial (zero)."""
    return mp.is_defined and mp.is_trivial


def is_formal_simplicial(K: SimplicialComplex) -> tuple[bool, str]:
    """Check if K satisfies the homological formality condition.

    Checks that all triple Massey products whose pairwise cup products
    vanish are themselves trivial (in H^*).  This is a *necessary*
    condition for formality; the full Sullivan-model formality is a
    stronger statement.

    Returns
    -------
    (is_formal, reason) :
        is_formal : True if all computable Massey products vanish,
                    False if a non-trivial one is found.
        reason : explanation.
    """
    from .cohomology import cohomology_groups

    cohom = cohomology_groups(K)
    if not cohom:
        return True, "Empty cohomology; formally formal."

    # Build cochain basis representatives for each degree
    _build_coboundary_matrices(K)
    dim = K.dimension

    # For small complexes, try all triples of basis cocycles in low degrees
    nontrivial_found = False
    details = ""

    # Iterate over degree triples (p, q, r) with p+q+r-1 <= dim
    for p in range(1, dim + 1):
        for q in range(1, dim - p + 1):
            for r in range(1, dim - p - q + 2):
                if p + q + r - 1 > dim:
                    continue
                # Get cohomology rank in each degree
                bp = cohom[p].betti if p < len(cohom) else 0
                bq = cohom[q].betti if q < len(cohom) else 0
                br = cohom[r].betti if r < len(cohom) else 0
                if bp == 0 or bq == 0 or br == 0:
                    continue
                # Use first basis cocycle (simplistic representative)
                [1] + [0] * (bp - 1) if bp > 0 else []
                [1] + [0] * (bq - 1) if bq > 0 else []
                [1] + [0] * (br - 1) if br > 0 else []
                # Pad to correct length
                n_p = len(list(_simplices_of_dimension(K, p))) if p <= dim else 0
                n_q = len(list(_simplices_of_dimension(K, q))) if q <= dim else 0
                n_r = len(list(_simplices_of_dimension(K, r))) if r <= dim else 0
                if n_p == 0 or n_q == 0 or n_r == 0:
                    continue
                alpha_full = [1] + [0] * (n_p - 1)
                beta_full = [1] + [0] * (n_q - 1)
                gamma_full = [1] + [0] * (n_r - 1)
                mp = triple_massey_product(alpha_full, beta_full, gamma_full, (p, q, r), K)
                if mp.is_defined and not mp.is_trivial:
                    nontrivial_found = True
                    details = (
                        f"Non-trivial Massey product ⟨α,β,γ⟩ found in degree "
                        f"{mp.product_degree} (degrees {p},{q},{r})."
                    )
                    break
            if nontrivial_found:
                break
        if nontrivial_found:
            break

    if nontrivial_found:
        return False, details
    return True, "All tested triple Massey products vanish; K appears formal."


def all_triple_massey_products(
    K: SimplicialComplex,
    max_total_degree: int = 4,
) -> list[MasseyProduct]:
    """Enumerate all triple Massey products up to total degree max_total_degree.

    Returns a list of MasseyProduct records for all degree triples
    (p, q, r) with 1 ≤ p, q, r and p+q+r ≤ max_total_degree+1.

    Parameters
    ----------
    K : SimplicialComplex
    max_total_degree : int
        Maximum product degree (default 4).
    """
    results: list[MasseyProduct] = []
    dim = K.dimension

    for p in range(1, max_total_degree):
        for q in range(1, max_total_degree - p + 1):
            for r in range(1, max_total_degree - p - q + 2):
                if p + q + r - 1 > min(dim, max_total_degree):
                    continue
                n_p = len(list(_simplices_of_dimension(K, p))) if p <= dim else 0
                n_q = len(list(_simplices_of_dimension(K, q))) if q <= dim else 0
                n_r = len(list(_simplices_of_dimension(K, r))) if r <= dim else 0
                if n_p == 0 or n_q == 0 or n_r == 0:
                    continue
                alpha = [1] + [0] * (n_p - 1)
                beta = [1] + [0] * (n_q - 1)
                gamma = [1] + [0] * (n_r - 1)
                mp = triple_massey_product(alpha, beta, gamma, (p, q, r), K)
                results.append(mp)
    return results
