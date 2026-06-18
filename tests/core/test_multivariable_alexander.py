"""Known-answer and property tests for the multivariable Alexander polynomial.

``multivariable_alexander(link)`` computes ``Δ_L(t₁, …, tₙ)`` from a link
diagram via a Wirtinger presentation and Fox calculus over the ``n``-variable
Laurent ring.  Coefficients are returned as ``{exponent_tuple: int}`` normalised
up to units.

Test strategy
-------------
1. **Knots (n = 1)** — the result, collapsed to a single variable, reproduces
   pytop's independent braid/Burau Alexander polynomial for the trefoil and the
   figure-eight.
2. **Links (n ≥ 2)** — the Hopf link gives ``1``; the ``(2, 2k)`` torus links
   give ``Σ (t₁t₂)^i`` and satisfy the **Torres condition**
   ``Δ(t₁, 1) = (t₁^k − 1)/(t₁ − 1)`` and the interchange symmetry; the split
   unlink gives ``0``.
"""

from __future__ import annotations

from fractions import Fraction

from pytop.knot_invariants import (
    KnotDiagram,
    LinkDiagram,
    Laurent,
    alexander_polynomial_from_braid,
    _normalize_alexander,
    multivariable_alexander,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Valid PD codes (these are genuine diagrams; each label appears exactly twice).
TREFOIL_PD = KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))
FIGURE_EIGHT_PD = KnotDiagram(
    [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)], signs=(1, -1, 1, -1)
)


def _collapse_to_single(poly: dict) -> Laurent:
    """Set every variable equal to ``t`` and return a single-variable Laurent."""
    collapsed: dict[int, int] = {}
    for exponent, coeff in poly.items():
        total = sum(exponent)
        collapsed[total] = collapsed.get(total, 0) + coeff
    return Laurent({Fraction(k): v for k, v in collapsed.items()})


def _sigma1_closure_link(n: int) -> LinkDiagram:
    """Return the closure of the 2-braid ``σ₁ⁿ`` as a :class:`LinkDiagram`.

    For even ``n`` this is the ``(2, n)`` torus link (two components).
    """
    rows = [[2 * k + 1, 2 * k + 2] for k in range(n)]  # edges below crossing k
    crossings = []
    for k in range(n):
        above_left, above_right = rows[(k - 1) % n]
        below_left, below_right = rows[k]
        # understrand a → c is the right-incoming → left-outgoing strand.
        crossings.append((above_right, above_left, below_left, below_right))
    return LinkDiagram(
        crossings=crossings,
        signs=[1] * n,
        n_components=2,
        component_map=[0] * (2 * n),
    )


def _substitute(poly: dict, *, t1: int | None = None, t2: int | None = None) -> dict:
    """Substitute integer values for chosen variables; return the reduced dict."""
    result: dict = {}
    for (e1, e2), coeff in poly.items():
        value = coeff
        key: list[int] = []
        if t1 is None:
            key.append(e1)
        else:
            value *= t1 ** e1
        if t2 is None:
            key.append(e2)
        else:
            value *= t2 ** e2
        reduced = tuple(key)
        result[reduced] = result.get(reduced, 0) + value
    return {k: v for k, v in result.items() if v != 0}


# ---------------------------------------------------------------------------
# Knots (n = 1) — differential against the braid Alexander polynomial
# ---------------------------------------------------------------------------


class TestKnots:
    def test_trefoil_matches_braid_alexander(self):
        mv = multivariable_alexander(LinkDiagram.from_knot(TREFOIL_PD))
        collapsed = _normalize_alexander(_collapse_to_single(mv))
        assert collapsed == alexander_polynomial_from_braid([1, 1, 1], 2)

    def test_figure_eight_matches_braid_alexander(self):
        mv = multivariable_alexander(LinkDiagram.from_knot(FIGURE_EIGHT_PD))
        collapsed = _normalize_alexander(_collapse_to_single(mv))
        assert collapsed == alexander_polynomial_from_braid([1, -2, 1, -2], 3)

    def test_trefoil_explicit_value(self):
        # Δ = 1 − t + t²  (normalised representative, single variable)
        mv = multivariable_alexander(LinkDiagram.from_knot(TREFOIL_PD))
        assert mv == {(0,): 1, (1,): -1, (2,): 1}

    def test_figure_eight_explicit_value(self):
        # Δ = 1 − 3t + t²
        mv = multivariable_alexander(LinkDiagram.from_knot(FIGURE_EIGHT_PD))
        assert mv == {(0,): 1, (1,): -3, (2,): 1}

    def test_keys_are_length_one_tuples(self):
        mv = multivariable_alexander(LinkDiagram.from_knot(TREFOIL_PD))
        assert all(isinstance(k, tuple) and len(k) == 1 for k in mv)


# ---------------------------------------------------------------------------
# Links (n ≥ 2)
# ---------------------------------------------------------------------------


class TestLinks:
    def test_hopf_link_is_one(self):
        hopf = _sigma1_closure_link(2)
        assert multivariable_alexander(hopf) == {(0, 0): 1}

    def test_hopf_link_chirality_independent(self):
        # Δ_Hopf = 1 regardless of crossing signs (it ignores the writhe array).
        negative_hopf = LinkDiagram(
            crossings=[(1, 4, 2, 3), (3, 2, 4, 1)],
            signs=[-1, -1],
            n_components=2,
            component_map=[0, 1, 0, 1],
        )
        assert multivariable_alexander(negative_hopf) == {(0, 0): 1}

    def test_torus_link_2_4_value(self):
        # Δ_{T(2,4)} = 1 + t₁t₂
        delta = multivariable_alexander(_sigma1_closure_link(4))
        assert delta == {(0, 0): 1, (1, 1): 1}

    def test_torus_link_2_6_value(self):
        # Δ_{T(2,6)} = 1 + t₁t₂ + (t₁t₂)²
        delta = multivariable_alexander(_sigma1_closure_link(6))
        assert delta == {(0, 0): 1, (1, 1): 1, (2, 2): 1}

    def test_torus_link_torres_condition(self):
        # Δ(t₁, 1) = (t₁^k − 1)/(t₁ − 1) = 1 + t₁ + … + t₁^{k−1}, lk = k.
        delta = multivariable_alexander(_sigma1_closure_link(6))  # k = 3
        assert _substitute(delta, t2=1) == {(0,): 1, (1,): 1, (2,): 1}

    def test_torus_link_interchange_symmetry(self):
        delta = multivariable_alexander(_sigma1_closure_link(4))
        swapped = {(e2, e1): c for (e1, e2), c in delta.items()}
        assert delta == swapped

    def test_split_unlink_is_zero(self):
        unlink = LinkDiagram(crossings=[], signs=[], n_components=2, component_map=[])
        assert multivariable_alexander(unlink) == {}

    def test_unknot_is_one(self):
        unknot = LinkDiagram(crossings=[], signs=[], n_components=1, component_map=[])
        assert multivariable_alexander(unknot) == {(0,): 1}
