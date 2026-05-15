from pytop import (
    ANRProfile,
    AbsoluteRetractProfile,
    DeformationRetractionProfile,
    RetractProfileError,
    RetractionProfile,
    absolute_retract_profile,
    absolute_retract_summary,
    anr_profile,
    anr_summary,
    certified_retraction_profile,
    deformation_retract_profile,
    disk_ar_profile,
    finite_polyhedron_anr_profile,
    interval_ar_profile,
    is_certified_absolute_retract,
    is_certified_anr,
    is_certified_retract,
    known_absolute_retract_profile,
    known_anr_profile,
    not_certified_retraction_profile,
    point_ar_profile,
    retraction_profile,
    retraction_summary,
    topological_manifold_anr_profile,
    unknown_retraction_profile,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_retraction_profile_certified_unknown_and_not_certified():
    certified = certified_retraction_profile(
        "annulus_to_core",
        "annulus",
        "core circle",
        retraction_label="radial projection",
        deformation_available=True,
        strong_deformation=True,
        homotopy_equivalence_hint="same homotopy type as S^1",
    )
    unknown = unknown_retraction_profile("mystery", "X", "A")
    failed = not_certified_retraction_profile("bad", "X", "A")

    assert isinstance(certified, RetractionProfile)
    assert is_certified_retract(certified)
    assert retraction_summary(certified)["is_deformation_retract"] is True
    assert unknown.status == "unknown"
    assert failed.status == "not_certified"
    assert failed.fixed_on_subspace is False


def test_deformation_retract_profile_reuses_homotopy_layer():
    profile = deformation_retract_profile(
        "disk_to_point",
        "D^2",
        "{0}",
        status="certified",
        strong=True,
        notes=("standard contraction profile",),
    )

    assert isinstance(profile, DeformationRetractionProfile)
    assert profile.status == "certified"
    assert profile.strong is True
    assert "standard" in profile.notes[0]


def test_absolute_retract_registry_and_summaries():
    point = point_ar_profile()
    interval = interval_ar_profile()
    disk = disk_ar_profile()
    unknown = known_absolute_retract_profile("wild continuum")

    assert isinstance(point, AbsoluteRetractProfile)
    assert is_certified_absolute_retract(point)
    assert interval.status == "certified"
    assert "convex" in interval.contractibility_hint
    assert disk.status == "certified"
    assert absolute_retract_summary(unknown)["status"] == "unknown"
    assert unknown.is_certified_ar is False


def test_anr_registry_certified_and_preview_profiles():
    polyhedron = finite_polyhedron_anr_profile()
    circle = known_anr_profile("circle")
    manifold = topological_manifold_anr_profile()
    unknown = known_anr_profile("unknown quotient")

    assert isinstance(polyhedron, ANRProfile)
    assert is_certified_anr(polyhedron)
    assert circle.status == "certified"
    assert manifold.status == "preview"
    assert "manifold" in anr_summary(manifold)["manifold_or_polyhedron_hint"]
    assert unknown.status == "unknown"


def test_manual_profile_builders_keep_unknown_as_unknown():
    retract = retraction_profile("manual", "X", "A", status="unknown")
    ar = absolute_retract_profile("manual_ar", "Y", status="unknown")
    anr = anr_profile("manual_anr", "Z", status="unknown")

    assert retract.is_unknown
    assert ar.is_certified_ar is False
    assert anr.is_certified_anr is False
    assert retraction_summary(retract)["status"] == "unknown"
    assert absolute_retract_summary(ar)["status"] == "unknown"
    assert anr_summary(anr)["status"] == "unknown"


def test_validation_guardrails():
    _assert_raises(RetractProfileError, retraction_profile, "", "X", "A")
    _assert_raises(RetractProfileError, retraction_profile, "bad", "X", "A", status="maybe")
    _assert_raises(RetractProfileError, absolute_retract_profile, "", "X")
    _assert_raises(RetractProfileError, absolute_retract_profile, "bad", "X", status="maybe")
    _assert_raises(RetractProfileError, anr_profile, "", "X")
    _assert_raises(RetractProfileError, anr_profile, "bad", "X", status="maybe")
