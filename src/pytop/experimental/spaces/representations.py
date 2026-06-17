"""Concrete computable space representations behind the :class:`Space` protocol.

A finite representation (carrier + explicit topology) plus several
finitely-presented infinite ones (cofinite, order topology on the rationals,
metric topology, and an opaque infinite space) — enough to exercise generic
algorithms across the finite / infinite-with-certificate / undecidable cases.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from fractions import Fraction
from itertools import combinations
from typing import Any

from .core import CarrierKind, Space, Verdict


class FiniteSpace(Space):
    """A finite topological space given by its carrier and its open sets."""

    def __init__(self, name: str, carrier: Iterable[Any], opens: Iterable[Iterable[Any]]) -> None:
        self.name = name
        self.carrier_kind = CarrierKind.FINITE
        self._carrier = frozenset(carrier)
        self._opens = frozenset(frozenset(o) for o in opens)

    def contains(self, point: Any) -> bool:
        return point in self._carrier

    def points(self) -> Iterable[Any]:
        return tuple(sorted(self._carrier, key=repr))

    def open_sets(self) -> frozenset[frozenset[Any]]:
        return self._opens

    def point_separation(self, x: Any, y: Any) -> Verdict:
        # Finite: enumerating all opens is a complete decision procedure.
        opens_with_x = [o for o in self._opens if x in o]
        opens_with_y = [o for o in self._opens if y in o]
        for u in opens_with_x:
            for v in opens_with_y:
                if not (u & v):
                    return Verdict.true(
                        reason=f"disjoint opens separate {x!r} and {y!r}",
                        witness=(u, v),
                    )
        return Verdict.false(
            reason=f"no disjoint opens contain {x!r} and {y!r} respectively",
            counterexample=(x, y),
        )


class CofiniteSpace(Space):
    """The cofinite topology on an infinite carrier (T1 but not Hausdorff).

    The carrier is described by a membership predicate (default: nonnegative
    integers). Opens are the empty set and the cofinite sets.
    """

    def __init__(self, name: str = "cofinite(N)", member: Callable[[Any], bool] | None = None) -> None:
        self.name = name
        self.carrier_kind = CarrierKind.COUNTABLE
        self._member = member or (lambda p: isinstance(p, int) and p >= 0)

    def contains(self, point: Any) -> bool:
        return bool(self._member(point))

    def point_separation(self, x: Any, y: Any) -> Verdict:
        # Any two nonempty cofinite opens have cofinite (hence nonempty) intersection.
        return Verdict.false(
            reason="cofinite topology on an infinite set: any two nonempty opens intersect",
            counterexample=(x, y),
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop in {"T0", "T1"}:
            return Verdict.true(reason="cofinite topology is T1 (points are closed)")
        if prop == "T2":
            return Verdict.false(
                reason="cofinite topology on an infinite set is not Hausdorff",
                counterexample="any two distinct points",
            )
        if prop == "compact":
            return Verdict.true(
                reason="cofinite topology is compact (each nonempty open omits only finitely many points)"
            )
        if prop == "connected":
            return Verdict.true(
                reason="cofinite topology on an infinite set is hyperconnected, hence connected"
            )
        if prop in {"regular", "normal"}:
            return Verdict.false(
                reason=f"cofinite topology on an infinite set is not {prop} "
                "(disjoint nonempty closed sets cannot be separated by disjoint opens)",
                counterexample="two disjoint finite closed sets",
            )
        return None


class OrderTopologySpace(Space):
    """The order topology on the rationals (Hausdorff, not discrete)."""

    def __init__(self, name: str = "order topology(Q)") -> None:
        self.name = name
        self.carrier_kind = CarrierKind.COUNTABLE

    def contains(self, point: Any) -> bool:
        return isinstance(point, (int, Fraction))

    def point_separation(self, x: Any, y: Any) -> Verdict:
        lo, hi = (x, y) if x < y else (y, x)
        mid = Fraction(lo + hi, 2)
        return Verdict.true(
            reason=f"order rays split at {mid}",
            witness=(("ray_below", mid), ("ray_above", mid)),
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop in {"T0", "T1", "T2", "regular", "normal"}:
            return Verdict.true(
                reason=f"order topology on Q is {prop} (linearly ordered spaces are monotonically normal)"
            )
        if prop == "compact":
            return Verdict.false(
                reason="the rationals are not compact",
                counterexample="the cover by rays around an irrational cut has no finite subcover",
            )
        if prop == "connected":
            return Verdict.false(
                reason="the rationals are totally disconnected",
                counterexample="a clopen split of Q at an irrational cut",
            )
        return None


class MetricTopologySpace(Space):
    """A metric topology from an exact distance function (always Hausdorff)."""

    def __init__(
        self,
        name: str,
        distance: Callable[[Any, Any], Fraction],
        member: Callable[[Any], bool],
        carrier_kind: CarrierKind = CarrierKind.COUNTABLE,
    ) -> None:
        self.name = name
        self.carrier_kind = carrier_kind
        self._distance = distance
        self._member = member

    def contains(self, point: Any) -> bool:
        return bool(self._member(point))

    def point_separation(self, x: Any, y: Any) -> Verdict:
        radius = Fraction(self._distance(x, y)) / 2
        return Verdict.true(
            reason=f"open balls of radius {radius} are disjoint",
            witness=((x, radius), (y, radius)),
        )

    def certificate(self, prop: str) -> Verdict | None:
        # Properties true for *every* metric space. Compactness/connectedness
        # depend on the specific metric, so they are left undecided here (honest).
        if prop in {"T0", "T1", "T2", "regular", "normal"}:
            return Verdict.true(reason=f"every metric space is {prop}")
        return None


class OpaqueInfiniteSpace(Space):
    """An infinite space with no separation certificate — the undecidable case.

    Demonstrates honest reporting: generic predicates cannot decide separation
    for it because it exposes neither enumeration nor a construction theorem.
    """

    def __init__(self, name: str, member: Callable[[Any], bool]) -> None:
        self.name = name
        self.carrier_kind = CarrierKind.COUNTABLE
        self._member = member

    def contains(self, point: Any) -> bool:
        return bool(self._member(point))


def rational_metric_space(name: str = "metric(Q, |x-y|)") -> MetricTopologySpace:
    """The standard metric topology on the rationals."""

    return MetricTopologySpace(
        name,
        distance=lambda a, b: abs(Fraction(a) - Fraction(b)),
        member=lambda p: isinstance(p, (int, Fraction)),
    )


def discrete_finite_space(carrier: Iterable[Any], name: str = "discrete") -> FiniteSpace:
    """The discrete topology on a finite carrier (every subset open)."""

    points = list(carrier)
    from itertools import chain
    subsets = chain.from_iterable(combinations(points, r) for r in range(len(points) + 1))
    return FiniteSpace(name, points, [frozenset(s) for s in subsets])


__all__ = [
    "FiniteSpace",
    "CofiniteSpace",
    "OrderTopologySpace",
    "MetricTopologySpace",
    "OpaqueInfiniteSpace",
    "rational_metric_space",
    "discrete_finite_space",
]
