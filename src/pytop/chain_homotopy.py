"""Chain homotopies and algebraic homotopy equivalence (Phase 13.1).

A chain homotopy h: C_* → D_{*+1} between chain maps f, g: C_* → D_*
satisfies the chain-homotopy equation

    f_k - g_k = ∂^D_{k+1} ∘ h_k + h_{k-1} ∘ ∂^C_k   for all k.

Chain-homotopic maps induce equal maps on homology.  Two chain complexes
C_* and D_* are *chain-homotopy equivalent* if there exist chain maps
f: C→D and g: D→C with g∘f ≃ id_C and f∘g ≃ id_D.

Splitting theorem (Munkres): every finitely generated free chain complex
over ℤ is chain-homotopy equivalent to its homology (with zero differential).
Consequently two such complexes are chain-homotopy equivalent iff their
integral homology groups are isomorphic in every degree.

Functions
---------
is_chain_homotopy
    Verify the chain-homotopy equation matrix-by-matrix.
find_chain_homotopy
    Solve for h: C_k → D_{k+1} by back-substitution over ℚ.
chain_homotopy_equiv
    Decide chain-homotopy equivalence from graded homology data.
homotopy_equivalence_simplicial
    Decide simplicial homotopy equivalence using all computable
    invariants (Betti numbers, torsion, Euler characteristic).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .homology import SimplicialComplex, homology_groups

Matrix = list[list[int]]

__all__ = [
    "ChainHomotopyResult",
    "HomotopyEquivalenceVerdict",
    "is_chain_homotopy",
    "find_chain_homotopy",
    "chain_homotopy_equiv",
    "homotopy_equivalence_simplicial",
]


# ---------------------------------------------------------------------------
# Internal matrix helpers
# ---------------------------------------------------------------------------

def _mmul(A: Matrix, B: Matrix) -> Matrix:
    if not A or not B or not B[0]:
        return []
    m, k, n = len(A), len(A[0]), len(B[0])
    return [
        [sum(A[i][p] * B[p][j] for p in range(k)) for j in range(n)]
        for i in range(m)
    ]


def _msub(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _madd(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _zero(m: int, n: int) -> Matrix:
    return [[0] * n for _ in range(m)]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ChainHomotopyResult:
    """Outcome of a chain-homotopy verification.

    Attributes
    ----------
    is_valid : bool
        True iff ∂^D h_k + h_{k-1} ∂^C_k = f_k - g_k holds at every k.
    equation_errors : tuple[int, ...]
        Sum of |A_{ij} - B_{ij}| at each degree k.  All zeros for a valid
        homotopy.
    """

    is_valid: bool
    equation_errors: tuple[int, ...]


@dataclass(frozen=True)
class HomotopyEquivalenceVerdict:
    """Verdict of the homotopy-equivalence test between two spaces/complexes.

    Attributes
    ----------
    verdict : str
        ``"equivalent"``, ``"not_equivalent"``, or ``"undecidable"``.
    reason : str
        Human-readable justification.
    betti_K, betti_L : tuple[int, ...]
        Betti numbers of K and L (padded to the same length).
    euler_K, euler_L : int
        Euler characteristics.
    """

    verdict: str
    reason: str
    betti_K: tuple[int, ...]
    betti_L: tuple[int, ...]
    euler_K: int
    euler_L: int

    @property
    def is_equivalent(self) -> bool:
        return self.verdict == "equivalent"

    @property
    def is_not_equivalent(self) -> bool:
        return self.verdict == "not_equivalent"


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def is_chain_homotopy(
    f: list[Matrix],
    g: list[Matrix],
    h: list[Matrix],
    boundary_C: list[Matrix],
    boundary_D: list[Matrix],
) -> ChainHomotopyResult:
    """Verify that h is a chain homotopy from f to g.

    Checks ∂^D_{k+1} h_k + h_{k-1} ∂^C_k = f_k - g_k for each k.

    Parameters
    ----------
    f, g :
        Chain maps f_k, g_k: C_k → D_k.
    h :
        Proposed chain homotopy h_k: C_k → D_{k+1}.
    boundary_C :
        ∂^C_k: C_k → C_{k-1}.
    boundary_D :
        ∂^D_k: D_k → D_{k-1}.

    Returns
    -------
    ChainHomotopyResult
    """
    n = len(f)
    errors: list[int] = []

    for k in range(n):
        fk, gk = f[k], g[k]
        if not fk or not fk[0]:
            errors.append(0)
            continue
        rhs = _msub(fk, gk)
        rows, cols = len(rhs), len(rhs[0])

        # ∂^D_{k+1} h_k
        if k < len(h) and h[k] and (k + 1) < len(boundary_D) and boundary_D[k + 1]:
            t1: Matrix = _mmul(boundary_D[k + 1], h[k])
        else:
            t1 = _zero(rows, cols)

        # h_{k-1} ∂^C_k
        if k >= 1 and (k - 1) < len(h) and h[k - 1] and k < len(boundary_C) and boundary_C[k]:
            t2: Matrix = _mmul(h[k - 1], boundary_C[k])
        else:
            t2 = _zero(rows, cols)

        lhs = _madd(t1, t2)
        err = sum(abs(lhs[i][j] - rhs[i][j]) for i in range(rows) for j in range(cols))
        errors.append(err)

    return ChainHomotopyResult(is_valid=all(e == 0 for e in errors), equation_errors=tuple(errors))


def find_chain_homotopy(
    f: list[Matrix],
    g: list[Matrix],
    boundary_C: list[Matrix],
    boundary_D: list[Matrix],
) -> tuple[list[Matrix] | None, str]:
    """Attempt to find a chain homotopy h: C_* → D_{*+1} with f ≃ g over ℤ.

    Solves ∂^D_{k+1} h_k = (f_k - g_k) - h_{k-1} ∂^C_k inductively
    using exact-fraction Gaussian elimination (over ℚ).

    Returns
    -------
    (h, message)
        h : list of integer matrices on success; None if no solution exists.
        message : human-readable result.
    """

    def _frac_solve(A_rows: list[list[int]], b: list[int]) -> list[Fraction] | None:
        m = len(A_rows)
        if m == 0:
            return []
        n = len(A_rows[0]) if A_rows[0] else 0
        aug = [
            [Fraction(A_rows[i][j]) for j in range(n)] + [Fraction(b[i])]
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
        x = [Fraction(0)] * n
        for i, pc in enumerate(pivot_cols):
            x[pc] = aug[i][n]
        return x

    n = len(f)
    h_out: list[Matrix] = []
    prev_h: Matrix = []

    for k in range(n):
        fk, gk = f[k], g[k]
        if not fk or not fk[0]:
            h_out.append([])
            continue

        d_rows, d_cols = len(fk), len(fk[0])
        residual = _msub(fk, gk)

        if prev_h and k < len(boundary_C) and boundary_C[k]:
            corr = _mmul(prev_h, boundary_C[k])
            residual = _msub(residual, corr)

        if (k + 1) < len(boundary_D) and boundary_D[k + 1]:
            dD = boundary_D[k + 1]
            dkp1_rows = len(dD[0]) if dD and dD[0] else 0
            hk_cols: list[list[Fraction]] = []
            for j in range(d_cols):
                b_col = [residual[i][j] for i in range(d_rows)]
                x = _frac_solve(dD, b_col)
                if x is None:
                    return None, f"No chain homotopy: degree-{k} system inconsistent over ℚ."
                hk_cols.append(x)
            hk: Matrix = []
            for i in range(dkp1_rows):
                row_vals: list[int] = []
                for j in range(d_cols):
                    v = hk_cols[j][i]
                    if v.denominator != 1:
                        return None, f"Chain homotopy exists over ℚ but not over ℤ at degree {k}."
                    row_vals.append(int(v))
                hk.append(row_vals)
        else:
            hk = []

        h_out.append(hk)
        prev_h = hk

    return h_out, "Chain homotopy found over ℤ."


def chain_homotopy_equiv(
    betti_C: list[int],
    torsion_C: list[tuple[int, ...]],
    betti_D: list[int],
    torsion_D: list[tuple[int, ...]],
) -> HomotopyEquivalenceVerdict:
    """Decide chain-homotopy equivalence from graded integral homology data.

    By the splitting theorem every finitely generated free chain complex
    over ℤ is chain-homotopy equivalent to its homology complex (with zero
    differential).  Two such complexes are therefore chain-homotopy equivalent
    iff H_k(C) ≅ H_k(D) as abelian groups for every k.

    Parameters
    ----------
    betti_C, betti_D :
        Free ranks β_k of H_k(C) and H_k(D).
    torsion_C, torsion_D :
        Torsion invariant factors (sorted) of H_k.
    """
    n = max(len(betti_C), len(betti_D))
    bC = list(betti_C) + [0] * (n - len(betti_C))
    bD = list(betti_D) + [0] * (n - len(betti_D))
    tC = list(torsion_C) + [()] * (n - len(torsion_C))
    tD = list(torsion_D) + [()] * (n - len(torsion_D))
    eC = sum((-1) ** k * b for k, b in enumerate(bC))
    eD = sum((-1) ** k * b for k, b in enumerate(bD))

    for k in range(n):
        if bC[k] != bD[k] or tuple(sorted(tC[k])) != tuple(sorted(tD[k])):
            return HomotopyEquivalenceVerdict(
                verdict="not_equivalent",
                reason=(
                    f"H_{k} differs: C has ℤ^{bC[k]}⊕{tC[k]}, "
                    f"D has ℤ^{bD[k]}⊕{tD[k]}."
                ),
                betti_K=tuple(bC),
                betti_L=tuple(bD),
                euler_K=eC,
                euler_L=eD,
            )

    return HomotopyEquivalenceVerdict(
        verdict="equivalent",
        reason=(
            "All integral homology groups agree; splitting theorem implies "
            "chain-homotopy equivalence of the free chain complexes."
        ),
        betti_K=tuple(bC),
        betti_L=tuple(bD),
        euler_K=eC,
        euler_L=eD,
    )


def homotopy_equivalence_simplicial(
    K: SimplicialComplex,
    L: SimplicialComplex,
) -> HomotopyEquivalenceVerdict:
    """Decide (up to computable invariants) if K and L are homotopy equivalent.

    Tests in order:
    1. Euler characteristic χ(K) vs χ(L).
    2. Betti numbers β_k(K) vs β_k(L) in every degree.
    3. Torsion invariant factors of H_k in every degree.

    Any mismatch → ``"not_equivalent"`` (rigorous).
    All agree → ``"undecidable"`` (higher homotopy groups are undecidable;
    the spaces could still differ in π_n for n ≥ 2).

    Parameters
    ----------
    K, L : SimplicialComplex
        Finite simplicial complexes.
    """
    hK = homology_groups(K)
    hL = homology_groups(L)
    n = max(len(hK), len(hL))

    bK = [hK[k].betti if k < len(hK) else 0 for k in range(n)]
    bL = [hL[k].betti if k < len(hL) else 0 for k in range(n)]
    tK = [hK[k].torsion if k < len(hK) else () for k in range(n)]
    tL = [hL[k].torsion if k < len(hL) else () for k in range(n)]

    eK = sum((-1) ** k * b for k, b in enumerate(bK))
    eL = sum((-1) ** k * b for k, b in enumerate(bL))

    if eK != eL:
        return HomotopyEquivalenceVerdict(
            verdict="not_equivalent",
            reason=f"Euler characteristics differ: χ(K)={eK}, χ(L)={eL}.",
            betti_K=tuple(bK), betti_L=tuple(bL), euler_K=eK, euler_L=eL,
        )

    for k in range(n):
        if bK[k] != bL[k]:
            return HomotopyEquivalenceVerdict(
                verdict="not_equivalent",
                reason=f"β_{k} differs: K has {bK[k]}, L has {bL[k]}.",
                betti_K=tuple(bK), betti_L=tuple(bL), euler_K=eK, euler_L=eL,
            )
        if tuple(sorted(tK[k])) != tuple(sorted(tL[k])):
            return HomotopyEquivalenceVerdict(
                verdict="not_equivalent",
                reason=f"Torsion of H_{k} differs: K has {tK[k]}, L has {tL[k]}.",
                betti_K=tuple(bK), betti_L=tuple(bL), euler_K=eK, euler_L=eL,
            )

    return HomotopyEquivalenceVerdict(
        verdict="undecidable",
        reason=(
            "All computed invariants (χ, Betti numbers, torsion of H_*) agree. "
            "Homotopy equivalence is undecidable in general; spaces may differ "
            "in π_n (n ≥ 2) or other invariants not computed here."
        ),
        betti_K=tuple(bK), betti_L=tuple(bL), euler_K=eK, euler_L=eL,
    )
