"""Foundational relation helpers for Volume I Chapters 1--2.

The functions here stay finite and explicit. They support relation-domain and
range inspection, inverse relations, composition, relation-property tests,
equivalence classes, and the equivalence/partition correspondence.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .families import is_partition, normalize_family


class RelationError(ValueError):
    """Raised when relation data is malformed or incompatible."""


def normalize_carrier(carrier: Iterable[Any]) -> tuple[Any, ...]:
    items = tuple(carrier)
    if len(set(items)) != len(items):
        raise RelationError('Carrier elements must be distinct.')
    return items


def normalize_relation(relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    normalized: set[tuple[Any, Any]] = set()
    for pair in relation:
        try:
            x, y = pair
        except Exception as exc:  # pragma: no cover - defensive guard
            raise RelationError('Each relation entry must be a pair.') from exc
        normalized.add((x, y))
    return normalized


def validate_relation_on(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> tuple[tuple[Any, ...], set[tuple[Any, Any]]]:
    carrier_tuple = normalize_carrier(carrier)
    carrier_set = set(carrier_tuple)
    relation_set = normalize_relation(relation)
    outside = {(x, y) for x, y in relation_set if x not in carrier_set or y not in carrier_set}
    if outside:
        raise RelationError('Relation contains elements outside the carrier.')
    return carrier_tuple, relation_set


def validate_relation_between(
    domain_carrier: Iterable[Any],
    codomain_carrier: Iterable[Any],
    relation: Iterable[tuple[Any, Any]],
) -> tuple[tuple[Any, ...], tuple[Any, ...], set[tuple[Any, Any]]]:
    r"""Validate a relation ``R \subseteq A \times B`` between two carriers."""

    domain_tuple = normalize_carrier(domain_carrier)
    codomain_tuple = normalize_carrier(codomain_carrier)
    domain_set = set(domain_tuple)
    codomain_set = set(codomain_tuple)
    relation_set = normalize_relation(relation)
    outside = {(x, y) for x, y in relation_set if x not in domain_set or y not in codomain_set}
    if outside:
        raise RelationError('Relation contains elements outside the declared domain/codomain carriers.')
    return domain_tuple, codomain_tuple, relation_set


def identity_relation(carrier: Iterable[Any]) -> set[tuple[Any, Any]]:
    """Return the diagonal/identity relation on the carrier."""

    carrier_tuple = normalize_carrier(carrier)
    return {(x, x) for x in carrier_tuple}


def relation_domain(relation: Iterable[tuple[Any, Any]]) -> set[Any]:
    """Return the set of first coordinates appearing in the relation."""

    return {x for x, _ in normalize_relation(relation)}


def relation_range(relation: Iterable[tuple[Any, Any]]) -> set[Any]:
    """Return the set of second coordinates appearing in the relation."""

    return {y for _, y in normalize_relation(relation)}


def inverse_relation(relation: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    """Return the inverse relation ``R^{-1}``."""

    return {(y, x) for x, y in normalize_relation(relation)}


def compose_relations(first: Iterable[tuple[Any, Any]], second: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    """Compose *second* after *first*.

    In other words, the result is ``second ∘ first``.
    """

    first_set = normalize_relation(first)
    second_set = normalize_relation(second)
    return {
        (x, z)
        for x, y in first_set
        for u, z in second_set
        if y == u
    }


def is_reflexive(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    return all((x, x) in relation_set for x in carrier_tuple)


def is_irreflexive(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    return all((x, x) not in relation_set for x in carrier_tuple)


def is_symmetric(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    _, relation_set = validate_relation_on(carrier, relation)
    return all((y, x) in relation_set for x, y in relation_set)


def is_transitive(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    _, relation_set = validate_relation_on(carrier, relation)
    return all((x, z) in relation_set for x, y in relation_set for u, z in relation_set if y == u)


def is_antisymmetric(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    _, relation_set = validate_relation_on(carrier, relation)
    return all(x == y or (y, x) not in relation_set for x, y in relation_set)


def is_preorder(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    return is_reflexive(carrier, relation) and is_transitive(carrier, relation)


def is_partial_order(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    return is_preorder(carrier, relation) and is_antisymmetric(carrier, relation)


def is_linear_order(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    if not is_partial_order(carrier_tuple, relation_set):
        return False
    return all((x, y) in relation_set or (y, x) in relation_set for x in carrier_tuple for y in carrier_tuple)


def is_total_order(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    return is_linear_order(carrier, relation)


def relation_profile(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> dict[str, Any]:
    """Return a compact structural profile for a finite relation on one carrier."""

    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    carrier_set = set(carrier_tuple)
    missing_reflexive_points = {x for x in carrier_tuple if (x, x) not in relation_set}
    incomparable_pairs = {
        (x, y)
        for x in carrier_tuple
        for y in carrier_tuple
        if x != y and (x, y) not in relation_set and (y, x) not in relation_set
    }
    profile = {
        'carrier': carrier_tuple,
        'carrier_size': len(carrier_tuple),
        'carrier_set': carrier_set,
        'relation': relation_set,
        'relation_size': len(relation_set),
        'identity_relation': identity_relation(carrier_tuple),
        'domain': relation_domain(relation_set),
        'range': relation_range(relation_set),
        'missing_reflexive_points': missing_reflexive_points,
        'incomparable_pairs': incomparable_pairs,
        'is_reflexive': is_reflexive(carrier_tuple, relation_set),
        'is_irreflexive': is_irreflexive(carrier_tuple, relation_set),
        'is_symmetric': is_symmetric(carrier_tuple, relation_set),
        'is_transitive': is_transitive(carrier_tuple, relation_set),
        'is_antisymmetric': is_antisymmetric(carrier_tuple, relation_set),
    }
    profile['is_equivalence_relation'] = bool(
        profile['is_reflexive'] and profile['is_symmetric'] and profile['is_transitive']
    )
    profile['is_preorder'] = bool(profile['is_reflexive'] and profile['is_transitive'])
    profile['is_partial_order'] = bool(profile['is_preorder'] and profile['is_antisymmetric'])
    profile['is_linear_order'] = bool(profile['is_partial_order'] and not incomparable_pairs)
    profile['is_total_order'] = profile['is_linear_order']
    profile['is_identity_relation'] = relation_set == profile['identity_relation']
    return profile


def is_equivalence_relation(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> bool:
    return is_reflexive(carrier, relation) and is_symmetric(carrier, relation) and is_transitive(carrier, relation)


def equivalence_class(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], point: Any) -> set[Any]:
    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    if point not in carrier_tuple:
        raise RelationError(f'Point {point!r} is not in the carrier.')
    if not is_equivalence_relation(carrier_tuple, relation_set):
        raise RelationError('Equivalence classes are only defined here for equivalence relations.')
    return {y for x, y in relation_set if x == point}


def partition_from_equivalence(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> set[frozenset[Any]]:
    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    if not is_equivalence_relation(carrier_tuple, relation_set):
        raise RelationError('The relation must be an equivalence relation.')
    remaining = set(carrier_tuple)
    blocks: set[frozenset[Any]] = set()
    while remaining:
        point = next(iter(remaining))
        block = frozenset(equivalence_class(carrier_tuple, relation_set, point))
        blocks.add(block)
        remaining -= set(block)
    return blocks



def quotient_set(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> tuple[frozenset[Any], ...]:
    r"""Return the quotient set ``X/{\sim}`` as an ordered tuple of blocks.

    The blocks are returned in a deterministic order so downstream pedagogy and
    reporting layers can use the result without re-sorting.
    """

    blocks = partition_from_equivalence(carrier, relation)
    return tuple(sorted(blocks, key=lambda block: (len(block), tuple(sorted(repr(x) for x in block)))))


def canonical_projection_from_equivalence(
    carrier: Iterable[Any],
    relation: Iterable[tuple[Any, Any]],
) -> dict[Any, frozenset[Any]]:
    r"""Return the canonical projection ``x \mapsto [x]`` for an equivalence relation."""

    carrier_tuple, relation_set = validate_relation_on(carrier, relation)
    blocks = quotient_set(carrier_tuple, relation_set)
    projection: dict[Any, frozenset[Any]] = {}
    for block in blocks:
        for x in block:
            projection[x] = block
    return projection

def equivalence_from_partition(
    universe: Iterable[Any],
    partition: Iterable[Iterable[Any]],
) -> set[tuple[Any, Any]]:
    universe_set = set(universe)
    normalized_partition = normalize_family(partition)
    if not is_partition(universe_set, normalized_partition):
        raise RelationError('The supplied family is not a partition of the universe.')
    relation: set[tuple[Any, Any]] = set()
    for block in normalized_partition:
        for x in block:
            for y in block:
                relation.add((x, y))
    return relation


__all__ = [
    'RelationError',
    'normalize_carrier',
    'normalize_relation',
    'validate_relation_on',
    'validate_relation_between',
    'identity_relation',
    'relation_domain',
    'relation_range',
    'inverse_relation',
    'compose_relations',
    'is_reflexive',
    'is_irreflexive',
    'is_symmetric',
    'is_transitive',
    'is_antisymmetric',
    'is_preorder',
    'is_partial_order',
    'is_linear_order',
    'is_total_order',
    'relation_profile',
    'is_equivalence_relation',
    'equivalence_class',
    'partition_from_equivalence',
    'quotient_set',
    'canonical_projection_from_equivalence',
    'equivalence_from_partition',
]
