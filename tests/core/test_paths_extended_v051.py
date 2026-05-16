"""Coverage-targeted tests for paths.py (v0.5.1)."""
import pytest
from pytop.paths import (
    PathProfile,
    PathProfileError,
    PathConnectednessDiagnostic,
    path_profile,
    concatenate_path_profiles,
    path_connectedness_diagnostic,
    _combined_certification,
)


# ---------------------------------------------------------------------------
# PathProfile.__post_init__ — line 31 (empty name raises)
# ---------------------------------------------------------------------------

def test_path_profile_empty_name_raises():
    with pytest.raises(PathProfileError, match="nonempty name"):
        PathProfile(name="   ", start=0, end=1)


# ---------------------------------------------------------------------------
# PathProfile.__post_init__ — line 37 (last point != end raises)
# ---------------------------------------------------------------------------

def test_path_profile_last_point_mismatch_raises():
    # First point matches start (0), but last point (1) != end (99)
    with pytest.raises(PathProfileError, match="last sampled point"):
        PathProfile(name="bad_path", start=0, end=99, points=(0, 1))


# ---------------------------------------------------------------------------
# PathProfile.concatenate — line 63 (end != other.start raises)
# ---------------------------------------------------------------------------

def test_concatenate_mismatched_endpoints_raises():
    p1 = path_profile("p1", start=0, end=1, points=(0, 1))
    p2 = path_profile("p2", start=5, end=6, points=(5, 6))
    with pytest.raises(PathProfileError, match="concatenated only when"):
        concatenate_path_profiles(p1, p2)


# ---------------------------------------------------------------------------
# path_connectedness_diagnostic — line 133 (empty carrier raises)
# ---------------------------------------------------------------------------

def test_path_connectedness_empty_carrier_raises():
    with pytest.raises(PathProfileError, match="nonempty carrier"):
        path_connectedness_diagnostic([], [])


# ---------------------------------------------------------------------------
# path_connectedness_diagnostic — line 137 (endpoint outside carrier raises)
# ---------------------------------------------------------------------------

def test_path_connectedness_endpoint_outside_carrier_raises():
    p = path_profile("edge", start=1, end=99, points=(1, 99))
    with pytest.raises(PathProfileError, match="must belong to the carrier"):
        path_connectedness_diagnostic([1, 2], [p])


# ---------------------------------------------------------------------------
# _combined_certification — line 183 (different certifications)
# ---------------------------------------------------------------------------

def test_combined_certification_different_returns_composite():
    result = _combined_certification("certified", "profile")
    assert result == "composite-profile"


def test_combined_certification_same_returns_same():
    result = _combined_certification("certified", "certified")
    assert result == "certified"
