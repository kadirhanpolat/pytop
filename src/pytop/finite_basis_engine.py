"""Finite basis/subbasis engine.

This module materializes the Chapter 06 API surface and connects it to the
v1.0.177 finite topological operator engine.  It is exact for explicit finite
carriers and finite subset families.

No external chapter text, examples, solutions, or exercise statements are
copied here.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from .finite_operator_engine import is_topology
from .finite_spaces import FiniteTopologicalSpace
from .subbases import (
    finite_intersection_basis,
    generate_topology_from_basis,
    generate_topology_from_subbasis,
    is_local_base_at,
)


class FiniteBasisEngineError(ValueError):
    """Raised when the finite basis engine receives malformed data."""


@dataclass(frozen=True)
class BasisAnalysis:
    carrier: frozenset[Any]
    basis: tuple[frozenset[Any], ...]
    is_basis: bool
    generated_topology: tuple[frozenset[Any], ...] | None
    coverage_missing: frozenset[Any]
    intersection_failures: tuple[tuple[frozenset[Any], frozenset[Any], Any, frozenset[Any]], ...]

    @property
    def failure_count(self) -> int:
        return (1 if self.coverage_missing else 0) + len(self.intersection_failures)

    def as_dict(self) -> dict[str, Any]:
        return {
            "carrier": self.carrier,
            "basis": self.basis,
            "is_basis": self.is_basis,
            "generated_topology": self.generated_topology,
            "coverage_missing": self.coverage_missing,
            "intersection_failures": self.intersection_failures,
            "failure_count": self.failure_count,
        }


@dataclass(frozen=True)
class SubbasisAnalysis:
    carrier: frozenset[Any]
    subbasis: tuple[frozenset[Any], ...]
    finite_intersection_basis: tuple[frozenset[Any], ...]
    generated_topology: tuple[frozenset[Any], ...]
    topology_is_valid: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "carrier": self.carrier,
            "subbasis": self.subbasis,
            "finite_intersection_basis": self.finite_intersection_basis,
            "generated_topology": self.generated_topology,
            "topology_is_valid": self.topology_is_valid,
        }


@dataclass(frozen=True)
class BasisComparison:
    carrier: frozenset[Any]
    first_topology: tuple[frozenset[Any], ...]
    second_topology: tuple[frozenset[Any], ...]
    same_topology: bool
    first_only: tuple[frozenset[Any], ...]
    second_only: tuple[frozenset[Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "carrier": self.carrier,
            "first_topology": self.first_topology,
            "second_topology": self.second_topology,
            "same_topology": self.same_topology,
            "first_only": self.first_only,
            "second_only": self.second_only,
        }


def analyze_basis(
    carrier: Iterable[Any],
    basis_family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> BasisAnalysis:
    carrier_set = _normalize_carrier(carrier)
    basis = _normalize_family(basis_family, carrier_set)
    coverage = frozenset().union(*basis) if basis else frozenset()
    coverage_missing = carrier_set - coverage
    failures = _basis_intersection_failures(basis)
    is_basis = not coverage_missing and not failures
    generated: tuple[frozenset[Any], ...] | None = None
    if is_basis:
        space = generate_topology_from_basis(carrier_set, basis)
        generated = _normalize_family(space.topology, carrier_set)
    return BasisAnalysis(
        carrier=carrier_set,
        basis=basis,
        is_basis=is_basis,
        generated_topology=generated,
        coverage_missing=coverage_missing,
        intersection_failures=failures,
    )


def generated_topology_from_basis(
    carrier: Iterable[Any],
    basis_family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> tuple[frozenset[Any], ...]:
    carrier_set = _normalize_carrier(carrier)
    space = generate_topology_from_basis(carrier_set, basis_family)
    topology = _normalize_family(space.topology, carrier_set)
    if not is_topology(carrier_set, topology):
        raise FiniteBasisEngineError("generated topology failed finite operator validation")
    return topology


def basis_from_subbasis(
    carrier: Iterable[Any],
    subbasis_family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> tuple[frozenset[Any], ...]:
    carrier_set = _normalize_carrier(carrier)
    return _normalize_family(finite_intersection_basis(carrier_set, subbasis_family), carrier_set)


def analyze_subbasis(
    carrier: Iterable[Any],
    subbasis_family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> SubbasisAnalysis:
    carrier_set = _normalize_carrier(carrier)
    subbasis = _normalize_family(subbasis_family, carrier_set)
    basis = basis_from_subbasis(carrier_set, subbasis)
    space = generate_topology_from_subbasis(carrier_set, subbasis)
    topology = _normalize_family(space.topology, carrier_set)
    return SubbasisAnalysis(
        carrier=carrier_set,
        subbasis=subbasis,
        finite_intersection_basis=basis,
        generated_topology=topology,
        topology_is_valid=is_topology(carrier_set, topology),
    )


def compare_generated_topologies_from_bases(
    carrier: Iterable[Any],
    first_basis: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
    second_basis: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
) -> BasisComparison:
    carrier_set = _normalize_carrier(carrier)
    first_topology = generated_topology_from_basis(carrier_set, first_basis)
    second_topology = generated_topology_from_basis(carrier_set, second_basis)
    first_set = set(first_topology)
    second_set = set(second_topology)
    return BasisComparison(
        carrier=carrier_set,
        first_topology=first_topology,
        second_topology=second_topology,
        same_topology=first_set == second_set,
        first_only=_sort_family(first_set - second_set),
        second_only=_sort_family(second_set - first_set),
    )


def relative_basis(
    basis_family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
    subspace: Iterable[Any],
    *,
    include_empty: bool = False,
) -> tuple[frozenset[Any], ...]:
    subspace_set = _normalize_carrier(subspace)
    basis = _normalize_family(basis_family, None)
    members = []
    for member in basis:
        restricted = member & subspace_set
        if restricted or include_empty:
            members.append(restricted)
    return _sort_family(members)


def local_base_report(
    carrier_or_space: Iterable[Any] | FiniteTopologicalSpace,
    point: Any,
    candidate_family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
    topology: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]] | None = None,
) -> dict[str, Any]:
    valid = is_local_base_at(carrier_or_space, point, candidate_family, topology=topology)
    if isinstance(carrier_or_space, FiniteTopologicalSpace):
        carrier_set = _normalize_carrier(carrier_or_space.carrier)
        topology_family = carrier_or_space.topology
    else:
        carrier_set = _normalize_carrier(carrier_or_space)
        topology_family = topology
    candidate = _normalize_family(candidate_family, carrier_set)
    neighborhoods = ()
    if topology_family is not None and point in carrier_set:
        topology_sets = _normalize_family(topology_family, carrier_set)
        neighborhoods = tuple(open_set for open_set in topology_sets if point in open_set)
    return {
        "point": point,
        "candidate_family": candidate,
        "is_local_base": valid,
        "neighborhoods_checked": _sort_family(neighborhoods),
    }


def continuity_via_basis_preimage(
    domain_carrier: Iterable[Any],
    domain_topology: Iterable[Iterable[Any]],
    codomain_basis: Iterable[Iterable[Any]],
    mapping: Mapping[Any, Any],
) -> dict[str, Any]:
    domain_set = _normalize_carrier(domain_carrier)
    domain_topology_sets = _normalize_family(domain_topology, domain_set)
    basis = _normalize_family(codomain_basis, None)
    if not is_topology(domain_set, domain_topology_sets):
        raise FiniteBasisEngineError("domain_topology is not a topology on domain_carrier")
    missing_points = domain_set - set(mapping)
    if missing_points:
        raise FiniteBasisEngineError(f"mapping is missing domain points: {sorted(map(repr, missing_points))}")
    checks = []
    for basis_member in basis:
        preimage = frozenset(point for point in domain_set if mapping[point] in basis_member)
        checks.append((basis_member, preimage, preimage in domain_topology_sets))
    return {
        "is_continuous_via_basis": all(item[2] for item in checks),
        "checks": tuple(checks),
    }


def minimal_basis(space: FiniteTopologicalSpace) -> tuple[frozenset[Any], ...]:
    """Return the unique minimal basis of a finite topological space.

    The minimal basis consists of the minimal open neighborhood of each point:
    for each x, intersect all open sets containing x.  These intersections are
    automatically open (finite topology is closed under finite intersections)
    and form the coarsest possible basis.

    Parameters
    ----------
    space:
        A FiniteTopologicalSpace instance.

    Returns
    -------
    Sorted tuple of distinct basis elements (frozensets).
    """
    carrier_set: frozenset[Any] = frozenset(space.carrier)
    opens = [frozenset(u) for u in space.topology]
    empty = frozenset()

    basis_elements: set[frozenset[Any]] = set()
    for x in carrier_set:
        neighborhoods = [u for u in opens if x in u]
        if not neighborhoods:
            # isolated point with no open neighborhood — degenerate topology
            continue
        min_nbhd: frozenset[Any] = neighborhoods[0]
        for u in neighborhoods[1:]:
            min_nbhd = min_nbhd & u
        if min_nbhd != empty:
            basis_elements.add(min_nbhd)

    return _sort_family(basis_elements)


def minimal_basis_report(space: FiniteTopologicalSpace) -> dict[str, Any]:
    """Return a report dict for the minimal basis of *space*.

    Keys: carrier, topology_size, minimal_basis, minimal_basis_size,
    reduction_ratio (topology_size / minimal_basis_size).
    """
    basis = minimal_basis(space)
    topo_size = len(list(space.topology))
    basis_size = len(basis)
    return {
        "carrier": frozenset(space.carrier),
        "topology_size": topo_size,
        "minimal_basis": basis,
        "minimal_basis_size": basis_size,
        "reduction_ratio": round(topo_size / basis_size, 3) if basis_size else None,
    }


def finite_basis_engine_capabilities() -> dict[str, int]:
    return {
        "basis_analysis": 1,
        "subbasis_analysis": 1,
        "basis_comparison": 1,
        "relative_basis": 1,
        "local_base_report": 1,
        "continuity_via_basis_preimage": 1,
        "minimal_basis": 1,
        "minimal_basis_report": 1,
    }


def _basis_intersection_failures(
    basis: tuple[frozenset[Any], ...]
) -> tuple[tuple[frozenset[Any], frozenset[Any], Any, frozenset[Any]], ...]:
    failures = []
    for left in basis:
        for right in basis:
            overlap = left & right
            for point in overlap:
                if not any(point in candidate and candidate.issubset(overlap) for candidate in basis):
                    failures.append((left, right, point, overlap))
    return tuple(failures)


def _normalize_carrier(carrier: Iterable[Any]) -> frozenset[Any]:
    if carrier is None or isinstance(carrier, (str, bytes)):
        raise FiniteBasisEngineError("carrier must be a finite iterable of hashable points")
    try:
        return frozenset(carrier)
    except TypeError as exc:
        raise FiniteBasisEngineError("carrier must contain hashable points") from exc


def _normalize_family(
    family: Mapping[Any, Iterable[Any]] | Iterable[Iterable[Any]],
    carrier_set: frozenset[Any] | None,
) -> tuple[frozenset[Any], ...]:
    members = family.values() if isinstance(family, Mapping) else family
    normalized = []
    for member in members:
        try:
            frozen = frozenset(member)
        except TypeError as exc:
            raise FiniteBasisEngineError("every family member must be iterable and hashable") from exc
        if carrier_set is not None and not frozen.issubset(carrier_set):
            raise FiniteBasisEngineError("family member is not a subset of the carrier")
        normalized.append(frozen)
    return _sort_family(normalized)


def _sort_family(family: Iterable[frozenset[Any]]) -> tuple[frozenset[Any], ...]:
    return tuple(sorted(set(family), key=lambda block: (len(block), tuple(map(repr, sorted(block, key=repr))))))


__all__ = [
    "FiniteBasisEngineError",
    "BasisAnalysis",
    "SubbasisAnalysis",
    "BasisComparison",
    "analyze_basis",
    "generated_topology_from_basis",
    "basis_from_subbasis",
    "analyze_subbasis",
    "compare_generated_topologies_from_bases",
    "relative_basis",
    "local_base_report",
    "continuity_via_basis_preimage",
    "minimal_basis",
    "minimal_basis_report",
    "finite_basis_engine_capabilities",
]
