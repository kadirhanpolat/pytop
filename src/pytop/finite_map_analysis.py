"""Core finite-map types, property analysis engine, and map builders.

This module contains:
- :class:`FiniteMap` — explicit finite map between topological spaces
- The central dispatcher :func:`analyze_map_property` and property wrappers
- Map-algebra helpers (preimage, image, restriction, fixed points, inverse)
- Builder functions (make_function, identity_function, constant_function)
- Taxonomy / reporting utilities
- All private finite-analysis helpers

Pointwise continuity and criterion-based checks live in
:mod:`pytop.map_continuity`.  The legacy entry point :mod:`pytop.maps`
re-exports everything from both modules.
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

MAP_PROPERTIES: frozenset[str] = frozenset({
    "continuous",
    "open",
    "closed",
    "injective",
    "surjective",
    "bijective",
    "embedding",
    "quotient",
    "homeomorphism",
})


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


_MAP_PROPERTY_ALIASES: dict[str, str] = {
    "one_to_one": "injective",
    "onto": "surjective",
    "quotient_map": "quotient",
    "open_map": "open",
    "closed_map": "closed",
}


def normalize_map_property(name: str) -> str:
    normalized = str(name).strip().lower().replace("-", "_").replace(" ", "_")
    normalized = _MAP_PROPERTY_ALIASES.get(normalized, normalized)
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
        return FiniteMap(
            domain=space,
            codomain=space,
            name=name,
            mapping={x: x for x in carrier},
            metadata={"description": "Identity map."},
            tags={"continuous", "open", "closed", "bijective", "injective", "surjective", "embedding", "quotient", "homeomorphism"},
        )
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
        missing = subset_set - graph.keys()
        if missing:
            raise ValueError(f"image_of_subset: points {sorted(missing, key=repr)} are not in the domain carrier.")
        return {graph[x] for x in subset_set}
    raise ValueError("Exact image computation requires a finite explicit map.")


def restriction_of_map(map_obj: FiniteMap, domain_subset: Iterable[Any]) -> FiniteMap:
    """Return f|_A : A → codomain with the subspace topology on A."""
    from .finite_spaces import FiniteTopologicalSpace

    graph = _graph_dict(map_obj)
    dom_points = set(getattr(map_obj.domain, "carrier", graph.keys()))
    sub = frozenset(domain_subset)
    if not sub.issubset(dom_points):
        raise ValueError("domain_subset must be contained in the domain carrier.")
    dom_topology: frozenset[Any] = getattr(map_obj.domain, "topology", frozenset())
    subspace_topology = frozenset(frozenset(set(U) & sub) for U in dom_topology)
    sub_space = FiniteTopologicalSpace(carrier=sub, topology=subspace_topology)
    return FiniteMap(domain=sub_space, codomain=map_obj.codomain, mapping={x: graph[x] for x in sub})


def fixed_points_of_map(map_obj: FiniteMap) -> frozenset[Any]:
    """Return {x ∈ domain : f(x) = x}."""
    graph = _graph_dict(map_obj)
    return frozenset(x for x, y in graph.items() if x == y)


def inverse_map(map_obj: FiniteMap) -> FiniteMap:
    """Return f⁻¹ : codomain → domain for a bijective *map_obj*.

    Raises
    ------
    ValueError
        If the map is not bijective or the codomain has no explicit carrier.
    """
    graph = _graph_dict(map_obj)
    raw_carrier = getattr(map_obj.codomain, "carrier", None)
    if raw_carrier is None:
        raise ValueError("inverse_map requires a codomain with an explicit carrier attribute.")
    cod_carrier = frozenset(raw_carrier)
    values = list(graph.values())
    if not (len(set(values)) == len(values) and set(values) == set(cod_carrier)):
        raise ValueError("inverse_map requires a bijective finite map.")
    return FiniteMap(domain=map_obj.codomain, codomain=map_obj.domain, mapping={y: x for x, y in graph.items()})


def compose_finite_maps(f: FiniteMap, g: FiniteMap) -> FiniteMap:
    """Return g ∘ f : dom(f) → cod(g) as a FiniteMap.

    Requires that the codomain carrier of *f* equals the domain carrier of *g*.

    Raises
    ------
    ValueError
        If the carriers are incompatible or either map lacks an explicit carrier.
    """
    f_graph = _graph_dict(f)
    g_graph = _graph_dict(g)
    f_cod_raw = getattr(f.codomain, "carrier", None)
    g_dom_raw = getattr(g.domain, "carrier", None)
    if f_cod_raw is None or g_dom_raw is None:
        raise ValueError("compose_finite_maps requires both maps to have explicit carrier attributes on their domain/codomain.")
    f_cod = frozenset(f_cod_raw)
    g_dom = frozenset(g_dom_raw)
    if f_cod != g_dom:
        raise ValueError(
            "compose_finite_maps: codomain of f must equal domain of g. "
            f"Got f.codomain.carrier={sorted(f_cod, key=repr)}, g.domain.carrier={sorted(g_dom, key=repr)}."
        )
    missing_in_g = set(f_graph.values()) - g_graph.keys()
    if missing_in_g:
        raise ValueError(
            f"compose_finite_maps: f maps to points {sorted(missing_in_g, key=repr)} "
            "that are not covered by g's mapping. Both maps must be total."
        )
    composed_mapping = {x: g_graph[f_graph[x]] for x in f_graph}
    return FiniteMap(
        domain=f.domain,
        codomain=g.codomain,
        mapping=composed_mapping,
        name=f"{getattr(g, 'name', 'g')}∘{getattr(f, 'name', 'f')}",
        metadata={"description": f"Composition of {getattr(f, 'name', 'f')} followed by {getattr(g, 'name', 'g')}."},
    )


def map_taxonomy_profile(map_obj: SymbolicMap) -> dict[str, bool | None]:
    profile: dict[str, bool | None] = {}
    for name in ("continuous", "open", "closed", "bijective", "homeomorphism"):
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
    map_name = getattr(map_obj, "name", "f")
    lines = [f"Map taxonomy report for {map_name}", ""]
    for key in ("continuous", "open", "closed", "bijective", "homeomorphism"):
        value = profile[key]
        status = "yes" if value is True else "no" if value is False else "unknown"
        lines.append(f"- {key}: {status}")
    if profile["bijective"] and profile["continuous"] and not profile["homeomorphism"]:
        lines.append("- warning-line: continuous bijection alone did not force homeomorphism.")
    if profile["open"] and profile["continuous"] is False:
        lines.append("- warning-line: openness did not imply continuity in this example.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Map builder functions
# ---------------------------------------------------------------------------

class MapBuilderError(ValueError):
    """Raised when a map builder receives invalid arguments."""


def make_function(
    domain_elements: Iterable[Any],
    codomain_elements: Iterable[Any],
    mapping: dict[Any, Any],
) -> FiniteMap:
    """Build a finite function from element sets and a mapping dictionary."""
    from .spaces import TopologicalSpace

    d = frozenset(domain_elements)
    c = frozenset(codomain_elements)
    mapping_keys = frozenset(mapping)
    if not mapping_keys.issubset(d):
        raise MapBuilderError("Mapping keys must be elements of the domain.")
    if not d.issubset(mapping_keys):
        missing = sorted(d - mapping_keys, key=repr)
        raise MapBuilderError(f"make_function requires a total function; domain points {missing} have no mapping value.")
    if not frozenset(mapping.values()).issubset(c):
        raise MapBuilderError("Mapping values must be elements of the codomain.")
    return FiniteMap(domain=TopologicalSpace(carrier=d), codomain=TopologicalSpace(carrier=c), mapping=dict(mapping))


def identity_function(elements: Iterable[Any]) -> FiniteMap:
    """Build the identity function on the given elements."""
    from .spaces import TopologicalSpace

    x = frozenset(elements)
    space = TopologicalSpace(carrier=x)
    return FiniteMap(
        domain=space,
        codomain=space,
        mapping={e: e for e in x},
        tags={"injective", "surjective", "bijective", "homeomorphism"},
    )


def constant_function(
    domain_elements: Iterable[Any],
    codomain_elements: Iterable[Any],
    value: Any,
) -> FiniteMap:
    """Build a constant function mapping every domain element to *value*."""
    from .spaces import TopologicalSpace

    d = frozenset(domain_elements)
    c = frozenset(codomain_elements)
    if value not in c:
        raise MapBuilderError("The constant value must be an element of the codomain.")
    return FiniteMap(domain=TopologicalSpace(carrier=d), codomain=TopologicalSpace(carrier=c), mapping={e: value for e in d})


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _can_do_exact_finite_map_analysis(map_obj: SymbolicMap) -> bool:
    return (
        isinstance(map_obj, FiniteMap)
        and _space_is_finite(map_obj.domain)
        and _space_is_finite(map_obj.codomain)
        and hasattr(map_obj.domain, "topology")
        and hasattr(map_obj.codomain, "topology")
    )


def _analyze_finite_map_property(map_obj: Any, property_name: str) -> Result | None:
    try:
        graph = _graph_dict(map_obj)
        dom_points = tuple(getattr(map_obj.domain, "carrier", ()))
        cod_points = tuple(getattr(map_obj.codomain, "carrier", ()))
        dom_open_sets = _normalize_family(getattr(map_obj.domain, "topology", ()))
        cod_open_sets = _normalize_family(getattr(map_obj.codomain, "topology", ()))
    except Exception:  # noqa: BLE001 — callable mappings can raise anything; fall through to symbolic engine
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
        verdict = _is_quotient_via_open_set_criterion(graph, dom_open_sets, cod_open_sets)
        return _exact_result(map_obj, property_name, verdict, "For a surjective map, a subset of the codomain is open iff its preimage is open in the domain.")

    return None


def _graph_dict(map_obj: Any) -> dict[Any, Any]:
    return map_obj.graph_dict()


def _preimage(graph: dict[Any, Any], subset: set[Any] | frozenset[Any]) -> frozenset[Any]:
    return frozenset({x for x, y in graph.items() if y in subset})


def _image(graph: dict[Any, Any], subset: Iterable[Any]) -> frozenset[Any]:
    subset_set = set(subset)
    return frozenset({graph[x] for x in subset_set})


def _closed_sets(points: Iterable[Any], open_sets: set[frozenset[Any]]) -> set[frozenset[Any]]:
    carrier = set(points)
    return {frozenset(carrier - set(U)) for U in open_sets}


def _subspace_topology(subset: set[Any] | frozenset[Any], ambient_open_sets: set[frozenset[Any]]) -> set[frozenset[Any]]:
    return {frozenset(set(U) & subset) for U in ambient_open_sets}


def _is_quotient_via_open_set_criterion(
    graph: dict[Any, Any],
    domain_open_sets: set[frozenset[Any]],
    codomain_open_sets: set[frozenset[Any]],
) -> bool:
    # O(|τ_Y| + |τ_X|) quotient criterion: surjective + continuous + saturated opens map open.
    for U in codomain_open_sets:
        if frozenset(x for x, y in graph.items() if y in U) not in domain_open_sets:
            return False
    for V in domain_open_sets:
        fV = frozenset(graph[x] for x in V if x in graph)
        pre_fV = frozenset(x for x, y in graph.items() if y in fV)
        if pre_fV == V and fV not in codomain_open_sets:
            return False
    return True


def _normalize_family(family: Iterable[Iterable[Any]]) -> set[frozenset[Any]]:
    return {frozenset(member) for member in family}


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
        metadata={"representation": "finite_map", "property": property_name, "map_name": getattr(map_obj, "name", "f")},
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
    "restriction_of_map",
    "fixed_points_of_map",
    "inverse_map",
    "compose_finite_maps",
    "map_taxonomy_profile",
    "render_map_taxonomy_report",
    "MapBuilderError",
    "make_function",
    "identity_function",
    "constant_function",
]
