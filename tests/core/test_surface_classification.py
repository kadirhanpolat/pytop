"""pytop.surface_classification icin MAN-01 testleri."""

from pytop.surface_classification import (
    CompactSurfaceClassificationProfile,
    compact_surface_classification_registry,
    get_compact_surface_classification_profiles,
    surface_euler_characteristic_summary,
    surface_orientability_summary,
)


def test_surface_profiles_cover_classical_compact_examples():
    profiles = get_compact_surface_classification_profiles()
    assert isinstance(profiles, tuple)
    assert len(profiles) >= 5
    assert all(isinstance(p, CompactSurfaceClassificationProfile) for p in profiles)
    keys = {p.key for p in profiles}
    assert {"sphere_surface", "torus_surface", "projective_plane_surface"}.issubset(keys)


def test_surface_profiles_have_euler_and_source_data():
    profiles = get_compact_surface_classification_profiles()
    assert all("Adams & Franzosa" in p.source_section for p in profiles)
    summary = surface_euler_characteristic_summary()
    assert summary["sphere_surface"] == 2
    assert summary["torus_surface"] == 0
    assert summary["klein_bottle_surface"] == 0


def test_surface_orientability_summary_distinguishes_families():
    summary = surface_orientability_summary()
    assert "sphere_surface" in summary["orientable"]
    assert "double_torus_surface" in summary["orientable"]
    assert "projective_plane_surface" in summary["nonorientable"]
    assert "klein_bottle_surface" in summary["nonorientable"]


def test_surface_registry_counts_match_getter():
    registry = compact_surface_classification_registry()
    assert registry["compact_surface_classification_profiles"] == len(
        get_compact_surface_classification_profiles()
    )
