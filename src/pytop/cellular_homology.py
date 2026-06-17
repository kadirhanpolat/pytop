"""Cellular homology for finite CW complexes.

A CW complex X is given by:
  * cell counts   cell_counts[k] = number of k-cells
  * boundary maps boundary_maps[k] = d_k : C_k → C_{k-1}  (integer matrix)

The cellular chain complex

    0 → C_n ─d_n→ C_{n-1} → ⋯ ─d_1→ C_0 → 0

has  H_k = ker(d_k) / im(d_{k+1}),  computed by Smith Normal Form —
the same algorithm as :mod:`pytop.homology` but operating on the
(usually much smaller) cellular chain complex.

Key theorem: cellular homology is naturally isomorphic to singular homology.

Convenience constructors
────────────────────────
``cw_sphere(n)``                    S^n   — minimal: one 0-cell + one n-cell
``cw_real_projective_space(n)``     RP^n  — one cell per dimension 0…n
``cw_complex_projective_space(n)``  CP^n  — one cell per even dimension 0…2n
``cw_torus()``                      T²    — 1+2+1 cells
``cw_klein_bottle()``               Klein bottle — 1+2+1 cells
``cw_lens_space(p)``                L(p,1) in dimension 3, H₁ = Z/p
``cw_moore_space(n, k)``            M(Z/n, k): H_k = Z/n, H_0 = Z, rest 0
``cw_from_simplicial(K)``           cells = simplices of K (cross-validation)
"""
from __future__ import annotations

from dataclasses import dataclass

from .homology import HomologyResult, _smith_normal_form
from .homology import _simplices_of_dimension, boundary_matrix as _simplicial_bm
from .simplicial_complexes import SimplicialComplex

Matrix = list[list[int]]


# ── Matrix helper ─────────────────────────────────────────────────────────────

def _mat_mul(A: Matrix, B: Matrix) -> Matrix:
    if not A or not A[0] or not B or not B[0]:
        return [[0] * (len(B[0]) if B and B[0] else 0) for _ in range(len(A))]
    r, k, c = len(A), len(B), len(B[0])
    return [[sum(A[i][s] * B[s][j] for s in range(k)) for j in range(c)] for i in range(r)]


def _rank(M: Matrix) -> int:
    if not M or not M[0]:
        return 0
    return len(_smith_normal_form(M))


# ── CWComplex ─────────────────────────────────────────────────────────────────

class CWComplexError(ValueError):
    """Raised when a CW complex fails the chain-complex condition."""


@dataclass
class CWComplex:
    """A finite CW complex specified by cell counts and integer boundary maps.

    Parameters
    ----------
    cell_counts:
        Maps dimension k to the number of k-cells.  Keys with value 0 are
        silently ignored.
    boundary_maps:
        Maps dimension k to the integer matrix of d_k : C_k → C_{k-1}.
        The matrix must have shape
        ``(cell_counts.get(k-1, 0), cell_counts.get(k, 0))``.
        Omitted entries default to the zero matrix of the correct shape.
        The entry for k = 0 is meaningless (C_{-1} = 0) and ignored.
    require_chain_complex:
        When True (default) the constructor verifies d_{k-1} ∘ d_k = 0
        for all k and raises :class:`CWComplexError` on failure.
    """

    cell_counts: dict[int, int]
    boundary_maps: dict[int, Matrix]
    require_chain_complex: bool = True

    def __post_init__(self) -> None:
        self.cell_counts = {k: v for k, v in self.cell_counts.items() if v > 0}
        if self.require_chain_complex:
            violations = self.verify_chain_complex()
            if violations:
                raise CWComplexError(
                    "Chain-complex condition d∘d = 0 violated:\n  "
                    + "\n  ".join(violations)
                )

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def dimension(self) -> int:
        return max(self.cell_counts.keys(), default=0)

    def euler_characteristic(self) -> int:
        """Alternating sum of cell counts  χ = Σ (-1)^k · (#k-cells)."""
        return sum((-1) ** k * c for k, c in self.cell_counts.items())

    # ── Internal ─────────────────────────────────────────────────────────────

    def _boundary_matrix(self, k: int) -> Matrix:
        """Return d_k : C_k → C_{k-1} as an integer matrix."""
        n_k = self.cell_counts.get(k, 0)
        n_km1 = self.cell_counts.get(k - 1, 0) if k >= 1 else 0
        if k <= 0 or n_k == 0:
            return []
        if k in self.boundary_maps:
            return self.boundary_maps[k]
        return [[0] * n_k for _ in range(n_km1)]

    # ── Validation ───────────────────────────────────────────────────────────

    def verify_chain_complex(self) -> list[str]:
        """Return violation strings where d_{k-1} ∘ d_k ≠ 0 (empty = valid)."""
        violations: list[str] = []
        for k in range(2, self.dimension + 1):
            dk = self._boundary_matrix(k)
            dkm1 = self._boundary_matrix(k - 1)
            if not dk or not dk[0] or not dkm1 or not dkm1[0]:
                continue
            comp = _mat_mul(dkm1, dk)
            for i in range(len(comp)):
                for j in range(len(comp[i])):
                    if comp[i][j] != 0:
                        violations.append(
                            f"d_{k - 1} ∘ d_{k}: entry ({i},{j}) = {comp[i][j]}"
                        )
        return violations


