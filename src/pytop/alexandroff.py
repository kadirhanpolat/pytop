"""Alexandroff-space helpers and order/topology bridges.

This module focuses on the finite exact layer. For finite spaces, Alexandroff
structure is especially natural: every finite topological space is an
Alexandroff space, and finite preorders can be turned into topologies by taking
upper sets.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable

from .finite_spaces import FiniteTopologicalSpace
from .relations import canonical_projection_from_equivalence, quotient_set
from .result import Result


class AlexandroffError(ValueError):
    """Raised for invalid Alexandroff/preorder data."""


def normalize_carrier(carrier: Iterable[Any]) -> tuple[Any, ...]:
    items = tuple(carrier)
    if len(set(items)) != len(items):
        raise AlexandroffError("Carrier elements must be distinct.")
    return items


def normalize_relation(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    carrier_tuple = normalize_carrier(carrier)
    carrier_set = set(carrier_tuple)
    normalized: set[tuple[Any, Any]] = set()
    for pair in relation:
        if len(pair) != 2:
            raise AlexandroffError("Relation pairs must have length 2.")
        x, y = pair
        if x not in carrier_set or y not in carrier_set:
            raise AlexandroffError("Relation contains elements outside the carrier.")
        normalized.add((x, y))
    return normalized


def reflexive_closure(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    carrier_tuple = normalize_carrier(carrier)
    closure = normalize_relation(carrier_tuple, relation)
    for x in carrier_tuple:
        closure.add((x, x))
    return closure


def transitive_closure(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    carrier_tuple = normalize_carrier(carrier)
    closure = set(normalize_relation(carrier_tuple, relation))
    changed = True
    while changed:
        changed = False
        new_pairs: set[tuple[Any, Any]] = set()
        for x, y in closure:
            for u, v in closure:
                if y == u and (x, v) not in closure:
                    new_pairs.add((x, v))
        if new_pairs:
            closure.update(new_pairs)
            changed = True
    return closure


def reflexive_transitive_closure(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    return transitive_closure(carrier, reflexive_closure(carrier, relation))


def is_reflexive(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = normalize_relation(carrier_tuple, relation)
    return all((x, x) in relation_set for x in carrier_tuple)


def is_transitive(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = normalize_relation(carrier_tuple, relation)
    return all((x, z) in relation_set for x, y in relation_set for u, z in relation_set if y == u)


def is_antisymmetric(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = normalize_relation(carrier_tuple, relation)
    return all(x == y or (y, x) not in relation_set for x, y in relation_set)


def is_preorder(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    return is_reflexive(carrier, relation) and is_transitive(carrier, relation)


def is_partial_order(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    return is_preorder(carrier, relation) and is_antisymmetric(carrier, relation)


def principal_upset(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], point: Any) -> set[Any]:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    if point not in carrier_tuple:
        raise AlexandroffError(f"Point {point!r} is not in the carrier.")
    return {y for x, y in relation_set if x == point}


def principal_downset(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], point: Any) -> set[Any]:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    if point not in carrier_tuple:
        raise AlexandroffError(f"Point {point!r} is not in the carrier.")
    return {x for x, y in relation_set if y == point}


def is_upper_set(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], subset: Iterable[Any]) -> bool:
    carrier_tuple = normalize_carrier(carrier)
    subset_set = set(subset)
    if not subset_set.issubset(set(carrier_tuple)):
        return False
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    return all(y in subset_set for x, y in relation_set if x in subset_set)


def upper_sets(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> list[set[Any]]:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    result: list[set[Any]] = [set()]
    for r in range(1, len(carrier_tuple) + 1):
        for combo in combinations(carrier_tuple, r):
            subset = set(combo)
            if is_upper_set(carrier_tuple, relation_set, subset):
                result.append(subset)
    full = set(carrier_tuple)
    if full not in result:
        result.append(full)
    return _normalize_topology(result)


def alexandroff_space_from_preorder(
    carrier: Iterable[Any],
    relation: Iterable[tuple[Any, Any]],
    *,
    description: str | None = None,
) -> FiniteTopologicalSpace:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    topology = upper_sets(carrier_tuple, relation_set)
    tags = {"finite", "alexandroff", "preorder"}
    if is_partial_order(carrier_tuple, relation_set):
        tags.update({"poset", "t0"})
    metadata = {
        "description": description or "Finite Alexandroff space induced by a preorder.",
        "representation": "finite",
        "relation": sorted(relation_set, key=lambda pair: (repr(pair[0]), repr(pair[1]))),
        "order_model": "partial_order" if "poset" in tags else "preorder",
    }
    return FiniteTopologicalSpace(carrier=carrier_tuple, topology=topology, metadata=metadata, tags=tags)


def minimal_open_neighborhood(space: Any, point: Any) -> set[Any]:
    topology = getattr(space, "topology", None)
    carrier = getattr(space, "carrier", None)
    if topology is None or carrier is None:
        raise AlexandroffError("Minimal open neighborhoods require an explicit topology.")
    if point not in carrier:
        raise AlexandroffError(f"Point {point!r} is not in the carrier.")
    containing = [set(U) for U in topology if point in U]
    if not containing:
        raise AlexandroffError(f"Point {point!r} is not contained in any open set.")
    result = set(containing[0])
    for open_set in containing[1:]:
        result.intersection_update(open_set)
    return result


def specialization_preorder(space: Any) -> set[tuple[Any, Any]]:
    topology = getattr(space, "topology", None)
    carrier = getattr(space, "carrier", None)
    if topology is None or carrier is None:
        raise AlexandroffError("Specialization preorder requires an explicit topology.")
    carrier_tuple = normalize_carrier(carrier)
    relation: set[tuple[Any, Any]] = set()
    for x in carrier_tuple:
        neighborhood = minimal_open_neighborhood(space, x)
        for y in neighborhood:
            relation.add((x, y))
    return reflexive_transitive_closure(carrier_tuple, relation)


def preorder_from_space(space: Any) -> set[tuple[Any, Any]]:
    return specialization_preorder(space)



def preorder_kernel_relation(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    """Return the equivalence relation induced by mutual comparability in a preorder."""

    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    return {(x, y) for x in carrier_tuple for y in carrier_tuple if (x, y) in relation_set and (y, x) in relation_set}


def preorder_t0_reduction_data(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> dict[str, Any]:
    """Collapse a preorder along its kernel to the associated ``T_0`` poset data."""

    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    kernel = preorder_kernel_relation(carrier_tuple, relation_set)
    quotient_blocks = quotient_set(carrier_tuple, kernel)
    projection = canonical_projection_from_equivalence(carrier_tuple, kernel)
    quotient_relation = {(projection[x], projection[y]) for x, y in relation_set}
    return {
        'carrier': carrier_tuple,
        'relation': relation_set,
        'kernel_relation': kernel,
        'quotient_blocks': quotient_blocks,
        'projection': projection,
        'quotient_relation': quotient_relation,
        'is_trivial_reduction': len(quotient_blocks) == len(carrier_tuple),
    }


def t0_reduction_profile(space: Any) -> dict[str, Any]:
    """Return specialization-preorder reduction data for an explicit finite topology."""

    topology = getattr(space, 'topology', None)
    carrier = getattr(space, 'carrier', None)
    if topology is None or carrier is None:
        raise AlexandroffError('T0 reduction requires an explicit finite topology.')
    data = preorder_t0_reduction_data(carrier, specialization_preorder(space))
    return {
        'carrier_size': len(data['carrier']),
        'quotient_size': len(data['quotient_blocks']),
        'quotient_blocks': data['quotient_blocks'],
        'kernel_relation': sorted(data['kernel_relation'], key=lambda pair: (repr(pair[0]), repr(pair[1]))),
        'quotient_relation': sorted(data['quotient_relation'], key=lambda pair: (repr(pair[0]), repr(pair[1]))),
        'is_trivial_reduction': data['is_trivial_reduction'],
    }

def analyze_alexandroff(space: Any) -> Result:
    representation = str(getattr(space, "metadata", {}).get("representation", "symbolic_general")).lower()
    tags = set(getattr(space, "tags", set())) | set(getattr(space, "metadata", {}).get("tags", []))
    tags = {str(tag).strip().lower() for tag in tags if str(tag).strip()}
    if getattr(space, "is_finite", lambda: False)() and getattr(space, "topology", None) is not None:
        return Result.true(
            mode="exact",
            value="alexandroff",
            justification=["Every finite topological space is an Alexandroff space."],
            proof_outline=[
                "A finite topology has only finitely many open sets.",
                "Any intersection of open sets reduces to the intersection of a finite subfamily.",
                "Finite intersections of opens are open, so arbitrary intersections are open.",
            ],
            metadata={"representation": representation, "tags": sorted(tags)},
        )
    if "alexandroff" in tags:
        return Result.true(
            mode="symbolic",
            value="alexandroff",
            justification=["The space carries an explicit Alexandroff tag."],
            metadata={"representation": representation, "tags": sorted(tags)},
        )
    return Result.unknown(
        value="alexandroff",
        justification=["No exact Alexandroff decision procedure is implemented for this representation."],
        metadata={"representation": representation, "tags": sorted(tags)},
    )


def is_alexandroff_space(space: Any) -> Result:
    return analyze_alexandroff(space)


def alexandroff_report(space: Any) -> dict[str, Any]:
    result = analyze_alexandroff(space)
    report: dict[str, Any] = {"alexandroff": result.to_dict()}
    if getattr(space, "topology", None) is not None and getattr(space, "carrier", None) is not None:
        report["specialization_preorder"] = sorted(
            specialization_preorder(space), key=lambda pair: (repr(pair[0]), repr(pair[1]))
        )
        report["minimal_open_neighborhoods"] = {
            repr(point): sorted(minimal_open_neighborhood(space, point), key=repr)
            for point in getattr(space, "carrier")
        }
    return report


def _normalize_topology(topology: Iterable[Iterable[Any]]) -> list[set[Any]]:
    normalized: list[set[Any]] = []
    seen: set[frozenset[Any]] = set()
    for open_set in topology:
        frozen = frozenset(open_set)
        if frozen not in seen:
            seen.add(frozen)
            normalized.append(set(open_set))
    return normalized


__all__ = [
    "AlexandroffError",
    "normalize_carrier",
    "normalize_relation",
    "reflexive_closure",
    "transitive_closure",
    "reflexive_transitive_closure",
    "is_reflexive",
    "is_transitive",
    "is_antisymmetric",
    "is_preorder",
    "is_partial_order",
    "principal_upset",
    "principal_downset",
    "is_upper_set",
    "upper_sets",
    "alexandroff_space_from_preorder",
    "minimal_open_neighborhood",
    "specialization_preorder",
    "preorder_from_space",
    "preorder_kernel_relation",
    "preorder_t0_reduction_data",
    "t0_reduction_profile",
    "analyze_alexandroff",
    "is_alexandroff_space",
    "alexandroff_report",
]
