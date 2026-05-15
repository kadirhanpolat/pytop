"""Retracts, absolute retracts, and ANR teaching profiles.

This module is part of the geometric topology bridge for route ``GEO-08``.
It records conservative profile data about retracts, deformation retracts,
absolute retracts (AR), and absolute neighbourhood retracts (ANR).  The module
is intentionally not a general decision procedure: unknown cases remain
explicitly unknown, and registered examples carry their certification notes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .homotopy import DeformationRetractionProfile, deformation_retraction_profile


class RetractProfileError(ValueError):
    """Raised when retract/AR/ANR profile metadata is malformed."""


RETRACT_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "not_certified", "unknown"})
AR_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "not_certified", "unknown"})
ANR_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "not_certified", "unknown"})


def _normalize_status(status: str, allowed: frozenset[str], label: str) -> str:
    value = str(status).strip().lower().replace("-", "_")
    if value not in allowed:
        raise RetractProfileError(f"Unsupported {label} status: {status!r}.")
    return value


def _as_tuple(items: Iterable[Any]) -> tuple[str, ...]:
    return tuple(str(item) for item in items)


@dataclass(frozen=True)
class RetractionProfile:
    """A conservative profile for a retraction ``r: X -> A`` with ``r|A = id_A``."""

    name: str
    space: Any
    subspace: Any
    status: str = "unknown"
    retraction_label: str = ""
    inclusion_label: str = ""
    fixed_on_subspace: bool | None = None
    deformation_available: bool | None = None
    strong_deformation: bool | None = None
    homotopy_equivalence_hint: str = ""
    certification: str = "profile"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        if not name:
            raise RetractProfileError("A retraction profile needs a nonempty name.")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "status", _normalize_status(self.status, RETRACT_PROFILE_STATUSES, "retraction"))
        object.__setattr__(self, "retraction_label", str(self.retraction_label))
        object.__setattr__(self, "inclusion_label", str(self.inclusion_label))
        object.__setattr__(self, "homotopy_equivalence_hint", str(self.homotopy_equivalence_hint))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "warnings", _as_tuple(self.warnings))
        object.__setattr__(self, "related_profiles", _as_tuple(self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified(self) -> bool:
        return self.status == "certified"

    @property
    def is_unknown(self) -> bool:
        return self.status == "unknown"

    @property
    def is_deformation_retract(self) -> bool:
        return self.deformation_available is True


@dataclass(frozen=True)
class AbsoluteRetractProfile:
    """Profile for an absolute retract claim in a stated category."""

    name: str
    space: Any
    category: str = "metric_spaces"
    status: str = "unknown"
    local_contractibility_hint: str = ""
    contractibility_hint: str = ""
    extension_property_hint: str = ""
    certification: str = "profile"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        if not name:
            raise RetractProfileError("An AR profile needs a nonempty name.")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "category", str(self.category).strip() or "metric_spaces")
        object.__setattr__(self, "status", _normalize_status(self.status, AR_PROFILE_STATUSES, "absolute retract"))
        object.__setattr__(self, "local_contractibility_hint", str(self.local_contractibility_hint))
        object.__setattr__(self, "contractibility_hint", str(self.contractibility_hint))
        object.__setattr__(self, "extension_property_hint", str(self.extension_property_hint))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "warnings", _as_tuple(self.warnings))
        object.__setattr__(self, "related_profiles", _as_tuple(self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified_ar(self) -> bool:
        return self.status == "certified"


@dataclass(frozen=True)
class ANRProfile:
    """Profile for an absolute neighbourhood retract claim in a stated category."""

    name: str
    space: Any
    category: str = "metric_spaces"
    status: str = "unknown"
    neighbourhood_extension_hint: str = ""
    local_contractibility_hint: str = ""
    manifold_or_polyhedron_hint: str = ""
    certification: str = "profile"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        if not name:
            raise RetractProfileError("An ANR profile needs a nonempty name.")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "category", str(self.category).strip() or "metric_spaces")
        object.__setattr__(self, "status", _normalize_status(self.status, ANR_PROFILE_STATUSES, "ANR"))
        object.__setattr__(self, "neighbourhood_extension_hint", str(self.neighbourhood_extension_hint))
        object.__setattr__(self, "local_contractibility_hint", str(self.local_contractibility_hint))
        object.__setattr__(self, "manifold_or_polyhedron_hint", str(self.manifold_or_polyhedron_hint))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "warnings", _as_tuple(self.warnings))
        object.__setattr__(self, "related_profiles", _as_tuple(self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified_anr(self) -> bool:
        return self.status == "certified"


def retraction_profile(
    name: str,
    space: Any,
    subspace: Any,
    *,
    status: str = "unknown",
    retraction_label: str = "",
    inclusion_label: str = "",
    fixed_on_subspace: bool | None = None,
    deformation_available: bool | None = None,
    strong_deformation: bool | None = None,
    homotopy_equivalence_hint: str = "",
    certification: str = "profile",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> RetractionProfile:
    return RetractionProfile(
        name=name,
        space=space,
        subspace=subspace,
        status=status,
        retraction_label=retraction_label,
        inclusion_label=inclusion_label,
        fixed_on_subspace=fixed_on_subspace,
        deformation_available=deformation_available,
        strong_deformation=strong_deformation,
        homotopy_equivalence_hint=homotopy_equivalence_hint,
        certification=certification,
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=dict(metadata or {}),
    )


def certified_retraction_profile(name: str, space: Any, subspace: Any, **kwargs: Any) -> RetractionProfile:
    return retraction_profile(name, space, subspace, status="certified", fixed_on_subspace=True, **kwargs)


def unknown_retraction_profile(name: str, space: Any, subspace: Any, *, reason: str = "No retraction certificate is registered.") -> RetractionProfile:
    return retraction_profile(
        name,
        space,
        subspace,
        status="unknown",
        fixed_on_subspace=None,
        certification="unknown",
        warnings=(reason, "This is not a negative theorem; it only records absence of certification."),
    )


def not_certified_retraction_profile(name: str, space: Any, subspace: Any, *, reason: str = "The supplied data does not certify a retraction.") -> RetractionProfile:
    return retraction_profile(
        name,
        space,
        subspace,
        status="not_certified",
        fixed_on_subspace=False,
        certification="failed-profile-check",
        warnings=(reason,),
    )


def deformation_retract_profile(
    name: str,
    space: Any,
    subspace: Any,
    *,
    status: str = "not_certified",
    strong: bool = False,
    certification: str = "profile",
    notes: Iterable[str] = (),
) -> DeformationRetractionProfile:
    """Build a deformation-retraction profile by reusing the homotopy layer."""

    return deformation_retraction_profile(
        name=name,
        space=space,
        subspace=subspace,
        status=status,
        strong=strong,
        certification=certification,
        notes=tuple(notes),
    )


def absolute_retract_profile(
    name: str,
    space: Any,
    *,
    category: str = "metric_spaces",
    status: str = "unknown",
    local_contractibility_hint: str = "",
    contractibility_hint: str = "",
    extension_property_hint: str = "",
    certification: str = "profile",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> AbsoluteRetractProfile:
    return AbsoluteRetractProfile(
        name=name,
        space=space,
        category=category,
        status=status,
        local_contractibility_hint=local_contractibility_hint,
        contractibility_hint=contractibility_hint,
        extension_property_hint=extension_property_hint,
        certification=certification,
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=dict(metadata or {}),
    )


def anr_profile(
    name: str,
    space: Any,
    *,
    category: str = "metric_spaces",
    status: str = "unknown",
    neighbourhood_extension_hint: str = "",
    local_contractibility_hint: str = "",
    manifold_or_polyhedron_hint: str = "",
    certification: str = "profile",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> ANRProfile:
    return ANRProfile(
        name=name,
        space=space,
        category=category,
        status=status,
        neighbourhood_extension_hint=neighbourhood_extension_hint,
        local_contractibility_hint=local_contractibility_hint,
        manifold_or_polyhedron_hint=manifold_or_polyhedron_hint,
        certification=certification,
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=dict(metadata or {}),
    )


def point_ar_profile() -> AbsoluteRetractProfile:
    return absolute_retract_profile(
        "one_point_absolute_retract",
        "one_point_space",
        status="certified",
        contractibility_hint="trivial",
        extension_property_hint="constant extension",
        certification="standard-registered-example",
        related_profiles=("contractible", "finite_spaces"),
    )


def interval_ar_profile() -> AbsoluteRetractProfile:
    return absolute_retract_profile(
        "closed_interval_absolute_retract",
        "[0,1]",
        status="certified",
        local_contractibility_hint="locally contractible continuum",
        contractibility_hint="convex subset of R",
        extension_property_hint="standard convex metric example",
        certification="registered-standard-theorem",
        warnings=("The theorem is recorded as registry metadata; no proof engine is supplied.",),
        related_profiles=("continua", "euclidean_topology"),
    )


def disk_ar_profile() -> AbsoluteRetractProfile:
    return absolute_retract_profile(
        "closed_disk_absolute_retract",
        "D^n",
        status="certified",
        local_contractibility_hint="locally contractible",
        contractibility_hint="convex closed ball model",
        extension_property_hint="standard convex metric example",
        certification="registered-standard-theorem",
        warnings=("Dimension is metadata here; no arbitrary subset recognition is attempted.",),
        related_profiles=("euclidean_topology", "manifolds", "continua"),
    )


def finite_polyhedron_anr_profile() -> ANRProfile:
    return anr_profile(
        "finite_polyhedron_ANR",
        "finite_polyhedron",
        status="certified",
        neighbourhood_extension_hint="standard neighbourhood retract behaviour in metric embeddings",
        local_contractibility_hint="finite polyhedra are locally contractible in the registered model",
        manifold_or_polyhedron_hint="finite simplicial complex / polyhedron",
        certification="registered-standard-theorem",
        warnings=("This does not classify arbitrary complexes or embeddings.",),
        related_profiles=("simplicial_complexes", "polyhedra"),
    )


def topological_manifold_anr_profile() -> ANRProfile:
    return anr_profile(
        "topological_manifold_ANR_preview",
        "metric_topological_manifold",
        status="preview",
        neighbourhood_extension_hint="registered as a teaching preview for metrizable manifolds",
        local_contractibility_hint="local Euclidean model suggests local contractibility",
        manifold_or_polyhedron_hint="topological manifold profile",
        certification="preview-not-full-proof",
        warnings=("The package does not verify metrizability or atlas compatibility here.",),
        related_profiles=("manifolds", "surfaces"),
    )


def circle_anr_profile() -> ANRProfile:
    return anr_profile(
        "circle_S1_ANR",
        "S^1",
        status="certified",
        neighbourhood_extension_hint="standard compact polyhedron/manifold example",
        local_contractibility_hint="locally interval-like",
        manifold_or_polyhedron_hint="1-dimensional compact manifold and finite polyhedron",
        certification="registered-standard-example",
        related_profiles=("surfaces", "fundamental_group", "continua"),
    )


KNOWN_ABSOLUTE_RETRACT_PROFILES: Mapping[str, AbsoluteRetractProfile] = {
    "point": point_ar_profile(),
    "one_point": point_ar_profile(),
    "one_point_space": point_ar_profile(),
    "interval": interval_ar_profile(),
    "closed_interval": interval_ar_profile(),
    "unit_interval": interval_ar_profile(),
    "i": interval_ar_profile(),
    "disk": disk_ar_profile(),
    "closed_disk": disk_ar_profile(),
    "closed_ball": disk_ar_profile(),
    "d_n": disk_ar_profile(),
}


KNOWN_ANR_PROFILES: Mapping[str, ANRProfile] = {
    "finite_polyhedron": finite_polyhedron_anr_profile(),
    "polyhedron": finite_polyhedron_anr_profile(),
    "circle": circle_anr_profile(),
    "s1": circle_anr_profile(),
    "circle_s1": circle_anr_profile(),
    "topological_manifold": topological_manifold_anr_profile(),
    "metric_topological_manifold": topological_manifold_anr_profile(),
    "manifold": topological_manifold_anr_profile(),
}


def _key(text: str) -> str:
    return str(text).strip().lower().replace(" ", "_").replace("-", "_").replace("^", "")


def known_absolute_retract_profile(key: str) -> AbsoluteRetractProfile:
    profile = KNOWN_ABSOLUTE_RETRACT_PROFILES.get(_key(key))
    if profile is not None:
        return profile
    return absolute_retract_profile(
        f"{_key(key) or 'unknown'}_absolute_retract_unknown",
        str(key),
        status="unknown",
        certification="known-example-registry",
        warnings=("No registered AR claim for this key.", "Unknown is not a negative theorem."),
    )


def known_anr_profile(key: str) -> ANRProfile:
    profile = KNOWN_ANR_PROFILES.get(_key(key))
    if profile is not None:
        return profile
    return anr_profile(
        f"{_key(key) or 'unknown'}_ANR_unknown",
        str(key),
        status="unknown",
        certification="known-example-registry",
        warnings=("No registered ANR claim for this key.", "Unknown is not a negative theorem."),
    )


def retraction_summary(profile: RetractionProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "space": profile.space,
        "subspace": profile.subspace,
        "status": profile.status,
        "fixed_on_subspace": profile.fixed_on_subspace,
        "deformation_available": profile.deformation_available,
        "strong_deformation": profile.strong_deformation,
        "homotopy_equivalence_hint": profile.homotopy_equivalence_hint,
        "certification": profile.certification,
        "warnings": profile.warnings,
        "is_certified": profile.is_certified,
        "is_deformation_retract": profile.is_deformation_retract,
    }


def absolute_retract_summary(profile: AbsoluteRetractProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "space": profile.space,
        "category": profile.category,
        "status": profile.status,
        "local_contractibility_hint": profile.local_contractibility_hint,
        "contractibility_hint": profile.contractibility_hint,
        "extension_property_hint": profile.extension_property_hint,
        "certification": profile.certification,
        "warnings": profile.warnings,
        "is_certified_ar": profile.is_certified_ar,
    }


def anr_summary(profile: ANRProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "space": profile.space,
        "category": profile.category,
        "status": profile.status,
        "neighbourhood_extension_hint": profile.neighbourhood_extension_hint,
        "local_contractibility_hint": profile.local_contractibility_hint,
        "manifold_or_polyhedron_hint": profile.manifold_or_polyhedron_hint,
        "certification": profile.certification,
        "warnings": profile.warnings,
        "is_certified_anr": profile.is_certified_anr,
    }


def is_certified_retract(profile: RetractionProfile) -> bool:
    return profile.is_certified


def is_certified_absolute_retract(profile: AbsoluteRetractProfile) -> bool:
    return profile.is_certified_ar


def is_certified_anr(profile: ANRProfile) -> bool:
    return profile.is_certified_anr


__all__ = [
    "ANRProfile",
    "ANR_PROFILE_STATUSES",
    "AR_PROFILE_STATUSES",
    "AbsoluteRetractProfile",
    "DeformationRetractionProfile",
    "KNOWN_ABSOLUTE_RETRACT_PROFILES",
    "KNOWN_ANR_PROFILES",
    "RETRACT_PROFILE_STATUSES",
    "RetractProfileError",
    "RetractionProfile",
    "absolute_retract_profile",
    "absolute_retract_summary",
    "anr_profile",
    "anr_summary",
    "certified_retraction_profile",
    "circle_anr_profile",
    "deformation_retract_profile",
    "disk_ar_profile",
    "finite_polyhedron_anr_profile",
    "interval_ar_profile",
    "is_certified_absolute_retract",
    "is_certified_anr",
    "is_certified_retract",
    "known_absolute_retract_profile",
    "known_anr_profile",
    "not_certified_retraction_profile",
    "point_ar_profile",
    "retraction_profile",
    "retraction_summary",
    "topological_manifold_anr_profile",
    "unknown_retraction_profile",
]
