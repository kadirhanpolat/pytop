"""Conservative surface profile helpers for the geometric topology bridge.

This module records standard compact surface examples with orientability,
genus/crosscap, boundary, and teaching metadata. It deliberately does not prove
the surface-classification theorem and it does not classify arbitrary polygon
gluings or arbitrary input spaces.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .manifolds import ManifoldProfile, manifold_profile


class SurfaceProfileError(ValueError):
    """Raised when surface profile data is malformed."""

SURFACE_ORIENTABILITY_VALUES = frozenset({"orientable", "nonorientable", "unknown"})
SURFACE_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "unknown"})

@dataclass(frozen=True)
class SurfaceProfile:
    """A teaching profile for a two-dimensional topological surface."""
    name: str
    orientability: str = "unknown"
    genus: int | None = None
    nonorientable_genus: int | None = None
    boundary_component_count: int = 0
    compact: bool | None = None
    connected: bool | None = True
    model: str = ""
    gluing_word: str = ""
    fundamental_group_hint: str = ""
    manifold_profile_key: str = ""
    status: str = "preview"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)
    def __post_init__(self) -> None:
        name = str(self.name).strip(); orient = str(self.orientability); status = str(self.status)
        if not name: raise SurfaceProfileError("A surface profile needs a nonempty name.")
        if orient not in SURFACE_ORIENTABILITY_VALUES: raise SurfaceProfileError(f"Unsupported surface orientability value: {self.orientability!r}.")
        if status not in SURFACE_PROFILE_STATUSES: raise SurfaceProfileError(f"Unsupported surface profile status: {self.status!r}.")
        if self.genus is not None and int(self.genus) < 0: raise SurfaceProfileError("Orientable genus cannot be negative.")
        if self.nonorientable_genus is not None and int(self.nonorientable_genus) <= 0: raise SurfaceProfileError("Nonorientable genus/crosscap count must be positive when supplied.")
        if int(self.boundary_component_count) < 0: raise SurfaceProfileError("Boundary component count cannot be negative.")
        if orient == "orientable" and self.nonorientable_genus is not None: raise SurfaceProfileError("An orientable surface profile should not carry a nonorientable genus.")
        if orient == "nonorientable" and self.genus is not None: raise SurfaceProfileError("A nonorientable surface profile should not carry an orientable genus.")
        object.__setattr__(self, "name", name); object.__setattr__(self, "orientability", orient); object.__setattr__(self, "status", status)
        object.__setattr__(self, "genus", None if self.genus is None else int(self.genus))
        object.__setattr__(self, "nonorientable_genus", None if self.nonorientable_genus is None else int(self.nonorientable_genus))
        object.__setattr__(self, "boundary_component_count", int(self.boundary_component_count))
        object.__setattr__(self, "model", str(self.model)); object.__setattr__(self, "gluing_word", str(self.gluing_word))
        object.__setattr__(self, "fundamental_group_hint", str(self.fundamental_group_hint)); object.__setattr__(self, "manifold_profile_key", str(self.manifold_profile_key))
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings)); object.__setattr__(self, "related_profiles", tuple(str(p) for p in self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))
    @property
    def dimension(self) -> int: return 2
    @property
    def has_boundary(self) -> bool: return self.boundary_component_count > 0
    @property
    def is_closed_surface(self) -> bool: return self.compact is True and self.boundary_component_count == 0
    @property
    def is_certified(self) -> bool: return self.status == "certified"
    @property
    def classification_label(self) -> str:
        suffix = "" if self.boundary_component_count == 0 else f" with {self.boundary_component_count} boundary component(s)"
        if self.orientability == "orientable" and self.genus is not None: return f"orientable genus {self.genus} surface{suffix}"
        if self.orientability == "nonorientable" and self.nonorientable_genus is not None: return f"nonorientable genus {self.nonorientable_genus} surface{suffix}"
        return f"unknown surface type{suffix}"

def surface_profile(name: str, *, orientability: str="unknown", genus: int|None=None, nonorientable_genus: int|None=None, boundary_component_count: int=0, compact: bool|None=None, connected: bool|None=True, model: str="", gluing_word: str="", fundamental_group_hint: str="", manifold_profile_key: str="", status: str="preview", warnings: Iterable[str]=(), related_profiles: Iterable[str]=(), metadata: dict[str, Any]|None=None) -> SurfaceProfile:
    return SurfaceProfile(name, orientability, genus, nonorientable_genus, boundary_component_count, compact, connected, model, gluing_word, fundamental_group_hint, manifold_profile_key, status, tuple(warnings), tuple(related_profiles), dict(metadata or {}))

def sphere_surface_profile() -> SurfaceProfile:
    return surface_profile("sphere_S2", orientability="orientable", genus=0, compact=True, connected=True, model="S^2", fundamental_group_hint="trivial", manifold_profile_key="sphere_s2", status="certified", related_profiles=("manifolds","euclidean_topology","fundamental_group"), metadata={"euler_characteristic": 2})
def torus_surface_profile() -> SurfaceProfile:
    return surface_profile("torus_T2", orientability="orientable", genus=1, compact=True, connected=True, model="square with opposite edges identified", gluing_word="a b a^-1 b^-1", fundamental_group_hint="Z^2", manifold_profile_key="torus_t2", status="certified", warnings=("The edge word is recorded as a standard model, not produced by a gluing classifier.",), related_profiles=("manifolds","surface_gluing","fundamental_group"), metadata={"euler_characteristic": 0})
def double_torus_surface_profile() -> SurfaceProfile:
    return surface_profile("double_torus_genus_2", orientability="orientable", genus=2, compact=True, connected=True, model="connected sum of two tori", gluing_word="a b a^-1 b^-1 c d c^-1 d^-1", fundamental_group_hint="standard genus-2 surface group presentation", status="certified", warnings=("Only the standard profile is recorded; no classification theorem is proved here.",), related_profiles=("manifolds","surface_gluing","fundamental_group"), metadata={"euler_characteristic": -2})
def disk_surface_profile() -> SurfaceProfile:
    return surface_profile("closed_disk_D2", orientability="orientable", genus=0, boundary_component_count=1, compact=True, connected=True, model="closed 2-disk", fundamental_group_hint="trivial", manifold_profile_key="closed_disk_d2", status="certified", related_profiles=("manifolds","euclidean_topology","retracts"), metadata={"boundary_model":"S^1","euler_characteristic":1})
def annulus_surface_profile() -> SurfaceProfile:
    return surface_profile("annulus", orientability="orientable", genus=0, boundary_component_count=2, compact=True, connected=True, model="S^1 x [0,1]", fundamental_group_hint="Z", status="certified", related_profiles=("manifolds","retracts"), metadata={"euler_characteristic":0})
def mobius_band_surface_profile() -> SurfaceProfile:
    return surface_profile("mobius_band", orientability="nonorientable", nonorientable_genus=1, boundary_component_count=1, compact=True, connected=True, model="rectangle with one reversed edge identification", gluing_word="a a", fundamental_group_hint="Z", status="certified", warnings=("Nonorientability is recorded as a standard-model fact.",), related_profiles=("quotients","surface_gluing"), metadata={"euler_characteristic":0})
def projective_plane_surface_profile() -> SurfaceProfile:
    return surface_profile("projective_plane_RP2", orientability="nonorientable", nonorientable_genus=1, compact=True, connected=True, model="disk with antipodal boundary identification", gluing_word="a a", fundamental_group_hint="Z/2Z", manifold_profile_key="projective_plane_rp2", status="certified", warnings=("No classification proof is supplied.",), related_profiles=("projective_spaces","quotients","manifolds"), metadata={"euler_characteristic":1})
def klein_bottle_surface_profile() -> SurfaceProfile:
    return surface_profile("klein_bottle", orientability="nonorientable", nonorientable_genus=2, compact=True, connected=True, model="square edge identification with one reversed pair", gluing_word="a b a^-1 b", fundamental_group_hint="<a,b | a b a^-1 = b^-1>", status="certified", warnings=("Classification and recognition algorithms are deferred.",), related_profiles=("surface_gluing","quotients"), metadata={"euler_characteristic":0})
def unknown_surface_profile(name: str, *, reason: str="No registered surface model.") -> SurfaceProfile:
    return surface_profile(f"{str(name).strip() or 'unknown'}_unknown_surface", orientability="unknown", compact=None, connected=None, status="unknown", warnings=(str(reason), "This profile does not certify surface recognition."))
KNOWN_SURFACE_PROFILES: Mapping[str, SurfaceProfile] = {
    "sphere": sphere_surface_profile(), "sphere_s2": sphere_surface_profile(), "s2": sphere_surface_profile(),
    "torus": torus_surface_profile(), "torus_t2": torus_surface_profile(), "t2": torus_surface_profile(),
    "double_torus": double_torus_surface_profile(), "double_torus_genus_2": double_torus_surface_profile(),
    "closed_disk_d2": disk_surface_profile(), "disk": disk_surface_profile(), "disk_d2": disk_surface_profile(),
    "annulus": annulus_surface_profile(), "mobius_band": mobius_band_surface_profile(), "moebius_band": mobius_band_surface_profile(),
    "projective_plane": projective_plane_surface_profile(), "projective_plane_rp2": projective_plane_surface_profile(), "rp2": projective_plane_surface_profile(),
    "klein_bottle": klein_bottle_surface_profile(),
}
def known_surface_profile(key: str) -> SurfaceProfile:
    norm = str(key).strip().lower().replace(" ", "_").replace("-", "_").replace("^", "")
    return KNOWN_SURFACE_PROFILES.get(norm) or unknown_surface_profile(str(key))
def as_manifold_profile(profile: SurfaceProfile) -> ManifoldProfile:
    local_model = "R^2" if not profile.has_boundary else "R^2 in the interior; closed half-space H^2 near boundary"
    return manifold_profile(profile.name, 2, with_boundary=profile.has_boundary, local_model=local_model, orientability=profile.orientability, compact=profile.compact, connected=profile.connected, charts=("surface-profile teaching charts",), atlas_note="Created from a SurfaceProfile; not an independent atlas verification.", status=profile.status, warnings=profile.warnings, related_profiles=profile.related_profiles, metadata={"source_surface_profile": profile.name, **profile.metadata})
def surface_profile_summary(profile: SurfaceProfile) -> dict[str, Any]:
    return {"name": profile.name, "dimension": profile.dimension, "orientability": profile.orientability, "genus": profile.genus, "nonorientable_genus": profile.nonorientable_genus, "boundary_component_count": profile.boundary_component_count, "compact": profile.compact, "connected": profile.connected, "model": profile.model, "gluing_word": profile.gluing_word, "fundamental_group_hint": profile.fundamental_group_hint, "status": profile.status, "warnings": profile.warnings, "classification_label": profile.classification_label, "has_boundary": profile.has_boundary}
__all__ = [
    "SurfaceProfileError",
    "SurfaceProfile",
    "surface_profile",
    "sphere_surface_profile",
    "torus_surface_profile",
    "double_torus_surface_profile",
    "disk_surface_profile",
    "annulus_surface_profile",
    "mobius_band_surface_profile",
    "projective_plane_surface_profile",
    "klein_bottle_surface_profile",
    "unknown_surface_profile",
    "known_surface_profile",
    "as_manifold_profile",
    "surface_profile_summary",
]
