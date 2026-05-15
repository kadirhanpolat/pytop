from pytop_experimental.research_path_registry import (
    get_named_research_path_profiles,
    research_path_chapter_index,
    research_path_layer_summary,
    research_path_route_index,
)


def test_research_path_registry_has_expected_keys():
    profiles = get_named_research_path_profiles()
    keys = {profile.key for profile in profiles}
    assert "hypothesis_sensitivity_of_size_bounds" in keys
    assert "compactness_variant_comparison" in keys
    assert "module_and_research_inventory" in keys



def test_research_path_layers_are_curated():
    profiles = get_named_research_path_profiles()
    layers = {profile.presentation_layer for profile in profiles}
    assert layers == {"main_text", "selected_block", "advanced_note"}
    summary = research_path_layer_summary()
    assert summary == {"main_text": 2, "selected_block": 2, "advanced_note": 1}


def test_research_paths_include_cross_links_and_start_routes():
    profiles = get_named_research_path_profiles()
    compactness = next(profile for profile in profiles if profile.key == "compactness_variant_comparison")
    assert compactness.example_bank_file == "compactness_cardinal_functions_examples.md"
    assert "compact_first_countable_continuum_bound" in compactness.theorem_draft_keys
    assert "compactification_upgrade_route" in compactness.bridge_route_keys
    assert "countably_compact_warning_anchor" in compactness.special_example_keys
    assert "Begin" in compactness.start_here
    assert '36' in research_path_chapter_index()
    assert 'module_and_research_inventory' in research_path_route_index()['registry_alignment_demo_space']
