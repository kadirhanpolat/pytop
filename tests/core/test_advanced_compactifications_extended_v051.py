"""Coverage-targeted tests for advanced_compactifications.py (v0.5.1)."""
import pytest
from pytop.advanced_compactifications import (
    is_cech_complete,
    is_realcompact,
    is_perfect_map,
    advanced_compactness_profile,
    _representation_of,
    _name_of,
    _bool_field,
)


# ---------------------------------------------------------------------------
# Helpers — simple attribute-bearing objects
# ---------------------------------------------------------------------------

class _Obj:
    """Generic stub space/mapping for attribute-path testing."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if not hasattr(self, "metadata"):
            self.metadata = {}
        if not hasattr(self, "tags"):
            self.tags = set()


# ---------------------------------------------------------------------------
# _representation_of — attribute path  (lines 111-113)
# ---------------------------------------------------------------------------

def test_representation_of_attr_path():
    obj = _Obj(representation="custom_attr_rep")
    assert _representation_of(obj) == "custom_attr_rep"


def test_representation_of_fallback():
    obj = _Obj()
    assert _representation_of(obj) == "symbolic_general"


def test_representation_of_dict_key():
    d = {"representation": "dict_rep"}
    assert _representation_of(d) == "dict_rep"


def test_representation_of_metadata_key():
    obj = _Obj()
    obj.metadata = {"representation": "from_meta"}
    assert _representation_of(obj) == "from_meta"


# ---------------------------------------------------------------------------
# _name_of — attribute path  (lines 125-128)
# ---------------------------------------------------------------------------

def test_name_of_attr_path():
    obj = _Obj(name="myspace")
    assert _name_of(obj, "fallback") == "myspace"


def test_name_of_fallback():
    obj = _Obj()
    assert _name_of(obj, "fallback") == "fallback"


def test_name_of_dict():
    d = {"name": "dict_name"}
    assert _name_of(d, "fallback") == "dict_name"


def test_name_of_metadata():
    obj = _Obj()
    obj.metadata = {"name": "meta_name"}
    assert _name_of(obj, "fallback") == "meta_name"


# ---------------------------------------------------------------------------
# _bool_field — metadata bool path (line 140) and attr path (lines 141-143)
# ---------------------------------------------------------------------------

def test_bool_field_metadata_true():
    obj = _Obj()
    obj.metadata = {"continuous": True}
    assert _bool_field(obj, "continuous") is True


def test_bool_field_metadata_false():
    obj = _Obj()
    obj.metadata = {"continuous": False}
    assert _bool_field(obj, "continuous") is False


def test_bool_field_attr_true():
    obj = _Obj(closed=True)
    assert _bool_field(obj, "closed") is True


def test_bool_field_attr_false():
    obj = _Obj(surjective=False)
    assert _bool_field(obj, "surjective") is False


def test_bool_field_none():
    obj = _Obj()
    assert _bool_field(obj, "compact_fibers") is None


# ---------------------------------------------------------------------------
# is_cech_complete — negative tag path  (line 168)
# ---------------------------------------------------------------------------

def test_is_cech_complete_false_tag():
    obj = _Obj(tags={"not_cech_complete"})
    r = is_cech_complete(obj)
    assert r.is_false


def test_is_cech_complete_finite_hausdorff():
    obj = _Obj(tags={"finite_hausdorff"})
    r = is_cech_complete(obj)
    assert r.is_true
    assert r.mode == "theorem"


def test_is_cech_complete_complete_metric_true():
    obj = _Obj(tags={"complete_metric"})
    r = is_cech_complete(obj)
    assert r.is_true


def test_is_cech_complete_metrizable_conditional():
    obj = _Obj(tags={"metrizable"})
    r = is_cech_complete(obj)
    assert r.status == "conditional"


def test_is_cech_complete_unknown():
    obj = _Obj(tags={"hausdorff"})
    r = is_cech_complete(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_realcompact — finite_hausdorff, tychonoff, unknown  (lines 247-274)
# ---------------------------------------------------------------------------

def test_is_realcompact_false_tag():
    obj = _Obj(tags={"not_realcompact"})
    r = is_realcompact(obj)
    assert r.is_false


def test_is_realcompact_true_tag():
    obj = _Obj(tags={"completely_metrizable"})
    r = is_realcompact(obj)
    assert r.is_true


def test_is_realcompact_finite_hausdorff():
    obj = _Obj(tags={"finite_hausdorff"})
    r = is_realcompact(obj)
    assert r.is_true
    assert r.mode == "theorem"


def test_is_realcompact_finite_discrete():
    obj = _Obj(tags={"finite_discrete"})
    r = is_realcompact(obj)
    assert r.is_true


def test_is_realcompact_tychonoff_conditional():
    obj = _Obj(tags={"tychonoff"})
    r = is_realcompact(obj)
    assert r.status == "conditional"


def test_is_realcompact_unknown():
    obj = _Obj(tags={"hausdorff"})
    r = is_realcompact(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# is_perfect_map — tag paths and feature-map paths  (lines 291-351)
# ---------------------------------------------------------------------------

def test_is_perfect_map_false_tag():
    obj = _Obj(tags={"not_perfect_map"})
    r = is_perfect_map(obj)
    assert r.is_false


def test_is_perfect_map_true_tag():
    obj = _Obj(tags={"perfect_map"})
    r = is_perfect_map(obj)
    assert r.is_true
    assert r.mode == "theorem"


def test_is_perfect_map_all_true_exact():
    obj = _Obj(continuous=True, closed=True, compact_fibers=True, surjective=True)
    r = is_perfect_map(obj)
    assert r.is_true
    assert r.mode == "exact"


def test_is_perfect_map_one_false_exact_false():
    obj = _Obj(continuous=True, closed=True, compact_fibers=True, surjective=False)
    r = is_perfect_map(obj)
    assert r.is_false
    assert r.mode == "exact"


def test_is_perfect_map_partial_conditional():
    obj = _Obj(continuous=True)
    r = is_perfect_map(obj)
    assert r.status == "conditional"


def test_is_perfect_map_unknown():
    obj = _Obj()
    r = is_perfect_map(obj)
    assert r.is_unknown


# ---------------------------------------------------------------------------
# advanced_compactness_profile — integration smoke test
# ---------------------------------------------------------------------------

def test_advanced_compactness_profile_keys():
    obj = _Obj(tags={"compact_hausdorff"})
    p = advanced_compactness_profile(obj)
    for key in ("cech_complete", "realcompact", "tags", "benchmark_summary"):
        assert key in p
    assert p["cech_complete"] is True
    assert p["realcompact"] is True
