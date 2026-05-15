"""Profile-based homotopy helpers.

This module records homotopy claims and teaching examples. It deliberately
does not try to solve the general homotopy decision problem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


class HomotopyProfileError(ValueError):
    """Raised when homotopy profile data is malformed."""


HOMOTOPY_STATUSES = frozenset({"homotopic", "not_certified", "unknown"})
RETRACTION_STATUSES = frozenset({"certified", "not_certified", "unknown"})
CONTRACTIBLE_STATUSES = frozenset({"certified", "not_certified", "unknown"})


@dataclass(frozen=True)
class HomotopyProfile:
    """A symbolic homotopy profile between two maps or path profiles.

    The status is a profile label. Unknown and not-certified cases are kept
    explicit so callers do not accidentally treat a missing proof as a
    negative theorem.
    """

    name: str
    source: Any
    target: Any
    status: str = "not_certified"
    relative_to: frozenset[Any] = frozenset()
    certification: str = "profile"
    witness: str = ""
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        normalized_status = str(self.status)
        if normalized_status not in HOMOTOPY_STATUSES:
            raise HomotopyProfileError(f"Unsupported homotopy status: {self.status!r}.")
        if not str(self.name).strip():
            raise HomotopyProfileError("A homotopy profile needs a nonempty name.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "relative_to", frozenset(self.relative_to))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "witness", str(self.witness))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified_homotopy(self) -> bool:
        return self.status == "homotopic"

    @property
    def has_relative_label(self) -> bool:
        return bool(self.relative_to)


@dataclass(frozen=True)
class DeformationRetractionProfile:
    """A symbolic deformation-retraction profile for a subspace."""

    name: str
    space: Any
    subspace: Any
    status: str = "not_certified"
    strong: bool = False
    certification: str = "profile"
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        normalized_status = str(self.status)
        if normalized_status not in RETRACTION_STATUSES:
            raise HomotopyProfileError(f"Unsupported deformation-retraction status: {self.status!r}.")
        if not str(self.name).strip():
            raise HomotopyProfileError("A deformation-retraction profile needs a nonempty name.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "strong", bool(self.strong))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "notes", tuple(str(note) for note in self.notes))


@dataclass(frozen=True)
class ContractibleProfile:
    """A conservative profile for a contractibility claim."""

    space: Any
    status: str = "unknown"
    witness: str = ""
    certification: str = "profile"
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        normalized_status = str(self.status)
        if normalized_status not in CONTRACTIBLE_STATUSES:
            raise HomotopyProfileError(f"Unsupported contractible status: {self.status!r}.")
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "witness", str(self.witness))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "notes", tuple(str(note) for note in self.notes))

    @property
    def is_certified_contractible(self) -> bool:
        return self.status == "certified"


KNOWN_CONTRACTIBLE_EXAMPLES: Mapping[str, ContractibleProfile] = {
    "point": ContractibleProfile(
        space="one-point space",
        status="certified",
        witness="constant contraction",
        certification="known-example-registry",
        notes=("Finite one-point space is contractible.",),
    ),
    "closed_interval": ContractibleProfile(
        space="[0, 1]",
        status="certified",
        witness="straight-line homotopy to 0",
        certification="known-example-registry",
        notes=("Convex subset of the real line.",),
    ),
    "convex_disk": ContractibleProfile(
        space="closed convex disk",
        status="certified",
        witness="linear contraction to a chosen center",
        certification="known-example-registry",
        notes=("Registered as a convex Euclidean example.",),
    ),
    "filled_simplex": ContractibleProfile(
        space="filled simplex",
        status="certified",
        witness="linear contraction to a vertex or barycenter",
        certification="known-example-registry",
        notes=("Applies to the filled geometric simplex, not only its boundary.",),
    ),
}


def homotopy_profile(
    name: str,
    source: Any,
    target: Any,
    *,
    status: str = "not_certified",
    relative_to: Iterable[Any] = (),
    certification: str = "profile",
    witness: str = "",
    metadata: dict[str, Any] | None = None,
) -> HomotopyProfile:
    """Convenience constructor for :class:`HomotopyProfile`."""

    return HomotopyProfile(
        name=name,
        source=source,
        target=target,
        status=status,
        relative_to=frozenset(relative_to),
        certification=certification,
        witness=witness,
        metadata=dict(metadata or {}),
    )


def homotopic(
    source: Any,
    target: Any,
    *,
    name: str | None = None,
    relative_to: Iterable[Any] = (),
    certification: str = "declared-profile",
    witness: str = "",
    metadata: dict[str, Any] | None = None,
) -> HomotopyProfile:
    """Record a positive homotopy claim with an explicit certification label."""

    return homotopy_profile(
        name=name or f"{source!r}_homotopic_to_{target!r}",
        source=source,
        target=target,
        status="homotopic",
        relative_to=relative_to,
        certification=certification,
        witness=witness,
        metadata=metadata,
    )


def not_certified_homotopy(
    source: Any,
    target: Any,
    *,
    name: str | None = None,
    reason: str = "No homotopy certificate has been supplied.",
    relative_to: Iterable[Any] = (),
) -> HomotopyProfile:
    """Record that the current data does not certify a homotopy."""

    return homotopy_profile(
        name=name or f"{source!r}_to_{target!r}_not_certified",
        source=source,
        target=target,
        status="not_certified",
        relative_to=relative_to,
        certification="absence-of-certificate",
        metadata={"reason": str(reason)},
    )


def unknown_homotopy(
    source: Any,
    target: Any,
    *,
    name: str | None = None,
    relative_to: Iterable[Any] = (),
    reason: str = "No decision procedure was applied.",
) -> HomotopyProfile:
    """Record an explicitly unknown homotopy relation."""

    return homotopy_profile(
        name=name or f"{source!r}_to_{target!r}_unknown",
        source=source,
        target=target,
        status="unknown",
        relative_to=relative_to,
        certification="unknown",
        metadata={"reason": str(reason)},
    )


def deformation_retraction_profile(
    name: str,
    space: Any,
    subspace: Any,
    *,
    status: str = "not_certified",
    strong: bool = False,
    certification: str = "profile",
    notes: Iterable[str] = (),
) -> DeformationRetractionProfile:
    """Build a deformation-retraction profile without proving it automatically."""

    return DeformationRetractionProfile(
        name=name,
        space=space,
        subspace=subspace,
        status=status,
        strong=strong,
        certification=certification,
        notes=tuple(notes),
    )


def contractible_profile(
    space: Any,
    *,
    status: str = "unknown",
    witness: str = "",
    certification: str = "profile",
    notes: Iterable[str] = (),
) -> ContractibleProfile:
    """Build a contractibility profile."""

    return ContractibleProfile(
        space=space,
        status=status,
        witness=witness,
        certification=certification,
        notes=tuple(notes),
    )


def known_contractible_profile(key: str) -> ContractibleProfile:
    """Return a safe registered contractible example, or an unknown profile."""

    normalized = str(key).strip().lower().replace(" ", "_").replace("-", "_")
    if normalized in KNOWN_CONTRACTIBLE_EXAMPLES:
        return KNOWN_CONTRACTIBLE_EXAMPLES[normalized]
    return ContractibleProfile(
        space=str(key),
        status="unknown",
        certification="known-example-registry",
        notes=("No contractibility claim is registered for this key.",),
    )


def homotopy_summary(profile: HomotopyProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "source": profile.source,
        "target": profile.target,
        "status": profile.status,
        "relative_to": tuple(sorted(profile.relative_to, key=repr)),
        "certification": profile.certification,
        "has_witness": bool(profile.witness),
    }


def deformation_retraction_summary(profile: DeformationRetractionProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "space": profile.space,
        "subspace": profile.subspace,
        "status": profile.status,
        "strong": profile.strong,
        "certification": profile.certification,
        "notes": profile.notes,
    }


def contractible_summary(profile: ContractibleProfile) -> dict[str, Any]:
    return {
        "space": profile.space,
        "status": profile.status,
        "certification": profile.certification,
        "has_witness": bool(profile.witness),
        "notes": profile.notes,
    }


__all__ = [
    "ContractibleProfile",
    "CONTRACTIBLE_STATUSES",
    "DeformationRetractionProfile",
    "HOMOTOPY_STATUSES",
    "HomotopyProfile",
    "HomotopyProfileError",
    "KNOWN_CONTRACTIBLE_EXAMPLES",
    "RETRACTION_STATUSES",
    "contractible_profile",
    "contractible_summary",
    "deformation_retraction_profile",
    "deformation_retraction_summary",
    "homotopic",
    "homotopy_profile",
    "homotopy_summary",
    "known_contractible_profile",
    "not_certified_homotopy",
    "unknown_homotopy",
]
