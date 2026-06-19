"""Mapper algorithm for topological data analysis (Singh–Mémoli–Carlsson 2007).

The Mapper algorithm constructs a combinatorial summary (simplicial complex or
graph) of a point cloud with a scalar filter function:

1. Apply a filter function f : X → ℝ to the data.
2. Cover f(X) with overlapping intervals (a *cover* of the image).
3. Pull each interval back: cluster f⁻¹(U_α) ⊂ X independently.
4. Build the *nerve* of the resulting cover: one node per cluster, edges
   (and higher simplices) where clusters share data points.

The result is a ``MapperComplex`` — a simplicial complex whose 0-cells are
clusters and whose higher cells encode shared membership.

Public API
----------
IntervalCover          — uniform interval cover of a real range
MapperNode             — a single cluster (node) in the Mapper graph
MapperComplex          — the full Mapper output (graph or simplicial complex)
mapper                 — compute the Mapper simplicial complex
single_linkage_labels  — simple single-linkage clustering on 1-D data (built-in)

References
----------
Singh, G., Mémoli, F., & Carlsson, G. (2007). Topological methods for the
analysis of high dimensional data sets and 3D object recognition. *SPBG*.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence


# ---------------------------------------------------------------------------
# Cover
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IntervalCover:
    """A uniform overlapping cover of a closed interval [low, high].

    The cover consists of ``num_intervals`` equal-width intervals with a
    fractional overlap ``overlap_fraction`` (0 < overlap_fraction < 1).
    The width of each interval is ``(high - low) / (num_intervals * (1 - overlap_fraction))``.

    Parameters
    ----------
    low, high:
        The endpoints of the interval to cover.
    num_intervals:
        Number of intervals.
    overlap_fraction:
        Fractional overlap between adjacent intervals (e.g. 0.5 means 50 % overlap).
    """

    low: float
    high: float
    num_intervals: int
    overlap_fraction: float

    def __post_init__(self) -> None:
        if self.num_intervals < 1:
            raise ValueError("num_intervals must be ≥ 1")
        if not (0.0 < self.overlap_fraction < 1.0):
            raise ValueError("overlap_fraction must be strictly between 0 and 1")
        if self.low >= self.high:
            raise ValueError("low must be < high")

    @property
    def step(self) -> float:
        """Distance between interval centres."""
        return (self.high - self.low) / self.num_intervals

    @property
    def width(self) -> float:
        """Width of each interval."""
        return self.step / (1.0 - self.overlap_fraction)

    def intervals(self) -> list[tuple[float, float]]:
        """Return the list of (a, b) interval endpoints."""
        result = []
        for k in range(self.num_intervals):
            centre = self.low + (k + 0.5) * self.step
            a = centre - self.width / 2
            b = centre + self.width / 2
            result.append((a, b))
        return result

    def interval_for(self, value: float) -> list[int]:
        """Return the indices of all intervals that contain ``value``."""
        return [
            k
            for k, (a, b) in enumerate(self.intervals())
            if a <= value <= b
        ]


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------


def single_linkage_labels(
    values: list[float],
    gap_threshold: float,
) -> list[int]:
    """Assign cluster labels by single-linkage on 1-D data.

    Points are sorted and a new cluster begins whenever the gap to the
    previous point exceeds ``gap_threshold``.

    Parameters
    ----------
    values:
        The 1-D filter values for the points in a pullback bin.
    gap_threshold:
        Minimum gap to start a new cluster.  Use ``math.inf`` to put all
        points in one cluster.

    Returns
    -------
    list[int]
        Cluster labels (0-indexed) in the same order as ``values``.
    """
    if not values:
        return []

    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    labels = [0] * n
    current_label = 0

    for rank in range(1, n):
        prev_idx = order[rank - 1]
        curr_idx = order[rank]
        if values[curr_idx] - values[prev_idx] > gap_threshold:
            current_label += 1
        labels[curr_idx] = current_label

    return labels


# ---------------------------------------------------------------------------
# Mapper output
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MapperNode:
    """A single cluster (node) in the Mapper complex.

    Parameters
    ----------
    interval_index:
        Index of the cover interval that produced this cluster.
    cluster_index:
        Index of the cluster within that interval's pullback.
    members:
        Indices into the original data set that belong to this cluster.
    """

    interval_index: int
    cluster_index: int
    members: frozenset[int]

    def __len__(self) -> int:
        return len(self.members)


@dataclass(frozen=True)
class MapperComplex:
    """The output of the Mapper algorithm.

    ``nodes`` is the ordered list of clusters (0-simplices); ``simplices``
    is the full Mapper simplicial complex as an abstract simplicial complex
    (node-index–based).  Edges (1-simplices) connect nodes whose ``members``
    intersect; triangles (2-simplices) exist when three mutually intersecting
    clusters exist, etc.

    Attributes
    ----------
    nodes:
        Ordered list of :class:`MapperNode` objects (vertex set).
    simplices:
        The abstract simplicial complex as a frozenset of frozensets of node
        indices.  Each element is a frozenset of node indices forming a simplex.
    filter_values:
        Filter value for each data point (same indexing as the original data).
    """

    nodes: tuple[MapperNode, ...]
    simplices: frozenset[frozenset[int]]
    filter_values: tuple[float, ...]

    @property
    def num_nodes(self) -> int:
        return len(self.nodes)

    @property
    def num_edges(self) -> int:
        return sum(1 for s in self.simplices if len(s) == 2)

    def edges(self) -> list[tuple[int, int]]:
        """Return edges as sorted (i, j) pairs with i < j."""
        return sorted(
            (min(s), max(s)) for s in self.simplices if len(s) == 2
        )

    def adjacency(self) -> dict[int, set[int]]:
        """Return the adjacency dict of the Mapper 1-skeleton."""
        adj: dict[int, set[int]] = {i: set() for i in range(self.num_nodes)}
        for i, j in self.edges():
            adj[i].add(j)
            adj[j].add(i)
        return adj

    def connected_components(self) -> list[frozenset[int]]:
        """Return connected components as frozensets of node indices."""
        adj = self.adjacency()
        visited: set[int] = set()
        components: list[frozenset[int]] = []
        for start in range(self.num_nodes):
            if start in visited:
                continue
            component: set[int] = set()
            stack = [start]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                stack.extend(adj[node] - visited)
            components.append(frozenset(component))
        return components


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------


def mapper(
    data: Sequence[Any],
    filter_fn: Callable[[Any], float],
    cover: IntervalCover | None = None,
    *,
    cluster_fn: Callable[[list[float], list[int]], list[int]] | None = None,
    max_simplex_dim: int = 2,
    num_intervals: int = 10,
    overlap_fraction: float = 0.5,
    gap_threshold: float | None = None,
) -> MapperComplex:
    """Compute the Mapper simplicial complex of a data set.

    Parameters
    ----------
    data:
        The input data set.  Each element is passed to ``filter_fn``.
    filter_fn:
        A scalar filter function f : X → ℝ.  Common choices include the
        first PCA coordinate, eccentricity, or density estimate.
    cover:
        An :class:`IntervalCover` for the image of f.  If ``None``, a uniform
        cover is constructed automatically from the data range using
        ``num_intervals`` and ``overlap_fraction``.
    cluster_fn:
        A function ``(filter_values, point_indices) → labels`` that clusters
        the points within a pullback bin.  Defaults to single-linkage on the
        filter values with ``gap_threshold`` (computed automatically if not
        given).
    max_simplex_dim:
        Maximum dimension of simplices to include in the nerve.  Set to 1 to
        produce only a graph (nodes + edges).
    num_intervals:
        Number of cover intervals (used when ``cover`` is ``None``).
    overlap_fraction:
        Overlap fraction for the automatic cover (used when ``cover`` is
        ``None``).
    gap_threshold:
        Gap threshold for the default single-linkage clustering.  Defaults to
        10 % of each pullback bin's value range; set explicitly to override.

    Returns
    -------
    MapperComplex
        The Mapper simplicial complex.
    """
    if not data:
        return MapperComplex(
            nodes=(),
            simplices=frozenset(),
            filter_values=(),
        )

    n = len(data)
    fvals = tuple(filter_fn(x) for x in data)

    f_min = min(fvals)
    f_max = max(fvals)

    if f_min == f_max:
        f_max = f_min + 1.0

    if cover is None:
        cover = IntervalCover(
            low=f_min,
            high=f_max,
            num_intervals=num_intervals,
            overlap_fraction=overlap_fraction,
        )

    intervals = cover.intervals()

    if cluster_fn is None:
        def _default_cluster(bin_fvals: list[float], _indices: list[int]) -> list[int]:
            if not bin_fvals:
                return []
            if gap_threshold is not None:
                thr = gap_threshold
            else:
                rng = max(bin_fvals) - min(bin_fvals)
                thr = rng * 0.1 if rng > 0 else math.inf
            return single_linkage_labels(bin_fvals, thr)

        cluster_fn = _default_cluster

    nodes: list[MapperNode] = []

    for interval_idx, (a, b) in enumerate(intervals):
        # Collect points in this interval
        bin_indices = [i for i in range(n) if a <= fvals[i] <= b]
        if not bin_indices:
            continue

        bin_fvals = [fvals[i] for i in bin_indices]
        labels = cluster_fn(bin_fvals, bin_indices)

        # Group by label
        clusters: dict[int, list[int]] = {}
        for local_idx, global_idx in enumerate(bin_indices):
            lbl = labels[local_idx]
            clusters.setdefault(lbl, []).append(global_idx)

        for cluster_idx, members in sorted(clusters.items()):
            nodes.append(
                MapperNode(
                    interval_index=interval_idx,
                    cluster_index=cluster_idx,
                    members=frozenset(members),
                )
            )

    num_nodes = len(nodes)

    # Build the nerve: simplex {i₀, ..., iₖ} exists iff ∩ nodes[iⱼ].members ≠ ∅
    simplices: set[frozenset[int]] = set()

    # Add all 0-simplices (nodes)
    for i in range(num_nodes):
        simplices.add(frozenset([i]))

    # Add higher simplices up to max_simplex_dim
    if max_simplex_dim >= 1:
        _build_nerve(nodes, num_nodes, max_simplex_dim, simplices)

    return MapperComplex(
        nodes=tuple(nodes),
        simplices=frozenset(simplices),
        filter_values=fvals,
    )


def _build_nerve(
    nodes: list[MapperNode],
    num_nodes: int,
    max_dim: int,
    simplices: set[frozenset[int]],
) -> None:
    """Add simplices to the nerve up to dimension max_dim.

    Uses the fact that a simplex {i_0, ..., i_k} is in the nerve iff the
    intersection of all member sets is nonempty.
    """
    from itertools import combinations

    for dim in range(1, max_dim + 1):
        for combo in combinations(range(num_nodes), dim + 1):
            intersection = nodes[combo[0]].members
            for idx in combo[1:]:
                intersection = intersection & nodes[idx].members
                if not intersection:
                    break
            if intersection:
                simplices.add(frozenset(combo))
