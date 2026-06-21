"""Morse complex from a discrete gradient vector field.

P7.6 milestone — three public objects:

MorseChainComplex     : chain complex built from critical simplices
morse_chain_complex   : construct MorseChainComplex from a MorseMatching
morse_boundary_operator : boundary matrix ∂^M_k: C^M_k → C^M_{k-1}
morse_homology         : H_*(C^M; Z) and cross-validation against H_*(K; Z)

Mathematical background
-----------------------
Given a discrete Morse matching M on a simplicial complex K (Forman 1998),
the **Morse chain complex** is

    C^M_k = ⊕_{σ critical k-simplex} Z · σ

with boundary operator ∂^M: C^M_k → C^M_{k-1} defined by:

    ∂^M(σ) = Σ_{τ critical} n(σ, τ) · τ

where n(σ, τ) is the algebraic count of **gradient V-paths** from σ to τ.

A gradient V-path from a critical k-simplex σ to a critical (k-1)-simplex τ
is a sequence σ = c₀, f₁, c₁, f₂, ..., f_r, cᵣ where:
- fᵢ is a (k-1)-face of cᵢ₋₁
- (fᵢ, cᵢ) is a Morse pair for i < r  (fᵢ pairs with the next k-simplex cᵢ)
- fᵣ = τ is critical

The sign of a V-path is the product of incidence numbers along the path:

    sign = ε(c₀, f₁) × Π_{i=1}^{r-1} [-ε(cᵢ, fᵢ) · ε(cᵢ, fᵢ₊₁)]

where ε(σ, τ) = (-1)^i when τ is the face of σ obtained by removing the i-th
vertex (in canonical order).

**Morse homology theorem**: H_*(C^M; Z) ≅ H_*(K; Z) for any acyclic matching M.

Path counting uses DFS on the gradient graph.  The DFS is guaranteed to
terminate because the matching is acyclic.

References
----------
Forman, R. (1998). Morse theory for cell complexes.
  *Advances in Mathematics*, 134(1), 90–145.
Scoville, N. (2019). *Discrete Morse Theory*. AMS Student Mathematical Library.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .discrete_morse import MorseMatching
from .homology import HomologyResult, simplicial_homology, _smith_normal_form_python
from .simplices import Simplex
from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class MorseChainComplex:
    """The chain complex C^M_* built from critical simplices.

    Attributes
    ----------
    complex_obj : SimplicialComplex
        The original simplicial complex K.
    matching : MorseMatching
        The discrete gradient matching M on K.
    critical_simplices : dict[int, list[tuple]]
        Maps dimension k → list of critical k-simplices as sorted vertex tuples
        (in canonical order by repr).
    boundary_matrices : dict[int, Matrix]
        Maps k → ∂^M_k matrix (rows = critical (k-1)-simplices, columns =
        critical k-simplices, same order as ``critical_simplices``).
    """

    complex_obj: SimplicialComplex
    matching: MorseMatching
    critical_simplices: dict[int, list[tuple[Any, ...]]]
    boundary_matrices: dict[int, Matrix]

    def num_critical(self, k: int) -> int:
        """Number of critical k-simplices."""
        return len(self.critical_simplices.get(k, []))

    def morse_vector(self) -> tuple[int, ...]:
        """Tuple (m_0, m_1, ..., m_d) of critical cell counts."""
        max_k = max(self.critical_simplices.keys(), default=-1)
        if max_k < 0:
            return ()
        return tuple(self.num_critical(k) for k in range(max_k + 1))


@dataclass
class MorseHomologyResult:
    """Homology of the Morse complex, with cross-validation.

    Attributes
    ----------
    groups : list[HomologyResult]
        H_k(C^M; Z) for k = 0, 1, …, max_degree.
    validates : bool
        True if H_k(C^M) matches H_k(K) for all k (Morse homology theorem).
    """

    groups: list[HomologyResult]
    validates: bool

    def get(self, degree: int) -> HomologyResult:
        if 0 <= degree < len(self.groups):
            return self.groups[degree]
        return HomologyResult(degree=degree, betti=0, torsion=())


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _canonical_order(vertices: frozenset[Any]) -> tuple[Any, ...]:
    """Sort vertices by repr — same convention as homology.py."""
    return tuple(sorted(vertices, key=repr))


def _boundary_incidence(sigma_vs: tuple[Any, ...], face_vs: tuple[Any, ...]) -> int:
    """Return ε(σ, τ): the signed incidence number of face τ in ∂σ.

    τ is obtained by removing vertex i from σ (in canonical order), so
    ε(σ, τ) = (-1)^i.  Returns 0 if τ is not a codimension-one face of σ.
    """
    face_set = set(face_vs)
    for i, v in enumerate(sigma_vs):
        if v not in face_set:
            # Removing this vertex gives the face
            if len(sigma_vs) - 1 == len(face_vs):
                return (-1) ** i
    return 0


def _faces_of(sigma_vs: tuple[Any, ...]) -> list[tuple[Any, ...]]:
    """All codimension-one faces of sigma_vs as sorted vertex tuples."""
    return [sigma_vs[:i] + sigma_vs[i + 1:] for i in range(len(sigma_vs))]


# ---------------------------------------------------------------------------
# Core path-counting algorithm
# ---------------------------------------------------------------------------


def _count_morse_paths(
    sigma_vs: tuple[Any, ...],
    face_to_coface: dict[tuple[Any, ...], tuple[Any, ...]],
    is_critical_km1: set[tuple[Any, ...]],
) -> dict[tuple[Any, ...], int]:
    """Count signed gradient V-paths from critical k-simplex σ to critical (k-1)-simplices.

    Parameters
    ----------
    sigma_vs : tuple
        Sorted vertex tuple of the source critical k-simplex.
    face_to_coface : dict
        Maps (k-1)-simplex vertices → k-simplex vertices for each Morse pair
        at this dimension.  Only pairs with face-dim = k-1 are included.
    is_critical_km1 : set
        Set of critical (k-1)-simplex vertex tuples.

    Returns
    -------
    dict
        Maps critical (k-1)-simplex → algebraic count (integer).
    """
    counts: dict[tuple[Any, ...], int] = {}

    def dfs(
        current: tuple[Any, ...],
        acc_sign: int,
        came_from: tuple[Any, ...] | None,
    ) -> None:
        for face in _faces_of(current):
            if face == came_from:
                continue
            inc = _boundary_incidence(current, face)
            if face in is_critical_km1:
                counts[face] = counts.get(face, 0) + acc_sign * inc
            elif face in face_to_coface:
                coface = face_to_coface[face]
                step = -_boundary_incidence(coface, face)
                dfs(coface, acc_sign * inc * step, face)

    dfs(sigma_vs, 1, None)
    return counts


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def morse_boundary_operator(
    complex_obj: SimplicialComplex,
    matching: MorseMatching,
    k: int,
) -> Matrix:
    """Compute the Morse boundary matrix ∂^M_k: C^M_k → C^M_{k-1}.

    Rows are indexed by critical (k-1)-simplices, columns by critical
    k-simplices (both in canonical repr order).

    Parameters
    ----------
    complex_obj : SimplicialComplex
        The simplicial complex K.
    matching : MorseMatching
        A (valid) acyclic Morse matching on K.
    k : int
        Chain degree k (k ≥ 1).

    Returns
    -------
    Matrix
        Integer matrix of size ``|crit_{k-1}| × |crit_k|``.  Empty when
        either set of critical simplices is empty.

    Examples
    --------
    On the circle S¹ with matching leaving one vertex and one edge critical,
    ∂^M_1 is the 1×1 zero matrix (the edge is the H_1 generator):

    >>> # (See test file for a concrete example.)
    """
    if k <= 0:
        return []

    # Build lookup structures
    critical_k = sorted(
        [_canonical_order(s.vertices) for s in matching.critical if s.dimension == k],
        key=lambda vs: tuple(repr(v) for v in vs),
    )
    critical_km1 = sorted(
        [_canonical_order(s.vertices) for s in matching.critical if s.dimension == k - 1],
        key=lambda vs: tuple(repr(v) for v in vs),
    )

    if not critical_k or not critical_km1:
        return [[0] * len(critical_k) for _ in range(len(critical_km1))]

    is_crit_km1: set[tuple[Any, ...]] = set(critical_km1)

    # face_to_coface: maps (k-1)-simplex → k-simplex for Morse pairs at dim k
    face_to_coface: dict[tuple[Any, ...], tuple[Any, ...]] = {}
    for pair in matching.pairs:
        if pair.face.dimension == k - 1:
            fvs = _canonical_order(pair.face.vertices)
            cvs = _canonical_order(pair.coface.vertices)
            face_to_coface[fvs] = cvs

    km1_idx = {vs: i for i, vs in enumerate(critical_km1)}
    n_k = len(critical_k)
    n_km1 = len(critical_km1)
    mat: Matrix = [[0] * n_k for _ in range(n_km1)]

    for col, sigma_vs in enumerate(critical_k):
        path_counts = _count_morse_paths(sigma_vs, face_to_coface, is_crit_km1)
        for tau_vs, count in path_counts.items():
            if tau_vs in km1_idx:
                mat[km1_idx[tau_vs]][col] = count

    return mat


def morse_chain_complex(
    complex_obj: SimplicialComplex,
    matching: MorseMatching,
) -> MorseChainComplex:
    """Build the Morse chain complex C^M_* from a discrete gradient matching.

    Computes the critical simplices and all Morse boundary matrices via the
    gradient path-counting algorithm.

    Parameters
    ----------
    complex_obj : SimplicialComplex
        The simplicial complex K.
    matching : MorseMatching
        A valid acyclic Morse matching on K (use ``is_valid_morse_matching``
        to verify before calling).

    Returns
    -------
    MorseChainComplex
        Containing critical simplices (by dimension) and boundary matrices.

    Examples
    --------
    >>> from pytop.simplices import Simplex
    >>> from pytop.simplicial_complexes import SimplicialComplex
    >>> from pytop.discrete_morse import discrete_gradient_matching
    >>> circle = SimplicialComplex([
    ...     Simplex([0]), Simplex([1]), Simplex([2]),
    ...     Simplex([0,1]), Simplex([0,2]), Simplex([1,2]),
    ... ])
    >>> M = discrete_gradient_matching(circle)
    >>> cc = morse_chain_complex(circle, M)
    >>> cc.morse_vector()
    (1, 1)
    """
    if not matching.critical:
        max_dim = complex_obj.dimension
        return MorseChainComplex(
            complex_obj=complex_obj,
            matching=matching,
            critical_simplices={},
            boundary_matrices={},
        )

    max_dim = max(s.dimension for s in matching.critical)

    # Organise critical simplices by dimension (canonical order)
    critical_simplices: dict[int, list[tuple[Any, ...]]] = {}
    for k in range(max_dim + 1):
        critical_k = sorted(
            [_canonical_order(s.vertices) for s in matching.critical if s.dimension == k],
            key=lambda vs: tuple(repr(v) for v in vs),
        )
        critical_simplices[k] = critical_k

    # Compute boundary matrices
    boundary_matrices: dict[int, Matrix] = {}
    for k in range(1, max_dim + 1):
        boundary_matrices[k] = morse_boundary_operator(complex_obj, matching, k)

    return MorseChainComplex(
        complex_obj=complex_obj,
        matching=matching,
        critical_simplices=critical_simplices,
        boundary_matrices=boundary_matrices,
    )


def morse_homology(
    complex_obj: SimplicialComplex,
    matching: MorseMatching,
    max_degree: int | None = None,
) -> MorseHomologyResult:
    """Compute H_*(C^M; Z) and cross-validate against H_*(K; Z).

    Applies Smith Normal Form to the Morse boundary matrices and verifies
    the Morse homology theorem: H_*(C^M) ≅ H_*(K).

    Parameters
    ----------
    complex_obj : SimplicialComplex
        The simplicial complex K.
    matching : MorseMatching
        A valid acyclic Morse matching.
    max_degree : int | None
        Maximum degree to compute.  Defaults to the complex dimension + 1.

    Returns
    -------
    MorseHomologyResult
        With ``groups`` and a boolean ``validates`` flag.

    Examples
    --------
    For the circle with a Morse matching giving 1 vertex and 1 edge critical,
    the Morse complex has H_0 = Z and H_1 = Z:

    >>> # morse_homology(circle, M).groups[1].betti == 1  # ✓
    """
    cc = morse_chain_complex(complex_obj, matching)
    top = max_degree if max_degree is not None else complex_obj.dimension + 1

    groups: list[HomologyResult] = []
    for k in range(top + 1):
        n_k = cc.num_critical(k)
        if n_k == 0:
            groups.append(HomologyResult(degree=k, betti=0, torsion=()))
            continue

        # rank of ∂^M_k (boundary from k → k-1)
        mat_k = cc.boundary_matrices.get(k, [])
        if mat_k and any(any(v != 0 for v in row) for row in mat_k):
            inv_k = _smith_normal_form_python(mat_k)
            rank_k = len(inv_k)
        else:
            inv_k = []
            rank_k = 0

        # rank of ∂^M_{k+1} (boundary from k+1 → k)
        mat_k1 = cc.boundary_matrices.get(k + 1, [])
        if mat_k1 and any(any(v != 0 for v in row) for row in mat_k1):
            inv_k1 = _smith_normal_form_python(mat_k1)
            rank_k1 = len(inv_k1)
            torsion = tuple(d for d in inv_k1 if d > 1)
        else:
            inv_k1 = []
            rank_k1 = 0
            torsion = ()

        betti = n_k - rank_k - rank_k1
        groups.append(HomologyResult(degree=k, betti=max(0, betti), torsion=torsion))

    # Cross-validate against simplicial_homology
    validates = True
    for k in range(top + 1):
        morse_h = groups[k]
        simp_h = simplicial_homology(complex_obj, k)
        if morse_h.betti != simp_h.betti or set(morse_h.torsion) != set(simp_h.torsion):
            validates = False
            break

    return MorseHomologyResult(groups=groups, validates=validates)
