"""Coverage-targeted tests for continua.py (v0.5.1)."""
import pytest
from pytop.continua import (
    ContinuumProfile,
    ContinuumProfileError,
    continuum_condition_report,
)


# ---------------------------------------------------------------------------
# ContinuumProfile.__post_init__ — line 45 (empty name raises)
# ---------------------------------------------------------------------------

def test_empty_name_raises():
    with pytest.raises(ContinuumProfileError, match="nonempty name"):
        ContinuumProfile(name="   ")


# ---------------------------------------------------------------------------
# ContinuumProfile.condition_tuple — line 77
# ---------------------------------------------------------------------------

def test_condition_tuple():
    p = ContinuumProfile(
        name="arc",
        compact=True,
        connected=True,
        metric=True,
        nonempty=True,
        continuum=True,
        status="certified",
    )
    assert p.condition_tuple == (True, True, True, True)


# ---------------------------------------------------------------------------
# ContinuumProfile.continuum_label — line 82 (continuum is True)
# ---------------------------------------------------------------------------

def test_continuum_label_true():
    p = ContinuumProfile(
        name="arc",
        compact=True,
        connected=True,
        metric=True,
        nonempty=True,
        continuum=True,
        status="certified",
    )
    assert p.continuum_label == "continuum"


# ---------------------------------------------------------------------------
# ContinuumProfile.continuum_label — line 85 (continuum is None)
# ---------------------------------------------------------------------------

def test_continuum_label_unknown():
    p = ContinuumProfile(name="X")
    assert p.continuum_label == "continuum status unknown"


# ---------------------------------------------------------------------------
# continuum_condition_report — line 300 (verdict = "unknown")
# ---------------------------------------------------------------------------

def test_continuum_condition_report_unknown_verdict():
    p = ContinuumProfile(name="X")
    result = continuum_condition_report(p)
    assert result["verdict"] == "unknown"
