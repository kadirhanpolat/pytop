"""Stable core-facing compactness-strengthened profile registries.

This module promotes the Chapter 35 comparison surface that has become stable
enough to use directly from :mod:`pytop`. The profiles stay lightweight and
chapter-aware so theorem alignment and pedagogy layers can share the same
vocabulary without importing research-only scaffolding.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class CompactnessStrengthenedProfile:
    """A compactness-strengthened family that is stable enough for core use."""

    key: str
    display_name: str
    compactness_family: str
    presentation_layer: str
    teaching_lane: str
    focus: str
    chapter_targets: tuple[str, ...]
    prerequisite_profile_keys: tuple[str, ...]
    benchmark_question: str

    @property
    def writing_layer(self) -> str:
        """Backward-compatible alias kept for the experimental import path."""

        return self.presentation_layer


def get_named_compactness_strengthened_profiles() -> tuple[CompactnessStrengthenedProfile, ...]:
    """Return the promoted compactness-strengthened comparison families."""

    return (
        CompactnessStrengthenedProfile(
            key="compact_lindelof_collapse",
            display_name="Compact Lindelof collapse",
            compactness_family="compact",
            presentation_layer="main_text",
            teaching_lane="entry",
            focus="record that compactness turns the Chapter 31 Lindelof threshold into automatic data",
            chapter_targets=("31", "35"),
            prerequisite_profile_keys=("hausdorff_density_character_code",),
            benchmark_question="Why does compactness make the Chapter 31 Lindelof threshold automatic before stronger size bounds are used?",
        ),
        CompactnessStrengthenedProfile(
            key="compact_hausdorff_first_countable_continuum",
            display_name="Compact Hausdorff first-countable continuum bound",
            compactness_family="compact_hausdorff",
            presentation_layer="main_text",
            teaching_lane="entry",
            focus="track the safe continuum-size conclusion obtained from compactness plus small character",
            chapter_targets=("34", "35"),
            prerequisite_profile_keys=("compact_hausdorff_character_benchmark",),
            benchmark_question="Which Chapter 34 compact-Hausdorff benchmark becomes a safe main-text theorem once compactness and first countability are combined?",
        ),
        CompactnessStrengthenedProfile(
            key="countably_compact_warning_omega1",
            display_name="Countably compact warning omega_1 line",
            compactness_family="countably_compact",
            presentation_layer="selected_block",
            teaching_lane="warning",
            focus="keep the warning example line separate from genuinely compact benchmark families",
            chapter_targets=("31", "35"),
            prerequisite_profile_keys=("hereditary_local_warning_line",),
            benchmark_question="Why does the omega_1 warning line block a blind transfer from compact to merely countably compact arguments?",
        ),
        CompactnessStrengthenedProfile(
            key="one_point_compactification_bridge",
            display_name="One-point compactification bridge",
            compactness_family="local_compactness",
            presentation_layer="selected_block",
            teaching_lane="selected",
            focus="connect local compactness data to a compact Hausdorff envelope",
            chapter_targets=("22", "35"),
            prerequisite_profile_keys=("compact_lindelof_collapse",),
            benchmark_question="How does one-point compactification move local compactness data into the compact Hausdorff safe zone?",
        ),
        CompactnessStrengthenedProfile(
            key="fine_cardinal_compactness_upgrade",
            display_name="Fine-cardinal compactness upgrade",
            compactness_family="fine_cardinal_data",
            presentation_layer="advanced_note",
            teaching_lane="selected",
            focus="record the research-facing question of which fine-cardinal data truly strengthen under compactness",
            chapter_targets=("32", "33", "34", "35"),
            prerequisite_profile_keys=(
                "compact_hausdorff_first_countable_continuum",
                "countably_compact_warning_omega1",
            ),
            benchmark_question="Which fine-cardinal inputs become sharper under compactness, and which ones still belong to the warning-line filter?",
        ),
    )


def compactness_strengthened_layer_summary() -> dict[str, int]:
    """Return counts by presentation layer."""

    return dict(Counter(profile.presentation_layer for profile in get_named_compactness_strengthened_profiles()))


def compactness_strengthened_lane_summary() -> dict[str, int]:
    """Return counts by teaching lane."""

    return dict(Counter(profile.teaching_lane for profile in get_named_compactness_strengthened_profiles()))


def compactness_strengthened_entry_profiles() -> tuple[CompactnessStrengthenedProfile, ...]:
    """Return Chapter 35 first-reading profiles."""

    return tuple(profile for profile in get_named_compactness_strengthened_profiles() if profile.teaching_lane == "entry")


def compactness_strengthened_selected_profiles() -> tuple[CompactnessStrengthenedProfile, ...]:
    """Return selected-block continuation profiles."""

    return tuple(profile for profile in get_named_compactness_strengthened_profiles() if profile.teaching_lane == "selected")


def compactness_strengthened_warning_profiles() -> tuple[CompactnessStrengthenedProfile, ...]:
    """Return warning-line profiles."""

    return tuple(profile for profile in get_named_compactness_strengthened_profiles() if profile.teaching_lane == "warning")


def compactness_strengthened_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return promoted profile keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_compactness_strengthened_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def compactness_strengthened_prerequisite_bridge() -> dict[str, tuple[str, ...]]:
    """Return prerequisite-profile keys for each Chapter 35 benchmark family."""

    return {
        profile.key: profile.prerequisite_profile_keys
        for profile in get_named_compactness_strengthened_profiles()
    }


def render_compactness_strengthened_report() -> str:
    """Render a compact human-readable Chapter 35 strengthening report."""

    lines = [
        "Compactness-strengthened profile report",
        "",
        f"- layer summary: {compactness_strengthened_layer_summary()}",
        f"- lane summary: {compactness_strengthened_lane_summary()}",
        "",
        "Profiles:",
    ]
    for profile in get_named_compactness_strengthened_profiles():
        lines.append(
            f"- {profile.key}: lane={profile.teaching_lane}; layer={profile.presentation_layer}; "
            f"bridge={profile.prerequisite_profile_keys}"
        )
    lines.append("")
    lines.append("Questionbank alignment should reuse these lane labels for Chapter 35 direct routes.")
    return "\n".join(lines)
