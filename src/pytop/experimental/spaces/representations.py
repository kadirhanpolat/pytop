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

from .core import CardinalValue, CarrierKind, Space, Verdict


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
        if prop in {"lindelof", "separable", "second_countable", "first_countable"}:
            return Verdict.true(
                reason="the cofinite topology on a countable set has a countable topology, "
                f"hence is {prop}"
            )
        if prop in {"tychonoff", "T5", "T6"}:
            return Verdict.false(
                reason=f"the cofinite topology on an infinite set is not regular, so not {prop}"
            )
        return None

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        # weight: the whole topology has ℵ₀ members (cofinite sets of N)
        # density: no finite dense subset (every nonempty open is cofinite, a finite set misses it)
        # character: ℵ₀ (local base at x needs ℵ₀ cofinite sets to cover all neighbourhoods)
        # cellularity: 1 (any two nonempty cofinite opens intersect)
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.aleph_0(),
            "cellularity": CardinalValue.of(1),
        }.get(invariant)


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
        if prop in {"lindelof", "separable", "second_countable", "first_countable"}:
            return Verdict.true(reason=f"the rationals with the order topology are {prop}")
        if prop in {"tychonoff", "T5", "T6"}:
            return Verdict.true(
                reason=f"the rationals are metrizable, hence {prop}"
            )
        return None

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        # Q with the order topology is second-countable (base = rational open intervals)
        # density: Q itself is countably infinite and dense; no finite dense subset exists
        # character: ℵ₀ (countable local base of intervals at each point)
        # cellularity: ℵ₀ (disjoint open intervals (q, q+1) for q ∈ Z)
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.aleph_0(),
            "cellularity": CardinalValue.aleph_0(),
        }.get(invariant)


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
        # Properties true for *every* metric space. Compactness/connectedness and
        # separability/second-countability/Lindelöf depend on the specific metric,
        # so they are left undecided here (honest).
        if prop in {"T0", "T1", "T2", "regular", "normal"}:
            return Verdict.true(reason=f"every metric space is {prop}")
        if prop == "first_countable":
            return Verdict.true(reason="every metric space is first countable (balls of radius 1/n)")
        if prop in {"tychonoff", "T5", "T6"}:
            return Verdict.true(
                reason=f"every metric space is {prop} (metric ⟹ perfectly normal)",
                witness=(
                    {"method": "distance_ratio",
                     "formula": "f(y) = min(1, d(x₀, y) / d(x₀, C))  "
                                "separates x₀ from any closed C not containing x₀"}
                    if prop == "tychonoff"
                    else None
                ),
            )
        return None

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        # Every metric space has character ℵ₀ (balls of radius 1/n form a local base).
        # Weight, density, cellularity depend on the specific metric — left unknown (honest).
        if invariant == "character":
            return CardinalValue.aleph_0()
        return None


class SorgenfreyLineSpace(Space):
    """The Sorgenfrey (lower-limit) line — the canonical separable, first-countable,
    Lindelöf, **not** second-countable, normal, totally disconnected example."""

    _CERTIFICATES = {
        "T0": True, "T1": True, "T2": True, "regular": True, "normal": True,
        "tychonoff": True, "T5": True, "T6": True,
        "compact": False, "connected": False,
        "lindelof": True, "separable": True, "first_countable": True,
        "second_countable": False,
    }

    def __init__(self, name: str = "Sorgenfrey line") -> None:
        self.name = name
        self.carrier_kind = CarrierKind.UNCOUNTABLE

    def contains(self, point: Any) -> bool:
        return isinstance(point, (int, float, Fraction))

    def certificate(self, prop: str) -> Verdict | None:
        if prop not in self._CERTIFICATES:
            return None
        value = self._CERTIFICATES[prop]
        reason = f"the Sorgenfrey line is {'' if value else 'not '}{prop}"
        return Verdict.true(reason=reason) if value else Verdict.false(reason=reason)

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        # weight: ℵ₀ (base = {[a,b) : a,b ∈ Q}, a countable family)
        # density: ℵ₀ (Q is dense; no finite dense subset)
        # character: ℵ₀ ({[x, x+1/n) : n ≥ 1} is a countable local base at x)
        # cellularity: ℵ₀ (separable ⟹ c(X) ≤ ℵ₀; {[n,n+1): n∈Z} witnesses ℵ₀)
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.aleph_0(),
            "cellularity": CardinalValue.aleph_0(),
        }.get(invariant)


