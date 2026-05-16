"""Coverage-targeted tests for cardinal_numbers.py (v0.5.1)."""
import pytest
from pytop.cardinal_numbers import (
    cardinality_class,
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
    obj = _MetaObj(metadata={"representation": "infinite_metric"})
    assert _representation_of(obj) == "infinite_metric"


# ---------------------------------------------------------------------------
# _representation_of — line 63 (fallback "symbolic_general")
# ---------------------------------------------------------------------------

def test_representation_of_fallback():
    obj = _MetaObj()
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — lines 79-82 (len(carrier) raises TypeError)
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
# cardinality_class — line 116 (n is not None, rep != "finite")
# ---------------------------------------------------------------------------

def test_cardinality_class_carrier_size_non_finite_rep():
    # carrier has size 3, rep = "symbolic_ordinal" ≠ "finite" → line 116 fires
    obj = _MetaObj(metadata={"representation": "symbolic_ordinal"}, carrier=[1, 2, 3])
    result = cardinality_class(obj)
    assert result == "finite"
