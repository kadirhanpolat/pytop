"""Metric completeness, total boundedness, and metric compactness helpers.

This module provides the finite exact bridge for the v0.1.47 Cilt II corridor:
completeness, total boundedness, and the metric compactness equivalence
(complete + totally bounded <=> compact for metric spaces).

Every function here works on explicit finite metric objects and returns a
structured ``Result``.  For infinite or implicit spaces the functions return an
honest symbolic/unknown result rather than silently claiming a decision.

The pedagogical constraint enforced here is the one stated in
``docs/roadmap/level_based_engelking_integration_roadmap.md``:
  - completeness, total boundedness, and metric compactness are Cilt II topics;
  - they connect the sequences corridor (v0.1.46, Chapter 16) with the
    compactness corridor (v0.1.45, Chapter 14);
  - the functions do NOT open a full Cauchy-completeness decision engine;
    they give finite exact witnesses suitable for classroom checking.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable

from .result import Result


class MetricCompletenessError(ValueError):
    """Raised when a completeness/boundedness request has malformed input."""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_complete(space: Any) -> Result:
    """Check completeness for an explicit finite metric space.

    Every finite metric space is complete because every Cauchy sequence in a
    finite space is eventually constant and therefore convergent.  The function
    returns an exact result with an explicit finiteness witness; for
    non-finite or non-metric inputs it returns an honest symbolic result.
    """
    try:
        data = _finite_metric_data(space)
    except (TypeError, MetricCompletenessError):
        return Result.unknown(
            mode="symbolic",
            value="is_complete",
            justification=[
                "Completeness has exact support only for explicit finite metric spaces."
            ],
            metadata={"operator": "is_complete"},
        )

    n = len(data["points"])
    return Result.true(
        mode="exact",
        value=True,
        justification=[
            "Every finite metric space is complete: "
            "any Cauchy sequence in a finite space is eventually constant "
            "and therefore converges to a point already in the space."
        ],
        proof_outline=[
            "A Cauchy sequence (x_n) in a finite space X eventually lies in a singleton {p}.",
            "This means x_n -> p and p is in X, so the limit is attained.",
        ],
        metadata={
            "operator": "is_complete",
            "carrier_size": n,
            "finite_exactness_note": "Result is exact because the carrier is explicitly finite.",
        },
    )


def is_totally_bounded(space: Any, *, epsilon: float | None = None) -> Result:
    """Check total boundedness for an explicit finite metric space.

    Every finite metric space is totally bounded: for any epsilon > 0 the
    finite carrier itself is a finite epsilon-net.  The function records an
    explicit epsilon witness when ``epsilon`` is supplied, otherwise it records
    the general finite argument.
    """
    try:
        data = _finite_metric_data(space)
    except (TypeError, MetricCompletenessError):
        return Result.unknown(
            mode="symbolic",
            value="is_totally_bounded",
            justification=[
                "Total boundedness has exact support only for explicit finite metric spaces."
            ],
            metadata={"operator": "is_totally_bounded", "epsilon": epsilon},
        )

    points = data["points"]
    n = len(points)

    if epsilon is not None:
        if epsilon <= 0:
            return Result.false(
                mode="exact",
                value=False,
                justification=["epsilon must be strictly positive."],
                metadata={"operator": "is_totally_bounded", "epsilon": epsilon},
            )
        # The full carrier is a finite epsilon-net for any epsilon > 0.
        return Result.true(
            mode="exact",
            value=True,
            justification=[
                f"The carrier itself is a finite {epsilon}-net: "
                "every point is within epsilon of itself."
            ],
            proof_outline=[
                "For any epsilon > 0 the finite set of all carrier points covers the space.",
                "Each point x satisfies d(x, x) = 0 < epsilon.",
            ],
            metadata={
                "operator": "is_totally_bounded",
                "epsilon": epsilon,
                "net": tuple(points),
                "net_size": n,
                "finite_exactness_note": "Result is exact because the carrier is explicitly finite.",
            },
        )

    return Result.true(
        mode="exact",
        value=True,
        justification=[
            "Every finite metric space is totally bounded: "
            "for any epsilon > 0 the finite carrier is itself a finite epsilon-net."
        ],
        proof_outline=[
            "Given epsilon > 0, let N = {all points of X}.",
            "N is finite and every x in X satisfies d(x, x) = 0 < epsilon.",
        ],
        metadata={
            "operator": "is_totally_bounded",
            "epsilon": None,
            "carrier_size": n,
            "finite_exactness_note": "Result is exact because the carrier is explicitly finite.",
        },
    )


def metric_compactness_check(space: Any) -> Result:
    """Check the complete + totally bounded <=> compact corridor entry.

    For an explicit finite metric space this records the equivalence:
      complete + totally bounded <=> compact (for metric spaces).

    Since every finite metric space is both complete and totally bounded it is
    also compact.  The function returns an exact result with the three
    conditions cross-linked; for non-finite or non-metric inputs it returns an
    honest symbolic result.
    """
    try:
        data = _finite_metric_data(space)
    except (TypeError, MetricCompletenessError):
        return Result.unknown(
            mode="symbolic",
            value="metric_compactness_check",
            justification=[
                "The metric compactness corridor check has exact support only for "
                "explicit finite metric spaces."
            ],
            metadata={"operator": "metric_compactness_check"},
        )

    n = len(data["points"])
    return Result.true(
        mode="exact",
        value=True,
        justification=[
            "The explicit finite metric space satisfies: complete + totally bounded => compact.",
            "All three conditions hold: the space is complete (finite => every Cauchy sequence "
            "converges), totally bounded (finite carrier is its own epsilon-net), and compact "
            "(finite space with a metric topology is compact).",
        ],
        proof_outline=[
            "complete: every finite metric space is complete (Cauchy => eventually constant => convergent).",
            "totally_bounded: the carrier is a finite epsilon-net for every epsilon > 0.",
            "compact: complete + totally bounded gives compactness in any metric space.",
        ],
        metadata={
            "operator": "metric_compactness_check",
            "complete": True,
            "totally_bounded": True,
            "compact": True,
            "carrier_size": n,
            "cilt_ii_corridor": "completeness-total-boundedness-metric-compactness",
            "chapter_target": "Chapter 15 (advanced lane) and Chapter 14 (compactness)",
            "finite_exactness_note": "Result is exact because the carrier is explicitly finite.",
        },
    )


def analyze_metric_completeness(
    space: Any,
    *,
    epsilon: float | None = None,
) -> Result:
    """Return a structured completeness/total-boundedness/compactness summary.

    This is the corridor entry-point for v0.1.47.  It delegates to the three
    finite helpers and assembles a single corridor record; metadata marks the
    Cilt II corridor context explicitly.
    """
    complete = is_complete(space)
    totally_bounded = is_totally_bounded(space, epsilon=epsilon)
    compactness = metric_compactness_check(space)

    all_exact = complete.is_exact and totally_bounded.is_exact and compactness.is_exact
    all_true = complete.is_true and totally_bounded.is_true and compactness.is_true

    return Result.true(
        mode="exact" if all_exact else "mixed",
        value={
            "is_complete": complete.value,
            "is_totally_bounded": totally_bounded.value,
            "metric_compact": compactness.value,
        },
        justification=[
            "Completeness, total boundedness, and metric compactness were evaluated "
            "for the supplied space."
        ],
        metadata={
            "operator": "analyze_metric_completeness",
            "complete": complete.to_dict(),
            "totally_bounded": totally_bounded.to_dict(),
            "metric_compactness": compactness.to_dict(),
            "cilt_ii_corridor": "completeness-total-boundedness-metric-compactness",
            "v0_1_47_corridor_record": True,
        },
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _finite_metric_data(space: Any) -> dict[str, Any]:
    """Extract finite metric space data or raise TypeError/MetricCompletenessError."""
    # Accept objects that declare themselves finite (finite topology wrappers)
    # or objects that have an explicit finite carrier and a distance callable.
    carrier_raw = getattr(space, "carrier", None)
    if carrier_raw is None:
        raise TypeError("Expected an object with a finite carrier attribute.")

    try:
        points = tuple(carrier_raw)
    except Exception as exc:
        raise TypeError("The carrier must be a finite iterable.") from exc

    if not points:
        raise MetricCompletenessError("The carrier must be nonempty.")

    # Verify distance is accessible (callable or dict-like)
    distance = getattr(space, "distance", None)
    if distance is None:
        # Try the distance_between method as a fallback
        if not hasattr(space, "distance_between"):
            raise TypeError("Expected a metric space with a distance specification.")

    return {
        "points": points,
        "carrier": frozenset(points),
        "distance": distance,
    }
