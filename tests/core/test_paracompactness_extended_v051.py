"""Coverage-targeted tests for paracompactness.py (v0.5.1)."""
import pytest
from pytop.paracompactness import (
    is_paracompact,
    paracompact_profile,
    analyze_paracompactness,
    is_locally_finite_refinement,
    is_star_refinement,
    _representation_of,
    _carrier_size,
)
from pytop.finite_spaces import FiniteTopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _finite_space():
    carrier = frozenset({1, 2})
    topology = frozenset([frozenset(), frozenset({1}), frozenset({1, 2})])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


class _Obj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, "metadata"):
            self.metadata = {}
        if not hasattr(self, "tags"):
            self.tags = set()


# ---------------------------------------------------------------------------
# _representation_of — metadata path (line 52)
# ---------------------------------------------------------------------------

def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "infinite_metric"}
    assert _representation_of(obj) == "infinite_metric"


def test_representation_of_finite_space():
    assert _representation_of(_finite_space()) == "finite"


# ---------------------------------------------------------------------------
# _representation_of — fallback (line 56)
# ---------------------------------------------------------------------------

def test_representation_of_fallback():
    obj = _Obj()
    obj.metadata = {}
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — try/except block (lines 72-75)
# ---------------------------------------------------------------------------

def test_carrier_size_finite_space():
    assert _carrier_size(_finite_space()) == 2


def test_carrier_size_list_carrier():
    obj = _Obj()
    obj.carrier = [1, 2, 3]
    assert _carrier_size(obj) == 3


def test_carrier_size_none_carrier():
    obj = _Obj()
    obj.carrier = None
    assert _carrier_size(obj) is None


def test_carrier_size_type_error():
    class BadLen:
        def __len__(self):
            raise TypeError("no len")

    obj = _Obj()
    obj.carrier = BadLen()
    assert _carrier_size(obj) is None


# ---------------------------------------------------------------------------
# paracompact_profile — paracompact but no Hausdorff (line 222)
# ---------------------------------------------------------------------------

def test_paracompact_profile_paracompact_no_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact"}  # is_paracompact → true via explicit tag, no hausdorff
    profile = paracompact_profile(obj)
    assert "Hausdorff not confirmed" in profile["full_normality"]


# ---------------------------------------------------------------------------
# is_paracompact — various paths
# ---------------------------------------------------------------------------

def test_is_paracompact_not_paracompact_tag():
    obj = _Obj()
    obj.tags = {"not_paracompact"}
    result = is_paracompact(obj)
    assert result.is_false


def test_is_paracompact_finite_space():
    result = is_paracompact(_finite_space())
    assert result.is_true


def test_is_paracompact_metrizable():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = is_paracompact(obj)
    assert result.is_true


def test_is_paracompact_compact():
    obj = _Obj()
    obj.tags = {"compact"}
    result = is_paracompact(obj)
    assert result.is_true


def test_is_paracompact_regular_lindelof():
    obj = _Obj()
    obj.tags = {"regular", "lindelof"}
    result = is_paracompact(obj)
    assert result.is_true


def test_is_paracompact_explicit_tag():
    obj = _Obj()
    obj.tags = {"paracompact"}
    result = is_paracompact(obj)
    assert result.is_true


def test_is_paracompact_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    result = is_paracompact(obj)
    assert result.is_unknown


# ---------------------------------------------------------------------------
# is_locally_finite_refinement — returns False (line 333)
# ---------------------------------------------------------------------------

def test_is_locally_finite_refinement_returns_false():
    result = is_locally_finite_refinement([], [])
    assert result is False


# ---------------------------------------------------------------------------
# is_star_refinement — returns False (line 339)
# ---------------------------------------------------------------------------

def test_is_star_refinement_returns_false():
    result = is_star_refinement([], [])
    assert result is False


# ---------------------------------------------------------------------------
# analyze_paracompactness — facade
# ---------------------------------------------------------------------------

def test_analyze_paracompactness_finite():
    result = analyze_paracompactness(_finite_space())
    assert result.is_true


def test_analyze_paracompactness_symbolic():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = analyze_paracompactness(obj)
    assert result.is_true
