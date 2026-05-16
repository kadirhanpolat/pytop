"""Hyperspaces: Vietoris topology, Hausdorff metric, and K(X) theory.

Key theorems implemented
------------------------
- Hausdorff metric: if (X, d) is a metric space, K(X) = {non-empty compact subsets}
  with d_H(A, B) = max(sup_{a∈A} d(a,B), sup_{b∈B} d(b,A)) is a metric space.
- Blaschke Selection theorem: K(X) is compact iff X is compact metrizable.
- K(X) Polish theorem: if X is a Polish space then K(X) (with the Hausdorff metric)
  is also a Polish space.
- Vietoris topology: the hyperspace 2^X of non-empty closed subsets with the
  Vietoris (finite) topology is compact iff X is compact.
- Curtis-Schori-West theorem: K([0,1]) is homeomorphic to the Hilbert cube [0,1]^ω.
- Cantor hyperspace: K(C) (C = Cantor set) is homeomorphic to C itself.
- A hyperspace K(X) is connected iff X is connected.
- In a Polish space, the closed sets of measure zero form a co-analytic set in 2^X.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class HyperspaceProfile:
    """A curated hyperspace example."""

    key: str
    display_name: str
    hyperspace_type: str
    base_space_class: str
    is_compact: bool
    is_polish: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

COMPACT_METRIZABLE_TAGS: set[str] = {
    "compact_metrizable", "compact_metric",
    "compact", "compact_hausdorff", "compact_t2",
    "cantor_set", "cantor_space",
    "closed_interval", "closed_ball",
    "finite_space",
}
POLISH_BASE_TAGS: set[str] = {
    "polish_space", "polish",
    "completely_metrizable", "completely_metrizable_space",
    "compact_metrizable", "compact_metric",
    "cantor_set", "irrationals",
    "banach_space", "hilbert_space", "frechet_space",
}
LOCALLY_COMPACT_METRIZABLE_TAGS: set[str] = {
    "locally_compact_metrizable", "locally_compact_metric",
    "locally_compact_hausdorff_metrizable",
    "real_line", "reals", "euclidean",
    "locally_compact_polish",
}
METRIZABLE_BASE_TAGS: set[str] = {
    "metric", "metrizable",
    "completely_metrizable", "polish_space",
    "compact_metrizable", "compact_metric",
}
CONNECTED_BASE_TAGS: set[str] = {
    "connected", "path_connected", "locally_path_connected",
    "continuum", "interval", "disk",
    "closed_interval", "real_line", "reals",
}
HAUSDORFF_METRIC_TAGS: set[str] = {
    "metric", "metrizable",
    "compact_metrizable", "compact_metric",
    "polish_space", "completely_metrizable",
    "locally_compact_metrizable",
    "real_line", "reals", "euclidean",
}
NOT_HYPERSPACE_COMPACT_TAGS: set[str] = {
    "non_compact", "not_compact",
    "real_line", "reals", "euclidean",
    "irrationals", "polish_not_compact",
    "locally_compact_not_compact",
}
VIETORIS_COMPACT_TAGS: set[str] = {
    "compact", "compact_hausdorff", "compact_t2",
    "compact_metrizable", "compact_metric",
    "cantor_set", "closed_interval",
}


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
# Named example registry
# ---------------------------------------------------------------------------

def get_named_hyperspace_profiles() -> tuple[HyperspaceProfile, ...]:
    """Return the registry of canonical hyperspace examples."""
    return (
        HyperspaceProfile(
            key="k_closed_interval",
            display_name="K([0,1]) — hyperspace of the closed unit interval",
            hyperspace_type="compact_polish",
            base_space_class="compact_metrizable",
            is_compact=True,
            is_polish=True,
            presentation_layer="main_text",
            focus=(
                "K([0,1]) with the Hausdorff metric is both compact and Polish. "
                "The Blaschke selection theorem guarantees compactness: any sequence of "
                "compact subsets of [0,1] has a convergent subsequence. "
                "The Curtis-Schori-West theorem shows K([0,1]) is homeomorphic to the "
                "Hilbert cube [0,1]^omega — a remarkable infinite-dimensional compactum. "
                "Since [0,1] is connected, K([0,1]) is also connected."
            ),
            chapter_targets=("4", "27"),
        ),
        HyperspaceProfile(
            key="k_cantor",
            display_name="K(C) — hyperspace of the Cantor set",
            hyperspace_type="compact_zero_dimensional",
            base_space_class="compact_metrizable",
            is_compact=True,
            is_polish=True,
            presentation_layer="main_text",
            focus=(
                "K(C) with the Hausdorff metric is compact and Polish. "
                "Remarkably, K(C) is homeomorphic to C itself — the Cantor set. "
                "This follows because C is the universal compact metrizable "
                "zero-dimensional space, and K(C) is also compact, metrizable, and "
                "zero-dimensional. Since C is totally disconnected, K(C) is also "
                "totally disconnected (hyperspace connectedness mirrors base space)."
            ),
            chapter_targets=("4", "27"),
        ),
        HyperspaceProfile(
            key="k_real_line",
            display_name="K(R) — hyperspace of the real line",
            hyperspace_type="polish_not_compact",
            base_space_class="locally_compact_polish",
            is_compact=False,
            is_polish=True,
            presentation_layer="selected_block",
            focus=(
                "K(R) (non-empty compact subsets of R with the Hausdorff metric) is "
                "Polish but NOT compact: the sequence {[n, n+1]} has no convergent "
                "subsequence in K(R). The Hausdorff metric is well-defined since R is "
                "a metric space and compacts are bounded. K(R) is completely metrizable "
                "and separable (countable dense subsets: finite sets with rational endpoints). "
                "K(R) is connected since R is connected."
            ),
            chapter_targets=("4", "27"),
        ),
        HyperspaceProfile(
            key="vietoris_compact",
            display_name="2^X (Vietoris topology) for compact X",
            hyperspace_type="compact_vietoris",
            base_space_class="compact",
            is_compact=True,
            is_polish=False,
            presentation_layer="selected_block",
            focus=(
                "The hyperspace 2^X of all non-empty closed subsets of a compact "
                "space X, equipped with the Vietoris (finite) topology, is compact. "
                "The Vietoris topology is generated by sets of the form {A : A ∩ U ≠ ∅} "
                "and {A : A ⊆ U} for open U ⊆ X. When X is compact metrizable, "
                "the Vietoris topology coincides with the Hausdorff metric topology on K(X). "
                "For non-metrizable compact X, 2^X may not be metrizable."
            ),
            chapter_targets=("4", "9"),
        ),
        HyperspaceProfile(
            key="k_polish_space",
            display_name="K(X) for Polish X — Polish hyperspace",
            hyperspace_type="polish",
            base_space_class="polish",
            is_compact=False,
            is_polish=True,
            presentation_layer="advanced_note",
            focus=(
                "For any Polish space X, K(X) with the Hausdorff metric is also a "
                "Polish space. The Hausdorff metric makes K(X) a completely metrizable "
                "separable space. This is the content of the K(X) Polish theorem. "
                "Moreover, the map X → K(X), x ↦ {x}, is an isometric embedding. "
                "The subspace F(X) of all closed subsets (with the Wijsman or Fell topology) "
                "extends this to a larger hyperspace, important in descriptive set theory."
            ),
            chapter_targets=("4", "27", "52"),
        ),
    )


def hyperspace_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_hyperspace_profiles()))


def hyperspace_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_hyperspace_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def hyperspace_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from hyperspace_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_hyperspace_profiles():
        index.setdefault(p.hyperspace_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def hausdorff_metric_applicable(space: Any) -> Result:
    """Check whether the Hausdorff metric can be defined on K(space).

    The Hausdorff metric d_H(A, B) = max(sup_{a∈A} d(a,B), sup_{b∈B} d(b,A))
    is defined on the collection K(X) of non-empty compact subsets of a metric
    space (X, d). Key facts:
    - Requires X to be metrizable (to have a compatible metric).
    - The Hausdorff metric makes K(X) into a metric space.
    - If X is complete, K(X) is complete under d_H.
    - If X is Polish, K(X) is Polish (completely metrizable + separable).

    Decision layers
    ---------------
    1. Polish space → true (Polish implies completely metrizable metric space).
    2. Compact metrizable → true.
    3. Locally compact metrizable → true.
    4. Direct metrizable tags → true.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, POLISH_BASE_TAGS):
        witness = next(t for t in tags if t in POLISH_BASE_TAGS)
        return Result.true(
            mode="theorem",
            value="hausdorff_metric_applicable",
            justification=[
                f"Tag {witness!r}: Polish spaces are completely metrizable, so the "
                "Hausdorff metric d_H is defined on K(X). The resulting K(X) is "
                "itself a Polish space.",
            ],
            metadata={**base, "criterion": "polish", "witness": witness},
        )

    if _matches_any(tags, COMPACT_METRIZABLE_TAGS) and _matches_any(
        tags, {"metric", "metrizable", "compact_metrizable"}
    ):
        witness = next(t for t in tags if t in COMPACT_METRIZABLE_TAGS)
        return Result.true(
            mode="theorem",
            value="hausdorff_metric_applicable",
            justification=[
                f"Tag {witness!r}: compact metrizable spaces carry a compatible metric, "
                "so the Hausdorff metric is defined on K(X). "
                "By the Blaschke selection theorem, K(X) is compact.",
            ],
            metadata={**base, "criterion": "compact_metrizable", "witness": witness},
        )

    if _matches_any(tags, LOCALLY_COMPACT_METRIZABLE_TAGS):
        witness = next(t for t in tags if t in LOCALLY_COMPACT_METRIZABLE_TAGS)
        return Result.true(
            mode="theorem",
            value="hausdorff_metric_applicable",
            justification=[
                f"Tag {witness!r}: locally compact metrizable spaces carry a compatible "
                "metric, so the Hausdorff metric is defined on K(X). "
                "K(X) is a Polish space if X is locally compact Polish.",
            ],
            metadata={**base, "criterion": "locally_compact_metrizable", "witness": witness},
        )

    if _matches_any(tags, HAUSDORFF_METRIC_TAGS):
        witness = next(t for t in tags if t in HAUSDORFF_METRIC_TAGS)
        return Result.true(
            mode="theorem",
            value="hausdorff_metric_applicable",
            justification=[
                f"Tag {witness!r}: the Hausdorff metric is defined on K(X) for any "
                "metric space (X, d).",
            ],
            metadata={**base, "criterion": "metrizable", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="hausdorff_metric_applicable",
        justification=[
            "Insufficient tags to determine Hausdorff metric applicability. "
            "Supply tags such as 'metric', 'metrizable', 'polish_space', "
            "'compact_metrizable', or 'real_line'.",
        ],
        metadata={**base, "criterion": None},
    )


def hyperspace_is_compact(space: Any) -> Result:
    """Check whether K(space) is compact (Blaschke selection theorem).

    The Blaschke selection theorem: K(X) with the Hausdorff metric is compact
    if and only if X is compact metrizable. Key facts:
    - K([0,1]) is compact (and homeomorphic to the Hilbert cube [0,1]^omega).
    - K(R) is NOT compact (R is not compact).
    - For non-compact X, K(X) is still Polish if X is Polish.
    - For compact X, every sequence in K(X) has a convergent subsequence.

    Decision layers
    ---------------
    1. Explicit non-compact base → false.
    2. Compact metrizable → true (Blaschke).
    3. Vietoris topology on compact → true.
    4. Compact (not necessarily metrizable) → unknown for Hausdorff metric.
    5. Polish but not compact → false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, NOT_HYPERSPACE_COMPACT_TAGS):
        blocking = next(t for t in tags if t in NOT_HYPERSPACE_COMPACT_TAGS)
        return Result.false(
            mode="theorem",
            value="hyperspace_compact",
            justification=[
                f"Tag {blocking!r}: K(X) is compact iff X is compact. "
                "The base space is not compact, so K(X) is not compact. "
                "(Blaschke selection theorem: compactness of K(X) ↔ compactness of X.)",
            ],
            metadata={**base, "criterion": "not_compact_base"},
        )

    if _matches_any(tags, {"compact_metrizable", "compact_metric"}):
        witness = next(t for t in tags if t in {"compact_metrizable", "compact_metric"})
        return Result.true(
            mode="theorem",
            value="hyperspace_compact",
            justification=[
                f"Tag {witness!r}: by the Blaschke selection theorem, K(X) is compact "
                "when X is compact metrizable. Every sequence of compact subsets has "
                "a subsequence convergent in the Hausdorff metric.",
            ],
            metadata={**base, "criterion": "blaschke", "witness": witness},
        )

    if _matches_any(tags, VIETORIS_COMPACT_TAGS) and _matches_any(
        tags, {"metric", "metrizable", "compact_metrizable"}
    ):
        witness = next(t for t in tags if t in VIETORIS_COMPACT_TAGS)
        return Result.true(
            mode="theorem",
            value="hyperspace_compact",
            justification=[
                f"Tag {witness!r}: compact metrizable space; K(X) is compact "
                "by the Blaschke selection theorem.",
            ],
            metadata={**base, "criterion": "blaschke_vietoris", "witness": witness},
        )

    if _matches_any(tags, {"cantor_set", "cantor_space", "closed_interval"}):
        witness = next(t for t in tags if t in {"cantor_set", "cantor_space", "closed_interval"})
        return Result.true(
            mode="theorem",
            value="hyperspace_compact",
            justification=[
                f"Tag {witness!r}: K(C) is compact since C is compact metrizable. "
                "Notably K(Cantor set) is homeomorphic to the Cantor set itself.",
            ],
            metadata={**base, "criterion": "blaschke_canonical", "witness": witness},
        )

    if _matches_any(tags, POLISH_BASE_TAGS) and not _matches_any(
        tags, {"compact", "compact_metrizable", "compact_hausdorff"}
    ):
        return Result.false(
            mode="theorem",
            value="hyperspace_compact",
            justification=[
                "Polish but non-compact base space: K(X) is Polish (completely "
                "metrizable and separable) but NOT compact. "
                "Compactness of K(X) requires compactness of X.",
            ],
            metadata={**base, "criterion": "polish_not_compact"},
        )

    return Result.unknown(
        mode="symbolic",
        value="hyperspace_compact",
        justification=[
            "Insufficient tags to determine compactness of K(X). "
            "Supply tags such as 'compact_metrizable', 'cantor_set', 'closed_interval', "
            "'real_line' (not compact), or 'polish_space'.",
        ],
        metadata={**base, "criterion": None},
    )


def hyperspace_is_polish(space: Any) -> Result:
    """Check whether K(space) is a Polish space (K(X) Polish theorem).

    If X is a Polish space, then K(X) with the Hausdorff metric is also Polish.
    Key facts:
    - K(X) Polish ↔ X Polish (for metrizable X).
    - K([0,1]) is Polish (compact metrizable → compact Polish).
    - K(R) is Polish (locally compact Polish).
    - K(C) is Polish (Cantor set is compact Polish).
    - The Hausdorff metric makes K(X) completely metrizable when X is.

    Decision layers
    ---------------
    1. Compact metrizable → true (compact metrizable is Polish; K(X) inherits).
    2. Polish (completely metrizable + separable) → true.
    3. Locally compact metrizable → true (locally compact Polish → K(X) Polish).
    4. Completely metrizable (without separability info) → unknown.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"compact_metrizable", "compact_metric", "cantor_set",
                            "cantor_space", "closed_interval"}):
        witness = next(t for t in tags if t in {"compact_metrizable", "compact_metric",
                                                  "cantor_set", "cantor_space", "closed_interval"})
        return Result.true(
            mode="theorem",
            value="hyperspace_polish",
            justification=[
                f"Tag {witness!r}: compact metrizable spaces are Polish (complete + separable). "
                "By the K(X) Polish theorem, K(X) is also Polish.",
            ],
            metadata={**base, "criterion": "compact_metrizable", "witness": witness},
        )

    if _matches_any(tags, POLISH_BASE_TAGS):
        witness = next(t for t in tags if t in POLISH_BASE_TAGS)
        return Result.true(
            mode="theorem",
            value="hyperspace_polish",
            justification=[
                f"Tag {witness!r}: by the K(X) Polish theorem, K(X) with the Hausdorff "
                "metric is a Polish space whenever X is Polish. The Hausdorff metric "
                "makes K(X) completely metrizable and separable.",
            ],
            metadata={**base, "criterion": "polish", "witness": witness},
        )

    if _matches_any(tags, LOCALLY_COMPACT_METRIZABLE_TAGS):
        witness = next(t for t in tags if t in LOCALLY_COMPACT_METRIZABLE_TAGS)
        return Result.true(
            mode="theorem",
            value="hyperspace_polish",
            justification=[
                f"Tag {witness!r}: locally compact Polish spaces (like R) have Polish "
                "hyperspace K(X): the Hausdorff metric is complete and K(X) is separable.",
            ],
            metadata={**base, "criterion": "locally_compact_polish", "witness": witness},
        )

    if _matches_any(tags, {"completely_metrizable", "completely_metrizable_space"}):
        witness = next(t for t in tags if t in {"completely_metrizable", "completely_metrizable_space"})
        return Result.true(
            mode="theorem",
            value="hyperspace_polish",
            justification=[
                f"Tag {witness!r}: if X is completely metrizable, K(X) is completely "
                "metrizable under the Hausdorff metric. If X is also separable (Polish), "
                "K(X) is Polish.",
            ],
            metadata={**base, "criterion": "completely_metrizable", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="hyperspace_polish",
        justification=[
            "Insufficient tags to determine whether K(X) is Polish. "
            "Supply tags such as 'polish_space', 'compact_metrizable', "
            "'completely_metrizable', or 'real_line'.",
        ],
        metadata={**base, "criterion": None},
    )


def vietoris_topology_hausdorff(space: Any) -> Result:
    """Check whether the Vietoris hyperspace 2^X is Hausdorff.

    The Vietoris topology on 2^X (non-empty closed subsets) is generated by sets
    of the form {A : A ∩ U ≠ ∅} and {A : A ⊆ U} for open U ⊆ X. Key facts:
    - 2^X with the Vietoris topology is Hausdorff iff X is Hausdorff.
    - When X is compact metrizable, the Vietoris topology = Hausdorff metric topology.
    - For compact X, 2^X is compact (Tychonoff-type argument on the Vietoris topology).
    - The subspace K(X) ⊆ 2^X of compact subsets inherits the Hausdorff property.

    Decision layers
    ---------------
    1. Hausdorff / T2 base → true.
    2. Metric or metrizable (implies Hausdorff) → true.
    3. Compact Hausdorff → true.
    4. T1 but not T2 known → false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"hausdorff", "t2", "regular", "t3", "normal", "t4",
                            "metric", "metrizable", "compact_hausdorff",
                            "compact_t2", "polish_space", "compact_metrizable"}):
        witness = next(t for t in tags if t in {"hausdorff", "t2", "regular", "t3",
                                                  "normal", "t4", "metric", "metrizable",
                                                  "compact_hausdorff", "compact_t2",
                                                  "polish_space", "compact_metrizable"})
        return Result.true(
            mode="theorem",
            value="vietoris_hausdorff",
            justification=[
                f"Tag {witness!r}: the Vietoris hyperspace 2^X is Hausdorff iff X is "
                "Hausdorff. Since X is Hausdorff (T2), singletons are closed and distinct "
                "compact sets can be separated by Vietoris open sets.",
            ],
            metadata={**base, "criterion": "hausdorff_base", "witness": witness},
        )

    if _matches_any(tags, {"t1", "t1_space"}) and not _matches_any(
        tags, {"hausdorff", "t2", "metric", "metrizable"}
    ):
        return Result.false(
            mode="theorem",
            value="vietoris_hausdorff",
            justification=[
                "T1 but non-Hausdorff base: the Vietoris hyperspace 2^X is Hausdorff "
                "only when X is Hausdorff. A T1 non-T2 space yields a non-Hausdorff 2^X.",
            ],
            metadata={**base, "criterion": "t1_not_t2"},
        )

    return Result.unknown(
        mode="symbolic",
        value="vietoris_hausdorff",
        justification=[
            "Insufficient tags to determine whether the Vietoris hyperspace is Hausdorff. "
            "Supply tags such as 'hausdorff', 't2', 'metric', 'metrizable', or 't1'.",
        ],
        metadata={**base, "criterion": None},
    )


def hyperspace_is_connected(space: Any) -> Result:
    """Check whether K(space) is connected (mirror theorem).

    K(X) is connected iff X is connected. More specifically:
    - X connected → K(X) connected (singletons form a connected path in K(X)).
    - X disconnected → K(X) disconnected (K(A) and K(B) separate K(X) when X = A ∪ B).
    - The map x ↦ {x} embeds X into K(X) as a retract, preserving connectedness.

    Decision layers
    ---------------
    1. Connected / path-connected base → true.
    2. Totally disconnected → false.
    3. Disconnected → false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, CONNECTED_BASE_TAGS):
        witness = next(t for t in tags if t in CONNECTED_BASE_TAGS)
        return Result.true(
            mode="theorem",
            value="hyperspace_connected",
            justification=[
                f"Tag {witness!r}: K(X) is connected iff X is connected. "
                "The map x ↦ {{x}} embeds X into K(X), so connectedness is inherited. "
                "Moreover, K(X) is arcwise connected when X is compact connected.",
            ],
            metadata={**base, "criterion": "connected_base", "witness": witness},
        )

    if _matches_any(tags, {"totally_disconnected", "zero_dimensional",
                            "cantor_set", "cantor_space", "profinite",
                            "discrete", "disconnected"}):
        blocking = next(t for t in tags if t in {"totally_disconnected", "zero_dimensional",
                                                   "cantor_set", "cantor_space", "profinite",
                                                   "discrete", "disconnected"})
        return Result.false(
            mode="theorem",
            value="hyperspace_connected",
            justification=[
                f"Tag {blocking!r}: K(X) is disconnected when X is totally disconnected "
                "or disconnected. The compact subsets of a totally disconnected space are "
                "themselves totally disconnected — so K(X) is not connected.",
            ],
            metadata={**base, "criterion": "disconnected_base"},
        )

    return Result.unknown(
        mode="symbolic",
        value="hyperspace_connected",
        justification=[
            "Insufficient tags to determine connectedness of K(X). "
            "Supply tags such as 'connected', 'path_connected', 'totally_disconnected', "
            "or 'disconnected'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_hyperspace(space: Any) -> dict[str, Any]:
    """Classify the hyperspace K(space) by its topological properties.

    Keys
    ----
    hyperspace_type : str
        One of ``"compact_polish"``, ``"polish"``, ``"compact"``,
        ``"metrizable"``, ``"unknown"``.
    hausdorff_metric : Result
    is_compact : Result
    is_polish : Result
    vietoris_hausdorff : Result
    is_connected : Result
    key_properties : list[str]
    representation : str
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    hm_r = hausdorff_metric_applicable(space)
    comp_r = hyperspace_is_compact(space)
    pol_r = hyperspace_is_polish(space)
    viet_r = vietoris_topology_hausdorff(space)
    conn_r = hyperspace_is_connected(space)

    if comp_r.is_true and pol_r.is_true:
        hyperspace_type = "compact_polish"
    elif pol_r.is_true and comp_r.is_false:
        hyperspace_type = "polish"
    elif comp_r.is_true:
        hyperspace_type = "compact"
    elif hm_r.is_true:
        hyperspace_type = "metrizable"
    else:
        hyperspace_type = "unknown"

    key_properties: list[str] = []
    if hm_r.is_true:
        key_properties.append("hausdorff_metric")
    if comp_r.is_true:
        key_properties.append("compact")
    if pol_r.is_true:
        key_properties.append("polish")
    if viet_r.is_true:
        key_properties.append("vietoris_hausdorff")
    if conn_r.is_true:
        key_properties.append("connected")
    if conn_r.is_false:
        key_properties.append("disconnected")

    return {
        "hyperspace_type": hyperspace_type,
        "hausdorff_metric": hm_r,
        "is_compact": comp_r,
        "is_polish": pol_r,
        "vietoris_hausdorff": viet_r,
        "is_connected": conn_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def hyperspace_profile(space: Any) -> dict[str, Any]:
    """Full hyperspace profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_hyperspace`.
    named_profiles : tuple[HyperspaceProfile, ...]
        Registry of canonical hyperspace examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_hyperspace(space),
        "named_profiles": get_named_hyperspace_profiles(),
        "layer_summary": hyperspace_layer_summary(),
    }


__all__ = [
    "HyperspaceProfile",
    "COMPACT_METRIZABLE_TAGS",
    "POLISH_BASE_TAGS",
    "LOCALLY_COMPACT_METRIZABLE_TAGS",
    "METRIZABLE_BASE_TAGS",
    "CONNECTED_BASE_TAGS",
    "HAUSDORFF_METRIC_TAGS",
    "NOT_HYPERSPACE_COMPACT_TAGS",
    "VIETORIS_COMPACT_TAGS",
    "get_named_hyperspace_profiles",
    "hyperspace_layer_summary",
    "hyperspace_chapter_index",
    "hyperspace_type_index",
    "hausdorff_metric_applicable",
    "hyperspace_is_compact",
    "hyperspace_is_polish",
    "vietoris_topology_hausdorff",
    "hyperspace_is_connected",
    "classify_hyperspace",
    "hyperspace_profile",
]
