"""Advanced separation-axiom queries — T3 through T6 and Tychonoff multi-criterion.

This module contains:
- Convenience wrappers for T3, T3.5 (Tychonoff), T4, T5, T6 and related properties
- :func:`check_tychonoff` — multi-criterion Tychonoff decision procedure
- :func:`tychonoff_characterization` — structured characterization report
- :func:`separation_chain` — full T0–T6 ordered result dict

The shared engine, data constants, and basic queries (T0–T2.5) live in
:mod:`pytop.separation_basic`.  The legacy entry point :mod:`pytop.separation`
re-exports everything from both modules.
"""

from __future__ import annotations

from typing import Any

from .property_utils import _extract_tags, _matches_any, _representation_of
from .result import Result
from .separation_basic import (
    TRUE_TAGS,
    TYCHONOFF_POSITIVE_TAGS,
    _positive_tag_implies,
    analyze_separation,
)

_TYCHONOFF_BLOCKING_TAGS: frozenset[str] = frozenset({
    "not_tychonoff", "not_t3_5", "not_completely_regular", "not_t1",
})


def is_regular(space: Any) -> Result:
    return analyze_separation(space, "regular")


def is_t3(space: Any) -> Result:
    return analyze_separation(space, "t3")


def is_completely_regular(space: Any) -> Result:
    return analyze_separation(space, "completely_regular")


def is_tychonoff(space: Any) -> Result:
    return analyze_separation(space, "tychonoff")


def is_normal(space: Any) -> Result:
    return analyze_separation(space, "normal")


def is_t4(space: Any) -> Result:
    return analyze_separation(space, "t4")


def is_completely_normal(space: Any) -> Result:
    return analyze_separation(space, "completely_normal")


def is_t5(space: Any) -> Result:
    return analyze_separation(space, "t5")


def is_perfectly_normal(space: Any) -> Result:
    return analyze_separation(space, "perfectly_normal")


