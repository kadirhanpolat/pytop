from pytop import (
    CoveringSpaceProfileError,
    assumed_covering_map_profile,
    circle_degree_covering_profile,
    covering_map_profile,
    covering_profile_summary,
    known_covering_profile,
    unknown_covering_map_profile,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_real_line_to_circle_registry_profile():
    profile = known_covering_profile("real line to circle")
    summary = covering_profile_summary(profile)

    assert profile.is_certified
    assert summary["total_space"] == "R"
    assert summary["base_space"] == "S^1"
    assert summary["sheet_count"] == "countably infinite"
    assert "pi_1(S^1)" in summary["fundamental_group_note"]


def test_circle_degree_covering_profile_records_degree_and_pi1_note():
    profile = circle_degree_covering_profile(4)

    assert profile.sheet_count == 4
    assert profile.metadata["degree"] == 4
    assert "multiplies by 4" in profile.fundamental_group_note
    _assert_raises(CoveringSpaceProfileError, circle_degree_covering_profile, 0)


def test_trivial_two_sheet_cover_is_registered():
    profile = known_covering_profile("trivial_two_sheet_cover")

    assert profile.status == "certified"
    assert profile.sheet_count == 2
    assert profile.covering_map == "projection to B"


def test_assumed_covering_profile_keeps_local_homeomorphism_warning():
    profile = assumed_covering_map_profile("candidate", "E", "B", sheet_count="finite")

    assert profile.status == "assumed"
    assert profile.local_homeomorphism_assumption == "assumed"
    assert profile.has_local_homeomorphism_warning


def test_unknown_covering_profile_does_not_overclaim():
    profile = known_covering_profile("mystery cover")
    explicit = unknown_covering_map_profile("unknown", "E", "B")

    assert profile.status == "unknown"
    assert explicit.status == "unknown"
    assert explicit.is_certified is False


def test_covering_profile_validation_rejects_bad_status_and_sheet_count():
    _assert_raises(
        CoveringSpaceProfileError,
        covering_map_profile,
        "bad status",
        "E",
        "B",
        status="proved_by_magic",
    )
    _assert_raises(
        CoveringSpaceProfileError,
        covering_map_profile,
        "bad sheet count",
        "E",
        "B",
        sheet_count=0,
    )
