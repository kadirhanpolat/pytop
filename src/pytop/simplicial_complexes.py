"""Finite simplicial complex helpers for the geometric topology bridge."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .simplices import Simplex


class SimplicialComplexError(ValueError):
    """Raised when a finite simplicial complex fails validation."""


@dataclass(frozen=True)
class SimplicialComplexDiagnostic:
    """Validation diagnostics for a finite simplex family."""

    is_face_closed: bool
    missing_faces: tuple[frozenset[Any], ...] = ()


@dataclass(frozen=True)
class SimplicialComplex:
    """A finite abstract simplicial complex.

    The family stores nonempty simplexes only. The empty face is treated as a
    standard background convention and is not materialized as a ``Simplex``.
    """

    simplexes: frozenset[Simplex]
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __init__(
        self,
        simplexes: Iterable[Simplex | Iterable[Any]],
        *,
        metadata: dict[str, Any] | None = None,
        require_face_closed: bool = True,
    ) -> None:
        normalized = frozenset(_coerce_simplex(item) for item in simplexes)
        if not normalized:
            raise SimplicialComplexError("A simplicial complex requires at least one nonempty simplex.")
        diagnostic = face_closure_diagnostic(normalized)
        if require_face_closed and not diagnostic.is_face_closed:
            raise SimplicialComplexError(
                "The simplex family is not face-closed; inspect face_closure_diagnostic for missing faces."
            )
        object.__setattr__(self, "simplexes", normalized)
        object.__setattr__(self, "metadata", dict(metadata or {}))

    @property
    def vertices(self) -> frozenset[Any]:
        return frozenset().union(*(simplex.vertices for simplex in self.simplexes))

    @property
    def dimension(self) -> int:
        return max(simplex.dimension for simplex in self.simplexes)

    def facets(self) -> set[Simplex]:
        """Return inclusion-maximal simplexes."""

        return {
            candidate
            for candidate in self.simplexes
            if not any(candidate.vertices < other.vertices for other in self.simplexes)
        }

    def skeleton(self, dimension: int) -> "SimplicialComplex":
        """Return the subcomplex of simplexes of dimension at most ``dimension``."""

        if dimension < 0:
            raise SimplicialComplexError("Skeleton dimension must be nonnegative.")
        members = [simplex for simplex in self.simplexes if simplex.dimension <= dimension]
        if not members:
            raise SimplicialComplexError("The requested skeleton has no nonempty simplexes.")
        return SimplicialComplex(members, metadata={"source": "skeleton", "dimension": dimension})

    def simplexes_by_dimension(self, dimension: int) -> set[Simplex]:
        return {simplex for simplex in self.simplexes if simplex.dimension == dimension}

    def f_vector(self) -> tuple[int, ...]:
        """Return counts of simplexes by dimension, from 0 through dimension."""

        return tuple(len(self.simplexes_by_dimension(dim)) for dim in range(self.dimension + 1))

    def euler_characteristic(self) -> int:
        """Return the introductory Euler characteristic alternating sum."""

        return sum(((-1) ** dim) * count for dim, count in enumerate(self.f_vector()))

    def one_skeleton_edges(self) -> set[frozenset[Any]]:
        """Return vertex-pair edges in the 1-skeleton."""

        return {simplex.vertices for simplex in self.simplexes if simplex.dimension == 1}

    def connectedness_preview(self) -> dict[str, Any]:
        """Return a graph-based connectedness preview for the 1-skeleton.

        This is a finite graph diagnostic, not a theorem prover for arbitrary
        topological connectedness.
        """

        vertices = set(self.vertices)
        if not vertices:
            return {"connected": False, "components": ()}
        adjacency = {vertex: set() for vertex in vertices}
        for edge in self.one_skeleton_edges():
            left, right = tuple(edge)
            adjacency[left].add(right)
            adjacency[right].add(left)
        components: list[frozenset[Any]] = []
        unseen = set(vertices)
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
        return {"connected": len(components) == 1, "components": tuple(sorted(components, key=lambda c: sorted(map(repr, c))))}


def simplicial_complex(
    simplexes: Iterable[Simplex | Iterable[Any]],
    *,
    metadata: dict[str, Any] | None = None,
    require_face_closed: bool = True,
) -> SimplicialComplex:
    """Convenience constructor for :class:`SimplicialComplex`."""

    return SimplicialComplex(simplexes, metadata=metadata, require_face_closed=require_face_closed)


def generated_subcomplex(generators: Iterable[Simplex | Iterable[Any]]) -> SimplicialComplex:
    """Generate the smallest nonempty-face complex containing the generators."""

    generated: set[Simplex] = set()
    for item in generators:
        simplex = _coerce_simplex(item)
        generated.update(simplex.faces())
    return SimplicialComplex(generated, metadata={"construction": "generated_subcomplex"})


def face_closure_diagnostic(simplexes: Iterable[Simplex | Iterable[Any]]) -> SimplicialComplexDiagnostic:
    family = frozenset(_coerce_simplex(item) for item in simplexes)
    present = {simplex.vertices for simplex in family}
    missing: set[frozenset[Any]] = set()
    for simplex in family:
        for face in simplex.faces():
            if face.vertices not in present:
                missing.add(face.vertices)
    return SimplicialComplexDiagnostic(
        is_face_closed=not missing,
        missing_faces=tuple(sorted(missing, key=lambda face: (len(face), sorted(map(repr, face))))),
    )


def simplicial_complex_summary(complex_obj: SimplicialComplex) -> dict[str, Any]:
    """Return a compact report for examples and tests."""

    return {
        "vertex_count": len(complex_obj.vertices),
        "simplex_count": len(complex_obj.simplexes),
        "dimension": complex_obj.dimension,
        "facet_count": len(complex_obj.facets()),
        "f_vector": complex_obj.f_vector(),
        "euler_characteristic": complex_obj.euler_characteristic(),
        "one_skeleton_edges": tuple(sorted(complex_obj.one_skeleton_edges(), key=lambda edge: sorted(map(repr, edge)))),
        "connectedness_preview": complex_obj.connectedness_preview(),
    }


def _coerce_simplex(item: Simplex | Iterable[Any]) -> Simplex:
    if isinstance(item, Simplex):
        return item
    return Simplex(item)


__all__ = [
    "SimplicialComplex",
    "SimplicialComplexDiagnostic",
    "SimplicialComplexError",
    "simplicial_complex",
    "generated_subcomplex",
    "face_closure_diagnostic",
    "simplicial_complex_summary",
]
