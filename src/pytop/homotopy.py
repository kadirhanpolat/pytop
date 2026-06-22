"""Profile-based homotopy helpers.

This module records homotopy claims and teaching examples. It deliberately
does not try to solve the general homotopy decision problem.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any


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


# ===========================================================================
# Computational engines — homology-based homotopy invariants
# ===========================================================================


def _face_close(simplices: list[list[Any]]) -> list[list[Any]]:
    from itertools import combinations

    seen: set[frozenset] = set()
    result: list[list[Any]] = []
    for s in simplices:
        for r in range(1, len(s) + 1):
            for face in combinations(s, r):
                fs = frozenset(face)
                if fs not in seen:
                    seen.add(fs)
                    result.append(list(face))
    return result


def is_contractible_simplicial(simplices: list[list[Any]]) -> bool:
    """Test whether a finite simplicial complex is acyclic (contractible homology).

    Returns ``True`` iff ``H_*(X; ℤ) ≅ H_*(point; ℤ)``:

    * H₀(X; ℤ) = ℤ  (connected, one component)
    * H_k(X; ℤ) = 0  for all k ≥ 1

    For CW complexes of dimension ≤ 2 this condition is equivalent to
    contractibility by Whitehead's theorem.  For higher dimensions it is
    a necessary condition (homological contractibility).

    Parameters
    ----------
    simplices:
        List of simplices as lists of vertex labels, e.g.
        ``[[0, 1, 2], [1, 2], [0, 2]]``.  Face closure is enforced
        automatically.

    Returns
    -------
    bool

    Examples
    --------
    A filled triangle is contractible:

    >>> is_contractible_simplicial([[0, 1, 2], [0, 1], [0, 2], [1, 2], [0], [1], [2]])
    True

    The boundary of a triangle (circle S¹) is not contractible:

    >>> is_contractible_simplicial([[0, 1], [1, 2], [2, 0]])
    False
    """
    from .homology import homology_groups
    from .simplicial_complexes import simplicial_complex

    sc = simplicial_complex(_face_close(simplices))
    groups = homology_groups(sc)
    if not groups:
        return False
    h0 = groups[0]
    if h0.betti != 1 or h0.torsion:
        return False
    for h in groups[1:]:
        if h.betti != 0 or h.torsion:
            return False
    return True


def has_sphere_homology(simplices: list[list[Any]], n: int) -> bool:
    """Test whether a simplicial complex has the homology of S^n.

    Returns ``True`` iff ``H_*(X; ℤ) ≅ H_*(S^n; ℤ)``:

    * For n ≥ 1: H₀ = ℤ, H_n = ℤ, H_k = 0 otherwise.
    * For n = 0: H₀ = ℤ² (two components), H_k = 0 for k ≥ 1.

    By Whitehead's theorem, for simply-connected CW complexes of dimension n,
    this implies actual homotopy equivalence to S^n.

    Parameters
    ----------
    simplices:
        Simplices as lists of vertex labels.
    n:
        The dimension of the sphere to compare against.

    Returns
    -------
    bool
    """
    if n < 0:
        raise ValueError(f"Sphere dimension must be non-negative, got {n!r}")

    from .homology import homology_groups
    from .simplicial_complexes import simplicial_complex

    sc = simplicial_complex(_face_close(simplices))
    groups = homology_groups(sc)
    h_by_degree = {g.degree: g for g in groups}

    expected_h0_betti = 2 if n == 0 else 1
    h0 = h_by_degree.get(0)
    if h0 is None or h0.betti != expected_h0_betti or h0.torsion:
        return False

    if n >= 1:
        hn = h_by_degree.get(n)
        if hn is None or hn.betti != 1 or hn.torsion:
            return False

    for g in groups:
        if g.degree == 0:
            continue
        if g.degree == n and n >= 1:
            continue
        if g.betti != 0 or g.torsion:
            return False

    return True


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
    "has_sphere_homology",
    "homotopic",
    "homotopy_profile",
    "homotopy_summary",
    "is_contractible_simplicial",
    "known_contractible_profile",
    "not_certified_homotopy",
    "unknown_homotopy",
]
