"""Coverage-targeted tests for fundamental_group.py (v0.5.1)."""
import pytest
from pytop.fundamental_group import (
    FundamentalGroupProfile,
    FundamentalGroupProfileError,
    fundamental_group_profile,
)


# ---------------------------------------------------------------------------
# FundamentalGroupProfile.__post_init__ — line 41 (invalid kind)
# ---------------------------------------------------------------------------

def test_invalid_kind_raises():
    with pytest.raises(FundamentalGroupProfileError, match="kind"):
        FundamentalGroupProfile(space="X", kind="abelian", status="unknown")


# ---------------------------------------------------------------------------
# FundamentalGroupProfile.__post_init__ — line 43 (invalid status)
# ---------------------------------------------------------------------------

def test_invalid_status_raises():
    with pytest.raises(FundamentalGroupProfileError, match="status"):
        FundamentalGroupProfile(space="X", kind="profile", status="maybe")


# ---------------------------------------------------------------------------
# FundamentalGroupProfile.__post_init__ — line 46 (negative rank)
# ---------------------------------------------------------------------------

def test_negative_rank_raises():
    with pytest.raises(FundamentalGroupProfileError, match="negative"):
        FundamentalGroupProfile(space="X", kind="profile", status="unknown", rank=-1)


# ---------------------------------------------------------------------------
# FundamentalGroupProfile.__post_init__ — line 48 (trivial + generators)
# ---------------------------------------------------------------------------

def test_trivial_with_generators_raises():
    with pytest.raises(FundamentalGroupProfileError, match="trivial"):
        FundamentalGroupProfile(
            space="X",
            kind="trivial",
            status="certified",
            generators=("a",),
            rank=0,
        )


# ---------------------------------------------------------------------------
# FundamentalGroupProfile.__post_init__ — line 50 (free + no rank)
# ---------------------------------------------------------------------------

def test_free_without_rank_raises():
    with pytest.raises(FundamentalGroupProfileError, match="rank"):
        FundamentalGroupProfile(
            space="X",
            kind="free",
            status="certified",
            generators=("a",),
            rank=None,
        )