class DiscreteCountableSpace(Space):
    """The discrete topology on a countably infinite set (metrizable, not compact)."""

    _CERTIFICATES = {
        "T0": True, "T1": True, "T2": True, "regular": True, "normal": True,
        "tychonoff": True, "T5": True, "T6": True,
        "compact": False, "connected": False,
        "lindelof": True, "separable": True, "first_countable": True,
        "second_countable": True,
    }

    def __init__(self, name: str = "discrete(N)") -> None:
        self.name = name
        self.carrier_kind = CarrierKind.COUNTABLE

    def contains(self, point: Any) -> bool:
        return isinstance(point, int) and point >= 0

    def certificate(self, prop: str) -> Verdict | None:
        if prop not in self._CERTIFICATES:
            return None
        value = self._CERTIFICATES[prop]
        reason = f"the countable discrete space is {'' if value else 'not '}{prop}"
        return Verdict.true(reason=reason) if value else Verdict.false(reason=reason)

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        # weight: ℵ₀ (base = singletons {{n} : n ∈ N})
        # density: ℵ₀ (no finite dense subset; N itself is the unique minimal dense set)
        # character: 1 ({{x}} is a local base at each x)
        # cellularity: ℵ₀ (singletons are pairwise disjoint nonempty opens)
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.of(1),
            "cellularity": CardinalValue.aleph_0(),
        }.get(invariant)


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


# --------------------------------------------------------------------------
# Helper shared by SubbaseSpace and InverseLimitSpace
# --------------------------------------------------------------------------

def _close_under_unions(basis: Iterable[frozenset]) -> set[frozenset]:
    opens: set[frozenset] = {frozenset()}
    opens.update(frozenset(b) for b in basis)
    changed = True
    while changed:
        changed = False
        current = list(opens)
        for i in range(len(current)):
            for j in range(i + 1, len(current)):
                union = current[i] | current[j]
                if union not in opens:
                    opens.add(union)
                    changed = True
    return opens


# --------------------------------------------------------------------------
# AlexandroffSpace
# --------------------------------------------------------------------------

