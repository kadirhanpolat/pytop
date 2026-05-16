"""Coverage-targeted tests for ordinal_numbers.py (v0.5.1)."""
import pytest
from pytop.ordinal_numbers import (
    ordinal_class,
    ordinal_profile,
    _representation_of,
    _carrier_size,
)


class _MetaObj:
    def __init__(self, metadata=None, carrier=None):
        self.metadata = metadata or {}
        if carrier is not None:
            self.carrier = carrier


# ---------------------------------------------------------------------------
# _representation_of — line 59 (metadata has "representation" key)
# ---------------------------------------------------------------------------

def test_representation_of_from_metadata():
    obj = _MetaObj(metadata={"representation": "symbolic_ordinal"})
    assert _representation_of(obj) == "symbolic_ordinal"


# ---------------------------------------------------------------------------
# _representation_of — line 63 (fallback "symbolic_general")
# ---------------------------------------------------------------------------

def test_representation_of_fallback():
    obj = _MetaObj()  # no representation in metadata, no .representation attr
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — lines 79-82 (len(carrier) raises TypeError → pass → None)
# ---------------------------------------------------------------------------

def test_carrier_size_no_len_raises_returns_none():
    class _NoLen:
        def __len__(self):
            raise TypeError("no len")

    obj = _MetaObj()
    obj.carrier = _NoLen()
    result = _carrier_size(obj)
    assert result is None


# ---------------------------------------------------------------------------
# ordinal_class — line 124 (n is not None, rep != "finite")
# ---------------------------------------------------------------------------

def test_ordinal_class_carrier_size_not_finite_rep():
    # carrier has a size (n=3) but representation is "symbolic_ordinal" ≠ "finite"
    # → line 121 skipped, line 123-124 fires
    obj = _MetaObj(metadata={"representation": "symbolic_ordinal"}, carrier=[1, 2, 3])
    result = ordinal_class(obj)
    assert result == "finite_ordinal"
