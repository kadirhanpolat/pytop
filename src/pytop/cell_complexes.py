"""Teaching-level finite cell complex profiles for the geometric bridge."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


class CellComplexError(ValueError):
    """Raised when a teaching-level cell complex profile is malformed."""


@dataclass(frozen=True)
class Cell:
    """A finite cell record with dimension and attaching description."""

    name: str
    dimension: int
    attaching: str = "not specified"
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not str(self.name).strip():
            raise CellComplexError("A cell needs a nonempty name.")
        if self.dimension < 0:
            raise CellComplexError("A cell dimension must be nonnegative.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "attaching", str(self.attaching))
        object.__setattr__(self, "metadata", dict(self.metadata))


@dataclass(frozen=True)
class CellComplexProfile:
    """A finite, teaching-level cell complex profile.

    This is not a CW-complex validator. It records finite cells, dimensions,
    attaching language, and optional links to simplicial-complex data.
    """

    name: str
    cells: tuple[Cell, ...]
    relation_to_simplicial_complex: str = "not specified"
    certification: str = "teaching-profile"
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not str(self.name).strip():
            raise CellComplexError("A cell complex profile needs a nonempty name.")
        normalized = tuple(self.cells)
        if not normalized:
            raise CellComplexError("A cell complex profile needs at least one cell.")
        names = [cell.name for cell in normalized]
        if len(names) != len(set(names)):
            raise CellComplexError("Cell names must be unique within a profile.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "cells", normalized)
        object.__setattr__(self, "relation_to_simplicial_complex", str(self.relation_to_simplicial_complex))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def dimension(self) -> int:
        return max(cell.dimension for cell in self.cells)

    @property
    def cell_count(self) -> int:
        return len(self.cells)

    def cells_by_dimension(self, dimension: int) -> tuple[Cell, ...]:
        return tuple(cell for cell in self.cells if cell.dimension == dimension)

    def cell_counts_by_dimension(self) -> dict[int, int]:
        return {dim: len(self.cells_by_dimension(dim)) for dim in range(self.dimension + 1)}

    def attaching_descriptions(self) -> dict[str, str]:
        return {cell.name: cell.attaching for cell in self.cells}


def cell(name: str, dimension: int, attaching: str = "not specified", *, metadata: dict[str, Any] | None = None) -> Cell:
    """Convenience constructor for :class:`Cell`."""

    return Cell(name=name, dimension=dimension, attaching=attaching, metadata=dict(metadata or {}))


def cell_complex_profile(
    name: str,
    cells: Iterable[Cell],
    *,
    relation_to_simplicial_complex: str = "not specified",
    metadata: dict[str, Any] | None = None,
) -> CellComplexProfile:
    """Build a finite teaching-level cell complex profile."""

    return CellComplexProfile(
        name=name,
        cells=tuple(cells),
        relation_to_simplicial_complex=relation_to_simplicial_complex,
        metadata=dict(metadata or {}),
    )


def validate_finite_cell_profile(profile: CellComplexProfile) -> bool:
    """Return whether the profile satisfies the package's finite-cell checks."""

    try:
        CellComplexProfile(
            name=profile.name,
            cells=profile.cells,
            relation_to_simplicial_complex=profile.relation_to_simplicial_complex,
            metadata=profile.metadata,
        )
    except CellComplexError:
        return False
    return profile.certification == "teaching-profile"


def cell_complex_summary(profile: CellComplexProfile) -> dict[str, Any]:
    """Return a compact summary for examples and later route checks."""

    return {
        "name": profile.name,
        "dimension": profile.dimension,
        "cell_count": profile.cell_count,
        "cell_counts_by_dimension": profile.cell_counts_by_dimension(),
        "attaching_descriptions": profile.attaching_descriptions(),
        "relation_to_simplicial_complex": profile.relation_to_simplicial_complex,
        "certification": profile.certification,
    }


def simplex_as_cell_profile(simplex_dimension: int, *, name: str | None = None) -> CellComplexProfile:
    """Return the usual teaching profile for one closed n-simplex.

    The profile has one cell in each dimension 0..n. It is a mnemonic bridge,
    not a geometric realization theorem.
    """

    if simplex_dimension < 0:
        raise CellComplexError("Simplex dimension must be nonnegative.")
    cells = [
        Cell(
            name=f"e{dim}",
            dimension=dim,
            attaching="new vertex" if dim == 0 else f"attached along previously listed lower-dimensional cells up to dimension {dim - 1}",
        )
        for dim in range(simplex_dimension + 1)
    ]
    return CellComplexProfile(
        name=name or f"closed_{simplex_dimension}_simplex_profile",
        cells=tuple(cells),
        relation_to_simplicial_complex="Mnemonic profile associated with one closed simplex; not a CW validation theorem.",
    )


__all__ = [
    "Cell",
    "CellComplexProfile",
    "CellComplexError",
    "cell",
    "cell_complex_profile",
    "validate_finite_cell_profile",
    "cell_complex_summary",
    "simplex_as_cell_profile",
]
