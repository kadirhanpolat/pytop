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

import sys
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


# ---------------------------------------------------------------------------
# Polynomial planarity decision — the left-right algorithm (Brandes 2009)
# ---------------------------------------------------------------------------
#
# is_planar uses an O(V + E) left-right planarity test (de Fraysseix–Rosenstiehl;
# Brandes, "The Left-Right Planarity Test", 2009) rather than the exponential
# rotation-system search, so it decides planarity for graphs of *any* size and
# never raises GraphPlanarityError.  graph_genus keeps the rotation-system search:
# computing the exact minimum genus (not just whether it is 0) is genuinely harder.
#
# This is a decision-only port (no embedding is constructed).  It is validated
# against networkx's independent planarity test on exhaustive small graphs and
# random larger graphs (tests/core/test_graph_planarity.py).


class _Interval:
    """An interval of return edges, given by its lowest and highest edge."""

    __slots__ = ("low", "high")

    def __init__(self, low: tuple | None = None, high: tuple | None = None) -> None:
        self.low = low
        self.high = high

    def empty(self) -> bool:
        return self.low is None and self.high is None

    def copy(self) -> _Interval:
        return _Interval(self.low, self.high)


class _ConflictPair:
    """A pair of (left, right) intervals that must be embedded on opposite sides."""

    __slots__ = ("L", "R")

    def __init__(self, left: _Interval | None = None, right: _Interval | None = None) -> None:
        self.L = left if left is not None else _Interval()
        self.R = right if right is not None else _Interval()

    def swap(self) -> None:
        self.L, self.R = self.R, self.L


