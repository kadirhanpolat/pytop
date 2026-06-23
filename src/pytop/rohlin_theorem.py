"""Rohlin's theorem and spin structures on 4-manifolds (Phase 15.5).

Rohlin's Theorem (1952)
-----------------------
If X is a smooth closed simply-connected oriented spin 4-manifold, then
  σ(X) ≡ 0 (mod 16)

where σ(X) is the signature of the intersection form.

Recall:
  - X is **spin** iff w₂(X) = 0 iff the intersection form Q_X is *even*
    (Q_X(x,x) ≡ 0 mod 2 for all x ∈ H₂(X; ℤ)).
  - σ(X) = number of positive - negative eigenvalues of Q_X.

The theorem is optimal: the K3 surface has σ = -16, and there is no smooth
closed spin 4-manifold with σ = ±8 (e.g., the E₈ manifold is not smoothable).

Equivalence with Casson invariant:
  For a spin rational homology sphere M³, the Rohlin invariant
    μ(M) = λ(M) mod 2 ∈ ℤ/2

Kirby–Siebenmann obstruction:
  A topological 4-manifold has a smooth structure iff the Kirby–Siebenmann
  invariant ks(X) ∈ H⁴(X; ℤ/2) vanishes.  For spin manifolds, ks(X) = σ/8 mod 2.

Donaldson–Rohlin combination:
  - Definite smooth 4-manifolds must have diagonal intersection form (Donaldson).
  - Spin manifolds have even intersection form.
  - Combining: no smooth spin 4-manifold with definite non-standard form.

Freedman's theorem (contrast):
  Every symmetric bilinear form over ℤ is realized by a *topological*
  simply-connected closed 4-manifold:
    - Even form → unique topological manifold.
    - Odd form → two topological manifolds (one spin, one not).
  The E₈ manifold exists *topologically* but not *smoothly*.

Spin structures
---------------
A spin structure on X is a lift of the frame bundle from SO(4) to Spin(4).
It exists iff w₂(X) = 0.  On a simply-connected manifold, the number of
spin structures is |H¹(X; ℤ/2)| = 1 (unique, since π₁ = 1).

References: Rohlin 1952, Milnor 1958, Kirby–Siebenmann 1977, Freedman 1982,
Donaldson 1983.
"""

from __future__ import annotations

from dataclasses import dataclass

from .intersection_forms import (
    IntersectionForm,
)

