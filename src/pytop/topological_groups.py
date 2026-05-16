"""Topological group support: axiom checks, separation theorems, and classification.

Key theorems implemented
------------------------
- Every T0 topological group is Tychonoff (T3.5).
- Every Lie group is metrizable (hence Tychonoff).
- Every profinite group is compact Hausdorff totally disconnected.
- T0 + continuous group operations → topological group axioms satisfied.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class TopologicalGroupProfile:
    """A curated topological group family for the named profile registry."""

    key: str
    display_name: str
    group_type: str
    presentation_layer: str
    focus: str
    separation_level: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

GROUP_POSITIVE_TAGS: set[str] = {
    "topological_group", "group", "lie_group",
    "profinite_group", "profinite", "compact_group",
    "locally_compact_group", "lca_group", "discrete_group", "abelian_group",
}
GROUP_NEGATIVE_TAGS: set[str] = {"not_group", "not_topological_group", "semigroup_only"}
CONTINUOUS_OP_TAGS: set[str] = {
    "continuous_multiplication", "continuous_inversion", "continuous_group_ops",
}
LIE_GROUP_TAGS: set[str] = {"lie_group", "lie", "smooth_manifold_group"}
PROFINITE_TAGS: set[str] = {"profinite", "profinite_group", "profinite_completion"}
COMPACT_GROUP_TAGS: set[str] = {
    "compact_group", "compact_hausdorff_group", "compact_lie_group",
}
LC_GROUP_TAGS: set[str] = {"locally_compact_group", "lca_group"}
LOCALLY_COMPACT_TAGS: set[str] = {"locally_compact", "locally_compact_group", "lca_group"}
ABELIAN_TAGS: set[str] = {"abelian", "abelian_group", "commutative_group", "lca_group"}
DISCRETE_GROUP_TAGS: set[str] = {"discrete_group", "discrete"}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_tags(space: Any) -> set[str]:
    raw = getattr(space, "tags", None) or getattr(space, "_tags", None)
    if isinstance(raw, (set, list, tuple, frozenset)):
        return {str(t).strip().lower() for t in raw}
    return set()


def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _matches_any(tags: set[str], candidates: set[str]) -> bool:
    return bool(tags & candidates)


# ---------------------------------------------------------------------------
# Named profile registry
# ---------------------------------------------------------------------------

def get_named_topological_group_profiles() -> tuple[TopologicalGroupProfile, ...]:
    """Return the registry of well-known topological group families."""
    return (
        TopologicalGroupProfile(
            key="real_lie_group",
            display_name="Real Lie group",
            group_type="lie",
            presentation_layer="main_text",
            focus=(
                "smooth manifold with compatible group structure; metrizable and Tychonoff; "
                "canonical examples: GL(n,R), SL(n,R), O(n), SO(n)"
            ),
            separation_level="T3.5",
            chapter_targets=("20", "36"),
        ),
        TopologicalGroupProfile(
            key="compact_lie_group",
            display_name="Compact Lie group",
            group_type="compact_lie",
            presentation_layer="main_text",
            focus=(
                "compact Lie group admitting a bi-invariant Riemannian metric; "
                "canonical examples: SO(n), SU(n), U(n), Sp(n)"
            ),
            separation_level="T3.5",
            chapter_targets=("20", "35", "36"),
        ),
        TopologicalGroupProfile(
            key="profinite_group",
            display_name="Profinite group",
            group_type="profinite",
            presentation_layer="advanced_note",
            focus=(
                "inverse limit of finite discrete groups; compact Hausdorff totally disconnected; "
                "canonical examples: Gal(K̄/K), ℤ̂ = ∏_p ℤ_p, ℤ_p"
            ),
            separation_level="T3.5",
            chapter_targets=("20", "34", "36"),
        ),
        TopologicalGroupProfile(
            key="locally_compact_abelian_group",
            display_name="Locally compact abelian (LCA) group",
            group_type="locally_compact_abelian",
            presentation_layer="advanced_note",
            focus=(
                "Pontryagin duality domain; self-dual up to isomorphism; "
                "canonical examples: R, Z, T = R/Z, Z/nZ, Q_p"
            ),
            separation_level="T3.5",
            chapter_targets=("20", "36"),
        ),
        TopologicalGroupProfile(
            key="discrete_group",
            display_name="Discrete topological group",
            group_type="discrete",
            presentation_layer="selected_block",
            focus=(
                "any group with the discrete topology; metrizable and Tychonoff; "
                "canonical examples: Z, Q, free groups, symmetric groups S_n"
            ),
            separation_level="T3.5",
            chapter_targets=("20",),
        ),
    )


def topological_group_layer_summary() -> dict[str, int]:
    """Return counts of named profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_topological_group_profiles()))


