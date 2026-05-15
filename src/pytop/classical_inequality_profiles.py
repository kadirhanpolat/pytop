"""Stable classical-cardinal-inequality profile registries.

This module promotes the most reusable Chapter 34 inequality families into the
main ``pytop`` package.  The profiles stay intentionally lightweight so the
manuscript, notebooks, examples bank, and questionbank surfaces can all share
the same benchmark / selected-block / warning-line vocabulary.

The v0.1.79 strengthening turns the earlier experimental note set into a
durable core-facing API and keeps the v0.1.77--v0.1.78 lane vocabulary visible
before Chapter 35 compactness upgrades are discussed.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class ClassicalInequalityProfile:
    """A classical-cardinal-inequality profile stable enough for core use."""

    key: str
    display_name: str
    focus: str
    writing_layer: str
    chapter_targets: tuple[str, ...]
    teaching_lane: str
    prerequisite_profile_keys: tuple[str, ...]
    benchmark_question: str

    @property
    def is_entry_lane(self) -> bool:
        return self.teaching_lane == "entry"

    @property
    def is_selected_lane(self) -> bool:
        return self.teaching_lane == "selected"

    @property
    def is_warning_lane(self) -> bool:
        return self.teaching_lane == "warning"

    @property
    def has_prerequisite_bridge(self) -> bool:
        return bool(self.prerequisite_profile_keys)


def get_named_classical_inequality_profiles() -> tuple[ClassicalInequalityProfile, ...]:
    """Return the promoted Chapter 34 inequality families."""

    return (
        ClassicalInequalityProfile(
            key="hausdorff_density_character_code",
            display_name="Hausdorff density-character code",
            focus="record the safe coding route from a dense set and local bases to a global size bound",
            writing_layer="main_text",
            chapter_targets=("30", "34"),
            teaching_lane="entry",
            prerequisite_profile_keys=("second_countable_safe_region",),
            benchmark_question="How do a dense set and local bases code point separation into a size bound?",
        ),
        ClassicalInequalityProfile(
            key="countable_network_continuum_line",
            display_name="Countable-network continuum line",
            focus="track the route from countable network data toward separability and a continuum-size corollary",
            writing_layer="main_text",
            chapter_targets=("32", "34"),
            teaching_lane="entry",
            prerequisite_profile_keys=("character_controls_tightness", "network_vs_weight_control"),
            benchmark_question="Which Chapter 32 network witness turns into separability before the continuum corollary?",
        ),
        ClassicalInequalityProfile(
            key="lindelof_character_benchmark",
            display_name="Lindelof-character benchmark",
            focus="mark the selected-block family where cover control and local base size jointly bound global size",
            writing_layer="selected_block",
            chapter_targets=("30", "34", "35"),
            teaching_lane="selected",
            prerequisite_profile_keys=("global_vs_hereditary_lindelof",),
            benchmark_question="Why is the Lindelof-character line a selected benchmark rather than the first main-text route?",
        ),
        ClassicalInequalityProfile(
            key="compact_hausdorff_character_benchmark",
            display_name="Compact Hausdorff character benchmark",
            focus="record the compact benchmark line that will be upgraded in the next chapter",
            writing_layer="selected_block",
            chapter_targets=("22", "34", "35"),
            teaching_lane="selected",
            prerequisite_profile_keys=("second_countable_safe_region",),
            benchmark_question="Which compactness-safe hypothesis makes the character benchmark ready for Chapter 35?",
        ),
        ClassicalInequalityProfile(
            key="hereditary_local_warning_line",
            display_name="Hereditary/local warning line",
            focus="separate global size inequalities from their hereditary or pointwise reinterpretations",
            writing_layer="advanced_note",
            chapter_targets=("33", "34", "36"),
            teaching_lane="warning",
            prerequisite_profile_keys=("global_vs_hereditary_density", "local_good_global_large_sum"),
            benchmark_question="Which hereditary or local reading blocks a blind reuse of the global inequality form?",
        ),
    )


def classical_inequality_layer_summary() -> dict[str, int]:
    """Return counts by Chapter 34 writing layer."""

    return dict(Counter(profile.writing_layer for profile in get_named_classical_inequality_profiles()))


def classical_inequality_lane_summary() -> dict[str, int]:
    """Return counts by the v0.1.79 teaching lane."""

    return dict(Counter(profile.teaching_lane for profile in get_named_classical_inequality_profiles()))


def classical_inequality_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return stable profile keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_classical_inequality_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def classical_inequality_entry_profiles() -> tuple[ClassicalInequalityProfile, ...]:
    """Return first-reading Chapter 34 profiles."""

    return tuple(profile for profile in get_named_classical_inequality_profiles() if profile.is_entry_lane)


def classical_inequality_selected_profiles() -> tuple[ClassicalInequalityProfile, ...]:
    """Return selected-block benchmark profiles."""

    return tuple(
        profile for profile in get_named_classical_inequality_profiles() if profile.is_selected_lane
    )


def classical_inequality_warning_profiles() -> tuple[ClassicalInequalityProfile, ...]:
    """Return explicit warning-line profiles."""

    return tuple(profile for profile in get_named_classical_inequality_profiles() if profile.is_warning_lane)


def classical_inequality_prerequisite_bridge() -> dict[str, tuple[str, ...]]:
    """Map each Chapter 34 profile to prerequisite bridge keys."""

    return {
        profile.key: profile.prerequisite_profile_keys
        for profile in get_named_classical_inequality_profiles()
        if profile.has_prerequisite_bridge
    }


def render_classical_inequality_strengthening_report() -> str:
    """Render a compact report for the v0.1.79 strengthening."""

    lane_summary = classical_inequality_lane_summary()
    layer_summary = classical_inequality_layer_summary()
    bridge = classical_inequality_prerequisite_bridge()
    lines = ["Classical cardinal inequalities strengthening"]
    lines.append(
        "lanes: " + ", ".join(f"{lane}={count}" for lane, count in sorted(lane_summary.items()))
    )
    lines.append(
        "layers: " + ", ".join(f"{layer}={count}" for layer, count in sorted(layer_summary.items()))
    )
    lines.append("Prerequisite bridge:")
    for profile_key in sorted(bridge):
        lines.append(f"- {profile_key}: {', '.join(bridge[profile_key])}")
    lines.append("Chapter 34 now keeps entry benchmarks separate from selected blocks and the hereditary/local warning line")
    lines.append("Questionbank alignment should reuse these lane labels when selecting direct Chapter 34 routes")
    return "\n".join(lines)
