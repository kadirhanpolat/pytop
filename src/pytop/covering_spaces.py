"""Profile-based covering space helpers.

The module records covering-map teaching examples and assumptions. It does not
verify the local homeomorphism condition for arbitrary maps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


class CoveringSpaceProfileError(ValueError):
    """Raised when covering profile data is malformed."""


COVERING_PROFILE_STATUSES = frozenset({"certified", "assumed", "not_certified", "unknown"})


@dataclass(frozen=True)
class CoveringMapProfile:
    """A conservative profile for a covering map."""

    name: str
    total_space: Any
    base_space: Any
    sheet_count: int | str | None = None
    status: str = "unknown"
    covering_map: str = ""
    local_homeomorphism_assumption: str = "not verified"
    fundamental_group_note: str = ""
    certification: str = "profile"
    warnings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        normalized_status = str(self.status)
        if normalized_status not in COVERING_PROFILE_STATUSES:
            raise CoveringSpaceProfileError(f"Unsupported covering profile status: {self.status!r}.")
        if not str(self.name).strip():
            raise CoveringSpaceProfileError("A covering map profile needs a nonempty name.")
        sheet_count = self.sheet_count
        if isinstance(sheet_count, int) and sheet_count <= 0:
            raise CoveringSpaceProfileError("Sheet count must be positive when it is numeric.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "covering_map", str(self.covering_map))
        object.__setattr__(self, "local_homeomorphism_assumption", str(self.local_homeomorphism_assumption))
        object.__setattr__(self, "fundamental_group_note", str(self.fundamental_group_note))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "warnings", tuple(str(warning) for warning in self.warnings))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified(self) -> bool:
        return self.status == "certified"

    @property
    def has_local_homeomorphism_warning(self) -> bool:
        return any("local homeomorphism" in warning.lower() for warning in self.warnings)


def covering_map_profile(
    name: str,
    total_space: Any,
    base_space: Any,
    *,
    sheet_count: int | str | None = None,
    status: str = "unknown",
    covering_map: str = "",
    local_homeomorphism_assumption: str = "not verified",
    fundamental_group_note: str = "",
    certification: str = "profile",
    warnings: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> CoveringMapProfile:
    """Build a covering map profile without verifying arbitrary coverings."""

    return CoveringMapProfile(
        name=name,
        total_space=total_space,
        base_space=base_space,
        sheet_count=sheet_count,
        status=status,
        covering_map=covering_map,
        local_homeomorphism_assumption=local_homeomorphism_assumption,
        fundamental_group_note=fundamental_group_note,
        certification=certification,
        warnings=tuple(warnings),
        metadata=dict(metadata or {}),
    )


def assumed_covering_map_profile(
    name: str,
    total_space: Any,
    base_space: Any,
    *,
    sheet_count: int | str | None = None,
    covering_map: str = "",
    fundamental_group_note: str = "",
    warnings: Iterable[str] = (),
) -> CoveringMapProfile:
    """Record a covering profile whose local data is assumed, not checked."""

    warning_tuple = tuple(warnings) + ("Local homeomorphism condition is recorded as an assumption.",)
    return covering_map_profile(
        name,
        total_space,
        base_space,
        sheet_count=sheet_count,
        status="assumed",
        covering_map=covering_map,
        local_homeomorphism_assumption="assumed",
        fundamental_group_note=fundamental_group_note,
        certification="assumption-profile",
        warnings=warning_tuple,
    )


def unknown_covering_map_profile(
    name: str,
    total_space: Any,
    base_space: Any,
    *,
    reason: str = "No covering-space certificate or registry match was supplied.",
) -> CoveringMapProfile:
    """Record an explicitly unknown covering profile."""

    return covering_map_profile(
        name,
        total_space,
        base_space,
        status="unknown",
        certification="unknown",
        warnings=(str(reason),),
    )


KNOWN_COVERING_MODELS: Mapping[str, CoveringMapProfile] = {
    "real_line_to_circle": covering_map_profile(
        "real_line_to_circle",
        total_space="R",
        base_space="S^1",
        sheet_count="countably infinite",
        status="certified",
        covering_map="t -> exp(2*pi*i*t)",
        local_homeomorphism_assumption="standard theorem",
        fundamental_group_note="Deck translation intuition connects to pi_1(S^1) being infinite cyclic.",
        certification="known-model-registry",
        warnings=("Standard model; not an arbitrary covering verifier.",),
    ),
    "circle_to_circle_degree_n": covering_map_profile(
        "circle_to_circle_degree_n",
        total_space="S^1",
        base_space="S^1",
        sheet_count="n",
        status="assumed",
        covering_map="z -> z^n",
        local_homeomorphism_assumption="assume n is a positive integer",
        fundamental_group_note="On pi_1(S^1), the induced map is multiplication by n in the standard profile.",
        certification="known-model-registry",
        warnings=("Use a concrete positive integer n for a numeric sheet count.",),
    ),
    "trivial_two_sheet_cover": covering_map_profile(
        "trivial_two_sheet_cover",
        total_space="B x {0, 1}",
        base_space="B",
        sheet_count=2,
        status="certified",
        covering_map="projection to B",
        local_homeomorphism_assumption="product/disjoint-copy teaching model",
        fundamental_group_note="Trivial covers preserve local base-space intuition sheetwise.",
        certification="known-model-registry",
        warnings=("Teaching profile for a trivial finite-sheet cover.",),
    ),
}


def circle_degree_covering_profile(degree: int) -> CoveringMapProfile:
    """Return the standard degree-n circle covering profile for a positive n."""

    if int(degree) <= 0:
        raise CoveringSpaceProfileError("Circle degree covering requires a positive integer degree.")
    return covering_map_profile(
        f"circle_to_circle_degree_{int(degree)}",
        total_space="S^1",
        base_space="S^1",
        sheet_count=int(degree),
        status="certified",
        covering_map=f"z -> z^{int(degree)}",
        local_homeomorphism_assumption="standard finite circle covering model",
        fundamental_group_note=f"Standard pi_1 profile: induced map multiplies by {int(degree)}.",
        certification="known-model-registry",
        warnings=("Standard model; not an arbitrary covering verifier.",),
        metadata={"degree": int(degree)},
    )


def known_covering_profile(key: str) -> CoveringMapProfile:
    """Return a registered covering example, or an unknown profile."""

    normalized = str(key).strip().lower().replace(" ", "_").replace("-", "_")
    profile = KNOWN_COVERING_MODELS.get(normalized)
    if profile is not None:
        return profile
    return unknown_covering_map_profile(
        f"{normalized}_unknown_covering",
        total_space=str(key),
        base_space="unknown",
        reason="No registered covering-space model.",
    )


def covering_profile_summary(profile: CoveringMapProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "total_space": profile.total_space,
        "base_space": profile.base_space,
        "sheet_count": profile.sheet_count,
        "status": profile.status,
        "covering_map": profile.covering_map,
        "local_homeomorphism_assumption": profile.local_homeomorphism_assumption,
        "fundamental_group_note": profile.fundamental_group_note,
        "certification": profile.certification,
        "warnings": profile.warnings,
    }


__all__ = [
    "COVERING_PROFILE_STATUSES",
    "CoveringMapProfile",
    "CoveringSpaceProfileError",
    "KNOWN_COVERING_MODELS",
    "assumed_covering_map_profile",
    "circle_degree_covering_profile",
    "covering_map_profile",
    "covering_profile_summary",
    "known_covering_profile",
    "unknown_covering_map_profile",
]
