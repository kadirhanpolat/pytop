from pytop import (
    ManifoldProfileError,
    circle_manifold_profile,
    disk_with_boundary_profile,
    known_manifold_profile,
    manifold_profile,
    manifold_profile_summary,
    projective_plane_manifold_profile,
    real_line_manifold_profile,
    sphere_manifold_profile,
    torus_manifold_profile,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_basic_one_dimensional_manifold_profiles():
    line = real_line_manifold_profile()
    circle = circle_manifold_profile()

    assert line.dimension == 1
    assert line.local_model == "R^1"
    assert line.compact is False
    assert circle.compact is True
    assert circle.orientability == "orientable"
    assert circle.is_certified


def test_sphere_and_disk_profiles_record_boundary_distinction():
    sphere = sphere_manifold_profile(2)
    disk = disk_with_boundary_profile(2)
    summary = manifold_profile_summary(disk)

    assert sphere.dimension == 2
    assert sphere.has_boundary is False
    assert disk.has_boundary is True
    assert disk.metadata["boundary_model"] == "S^1"
    assert "half-space" in summary["local_model"]


def test_surface_examples_record_orientability_without_classifying():
    torus = torus_manifold_profile()
    projective_plane = projective_plane_manifold_profile()

    assert torus.is_surface
    assert torus.orientability == "orientable"
    assert projective_plane.is_surface
    assert projective_plane.orientability == "nonorientable"
    assert any("classification" in warning.lower() for warning in projective_plane.warnings)


def test_registry_known_and_unknown_behaviour():
    assert known_manifold_profile("S2").name == "sphere_S2"
    assert known_manifold_profile("projective plane").orientability == "nonorientable"

    unknown = known_manifold_profile("wild quotient candidate")
    assert unknown.status == "unknown"
    assert unknown.orientability == "unknown"
    assert unknown.is_certified is False


def test_manifold_profile_validation_guardrails():
    _assert_raises(ManifoldProfileError, manifold_profile, "bad", -1, local_model="R^-1")
    _assert_raises(ManifoldProfileError, manifold_profile, "bad", 2, local_model="R^2", orientability="maybe")
    _assert_raises(ManifoldProfileError, manifold_profile, "bad", 2, local_model="")
    _assert_raises(ManifoldProfileError, sphere_manifold_profile, 0)
    _assert_raises(ManifoldProfileError, disk_with_boundary_profile, 0)