class AlexandroffSpace(Space):
    """Alexandroff topology on a finite preorder: open sets = upper sets (upsets).

    Given a preorder ≤ on a finite carrier X, the open sets are exactly the
    upward-closed sets: U is open iff (x ∈ U and x ≤ y ⟹ y ∈ U). This
    establishes the classical bijection between finite preorders and finite
    Alexandroff topologies.

    The ``order`` argument lists pairs (x, y) meaning x ≤ y; reflexivity and
    transitivity are closed automatically.

    Example — the Sierpinski space via the order 0 ≤ 1::

        AlexandroffSpace("S", {0, 1}, [(0, 1)])
        # Opens: {}, {1}, {0, 1}
    """

    def __init__(
        self,
        name: str,
        carrier: Iterable[Any],
        order: Iterable[tuple[Any, Any]],
    ) -> None:
        pts = list(carrier)
        self.name = name
        self.carrier_kind = CarrierKind.FINITE
        self._carrier = frozenset(pts)

        # Build reflexive-transitive closure
        rel: set[tuple[Any, Any]] = set(order)
        for p in pts:
            rel.add((p, p))
        changed = True
        while changed:
            additions = {(a, c) for (a, b1) in rel for (b2, c) in rel if b1 == b2}
            changed = not (additions <= rel)
            rel |= additions
        self._order: frozenset[tuple[Any, Any]] = frozenset(rel)

        # Enumerate upper sets
        def _is_upset(sub: frozenset) -> bool:
            return all(b in sub for (a, b) in self._order if a in sub)

        all_subs = (
            frozenset(s)
            for r in range(len(pts) + 1)
            for s in combinations(pts, r)
        )
        self._opens = frozenset(s for s in all_subs if _is_upset(s))

    def contains(self, point: Any) -> bool:
        return point in self._carrier

    def points(self) -> tuple:
        return tuple(sorted(self._carrier, key=repr))

    def open_sets(self) -> frozenset:
        return self._opens

    @property
    def order(self) -> frozenset[tuple[Any, Any]]:
        """The reflexive-transitive closure of the defining preorder."""
        return self._order

    # -- structural certificates (use order, not open-set enumeration) ------

    def _is_antisymmetric(self) -> bool:
        """True iff the order relation is antisymmetric (i.e., is a partial order)."""
        for (x, y) in self._order:
            if x != y and (y, x) in self._order:
                return False
        return True

    def _antisymmetry_counterexample(self) -> tuple[Any, Any] | None:
        for (x, y) in self._order:
            if x != y and (y, x) in self._order:
                return (x, y)
        return None

    def _order_graph_connected(self) -> bool:
        """True iff the undirected graph of the strict order relation is connected."""
        pts = list(self._carrier)
        if len(pts) <= 1:
            return True
        parent: dict[Any, Any] = {p: p for p in pts}

        def find(p: Any) -> Any:
            while parent[p] != p:
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        for (x, y) in self._order:
            if x != y:
                rx, ry = find(x), find(y)
                if rx != ry:
                    parent[rx] = ry

        return len({find(p) for p in pts}) == 1

    def certificate(self, prop: str) -> Verdict | None:
        if prop == "T0":
            if self._is_antisymmetric():
                return Verdict.true(
                    reason="AlexandroffSpace: order is antisymmetric (partial order) ⟹ T0",
                    witness={"pairs_checked": len(self._order)},
                )
            ce = self._antisymmetry_counterexample()
            return Verdict.false(
                reason=f"AlexandroffSpace: order has x ≤ y and y ≤ x for x ≠ y "
                       f"({ce[0]!r} and {ce[1]!r}) — not antisymmetric, so not T0",
                counterexample=ce,
            )

        if prop == "connected":
            if self._order_graph_connected():
                return Verdict.true(
                    reason="AlexandroffSpace: the order-relation graph is connected",
                )
            pts = list(self._carrier)
            parent: dict[Any, Any] = {p: p for p in pts}

            def find(p: Any) -> Any:
                while parent[p] != p:
                    parent[p] = parent[parent[p]]
                    p = parent[p]
                return p

            for (x, y) in self._order:
                if x != y:
                    rx, ry = find(x), find(y)
                    if rx != ry:
                        parent[rx] = ry
            roots = {find(p) for p in pts}
            return Verdict.false(
                reason=f"AlexandroffSpace: order graph has {len(roots)} disconnected component(s)",
                counterexample=f"{len(roots)} components",
            )

        return None

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        n = len(self._carrier)
        if invariant == "character":
            # At each x, the principal upset ↑x is the unique minimal open neighbourhood.
            # A local base of size 1 suffices everywhere → χ(X) = 1.
            return CardinalValue.of(1)
        if invariant == "weight":
            if self._is_antisymmetric():
                # {↑x : x ∈ X} is a minimal base with |X| elements (all upsets distinct).
                return CardinalValue.of(n)
            # Non-T0: equivalent points share upsets; actual weight may be < n.
            return None  # let the module compute it
        return None


# --------------------------------------------------------------------------
# SubbaseSpace
# --------------------------------------------------------------------------

