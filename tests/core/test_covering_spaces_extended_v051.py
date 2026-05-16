"""Coverage-targeted tests for covering_spaces.py (v0.5.1)."""
import pytest
from pytop.covering_spaces import (
    CoveringSpaceProfileError,
    CoveringMapProfile,
)


# ---------------------------------------------------------------------------
# CoveringMapProfile — line 42 (empty name after valid status check)
# ---------------------------------------------------------------------------

def test_covering_map_profile_empty_name_raises():
    with pytest.raises(CoveringSpaceProfileError, match="nonempty name"):
        CoveringMapProfile(name="   ", total_space="E", base_space="B", status="unknown")


def test_covering_map_profile_invalid_status_raises():
    with pytest.raises(CoveringSpaceProfileError, match="Unsupported covering profile status"):
        CoveringMapProfile(name="p", total_space="E", base_space="B", status="bad_status")


def test_covering_map_profile_valid():
    p = CoveringMapProfile(name="p", total_space="R", base_space="S1", sheet_count="infinite", status="certified")
    assert p.is_certified


def test_covering_map_profile_negative_sheet_count_raises():
    with pytest.raises(CoveringSpaceProfileError, match="positive"):
        CoveringMapProfile(name="p", total_space="E", base_space="B", sheet_count=-1, status="unknown")
