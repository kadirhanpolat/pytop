"""Stable theorem-engine alignments for promoted profile registries.

This module gives the promoted profile families a theorem-facing vocabulary.
The goal is intentionally modest: rather than turning profile registries into
an automated proof search system, it records safe theorem alignments that the
core theorem engine can expose with explicit profile metadata.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TheoremProfileAlignment:
    """One safe theorem-facing alignment for a promoted profile family."""

    key: str
    theorem_rule_name: str
    feature: str
    profile_family: str
    profile_keys: tuple[str, ...]
    required_tags: tuple[str, ...]
    result_value: Any | None
    chapter_targets: tuple[str, ...]
    assumptions: tuple[str, ...]
    justification: tuple[str, ...]
    proof_outline: tuple[str, ...]
    focus: str


def get_promoted_theorem_profile_alignments() -> tuple[TheoremProfileAlignment, ...]:
    """Return the safe theorem-facing alignments for promoted profile families."""

    return (
        TheoremProfileAlignment(
            key='metric_countable_tightness',
            theorem_rule_name='metric_spaces_have_countable_tightness',
            feature='tightness',
            profile_family='tightness_network',
            profile_keys=('character_controls_tightness', 'sequential_warning_surface'),
            required_tags=('metric',),
            result_value='aleph_0',
            chapter_targets=('20', '32'),
            assumptions=('Interpret tightness as the least size of a closure witness at a point.',),
            justification=('Metric spaces are first countable, hence have countable tightness.',),
            proof_outline=(
                'Use the metric balls B(x,1/n) to obtain a countable local base at each point.',
                'A countable local base yields countable tightness by selecting one witness from each relevant neighbourhood stage.',
            ),
            focus='tie the promoted character/tightness registry to a classical countable-tightness theorem surface',
        ),
        TheoremProfileAlignment(
            key='first_countable_countable_tightness',
            theorem_rule_name='first_countable_spaces_have_countable_tightness',
            feature='tightness',
            profile_family='tightness_network',
            profile_keys=('character_controls_tightness',),
            required_tags=('first_countable',),
            result_value='aleph_0',
            chapter_targets=('20', '30', '32'),
            assumptions=('Interpret tightness as a closure-witness invariant.',),
            justification=('Every first-countable space has countable tightness.',),
            proof_outline=(
                'Fix a point x in the closure of a set A.',
                'Choose a countable local base at x and select one point of A from each neighbourhood in the base.',
                'The selected countable subset still witnesses x in the closure.',
            ),
            focus='make the promoted tightness registry usable by the core theorem engine outside the metric-only setting',
        ),
        TheoremProfileAlignment(
            key='second_countable_network_weight',
            theorem_rule_name='second_countable_spaces_have_countable_network_and_weight',
            feature='network_weight_alignment',
            profile_family='tightness_network',
            profile_keys=('network_vs_weight_control',),
            required_tags=('second_countable',),
            result_value={'network': 'aleph_0', 'weight': 'aleph_0'},
            chapter_targets=('25', '30', '32', '34'),
            assumptions=('Interpret the query as comparing network size and weight on a standard countability line.',),
            justification=('A second-countable space has a countable base, so it has both countable weight and a countable network.',),
            proof_outline=(
                'Use the given countable base as a witness for countable weight.',
                'The same countable base is automatically a countable network.',
            ),
            focus='turn the network-versus-weight registry into a theorem-facing comparison surface',
        ),
        TheoremProfileAlignment(
            key='second_countable_hereditary_smallness',
            theorem_rule_name='second_countable_spaces_are_hereditarily_lindelof_and_separable',
            feature='hereditary_smallness',
            profile_family='hereditary_local',
            profile_keys=('second_countable_safe_region', 'global_vs_hereditary_lindelof'),
            required_tags=('second_countable',),
            result_value='hereditarily_lindelof_and_separable',
            chapter_targets=('25', '30', '33'),
            assumptions=('Interpret hereditary smallness here as the classical second-countable safe region for subspaces.',),
            justification=('Every subspace of a second-countable space is second countable, hence Lindelof and separable.',),
            proof_outline=(
                'Restrict a countable base of the ambient space to the chosen subspace.',
                'Apply the usual second-countable consequences inside that subspace.',
            ),
            focus='connect the promoted hereditary/local safe-region vocabulary to an explicit theorem consequence',
        ),
        TheoremProfileAlignment(
            key='compact_lindelof_transition',
            theorem_rule_name='compact_lindelof_threshold_collapse',
            feature='compactness_transition',
            profile_family='compactness_strengthened',
            profile_keys=('compact_lindelof_collapse',),
            required_tags=('compact', 'lindelof'),
            result_value='compact_collapse_visible',
            chapter_targets=('31', '35'),
            assumptions=('Interpret the query as asking for the compact-versus-Lindelof transition line in the promoted Chapter 35 vocabulary.',),
            justification=('Once compactness is present, the Chapter 31 Lindelof threshold becomes automatic rather than an extra burden.',),
            proof_outline=(
                'Start from the compact hypothesis and read Lindelofness as already forced in the benchmark line.',
                'Record the transition as a compactness-strengthened comparison rather than as an independent warning surface.',
            ),
            focus='promote the compact-Lindelof collapse line into theorem-visible metadata',
        ),
        TheoremProfileAlignment(
            key='compact_hausdorff_continuum_bound',
            theorem_rule_name='compact_hausdorff_first_countable_continuum_bound',
            feature='compactness_size_bound',
            profile_family='compactness_strengthened',
            profile_keys=('compact_hausdorff_first_countable_continuum',),
            required_tags=('compact', 'hausdorff', 'first_countable'),
            result_value='continuum_bound',
            chapter_targets=('34', '35'),
            assumptions=('Interpret the query as asking for the safe continuum-size line visible in compact Hausdorff first-countable settings.',),
            justification=('Compact Hausdorff spaces with countable local character sit in the standard continuum-bound safe zone.',),
            proof_outline=(
                'Read first countability as countable character data in the compact Hausdorff setting.',
                'Invoke the classical compact Hausdorff size-bound safe region to obtain the continuum cap.',
            ),
            focus='make the compact Hausdorff first-countable benchmark visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='one_point_compactification_available',
            theorem_rule_name='one_point_compactification_bridge_available',
            feature='compactification_bridge',
            profile_family='compactness_strengthened',
            profile_keys=('one_point_compactification_bridge',),
            required_tags=('locally_compact', 'hausdorff', 'noncompact'),
            result_value='one_point_compactification_available',
            chapter_targets=('22', '35'),
            assumptions=('Interpret the query as asking whether the promoted one-point compactification bridge is available.',),
            justification=('A noncompact locally compact Hausdorff space admits a one-point compactification.',),
            proof_outline=(
                'Start from local compactness and Hausdorff separation in the noncompact setting.',
                'Apply the classical one-point compactification theorem and record it as a bridge surface.',
            ),
            focus='turn the promoted compactification bridge into a theorem-visible route',
        ),
        TheoremProfileAlignment(
            key='safe_zone_sharpness_bridge_route',
            theorem_rule_name='compact_hausdorff_first_countable_safe_zone_bridge_route',
            feature='research_bridge',
            profile_family='research_bridge',
            profile_keys=('safe_zone_sharpness_route',),
            required_tags=('compact', 'hausdorff', 'first_countable'),
            result_value='safe_zone_sharpness_route',
            chapter_targets=('34', '35', '36'),
            assumptions=('Interpret the query as asking which promoted research bridge route should organize the safe compact Hausdorff first-countable corridor.',),
            justification=('The promoted research-bridge registry records the compact Hausdorff first-countable safe zone as the canonical sharpness route.',),
            proof_outline=(
                'Recognize the compact Hausdorff first-countable benchmark as the stable safe-zone corridor.',
                'Return the named research-bridge route rather than expanding into a full research note.',
            ),
            focus='make the safe-zone bridge route visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='compactification_upgrade_bridge_route',
            theorem_rule_name='one_point_compactification_upgrade_bridge_route',
            feature='research_bridge',
            profile_family='research_bridge',
            profile_keys=('compactification_upgrade_route',),
            required_tags=('locally_compact', 'hausdorff', 'noncompact'),
            result_value='compactification_upgrade_route',
            chapter_targets=('22', '35', '36'),
            assumptions=('Interpret the query as asking which promoted bridge route organizes the one-point compactification upgrade line.',),
            justification=('The promoted research-bridge registry treats one-point compactification as the standard upgrade route from the noncompact locally compact Hausdorff setting.',),
            proof_outline=(
                'Read local compactness plus Hausdorff separation in the noncompact setting as the compactification corridor.',
                'Expose the named bridge route that turns that corridor into a reusable Chapter 35/36 planning surface.',
            ),
            focus='make the compactification-upgrade route visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='hereditary_local_warning_bridge_route',
            theorem_rule_name='local_small_global_large_warning_bridge_route',
            feature='research_bridge',
            profile_family='research_bridge',
            profile_keys=('hereditary_local_warning_route',),
            required_tags=('local_small_global_large',),
            result_value='hereditary_local_warning_route',
            chapter_targets=('33', '36'),
            assumptions=('Interpret the query as asking for the promoted bridge route attached to the local-small versus global-large warning line.',),
            justification=('The promoted research-bridge registry records the hereditary/local warning route as the stable bridge between warning examples and Chapter 36 research prose.',),
            proof_outline=(
                'Recognize the local-small/global-large warning configuration.',
                'Return the curated bridge route that keeps the warning line visible without unfolding the full draft apparatus.',
            ),
            focus='keep the hereditary/local warning bridge visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='hypothesis_sensitivity_research_path',
            theorem_rule_name='compact_hausdorff_first_countable_size_bound_research_path',
            feature='research_path',
            profile_family='research_path',
            profile_keys=('hypothesis_sensitivity_of_size_bounds',),
            required_tags=('compact', 'hausdorff', 'first_countable'),
            result_value='hypothesis_sensitivity_of_size_bounds',
            chapter_targets=('34', '36'),
            assumptions=('Interpret the query as asking for the named research path behind the safe size-bound benchmark rather than a new theorem statement.',),
            justification=('The promoted research-path registry records the hypothesis-sensitivity route as the stable way to revisit the compact Hausdorff first-countable size-bound corridor.',),
            proof_outline=(
                'Recognize the compact Hausdorff first-countable safe benchmark configuration.',
                'Return the named research path that tracks which additional hypotheses really matter for sharpening the size-bound story.',
            ),
            focus='keep the size-bound research path visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='compactness_variant_research_path',
            theorem_rule_name='countably_compact_comparison_research_path',
            feature='research_path',
            profile_family='research_path',
            profile_keys=('compactness_variant_comparison',),
            required_tags=('countably_compact',),
            result_value='compactness_variant_comparison',
            chapter_targets=('35', '36'),
            assumptions=('Interpret countably compact data as a request to enter the compact-versus-countably-compact comparison corridor.',),
            justification=('The promoted research-path registry records a dedicated compactness-variant comparison path anchored by countably compact warning lines.',),
            proof_outline=(
                'Read the tags as signaling the compactness-comparison corridor rather than a single safe implication.',
                'Return the named path that compares compact, countably compact, and local compact behavior under shared cardinal data.',
            ),
            focus='make the compactness-comparison path visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='fine_cardinal_warning_research_path',
            theorem_rule_name='local_small_global_large_warning_research_path',
            feature='research_path',
            profile_family='research_path',
            profile_keys=('fine_cardinal_warning_lines',),
            required_tags=('local_small_global_large',),
            result_value='fine_cardinal_warning_lines',
            chapter_targets=('32', '33', '34', '36'),
            assumptions=('Interpret the warning tags as requesting the named fine-cardinal warning path, not a general theorem safe zone.',),
            justification=('The promoted research-path registry records fine-cardinal warning lines as the stable route linking tightness, network, and hereditary/local warning surfaces.',),
            proof_outline=(
                'Recognize the local-small/global-large warning configuration.',
                'Return the named path that reopens the fine-cardinal warning line across Chapters 32, 33, 34, and 36.',
            ),
            focus='keep the fine-cardinal warning path visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='counterexample_generation_research_path',
            theorem_rule_name='warning_example_counterexample_research_path',
            feature='research_path',
            profile_family='research_path',
            profile_keys=('counterexample_generation_surface',),
            required_tags=('warning_example',),
            result_value='counterexample_generation_surface',
            chapter_targets=('31', '33', '35', '36'),
            assumptions=('Interpret the warning-example tag as a request for the counterexample-generation route rather than as a settled theorem implication.',),
            justification=('The promoted research-path registry records a dedicated counterexample-generation surface built around named warning examples.',),
            proof_outline=(
                'Treat the warning example as the entry point, not as a conclusion.',
                'Return the named path that organizes counterexample search around the recorded warning anchors.',
            ),
            focus='make the counterexample-generation path visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='module_inventory_research_path',
            theorem_rule_name='registry_alignment_research_path',
            feature='research_path',
            profile_family='research_path',
            profile_keys=('module_and_research_inventory',),
            required_tags=('registry_alignment',),
            result_value='module_and_research_inventory',
            chapter_targets=('34', '35', '36'),
            assumptions=('Interpret the registry-alignment tag as asking for the inventory path that aligns modules, manuscript headings, and report surfaces.',),
            justification=('The promoted research-path registry records a project-alignment path that ties code registries to manuscript and export surfaces.',),
            proof_outline=(
                'Recognize that the query is about registry and export alignment rather than only mathematical implication.',
                'Return the named inventory path that organizes those cross-surface checks.',
            ),
            focus='keep the inventory/alignment path visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='urysohn_metrization_route',
            theorem_rule_name='second_countable_regular_hausdorff_spaces_are_metrizable',
            feature='metrizable',
            profile_family='metrization',
            profile_keys=('urysohn_second_countable_regular_route',),
            required_tags=('second_countable', 'regular', 'hausdorff'),
            result_value='metrizable',
            chapter_targets=('15', '23'),
            assumptions=('Interpret the query as asking for a classical sufficient metrization criterion rather than a converse characterization.',),
            justification=('Every second-countable regular Hausdorff space is metrizable.',),
            proof_outline=(
                'Read the hypothesis as the standard Urysohn metrization corridor.',
                'Use second countability to control the base size and regular Hausdorff separation to build a compatible metric.',
            ),
            focus='make the promoted Urysohn-style route visible through theorem metadata',
        ),
        TheoremProfileAlignment(
            key='compact_second_countable_metrization_route',
            theorem_rule_name='compact_hausdorff_second_countable_spaces_are_metrizable',
            feature='metrizable',
            profile_family='metrization',
            profile_keys=('compact_hausdorff_second_countable_route',),
            required_tags=('compact', 'hausdorff', 'second_countable'),
            result_value='metrizable',
            chapter_targets=('14', '23', '35'),
            assumptions=('Interpret compact Hausdorff second countability as a safe metrization corridor inside the promoted compactness-aware registry line.',),
            justification=('Every compact Hausdorff second-countable space is metrizable.',),
            proof_outline=(
                'Use compact Hausdorff separation to enter the regular/normal compact corridor.',
                'Apply the second-countable metrization criterion inside that corridor.',
            ),
            focus='connect compact Hausdorff second-countable data to a theorem-visible metrization route',
        ),
        TheoremProfileAlignment(
            key='moore_metrization_route',
            theorem_rule_name='regular_developable_hausdorff_spaces_are_metrizable',
            feature='metrizable',
            profile_family='metrization',
            profile_keys=('moore_developable_regular_route',),
            required_tags=('regular', 'developable', 'hausdorff'),
            result_value='metrizable',
            chapter_targets=('23', '36'),
            assumptions=('Interpret the query as invoking the classical Moore-style developable route rather than claiming a universal metrization converse.',),
            justification=('A regular Hausdorff developable space is metrizable.',),
            proof_outline=(
                'Treat developability as the sequence-of-covers input in the Moore metrization theorem.',
                'Combine it with regular Hausdorff separation to recover a compatible metric.',
            ),
            focus='keep the developable route visible as an advanced but still safe theorem-facing line',
        ),
    )


def theorem_profile_alignment_summary() -> dict[str, int]:
    """Return counts by target feature."""

    return dict(Counter(alignment.feature for alignment in get_promoted_theorem_profile_alignments()))


def theorem_profile_family_summary() -> dict[str, int]:
    """Return counts by profile family."""

    return dict(Counter(alignment.profile_family for alignment in get_promoted_theorem_profile_alignments()))


def theorem_profile_feature_index() -> dict[str, tuple[str, ...]]:
    """Return alignment keys grouped by theorem feature."""

    feature_map: dict[str, list[str]] = {}
    for alignment in get_promoted_theorem_profile_alignments():
        feature_map.setdefault(alignment.feature, []).append(alignment.key)
    return {feature: tuple(keys) for feature, keys in sorted(feature_map.items())}


def theorem_profile_index_by_profile_key() -> dict[str, tuple[str, ...]]:
    """Return alignment keys grouped by promoted profile key."""

    profile_map: dict[str, list[str]] = {}
    for alignment in get_promoted_theorem_profile_alignments():
        for profile_key in alignment.profile_keys:
            profile_map.setdefault(profile_key, []).append(alignment.key)
    return {profile_key: tuple(keys) for profile_key, keys in sorted(profile_map.items())}


__all__ = [
    "TheoremProfileAlignment",
    "get_promoted_theorem_profile_alignments",
    "theorem_profile_alignment_summary",
    "theorem_profile_family_summary",
    "theorem_profile_feature_index",
    "theorem_profile_index_by_profile_key",
]