class SubbaseSpace(Space):
    """A finite topological space generated by a subbase.

    Given a finite carrier and a subbase S (any collection of subsets), the
    topology is generated by:

    1. Closing S ∪ {carrier} under finite intersections (to produce a base B).
    2. Closing B under arbitrary unions (to produce the full topology).

    Example — the standard topology on {0, 1, 2} generated by {{0,1}, {1,2}}::

        SubbaseSpace("X", {0, 1, 2}, [{0, 1}, {1, 2}])
        # Base: {{0,1}, {1,2}, {1}, {0,1,2}}
        # Topology adds arbitrary unions of base elements.
    """

    def __init__(
        self,
        name: str,
        carrier: Iterable[Any],
        subbase: Iterable[Iterable[Any]],
    ) -> None:
        pts = list(carrier)
        self.name = name
        self.carrier_kind = CarrierKind.FINITE
        self._carrier = frozenset(pts)

        # Step 1: close subbase under finite intersections
        base: set[frozenset] = {self._carrier}  # empty intersection = carrier
        base.update(frozenset(s) & self._carrier for s in subbase)
        changed = True
        while changed:
            changed = False
            current = list(base)
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    inter = current[i] & current[j]
                    if inter not in base:
                        base.add(inter)
                        changed = True

        # Step 2: close under arbitrary unions
        self._opens = frozenset(_close_under_unions(base))

    def contains(self, point: Any) -> bool:
        return point in self._carrier

    def points(self) -> tuple:
        return tuple(sorted(self._carrier, key=repr))

    def open_sets(self) -> frozenset:
        return self._opens


# --------------------------------------------------------------------------
# InverseLimitSpace
# --------------------------------------------------------------------------

class InverseLimitSpace(Space):
    """Inverse limit of a finite system of finite topological spaces.

    Given spaces [X₀, X₁, …, Xₙ] and bonding maps [f₁: X₁→X₀, …, fₙ: Xₙ→Xₙ₋₁],
    the inverse limit is::

        lim← = {(x₀, …, xₙ) ∈ X₀ × … × Xₙ : fₖ(xₖ) = xₖ₋₁  for all k}

    equipped with the subspace topology inherited from the product X₀ × … × Xₙ
    (product basis = products of opens, restricted to compatible tuples).

    Example — the two-point discrete space as lim← of two copies with identity::

        d2 = discrete_finite_space({0, 1})
        InverseLimitSpace("lim←", [d2, d2], [lambda x: x])
        # Limit = {(0,0), (1,1)} with the subspace topology.
    """

    def __init__(
        self,
        name: str,
        spaces: "Sequence[Space]",
        bonding_maps: "Sequence[Callable[[Any], Any]]",
    ) -> None:
        if len(bonding_maps) != len(spaces) - 1:
            raise ValueError(
                f"Need exactly len(spaces) - 1 = {len(spaces) - 1} bonding maps, "
                f"got {len(bonding_maps)}."
            )
        self.name = name
        self.carrier_kind = CarrierKind.FINITE

        # Enumerate compatible tuples
        from itertools import product as _product
        all_points = [list(s.points()) for s in spaces]
        carrier: list[tuple] = [
            combo
            for combo in _product(*all_points)
            if all(bonding_maps[k](combo[k + 1]) == combo[k] for k in range(len(bonding_maps)))
        ]
        self._carrier_set = frozenset(carrier)
        self._points_list = carrier

        # Product basis restricted to inverse limit
        all_opens = [list(s.open_sets()) for s in spaces]
        basis: set[frozenset] = set()
        for open_combo in _product(*all_opens):
            cell = frozenset(
                pt for pt in carrier
                if all(pt[k] in open_combo[k] for k in range(len(spaces)))
            )
            basis.add(cell)

        self._opens = frozenset(_close_under_unions(basis))

    def contains(self, point: Any) -> bool:
        return point in self._carrier_set

    def points(self) -> tuple:
        return tuple(self._points_list)

    def open_sets(self) -> frozenset:
        return self._opens


