"""Stable core-facing compactness bridge registries.

The bridge families in this module are the first promotion-ready slice of the
former experimental compactness/cardinal-functions surface.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class CompactnessBridgeProfile:
    """A compactness/cardinal-functions bridge that is stable enough for core use."""

    key: str
    display_name: str
    compactness_family: str
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


def get_named_compactness_bridge_profiles() -> tuple[CompactnessBridgeProfile, ...]:
    """Return curated compactness bridge families promoted into ``pytop``."""

    return (
        CompactnessBridgeProfile(
            key="compact_hausdorff_size_improvements",
            display_name="Compact Hausdorff size improvements",
            compactness_family="compact_hausdorff",
            presentation_layer="main_text",
            focus="track which core size bounds become visibly stronger in good compact settings",
            chapter_targets=("34", "35"),
        ),
        CompactnessBridgeProfile(
            key="countably_compact_warning_line",
            display_name="Countably compact warning line",
            compactness_family="countably_compact",
            presentation_layer="selected_block",
            focus="separate compact-like behavior from genuinely compact behavior",
            chapter_targets=("31", "35"),
        ),
        CompactnessBridgeProfile(
            key="local_compactness_compactification_bridge",
            display_name="Local compactness / compactification bridge",
            compactness_family="local_compactness",
            presentation_layer="selected_block",
            focus="connect local compactness data to global cardinal-function readings",
            chapter_targets=("22", "35"),
        ),
        CompactnessBridgeProfile(
            key="lindelof_to_compactness_transition",
            display_name="Lindelof to compactness transition",
            compactness_family="cover_based_transition",
            presentation_layer="main_text",
            focus="reinterpret the Chapter 31 cover-based threshold language under stronger compactness hypotheses",
            chapter_targets=("31", "35"),
        ),
        CompactnessBridgeProfile(
            key="fine_cardinal_compactness_questions",
            display_name="Fine-cardinal compactness questions",
            compactness_family="fine_cardinal_data",
            presentation_layer="advanced_note",
            focus="record research-facing questions involving tightness, networks, and hereditary/local data under compactness",
            chapter_targets=("32", "33", "35"),
        ),
    )


def compactness_bridge_layer_summary() -> dict[str, int]:
    """Return counts by presentation layer."""

    return dict(Counter(profile.presentation_layer for profile in get_named_compactness_bridge_profiles()))


def compactness_bridge_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return stable bridge keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_compactness_bridge_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}
