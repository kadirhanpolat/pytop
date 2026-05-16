"""Coverage-targeted tests for surfaces.py (v0.5.1)."""
from pytop.surfaces import surface_profile


# ---------------------------------------------------------------------------
# SurfaceProfile.classification_label — line 72 (nonorientable + nonorientable_genus)
# ---------------------------------------------------------------------------

def test_classification_label_nonorientable():
    p = surface_profile("rp2", orientability="nonorientable", nonorientable_genus=1)
    label = p.classification_label
    assert "nonorientable" in label
    assert "1" in label


# ---------------------------------------------------------------------------
# SurfaceProfile.classification_label — line 73 (unknown orientability fallback)
# ---------------------------------------------------------------------------

def test_classification_label_unknown():
    p = surface_profile("unknown_surf")
    label = p.classification_label
    assert "unknown" in label
