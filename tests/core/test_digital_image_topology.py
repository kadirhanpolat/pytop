"""pytop.digital_image_topology için EMB-02 testleri."""

from pytop.digital_image_topology import (
    DigitalAdjacencyProfile,
    DigitalCurveProfile,
    DigitalImageSegmentationProfile,
    digital_image_topology_registry,
    get_digital_adjacency_profiles,
    get_digital_curve_profiles,
    get_digital_image_segmentation_profiles,
)


def test_digital_adjacency_profiles_cover_four_and_eight_adjacency():
    profiles = get_digital_adjacency_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, DigitalAdjacencyProfile) for p in profiles)
    kinds = {p.adjacency_kind for p in profiles}
    assert "4-adjacency" in kinds
    assert "8-adjacency" in kinds


def test_adjacency_profiles_are_turkish_teaching_records():
    profiles = get_digital_adjacency_profiles()
    assert all("bağlı" in p.display_name.lower() for p in profiles)
    assert all("Adams & Franzosa" in p.source_section for p in profiles)


def test_digital_curve_profiles_explain_separation_behavior():
    profiles = get_digital_curve_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, DigitalCurveProfile) for p in profiles)
    assert all("ayr" in p.separation_behavior.lower() or "bağlı" in p.separation_behavior.lower()
               for p in profiles)


def test_simple_closed_curve_uses_four_eight_pairing():
    profiles = {p.key: p for p in get_digital_curve_profiles()}
    profile = profiles["simple_closed_digital_curve_4_8"]
    assert profile.foreground_adjacency == "4-adjacency"
    assert profile.background_adjacency == "8-adjacency"
    assert "Jordan" in profile.teaching_note


def test_segmentation_profiles_have_failure_modes():
    profiles = get_digital_image_segmentation_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 2
    assert all(isinstance(p, DigitalImageSegmentationProfile) for p in profiles)
    assert all(p.failure_mode for p in profiles)


def test_foreground_background_duality_mentions_both_rules():
    profiles = {p.key: p for p in get_digital_image_segmentation_profiles()}
    profile = profiles["foreground_background_duality"]
    assert "4-bağlılık" in profile.topology_signal
    assert "8-bağlılık" in profile.topology_signal


def test_digital_image_topology_registry_counts_match_getters():
    registry = digital_image_topology_registry()
    assert registry["digital_adjacency_profiles"] == len(get_digital_adjacency_profiles())
    assert registry["digital_curve_profiles"] == len(get_digital_curve_profiles())
    assert registry["digital_image_segmentation_profiles"] == len(
        get_digital_image_segmentation_profiles()
    )
    assert sum(registry.values()) >= 6
