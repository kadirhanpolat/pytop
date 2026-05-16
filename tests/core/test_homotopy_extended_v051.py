"""Coverage-targeted tests for homotopy.py (v0.5.1)."""
import pytest
from pytop.homotopy import (
    HomotopyProfileError,
    HomotopyProfile,
    DeformationRetractionProfile,
    ContractibleProfile,
)


# ---------------------------------------------------------------------------
# HomotopyProfile — line 46 (empty name raises)
# ---------------------------------------------------------------------------

def test_homotopy_profile_empty_name_raises():
    with pytest.raises(HomotopyProfileError, match="nonempty name"):
        HomotopyProfile(name="   ", source="f", target="g", status="homotopic")


def test_homotopy_profile_invalid_status_raises():
    with pytest.raises(HomotopyProfileError, match="Unsupported homotopy status"):
        HomotopyProfile(name="h", source="f", target="g", status="bad_status")


def test_homotopy_profile_valid():
    p = HomotopyProfile(name="H", source="f", target="g", status="homotopic")
    assert p.is_certified_homotopy


# ---------------------------------------------------------------------------
# DeformationRetractionProfile — line 78 (invalid status), line 80 (empty name)
# ---------------------------------------------------------------------------

def test_deformation_retraction_invalid_status_raises():
    with pytest.raises(HomotopyProfileError, match="Unsupported deformation-retraction status"):
        DeformationRetractionProfile(name="R", space="S", subspace="p", status="bad_status")


def test_deformation_retraction_empty_name_raises():
    with pytest.raises(HomotopyProfileError, match="nonempty name"):
        DeformationRetractionProfile(name="   ", space="S", subspace="p", status="not_certified")


def test_deformation_retraction_valid():
    p = DeformationRetractionProfile(name="R", space="D^2", subspace="pt", status="certified")
    assert p.status == "certified"


# ---------------------------------------------------------------------------
# ContractibleProfile — line 101 (invalid status)
# ---------------------------------------------------------------------------

def test_contractible_profile_invalid_status_raises():
    with pytest.raises(HomotopyProfileError, match="Unsupported contractible status"):
        ContractibleProfile(space="X", status="bad_status")


def test_contractible_profile_valid():
    p = ContractibleProfile(space="D^n", status="certified")
    assert p.is_certified_contractible
