from pytop.paths import (
    PathProfileError,
    concatenate_path_profiles,
    is_loop_path,
    path_connectedness_diagnostic,
    path_profile,
    path_profile_summary,
    reverse_path_profile,
)


def test_path_profile_records_endpoints_samples_and_loop_status():
    path = path_profile("arc", "a", "b", points=("a", "m", "b"))
    loop = path_profile("loop", "a", "a", points=("a", "m", "a"))

    assert path.start == "a"
    assert path.end == "b"
    assert path_profile_summary(path)["sample_count"] == 3
    assert is_loop_path(path) is False
    assert is_loop_path(loop) is True


def test_path_profile_rejects_sample_endpoint_mismatch():
    try:
        path_profile("bad", "a", "b", points=("x", "b"))
    except PathProfileError:
        pass
    else:
        raise AssertionError("sample endpoint mismatch should be rejected")


def test_reverse_and_concatenate_path_profiles():
    ab = path_profile("ab", "a", "b", points=("a", "b"))
    bc = path_profile("bc", "b", "c", points=("b", "c"))

    ba = reverse_path_profile(ab)
    ac = concatenate_path_profiles(ab, bc, name="ac")

    assert ba.start == "b"
    assert ba.end == "a"
    assert ac.start == "a"
    assert ac.end == "c"
    assert ac.points == ("a", "b", "c")


def test_concatenate_rejects_nonmatching_endpoints():
    ab = path_profile("ab", "a", "b", points=("a", "b"))
    cd = path_profile("cd", "c", "d", points=("c", "d"))

    try:
        concatenate_path_profiles(ab, cd)
    except PathProfileError:
        pass
    else:
        raise AssertionError("nonmatching endpoints should be rejected")


def test_path_connectedness_diagnostic_uses_recorded_paths_only():
    ab = path_profile("ab", "a", "b", points=("a", "b"))
    cd = path_profile("cd", "c", "d", points=("c", "d"))

    disconnected = path_connectedness_diagnostic({"a", "b", "c", "d"}, [ab, cd])
    connected = path_connectedness_diagnostic({"a", "b", "c"}, [ab, path_profile("bc", "b", "c", points=("b", "c"))])

    assert disconnected.connected is False
    assert disconnected.components == (frozenset({"a", "b"}), frozenset({"c", "d"}))
    assert connected.connected is True
    assert any("Connectedness and path-connectedness are distinct" in note for note in connected.notes)
