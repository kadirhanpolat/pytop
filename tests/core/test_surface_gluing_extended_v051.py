"""Coverage-targeted tests for surface_gluing.py (v0.5.1)."""
from pytop.surface_gluing import compare_gluing_to_surface_profile, torus_gluing_profile


# ---------------------------------------------------------------------------
# compare_gluing_to_surface_profile — line 130 (surface=None → else branch)
# ---------------------------------------------------------------------------

def test_compare_gluing_profile_no_surface_arg():
    # surface defaults to None → line 130 fires (else branch)
    profile = torus_gluing_profile()
    result = compare_gluing_to_surface_profile(profile)
    assert "gluing_name" in result
    assert result["gluing_name"] == profile.name
