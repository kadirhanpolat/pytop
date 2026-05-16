"""Descriptive set theory: Borel hierarchy, Baire property, and perfect sets.

Key theorems implemented
------------------------
- Alexandrov's Theorem: A metrizable space is completely metrizable iff it is
  a G_delta in any (equivalently, in its own) metric completion.
- Closed sets in metrizable spaces are G_delta (via distance functions).
- Open sets in metrizable spaces are F_sigma (complement of closed = G_delta).
- Borel sets (G_delta, F_sigma, G_delta_sigma, ...) all have the Baire property.
- Cantor-Bendixson Theorem: every closed set F in a Polish space decomposes
  as F = P ∪ C where P is perfect and C is countable (and open in F).
- A countable T1 space is scattered (every subspace has an isolated point).
- The irrationals are G_delta in R and form a perfect, completely metrizable space.
- Q is F_sigma in R but NOT G_delta (if it were, it would be comeager,
  contradicting the Baire Category Theorem).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class DescriptiveSetProfile:
    """A curated descriptive set theory example."""

    key: str
    display_name: str
    borel_class: str
    has_baire_property: bool
    is_perfect: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

G_DELTA_TAGS: set[str] = {
    "g_delta", "open", "g_delta_set",
    "completely_metrizable", "completely_metrizable_space",
    "polish_space", "polish",
    "irrationals", "baire_space_omega",
    "closed_metrizable",
}
F_SIGMA_TAGS: set[str] = {
    "f_sigma", "closed", "f_sigma_set",
    "sigma_compact", "countable_t1",
    "rationals_like", "rationals",
    "open_metrizable",
}
PERFECT_SET_TAGS: set[str] = {
    "perfect_set", "perfect_space", "perfect",
    "cantor_set", "cantor_space",
    "irrationals", "no_isolated_points_closed",
}
SCATTERED_TAGS: set[str] = {
    "scattered", "scattered_space",
    "countable_ordinal", "successor_ordinal_space",
    "well_ordered_discrete",
}
BAIRE_PROPERTY_TAGS: set[str] = {
    "open", "closed",
    "g_delta", "f_sigma",
    "g_delta_sigma", "f_sigma_delta",
    "borel", "borel_set", "analytic", "analytic_set",
    "meager", "comeager", "residual",
    "complete_metric", "completely_metrizable", "polish_space",
    "metric", "metrizable",
}
BOREL_NEGATIVE_TAGS: set[str] = {
    "non_borel", "not_borel", "non_measurable",
    "bernstein_set", "vitali_set",
}
G_DELTA_NEGATIVE_TAGS: set[str] = {
    "not_g_delta", "rationals_like", "rationals",
    "f_sigma_not_g_delta",
}
CLOSED_IN_METRIZABLE_TAGS: set[str] = {
    "closed_metrizable", "closed_in_polish",
    "compact", "compact_hausdorff", "compact_t2",
    "cantor_set", "perfect_set",
}
OPEN_IN_METRIZABLE_TAGS: set[str] = {
    "open_metrizable", "open_in_polish",
    "open", "open_subspace",
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

def get_named_descriptive_profiles() -> tuple[DescriptiveSetProfile, ...]:
    """Return the registry of canonical descriptive set theory examples."""
    return (
        DescriptiveSetProfile(
            key="irrationals_g_delta",
            display_name="Irrationals in R (G_delta, perfect, Polish)",
            borel_class="g_delta",
            has_baire_property=True,
            is_perfect=True,
            presentation_layer="main_text",
            focus=(
                "The irrationals R \\ Q are a G_delta in R: they equal the "
                "intersection of dense open sets R \\ {q} for each q in Q. "
                "By Alexandrov's theorem, the irrationals are completely metrizable "
                "(homeomorphic to Baire space omega^omega) and hence a Baire space. "
                "They form a perfect space (closed in themselves, no isolated points)."
            ),
            chapter_targets=("27", "52"),
        ),
        DescriptiveSetProfile(
            key="rationals_f_sigma",
            display_name="Rationals Q in R (F_sigma, meager, NOT G_delta)",
            borel_class="f_sigma",
            has_baire_property=True,
            is_perfect=False,
            presentation_layer="main_text",
            focus=(
                "Q is F_sigma in R: it equals the countable union of closed singletons "
                "{q} for q in Q. By the Baire Category Theorem, Q is NOT G_delta in R: "
                "if it were, Q would be a comeager G_delta in a Baire space, "
                "contradicting Q being meager (each {q} is nowhere dense)."
            ),
            chapter_targets=("27", "48"),
        ),
        DescriptiveSetProfile(
            key="cantor_set_perfect",
            display_name="Cantor set C (perfect, compact, G_delta)",
            borel_class="g_delta",
            has_baire_property=True,
            is_perfect=True,
            presentation_layer="selected_block",
            focus=(
                "The Cantor set is closed in R (hence F_sigma and G_delta in a "
                "metric space) and perfect: it is closed with no isolated points. "
                "Homeomorphic to 2^omega, it is compact, totally disconnected, "
                "and the universal compact metrizable zero-dimensional space. "
                "Every perfect Polish space contains a homeomorphic copy of C."
            ),
            chapter_targets=("27", "45"),
        ),
        DescriptiveSetProfile(
            key="open_interval_g_delta_f_sigma",
            display_name="Open interval (a,b) in R (G_delta and F_sigma)",
            borel_class="g_delta",
            has_baire_property=True,
            is_perfect=True,
            presentation_layer="selected_block",
            focus=(
                "Every open set in a metric space is trivially G_delta (it equals "
                "the intersection of itself with itself). In a metrizable space, "
                "opens are also F_sigma: (a,b) = union of [a+1/n, b-1/n] for n large. "
                "Open intervals in R are perfect (no isolated points) and Baire."
            ),
            chapter_targets=("27", "32"),
        ),
        DescriptiveSetProfile(
            key="countable_scattered_ordinal",
            display_name="Countable successor ordinal omega+1 (scattered, F_sigma)",
            borel_class="f_sigma",
            has_baire_property=True,
            is_perfect=False,
            presentation_layer="advanced_note",
            focus=(
                "The ordinal space omega+1 = {0,1,2,...,omega} with the order topology "
                "is compact, countable, and scattered: every non-empty subspace has an "
                "isolated point. Its Cantor-Bendixson rank is 1 (the derived set is "
                "{omega}, which is isolated from below). Scattered countable spaces "
                "are never perfect."
            ),
            chapter_targets=("27", "52"),
        ),
    )


def descriptive_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_descriptive_profiles()))


def descriptive_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_descriptive_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def descriptive_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from borel_class to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_descriptive_profiles():
        index.setdefault(p.borel_class, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_g_delta(space: Any) -> Result:
    """Check whether the space is (or represents) a G_delta set.

    A G_delta is a countable intersection of open sets. Key facts:
    - Open sets are G_delta (trivially).
    - Closed sets in metrizable spaces are G_delta (via distance-to-set functions).
    - Completely metrizable spaces are G_delta in any metric completion (Alexandrov).
    - Q is NOT G_delta in R (would be comeager, contradicting BCT).

    Decision layers
    ---------------
    1. Explicit not-G_delta tags → false.
    2. Direct G_delta / open tags → true.
    3. Completely metrizable / Polish → true (Alexandrov's theorem).
    4. Closed in metrizable space → true (G_delta via distance function).
    5. F_sigma-but-not-G_delta (rationals-like) → false (BCT argument).
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, G_DELTA_NEGATIVE_TAGS):
        blocking = next(t for t in tags if t in G_DELTA_NEGATIVE_TAGS)
        return Result.false(
            mode="theorem",
            value="g_delta",
            justification=[
                f"Tag {blocking!r}: this space is not G_delta. "
                "If Q ⊆ R were G_delta, it would be comeager in R, "
                "contradicting the Baire Category Theorem (Q is meager).",
            ],
            metadata={**base, "criterion": None},
        )

    if _matches_any(tags, {"g_delta", "g_delta_set", "open", "open_subspace", "irrationals", "baire_space_omega"}):
        witness = next(t for t in tags if t in {"g_delta", "g_delta_set", "open", "open_subspace", "irrationals", "baire_space_omega"})
        return Result.true(
            mode="theorem",
            value="g_delta",
            justification=[f"Tag {witness!r}: the space is directly tagged as a G_delta set."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    if _matches_any(tags, {"completely_metrizable", "completely_metrizable_space", "polish_space", "polish"}):
        witness = next(t for t in tags if t in {"completely_metrizable", "completely_metrizable_space", "polish_space", "polish"})
        return Result.true(
            mode="theorem",
            value="g_delta",
            justification=[
                f"Tag {witness!r}: by Alexandrov's theorem, a metrizable space is "
                "completely metrizable if and only if it is a G_delta in its metric "
                "completion (and in any complete metric space it embeds into densely).",
            ],
            metadata={**base, "criterion": "alexandrov", "witness": witness},
        )

    if _matches_any(tags, CLOSED_IN_METRIZABLE_TAGS) and _matches_any(tags, {"metric", "metrizable", "metric_space"}):
        witness = next(t for t in tags if t in CLOSED_IN_METRIZABLE_TAGS)
        return Result.true(
            mode="theorem",
            value="g_delta",
            justification=[
                f"Tag {witness!r} in a metrizable space: every closed set C is G_delta "
                "via C = intersection{{x : d(x,C) < 1/n}} for n = 1, 2, ...",
            ],
            metadata={**base, "criterion": "closed_in_metrizable", "witness": witness},
        )

    if _matches_any(tags, CLOSED_IN_METRIZABLE_TAGS) and _matches_any(
        tags, {"compact_hausdorff", "compact_t2", "cantor_set", "compact"}
    ):
        witness = next(t for t in tags if t in CLOSED_IN_METRIZABLE_TAGS | {"compact_hausdorff", "compact_t2", "cantor_set"})
        return Result.true(
            mode="theorem",
            value="g_delta",
            justification=[
                f"Tag {witness!r}: compact metrizable spaces are completely metrizable "
                "(compact + metrizable → completely metrizable), hence G_delta in their completions.",
            ],
            metadata={**base, "criterion": "compact_metrizable", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="g_delta",
        justification=[
            "Insufficient tags to determine G_delta status. "
            "Supply tags such as 'g_delta', 'open', 'completely_metrizable', "
            "'polish_space', or 'closed_metrizable'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_f_sigma(space: Any) -> Result:
    """Check whether the space is (or represents) an F_sigma set.

    An F_sigma is a countable union of closed sets. Key facts:
    - Closed sets are F_sigma (trivially: a single closed set is a finite union).
    - Open sets in metrizable spaces are F_sigma (complement of a G_delta).
    - Sigma-compact spaces are F_sigma (countable union of compact = closed sets).
    - Countable T1 spaces are F_sigma (countable union of closed singletons).
    - Q is F_sigma in R (union of all {q}).

    Decision layers
    ---------------
    1. Direct F_sigma / closed tags → true.
    2. Open in metrizable → true (open is G_delta's complement = F_sigma's dual).
    3. Sigma-compact → true (countable union of compact ⊆ closed sets).
    4. Countable T1 space → true (union of closed singletons).
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, {"f_sigma", "f_sigma_set", "closed", "rationals", "rationals_like", "countable_t1"}):
        witness = next(t for t in tags if t in {"f_sigma", "f_sigma_set", "closed", "rationals", "rationals_like", "countable_t1"})
        return Result.true(
            mode="theorem",
            value="f_sigma",
            justification=[f"Tag {witness!r}: the space is directly tagged as an F_sigma set."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    if _matches_any(tags, {"open", "open_subspace", "open_metrizable"}) and _matches_any(
        tags, {"metric", "metrizable", "metric_space", "polish_space", "completely_metrizable"}
    ):
        witness = next(t for t in tags if t in {"open", "open_subspace", "open_metrizable"})
        return Result.true(
            mode="theorem",
            value="f_sigma",
            justification=[
                f"Tag {witness!r} in a metrizable space: every open set G is F_sigma "
                "because G^c is closed (= G_delta in metrizable), so G is F_sigma.",
            ],
            metadata={**base, "criterion": "open_in_metrizable", "witness": witness},
        )

    if _matches_any(tags, {"sigma_compact", "sigma_compact_space"}):
        witness = next(t for t in tags if t in {"sigma_compact", "sigma_compact_space"})
        return Result.true(
            mode="theorem",
            value="f_sigma",
            justification=[
                f"Tag {witness!r}: sigma-compact means X = union of compact sets K_n. "
                "In a Hausdorff space, compact sets are closed, so X is F_sigma.",
            ],
            metadata={**base, "criterion": "sigma_compact", "witness": witness},
        )

    if _matches_any(tags, {"countable", "countably_infinite", "omega"}) and _matches_any(
        tags, {"t1", "hausdorff", "t2", "metric", "metrizable"}
    ):
        witness = "countable+t1"
        return Result.true(
            mode="theorem",
            value="f_sigma",
            justification=[
                "Countable T1 space: each singleton {x} is closed (T1), "
                "so the space is a countable union of closed singletons — an F_sigma.",
            ],
            metadata={**base, "criterion": "countable_t1", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="f_sigma",
        justification=[
            "Insufficient tags to determine F_sigma status. "
            "Supply tags such as 'f_sigma', 'closed', 'sigma_compact', "
            "or 'countable_t1'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_perfect_set(space: Any) -> Result:
    """Check whether the space is (or represents) a perfect set.

    A perfect set is a closed set with no isolated points (every point is
    a limit point). Key facts:
    - The Cantor set is the prototypical perfect compact metrizable set.
    - Every perfect Polish space is homeomorphic to the Cantor set (Cantor's theorem).
    - The Cantor-Bendixson theorem: every closed set = perfect ∪ countable scattered.
    - Countable T1 spaces are scattered, hence not perfect.

    Decision layers
    ---------------
    1. Direct perfect/scattered tags → true/false accordingly.
    2. Cantor set → true (perfect by definition).
    3. Irrationals → true (closed in themselves, no isolated points).
    4. Countable T1 → false (scattered: singletons are isolated).
    5. Scattered tags → false.
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, SCATTERED_TAGS):
        witness = next(t for t in tags if t in SCATTERED_TAGS)
        return Result.false(
            mode="theorem",
            value="perfect_set",
            justification=[
                f"Tag {witness!r}: scattered spaces have isolated points in every "
                "nonempty subspace, so they are never perfect.",
            ],
            metadata={**base, "criterion": "scattered"},
        )

    if _matches_any(tags, {"perfect_set", "perfect", "perfect_space"}):
        witness = next(t for t in tags if t in {"perfect_set", "perfect", "perfect_space"})
        return Result.true(
            mode="theorem",
            value="perfect_set",
            justification=[f"Tag {witness!r}: the space is directly tagged as a perfect set."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    if _matches_any(tags, {"cantor_set", "cantor_space"}):
        return Result.true(
            mode="theorem",
            value="perfect_set",
            justification=[
                "The Cantor set is a perfect set: it is closed in R and has no isolated "
                "points (every point is a limit point of the Cantor set). "
                "It is the prototypical compact perfect metrizable space.",
            ],
            metadata={**base, "criterion": "cantor_set"},
        )

    if _matches_any(tags, {"irrationals"}):
        return Result.true(
            mode="theorem",
            value="perfect_set",
            justification=[
                "The irrationals form a perfect space: they are closed in themselves "
                "(as a subspace) and have no isolated points — every irrational is a "
                "limit of other irrationals.",
            ],
            metadata={**base, "criterion": "irrationals"},
        )

    has_countable = _matches_any(tags, {"countable", "countably_infinite", "omega", "finite"})
    has_t1 = _matches_any(tags, {"t1", "hausdorff", "t2", "metric", "metrizable"})
    if has_countable and has_t1:
        return Result.false(
            mode="theorem",
            value="perfect_set",
            justification=[
                "A countable T1 space is scattered: by the Cantor-Bendixson theorem, "
                "every closed subset has an isolated point, so the space is never perfect.",
            ],
            metadata={**base, "criterion": "countable_t1_scattered"},
        )

    if _matches_any(tags, {"no_isolated_points", "dense_in_itself"}) and _matches_any(
        tags, {"closed", "compact", "complete_metric", "metric"}
    ):
        witness = "no_isolated_points+closed"
        return Result.true(
            mode="theorem",
            value="perfect_set",
            justification=[
                "The space has no isolated points and is closed in a metric space, "
                "satisfying the definition of a perfect set.",
            ],
            metadata={**base, "criterion": "no_isolated_points_closed", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="perfect_set",
        justification=[
            "Insufficient tags to determine whether the space is a perfect set. "
            "Supply tags such as 'perfect_set', 'cantor_set', 'no_isolated_points', "
            "or 'scattered'.",
        ],
        metadata={**base, "criterion": None},
    )


def has_baire_property(space: Any) -> Result:
    """Check whether the space has the Baire property.

    A set A has the Baire property if there exists an open set U such that
    the symmetric difference A △ U is meager (first category). Key facts:
    - All open and closed sets have the Baire property.
    - All Borel sets (G_delta, F_sigma, G_delta_sigma, ...) have the property.
    - All analytic sets have the Baire property.
    - Non-measurable sets (Bernstein, Vitali) typically lack the Baire property
      (assuming AC).

    Decision layers
    ---------------
    1. Explicit non-Borel / non-measurable tags → false.
    2. Open, closed, G_delta, F_sigma tags → true.
    3. Borel / analytic tags → true.
    4. Metrizable (all Borel sets are measurable in a complete metric space) → true.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, BOREL_NEGATIVE_TAGS):
        blocking = next(t for t in tags if t in BOREL_NEGATIVE_TAGS)
        return Result.false(
            mode="theorem",
            value="baire_property",
            justification=[
                f"Tag {blocking!r}: non-measurable / non-Borel sets such as Bernstein "
                "or Vitali sets do not have the Baire property (under AC).",
            ],
            metadata={**base, "criterion": None},
        )

    if _matches_any(tags, {"open", "closed"}):
        witness = next(t for t in tags if t in {"open", "closed"})
        return Result.true(
            mode="theorem",
            value="baire_property",
            justification=[
                f"Tag {witness!r}: open and closed sets trivially have the Baire property "
                "(take U = interior; the symmetric difference is meager).",
            ],
            metadata={**base, "criterion": "open_or_closed", "witness": witness},
        )

    if _matches_any(tags, {"g_delta", "f_sigma", "g_delta_set", "f_sigma_set",
                            "g_delta_sigma", "f_sigma_delta"}):
        witness = next(t for t in tags if t in {"g_delta", "f_sigma", "g_delta_set", "f_sigma_set", "g_delta_sigma", "f_sigma_delta"})
        return Result.true(
            mode="theorem",
            value="baire_property",
            justification=[
                f"Tag {witness!r}: all G_delta and F_sigma sets (and all Borel sets) "
                "have the Baire property — they lie in the smallest sigma-algebra "
                "generated by the topology and closed under meager modifications.",
            ],
            metadata={**base, "criterion": "g_delta_or_f_sigma", "witness": witness},
        )

    if _matches_any(tags, {"borel", "borel_set", "analytic", "analytic_set"}):
        witness = next(t for t in tags if t in {"borel", "borel_set", "analytic", "analytic_set"})
        return Result.true(
            mode="theorem",
            value="baire_property",
            justification=[
                f"Tag {witness!r}: all Borel sets and analytic sets have the Baire "
                "property in any Polish space.",
            ],
            metadata={**base, "criterion": "borel_analytic", "witness": witness},
        )

    if _matches_any(tags, {"metric", "metrizable", "completely_metrizable", "polish_space"}):
        witness = next(t for t in tags if t in {"metric", "metrizable", "completely_metrizable", "polish_space"})
        return Result.true(
            mode="theorem",
            value="baire_property",
            justification=[
                f"Tag {witness!r}: in a completely metrizable (Polish) space, every "
                "Borel set has the Baire property. Metrizable spaces as wholes have "
                "the Baire property (take U = interior of the whole space = whole space).",
            ],
            metadata={**base, "criterion": "metrizable", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="baire_property",
        justification=[
            "Insufficient tags to determine the Baire property. "
            "Supply tags such as 'open', 'closed', 'g_delta', 'f_sigma', 'borel', "
            "or 'metrizable'.",
        ],
        metadata={**base, "criterion": None},
    )


def cantor_bendixson_analysis(space: Any) -> Result:
    """Apply the Cantor-Bendixson theorem to the space.

    The Cantor-Bendixson theorem states: every closed set F in a Polish space
    decomposes uniquely as F = P ∪ C where P is perfect (closed, no isolated points)
    and C is countable (and open in F). The Cantor-Bendixson rank measures how many
    times the 'derived set' operation must be applied to reach a perfect set.

    Decision layers
    ---------------
    1. Not closed in Polish → unknown (theorem requires closed set in Polish space).
    2. Perfect set → trivial decomposition P=F, C=∅.
    3. Scattered → P=∅, C=F (entire space is countable scattered part).
    4. Closed in Polish → theorem applies; decomposition exists.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    is_in_polish = _matches_any(tags, {"metric", "metrizable", "completely_metrizable",
                                        "polish_space", "polish", "closed_in_polish",
                                        "closed_metrizable"})

    if _matches_any(tags, {"perfect_set", "perfect", "cantor_set", "irrationals"}):
        return Result.true(
            mode="theorem",
            value="cantor_bendixson_applies",
            justification=[
                "The space is perfect (P = F, C = ∅). The Cantor-Bendixson "
                "decomposition is trivial: the perfect part is the whole space and "
                "the scattered part is empty.",
            ],
            metadata={**base, "criterion": "perfect", "cb_rank": 0},
        )

    if _matches_any(tags, SCATTERED_TAGS):
        return Result.true(
            mode="theorem",
            value="cantor_bendixson_applies",
            justification=[
                "The space is scattered (P = ∅, C = F if countable). "
                "The Cantor-Bendixson decomposition yields an empty perfect part; "
                "the entire space is the scattered (countable) component.",
            ],
            metadata={**base, "criterion": "scattered", "cb_rank": "finite_or_omega"},
        )

    if is_in_polish and _matches_any(tags, {"closed", "compact", "closed_metrizable", "closed_in_polish"}):
        witness = next(
            t for t in tags
            if t in {"closed", "compact", "closed_metrizable", "closed_in_polish"}
        )
        return Result.true(
            mode="theorem",
            value="cantor_bendixson_applies",
            justification=[
                f"Tag {witness!r} in a Polish space: the Cantor-Bendixson theorem "
                "guarantees a unique decomposition F = P ∪ C where P is perfect "
                "and C is countable (and open in F).",
            ],
            metadata={**base, "criterion": "closed_in_polish", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="cantor_bendixson_applies",
        justification=[
            "Cantor-Bendixson analysis requires the space to be a closed subset of "
            "a Polish space. Supply tags such as 'closed_in_polish', 'polish_space', "
            "or 'compact_metrizable'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_descriptive_complexity(space: Any) -> dict[str, Any]:
    """Classify a space by its descriptive set-theoretic complexity.

    Keys
    ----
    borel_class : str
        One of ``"open"``, ``"closed"``, ``"g_delta"``, ``"f_sigma"``,
        ``"borel"``, ``"unknown"``.
    is_g_delta : Result
    is_f_sigma : Result
    is_perfect : Result
    has_baire_property : Result
    cb_analysis : Result
    key_properties : list[str]
    representation : str
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    g_delta_r = is_g_delta(space)
    f_sigma_r = is_f_sigma(space)
    perfect_r = is_perfect_set(space)
    baire_prop_r = has_baire_property(space)
    cb_r = cantor_bendixson_analysis(space)

    if _matches_any(tags, {"open", "open_subspace"}):
        borel_class = "open"
    elif _matches_any(tags, {"closed"}):
        borel_class = "closed"
    elif g_delta_r.is_true and f_sigma_r.is_false:
        borel_class = "g_delta"
    elif f_sigma_r.is_true and g_delta_r.is_false:
        borel_class = "f_sigma"
    elif g_delta_r.is_true or f_sigma_r.is_true:
        borel_class = "g_delta" if g_delta_r.is_true else "f_sigma"
    elif _matches_any(tags, {"borel", "borel_set"}):
        borel_class = "borel"
    else:
        borel_class = "unknown"

    key_properties: list[str] = []
    if g_delta_r.is_true:
        key_properties.append("g_delta")
    if f_sigma_r.is_true:
        key_properties.append("f_sigma")
    if perfect_r.is_true:
        key_properties.append("perfect")
    if baire_prop_r.is_true:
        key_properties.append("has_baire_property")
    if _matches_any(tags, SCATTERED_TAGS):
        key_properties.append("scattered")
    if _matches_any(tags, {"completely_metrizable", "polish_space", "polish"}):
        key_properties.append("completely_metrizable")

    return {
        "borel_class": borel_class,
        "is_g_delta": g_delta_r,
        "is_f_sigma": f_sigma_r,
        "is_perfect": perfect_r,
        "has_baire_property": baire_prop_r,
        "cb_analysis": cb_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def descriptive_set_profile(space: Any) -> dict[str, Any]:
    """Full descriptive set theory profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_descriptive_complexity`.
    named_profiles : tuple[DescriptiveSetProfile, ...]
        Registry of canonical descriptive set theory examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_descriptive_complexity(space),
        "named_profiles": get_named_descriptive_profiles(),
        "layer_summary": descriptive_layer_summary(),
    }


__all__ = [
    "DescriptiveSetProfile",
    "G_DELTA_TAGS",
    "F_SIGMA_TAGS",
    "PERFECT_SET_TAGS",
    "SCATTERED_TAGS",
    "BAIRE_PROPERTY_TAGS",
    "BOREL_NEGATIVE_TAGS",
    "G_DELTA_NEGATIVE_TAGS",
    "CLOSED_IN_METRIZABLE_TAGS",
    "OPEN_IN_METRIZABLE_TAGS",
    "get_named_descriptive_profiles",
    "descriptive_layer_summary",
    "descriptive_chapter_index",
    "descriptive_type_index",
    "is_g_delta",
    "is_f_sigma",
    "is_perfect_set",
    "has_baire_property",
    "cantor_bendixson_analysis",
    "classify_descriptive_complexity",
    "descriptive_set_profile",
]
