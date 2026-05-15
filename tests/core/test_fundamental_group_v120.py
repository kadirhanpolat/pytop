from pytop import (
    FundamentalGroupProfileError,
    free_group_profile,
    fundamental_group_profile,
    fundamental_group_summary,
    infinite_cyclic_group_profile,
    known_fundamental_group_profile,
    trivial_group_profile,
    unknown_fundamental_group_profile,
)


def _assert_raises(error_type, callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except error_type:
        return
    raise AssertionError(f"{error_type.__name__} was not raised")


def test_trivial_group_profile_records_basepoint_and_certification():
    profile = trivial_group_profile("contractible space", basepoint="x0")
    summary = fundamental_group_summary(profile)

    assert profile.is_certified
    assert profile.is_trivial
    assert summary["basepoint"] == "x0"
    assert summary["kind"] == "trivial"
    assert summary["rank"] == 0
    assert summary["generators"] == ()


def test_circle_registry_is_infinite_cyclic():
    profile = known_fundamental_group_profile("circle")

    assert profile.kind == "infinite_cyclic"
    assert profile.status == "certified"
    assert profile.rank == 1
    assert profile.generators == ("loop",)


def test_free_group_profile_requires_rank_generator_consistency():
    profile = free_group_profile("wedge of two circles", basepoint="*", generators=("a", "b"))

    assert profile.kind == "free"
    assert profile.rank == 2
    assert profile.presentation == "< a, b | >"
    _assert_raises(
        FundamentalGroupProfileError,
        fundamental_group_profile,
        "bad free profile",
        kind="free",
        status="certified",
        rank=2,
        generators=("a",),
    )


def test_infinite_cyclic_profile_requires_one_generator():
    profile = infinite_cyclic_group_profile("circle", generator="z")

    assert profile.generators == ("z",)
    assert profile.presentation == "< z | >"
    _assert_raises(
        FundamentalGroupProfileError,
        fundamental_group_profile,
        "bad cyclic profile",
        kind="infinite_cyclic",
        status="certified",
        generators=("a", "b"),
    )


def test_unknown_registry_lookup_does_not_overclaim():
    profile = known_fundamental_group_profile("mystery_space")
    explicit = unknown_fundamental_group_profile("another_space")

    assert profile.status == "unknown"
    assert profile.kind == "profile"
    assert explicit.status == "unknown"
    assert explicit.is_certified is False


def test_basepoint_relabel_is_marked_as_profile_metadata():
    profile = known_fundamental_group_profile("circle", basepoint="other")

    assert profile.basepoint == "other"
    assert profile.metadata["basepoint_relabel"] is True
    assert any("Basepoint was relabeled" in note for note in profile.notes)