# ── Cellular homology computation ────────────────────────────────────────────

def cellular_homology(cw: CWComplex, degree: int) -> HomologyResult:
    """Return H_{degree}(cw; Z) as a :class:`~pytop.homology.HomologyResult`.

    The group is computed from the cellular chain complex via Smith Normal
    Form — the identical algorithm to :func:`~pytop.homology.simplicial_homology`,
    but acting on the (typically much smaller) cellular chain groups.
    """
    if degree < 0:
        return HomologyResult(degree=degree, betti=0, torsion=())

    n_k = cw.cell_counts.get(degree, 0)
    if n_k == 0:
        return HomologyResult(degree=degree, betti=0, torsion=())

    rank_k = _rank(cw._boundary_matrix(degree))

    dk1 = cw._boundary_matrix(degree + 1)
    next_factors = _smith_normal_form(dk1) if (dk1 and dk1[0]) else []

    betti = (n_k - rank_k) - len(next_factors)
    torsion = tuple(f for f in next_factors if f > 1)
    return HomologyResult(degree=degree, betti=betti, torsion=torsion)


def cellular_homology_groups(cw: CWComplex) -> tuple[HomologyResult, ...]:
    """Return H_0, …, H_dim of ``cw``."""
    return tuple(cellular_homology(cw, k) for k in range(cw.dimension + 1))


def cellular_betti_numbers(cw: CWComplex) -> tuple[int, ...]:
    """Return (b_0, …, b_dim), the ranks of the integral homology groups."""
    return tuple(h.betti for h in cellular_homology_groups(cw))


def cellular_euler_characteristic(cw: CWComplex) -> int:
    """Alternating sum of Betti numbers — equals ``cw.euler_characteristic()``."""
    return sum((-1) ** k * b for k, b in enumerate(cellular_betti_numbers(cw)))


# ── Convenience constructors ─────────────────────────────────────────────────

def cw_sphere(n: int) -> CWComplex:
    """Minimal CW structure on S^n.

    S^0 uses two 0-cells; S^n (n ≥ 1) uses one 0-cell and one n-cell.
    All boundary maps are zero.

    H_0 = Z,  H_n = Z  (n ≥ 1),  H_k = 0 otherwise.
    H_0(S^0) = Z^2.
    """
    if n < 0:
        raise ValueError(f"n must be ≥ 0, got {n}.")
    if n == 0:
        return CWComplex(cell_counts={0: 2}, boundary_maps={})
    return CWComplex(cell_counts={0: 1, n: 1}, boundary_maps={})


def cw_real_projective_space(n: int) -> CWComplex:
    """Standard CW structure on RP^n: one cell per dimension 0…n.

    Boundary maps  d_k = 1 + (−1)^k  (scalar, i.e. a 1×1 matrix):
      d_1 = 0,   d_k = 0 for k odd ≥ 3,   d_k = 2 for k even ≥ 2.

    Known homology (integral):
      H_0 = Z
      H_k = Z/2   for k odd, 0 < k < n
      H_n = Z     if n is odd
      H_n = 0     if n is even  (n > 0)
      H_k = 0     otherwise
    """
    if n < 0:
        raise ValueError(f"n must be ≥ 0, got {n}.")
    if n == 0:
        return CWComplex(cell_counts={0: 1}, boundary_maps={})

    cell_counts = {k: 1 for k in range(n + 1)}
    boundary_maps: dict[int, Matrix] = {1: [[0]]}
    for k in range(2, n + 1):
        boundary_maps[k] = [[1 + (-1) ** k]]   # 0 if k odd, 2 if k even
    return CWComplex(cell_counts=cell_counts, boundary_maps=boundary_maps)


def cw_complex_projective_space(n: int) -> CWComplex:
    """Standard CW structure on CP^n: one cell in each even dimension 0, 2, …, 2n.

    All boundary maps are zero (no cells in odd dimensions).

    H_{2k} = Z  for 0 ≤ k ≤ n,  H_odd = 0.
    """
    if n < 0:
        raise ValueError(f"n must be ≥ 0, got {n}.")
    return CWComplex(cell_counts={2 * k: 1 for k in range(n + 1)}, boundary_maps={})


