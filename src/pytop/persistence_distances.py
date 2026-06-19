"""Persistence diagram distances and statistics.

Computes distances between persistence diagrams and summary statistics.

All functions accept the output of ``persistence_pairs``,
``persistence_pairs_twist``, or ``persistence_pairs_cohomology`` directly as
``tuple[PersistencePair, ...]``.

Public API
----------
bottleneck_distance   — d_B(D1, D2): min-max L∞ matching cost
wasserstein_distance  — d_W^p(D1, D2): p-Wasserstein distance (p≥1)
persistence_entropy   — Shannon entropy of the finite-bar persistence distribution
persistence_landscape — k-th landscape function sampled on a uniform time grid

References
----------
Cohen-Steiner, D., Edelsbrunner, H., & Harer, J. (2007). Stability of
persistence diagrams. *Discrete & Computational Geometry*, 37(1), 103–120.

Bubenik, P. (2015). Statistical topological data analysis using persistence
landscapes. *Journal of Machine Learning Research*, 16(1), 77–102.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .persistent_homology import PersistencePair


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _finite_pairs(
    pairs: tuple[PersistencePair, ...],
    degree: int | None,
) -> list[tuple[float, float]]:
    """Return (birth, death) for finite pairs, optionally filtered by degree."""
    return [
        (p.birth, p.death)
        for p in pairs
        if not p.is_essential and (degree is None or p.dimension == degree)
    ]


def _diagonal_cost(birth: float, death: float) -> float:
    """L∞ distance from (birth, death) to the diagonal."""
    return (death - birth) / 2


def _linf(b1: float, d1: float, b2: float, d2: float) -> float:
    return max(abs(b1 - b2), abs(d1 - d2))


def _build_augmented_cost(
    diag1: list[tuple[float, float]],
    diag2: list[tuple[float, float]],
    power: float = 1.0,
) -> list[list[float]]:
    """Build the (m+n) × (m+n) augmented cost matrix.

    Row structure: m real D_1 points, then n dummy rows (diagonal copies of D_2).
    Col structure: n real D_2 points, then m dummy cols (diagonal copies of D_1).

    Matching a real D_1 point to a dummy column is equivalent to assigning it to
    the diagonal; matching a dummy row to a real D_2 point is the same for D_2;
    dummy ↔ dummy has zero cost.
    """
    m, n = len(diag1), len(diag2)
    size = m + n
    cost = [[0.0] * size for _ in range(size)]

    # Top-left m×n: real D_1 to real D_2
    for i, (b1, d1) in enumerate(diag1):
        for j, (b2, d2) in enumerate(diag2):
            cost[i][j] = _linf(b1, d1, b2, d2) ** power

    # Top-right m×m: D_1[i] to diagonal (all dummy columns have same cost)
    for i, (b1, d1) in enumerate(diag1):
        dc = _diagonal_cost(b1, d1) ** power
        for i2 in range(m):
            cost[i][n + i2] = dc

    # Bottom-left n×n: D_2[j] to diagonal (all dummy rows have same cost)
    for j, (b2, d2) in enumerate(diag2):
        dc = _diagonal_cost(b2, d2) ** power
        for j2 in range(n):
            cost[m + j2][j] = dc

    # Bottom-right n×m: dummy ↔ dummy = 0 (already initialised)

    return cost


def _hungarian(cost: list[list[float]]) -> tuple[float, list[int]]:
    """Jonker-Volgenant O(n³) minimum-cost perfect assignment.

    Returns (total_cost, assignment) where assignment[i] is the column
    assigned to row i.
    """
    n = len(cost)
    if n == 0:
        return 0.0, []

    INF = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        min_val = [INF] * (n + 1)
        used = [False] * (n + 1)

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = -1

            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < min_val[j]:
                        min_val[j] = cur
                        way[j] = j0
                    if min_val[j] < delta:
                        delta = min_val[j]
                        j1 = j

            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    min_val[j] -= delta

            j0 = j1
            if p[j0] == 0:
                break

        while j0 != 0:
            p[j0] = p[way[j0]]
            j0 = way[j0]

    assignment = [0] * n
    total = 0.0
    for j in range(1, n + 1):
        if p[j] != 0:
            row = p[j] - 1
            col = j - 1
            assignment[row] = col
            total += cost[row][col]

    return total, assignment


def _max_bipartite_matching(n: int, adj: list[list[int]]) -> int:
    """Augmenting-path DFS maximum bipartite matching."""
    match_r = [-1] * n

    def dfs(u: int, seen: list[bool]) -> bool:
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                if match_r[v] == -1 or dfs(match_r[v], seen):
                    match_r[v] = u
                    return True
        return False

    result = 0
    for u in range(n):
        seen = [False] * n
        if dfs(u, seen):
            result += 1
    return result


def _bottleneck_via_binary_search(cost: list[list[float]]) -> float:
    """Find the bottleneck assignment cost via sorted-threshold binary search."""
    n = len(cost)
    if n == 0:
        return 0.0

    # Collect all unique costs and sort them
    thresholds = sorted({cost[i][j] for i in range(n) for j in range(n)})

    # Binary search: find minimum threshold that allows a perfect matching
    lo, hi = 0, len(thresholds) - 1
    result = thresholds[-1]

    while lo <= hi:
        mid = (lo + hi) // 2
        eps = thresholds[mid]
        adj = [[j for j in range(n) if cost[i][j] <= eps] for i in range(n)]
        if _max_bipartite_matching(n, adj) == n:
            result = eps
            hi = mid - 1
        else:
            lo = mid + 1

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def bottleneck_distance(
    pairs1: tuple[PersistencePair, ...],
    pairs2: tuple[PersistencePair, ...],
    *,
    degree: int | None = None,
) -> float:
    """Compute the bottleneck distance between two persistence diagrams.

    The bottleneck distance is:

        d_B(D_1, D_2) = inf_{η} sup_{p ∈ D_1} ‖p − η(p)‖_∞

    where η ranges over all bijections from D_1 ∪ Δ to D_2 ∪ Δ (Δ = diagonal).
    Essential (infinite lifetime) bars are excluded.

    Parameters
    ----------
    pairs1, pairs2:
        Persistence pairs from ``persistence_pairs`` or similar.
    degree:
        If given, restrict to homological degree ``degree``.

    Returns
    -------
    float
        The bottleneck distance d_B(D_1, D_2) ≥ 0.
    """
    d1 = _finite_pairs(pairs1, degree)
    d2 = _finite_pairs(pairs2, degree)

    if not d1 and not d2:
        return 0.0
    if not d1:
        return max(_diagonal_cost(b, d) for b, d in d2)
    if not d2:
        return max(_diagonal_cost(b, d) for b, d in d1)

    cost = _build_augmented_cost(d1, d2, power=1.0)
    return _bottleneck_via_binary_search(cost)


def wasserstein_distance(
    pairs1: tuple[PersistencePair, ...],
    pairs2: tuple[PersistencePair, ...],
    *,
    p: float = 1.0,
    degree: int | None = None,
) -> float:
    """Compute the p-Wasserstein distance between two persistence diagrams.

    The p-Wasserstein distance is:

        d_W^p(D_1, D_2) = inf_{η} (Σ_{x ∈ D_1} ‖x − η(x)‖_∞^p)^{1/p}

    Essential bars are excluded.

    Parameters
    ----------
    pairs1, pairs2:
        Persistence pairs.
    p:
        Wasserstein exponent p ≥ 1.  ``p=1`` gives the 1-Wasserstein (earth
        mover's distance); ``p=2`` gives the 2-Wasserstein.
    degree:
        If given, restrict to homological degree ``degree``.

    Returns
    -------
    float
        The Wasserstein distance ≥ 0.
    """
    if p < 1:
        raise ValueError(f"Wasserstein exponent p must be ≥ 1, got {p}")

    d1 = _finite_pairs(pairs1, degree)
    d2 = _finite_pairs(pairs2, degree)

    if not d1 and not d2:
        return 0.0
    if not d1:
        return sum(_diagonal_cost(b, d) ** p for b, d in d2) ** (1 / p)
    if not d2:
        return sum(_diagonal_cost(b, d) ** p for b, d in d1) ** (1 / p)

    cost = _build_augmented_cost(d1, d2, power=p)
    total, _ = _hungarian(cost)
    return total ** (1 / p)


def persistence_entropy(
    pairs: tuple[PersistencePair, ...],
    *,
    degree: int | None = None,
) -> float:
    """Compute the persistence entropy of a persistence diagram.

    Persistence entropy is the Shannon entropy of the normalised persistence
    distribution::

        H = -Σ_i (p_i / L) log(p_i / L)

    where p_i = death_i − birth_i is the bar length and L = Σ p_i is the
    total persistence.  Essential bars are excluded.

    Returns 0.0 for an empty or single-bar diagram.

    Parameters
    ----------
    pairs:
        Persistence pairs.
    degree:
        If given, restrict to homological degree ``degree``.

    Returns
    -------
    float
        Persistence entropy H ≥ 0.
    """
    pts = _finite_pairs(pairs, degree)
    if not pts:
        return 0.0

    lengths = [d - b for b, d in pts if d > b]
    if not lengths:
        return 0.0

    total = sum(lengths)
    if total == 0.0:
        return 0.0

    entropy = 0.0
    for length in lengths:
        ratio = length / total
        if ratio > 0:
            entropy -= ratio * math.log(ratio)
    return entropy


@dataclass(frozen=True)
class PersistenceLandscape:
    """Sampled persistence landscape functions.

    ``grid`` is the 1-D time grid; ``layers[k][i]`` is λ_{k+1}(grid[i])
    (1-indexed landscape layers, 0-indexed in the array).
    """

    grid: tuple[float, ...]
    layers: tuple[tuple[float, ...], ...]

    @property
    def num_layers(self) -> int:
        return len(self.layers)

    @property
    def grid_size(self) -> int:
        return len(self.grid)

    def layer(self, k: int) -> tuple[float, ...]:
        """Return the k-th landscape layer (1-indexed, k ≥ 1)."""
        if k < 1 or k > self.num_layers:
            raise IndexError(f"Layer k={k} out of range [1, {self.num_layers}]")
        return self.layers[k - 1]


def persistence_landscape(
    pairs: tuple[PersistencePair, ...],
    *,
    degree: int | None = None,
    num_layers: int = 1,
    num_grid_points: int = 100,
    t_min: float | None = None,
    t_max: float | None = None,
) -> PersistenceLandscape:
    """Compute the persistence landscape of a persistence diagram.

    For each bar (b, d) define a tent function::

        λ_{b,d}(t) = max(0, min(t − b, d − t))

    The k-th landscape function λ_k(t) is the k-th largest value of
    {λ_{b,d}(t)} over all bars.

    Parameters
    ----------
    pairs:
        Persistence pairs.
    degree:
        If given, restrict to homological degree ``degree``.
    num_layers:
        Number of landscape layers to compute.
    num_grid_points:
        Number of sample points on the time grid.
    t_min, t_max:
        Time range.  Defaults to the span of all finite bar endpoints.

    Returns
    -------
    PersistenceLandscape
        Sampled landscape functions.
    """
    if num_layers < 1:
        raise ValueError("num_layers must be ≥ 1")
    if num_grid_points < 2:
        raise ValueError("num_grid_points must be ≥ 2")

    pts = _finite_pairs(pairs, degree)

    if not pts:
        grid = tuple(float(i) / (num_grid_points - 1) for i in range(num_grid_points))
        empty: tuple[float, ...] = (0.0,) * num_grid_points
        return PersistenceLandscape(
            grid=grid,
            layers=tuple(empty for _ in range(num_layers)),
        )

    births = [b for b, _ in pts]
    deaths = [d for _, d in pts]
    lo = t_min if t_min is not None else min(births)
    hi = t_max if t_max is not None else max(deaths)

    if lo >= hi:
        hi = lo + 1.0

    step = (hi - lo) / (num_grid_points - 1)
    grid = tuple(lo + i * step for i in range(num_grid_points))

    actual_layers = min(num_layers, len(pts))
    raw_layers: list[list[float]] = []

    for _ in range(actual_layers):
        raw_layers.append([0.0] * num_grid_points)

    for t_idx, t in enumerate(grid):
        values = sorted(
            (max(0.0, min(t - b, d - t)) for b, d in pts),
            reverse=True,
        )
        for k in range(actual_layers):
            raw_layers[k][t_idx] = values[k] if k < len(values) else 0.0

    # Pad with zero layers if num_layers > number of bars
    zero_layer: tuple[float, ...] = (0.0,) * num_grid_points
    all_layers = tuple(tuple(layer) for layer in raw_layers)
    while len(all_layers) < num_layers:
        all_layers = all_layers + (zero_layer,)

    return PersistenceLandscape(grid=grid, layers=all_layers)
