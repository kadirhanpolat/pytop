"""Stable core-facing special-example registries.

This module promotes the previously empty special-example surface into a
light-weight named-example registry that other layers can reference without
pulling in draft-only research scaffolding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class SpecialExampleProfile:
    """A curated named example surface that is stable enough for core use."""

    key: str
    display_name: str
    example_family: str
    example_role: str
    chapter_targets: tuple[str, ...]
    example_bank_file: str
    bridge_route_keys: tuple[str, ...]
    research_path_keys: tuple[str, ...]
    theorem_alignment_keys: tuple[str, ...]
    caution: str


def get_named_special_example_profiles() -> tuple[SpecialExampleProfile, ...]:
    return (
        SpecialExampleProfile(
            key='safe_zone_benchmark_space',
            display_name='Safe-zone benchmark space',
            example_family='benchmark_space',
            example_role='safe_zone',
            chapter_targets=('32', '34', '36'),
            example_bank_file='advanced_directions_research_paths_examples.md',
            bridge_route_keys=('safe_zone_sharpness_route',),
            research_path_keys=('hypothesis_sensitivity_of_size_bounds', 'fine_cardinal_warning_lines'),
            theorem_alignment_keys=('metric_countable_tightness', 'second_countable_network_weight'),
            caution='Use this surface as the stable comparison point before introducing warning-line examples.',
        ),
        SpecialExampleProfile(
            key='local_small_global_large_warning_space',
            display_name='Local-small global-large warning space',
            example_family='warning_space',
            example_role='warning_line',
            chapter_targets=('33', '36'),
            example_bank_file='hereditary_local_cardinal_functions_examples.md',
            bridge_route_keys=('hereditary_local_warning_route', 'counterexample_search_route'),
            research_path_keys=('fine_cardinal_warning_lines', 'counterexample_generation_surface'),
            theorem_alignment_keys=('second_countable_hereditary_smallness',),
            caution='This route is not a safe-region theorem witness; it is the named warning surface for hereditary/local contrasts.',
        ),
        SpecialExampleProfile(
            key='compactification_upgrade_benchmark_space',
            display_name='Compactification upgrade benchmark space',
            example_family='upgrade_bridge',
            example_role='upgrade_route',
            chapter_targets=('22', '35', '36'),
            example_bank_file='compactness_cardinal_functions_examples.md',
            bridge_route_keys=('compactification_upgrade_route',),
            research_path_keys=('compactness_variant_comparison',),
            theorem_alignment_keys=('compactification_upgrade_bridge', 'compact_lindelof_transition'),
            caution='Read this example as a bridge between compactification vocabulary and compactness-comparison routes, not as a blanket implication schema.',
        ),
        SpecialExampleProfile(
            key='countably_compact_warning_anchor',
            display_name='Countably compact warning anchor',
            example_family='warning_space',
            example_role='counterexample_anchor',
            chapter_targets=('35', '36'),
            example_bank_file='compactness_cardinal_functions_examples.md',
            bridge_route_keys=('counterexample_search_route',),
            research_path_keys=('compactness_variant_comparison', 'counterexample_generation_surface'),
            theorem_alignment_keys=('countably_compact_warning_line',),
            caution='This anchor should be used to delimit where compact and countably compact reading paths stop agreeing.',
        ),
        SpecialExampleProfile(
            key='registry_alignment_demo_space',
            display_name='Registry-alignment demo space',
            example_family='project_alignment',
            example_role='inventory_demo',
            chapter_targets=('34', '35', '36'),
            example_bank_file='advanced_directions_research_paths_examples.md',
            bridge_route_keys=('future_threshold_release_route',),
            research_path_keys=('module_and_research_inventory',),
            theorem_alignment_keys=('selected_lindelof_character_bound',),
            caution='Treat this as a visibility/demo route tying code registries, manuscript headings, and report exports together.',
        ),
    )


def special_example_role_summary() -> dict[str, int]:
    return dict(Counter(profile.example_role for profile in get_named_special_example_profiles()))


def special_example_chapter_index() -> dict[str, tuple[str, ...]]:
    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_special_example_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def special_example_route_index() -> dict[str, tuple[str, ...]]:
    route_map: dict[str, list[str]] = {}
    for profile in get_named_special_example_profiles():
        for route in profile.bridge_route_keys + profile.research_path_keys:
            route_map.setdefault(route, []).append(profile.key)
    return {route: tuple(keys) for route, keys in sorted(route_map.items())}


__all__ = [
    "SpecialExampleProfile",
    "get_named_special_example_profiles",
    "special_example_role_summary",
    "special_example_chapter_index",
    "special_example_route_index",
]
