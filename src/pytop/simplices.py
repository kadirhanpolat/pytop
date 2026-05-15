"""Small combinatorial simplex model for the geometric topology bridge."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Iterable


class SimplexError(ValueError):
    """Raised when a simplex construction receives invalid vertex data."""


@dataclass(frozen=True)
class Simplex:
    """A finite abstract simplex, represented only by its vertex set.

    This is the combinatorial layer needed before simplicial complexes and
    polyhedra. It intentionally avoids coordinates, PL topology, and homology.
    """

    vertices: frozenset[Any]
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __init__(self, vertices: Iterable[Any], metadata: dict[str, Any] | None = None) -> None:
        normalized = frozenset(vertices)
        if not normalized:
            raise SimplexError("A simplex must have at least one vertex.")
        object.__setattr__(self, "vertices", normalized)
        object.__setattr__(self, "metadata", dict(metadata or {}))

    @property
    def dimension(self) -> int:
        """Return the simplex dimension, equal to ``len(vertices) - 1``."""

        return len(self.vertices) - 1

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    def faces(self, *, include_empty: bool = False) -> set["Simplex"]:
        """Return all nonempty faces, optionally including no empty face.

        The empty face is not materialized as a ``Simplex`` because this module
        treats a simplex as a nonempty finite vertex set.
        """

        start = 1
        if include_empty:
            raise SimplexError("The empty face is tracked conceptually but is not represented as a Simplex.")
        return {
            Simplex(face)
            for size in range(start, len(self.vertices) + 1)
            for face in combinations(_ordered_vertices(self.vertices), size)
        }

    def proper_faces(self) -> set["Simplex"]:
        """Return all nonempty faces other than the simplex itself."""

        return {face for face in self.faces() if face.vertices != self.vertices}

    def boundary_faces(self) -> set["Simplex"]:
        """Return codimension-one faces.

        A 0-simplex has no nonempty boundary face in this representation.
        """

        if self.dimension == 0:
            return set()
        size = len(self.vertices) - 1
        return {Simplex(face) for face in combinations(_ordered_vertices(self.vertices), size)}

    def contains_face(self, candidate: "Simplex | Iterable[Any]") -> bool:
        face = candidate.vertices if isinstance(candidate, Simplex) else frozenset(candidate)
        return bool(face) and face.issubset(self.vertices)

    def face_dimensions(self) -> dict[int, int]:
        """Return the number of nonempty faces in each dimension."""

        return {
            dimension: len([face for face in self.faces() if face.dimension == dimension])
            for dimension in range(self.dimension + 1)
        }


def simplex(vertices: Iterable[Any], *, metadata: dict[str, Any] | None = None) -> Simplex:
    """Convenience constructor for :class:`Simplex`."""

    return Simplex(vertices, metadata=metadata)


def validate_simplex(candidate: Simplex | Iterable[Any]) -> bool:
    """Return whether the candidate can be represented as a nonempty simplex."""

    if isinstance(candidate, Simplex):
        return bool(candidate.vertices)
    try:
        return bool(frozenset(candidate))
    except TypeError:
        return False


def simplex_boundary_vertices(simplex_obj: Simplex) -> set[frozenset[Any]]:
    """Return codimension-one boundary faces as vertex sets."""

    return {face.vertices for face in simplex_obj.boundary_faces()}


def simplex_summary(simplex_obj: Simplex) -> dict[str, Any]:
    """Return a small report useful for examples and later complex checks."""

    return {
        "vertices": tuple(_ordered_vertices(simplex_obj.vertices)),
        "dimension": simplex_obj.dimension,
        "vertex_count": simplex_obj.vertex_count,
        "face_count": len(simplex_obj.faces()),
        "proper_face_count": len(simplex_obj.proper_faces()),
        "boundary_face_count": len(simplex_obj.boundary_faces()),
        "face_dimensions": simplex_obj.face_dimensions(),
    }


def _ordered_vertices(vertices: Iterable[Any]) -> tuple[Any, ...]:
    return tuple(sorted(vertices, key=repr))


__all__ = [
    "Simplex",
    "SimplexError",
    "simplex",
    "validate_simplex",
    "simplex_boundary_vertices",
    "simplex_summary",
]
