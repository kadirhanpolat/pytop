"""Profile-based fundamental group helpers.

The module records standard teaching profiles for pi_1. It is not a general
fundamental group calculator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


class FundamentalGroupProfileError(ValueError):
    """Raised when fundamental group profile data is malformed."""


GROUP_PROFILE_STATUSES = frozenset({"certified", "not_certified", "unknown"})
GROUP_KINDS = frozenset({"trivial", "infinite_cyclic", "free", "profile"})


@dataclass(frozen=True)
class FundamentalGroupProfile:
    """A conservative profile for a fundamental group claim."""

    space: Any
    basepoint: Any = None
    kind: str = "profile"
    status: str = "unknown"
    generators: tuple[str, ...] = ()
    rank: int | None = None
    presentation: str = ""
    certification: str = "profile"
    notes: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        normalized_kind = str(self.kind)
        normalized_status = str(self.status)
        if normalized_kind not in GROUP_KINDS:
            raise FundamentalGroupProfileError(f"Unsupported fundamental group kind: {self.kind!r}.")
        if normalized_status not in GROUP_PROFILE_STATUSES:
            raise FundamentalGroupProfileError(f"Unsupported fundamental group status: {self.status!r}.")
        generators = tuple(str(generator) for generator in self.generators)
        if self.rank is not None and int(self.rank) < 0:
            raise FundamentalGroupProfileError("Fundamental group rank cannot be negative.")
        if normalized_kind == "trivial" and generators:
            raise FundamentalGroupProfileError("A trivial group profile cannot list nontrivial generators.")
        if normalized_kind == "free" and self.rank is None:
            raise FundamentalGroupProfileError("A free group profile needs an explicit rank.")
        if normalized_kind == "free" and self.rank is not None and len(generators) != int(self.rank):
            raise FundamentalGroupProfileError("Free group generator count must match rank.")
        if normalized_kind == "infinite_cyclic" and len(generators) != 1:
            raise FundamentalGroupProfileError("An infinite cyclic profile needs exactly one generator.")
        object.__setattr__(self, "kind", normalized_kind)
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "generators", generators)
        object.__setattr__(self, "rank", None if self.rank is None else int(self.rank))
        object.__setattr__(self, "presentation", str(self.presentation))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "notes", tuple(str(note) for note in self.notes))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified(self) -> bool:
        return self.status == "certified"

    @property
    def is_trivial(self) -> bool:
        return self.kind == "trivial"


def fundamental_group_profile(
    space: Any,
    *,
    basepoint: Any = None,
    kind: str = "profile",
    status: str = "unknown",
    generators: Iterable[str] = (),
    rank: int | None = None,
    presentation: str = "",
    certification: str = "profile",
    notes: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> FundamentalGroupProfile:
    """Build a fundamental group profile without computing pi_1."""

    return FundamentalGroupProfile(
        space=space,
        basepoint=basepoint,
        kind=kind,
        status=status,
        generators=tuple(generators),
        rank=rank,
        presentation=presentation,
        certification=certification,
        notes=tuple(notes),
        metadata=dict(metadata or {}),
    )


def trivial_group_profile(
    space: Any,
    *,
    basepoint: Any = None,
    certification: str = "declared-profile",
    notes: Iterable[str] = (),
) -> FundamentalGroupProfile:
    """Record a trivial fundamental group profile."""

    return fundamental_group_profile(
        space,
        basepoint=basepoint,
        kind="trivial",
        status="certified",
        generators=(),
        rank=0,
        presentation="< >",
        certification=certification,
        notes=notes,
    )


def infinite_cyclic_group_profile(
    space: Any,
    *,
    basepoint: Any = None,
    generator: str = "a",
    certification: str = "declared-profile",
    notes: Iterable[str] = (),
) -> FundamentalGroupProfile:
    """Record an infinite cyclic fundamental group profile."""

    return fundamental_group_profile(
        space,
        basepoint=basepoint,
        kind="infinite_cyclic",
        status="certified",
        generators=(generator,),
        rank=1,
        presentation=f"< {generator} | >",
        certification=certification,
        notes=notes,
    )


def free_group_profile(
    space: Any,
    *,
    basepoint: Any = None,
    generators: Iterable[str],
    certification: str = "declared-profile",
    notes: Iterable[str] = (),
) -> FundamentalGroupProfile:
    """Record a free group profile on the listed generators."""

    normalized_generators = tuple(str(generator) for generator in generators)
    presentation = f"< {', '.join(normalized_generators)} | >" if normalized_generators else "< >"
    return fundamental_group_profile(
        space,
        basepoint=basepoint,
        kind="free",
        status="certified",
        generators=normalized_generators,
        rank=len(normalized_generators),
        presentation=presentation,
        certification=certification,
        notes=notes,
    )


def unknown_fundamental_group_profile(
    space: Any,
    *,
    basepoint: Any = None,
    reason: str = "No fundamental group computation or registry match was supplied.",
) -> FundamentalGroupProfile:
    """Record an explicitly unknown pi_1 profile."""

    return fundamental_group_profile(
        space,
        basepoint=basepoint,
        kind="profile",
        status="unknown",
        certification="unknown",
        notes=(str(reason),),
    )


KNOWN_FUNDAMENTAL_GROUP_MODELS: Mapping[str, FundamentalGroupProfile] = {
    "contractible_space": trivial_group_profile(
        "contractible space",
        basepoint="any point",
        certification="known-model-registry",
        notes=("Contractible spaces have trivial fundamental group.",),
    ),
    "point": trivial_group_profile(
        "one-point space",
        basepoint="*",
        certification="known-model-registry",
        notes=("The one-point space is contractible.",),
    ),
    "closed_interval": trivial_group_profile(
        "[0, 1]",
        basepoint=0,
        certification="known-model-registry",
        notes=("The closed interval is contractible.",),
    ),
    "circle": infinite_cyclic_group_profile(
        "S^1",
        basepoint="1",
        generator="loop",
        certification="known-model-registry",
        notes=("Standard teaching model: pi_1(S^1) is infinite cyclic.",),
    ),
    "wedge_of_two_circles": free_group_profile(
        "S^1 vee S^1",
        basepoint="wedge point",
        generators=("a", "b"),
        certification="known-model-registry",
        notes=("Standard teaching model: rank-two free group.",),
    ),
}


def known_fundamental_group_profile(key: str, *, basepoint: Any = None) -> FundamentalGroupProfile:
    """Return a registered standard model, or an unknown profile."""

    normalized = str(key).strip().lower().replace(" ", "_").replace("-", "_")
    profile = KNOWN_FUNDAMENTAL_GROUP_MODELS.get(normalized)
    if profile is None:
        return unknown_fundamental_group_profile(key, basepoint=basepoint, reason="No registered pi_1 model.")
    if basepoint is None or basepoint == profile.basepoint:
        return profile
    return fundamental_group_profile(
        profile.space,
        basepoint=basepoint,
        kind=profile.kind,
        status=profile.status,
        generators=profile.generators,
        rank=profile.rank,
        presentation=profile.presentation,
        certification=profile.certification,
        notes=profile.notes + ("Basepoint was relabeled by caller; path-connected basepoint transport is assumed only as a profile label.",),
        metadata={**profile.metadata, "basepoint_relabel": True},
    )


def fundamental_group_summary(profile: FundamentalGroupProfile) -> dict[str, Any]:
    return {
        "space": profile.space,
        "basepoint": profile.basepoint,
        "kind": profile.kind,
        "status": profile.status,
        "rank": profile.rank,
        "generators": profile.generators,
        "presentation": profile.presentation,
        "certification": profile.certification,
        "notes": profile.notes,
    }


__all__ = [
    "FundamentalGroupProfile",
    "FundamentalGroupProfileError",
    "GROUP_KINDS",
    "GROUP_PROFILE_STATUSES",
    "KNOWN_FUNDAMENTAL_GROUP_MODELS",
    "free_group_profile",
    "fundamental_group_profile",
    "fundamental_group_summary",
    "infinite_cyclic_group_profile",
    "known_fundamental_group_profile",
    "trivial_group_profile",
    "unknown_fundamental_group_profile",
]
