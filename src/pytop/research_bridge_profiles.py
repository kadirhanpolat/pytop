"""Stable core-facing research-bridge profile registries.

This module promotes the reusable route vocabulary from the former
``pytop_experimental.research_bridge_profiles`` surface into the main
``pytop`` package. The profiles remain intentionally light-weight: they record
stable named bridge routes that other layers can reference without importing
research-draft scaffolding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchBridgeProfile:
    """A curated bridge route that is stable enough for core use."""

    key: str
    display_name: str
    starting_benchmark: str
    writing_layer: str
    example_bank_file: str
    experimental_note: str
    experimental_module: str
    chapter_targets: tuple[str, ...]


def get_named_research_bridge_profiles() -> tuple[ResearchBridgeProfile, ...]:
    """Return curated cross-layer research routes aligned with Volume III."""

    return (
        ResearchBridgeProfile(
            key="safe_zone_sharpness_route",
            display_name="Safe-zone sharpness route",
            starting_benchmark="compact Hausdorff first-countable continuum bound",
            writing_layer="main_text",
            example_bank_file="advanced_directions_research_paths_examples.md",
            experimental_note="research_bridge_notes_v0_6_30.md",
            experimental_module="research_bridge_profiles.py",
            chapter_targets=("34", "35", "36"),
        ),
        ResearchBridgeProfile(
            key="compactification_upgrade_route",
            display_name="Compactification upgrade route",
            starting_benchmark="one-point compactification bridge",
            writing_layer="main_text",
            example_bank_file="compactness_cardinal_functions_examples.md",
            experimental_note="research_bridge_notes_v0_6_30.md",
            experimental_module="compactness_strengthened_profiles.py",
            chapter_targets=("22", "35", "36"),
        ),
        ResearchBridgeProfile(
            key="hereditary_local_warning_route",
            display_name="Hereditary/local warning route",
            starting_benchmark="local-small global-large topological sum warning",
            writing_layer="selected_block",
            example_bank_file="hereditary_local_cardinal_functions_examples.md",
            experimental_note="research_bridge_notes_v0_6_30.md",
            experimental_module="hereditary_local_profiles.py",
            chapter_targets=("33", "36"),
        ),
        ResearchBridgeProfile(
            key="counterexample_search_route",
            display_name="Counterexample-search route",
            starting_benchmark="named warning examples from Chapters 33 and 35",
            writing_layer="selected_block",
            example_bank_file="advanced_directions_research_paths_examples.md",
            experimental_note="advanced_directions_notes_v0_6_25.md",
            experimental_module="research_path_registry.py",
            chapter_targets=("31", "33", "35", "36"),
        ),
        ResearchBridgeProfile(
            key="future_threshold_release_route",
            display_name="Future threshold-release route",
            starting_benchmark="first real Volume III writing band complete",
            writing_layer="advanced_note",
            example_bank_file="volume_3_index.md",
            experimental_note="research_bridge_notes_v0_6_30.md",
            experimental_module="research_bridge_profiles.py",
            chapter_targets=("32", "33", "34", "35", "36"),
        ),
    )


def research_bridge_layer_summary() -> dict[str, int]:
    """Return counts by writing layer."""

    return dict(Counter(profile.writing_layer for profile in get_named_research_bridge_profiles()))


def research_bridge_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return stable route keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_research_bridge_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


__all__ = [
    "ResearchBridgeProfile",
    "get_named_research_bridge_profiles",
    "research_bridge_layer_summary",
    "research_bridge_chapter_index",
]
