"""Exact finite topological operator engine.

This module is the first concrete implementation pass for the Chapter 05
operator API surface listed in the v1.0.176 synchronization layer.  It is
deliberately finite and explicit: the caller supplies a carrier and a candidate
topology as iterable families of subsets.

The implementation is original to this package.  It does not copy examples,
exercises, or wording from any external chapter package.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable


class FiniteOperatorEngineError(ValueError):
    """Raised when the finite operator engine receives malformed data."""


@dataclass(frozen=True)
class TopologyValidation:
    carrier: frozenset[Any]
    opens: tuple[frozenset[Any], ...]
    is_topology: bool
    missing_required: tuple[frozenset[Any], ...]
    non_subset_members: tuple[frozenset[Any], ...]
    union_failures: tuple[tuple[frozenset[Any], frozenset[Any], frozenset[Any]], ...]
    intersection_failures: tuple[tuple[frozenset[Any], frozenset[Any], frozenset[Any]], ...]

    @property
    def failure_count(self) -> int:
        return (
            len(self.missing_required)
            + len(self.non_subset_members)
            + len(self.union_failures)
            + len(self.intersection_failures)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "carrier": self.carrier,
            "opens": self.opens,
            "is_topology": self.is_topology,
            "missing_required": self.missing_required,
            "non_subset_members": self.non_subset_members,
            "union_failures": self.union_failures,
            "intersection_failures": self.intersection_failures,
            "failure_count": self.failure_count,
        }


@dataclass(frozen=True)
class FiniteOperatorTable:
    carrier: frozenset[Any]
    subset: frozenset[Any]
    closure: frozenset[Any]
    interior: frozenset[Any]
    exterior: frozenset[Any]
    boundary: frozenset[Any]
    derived_set: frozenset[Any]
    closed_sets: tuple[frozenset[Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "carrier": self.carrier,
            "subset": self.subset,
            "closure": self.closure,
            "interior": self.interior,
            "exterior": self.exterior,
            "boundary": self.boundary,
            "derived_set": self.derived_set,
            "closed_sets": self.closed_sets,
        }


def validate_topology_candidate(carrier: Iterable[Any], topology: Iterable[Iterable[Any]]) -> TopologyValidation:
    carrier_set = _normalize_carrier(carrier)
    opens = _normalize_family(topology, carrier_set, allow_external=True)
    open_set = set(opens)

    non_subset_members = tuple(member for member in opens if not member.issubset(carrier_set))
    missing_required = tuple(member for member in (frozenset(), carrier_set) if member not in open_set)

    union_failures: list[tuple[frozenset[Any], frozenset[Any], frozenset[Any]]] = []
    intersection_failures: list[tuple[frozenset[Any], frozenset[Any], frozenset[Any]]] = []
    for left in opens:
        for right in opens:
            union = left | right
            intersection = left & right
            if union not in open_set:
                union_failures.append((left, right, union))
            if intersection not in open_set:
                intersection_failures.append((left, right, intersection))

    is_valid = not (missing_required or non_subset_members or union_failures or intersection_failures)
    return TopologyValidation(
        carrier=carrier_set,
        opens=_sort_family(opens),
        is_topology=is_valid,
        missing_required=_sort_family(missing_required),
        non_subset_members=_sort_family(non_subset_members),
        union_failures=tuple(union_failures),
        intersection_failures=tuple(intersection_failures),
    )


def is_topology(carrier: Iterable[Any], topology: Iterable[Iterable[Any]]) -> bool:
    return validate_topology_candidate(carrier, topology).is_topology


def closed_sets_from_topology(carrier: Iterable[Any], topology: Iterable[Iterable[Any]]) -> tuple[frozenset[Any], ...]:
    carrier_set, opens = _valid_topology_data(carrier, topology)
    return _sort_family(carrier_set - open_set for open_set in opens)


def closure(carrier: Iterable[Any], topology: Iterable[Iterable[Any]], subset: Iterable[Any]) -> frozenset[Any]:
    carrier_set, opens = _valid_topology_data(carrier, topology)
    subset_set = _normalize_subset(subset, carrier_set)
    closed_sets = closed_sets_from_topology(carrier_set, opens)
    candidates = [closed for closed in closed_sets if subset_set.issubset(closed)]
    if not candidates:
        return carrier_set
    result = set(carrier_set)
    for closed in candidates:
        result &= set(closed)
    return frozenset(result)


def interior(carrier: Iterable[Any], topology: Iterable[Iterable[Any]], subset: Iterable[Any]) -> frozenset[Any]:
    carrier_set, opens = _valid_topology_data(carrier, topology)
    subset_set = _normalize_subset(subset, carrier_set)
    result: set[Any] = set()
    for open_set in opens:
        if open_set.issubset(subset_set):
            result |= set(open_set)
    return frozenset(result)


def exterior(carrier: Iterable[Any], topology: Iterable[Iterable[Any]], subset: Iterable[Any]) -> frozenset[Any]:
    carrier_set, _ = _valid_topology_data(carrier, topology)
    subset_set = _normalize_subset(subset, carrier_set)
    return interior(carrier_set, topology, carrier_set - subset_set)


def boundary(carrier: Iterable[Any], topology: Iterable[Iterable[Any]], subset: Iterable[Any]) -> frozenset[Any]:
    subset_set = _normalize_subset(subset, _normalize_carrier(carrier))
    return closure(carrier, topology, subset_set) - interior(carrier, topology, subset_set)


def derived_set(carrier: Iterable[Any], topology: Iterable[Iterable[Any]], subset: Iterable[Any]) -> frozenset[Any]:
    carrier_set, opens = _valid_topology_data(carrier, topology)
    subset_set = _normalize_subset(subset, carrier_set)
    derived: set[Any] = set()
    for point in carrier_set:
        neighborhoods = [open_set for open_set in opens if point in open_set]
        deleted_subset = subset_set - {point}
        if all(open_set & deleted_subset for open_set in neighborhoods):
            derived.add(point)
    return frozenset(derived)


def neighborhood_system(carrier: Iterable[Any], topology: Iterable[Iterable[Any]], point: Any) -> tuple[frozenset[Any], ...]:
    carrier_set, opens = _valid_topology_data(carrier, topology)
    if point not in carrier_set:
        raise FiniteOperatorEngineError(f"point {point!r} is not in the carrier")
    subsets = _powerset(carrier_set)
    neighborhoods = []
    for candidate in subsets:
        if any(point in open_set and open_set.issubset(candidate) for open_set in opens):
            neighborhoods.append(candidate)
    return _sort_family(neighborhoods)


def relative_topology(
    carrier: Iterable[Any],
    topology: Iterable[Iterable[Any]],
    subspace: Iterable[Any],
) -> tuple[frozenset[Any], ...]:
    carrier_set, opens = _valid_topology_data(carrier, topology)
    subspace_set = _normalize_subset(subspace, carrier_set)
    return _sort_family(open_set & subspace_set for open_set in opens)


def kuratowski_closure_check(carrier: Iterable[Any], topology: Iterable[Iterable[Any]]) -> dict[str, bool]:
    carrier_set, _ = _valid_topology_data(carrier, topology)
    all_subsets = _powerset(carrier_set)

    empty_ok = closure(carrier_set, topology, frozenset()) == frozenset()
    extensive_ok = all(subset.issubset(closure(carrier_set, topology, subset)) for subset in all_subsets)
    idempotent_ok = all(
        closure(carrier_set, topology, closure(carrier_set, topology, subset))
        == closure(carrier_set, topology, subset)
        for subset in all_subsets
    )
    union_ok = all(
        closure(carrier_set, topology, left | right)
        == (closure(carrier_set, topology, left) | closure(carrier_set, topology, right))
        for left in all_subsets
        for right in all_subsets
    )
    return {
        "empty": empty_ok,
        "extensive": extensive_ok,
        "idempotent": idempotent_ok,
        "finite_union": union_ok,
        "all": empty_ok and extensive_ok and idempotent_ok and union_ok,
    }


def operator_table(
    carrier: Iterable[Any],
    topology: Iterable[Iterable[Any]],
    subset: Iterable[Any],
) -> FiniteOperatorTable:
    carrier_set, _ = _valid_topology_data(carrier, topology)
    subset_set = _normalize_subset(subset, carrier_set)
    return FiniteOperatorTable(
        carrier=carrier_set,
        subset=subset_set,
        closure=closure(carrier_set, topology, subset_set),
        interior=interior(carrier_set, topology, subset_set),
        exterior=exterior(carrier_set, topology, subset_set),
        boundary=boundary(carrier_set, topology, subset_set),
        derived_set=derived_set(carrier_set, topology, subset_set),
        closed_sets=closed_sets_from_topology(carrier_set, topology),
    )


def _valid_topology_data(
    carrier: Iterable[Any],
    topology: Iterable[Iterable[Any]],
) -> tuple[frozenset[Any], tuple[frozenset[Any], ...]]:
    validation = validate_topology_candidate(carrier, topology)
    if not validation.is_topology:
        raise FiniteOperatorEngineError(
            "The supplied family is not a topology on the carrier. "
            f"failure_count={validation.failure_count}"
        )
    return validation.carrier, validation.opens


def _normalize_carrier(carrier: Iterable[Any]) -> frozenset[Any]:
    if carrier is None or isinstance(carrier, (str, bytes)):
        raise FiniteOperatorEngineError("carrier must be a finite iterable of points")
    try:
        return frozenset(carrier)
    except TypeError as exc:
        raise FiniteOperatorEngineError("carrier must contain hashable points") from exc


def _normalize_family(
    family: Iterable[Iterable[Any]],
    carrier_set: frozenset[Any],
    *,
    allow_external: bool = False,
) -> tuple[frozenset[Any], ...]:
    if family is None:
        raise FiniteOperatorEngineError("topology/family must be an iterable of subsets")
    normalized = []
    try:
        iterator = iter(family)
    except TypeError as exc:
        raise FiniteOperatorEngineError("topology/family must be iterable") from exc
    for member in iterator:
        try:
            frozen = frozenset(member)
        except TypeError as exc:
            raise FiniteOperatorEngineError("every member of the family must be iterable and hashable") from exc
        if not allow_external and not frozen.issubset(carrier_set):
            raise FiniteOperatorEngineError("family member is not a subset of the carrier")
        normalized.append(frozen)
    return _sort_family(normalized)


def _normalize_subset(subset: Iterable[Any], carrier_set: frozenset[Any]) -> frozenset[Any]:
    try:
        frozen = frozenset(subset)
    except TypeError as exc:
        raise FiniteOperatorEngineError("subset must be an iterable of hashable points") from exc
    if not frozen.issubset(carrier_set):
        raise FiniteOperatorEngineError("subset must be contained in the carrier")
    return frozen


def _powerset(carrier_set: frozenset[Any]) -> tuple[frozenset[Any], ...]:
    points = sorted(carrier_set, key=repr)
    subsets: list[frozenset[Any]] = []
    for size in range(len(points) + 1):
        for combo in combinations(points, size):
            subsets.append(frozenset(combo))
    return tuple(subsets)


def _sort_family(family: Iterable[frozenset[Any]]) -> tuple[frozenset[Any], ...]:
    unique = set(family)
    return tuple(sorted(unique, key=lambda block: (len(block), tuple(map(repr, sorted(block, key=repr))))))


__all__ = [
    "FiniteOperatorEngineError",
    "TopologyValidation",
    "FiniteOperatorTable",
    "validate_topology_candidate",
    "is_topology",
    "closed_sets_from_topology",
    "closure",
    "interior",
    "exterior",
    "boundary",
    "derived_set",
    "neighborhood_system",
    "relative_topology",
    "kuratowski_closure_check",
    "operator_table",
]
