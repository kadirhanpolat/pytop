"""Stable core-facing cardinal-function profile registries.

This module promotes the most reusable parts of the former experimental
``advanced_cardinal_functions`` surface into the main ``pytop`` package.  The
profiles remain intentionally light-weight: they record stable named families
that other layers can reference without importing research-facing scaffolding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class CardinalFunctionProfile:
    """A curated cardinal-function family that is stable enough for core use."""

    key: str
    display_name: str
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


def get_named_cardinal_function_profiles() -> tuple[CardinalFunctionProfile, ...]:
    """Return the promoted cardinal-function profile families.

    The registry does not encode full theorem statements.  It provides a stable
    vocabulary for chapter planning, notebook references, and future theorem-
    engine integration.
    """

    return (
        CardinalFunctionProfile(
            key="character_lindelof_size_bounds",
            display_name="Character + Lindelof type size bounds",
            presentation_layer="main_text",
            focus="combine local-base control with Lindelof-style coverage control",
            chapter_targets=("34", "35"),
        ),
        CardinalFunctionProfile(
            key="density_local_interaction",
            display_name="Density + local-cardinality interaction",
            presentation_layer="main_text",
            focus="test when small density becomes effective only with extra local data",
            chapter_targets=("34",),
        ),
        CardinalFunctionProfile(
            key="tightness_network_contribution",
            display_name="Tightness / network contribution",
            presentation_layer="selected_block",
            focus="compare weight-driven and network-driven control",
            chapter_targets=("32", "34"),
        ),
        CardinalFunctionProfile(
            key="compact_hausdorff_improvements",
            display_name="Compact Hausdorff improvements",
            presentation_layer="selected_block",
            focus="record the stronger bounds available in well-behaved compact settings",
            chapter_targets=("34", "35"),
        ),
        CardinalFunctionProfile(
            key="hereditary_local_warning_variants",
            display_name="Hereditary / local warning variants",
            presentation_layer="advanced_note",
            focus="track which global inequalities need refinement at hereditary or local scale",
            chapter_targets=("33", "34"),
        ),
    )


def cardinal_function_layer_summary() -> dict[str, int]:
    """Return counts by presentation layer."""

    return dict(Counter(profile.presentation_layer for profile in get_named_cardinal_function_profiles()))


def cardinal_function_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return stable profile keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_cardinal_function_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


__all__ = [
    "CardinalFunctionProfile",
    "get_named_cardinal_function_profiles",
    "cardinal_function_layer_summary",
    "cardinal_function_chapter_index",
]
