"""Profile-based topological manifold helpers.

This module adds the first ``GEO-07`` manifold layer. It records conservative
teaching profiles for standard topological manifolds, their local model,
boundary flag, chart/atlas metadata, and orientability status. It is not a
smooth-manifold package and it does not recognize arbitrary spaces as
manifolds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


class ManifoldProfileError(ValueError):
    """Raised when manifold profile data is malformed."""


MANIFOLD_ORIENTABILITY_VALUES = frozenset({"orientable", "nonorientable", "unknown"})
MANIFOLD_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "unknown"})


@dataclass(frozen=True)
class ManifoldProfile:
    """A conservative profile for a topological manifold model.

    The profile stores metadata that is useful for teaching and examples. A
    ``certified`` status means the entry is a standard model in this registry;
    it is not an algorithmic certificate for an arbitrary input space.
    """

    name: str
    dimension: int
    with_boundary: bool = False
    local_model: str = ""
    orientability: str = "unknown"
    compact: bool | None = None
    connected: bool | None = None
    charts: tuple[str, ...] = ()
    atlas_note: str = ""
    status: str = "preview"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        normalized_name = str(self.name).strip()
        normalized_status = str(self.status)
        normalized_orientability = str(self.orientability)
        if not normalized_name:
            raise ManifoldProfileError("A manifold profile needs a nonempty name.")
        if int(self.dimension) < 0:
            raise ManifoldProfileError("Manifold dimension cannot be negative.")
        if not str(self.local_model).strip():
            raise ManifoldProfileError("A manifold profile needs a local-model label.")
        if normalized_orientability not in MANIFOLD_ORIENTABILITY_VALUES:
            raise ManifoldProfileError(f"Unsupported orientability value: {self.orientability!r}.")
        if normalized_status not in MANIFOLD_PROFILE_STATUSES:
            raise ManifoldProfileError(f"Unsupported manifold profile status: {self.status!r}.")
        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(self, "dimension", int(self.dimension))
        object.__setattr__(self, "with_boundary", bool(self.with_boundary))
        object.__setattr__(self, "local_model", str(self.local_model))
        object.__setattr__(self, "orientability", normalized_orientability)
        object.__setattr__(self, "charts", tuple(str(chart) for chart in self.charts))
        object.__setattr__(self, "atlas_note", str(self.atlas_note))
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "warnings", tuple(str(warning) for warning in self.warnings))
        object.__setattr__(self, "related_profiles", tuple(str(profile) for profile in self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified(self) -> bool:
        return self.status == "certified"

    @property
    def is_surface(self) -> bool:
        return self.dimension == 2

    @property
    def has_boundary(self) -> bool:
        return self.with_boundary


def manifold_profile(
    name: str,
    dimension: int,
    *,
    with_boundary: bool = False,
    local_model: str = "",
    orientability: str = "unknown",
    compact: bool | None = None,
    connected: bool | None = None,
    charts: Iterable[str] = (),
    atlas_note: str = "",
    status: str = "preview",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> ManifoldProfile:
    """Build a topological-manifold teaching profile."""

    return ManifoldProfile(
        name=name,
        dimension=dimension,
        with_boundary=with_boundary,
        local_model=local_model,
        orientability=orientability,
        compact=compact,
        connected=connected,
        charts=tuple(charts),
        atlas_note=atlas_note,
        status=status,
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=dict(metadata or {}),
    )


def real_line_manifold_profile() -> ManifoldProfile:
    """Return the standard one-dimensional real-line manifold profile."""

    return manifold_profile(
        "real_line",
        1,
        local_model="R^1",
        orientability="orientable",
        compact=False,
        connected=True,
        charts=("global identity chart",),
        atlas_note="The real line is modeled by one global coordinate chart.",
        status="certified",
        related_profiles=("metric_spaces", "euclidean_topology"),
    )


def circle_manifold_profile() -> ManifoldProfile:
    """Return the standard circle as a compact one-dimensional manifold."""

    return manifold_profile(
        "circle_S1",
        1,
        local_model="R^1",
        orientability="orientable",
        compact=True,
        connected=True,
        charts=("two overlapping arc charts",),
        atlas_note="At least two arc charts avoid treating the circle as a single interval.",
        status="certified",
        related_profiles=("fundamental_group", "euclidean_topology", "covering_spaces"),
    )


def sphere_manifold_profile(dimension: int = 2) -> ManifoldProfile:
    """Return the standard n-sphere as a topological n-manifold profile."""

    n = int(dimension)
    if n <= 0:
        raise ManifoldProfileError("This teaching profile expects a positive-dimensional sphere.")
    return manifold_profile(
        f"sphere_S{n}",
        n,
        local_model=f"R^{n}",
        orientability="orientable",
        compact=True,
        connected=True,
        charts=("stereographic chart from north pole", "stereographic chart from south pole"),
        atlas_note="Stereographic charts are recorded as standard atlas intuition, not as a coordinate-proof engine.",
        status="certified",
        warnings=("No invariance-of-domain proof or smooth structure is supplied.",),
        related_profiles=("euclidean_topology", "stereographic_projection"),
        metadata={"ambient_model": f"S^{n} subset R^{n + 1}"},
    )


def disk_with_boundary_profile(dimension: int = 2) -> ManifoldProfile:
    """Return the closed n-disk as a manifold-with-boundary profile."""

    n = int(dimension)
    if n <= 0:
        raise ManifoldProfileError("A disk-with-boundary profile needs positive dimension.")
    boundary = f"S^{n - 1}"
    return manifold_profile(
        f"closed_disk_D{n}",
        n,
        with_boundary=True,
        local_model=f"R^{n} in the interior; closed half-space H^{n} near boundary",
        orientability="orientable",
        compact=True,
        connected=True,
        charts=("interior Euclidean charts", "boundary half-space charts"),
        atlas_note="Boundary points use half-space local models rather than open Euclidean neighborhoods.",
        status="certified",
        related_profiles=("euclidean_topology", "sphere"),
        metadata={"boundary_model": boundary, "boundary_dimension": n - 1},
    )


def torus_manifold_profile() -> ManifoldProfile:
    """Return the standard two-torus profile."""

    return manifold_profile(
        "torus_T2",
        2,
        local_model="R^2",
        orientability="orientable",
        compact=True,
        connected=True,
        charts=("square edge-identification atlas",),
        atlas_note="The torus is recorded as a standard quotient/surface model for later gluing work.",
        status="certified",
        warnings=("Surface classification is deferred to later route work.",),
        related_profiles=("quotients", "surface_gluing", "fundamental_group"),
        metadata={"standard_edge_word": "a b a^-1 b^-1"},
    )


def projective_plane_manifold_profile() -> ManifoldProfile:
    """Return the real projective plane as a nonorientable surface profile."""

    return manifold_profile(
        "projective_plane_RP2",
        2,
        local_model="R^2",
        orientability="nonorientable",
        compact=True,
        connected=True,
        charts=("antipodal quotient charts on S^2",),
        atlas_note="The projective plane is treated as a standard quotient model, not classified from arbitrary data.",
        status="certified",
        warnings=("Nonorientability is a registered standard-model fact; no classification proof is supplied.",),
        related_profiles=("projective_preview", "quotients", "surfaces"),
        metadata={"quotient_model": "S^2 / (x ~ -x)"},
    )


def unknown_manifold_profile(
    name: str,
    *,
    dimension: int = 0,
    reason: str = "No manifold certificate or registry match was supplied.",
) -> ManifoldProfile:
    """Return an explicitly unknown manifold profile."""

    return manifold_profile(
        f"{str(name).strip() or 'unknown'}_unknown_manifold",
        int(dimension),
        local_model="unknown",
        orientability="unknown",
        compact=None,
        connected=None,
        status="unknown",
        warnings=(str(reason), "This profile does not certify manifold recognition."),
    )


KNOWN_MANIFOLD_PROFILES: Mapping[str, ManifoldProfile] = {
    "real_line": real_line_manifold_profile(),
    "r": real_line_manifold_profile(),
    "circle": circle_manifold_profile(),
    "circle_s1": circle_manifold_profile(),
    "s1": circle_manifold_profile(),
    "sphere_s2": sphere_manifold_profile(2),
    "s2": sphere_manifold_profile(2),
    "closed_disk_d2": disk_with_boundary_profile(2),
    "disk_d2": disk_with_boundary_profile(2),
    "torus": torus_manifold_profile(),
    "torus_t2": torus_manifold_profile(),
    "projective_plane": projective_plane_manifold_profile(),
    "projective_plane_rp2": projective_plane_manifold_profile(),
    "rp2": projective_plane_manifold_profile(),
}


def known_manifold_profile(key: str) -> ManifoldProfile:
    """Return a registered standard manifold profile or an unknown profile."""

    normalized = str(key).strip().lower().replace(" ", "_").replace("-", "_").replace("^", "")
    profile = KNOWN_MANIFOLD_PROFILES.get(normalized)
    if profile is not None:
        return profile
    return unknown_manifold_profile(str(key), reason="No registered topological-manifold model.")


def manifold_profile_summary(profile: ManifoldProfile) -> dict[str, Any]:
    """Return a small dictionary suitable for examples and tests."""

    return {
        "name": profile.name,
        "dimension": profile.dimension,
        "with_boundary": profile.with_boundary,
        "local_model": profile.local_model,
        "orientability": profile.orientability,
        "compact": profile.compact,
        "connected": profile.connected,
        "charts": profile.charts,
        "atlas_note": profile.atlas_note,
        "status": profile.status,
        "warnings": profile.warnings,
        "related_profiles": profile.related_profiles,
        "is_surface": profile.is_surface,
    }


__all__ = [
    "MANIFOLD_ORIENTABILITY_VALUES",
    "MANIFOLD_PROFILE_STATUSES",
    "KNOWN_MANIFOLD_PROFILES",
    "ManifoldProfile",
    "ManifoldProfileError",
    "manifold_profile",
    "real_line_manifold_profile",
    "circle_manifold_profile",
    "sphere_manifold_profile",
    "disk_with_boundary_profile",
    "torus_manifold_profile",
    "projective_plane_manifold_profile",
    "unknown_manifold_profile",
    "known_manifold_profile",
    "manifold_profile_summary",
]
