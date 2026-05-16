"""Stable core-facing metrization profile registries.

This module promotes the reusable part of the former experimental
``advanced_metrization`` surface into :mod:`pytop`. The profiles stay light:
they describe stable criterion families that theorem alignment, pedagogy, and
publishing layers can reference without depending on draft-only scaffolding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class MetrizationProfile:
    """A curated metrization family that is stable enough for core use."""

    key: str
    display_name: str
    criterion_family: str
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]



def get_named_metrization_profiles() -> tuple[MetrizationProfile, ...]:
    """Return the promoted metrization profile families."""

    return (
        MetrizationProfile(
            key='urysohn_second_countable_regular_route',
            display_name='Urysohn second-countable regular route',
            criterion_family='classical_sufficient',
            presentation_layer='main_text',
            focus='use second countability together with regular Hausdorff separation as the standard direct metrization criterion',
            chapter_targets=('15', '23'),
        ),
        MetrizationProfile(
            key='compact_hausdorff_second_countable_route',
            display_name='Compact Hausdorff second-countable route',
            criterion_family='compact_safe_region',
            presentation_layer='selected_block',
            focus='record the safe compact Hausdorff corridor where second countability forces metrizability',
            chapter_targets=('14', '23', '35'),
        ),
        MetrizationProfile(
            key='moore_developable_regular_route',
            display_name='Moore developable regular route',
            criterion_family='developable_route',
            presentation_layer='advanced_note',
            focus='keep the classical developable-regular line visible without turning the core package into a full metrization monograph',
            chapter_targets=('23', '36'),
        ),
        MetrizationProfile(
            key='nagata_smirnov_sigma_lf_base_route',
            display_name='Nagata-Smirnov σ-locally finite base route',
            criterion_family='sigma_locally_finite',
            presentation_layer='advanced_note',
            focus='characterise metrizability via T3 plus a σ-locally finite base, the Nagata-Smirnov necessary-and-sufficient criterion',
            chapter_targets=('23', '40'),
        ),
        MetrizationProfile(
            key='bing_sigma_discrete_base_route',
            display_name='Bing σ-discrete base route',
            criterion_family='sigma_discrete',
            presentation_layer='advanced_note',
            focus='characterise metrizability via T3 plus a σ-discrete base, Bing\'s refinement of the Nagata-Smirnov theorem',
            chapter_targets=('23', '40'),
        ),
    )



def metrization_layer_summary() -> dict[str, int]:
    return dict(Counter(profile.presentation_layer for profile in get_named_metrization_profiles()))



def metrization_chapter_index() -> dict[str, tuple[str, ...]]:
    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_metrization_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


# ---------------------------------------------------------------------------
# v0.1.57 durable API — is_metrizable, metrization_profile, analyze_metrization
# ---------------------------------------------------------------------------

from typing import Any  # noqa: E402

from .finite_spaces import FiniteTopologicalSpace  # noqa: E402
from .result import Result  # noqa: E402

TRUE_METRIZABLE_TAGS: set[str] = {
    "metrizable", "metric", "second_countable_regular",
    "second_countable_t3", "compact_hausdorff_second_countable",
    "urysohn_metrizable",
}

FALSE_METRIZABLE_TAGS: set[str] = {
    "not_metrizable", "non_metrizable",
    "not_first_countable", "not_hausdorff", "not_t2",
}

REGULAR_TAGS: set[str] = {"regular", "t3", "regular_t1", "t3_5", "tychonoff"}
NAGATA_SMIRNOV_TAGS: set[str] = {"sigma_locally_finite_base", "sigma_lf_base"}
BING_TAGS: set[str] = {"sigma_discrete_base", "sigma_d_base"}

_METRIZABLE_IMPLIES_TRUE: dict[str, str] = {
    "second_countable": "second_countable alone does not imply metrizable; need T3 as well.",
}


class MetrizationError(ValueError):
    pass


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


def _matches_any(tags: set[str], candidates: set[str]) -> bool:
    return bool(tags & candidates)


def is_metrizable(space: Any) -> Result:
    """Return a structured result for metrizability.

    Decision layers
    ---------------
    1. Explicit false tags (not_metrizable, not_hausdorff, etc.) → false.
    2. Finite spaces: every finite T1 space is metrizable iff it is discrete;
       finite non-discrete spaces are metrizable only if every singleton is open
       (i.e. the topology is discrete).  Conservative: returns theorem-level.
    3. Explicit positive tags (metrizable, metric, etc.) → true (theorem).
    4. Classic sufficient criterion: second_countable + (regular or t3) → true.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    # Layer 1: negative tags
    if _matches_any(tags, FALSE_METRIZABLE_TAGS):
        neg_tag = next(t for t in tags if t in FALSE_METRIZABLE_TAGS)
        return Result.false(
            mode="theorem",
            value="metrizable",
            justification=[
                f"The space carries negative tag {neg_tag!r} which blocks metrizability.",
                "Metrizability requires Hausdorff + first countable as necessary conditions.",
            ],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    # Layer 2: finite spaces
    if representation == "finite" and hasattr(space, "topology") and hasattr(space, "carrier"):
        carrier = list(space.carrier)
        topology = [frozenset(u) for u in space.topology]
        # Discrete iff every singleton is open
        singletons_open = all(frozenset({x}) in topology for x in carrier)
        if singletons_open:
            return Result.true(
                mode="exact",
                value="metrizable",
                justification=[
                    "The finite space has the discrete topology.",
                    "Every discrete space is metrizable (discrete metric d(x,y)=0 if x=y, 1 otherwise).",
                ],
                metadata={"representation": representation, "tags": sorted(tags)},
            )
        else:
            return Result.false(
                mode="theorem",
                value="metrizable",
                justification=[
                    "The finite space is not discrete (some singleton is not open).",
                    "A finite metrizable space must be discrete: finite metric spaces have isolated points.",
                ],
                metadata={"representation": representation, "tags": sorted(tags)},
            )

    # Layer 3: positive tags
    if _matches_any(tags, TRUE_METRIZABLE_TAGS):
        pos_tag = next(t for t in tags if t in TRUE_METRIZABLE_TAGS)
        return Result.true(
            mode="theorem",
            value="metrizable",
            justification=[f"The space carries positive metrizability tag {pos_tag!r}."],
            metadata={"representation": representation, "tags": sorted(tags)},
        )

    # Layer 4: Urysohn — second countable + T3
    has_2nd_countable = any(t in tags for t in ("second_countable", "second_countable_hausdorff"))
    has_regular = _matches_any(tags, REGULAR_TAGS)
    if has_2nd_countable and has_regular:
        return Result.true(
            mode="theorem",
            value="metrizable",
            justification=[
                "Second countable + T3 (regular Hausdorff) implies metrizable by Urysohn Metrization Theorem.",
                "The space embeds into a countable product of unit intervals.",
            ],
            metadata={
                "representation": representation,
                "tags": sorted(tags),
                "criterion": "urysohn_metrization",
            },
        )

    # Layer 5: Nagata-Smirnov — T3 + σ-locally finite base
    has_slf_base = _matches_any(tags, NAGATA_SMIRNOV_TAGS)
    if has_regular and has_slf_base:
        return Result.true(
            mode="theorem",
            value="metrizable",
            justification=[
                "T3 + σ-locally finite base satisfies the Nagata-Smirnov Metrization Theorem.",
                "A space is metrizable iff it is T3 and has a base expressible as a countable union of locally finite families.",
            ],
            metadata={
                "representation": representation,
                "tags": sorted(tags),
                "criterion": "nagata_smirnov",
            },
        )

    # Layer 6: Bing — T3 + σ-discrete base
    has_sd_base = _matches_any(tags, BING_TAGS)
    if has_regular and has_sd_base:
        return Result.true(
            mode="theorem",
            value="metrizable",
            justification=[
                "T3 + σ-discrete base satisfies the Bing Metrization Theorem.",
                "A space is metrizable iff it is T3 and has a base expressible as a countable union of discrete families.",
            ],
            metadata={
                "representation": representation,
                "tags": sorted(tags),
                "criterion": "bing_metrization",
            },
        )

    return Result.unknown(
        mode="symbolic",
        value="metrizable",
        justification=[
            "Insufficient information to decide metrizability.",
            "Tag the space with 'metrizable'/'not_metrizable', or add 'second_countable'+'t3' for Urysohn criterion.",
        ],
        metadata={"representation": representation, "tags": sorted(tags)},
    )


def metrization_profile(space: Any) -> dict[str, Any]:
    """Return a structured metrizability profile.

    Keys
    ----
    is_metrizable : Result
    criterion : str or None
        Which criterion decided the result (e.g. 'urysohn_metrization').
    named_profiles : tuple[MetrizationProfile, ...]
        Stable named metrization families from the registry.
    """
    result = is_metrizable(space)
    criterion = result.metadata.get("criterion") if isinstance(result.metadata, dict) else None
    return {
        "is_metrizable": result,
        "criterion": criterion,
        "named_profiles": get_named_metrization_profiles(),
    }


def analyze_metrization(space: Any) -> Result:
    """Single-call facade: metrizability result with profile metadata.

    This is the main entry point for notebooks and manuscript API-bridge remarks.
    """
    profile = metrization_profile(space)
    r = profile["is_metrizable"]
    named = profile["named_profiles"]

    metadata: dict[str, Any] = {
        "is_metrizable": r.status,
        "criterion": profile["criterion"],
        "named_profile_keys": tuple(p.key for p in named),
    }
    if isinstance(r.metadata, dict):
        metadata["tags"] = r.metadata.get("tags", [])
        metadata["representation"] = r.metadata.get("representation", "unknown")

    return Result(
        status=r.status,
        mode=r.mode,
        value="metrization_analysis",
        justification=r.justification,
        metadata=metadata,
    )


def check_nagata_smirnov(space: Any) -> Result:
    """Nagata-Smirnov criterion: T3 + σ-locally finite base ↔ metrizable.

    Returns true if both conditions are detected via tags, unknown otherwise.
    Tag the space with ``'t3'`` (or ``'regular'``) and
    ``'sigma_locally_finite_base'`` (or ``'sigma_lf_base'``) to trigger the
    criterion.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    has_regular = _matches_any(tags, REGULAR_TAGS)
    has_slf_base = _matches_any(tags, NAGATA_SMIRNOV_TAGS)

    if has_regular and has_slf_base:
        return Result.true(
            mode="theorem",
            value="metrizable",
            justification=[
                "T3 (regular Hausdorff) + σ-locally finite base satisfies the Nagata-Smirnov criterion.",
                "Nagata-Smirnov: a space is metrizable iff it is T3 and has a σ-locally finite base.",
            ],
            metadata={"representation": representation, "tags": sorted(tags), "criterion": "nagata_smirnov"},
        )

    missing = []
    if not has_regular:
        missing.append("T3 (regular Hausdorff)")
    if not has_slf_base:
        missing.append("σ-locally finite base")
    return Result.unknown(
        mode="symbolic",
        value="metrizable",
        justification=[
            f"Nagata-Smirnov criterion incomplete: missing {' and '.join(missing)}.",
            "Tag the space with 'regular'/'t3' and 'sigma_locally_finite_base' to apply this criterion.",
        ],
        metadata={"representation": representation, "tags": sorted(tags), "criterion": None},
    )


def check_bing_metrization(space: Any) -> Result:
    """Bing criterion: T3 + σ-discrete base ↔ metrizable.

    Returns true if both conditions are detected via tags, unknown otherwise.
    Tag the space with ``'t3'`` (or ``'regular'``) and
    ``'sigma_discrete_base'`` (or ``'sigma_d_base'``) to trigger the
    criterion.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    has_regular = _matches_any(tags, REGULAR_TAGS)
    has_sd_base = _matches_any(tags, BING_TAGS)

    if has_regular and has_sd_base:
        return Result.true(
            mode="theorem",
            value="metrizable",
            justification=[
                "T3 (regular Hausdorff) + σ-discrete base satisfies the Bing Metrization Theorem.",
                "Bing: a space is metrizable iff it is T3 and has a base that is a countable union of discrete families.",
            ],
            metadata={"representation": representation, "tags": sorted(tags), "criterion": "bing_metrization"},
        )

    missing = []
    if not has_regular:
        missing.append("T3 (regular Hausdorff)")
    if not has_sd_base:
        missing.append("σ-discrete base")
    return Result.unknown(
        mode="symbolic",
        value="metrizable",
        justification=[
            f"Bing criterion incomplete: missing {' and '.join(missing)}.",
            "Tag the space with 'regular'/'t3' and 'sigma_discrete_base' to apply this criterion.",
        ],
        metadata={"representation": representation, "tags": sorted(tags), "criterion": None},
    )


def metrization_theorem_check(space: Any) -> dict[str, Any]:
    """Run all three metrization criteria and return a combined summary.

    Keys
    ----
    urysohn : Result
        Result from the Urysohn second-countable + T3 criterion.
    nagata_smirnov : Result
        Result from the Nagata-Smirnov σ-locally-finite-base criterion.
    bing : Result
        Result from the Bing σ-discrete-base criterion.
    verdict : Result
        First true result; if none, first false; otherwise unknown.
    """
    urysohn_r = is_metrizable(space)
    ns_r = check_nagata_smirnov(space)
    bing_r = check_bing_metrization(space)

    for r in (urysohn_r, ns_r, bing_r):
        if r.is_true:
            verdict = r
            break
    else:
        for r in (urysohn_r, ns_r, bing_r):
            if r.is_false:
                verdict = r
                break
        else:
            verdict = urysohn_r

    return {
        "urysohn": urysohn_r,
        "nagata_smirnov": ns_r,
        "bing": bing_r,
        "verdict": verdict,
    }


__all__ = [
    "MetrizationProfile",
    "get_named_metrization_profiles",
    "metrization_layer_summary",
    "metrization_chapter_index",
    "TRUE_METRIZABLE_TAGS",
    "FALSE_METRIZABLE_TAGS",
    "REGULAR_TAGS",
    "NAGATA_SMIRNOV_TAGS",
    "BING_TAGS",
    "MetrizationError",
    "is_metrizable",
    "metrization_profile",
    "analyze_metrization",
    "check_nagata_smirnov",
    "check_bing_metrization",
    "metrization_theorem_check",
]