__all__ = [
    "SpinStructureResult",
    "RohlinCheck",
    "check_rohlin_theorem",
    "is_spin_manifold",
    "kirby_siebenmann_obstruction",
    "n_spin_structures",
    "check_freedman_realization",
    "rohlin_invariant_from_signature",
    "spin_cobordism_group",
    "spin_structure_result",
    "ROHLIN_EXAMPLES",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpinStructureResult:
    """Result of spin structure analysis.

    Attributes
    ----------
    is_spin : bool
        True iff w₂ = 0 (intersection form is even).
    form_type : str
        ``"even"`` or ``"odd"``.
    n_spin_structures : int
        Number of distinct spin structures (= |H¹(X; ℤ/2)|).
    w2_vanishes : bool
        Whether the second Stiefel–Whitney class vanishes.
    """

    is_spin: bool
    form_type: str
    n_spin_structures: int
    w2_vanishes: bool


@dataclass(frozen=True)
class RohlinCheck:
    """Result of Rohlin's theorem check.

    Attributes
    ----------
    manifold_description : str
    signature : int
        σ(X).
    is_spin : bool
        Whether the manifold is spin.
    rohlin_satisfied : bool
        True iff σ ≡ 0 (mod 16), or the manifold is not spin.
    obstruction : str
        Description of any violation.
    ks_obstruction : int
        Kirby–Siebenmann obstruction (σ/8 mod 2 for spin manifolds).
    freedman_realizable : bool
        Whether the form is realizable by a topological manifold (Freedman).
    smooth_possible : bool
        Whether a smooth structure is possible (Donaldson + Rohlin).
    """

    manifold_description: str
    signature: int
    is_spin: bool
    rohlin_satisfied: bool
    obstruction: str
    ks_obstruction: int
    freedman_realizable: bool
    smooth_possible: bool

    def __repr__(self) -> str:
        ok = "OK" if self.rohlin_satisfied else "VIOLATED"
        return (
            f"RohlinCheck({self.manifold_description!r}, "
            f"σ={self.signature}, spin={self.is_spin}, "
            f"Rohlin={ok})"
        )


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def is_spin_manifold(form: IntersectionForm) -> bool:
    """Determine if a 4-manifold is spin from its intersection form.

    X is spin iff w₂(X) = 0 iff Q_X is *even*
    (Q_X(x,x) ≡ 0 mod 2 for all x in the lattice).

    Parameters
    ----------
    form : IntersectionForm
    """
    return form.form_type == "even"


def kirby_siebenmann_obstruction(form: IntersectionForm) -> int:
    """Kirby–Siebenmann obstruction ks(X) ∈ ℤ/2.

    For spin manifolds: ks(X) = σ(X)/8 mod 2.
    For non-spin: ks(X) is defined but harder to compute from Q alone.

    Parameters
    ----------
    form : IntersectionForm

    Returns
    -------
    int
        0 or 1.
    """
    if form.form_type == "even":
        return (form.signature // 8) % 2
    return 0  # Non-spin: assume ks = 0 (standard)


def n_spin_structures(h1_rank: int = 0) -> int:
    """Number of spin structures on a manifold with H¹(X; ℤ/2) of given rank.

    A spin structure is a lift of the structure group from SO(n) to Spin(n).
    The set of spin structures is a torsor for H¹(X; ℤ/2).
    For simply-connected X: H¹(X; ℤ/2) = 0 → unique spin structure.

    Parameters
    ----------
    h1_rank : int
        Rank of H¹(X; ℤ/2) as an ℤ/2 vector space.
    """
    return 2 ** h1_rank


def check_rohlin_theorem(
    form: IntersectionForm,
    manifold_description: str = "X",
    h1_z2_rank: int = 0,
) -> RohlinCheck:
    """Check whether a smooth 4-manifold satisfies Rohlin's theorem.

    Parameters
    ----------
    form : IntersectionForm
        Intersection form of the (simply-connected) 4-manifold.
    manifold_description : str
        Human-readable name.
    h1_z2_rank : int
        Rank of H¹(X; ℤ/2) (0 for simply-connected).

    Returns
    -------
    RohlinCheck
    """
    sig = form.signature
    spin = is_spin_manifold(form)
    ks = kirby_siebenmann_obstruction(form)
    n_spin_structures(h1_z2_rank)

    # Rohlin: spin + smooth → σ ≡ 0 (mod 16)
    rohlin_ok: bool
    obstruction: str
    smooth_possible: bool

    if not spin:
        rohlin_ok = True  # Rohlin only constrains spin manifolds
        obstruction = "Not a spin manifold; Rohlin's theorem does not apply."
        smooth_possible = True  # May still be smoothable

        # But check Donaldson's theorem for definite non-spin forms
        def_str = form.definiteness
        if def_str in ("positive_definite", "negative_definite") and form.form_type == "odd":
            # Must be diagonal
            diagonal = all(
                form.matrix[i][j] == 0 if i != j else abs(form.matrix[i][i]) == 1
                for i in range(form.rank) for j in range(form.rank)
            )
            if not diagonal:
                smooth_possible = False
                obstruction = (
                    "Donaldson: definite non-diagonal intersection form. "
                    "No smooth 4-manifold exists with this form."
                )
    else:
        # Spin manifold: must have σ ≡ 0 (mod 16)
        if sig % 16 == 0:
            rohlin_ok = True
            obstruction = "Rohlin's theorem satisfied."
            smooth_possible = True
        else:
            rohlin_ok = False
            rem = sig % 16
            obstruction = (
                f"Rohlin VIOLATED: σ = {sig} ≡ {rem} (mod 16) ≠ 0. "
                "No smooth structure exists with this spin form."
            )
            smooth_possible = False

    # Freedman realization: every form is realizable topologically
    freedman_ok = True  # Freedman 1982: always yes for simply-connected

    return RohlinCheck(
        manifold_description=manifold_description,
        signature=sig,
        is_spin=spin,
        rohlin_satisfied=rohlin_ok,
        obstruction=obstruction,
        ks_obstruction=ks,
        freedman_realizable=freedman_ok,
        smooth_possible=smooth_possible,
    )


def check_freedman_realization(form: IntersectionForm) -> dict[str, object]:
    """Check Freedman's realization theorem.

    Every symmetric bilinear form over ℤ arises as Q_X for some closed
    simply-connected topological 4-manifold X (Freedman 1982).

    Parameters
    ----------
    form : IntersectionForm

    Returns
    -------
    dict with:
        ``"realizable_topologically"``: always True.
        ``"n_topological_realizations"``: 1 (even form) or 2 (odd form).
        ``"smoothable"``: whether a smooth structure is possible.
        ``"description"``: explanation.
    """
    ftype = form.form_type
    n_top = 1 if ftype == "even" else 2
    spin = is_spin_manifold(form)

    rohlin = check_rohlin_theorem(form)
    smoothable = rohlin.smooth_possible

    desc = (
        f"Form is {ftype}. "
        f"By Freedman: {n_top} topological realization(s). "
        f"Smooth structure: {'possible' if smoothable else 'obstructed (Rohlin/Donaldson)'}."
    )

    return {
        "realizable_topologically": True,
        "n_topological_realizations": n_top,
        "smoothable": smoothable,
        "description": desc,
        "spin": spin,
    }


def rohlin_invariant_from_signature(signature: int) -> int:
    """Rohlin invariant μ = σ/8 mod 2 for a spin manifold.

    Parameters
    ----------
    signature : int
        Signature of the spin 4-manifold (must be divisible by 8 by parity).
    """
    if signature % 8 != 0:
        raise ValueError(
            f"Signature {signature} of a spin manifold must be divisible by 8 "
            "(since the form is even and unimodular)"
        )
    return (signature // 8) % 2


def spin_cobordism_group(dimension: int) -> str:
    """Description of the spin cobordism group Ω^Spin_n.

    Parameters
    ----------
    dimension : int
        The dimension n.
    """
    groups = {
        0: "ℤ (point, generator: pt)",
        1: "ℤ/2 (generator: S¹ with bounding disk removed)",
        2: "ℤ/2 (generator: ?)",
        3: "0",
        4: "ℤ (generator: K3 surface, index = σ/16)",
        5: "0",
        6: "0",
        7: "0",
        8: "ℤ ⊕ ℤ (generators: K3², HP²)",
    }
    return groups.get(dimension, f"Ω^Spin_{dimension} (not in table)")


def spin_structure_result(form: IntersectionForm, h1_rank: int = 0) -> SpinStructureResult:
    """Compute spin structure data for a 4-manifold with given form.

    Parameters
    ----------
    form : IntersectionForm
    h1_rank : int
        Rank of H¹(X; ℤ/2).
    """
    spin = is_spin_manifold(form)
    n_sp = n_spin_structures(h1_rank) if spin else 0
    return SpinStructureResult(
        is_spin=spin,
        form_type=form.form_type,
        n_spin_structures=n_sp,
        w2_vanishes=spin,
    )


# ---------------------------------------------------------------------------
# Examples database
# ---------------------------------------------------------------------------

ROHLIN_EXAMPLES: dict[str, dict[str, object]] = {
    "S4": {
        "signature": 0,
        "form_type": "even",
        "spin": True,
        "rohlin_ok": True,
        "description": "S⁴: Q = 0, σ = 0 ≡ 0 (mod 16).",
    },
    "CP2": {
        "signature": 1,
        "form_type": "odd",
        "spin": False,
        "rohlin_ok": True,
        "description": "ℂP²: Q = ⟨1⟩, not spin, Rohlin doesn't apply.",
    },
    "minus_CP2": {
        "signature": -1,
        "form_type": "odd",
        "spin": False,
        "rohlin_ok": True,
        "description": "-ℂP²: Q = ⟨-1⟩, not spin.",
    },
    "K3": {
        "signature": -16,
        "form_type": "even",
        "spin": True,
        "rohlin_ok": True,
        "description": "K3: σ = -16 ≡ 0 (mod 16), spin, saturates Rohlin bound.",
    },
    "E8_manifold": {
        "signature": 8,
        "form_type": "even",
        "spin": True,
        "rohlin_ok": False,
        "description": "E₈ manifold: σ = 8 ≢ 0 (mod 16) → no smooth structure (Rohlin violated).",
    },
    "S2xS2": {
        "signature": 0,
        "form_type": "even",
        "spin": True,
        "rohlin_ok": True,
        "description": "S²×S²: Q = H, σ = 0, spin.",
    },
}
