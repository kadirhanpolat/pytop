"""Coverage-targeted tests for euclidean_topology.py (v0.5.1)."""
import pytest
from pytop.euclidean_topology import (
    EuclideanTopologyProfile,
    EuclideanTopologyProfileError,
    closed_disk_profile,
    punctured_sphere_profile,
    stereographic_projection_profile,
)


# ---------------------------------------------------------------------------
# EuclideanTopologyProfile.__post_init__ — line 54 (empty name raises)
# ---------------------------------------------------------------------------

def test_profile_empty_name_raises():
    with pytest.raises(EuclideanTopologyProfileError, match="nonempty name"):
        EuclideanTopologyProfile(name="   ", kind="open_ball")


# ---------------------------------------------------------------------------
# EuclideanTopologyProfile.__post_init__ — line 58 (invalid status raises)
# ---------------------------------------------------------------------------

def test_profile_invalid_status_raises():
    with pytest.raises(EuclideanTopologyProfileError, match="status"):
        EuclideanTopologyProfile(name="ball", kind="open_ball", status="maybe")


# ---------------------------------------------------------------------------
# EuclideanTopologyProfile.__post_init__ — line 60 (negative ambient dim)
# ---------------------------------------------------------------------------

def test_profile_negative_ambient_dimension_raises():
    with pytest.raises(EuclideanTopologyProfileError, match="Ambient dimension"):
        EuclideanTopologyProfile(name="ball", kind="open_ball", ambient_dimension=-1)


# ---------------------------------------------------------------------------
# EuclideanTopologyProfile.__post_init__ — line 62 (negative intrinsic dim)
# ---------------------------------------------------------------------------

def test_profile_negative_intrinsic_dimension_raises():
    with pytest.raises(EuclideanTopologyProfileError, match="Intrinsic dimension"):
        EuclideanTopologyProfile(name="ball", kind="open_ball", intrinsic_dimension=-1)


# ---------------------------------------------------------------------------
# punctured_sphere_profile — line 171 (dimension <= 0 raises)
# ---------------------------------------------------------------------------

def test_punctured_sphere_zero_dimension_raises():
    with pytest.raises(EuclideanTopologyProfileError, match="positive dimension"):
        punctured_sphere_profile(0)


# ---------------------------------------------------------------------------
# stereographic_projection_profile — line 189 (dimension <= 0 raises)
# ---------------------------------------------------------------------------

def test_stereographic_projection_zero_dimension_raises():
    with pytest.raises(EuclideanTopologyProfileError, match="positive dimension"):
        stereographic_projection_profile(0)
