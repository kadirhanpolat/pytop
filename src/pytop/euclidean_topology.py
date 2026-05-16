"""Profile-based Euclidean topology bridge helpers.

The module records teaching profiles for balls, disks, spheres, punctured
spheres, stereographic intuition, and projective previews. It does not prove
heavy theorems such as invariance of domain.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any


class EuclideanTopologyProfileError(ValueError):
    """Raised when Euclidean topology profile data is malformed."""


EUCLIDEAN_PROFILE_KINDS = frozenset(
    {
        "open_ball",
        "closed_ball",
        "sphere",
        "disk",
        "disk_boundary",
        "punctured_sphere",
        "stereographic_projection",
        "projective_preview",
    }
)
EUCLIDEAN_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "unknown"})


@dataclass(frozen=True)
class EuclideanTopologyProfile:
    """A conservative teaching profile for a Euclidean topology object."""

    name: str
    kind: str
    ambient_dimension: int | None = None
    intrinsic_dimension: int | None = None
    model: str = ""
    boundary: str = ""
    status: str = "preview"
    intuition: str = ""
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        normalized_kind = str(self.kind)
        normalized_status = str(self.status)
        if not str(self.name).strip():
            raise EuclideanTopologyProfileError("A Euclidean profile needs a nonempty name.")
        if normalized_kind not in EUCLIDEAN_PROFILE_KINDS:
            raise EuclideanTopologyProfileError(f"Unsupported Euclidean profile kind: {self.kind!r}.")
        if normalized_status not in EUCLIDEAN_PROFILE_STATUSES:
            raise EuclideanTopologyProfileError(f"Unsupported Euclidean profile status: {self.status!r}.")
        if self.ambient_dimension is not None and int(self.ambient_dimension) < 0:
            raise EuclideanTopologyProfileError("Ambient dimension cannot be negative.")
        if self.intrinsic_dimension is not None and int(self.intrinsic_dimension) < 0:
            raise EuclideanTopologyProfileError("Intrinsic dimension cannot be negative.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "kind", normalized_kind)
        object.__setattr__(self, "ambient_dimension", None if self.ambient_dimension is None else int(self.ambient_dimension))
        object.__setattr__(self, "intrinsic_dimension", None if self.intrinsic_dimension is None else int(self.intrinsic_dimension))
        object.__setattr__(self, "model", str(self.model))
        object.__setattr__(self, "boundary", str(self.boundary))
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "intuition", str(self.intuition))
        object.__setattr__(self, "warnings", tuple(str(warning) for warning in self.warnings))
        object.__setattr__(self, "related_profiles", tuple(str(profile) for profile in self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def has_boundary(self) -> bool:
        return bool(self.boundary)

    @property
    def is_preview(self) -> bool:
        return self.status == "preview"


def euclidean_topology_profile(
    name: str,
    kind: str,
    *,
    ambient_dimension: int | None = None,
    intrinsic_dimension: int | None = None,
    model: str = "",
    boundary: str = "",
    status: str = "preview",
    intuition: str = "",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> EuclideanTopologyProfile:
    """Build a Euclidean topology teaching profile."""

    return EuclideanTopologyProfile(
        name=name,
        kind=kind,
        ambient_dimension=ambient_dimension,
        intrinsic_dimension=intrinsic_dimension,
        model=model,
        boundary=boundary,
        status=status,
        intuition=intuition,
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=dict(metadata or {}),
    )


def open_ball_profile(dimension: int, *, radius_label: str = "r", center_label: str = "x") -> EuclideanTopologyProfile:
    """Return the standard open ball profile in R^n."""

    return euclidean_topology_profile(
        f"open_ball_R{int(dimension)}",
        "open_ball",
        ambient_dimension=dimension,
        intrinsic_dimension=dimension,
        model=f"{{y in R^{int(dimension)} : d(y, {center_label}) < {radius_label}}}",
        status="certified",
        intuition="Metric neighborhoods generate the standard Euclidean topology.",
        related_profiles=("metric_spaces",),
    )


def closed_disk_profile(dimension: int) -> EuclideanTopologyProfile:
    """Return a closed n-disk profile with boundary sphere label."""

    if int(dimension) <= 0:
        raise EuclideanTopologyProfileError("A disk profile needs a positive dimension.")
    boundary_dimension = int(dimension) - 1
    return euclidean_topology_profile(
        f"closed_disk_D{int(dimension)}",
        "disk",
        ambient_dimension=dimension,
        intrinsic_dimension=dimension,
        model=f"D^{int(dimension)}",
        boundary=f"S^{boundary_dimension}",
        status="certified",
        intuition="The boundary of a closed n-disk is the (n-1)-sphere in the standard teaching model.",
        related_profiles=("sphere", "compactness"),
        metadata={"boundary_dimension": boundary_dimension},
    )


def sphere_profile(dimension: int) -> EuclideanTopologyProfile:
    """Return the standard n-sphere profile embedded in R^(n+1)."""

    if int(dimension) < 0:
        raise EuclideanTopologyProfileError("Sphere dimension cannot be negative.")
    return euclidean_topology_profile(
        f"sphere_S{int(dimension)}",
        "sphere",
        ambient_dimension=int(dimension) + 1,
        intrinsic_dimension=dimension,
        model=f"S^{int(dimension)} subset R^{int(dimension) + 1}",
        status="certified",
        intuition="A sphere is the constant-radius boundary of a disk in the standard Euclidean model.",
        related_profiles=("disk_boundary",),
    )


def punctured_sphere_profile(dimension: int) -> EuclideanTopologyProfile:
    """Return a sphere-minus-point intuition profile."""

    if int(dimension) <= 0:
        raise EuclideanTopologyProfileError("Punctured sphere intuition needs positive dimension.")
    return euclidean_topology_profile(
        f"punctured_sphere_S{int(dimension)}",
        "punctured_sphere",
        ambient_dimension=int(dimension) + 1,
        intrinsic_dimension=dimension,
        model=f"S^{int(dimension)} minus one point",
        status="preview",
        intuition=f"S^{int(dimension)} minus a point is modeled by R^{int(dimension)} via stereographic intuition.",
        warnings=("This is an intuition/profile entry, not a full theorem proof.",),
        related_profiles=("stereographic_projection",),
    )


def stereographic_projection_profile(dimension: int) -> EuclideanTopologyProfile:
    """Return a stereographic projection intuition profile."""

    if int(dimension) <= 0:
        raise EuclideanTopologyProfileError("Stereographic projection profile needs positive dimension.")
    return euclidean_topology_profile(
        f"stereographic_projection_S{int(dimension)}",
        "stereographic_projection",
        ambient_dimension=int(dimension) + 1,
        intrinsic_dimension=dimension,
        model=f"S^{int(dimension)} minus north pole -> R^{int(dimension)}",
        status="preview",
        intuition="A punctured sphere can be pictured as Euclidean space by projecting from a chosen pole.",
        warnings=("No coordinate proof is supplied in this bridge profile.",),
        related_profiles=("punctured_sphere", "open_ball"),
    )


def projective_preview_profile(model: str = "projective_line") -> EuclideanTopologyProfile:
    """Return a projective-space preview profile."""

    normalized = str(model).strip().lower().replace(" ", "_").replace("-", "_")
    if normalized == "projective_line":
        return euclidean_topology_profile(
            "projective_line_preview",
            "projective_preview",
            intrinsic_dimension=1,
            model="RP^1 as antipodal pairs on S^1",
            status="preview",
            intuition="The projective line is introduced through antipodal identification on the circle.",
            warnings=("Preview only; no projective classification theorem is supplied.",),
            related_profiles=("quotients", "sphere"),
        )
    if normalized == "projective_plane":
        return euclidean_topology_profile(
            "projective_plane_preview",
            "projective_preview",
            intrinsic_dimension=2,
            model="RP^2 as antipodal pairs on S^2",
            status="preview",
            intuition="The projective plane is previewed as a quotient model for later surface work.",
            warnings=("Preview only; no full projective-space classification is supplied.",),
            related_profiles=("quotients", "surfaces"),
        )
    return euclidean_topology_profile(
        f"{normalized}_projective_preview_unknown",
        "projective_preview",
        model=str(model),
        status="unknown",
        intuition="No registered projective preview exists for this model.",
        warnings=("Unknown projective preview key.",),
    )


KNOWN_EUCLIDEAN_PROFILES: Mapping[str, EuclideanTopologyProfile] = {
    "open_ball_R2": open_ball_profile(2),
    "closed_disk_D2": closed_disk_profile(2),
    "sphere_S1": sphere_profile(1),
    "sphere_S2": sphere_profile(2),
    "punctured_sphere_S2": punctured_sphere_profile(2),
    "stereographic_projection_S2": stereographic_projection_profile(2),
    "projective_line_preview": projective_preview_profile("projective_line"),
    "projective_plane_preview": projective_preview_profile("projective_plane"),
}


def known_euclidean_profile(key: str) -> EuclideanTopologyProfile:
    """Return a registered Euclidean teaching profile, or an unknown preview."""

    normalized = str(key).strip().replace(" ", "_").replace("-", "_")
    profile = KNOWN_EUCLIDEAN_PROFILES.get(normalized)
    if profile is not None:
        return profile
    return euclidean_topology_profile(
        f"{normalized}_unknown",
        "projective_preview",
        model=str(key),
        status="unknown",
        intuition="No registered Euclidean topology profile exists for this key.",
        warnings=("Unknown Euclidean profile key.",),
    )


def euclidean_profile_summary(profile: EuclideanTopologyProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "kind": profile.kind,
        "ambient_dimension": profile.ambient_dimension,
        "intrinsic_dimension": profile.intrinsic_dimension,
        "model": profile.model,
        "boundary": profile.boundary,
        "status": profile.status,
        "intuition": profile.intuition,
        "warnings": profile.warnings,
        "related_profiles": profile.related_profiles,
    }


__all__ = [
    "EUCLIDEAN_PROFILE_KINDS",
    "EUCLIDEAN_PROFILE_STATUSES",
    "EuclideanTopologyProfile",
    "EuclideanTopologyProfileError",
    "KNOWN_EUCLIDEAN_PROFILES",
    "closed_disk_profile",
    "euclidean_profile_summary",
    "euclidean_topology_profile",
    "known_euclidean_profile",
    "open_ball_profile",
    "projective_preview_profile",
    "punctured_sphere_profile",
    "sphere_profile",
    "stereographic_projection_profile",
]
