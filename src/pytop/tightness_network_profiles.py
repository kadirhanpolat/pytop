"""Stable core-facing tightness/network profile registries.

This module promotes the most reusable parts of the former experimental
``tightness_network_profiles`` surface into the main ``pytop`` package.
The profiles stay lightweight and chapter-aware so other layers can use a
stable vocabulary without importing research-facing scaffolding.

The v0.1.77 extension makes the first Cilt V handoff explicit: each profile
now records whether it belongs to the entry lane or the advanced lane.  The
entry lane is suitable for first reading, worksheet, and quick-check use; the
advanced lane is reserved for warning-line or research-facing discussion.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class TightnessNetworkProfile:
    """A fine-cardinal profile that is stable enough for core use.

    ``teaching_lane`` is intentionally independent from ``presentation_layer``.
    A selected-block example can still be entry-ready, while an advanced note
    can be delayed until after the first Chapter 32 reading.
    """

    key: str
    display_name: str
    focus: str
    presentation_layer: str
    chapter_targets: tuple[str, ...]
    teaching_lane: str

    @property
    def is_entry_lane(self) -> bool:
        """Return whether the profile belongs in the first-reading lane."""

        return self.teaching_lane == "entry"

    @property
    def is_advanced_lane(self) -> bool:
        """Return whether the profile belongs in the advanced-warning lane."""

        return self.teaching_lane == "advanced"


def get_named_tightness_network_profiles() -> tuple[TightnessNetworkProfile, ...]:
    """Return the promoted tightness/network profile families."""

    return (
        TightnessNetworkProfile(
            key="character_controls_tightness",
            display_name="Character controls tightness",
            focus="record the safe upper-bound line from local bases to closure witnesses",
            presentation_layer="main_text",
            chapter_targets=("30", "32"),
            teaching_lane="entry",
        ),
        TightnessNetworkProfile(
            key="network_vs_weight_control",
            display_name="Network versus weight control",
            focus="track where network-based control is clearer than base-size control",
            presentation_layer="main_text",
            chapter_targets=("30", "32", "34"),
            teaching_lane="entry",
        ),
        TightnessNetworkProfile(
            key="discrete_extreme_behavior",
            display_name="Discrete extreme behavior",
            focus="compare the easiest closure behavior with the most expensive pointwise network tracking",
            presentation_layer="selected_block",
            chapter_targets=("32",),
            teaching_lane="entry",
        ),
        TightnessNetworkProfile(
            key="sequential_warning_surface",
            display_name="Sequential warning surface",
            focus="separate countable tightness from full sequence-driven control",
            presentation_layer="advanced_note",
            chapter_targets=("19", "20", "32", "36"),
            teaching_lane="advanced",
        ),
    )


def tightness_network_layer_summary() -> dict[str, int]:
    """Return counts by presentation layer."""

    return dict(Counter(profile.presentation_layer for profile in get_named_tightness_network_profiles()))


def tightness_network_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return stable profile keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_tightness_network_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def tightness_network_lane_summary() -> dict[str, int]:
    """Return counts by v0.1.77 teaching lane."""

    return dict(Counter(profile.teaching_lane for profile in get_named_tightness_network_profiles()))


def tightness_network_entry_profiles() -> tuple[TightnessNetworkProfile, ...]:
    """Return profiles suitable for first reading, worksheet, and quick-check use."""

    return tuple(profile for profile in get_named_tightness_network_profiles() if profile.is_entry_lane)


def tightness_network_advanced_profiles() -> tuple[TightnessNetworkProfile, ...]:
    """Return profiles reserved for advanced warning-line or research-facing use."""

    return tuple(profile for profile in get_named_tightness_network_profiles() if profile.is_advanced_lane)


def tightness_network_entry_advanced_split() -> dict[str, tuple[str, ...]]:
    """Return profile keys grouped into the entry and advanced lanes."""

    lane_map: dict[str, list[str]] = {"entry": [], "advanced": []}
    for profile in get_named_tightness_network_profiles():
        lane_map.setdefault(profile.teaching_lane, []).append(profile.key)
    return {lane: tuple(keys) for lane, keys in sorted(lane_map.items())}


def render_tightness_network_lane_report() -> str:
    """Render a compact human-readable report for the v0.1.77 lane split."""

    split = tightness_network_entry_advanced_split()
    lines = ["Tightness/network teaching-lane split"]
    lines.append(f"entry: {', '.join(split.get('entry', ())) }")
    lines.append(f"advanced: {', '.join(split.get('advanced', ())) }")
    lines.append("first reading keeps definitions, safe bounds, and discrete/metric benchmarks together")
    lines.append("advanced reading delays sequential warning-lines until the reader has the entry comparison table")
    return "\n".join(lines)


__all__ = [
    "TightnessNetworkProfile",
    "get_named_tightness_network_profiles",
    "tightness_network_layer_summary",
    "tightness_network_chapter_index",
    "tightness_network_lane_summary",
    "tightness_network_entry_profiles",
    "tightness_network_advanced_profiles",
    "tightness_network_entry_advanced_split",
    "render_tightness_network_lane_report",
]
