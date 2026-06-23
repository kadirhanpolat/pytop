"""Persistent Betti parity helpers (P16.2 / P16.3).

Cross-checks pytop's Vietoris-Rips persistent homology against external
oracles (GUDHI, Ripser) by comparing **Betti numbers at a scale** rather than
the raw persistence-pair count.

Two correctness principles make the comparison apples-to-apples:

1. **Betti-at-scale, not death-count.** The Betti number ``b_k(s)`` of a
   filtration at parameter ``s`` is the number of bars *alive* at ``s`` --
   ``birth <= s < death`` -- not the number of bars that have died by ``s``.
   Counting deaths (an earlier, buggy approach) compares a different quantity
   on each side and never agrees.

2. **Skeleton dimension governs which ``H_k`` is trustworthy.** A Vietoris-Rips
   complex truncated at simplex dimension ``d`` can only represent ``H_k``
   faithfully for ``k <= d - 1``: killing a ``k``-cycle requires
   ``(k+1)``-simplices. So a triangle-only (``d = 2``) complex gives correct
   ``H_0`` and ``H_1`` but spurious ``H_2`` (the filled triangles create
   2-cycles with nothing to bound them). To compare ``H_k`` both sides must
   build simplices up to dimension ``k + 1``.

The helpers below sample Betti numbers at the *midpoints between consecutive
filtration events*, where no bar boundary coincides, so the comparison is
free of floating-point boundary flicker and is not cherry-picked to a single
scale.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

# (dimension, birth, death) -- death may be ``math.inf`` for essential classes.
Bar = tuple[int, float, float]

__all__ = [
    "Bar",
    "BettiParity",
    "betti_at_scale",
    "comparison_scales",
    "pytop_rips_bars",
    "gudhi_rips_bars",
    "ripser_rips_bars",
    "compare_betti",
]


@dataclass(frozen=True)
class BettiParity:
    """Result of a pytop-vs-oracle Betti comparison over a range of scales."""

    oracle: str
    max_betti_dim: int
    scales: tuple[float, ...]
    # scale -> dim -> (pytop_betti, oracle_betti)
    samples: tuple[tuple[float, dict[int, tuple[int, int]]], ...]

    @property
    def agree(self) -> bool:
        """True iff pytop and the oracle agree on every sampled (scale, dim)."""
        return all(
            p == o
            for _, per_dim in self.samples
            for (p, o) in per_dim.values()
        )

    def disagreements(self) -> list[tuple[float, int, int, int]]:
        """List of (scale, dim, pytop_betti, oracle_betti) that disagree."""
        out: list[tuple[float, int, int, int]] = []
        for s, per_dim in self.samples:
            for dim, (p, o) in per_dim.items():
                if p != o:
                    out.append((s, dim, p, o))
        return out


def betti_at_scale(bars: list[Bar], scale: float, max_dim: int) -> dict[int, int]:
    """Betti numbers at filtration parameter ``scale``.

    Counts bars alive at ``scale`` (``birth <= scale < death``) per dimension,
    for dimensions ``0 .. max_dim`` inclusive.
    """
    betti = {d: 0 for d in range(max_dim + 1)}
    for dim, birth, death in bars:
        if dim <= max_dim and birth <= scale < death:
            betti[dim] += 1
    return betti


def comparison_scales(
    *bar_sets: list[Bar], max_scale: float, limit: int = 64
) -> tuple[float, ...]:
    """Midpoints between consecutive distinct filtration events.

    Merges the finite birth/death values from every supplied bar set (clamped
    to ``max_scale``), then returns the midpoints of consecutive distinct
    events. Sampling at midpoints avoids exact bar-boundary coincidences, so
    the resulting Betti counts are unambiguous for every implementation.
    """
    events: set[float] = {0.0, max_scale}
    for bars in bar_sets:
        for _dim, birth, death in bars:
            if 0.0 <= birth <= max_scale:
                events.add(round(birth, 9))
            if death != math.inf and 0.0 <= death <= max_scale:
                events.add(round(death, 9))
    ordered = sorted(events)
    mids = [
        (ordered[i] + ordered[i + 1]) / 2.0
        for i in range(len(ordered) - 1)
        if ordered[i + 1] - ordered[i] > 1e-9
    ]
    if len(mids) > limit:
        step = len(mids) / limit
        mids = [mids[int(i * step)] for i in range(limit)]
    return tuple(mids)


def pytop_rips_bars(
    points: Sequence[tuple[float, ...]], max_scale: float, max_betti_dim: int
) -> list[Bar]:
    """pytop Vietoris-Rips bars, with simplices up to dimension ``max_betti_dim + 1``."""
    from pytop import persistent_homology
    from pytop.metric_spaces import FiniteMetricSpace

    space = FiniteMetricSpace(
        carrier=tuple(points), distance=lambda p, q: math.dist(p, q)
    )
    pairs = persistent_homology(
        space, max_dimension=max_betti_dim + 1, max_scale=max_scale
    )
    return [(p.dimension, float(p.birth), float(p.death)) for p in pairs]


def gudhi_rips_bars(
    points: Sequence[tuple[float, ...]], max_scale: float, max_betti_dim: int
) -> list[Bar]:
    """GUDHI Vietoris-Rips bars, with simplices up to dimension ``max_betti_dim + 1``."""
    import gudhi  # noqa: PLC0415

    rips = gudhi.RipsComplex(points=points, max_edge_length=max_scale)
    tree = rips.create_simplex_tree(max_dimension=max_betti_dim + 1)
    tree.compute_persistence()
    bars: list[Bar] = []
    for dim, (birth, death) in tree.persistence():
        bars.append((dim, float(birth), float(death)))
    return bars


def ripser_rips_bars(
    points: Sequence[tuple[float, ...]], max_scale: float, max_betti_dim: int
) -> list[Bar]:
    """Ripser Vietoris-Rips bars (returns intervals per homology dimension)."""
    import numpy as np  # noqa: PLC0415
    import ripser as rp  # noqa: PLC0415

    result = rp.ripser(
        np.array(points), maxdim=max_betti_dim, thresh=max_scale, do_cocycles=False
    )
    bars: list[Bar] = []
    for dim, dgm in enumerate(result["dgms"]):
        for birth, death in dgm:
            bars.append((dim, float(birth), float(death)))
    return bars


def compare_betti(
    points: Sequence[tuple[float, ...]],
    *,
    oracle: str,
    max_scale: float,
    max_betti_dim: int,
) -> BettiParity:
    """Compare pytop vs an oracle Betti curve over event-midpoint scales.

    ``oracle`` is ``"gudhi"`` or ``"ripser"``. Raises ``ImportError`` if the
    requested oracle is not installed (callers should ``importorskip`` first).
    """
    pytop_bars = pytop_rips_bars(points, max_scale, max_betti_dim)
    if oracle == "gudhi":
        oracle_bars = gudhi_rips_bars(points, max_scale, max_betti_dim)
    elif oracle == "ripser":
        oracle_bars = ripser_rips_bars(points, max_scale, max_betti_dim)
    else:
        raise ValueError(f"unknown oracle {oracle!r}; expected 'gudhi' or 'ripser'")

    scales = comparison_scales(pytop_bars, oracle_bars, max_scale=max_scale)
    samples: list[tuple[float, dict[int, tuple[int, int]]]] = []
    for s in scales:
        bp = betti_at_scale(pytop_bars, s, max_betti_dim)
        bo = betti_at_scale(oracle_bars, s, max_betti_dim)
        per_dim = {d: (bp[d], bo[d]) for d in range(max_betti_dim + 1)}
        samples.append((s, per_dim))
    return BettiParity(
        oracle=oracle,
        max_betti_dim=max_betti_dim,
        scales=scales,
        samples=tuple(samples),
    )
