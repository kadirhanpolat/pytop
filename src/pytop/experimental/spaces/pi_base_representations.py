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
# Internal helpers for batch 2
# ===========================================================================

class _CertifiedSpace(Space):
    """Space with computable membership + pi-Base property certificates.

    Better than PiBaseSpace (which has certificates but opaque membership)
    for spaces whose underlying set has a decidable membership predicate.
    Does NOT provide computable point_separation.
    """

    def __init__(
        self,
        uid: str,
        member: Callable[[Any], bool],
        carrier_kind: CarrierKind,
    ) -> None:
        self._uid = uid
        self.name = space_name(uid)
        self.carrier_kind = carrier_kind
        self._member = member
        self._bridge = PiBaseSpace(uid)

    def contains(self, point: Any) -> bool:
        return bool(self._member(point))

    def certificate(self, prop: str) -> Any:
        return self._bridge.certificate(prop)


class _MetricWithCerts(MetricTopologySpace):
    """Metric space whose property certificates come from pi-Base (most specific).

    Combines computable point_separation (from the metric) with the full
    pi-Base deduced trait matrix (compact, connected, second-countable, …).
    """

    def __init__(
        self,
        uid: str,
        dist: Callable[[Any, Any], Fraction],
        member: Callable[[Any], bool],
        carrier_kind: CarrierKind,
    ) -> None:
        super().__init__(space_name(uid), dist, member, carrier_kind)
        self._bridge = PiBaseSpace(uid)

    def certificate(self, prop: str) -> Any:
        cert = self._bridge.certificate(prop)
        return cert if cert is not None else super().certificate(prop)


def _euclidean_dist(x: Any, y: Any) -> Fraction:
    return abs(Fraction(x) - Fraction(y))


def _plane_dist(p: Any, q: Any) -> Fraction:
    dx = Fraction(p[0]) - Fraction(q[0])
    dy = Fraction(p[1]) - Fraction(q[1])
    # Exact Pythagorean distance is irrational in general; use max-norm instead
    # (generates the same topology as Euclidean on ℝ²).
    return max(abs(dx), abs(dy))


# ===========================================================================
# Batch 2 — metric spaces
# ===========================================================================

