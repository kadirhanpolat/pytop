"""Generic, witness-producing predicates over the :class:`Space` protocol.

These algorithms target the protocol, not any concrete representation, and are
honest about decidability:

* **finite / enumerable** spaces are decided by computation from the topology
  (with a witness or a counterexample);
* **infinite** spaces are decided when the representation supplies a
  construction-level ``certificate`` (e.g. metric ⟹ normal);
* otherwise the verdict is reported as **undecidable** — never guessed.
"""

from __future__ import annotations

from collections.abc import Callable
from itertools import combinations
from typing import Any

from .core import Decidability, NotEnumerableError, Space, Verdict

FiniteTopology = tuple[frozenset, set, set]


def _finite_topology(space: Space) -> FiniteTopology:
    carrier = frozenset(space.points())
    opens = {frozenset(o) for o in space.open_sets()}
    closed = {carrier - o for o in opens}
    return carrier, opens, closed


def _via_certificate(space: Space, prop: str) -> Verdict:
    certificate = space.certificate(prop)
    if certificate is not None:
        return certificate
    return Verdict.undecidable(
        f"{space.name!r}: infinite space without a {prop!r} certificate; "
        "cannot enumerate the topology."
    )


def _decide(space: Space, prop: str, finite_rule: Callable[[FiniteTopology], Verdict]) -> Verdict:
    if space.is_finite():
        try:
            topology = _finite_topology(space)
        except NotEnumerableError:
            return Verdict.undecidable(f"{space.name!r}: topology not enumerable.")
        return finite_rule(topology)
    return _via_certificate(space, prop)


# --------------------------------------------------------------------------
# Separation axioms
# --------------------------------------------------------------------------


def is_hausdorff(space: Space) -> Verdict:
    """Decide whether ``space`` is Hausdorff (T2), with witness or counterexample."""

    if space.is_finite():
        return _decide_finite_hausdorff(space)
    return _via_certificate(space, "T2")


def _decide_finite_hausdorff(space: Space) -> Verdict:
    try:
        points = list(space.points())
    except NotEnumerableError:
        return Verdict.undecidable(f"{space.name!r}: carrier not enumerable.")
    checked = 0
    for x, y in combinations(points, 2):
        separation = space.point_separation(x, y)
        if separation.value is False:
            return Verdict.false(
                reason=f"{space.name!r}: {separation.reason}",
                counterexample=separation.counterexample or (x, y),
            )
        if separation.value is None:
            return Verdict(
                None,
                Decidability.UNDECIDABLE,
                reason=f"{space.name!r}: point separation undecidable for {(x, y)!r}",
            )
        checked += 1
    return Verdict.true(
        reason=f"{space.name!r}: all {checked} point pair(s) separated by disjoint opens",
        witness={"pairs_separated": checked},
    )


def is_t0(space: Space) -> Verdict:
    """Decide the Kolmogorov axiom T0 (distinct points are topologically distinguishable)."""

    def rule(topology: FiniteTopology) -> Verdict:
        carrier, opens, _ = topology
        for x, y in combinations(sorted(carrier, key=repr), 2):
            if not any((x in o) != (y in o) for o in opens):
                return Verdict.false(
                    reason=f"points {x!r} and {y!r} lie in exactly the same open sets",
                    counterexample=(x, y),
                )
        return Verdict.true(reason="all distinct points are topologically distinguishable")

    return _decide(space, "T0", rule)


def is_t1(space: Space) -> Verdict:
    """Decide the T1 axiom (every singleton is closed)."""

    def rule(topology: FiniteTopology) -> Verdict:
        carrier, _, closed = topology
        for x in sorted(carrier, key=repr):
            if frozenset({x}) not in closed:
                return Verdict.false(
                    reason=f"singleton {{{x!r}}} is not closed",
                    counterexample=x,
                )
        return Verdict.true(reason="every singleton is closed")

    return _decide(space, "T1", rule)


def is_regular(space: Space) -> Verdict:
    """Decide regularity (a point and a disjoint closed set have disjoint open nbhds)."""

    def rule(topology: FiniteTopology) -> Verdict:
        carrier, opens, closed = topology
        for x in carrier:
            for f in closed:
                if x in f:
                    continue
                if not _separated_by_opens(opens, {x}, f):
                    return Verdict.false(
                        reason=f"point {x!r} and closed set {set(f)!r} cannot be separated",
                        counterexample=(x, f),
                    )
        return Verdict.true(reason="every point/closed-set pair is separated")

    return _decide(space, "regular", rule)


def is_normal(space: Space) -> Verdict:
    """Decide normality (disjoint closed sets have disjoint open neighbourhoods)."""

    def rule(topology: FiniteTopology) -> Verdict:
        _, opens, closed = topology
        closed_list = sorted(closed, key=lambda s: (len(s), sorted(map(repr, s))))
        for f, g in combinations(closed_list, 2):
            if f & g:
                continue
            if not _separated_by_opens(opens, f, g):
                return Verdict.false(
                    reason=f"disjoint closed sets {set(f)!r} and {set(g)!r} cannot be separated",
                    counterexample=(f, g),
                )
        return Verdict.true(reason="every pair of disjoint closed sets is separated")

    return _decide(space, "normal", rule)


def _separated_by_opens(opens: set, a: Any, b: Any) -> bool:
    a, b = frozenset(a), frozenset(b)
    supersets_a = [o for o in opens if a <= o]
    supersets_b = [o for o in opens if b <= o]
    return any(not (u & v) for u in supersets_a for v in supersets_b)


# --------------------------------------------------------------------------
# Compactness and connectedness
# --------------------------------------------------------------------------


def is_compact(space: Space) -> Verdict:
    """Decide compactness. Every finite space is compact."""

    def rule(_: FiniteTopology) -> Verdict:
        return Verdict.true(reason="every finite topological space is compact")

    return _decide(space, "compact", rule)


def is_connected(space: Space) -> Verdict:
    """Decide connectedness (no nontrivial clopen set), with a disconnection witness."""

    def rule(topology: FiniteTopology) -> Verdict:
        carrier, opens, closed = topology
        for s in opens & closed:
            if s and s != carrier:
                return Verdict.false(
                    reason=f"{set(s)!r} is a nontrivial clopen set (a disconnection)",
                    counterexample=(s, carrier - s),
                )
        return Verdict.true(reason="the only clopen sets are the empty set and the whole space")

    return _decide(space, "connected", rule)


__all__ = [
    "is_hausdorff",
    "is_t0",
    "is_t1",
    "is_regular",
    "is_normal",
    "is_compact",
    "is_connected",
]
