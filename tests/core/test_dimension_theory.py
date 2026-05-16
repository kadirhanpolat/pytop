"""Tests for dimension_theory.py."""

import pytest
from pytop.dimension_theory import (
    Ind,
    dim,
    has_clopen_base,
    ind,
    is_totally_disconnected,
    is_zero_dimensional,
)


# ---------------------------------------------------------------------------
# Helpers — simple dict and object space stubs
# ---------------------------------------------------------------------------

def _tagged(*tags):
    return {"tags": list(tags)}


def _dim_space(**kw):
    return kw  # plain dict


class _Space:
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        if "metadata" not in kw:
            self.metadata = {}


# ===========================================================================
# ind / Ind / dim — basic value retrieval
# ===========================================================================

class TestIndIndDim:
    def test_ind_from_dict(self):
        assert ind({"ind": 2}) == 2

    def test_ind_from_metadata(self):
        s = _Space(metadata={"ind": 1})
        assert ind(s) == 1

    def test_ind_from_attribute(self):
        # covers _dimension_field attribute path (line 94)
        s = _Space(ind=3)
        assert ind(s) == 3

    def test_Ind_from_dict(self):
        assert Ind({"Ind": 1}) == 1

    def test_dim_from_dict(self):
        assert dim({"dim": 3}) == 3

    def test_returns_none_when_unknown(self):
        assert ind({}) is None

    def test_bool_value_returns_none(self):
        # covers _maybe_int bool branch (line 80)
        assert ind({"ind": True}) is None

    def test_cantor_set_name_gives_zero(self):
        assert ind({"metadata": {"space_type": "Cantor Set"}}) == 0

    def test_r_n_name_gives_n(self):
        assert ind({"metadata": {"name": "R^3"}}) == 3

    def test_euclidean_n_name_gives_n(self):
        # covers _benchmark_dimension_from_name euclidean branch (line 113)
        assert ind({"metadata": {"name": "euclidean_2"}}) == 2

    def test_zero_dimensional_tag_gives_zero(self):
        # covers _dimension_value ZERO_DIMENSION_TAGS path (line 126)
        assert ind(_tagged("cantor_set")) == 0

    def test_stone_space_tag_gives_zero(self):
        assert ind(_tagged("stone_space")) == 0


# ===========================================================================
# has_clopen_base
# ===========================================================================

class TestHasClopenBase:
    def test_zero_dimensional_tag_returns_true(self):
        assert has_clopen_base(_tagged("zero_dimensional")) is True

    def test_clopen_base_tag_returns_true(self):
        assert has_clopen_base(_tagged("clopen_base")) is True

    def test_not_zero_dimensional_tag_returns_false(self):
        assert has_clopen_base(_tagged("not_zero_dimensional")) is False

    def test_dim_zero_dict_representation_returns_true(self):
        # dim=0 in dict + explicit representation → covers _representation_of
        # dict branch (lines 67-68) and has_clopen_base return (line 153)
        s = {"dim": 0, "representation": "finite"}
        assert has_clopen_base(s) is True

    def test_dim_zero_metadata_representation_returns_true(self):
        # covers _representation_of metadata branch (lines 69-71)
        s = _Space(metadata={"dim": 0, "representation": "compact_T2"})
        assert has_clopen_base(s) is True

    def test_dim_zero_attribute_no_representation_returns_true(self):
        # covers _representation_of fallback (line 75): no representation attr → "symbolic_general"
        # but tags is truthy → or-condition True → line 153 fires
        s = _Space(dim=0, metadata={})
        s.tags = ["open"]  # non-ZERO, non-NEGATIVE → _extract_tags picks it up
        assert has_clopen_base(s) is True

    def test_dim_zero_representation_attribute_returns_true(self):
        # covers _representation_of attribute return (line 74)
        class SpaceWithRep:
            dim = 0
            representation = "metric"
            metadata = {}
            tags = []  # no ZERO/NEGATIVE tags
        assert has_clopen_base(SpaceWithRep()) is True

    def test_explicit_true_in_dict(self):
        # covers dict explicit has_clopen_base field (line 157)
        s = {"has_clopen_base": True}
        assert has_clopen_base(s) is True

    def test_explicit_false_in_dict(self):
        s = {"has_clopen_base": False}
        assert has_clopen_base(s) is False

    def test_explicit_true_in_metadata(self):
        # covers metadata explicit branch (line 161)
        s = _Space(metadata={"has_clopen_base": True})
        assert has_clopen_base(s) is True

    def test_explicit_false_in_metadata(self):
        s = _Space(metadata={"has_clopen_base": False})
        assert has_clopen_base(s) is False

    def test_explicit_true_as_attribute(self):
        # covers attribute branch (line 164)
        s = _Space(metadata={})
        s.has_clopen_base = True  # type: ignore[attr-defined]
        assert has_clopen_base(s) is True

    def test_no_info_returns_false(self):
        assert has_clopen_base(_Space(metadata={})) is False


