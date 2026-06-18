"""Concrete Space representations for pi-Base famous spaces.

For each of the 222 pi-Base spaces, :func:`best_space` returns the richest
available :class:`~pytop.experimental.spaces.core.Space` representation:

- **FiniteSpace** / **AlexandroffSpace** for the 17 finite pi-Base spaces
  (explicit carrier + topology, fully computable predicates)
- **Concrete infinite classes** for key named infinite spaces
  (Sorgenfrey line, Euclidean ℝ, discrete ω, cofinite on ω, order topology
  on ℚ — real membership, point_separation, and typed certificates)
- **PiBaseSpace fallback** for everything else (Boolean certificates from the
  pi-Base deductive closure; point set is opaque)

All 222 pi-Base spaces are accepted; 22 get a concrete representation.

Usage::

    from pytop.experimental.spaces.pi_base_representations import (
        best_space, is_representable, list_representable,
    )

    sp = best_space("Sierpinski space")   # FiniteSpace — fully computable
    sp = best_space("Long line")          # PiBaseSpace — certificate fallback
    sp = best_space("S000043")            # SorgenfreyLineSpace
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from itertools import combinations
from typing import Any

from ..pi_base_atlas import space_name, space_uid
from .core import CarrierKind, Space
from .pi_base_bridge import PiBaseSpace
from .representations import (
    AlexandroffSpace,
    CofiniteSpace,
    DiscreteCountableSpace,
    FiniteSpace,
    MetricTopologySpace,
    OrderTopologySpace,
    SorgenfreyLineSpace,
)

# ---------------------------------------------------------------------------
# Internal registry: UID → Space factory
# ---------------------------------------------------------------------------

_REPRESENTATIONS: dict[str, Callable[[], Space]] = {}


def _reg(uid: str) -> Callable[[Callable[[], Space]], Callable[[], Space]]:
    def decorator(fn: Callable[[], Space]) -> Callable[[], Space]:
        _REPRESENTATIONS[uid] = fn
        return fn
    return decorator


# ===========================================================================
# Finite spaces  (17 in pi-Base)
# ===========================================================================

def _all_subsets(pts: set) -> list[frozenset[Any]]:
    result: list[frozenset[Any]] = [frozenset()]
    for r in range(1, len(pts) + 1):
        result.extend(frozenset(s) for s in combinations(pts, r))
    return result


@_reg("S000001")
def _discrete_2pt() -> FiniteSpace:
    pts: set[int] = {0, 1}
    return FiniteSpace("Discrete topology on {0,1}", pts, _all_subsets(pts))


@_reg("S000004")
def _indiscrete_2pt() -> FiniteSpace:
    return FiniteSpace(
        "Indiscrete topology on {0,1}",
        {0, 1},
        [frozenset(), frozenset({0, 1})],
    )


@_reg("S000007")
def _particular_point_3pt() -> FiniteSpace:
    # Particular point topology on {0,1,2} with particular point p=0:
    # opens = {U : 0 ∈ U} ∪ {∅}
    return FiniteSpace(
        "Particular point topology on a three-point set",
        {0, 1, 2},
        [
            frozenset(),
            frozenset({0}),
            frozenset({0, 1}),
            frozenset({0, 2}),
            frozenset({0, 1, 2}),
        ],
    )


@_reg("S000010")
def _sierpinski() -> FiniteSpace:
    # Carrier {0,1}: open point is 1, closed (non-open singleton) is 0.
    return FiniteSpace(
        "Sierpinski space",
        {0, 1},
        [frozenset(), frozenset({1}), frozenset({0, 1})],
    )


@_reg("S000011")
def _excluded_point_3pt() -> FiniteSpace:
    # Excluded point topology on {0,1,2} with excluded point p=2:
    # opens = {U : 2 ∉ U} ∪ {X}
    return FiniteSpace(
        "Excluded Point Topology on a Three-Point Set",
        {0, 1, 2},
        [
            frozenset(),
            frozenset({0}),
            frozenset({1}),
            frozenset({0, 1}),
            frozenset({0, 1, 2}),
        ],
    )


@_reg("S000144")
def _diamond_alexandrov() -> AlexandroffSpace:
    # Diamond poset 2×2: {bot, a, b, top} with bot < a, bot < b, a < top, b < top.
    # Alexandroff upsets = opens: ∅, {top}, {a,top}, {b,top}, {a,b,top}, {bot,a,b,top}.
    return AlexandroffSpace(
        "Diamond poset 2x2 with Alexandrov topology",
        {"bot", "a", "b", "top"},
        [("bot", "a"), ("bot", "b"), ("a", "top"), ("b", "top")],
    )


@_reg("S000162")
def _singleton() -> FiniteSpace:
    return FiniteSpace("The Singleton", {0}, [frozenset(), frozenset({0})])


@_reg("S000163")
def _empty_space() -> FiniteSpace:
    return FiniteSpace("The Empty Space", set(), [frozenset()])


@_reg("S000164")
def _sum_singleton_indiscrete_2pt() -> FiniteSpace:
    # {0} ⊔ {1,2} (indiscrete on {1,2}).
    # Opens = {∅, {0}, {1,2}, {0,1,2}}.
    return FiniteSpace(
        "Sum of singleton and two-point indiscrete space",
        {0, 1, 2},
        [
            frozenset(),
            frozenset({0}),
            frozenset({1, 2}),
            frozenset({0, 1, 2}),
        ],
    )


@_reg("S000184")
def _sum_two_indiscrete_2pt() -> FiniteSpace:
    # {0,1} ⊔ {2,3}, both indiscrete.
    # Opens = {∅, {0,1}, {2,3}, {0,1,2,3}}.
    return FiniteSpace(
        "Sum of a pair of two-point indiscrete spaces",
        {0, 1, 2, 3},
        [
            frozenset(),
            frozenset({0, 1}),
            frozenset({2, 3}),
            frozenset({0, 1, 2, 3}),
        ],
    )


@_reg("S000187")
def _right_ray_3pt() -> AlexandroffSpace:
    # Right ray topology on {0,1,2}: total order 0 < 1 < 2.
    # Alexandroff upsets = opens: ∅, {2}, {1,2}, {0,1,2}.
    return AlexandroffSpace(
        "Right ray topology on a three-point set",
        {0, 1, 2},
        [(0, 1), (1, 2)],
    )


@_reg("S000188")
def _sum_singleton_sierpinski() -> FiniteSpace:
    # {0} ⊔ ({1,2} with Sierpiński: opens ∅, {1}, {1,2}).
    # Sum opens: ∅, {0}, {1}, {0,1}, {1,2}, {0,1,2}.
    return FiniteSpace(
        "Sum of singleton and Sierpinski space",
        {0, 1, 2},
        [
            frozenset(),
            frozenset({0}),
            frozenset({1}),
            frozenset({0, 1}),
            frozenset({1, 2}),
            frozenset({0, 1, 2}),
        ],
    )


@_reg("S000189")
def _discrete_3pt() -> FiniteSpace:
    pts: set[int] = {0, 1, 2}
    return FiniteSpace("Discrete topology on {0,1,2}", pts, _all_subsets(pts))


@_reg("S000190")
def _indiscrete_3pt() -> FiniteSpace:
    return FiniteSpace(
        "Indiscrete topology on {0,1,2}",
        {0, 1, 2},
        [frozenset(), frozenset({0, 1, 2})],
    )


@_reg("S000203")
def _three_pt_basis_singleton() -> FiniteSpace:
    # {0,1,2} with basis {{0}, X}: opens = {∅, {0}, {0,1,2}}.
    return FiniteSpace(
        "Three-point set with the basis {{0},X}",
        {0, 1, 2},
        [frozenset(), frozenset({0}), frozenset({0, 1, 2})],
    )


@_reg("S000204")
def _three_pt_basis_pair() -> FiniteSpace:
    # {0,1,2} with basis {{0,1}, X}: opens = {∅, {0,1}, {0,1,2}}.
    return FiniteSpace(
        "Three-point set with the basis {{0,1},X}",
        {0, 1, 2},
        [frozenset(), frozenset({0, 1}), frozenset({0, 1, 2})],
    )


@_reg("S000213")
def _pseudocircle() -> AlexandroffSpace:
    # 4 points {a,b,c,d} with preorder c < a, c < b, d < a, d < b.
    # Upsets (opens): ∅, {a}, {b}, {a,b}, {a,b,c}, {a,b,d}, {a,b,c,d}.
    return AlexandroffSpace(
        "Pseudocircle",
        {"a", "b", "c", "d"},
        [("c", "a"), ("c", "b"), ("d", "a"), ("d", "b")],
    )


# ===========================================================================
# Infinite spaces with concrete representations
# ===========================================================================

@_reg("S000002")
def _discrete_omega() -> DiscreteCountableSpace:
    return DiscreteCountableSpace("Discrete topology on omega")


@_reg("S000015")
def _cofinite_omega() -> CofiniteSpace:
    return CofiniteSpace(
        "Cofinite topology on omega",
        member=lambda p: isinstance(p, int) and p >= 0,
    )


@_reg("S000025")
def _euclidean_reals() -> MetricTopologySpace:
    # Points representable as int or Fraction (dense computable subset of ℝ).
    def dist(x: Any, y: Any) -> Fraction:
        return abs(Fraction(x) - Fraction(y))

    return MetricTopologySpace(
        "Euclidean real numbers R",
        distance=dist,
        member=lambda p: isinstance(p, (int, Fraction)),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000027")
def _rationals() -> OrderTopologySpace:
    return OrderTopologySpace("Rational numbers Q")


@_reg("S000043")
def _sorgenfrey_line() -> SorgenfreyLineSpace:
    return SorgenfreyLineSpace("Sorgenfrey line")


# ===========================================================================
# Public API
# ===========================================================================

def best_space(name_or_uid: str) -> Space:
    """Return the richest available Space for the given pi-Base space.

    For the 22 spaces with a concrete representation, returns a
    FiniteSpace / AlexandroffSpace / or specific infinite class whose point
    set and predicates are fully or partially computable.

    For all other pi-Base spaces (200 of 222), returns a :class:`PiBaseSpace`
    whose property certificates come from the pi-Base deductive closure.
    """
    uid = space_uid(name_or_uid)
    factory = _REPRESENTATIONS.get(uid)
    return factory() if factory is not None else PiBaseSpace(uid)


def is_representable(name_or_uid: str) -> bool:
    """True if a concrete (non-opaque) Space representation exists."""
    uid = space_uid(name_or_uid)
    return uid in _REPRESENTATIONS


def list_representable() -> list[tuple[str, str]]:
    """Return ``(uid, name)`` pairs for all concretely representable spaces."""
    return [(uid, space_name(uid)) for uid in sorted(_REPRESENTATIONS)]


__all__ = [
    "best_space",
    "is_representable",
    "list_representable",
]
