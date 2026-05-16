"""Local compactness and compactification helpers — Cilt III v0.1.56 corridor.

This module provides durable public helpers for local compactness, one-point
(Alexandroff) compactification, and related structural checks.  The design
principle is the same as for ``separation`` and ``compactness``: return
structured ``Result`` objects that distinguish exact finite answers from
theorem-level inferences and explicitly flag the unknown case instead of
guessing.

Public surface (Cilt III durable API)
--------------------------------------
``is_locally_compact(space)``
    Conservative local-compactness check. Exact for finite spaces with an
    explicit topology; theorem-level for tagged/known spaces.

``one_point_compactification(space)``
    Construct the Alexandroff one-point extension of a locally compact
    Hausdorff finite space, returning a new ``FiniteTopologicalSpace``.

``alexandroff_point_check(space)``
    Report whether the given space could serve as the base of an Alexandroff
    compactification (i.e. is locally compact Hausdorff and non-compact).

``local_compactness_profile(space)``
    Return a dict with ``is_locally_compact``, ``is_hausdorff``,
    ``is_compact``, and ``alexandroff_eligible`` as ``Result`` values.

``analyze_local_compactness(space)``
    Return a structured ``Result`` with all profile fields folded into
    metadata — a single-call facade for notebooks and manuscripts.
"""

from __future__ import annotations

from typing import Any

from .capabilities import DEFAULT_REGISTRY
from .compactness import analyze_compactness
from .finite_spaces import FiniteTopologicalSpace
from .result import Result
from .separation import analyze_separation

# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

TRUE_TAGS: set[str] = {
    "locally_compact",
    "locally_compact_hausdorff",
    "lc_hausdorff",
}

FALSE_TAGS: set[str] = {
    "not_locally_compact",
}

