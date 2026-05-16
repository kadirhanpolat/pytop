"""Profile-based taxonomy for maps between metric spaces.

The helpers in this module deliberately classify only what can be certified
from explicit finite data, or what the caller records as symbolic metadata.
They are not a general analysis proof engine for arbitrary functions.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from math import isclose
from typing import Any

from .metric_spaces import MetricSpace, validate_metric

MetricMapping = Mapping[Any, Any] | Callable[[Any], Any]


@dataclass(frozen=True)
class MetricMapProfile:
    """A compact classification profile for one metric-space map."""

    name: str
    domain_name: str = "X"
    codomain_name: str = "Y"
    certification: str = "profile"
    lipschitz_constant: float | None = None
    similarity_ratio: float | None = None
    non_expansive: bool | None = None
    lipschitz: bool | None = None
    uniformly_continuous: bool | None = None
    continuous: bool | None = None
    isometry: bool | None = None
    similarity: bool | None = None
    bijective: bool | None = None
    homeomorphism: bool | None = None
    notes: tuple[str, ...] = field(default_factory=tuple)

    def taxonomy(self) -> dict[str, bool | None]:
        return {
            "non_expansive": self.non_expansive,
            "lipschitz": self.lipschitz,
            "uniformly_continuous": self.uniformly_continuous,
            "continuous": self.continuous,
            "isometry": self.isometry,
            "similarity": self.similarity,
            "bijective": self.bijective,
            "homeomorphism": self.homeomorphism,
        }


def classify_finite_metric_map(
    domain: MetricSpace,
    codomain: MetricSpace,
    mapping: MetricMapping,
    *,
    name: str = "f",
    tolerance: float = 1e-12,
) -> MetricMapProfile:
    """Classify an explicit map between finite metric spaces.

    Finite metric spaces are discrete, so every explicit map between them is
    continuous and uniformly continuous. Lipschitz, non-expansive, isometry,
    similarity, bijectivity, and homeomorphism are certified by enumeration.
    """

    domain_points = _finite_carrier(domain, "domain")
    codomain_points = _finite_carrier(codomain, "codomain")
    _require_valid_metric(domain, "domain", tolerance)
    _require_valid_metric(codomain, "codomain", tolerance)
    graph = _normalize_graph(domain_points, codomain_points, mapping)
    lipschitz_constant = _finite_lipschitz_constant(domain, codomain, graph, domain_points)
    non_expansive = lipschitz_constant <= 1.0 + tolerance
    isometry = _preserves_all_distances(domain, codomain, graph, domain_points, tolerance)
    similarity_ratio = _finite_similarity_ratio(domain, codomain, graph, domain_points, tolerance)
    similarity = similarity_ratio is not None
    values = tuple(graph[x] for x in domain_points)
    bijective = len(set(values)) == len(values) and set(values) == set(codomain_points)
    homeomorphism = bijective
    notes = (
        "Exact finite certification by carrier enumeration.",
        "Finite metric spaces are discrete, so every explicit finite map is continuous and uniformly continuous.",
        "No claim is made for arbitrary implicit functions beyond this finite profile.",
    )
    return MetricMapProfile(
        name=name,
        domain_name=_space_name(domain, "X"),
        codomain_name=_space_name(codomain, "Y"),
        certification="exact-finite",
        lipschitz_constant=lipschitz_constant,
        similarity_ratio=similarity_ratio,
        non_expansive=non_expansive,
        lipschitz=True,
        uniformly_continuous=True,
        continuous=True,
        isometry=isometry,
        similarity=similarity,
        bijective=bijective,
        homeomorphism=homeomorphism,
        notes=notes,
    )


def metric_map_profile(
    *,
    name: str = "f",
    domain_name: str = "X",
    codomain_name: str = "Y",
    non_expansive: bool | None = None,
    lipschitz: bool | None = None,
    uniformly_continuous: bool | None = None,
    continuous: bool | None = None,
    isometry: bool | None = None,
    similarity: bool | None = None,
    bijective: bool | None = None,
    homeomorphism: bool | None = None,
    lipschitz_constant: float | None = None,
    similarity_ratio: float | None = None,
    notes: tuple[str, ...] | list[str] = (),
) -> MetricMapProfile:
    """Record a symbolic metric-map taxonomy without inventing proofs."""

    derived_notes = [
        "Symbolic/profile entry: unspecified classifications remain unknown.",
        "Use classify_finite_metric_map for exact finite certification.",
    ]
    return MetricMapProfile(
        name=name,
        domain_name=domain_name,
        codomain_name=codomain_name,
        certification="symbolic-profile",
        lipschitz_constant=lipschitz_constant,
        similarity_ratio=similarity_ratio,
        non_expansive=non_expansive,
        lipschitz=lipschitz,
        uniformly_continuous=uniformly_continuous,
        continuous=continuous,
        isometry=isometry,
        similarity=similarity,
        bijective=bijective,
        homeomorphism=homeomorphism,
        notes=tuple(notes) + tuple(derived_notes),
    )


def render_metric_map_taxonomy(profile: MetricMapProfile) -> str:
    """Render a short text report for a metric-map profile."""

    def label(value: bool | None) -> str:
        if value is True:
            return "yes"
        if value is False:
            return "no"
        return "unknown"

    lines = [
        f"Metric map taxonomy for {profile.name}: {profile.domain_name} -> {profile.codomain_name}",
        f"certification: {profile.certification}",
    ]
    if profile.lipschitz_constant is not None:
        lines.append(f"lipschitz_constant: {profile.lipschitz_constant:g}")
    if profile.similarity_ratio is not None:
        lines.append(f"similarity_ratio: {profile.similarity_ratio:g}")
    for key, value in profile.taxonomy().items():
        lines.append(f"- {key}: {label(value)}")
    for note in profile.notes:
        lines.append(f"note: {note}")
    return "\n".join(lines)


def _finite_carrier(space: MetricSpace, role: str) -> tuple[Any, ...]:
    carrier = getattr(space, "carrier", None)
    try:
        points = tuple(carrier)
    except TypeError as exc:
        raise ValueError(f"The {role} metric space must have an explicit finite carrier.") from exc
    if not points and carrier is None:
        raise ValueError(f"The {role} metric space must have an explicit finite carrier.")
    return points


def _require_valid_metric(space: MetricSpace, role: str, tolerance: float) -> None:
    validation = validate_metric(space, tolerance=tolerance)
    if validation.is_false:
        raise ValueError(f"The {role} distance data failed finite metric validation.")
    if validation.is_unknown:
        raise ValueError(f"The {role} metric space is not explicitly finite enough for certification.")


def _normalize_graph(
    domain_points: tuple[Any, ...],
    codomain_points: tuple[Any, ...],
    mapping: MetricMapping,
) -> dict[Any, Any]:
    if callable(mapping):
        graph = {x: mapping(x) for x in domain_points}
    else:
        graph = dict(mapping)
    if set(graph) != set(domain_points):
        raise ValueError("The mapping must define exactly one image for every domain point.")
    codomain_set = set(codomain_points)
    if any(y not in codomain_set for y in graph.values()):
        raise ValueError("Every image point must belong to the codomain carrier.")
    return graph


def _finite_lipschitz_constant(
    domain: MetricSpace,
    codomain: MetricSpace,
    graph: dict[Any, Any],
    domain_points: tuple[Any, ...],
) -> float:
    ratios: list[float] = []
    for x in domain_points:
        for y in domain_points:
            dx = domain.distance_between(x, y)
            if dx > 0:
                ratios.append(codomain.distance_between(graph[x], graph[y]) / dx)
    return max(ratios, default=0.0)


def _preserves_all_distances(
    domain: MetricSpace,
    codomain: MetricSpace,
    graph: dict[Any, Any],
    domain_points: tuple[Any, ...],
    tolerance: float,
) -> bool:
    return all(
        isclose(
            domain.distance_between(x, y),
            codomain.distance_between(graph[x], graph[y]),
            rel_tol=tolerance,
            abs_tol=tolerance,
        )
        for x in domain_points
        for y in domain_points
    )


def _finite_similarity_ratio(
    domain: MetricSpace,
    codomain: MetricSpace,
    graph: dict[Any, Any],
    domain_points: tuple[Any, ...],
    tolerance: float,
) -> float | None:
    ratios = []
    for x in domain_points:
        for y in domain_points:
            dx = domain.distance_between(x, y)
            if dx > 0:
                ratios.append(codomain.distance_between(graph[x], graph[y]) / dx)
    if not ratios:
        return 1.0
    candidate = ratios[0]
    if candidate <= tolerance:
        return None
    if all(isclose(ratio, candidate, rel_tol=tolerance, abs_tol=tolerance) for ratio in ratios):
        return candidate
    return None


def _space_name(space: MetricSpace, default: str) -> str:
    metadata = getattr(space, "metadata", {})
    return str(metadata.get("name") or metadata.get("description") or default)


__all__ = [
    "MetricMapProfile",
    "MetricMapping",
    "classify_finite_metric_map",
    "metric_map_profile",
    "render_metric_map_taxonomy",
]
