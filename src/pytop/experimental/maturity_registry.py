"""maturity_registry

Explicit maturity registry for experimental modules.

The goal of this pass is not to move modules out of ``pytop_experimental`` yet,
but to make their current status auditable and easier to explain across code,
manuscript, and release records.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .chapter_experimental_registry import build_chapter_experimental_registry


@dataclass(frozen=True)
class ExperimentalMaturityProfile:
    """Status record for one experimental module."""

    module_name: str
    maturity_tier: str
    preferred_home: str
    rationale: str
    next_action: str
    primary_chapters: tuple[str, ...]


def get_experimental_maturity_profiles() -> tuple[ExperimentalMaturityProfile, ...]:
    """Return the current maturity split for all shipped experimental modules."""

    return (
        ExperimentalMaturityProfile(
            module_name="advanced_cardinal_functions.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its abstractions now behave like reusable invariant machinery rather than chapter-only note support, and a first core-facing registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("32", "34"),
        ),
        ExperimentalMaturityProfile(
            module_name="advanced_metrization.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its metrization-criterion families now behave like reusable core-facing route vocabulary rather than a placeholder-only experimental note.",
            next_action="core_facade_available",
            primary_chapters=("15", "23"),
        ),
        ExperimentalMaturityProfile(
            module_name="compactness_cardinal_bridges.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="This module already behaves like a named bridge family that can support future core compactness workflows, and a first core-facing bridge registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("35",),
        ),
        ExperimentalMaturityProfile(
            module_name="experimental_inference.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="A stable theorem-profile alignment surface now exists under pytop, so the old experimental import path mainly remains as a compatibility facade.",
            next_action="core_facade_available",
            primary_chapters=("32", "33", "34", "35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="chapter_experimental_registry.py",
            maturity_tier="supported_experimental",
            preferred_home="pytop_experimental",
            rationale="It is stable and valuable, but its job is still to align Volume III chapter surfaces rather than serve the main package directly.",
            next_action="retain_registry_and_expand_cross_links",
            primary_chapters=("32", "33", "34", "35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="classical_inequality_profiles.py",
            maturity_tier="supported_experimental",
            preferred_home="pytop_experimental",
            rationale="The profile layer is exercised by notes and examples, yet it still packages chapter-facing benchmark families rather than settled core primitives.",
            next_action="retain_registry_and_expand_cross_links",
            primary_chapters=("34",),
        ),
        ExperimentalMaturityProfile(
            module_name="compactness_strengthened_profiles.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its comparison families now behave like reusable compactness vocabulary rather than chapter-only benchmark scaffolding, and a first core-facing registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("35",),
        ),
        ExperimentalMaturityProfile(
            module_name="hereditary_local_profiles.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its warning families now behave like reusable invariant-planning vocabulary rather than chapter-only note support, and a first core-facing registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("33",),
        ),
        ExperimentalMaturityProfile(
            module_name="research_bridge_inventory.py",
            maturity_tier="supported_experimental",
            preferred_home="pytop_experimental",
            rationale="The inventory is useful and stable for export/report surfaces, but its meaning still depends on experimental bridge language.",
            next_action="retain_registry_and_expand_cross_links",
            primary_chapters=("34", "35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="research_bridge_profiles.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its curated bridge routes now behave like reusable core-facing route vocabulary rather than purely experimental curation, and a first core-facing registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("34", "35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="research_notebook_registry.py",
            maturity_tier="supported_experimental",
            preferred_home="pytop_experimental",
            rationale="The notebook registry is intentionally cross-layer and still belongs near the research/manuscript seam.",
            next_action="retain_registry_and_expand_cross_links",
            primary_chapters=("32", "33", "34", "35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="tightness_network_profiles.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its profile families now behave like reusable fine-cardinal vocabulary rather than chapter-only scaffolding, and a first core-facing registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("32",),
        ),
        ExperimentalMaturityProfile(
            module_name="research_notes.py",
            maturity_tier="research_draft",
            preferred_home="manuscript_research",
            rationale="This surface is still note-oriented and is better treated as a draft support layer than as stable package behavior.",
            next_action="keep_as_draft",
            primary_chapters=("33", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="research_path_registry.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its named path families now behave like reusable route vocabulary that can connect bridge, special-example, theorem, and report surfaces through a stable core-facing registry under pytop.",
            next_action="core_facade_available",
            primary_chapters=("35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="special_example_spaces.py",
            maturity_tier="core_candidate",
            preferred_home="pytop",
            rationale="Its named special-example surfaces now behave like reusable core-facing example vocabulary rather than an empty draft placeholder, and a first core-facing registry now exists under pytop.",
            next_action="core_facade_available",
            primary_chapters=("33", "35", "36"),
        ),
        ExperimentalMaturityProfile(
            module_name="theorem_drafts.py",
            maturity_tier="research_draft",
            preferred_home="manuscript_research",
            rationale="The module is intentionally draft-oriented and should remain visibly separate from final theorem-engine surfaces.",
            next_action="keep_as_draft",
            primary_chapters=("32", "33", "34", "35"),
        ),
    )


def experimental_maturity_summary() -> dict[str, int]:
    """Return counts by maturity tier."""

    counts = Counter(profile.maturity_tier for profile in get_experimental_maturity_profiles())
    return dict(counts)


def preferred_home_summary() -> dict[str, int]:
    """Return counts by recommended home."""

    counts = Counter(profile.preferred_home for profile in get_experimental_maturity_profiles())
    return dict(counts)


def lookup_experimental_maturity(module_name: str) -> ExperimentalMaturityProfile:
    """Return the maturity profile for one module name."""

    for profile in get_experimental_maturity_profiles():
        if profile.module_name == module_name:
            return profile
    raise KeyError(module_name)


def chapter_primary_maturity_summary() -> dict[str, int]:
    """Return maturity counts for the primary chapter modules in the Volume III registry."""

    counts: Counter[str] = Counter()
    for entry in build_chapter_experimental_registry():
        counts[lookup_experimental_maturity(entry.primary_experimental_module).maturity_tier] += 1
    return dict(counts)


def promoted_core_facade_modules() -> tuple[str, ...]:
    """Return experimental module names that now have core-facing counterparts."""

    return tuple(
        profile.module_name
        for profile in get_experimental_maturity_profiles()
        if profile.next_action == "core_facade_available"
    )


def core_counterpart_index() -> dict[str, str]:
    """Return the preferred core-facing counterpart for promotion-ready wrappers."""

    return {
        "advanced_cardinal_functions.py": "pytop.cardinal_function_profiles",
        "advanced_metrization.py": "pytop.metrization_profiles",
        "compactness_cardinal_bridges.py": "pytop.compactness_bridges",
        "experimental_inference.py": "pytop.theorem_profile_alignment",
        "compactness_strengthened_profiles.py": "pytop.compactness_strengthened_profiles",
        "hereditary_local_profiles.py": "pytop.hereditary_local_profiles",
        "research_bridge_profiles.py": "pytop.research_bridge_profiles",
        "tightness_network_profiles.py": "pytop.tightness_network_profiles",
        "research_path_registry.py": "pytop.research_path_profiles",
        "special_example_spaces.py": "pytop.special_example_profiles",
    }


def retained_supported_experimental_modules() -> tuple[str, ...]:
    """Return stable registries that intentionally remain in the experimental package."""

    return tuple(
        profile.module_name
        for profile in get_experimental_maturity_profiles()
        if profile.maturity_tier == "supported_experimental"
    )


def retained_research_draft_modules() -> tuple[str, ...]:
    """Return intentionally draft-only research surfaces."""

    return tuple(
        profile.module_name
        for profile in get_experimental_maturity_profiles()
        if profile.maturity_tier == "research_draft"
    )


def consolidation_bucket_summary() -> dict[str, int]:
    """Return the post-cleanup consolidation split used by release-facing reports."""

    return {
        "core_counterpart_available": len(core_counterpart_index()),
        "retained_supported_experimental": len(retained_supported_experimental_modules()),
        "retained_research_draft": len(retained_research_draft_modules()),
    }