def check_tychonoff(space: Any) -> Result:
    """Multi-criterion Tychonoff (T3.5 / completely regular Hausdorff) check.

    Decision layers
    ---------------
    1. Explicit blocking tags (not_tychonoff, not_t3_5, not_completely_regular,
       not_t1) → false.
    2. Metric tag → true (every metric space is Tychonoff).
    3. Direct positive Tychonoff tags → true.
    4. T1 + completely_regular → true (characterisation theorem).
    5. T4 / normal + T1 → true (Urysohn's Lemma); perfectly_normal is covered
       here too via _positive_tag_implies(tags, "t4").
    6. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {
        "representation": representation,
        "property": "tychonoff",
        "tags": sorted(tags),
    }

    # Layer 1: explicit blocking tags
    if tags & _TYCHONOFF_BLOCKING_TAGS:
        blocking = next(t for t in tags if t in _TYCHONOFF_BLOCKING_TAGS)
        return Result.false(
            mode="theorem",
            value="tychonoff",
            justification=[
                f"The space carries blocking tag {blocking!r} which prevents Tychonoff (T3.5) status.",
            ],
            metadata={**base, "criterion": None},
        )

    has_t1 = _matches_any(tags, TRUE_TAGS["t1"]) or _positive_tag_implies(tags, "t1")
    has_cr = (
        _matches_any(tags, TRUE_TAGS["completely_regular"])
        or _positive_tag_implies(tags, "completely_regular")
    )
    has_normal = _matches_any(tags, TRUE_TAGS["normal"]) or _positive_tag_implies(tags, "normal")

    # Layer 2: metric space → completely regular + T1 → Tychonoff
    if "metric" in tags:
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Every metric space is completely regular and T1, hence Tychonoff (T3.5).",
                "The function d(x, ·) / (d(x, ·) + d(·, C)) continuously separates points from closed sets.",
            ],
            metadata={**base, "criterion": "metric"},
        )

    # Layer 3: direct positive Tychonoff tags
    all_tych_pos = TYCHONOFF_POSITIVE_TAGS | frozenset(TRUE_TAGS["tychonoff"])
    if _matches_any(tags, all_tych_pos):
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=["The space carries a direct Tychonoff (T3.5) positive tag."],
            metadata={**base, "criterion": "direct_tag"},
        )

    # Layer 4: T1 + completely_regular ↔ Tychonoff
    if has_t1 and has_cr:
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "T1 + completely regular ↔ Tychonoff (T3.5).",
                "Complete regularity provides Urysohn functions that separate each point from each closed set not containing it.",
            ],
            metadata={**base, "criterion": "cr_t1"},
        )

    # Layer 5: T4 / normal + T1 → Tychonoff (via Urysohn's Lemma)
    # Also covers perfectly_normal → T4 → Tychonoff via _positive_tag_implies.
    has_t4 = _matches_any(tags, TRUE_TAGS["t4"]) or _positive_tag_implies(tags, "t4")
    if has_t4 or (has_t1 and has_normal):
        return Result.true(
            mode="theorem",
            value="tychonoff",
            justification=[
                "Normal T1 (T4) implies Tychonoff: Urysohn's Lemma supplies continuous separation functions.",
            ],
            metadata={**base, "criterion": "normal_t1"},
        )

    return Result.unknown(
        mode="symbolic",
        value="tychonoff",
        justification=[
            "Insufficient information to decide Tychonoff (T3.5) status.",
            "Tag with 'tychonoff'/'t3_5', or supply 'completely_regular'+'t1', or 'normal'+'t1'.",
        ],
        metadata={**base, "criterion": None},
    )


def tychonoff_characterization(space: Any) -> dict[str, Any]:
    """Structured Tychonoff (T3.5) characterization report.

    Keys
    ----
    is_tychonoff : Result
        Multi-criterion Tychonoff result from :func:`check_tychonoff`.
    criterion : str | None
        Which criterion decided the result.
    is_completely_regular : Result
        Separate completely_regular analysis.
    is_t1 : Result
        Separate T1 analysis.
    note : str
        Human-readable summary of the space's position in the Tychonoff hierarchy.
    """
    tych_r = check_tychonoff(space)
    cr_r = analyze_separation(space, "completely_regular")
    t1_r = analyze_separation(space, "t1")
    criterion = tych_r.metadata.get("criterion") if isinstance(tych_r.metadata, dict) else None

    if tych_r.is_true:
        note = "The space is Tychonoff (T3.5 / completely regular Hausdorff)."
    elif tych_r.is_false:
        note = "The space fails the Tychonoff (T3.5) axiom."
    else:
        note = "Tychonoff (T3.5) status is undetermined from the available tags."

    return {
        "is_tychonoff": tych_r,
        "criterion": criterion,
        "is_completely_regular": cr_r,
        "is_t1": t1_r,
        "note": note,
    }


def separation_chain(space: Any) -> dict[str, Result]:
    """Return the full separation hierarchy for the space.

    The result is an ordered dict covering the standard chain
    T0 ≤ T1 ≤ T2 ≤ T2.5 ≤ T3 ≤ T3.5 ≤ T4 ≤ T5 ≤ T6, keyed by
    :data:`~pytop.separation_basic.SEPARATION_CHAIN_ORDER`.  The Tychonoff
    entry uses :func:`check_tychonoff` (multi-criterion) rather than the basic
    tag lookup.
    """
    return {
        "t0": analyze_separation(space, "t0"),
        "t1": analyze_separation(space, "t1"),
        "hausdorff": analyze_separation(space, "hausdorff"),
        "urysohn": analyze_separation(space, "urysohn"),
        "t3": analyze_separation(space, "t3"),
        "tychonoff": check_tychonoff(space),
        "t4": analyze_separation(space, "t4"),
        "completely_normal": analyze_separation(space, "completely_normal"),
        "perfectly_normal": analyze_separation(space, "perfectly_normal"),
    }


__all__ = [
    "is_regular",
    "is_t3",
    "is_completely_regular",
    "is_tychonoff",
    "is_normal",
    "is_t4",
    "is_completely_normal",
    "is_t5",
    "is_perfectly_normal",
    "check_tychonoff",
    "tychonoff_characterization",
    "separation_chain",
]
