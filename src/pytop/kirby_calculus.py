"""Kirby calculus and handle decompositions of 4-manifolds (Phase 15.2).

A 4-manifold can be described by a *Kirby diagram*: a framed link in S³
where each component specifies a 2-handle attachment.  The linking matrix
of the framed link is the intersection form of the 4-manifold.

Kirby moves
-----------
Two Kirby diagrams give diffeomorphic 4-manifolds iff they are related by:
  K1 (stabilization): add/remove an isolated ±1-framed unknot
      (adds/removes a ±ℂP² summand)
  K2 (handle slide): slide one 2-handle over another
      (modifies the linking matrix by row/column operations)

Handle decomposition
--------------------
A 4-manifold X has handles of indices 0, 1, 2, 3, 4.
  0-handle: a 4-disk D⁴ (one per connected component)
  1-handle: attaches as S⁰ × D³ → boundary
  2-handle: framed knot in ∂(previous handles) = S³
  3-handle: attaches as D² × S¹
  4-handle: fills in the remaining S³ boundary

For a simply-connected manifold: no 1- or 3-handles needed.
The Kirby diagram specifies only the 2-handles.

Linking matrix
--------------
For a Kirby diagram with components K_1, …, K_n:
  L_{ii} = framing of K_i
  L_{ij} = lk(K_i, K_j) for i ≠ j

This equals the intersection form Q_X on H_2(X; ℤ) = ℤ^n.

References: Kirby 1978, Kirby 1989, Gompf–Stipsicz 1999.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .intersection_forms import (
    IntersectionForm,
    form_signature,
    intersection_form,
)

__all__ = [
    "KirbyDiagram",
    "KirbyComponent",
    "KirbyMove",
    "kirby_diagram",
    "linking_matrix",
    "kirby_stabilize",
    "kirby_handle_slide",
    "kirby_to_intersection_form",
    "euler_characteristic_kirby",
    "signature_kirby",
    "b2_kirby",
    "is_kirby_equivalent",
    "kirby_diagram_cp2",
    "kirby_diagram_s2xs2",
    "kirby_diagram_k3_fiber",
    "dehn_surgery_matrix",
]

Matrix = list[list[int]]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KirbyComponent:
    """A framed knot component in a Kirby diagram.

    Attributes
    ----------
    name : str
        Label for the component.
    framing : int
        Framing coefficient (self-linking number).
    knot_type : str
        Type of the attaching knot (``"unknot"``, ``"trefoil"``, etc.)
    linking_numbers : tuple[int, ...]
        Linking numbers with each other component (indexed by position).
    """

    name: str
    framing: int
    knot_type: str = "unknot"
    linking_numbers: tuple[int, ...] = ()


@dataclass(frozen=True)
class KirbyDiagram:
    """A Kirby diagram: framed link in S³ specifying a 4-manifold.

    Attributes
    ----------
    components : tuple[KirbyComponent, ...]
        Framed link components.
    linking_matrix_data : tuple[tuple[int,...],...]
        The linking/framing matrix.
    n_zero_handles : int
        Number of 0-handles (default: 1).
    n_one_handles : int
        Number of 1-handles.
    n_three_handles : int
        Number of 3-handles.
    has_four_handle : bool
        Whether a 4-handle is present.
    name : str
        Name of the 4-manifold.
    """

    components: tuple[KirbyComponent, ...]
    linking_matrix_data: tuple[tuple[int, ...], ...]
    n_zero_handles: int = 1
    n_one_handles: int = 0
    n_three_handles: int = 0
    has_four_handle: bool = True
    name: str = ""

    @property
    def n_two_handles(self) -> int:
        return len(self.components)

    def matrix(self) -> Matrix:
        return [list(row) for row in self.linking_matrix_data]


@dataclass(frozen=True)
class KirbyMove:
    """Record of a Kirby move applied to a diagram.

    Attributes
    ----------
    move_type : str
        ``"stabilize_plus"``, ``"stabilize_minus"``, ``"handle_slide"``.
    details : str
        Human-readable description.
    """

    move_type: str
    details: str


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def linking_matrix(components: list[KirbyComponent]) -> Matrix:
    """Build the linking/framing matrix from a list of components.

    The matrix L has:
      L[i][i] = framing of component i
      L[i][j] = linking_numbers[j] of component i (for i < j, and symmetric)
    """
    n = len(components)
    mat: Matrix = [[0] * n for _ in range(n)]
    for i, comp in enumerate(components):
        mat[i][i] = comp.framing
        for j, lk in enumerate(comp.linking_numbers):
            if j < n and i != j:
                mat[i][j] = lk
                mat[j][i] = lk
    return mat


def kirby_diagram(
    framings: list[int],
    lk_matrix: Optional[Matrix] = None,
    knot_types: Optional[list[str]] = None,
    name: str = "",
    one_handles: int = 0,
    three_handles: int = 0,
    four_handle: bool = True,
) -> KirbyDiagram:
    """Build a Kirby diagram from framings and an optional linking matrix.

    Parameters
    ----------
    framings : list[int]
        Framing coefficients for each 2-handle.
    lk_matrix : Matrix or None
        Off-diagonal linking numbers.  If None, all off-diagonal = 0.
    knot_types : list[str] or None
        Knot types for each component.
    name : str
        Name of the manifold.
    """
    n = len(framings)
    if lk_matrix is None:
        lk_matrix = [[framings[i] if i == j else 0 for j in range(n)] for i in range(n)]
    if knot_types is None:
        knot_types = ["unknot"] * n

    components = []
    for i in range(n):
        lks = tuple(lk_matrix[i][j] for j in range(n) if j != i)
        components.append(KirbyComponent(
            name=f"K{i+1}",
            framing=framings[i],
            knot_type=knot_types[i],
            linking_numbers=lks,
        ))

    mat = lk_matrix

    return KirbyDiagram(
        components=tuple(components),
        linking_matrix_data=tuple(tuple(row) for row in mat),
        n_zero_handles=1,
        n_one_handles=one_handles,
        n_three_handles=three_handles,
        has_four_handle=four_handle,
        name=name,
    )


# ---------------------------------------------------------------------------
# Kirby moves
# ---------------------------------------------------------------------------


def kirby_stabilize(diagram: KirbyDiagram, sign: int = 1) -> tuple[KirbyDiagram, KirbyMove]:
    """Apply a K1 stabilization move: add an isolated ±1-framed unknot.

    This corresponds to the connected sum X # ±ℂP².

    Parameters
    ----------
    diagram : KirbyDiagram
    sign : int
        +1 or -1 (adds +ℂP² or -ℂP² summand).

    Returns
    -------
    (new_diagram, move_record)
    """
    old_mat = diagram.matrix()
    n = len(old_mat)
    new_n = n + 1
    new_mat = [[0] * new_n for _ in range(new_n)]
    for i in range(n):
        for j in range(n):
            new_mat[i][j] = old_mat[i][j]
    new_mat[n][n] = sign

    new_comp = KirbyComponent(
        name=f"K{new_n}",
        framing=sign,
        knot_type="unknot",
        linking_numbers=tuple([0] * n),
    )
    old_comps = list(diagram.components)
    # Update old components to have an extra 0 linking number
    updated_comps = []
    for comp in old_comps:
        updated_comps.append(KirbyComponent(
            name=comp.name,
            framing=comp.framing,
            knot_type=comp.knot_type,
            linking_numbers=comp.linking_numbers + (0,),
        ))
    updated_comps.append(new_comp)

    move = KirbyMove(
        move_type=f"stabilize_{'plus' if sign > 0 else 'minus'}",
        details=f"Added isolated {'+' if sign > 0 else '-'}1-framed unknot (#{new_n}).",
    )
    new_diagram = KirbyDiagram(
        components=tuple(updated_comps),
        linking_matrix_data=tuple(tuple(row) for row in new_mat),
        n_zero_handles=diagram.n_zero_handles,
        n_one_handles=diagram.n_one_handles,
        n_three_handles=diagram.n_three_handles,
        has_four_handle=diagram.has_four_handle,
        name=diagram.name + f"#{'+' if sign > 0 else '-'}CP2",
    )
    return new_diagram, move


def kirby_handle_slide(
    diagram: KirbyDiagram,
    slide_idx: int,
    over_idx: int,
) -> tuple[KirbyDiagram, KirbyMove]:
    """Apply a K2 handle slide: slide component `slide_idx` over `over_idx`.

    The effect on the linking matrix:
      L[slide_idx][j] += L[over_idx][j]  for all j
      L[j][slide_idx] += L[j][over_idx]  for all j
      L[slide_idx][slide_idx] += L[over_idx][over_idx] + 2*L[slide_idx][over_idx]

    Parameters
    ----------
    diagram : KirbyDiagram
    slide_idx : int
        Index of the handle being slid.
    over_idx : int
        Index of the handle being slid over.

    Returns
    -------
    (new_diagram, move_record)
    """
    mat = diagram.matrix()
    n = len(mat)
    new_mat = [row[:] for row in mat]

    lk = mat[slide_idx][over_idx]
    new_mat[slide_idx][slide_idx] += mat[over_idx][over_idx] + 2 * lk
    for j in range(n):
        if j != slide_idx:
            new_mat[slide_idx][j] += mat[over_idx][j]
            new_mat[j][slide_idx] = new_mat[slide_idx][j]

    move = KirbyMove(
        move_type="handle_slide",
        details=f"Slid component K{slide_idx+1} over K{over_idx+1}.",
    )
    new_diagram = KirbyDiagram(
        components=diagram.components,
        linking_matrix_data=tuple(tuple(row) for row in new_mat),
        n_zero_handles=diagram.n_zero_handles,
        n_one_handles=diagram.n_one_handles,
        n_three_handles=diagram.n_three_handles,
        has_four_handle=diagram.has_four_handle,
        name=diagram.name,
    )
    return new_diagram, move


# ---------------------------------------------------------------------------
# Invariants from Kirby diagrams
# ---------------------------------------------------------------------------


def kirby_to_intersection_form(diagram: KirbyDiagram) -> IntersectionForm:
    """Compute the intersection form from a Kirby diagram's linking matrix."""
    mat = diagram.matrix()
    return intersection_form(mat)


