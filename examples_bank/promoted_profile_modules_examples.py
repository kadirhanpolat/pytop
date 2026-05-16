"""
Promoted profile modules — working examples.

These modules were promoted from pytop.experimental to pytop core.
Each can still be imported from either path for backward compatibility.
Added in v0.5.2.
"""

# ---------------------------------------------------------------------------
# cardinal_function_profiles
# ---------------------------------------------------------------------------
from pytop.cardinal_function_profiles import (
    get_named_cardinal_function_profiles,
    cardinal_function_layer_summary,
    cardinal_function_chapter_index,
)


def example_cardinal_function_profiles():
    profiles = get_named_cardinal_function_profiles()
    first = profiles[0]
    return {
        "total": len(profiles),
        "first_key": first.key,
        "first_display": first.display_name,
        "layer_counts": cardinal_function_layer_summary(),
        "chapters_covered": list(cardinal_function_chapter_index().keys()),
    }


# ---------------------------------------------------------------------------
# compactness_bridges
# ---------------------------------------------------------------------------
from pytop.compactness_bridges import (
    get_named_compactness_bridge_profiles,
    compactness_bridge_layer_summary,
)


def example_compactness_bridges():
    profiles = get_named_compactness_bridge_profiles()
    return {
        "total": len(profiles),
        "families": sorted({p.compactness_family for p in profiles}),
        "layer_counts": compactness_bridge_layer_summary(),
    }


# ---------------------------------------------------------------------------
# compactness_strengthened_profiles
# ---------------------------------------------------------------------------
from pytop.compactness_strengthened_profiles import (
    get_named_compactness_strengthened_profiles,
    compactness_strengthened_layer_summary,
    compactness_strengthened_entry_profiles,
    compactness_strengthened_warning_profiles,
)


def example_compactness_strengthened():
    return {
        "total": len(get_named_compactness_strengthened_profiles()),
        "entry_count": len(compactness_strengthened_entry_profiles()),
        "warning_count": len(compactness_strengthened_warning_profiles()),
        "layer_counts": compactness_strengthened_layer_summary(),
    }


# ---------------------------------------------------------------------------
# classical_inequality_profiles
# ---------------------------------------------------------------------------
from pytop.classical_inequality_profiles import (
    get_named_classical_inequality_profiles,
    classical_inequality_layer_summary,
    classical_inequality_entry_profiles,
    classical_inequality_warning_profiles,
)


def example_classical_inequality_profiles():
    return {
        "total": len(get_named_classical_inequality_profiles()),
        "entry_count": len(classical_inequality_entry_profiles()),
        "warning_count": len(classical_inequality_warning_profiles()),
        "layer_counts": classical_inequality_layer_summary(),
    }


# ---------------------------------------------------------------------------
# hereditary_local_profiles
# ---------------------------------------------------------------------------
from pytop.hereditary_local_profiles import (
    get_named_hereditary_local_profiles,
    hereditary_local_entry_profiles,
    hereditary_local_warning_profiles,
    hereditary_local_quantifier_summary,
)


def example_hereditary_local_profiles():
    profiles = get_named_hereditary_local_profiles()
    first = profiles[0]
    return {
        "total": len(profiles),
        "first_key": first.key,
        "first_comparison_question": first.comparison_question,
        "entry_count": len(hereditary_local_entry_profiles()),
        "warning_count": len(hereditary_local_warning_profiles()),
        "quantifier_counts": hereditary_local_quantifier_summary(),
    }


# ---------------------------------------------------------------------------
# tightness_network_profiles
# ---------------------------------------------------------------------------
from pytop.tightness_network_profiles import (
    get_named_tightness_network_profiles,
    tightness_network_layer_summary,
    tightness_network_entry_profiles,
    tightness_network_advanced_profiles,
)


def example_tightness_network_profiles():
    return {
        "total": len(get_named_tightness_network_profiles()),
        "entry_count": len(tightness_network_entry_profiles()),
        "advanced_count": len(tightness_network_advanced_profiles()),
        "layer_counts": tightness_network_layer_summary(),
    }


