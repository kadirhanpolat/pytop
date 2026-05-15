"""Continuum and Hilbert cube teaching profiles for the geometric topology bridge.

The helpers in this module deliberately remain conservative.  They record
standard examples and counterexamples for the route ``GEO-08`` without claiming
a general decision procedure for compactness, connectedness, metrizability, or
continuum recognition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


class ContinuumProfileError(ValueError):
    """Raised when continuum profile metadata is malformed."""


CONTINUUM_PROFILE_STATUSES = frozenset({"certified", "preview", "assumed", "counterexample", "unknown"})


@dataclass(frozen=True)
class ContinuumProfile:
    """A conservative profile for compact connected metric spaces."""

    name: str
    compact: bool | None = None
    connected: bool | None = None
    metric: bool | None = None
    nonempty: bool | None = True
    continuum: bool | None = None
    model: str = ""
    dimension_hint: str = ""
    local_connectedness_hint: str = "unknown"
    status: str = "preview"
    warnings: tuple[str, ...] = ()
    related_profiles: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        status = str(self.status).strip().lower()
        if not name:
            raise ContinuumProfileError("A continuum profile needs a nonempty name.")
        if status not in CONTINUUM_PROFILE_STATUSES:
            raise ContinuumProfileError(f"Unsupported continuum profile status: {self.status!r}.")
        if self.continuum is True:
            required = {"nonempty": self.nonempty, "compact": self.compact, "connected": self.connected, "metric": self.metric}
            missing = tuple(key for key, value in required.items() if value is not True)
            if missing:
                raise ContinuumProfileError(
                    "A profile marked as a continuum must explicitly set nonempty, compact, connected, and metric to True; "
                    f"missing/false fields: {missing}."
                )
        if self.status == "counterexample" and self.continuum is not False:
            raise ContinuumProfileError("A counterexample profile must set continuum=False.")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "model", str(self.model))
        object.__setattr__(self, "dimension_hint", str(self.dimension_hint))
        object.__setattr__(self, "local_connectedness_hint", str(self.local_connectedness_hint))
        object.__setattr__(self, "warnings", tuple(str(w) for w in self.warnings))
        object.__setattr__(self, "related_profiles", tuple(str(p) for p in self.related_profiles))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified_continuum(self) -> bool:
        return self.continuum is True and self.status == "certified"

    @property
    def is_known_noncontinuum(self) -> bool:
        return self.continuum is False and self.status == "counterexample"

    @property
    def condition_tuple(self) -> tuple[bool | None, bool | None, bool | None, bool | None]:
        return (self.nonempty, self.compact, self.connected, self.metric)

    @property
    def continuum_label(self) -> str:
        if self.continuum is True:
            return "continuum"
        if self.continuum is False:
            return "not a continuum"
        return "continuum status unknown"


def continuum_profile(
    name: str,
    *,
    compact: bool | None = None,
    connected: bool | None = None,
    metric: bool | None = None,
    nonempty: bool | None = True,
    continuum: bool | None = None,
    model: str = "",
    dimension_hint: str = "",
    local_connectedness_hint: str = "unknown",
    status: str = "preview",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> ContinuumProfile:
    return ContinuumProfile(
        name=name,
        compact=compact,
        connected=connected,
        metric=metric,
        nonempty=nonempty,
        continuum=continuum,
        model=model,
        dimension_hint=dimension_hint,
        local_connectedness_hint=local_connectedness_hint,
        status=status,
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=dict(metadata or {}),
    )


def certified_continuum_profile(
    name: str,
    *,
    model: str,
    dimension_hint: str = "",
    local_connectedness_hint: str = "unknown",
    warnings: Iterable[str] = (),
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> ContinuumProfile:
    return continuum_profile(
        name,
        compact=True,
        connected=True,
        metric=True,
        nonempty=True,
        continuum=True,
        model=model,
        dimension_hint=dimension_hint,
        local_connectedness_hint=local_connectedness_hint,
        status="certified",
        warnings=tuple(warnings),
        related_profiles=tuple(related_profiles),
        metadata=metadata,
    )


def non_continuum_profile(
    name: str,
    *,
    reason: str,
    compact: bool | None = None,
    connected: bool | None = None,
    metric: bool | None = None,
    nonempty: bool | None = True,
    model: str = "",
    related_profiles: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> ContinuumProfile:
    return continuum_profile(
        name,
        compact=compact,
        connected=connected,
        metric=metric,
        nonempty=nonempty,
        continuum=False,
        model=model,
        status="counterexample",
        warnings=(str(reason),),
        related_profiles=tuple(related_profiles),
        metadata=metadata,
    )


def interval_continuum_profile() -> ContinuumProfile:
    return certified_continuum_profile(
        "closed_interval_I",
        model="the closed interval [0,1] with the usual metric topology",
        dimension_hint="one-dimensional",
        local_connectedness_hint="locally connected",
        related_profiles=("metric_spaces", "compactness", "connectedness"),
        metadata={"standard_notation": "I"},
    )


def circle_continuum_profile() -> ContinuumProfile:
    return certified_continuum_profile(
        "circle_S1",
        model="unit circle in the Euclidean plane",
        dimension_hint="one-dimensional manifold",
        local_connectedness_hint="locally connected",
        related_profiles=("surfaces", "manifolds", "fundamental_group"),
        metadata={"standard_notation": "S^1"},
    )


def disk_continuum_profile() -> ContinuumProfile:
    return certified_continuum_profile(
        "closed_disk_D2",
        model="closed 2-disk with the Euclidean subspace topology",
        dimension_hint="two-dimensional with boundary",
        local_connectedness_hint="locally connected",
        related_profiles=("euclidean_topology", "manifolds", "surfaces"),
        metadata={"boundary_model": "S^1"},
    )


def hilbert_cube_profile() -> ContinuumProfile:
    return certified_continuum_profile(
        "hilbert_cube_I_omega",
        model="countable product of closed intervals with the standard product metric model",
        dimension_hint="infinite-dimensional compact metric model",
        local_connectedness_hint="locally connected in the standard product model",
        warnings=(
            "This registry records the standard Hilbert cube continuum fact; it does not build a functional-analysis engine.",
            "Coordinate-level product proofs are deferred to the advanced metric-spaces route.",
        ),
        related_profiles=("metric_spaces_II", "products", "compactness", "continua"),
        metadata={"standard_notation": "I^omega", "coordinate_bound": "0 <= x_n <= 1/n or equivalent compact product model"},
    )


def cantor_set_noncontinuum_profile() -> ContinuumProfile:
    return non_continuum_profile(
        "cantor_set",
        compact=True,
        connected=False,
        metric=True,
        model="middle-third Cantor set in the real line",
        reason="The Cantor set is compact and metric but not connected, hence not a continuum.",
        related_profiles=("compactness", "zero_dimensionality", "counterexamples"),
        metadata={"failure_condition": "connected"},
    )


def topologist_sine_curve_profile() -> ContinuumProfile:
    return continuum_profile(
        "topologist_sine_curve_closure",
        compact=True,
        connected=True,
        metric=True,
        nonempty=True,
        continuum=True,
        model="closure of the graph y = sin(1/x) for 0 < x <= 1 together with its limit segment",
        dimension_hint="plane continuum example",
        local_connectedness_hint="not locally connected at the limit segment",
        status="preview",
        warnings=("This is a preview registry entry: the package records the standard example but does not prove its connectedness.",),
        related_profiles=("continua", "counterexamples", "euclidean_topology"),
        metadata={"teaching_use": "connected but locally subtle continuum"},
    )


KNOWN_CONTINUUM_PROFILES: Mapping[str, ContinuumProfile] = {
    "interval": interval_continuum_profile(),
    "closed_interval": interval_continuum_profile(),
    "unit_interval": interval_continuum_profile(),
    "i": interval_continuum_profile(),
    "circle": circle_continuum_profile(),
    "circle_s1": circle_continuum_profile(),
    "s1": circle_continuum_profile(),
    "disk": disk_continuum_profile(),
    "closed_disk": disk_continuum_profile(),
    "closed_disk_d2": disk_continuum_profile(),
    "d2": disk_continuum_profile(),
    "hilbert_cube": hilbert_cube_profile(),
    "hilbert_cube_i_omega": hilbert_cube_profile(),
    "i_omega": hilbert_cube_profile(),
    "cantor_set": cantor_set_noncontinuum_profile(),
    "cantor": cantor_set_noncontinuum_profile(),
    "topologist_sine_curve": topologist_sine_curve_profile(),
    "topologist_sine_curve_closure": topologist_sine_curve_profile(),
}


def known_continuum_profile(key: str) -> ContinuumProfile:
    normalized = str(key).strip().lower().replace(" ", "_").replace("-", "_").replace("^", "")
    profile = KNOWN_CONTINUUM_PROFILES.get(normalized)
    if profile is not None:
        return profile
    return continuum_profile(
        f"{normalized or 'unknown'}_unknown_continuum_profile",
        compact=None,
        connected=None,
        metric=None,
        nonempty=None,
        continuum=None,
        status="unknown",
        warnings=("No registered continuum model; no recognition claim is made.",),
    )


def continuum_condition_report(profile: ContinuumProfile) -> dict[str, Any]:
    conditions = {"nonempty": profile.nonempty, "compact": profile.compact, "connected": profile.connected, "metric": profile.metric}
    if profile.continuum is True:
        verdict = "continuum"
    elif profile.continuum is False:
        verdict = "not_continuum"
    else:
        verdict = "unknown"
    return {
        "name": profile.name,
        "conditions": conditions,
        "verdict": verdict,
        "status": profile.status,
        "warnings": profile.warnings,
        "related_profiles": profile.related_profiles,
    }


def continuum_profile_summary(profile: ContinuumProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "compact": profile.compact,
        "connected": profile.connected,
        "metric": profile.metric,
        "nonempty": profile.nonempty,
        "continuum": profile.continuum,
        "continuum_label": profile.continuum_label,
        "model": profile.model,
        "dimension_hint": profile.dimension_hint,
        "local_connectedness_hint": profile.local_connectedness_hint,
        "status": profile.status,
        "is_certified_continuum": profile.is_certified_continuum,
        "is_known_noncontinuum": profile.is_known_noncontinuum,
        "warnings": profile.warnings,
        "metadata": dict(profile.metadata),
    }


def is_continuum_profile(profile: ContinuumProfile) -> bool | None:
    """Return the recorded continuum verdict without attempting recognition."""
    return profile.continuum


__all__ = [
    "CONTINUUM_PROFILE_STATUSES",
    "KNOWN_CONTINUUM_PROFILES",
    "ContinuumProfile",
    "ContinuumProfileError",
    "continuum_profile",
    "certified_continuum_profile",
    "non_continuum_profile",
    "interval_continuum_profile",
    "circle_continuum_profile",
    "disk_continuum_profile",
    "hilbert_cube_profile",
    "cantor_set_noncontinuum_profile",
    "topologist_sine_curve_profile",
    "known_continuum_profile",
    "continuum_condition_report",
    "continuum_profile_summary",
    "is_continuum_profile",
]
