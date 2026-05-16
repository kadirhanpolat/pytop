"""Coverage-targeted tests for cofinality.py (v0.5.1)."""
import pytest
from pytop.cofinality import (
    cofinality_class,
    cofinality_profile,
    _representation_of,
    _carrier_size,
)


class _MetaObj:
    def __init__(self, metadata=None, carrier=None):
        self.metadata = metadata or {}
        if carrier is not None:
            self.carrier = carrier


# ---------------------------------------------------------------------------
# _representation_of — line 60 (metadata has "representation" key)
# ---------------------------------------------------------------------------

def test_representation_of_from_metadata():
    obj = _MetaObj(metadata={"representation": "symbolic_cf"})
    assert _representation_of(obj) == "symbolic_cf"


# ---------------------------------------------------------------------------
# _representation_of — line 64 (fallback "symbolic_general")
# ---------------------------------------------------------------------------

def test_representation_of_fallback():
    obj = _MetaObj()
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — lines 80-83 (try/except block for len)
# ---------------------------------------------------------------------------

def test_carrier_size_successful_len():
    obj = _MetaObj(carrier=[1, 2, 3])
    assert _carrier_size(obj) == 3


def test_carrier_size_type_error_returns_none():
    class _NoLen:
        def __len__(self):
            raise TypeError("no len")

    obj = _MetaObj()
    obj.carrier = _NoLen()
    assert _carrier_size(obj) is None


# ---------------------------------------------------------------------------
# cofinality_class — line 120 (n is not None, rep != "finite")
# ---------------------------------------------------------------------------

def test_cofinality_class_carrier_size_non_finite_rep():
    # rep="symbolic_cf" ≠ "finite", n=3 → line 120 fires
    obj = _MetaObj(metadata={"representation": "symbolic_cf"}, carrier=[1, 2, 3])
    result = cofinality_class(obj)
    assert result == "finite"


# ---------------------------------------------------------------------------
# cofinality_profile — line 189 (n == 1 label branch)
# ---------------------------------------------------------------------------

def test_cofinality_profile_n_equals_one():
    # carrier of size 1 → cf_class="finite", n=1 → line 189 fires
    obj = _MetaObj(metadata={"representation": "symbolic_cf"}, carrier=[42])
    profile = cofinality_profile(obj)
    assert "cf(1)" in profile["cofinality_label"]
