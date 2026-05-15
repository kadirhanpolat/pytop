"""pytop.cosmology_topology icin MAN-03 testleri."""

from pytop.cosmology_topology import (
    CosmicTopologyObservationProfile,
    UniverseGeometryProfile,
    cosmic_observation_method_summary,
    cosmology_topology_profile_registry,
    get_cosmic_topology_observation_profiles,
    get_universe_geometry_profiles,
    universe_geometry_summary,
)


def test_universe_geometry_profiles_cover_three_geometry_signals():
    profiles = get_universe_geometry_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(profile, UniverseGeometryProfile) for profile in profiles)
    geometries = {profile.local_geometry for profile in profiles}
    assert {"positive_curvature", "zero_curvature", "negative_curvature"}.issubset(
        geometries
    )


def test_universe_geometry_profiles_have_source_and_models():
    profiles = get_universe_geometry_profiles()
    assert all("Adams & Franzosa" in profile.source_section for profile in profiles)
    by_key = {profile.key: profile for profile in profiles}
    assert "3-torus" in by_key["flat_universe_models"].model_examples
    assert by_key["spherical_universe_models"].compactness_signal
    assert "H^3" in by_key["hyperbolic_universe_models"].curvature_signal


def test_cosmic_observation_profiles_cover_core_detection_methods():
    profiles = get_cosmic_topology_observation_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(profile, CosmicTopologyObservationProfile) for profile in profiles)
    methods = {profile.observation_method for profile in profiles}
    assert {
        "cosmic_crystallography",
        "matched_circles_in_cmb",
        "cmb_temperature_pattern_comparison",
    }.issubset(methods)


def test_cosmology_summaries_group_profiles():
    geometry_summary = universe_geometry_summary()
    observation_summary = cosmic_observation_method_summary()
    assert "flat_universe_models" in geometry_summary["zero_curvature"]
    assert "circles_in_the_sky_pattern" in observation_summary["matched_circles_in_cmb"]


def test_cosmology_topology_registry_counts_match_getters():
    registry = cosmology_topology_profile_registry()
    assert registry["universe_geometry_profiles"] == len(get_universe_geometry_profiles())
    assert registry["cosmic_topology_observation_profiles"] == len(
        get_cosmic_topology_observation_profiles()
    )
    assert sum(registry.values()) >= 6
