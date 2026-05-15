from pytop.research_bridge_profiles import get_named_research_bridge_profiles as get_core_profiles
from pytop_experimental.research_bridge_profiles import (
    get_named_research_bridge_profiles,
    research_bridge_layer_summary,
)


def test_research_bridge_registry_has_expected_routes():
    profiles = get_named_research_bridge_profiles()
    keys = {profile.key for profile in profiles}
    assert 'safe_zone_sharpness_route' in keys
    assert 'compactification_upgrade_route' in keys
    assert 'future_threshold_release_route' in keys


def test_research_bridge_registry_layers_are_curated():
    assert research_bridge_layer_summary() == {
        'main_text': 2,
        'selected_block': 2,
        'advanced_note': 1,
    }


def test_research_bridge_registry_is_a_compatibility_wrapper():
    assert get_named_research_bridge_profiles() == get_core_profiles()