def cw_torus() -> CWComplex:
    """Standard CW structure on T² = S¹ × S¹.

    Cells: one 0-cell, two 1-cells a and b, one 2-cell F.
      d_1 = [[0, 0]]      (both 1-cells are loops)
      d_2 = [[0], [0]]    (word aba⁻¹b⁻¹ → 0 in the abelianisation)

    H_0 = Z,  H_1 = Z²,  H_2 = Z.
    """
    return CWComplex(
        cell_counts={0: 1, 1: 2, 2: 1},
        boundary_maps={1: [[0, 0]], 2: [[0], [0]]},
    )


def cw_klein_bottle() -> CWComplex:
    """Standard CW structure on the Klein bottle.

    Cells: one 0-cell, two 1-cells a and b, one 2-cell F.
      d_1 = [[0, 0]]     (both 1-cells are loops)
      d_2 = [[0], [2]]   (word aba⁻¹b → coefficient 2 on b in abelianisation)

    H_0 = Z,  H_1 = Z ⊕ Z/2,  H_2 = 0.
    """
    return CWComplex(
        cell_counts={0: 1, 1: 2, 2: 1},
        boundary_maps={1: [[0, 0]], 2: [[0], [2]]},
    )


def cw_lens_space(p: int) -> CWComplex:
    """Standard CW structure on the 3-dimensional lens space L(p, 1).

    Cells: one cell in each dimension 0, 1, 2, 3.
      d_1 = [[0]],  d_2 = [[p]],  d_3 = [[0]]

    H_0 = Z,  H_1 = Z/p  (Z if p = 0),  H_2 = 0,  H_3 = Z.
    For p = 0:  L(0,1) = S² × S¹ in this model; H_1 = Z.
    """
    if p < 0:
        raise ValueError(f"p must be ≥ 0, got {p}.")
    return CWComplex(
        cell_counts={0: 1, 1: 1, 2: 1, 3: 1},
        boundary_maps={1: [[0]], 2: [[p]], 3: [[0]]},
    )


def cw_moore_space(n: int, k: int) -> CWComplex:
    """CW model of the Moore space M(Z/n, k).

    A Moore space M(Z/n, k) has H_k = Z/n, H_0 = Z, H_i = 0 otherwise.

    Construction: take S^k and attach a (k+1)-cell via a degree-n map.
      For k = 1:   cells {e⁰, e¹, e²},       d_1 = [[0]], d_2 = [[n]].
      For k ≥ 2:   cells {e⁰, e^k, e^{k+1}}, d_{k+1} = [[n]].

    Requires n ≥ 2, k ≥ 1.
    """
    if n < 2:
        raise ValueError(f"n must be ≥ 2 for a nontrivial Moore space, got {n}.")
    if k < 1:
        raise ValueError(f"k must be ≥ 1, got {k}.")
    if k == 1:
        return CWComplex(
            cell_counts={0: 1, 1: 1, 2: 1},
            boundary_maps={1: [[0]], 2: [[n]]},
        )
    return CWComplex(
        cell_counts={0: 1, k: 1, k + 1: 1},
        boundary_maps={k + 1: [[n]]},
    )


def cw_from_simplicial(complex_obj: SimplicialComplex) -> CWComplex:
    """Construct a CW complex from a simplicial complex.

    Each k-simplex becomes a k-cell; the cellular boundary maps are the
    simplicial boundary matrices.  Since cellular homology is isomorphic
    to simplicial homology, this provides an exact cross-validation bridge:

        cellular_homology(cw_from_simplicial(K), k) == simplicial_homology(K, k)
    """
    dim = complex_obj.dimension
    cell_counts: dict[int, int] = {}
    boundary_maps: dict[int, Matrix] = {}

    for k in range(dim + 1):
        count = len(_simplices_of_dimension(complex_obj, k))
        if count > 0:
            cell_counts[k] = count

    for k in range(1, dim + 1):
        if cell_counts.get(k, 0) > 0 and cell_counts.get(k - 1, 0) > 0:
            mat = _simplicial_bm(complex_obj, k)
            if mat and mat[0]:
                boundary_maps[k] = mat

    return CWComplex(cell_counts=cell_counts, boundary_maps=boundary_maps)


__all__ = [
    "CWComplex",
    "CWComplexError",
    "cellular_homology",
    "cellular_homology_groups",
    "cellular_betti_numbers",
    "cellular_euler_characteristic",
    "cw_sphere",
    "cw_real_projective_space",
    "cw_complex_projective_space",
    "cw_torus",
    "cw_klein_bottle",
    "cw_lens_space",
    "cw_moore_space",
    "cw_from_simplicial",
]
