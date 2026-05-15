from pytop import (
    ContinuumProfileError,
    cantor_set_noncontinuum_profile,
    circle_continuum_profile,
    continuum_condition_report,
    continuum_profile,
    continuum_profile_summary,
    disk_continuum_profile,
    hilbert_cube_profile,
    interval_continuum_profile,
    is_continuum_profile,
    known_continuum_profile,
    non_continuum_profile,
    topologist_sine_curve_profile,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_standard_certified_continua_have_required_conditions():
    interval = interval_continuum_profile()
    circle = circle_continuum_profile()
    disk = disk_continuum_profile()

    for profile in (interval, circle, disk):
        assert profile.compact is True
        assert profile.connected is True
        assert profile.metric is True
        assert profile.nonempty is True
        assert profile.continuum is True
        assert profile.is_certified_continuum
        assert continuum_condition_report(profile)["verdict"] == "continuum"

    assert circle.metadata["standard_notation"] == "S^1"
    assert disk.metadata["boundary_model"] == "S^1"


def test_cantor_set_is_registered_as_noncontinuum_counterexample():
    cantor = cantor_set_noncontinuum_profile()
    report = continuum_condition_report(cantor)
    summary = continuum_profile_summary(cantor)

    assert cantor.compact is True
    assert cantor.metric is True
    assert cantor.connected is False
    assert cantor.continuum is False
    assert cantor.is_known_noncontinuum
    assert report["verdict"] == "not_continuum"
    assert summary["is_known_noncontinuum"] is True
    assert "not connected" in " ".join(cantor.warnings).lower()


def test_hilbert_cube_and_topologist_sine_curve_are_conservative_profiles():
    cube = hilbert_cube_profile()
    sine = topologist_sine_curve_profile()

    assert cube.continuum is True
    assert cube.is_certified_continuum
    assert cube.metadata["standard_notation"] == "I^omega"
    assert any("functional-analysis" in warning for warning in cube.warnings)
    assert sine.continuum is True
    assert sine.status == "preview"
    assert not sine.is_certified_continuum
    assert "not locally connected" in sine.local_connectedness_hint


def test_registry_summary_and_unknown_behavior():
    by_name = known_continuum_profile("unit interval")
    unknown = known_continuum_profile("wild continuum candidate")

    assert by_name.name == "closed_interval_I"
    assert is_continuum_profile(by_name) is True
    assert unknown.status == "unknown"
    assert unknown.continuum is None
    assert is_continuum_profile(unknown) is None
    assert "no recognition claim" in " ".join(unknown.warnings).lower()


def test_continuum_profile_validation_guardrails():
    _assert_raises(ContinuumProfileError, continuum_profile, "bad", status="invalid")
    _assert_raises(
        ContinuumProfileError,
        continuum_profile,
        "bad continuum",
        compact=True,
        connected=False,
        metric=True,
        nonempty=True,
        continuum=True,
    )
    _assert_raises(
        ContinuumProfileError,
        continuum_profile,
        "bad counterexample",
        continuum=None,
        status="counterexample",
    )

    profile = non_continuum_profile(
        "two_point_discrete_space",
        compact=True,
        connected=False,
        metric=True,
        reason="Disconnected finite metric example.",
    )
    assert profile.continuum is False
    assert profile.status == "counterexample"
