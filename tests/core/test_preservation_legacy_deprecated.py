"""Tests for preservation_legacy.py — deprecated facade."""

import warnings
import pytest
from pytop.preservation_legacy import (
    preservation_table_lookup,
    preservation_table_row,
    preservation_table_column,
    analyze_preservation_table,
)
from pytop.result import Result


def _call_with_warning(fn, *args, **kwargs):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", DeprecationWarning)
        result = fn(*args, **kwargs)
    dep_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
    return result, dep_warnings


# ---------------------------------------------------------------------------
# preservation_table_lookup
# ---------------------------------------------------------------------------

class TestPreservationTableLookup:
    def test_compact_subspace_is_conditional(self):
        r, _ = _call_with_warning(preservation_table_lookup, "compact", "subspace")
        assert r.status == "conditional"

    def test_compact_finite_product_is_true(self):
        r, _ = _call_with_warning(preservation_table_lookup, "compact", "finite_product")
        assert r.is_true

    def test_hausdorff_quotient_is_false(self):
        r, _ = _call_with_warning(preservation_table_lookup, "hausdorff", "quotient")
        assert r.is_false

    def test_connected_continuous_image_is_true(self):
        r, _ = _call_with_warning(preservation_table_lookup, "connected", "continuous_image")
        assert r.is_true

    def test_returns_result_instance(self):
        r, _ = _call_with_warning(preservation_table_lookup, "t1", "subspace")
        assert isinstance(r, Result)

    def test_alias_compact_accepted(self):
        r, _ = _call_with_warning(preservation_table_lookup, "compactness", "subspace")
        assert r.status == "conditional"

    def test_alias_t2_accepted(self):
        r, _ = _call_with_warning(preservation_table_lookup, "t2", "finite_product")
        assert r.is_true

    def test_unknown_property_raises(self):
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            with pytest.raises(ValueError):
                preservation_table_lookup("not_a_property", "subspace")

    def test_unknown_construction_raises(self):
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            with pytest.raises(ValueError):
                preservation_table_lookup("compact", "not_a_construction")

    def test_emits_deprecation_warning(self):
        _, warns = _call_with_warning(preservation_table_lookup, "compact", "subspace")
        assert len(warns) >= 1
        assert "deprecated" in str(warns[0].message).lower()

    def test_metadata_has_v0_1_48_record(self):
        r, _ = _call_with_warning(preservation_table_lookup, "compact", "quotient")
        assert r.metadata.get("v0_1_48_corridor_record") is True


# ---------------------------------------------------------------------------
# preservation_table_row
# ---------------------------------------------------------------------------

class TestPreservationTableRow:
    def test_returns_result_with_dict_value(self):
        r, _ = _call_with_warning(preservation_table_row, "compact")
        assert r.is_true
        assert isinstance(r.value, dict)

    def test_row_has_all_constructions(self):
        r, _ = _call_with_warning(preservation_table_row, "hausdorff")
        for key in ("subspace", "finite_product", "countable_product", "quotient", "continuous_image"):
            assert key in r.value

    def test_emits_deprecation_warning(self):
        _, warns = _call_with_warning(preservation_table_row, "compact")
        assert any("deprecated" in str(w.message).lower() for w in warns)


# ---------------------------------------------------------------------------
# preservation_table_column
# ---------------------------------------------------------------------------

class TestPreservationTableColumn:
    def test_returns_result_with_dict_value(self):
        r, _ = _call_with_warning(preservation_table_column, "subspace")
        assert r.is_true
        assert isinstance(r.value, dict)

    def test_column_has_all_properties(self):
        r, _ = _call_with_warning(preservation_table_column, "quotient")
        for key in ("connectedness", "compactness", "hausdorff", "t1", "second_countability"):
            assert key in r.value

    def test_emits_deprecation_warning(self):
        _, warns = _call_with_warning(preservation_table_column, "quotient")
        assert any("deprecated" in str(w.message).lower() for w in warns)


# ---------------------------------------------------------------------------
# analyze_preservation_table
# ---------------------------------------------------------------------------

class TestAnalyzePreservationTable:
    def test_full_table_when_no_args(self):
        r, _ = _call_with_warning(analyze_preservation_table)
        assert r.is_true
        assert isinstance(r.value, dict)
        assert "connectedness" in r.value

    def test_lookup_with_both_args(self):
        r, _ = _call_with_warning(analyze_preservation_table, "compact", "finite_product")
        assert r.is_true

    def test_row_with_property_only(self):
        r, _ = _call_with_warning(analyze_preservation_table, property_name="t1")
        assert r.is_true
        assert isinstance(r.value, dict)

    def test_column_with_construction_only(self):
        r, _ = _call_with_warning(analyze_preservation_table, construction="subspace")
        assert r.is_true
        assert isinstance(r.value, dict)

    def test_emits_deprecation_warning(self):
        _, warns = _call_with_warning(analyze_preservation_table)
        assert any("deprecated" in str(w.message).lower() for w in warns)