def finite_circle() -> AlexandroffSpace:
    """4-point minimal T0 model of S¹ (diamond poset).

    The diamond poset {0,1,2,3} with cover relations 0 < 2, 0 < 3, 1 < 2, 1 < 3
    is the minimal finite T0 space weakly homotopy equivalent to S¹ (McCord).
    Its order complex is K_{2,2} (the 4-cycle), giving π₁ = ℤ.
    """
    return AlexandroffSpace("S^1", {0, 1, 2, 3}, [(0, 2), (0, 3), (1, 2), (1, 3)])


def finite_sphere(n: int) -> AlexandroffSpace:
    """Minimal finite T0 model of S^n via iterated suspension.

    * S^0 — 2 discrete points (empty order).
    * S^1 — 4-point diamond (``finite_circle()``).
    * S^n — suspension of S^{n-1}: two new points new_bottom < every old
             point < new_top are added. Total: 2(n+1) points.

    By the McCord theorem, the geometric realization of the order complex is
    weakly homotopy equivalent to S^n, so π₁ = trivial for n ≥ 2 and ℤ for n=1.
    """
    if n < 0:
        raise ValueError(f"finite_sphere: n must be ≥ 0, got {n}")
    if n == 0:
        return AlexandroffSpace("S^0", {0, 1}, [])

    # S^1 = diamond
    carrier: set[int] = {0, 1, 2, 3}
    cover: list[tuple[int, int]] = [(0, 2), (0, 3), (1, 2), (1, 3)]

    for _ in range(2, n + 1):
        new_bottom = max(carrier) + 1
        new_top = max(carrier) + 2
        extended: list[tuple[int, int]] = list(cover)
        for p in sorted(carrier):
            extended.append((new_bottom, p))
            extended.append((p, new_top))
        carrier = carrier | {new_bottom, new_top}
        cover = extended

    return AlexandroffSpace(f"S^{n}", carrier, cover)


def finite_wedge_circles(k: int, *, name: str | None = None) -> AlexandroffSpace:
    """Minimal finite T0 model of S¹ ∨ ⋯ ∨ S¹  (k circles joined at a basepoint).

    Uses 1 + 3k points:

    * Basepoint 0 (shared by all circles).
    * For circle i (1 ≤ i ≤ k): second bottom vertex ``i`` and two top
      vertices ``k + 2i - 1``, ``k + 2i``.
    * Cover relations: 0 < top₁, 0 < top₂, bᵢ < top₁, bᵢ < top₂ per circle.

    By the McCord theorem the order complex is k 4-cycles sharing vertex 0,
    giving π₁ = F_k (free group of rank k).
    """
    if k < 0:
        raise ValueError(f"finite_wedge_circles: k must be ≥ 0, got {k}")
    if k == 0:
        return AlexandroffSpace(name or "pt", {0}, [])

    carrier: set[int] = {0}
    cover: list[tuple[int, int]] = []
    for i in range(1, k + 1):
        b = i
        t1 = k + 2 * i - 1
        t2 = k + 2 * i
        carrier |= {b, t1, t2}
        cover += [(0, t1), (0, t2), (b, t1), (b, t2)]

    return AlexandroffSpace(name or f"S^1_wedge_{k}", carrier, cover)


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
    "AlexandroffSpace",
    "CofiniteSpace",
    "DiscreteCountableSpace",
    "FiniteSpace",
    "InverseLimitSpace",
    "MetricTopologySpace",
    "OpaqueInfiniteSpace",
    "OrderTopologySpace",
    "SorgenfreyLineSpace",
    "SubbaseSpace",
    # Factory functions
    "finite_circle",
    "finite_sphere",
    "finite_wedge_circles",
    "discrete_finite_space",
    "rational_metric_space",
]