@_reg("S000003")
def _discrete_reals() -> _MetricWithCerts:
    # Discrete topology on ℝ: discrete metric d(x,y)=1 for x≠y.
    def _disc_dist(x: Any, y: Any) -> Fraction:
        return Fraction(0) if Fraction(x) == Fraction(y) else Fraction(1)

    return _MetricWithCerts(
        "S000003",
        dist=_disc_dist,
        member=lambda p: isinstance(p, (int, Fraction)),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000133")
def _post_office_metric() -> _MetricWithCerts:
    # Post office metric on ℝ: d(x,y) = |x|+|y| for x≠y, 0 for x=y.
    def _post_dist(x: Any, y: Any) -> Fraction:
        fx, fy = Fraction(x), Fraction(y)
        return Fraction(0) if fx == fy else abs(fx) + abs(fy)

    return _MetricWithCerts(
        "S000133",
        dist=_post_dist,
        member=lambda p: isinstance(p, (int, Fraction)),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000158")
def _unit_interval() -> _MetricWithCerts:
    # Unit interval [0,1] with Euclidean metric.
    return _MetricWithCerts(
        "S000158",
        dist=_euclidean_dist,
        member=lambda p: isinstance(p, (int, Fraction)) and Fraction(0) <= Fraction(p) <= Fraction(1),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000176")
def _euclidean_plane() -> _MetricWithCerts:
    # Euclidean plane ℝ² — points as (Fraction, Fraction) or (int, int) tuples.
    # Uses max-norm (equivalent topology to Euclidean, exact arithmetic).
    return _MetricWithCerts(
        "S000176",
        dist=_plane_dist,
        member=lambda p: (
            isinstance(p, tuple)
            and len(p) == 2
            and isinstance(p[0], (int, Fraction))
            and isinstance(p[1], (int, Fraction))
        ),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000210")
def _half_open_interval() -> _MetricWithCerts:
    # Half-open interval [0,1) with Euclidean subspace metric.
    return _MetricWithCerts(
        "S000210",
        dist=_euclidean_dist,
        member=lambda p: isinstance(p, (int, Fraction)) and Fraction(0) <= Fraction(p) < Fraction(1),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000225")
def _upper_half_plane() -> _MetricWithCerts:
    # Closed upper half-plane ℝ²₊ = {(x,y) : y ≥ 0} with Euclidean (max-norm) metric.
    return _MetricWithCerts(
        "S000225",
        dist=_plane_dist,
        member=lambda p: (
            isinstance(p, tuple)
            and len(p) == 2
            and isinstance(p[0], (int, Fraction))
            and isinstance(p[1], (int, Fraction))
            and Fraction(p[1]) >= 0
        ),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


# ===========================================================================
# Batch 2 — certified countable/infinite spaces
# ===========================================================================

def _OMEGA_MEMBER(p: Any) -> bool:
    return isinstance(p, int) and p >= 0

def _POS_INT_MEMBER(p: Any) -> bool:
    return isinstance(p, int) and p > 0

def _INT_MEMBER(p: Any) -> bool:
    return isinstance(p, int)

def _REAL_MEMBER(p: Any) -> bool:
    return isinstance(p, (int, Fraction))


@_reg("S000005")
def _odd_even() -> _CertifiedSpace:
    # Odd-Even topology on ℤ+ = {1,2,3,…}.
    return _CertifiedSpace("S000005", _POS_INT_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000008")
def _particular_point_omega() -> _CertifiedSpace:
    # Particular point topology on a countably infinite set (carrier ω).
    return _CertifiedSpace("S000008", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000009")
def _particular_point_reals() -> _CertifiedSpace:
    # Particular point topology on ℝ.
    return _CertifiedSpace("S000009", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000012")
def _excluded_point_omega() -> _CertifiedSpace:
    # Excluded Point Topology on a Countably Infinite Set (carrier ω).
    return _CertifiedSpace("S000012", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000013")
def _excluded_point_reals() -> _CertifiedSpace:
    # Excluded point topology on ℝ.
    return _CertifiedSpace("S000013", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000016")
def _cofinite_reals() -> _CertifiedSpace:
    # Cofinite topology on ℝ — NOT second-countable (pi-Base correctly deduces False).
    return _CertifiedSpace("S000016", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000017")
def _cocountable_reals() -> _CertifiedSpace:
    # Cocountable topology on ℝ.
    return _CertifiedSpace("S000017", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000049")
def _divisor_topology() -> _CertifiedSpace:
    # Divisor topology on ℤ+ = {1,2,3,…}.
    return _CertifiedSpace("S000049", _POS_INT_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000051")
def _khalimsky_line() -> _CertifiedSpace:
    # Khalimsky line on ℤ.
    return _CertifiedSpace("S000051", _INT_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000052")
def _relatively_prime_integers() -> _CertifiedSpace:
    # Relatively prime integer topology on ℤ+.
    return _CertifiedSpace("S000052", _POS_INT_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000053")
def _prime_integer_topology() -> _CertifiedSpace:
    # Prime integer topology on ℤ+.
    return _CertifiedSpace("S000053", _POS_INT_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000193")
def _indiscrete_omega() -> _CertifiedSpace:
    # Indiscrete topology on ω.
    return _CertifiedSpace("S000193", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000199")
def _left_ray_omega() -> _CertifiedSpace:
    # Left ray topology on ω: opens are left rays {0,…,n} and ∅.
    return _CertifiedSpace("S000199", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000200")
def _right_ray_omega() -> _CertifiedSpace:
    # Right ray topology on ω: opens are right rays {n, n+1,…} and ∅.
    return _CertifiedSpace("S000200", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


# ===========================================================================
# Batch 3 — metric spaces with radial/post-office structure
# ===========================================================================

@_reg("S000134")
def _radial_metric_plane() -> _MetricWithCerts:
    # Radial (French railway) metric on ℝ²: d(p,q) = ||p-O||+||q-O|| unless
    # p,q lie on the same ray from O, where d = |||p|-|q|||.  Uses max-norm.
    def _radial_dist(p: Any, q: Any) -> Fraction:
        if p == q:
            return Fraction(0)
        px, py = Fraction(p[0]), Fraction(p[1])
        qx, qy = Fraction(q[0]), Fraction(q[1])
        norm_p = max(abs(px), abs(py))
        norm_q = max(abs(qx), abs(qy))
        cross = px * qy - py * qx
        dot = px * qx + py * qy
        if cross == 0 and dot >= 0:          # same ray from origin
            return abs(norm_p - norm_q)
        return norm_p + norm_q

    return _MetricWithCerts(
        "S000134",
        dist=_radial_dist,
        member=lambda p: (
            isinstance(p, tuple)
            and len(p) == 2
            and isinstance(p[0], (int, Fraction))
            and isinstance(p[1], (int, Fraction))
        ),
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


@_reg("S000198")
def _disjoint_union_reals_singleton() -> _MetricWithCerts:
    # Disjoint union ℝ ⊔ {∗}: d(a,b)=|a-b| within ℝ; d(∗,x)=1 across components.
    def _du_dist(a: Any, b: Any) -> Fraction:
        if a == b:
            return Fraction(0)
        if isinstance(a, (int, Fraction)) and isinstance(b, (int, Fraction)):
            return abs(Fraction(a) - Fraction(b))
        return Fraction(1)   # different components

    def _du_member(p: Any) -> bool:
        return p == "*" or isinstance(p, (int, Fraction))

    return _MetricWithCerts(
        "S000198",
        dist=_du_dist,
        member=_du_member,
        carrier_kind=CarrierKind.UNCOUNTABLE,
    )


# ===========================================================================
# Batch 3 — certified countable/infinite spaces
# ===========================================================================

def _OMEGA1_MEMBER(p: Any) -> bool:
    """Carrier ω+1 = ω ∪ {ω}."""
    return p == "ω" or (isinstance(p, int) and p >= 0)

def _Q01_MEMBER(p: Any) -> bool:
    """Carrier ℚ ∩ [0,1]."""
    return isinstance(p, (int, Fraction)) and Fraction(0) <= Fraction(p) <= Fraction(1)

def _ORDINAL_WW_MEMBER(p: Any) -> bool:
    """Carrier ω+ω as pairs (copy, index): (0,n) for first ω, (1,n) for second."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and p[0] in (0, 1)
        and isinstance(p[1], int)
        and p[1] >= 0
    )

def _ORDINAL_WW1_MEMBER(p: Any) -> bool:
    """Carrier ω+ω+1: pairs (0|1, n≥0) plus sentinel 'Ω'."""
    return p == "Ω" or _ORDINAL_WW_MEMBER(p)

def _GRID_OR_INF_MEMBER(p: Any) -> bool:
    """Carrier ω×ω ∪ {∞}: (int≥0, int≥0) tuples or '∞'."""
    return p == "∞" or (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], int) and p[0] >= 0
        and isinstance(p[1], int) and p[1] >= 0
    )

def _SIERP_SUM_MEMBER(p: Any) -> bool:
    """Carrier ω×{0,1}: (n, b) with n≥0 int, b in {0,1}."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], int) and p[0] >= 0
        and p[1] in (0, 1)
    )

def _TWO_ORIGIN_MEMBER(p: Any) -> bool:
    """Line with two origins: real points (Fraction, non-zero) or '0a'/'0b'."""
    if p in ("0a", "0b"):
        return True
    return isinstance(p, (int, Fraction)) and Fraction(p) != 0

def _DOUBLE_REAL_MEMBER(p: Any) -> bool:
    """Double pointed reals ℝ×{0,1}: (x, k) with x∈ℚ, k∈{0,1}."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], (int, Fraction))
        and p[1] in (0, 1)
    )

def _INT_BROOM_MEMBER(p: Any) -> bool:
    """Integer broom: (n, t) with n∈ℤ, t∈ℚ∩[0,1]."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], int)
        and isinstance(p[1], (int, Fraction))
        and Fraction(0) <= Fraction(p[1]) <= Fraction(1)
    )

def _SEQ_FAN_MEMBER(p: Any) -> bool:
    """Metric fan (ω-many spines): (n, m) with n≥0, m≥0 or '∞'."""
    return p == "∞" or (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], int) and p[0] >= 0
        and isinstance(p[1], int) and p[1] >= 0
    )

def _CONV_SEQ_MEMBER(p: Any) -> bool:
    """Converging sequence of non-Hausdorff spaces: (n, b) or '∞'."""
    return p == "∞" or (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], int) and p[0] >= 0
        and p[1] in (0, 1)
    )

def _FOCAL_MEMBER(p: Any) -> bool:
    """ℚ extended by focal point: Fraction or '∗'."""
    return p == "*" or isinstance(p, (int, Fraction))


# — ordinal spaces —

@_reg("S000033")
def _ordinal_omega_omega() -> _CertifiedSpace:
    return _CertifiedSpace("S000033", _ORDINAL_WW_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000034")
def _ordinal_omega_omega_1() -> _CertifiedSpace:
    return _CertifiedSpace("S000034", _ORDINAL_WW1_MEMBER, CarrierKind.COUNTABLE)


# — uncountable spaces with computable membership —

@_reg("S000042")
def _right_ray_reals() -> _CertifiedSpace:
    # Right ray topology on ℝ: opens are right rays (a,∞) and ∅. T0 but not T1.
    return _CertifiedSpace("S000042", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000054")
def _double_pointed_reals() -> _CertifiedSpace:
    # Double pointed reals ℝ×{0,1}: (x,0) and (x,1) are topologically indistinct.
    return _CertifiedSpace("S000054", _DOUBLE_REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000083")
def _line_two_origins() -> _CertifiedSpace:
    # Line with two origins: ℝ with 0 doubled to '0a' and '0b'. T1, not T2.
    return _CertifiedSpace("S000083", _TWO_ORIGIN_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000194")
def _indiscrete_reals() -> _CertifiedSpace:
    # Indiscrete topology on ℝ: only ∅ and ℝ are open.
    return _CertifiedSpace("S000194", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


# — countable spaces: one-point compactifications —

@_reg("S000023")
def _arens_fort() -> _CertifiedSpace:
    # Arens-Fort space: carrier ω×ω ∪ {∞}, the unique limit point is '∞'.
    return _CertifiedSpace("S000023", _GRID_OR_INF_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000029")
def _one_pt_compact_Q() -> _CertifiedSpace:
    # One-point compactification of ℚ: ℚ ∪ {∞}.
    return _CertifiedSpace("S000029", _FOCAL_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000050")
def _Q_focal_point() -> _CertifiedSpace:
    # ℚ extended by a focal point '∗': ∗ belongs to every nonempty open set.
    return _CertifiedSpace("S000050", _FOCAL_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000165")
def _one_pt_compact_arens_fort() -> _CertifiedSpace:
    # One-point compactification of the Arens-Fort space: grid ∪ {∞}.
    return _CertifiedSpace("S000165", _GRID_OR_INF_MEMBER, CarrierKind.COUNTABLE)


# — countable spaces: ray topologies on ω+1 —

@_reg("S000160")
def _right_open_ray_omega1() -> _CertifiedSpace:
    # Right "open-ray" topology on ω+1: carrier = ω ∪ {ω}.
    return _CertifiedSpace("S000160", _OMEGA1_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000166")
def _left_ray_omega1() -> _CertifiedSpace:
    # Left ray topology on ω+1: opens are downward-closed initial segments.
    return _CertifiedSpace("S000166", _OMEGA1_MEMBER, CarrierKind.COUNTABLE)


# — countable spaces: interval topologies on ℚ∩[0,1] —

@_reg("S000150")
def _right_closed_ray_Q01() -> _CertifiedSpace:
    # Right "closed-ray" topology on ℚ∩[0,1]: opens are [a,1]∩ℚ∩[0,1].
    return _CertifiedSpace("S000150", _Q01_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000151")
def _right_open_ray_Q01() -> _CertifiedSpace:
    # Right "open-ray" topology on ℚ∩[0,1]: opens are (a,1]∩ℚ∩[0,1].
    return _CertifiedSpace("S000151", _Q01_MEMBER, CarrierKind.COUNTABLE)


# — countable spaces: sum/fan/broom structures —

@_reg("S000047")
def _countable_sum_sierpinski() -> _CertifiedSpace:
    # Countable sum of Sierpiński spaces: ω×{0,1} with Sierpiński topo on each copy.
    return _CertifiedSpace("S000047", _SIERP_SUM_MEMBER, CarrierKind.COUNTABLE)


def _OMEGA_OR_STAR_MEMBER(p: Any) -> bool:
    """Carrier ω ∪ {'∗'}: non-negative int or the sentinel '∗'."""
    return p == "*" or (isinstance(p, int) and p >= 0)


@_reg("S000048")
def _cofinite_omega_generic() -> _CertifiedSpace:
    # Cofinite on ω extended by a non-open generic point '∗'.
    return _CertifiedSpace("S000048", _OMEGA_OR_STAR_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000096")
def _appert_space() -> _CertifiedSpace:
    # Appert space: carrier ℤ>0.
    return _CertifiedSpace("S000096", _POS_INT_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000097")
def _one_pt_compact_seq_fan() -> _CertifiedSpace:
    # One-point compactification of sequential fan S_ω: (n,m) ∪ {∞}.
    return _CertifiedSpace("S000097", _SEQ_FAN_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000098")
def _minimal_hausdorff_omega() -> _CertifiedSpace:
    # Minimal Hausdorff topology on ω.
    return _CertifiedSpace("S000098", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000100")
def _david_gao_space() -> _CertifiedSpace:
    # David Gao's ultraconnected non-contractible space: carrier ω.
    return _CertifiedSpace("S000100", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000118")
def _integer_broom() -> _CertifiedSpace:
    # Integer broom: (n, t) pairs with n∈ℤ, t∈ℚ∩[0,1].
    return _CertifiedSpace("S000118", _INT_BROOM_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000185")
def _one_pt_compact_metric_fan() -> _CertifiedSpace:
    # One-point compactification of the metric fan: (n,m) pairs ∪ {∞}.
    return _CertifiedSpace("S000185", _SEQ_FAN_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000186")
def _converging_seq_non_hausdorff() -> _CertifiedSpace:
    # Converging sequence of non-Hausdorff spaces: (n,b) pairs ∪ {∞}.
    return _CertifiedSpace("S000186", _CONV_SEQ_MEMBER, CarrierKind.COUNTABLE)


# ===========================================================================
# Batch 4 — member helpers
# ===========================================================================

def _R_MINUS_Z_MEMBER(p: Any) -> bool:
    r"""ℝ\ℤ — Fraction-valued rationals that are not integers."""
    return isinstance(p, Fraction) and p.denominator != 1


def _Q_CLOSED_UNIT_MEMBER(p: Any) -> bool:
    """Q ∩ [-1,1]."""
    return isinstance(p, (int, Fraction)) and Fraction(-1) <= Fraction(p) <= Fraction(1)


def _PLANE_MEMBER(p: Any) -> bool:
    """ℝ² — (int|Fraction, int|Fraction) pairs."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], (int, Fraction))
        and isinstance(p[1], (int, Fraction))
    )


def _TELOPHASE_MEMBER(p: Any) -> bool:
    """[0,1) ∪ {'1a','1b'} — doubled endpoint variant of [0,1]."""
    if p in ("1a", "1b"):
        return True
    return isinstance(p, (int, Fraction)) and Fraction(0) <= Fraction(p) < Fraction(1)


def _DOUBLE_ORIGIN_PLANE_MEMBER(p: Any) -> bool:
    r"""ℝ²\{(0,0)} ∪ {'0a','0b'} — plane with doubled origin."""
    if p in ("0a", "0b"):
        return True
    return (
        _PLANE_MEMBER(p)
        and (Fraction(p[0]) != 0 or Fraction(p[1]) != 0)
    )


def _DOUBLE_ARROW_MEMBER(p: Any) -> bool:
    """{0,1} × (Q∩[0,1]) — double arrow space."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and p[0] in (0, 1)
        and isinstance(p[1], (int, Fraction))
        and Fraction(0) <= Fraction(p[1]) <= Fraction(1)
    )


# ===========================================================================
# Batch 4 — certified spaces
# ===========================================================================

@_reg("S000006")
def _deleted_integer_topology() -> _CertifiedSpace:
    # Deleted integer topology on ℝ\ℤ: non-integer rationals.
    return _CertifiedSpace("S000006", _R_MINUS_Z_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000014")
def _either_or_topology() -> _CertifiedSpace:
    # Either-Or topology on [-1,1]: carrier Q ∩ [-1,1].
    return _CertifiedSpace("S000014", _Q_CLOSED_UNIT_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000019")
def _compact_complement_reals() -> _CertifiedSpace:
    # Compact complement topology for Euclidean ℝ.
    return _CertifiedSpace("S000019", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000020")
def _fort_space_omega() -> _CertifiedSpace:
    # Fort space on a countably infinite set (carrier ω ∪ {∗}).
    return _CertifiedSpace("S000020", _OMEGA_OR_STAR_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000022")
def _fortissimo_reals() -> _CertifiedSpace:
    # Fortissimo space on ℝ (carrier ℝ ∪ {∗}).
    return _CertifiedSpace("S000022", _FOCAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000024")
def _modified_fort_reals() -> _CertifiedSpace:
    # Modified Fort space on ℝ (carrier ℝ ∪ {∗}).
    return _CertifiedSpace("S000024", _FOCAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000044")
def _nested_interval_topology() -> _CertifiedSpace:
    # Nested interval topology on ℝ.
    return _CertifiedSpace("S000044", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000045")
def _overlapping_interval_topology() -> _CertifiedSpace:
    # Overlapping interval topology on ℝ.
    return _CertifiedSpace("S000045", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000046")
def _interlocking_interval_topology() -> _CertifiedSpace:
    # Interlocking interval topology on ℝ.
    return _CertifiedSpace("S000046", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000055")
def _countable_complement_extension() -> _CertifiedSpace:
    # Countable complement extension topology on ℝ.
    return _CertifiedSpace("S000055", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000056")
def _smirnov_deleted_sequence() -> _CertifiedSpace:
    # Smirnov's deleted sequence topology on ℝ.
    return _CertifiedSpace("S000056", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000057")
def _rational_sequence_topology() -> _CertifiedSpace:
    # Rational sequence topology on ℝ.
    return _CertifiedSpace("S000057", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000063")
def _michael_line() -> _CertifiedSpace:
    # Michael line on ℝ.
    return _CertifiedSpace("S000063", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000065")
def _telophase_topology() -> _CertifiedSpace:
    # Telophase topology on [0,1] with endpoint 1 doubled to '1a','1b'.
    return _CertifiedSpace("S000065", _TELOPHASE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000066")
def _double_origin_plane() -> _CertifiedSpace:
    # Double origin plane: ℝ²\{(0,0)} ∪ {'0a','0b'}.
    return _CertifiedSpace("S000066", _DOUBLE_ORIGIN_PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000076")
def _sorgenfrey_plane() -> _CertifiedSpace:
    # Sorgenfrey plane ℝ²_ℓ: product of two Sorgenfrey lines (carrier ℝ²).
    return _CertifiedSpace("S000076", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000093")
def _double_arrow_space() -> _CertifiedSpace:
    # Double arrow space {0,1}×[0,1] with lexicographic order topology.
    return _CertifiedSpace("S000093", _DOUBLE_ARROW_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000131")
def _sequential_fan_omega_spines() -> _CertifiedSpace:
    # Sequential fan S_ω with ω-many spines (carrier (n,m)∪{∞}).
    return _CertifiedSpace("S000131", _SEQ_FAN_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000140")
def _reals_cocountable_pt() -> _CertifiedSpace:
    # ℝ extended by a point '∗' with co-countable open neighborhoods.
    return _CertifiedSpace("S000140", _FOCAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000154")
def _fort_space_reals() -> _CertifiedSpace:
    # Fort space on ℝ (carrier ℝ ∪ {∗}).
    return _CertifiedSpace("S000154", _FOCAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000159")
def _right_open_ray_01() -> _CertifiedSpace:
    # Right "open-ray" topology on [0,1]: opens are (a,1] ∩ [0,1].
    return _CertifiedSpace("S000159", _Q01_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000202")
def _metric_fan_omega_spines() -> _CertifiedSpace:
    # Metric fan with ω-many spines (carrier (n,m)∪{∞}).
    return _CertifiedSpace("S000202", _SEQ_FAN_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000206")
def _deleted_sequence_intervals() -> _CertifiedSpace:
    # Deleted Sequence of Intervals Topology on ℝ.
    return _CertifiedSpace("S000206", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


# ===========================================================================
# Batch 5 — member helpers
# ===========================================================================

def _UPPER_HALF_MEMBER(p: Any) -> bool:
    """Closed upper half-plane {(x,y): y ≥ 0}."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], (int, Fraction))
        and isinstance(p[1], (int, Fraction))
        and Fraction(p[1]) >= 0
    )


def _UNIT_SQUARE_MEMBER(p: Any) -> bool:
    """Q² ∩ [0,1]² — rational points in the unit square."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], (int, Fraction))
        and isinstance(p[1], (int, Fraction))
        and Fraction(0) <= Fraction(p[0]) <= Fraction(1)
        and Fraction(0) <= Fraction(p[1]) <= Fraction(1)
    )


def _INT_PLANE_MEMBER(p: Any) -> bool:
    """ℤ² — pairs of integers."""
    return isinstance(p, tuple) and len(p) == 2 and isinstance(p[0], int) and isinstance(p[1], int)


def _LINE_COUNT_ORIGINS_MEMBER(p: Any) -> bool:
    """ℝ\\{0} ∪ {(0,n): n∈ω} — line with countably many origins."""
    if isinstance(p, tuple) and len(p) == 2 and p[0] == 0 and isinstance(p[1], int) and p[1] >= 0:
        return True
    return isinstance(p, (int, Fraction)) and Fraction(p) != 0


def _OPC_Q_SQ_MEMBER(p: Any) -> bool:
    """(Q∪{∞})² — carrier of the square of one-point compactification of Q."""
    def _opc_coord(x: Any) -> bool:
        return x == "∞" or isinstance(x, (int, Fraction))
    return isinstance(p, tuple) and len(p) == 2 and _opc_coord(p[0]) and _opc_coord(p[1])


def _INFBROOM_MEMBER(p: Any) -> bool:
    """{(0,0)} ∪ {(x,y): x=1/n n∈ℤ+, y∈Q∩[0,1]} — infinite broom."""
    if not (isinstance(p, tuple) and len(p) == 2):
        return False
    x, y = p
    if not (isinstance(x, (int, Fraction)) and isinstance(y, (int, Fraction))):
        return False
    fx, fy = Fraction(x), Fraction(y)
    if not (Fraction(0) <= fy <= Fraction(1)):
        return False
    if fx == 0:
        return fy == 0   # only (0,0) on the y-axis
    if fx <= 0:
        return False
    # x must equal 1/n for some positive integer n, i.e., 1/x is a positive integer
    inv_x = Fraction(1) / fx
    return inv_x.denominator == 1 and inv_x >= 1


def _CLOSED_INFBROOM_MEMBER(p: Any) -> bool:
    """{0}×(Q∩[0,1]) ∪ {(x,y): x=1/n n∈ℤ+, y∈Q∩[0,1]} — closed infinite broom."""
    if not (isinstance(p, tuple) and len(p) == 2):
        return False
    x, y = p
    if not (isinstance(x, (int, Fraction)) and isinstance(y, (int, Fraction))):
        return False
    fx, fy = Fraction(x), Fraction(y)
    if not (Fraction(0) <= fy <= Fraction(1)):
        return False
    if fx == 0:
        return True   # entire spine {0}×[0,1]
    if fx <= 0:
        return False
    inv_x = Fraction(1) / fx
    return inv_x.denominator == 1 and inv_x >= 1


# ===========================================================================
# Batch 5 — certified spaces
# ===========================================================================

@_reg("S000018")
def _double_pointed_cocountable() -> _CertifiedSpace:
    # Double pointed cocountable topology on ℝ (carrier ℝ×{0,1}).
    return _CertifiedSpace("S000018", _DOUBLE_REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000031")
def _square_opc_Q() -> _CertifiedSpace:
    # Square of one-point compactification of Q: carrier (Q∪{∞})².
    return _CertifiedSpace("S000031", _OPC_Q_SQ_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000041")
def _lex_ordered_unit_square() -> _CertifiedSpace:
    # Lexicographically ordered unit square [0,1]²: carrier Q²∩[0,1]².
    return _CertifiedSpace("S000041", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000067")
def _irrational_slope_topology() -> _CertifiedSpace:
    # Irrational slope topology on Q²: carrier Q² (plane with rational coords).
    return _CertifiedSpace("S000067", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000068")
def _deleted_diameter_topology() -> _CertifiedSpace:
    # Deleted diameter topology: carrier ℝ².
    return _CertifiedSpace("S000068", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000069")
def _deleted_radius_topology() -> _CertifiedSpace:
    # Deleted radius topology: carrier ℝ².
    return _CertifiedSpace("S000069", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000070")
def _half_disc_topology() -> _CertifiedSpace:
    # Half-disc topology: carrier = closed upper half-plane {y ≥ 0}.
    return _CertifiedSpace("S000070", _UPPER_HALF_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000071")
def _irregular_lattice_topology() -> _CertifiedSpace:
    # Irregular lattice topology: carrier ℤ².
    return _CertifiedSpace("S000071", _INT_PLANE_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000074")
def _niemytzki_plane() -> _CertifiedSpace:
    # Niemytzki (tangent disc) plane: carrier = closed upper half-plane {y ≥ 0}.
    return _CertifiedSpace("S000074", _UPPER_HALF_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000075")
def _rational_tangent_disc() -> _CertifiedSpace:
    # Rational tangent disc topology: carrier ℝ².
    return _CertifiedSpace("S000075", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000084")
def _line_countable_origins() -> _CertifiedSpace:
    # Line with countably many origins: ℝ\\{0} ∪ {(0,n): n∈ω}.
    return _CertifiedSpace("S000084", _LINE_COUNT_ORIGINS_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000086")
def _everywhere_doubled_line() -> _CertifiedSpace:
    # Everywhere doubled line: ℝ×{0,1}.
    return _CertifiedSpace("S000086", _DOUBLE_REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000094")
def _strong_parallel_line() -> _CertifiedSpace:
    # Strong parallel line topology: carrier ℝ².
    return _CertifiedSpace("S000094", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000095")
def _concentric_circles() -> _CertifiedSpace:
    # Concentric circles topology: carrier ℝ².
    return _CertifiedSpace("S000095", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000099")
def _alexandroff_square() -> _CertifiedSpace:
    # Alexandroff square [0,1]²: carrier Q²∩[0,1]².
    return _CertifiedSpace("S000099", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000112")
def _nested_rectangles() -> _CertifiedSpace:
    # Nested rectangles in the real plane: carrier ℝ².
    return _CertifiedSpace("S000112", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000116")
def _infinite_broom() -> _CertifiedSpace:
    # Infinite broom: {(0,0)} ∪ spokes {(1/n, t): n∈ℤ+, t∈[0,1]}.
    return _CertifiedSpace("S000116", _INFBROOM_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000117")
def _closed_infinite_broom() -> _CertifiedSpace:
    # Closed infinite broom: spine {0}×[0,1] ∪ spokes {(1/n,t): n∈ℤ+, t∈[0,1]}.
    return _CertifiedSpace("S000117", _CLOSED_INFBROOM_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000119")
def _nested_angles() -> _CertifiedSpace:
    # Nested angles in the real plane: carrier ℝ².
    return _CertifiedSpace("S000119", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


# ===========================================================================
# Batch 6 — member helpers
# ===========================================================================

def _POINTED_RAT_EXT_MEMBER(p: Any) -> bool:
    """ℝ ∪ {(q,1): q∈Q} — pointed rational extension carrier."""
    if isinstance(p, tuple) and len(p) == 2 and isinstance(p[0], (int, Fraction)) and p[1] == 1:
        return True
    return isinstance(p, (int, Fraction))


def _CIRCLE_MEMBER(p: Any) -> bool:
    """Rational points on S¹: {(p,q)∈Q²: p²+q²=1}."""
    if not (isinstance(p, tuple) and len(p) == 2):
        return False
    x, y = p
    if not (isinstance(x, (int, Fraction)) and isinstance(y, (int, Fraction))):
        return False
    return Fraction(x) ** 2 + Fraction(y) ** 2 == Fraction(1)


def _SPHERE_MEMBER(p: Any) -> bool:
    """Rational points on S²: {(p,q,r)∈Q³: p²+q²+r²=1}."""
    if not (isinstance(p, tuple) and len(p) == 3):
        return False
    x, y, z = p
    if not (isinstance(x, (int, Fraction)) and isinstance(y, (int, Fraction)) and isinstance(z, (int, Fraction))):
        return False
    return Fraction(x) ** 2 + Fraction(y) ** 2 + Fraction(z) ** 2 == Fraction(1)


def _POSET_BROOM_MEMBER(p: Any) -> bool:
    r"""Carrier of {-1, 0_a, 0_b} ∪ {1/n: n∈Z+} with Alexandroff topology."""
    if p in (-1, "0a", "0b"):
        return True
    if not isinstance(p, (int, Fraction)):
        return False
    fp = Fraction(p)
    if fp <= 0:
        return False
    inv = Fraction(1) / fp
    return inv.denominator == 1 and inv >= 1


def _BOUQUET_MEMBER(p: Any) -> bool:
    """Countable bouquet of circles: (n, q) with n∈ω, q∈Q∩[0,1)."""
    return (
        isinstance(p, tuple)
        and len(p) == 2
        and isinstance(p[0], int) and p[0] >= 0
        and isinstance(p[1], (int, Fraction))
        and Fraction(0) <= Fraction(p[1]) < Fraction(1)
    )


def _CIRCLE_TWO_ORIGINS_MEMBER(p: Any) -> bool:
    """S¹ with doubled basepoint: rational S¹\\{(1,0)} ∪ {'0a','0b'}."""
    if p in ("0a", "0b"):
        return True
    if not _CIRCLE_MEMBER(p):
        return False
    return p != (Fraction(1), Fraction(0)) and p != (1, 0)


# ===========================================================================
# Batch 6 — certified spaces
# ===========================================================================

@_reg("S000060")
def _pointed_rational_extension() -> _CertifiedSpace:
    # Pointed rational extension of ℝ: ℝ ∪ {(q,1): q∈Q}.
    return _CertifiedSpace("S000060", _POINTED_RAT_EXT_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000062")
def _discrete_rational_extension() -> _CertifiedSpace:
    # Discrete rational extension of ℝ: carrier ℝ ∪ {(q,1): q∈Q}.
    return _CertifiedSpace("S000062", _POINTED_RAT_EXT_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000072")
def _arens_square() -> _CertifiedSpace:
    # Arens square: specific topology on a subset of [0,1]², carrier Q²∩[0,1]².
    return _CertifiedSpace("S000072", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000073")
def _simplified_arens_square() -> _CertifiedSpace:
    # Simplified Arens square: carrier Q²∩[0,1]².
    return _CertifiedSpace("S000073", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000080")
def _scott_modified_arens_square() -> _CertifiedSpace:
    # B. Scott's modified Arens square: carrier Q²∩[0,1]².
    return _CertifiedSpace("S000080", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000129")
def _wheel_without_hub() -> _CertifiedSpace:
    # Wheel without its hub: subspace of ℝ², carrier ℝ².
    return _CertifiedSpace("S000129", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000135")
def _radial_interval_topology() -> _CertifiedSpace:
    # Radial interval topology on ℝ²: carrier ℝ².
    return _CertifiedSpace("S000135", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000139")
def _countable_bouquet_circles() -> _CertifiedSpace:
    # Countable bouquet of circles: carrier ω×(Q∩[0,1)).
    return _CertifiedSpace("S000139", _BOUQUET_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000143")
def _butterfly_space() -> _CertifiedSpace:
    # Butterfly space: topology on ℝ² with butterfly-shaped neighborhoods.
    return _CertifiedSpace("S000143", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000145")
def _free_ultrafilter_omega() -> _CertifiedSpace:
    # Free ultrafilter topology on ω: carrier ω.
    return _CertifiedSpace("S000145", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000152")
def _poset_broom_alexandroff() -> _CertifiedSpace:
    # Poset {-1, 0_a, 0_b} ∪ {1/n: n∈Z+} with Alexandroff topology.
    return _CertifiedSpace("S000152", _POSET_BROOM_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000156")
def _arens_space() -> _CertifiedSpace:
    # Arens space: sequential but non-first-countable countable space (carrier ω×ω ∪ {∞}).
    return _CertifiedSpace("S000156", _GRID_OR_INF_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000169")
def _sphere_S2() -> _CertifiedSpace:
    # Sphere S²: rational points on unit sphere {p²+q²+r²=1}.
    return _CertifiedSpace("S000169", _SPHERE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000170")
def _circle_S1() -> _CertifiedSpace:
    # Circle S¹: rational points on unit circle {p²+q²=1}.
    return _CertifiedSpace("S000170", _CIRCLE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000175")
def _radial_plane() -> _CertifiedSpace:
    # Radial plane: topology on ℝ² using radial neighborhoods.
    return _CertifiedSpace("S000175", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000192")
def _modified_telophase() -> _CertifiedSpace:
    # Modified telophase topology on [0,1]: carrier Q∩[0,1].
    return _CertifiedSpace("S000192", _Q01_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000201")
def _infinite_earring() -> _CertifiedSpace:
    # Infinite earring: wedge of countably many circles (subspace of ℝ²).
    return _CertifiedSpace("S000201", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000205")
def _warsaw_circle() -> _CertifiedSpace:
    # Warsaw circle: compact connected subspace of ℝ².
    return _CertifiedSpace("S000205", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000209")
def _circle_two_origins() -> _CertifiedSpace:
    # Circle with two origins: S¹ with basepoint (1,0) doubled to '0a','0b'.
    return _CertifiedSpace("S000209", _CIRCLE_TWO_ORIGINS_MEMBER, CarrierKind.UNCOUNTABLE)


# ===========================================================================
# Batch 7 — member helpers
# ===========================================================================

def _RAT_EXT_PLANE_MEMBER(p: Any) -> bool:
    r"""ℝ² ∪ {(x,y,1): x,y∈Q} — rational extension of the plane."""
    if isinstance(p, tuple) and len(p) == 3 and isinstance(p[0], (int, Fraction)) and isinstance(p[1], (int, Fraction)) and p[2] == 1:
        return True
    return _PLANE_MEMBER(p)


def _W_INF_W_STAR_MEMBER(p: Any) -> bool:
    r"""ω+1+ω* carrier: {(0,n):n∈ω} ∪ {'∞'} ∪ {(1,n):n∈ω}."""
    return p == "∞" or _ORDINAL_WW_MEMBER(p)


# ===========================================================================
# Batch 7 — certified spaces
# ===========================================================================

@_reg("S000058")
def _indiscrete_rational_extension() -> _CertifiedSpace:
    # Indiscrete rational extension of ℝ: carrier ℝ (rational part only representable).
    return _CertifiedSpace("S000058", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000059")
def _indiscrete_irrational_extension() -> _CertifiedSpace:
    # Indiscrete irrational extension of ℝ: carrier ℝ (rational part only representable).
    return _CertifiedSpace("S000059", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000061")
def _pointed_irrational_extension() -> _CertifiedSpace:
    # Pointed irrational extension of ℝ: carrier ℝ (rational part only representable).
    return _CertifiedSpace("S000061", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000064")
def _rational_extension_plane() -> _CertifiedSpace:
    # Rational extension of the plane: ℝ² ∪ {(x,y,1): x,y∈Q}.
    return _CertifiedSpace("S000064", _RAT_EXT_PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000113")
def _topologist_sine_curve() -> _CertifiedSpace:
    # Topologist's sine curve: subspace of ℝ² (carrier ℝ²).
    return _CertifiedSpace("S000113", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000114")
def _closed_topologist_sine() -> _CertifiedSpace:
    # Closed topologist's sine curve: compact subspace of ℝ².
    return _CertifiedSpace("S000114", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000115")
def _extended_topologist_sine() -> _CertifiedSpace:
    # Extended topologist's sine curve: compact subspace of ℝ².
    return _CertifiedSpace("S000115", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000120")
def _infinite_cage() -> _CertifiedSpace:
    # Infinite cage: connected subspace of ℝ².
    return _CertifiedSpace("S000120", _PLANE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000122")
def _gustin_sequence_space() -> _CertifiedSpace:
    # Gustin's sequence space: countable connected Hausdorff space (carrier ω).
    return _CertifiedSpace("S000122", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000123")
def _roy_lattice_space() -> _CertifiedSpace:
    # Roy's lattice space: carrier ℤ².
    return _CertifiedSpace("S000123", _INT_PLANE_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000124")
def _roy_lattice_subspace() -> _CertifiedSpace:
    # Roy's lattice subspace: carrier ℤ².
    return _CertifiedSpace("S000124", _INT_PLANE_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000125")
def _kk_fan() -> _CertifiedSpace:
    # Knaster–Kuratowski fan: subspace of [0,1]² (carrier Q²∩[0,1]²).
    return _CertifiedSpace("S000125", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000126")
def _punctured_kk_fan() -> _CertifiedSpace:
    # Punctured Knaster–Kuratowski fan: subspace of [0,1]².
    return _CertifiedSpace("S000126", _UNIT_SQUARE_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000130")
def _tangora_connected_space() -> _CertifiedSpace:
    # Tangora's connected space: countable connected Hausdorff space (carrier ω).
    return _CertifiedSpace("S000130", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000132")
def _duncan_space() -> _CertifiedSpace:
    # Duncan's space: countable Hausdorff not-connected space (carrier ω).
    return _CertifiedSpace("S000132", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000161")
def _van_douwen_space() -> _CertifiedSpace:
    # Van Douwen's anti-Hausdorff Fréchet space (carrier ω×ω ∪ {∞}).
    return _CertifiedSpace("S000161", _GRID_OR_INF_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000167")
def _right_open_ray_w1_wstar() -> _CertifiedSpace:
    # Right open-ray topology on ω+1+ω*: pairs (0|1,n) ∪ {'∞'}.
    return _CertifiedSpace("S000167", _W_INF_W_STAR_MEMBER, CarrierKind.COUNTABLE)


@_reg("S000171")
def _brian_example() -> _CertifiedSpace:
    # Brian's Example: Hausdorff, not connected, not compact (carrier ℝ).
    return _CertifiedSpace("S000171", _REAL_MEMBER, CarrierKind.UNCOUNTABLE)


@_reg("S000183")
def _kp_hart_modified_cocountable() -> _CertifiedSpace:
    # KP Hart's non-sequentially discrete modified cocountable topology (carrier ω).
    return _CertifiedSpace("S000183", _OMEGA_MEMBER, CarrierKind.COUNTABLE)


# ===========================================================================
# Public API
# ===========================================================================

def best_space(name_or_uid: str) -> Space:
    """Return the richest available Space for the given pi-Base space.

    For representable spaces, returns:

    - **FiniteSpace / AlexandroffSpace** for the 17 finite pi-Base spaces
    - **_MetricWithCerts** for metric spaces: computable point_separation
      (metric) *and* full pi-Base property certificates
    - **_CertifiedSpace** for other infinite spaces: computable membership
      *and* pi-Base property certificates
    - **DiscreteCountableSpace / CofiniteSpace / OrderTopologySpace /
      SorgenfreyLineSpace** for specific named topologies

    For all remaining pi-Base spaces, returns a :class:`PiBaseSpace` whose
    property certificates come from the pi-Base deductive closure.
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