def topological_group_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from group_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_topological_group_profiles():
        index.setdefault(p.group_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_topological_group(space: Any) -> Result:
    """Check whether a space is (or carries structure of) a topological group.

    Decision layers
    ---------------
    1. Explicit negative tags → false.
    2. Lie group tags → true (every Lie group is a topological group).
    3. Profinite tags → true (every profinite group is a topological group).
    4. Compact group / locally compact group tags → true.
    5. Direct topological group, abelian group, or discrete group tag → true.
    6. T0 + continuous group operations → true (axioms satisfied via tags).
    7. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    # Layer 1: explicit negative tags
    if _matches_any(tags, GROUP_NEGATIVE_TAGS):
        blocking = next(t for t in tags if t in GROUP_NEGATIVE_TAGS)
        return Result.false(
            mode="theorem",
            value="topological_group",
            justification=[f"The space carries blocking tag {blocking!r} which rules out topological group structure."],
            metadata={**base, "criterion": None},
        )

    # Layer 2: Lie group
    if _matches_any(tags, LIE_GROUP_TAGS):
        return Result.true(
            mode="theorem",
            value="topological_group",
            justification=[
                "A Lie group is a smooth manifold with a compatible group structure, hence a topological group.",
            ],
            metadata={**base, "criterion": "lie_group"},
        )

    # Layer 3: profinite
    if _matches_any(tags, PROFINITE_TAGS):
        return Result.true(
            mode="theorem",
            value="topological_group",
            justification=[
                "Profinite groups are inverse limits of finite discrete groups and carry a canonical compact Hausdorff topological group structure.",
            ],
            metadata={**base, "criterion": "profinite"},
        )

    # Layer 4: compact group / locally compact group
    if _matches_any(tags, COMPACT_GROUP_TAGS | LC_GROUP_TAGS):
        return Result.true(
            mode="theorem",
            value="topological_group",
            justification=["The space is tagged as a compact or locally compact group, which is a topological group."],
            metadata={**base, "criterion": "compact_or_lc_group"},
        )

    # Layer 5: direct group tags
    direct_tags = GROUP_POSITIVE_TAGS | ABELIAN_TAGS | DISCRETE_GROUP_TAGS
    if _matches_any(tags, direct_tags):
        return Result.true(
            mode="theorem",
            value="topological_group",
            justification=["The space carries a direct topological group tag."],
            metadata={**base, "criterion": "direct_tag"},
        )

    # Layer 6: T0 + continuous operations
    has_t0 = bool(tags & {
        "t0", "t1", "hausdorff", "t2", "t3", "tychonoff", "t3_5", "t4", "metric",
    })
    if has_t0 and _matches_any(tags, CONTINUOUS_OP_TAGS):
        return Result.true(
            mode="theorem",
            value="topological_group",
            justification=[
                "T0 separation + continuous group operations confirms the topological group axioms.",
                "A topological group requires multiplication (x,y) ↦ xy and inversion x ↦ x⁻¹ to be jointly continuous.",
            ],
            metadata={**base, "criterion": "axioms_via_tags"},
        )

    return Result.unknown(
        mode="symbolic",
        value="topological_group",
        justification=[
            "Insufficient information to confirm topological group structure.",
            "Tag with 'topological_group', 'lie_group', 'profinite', or provide 't0'+'continuous_group_ops'.",
        ],
        metadata={**base, "criterion": None},
    )


def topological_group_separation(space: Any) -> Result:
    """Establish the Tychonoff (T3.5) separation level of a topological group.

    Core theorem: Every T0 topological group is Tychonoff (T3.5).
    In a topological group, left translations x ↦ ax are homeomorphisms
    (homogeneity), so T0 forces Hausdorff, and the group structure yields
    complete regularity via Urysohn-type separation.

    Returns unknown if the space is not confirmed to be a topological group.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    grp_r = is_topological_group(space)
    if not grp_r.is_true:
        return Result.unknown(
            mode="symbolic",
            value="tychonoff",
            justification=[
                "Cannot determine separation level: the space is not confirmed to be a topological group.",
            ],
            metadata={**base, "group_confirmed": False},
        )

    # Lie groups: smooth manifolds are metrizable
    if _matches_any(tags, LIE_GROUP_TAGS):
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Every Lie group is a smooth manifold, hence metrizable and Tychonoff (T3.5).",
            ],
            metadata={**base, "criterion": "lie_group_metrizable", "group_confirmed": True},
        )

    # Profinite groups: compact Hausdorff → T4 → Tychonoff
    if _matches_any(tags, PROFINITE_TAGS):
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Every profinite group is compact Hausdorff (T4), hence Tychonoff (T3.5) by Urysohn's Lemma.",
            ],
            metadata={**base, "criterion": "profinite_compact_hausdorff", "group_confirmed": True},
        )

    # Compact group → compact Hausdorff → T4 → Tychonoff
    if _matches_any(tags, COMPACT_GROUP_TAGS):
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Every compact Hausdorff group is T4, hence Tychonoff (T3.5) by Urysohn's Lemma.",
            ],
            metadata={**base, "criterion": "compact_group_hausdorff", "group_confirmed": True},
        )

    # Discrete group → metrizable (discrete metric) → Tychonoff
    if _matches_any(tags, DISCRETE_GROUP_TAGS):
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Every discrete topological group is metrizable (discrete metric), hence Tychonoff (T3.5).",
            ],
            metadata={**base, "criterion": "discrete_group_metrizable", "group_confirmed": True},
        )

    # General T0 topological group → Tychonoff
    has_t0 = bool(tags & {
        "t0", "t1", "hausdorff", "t2", "t3", "tychonoff", "t3_5", "t4", "metric",
        "locally_compact", "locally_compact_group", "lca_group",
    })
    if has_t0:
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Every T0 topological group is Tychonoff (T3.5).",
                "Homogeneity (translations are homeomorphisms) upgrades T0 to Hausdorff; complete regularity follows from the group structure.",
            ],
            metadata={**base, "criterion": "t0_group_is_tychonoff", "group_confirmed": True},
        )

    return Result.unknown(
        mode="symbolic",
        value="tychonoff",
        justification=[
            "The space is a topological group but no T0-or-stronger separation tag is available.",
            "Add a T0 (or stronger) tag to apply the T0-topological-group-is-Tychonoff theorem.",
        ],
        metadata={**base, "criterion": None, "group_confirmed": True},
    )


