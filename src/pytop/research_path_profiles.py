"""Stable core-facing research-path profile registries.

This module promotes the reusable part of the former experimental
``research_path_registry`` surface into :mod:`pytop`. The profiles stay
light-weight but now explicitly connect path families to promoted bridge,
special-example, and theorem-alignment vocabulary so that theorem and report
surfaces can reference them without importing draft-only scaffolding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchPathProfile:
    """A curated research path that is stable enough for core use."""

    key: str
    display_name: str
    path_family: str
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]
    example_bank_file: str
    experimental_profile: str
    theorem_draft_keys: tuple[str, ...]
    bridge_route_keys: tuple[str, ...]
    special_example_keys: tuple[str, ...]
    theorem_alignment_keys: tuple[str, ...]
    start_here: str


def get_named_research_path_profiles() -> tuple[ResearchPathProfile, ...]:
    return (
        ResearchPathProfile(
            key="hypothesis_sensitivity_of_size_bounds",
            display_name="Hypothesis sensitivity of size bounds",
            path_family="inequality_sharpness",
            presentation_layer="main_text",
            focus="track which hypothesis families really control the strength of size bounds",
            chapter_targets=("34", "36"),
            example_bank_file="classical_cardinal_inequalities_examples.md",
            experimental_profile="classical_inequality_profiles.py",
            theorem_draft_keys=("hausdorff_density_character_bound", "lindelof_character_selected_benchmark"),
            bridge_route_keys=("safe_zone_sharpness_route",),
            special_example_keys=("safe_zone_benchmark_space",),
            theorem_alignment_keys=("compact_hausdorff_continuum_bound",),
            start_here="Start with Chapter 34's Hausdorff d-chi bound, then compare it with the Lindelof/character selected benchmark before moving to Chapter 36.",
        ),
        ResearchPathProfile(
            key="compactness_variant_comparison",
            display_name="Compactness-variant comparison",
            path_family="compactness_comparison",
            presentation_layer="main_text",
            focus="compare compact, countably compact, and local compact behavior under the same cardinal data",
            chapter_targets=("35", "36"),
            example_bank_file="compactness_cardinal_functions_examples.md",
            experimental_profile="compactness_strengthened_profiles.py",
            theorem_draft_keys=("compact_first_countable_continuum_bound", "countably_compact_warning_line"),
            bridge_route_keys=("compactification_upgrade_route", "counterexample_search_route"),
            special_example_keys=("compactification_upgrade_benchmark_space", "countably_compact_warning_anchor"),
            theorem_alignment_keys=("compact_lindelof_transition", "compactification_upgrade_bridge_route"),
            start_here="Begin with the compact Hausdorff first-countable continuum bound, then cross the countably compact warning line and only after that read the Chapter 36 comparison route.",
        ),
        ResearchPathProfile(
            key="fine_cardinal_warning_lines",
            display_name="Fine-cardinal warning lines",
            path_family="warning_examples",
            presentation_layer="selected_block",
            focus="record where tightness, networks, and local data become decisive warning variables",
            chapter_targets=("32", "33", "34", "36"),
            example_bank_file="advanced_directions_research_paths_examples.md",
            experimental_profile="tightness_network_profiles.py",
            theorem_draft_keys=("tightness_character_bound", "second_countable_hereditary_smallness", "local_small_global_large_warning"),
            bridge_route_keys=("hereditary_local_warning_route",),
            special_example_keys=("local_small_global_large_warning_space",),
            theorem_alignment_keys=("metric_countable_tightness", "second_countable_network_weight", "second_countable_hereditary_smallness"),
            start_here="Start at Chapter 32 for the safe fine-cardinal comparison, then jump to Chapter 33's warning scheme before reopening Chapter 36.",
        ),
        ResearchPathProfile(
            key="counterexample_generation_surface",
            display_name="Counterexample-generation surface",
            path_family="counterexample_search",
            presentation_layer="selected_block",
            focus="prepare named warning examples and future automated counterexample-search directions",
            chapter_targets=("31", "33", "35", "36"),
            example_bank_file="advanced_directions_research_paths_examples.md",
            experimental_profile="research_path_registry.py",
            theorem_draft_keys=("local_small_global_large_warning", "countably_compact_warning_line"),
            bridge_route_keys=("counterexample_search_route",),
            special_example_keys=("local_small_global_large_warning_space", "countably_compact_warning_anchor"),
            theorem_alignment_keys=("hereditary_local_warning_bridge_route",),
            start_here="Start from a warning-line example, not from a main theorem: Chapter 33 local-small/global-large and Chapter 35 countably compact are the intended entry points.",
        ),
        ResearchPathProfile(
            key="module_and_research_inventory",
            display_name="Module and research-path inventory",
            path_family="project_alignment",
            presentation_layer="advanced_note",
            focus="align manuscript headings with code modules, notes, and research-facing documentation",
            chapter_targets=("34", "35", "36"),
            example_bank_file="advanced_directions_research_paths_examples.md",
            experimental_profile="research_bridge_profiles.py",
            theorem_draft_keys=("lindelof_character_selected_benchmark", "compact_first_countable_continuum_bound"),
            bridge_route_keys=("future_threshold_release_route",),
            special_example_keys=("registry_alignment_demo_space",),
            theorem_alignment_keys=("safe_zone_sharpness_bridge_route", "compactification_upgrade_bridge_route"),
            start_here="Enter through the registry surfaces: chapter-experimental registry first, then the theorem-draft benchmark map, and only then the open-question notes.",
        ),
    )


def research_path_layer_summary() -> dict[str, int]:
    return dict(Counter(profile.presentation_layer for profile in get_named_research_path_profiles()))


def research_path_chapter_index() -> dict[str, tuple[str, ...]]:
    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_research_path_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def research_path_route_index() -> dict[str, tuple[str, ...]]:
    route_map: dict[str, list[str]] = {}
    for profile in get_named_research_path_profiles():
        for route in profile.bridge_route_keys + profile.special_example_keys:
            route_map.setdefault(route, []).append(profile.key)
    return {route: tuple(keys) for route, keys in sorted(route_map.items())}


__all__ = [
    "ResearchPathProfile",
    "get_named_research_path_profiles",
    "research_path_layer_summary",
    "research_path_chapter_index",
    "research_path_route_index",
]
