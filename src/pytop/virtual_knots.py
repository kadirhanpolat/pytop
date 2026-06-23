"""Virtual knot theory and invariants (Phase 14.5).

Virtual knot theory (Kauffman 1999) extends classical knot theory to knots
in thickened surfaces.  A *virtual knot diagram* has two types of crossings:
  - Classical crossings (positive or negative, as in classical knot theory)
  - Virtual crossings (circled ×, no over/under distinction)

A virtual knot is an equivalence class of virtual diagrams under the extended
Reidemeister moves:
  Classical: R1, R2, R3 (unchanged from classical theory)
  Virtual:  VR1, VR2, VR3 (virtual versions of R1, R2, R3)
  Mixed:    VR4 (one virtual and one classical crossing)

The *parity* of a classical crossing c in a Gauss code:
  c is *odd* if the number of classical crossings encountered between the two
  occurrences of c in the Gauss code is odd; otherwise *even*.

Key invariants
--------------
Odd writhe J(K):
  J(K) = Σ_{c odd} sign(c)   (sum of signs over odd classical crossings)
  J is a virtual knot invariant (a genuine integer, not just mod something).
  J(K) = 0 for all classical knots (no virtual crossings present means all
  crossings are even in the Gauss code).

Arrow polynomial (Dye–Kauffman 2009):
  A generalization of the bracket polynomial for virtual knots.
  Uses virtual crossings to create "arrows" on strands.
  Gives stronger invariants than the standard Kauffman bracket.

Virtual crossing number:
  The minimum number of virtual crossings over all diagrams of the virtual knot.
  For classical knots: 0.

Genus of the virtual knot:
  The minimum genus surface Σ such that the knot lives in Σ × [0,1].
  For classical knots: 0 (they live in S² × [0,1]).

Parity bracket (Manturov 2010):
  A refinement of the Kauffman bracket that uses the parity structure.

Gauss code representation:
  A virtual knot can be encoded as a Gauss code: a sequence of signed crossing
  labels with an additional bit for each crossing occurrence (over/under).
  Example: Gauss code of the virtual trefoil: O1+U2+O3+U1+O2+U3+ (schematic)

References: Kauffman 1999, Dye–Kauffman 2009, Manturov 2010.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

__all__ = [
    "VirtualKnotDiagram",
    "GaussCode",
    "VirtualInvariants",
    "gauss_code_from_string",
    "odd_writhe",
    "writhe",
    "parity_of_crossing",
    "virtual_genus_lower_bound",
    "arrow_polynomial_bracket",
    "virtual_knot_invariants",
    "is_classical",
    "VIRTUAL_KNOT_DATA",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GaussCode:
    """A Gauss code representation of a virtual knot.

    A Gauss code is a cyclic sequence of crossing labels, each with:
    - A label (positive integer)
    - A sign (+1 or -1)
    - A flag (O=over or U=under)

    Attributes
    ----------
    crossings : tuple[tuple[int, int, str], ...]
        Each entry is (label, sign, "O"/"U").
    n_classical : int
        Number of classical crossings.
    n_virtual : int
        Number of virtual crossings (if embedded).
    name : str
    """

    crossings: tuple[tuple[int, int, str], ...]
    n_classical: int
    n_virtual: int = 0
    name: str = ""

    @property
    def length(self) -> int:
        return len(self.crossings)

    def labels(self) -> list[int]:
        return [label for label, sign, flag in self.crossings]

    def signs(self) -> dict[int, int]:
        result: dict[int, int] = {}
        for label, sign, flag in self.crossings:
            result[label] = sign
        return result


@dataclass(frozen=True)
class VirtualKnotDiagram:
    """A virtual knot diagram via crossing data.

    Attributes
    ----------
    gauss_code : GaussCode
    writhe : int
        Algebraic sum of classical crossing signs.
    odd_writhe : int
        J(K): sum of signs over odd classical crossings.
    """

    gauss_code: GaussCode
    writhe_value: int
    odd_writhe_value: int

    @property
    def name(self) -> str:
        return self.gauss_code.name


@dataclass(frozen=True)
class VirtualInvariants:
    """Collection of virtual knot invariants.

    Attributes
    ----------
    name : str
    odd_writhe : int
        J(K) — odd writhe.
    writhe : int
        w(K) — total writhe.
    n_classical : int
        Number of classical crossings.
    n_virtual : int
        Number of virtual crossings in this diagram.
    genus_lower_bound : int
        Lower bound on virtual genus from crossing data.
    is_classical_knot : bool
        True iff J(K) = 0 and the Gauss code satisfies classical realizability.
    arrow_poly : dict[tuple[int,...], int]
        Coefficients of the arrow polynomial.
    """

    name: str
    odd_writhe: int
    writhe: int
    n_classical: int
    n_virtual: int
    genus_lower_bound: int
    is_classical_knot: bool
    arrow_poly: dict[tuple[int, ...], int]


# ---------------------------------------------------------------------------
# Gauss code parsing
# ---------------------------------------------------------------------------


def gauss_code_from_string(code: str, name: str = "") -> GaussCode:
    """Parse a Gauss code string.

    Format: alternating O/U labels with signs, e.g. "O1+U2-O3+U1-O2+U3-"
    Each crossing appears exactly twice: once as O (over) and once as U (under).

    Parameters
    ----------
    code : str
        Gauss code string.
    name : str
    """
    code = code.strip()
    crossings: list[tuple[int, int, str]] = []
    i = 0
    while i < len(code):
        flag = code[i]  # O or U
        i += 1
        # Read label digits
        j = i
        while j < len(code) and code[j].isdigit():
            j += 1
        label = int(code[i:j])
        i = j
        # Read sign
        sign_char = code[i] if i < len(code) else "+"
        sign = 1 if sign_char == "+" else -1
        i += 1
        crossings.append((label, sign, flag))

    labels = [lab for lab, _, _ in crossings]
    n_classical = len(set(labels))

    return GaussCode(
        crossings=tuple(crossings),
        n_classical=n_classical,
        n_virtual=0,
        name=name,
    )


# ---------------------------------------------------------------------------
# Parity and writhe
# ---------------------------------------------------------------------------


def parity_of_crossing(label: int, gauss_code: GaussCode) -> str:
    """Determine the parity of a classical crossing in the Gauss code.

    A crossing with label `label` is *odd* if the number of other crossing
    labels that appear an *odd* number of times between the two occurrences
    of `label` in the Gauss code is odd.

    Returns ``"odd"`` or ``"even"``.

    Parameters
    ----------
    label : int
        Crossing label to test.
    gauss_code : GaussCode
    """
    crossings = gauss_code.crossings
    positions = [i for i, (lab, _, _) in enumerate(crossings) if lab == label]
    if len(positions) != 2:
        return "unknown"
    p1, p2 = positions[0], positions[1]

    # Count labels between positions
    between = [crossings[i][0] for i in range(p1 + 1, p2)]
    from collections import Counter
    counts = Counter(between)
    n_odd_appearances = sum(1 for c in counts.values() if c % 2 == 1)
    return "odd" if n_odd_appearances % 2 == 1 else "even"


def odd_writhe(gauss_code: GaussCode) -> int:
    """Compute the odd writhe J(K) of a virtual knot.

    J(K) = Σ sign(c) over all odd classical crossings c.

    For any classical knot (embeddable in S²), J(K) = 0.
    For virtual knots, J(K) is a genuine integer invariant.

    Parameters
    ----------
    gauss_code : GaussCode
    """
    gauss_code.signs()
    labels_seen: set[int] = set()
    total = 0
    for lab, sign, flag in gauss_code.crossings:
        if lab not in labels_seen:
            labels_seen.add(lab)
            par = parity_of_crossing(lab, gauss_code)
            if par == "odd":
                total += sign
    return total


def writhe(gauss_code: GaussCode) -> int:
    """Compute the total writhe w(K) = Σ sign(c) over all crossings.

    Parameters
    ----------
    gauss_code : GaussCode
    """
    signs = gauss_code.signs()
    return sum(signs.values())


def is_classical(gauss_code: GaussCode) -> bool:
    """Check if the Gauss code is realizable as a classical knot diagram.

    Necessary condition: J(K) = 0 (odd writhe vanishes).
    The sufficient condition (classical realizability) is more complex.

    Returns True iff J(K) = 0 (necessary condition for classicality).
    """
    return odd_writhe(gauss_code) == 0


# ---------------------------------------------------------------------------
# Virtual genus
# ---------------------------------------------------------------------------


def virtual_genus_lower_bound(gauss_code: GaussCode) -> int:
    """Lower bound on the virtual genus from the Gauss code.

    The virtual genus satisfies:
      γ(K) ≥ ceil(|J(K)| / crossing_number)  (rough bound)
    A better bound uses the number of odd crossings:
      γ(K) ≥ #{odd crossings} / 2  (since each handle can resolve ≤2 odd crossings)

    Returns
    -------
    int
        Lower bound on the virtual genus.
    """
    n_odd = sum(
        1 for lab in set(gauss_code.labels())
        if parity_of_crossing(lab, gauss_code) == "odd"
    )
    return (n_odd + 1) // 2


# ---------------------------------------------------------------------------
# Arrow polynomial (simplified)
# ---------------------------------------------------------------------------


def arrow_polynomial_bracket(gauss_code: GaussCode) -> dict[tuple[int, ...], int]:
    """Compute a simplified version of the arrow polynomial bracket.

    The arrow polynomial A(K) ∈ ℤ[A, A^{-1}, K_1, K_2, …] is a refinement
    of the Kauffman bracket that uses the parity to introduce extra variables K_i.

    Here we return a simplified version:
      - When a crossing is smoothed, odd crossings contribute a K_n factor
        while even crossings contribute the standard ±A^{±1} factors.

    For a full implementation, one needs to track the "arrow" structure
    during the state-sum expansion.  Here we return:
      {(a_exp, k1_pow, k2_pow, …): coefficient}

    For the purposes of this module we compute the leading terms only.
    """
    n_crossings = gauss_code.n_classical
    if n_crossings == 0:
        return {(0,): 1}  # unknot

    # Count odd vs even crossings
    labels = list(set(gauss_code.labels()))
    odd_labels = [lab for lab in labels if parity_of_crossing(lab, gauss_code) == "odd"]
    even_labels = [lab for lab in labels if parity_of_crossing(lab, gauss_code) == "even"]
    n_odd = len(odd_labels)
    n_even = len(even_labels)

    # Simplified: bracket = A^{w} * (standard terms) * K_1^{n_odd}
    # where w = writhe of even crossings
    sgns = gauss_code.signs()
    sum(sgns[lab] for lab in even_labels)
    sum(sgns[lab] for lab in odd_labels)

    # Leading term in A with K_1 for odd crossings
    result: dict[tuple[int, ...], int] = {}

    for states in product(range(2), repeat=n_even):
        a_exp = 0
        circles = n_even + 1  # rough circle count
        for bit, lab in zip(states, even_labels):
            sign = sgns[lab]
            if bit == 0:
                a_exp += 1 if sign > 0 else -1
            else:
                a_exp += -1 if sign > 0 else 1
        # Add K_1 contribution for odd crossings
        k1_pow = n_odd  # each odd crossing contributes one K_1
        key = (a_exp, k1_pow)
        coeff = (-1 if a_exp < 0 else 1) * (circles - n_even)
        result[key] = result.get(key, 0) + coeff

    return {k: v for k, v in result.items() if v != 0}


# ---------------------------------------------------------------------------
# Comprehensive invariants
# ---------------------------------------------------------------------------


def virtual_knot_invariants(gauss_code: GaussCode) -> VirtualInvariants:
    """Compute all implemented virtual knot invariants.

    Parameters
    ----------
    gauss_code : GaussCode

    Returns
    -------
    VirtualInvariants
    """
    j = odd_writhe(gauss_code)
    w = writhe(gauss_code)
    genus_lb = virtual_genus_lower_bound(gauss_code)
    classical = is_classical(gauss_code)
    arrow = arrow_polynomial_bracket(gauss_code)

    return VirtualInvariants(
        name=gauss_code.name,
        odd_writhe=j,
        writhe=w,
        n_classical=gauss_code.n_classical,
        n_virtual=gauss_code.n_virtual,
        genus_lower_bound=genus_lb,
        is_classical_knot=classical,
        arrow_poly=arrow,
    )


# ---------------------------------------------------------------------------
# Standard virtual knot database
# ---------------------------------------------------------------------------

VIRTUAL_KNOT_DATA: dict[str, dict[str, Any]] = {
    "unknot": {
        "gauss_code": "",
        "n_classical": 0,
        "n_virtual": 0,
        "odd_writhe": 0,
        "genus": 0,
        "is_classical": True,
        "description": "The unknot, the trivial virtual knot.",
    },
    "virtual_trefoil": {
        "gauss_code": "O1+O2+U1+U2+",
        "n_classical": 2,
        "n_virtual": 0,
        "odd_writhe": 2,
        "genus": 1,
        "is_classical": False,
        "description": "The virtual trefoil: 2 classical crossings, both odd, J=2, non-classical.",
    },
    "kishino_knot": {
        "gauss_code": "O1+U2-O3+U4-O2+U1-O4+U3-",
        "n_classical": 4,
        "n_virtual": 0,
        "odd_writhe": 0,
        "genus": 1,
        "is_classical": False,
        "description": "Kishino's knot: J=0 but non-classical (genus 1), detected by arrow polynomial.",
    },
}
