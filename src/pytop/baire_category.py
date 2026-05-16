"""Baire category theory: Baire spaces, meager sets, and the Baire Category Theorem.

Key theorems implemented
------------------------
- BCT (metric form): Every complete metric space is a Baire space.
- BCT (topological form): Every locally compact Hausdorff space is a Baire space.
- Polish spaces (completely metrizable + second-countable) are Baire.
- A countable T1 space with no isolated points is NOT Baire (meager in itself).
- An open dense subspace of a Baire space is Baire.
- A comeager subset of a Baire space is dense.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class BaireCategoryProfile:
    """A curated Baire category example for the named profile registry."""

    key: str
    display_name: str
    is_baire: bool
    presentation_layer: str
    focus: str
    category_type: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

BAIRE_POSITIVE_TAGS: set[str] = {
    "baire", "baire_space",
    "complete_metric", "completely_metrizable", "completely_metrizable_space",
    "polish_space", "polish",
    "locally_compact_hausdorff", "lch",
    "compact_hausdorff", "compact_t2",
    "banach_space", "hilbert_space", "frechet_space",
    "cantor_set", "cantor_space",
    "baire_space_omega",
}
BAIRE_NEGATIVE_TAGS: set[str] = {
    "not_baire", "meager_space", "first_category_space",
    "countable_no_isolated_points", "rationals_like",
}
COMPLETE_METRIC_TAGS: set[str] = {
    "complete_metric", "completely_metrizable", "completely_metrizable_space",
    "polish_space", "polish",
    "banach_space", "hilbert_space", "frechet_space",
}
LCH_TAGS: set[str] = {
    "locally_compact_hausdorff", "lch",
    "compact_hausdorff", "compact_t2",
    "locally_compact_t2",
}
POLISH_TAGS: set[str] = {
    "polish_space", "polish",
    "completely_metrizable", "completely_metrizable_space",
}
MEAGER_SPACE_TAGS: set[str] = {
    "meager_space", "first_category_space",
    "countable_no_isolated_points", "rationals_like",
}
COMEAGER_TAGS: set[str] = {
    "comeager", "residual", "generic_subset",
    "dense_g_delta",
}
OPEN_DENSE_TAGS: set[str] = {
    "open_dense_subspace", "open_baire_subspace",
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

def get_named_baire_examples() -> tuple[BaireCategoryProfile, ...]:
    """Return the registry of canonical Baire category examples."""
    return (
        BaireCategoryProfile(
            key="real_line_complete_metric",
            display_name="Real line ℝ (complete metric space)",
            is_baire=True,
            presentation_layer="main_text",
            category_type="complete_metric",
            focus=(
                "ℝ with the standard metric is complete; the Baire Category Theorem "
                "guarantees that any countable intersection of dense open sets is dense. "
                "This is the canonical example for BCT in analysis."
            ),
            chapter_targets=("27", "48"),
        ),
        BaireCategoryProfile(
            key="closed_unit_interval",
            display_name="Closed unit interval [0,1] (compact Hausdorff)",
            is_baire=True,
            presentation_layer="main_text",
            category_type="locally_compact_hausdorff",
            focus=(
                "[0,1] is compact Hausdorff and hence locally compact Hausdorff. "
                "The topological form of BCT applies: the intersection of any "
                "countably many dense open sets is dense."
            ),
            chapter_targets=("27", "48"),
        ),
        BaireCategoryProfile(
            key="cantor_set",
            display_name="Cantor set C (compact metrizable, Baire)",
            is_baire=True,
            presentation_layer="selected_block",
            category_type="complete_metric",
            focus=(
                "The Cantor set is homeomorphic to 2^ω (product of countably many "
                "2-point discrete spaces). It is compact, metrizable, and completely "
                "metrizable, hence a Baire space. It is also nowhere dense in ℝ."
            ),
            chapter_targets=("27", "45"),
        ),
        BaireCategoryProfile(
            key="baire_space_omega_omega",
            display_name="Baire space ω^ω (irrationals as topological space)",
            is_baire=True,
            presentation_layer="advanced_note",
            category_type="polish",
            focus=(
                "The product ω^ω = ℕ^ℕ with the product of discrete topologies is "
                "homeomorphic to the space of irrationals in ℝ. It is a Polish space "
                "(completely metrizable + second-countable) and hence a Baire space. "
                "It is the prototypical 'Baire space' in descriptive set theory."
            ),
            chapter_targets=("27", "52"),
        ),
        BaireCategoryProfile(
            key="rationals_not_baire",
            display_name="Rationals ℚ (countable, NOT Baire)",
            is_baire=False,
            presentation_layer="selected_block",
            category_type="not_baire",
            focus=(
                "ℚ with the subspace topology from ℝ is a countable T1 space with no "
                "isolated points. Each singleton {q} is nowhere dense (its interior in ℚ "
                "is empty), so ℚ = ∪_{q∈ℚ}{q} is a countable union of nowhere dense sets "
                "— meager in itself. By BCT-contrapositive, ℚ is not complete and not Baire."
            ),
            chapter_targets=("27", "48"),
        ),
    )


def baire_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_baire_examples()))


def baire_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_baire_examples():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def baire_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from category_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_baire_examples():
        index.setdefault(p.category_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_baire_space(space: Any) -> Result:
    """Check whether a space is a Baire space.

    A topological space is Baire if every countable intersection of dense open
    sets is dense, equivalently if no nonempty open set is meager.

    Decision layers
    ---------------
    1. Explicit negative tags → false.
    2. Complete metric space tags → true (BCT, metric form).
    3. Locally compact Hausdorff tags → true (BCT, topological form).
    4. Polish / completely metrizable → true (Polish ⊂ complete metric).
    5. Open dense subspace of a Baire-tagged space → true.
    6. Countable T1 space with no isolated points → false (meager in itself).
    7. Direct Baire positive tags → true.
    8. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    # Layer 1: explicit negative tags
    if _matches_any(tags, BAIRE_NEGATIVE_TAGS):
        blocking = next(t for t in tags if t in BAIRE_NEGATIVE_TAGS)
        return Result.false(
            mode="theorem",
            value="baire_space",
            justification=[
                f"The space carries blocking tag {blocking!r} which contradicts Baire space status.",
            ],
            metadata={**base, "criterion": None},
        )

    # Layer 2: complete metric space → Baire (BCT metric form)
    if _matches_any(tags, COMPLETE_METRIC_TAGS):
        witness = next(t for t in tags if t in COMPLETE_METRIC_TAGS)
        return Result.true(
            mode="theorem",
            value="baire_space",
            justification=[
                f"Tag {witness!r}: every complete metric space is a Baire space "
                "(Baire Category Theorem, metric form). "
                "The intersection of any countably many dense open sets is dense.",
            ],
            metadata={**base, "criterion": "complete_metric", "witness": witness},
        )

    # Layer 3: locally compact Hausdorff → Baire (BCT topological form)
    if _matches_any(tags, LCH_TAGS):
        witness = next(t for t in tags if t in LCH_TAGS)
        return Result.true(
            mode="theorem",
            value="baire_space",
            justification=[
                f"Tag {witness!r}: every locally compact Hausdorff space is a Baire space "
                "(Baire Category Theorem, topological form). "
                "Compactness of neighborhood closures prevents meager open sets.",
            ],
            metadata={**base, "criterion": "locally_compact_hausdorff", "witness": witness},
        )

    # Layer 4: open dense subspace of baire → baire
    if _matches_any(tags, OPEN_DENSE_TAGS) and _matches_any(tags, BAIRE_POSITIVE_TAGS):
        return Result.true(
            mode="theorem",
            value="baire_space",
            justification=[
                "An open subspace of a Baire space is itself a Baire space "
                "(the Baire property is inherited by open subsets).",
            ],
            metadata={**base, "criterion": "open_subspace_of_baire"},
        )

    # Layer 5: countable T1 with no isolated points → not Baire
    has_countable = _matches_any(tags, {"countable", "countably_infinite", "omega"})
    has_t1 = _matches_any(tags, {"t1", "hausdorff", "t2", "metric", "metrizable", "t3"})
    has_no_iso = _matches_any(tags, {"no_isolated_points", "perfect_space", "dense_in_itself"})
    if has_countable and has_t1 and has_no_iso:
        return Result.false(
            mode="theorem",
            value="baire_space",
            justification=[
                "A countable T1 space with no isolated points is NOT Baire: "
                "each singleton is nowhere dense (no interior), so the entire space is "
                "a countable union of nowhere dense sets — meager in itself.",
            ],
            metadata={**base, "criterion": "countable_t1_no_isolated_points"},
        )

    # Layer 6: direct Baire positive tags
    if _matches_any(tags, BAIRE_POSITIVE_TAGS):
        witness = next(t for t in tags if t in BAIRE_POSITIVE_TAGS)
        return Result.true(
            mode="theorem",
            value="baire_space",
            justification=[f"The space carries direct Baire-confirming tag {witness!r}."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="baire_space",
        justification=[
            "Insufficient tags to determine Baire space status. "
            "Supply tags such as 'complete_metric', 'locally_compact_hausdorff', "
            "'polish_space', or 'baire'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_meager_space(space: Any) -> Result:
    """Check whether the entire space is meager (first category) in itself.

    A space is meager in itself if it equals a countable union of nowhere dense
    subsets. By the contrapositive of BCT, a Baire space cannot be meager.

    Decision layers
    ---------------
    1. Explicit meager tags → true (space is meager in itself).
    2. Countable T1 space with no isolated points → true.
    3. Space confirmed Baire → false (Baire spaces are never meager in themselves).
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    # Layer 1: direct meager tags
    if _matches_any(tags, MEAGER_SPACE_TAGS):
        witness = next(t for t in tags if t in MEAGER_SPACE_TAGS)
        return Result.true(
            mode="theorem",
            value="meager_space",
            justification=[f"The space carries tag {witness!r} confirming it is meager in itself."],
            metadata={**base, "criterion": "direct_tag", "witness": witness},
        )

    # Layer 2: countable T1 no isolated points → meager
    has_countable = _matches_any(tags, {"countable", "countably_infinite", "omega"})
    has_t1 = _matches_any(tags, {"t1", "hausdorff", "t2", "metric", "metrizable", "t3"})
    has_no_iso = _matches_any(tags, {"no_isolated_points", "perfect_space", "dense_in_itself"})
    if has_countable and has_t1 and has_no_iso:
        return Result.true(
            mode="theorem",
            value="meager_space",
            justification=[
                "A countable T1 space with no isolated points is meager in itself: "
                "each singleton is nowhere dense, and the space is their countable union.",
            ],
            metadata={**base, "criterion": "countable_t1_no_isolated_points"},
        )

    # Layer 3: Baire space → not meager
    baire_r = is_baire_space(space)
    if baire_r.is_true:
        return Result.false(
            mode="theorem",
            value="meager_space",
            justification=[
                "The space is a Baire space; by the Baire Category Theorem a Baire space "
                "cannot be meager in itself.",
            ],
            metadata={**base, "criterion": "baire_not_meager"},
        )

    return Result.unknown(
        mode="symbolic",
        value="meager_space",
        justification=[
            "Insufficient tags to determine whether the space is meager in itself.",
        ],
        metadata={**base, "criterion": None},
    )


def baire_category_theorem_check(space: Any) -> Result:
    """Apply the Baire Category Theorem explicitly.

    Returns a Result explaining which form of BCT applies (if any):
    - Metric form: complete metric space.
    - Topological form: locally compact Hausdorff space.
    - Polish form: Polish (completely metrizable + second-countable) space.

    Returns Result.false if BCT's hypotheses are explicitly violated.
    Returns Result.unknown if it cannot be determined.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, BAIRE_NEGATIVE_TAGS):
        return Result.false(
            mode="theorem",
            value="bct_applies",
            justification=[
                "The space is explicitly not a Baire space; BCT hypotheses are violated.",
            ],
            metadata={**base, "bct_form": None, "criterion": None},
        )

    # Polish: completely metrizable + second-countable
    is_polish = _matches_any(tags, POLISH_TAGS) or (
        _matches_any(tags, COMPLETE_METRIC_TAGS) and
        _matches_any(tags, {"second_countable", "separable_metrizable"})
    )
    if is_polish:
        return Result.true(
            mode="theorem",
            value="bct_applies",
            justification=[
                "BCT (Polish form): every Polish space (completely metrizable and "
                "second-countable) is a Baire space.",
            ],
            metadata={**base, "bct_form": "polish", "criterion": "polish_space"},
        )

    if _matches_any(tags, COMPLETE_METRIC_TAGS):
        witness = next(t for t in tags if t in COMPLETE_METRIC_TAGS)
        return Result.true(
            mode="theorem",
            value="bct_applies",
            justification=[
                f"BCT (metric form): tag {witness!r} confirms a complete metric space. "
                "The intersection of any countably many dense open sets is dense.",
            ],
            metadata={**base, "bct_form": "metric", "criterion": "complete_metric", "witness": witness},
        )

    if _matches_any(tags, LCH_TAGS):
        witness = next(t for t in tags if t in LCH_TAGS)
        return Result.true(
            mode="theorem",
            value="bct_applies",
            justification=[
                f"BCT (topological form): tag {witness!r} confirms a locally compact "
                "Hausdorff space. Every nonempty open set has a compact closure that "
                "blocks meagerness.",
            ],
            metadata={**base, "bct_form": "topological", "criterion": "locally_compact_hausdorff", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="bct_applies",
        justification=[
            "BCT cannot be applied: the space is not tagged as complete metric "
            "or locally compact Hausdorff.",
        ],
        metadata={**base, "bct_form": None, "criterion": None},
    )


def classify_baire_category(space: Any) -> dict[str, Any]:
    """Classify a space by its Baire category properties.

    Keys
    ----
    is_baire : Result
    is_meager_space : Result
    bct_applies : Result
    baire_type : str
        One of ``"complete_metric"``, ``"locally_compact_hausdorff"``,
        ``"polish"``, ``"not_baire"``, ``"unknown"``.
    key_properties : list[str]
    representation : str
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    baire_r = is_baire_space(space)
    meager_r = is_meager_space(space)
    bct_r = baire_category_theorem_check(space)

    criterion = baire_r.metadata.get("criterion") if isinstance(baire_r.metadata, dict) else None

    if bct_r.metadata.get("bct_form") == "polish":
        baire_type = "polish"
    elif criterion == "complete_metric":
        baire_type = "complete_metric"
    elif criterion == "locally_compact_hausdorff":
        baire_type = "locally_compact_hausdorff"
    elif baire_r.is_false or meager_r.is_true:
        baire_type = "not_baire"
    elif baire_r.is_true:
        baire_type = "baire"
    else:
        baire_type = "unknown"

    key_properties: list[str] = []
    if baire_r.is_true:
        key_properties.append("baire_space")
    if _matches_any(tags, COMPLETE_METRIC_TAGS):
        key_properties.append("complete_metric")
    if _matches_any(tags, LCH_TAGS):
        key_properties.append("locally_compact_hausdorff")
    if _matches_any(tags, POLISH_TAGS):
        key_properties.append("polish")
    if meager_r.is_true:
        key_properties.append("meager_in_itself")

    return {
        "is_baire": baire_r,
        "is_meager_space": meager_r,
        "bct_applies": bct_r,
        "baire_type": baire_type,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def baire_category_profile(space: Any) -> dict[str, Any]:
    """Full Baire category profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_baire_category`.
    named_examples : tuple[BaireCategoryProfile, ...]
        Registry of canonical Baire category examples.
    layer_summary : dict[str, int]
        Example count by presentation_layer.
    """
    return {
        "classification": classify_baire_category(space),
        "named_examples": get_named_baire_examples(),
        "layer_summary": baire_layer_summary(),
    }


__all__ = [
    "BaireCategoryProfile",
    "BAIRE_POSITIVE_TAGS",
    "BAIRE_NEGATIVE_TAGS",
    "COMPLETE_METRIC_TAGS",
    "LCH_TAGS",
    "POLISH_TAGS",
    "MEAGER_SPACE_TAGS",
    "COMEAGER_TAGS",
    "OPEN_DENSE_TAGS",
    "get_named_baire_examples",
    "baire_layer_summary",
    "baire_chapter_index",
    "baire_type_index",
    "is_baire_space",
    "is_meager_space",
    "baire_category_theorem_check",
    "classify_baire_category",
    "baire_category_profile",
]
