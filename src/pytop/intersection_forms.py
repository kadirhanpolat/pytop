"""Intersection forms on 4-manifolds (Phase 15.1).

The intersection form of a closed oriented 4-manifold X is the symmetric
bilinear form

    Q_X : H_2(X; ℤ) × H_2(X; ℤ) → ℤ

obtained by algebraically counting intersection points of transverse surfaces.

Key invariants
--------------
Rank r: rank of H_2(X; ℤ) (ignoring torsion).
Signature σ: signature of Q_X (number of positive minus negative eigenvalues).
Type:
  - Even (Type II): Q_X(x,x) ≡ 0 (mod 2) for all x.  Equivalently Q is
    even, i.e. all diagonal entries are even.  This holds iff w_2(X) = 0
    (X is spin).
  - Odd (Type I): some Q_X(x,x) is odd.

Definiteness:
  - Positive definite: all eigenvalues > 0.
  - Negative definite: all eigenvalues < 0.
  - Indefinite: both positive and negative eigenvalues.

Classification (indefinite, over ℤ):
  Odd: Q ≅ ⟨1⟩^p ⊕ ⟨-1⟩^q  (p+q = rank, p-q = signature)
  Even: Q ≅ p·E_8 ⊕ q·H      (H = [[0,1],[1,0]] hyperbolic pair)
  This is the theorem of Serre (indefinite case) / Milnor.

Standard forms:
  E_8 lattice: the unique positive-definite even unimodular form of rank 8.
  H (hyperbolic): rank 2, signature 0, even.
  ⟨1⟩, ⟨-1⟩: rank 1, odd.

References: Milnor–Husemoller, Kirby 1989, Donaldson–Kronheimer 1990.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .homology import _smith_normal_form

__all__ = [
    "IntersectionForm",
    "intersection_form",
    "form_rank",
    "form_signature",
    "form_type",
    "is_unimodular",
    "is_definite",
    "classify_indefinite_form",
    "e8_form",
    "hyperbolic_form",
    "diagonal_form",
    "connected_sum_form",
    "donaldson_theorem",
    "STANDARD_FORMS",
]

Matrix = list[list[int]]


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IntersectionForm:
    """Symmetric bilinear form over ℤ.

    Attributes
    ----------
    matrix : tuple[tuple[int,...],...]
        The Gram matrix in some basis.
    rank : int
    signature : int
        p - q  (positive minus negative eigenvalues).
    form_type : str
        ``"even"`` or ``"odd"``.
    is_unimodular : bool
        True iff |det(Q)| = 1.
    definiteness : str
        ``"positive_definite"``, ``"negative_definite"``, or ``"indefinite"``.
    classification : str
        Isomorphism class name (indefinite case only).
    """

    matrix: tuple[tuple[int, ...], ...]
    rank: int
    signature: int
    form_type: str
    is_unimodular: bool
    definiteness: str
    classification: str

    @property
    def b2_plus(self) -> int:
        return (self.rank + self.signature) // 2

    @property
    def b2_minus(self) -> int:
        return (self.rank - self.signature) // 2

    def euler_contribution(self) -> int:
        return self.rank

    def __repr__(self) -> str:
        return (
            f"IntersectionForm(rank={self.rank}, σ={self.signature}, "
            f"type={self.form_type}, unimod={self.is_unimodular}, "
            f"def={self.definiteness})"
        )


# ---------------------------------------------------------------------------
# Linear algebra helpers
# ---------------------------------------------------------------------------


def _det(mat: Matrix) -> int:
    """Determinant of an integer matrix (via SNF invariant factors)."""
    if not mat:
        return 1
    # _smith_normal_form returns list[int] of nonzero invariant factors
    factors = _smith_normal_form(mat)
    if len(factors) < len(mat):
        return 0  # rank-deficient
    d = 1
    for f in factors:
        d *= f
    return d


def _eigenvalue_signs(mat: Matrix) -> tuple[int, int]:
    """Count positive and negative eigenvalues via Sylvester's law of inertia.

    Uses the SNF of the matrix to count sign-changes (Jacobi's criterion
    on leading principal minors).  Returns (n_pos, n_neg).
    """
    n = len(mat)
    if n == 0:
        return (0, 0)

    # Use the Gram–Schmidt approach: count sign changes of leading minors
    # For diagonal detection
    # We compute the sequence of leading minors
    def leading_minor(k: int) -> int:
        sub = [row[:k] for row in mat[:k]]
        return _det(sub)

    signs = []
    for k in range(1, n + 1):
        m = leading_minor(k)
        if m != 0:
            signs.append(1 if m > 0 else -1)

    # Sylvester: count sign changes → negative count
    if not signs:
        return (0, 0)

    # Delegate to the rational diagonalization
    return _sylvester_signature(mat)


def _sylvester_signature(mat: Matrix) -> tuple[int, int]:
    """Compute (n_positive, n_negative) eigenvalues via Sylvester's law of inertia.

    Diagonalises the symmetric form by *congruence* (simultaneous row/column
    operations), which preserves the signature.  Crucially, when a diagonal
    pivot is zero we first apply a symmetric congruence
    (add row/col j to row/col k) to create a non-zero diagonal entry — without
    this the off-diagonal hyperbolic block H = [[0,1],[1,0]] would be misread
    as positive definite instead of signature 0.
    """
    n = len(mat)
    # Work with Fractions for exact arithmetic.
    A = [[Fraction(mat[i][j]) for j in range(n)] for i in range(n)]

    n_pos = 0
    n_neg = 0
    for k in range(n):
        if A[k][k] == 0:
            # Find an off-diagonal partner to make the diagonal non-zero.
            j = next((c for c in range(k + 1, n) if A[k][c] != 0), None)
            if j is None:
                # Whole k-th row (from k on) is zero → degenerate direction.
                continue
            # Symmetric congruence: row_k += row_j and col_k += col_j.
            for c in range(n):
                A[k][c] += A[j][c]
            for r in range(n):
                A[r][k] += A[r][j]
        pivot = A[k][k]
        if pivot > 0:
            n_pos += 1
        else:
            n_neg += 1
        # Symmetric Gaussian elimination of the rest against the pivot.
        for r in range(k + 1, n):
            if A[r][k] != 0:
                factor = A[r][k] / pivot
                for c in range(n):
                    A[r][c] -= factor * A[k][c]
                for rr in range(n):
                    A[rr][r] -= factor * A[rr][k]

    return (n_pos, n_neg)


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def form_rank(matrix: Matrix) -> int:
    """Rank of the intersection form (ignoring torsion)."""
    if not matrix:
        return 0
    return len(_smith_normal_form(matrix))


def form_signature(matrix: Matrix) -> int:
    """Signature of the intersection form: n_pos - n_neg."""
    n_pos, n_neg = _sylvester_signature(matrix)
    return n_pos - n_neg


def form_type(matrix: Matrix) -> str:
    """Determine if the form is ``"even"`` or ``"odd"``."""
    for i in range(len(matrix)):
        if matrix[i][i] % 2 != 0:
            return "odd"
    return "even"


def is_unimodular(matrix: Matrix) -> bool:
    """Return True iff |det(Q)| = 1."""
    d = _det(matrix)
    return abs(d) == 1


def is_definite(matrix: Matrix) -> str:
    """Return ``"positive_definite"``, ``"negative_definite"``, or ``"indefinite"``."""
    n_pos, n_neg = _sylvester_signature(matrix)
    n = len(matrix)
    if n_pos == n:
        return "positive_definite"
    if n_neg == n:
        return "negative_definite"
    return "indefinite"


def classify_indefinite_form(matrix: Matrix) -> str:
    """Classify an indefinite unimodular form (Serre's theorem).

    Returns a string like ``"p<1> + q<-1>"`` (odd type) or
    ``"aE8 + bH"`` (even type).

    Parameters
    ----------
    matrix : Matrix
        Integer Gram matrix of a unimodular indefinite form.
    """
    n = len(matrix)
    if n == 0:
        return "trivial"
    sig = form_signature(matrix)
    ftype = form_type(matrix)
    n_pos = (n + sig) // 2
    n_neg = (n - sig) // 2
    def_str = is_definite(matrix)

    if def_str == "positive_definite":
        return f"positive_definite_rank_{n}"
    if def_str == "negative_definite":
        return f"negative_definite_rank_{n}"

    if ftype == "odd":
        return f"{n_pos}<1> + {n_neg}<-1>"
    else:
        # Even indefinite unimodular: p·E8 + q·H
        # signature = 8p (if p copies of E8 with sign ε) and q hyperbolic pairs
        # Simplified: rank = 8|p_e8| + 2q, σ = 8 * p_e8
        q = n_neg  # number of H pairs (each contributes rank 2, sigma 0)
        p_e8 = sig // 8
        return f"{abs(p_e8)}E8({'+' if p_e8 >= 0 else '-'}) + {q}H"


def intersection_form(matrix: Matrix) -> IntersectionForm:
    """Compute all invariants of an intersection form.

    Parameters
    ----------
    matrix : Matrix
        Integer symmetric Gram matrix Q.

    Returns
    -------
    IntersectionForm
    """
    len(matrix)
    r = form_rank(matrix)
    sig = form_signature(matrix)
    ftype = form_type(matrix)
    unimod = is_unimodular(matrix)
    def_str = is_definite(matrix)
    classif = classify_indefinite_form(matrix)

    return IntersectionForm(
        matrix=tuple(tuple(row) for row in matrix),
        rank=r,
        signature=sig,
        form_type=ftype,
        is_unimodular=unimod,
        definiteness=def_str,
        classification=classif,
    )


# ---------------------------------------------------------------------------
# Standard forms
# ---------------------------------------------------------------------------


def e8_form() -> IntersectionForm:
    """The E_8 lattice intersection form (rank 8, even, positive definite, unimodular)."""
    Q = [
        [2, -1, 0, 0, 0, 0, 0, 0],
        [-1, 2, -1, 0, 0, 0, 0, 0],
        [0, -1, 2, -1, 0, 0, 0, -1],
        [0, 0, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, -1, 0, 0, 0, 0, 2],
    ]
    return intersection_form(Q)


def hyperbolic_form() -> IntersectionForm:
    """The hyperbolic form H = [[0,1],[1,0]] (rank 2, even, indefinite, unimodular)."""
    return intersection_form([[0, 1], [1, 0]])


def diagonal_form(entries: list[int]) -> IntersectionForm:
    """Diagonal intersection form with given entries.

    Parameters
    ----------
    entries : list[int]
        Diagonal entries (typically ±1).
    """
    n = len(entries)
    Q = [[entries[i] if i == j else 0 for j in range(n)] for i in range(n)]
    return intersection_form(Q)


def connected_sum_form(Q1: IntersectionForm, Q2: IntersectionForm) -> IntersectionForm:
    """Intersection form of the connected sum X1 # X2.

    Q_{X1#X2} = Q_{X1} ⊕ Q_{X2} (block diagonal sum).

    Parameters
    ----------
    Q1, Q2 : IntersectionForm
    """
    n1 = Q1.rank
    n2 = Q2.rank
    n = n1 + n2
    M: Matrix = [[0] * n for _ in range(n)]
    for i in range(n1):
        for j in range(n1):
            M[i][j] = Q1.matrix[i][j]
    for i in range(n2):
        for j in range(n2):
            M[n1 + i][n1 + j] = Q2.matrix[i][j]
    return intersection_form(M)


def donaldson_theorem(form: IntersectionForm) -> dict[str, object]:
    """Apply Donaldson's theorem to the given form.

    Donaldson's theorem (1983): If X is a smooth simply-connected closed
    4-manifold with a *positive-definite* intersection form, then Q_X is
    diagonalizable over ℤ (i.e., isomorphic to n·⟨1⟩).

    Parameters
    ----------
    form : IntersectionForm

    Returns
    -------
    dict with keys:
        ``"is_standard"``: bool — True iff form satisfies Donaldson constraint.
        ``"verdict"``: str — explanation.
        ``"exotic_obstruction"``: bool — True iff form is definite but non-diagonal,
            implying no smooth structure (exotic obstruction).
    """
    if form.definiteness == "indefinite":
        return {
            "is_standard": True,
            "verdict": "Indefinite forms are not constrained by Donaldson's theorem.",
            "exotic_obstruction": False,
        }
    if form.form_type == "odd" and form.definiteness in ("positive_definite", "negative_definite"):
        # Diagonal form: already standard
        diagonal_check = all(
            form.matrix[i][j] == 0 if i != j else abs(form.matrix[i][i]) == 1
            for i in range(form.rank) for j in range(form.rank)
        )
        if diagonal_check:
            return {
                "is_standard": True,
                "verdict": "Form is diagonal ⟨±1⟩^n — satisfies Donaldson's theorem.",
                "exotic_obstruction": False,
            }
        else:
            return {
                "is_standard": False,
                "verdict": (
                    "Definite odd non-diagonal form violates Donaldson's theorem: "
                    "no smooth 4-manifold can have this form."
                ),
                "exotic_obstruction": True,
            }
    # Even definite: E8, Γ_8, etc. are forbidden by Donaldson
    if form.form_type == "even" and form.definiteness in ("positive_definite", "negative_definite"):
        return {
            "is_standard": False,
            "verdict": (
                f"Even definite form (rank={form.rank}, σ={form.signature}) violates "
                "Donaldson's theorem: no smooth 4-manifold has this intersection form."
            ),
            "exotic_obstruction": True,
        }
    return {
        "is_standard": True,
        "verdict": "No obstruction from Donaldson's theorem.",
        "exotic_obstruction": False,
    }


# ---------------------------------------------------------------------------
# Standard forms database
# ---------------------------------------------------------------------------

STANDARD_FORMS: dict[str, dict[str, object]] = {
    "CP2": {
        "matrix": [[1]],
        "rank": 1,
        "signature": 1,
        "type": "odd",
        "description": "ℂP²: Q = ⟨1⟩",
    },
    "minus_CP2": {
        "matrix": [[-1]],
        "rank": 1,
        "signature": -1,
        "type": "odd",
        "description": "-ℂP²: Q = ⟨-1⟩",
    },
    "S2xS2": {
        "matrix": [[0, 1], [1, 0]],
        "rank": 2,
        "signature": 0,
        "type": "even",
        "description": "S²×S²: Q = H (hyperbolic)",
    },
    "K3": {
        "matrix": None,
        "rank": 22,
        "signature": -16,
        "type": "even",
        "description": "K3 surface: Q = 3H ⊕ (-2)E_8",
    },
    "E8_manifold": {
        "matrix": None,
        "rank": 8,
        "signature": 8,
        "type": "even",
        "description": "Hypothetical manifold with Q = E_8 (no smooth version by Donaldson)",
    },
}