def classify_topological_group(space: Any) -> dict[str, Any]:
    """Classify a topological group by structural type.

    Keys
    ----
    group_type : str
        One of ``"lie"``, ``"compact_lie"``, ``"profinite"``,
        ``"compact_abelian"``, ``"locally_compact_abelian"``,
        ``"compact"``, ``"discrete"``, ``"general"``, ``"unknown"``.
    is_topological_group : Result
    is_compact : bool or None
    is_abelian : bool or None
    is_discrete : bool or None
    separation : Result
    key_properties : list[str]
    """
    tags = _extract_tags(space)
    grp_r = is_topological_group(space)
    sep_r = topological_group_separation(space)

    is_compact_v: bool | None = (
        True if bool(tags & {"compact", "compact_group", "compact_lie_group",
                             "profinite", "compact_hausdorff_group"})
        else (False if "not_compact" in tags else None)
    )
    is_abelian_v: bool | None = (
        True if _matches_any(tags, ABELIAN_TAGS)
        else (False if "not_abelian" in tags else None)
    )
    is_discrete_v: bool | None = (
        True if _matches_any(tags, DISCRETE_GROUP_TAGS)
        else (False if "not_discrete" in tags else None)
    )

    empty_result: dict[str, Any] = {
        "group_type": "unknown",
        "is_topological_group": grp_r,
        "is_compact": is_compact_v,
        "is_abelian": is_abelian_v,
        "is_discrete": is_discrete_v,
        "separation": sep_r,
        "key_properties": [],
    }

    if not grp_r.is_true:
        return empty_result

    # Priority-ordered type determination
    if _matches_any(tags, LIE_GROUP_TAGS):
        group_type = "compact_lie" if is_compact_v else "lie"
    elif _matches_any(tags, PROFINITE_TAGS):
        group_type = "profinite"
    elif _matches_any(tags, DISCRETE_GROUP_TAGS):
        group_type = "discrete"
    elif is_compact_v and is_abelian_v:
        group_type = "compact_abelian"
    elif _matches_any(tags, LC_GROUP_TAGS) and is_abelian_v:
        group_type = "locally_compact_abelian"
    elif is_compact_v or _matches_any(tags, COMPACT_GROUP_TAGS):
        group_type = "compact"
    else:
        group_type = "general"

    key_properties: list[str] = ["topological_group"]
    if sep_r.is_true:
        key_properties.append("tychonoff")
    if is_compact_v:
        key_properties.append("compact")
    if is_abelian_v:
        key_properties.append("abelian")
    if is_discrete_v:
        key_properties.append("discrete")
    if _matches_any(tags, LIE_GROUP_TAGS):
        key_properties.append("lie")
    if _matches_any(tags, PROFINITE_TAGS):
        key_properties.append("profinite")

    return {
        "group_type": group_type,
        "is_topological_group": grp_r,
        "is_compact": is_compact_v,
        "is_abelian": is_abelian_v,
        "is_discrete": is_discrete_v,
        "separation": sep_r,
        "key_properties": key_properties,
    }


def topological_group_profile(space: Any) -> dict[str, Any]:
    """Full topological group profile combining classification and named registry.

    Keys
    ----
    classification : dict
        Output of :func:`classify_topological_group`.
    named_profiles : tuple[TopologicalGroupProfile, ...]
        Registry of well-known topological group families.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_topological_group(space),
        "named_profiles": get_named_topological_group_profiles(),
        "layer_summary": topological_group_layer_summary(),
    }


__all__ = [
    "TopologicalGroupProfile",
    "GROUP_POSITIVE_TAGS",
    "GROUP_NEGATIVE_TAGS",
    "CONTINUOUS_OP_TAGS",
    "LIE_GROUP_TAGS",
    "PROFINITE_TAGS",
    "COMPACT_GROUP_TAGS",
    "LC_GROUP_TAGS",
    "LOCALLY_COMPACT_TAGS",
    "ABELIAN_TAGS",
    "DISCRETE_GROUP_TAGS",
    "get_named_topological_group_profiles",
    "topological_group_layer_summary",
    "topological_group_type_index",
    "is_topological_group",
    "topological_group_separation",
    "classify_topological_group",
    "topological_group_profile",
]