def euler_characteristic_kirby(diagram: KirbyDiagram) -> int:
    """Euler characteristic: χ = 2 + b_2 (for closed simply-connected 4-manifold)."""
    n2 = diagram.n_two_handles
    n1 = diagram.n_one_handles
    n3 = diagram.n_three_handles
    # χ = Σ (-1)^k * n_k where n_k = # k-handles
    # For simply-connected: n1=n3=0 → χ = 2 + n2
    return 2 + n2 - 2 * n1 - 2 * n3


def signature_kirby(diagram: KirbyDiagram) -> int:
    """Compute the signature σ(X) from the linking matrix."""
    return form_signature(diagram.matrix())


def b2_kirby(diagram: KirbyDiagram) -> int:
    """Second Betti number b_2 = number of 2-handles."""
    return diagram.n_two_handles


def is_kirby_equivalent(
    d1: KirbyDiagram,
    d2: KirbyDiagram,
) -> bool:
    """Test Kirby equivalence via signature and rank invariants.

    Two diagrams are Kirby equivalent only if they have the same signature
    and rank (necessary conditions).  Full Kirby equivalence is undecidable
    in general; this tests the computable invariants.

    Returns True iff σ(d1) = σ(d2) and rank(d1) = rank(d2).
    """
    return signature_kirby(d1) == signature_kirby(d2) and b2_kirby(d1) == b2_kirby(d2)


