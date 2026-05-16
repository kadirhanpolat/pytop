"""Stable core-facing hereditary/local profile registries.

This module promotes the most reusable parts of the former experimental
``hereditary_local_profiles`` surface into the main ``pytop`` package.
The profiles stay intentionally light-weight so chapter planning, notebooks,
and future theorem-engine work can share a settled vocabulary.

The v0.1.78 strengthening connects Chapter 33 hereditary/local profiles to
the v0.1.77 Chapter 32 entry-lane vocabulary before Chapter 34 classical
inequalities are read.  The connection is not a new registry: it is metadata
on the existing durable profile surface.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class HereditaryLocalProfile:
    """A hereditary/local profile that is stable enough for core use.

    ``teaching_lane`` says how the profile should be introduced in Chapter 33.
    ``chapter32_entry_bridge_keys`` records which first-reading Chapter 32
    profile keys should be recalled before this profile is used.  This keeps
    hereditary/local warnings tied to the already-stabilized tightness/network
    entry lane instead of opening a second route vocabulary.
    """

    key: str
    display_name: str
    focus: str
    quantifier_surface: str
    chapter_targets: tuple[str, ...]
    teaching_lane: str
    chapter32_entry_bridge_keys: tuple[str, ...]
    comparison_question: str

    @property
    def is_entry_lane(self) -> bool:
        """Return whether the profile is safe for first reading."""

        return self.teaching_lane == "entry"

    @property
    def is_warning_lane(self) -> bool:
        """Return whether the profile should be handled as a warning line."""

        return self.teaching_lane == "warning"

    @property
    def has_chapter32_entry_bridge(self) -> bool:
        """Return whether the profile explicitly points back to Chapter 32."""

        return bool(self.chapter32_entry_bridge_keys)


def get_named_hereditary_local_profiles() -> tuple[HereditaryLocalProfile, ...]:
    """Return the promoted hereditary/local profile families."""

    return (
        HereditaryLocalProfile(
            key="global_vs_hereditary_density",
            display_name="Global versus hereditary density",
            focus="track when a small global density statement hides a larger subspace witness",
            quantifier_surface="hereditary",
            chapter_targets=("30", "33", "35"),
            teaching_lane="bridge",
            chapter32_entry_bridge_keys=("discrete_extreme_behavior",),
            comparison_question="Does small global density control the densities of all subspaces?",
        ),
        HereditaryLocalProfile(
            key="global_vs_hereditary_lindelof",
            display_name="Global versus hereditary Lindelof behavior",
            focus="separate whole-space cover control from worst-subspace cover control",
            quantifier_surface="hereditary",
            chapter_targets=("30", "33", "35"),
            teaching_lane="bridge",
            chapter32_entry_bridge_keys=("network_vs_weight_control",),
            comparison_question="Does whole-space cover control survive the worst subspace?",
        ),
        HereditaryLocalProfile(
            key="local_good_global_large_sum",
            display_name="Local good / global large topological sums",
            focus="record the sum-space warning where pointwise smallness does not force small global invariants",
            quantifier_surface="local_warning",
            chapter_targets=("32", "33", "34"),
            teaching_lane="warning",
            chapter32_entry_bridge_keys=("character_controls_tightness", "discrete_extreme_behavior"),
            comparison_question="Which local first-reading controls fail to bound a large global sum?",
        ),
        HereditaryLocalProfile(
            key="second_countable_safe_region",
            display_name="Second-countable safe region",
            focus="identify the class where hereditary and local smallness remain aligned and easy to teach",
            quantifier_surface="safe_region",
            chapter_targets=("25", "30", "33"),
            teaching_lane="entry",
            chapter32_entry_bridge_keys=("character_controls_tightness", "network_vs_weight_control"),
            comparison_question="Why does the second-countable benchmark keep global, hereditary, and local readings small?",
        ),
    )


def hereditary_local_quantifier_summary() -> dict[str, int]:
    """Return counts by hereditary/local warning surface."""

    return dict(Counter(profile.quantifier_surface for profile in get_named_hereditary_local_profiles()))


def hereditary_local_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return stable profile keys grouped by chapter target."""

    chapter_map: dict[str, list[str]] = {}
    for profile in get_named_hereditary_local_profiles():
        for chapter in profile.chapter_targets:
            chapter_map.setdefault(chapter, []).append(profile.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def hereditary_local_lane_summary() -> dict[str, int]:
    """Return counts by the v0.1.78 Chapter 33 teaching lane."""

    return dict(Counter(profile.teaching_lane for profile in get_named_hereditary_local_profiles()))


def hereditary_local_entry_profiles() -> tuple[HereditaryLocalProfile, ...]:
    """Return first-reading hereditary/local profiles."""

    return tuple(profile for profile in get_named_hereditary_local_profiles() if profile.is_entry_lane)


def hereditary_local_warning_profiles() -> tuple[HereditaryLocalProfile, ...]:
    """Return hereditary/local profiles reserved for explicit warning-line use."""

    return tuple(profile for profile in get_named_hereditary_local_profiles() if profile.is_warning_lane)


def hereditary_local_chapter32_entry_bridge() -> dict[str, tuple[str, ...]]:
    """Map each Chapter 33 profile to its Chapter 32 entry-lane bridge keys."""

    return {
        profile.key: profile.chapter32_entry_bridge_keys
        for profile in get_named_hereditary_local_profiles()
        if profile.has_chapter32_entry_bridge
    }


def render_hereditary_local_strengthening_report() -> str:
    """Render a compact report for the v0.1.78 hereditary/local strengthening."""

    lane_summary = hereditary_local_lane_summary()
    bridge = hereditary_local_chapter32_entry_bridge()
    lines = ["Hereditary/local cardinal-function strengthening"]
    lines.append(
        "lanes: " + ", ".join(f"{lane}={count}" for lane, count in sorted(lane_summary.items()))
    )
    lines.append("Chapter 32 entry bridge:")
    for profile_key in sorted(bridge):
        lines.append(f"- {profile_key}: {', '.join(bridge[profile_key])}")
    lines.append("Chapter 33 now reads second-countable safety before hereditary/local warning lines")
    lines.append("Chapter 34 should use these lane labels when selecting classical inequality examples")
    return "\n".join(lines)


__all__ = [
    "HereditaryLocalProfile",
    "get_named_hereditary_local_profiles",
    "hereditary_local_quantifier_summary",
    "hereditary_local_chapter_index",
    "hereditary_local_lane_summary",
    "hereditary_local_entry_profiles",
    "hereditary_local_warning_profiles",
    "hereditary_local_chapter32_entry_bridge",
    "render_hereditary_local_strengthening_report",
]
