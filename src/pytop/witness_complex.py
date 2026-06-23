"""Approximate persistence via landmark sampling and witness complexes.

The witness complex (de Silva & Carlsson 2004) approximates the topology of a
large point cloud ``P ⊂ ℝ^d`` using a small set of ``k`` landmarks ``L ⊂ P``.
A simplex ``σ ⊆ L`` enters the filtration at the scale where some point in
``P`` is within distance ``ε`` of every vertex of ``σ`` — that point *witnesses*
``σ``.  For ``k ≪ |P|`` the resulting :class:`FilteredComplex` is far smaller
than the full Vietoris–Rips complex on ``P``.

Pure Python, no dependencies.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations

from .persistent_homology import FilteredComplex, PersistencePair
from .persistent_homology_optimized import persistence_pairs_twist

__all__ = [
    "landmark_sample",
    "WitnessComplex",
    "witness_filtration",
    "persistent_homology_witness",
]

Point = Sequence[float]


# ---------------------------------------------------------------------------
# Distance helpers
# ---------------------------------------------------------------------------


def _dist(a: Point, b: Point) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# ---------------------------------------------------------------------------
# Landmark selection
# ---------------------------------------------------------------------------


def landmark_sample(
    points: Sequence[Point],
    k: int,
    *,
    method: str = "maxmin",
    seed: int | None = None,
) -> list[int]:
    """Select ``k`` landmark indices from ``points``.

    Parameters
    ----------
    points:
        Point cloud as a sequence of coordinate tuples.
    k:
        Number of landmarks.  Must satisfy ``1 ≤ k ≤ len(points)``.
    method:
        ``"maxmin"`` (default) — greedy farthest-point sampling: each new
        landmark is the point farthest from the current landmark set,
        maximising the minimum covering radius.  Gives better coverage than
        random sampling.

        ``"random"`` — uniform random sample without replacement.
    seed:
        Optional RNG seed (affects both methods for reproducibility).

    Returns
    -------
    list[int]
        Indices into ``points`` of the selected landmarks, in selection order.
    """
    n = len(points)
    if not 1 <= k <= n:
        raise ValueError(f"k must satisfy 1 ≤ k ≤ {n}, got {k}.")

    rng = random.Random(seed)

    if method == "random":
        return rng.sample(range(n), k)

    if method == "maxmin":
        first = rng.randrange(n)
        landmarks = [first]
        # min_dist[i] = distance from point i to the nearest current landmark
        min_dist = [_dist(points[i], points[first]) for i in range(n)]

        while len(landmarks) < k:
            # Next landmark: point farthest from all current landmarks
            nxt = max(range(n), key=lambda i: min_dist[i])
            landmarks.append(nxt)
            p_nxt = points[nxt]
            for i in range(n):
                d = _dist(points[i], p_nxt)
                if d < min_dist[i]:
                    min_dist[i] = d

        return landmarks

    raise ValueError(f"Unknown landmark method {method!r}. Use 'maxmin' or 'random'.")


# ---------------------------------------------------------------------------
# Witness filtration
# ---------------------------------------------------------------------------


def witness_filtration(
    points: Sequence[Point],
    landmarks: Sequence[Point],
    max_dim: int = 1,
    max_eps: float = math.inf,
) -> FilteredComplex:
    """Build a witness filtration on ``landmarks`` witnessed by ``points``.

    A simplex ``σ = {l₀, …, l_p} ⊆ L`` enters at

        ε(σ) = min_{w ∈ P}  max_{l_i ∈ σ}  d(w, l_i)

    (the smallest scale at which *some* witness ``w`` is within ``ε`` of every
    vertex).  This is the *strong witness* definition (de Silva & Carlsson 2004,
    Def. 3.2).

    Parameters
    ----------
    points:
        Full point cloud (witnesses).
    landmarks:
        Landmark points (vertices of the complex).
    max_dim:
        Maximum simplex dimension to include (default 1 = edges only).
    max_eps:
        Discard simplices with birth > ``max_eps`` (default: include all).

    Returns
    -------
    FilteredComplex
        Simplices sorted by birth time, faces before cofaces.
    """
    n_l = len(landmarks)
    n_p = len(points)

    # Precompute distances d[w][lm] = d(points[w], landmarks[lm])
    d: list[list[float]] = [
        [_dist(points[w], landmarks[lm]) for lm in range(n_l)]
        for w in range(n_p)
    ]

    # For each potential simplex σ, find the minimum ε across all witnesses.
    # ε(σ, w) = max_{l ∈ σ} d(w, l).  ε(σ) = min_w ε(σ, w).
    result_simplices: list[tuple[int, ...]] = []
    result_births: list[float] = []
    result_dims: list[int] = []

    for dim in range(max_dim + 1):
        for sigma in combinations(range(n_l), dim + 1):
            eps_sigma = math.inf
            for w in range(n_p):
                eps_w = max(d[w][lm] for lm in sigma)
                if eps_w < eps_sigma:
                    eps_sigma = eps_w
            if eps_sigma <= max_eps:
                result_simplices.append(sigma)
                result_births.append(eps_sigma)
                result_dims.append(dim)

    # Sort: by birth ascending, then by dimension (faces before cofaces at same birth).
    order = sorted(
        range(len(result_simplices)),
        key=lambda i: (result_births[i], result_dims[i]),
    )
    return FilteredComplex(
        simplices=tuple(result_simplices[i] for i in order),
        births=tuple(result_births[i] for i in order),
        dimensions=tuple(result_dims[i] for i in order),
    )


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WitnessComplex:
    """Result of a witness-complex computation.

    Attributes
    ----------
    filtration:
        The :class:`FilteredComplex` built on the selected landmarks.
    landmark_indices:
        Indices into the original point cloud that were chosen as landmarks.
    pairs:
        Persistence pairs computed from the filtration.
    """

    filtration: FilteredComplex
    landmark_indices: list[int]
    pairs: tuple[PersistencePair, ...]


def persistent_homology_witness(
    points: Sequence[Point],
    k: int,
    max_dim: int = 1,
    *,
    max_eps: float = math.inf,
    landmark_method: str = "maxmin",
    seed: int | None = None,
) -> WitnessComplex:
    """Approximate persistence of a point cloud via witness-complex sampling.

    Selects ``k`` landmarks from ``points``, builds a witness filtration up to
    dimension ``max_dim``, and reduces it with Twist+Clearing.

    Parameters
    ----------
    points:
        Input point cloud.
    k:
        Number of landmarks (``k ≪ len(points)`` for the approximation to be
        useful).
    max_dim:
        Maximum homological dimension to compute (default 1).
    max_eps:
        Filtration cutoff — simplices with birth > ``max_eps`` are excluded.
    landmark_method:
        ``"maxmin"`` (default) or ``"random"``.
    seed:
        RNG seed passed to :func:`landmark_sample`.

    Returns
    -------
    WitnessComplex
    """
    land_idx = landmark_sample(points, k, method=landmark_method, seed=seed)
    land_pts = [points[i] for i in land_idx]
    filt = witness_filtration(points, land_pts, max_dim=max_dim, max_eps=max_eps)
    pairs = persistence_pairs_twist(filt)
    return WitnessComplex(
        filtration=filt,
        landmark_indices=land_idx,
        pairs=pairs,
    )
