from pytop import (
    HomotopyProfileError,
    contractible_profile,
    contractible_summary,
    deformation_retraction_profile,
    deformation_retraction_summary,
    homotopic,
    homotopy_profile,
    homotopy_summary,
    known_contractible_profile,
    not_certified_homotopy,
    unknown_homotopy,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_homotopic_profile_records_relative_label_and_witness():
    profile = homotopic(
        "straight_path",
        "curved_path",
        relative_to={"start", "end"},
        witness="endpoint-fixed homotopy",
    )

    summary = homotopy_summary(profile)

    assert profile.is_certified_homotopy
    assert profile.has_relative_label
    assert summary["status"] == "homotopic"
    assert summary["relative_to"] == ("end", "start")
    assert summary["has_witness"] is True


def test_not_certified_and_unknown_do_not_overclaim():
    missing = not_certified_homotopy("map_f", "map_g")
    unknown = unknown_homotopy("map_h", "map_k")

    assert missing.status == "not_certified"
    assert missing.is_certified_homotopy is False
    assert missing.metadata["reason"]
    assert unknown.status == "unknown"
    assert unknown.certification == "unknown"


def test_status_validation_rejects_definite_negative_shortcut():
    _assert_raises(HomotopyProfileError, homotopy_profile, "bad", "f", "g", status="not_homotopic")


def test_known_contractible_registry_is_safe_and_limited():
    interval = known_contractible_profile("closed interval")
    circle = known_contractible_profile("circle")

    assert interval.status == "certified"
    assert interval.is_certified_contractible
    assert contractible_summary(interval)["has_witness"] is True
    assert circle.status == "unknown"
    assert circle.is_certified_contractible is False


def test_deformation_retraction_profile_keeps_certification_label():
    profile = deformation_retraction_profile(
        "annulus_core_profile",
        space="annulus",
        subspace="core circle",
        status="not_certified",
        strong=True,
        notes=("symbolic profile",),
    )

    summary = deformation_retraction_summary(profile)

    assert summary["status"] == "not_certified"
    assert summary["strong"] is True
    assert summary["notes"] == ("symbolic profile",)


def test_contractible_profile_unknown_by_default():
    profile = contractible_profile("space_x")

    assert profile.status == "unknown"
    assert profile.is_certified_contractible is False
