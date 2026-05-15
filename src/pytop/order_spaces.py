"""Order-based space constructions.

This module provides thin wrappers around the Alexandroff bridge so that
finite preorders and finite partial orders can be treated as first-class space
objects inside the core package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .alexandroff import (
    AlexandroffError,
    alexandroff_space_from_preorder,
    is_partial_order,
    minimal_open_neighborhood,
    normalize_carrier,
    preorder_t0_reduction_data,
    reflexive_transitive_closure,
    specialization_preorder,
)
from .finite_spaces import FiniteTopologicalSpace
from .result import Result


@dataclass
class FinitePreorderSpace(FiniteTopologicalSpace):
    relation: set[tuple[Any, Any]] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.carrier = normalize_carrier(self.carrier)
        self.relation = reflexive_transitive_closure(self.carrier, self.relation)
        base = alexandroff_space_from_preorder(
            self.carrier,
            self.relation,
            description=self.metadata.get("description") if isinstance(self.metadata, dict) else None,
        )
        self.topology = base.topology
        base_metadata = dict(base.metadata)
        if isinstance(self.metadata, dict):
            base_metadata.update(self.metadata)
        self.metadata = base_metadata
        self.tags = set(getattr(base, "tags", set())) | set(getattr(self, "tags", set()))
        super().__post_init__()
        self.metadata["relation"] = sorted(self.relation, key=lambda pair: (repr(pair[0]), repr(pair[1])))
        self.metadata["order_model"] = "preorder"
        self.add_tags("alexandroff", "preorder")


@dataclass
class FinitePosetSpace(FinitePreorderSpace):
    def __post_init__(self) -> None:
        carrier_tuple = normalize_carrier(self.carrier)
        relation_set = reflexive_transitive_closure(carrier_tuple, self.relation)
        if not is_partial_order(carrier_tuple, relation_set):
            raise AlexandroffError("FinitePosetSpace requires an antisymmetric preorder.")
        self.carrier = carrier_tuple
        self.relation = relation_set
        super().__post_init__()
        self.metadata["order_model"] = "partial_order"
        self.add_tags("poset", "t0")


def preorder_space(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], *, description: str | None = None) -> FinitePreorderSpace:
    return FinitePreorderSpace(
        carrier=tuple(carrier),
        relation=set(relation),
        topology=[],
        metadata={"description": description or "Finite preorder space."},
    )


def poset_space(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], *, description: str | None = None) -> FinitePosetSpace:
    return FinitePosetSpace(
        carrier=tuple(carrier),
        relation=set(relation),
        topology=[],
        metadata={"description": description or "Finite poset space."},
    )


def upper_space_from_order(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], *, description: str | None = None) -> FinitePreorderSpace:
    return preorder_space(carrier, relation, description=description or "Upper Alexandroff space from an order.")


def lower_space_from_order(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]], *, description: str | None = None) -> FinitePreorderSpace:
    carrier_tuple = normalize_carrier(carrier)
    relation_set = reflexive_transitive_closure(carrier_tuple, relation)
    reversed_relation = {(y, x) for x, y in relation_set}
    return preorder_space(carrier_tuple, reversed_relation, description=description or "Lower Alexandroff space from an order.")



def preorder_t0_reduction(
    carrier: Iterable[Any],
    relation: Iterable[tuple[Any, Any]],
    *,
    description: str | None = None,
) -> FinitePosetSpace:
    """Return the poset obtained by quotienting a preorder by its kernel."""

    data = preorder_t0_reduction_data(carrier, relation)
    metadata = {
        'description': description or 'T0 reduction of a finite preorder space.',
        'kernel_blocks': [sorted(block, key=repr) for block in data['quotient_blocks']],
        'projection': {repr(point): sorted(block, key=repr) for point, block in data['projection'].items()},
        'construction': 'preorder_t0_reduction',
    }
    reduced = poset_space(data['quotient_blocks'], data['quotient_relation'], description=metadata['description'])
    reduced.metadata.update(metadata)
    reduced.add_tags('t0_reduction')
    return reduced


def specialization_poset(space: Any, *, description: str | None = None) -> FinitePosetSpace:
    """Return the ``T_0`` poset associated to the specialization preorder of a finite space."""

    carrier = getattr(space, 'carrier', None)
    topology = getattr(space, 'topology', None)
    if carrier is None or topology is None:
        raise AlexandroffError('Specialization-poset reduction requires an explicit finite topology.')
    reduced = preorder_t0_reduction(
        carrier,
        specialization_preorder(space),
        description=description or 'T0 specialization reduction of a finite topological space.',
    )
    reduced.metadata['source_space_description'] = getattr(space, 'metadata', {}).get('description', 'finite topology')
    reduced.add_tags('specialization_poset')
    return reduced


def preorder_reduction_report(carrier: Iterable[Any], relation: Iterable[tuple[Any, Any]]) -> dict[str, Any]:
    """Summarize the kernel quotient of a finite preorder."""

    data = preorder_t0_reduction_data(carrier, relation)
    return {
        'carrier_size': len(data['carrier']),
        'quotient_size': len(data['quotient_blocks']),
        'kernel_blocks': data['quotient_blocks'],
        'quotient_relation': sorted(data['quotient_relation'], key=lambda pair: (repr(pair[0]), repr(pair[1]))),
        'is_trivial_reduction': data['is_trivial_reduction'],
    }

def neighborhood_profile(space: FinitePreorderSpace) -> dict[Any, set[Any]]:
    return {point: minimal_open_neighborhood(space, point) for point in space.carrier}


def analyze_order_space(space: Any) -> Result:
    if isinstance(space, FinitePosetSpace):
        return Result.true(
            mode="exact",
            value="finite_poset_space",
            justification=["The space is explicitly represented as a finite poset space."],
            metadata={"order_model": "partial_order", "carrier_size": len(space.carrier)},
        )
    if isinstance(space, FinitePreorderSpace):
        return Result.true(
            mode="exact",
            value="finite_preorder_space",
            justification=["The space is explicitly represented as a finite preorder space."],
            metadata={"order_model": "preorder", "carrier_size": len(space.carrier)},
        )
    return Result.unknown(
        value="order_space",
        justification=["No explicit finite order-space representation was detected."],
    )


def order_space_report(space: FinitePreorderSpace) -> dict[str, Any]:
    return {
        "carrier_size": len(space.carrier),
        "order_model": space.metadata.get("order_model", "preorder"),
        "relation": sorted(space.relation, key=lambda pair: (repr(pair[0]), repr(pair[1]))),
        "neighborhoods": {repr(point): sorted(neighborhood, key=repr) for point, neighborhood in neighborhood_profile(space).items()},
    }


__all__ = [
    "FinitePreorderSpace",
    "FinitePosetSpace",
    "preorder_space",
    "poset_space",
    "upper_space_from_order",
    "lower_space_from_order",
    "preorder_t0_reduction",
    "specialization_poset",
    "preorder_reduction_report",
    "neighborhood_profile",
    "analyze_order_space",
    "order_space_report",
]
