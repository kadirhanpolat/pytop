"""Normal spaces: Urysohn's Lemma, Tietze Extension, and normality profiles.

Key theorems implemented
------------------------
- Urysohn's Lemma: X is normal iff for every pair of disjoint closed sets A, B
  there exists a continuous function f: X → [0,1] with f(A)⊆{0} and f(B)⊆{1}.
- Tietze Extension Theorem: X is normal T1 (T4) iff every continuous function
  f: C → R defined on a closed subset C extends to a continuous F: X → R.
- Dieudonné's Theorem: Every paracompact Hausdorff space is normal.
- Compact Hausdorff → normal (T4): compact + T2 forces disjoint closed sets apart.
- Metrizable → perfectly normal: closed sets are G-delta via distance functions.
- Shrinking Lemma: open covers of normal spaces have open shrinkings.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class NormalSpaceProfile:
    """A curated normal space example for the named profile registry."""

    key: str
    display_name: str
    normality_type: str
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

NORMAL_POSITIVE_TAGS: set[str] = {
    "normal", "t4", "normal_t1",
    "perfectly_normal", "t6",
    "metric", "metrizable", "completely_metrizable",
    "compact_hausdorff", "compact_t2",
    "paracompact_hausdorff",
    "cw_complex", "manifold", "polish_space",
    "second_countable_t3",
}
NORMAL_NEGATIVE_TAGS: set[str] = {
    "not_normal", "not_t4",
    "sorgenfrey_plane", "moore_plane_full",
}
PERFECTLY_NORMAL_TAGS: set[str] = {
    "perfectly_normal", "t6",
    "metric", "metrizable", "completely_metrizable", "polish_space",
    "second_countable_t3",
}
METRIZABLE_NORMAL_TAGS: set[str] = {
    "metric", "metrizable", "completely_metrizable",
    "polish_space", "banach_space", "hilbert_space",
}
COMPACT_HAUSDORFF_TAGS: set[str] = {
    "compact_hausdorff", "compact_t2",
    "profinite", "compact_lie_group",
}
PARACOMPACT_HAUSDORFF_TAGS: set[str] = {
    "paracompact_hausdorff",
    "cw_complex", "manifold", "metrizable",
}
URYSOHN_CONFIRMING_TAGS: set[str] = NORMAL_POSITIVE_TAGS
TIETZE_CONFIRMING_TAGS: set[str] = {
    "normal_t1", "t4",
    "metric", "metrizable", "completely_metrizable",
    "compact_hausdorff", "compact_t2",
    "paracompact_hausdorff", "cw_complex",
    "perfectly_normal", "t6", "polish_space",
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
# Named profile registry
# ---------------------------------------------------------------------------

def get_named_normal_space_profiles() -> tuple[NormalSpaceProfile, ...]:
    """Return the registry of canonical normal space examples."""
    return (
        NormalSpaceProfile(
            key="metrizable_space",
            display_name="Metrizable space (perfectly normal)",
            normality_type="perfectly_normal",
            presentation_layer="main_text",
            focus=(
                "Every metrizable space is perfectly normal (T6): closed sets are "
                "G-delta via the distance function d(x, C), and metrizable spaces "
                "are paracompact, hence normal. Urysohn's Lemma applies in the "
                "explicit form f(x) = d(x,A)/(d(x,A)+d(x,B))."
            ),
            chapter_targets=("15", "32"),
        ),
        NormalSpaceProfile(
            key="compact_hausdorff_space",
            display_name="Compact Hausdorff space (normal)",
            normality_type="normal",
            presentation_layer="main_text",
            focus=(
                "Every compact Hausdorff space is normal (T4): given disjoint closed "
                "sets A, B, compactness separates them by disjoint open sets. "
                "Urysohn's Lemma and Tietze Extension both apply."
            ),
            chapter_targets=("17", "32"),
        ),
        NormalSpaceProfile(
            key="cw_complex",
            display_name="CW-complex (normal)",
            normality_type="normal",
            presentation_layer="selected_block",
            focus=(
                "Every CW-complex is paracompact and Hausdorff, hence normal "
                "(Dieudonné's theorem). This makes Tietze Extension available for "
                "constructing homotopies and characteristic maps on CW-complexes."
            ),
            chapter_targets=("29", "32"),
        ),
        NormalSpaceProfile(
            key="niemytzki_plane",
            display_name="Niemytzki (Moore) plane (normal, not perfectly normal)",
            normality_type="normal",
            presentation_layer="advanced_note",
            focus=(
                "The Niemytzki plane (tangent-disk topology on the closed upper half-plane) "
                "is a classical example of a space that is normal (T4) but NOT perfectly "
                "normal (T6): the x-axis is a closed set that is not a G-delta. "
                "Urysohn's Lemma applies, but Tietze Extension for G-delta closed sets fails."
            ),
            chapter_targets=("32", "36"),
        ),
        NormalSpaceProfile(
            key="sorgenfrey_plane",
            display_name="Sorgenfrey plane S x S (not normal)",
            normality_type="not_normal",
            presentation_layer="selected_block",
            focus=(
                "The Sorgenfrey line S (R with the lower limit topology) is Lindelöf "
                "and hence normal, but S x S is NOT normal: the antidiagonal "
                "{(x,-x) : x in R} is closed and discrete yet uncountable, "
                "preventing a normal separation. Urysohn's Lemma fails."
            ),
            chapter_targets=("32", "36"),
        ),
    )


def normal_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(p.presentation_layer for p in get_named_normal_space_profiles()))


def normal_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_normal_space_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def normal_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from normality_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_normal_space_profiles():
        index.setdefault(p.normality_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def urysohn_function_exists(space: Any) -> Result:
    """Check whether Urysohn's Lemma applies to the space.

    Urysohn's Lemma states that a topological space X is normal if and only if
    for every pair of disjoint closed sets A, B there exists a continuous function
    f: X → [0,1] with f(A) ⊆ {0} and f(B) ⊆ {1}.

    Decision layers
    ---------------
    1. Explicit not-normal tags → false (Urysohn functions cannot always be found).
    2. Metrizable → true (explicit form: f(x) = d(x,A)/(d(x,A)+d(x,B))).
    3. Compact Hausdorff → true (normality confirmed by compactness).
    4. Paracompact Hausdorff → true (Dieudonné: paracompact + T2 → normal).
    5. Perfectly normal tags → true (stronger than normal; Urysohn applies).
    6. Normal / T4 tags → true (Urysohn's Lemma is equivalent to normality).
    7. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, NORMAL_NEGATIVE_TAGS):
        blocking = next(t for t in tags if t in NORMAL_NEGATIVE_TAGS)
        return Result.false(
            mode="theorem",
            value="urysohn_function_exists",
            justification=[
                f"Tag {blocking!r} rules out normality; Urysohn separation functions "
                "cannot always be found for disjoint closed sets.",
            ],
            metadata={**base, "criterion": None},
        )

    if _matches_any(tags, METRIZABLE_NORMAL_TAGS):
        witness = next(t for t in tags if t in METRIZABLE_NORMAL_TAGS)
        return Result.true(
            mode="theorem",
            value="urysohn_function_exists",
            justification=[
                f"Tag {witness!r}: metrizable spaces are perfectly normal. "
                "Urysohn functions are explicit: f(x) = d(x,A)/(d(x,A)+d(x,B)) "
                "separates disjoint closed sets A and B continuously.",
            ],
            metadata={**base, "criterion": "metrizable", "witness": witness},
        )

    if _matches_any(tags, COMPACT_HAUSDORFF_TAGS):
        witness = next(t for t in tags if t in COMPACT_HAUSDORFF_TAGS)
        return Result.true(
            mode="theorem",
            value="urysohn_function_exists",
            justification=[
                f"Tag {witness!r}: compact Hausdorff spaces are normal (T4). "
                "By Urysohn's Lemma, continuous separation functions exist for "
                "every pair of disjoint closed sets.",
            ],
            metadata={**base, "criterion": "compact_hausdorff", "witness": witness},
        )

    if _matches_any(tags, PARACOMPACT_HAUSDORFF_TAGS):
        witness = next(t for t in tags if t in PARACOMPACT_HAUSDORFF_TAGS)
        return Result.true(
            mode="theorem",
            value="urysohn_function_exists",
            justification=[
                f"Tag {witness!r}: by Dieudonné's theorem, paracompact Hausdorff "
                "spaces are normal. Urysohn's Lemma then guarantees separation functions.",
            ],
            metadata={**base, "criterion": "paracompact_hausdorff", "witness": witness},
        )

    if _matches_any(tags, PERFECTLY_NORMAL_TAGS - METRIZABLE_NORMAL_TAGS - PARACOMPACT_HAUSDORFF_TAGS):
        witness = next(t for t in tags if t in PERFECTLY_NORMAL_TAGS)
        return Result.true(
            mode="theorem",
            value="urysohn_function_exists",
            justification=[
                f"Tag {witness!r}: perfectly normal spaces are normal (T4). "
                "Urysohn's Lemma applies; separation functions can be taken to be "
                "zero exactly on A and one exactly on B.",
            ],
            metadata={**base, "criterion": "perfectly_normal", "witness": witness},
        )

    if _matches_any(tags, {"normal", "t4", "normal_t1"}):
        witness = next(t for t in tags if t in {"normal", "t4", "normal_t1"})
        return Result.true(
            mode="theorem",
            value="urysohn_function_exists",
            justification=[
                f"Tag {witness!r}: normality (T4) is equivalent to the existence of "
                "Urysohn separation functions (Urysohn's Lemma).",
            ],
            metadata={**base, "criterion": "normal_tag", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="urysohn_function_exists",
        justification=[
            "Normality cannot be confirmed; Urysohn separation functions may not exist. "
            "Supply tags such as 'normal', 'metric', 'compact_hausdorff', "
            "or 'paracompact_hausdorff'.",
        ],
        metadata={**base, "criterion": None},
    )


def tietze_extension_applicable(space: Any) -> Result:
    """Check whether the Tietze Extension Theorem applies to the space.

    Tietze Extension Theorem: X is a normal T1 space (T4) if and only if
    every continuous function f: C → R defined on a closed subset C ⊆ X
    extends to a continuous function F: X → R.

    Decision layers
    ---------------
    1. Explicit not-normal or not-T1 tags → false.
    2. Metrizable → true (metrizable → T4; extension is constructive via Urysohn).
    3. Compact Hausdorff → true (compact T2 → T4 → Tietze).
    4. Paracompact Hausdorff → true (Dieudonné → normal; T4 + T1 → Tietze).
    5. T4 / normal T1 tags → true (Tietze is equivalent to T4).
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    has_not_normal = _matches_any(tags, NORMAL_NEGATIVE_TAGS)
    has_not_t1 = _matches_any(tags, {"not_t1", "not_hausdorff"}) and not _matches_any(tags, {"t1", "hausdorff", "t2", "metric"})
    if has_not_normal or has_not_t1:
        blocking = next(
            (t for t in tags if t in NORMAL_NEGATIVE_TAGS | {"not_t1"}),
            "not_normal",
        )
        return Result.false(
            mode="theorem",
            value="tietze_extension_applicable",
            justification=[
                f"Tag {blocking!r}: Tietze Extension requires a normal T1 (T4) space. "
                "Normality or T1 is not satisfied.",
            ],
            metadata={**base, "criterion": None},
        )

    if _matches_any(tags, METRIZABLE_NORMAL_TAGS):
        witness = next(t for t in tags if t in METRIZABLE_NORMAL_TAGS)
        return Result.true(
            mode="theorem",
            value="tietze_extension_applicable",
            justification=[
                f"Tag {witness!r}: metrizable spaces are T4 (normal + T1). "
                "The Tietze Extension Theorem applies: every continuous f: C → R "
                "(C closed) extends to F: X → R.",
            ],
            metadata={**base, "criterion": "metrizable", "witness": witness},
        )

    if _matches_any(tags, COMPACT_HAUSDORFF_TAGS):
        witness = next(t for t in tags if t in COMPACT_HAUSDORFF_TAGS)
        return Result.true(
            mode="theorem",
            value="tietze_extension_applicable",
            justification=[
                f"Tag {witness!r}: compact Hausdorff spaces are T4. "
                "Tietze Extension applies; every real-valued continuous function "
                "on a closed subspace extends to the whole space.",
            ],
            metadata={**base, "criterion": "compact_hausdorff", "witness": witness},
        )

    if _matches_any(tags, PARACOMPACT_HAUSDORFF_TAGS):
        witness = next(t for t in tags if t in PARACOMPACT_HAUSDORFF_TAGS)
        return Result.true(
            mode="theorem",
            value="tietze_extension_applicable",
            justification=[
                f"Tag {witness!r}: paracompact Hausdorff spaces are normal (T4) "
                "by Dieudonné's theorem. Tietze Extension therefore applies.",
            ],
            metadata={**base, "criterion": "paracompact_hausdorff", "witness": witness},
        )

    if _matches_any(tags, TIETZE_CONFIRMING_TAGS):
        witness = next(t for t in tags if t in TIETZE_CONFIRMING_TAGS)
        return Result.true(
            mode="theorem",
            value="tietze_extension_applicable",
            justification=[
                f"Tag {witness!r} confirms T4 (normal T1) status. "
                "The Tietze Extension Theorem applies.",
            ],
            metadata={**base, "criterion": "t4_tag", "witness": witness},
        )

    return Result.unknown(
        mode="symbolic",
        value="tietze_extension_applicable",
        justification=[
            "T4 (normal T1) status cannot be confirmed; Tietze Extension may not apply. "
            "Supply tags such as 'normal_t1', 't4', 'metric', or 'compact_hausdorff'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_normality(space: Any) -> dict[str, Any]:
    """Classify a space by its normality level.

    Keys
    ----
    normality_type : str
        One of ``"perfectly_normal"``, ``"normal"``, ``"not_normal"``, ``"unknown"``.
    urysohn : Result
        Whether Urysohn separation functions exist.
    tietze : Result
        Whether Tietze Extension applies.
    key_properties : list[str]
    representation : str
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    urysohn_r = urysohn_function_exists(space)
    tietze_r = tietze_extension_applicable(space)

    if _matches_any(tags, NORMAL_NEGATIVE_TAGS):
        normality_type = "not_normal"
    elif _matches_any(tags, PERFECTLY_NORMAL_TAGS):
        normality_type = "perfectly_normal"
    elif urysohn_r.is_true:
        normality_type = "normal"
    elif urysohn_r.is_false:
        normality_type = "not_normal"
    else:
        normality_type = "unknown"

    key_properties: list[str] = []
    if urysohn_r.is_true:
        key_properties.append("normal")
    if _matches_any(tags, PERFECTLY_NORMAL_TAGS):
        key_properties.append("perfectly_normal")
    if tietze_r.is_true:
        key_properties.append("tietze_extension")
    if _matches_any(tags, METRIZABLE_NORMAL_TAGS):
        key_properties.append("metrizable")
    if _matches_any(tags, COMPACT_HAUSDORFF_TAGS):
        key_properties.append("compact_hausdorff")
    if _matches_any(tags, PARACOMPACT_HAUSDORFF_TAGS):
        key_properties.append("paracompact_hausdorff")

    return {
        "normality_type": normality_type,
        "urysohn": urysohn_r,
        "tietze": tietze_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def normal_space_profile(space: Any) -> dict[str, Any]:
    """Full normality profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_normality`.
    named_profiles : tuple[NormalSpaceProfile, ...]
        Registry of canonical normal space examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_normality(space),
        "named_profiles": get_named_normal_space_profiles(),
        "layer_summary": normal_layer_summary(),
    }


__all__ = [
    "NormalSpaceProfile",
    "NORMAL_POSITIVE_TAGS",
    "NORMAL_NEGATIVE_TAGS",
    "PERFECTLY_NORMAL_TAGS",
    "METRIZABLE_NORMAL_TAGS",
    "COMPACT_HAUSDORFF_TAGS",
    "PARACOMPACT_HAUSDORFF_TAGS",
    "URYSOHN_CONFIRMING_TAGS",
    "TIETZE_CONFIRMING_TAGS",
    "get_named_normal_space_profiles",
    "normal_layer_summary",
    "normal_chapter_index",
    "normal_type_index",
    "urysohn_function_exists",
    "tietze_extension_applicable",
    "classify_normality",
    "normal_space_profile",
]
