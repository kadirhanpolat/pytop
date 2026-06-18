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


def _is_bipartite(vertices: list[Any], neighbors: dict[Any, list[Any]]) -> bool:
    """Return whether the component is 2-colourable (BFS).

    A simple *bipartite* planar graph satisfies the tighter Euler bound
    ``E <= 2V - 4`` (it is triangle-free), versus ``E <= 3V - 6`` in general --
    so detecting bipartiteness lets :func:`is_planar` reject dense bipartite
    graphs (e.g. ``K_{4,4}``) without any rotation-system search.
    """

    color: dict[Any, int] = {}
    for start in vertices:
        if start in color:
            continue
        color[start] = 0
        queue = [start]
        while queue:
            u = queue.pop()
            for w in neighbors[u]:
                if w not in color:
                    color[w] = color[u] ^ 1
                    queue.append(w)
                elif color[w] == color[u]:
                    return False
    return True


def _per_vertex_rotations(
    vertices: list[Any], neighbors: dict[Any, list[Any]]
) -> list[list[list[Any]]]:
    """Per-vertex cyclic orderings: fix the first neighbor (factor out the cyclic
    symmetry) and permute the rest. The product of their lengths is the search
    space, ``∏_v (deg(v) − 1)!``.
    """

    rotations: list[list[list[Any]]] = []
    for v in vertices:
        order = neighbors[v]
        if len(order) <= 2:
            rotations.append([order])
        else:
            head, rest = order[0], order[1:]
            rotations.append([[head, *perm] for perm in permutations(rest)])
    return rotations


def _search_max_faces(
    vertices: list[Any],
    per_vertex_rotations: list[list[list[Any]]],
    *,
    target: int,
) -> int:
    """DFS over rotation systems, returning the maximum face count found.

    For a connected graph the face count satisfies ``F <= E - V + 2``, with
    equality iff the embedding has genus 0 -- the global optimum. So the search
    **stops as soon as ``target = E - V + 2`` faces are reached**: no rotation
    system can do better, so neither the exact genus nor a planarity verdict can
    change. This early termination makes planar graphs dramatically cheaper while
    leaving the result identical to a full enumeration.
    """

    n = len(vertices)
    best = 0
    done = False
    rotation: dict[Any, list[Any]] = {}

    def search(index: int) -> None:
        nonlocal best, done
        if index == n:
            faces = _count_faces(rotation)
            if faces > best:
                best = faces
            if best >= target:
                done = True
            return
        for order in per_vertex_rotations[index]:
            rotation[vertices[index]] = order
            search(index + 1)
            if done:
                return

    search(0)
    return best


def _component_min_genus(component: set[Any], adjacency: dict[Any, set[Any]]) -> int:
    vertices = sorted(component, key=repr)
    neighbors = {v: sorted(adjacency[v], key=repr) for v in vertices}
    edge_count = sum(len(neighbors[v]) for v in vertices) // 2
    vertex_count = len(vertices)

    if edge_count == 0:
        return 0  # isolated vertex: planar

    # The exact minimum genus needs the full enumeration (a genus-0 embedding lets
    # us stop early, but a non-planar graph must be searched exhaustively), so the
    # static search-space cap still guards graph_genus.
    search_space = 1
    for v in vertices:
        search_space *= factorial(max(len(neighbors[v]) - 1, 0))
    if search_space > _MAX_ROTATIONS:
        raise GraphPlanarityError(
            f"Rotation-system search space ({search_space}) exceeds the limit "
            f"({_MAX_ROTATIONS}); this exact method is for small graphs."
        )

    per_vertex_rotations = _per_vertex_rotations(vertices, neighbors)
    # Euler: V - E + F = 2 - 2g  =>  g = (2 - V + E - F) / 2, minimized by max F.
    target_faces = edge_count - vertex_count + 2  # genus-0 face count (global max)
    best_faces = _search_max_faces(vertices, per_vertex_rotations, target=target_faces)
    return (2 - vertex_count + edge_count - best_faces) // 2


def _violates_planar_edge_bound(component: set[Any], adjacency: dict[Any, set[Any]]) -> bool:
    """Return whether a component fails the necessary Euler edge bound.

    A simple planar graph has ``E <= 3V - 6`` (``E <= 2V - 4`` if bipartite). When
    violated the component is certainly non-planar, so :func:`is_planar` can reject
    it with no rotation-system search at all -- this is what makes ``K_n`` and
    ``K_{m,n}`` (whose search spaces are astronomical) decide instantly.
    """

    vertices = sorted(component, key=repr)
    neighbors = {v: sorted(adjacency[v], key=repr) for v in vertices}
    vertex_count = len(vertices)
    if vertex_count < 3:
        return False
    edge_count = sum(len(neighbors[v]) for v in vertices) // 2
    bound = (2 * vertex_count - 4) if _is_bipartite(vertices, neighbors) else (3 * vertex_count - 6)
    return edge_count > bound


def _component_is_planar(component: set[Any], adjacency: dict[Any, set[Any]]) -> bool:
    """Decide planarity of one connected component (genus 0).

    First the cheap Euler edge bound rejects dense graphs with no search; only if
    that passes do we compute the genus, which early-terminates as soon as a
    genus-0 embedding is found.
    """

    if _violates_planar_edge_bound(component, adjacency):
        return False
    return _component_min_genus(component, adjacency) == 0


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
    """Return whether the graph is planar (orientable genus zero).

    A graph is planar iff every connected component is, so this short-circuits on
    the first non-planar component. Each component is decided by
    :func:`_component_is_planar`, which rejects dense graphs via the Euler edge
    bound (no search) and otherwise stops at the first genus-0 embedding -- far
    cheaper than computing the full genus via :func:`graph_genus`.

    Complexity
    ----------
    Worst case still exponential (a non-planar graph passing the edge bound is
    searched), but planar graphs and dense non-planar graphs (``K_n``, ``K_{m,n}``)
    are decided cheaply. See ``docs/COMPLEXITY.md``.
    """

    edge_list = [tuple(e) for e in edges]
    adjacency = _adjacency(vertices, edge_list)
    return all(_component_is_planar(c, adjacency) for c in _components(adjacency))


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
