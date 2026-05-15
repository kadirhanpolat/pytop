from pytop import (
    EuclideanTopologyProfileError,
    closed_disk_profile,
    euclidean_topology_profile,
    euclidean_profile_summary,
    known_euclidean_profile,
    open_ball_profile,
    projective_preview_profile,
    punctured_sphere_profile,
    sphere_profile,
    stereographic_projection_profile,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_open_ball_and_closed_disk_profiles():
    ball = open_ball_profile(2)
    disk = closed_disk_profile(2)

    assert ball.kind == "open_ball"
    assert ball.ambient_dimension == 2
    assert disk.boundary == "S^1"
    assert disk.metadata["boundary_dimension"] == 1
    assert disk.has_boundary


def test_sphere_and_punctured_sphere_profiles():
    sphere = sphere_profile(2)
    punctured = punctured_sphere_profile(2)

    assert sphere.model == "S^2 subset R^3"
    assert sphere.intrinsic_dimension == 2
    assert punctured.status == "preview"
    assert "R^2" in punctured.intuition
    assert punctured.is_preview


def test_stereographic_projection_profile_is_preview_only():
    profile = stereographic_projection_profile(2)
    summary = euclidean_profile_summary(profile)

    assert summary["kind"] == "stereographic_projection"
    assert summary["status"] == "preview"
    assert any("No coordinate proof" in warning for warning in summary["warnings"])


def test_projective_preview_profiles_do_not_classify():
    line = projective_preview_profile("projective_line")
    plane = projective_preview_profile("projective_plane")
    unknown = projective_preview_profile("projective_three_space")

    assert "antipodal" in line.model
    assert plane.status == "preview"
    assert unknown.status == "unknown"


def test_known_euclidean_registry_and_unknown_fallback():
    known = known_euclidean_profile("sphere_S2")
    unknown = known_euclidean_profile("mystery geometry")

    assert known.kind == "sphere"
    assert unknown.status == "unknown"


def test_euclidean_profile_validation():
    _assert_raises(
        EuclideanTopologyProfileError,
        euclidean_topology_profile,
        "bad",
        "unsupported_kind",
    )
    _assert_raises(EuclideanTopologyProfileError, sphere_profile, -1)
    _assert_raises(EuclideanTopologyProfileError, closed_disk_profile, 0)
