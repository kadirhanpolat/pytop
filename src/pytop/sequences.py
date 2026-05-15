"""Finite sequence-convergence helpers for the topology book ecosystem.

The functions in this module give Chapter 16 a small exact finite bridge.
They deliberately do not claim a general symbolic decision procedure for
arbitrary infinite spaces.  For explicit finite topological spaces, convergence
is checked with the textbook open-neighborhood tail criterion.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable

from .result import Result


class SequenceError(ValueError):
    """Raised when a finite sequence request has malformed input."""


def sequence_converges_to(space: Any, sequence: Iterable[Any], point: Any) -> Result:
    """Check finite-prefix sequence convergence to ``point``.

    For an explicit finite topology this returns an exact result by checking
    whether every open neighborhood of ``point`` eventually contains all terms
    of the supplied finite sequence.  Since the input is finite, the witness is
    a tail index in the observed sequence; metadata records this finite-prefix
    nature explicitly.
    """

    try:
        data = _finite_space_data(space)
        target = _as_point(data, point)
        seq = tuple(sequence)
    except (TypeError, SequenceError):
        return Result.unknown(
            mode="symbolic",
            value="sequence_converges_to",
            justification=[
                "Sequence convergence currently has exact support only for explicit finite spaces."
            ],
            metadata={"operator": "sequence_converges_to", "point_repr": repr(point)},
        )

    if not seq:
        return Result.false(
            mode="exact",
            value=False,
            justification=["An empty finite sequence has no tail witnessing convergence."],
            metadata={
                "operator": "sequence_converges_to",
                "point": target,
                "sequence_length": 0,
                "finite_prefix_semantics": True,
            },
        )

    outside_terms = tuple(term for term in seq if term not in data["carrier"])
    if outside_terms:
        return Result.false(
            mode="exact",
            value=False,
            justification=["At least one sequence term is outside the carrier."],
            metadata={
                "operator": "sequence_converges_to",
                "point": target,
                "outside_terms": tuple(map(repr, outside_terms)),
                "finite_prefix_semantics": True,
            },
        )

    open_neighborhoods = _open_neighborhoods(data, target)
    witnesses: dict[frozenset[Any], int] = {}
    failures: list[frozenset[Any]] = []
    for neighborhood in open_neighborhoods:
        witness = _tail_witness(seq, neighborhood)
        if witness is None:
            failures.append(neighborhood)
        else:
            witnesses[neighborhood] = witness

    metadata = {
        "operator": "sequence_converges_to",
        "point": target,
        "sequence_length": len(seq),
        "open_neighborhoods": tuple(_sort_frozensets(open_neighborhoods)),
        "failed_open_neighborhoods": tuple(_sort_frozensets(failures)),
        "witness_by_open_neighborhood": tuple(
            (neighborhood, witnesses[neighborhood])
            for neighborhood in _sort_frozensets(witnesses)
        ),
        "finite_prefix_semantics": True,
    }

    if failures:
        return Result.false(
            mode="exact",
            value=False,
            justification=[
                "At least one open neighborhood of the point has no finite tail witness."
            ],
            metadata=metadata,
        )

    return Result.true(
        mode="exact",
        value=True,
        justification=[
            "Every open neighborhood of the point contains a tail of the supplied finite sequence."
        ],
        proof_outline=[
            "Enumerate open neighborhoods of the target point.",
            "For each neighborhood, find a tail index after which all listed terms lie in it.",
        ],
        metadata=metadata,
    )


def sequence_cluster_point(space: Any, sequence: Iterable[Any], point: Any) -> Result:
    """Check a finite-prefix cluster-point witness for ``point``.

    The finite helper uses the observable criterion that every open
    neighborhood of ``point`` meets the supplied sequence.  Metadata marks this
    as a finite-prefix diagnostic, not a full infinite-sequence theorem.
    """

    try:
        data = _finite_space_data(space)
        target = _as_point(data, point)
        seq = tuple(sequence)
    except (TypeError, SequenceError):
        return Result.unknown(
            mode="symbolic",
            value="sequence_cluster_point",
            justification=[
                "Sequence cluster-point diagnostics currently have exact support only for explicit finite spaces."
            ],
            metadata={"operator": "sequence_cluster_point", "point_repr": repr(point)},
        )

    outside_terms = tuple(term for term in seq if term not in data["carrier"])
    if outside_terms:
        return Result.false(
            mode="exact",
            value=False,
            justification=["At least one sequence term is outside the carrier."],
            metadata={
                "operator": "sequence_cluster_point",
                "point": target,
                "outside_terms": tuple(map(repr, outside_terms)),
                "finite_prefix_semantics": True,
            },
        )

    open_neighborhoods = _open_neighborhoods(data, target)
    failures = [neighborhood for neighborhood in open_neighborhoods if not any(term in neighborhood for term in seq)]
    metadata = {
        "operator": "sequence_cluster_point",
        "point": target,
        "sequence_length": len(seq),
        "open_neighborhoods": tuple(_sort_frozensets(open_neighborhoods)),
        "failed_open_neighborhoods": tuple(_sort_frozensets(failures)),
        "finite_prefix_semantics": True,
    }

    if failures:
        return Result.false(
            mode="exact",
            value=False,
            justification=["Some open neighborhood of the point is not visited by the supplied finite sequence."],
            metadata=metadata,
        )

    return Result.true(
        mode="exact",
        value=True,
        justification=["Every open neighborhood of the point is visited by the supplied finite sequence."],
        metadata=metadata,
    )


def sequential_closure(space: Any, subset: Iterable[Any]) -> Result:
    """Compute the exact sequential closure in an explicit finite space.

    In a finite topology, a sequence from ``A`` can converge to ``x`` exactly
    when ``A`` meets the minimal open neighborhood of ``x``.  This finite
    formula is used here as an exact classroom bridge.
    """

    try:
        data = _finite_space_data(space)
        sub = frozenset(subset)
    except TypeError:
        return Result.unknown(
            mode="symbolic",
            value="sequential_closure",
            justification=[
                "Sequential closure currently has exact support only for explicit finite spaces."
            ],
            metadata={"operator": "sequential_closure", "subset_repr": repr(subset)},
        )

    outside = tuple(x for x in sub if x not in data["carrier"])
    if outside:
        return Result.false(
            mode="exact",
            value=False,
            justification=["The subset contains at least one point outside the carrier."],
            metadata={
                "operator": "sequential_closure",
                "outside_points": tuple(map(repr, outside)),
            },
        )

    closure_points = []
    witnesses: dict[Any, frozenset[Any]] = {}
    for point in data["points"]:
        minimal = _minimal_open_neighborhood(data, point)
        if sub & minimal:
            closure_points.append(point)
            witnesses[point] = minimal

    value = frozenset(closure_points)
    return Result.true(
        mode="exact",
        value=value,
        justification=[
            "Computed using the finite criterion A meets the minimal open neighborhood of x."
        ],
        proof_outline=[
            "A sequence from A converges to x iff it is eventually in every open neighborhood of x.",
            "In a finite topology this is equivalent to being eventually in the intersection of all open neighborhoods of x.",
        ],
        metadata={
            "operator": "sequential_closure",
            "subset": sub,
            "witness_minimal_open_neighborhoods": tuple(
                (point, witnesses[point]) for point in _sort_points(witnesses)
            ),
        },
    )


def analyze_sequences(
    space: Any,
    *,
    sequence: Iterable[Any] | None = None,
    point: Any | None = None,
    subset: Iterable[Any] | None = None,
) -> Result:
    """Return a small structured summary for the sequence layer.

    The function is intentionally conservative: it delegates to exact finite
    helpers when enough data are supplied and otherwise returns an honest
    symbolic/unknown result.
    """

    if sequence is not None and point is not None:
        convergence = sequence_converges_to(space, sequence, point)
        cluster = sequence_cluster_point(space, sequence, point)
        return Result.true(
            mode="exact" if convergence.is_exact and cluster.is_exact else "mixed",
            value={"converges_to_point": convergence.value, "cluster_point": cluster.value},
            justification=["Sequence convergence and cluster diagnostics were evaluated for the supplied point."],
            metadata={
                "operator": "analyze_sequences",
                "convergence": convergence.to_dict(),
                "cluster_point": cluster.to_dict(),
            },
        )

    if subset is not None:
        closure = sequential_closure(space, subset)
        if closure.is_true:
            return Result.true(
                mode=closure.mode,
                value={"sequential_closure": closure.value},
                justification=["Sequential closure was computed for the supplied subset."],
                metadata={"operator": "analyze_sequences", "sequential_closure": closure.to_dict()},
            )
        return closure

    return Result.unknown(
        mode="symbolic",
        value="analyze_sequences",
        justification=["Provide either (sequence, point) or subset to run the finite sequence helpers."],
        metadata={"operator": "analyze_sequences"},
    )


# ---------------------------------------------------------------------------
# Finite topology helpers
# ---------------------------------------------------------------------------


def _finite_space_data(space: Any) -> dict[str, Any]:
    if not getattr(space, "is_finite", lambda: False)() or not hasattr(space, "topology"):
        raise TypeError("Expected an explicit finite topological space.")
    try:
        carrier = frozenset(space.carrier)
        opens = tuple(frozenset(open_set) for open_set in space.topology)
    except Exception as exc:  # pragma: no cover - defensive normalization
        raise TypeError("The carrier and topology must be finite iterable objects.") from exc
    if frozenset() not in opens or carrier not in opens:
        raise SequenceError("The topology must contain the empty set and the full carrier.")
    if any(not open_set.issubset(carrier) for open_set in opens):
        raise SequenceError("Every open set must be a subset of the carrier.")
    return {
        "carrier": carrier,
        "opens": tuple(_sort_frozensets(opens)),
        "points": tuple(_sort_points(carrier)),
    }


def _as_point(data: dict[str, Any], point: Any) -> Any:
    if point not in data["carrier"]:
        raise SequenceError(f"Point {point!r} is not in the carrier.")
    return point


def _open_neighborhoods(data: dict[str, Any], point: Any) -> tuple[frozenset[Any], ...]:
    return tuple(open_set for open_set in data["opens"] if point in open_set)


def _minimal_open_neighborhood(data: dict[str, Any], point: Any) -> frozenset[Any]:
    neighborhoods = _open_neighborhoods(data, point)
    if not neighborhoods:
        return frozenset()
    current = set(neighborhoods[0])
    for neighborhood in neighborhoods[1:]:
        current &= set(neighborhood)
    return frozenset(current)


def _tail_witness(sequence: tuple[Any, ...], subset: frozenset[Any]) -> int | None:
    for start in range(len(sequence)):
        if all(term in subset for term in sequence[start:]):
            return start
    return None


def _sort_points(points: Iterable[Any]) -> tuple[Any, ...]:
    return tuple(sorted(points, key=lambda value: (type(value).__name__, repr(value))))


def _sort_frozensets(sets: Iterable[frozenset[Any]]) -> tuple[frozenset[Any], ...]:
    return tuple(sorted(sets, key=lambda s: (len(s), tuple(repr(x) for x in _sort_points(s)))))
