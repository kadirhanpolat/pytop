"""Profile-based path and path-connectedness helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


class PathProfileError(ValueError):
    """Raised when path profile data is malformed."""


@dataclass(frozen=True)
class PathProfile:
    """A symbolic or finite-sample path profile.

    The points field is a finite sample or teaching trace. It is not an
    analytic continuity certificate for arbitrary functions.
    """

    name: str
    start: Any
    end: Any
    points: tuple[Any, ...] = ()
    certification: str = "profile"
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not str(self.name).strip():
            raise PathProfileError("A path profile needs a nonempty name.")
        normalized = tuple(self.points)
        if normalized:
            if normalized[0] != self.start:
                raise PathProfileError("The first sampled point must match the path start.")
            if normalized[-1] != self.end:
                raise PathProfileError("The last sampled point must match the path end.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "points", normalized)
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_loop(self) -> bool:
        return self.start == self.end

    def reverse(self, *, name: str | None = None) -> "PathProfile":
        return PathProfile(
            name=name or f"{self.name}_reverse",
            start=self.end,
            end=self.start,
            points=tuple(reversed(self.points)) if self.points else (),
            certification=self.certification,
            metadata={**self.metadata, "operation": "reverse"},
        )

    def concatenate(self, other: "PathProfile", *, name: str | None = None) -> "PathProfile":
        if self.end != other.start:
            raise PathProfileError("Paths can be concatenated only when the first end equals the second start.")
        if self.points and other.points:
            points = self.points + other.points[1:]
        else:
            points = ()
        return PathProfile(
            name=name or f"{self.name}_then_{other.name}",
            start=self.start,
            end=other.end,
            points=points,
            certification=_combined_certification(self.certification, other.certification),
            metadata={"operation": "concatenate", "first": self.name, "second": other.name},
        )


@dataclass(frozen=True)
class PathConnectednessDiagnostic:
    """Finite/profile diagnostic for path-connectedness."""

    carrier: frozenset[Any]
    connected: bool | None
    components: tuple[frozenset[Any], ...]
    certification: str
    notes: tuple[str, ...] = ()


def path_profile(
    name: str,
    start: Any,
    end: Any,
    *,
    points: Iterable[Any] = (),
    certification: str = "profile",
    metadata: dict[str, Any] | None = None,
) -> PathProfile:
    """Convenience constructor for :class:`PathProfile`."""

    return PathProfile(
        name=name,
        start=start,
        end=end,
        points=tuple(points),
        certification=certification,
        metadata=dict(metadata or {}),
    )


def is_loop_path(path: PathProfile) -> bool:
    return path.is_loop


def reverse_path_profile(path: PathProfile, *, name: str | None = None) -> PathProfile:
    return path.reverse(name=name)


def concatenate_path_profiles(first: PathProfile, second: PathProfile, *, name: str | None = None) -> PathProfile:
    return first.concatenate(second, name=name)


def path_connectedness_diagnostic(
    carrier: Iterable[Any],
    paths: Iterable[PathProfile],
    *,
    certification: str = "finite-path-graph",
) -> PathConnectednessDiagnostic:
    """Diagnose path-connectedness from a finite family of known paths.

    The diagnostic builds an undirected graph whose edges are known path
    endpoints. It is exact only for the finite recorded path graph, not for an
    arbitrary topological space.
    """

    points = frozenset(carrier)
    if not points:
        raise PathProfileError("Path-connectedness diagnostics require a nonempty carrier.")
    adjacency = {point: set() for point in points}
    for path in paths:
        if path.start not in points or path.end not in points:
            raise PathProfileError("Every path endpoint must belong to the carrier.")
        adjacency[path.start].add(path.end)
        adjacency[path.end].add(path.start)
    unseen = set(points)
    components: list[frozenset[Any]] = []
    while unseen:
        start = unseen.pop()
        component = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(frozenset(component))
    connected = len(components) == 1
    notes = (
        "Graph diagnostic built from recorded path endpoints.",
        "This does not certify analytic continuity of arbitrary path maps.",
        "Connectedness and path-connectedness are distinct notions.",
    )
    return PathConnectednessDiagnostic(
        carrier=points,
        connected=connected,
        components=tuple(sorted(components, key=lambda c: sorted(map(repr, c)))),
        certification=certification,
        notes=notes,
    )


def path_profile_summary(path: PathProfile) -> dict[str, Any]:
    return {
        "name": path.name,
        "start": path.start,
        "end": path.end,
        "is_loop": path.is_loop,
        "sample_count": len(path.points),
        "certification": path.certification,
    }


def _combined_certification(first: str, second: str) -> str:
    if first == second:
        return first
    return "composite-profile"


__all__ = [
    "PathProfile",
    "PathProfileError",
    "PathConnectednessDiagnostic",
    "path_profile",
    "is_loop_path",
    "reverse_path_profile",
    "concatenate_path_profiles",
    "path_connectedness_diagnostic",
    "path_profile_summary",
]
