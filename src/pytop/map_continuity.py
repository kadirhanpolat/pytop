"""Pointwise continuity and criterion-based continuity checks for finite maps.

This module contains:
- :func:`is_continuous_at_point` — neighborhood criterion at a single point
- :func:`is_sequentially_continuous_at_point` — derived via first-countability
- :func:`continuity_via_codomain_basis` — basis criterion (Chapter 06)
- :func:`continuity_via_codomain_subbasis` — subbasis criterion (Chapter 06)
- :func:`satisfies_closure_image_inclusion` — f(cl(A)) ⊆ cl(f(A)) check
- :func:`initial_topology_from_maps` — coarsest topology making maps continuous

The core analysis engine, types, and private helpers live in
:mod:`pytop.finite_map_analysis`.  The legacy entry point :mod:`pytop.maps`
re-exports everything from both modules.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .finite_map_analysis import (
    FiniteMap,
    image_of_subset,
    preimage_of_subset,
    _can_do_exact_finite_map_analysis,
    _exact_result,
    _graph_dict,
    _normalize_family,
    _preimage,
)
from .infinite_maps import SymbolicMap
from .result import Result
from .finite_spaces import FiniteTopologicalSpace
from .subbases import generate_topology_from_subbasis, is_basis_for_topology
from .subset_operators import closure_of_subset


def is_continuous_at_point(map_obj: SymbolicMap, point: Any) -> Result:
    if _can_do_exact_finite_map_analysis(map_obj):
        graph = _graph_dict(map_obj)
        dom_points = tuple(getattr(map_obj.domain, "carrier", ()))
        dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
        cod_open_sets = _normalize_family(getattr(map_obj.codomain, "topology", ()))
        if point not in dom_points:
            return Result.unknown(
                mode="exact",
                value="continuous_at_point",
                justification=["The requested point does not belong to the explicit finite domain carrier; continuity at an external point is undefined."],
                metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
            )
        image_point = graph[point]
        for neighborhood in cod_open_sets:
            if image_point not in neighborhood:
                continue
            pre = _preimage(graph, set(neighborhood))
            if not any(point in open_set and open_set.issubset(pre) for open_set in dom_open_sets):
                return Result.false(
                    mode="exact",
                    value="continuous_at_point",
                    justification=["A codomain neighborhood of f(point) failed to pull back to a neighborhood of the chosen domain point."],
                    proof_outline=["Use the neighborhood criterion for continuity at a point."],
                    metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
                )
        return Result.true(
            mode="exact",
            value="continuous_at_point",
            justification=["Every open neighborhood of f(point) pulled back to a neighborhood of the chosen point."],
            proof_outline=["Check the pointwise neighborhood criterion against the explicit finite topology."],
            metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
        )
    return Result.unknown(
        mode="symbolic",
        value="continuous_at_point",
        justification=["Exact pointwise continuity is currently implemented only for explicit finite maps."],
        metadata={"representation": getattr(map_obj, "metadata", {}).get("representation", "symbolic_map"), "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
    )


def is_sequentially_continuous_at_point(map_obj: SymbolicMap, point: Any) -> Result:
    pointwise = is_continuous_at_point(map_obj, point)
    if _can_do_exact_finite_map_analysis(map_obj):
        if pointwise.is_true:
            return Result.true(
                mode="theorem",
                value="sequentially_continuous_at_point",
                assumptions=["Finite spaces are first countable at every point."],
                justification=["In first countable spaces, continuity at a point implies sequential continuity at that point."],
                proof_outline=["Use the Chapter 06 first-countable criterion after exact pointwise continuity has been established."],
                metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
            )
        if pointwise.is_false:
            return Result.false(
                mode="theorem",
                value="sequentially_continuous_at_point",
                assumptions=["Finite spaces are first countable at every point."],
                justification=["On first countable spaces, failure of continuity at a point also rules out sequential continuity there."],
                proof_outline=["Use the Chapter 06 first-countable equivalence between pointwise continuity and sequential continuity."],
                metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
            )
    return Result.unknown(
        mode="symbolic",
        value="sequentially_continuous_at_point",
        justification=["Sequential continuity at a point is currently derived automatically only in the explicit finite / first-countable setting."],
        metadata={"representation": getattr(map_obj, "metadata", {}).get("representation", "symbolic_map"), "map_name": getattr(map_obj, "name", "f"), "point": repr(point)},
    )


def continuity_via_codomain_basis(map_obj: SymbolicMap, basis_family: Iterable[Iterable[Any]]) -> Result:
    if not _can_do_exact_finite_map_analysis(map_obj):
        return Result.unknown(
            mode="symbolic",
            value="continuous",
            justification=["Basis-level continuity checks are currently exact only for explicit finite maps."],
            metadata={"criterion": "basis", "map_name": getattr(map_obj, "name", "f")},
        )
    basis_list = list(basis_family)
    if not is_basis_for_topology(map_obj.codomain, basis_list):
        return Result.false(
            mode="exact",
            value="continuous",
            justification=["The supplied family is not a basis for the codomain topology, so the basis criterion cannot be applied honestly."],
            metadata={"criterion": "basis", "map_name": getattr(map_obj, "name", "f")},
        )
    graph = _graph_dict(map_obj)
    dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
    verdict = all(_preimage(graph, set(member)) in dom_open_sets for member in basis_list)
    return _exact_result(map_obj, "continuous", verdict, "Apply the Chapter 06 basis criterion to the supplied codomain basis family.")


def continuity_via_codomain_subbasis(map_obj: SymbolicMap, subbasis_family: Iterable[Iterable[Any]]) -> Result:
    if not _can_do_exact_finite_map_analysis(map_obj):
        return Result.unknown(
            mode="symbolic",
            value="continuous",
            justification=["Subbasis-level continuity checks are currently exact only for explicit finite maps."],
            metadata={"criterion": "subbasis", "map_name": getattr(map_obj, "name", "f")},
        )
    subbasis_list = list(subbasis_family)
    codomain_carrier = getattr(map_obj.codomain, "carrier", ())
    generated = generate_topology_from_subbasis(codomain_carrier, subbasis_list)
    if _normalize_family(getattr(generated, "topology", ())) != _normalize_family(getattr(map_obj.codomain, "topology", ())):
        return Result.false(
            mode="exact",
            value="continuous",
            justification=["The supplied family does not generate the codomain topology, so the subbasis criterion cannot be applied honestly."],
            metadata={"criterion": "subbasis", "map_name": getattr(map_obj, "name", "f")},
        )
    graph = _graph_dict(map_obj)
    dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
    verdict = all(_preimage(graph, set(member)) in dom_open_sets for member in subbasis_list)
    return _exact_result(map_obj, "continuous", verdict, "Apply the Chapter 06 subbasis criterion to the supplied codomain subbasis family.")


def satisfies_closure_image_inclusion(map_obj: SymbolicMap, subset: Iterable[Any]) -> Result:
    if not _can_do_exact_finite_map_analysis(map_obj):
        return Result.unknown(
            mode="symbolic",
            value="closure_image_inclusion",
            justification=["Closure-image checks are currently exact only for explicit finite maps."],
            metadata={"map_name": getattr(map_obj, "name", "f")},
        )
    subset_set = set(subset)
    dom_closure = closure_of_subset(map_obj.domain, subset_set)
    if dom_closure.value is None:
        return Result.unknown(
            mode="exact",
            value="closure_image_inclusion",
            justification=["Could not compute the closure of the subset in the domain."],
            metadata={"map_name": getattr(map_obj, "name", "f")},
        )
    image_closure = image_of_subset(map_obj, dom_closure.value)
    image_subset = image_of_subset(map_obj, subset_set)
    cod_closure = closure_of_subset(map_obj.codomain, image_subset)
    if cod_closure.value is None:
        return Result.unknown(
            mode="exact",
            value="closure_image_inclusion",
            justification=["Could not compute the closure of the image subset in the codomain."],
            metadata={"map_name": getattr(map_obj, "name", "f")},
        )
    verdict = image_closure.issubset(set(cod_closure.value))
    cls = Result.true if verdict else Result.false
    return cls(
        mode="exact",
        value="closure_image_inclusion",
        justification=["Computed exactly whether f(cl(A)) is contained in cl(f(A)) for the supplied finite subset."],
        proof_outline=["Use Chapter 05 closure operators on both domain and codomain and compare the resulting explicit subsets."],
        metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "subset": sorted(subset_set, key=repr)},
    )


def initial_topology_from_maps(
    carrier: Iterable[Any],
    maps: Iterable[FiniteMap],
    *,
    name: str = "initial_topology",
    description: str | None = None,
) -> FiniteTopologicalSpace:
    carrier_set = set(carrier)
    maps = list(maps)
    if not maps:
        raise ValueError("initial_topology_from_maps requires at least one explicit finite map.")
    subbasis: list[set[Any]] = []
    defining_names: list[str] = []
    for map_obj in maps:
        if not _can_do_exact_finite_map_analysis(map_obj):
            raise ValueError("initial_topology_from_maps requires explicit finite maps with explicit domain/codomain topologies.")
        domain_points = set(getattr(map_obj.domain, "carrier", ()))
        if domain_points != carrier_set:
            raise ValueError("All defining maps must have the same finite domain carrier as the requested initial topology.")
        defining_names.append(getattr(map_obj, "name", "f"))
        codomain_open_sets = _normalize_family(getattr(map_obj.codomain, "topology", ()))
        for open_set in codomain_open_sets:
            subbasis.append(set(preimage_of_subset(map_obj, set(open_set))))
    space = generate_topology_from_subbasis(
        carrier_set,
        subbasis,
        description=description or "The coarsest topology making the supplied maps continuous.",
    )
    space.metadata.update({"construction": "initial_topology_from_maps", "name": name, "defining_maps": defining_names})
    space.add_tags("initial-topology", "continuity-generated")
    return space


__all__ = [
    "is_continuous_at_point",
    "is_sequentially_continuous_at_point",
    "continuity_via_codomain_basis",
    "continuity_via_codomain_subbasis",
    "satisfies_closure_image_inclusion",
    "initial_topology_from_maps",
]
