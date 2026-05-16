"""Coverage-targeted tests for manifolds.py (v0.5.1)."""
import pytest
from pytop.manifolds import ManifoldProfile, ManifoldProfileError


# ---------------------------------------------------------------------------
# ManifoldProfile.__post_init__ — line 53 (empty name raises)
# ---------------------------------------------------------------------------

def test_manifold_profile_empty_name_raises():
    with pytest.raises(ManifoldProfileError, match="nonempty name"):
        ManifoldProfile(name="   ", dimension=0, local_model="R^n")


# ---------------------------------------------------------------------------
# ManifoldProfile.__post_init__ — line 61 (invalid status raises)
# ---------------------------------------------------------------------------

def test_manifold_profile_invalid_status_raises():
    with pytest.raises(ManifoldProfileError, match="status"):
        ManifoldProfile(name="M", dimension=1, local_model="R", status="invalid_status")
