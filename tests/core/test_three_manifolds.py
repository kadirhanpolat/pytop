"""pytop.three_manifolds icin MAN-02 testleri."""

from pytop.three_manifolds import (
    ThreeManifoldInvariantProfile,
    ThreeManifoldProfile,
    get_three_manifold_invariant_profiles,
    get_three_manifold_profiles,
    three_manifold_family_summary,
    three_manifold_invariant_kind_summary,
    three_manifold_profile_registry,
)


def test_three_manifold_profiles_cover_classical_families():
    profiles = get_three_manifold_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 4
    assert all(isinstance(profile, ThreeManifoldProfile) for profile in profiles)
    families = {profile.model_family for profile in profiles}
    assert {"sphere", "lens_space", "seifert_fibered", "torus_bundle"}.issubset(
        families
    )


def test_three_manifold_profiles_have_source_and_compactness_data():
    profiles = get_three_manifold_profiles()
    assert all("Adams & Franzosa" in profile.source_section for profile in profiles)
    by_key = {profile.key: profile for profile in profiles}
    assert by_key["three_sphere_baseline"].compactness == "compact"
    assert by_key["lens_space_l_p_q"].orientability == "orientable"
    assert "Monodromy" in by_key["torus_bundle_mapping_torus"].primary_invariant_signal


def test_three_manifold_family_summary_groups_profiles():
    summary = three_manifold_family_summary()
    assert "three_sphere_baseline" in summary["sphere"]
    assert "lens_space_l_p_q" in summary["lens_space"]
    assert "seifert_fibered_space" in summary["seifert_fibered"]
    assert "torus_bundle_mapping_torus" in summary["torus_bundle"]


def test_three_manifold_invariant_profiles_cover_core_signals():
    profiles = get_three_manifold_invariant_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 3
    assert all(isinstance(profile, ThreeManifoldInvariantProfile) for profile in profiles)
    kinds = {profile.invariant_kind for profile in profiles}
    assert {"fundamental_group", "fibration_data", "monodromy"}.issubset(kinds)


def test_three_manifold_invariant_summary_groups_profiles():
    summary = three_manifold_invariant_kind_summary()
    assert "lens_space_fundamental_group_signal" in summary["fundamental_group"]
    assert "seifert_fibration_signal" in summary["fibration_data"]
    assert "torus_bundle_monodromy_signal" in summary["monodromy"]


def test_three_manifold_registry_counts_match_getters():
    registry = three_manifold_profile_registry()
    assert registry["three_manifold_profiles"] == len(get_three_manifold_profiles())
    assert registry["three_manifold_invariant_profiles"] == len(
        get_three_manifold_invariant_profiles()
    )
    assert sum(registry.values()) >= 7
