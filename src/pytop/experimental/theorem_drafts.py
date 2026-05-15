"""theorem_drafts

Curated theorem-draft and benchmark registry for the second visible Phase L pass.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class TheoremDraftProfile:
    """A recorded benchmark or warning-line surface tied to a Chapter 32--36 draft."""

    key: str
    display_name: str
    chapter_anchor: str
    benchmark_class: str
    source_surface: str
    example_bank_file: str
    experimental_profile: str
    route_keys: tuple[str, ...]
    research_path_keys: tuple[str, ...]
    starting_use: str



def get_named_theorem_draft_profiles() -> tuple[TheoremDraftProfile, ...]:
    """Return curated theorem-draft surfaces used by the Phase L benchmark map."""

    return (
        TheoremDraftProfile(
            key="tightness_character_bound",
            display_name="Tightness/character comparison bound",
            chapter_anchor="32",
            benchmark_class="proved_main_text",
            source_surface="prop:v3-tightness-character-bound",
            example_bank_file="tightness_network_invariants_examples.md",
            experimental_profile="tightness_network_profiles.py",
            route_keys=(),
            research_path_keys=("fine_cardinal_warning_lines",),
            starting_use="Start here when Chapter 32 is being reread as a safe benchmark before moving to hereditary/local warning lines.",
        ),
        TheoremDraftProfile(
            key="second_countable_hereditary_smallness",
            display_name="Second-countable hereditary-smallness screen",
            chapter_anchor="33",
            benchmark_class="proved_main_text",
            source_surface="prop:v3-second-countable-hereditary-small",
            example_bank_file="hereditary_local_cardinal_functions_examples.md",
            experimental_profile="hereditary_local_profiles.py",
            route_keys=("hereditary_local_warning_route",),
            research_path_keys=("fine_cardinal_warning_lines",),
            starting_use="Use this screen before proposing any large hereditary-density program inside a second-countable setting.",
        ),
        TheoremDraftProfile(
            key="hausdorff_density_character_bound",
            display_name="Hausdorff density-character size bound",
            chapter_anchor="34",
            benchmark_class="proved_main_text",
            source_surface="thm:v3-hausdorff-d-chi",
            example_bank_file="classical_cardinal_inequalities_examples.md",
            experimental_profile="classical_inequality_profiles.py",
            route_keys=("safe_zone_sharpness_route",),
            research_path_keys=("hypothesis_sensitivity_of_size_bounds",),
            starting_use="Begin here for the sharpness family: it is the cleanest proved size-bound benchmark in the Chapter 34 line.",
        ),
        TheoremDraftProfile(
            key="lindelof_character_selected_benchmark",
            display_name="Lindelof/character selected benchmark",
            chapter_anchor="34",
            benchmark_class="selected_block",
            source_surface="selected-block benchmark in Chapter 34",
            example_bank_file="classical_cardinal_inequalities_examples.md",
            experimental_profile="classical_inequality_profiles.py",
            route_keys=("safe_zone_sharpness_route",),
            research_path_keys=("hypothesis_sensitivity_of_size_bounds", "module_and_research_inventory"),
            starting_use="Choose this benchmark when the reader wants a curated inequality family without leaving the selected-block layer.",
        ),
        TheoremDraftProfile(
            key="compact_first_countable_continuum_bound",
            display_name="Compact Hausdorff first-countable continuum bound",
            chapter_anchor="35",
            benchmark_class="proved_main_text",
            source_surface="thm:v3-compact-first-countable-continuum",
            example_bank_file="compactness_cardinal_functions_examples.md",
            experimental_profile="compactness_strengthened_profiles.py",
            route_keys=("safe_zone_sharpness_route", "compactification_upgrade_route"),
            research_path_keys=("compactness_variant_comparison",),
            starting_use="Start here for any compactness comparison program; this is the safest compact benchmark carried into Chapter 36.",
        ),
        TheoremDraftProfile(
            key="countably_compact_warning_line",
            display_name="Countably compact warning line",
            chapter_anchor="35",
            benchmark_class="warning_line",
            source_surface="warning-line example in Chapter 35",
            example_bank_file="compactness_cardinal_functions_examples.md",
            experimental_profile="compactness_cardinal_bridges.py",
            route_keys=("compactification_upgrade_route",),
            research_path_keys=("compactness_variant_comparison", "counterexample_generation_surface"),
            starting_use="Move to this warning line once the compact safe zone is understood and the reader wants to test where the package breaks.",
        ),
        TheoremDraftProfile(
            key="local_small_global_large_warning",
            display_name="Local-small/global-large warning scheme",
            chapter_anchor="33",
            benchmark_class="warning_line",
            source_surface="prop:v3-local-sum-warning",
            example_bank_file="hereditary_local_cardinal_functions_examples.md",
            experimental_profile="hereditary_local_profiles.py",
            route_keys=("hereditary_local_warning_route", "counterexample_search_route"),
            research_path_keys=("fine_cardinal_warning_lines", "counterexample_generation_surface"),
            starting_use="Use this scheme when the goal is to generate counterexamples rather than sharpen a safe inequality benchmark.",
        ),
    )



def benchmark_class_summary() -> dict[str, int]:
    counts = Counter(entry.benchmark_class for entry in get_named_theorem_draft_profiles())
    return dict(counts)


def chapter_draft_summary() -> dict[str, int]:
    counts = Counter(entry.chapter_anchor for entry in get_named_theorem_draft_profiles())
    return dict(counts)
