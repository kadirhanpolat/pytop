"""Finite map and continuity engine.

This module materializes the Chapter 02/04/06 map-continuity corridor for
explicit finite spaces.  It is intentionally small: carriers, topologies and
maps are supplied as concrete finite data.  The goal is to connect image,
preimage, injective/surjective checks, continuity via open sets, and continuity
via codomain bases.

No external chapter wording, examples, solved problems, images, or exercise
statements are copied here.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from .finite_basis_engine import continuity_via_basis_preimage
from .finite_operator_engine import is_topology


class FiniteMapEngineError(ValueError):
    """Raised when finite map data is malformed."""


@dataclass(frozen=True)
class FiniteMapData:
    domain: frozenset[Any]
    codomain: frozenset[Any]
    mapping: dict[Any, Any]

    def image_of_point(self, point: Any) -> Any:
        if point not in self.domain:
            raise FiniteMapEngineError(f"point {point!r} is not in the domain")
        return self.mapping[point]

    @property
    def graph(self) -> tuple[tuple[Any, Any], ...]:
        return tuple(sorted(self.mapping.items(), key=lambda item: repr(item[0])))


@dataclass(frozen=True)
class FiniteMapAnalysis:
    map_data: FiniteMapData
    image: frozenset[Any]
    is_total: bool
    is_well_defined: bool
    is_injective: bool
    is_surjective: bool
    is_bijective: bool
    is_continuous: bool
    continuity_checks: tuple[tuple[frozenset[Any], frozenset[Any], bool], ...]

    @property
    def is_homeomorphism_candidate(self) -> bool:
        return self.is_bijective and self.is_continuous

    def as_dict(self) -> dict[str, Any]:
        return {
            "domain": self.map_data.domain,
            "codomain": self.map_data.codomain,
            "graph": self.map_data.graph,
            "image": self.image,
            "is_total": self.is_total,
            "is_well_defined": self.is_well_defined,
            "is_injective": self.is_injective,
            "is_surjective": self.is_surjective,
            "is_bijective": self.is_bijective,
            "is_continuous": self.is_continuous,
            "continuity_checks": self.continuity_checks,
            "is_homeomorphism_candidate": self.is_homeomorphism_candidate,
        }


def normalize_finite_map_data(
    domain: Iterable[Any],
    codomain: Iterable[Any],
    mapping: Mapping[Any, Any],
) -> FiniteMapData:
    domain_set = _normalize_carrier(domain, "domain")
    codomain_set = _normalize_carrier(codomain, "codomain")
    mapping_dict = dict(mapping)
    missing = domain_set - set(mapping_dict)
    if missing:
        raise FiniteMapEngineError(f"mapping is missing domain points: {sorted(map(repr, missing))}")
    extra = set(mapping_dict) - domain_set
    if extra:
        raise FiniteMapEngineError(f"mapping has keys outside the domain: {sorted(map(repr, extra))}")
    outside = {value for value in mapping_dict.values() if value not in codomain_set}
    if outside:
        raise FiniteMapEngineError(f"mapping has values outside the codomain: {sorted(map(repr, outside))}")
    return FiniteMapData(domain=domain_set, codomain=codomain_set, mapping=mapping_dict)


def image_of_subset_finite(map_data: FiniteMapData, subset: Iterable[Any]) -> frozenset[Any]:
    subset_set = _normalize_subset(subset, map_data.domain, "subset")
    return frozenset(map_data.mapping[x] for x in subset_set)


def preimage_of_subset_finite(map_data: FiniteMapData, subset: Iterable[Any]) -> frozenset[Any]:
    subset_set = _normalize_subset(subset, map_data.codomain, "subset")
    return frozenset(x for x in map_data.domain if map_data.mapping[x] in subset_set)


def finite_map_table(
    domain: Iterable[Any],
    codomain: Iterable[Any],
    mapping: Mapping[Any, Any],
) -> dict[str, Any]:
    map_data = normalize_finite_map_data(domain, codomain, mapping)
    return {
        "domain": map_data.domain,
        "codomain": map_data.codomain,
        "graph": map_data.graph,
        "image": image_of_subset_finite(map_data, map_data.domain),
    }


def is_injective_finite_map(map_data: FiniteMapData) -> bool:
    values = list(map_data.mapping.values())
    return len(set(values)) == len(values)


def is_surjective_finite_map(map_data: FiniteMapData) -> bool:
    return image_of_subset_finite(map_data, map_data.domain) == map_data.codomain


def is_bijective_finite_map(map_data: FiniteMapData) -> bool:
    return is_injective_finite_map(map_data) and is_surjective_finite_map(map_data)


def continuity_checks_by_opens(
    domain: Iterable[Any],
    domain_topology: Iterable[Iterable[Any]],
    codomain: Iterable[Any],
    codomain_topology: Iterable[Iterable[Any]],
    mapping: Mapping[Any, Any],
) -> tuple[tuple[frozenset[Any], frozenset[Any], bool], ...]:
    map_data = normalize_finite_map_data(domain, codomain, mapping)
    domain_topology_sets = _normalize_topology(domain_topology, map_data.domain, "domain_topology")
    codomain_topology_sets = _normalize_topology(codomain_topology, map_data.codomain, "codomain_topology")
    if not is_topology(map_data.domain, domain_topology_sets):
        raise FiniteMapEngineError("domain_topology is not a topology on the domain")
    if not is_topology(map_data.codomain, codomain_topology_sets):
        raise FiniteMapEngineError("codomain_topology is not a topology on the codomain")
    checks = []
    for open_set in codomain_topology_sets:
        preimage = preimage_of_subset_finite(map_data, open_set)
        checks.append((open_set, preimage, preimage in domain_topology_sets))
    return tuple(checks)


def is_continuous_finite_map(
    domain: Iterable[Any],
    domain_topology: Iterable[Iterable[Any]],
    codomain: Iterable[Any],
    codomain_topology: Iterable[Iterable[Any]],
    mapping: Mapping[Any, Any],
) -> bool:
    return all(item[2] for item in continuity_checks_by_opens(domain, domain_topology, codomain, codomain_topology, mapping))


def continuity_via_codomain_basis_finite(
    domain: Iterable[Any],
    domain_topology: Iterable[Iterable[Any]],
    codomain_basis: Iterable[Iterable[Any]],
    mapping: Mapping[Any, Any],
) -> dict[str, Any]:
    return continuity_via_basis_preimage(domain, domain_topology, codomain_basis, mapping)


def analyze_finite_map(
    domain: Iterable[Any],
    domain_topology: Iterable[Iterable[Any]],
    codomain: Iterable[Any],
    codomain_topology: Iterable[Iterable[Any]],
    mapping: Mapping[Any, Any],
) -> FiniteMapAnalysis:
    map_data = normalize_finite_map_data(domain, codomain, mapping)
    checks = continuity_checks_by_opens(domain, domain_topology, codomain, codomain_topology, mapping)
    image = image_of_subset_finite(map_data, map_data.domain)
    injective = is_injective_finite_map(map_data)
    surjective = image == map_data.codomain
    return FiniteMapAnalysis(
        map_data=map_data,
        image=image,
        is_total=True,
        is_well_defined=True,
        is_injective=injective,
        is_surjective=surjective,
        is_bijective=injective and surjective,
        is_continuous=all(item[2] for item in checks),
        continuity_checks=checks,
    )


def finite_map_engine_capabilities() -> dict[str, int]:
    return {
        "normalize_finite_map_data": 1,
        "image_of_subset_finite": 1,
        "preimage_of_subset_finite": 1,
        "finite_map_table": 1,
        "injective_surjective_bijective": 3,
        "continuity_checks_by_opens": 1,
        "continuity_via_codomain_basis_finite": 1,
        "analyze_finite_map": 1,
    }


def _normalize_carrier(carrier: Iterable[Any], label: str) -> frozenset[Any]:
    if carrier is None or isinstance(carrier, (str, bytes)):
        raise FiniteMapEngineError(f"{label} must be a finite iterable of hashable points")
    try:
        return frozenset(carrier)
    except TypeError as exc:
        raise FiniteMapEngineError(f"{label} must contain hashable points") from exc


def _normalize_subset(subset: Iterable[Any], carrier: frozenset[Any], label: str) -> frozenset[Any]:
    try:
        subset_set = frozenset(subset)
    except TypeError as exc:
        raise FiniteMapEngineError(f"{label} must be an iterable of hashable points") from exc
    if not subset_set.issubset(carrier):
        raise FiniteMapEngineError(f"{label} must be contained in the corresponding carrier")
    return subset_set


def _normalize_topology(
    topology: Iterable[Iterable[Any]],
    carrier: frozenset[Any],
    label: str,
) -> tuple[frozenset[Any], ...]:
    if topology is None:
        raise FiniteMapEngineError(f"{label} must be an iterable of subsets")
    members = []
    for member in topology:
        frozen = frozenset(member)
        if not frozen.issubset(carrier):
            raise FiniteMapEngineError(f"{label} member is not a subset of the carrier")
        members.append(frozen)
    return tuple(sorted(set(members), key=lambda block: (len(block), tuple(map(repr, sorted(block, key=repr))))))


__all__ = [
    "FiniteMapEngineError",
    "FiniteMapData",
    "FiniteMapAnalysis",
    "normalize_finite_map_data",
    "image_of_subset_finite",
    "preimage_of_subset_finite",
    "finite_map_table",
    "is_injective_finite_map",
    "is_surjective_finite_map",
    "is_bijective_finite_map",
    "continuity_checks_by_opens",
    "is_continuous_finite_map",
    "continuity_via_codomain_basis_finite",
    "analyze_finite_map",
    "finite_map_engine_capabilities",
]