COMPACT_TRUE_TAGS: set[str] = {"compact", "marked_compact"}
HAUSDORFF_TRUE_TAGS: set[str] = {"hausdorff", "t2", "lc_hausdorff", "locally_compact_hausdorff"}
HAUSDORFF_FALSE_TAGS: set[str] = {"not_hausdorff", "not_t2"}


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class LocalCompactnessError(ValueError):
    """Raised for invalid input to local compactness helpers."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_tags(space: Any) -> set[str]:
    raw = getattr(space, "tags", None) or getattr(space, "_tags", None)
    if isinstance(raw, (set, list, tuple, frozenset)):
        return {str(t).strip().lower() for t in raw}
    return set()


def _representation_of(space: Any) -> str:
    if isinstance(space, FiniteTopologicalSpace):
        return "finite"
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _mode_from_support(support: str) -> str:
    mapping = {"exact": "exact", "theorem": "theorem", "symbolic": "symbolic"}
    return mapping.get(support, "symbolic")


def _matches_any(tags: set[str], candidates: set[str]) -> bool:
    return bool(tags & candidates)


# ---------------------------------------------------------------------------
# Finite exact check
# ---------------------------------------------------------------------------

def _finite_is_locally_compact(space: FiniteTopologicalSpace) -> bool:
    """Every point has a compact neighbourhood.

    For finite spaces every open set is compact (finite sets are compact under
    any topology), so a point has a compact neighbourhood if and only if it has
    *some* open neighbourhood — which is always true because the whole space is
    open.  Hence every finite topological space is locally compact.
    """
    # Every finite space is locally compact: the whole space is a compact
    # neighbourhood of each point (finite spaces are compact).
    return True


def _finite_is_hausdorff(space: FiniteTopologicalSpace) -> bool:
    """Exact Hausdorff check for finite spaces."""
    points = list(space.carrier)
    topology = space.topology
    for i, x in enumerate(points):
        for y in points[i + 1:]:
            separated = False
            for u in topology:
                if x in u and y not in u:
                    for v in topology:
                        if y in v and x not in v and not (u & v):
                            separated = True
                            break
                if separated:
                    break
            if not separated:
                return False
    return True


def _finite_is_compact(space: FiniteTopologicalSpace) -> bool:
    """Every finite topological space is compact."""
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_locally_compact(space: Any) -> Result:
    """Return a structured result for local compactness.

    Exact for finite spaces; theorem-level for well-known tagged spaces;
    unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    capability = DEFAULT_REGISTRY.support_for(representation, "locally_compact")

    if _matches_any(tags, FALSE_TAGS):
        return Result.false(
            mode=_mode_from_support(capability.support),
            value="locally_compact",
            justification=["The space carries an explicit negative tag for local compactness."],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    if representation == "finite" and hasattr(space, "topology"):
        exact = _finite_is_locally_compact(space)
        return Result(
            status="true" if exact else "false",
            mode="exact",
            value="locally_compact",
            justification=["Every finite topological space is locally compact: finite sets are compact."],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    if _matches_any(tags, TRUE_TAGS):
        return Result.true(
            mode="theorem",
            value="locally_compact",
            justification=["The space carries a positive local compactness tag."],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    # Well-known theorem-level inferences
    if _matches_any(tags, COMPACT_TRUE_TAGS):
        return Result.true(
            mode="theorem",
            value="locally_compact",
            justification=["Every compact space is locally compact (the whole space is a compact neighbourhood)."],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    metric_tags = {"metric", "metrizable", "complete_metric"}
    if _matches_any(tags, metric_tags):
        return Result(
            status="conditional",
            mode="theorem",
            value="locally_compact",
            justification=[
                "Metric spaces are not automatically locally compact.",
                "ℝⁿ is locally compact; ℓ² (infinite-dimensional Hilbert space) is not.",
                "Tag the space explicitly or add 'locally_compact'/'not_locally_compact'.",
            ],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    return Result.unknown(
        mode=_mode_from_support(capability.support),
        value="locally_compact",
        justification=["Insufficient information to decide local compactness for this space."],
        metadata={"representation": representation, "tags": sorted(tags)},
    )


def one_point_compactification(space: FiniteTopologicalSpace, point_label: Any = "∞") -> FiniteTopologicalSpace:
    """Construct the Alexandroff one-point compactification.

    The input space must be a locally compact Hausdorff finite space.  The
    new point ``point_label`` (default ``'∞'``) is added; open sets of the
    extension are:

    * every open set of the original space, and
    * sets of the form ``{point_label} ∪ (X \\ K)`` where ``K`` is a compact
      (here: any) closed subset of the original space.

    For finite spaces every subset is compact, so the second family gives
    ``{point_label} ∪ (X \\ C)`` for every closed ``C``.

    Parameters
    ----------
    space:
        A ``FiniteTopologicalSpace``.  Local compactness and Hausdorff checks
        are advisory here; the construction is always well-defined on finite
        data.
    point_label:
        Label for the new point.  Defaults to ``'∞'``.

    Returns
    -------
    FiniteTopologicalSpace
        The Alexandroff extension with one extra point.
    """
    if not isinstance(space, FiniteTopologicalSpace):
        raise LocalCompactnessError(
            "one_point_compactification requires a FiniteTopologicalSpace instance."
        )
    if point_label in space.carrier:
        raise LocalCompactnessError(
            f"point_label {point_label!r} already exists in the space."
        )

    old_points = frozenset(space.carrier)
    new_points = old_points | {point_label}

    old_topology: list[frozenset[Any]] = [frozenset(u) for u in space.topology]
    all_open: set[frozenset[Any]] = set(old_topology)

    # Closed sets of the original space
    closed_sets = [old_points - u for u in old_topology]

    # For each closed (= compact in finite case) subset C add {∞} ∪ (X \ C)
    for c in closed_sets:
        new_open = frozenset({point_label}) | (old_points - c)
        all_open.add(new_open)

    # The whole extension must be open
    all_open.add(frozenset(new_points))
    # Empty set
    all_open.add(frozenset())

    return FiniteTopologicalSpace(carrier=list(new_points), topology=list(all_open))


def alexandroff_point_check(space: Any) -> Result:
    """Report whether ``space`` is eligible as the base of an Alexandroff compactification.

    Eligibility requires:
    * locally compact,
    * Hausdorff,
    * non-compact.

    Returns a structured ``Result``.  For finite spaces the compact condition
    always holds (finite spaces are compact), so the result is always
    ``false`` with an explanation.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    lc_result = is_locally_compact(space)
    hausdorff_result = analyze_separation(space, "hausdorff")
    compact_result = analyze_compactness(space, "compact")

    lc_ok = lc_result.status == "true"
    h_ok = hausdorff_result.status == "true"
    compact_ok = compact_result.status == "true"
    eligibility_metadata = {
        "representation": representation,
        "locally_compact": lc_ok,
        "hausdorff": h_ok,
        "compact": compact_ok,
        "tags": sorted(tags),
    }

    if representation == "finite":
        return Result(
            status="false",
            mode="exact",
            value="alexandroff_eligible",
            justification=[
                "Every finite topological space is compact.",
                "The Alexandroff compactification is meaningful only for non-compact spaces.",
                "A finite space can still be extended by one point for pedagogical illustration.",
            ],
            metadata=eligibility_metadata,
        )

    if not lc_ok:
        return Result.false(
            mode="theorem",
            value="alexandroff_eligible",
            justification=["Space is not locally compact — Alexandroff compactification condition fails."],
            metadata=eligibility_metadata,
        )
    if not h_ok:
        return Result.false(
            mode="theorem",
            value="alexandroff_eligible",
            justification=["Space is not Hausdorff — the one-point extension would not be Hausdorff."],
            metadata=eligibility_metadata,
        )
    if compact_ok:
        return Result.false(
            mode="theorem",
            value="alexandroff_eligible",
            justification=["Space is already compact — the one-point compactification adds a trivial isolated point."],
            metadata=eligibility_metadata,
        )

    return Result.true(
        mode="theorem",
        value="alexandroff_eligible",
        justification=[
            "Space is locally compact, Hausdorff, and non-compact.",
            "The Alexandroff one-point compactification produces a compact Hausdorff space.",
        ],
        metadata=eligibility_metadata,
    )


def local_compactness_profile(space: Any) -> dict[str, Result]:
    """Return a structured profile covering local compactness, Hausdorff, compactness, and Alexandroff eligibility."""
    return {
        "is_locally_compact": is_locally_compact(space),
        "is_hausdorff": analyze_separation(space, "hausdorff"),
        "is_compact": analyze_compactness(space, "compact"),
        "alexandroff_eligible": alexandroff_point_check(space),
    }


def analyze_local_compactness(space: Any) -> Result:
    """Single-call facade: local compactness result with full profile in metadata.

    This is the main entry point for notebooks and manuscript API-bridge remarks.
    """
    profile = local_compactness_profile(space)
    lc = profile["is_locally_compact"]

    metadata = {
        "is_locally_compact": lc.status,
        "is_hausdorff": profile["is_hausdorff"].status,
        "is_compact": profile["is_compact"].status,
        "alexandroff_eligible": profile["alexandroff_eligible"].status,
    }

    return Result(
        status=lc.status,
        mode=lc.mode,
        value="local_compactness_analysis",
        justification=lc.justification,
        metadata=metadata,
    )


__all__ = [
    "LocalCompactnessError",
    "is_locally_compact",
    "one_point_compactification",
    "alexandroff_point_check",
    "local_compactness_profile",
    "analyze_local_compactness",
]
