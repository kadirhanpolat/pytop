"""chapter_experimental_registry

Named chapter -> experimental-module alignment registry for the first Phase L pass.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ChapterExperimentalRegistryEntry:
    """A chapter-level registry entry aligning a Volume III chapter with research-facing surfaces."""

    chapter_number: str
    chapter_title: str
    manuscript_file: str
    primary_example_bank_file: str
    primary_experimental_note: str
    primary_experimental_module: str
    supporting_modules: tuple[str, ...]
    bridge_route_keys: tuple[str, ...]
    research_path_keys: tuple[str, ...]
    notebook_surfaces: tuple[str, ...]


def build_chapter_experimental_registry() -> tuple[ChapterExperimentalRegistryEntry, ...]:
    """Return the curated Chapter 32--36 registry used by the first Phase L pass."""

    return (
        ChapterExperimentalRegistryEntry(
            chapter_number="32",
            chapter_title="Tightness and Network Invariants",
            manuscript_file="manuscript/volume_3/chapters/32_tightness_and_network_invariants.tex",
            primary_example_bank_file="examples_bank/tightness_network_invariants_examples.md",
            primary_experimental_note="docs/experimental/tightness_network_notes_v0_6_26.md",
            primary_experimental_module="tightness_network_profiles.py",
            supporting_modules=("advanced_cardinal_functions.py",),
            bridge_route_keys=(),
            research_path_keys=("fine_cardinal_warning_lines",),
            notebook_surfaces=(
                "notebooks/exploration/18_tightness_and_network_invariants.ipynb",
                "manuscript/volume_3/worksheets/01_tightness_network_and_locality.md",
                "manuscript/volume_3/quick_checks/01_tightness_network_and_locality.tex",
            ),
        ),
        ChapterExperimentalRegistryEntry(
            chapter_number="33",
            chapter_title="Hereditary and Local Cardinal Functions",
            manuscript_file="manuscript/volume_3/chapters/33_hereditary_and_local_cardinal_functions.tex",
            primary_example_bank_file="examples_bank/hereditary_local_cardinal_functions_examples.md",
            primary_experimental_note="docs/experimental/hereditary_local_notes_v0_6_27.md",
            primary_experimental_module="hereditary_local_profiles.py",
            supporting_modules=("research_notes.py",),
            bridge_route_keys=("hereditary_local_warning_route",),
            research_path_keys=("fine_cardinal_warning_lines", "counterexample_generation_surface"),
            notebook_surfaces=(
                "notebooks/exploration/19_hereditary_and_local_cardinal_functions.ipynb",
                "manuscript/volume_3/worksheets/01_tightness_network_and_locality.md",
            ),
        ),
        ChapterExperimentalRegistryEntry(
            chapter_number="34",
            chapter_title="Classical Cardinal Inequalities",
            manuscript_file="manuscript/volume_3/chapters/34_classical_cardinal_inequalities.tex",
            primary_example_bank_file="examples_bank/classical_cardinal_inequalities_examples.md",
            primary_experimental_note="docs/experimental/classical_inequalities_notes_v0_6_28.md",
            primary_experimental_module="classical_inequality_profiles.py",
            supporting_modules=("advanced_cardinal_functions.py", "tightness_network_profiles.py"),
            bridge_route_keys=("safe_zone_sharpness_route",),
            research_path_keys=("hypothesis_sensitivity_of_size_bounds", "fine_cardinal_warning_lines"),
            notebook_surfaces=(
                "notebooks/exploration/20_classical_cardinal_inequalities.ipynb",
                "notebooks/teaching/lesson_14_classical_cardinal_inequalities.ipynb",
                "manuscript/volume_3/worksheets/02_classical_inequalities_and_compactness.md",
                "manuscript/volume_3/quick_checks/02_classical_inequalities_and_compactness.tex",
            ),
        ),
        ChapterExperimentalRegistryEntry(
            chapter_number="35",
            chapter_title="Compactness and Cardinal Functions",
            manuscript_file="manuscript/volume_3/chapters/35_compactness_and_cardinal_functions.tex",
            primary_example_bank_file="examples_bank/compactness_cardinal_functions_examples.md",
            primary_experimental_note="docs/experimental/compactness_strengthened_notes_v0_6_29.md",
            primary_experimental_module="compactness_strengthened_profiles.py",
            supporting_modules=("compactness_cardinal_bridges.py",),
            bridge_route_keys=("compactification_upgrade_route", "safe_zone_sharpness_route"),
            research_path_keys=("compactness_variant_comparison", "module_and_research_inventory"),
            notebook_surfaces=(
                "notebooks/teaching/lesson_15_compactness_and_cardinal_functions.ipynb",
                "manuscript/volume_3/worksheets/02_classical_inequalities_and_compactness.md",
                "manuscript/volume_3/quick_checks/02_classical_inequalities_and_compactness.tex",
            ),
        ),
        ChapterExperimentalRegistryEntry(
            chapter_number="36",
            chapter_title="Advanced Directions and Research Paths",
            manuscript_file="manuscript/volume_3/chapters/36_advanced_directions_and_research_paths.tex",
            primary_example_bank_file="examples_bank/advanced_directions_research_paths_examples.md",
            primary_experimental_note="docs/experimental/research_bridge_notes_v0_6_30.md",
            primary_experimental_module="research_bridge_profiles.py",
            supporting_modules=("research_path_registry.py", "theorem_drafts.py", "research_bridge_inventory.py"),
            bridge_route_keys=("safe_zone_sharpness_route", "counterexample_search_route", "future_threshold_release_route"),
            research_path_keys=("counterexample_generation_surface", "module_and_research_inventory", "compactness_variant_comparison"),
            notebook_surfaces=(
                "manuscript/volume_3/worksheets/03_research_paths_transition.md",
                "manuscript/volume_3/quick_checks/03_research_paths_transition.tex",
                "notebooks/research/advanced_examples.ipynb",
            ),
        ),
    )


def chapter_registry_summary() -> dict[str, int]:
    """Return a compact summary keyed by primary experimental module."""

    counts = Counter(entry.primary_experimental_module for entry in build_chapter_experimental_registry())
    return dict(counts)


def chapter_route_summary() -> dict[str, int]:
    """Return how many chapter entries mention each bridge route."""

    counts: Counter[str] = Counter()
    for entry in build_chapter_experimental_registry():
        counts.update(entry.bridge_route_keys)
    return dict(counts)
