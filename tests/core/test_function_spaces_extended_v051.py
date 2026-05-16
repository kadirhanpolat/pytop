"""Coverage-targeted tests for function_spaces.py (v0.5.1)."""
import pytest
from pytop.function_spaces import (
    FunctionSpaceError,
    _representation_of,
    _carrier_size,
    _family_lane,
    _family_focus,
    _family_warning,
)
from pytop.finite_spaces import FiniteTopologicalSpace


class _Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, "metadata"):
            self.metadata = {}
        if not hasattr(self, "tags"):
            self.tags = []


# ---------------------------------------------------------------------------
# _representation_of — line 49 (metadata path), line 53 (fallback)
# ---------------------------------------------------------------------------

def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "compact_open_type"}
    assert _representation_of(obj) == "compact_open_type"


def test_representation_of_repr_attr():
    obj = _Obj()
    obj.representation = "custom_rep"
    assert _representation_of(obj) == "custom_rep"


def test_representation_of_fallback():
    obj = _Obj()
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — lines 71-74 (TypeError path)
# ---------------------------------------------------------------------------

def test_carrier_size_type_error():
    class BadCarrier:
        def __len__(self):
            raise TypeError("unsized")

    obj = _Obj()
    obj.carrier = BadCarrier()
    assert _carrier_size(obj) is None


def test_carrier_size_none_returns_none():
    obj = _Obj()
    assert _carrier_size(obj) is None


# ---------------------------------------------------------------------------
# _family_lane — line 86 (unknown key raises)
# ---------------------------------------------------------------------------

def test_family_lane_pointwise():
    assert _family_lane("pointwise") == "entry"


def test_family_lane_compact_open():
    assert _family_lane("compact_open") == "bridge"


def test_family_lane_uniform():
    assert _family_lane("uniform") == "advanced"


def test_family_lane_unknown_raises():
    with pytest.raises(FunctionSpaceError, match="unknown function-space family key"):
        _family_lane("unknown_key")


# ---------------------------------------------------------------------------
# _family_focus — line 97 (unknown key raises)
# ---------------------------------------------------------------------------

def test_family_focus_unknown_raises():
    with pytest.raises(FunctionSpaceError, match="unknown function-space family key"):
        _family_focus("bad_key")


# ---------------------------------------------------------------------------
# _family_warning — line 124 (unknown key raises)
# ---------------------------------------------------------------------------

def test_family_warning_unknown_raises():
    with pytest.raises(FunctionSpaceError, match="unknown function-space family key"):
        _family_warning("bad_key", "symbolic_general", frozenset())


def test_family_warning_pointwise():
    result = _family_warning("pointwise", "symbolic_general", frozenset())
    assert "pointwise" in result


def test_family_warning_compact_open_locally_compact():
    result = _family_warning("compact_open", "symbolic_general", frozenset({"locally_compact"}))
    assert "compact-open" in result


def test_family_warning_uniform_compact():
    result = _family_warning("uniform", "symbolic_general", frozenset({"compact"}))
    assert "uniform" in result
