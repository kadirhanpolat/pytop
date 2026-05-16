"""Unified map support for finite, infinite, and symbolic settings.

This module bridges the exact finite-space layer with the symbolic/theorem-based
infinite map layer. The main entry point is :func:`analyze_map_property`, which
returns a structured :class:`pytop.result.Result` describing both the answer and
how it was obtained.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Any

from .infinite_maps import (
    ConstantMap,
    ContinuousMap,
    EmbeddingMap,
    HomeomorphismMap,
    QuotientMap,
    SymbolicMap,
    analyze_infinite_map_property,
    compose_maps,
)
from .infinite_maps import (
    identity_map as symbolic_identity_map,
)
from .result import Result
from .subbases import generate_topology_from_subbasis, is_basis_for_topology
from .subset_operators import closure_of_subset

MAP_PROPERTIES = {
    "continuous",
    "open",
    "closed",
    "injective",
    "surjective",
    "bijective",
    "embedding",
    "quotient",
    "homeomorphism",
}


@dataclass
class FiniteMap(SymbolicMap):
    """Explicit map between finite topological spaces.

    Parameters
    ----------
    mapping:
        Either a dictionary on the carrier of the domain or a callable that can
        be evaluated on each point of the finite carrier.
    """

    mapping: dict[Any, Any] | Callable[[Any], Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.metadata["representation"] = "finite_map"
        self.add_tags("finite_map")
        if _space_is_finite(self.domain) and _space_is_finite(self.codomain):
            self.add_tags("finite")

    def image_of_point(self, point: Any) -> Any:
        if callable(self.mapping):
            return self.mapping(point)
        return self.mapping[point]

    def graph_dict(self) -> dict[Any, Any]:
        if callable(self.mapping):
            return {x: self.mapping(x) for x in getattr(self.domain, "carrier", [])}
        return dict(self.mapping)


def normalize_map_property(name: str) -> str:
    normalized = str(name).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "one_to_one": "injective",
        "onto": "surjective",
        "quotient_map": "quotient",
        "open_map": "open",
        "closed_map": "closed",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in MAP_PROPERTIES:
        raise ValueError(f"Unsupported map property {name!r}. Expected one of {sorted(MAP_PROPERTIES)}.")
    return normalized


def analyze_map_property(map_obj: SymbolicMap, property_name: str = "continuous") -> Result:
    property_name = normalize_map_property(property_name)
    if _can_do_exact_finite_map_analysis(map_obj):
        exact = _analyze_finite_map_property(map_obj, property_name)
        if exact is not None:
            return exact
    return analyze_infinite_map_property(map_obj, property_name)


def is_continuous_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "continuous")


def is_open_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "open")


def is_closed_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "closed")


def is_injective_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "injective")


def is_surjective_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "surjective")


def is_bijective_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "bijective")


def is_embedding_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "embedding")


def is_quotient_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "quotient")


def is_homeomorphism_map(map_obj: SymbolicMap) -> Result:
    return analyze_map_property(map_obj, "homeomorphism")


def map_report(map_obj: SymbolicMap) -> dict[str, Result]:
    return {name: analyze_map_property(map_obj, name) for name in sorted(MAP_PROPERTIES)}


def identity_map(space: Any, *, name: str = "id") -> SymbolicMap:
    if _space_is_finite(space):
        carrier = tuple(getattr(space, "carrier", ()))
        return FiniteMap(domain=space, codomain=space, name=name, mapping={x: x for x in carrier}, metadata={"description": "Identity map."}, tags={"continuous", "open", "closed", "bijective", "injective", "surjective", "embedding", "quotient", "homeomorphism"})
    return symbolic_identity_map(space, name=name)


def preimage_of_subset(map_obj: SymbolicMap, subset: Iterable[Any]) -> set[Any]:
    subset_set = set(subset)
    if _can_do_exact_finite_map_analysis(map_obj):
        graph = _graph_dict(map_obj)
        return {x for x, y in graph.items() if y in subset_set}
    raise ValueError("Exact preimage computation requires a finite explicit map.")


def image_of_subset(map_obj: SymbolicMap, subset: Iterable[Any]) -> set[Any]:
    subset_set = set(subset)
    if _can_do_exact_finite_map_analysis(map_obj):
        graph = _graph_dict(map_obj)
        return {graph[x] for x in subset_set}
    raise ValueError("Exact image computation requires a finite explicit map.")




def is_continuous_at_point(map_obj: SymbolicMap, point: Any) -> Result:
    if _can_do_exact_finite_map_analysis(map_obj):
        graph = _graph_dict(map_obj)
        dom_points = tuple(getattr(map_obj.domain, "carrier", ()))
        dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
        cod_open_sets = _normalize_family(getattr(map_obj.codomain, "topology", ()))
        if point not in dom_points:
            return Result.false(
                mode="exact",
                value="continuous_at_point",
                justification=["The requested point does not belong to the explicit finite domain carrier."],
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
    if not is_basis_for_topology(map_obj.codomain, basis_family):
        return Result.false(
            mode="exact",
            value="continuous",
            justification=["The supplied family is not a basis for the codomain topology, so the basis criterion cannot be applied honestly."],
            metadata={"criterion": "basis", "map_name": getattr(map_obj, "name", "f")},
        )
    graph = _graph_dict(map_obj)
    dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
    verdict = all(_preimage(graph, set(member)) in dom_open_sets for member in basis_family)
    return _exact_result(map_obj, "continuous", verdict, "Apply the Chapter 06 basis criterion to the supplied codomain basis family.")



def continuity_via_codomain_subbasis(map_obj: SymbolicMap, subbasis_family: Iterable[Iterable[Any]]) -> Result:
    if not _can_do_exact_finite_map_analysis(map_obj):
        return Result.unknown(
            mode="symbolic",
            value="continuous",
            justification=["Subbasis-level continuity checks are currently exact only for explicit finite maps."],
            metadata={"criterion": "subbasis", "map_name": getattr(map_obj, "name", "f")},
        )
    codomain_carrier = getattr(map_obj.codomain, "carrier", ())
    generated = generate_topology_from_subbasis(codomain_carrier, subbasis_family)
    if _normalize_family(getattr(generated, "topology", ())) != _normalize_family(getattr(map_obj.codomain, "topology", ())):
        return Result.false(
            mode="exact",
            value="continuous",
            justification=["The supplied family does not generate the codomain topology, so the subbasis criterion cannot be applied honestly."],
            metadata={"criterion": "subbasis", "map_name": getattr(map_obj, "name", "f")},
        )
    graph = _graph_dict(map_obj)
    dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
    verdict = all(_preimage(graph, set(member)) in dom_open_sets for member in subbasis_family)
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
    image_closure = image_of_subset(map_obj, dom_closure.value)
    image_subset = image_of_subset(map_obj, subset_set)
    cod_closure = closure_of_subset(map_obj.codomain, image_subset)
    verdict = set(image_closure).issubset(set(cod_closure.value))
    cls = Result.true if verdict else Result.false
    return cls(
        mode="exact",
        value="closure_image_inclusion",
        justification=["Computed exactly whether f(cl(A)) is contained in cl(f(A)) for the supplied finite subset."],
        proof_outline=["Use Chapter 05 closure operators on both domain and codomain and compare the resulting explicit subsets."],
        metadata={"representation": "finite_map", "map_name": getattr(map_obj, "name", "f"), "subset": sorted(subset_set, key=repr)},
    )



def initial_topology_from_maps(carrier: Iterable[Any], maps: Iterable[FiniteMap], *, name: str = "initial_topology", description: str | None = None) -> Any:
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


def map_taxonomy_profile(map_obj: SymbolicMap) -> dict[str, bool | None]:
    profile: dict[str, bool | None] = {}
    for name in ('continuous', 'open', 'closed', 'bijective', 'homeomorphism'):
        result = analyze_map_property(map_obj, name)
        if result.is_true:
            profile[name] = True
        elif result.is_false:
            profile[name] = False
        else:
            profile[name] = None
    return profile


def render_map_taxonomy_report(map_obj: SymbolicMap) -> str:
    profile = map_taxonomy_profile(map_obj)
    map_name = getattr(map_obj, 'name', 'f')
    lines = [
        f'Map taxonomy report for {map_name}',
        '',
    ]
    for key in ('continuous', 'open', 'closed', 'bijective', 'homeomorphism'):
        value = profile[key]
        status = 'yes' if value is True else 'no' if value is False else 'unknown'
        lines.append(f'- {key}: {status}')
    if profile['bijective'] and profile['continuous'] and not profile['homeomorphism']:
        lines.append('- warning-line: continuous bijection alone did not force homeomorphism.')
    if profile['open'] and profile['continuous'] is False:
        lines.append('- warning-line: openness did not imply continuity in this example.')
    return '\n'.join(lines)

def _can_do_exact_finite_map_analysis(map_obj: SymbolicMap) -> bool:
    return isinstance(map_obj, FiniteMap) and _space_is_finite(map_obj.domain) and _space_is_finite(map_obj.codomain) and hasattr(map_obj.domain, "topology") and hasattr(map_obj.codomain, "topology")


def _analyze_finite_map_property(map_obj: FiniteMap, property_name: str) -> Result | None:
    try:
        graph = _graph_dict(map_obj)
        dom_points = tuple(getattr(map_obj.domain, "carrier", ()))
        cod_points = tuple(getattr(map_obj.codomain, "carrier", ()))
        dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
        cod_open_sets = _normalize_family(getattr(map_obj.codomain, "topology", ()))
    except Exception:
        return None

    if set(graph) != set(dom_points):
        return Result.unknown(
            mode="symbolic",
            value=property_name,
            justification=["The explicit mapping does not cover the whole finite domain carrier."],
            metadata={"property": property_name, "representation": "finite_map"},
        )

    if property_name == "continuous":
        verdict = all(_preimage(graph, V) in dom_open_sets for V in cod_open_sets)
        return _exact_result(map_obj, property_name, verdict, "Check that the preimage of each open codomain set is open in the domain.")

    if property_name == "injective":
        values = [graph[x] for x in dom_points]
        verdict = len(set(values)) == len(values)
        return _exact_result(map_obj, property_name, verdict, "Compare the cardinality of the image multiset with the domain carrier.")

    if property_name == "surjective":
        verdict = {graph[x] for x in dom_points} == set(cod_points)
        return _exact_result(map_obj, property_name, verdict, "Check whether every codomain point is hit by the explicit map.")

    if property_name == "bijective":
        inj = _analyze_finite_map_property(map_obj, "injective")
        sur = _analyze_finite_map_property(map_obj, "surjective")
        verdict = bool(inj and sur and inj.is_true and sur.is_true)
        return _exact_result(map_obj, property_name, verdict, "A map is bijective exactly when it is both injective and surjective.")

    if property_name == "open":
        verdict = all(_image(graph, U) in cod_open_sets for U in dom_open_sets)
        return _exact_result(map_obj, property_name, verdict, "Check that the image of each open domain set is open in the codomain.")

    if property_name == "closed":
        dom_closed_sets = _closed_sets(dom_points, dom_open_sets)
        cod_closed_sets = _closed_sets(cod_points, cod_open_sets)
        verdict = all(_image(graph, F) in cod_closed_sets for F in dom_closed_sets)
        return _exact_result(map_obj, property_name, verdict, "Check that the image of each closed domain set is closed in the codomain.")

    if property_name == "embedding":
        cont = _analyze_finite_map_property(map_obj, "continuous")
        inj = _analyze_finite_map_property(map_obj, "injective")
        if not (cont and cont.is_true and inj and inj.is_true):
            return _exact_result(map_obj, property_name, False, "An embedding must at least be continuous and injective.")
        image_set = _image(graph, set(dom_points))
        subspace_opens = _subspace_topology(image_set, cod_open_sets)
        verdict = all(_image(graph, U) in subspace_opens for U in dom_open_sets)
        return _exact_result(map_obj, property_name, verdict, "Check openness of the map onto its image subspace.")

    if property_name == "homeomorphism":
        bij = _analyze_finite_map_property(map_obj, "bijective")
        cont = _analyze_finite_map_property(map_obj, "continuous")
        open_res = _analyze_finite_map_property(map_obj, "open")
        verdict = bool(bij and cont and open_res and bij.is_true and cont.is_true and open_res.is_true)
        return _exact_result(map_obj, property_name, verdict, "A bijective continuous open map is a homeomorphism.")

    if property_name == "quotient":
        sur = _analyze_finite_map_property(map_obj, "surjective")
        if not (sur and sur.is_true):
            return _exact_result(map_obj, property_name, False, "A quotient map must be surjective.")
        verdict = _is_quotient_via_open_set_criterion(graph, dom_open_sets, cod_open_sets, cod_points)
        return _exact_result(map_obj, property_name, verdict, "For a surjective map, a subset of the codomain is open iff its preimage is open in the domain.")

    return None


def _graph_dict(map_obj: FiniteMap) -> dict[Any, Any]:
    return map_obj.graph_dict()


def _preimage(graph: dict[Any, Any], subset: set[Any]) -> frozenset[Any]:
    return frozenset({x for x, y in graph.items() if y in subset})


def _image(graph: dict[Any, Any], subset: Iterable[Any]) -> frozenset[Any]:
    subset_set = set(subset)
    return frozenset({graph[x] for x in subset_set})


def _closed_sets(points: Iterable[Any], open_sets: set[frozenset[Any]]) -> set[frozenset[Any]]:
    carrier = set(points)
    return {frozenset(carrier - set(U)) for U in open_sets}


def _subspace_topology(subset: set[Any], ambient_open_sets: set[frozenset[Any]]) -> set[frozenset[Any]]:
    return {frozenset(set(U) & subset) for U in ambient_open_sets}


def _is_quotient_via_open_set_criterion(graph: dict[Any, Any], domain_open_sets: set[frozenset[Any]], codomain_open_sets: set[frozenset[Any]], codomain_points: Iterable[Any]) -> bool:
    cod_carrier = list(codomain_points)
    for subset in _powerset(cod_carrier):
        subset_f = frozenset(subset)
        pre = _preimage(graph, set(subset_f))
        if (subset_f in codomain_open_sets) != (pre in domain_open_sets):
            return False
    return True


def _normalize_family(family: Iterable[Iterable[Any]]) -> set[frozenset[Any]]:
    return {frozenset(member) for member in family}


def _powerset(items: Iterable[Any]) -> list[set[Any]]:
    items = list(items)
    out: list[set[Any]] = []
    for mask in range(1 << len(items)):
        out.append({items[i] for i in range(len(items)) if mask & (1 << i)})
    return out


def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False


def _exact_result(map_obj: SymbolicMap, property_name: str, verdict: bool, proof_hint: str) -> Result:
    cls = Result.true if verdict else Result.false
    verdict_word = "satisfies" if verdict else "fails"
    return cls(
        mode="exact",
        value=property_name,
        justification=[f"The explicit finite map {verdict_word} {property_name}."],
        proof_outline=[proof_hint],
        metadata={
            "representation": "finite_map",
            "property": property_name,
            "map_name": getattr(map_obj, "name", "f"),
        },
    )


__all__ = [
    "MAP_PROPERTIES",
    "SymbolicMap",
    "ContinuousMap",
    "EmbeddingMap",
    "QuotientMap",
    "HomeomorphismMap",
    "ConstantMap",
    "FiniteMap",
    "normalize_map_property",
    "analyze_map_property",
    "is_continuous_map",
    "is_open_map",
    "is_closed_map",
    "is_injective_map",
    "is_surjective_map",
    "is_bijective_map",
    "is_embedding_map",
    "is_quotient_map",
    "is_homeomorphism_map",
    "map_report",
    "identity_map",
    "compose_maps",
    "preimage_of_subset",
    "image_of_subset",
    "is_continuous_at_point",
    "is_sequentially_continuous_at_point",
    "continuity_via_codomain_basis",
    "continuity_via_codomain_subbasis",
    "satisfies_closure_image_inclusion",
    "initial_topology_from_maps",
    "map_taxonomy_profile",
    "render_map_taxonomy_report",
]