class _LRPlanarity:
    """Left-right planarity test (decision only)."""

    def __init__(self, adjacency: dict[Any, set[Any]]) -> None:
        self.adj: dict[Any, list[Any]] = {v: list(nbrs) for v, nbrs in adjacency.items()}
        self.height: dict[Any, int | None] = {v: None for v in self.adj}
        self.lowpt: dict[tuple, int] = {}
        self.lowpt2: dict[tuple, int] = {}
        self.nesting_depth: dict[tuple, int] = {}
        self.parent_edge: dict[Any, tuple | None] = {v: None for v in self.adj}
        self.oriented_adj: dict[Any, list[tuple]] = {v: [] for v in self.adj}
        self.oriented: set[tuple] = set()
        self.ref: dict[tuple, tuple | None] = {}
        self.side: dict[tuple, int] = {}
        self.stack: list[_ConflictPair] = []
        self.stack_bottom: dict[tuple, _ConflictPair | None] = {}
        self.lowpt_edge: dict[tuple, tuple] = {}
        self.roots: list[Any] = []

    def is_planar(self) -> bool:
        n = len(self.adj)
        if n == 0:
            return True
        # Deep DFS trees (e.g. long paths) can exceed the default recursion limit.
        needed = 4 * n + 100
        if sys.getrecursionlimit() < needed:
            sys.setrecursionlimit(needed)
        # Phase 1 — orientation (DFS forest with lowpoints + nesting depth).
        for v in self.adj:
            if self.height[v] is None:
                self.height[v] = 0
                self.roots.append(v)
                self._orient(v)
        for v in self.adj:
            self.oriented_adj[v].sort(key=lambda e: self.nesting_depth[e])
        # Phase 2 — testing.
        for v in self.roots:
            if not self._test(v):
                return False
        return True

    def _orient(self, v: Any) -> None:
        e = self.parent_edge[v]
        hv = self.height[v]
        assert hv is not None
        for w in self.adj[v]:
            if (v, w) in self.oriented or (w, v) in self.oriented:
                continue
            vw = (v, w)
            self.oriented.add(vw)
            self.oriented_adj[v].append(vw)
            self.lowpt[vw] = self.lowpt2[vw] = hv
            if self.height[w] is None:  # tree edge
                self.parent_edge[w] = vw
                self.height[w] = hv + 1
                self._orient(w)
            else:  # back edge
                hw = self.height[w]
                assert hw is not None
                self.lowpt[vw] = hw
            self.nesting_depth[vw] = 2 * self.lowpt[vw]
            if self.lowpt2[vw] < hv:  # chordal — nest deeper
                self.nesting_depth[vw] += 1
            if e is not None:  # update lowpoints of the parent edge
                if self.lowpt[vw] < self.lowpt[e]:
                    self.lowpt2[e] = min(self.lowpt[e], self.lowpt2[vw])
                    self.lowpt[e] = self.lowpt[vw]
                elif self.lowpt[vw] > self.lowpt[e]:
                    self.lowpt2[e] = min(self.lowpt2[e], self.lowpt[vw])
                else:
                    self.lowpt2[e] = min(self.lowpt2[e], self.lowpt2[vw])

    def _top(self) -> _ConflictPair | None:
        return self.stack[-1] if self.stack else None

    def _lowest(self, pair: _ConflictPair) -> int:
        if pair.L.empty():
            return self.lowpt[pair.R.low]  # type: ignore[index]
        if pair.R.empty():
            return self.lowpt[pair.L.low]  # type: ignore[index]
        return min(self.lowpt[pair.L.low], self.lowpt[pair.R.low])  # type: ignore[index]

    def _conflicting(self, interval: _Interval, b: tuple) -> bool:
        return (not interval.empty()) and self.lowpt[interval.high] > self.lowpt[b]  # type: ignore[index]

    def _test(self, v: Any) -> bool:
        e = self.parent_edge[v]
        hv = self.height[v]
        assert hv is not None
        for ei in self.oriented_adj[v]:
            self.stack_bottom[ei] = self._top()
            if ei == self.parent_edge[ei[1]]:  # tree edge
                if not self._test(ei[1]):
                    return False
            else:  # back edge
                self.lowpt_edge[ei] = ei
                self.stack.append(_ConflictPair(right=_Interval(ei, ei)))
            if self.lowpt[ei] < hv:  # ei has a return edge
                # a return edge above v implies v is not a DFS root, so e exists
                assert e is not None
                if ei == self.oriented_adj[v][0]:
                    self.lowpt_edge[e] = self.lowpt_edge[ei]
                elif not self._add_constraints(ei, e):
                    return False
        if e is not None:  # integrate back into the parent edge
            u = e[0]
            self._trim_back_edges(u)
            hu = self.height[u]
            assert hu is not None
            if self.lowpt[e] < hu:
                top = self._top()
                assert top is not None
                hl, hr = top.L.high, top.R.high
                if hl is not None and (hr is None or self.lowpt[hl] > self.lowpt[hr]):
                    self.ref[e] = hl
                else:
                    self.ref[e] = hr
        return True

    def _add_constraints(self, ei: tuple, e: tuple) -> bool:
        pair = _ConflictPair()
        # Merge the return edges of ei into pair.R.
        while True:
            q = self.stack.pop()
            if not q.L.empty():
                q.swap()
            if not q.L.empty():
                return False  # left and right both nonempty → not planar
            if self.lowpt[q.R.low] > self.lowpt[e]:  # type: ignore[index]
                if pair.R.empty():
                    pair.R = q.R.copy()
                else:
                    self.ref[pair.R.low] = q.R.high  # type: ignore[index]
                pair.R.low = q.R.low
            else:
                self.ref[q.R.low] = self.lowpt_edge[e]  # type: ignore[index]
            if self._top() is self.stack_bottom[ei]:
                break
        # Merge the conflicting return edges of e_1..e_{i-1} into pair.L.
        while self._conflicting(self._top().L, ei) or self._conflicting(self._top().R, ei):  # type: ignore[union-attr]
            q = self.stack.pop()
            if self._conflicting(q.R, ei):
                q.swap()
            if self._conflicting(q.R, ei):
                return False  # not planar
            self.ref[pair.R.low] = q.R.high  # type: ignore[index]
            if q.R.low is not None:
                pair.R.low = q.R.low
            if pair.L.empty():
                pair.L = q.L.copy()
            else:
                self.ref[pair.L.low] = q.L.high  # type: ignore[index]
            pair.L.low = q.L.low
        if not (pair.L.empty() and pair.R.empty()):
            self.stack.append(pair)
        return True

    def _trim_back_edges(self, u: Any) -> None:
        while self.stack and self._lowest(self._top()) == self.height[u]:  # type: ignore[arg-type]
            popped = self.stack.pop()
            if popped.L.low is not None:
                self.side[popped.L.low] = -1
        if self.stack:
            pair = self.stack.pop()
            while pair.L.high is not None and pair.L.high[1] == u:
                pair.L.high = self.ref.get(pair.L.high)
            if pair.L.high is None and pair.L.low is not None:
                self.ref[pair.L.low] = pair.R.low
                self.side[pair.L.low] = -1
                pair.L.low = None
            while pair.R.high is not None and pair.R.high[1] == u:
                pair.R.high = self.ref.get(pair.R.high)
            if pair.R.high is None and pair.R.low is not None:
                self.ref[pair.R.low] = pair.L.low
                self.side[pair.R.low] = -1
                pair.R.low = None
            self.stack.append(pair)


def _lr_is_planar(adjacency: dict[Any, set[Any]]) -> bool:
    """Decide planarity of a whole graph (all components) via the LR test."""
    return _LRPlanarity(adjacency).is_planar()


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

    Uses the linear-time **left-right planarity test** (Brandes 2009), so it
    decides planarity for graphs of *any* size and **never raises** -- unlike
    :func:`graph_genus`, which enumerates rotation systems. A cheap Euler edge
    bound rejects dense graphs up front (and double-checks the LR verdict on
    them).

    Complexity
    ----------
    ``O(V + E)``. See ``docs/COMPLEXITY.md``.
    """

    edge_list = [tuple(e) for e in edges]
    adjacency = _adjacency(vertices, edge_list)
    # Cheap necessary Euler reject per component (also a safety net on the LR test).
    for component in _components(adjacency):
        if _violates_planar_edge_bound(component, adjacency):
            return False
    return _lr_is_planar(adjacency)


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
