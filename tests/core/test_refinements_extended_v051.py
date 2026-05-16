"""Coverage-targeted tests for refinements.py (v0.5.1)."""
import pytest
from pytop.refinements import (
    is_locally_finite_cover,
    refinement_profile,
    analyze_cover_refinement,
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
# _representation_of — metadata path (line 51)
# ---------------------------------------------------------------------------

def test_representation_of_metadata_path():
    obj = _Obj()
    obj.metadata = {"representation": "infinite_metric"}
    assert _representation_of(obj) == "infinite_metric"


def test_representation_of_finite_space():
    assert _representation_of(_finite_space()) == "finite"


# ---------------------------------------------------------------------------
# _representation_of — fallback (line 55)
# ---------------------------------------------------------------------------

def test_representation_of_fallback():
    obj = _Obj()
    obj.metadata = {}
    assert _representation_of(obj) == "symbolic_general"


# ---------------------------------------------------------------------------
# _carrier_size — try/except TypeError (lines 71-74)
# ---------------------------------------------------------------------------

def test_carrier_size_finite_space():
    assert _carrier_size(_finite_space()) == 2


def test_carrier_size_list_carrier():
    obj = _Obj()
    obj.carrier = [1, 2, 3]
    assert _carrier_size(obj) == 3


def test_carrier_size_none():
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
# refinement_profile — paracompact but no Hausdorff (line 218)
# ---------------------------------------------------------------------------

def test_refinement_profile_paracompact_no_hausdorff():
    obj = _Obj()
    obj.tags = {"paracompact"}  # paracompact confirmed, no Hausdorff tag
    profile = refinement_profile(obj)
    assert "Hausdorff not confirmed" in profile["star_refinement"]


# ---------------------------------------------------------------------------
# refinement_profile — sigma_lf via paracompact tag (line 268)
# ---------------------------------------------------------------------------

def test_refinement_profile_sigma_lf_via_paracompact():
    obj = _Obj()
    # paracompact but not metrizable, not second_countable, not finite
    obj.tags = {"paracompact"}
    profile = refinement_profile(obj)
    assert "paracompact" in profile["sigma_locally_finite"].lower()


# ---------------------------------------------------------------------------
# is_locally_finite_cover — all paths
# ---------------------------------------------------------------------------

def test_locally_finite_cover_not_paracompact_tag():
    obj = _Obj()
    obj.tags = {"not_paracompact"}
    result = is_locally_finite_cover(obj)
    assert result.is_false


def test_locally_finite_cover_finite_space():
    result = is_locally_finite_cover(_finite_space())
    assert result.is_true


def test_locally_finite_cover_metrizable():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = is_locally_finite_cover(obj)
    assert result.is_true


def test_locally_finite_cover_compact():
    obj = _Obj()
    obj.tags = {"compact"}
    result = is_locally_finite_cover(obj)
    assert result.is_true


def test_locally_finite_cover_regular_lindelof():
    obj = _Obj()
    obj.tags = {"regular", "lindelof"}
    result = is_locally_finite_cover(obj)
    assert result.is_true


def test_locally_finite_cover_explicit_tag():
    obj = _Obj()
    obj.tags = {"paracompact"}
    result = is_locally_finite_cover(obj)
    assert result.is_true


def test_locally_finite_cover_unknown():
    obj = _Obj()
    obj.tags = {"connected"}
    result = is_locally_finite_cover(obj)
    assert result.is_unknown


# ---------------------------------------------------------------------------
# analyze_cover_refinement — facade
# ---------------------------------------------------------------------------

def test_analyze_cover_refinement_finite():
    result = analyze_cover_refinement(_finite_space())
    assert result.is_true


def test_analyze_cover_refinement_symbolic():
    obj = _Obj()
    obj.tags = {"metrizable"}
    result = analyze_cover_refinement(obj)
    assert result.is_true