# ---------------------------------------------------------------------------
# metrization_profiles
# ---------------------------------------------------------------------------
from pytop.metrization_profiles import (
    get_named_metrization_profiles,
    metrization_layer_summary,
    metrization_chapter_index,
)


def example_metrization_profiles():
    profiles = get_named_metrization_profiles()
    return {
        "total": len(profiles),
        "criterion_families": sorted({p.criterion_family for p in profiles}),
        "layer_counts": metrization_layer_summary(),
        "chapters_covered": list(metrization_chapter_index().keys()),
    }


# ---------------------------------------------------------------------------
# research_bridge_profiles
# ---------------------------------------------------------------------------
from pytop.research_bridge_profiles import (
    get_named_research_bridge_profiles,
    research_bridge_layer_summary,
    research_bridge_chapter_index,
)


def example_research_bridge_profiles():
    profiles = get_named_research_bridge_profiles()
    first = profiles[0]
    return {
        "total": len(profiles),
        "first_key": first.key,
        "first_starting_benchmark": first.starting_benchmark,
        "layer_counts": research_bridge_layer_summary(),
        "chapters_covered": list(research_bridge_chapter_index().keys()),
    }


# ---------------------------------------------------------------------------
# research_path_profiles
# ---------------------------------------------------------------------------
from pytop.research_path_profiles import (
    get_named_research_path_profiles,
    research_path_layer_summary,
    research_path_route_index,
    research_path_chapter_index,
)


def example_research_path_profiles():
    profiles = get_named_research_path_profiles()
    return {
        "total": len(profiles),
        "path_families": sorted({p.path_family for p in profiles}),
        "layer_counts": research_path_layer_summary(),
        "route_index_size": len(research_path_route_index()),
        "chapters_covered": list(research_path_chapter_index().keys()),
    }


# ---------------------------------------------------------------------------
# special_example_profiles
# ---------------------------------------------------------------------------
from pytop.special_example_profiles import (
    get_named_special_example_profiles,
    special_example_role_summary,
    special_example_chapter_index,
)


def example_special_example_profiles():
    profiles = get_named_special_example_profiles()
    return {
        "total": len(profiles),
        "example_roles": special_example_role_summary(),
        "chapters_covered": list(special_example_chapter_index().keys()),
    }


# ---------------------------------------------------------------------------
# theorem_profile_alignment
# ---------------------------------------------------------------------------
from pytop.theorem_profile_alignment import (
    get_promoted_theorem_profile_alignments,
    theorem_profile_alignment_summary,
    theorem_profile_family_summary,
    theorem_profile_feature_index,
)


def example_theorem_profile_alignment():
    alignments = get_promoted_theorem_profile_alignments()
    first = alignments[0]
    return {
        "total": len(alignments),
        "first_key": first.key,
        "first_theorem_rule": first.theorem_rule_name,
        "first_feature": first.feature,
        "result_value": first.result_value,
        "family_counts": theorem_profile_family_summary(),
        "feature_index_size": len(theorem_profile_feature_index()),
    }


if __name__ == "__main__":
    examples = [
        ("cardinal_function_profiles", example_cardinal_function_profiles),
        ("compactness_bridges", example_compactness_bridges),
        ("compactness_strengthened_profiles", example_compactness_strengthened),
        ("classical_inequality_profiles", example_classical_inequality_profiles),
        ("hereditary_local_profiles", example_hereditary_local_profiles),
        ("tightness_network_profiles", example_tightness_network_profiles),
        ("metrization_profiles", example_metrization_profiles),
        ("research_bridge_profiles", example_research_bridge_profiles),
        ("research_path_profiles", example_research_path_profiles),
        ("special_example_profiles", example_special_example_profiles),
        ("theorem_profile_alignment", example_theorem_profile_alignment),
    ]
    for name, fn in examples:
        print(f"--- {name} ---")
        result = fn()
        for k, v in result.items():
            print(f"  {k}: {v}")
        print()