# ---------------------------------------------------------------------------
# Standard Kirby diagrams
# ---------------------------------------------------------------------------


def kirby_diagram_cp2() -> KirbyDiagram:
    """Kirby diagram for ℂP²: single +1-framed unknot."""
    return kirby_diagram(framings=[1], name="CP2")


def kirby_diagram_s2xs2() -> KirbyDiagram:
    """Kirby diagram for S²×S²: two 0-framed unknots with linking number 1."""
    mat = [[0, 1], [1, 0]]
    return kirby_diagram(framings=[0, 0], lk_matrix=mat, name="S2xS2")


def kirby_diagram_k3_fiber() -> KirbyDiagram:
    """Kirby diagram for the K3 surface (fiber-sum description).

    K3 is the fiber sum of two E(1) = ℂP² # 9(-ℂP²).
    Intersection form: Q_{K3} = 3H ⊕ (-2)E_8 (rank 22, σ = -16).

    This returns the plumbing description via the E_8 + 3H plumbing diagram.
    """
    # Simplified: 22 handles in the plumbing form
    # E_8 plumbing: 8 × (-2)-framed unknots in the E_8 pattern
    # Plus 3 hyperbolic pairs
    # We use the linking matrix of the full K3
    n = 22
    mat: Matrix = [[0] * n for _ in range(n)]
    # First 8: E_8 with sign -1 (negative definite copy)
    e8_graph = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7)]  # E_8 Dynkin
    for i in range(8):
        mat[i][i] = -2
    for a, b in e8_graph:
        mat[a][b] = -1
        mat[b][a] = -1
    # Second E_8 copy (indices 8..15)
    for i in range(8):
        mat[8+i][8+i] = -2
    for a, b in e8_graph:
        mat[8+a][8+b] = -1
        mat[8+b][8+a] = -1
    # Three H pairs (indices 16..21)
    for k in range(3):
        i = 16 + 2*k
        mat[i][i+1] = 1
        mat[i+1][i] = 1

    return KirbyDiagram(
        components=tuple(
            KirbyComponent(name=f"K{i+1}", framing=mat[i][i], knot_type="unknot",
                           linking_numbers=tuple(mat[i][j] for j in range(n) if j != i))
            for i in range(n)
        ),
        linking_matrix_data=tuple(tuple(row) for row in mat),
        n_zero_handles=1,
        name="K3",
    )


def dehn_surgery_matrix(
    surgery_coefficients: list[tuple[int, int]],
    linking_matrix_off: Optional[Matrix] = None,
) -> Matrix:
    """Build the linking matrix from Dehn surgery coefficients p/q.

    For a rational surgery on a framed link, the surgery coefficient p/q
    gives a framing p for the corresponding handle (in the integer surgery
    presentation after blowing down).

    Parameters
    ----------
    surgery_coefficients : list[(p, q)]
        Pairs (p, q) for each surgery component.
    linking_matrix_off : Matrix or None
        Off-diagonal linking numbers.

    Returns
    -------
    Matrix
        The linking/framing matrix (framings are p values, off-diagonal from linking).
    """
    n = len(surgery_coefficients)
    framings = [p for p, q in surgery_coefficients]
    if linking_matrix_off is None:
        mat = [[framings[i] if i == j else 0 for j in range(n)] for i in range(n)]
    else:
        mat = [row[:] for row in linking_matrix_off]
        for i in range(n):
            mat[i][i] = framings[i]
    return mat
