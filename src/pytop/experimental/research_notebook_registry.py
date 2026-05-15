"""research_notebook_registry

Curated research-notebook registry for the Phase L readability pass.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchNotebookProfile:
    """A notebook-facing bridge between Volume III chapters and research-oriented surfaces."""

    key: str
    notebook_file: str
    display_name: str
    chapter_targets: tuple[str, ...]
    primary_module: str
    supporting_modules: tuple[str, ...]
    research_path_keys: tuple[str, ...]
    prerequisite_topics: tuple[str, ...]
    usage_note: str


def get_research_notebook_profiles() -> tuple[ResearchNotebookProfile, ...]:
    return (
        ResearchNotebookProfile(
            key="invariant_experiments",
            notebook_file="notebooks/research/invariant_experiments.ipynb",
            display_name="Invariant experiments",
            chapter_targets=("32", "34"),
            primary_module="tightness_network_profiles.py",
            supporting_modules=("classical_inequality_profiles.py",),
            research_path_keys=("fine_cardinal_warning_lines", "hypothesis_sensitivity_of_size_bounds"),
            prerequisite_topics=(
                "Volume II Chapters 29--31: density / character / Lindelof-number vocabulary",
                "Volume III Chapter 32: tightness, network character, and safe warning-line comparisons",
                "Volume III Chapter 34: first main-text size-bound benchmark",
            ),
            usage_note="Use this notebook after the exploration route when the reader wants to compare safe benchmark inequalities with fine-cardinal warning variables in one place.",
        ),
        ResearchNotebookProfile(
            key="infinite_spaces_symbolic_support",
            notebook_file="notebooks/research/infinite_spaces_symbolic_support.ipynb",
            display_name="Infinite-spaces symbolic support",
            chapter_targets=("33", "35", "36"),
            primary_module="hereditary_local_profiles.py",
            supporting_modules=("compactness_strengthened_profiles.py", "research_path_registry.py"),
            research_path_keys=("compactness_variant_comparison", "counterexample_generation_surface"),
            prerequisite_topics=(
                "Volume III Chapter 33: hereditary / local cardinal-function split",
                "Volume III Chapter 35: compactness-strengthened benchmarks and countably compact warning lines",
                "Volume III Chapter 36: named research-path filters",
            ),
            usage_note="Open this notebook when the reader wants symbolic or semi-experimental support while comparing compactness variants with hereditary/local warning examples.",
        ),
        ResearchNotebookProfile(
            key="advanced_examples",
            notebook_file="notebooks/research/advanced_examples.ipynb",
            display_name="Advanced examples",
            chapter_targets=("34", "35", "36"),
            primary_module="research_bridge_profiles.py",
            supporting_modules=("theorem_drafts.py", "research_bridge_inventory.py"),
            research_path_keys=("module_and_research_inventory", "counterexample_generation_surface"),
            prerequisite_topics=(
                "Volume III Chapter 34: benchmark vs selected-block distinction",
                "Volume III Chapter 35: compactification route and compact Hausdorff safe zone",
                "Volume III Chapter 36: open-problem families and registry surfaces",
            ),
            usage_note="This notebook is the preferred final stop when a reader wants chapter-level examples, theorem-draft classes, and research-route registries to be visible together.",
        ),
    )


def notebook_profile_summary() -> dict[str, int]:
    counts = Counter()
    for profile in get_research_notebook_profiles():
        for chapter in profile.chapter_targets:
            counts[chapter] += 1
    return dict(counts)
