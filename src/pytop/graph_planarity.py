"""Exact planarity and genus of small graphs via rotation-system search.

A combinatorial embedding of a graph in an orientable surface is a *rotation
system*: a cyclic ordering of the edges around each vertex. Tracing the faces of
a rotation system and applying Euler's formula gives the genus of that embedding;
the minimum genus over all rotation systems is the (orientable) genus of the
graph, and the graph is planar iff that minimum is ``0``.

This module computes the genus exactly by enumerating rotation systems. That is
exponential in the vertex degrees, so it is intended for small graphs (the
canonical examples K5, K3,3, the Petersen graph, wheels, etc. are all well within
reach). A guard raises :class:`GraphPlanarityError` if the search space is too
large, rather than hanging.

This is the constructive companion to the descriptive ``graph_topology``
profiles: it actually decides planarity and computes genus from an edge list.
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import permutations
from math import factorial
from typing import Any

Edge = tuple[Any, Any]

# Cap on the number of rotation systems to enumerate before giving up.
_MAX_ROTATIONS = 2_000_000


class GraphPlanarityError(ValueError):
    """Raised for malformed input or a search space that is too large."""


def _adjacency(vertices: Iterable[Any], edges: Iterable[Edge]) -> dict[Any, set[Any]]:
    adjacency: dict[Any, set[Any]] = {v: set() for v in vertices}
    for u, v in edges:
        if u == v:
            continue  # ignore self-loops (irrelevant to planarity)
        adjacency.setdefault(u, set()).add(v)
        adjacency.setdefault(v, set()).add(u)
    return adjacency


def _components(adjacency: dict[Any, set[Any]]) -> list[set[Any]]:
    seen: set[Any] = set()
    components: list[set[Any]] = []
    for start in adjacency:
        if start in seen:
            continue
        stack = [start]
        component: set[Any] = set()
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            component.add(node)
            stack.extend(adjacency[node] - seen)
        components.append(component)
    return components


def _count_faces(rotation: dict[Any, list[Any]]) -> int:
    """Count faces of a rotation system by tracing the face permutation.

    The face permutation is ``phi(dart) = sigma(reverse(dart))`` where ``sigma``
    advances to the next dart in the rotation at the dart's head.
    """

    next_in_rotation: dict[tuple[Any, Any], tuple[Any, Any]] = {}
    for vertex, order in rotation.items():
        degree = len(order)
        for i, neighbor in enumerate(order):
            next_in_rotation[(vertex, neighbor)] = (vertex, order[(i + 1) % degree])

    unseen = set(next_in_rotation)
    faces = 0
    while unseen:
        start = next(iter(unseen))
        u, v = start
        while (u, v) in unseen:
            unseen.discard((u, v))
            # phi(u, v) = sigma(v, u)
            u, v = next_in_rotation[(v, u)]
        faces += 1
    return faces


def _component_min_genus(component: set[Any], adjacency: dict[Any, set[Any]]) -> int:
    vertices = sorted(component, key=repr)
    neighbors = {v: sorted(adjacency[v], key=repr) for v in vertices}
    edge_count = sum(len(neighbors[v]) for v in vertices) // 2
    vertex_count = len(vertices)

    if edge_count == 0:
        return 0  # isolated vertex: planar

    # Enumerate rotation systems: fix the first neighbor at each vertex to factor
    # out the cyclic symmetry, permuting the rest. Size = product of (deg-1)!.
    search_space = 1
    for v in vertices:
        search_space *= factorial(max(len(neighbors[v]) - 1, 0))
    if search_space > _MAX_ROTATIONS:
        raise GraphPlanarityError(
            f"Rotation-system search space ({search_space}) exceeds the limit "
            f"({_MAX_ROTATIONS}); this exact method is for small graphs."
        )

    per_vertex_rotations: list[list[list[Any]]] = []
    for v in vertices:
        order = neighbors[v]
        if len(order) <= 2:
            per_vertex_rotations.append([order])
        else:
            head, rest = order[0], order[1:]
            per_vertex_rotations.append([[head, *perm] for perm in permutations(rest)])

    best_faces = 0

    def search(index: int, rotation: dict[Any, list[Any]]) -> None:
        nonlocal best_faces
        if index == len(vertices):
            best_faces = max(best_faces, _count_faces(rotation))
            return
        vertex = vertices[index]
        for order in per_vertex_rotations[index]:
            rotation[vertex] = order
            search(index + 1, rotation)

    search(0, {})
    # Euler: V - E + F = 2 - 2g  =>  g = (2 - V + E - F) / 2, minimized by max F.
    return (2 - vertex_count + edge_count - best_faces) // 2


def graph_genus(edges: Iterable[Edge], vertices: Iterable[Any] = ()) -> int:
    """Return the minimum orientable genus of the graph.

    ``edges`` is an iterable of vertex pairs; extra isolated ``vertices`` may be
    supplied. The genus of a disconnected graph is the sum of its components'
    genera.

    Complexity
    ----------
    Exact but **small-graph only**: the minimum is taken over all rotation
    systems, of which there are ``∏_v (deg(v) − 1)!`` — super-exponential in the
    vertex degrees. Use :func:`satisfies_planar_edge_bound` as a cheap necessary
    pre-filter for planarity. See ``docs/COMPLEXITY.md``.
    """

    edge_list = [tuple(e) for e in edges]
    adjacency = _adjacency(vertices, edge_list)
    return sum(_component_min_genus(c, adjacency) for c in _components(adjacency))


def is_planar(edges: Iterable[Edge], vertices: Iterable[Any] = ()) -> bool:
    """Return whether the graph is planar (orientable genus zero)."""

    return graph_genus(edges, vertices) == 0


def satisfies_planar_edge_bound(vertex_count: int, edge_count: int, *, bipartite: bool = False) -> bool:
    """Return the necessary Euler edge bound for simple planar graphs.

    A simple planar graph with ``V >= 3`` has ``E <= 3V - 6`` (``E <= 2V - 4`` if
    bipartite/triangle-free). This is necessary but not sufficient -- use
    :func:`is_planar` for a decision.
    """

    if vertex_count < 3:
        return True
    bound = (2 * vertex_count - 4) if bipartite else (3 * vertex_count - 6)
    return edge_count <= bound


__all__ = [
    "GraphPlanarityError",
    "graph_genus",
    "is_planar",
    "satisfies_planar_edge_bound",
]