# ===========================================================================
# is_zero_dimensional
# ===========================================================================

class TestIsZeroDimensional:
    def test_zero_dimensional_tag(self):
        assert is_zero_dimensional(_tagged("zero_dimensional")) is True

    def test_not_zero_dimensional_tag(self):
        assert is_zero_dimensional(_tagged("not_zero_dimensional")) is False

    def test_clopen_base_implies_zero_dim(self):
        assert is_zero_dimensional(_tagged("clopen_base")) is True

    def test_ind_zero_returns_true(self):
        # covers is_zero_dimensional line 177 (ind=0 path, no clopen_base tag)
        assert is_zero_dimensional({"ind": 0}) is True

    def test_ind_one_returns_false(self):
        assert is_zero_dimensional({"ind": 1}) is False

    def test_no_info_returns_false(self):
        assert is_zero_dimensional({}) is False


# ===========================================================================
# is_totally_disconnected
# ===========================================================================

class TestIsTotallyDisconnected:
    def test_totally_disconnected_tag(self):
        assert is_totally_disconnected(_tagged("totally_disconnected")) is True

    def test_cantor_set_tag(self):
        assert is_totally_disconnected(_tagged("cantor_set")) is True

    def test_zero_dim_implies_totally_disconnected(self):
        # covers is_totally_disconnected line 187 (is_zero_dimensional path)
        assert is_totally_disconnected({"ind": 0}) is True

    def test_explicit_true_in_dict(self):
        # dict-level field (lines 188-191 — already covered by existing tests,
        # but we ensure the branch is exercised)
        assert is_totally_disconnected({"is_totally_disconnected": True}) is True

    def test_explicit_false_in_dict(self):
        assert is_totally_disconnected({"is_totally_disconnected": False}) is False

    def test_explicit_true_in_metadata(self):
        # covers metadata branch (lines 192-195)
        s = _Space(metadata={"is_totally_disconnected": True})
        assert is_totally_disconnected(s) is True

    def test_explicit_false_in_metadata(self):
        s = _Space(metadata={"is_totally_disconnected": False})
        assert is_totally_disconnected(s) is False

    def test_explicit_true_as_attribute(self):
        # covers attribute branch (lines 196-198)
        s = _Space(metadata={})
        s.totally_disconnected_explicit = None  # ensure metadata not set
        # set the attribute the function looks for
        type(s).is_totally_disconnected = True  # class-level bool attribute
        assert is_totally_disconnected(s) is True
        del type(s).is_totally_disconnected  # clean up

    def test_no_info_returns_false(self):
        # covers line 199 (return False fallback)
        assert is_totally_disconnected(_Space(metadata={})) is False

    def test_not_totally_disconnected_tag_overrides(self):
        # not in TOTALLY_DISCONNECTED_TAGS but not zero_dim either
        assert is_totally_disconnected({"ind": 2}) is False
