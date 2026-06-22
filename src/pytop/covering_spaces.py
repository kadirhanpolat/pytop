"""Profile-based covering space helpers.

The module records covering-map teaching examples and assumptions. It does not
verify the local homeomorphism condition for arbitrary maps.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any


class CoveringSpaceProfileError(ValueError):
    """Raised when covering profile data is malformed."""


COVERING_PROFILE_STATUSES = frozenset({"certified", "assumed", "not_certified", "unknown"})


@dataclass(frozen=True)
class CoveringMapProfile:
    """A conservative profile for a covering map."""

    name: str
    total_space: Any
    base_space: Any
    sheet_count: int | str | None = None
    status: str = "unknown"
    covering_map: str = ""
    local_homeomorphism_assumption: str = "not verified"
    fundamental_group_note: str = ""
    certification: str = "profile"
    warnings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        normalized_status = str(self.status)
        if normalized_status not in COVERING_PROFILE_STATUSES:
            raise CoveringSpaceProfileError(f"Unsupported covering profile status: {self.status!r}.")
        if not str(self.name).strip():
            raise CoveringSpaceProfileError("A covering map profile needs a nonempty name.")
        sheet_count = self.sheet_count
        if isinstance(sheet_count, int) and sheet_count <= 0:
            raise CoveringSpaceProfileError("Sheet count must be positive when it is numeric.")
        object.__setattr__(self, "name", str(self.name))
        object.__setattr__(self, "status", normalized_status)
        object.__setattr__(self, "covering_map", str(self.covering_map))
        object.__setattr__(self, "local_homeomorphism_assumption", str(self.local_homeomorphism_assumption))
        object.__setattr__(self, "fundamental_group_note", str(self.fundamental_group_note))
        object.__setattr__(self, "certification", str(self.certification))
        object.__setattr__(self, "warnings", tuple(str(warning) for warning in self.warnings))
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def is_certified(self) -> bool:
        return self.status == "certified"

    @property
    def has_local_homeomorphism_warning(self) -> bool:
        return any("local homeomorphism" in warning.lower() for warning in self.warnings)


def covering_map_profile(
    name: str,
    total_space: Any,
    base_space: Any,
    *,
    sheet_count: int | str | None = None,
    status: str = "unknown",
    covering_map: str = "",
    local_homeomorphism_assumption: str = "not verified",
    fundamental_group_note: str = "",
    certification: str = "profile",
    warnings: Iterable[str] = (),
    metadata: dict[str, Any] | None = None,
) -> CoveringMapProfile:
    """Build a covering map profile without verifying arbitrary coverings."""

    return CoveringMapProfile(
        name=name,
        total_space=total_space,
        base_space=base_space,
        sheet_count=sheet_count,
        status=status,
        covering_map=covering_map,
        local_homeomorphism_assumption=local_homeomorphism_assumption,
        fundamental_group_note=fundamental_group_note,
        certification=certification,
        warnings=tuple(warnings),
        metadata=dict(metadata or {}),
    )


def assumed_covering_map_profile(
    name: str,
    total_space: Any,
    base_space: Any,
    *,
    sheet_count: int | str | None = None,
    covering_map: str = "",
    fundamental_group_note: str = "",
    warnings: Iterable[str] = (),
) -> CoveringMapProfile:
    """Record a covering profile whose local data is assumed, not checked."""

    warning_tuple = tuple(warnings) + ("Local homeomorphism condition is recorded as an assumption.",)
    return covering_map_profile(
        name,
        total_space,
        base_space,
        sheet_count=sheet_count,
        status="assumed",
        covering_map=covering_map,
        local_homeomorphism_assumption="assumed",
        fundamental_group_note=fundamental_group_note,
        certification="assumption-profile",
        warnings=warning_tuple,
    )


def unknown_covering_map_profile(
    name: str,
    total_space: Any,
    base_space: Any,
    *,
    reason: str = "No covering-space certificate or registry match was supplied.",
) -> CoveringMapProfile:
    """Record an explicitly unknown covering profile."""

    return covering_map_profile(
        name,
        total_space,
        base_space,
        status="unknown",
        certification="unknown",
        warnings=(str(reason),),
    )


KNOWN_COVERING_MODELS: Mapping[str, CoveringMapProfile] = {
    "real_line_to_circle": covering_map_profile(
        "real_line_to_circle",
        total_space="R",
        base_space="S^1",
        sheet_count="countably infinite",
        status="certified",
        covering_map="t -> exp(2*pi*i*t)",
        local_homeomorphism_assumption="standard theorem",
        fundamental_group_note="Deck translation intuition connects to pi_1(S^1) being infinite cyclic.",
        certification="known-model-registry",
        warnings=("Standard model; not an arbitrary covering verifier.",),
    ),
    "circle_to_circle_degree_n": covering_map_profile(
        "circle_to_circle_degree_n",
        total_space="S^1",
        base_space="S^1",
        sheet_count="n",
        status="assumed",
        covering_map="z -> z^n",
        local_homeomorphism_assumption="assume n is a positive integer",
        fundamental_group_note="On pi_1(S^1), the induced map is multiplication by n in the standard profile.",
        certification="known-model-registry",
        warnings=("Use a concrete positive integer n for a numeric sheet count.",),
    ),
    "trivial_two_sheet_cover": covering_map_profile(
        "trivial_two_sheet_cover",
        total_space="B x {0, 1}",
        base_space="B",
        sheet_count=2,
        status="certified",
        covering_map="projection to B",
        local_homeomorphism_assumption="product/disjoint-copy teaching model",
        fundamental_group_note="Trivial covers preserve local base-space intuition sheetwise.",
        certification="known-model-registry",
        warnings=("Teaching profile for a trivial finite-sheet cover.",),
    ),
}


def circle_degree_covering_profile(degree: int) -> CoveringMapProfile:
    """Return the standard degree-n circle covering profile for a positive n."""

    if int(degree) <= 0:
        raise CoveringSpaceProfileError("Circle degree covering requires a positive integer degree.")
    return covering_map_profile(
        f"circle_to_circle_degree_{int(degree)}",
        total_space="S^1",
        base_space="S^1",
        sheet_count=int(degree),
        status="certified",
        covering_map=f"z -> z^{int(degree)}",
        local_homeomorphism_assumption="standard finite circle covering model",
        fundamental_group_note=f"Standard pi_1 profile: induced map multiplies by {int(degree)}.",
        certification="known-model-registry",
        warnings=("Standard model; not an arbitrary covering verifier.",),
        metadata={"degree": int(degree)},
    )


def known_covering_profile(key: str) -> CoveringMapProfile:
    """Return a registered covering example, or an unknown profile."""

    normalized = str(key).strip().lower().replace(" ", "_").replace("-", "_")
    profile = KNOWN_COVERING_MODELS.get(normalized)
    if profile is not None:
        return profile
    return unknown_covering_map_profile(
        f"{normalized}_unknown_covering",
        total_space=str(key),
        base_space="unknown",
        reason="No registered covering-space model.",
    )


def covering_profile_summary(profile: CoveringMapProfile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "total_space": profile.total_space,
        "base_space": profile.base_space,
        "sheet_count": profile.sheet_count,
        "status": profile.status,
        "covering_map": profile.covering_map,
        "local_homeomorphism_assumption": profile.local_homeomorphism_assumption,
        "fundamental_group_note": profile.fundamental_group_note,
        "certification": profile.certification,
        "warnings": profile.warnings,
    }


# ===========================================================================
# Computational covering-space engines
# ===========================================================================


@dataclass(frozen=True)
class CoveringGraph:
    """An n-sheeted covering of a finite graph via voltage assignment in ℤ/nℤ.

    Vertices of the covering graph are pairs ``(v, k)`` with ``v`` a base
    vertex and ``k ∈ {0, …, n−1}``.  An edge ``(u, v)`` with voltage ``α``
    lifts to edges ``(u, k) → (v, (k+α) mod n)`` for each sheet ``k``.
    """

    n: int
    base_vertices: tuple[int | str, ...]
    base_edges: tuple[tuple[int | str, int | str], ...]
    voltages: tuple[int, ...]

    @property
    def cover_vertices(self) -> list[tuple[int | str, int]]:
        """All ``(base_vertex, sheet)`` pairs."""
        return [(v, k) for v in self.base_vertices for k in range(self.n)]

    @property
    def cover_edges(self) -> list[tuple[tuple[int | str, int], tuple[int | str, int]]]:
        """Lifted edges of the covering graph."""
        result = []
        for (u, v), volt in zip(self.base_edges, self.voltages):
            for k in range(self.n):
                result.append(((u, k), (v, (k + volt) % self.n)))
        return result

    @property
    def num_cover_vertices(self) -> int:
        return len(self.base_vertices) * self.n

    @property
    def num_cover_edges(self) -> int:
        return len(self.base_edges) * self.n


def _cs_bfs_tree_indices(
    vertices: list[int | str],
    edges: list[tuple[int | str, int | str]],
) -> set[int]:
    """Return edge indices forming a BFS spanning tree of the first component."""
    adj: dict[int | str, list[tuple[int, int | str]]] = {v: [] for v in vertices}
    for idx, (u, v) in enumerate(edges):
        adj[u].append((idx, v))
        adj[v].append((idx, u))
    if not vertices:
        return set()
    visited: set[int | str] = {vertices[0]}
    tree: set[int] = set()
    queue: list[int | str] = [vertices[0]]
    while queue:
        node = queue.pop(0)
        for idx, nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                tree.add(idx)
                queue.append(nb)
    return tree


def cyclic_voltage_cover(
    vertices: list[int | str],
    edges: list[tuple[int | str, int | str]],
    n: int,
    voltages: list[int] | None = None,
) -> CoveringGraph:
    """Construct the n-sheeted cyclic covering of a finite graph.

    Uses voltage assignment in ℤ/nℤ.  When *voltages* is ``None`` the
    function assigns voltage 1 to the first non-tree edge and 0 to all
    others, producing the connected n-sheeted cyclic cover associated with
    a single generator of π₁.

    Parameters
    ----------
    vertices:
        Vertex labels of the base graph.
    edges:
        Undirected edges of the base graph (each listed once as a pair).
    n:
        Number of sheets (positive integer).
    voltages:
        Optional voltage in ℤ/nℤ for each edge, in the same order as
        *edges*.  Must have ``len(voltages) == len(edges)`` when supplied.

    Returns
    -------
    CoveringGraph

    Raises
    ------
    ValueError
        If ``n ≤ 0``, *vertices* is empty, or the voltage list length
        does not match the edge list.

    Examples
    --------
    The 2-sheeted cover of S¹ (one edge, one vertex loop) lifts the circle
    to itself with two sheets:

    >>> cg = cyclic_voltage_cover([0], [(0, 0)], n=2)
    >>> len(cg.cover_vertices)
    2
    """
    if n <= 0:
        raise ValueError(f"Sheet count must be positive, got {n!r}")
    if not vertices:
        raise ValueError("Graph must have at least one vertex")

    if voltages is None:
        tree_idx = _cs_bfs_tree_indices(vertices, edges)
        found_first_non_tree = False
        voltages = []
        for i in range(len(edges)):
            if i in tree_idx:
                voltages.append(0)
            elif not found_first_non_tree:
                voltages.append(1)
                found_first_non_tree = True
            else:
                voltages.append(0)

    if len(voltages) != len(edges):
        raise ValueError(f"Need {len(edges)} voltages, got {len(voltages)}")

    typed_edges: tuple[tuple[int | str, int | str], ...] = tuple(
        (u, v) for u, v in edges
    )
    return CoveringGraph(
        n=n,
        base_vertices=tuple(vertices),
        base_edges=typed_edges,
        voltages=tuple(v % n for v in voltages),
    )


def universal_covering_tree(
    vertices: list[int | str],
    edges: list[tuple[int | str, int | str]],
    max_depth: int = 6,
) -> tuple[
    list[tuple[int | str, ...]],
    list[tuple[tuple[int | str, ...], tuple[int | str, ...]]],
]:
    """Compute a finite BFS approximation of the universal covering tree.

    The universal cover of any connected graph is a tree.  Each cover vertex
    is a path (tuple of base-graph vertices) from the basepoint; immediate
    backtracking is forbidden to enforce the tree condition.

    Parameters
    ----------
    vertices:
        Vertices of the base graph.
    edges:
        Undirected edges of the base graph.
    max_depth:
        Maximum path length (number of edges from basepoint) to expand.

    Returns
    -------
    (cover_vertices, cover_edges)
        *cover_vertices* — list of paths (tuples of base vertices).
        *cover_edges* — list of ``(path_u, path_v)`` pairs.
    """
    if not vertices:
        return [], []

    adj: dict[int | str, list[int | str]] = {v: [] for v in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    start: tuple[int | str, ...] = (vertices[0],)
    cover_verts: list[tuple[int | str, ...]] = [start]
    cover_edgs: list[tuple[tuple[int | str, ...], tuple[int | str, ...]]] = []
    queue: list[tuple[int | str, ...]] = [start]
    seen: set[tuple[int | str, ...]] = {start}

    while queue:
        path = queue.pop(0)
        if len(path) - 1 >= max_depth:
            continue
        current = path[-1]
        parent = path[-2] if len(path) >= 2 else None
        for nb in adj[current]:
            if nb == parent:
                continue
            new_path = path + (nb,)
            if new_path not in seen:
                seen.add(new_path)
                cover_verts.append(new_path)
                cover_edgs.append((path, new_path))
                queue.append(new_path)

    return cover_verts, cover_edgs


def fundamental_group_rank_graph(
    vertices: list[int | str],
    edges: list[tuple[int | str, int | str]],
) -> int:
    """Return the rank of π₁(G) for a finite graph G.

    π₁(G) is free of rank β₁(G) = |E| − |V| + (number of connected
    components).  For a connected graph this simplifies to |E| − |V| + 1.

    Parameters
    ----------
    vertices:
        Vertex labels.
    edges:
        Undirected edges (each listed once).

    Returns
    -------
    int — rank of the free group π₁(G).

    Examples
    --------
    >>> fundamental_group_rank_graph([0, 1, 2], [(0, 1), (1, 2), (2, 0)])
    1   # triangle = S¹, π₁ = ℤ
    >>> fundamental_group_rank_graph([0, 1], [(0, 1)])
    0   # tree, simply connected
    """
    if not vertices:
        return 0

    parent: dict[int | str, int | str] = {v: v for v in vertices}

    def _find(x: int | str) -> int | str:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def _union(x: int | str, y: int | str) -> None:
        rx, ry = _find(x), _find(y)
        if rx != ry:
            parent[rx] = ry

    for u, v in edges:
        _union(u, v)

    components = len({_find(v) for v in vertices})
    return len(edges) - len(vertices) + components


def is_graph_covering_map(
    total_vertices: list[int | str],
    total_edges: list[tuple[int | str, int | str]],
    base_vertices: list[int | str],
    base_edges: list[tuple[int | str, int | str]],
    projection: dict[int | str, int | str],
) -> bool:
    """Check whether *projection* defines a graph-theoretic covering map.

    A graph homomorphism p: G̃ → G is a covering map iff for every vertex
    ṽ ∈ G̃ the restriction of p to the neighbourhood N(ṽ) → N(p(ṽ)) is a
    bijection (local bijectivity / evenly-covered open stars).

    Parameters
    ----------
    total_vertices, total_edges:
        The covering graph G̃.
    base_vertices, base_edges:
        The base graph G.
    projection:
        Maps each vertex of G̃ to a vertex of G.

    Returns
    -------
    bool — ``True`` iff *projection* is a valid graph covering map.
    """
    if not set(base_vertices).issubset(set(projection.values())):
        return False

    base_adj: dict[int | str, list[int | str]] = {v: [] for v in base_vertices}
    for u, v in base_edges:
        base_adj[u].append(v)
        base_adj[v].append(u)

    total_adj: dict[int | str, list[int | str]] = {v: [] for v in total_vertices}
    for u, v in total_edges:
        total_adj[u].append(v)
        total_adj[v].append(u)

    for vt in total_vertices:
        if vt not in projection:
            return False
        vb = projection[vt]
        if vb not in base_adj:
            return False
        proj_nbs = sorted(str(projection[nb]) for nb in total_adj.get(vt, []) if nb in projection)
        base_nbs = sorted(str(nb) for nb in base_adj[vb])
        if proj_nbs != base_nbs:
            return False

    return True


__all__ = [
    "COVERING_PROFILE_STATUSES",
    "CoveringGraph",
    "CoveringMapProfile",
    "CoveringSpaceProfileError",
    "KNOWN_COVERING_MODELS",
    "assumed_covering_map_profile",
    "circle_degree_covering_profile",
    "covering_map_profile",
    "covering_profile_summary",
    "cyclic_voltage_cover",
    "fundamental_group_rank_graph",
    "is_graph_covering_map",
    "known_covering_profile",
    "universal_covering_tree",
    "unknown_covering_map_profile",
]
