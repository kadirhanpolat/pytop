"""Constructive classification of closed surfaces from a polygon gluing word.

Given the boundary word of a polygon with edge identifications (the format used
by :mod:`pytop.surface_gluing`, e.g. ``"a b a^-1 b^-1"``), this computes the
genuine topological type of the resulting closed surface:

* the **Euler characteristic** ``chi = V - E + F`` (``F = 1``, ``E`` = number of
  edge labels, ``V`` = number of vertex classes after identification),
* **orientability** (orientable iff every label occurs once as ``x`` and once as
  ``x^-1``),
* the **genus**, and a human-readable classification name.

This realizes the classification theorem of compact surfaces as an algorithm,
complementing the descriptive profiles in :mod:`pytop.surface_classification`.
Words with unpaired (boundary) edges are detected and reported but not assigned a
closed-surface genus.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .surface_gluing import SurfaceGluingError, parse_edge_word, validate_edge_pairing


@dataclass(frozen=True)
class SurfaceClassification:
    """The topological type of the surface built from a polygon word."""

    euler_characteristic: int
    orientable: bool
    genus: int | None
    has_boundary: bool
    name: str


def _vertex_class_count(tokens: tuple[Any, ...]) -> int:
    """Count vertex equivalence classes of the polygon corners after gluing.

    Corner ``i`` sits between edges ``i-1`` and ``i``. Each label's two
    occurrences identify their tail-corners together and their head-corners
    together (tail/head taken with respect to the label's intrinsic direction).
    """

    n = len(tokens)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        parent[find(a)] = find(b)

    # For each label collect the tail-corner and head-corner of every occurrence.
    tails: dict[str, list[int]] = {}
    heads: dict[str, list[int]] = {}
    for i, token in enumerate(tokens):
        nxt = (i + 1) % n
        if token.orientation == 1:
            tail, head = i, nxt
        else:
            tail, head = nxt, i
        tails.setdefault(token.label, []).append(tail)
        heads.setdefault(token.label, []).append(head)

    for label in tails:
        corners = tails[label]
        for other in corners[1:]:
            union(corners[0], other)
        hcorners = heads[label]
        for other in hcorners[1:]:
            union(hcorners[0], other)

    return len({find(i) for i in range(n)})


def _name(orientable: bool, genus: int) -> str:
    if orientable:
        if genus == 0:
            return "sphere"
        if genus == 1:
            return "torus"
        return f"orientable genus-{genus} surface"
    if genus == 1:
        return "projective plane"
    if genus == 2:
        return "Klein bottle"
    return f"non-orientable genus-{genus} surface"


def classify_surface_word(edge_word: Any) -> SurfaceClassification:
    """Classify the closed surface determined by a polygon gluing ``edge_word``.

    Raises :class:`~pytop.surface_gluing.SurfaceGluingError` if a label occurs
    more than twice (not a valid surface identification).
    """

    tokens = parse_edge_word(edge_word)
    if not tokens:
        raise SurfaceGluingError("An edge word must contain at least one edge.")
    diagnostic = validate_edge_pairing(edge_word, allow_boundary_edges=True)
    if diagnostic.overused_labels:
        raise SurfaceGluingError(
            f"Labels used more than twice are not surface identifications: {diagnostic.overused_labels}"
        )

    has_boundary = bool(diagnostic.boundary_labels)
    edge_count = len({token.label for token in tokens})
    face_count = 1
    vertex_count = _vertex_class_count(tokens)
    chi = vertex_count - edge_count + face_count

    # orientable iff every (paired) label appears once with each orientation
    orientations: dict[str, list[int]] = {}
    for token in tokens:
        orientations.setdefault(token.label, []).append(token.orientation)
    orientable = all(
        sorted(orients) == [-1, 1]
        for label, orients in orientations.items()
        if len(orients) == 2
    )

    if has_boundary:
        return SurfaceClassification(
            euler_characteristic=chi,
            orientable=orientable,
            genus=None,
            has_boundary=True,
            name="surface with boundary",
        )

    if orientable:
        genus = (2 - chi) // 2
    else:
        genus = 2 - chi
    return SurfaceClassification(
        euler_characteristic=chi,
        orientable=orientable,
        genus=genus,
        has_boundary=False,
        name=_name(orientable, genus),
    )


__all__ = [
    "SurfaceClassification",
    "classify_surface_word",
]
