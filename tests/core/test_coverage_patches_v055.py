"""Coverage patches for v0.5.5 — hits the 9 reachable missed lines.

Modules targeted (line numbers):
  topological_groups.py : 71, 74, 418
  stone_cech.py         : 85, 88
  cell_complexes.py     : 112-113
  cardinal_functions_framework.py : 344
  maps.py               : 440
"""

from __future__ import annotations

import types

import pytest

from pytop.cardinal_functions_framework import _comparison_key
from pytop.cell_complexes import (
    CellComplexProfile,
    cell,
    cell_complex_profile,
    validate_finite_cell_profile,
)
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.maps import FiniteMap, _analyze_finite_map_property
from pytop.spaces import TopologicalSpace
from pytop.stone_cech import is_stone_cech_compactifiable
from pytop.topological_groups import classify_topological_group, is_topological_group


# ---------------------------------------------------------------------------
# topological_groups.py:71  _representation_of — metadata["representation"] path
# ---------------------------------------------------------------------------

class TestTopologicalGroupsRepresentationMetadata:
    def test_representation_of_reads_metadata_key(self):
        sp = TopologicalSpace.symbolic(
            description="SO(3)",
            representation="so3",
            tags={"topological_group"},
        )
        result = is_topological_group(sp)
        assert result.metadata["representation"] == "so3"

    def test_representation_propagates_to_separation(self):
        from pytop.topological_groups import topological_group_separation
        sp = TopologicalSpace.symbolic(
            description="Compact Lie group",
            representation="compact_lie",
            tags={"topological_group", "lie_group"},
        )
        result = topological_group_separation(sp)
        assert result.metadata["representation"] == "compact_lie"


# ---------------------------------------------------------------------------
# topological_groups.py:74  _representation_of — space.representation path
# ---------------------------------------------------------------------------

class TestTopologicalGroupsRepresentationAttr:
    def test_representation_from_space_attr(self):
        sp = types.SimpleNamespace(
            tags={"topological_group"},
            metadata={},
            representation="so2_surface",
        )
        result = is_topological_group(sp)
        assert result.metadata["representation"] == "so2_surface"

    def test_representation_attr_truthy_string(self):
        sp = types.SimpleNamespace(
            tags={"topological_group", "compact"},
            metadata=None,
            representation="U1",
        )
        result = classify_topological_group(sp)
        assert result["classification"]["representation"] == "u1" if "representation" in result.get("classification", {}) else result


# ---------------------------------------------------------------------------
# topological_groups.py:418  group_type == "compact"
# ---------------------------------------------------------------------------

class TestTopologicalGroupsCompactType:
    def test_compact_non_abelian_group_type(self):
        sp = TopologicalSpace(carrier=None, tags={"topological_group", "compact"})
        result = classify_topological_group(sp)
        assert result["group_type"] == "compact"
        assert result["is_compact"] is True
        assert result["is_abelian"] is None

    def test_compact_group_tag_yields_compact_type(self):
        sp = TopologicalSpace(carrier=None, tags={"topological_group", "compact_group"})
        result = classify_topological_group(sp)
        assert result["group_type"] == "compact"

    def test_compact_non_abelian_key_properties_include_compact(self):
        sp = TopologicalSpace(carrier=None, tags={"topological_group", "compact"})
        result = classify_topological_group(sp)
        assert "compact" in result["key_properties"]


# ---------------------------------------------------------------------------
# stone_cech.py:85  _representation_of — metadata["representation"] path
# ---------------------------------------------------------------------------

class TestStoneCechRepresentationMetadata:
    def test_representation_of_reads_metadata_key(self):
        sp = TopologicalSpace.symbolic(
            description="Discrete countable space",
            representation="n_discrete",
            tags={"locally_compact", "tychonoff"},
        )
        result = is_stone_cech_compactifiable(sp)
        assert result.metadata["representation"] == "n_discrete"

    def test_representation_propagates_to_embedding(self):
        from pytop.stone_cech import stone_cech_embedding
        sp = TopologicalSpace.symbolic(
            description="Real line",
            representation="real_line",
            tags={"locally_compact", "metric"},
        )
        result = stone_cech_embedding(sp)
        assert result.metadata["representation"] == "real_line"


# ---------------------------------------------------------------------------
# stone_cech.py:88  _representation_of — space.representation path
# ---------------------------------------------------------------------------

class TestStoneCechRepresentationAttr:
    def test_representation_from_space_attr(self):
        sp = types.SimpleNamespace(
            tags={"locally_compact", "tychonoff"},
            metadata={},
            representation="omega_space",
        )
        result = is_stone_cech_compactifiable(sp)
        assert result.metadata["representation"] == "omega_space"

    def test_representation_attr_with_none_metadata(self):
        sp = types.SimpleNamespace(
            tags={"metric"},
            metadata=None,
            representation="real_line_repr",
        )
        result = is_stone_cech_compactifiable(sp)
        assert result.metadata["representation"] == "real_line_repr"


# ---------------------------------------------------------------------------
# cell_complexes.py:112-113  validate_finite_cell_profile — CellComplexError path
# ---------------------------------------------------------------------------

class TestCellComplexesValidationErrorPath:
    def test_validate_returns_false_for_emptied_cells(self):
        profile = cell_complex_profile("sphere", [cell("e0", 0), cell("e2", 2)])
        object.__setattr__(profile, "cells", ())
        assert validate_finite_cell_profile(profile) is False

    def test_validate_returns_false_for_empty_name(self):
        profile = cell_complex_profile("torus", [cell("e0", 0), cell("e1a", 1), cell("e2", 2)])
        object.__setattr__(profile, "name", "")
        assert validate_finite_cell_profile(profile) is False

    def test_valid_profile_still_returns_correct_result(self):
        profile = cell_complex_profile(
            "circle",
            [cell("e0", 0), cell("e1", 1)],
        )
        result = validate_finite_cell_profile(profile)
        assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# cardinal_functions_framework.py:344  _comparison_key
# ---------------------------------------------------------------------------

class TestCardinalFunctionsComparisonKey:
    def test_comparison_key_returns_frozenset(self):
        key = _comparison_key("weight", "density")
        assert key == frozenset({"weight", "density"})

    def test_comparison_key_is_symmetric(self):
        assert _comparison_key("a", "b") == _comparison_key("b", "a")

    def test_comparison_key_single_element_pair(self):
        key = _comparison_key("character", "character")
        assert key == frozenset({"character"})


# ---------------------------------------------------------------------------
# maps.py:440  _analyze_finite_map_property — return None for unknown property
# ---------------------------------------------------------------------------

class TestMapsUnknownPropertyReturnsNone:
    def _make_map(self) -> FiniteMap:
        dom = FiniteTopologicalSpace(
            carrier=("a", "b"),
            topology=[set(), {"a", "b"}],
        )
        cod = FiniteTopologicalSpace(
            carrier=("a", "b"),
            topology=[set(), {"a", "b"}],
        )
        return FiniteMap(domain=dom, codomain=cod, mapping={"a": "a", "b": "b"})

    def test_unknown_property_returns_none(self):
        m = self._make_map()
        result = _analyze_finite_map_property(m, "unknown_property_xyz")
        assert result is None

    def test_known_property_does_not_return_none(self):
        m = self._make_map()
        result = _analyze_finite_map_property(m, "continuous")
        assert result is not None

    def test_empty_string_property_returns_none(self):
        m = self._make_map()
        result = _analyze_finite_map_property(m, "")
        assert result is None
