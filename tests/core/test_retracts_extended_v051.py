"""Coverage-targeted tests for retracts.py (v0.5.1)."""
from pytop.retracts import known_absolute_retract_profile


# ---------------------------------------------------------------------------
# known_absolute_retract_profile — line 416 (profile found → return profile)
# ---------------------------------------------------------------------------

def test_known_absolute_retract_profile_found():
    profile = known_absolute_retract_profile("disk")
    assert profile is not None
    assert profile.status != "unknown"


def test_known_absolute_retract_profile_interval():
    profile = known_absolute_retract_profile("interval")
    assert profile is not None
