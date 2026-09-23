"""Deciding homeomorphism where it is decidable, and certifying it where it is not.

Homeomorphism is undecidable in general -- for 4-manifolds outright, and beyond
reach for most of what pytop can build. This module does the two honest things
instead of pretending otherwise.

**Decide, on finite spaces.** For a finite topological space the topology is
equivalent to its specialization preorder (Alexandroff), and a bijection is a
homeomorphism exactly when it is an isomorphism of those preorders. That makes
homeomorphism of finite spaces *decidable*, and :func:`finite_homeomorphic`
decides it, returning the explicit bijection as a witness.

**Certify distinctness, on anything.** :func:`homeomorphism_obstruction` compares
computable invariants of two objects. Differing invariants **prove** the objects
are not homeomorphic, and the differing pair is returned as the certificate.
Agreeing invariants prove nothing, and the verdict says so: this module never
reports "homeomorphic" without a bijection to show for it.

The existing :func:`pytop.finite_homeomorphism_result` is a descriptive-layer
stub that answers ``status='unknown'`` for every input, including two genuinely
homeomorphic spaces. This module is the computational counterpart.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

__all__ = [
    "HomeoVerdict",
    "HomeomorphismResult",
    "InvariantObstruction",
    "finite_homeomorphic",
    "homeomorphism_obstruction",
    "preorder_isomorphism",
    "specialization_preorder",
]

Point = Hashable
Relation = frozenset[tuple[Point, Point]]


class HomeoVerdict(Enum):
    """How firmly the question was answered.

    There is deliberately no verdict meaning "probably homeomorphic": a positive
    answer requires a bijection, and without one the honest report is
    :attr:`INCONCLUSIVE`.
    """

    HOMEOMORPHIC = "homeomorphic"
    DISTINCT = "distinct"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True)
class InvariantObstruction:
    """An invariant on which two objects differ -- a proof they are not homeomorphic."""

    invariant: str
    left: object
    right: object

    def __str__(self) -> str:
        return f"{self.invariant}: {self.left!r} vs {self.right!r}"


@dataclass(frozen=True)
class HomeomorphismResult:
    """The verdict, plus whatever establishes it."""

    verdict: HomeoVerdict
    witness: Mapping[Point, Point] | None
    obstruction: InvariantObstruction | None
    reason: str

    def __bool__(self) -> bool:
        """True only for a proven homeomorphism."""
        return self.verdict is HomeoVerdict.HOMEOMORPHIC


# ---------------------------------------------------------------------------
# Finite spaces: decidable
# ---------------------------------------------------------------------------


def specialization_preorder(
    carrier: Iterable[Point], opens: Iterable[Iterable[Point]]
) -> Relation:
    """``x <= y`` iff every open set containing ``x`` also contains ``y``.

    For a finite space this preorder carries exactly as much information as the
    topology, which is why homeomorphism reduces to preorder isomorphism.
    """
    points = tuple(carrier)
    open_sets = [frozenset(o) for o in opens]
    return frozenset(
        (x, y)
        for x in points
        for y in points
        if all(y in o for o in open_sets if x in o)
    )


def _signature(point: Point, relation: Relation, depth: int) -> tuple:
    """A colour refining candidate matches, cheap enough to run per node."""
    up = {b for a, b in relation if a == point}
    down = {a for a, b in relation if b == point}
    base: tuple = (len(up), len(down))
    for _ in range(depth):
        base = (
            base,
            tuple(sorted(len({b for a, b in relation if a == u}) for u in up)),
            tuple(sorted(len({a for a, b in relation if b == d}) for d in down)),
        )
    return base


def preorder_isomorphism(
    left_carrier: Iterable[Point],
    left_relation: Iterable[tuple[Point, Point]],
    right_carrier: Iterable[Point],
    right_relation: Iterable[tuple[Point, Point]],
) -> dict[Point, Point] | None:
    """An isomorphism of preorders, or ``None`` if none exists.

    Backtracking refined by local signatures rather than enumerating all ``n!``
    bijections: candidates are grouped by up/down-set profile first, so most
    non-isomorphic pairs are rejected without any search.
    """
    left = tuple(left_carrier)
    right = tuple(right_carrier)
    if len(left) != len(right):
        return None
    lrel = frozenset(left_relation)
    rrel = frozenset(right_relation)
    if len(lrel) != len(rrel):
        return None

    lsig = {p: _signature(p, lrel, 2) for p in left}
    rsig = {p: _signature(p, rrel, 2) for p in right}
    if sorted(map(repr, lsig.values())) != sorted(map(repr, rsig.values())):
        return None

    # Order the search by the most constrained point first.
    candidates = {p: [q for q in right if rsig[q] == lsig[p]] for p in left}
    if any(not c for c in candidates.values()):
        return None
    order = sorted(left, key=lambda p: len(candidates[p]))

    mapping: dict[Point, Point] = {}
    used: set[Point] = set()

    def consistent(p: Point, q: Point) -> bool:
        for a, b in mapping.items():
            if ((p, a) in lrel) != ((q, b) in rrel):
                return False
            if ((a, p) in lrel) != ((b, q) in rrel):
                return False
        return ((p, p) in lrel) == ((q, q) in rrel)

    def search(i: int) -> bool:
        if i == len(order):
            return True
        p = order[i]
        for q in candidates[p]:
            if q in used or not consistent(p, q):
                continue
            mapping[p] = q
            used.add(q)
            if search(i + 1):
                return True
            del mapping[p]
            used.discard(q)
        return False

    return dict(mapping) if search(0) else None


def _resolve(space: object, names: tuple[str, ...]) -> Any:
    """First present attribute among ``names``, called if it is a method.

    ``FiniteSpace`` exposes ``points()`` and ``open_sets()`` as methods while
    other finite-space shapes in the codebase use plain attributes, so this
    accepts either rather than assuming one.
    """
    for name in names:
        value = getattr(space, name, None)
        if value is None:
            continue
        return value() if callable(value) else value
    return None


def _space_data(space: object) -> tuple[tuple[Point, ...], list[frozenset[Point]]]:
    """Pull carrier and open sets out of the finite-space shapes pytop uses."""
    points = _resolve(space, ("points", "carrier"))
    opens = _resolve(space, ("open_sets", "opens", "topology"))
    if points is None or opens is None:
        raise TypeError(
            f"expected a finite space exposing points/carrier and open_sets, got "
            f"{type(space).__name__}. Pass an experimental.spaces.FiniteSpace, or "
            f"any object with those attributes (methods or plain values both work)."
        )
    return tuple(points), [frozenset(o) for o in opens]


def finite_homeomorphic(left: object, right: object) -> HomeomorphismResult:
    """Decide whether two **finite** spaces are homeomorphic.

    This is a decision, not a heuristic: for finite spaces the topology and the
    specialization preorder determine each other, so a preorder isomorphism *is*
    a homeomorphism and its absence *is* a proof of distinctness. A positive
    result carries the bijection.

    Examples
    --------
    >>> from pytop.experimental.spaces import FiniteSpace
    >>> s = FiniteSpace("sierpinski", (0, 1), [(), (0,), (0, 1)])
    >>> t = FiniteSpace("relabelled", ("a", "b"), [(), ("b",), ("a", "b")])
    >>> bool(finite_homeomorphic(s, t))
    True
    >>> d = FiniteSpace("discrete", (0, 1), [(), (0,), (1,), (0, 1)])
    >>> finite_homeomorphic(s, d).verdict.value
    'distinct'
    """
    lpoints, lopens = _space_data(left)
    rpoints, ropens = _space_data(right)

    for name, a, b in (
        ("cardinality", len(lpoints), len(rpoints)),
        ("open set count", len(lopens), len(ropens)),
        (
            "open set size profile",
            tuple(sorted(len(o) for o in lopens)),
            tuple(sorted(len(o) for o in ropens)),
        ),
    ):
        if a != b:
            return HomeomorphismResult(
                verdict=HomeoVerdict.DISTINCT,
                witness=None,
                obstruction=InvariantObstruction(name, a, b),
                reason=(
                    f"{name} differs ({a} vs {b}); a homeomorphism preserves it, "
                    f"so none exists."
                ),
            )

    lrel = specialization_preorder(lpoints, lopens)
    rrel = specialization_preorder(rpoints, ropens)
    mapping = preorder_isomorphism(lpoints, lrel, rpoints, rrel)
    if mapping is None:
        return HomeomorphismResult(
            verdict=HomeoVerdict.DISTINCT,
            witness=None,
            obstruction=InvariantObstruction(
                "specialization preorder", "no isomorphism", "no isomorphism"
            ),
            reason=(
                "the specialization preorders are not isomorphic. For finite "
                "spaces the topology and this preorder determine each other, so "
                "this rules out every bijection, not just the ones tried."
            ),
        )
    return HomeomorphismResult(
        verdict=HomeoVerdict.HOMEOMORPHIC,
        witness=mapping,
        obstruction=None,
        reason=(
            "the specialization preorders are isomorphic, and for finite spaces "
            "such an isomorphism is a homeomorphism."
        ),
    )


# ---------------------------------------------------------------------------
# Anything else: certify distinctness only
# ---------------------------------------------------------------------------


def homeomorphism_obstruction(
    left_invariants: Mapping[str, object],
    right_invariants: Mapping[str, object],
    *,
    order: Sequence[str] | None = None,
) -> HomeomorphismResult:
    """Look for an invariant proving two objects are **not** homeomorphic.

    Only invariants present on both sides are compared; a name missing from
    either is skipped rather than treated as a difference, since absence means
    "not computed", not "different".

    A difference is a proof. Agreement is not: the result is then
    :attr:`HomeoVerdict.INCONCLUSIVE`, never "homeomorphic". Homeomorphism is
    undecidable in general, and no finite list of matching invariants changes
    that.

    Examples
    --------
    >>> a = {"betti": (1, 2, 1), "euler": 0}
    >>> b = {"betti": (1, 0, 1), "euler": 2}
    >>> homeomorphism_obstruction(a, b).verdict.value
    'distinct'
    >>> homeomorphism_obstruction(a, dict(a)).verdict.value
    'inconclusive'
    """
    shared = [k for k in (order or sorted(left_invariants)) if k in left_invariants
              and k in right_invariants]
    for name in shared:
        a, b = left_invariants[name], right_invariants[name]
        if a != b:
            return HomeomorphismResult(
                verdict=HomeoVerdict.DISTINCT,
                witness=None,
                obstruction=InvariantObstruction(name, a, b),
                reason=(
                    f"{name} differs ({a!r} vs {b!r}); it is a homeomorphism "
                    f"invariant, so no homeomorphism exists."
                ),
            )
    if not shared:
        return HomeomorphismResult(
            verdict=HomeoVerdict.INCONCLUSIVE,
            witness=None,
            obstruction=None,
            reason=(
                "no invariant was computed on both sides, so nothing was "
                "compared. Supply at least one invariant present in both."
            ),
        )
    return HomeomorphismResult(
        verdict=HomeoVerdict.INCONCLUSIVE,
        witness=None,
        obstruction=None,
        reason=(
            f"{len(shared)} invariant(s) agree ({', '.join(shared)}), which rules "
            f"nothing out and proves nothing: agreeing invariants never establish "
            f"a homeomorphism. Use finite_homeomorphic() where the objects are "
            f"finite spaces, which is the case this library can decide."
        ),
    )
