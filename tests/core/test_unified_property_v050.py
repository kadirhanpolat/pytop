"""Tests for unified_property.py (v0.5.0)."""
import pytest
from pytop.unified_property import (
    analyze_property,
    analyze_space,
    unified_compactness_report,
    unified_connectedness_report,
    unified_separation_report,
    property_registry,
    is_finite_space,
    is_infinite_space,
)
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import DiscreteInfiniteSpace, IndiscreteInfiniteSpace


def _discrete2():
    """Discrete topology on {a, b}: all subsets open."""
    carrier = frozenset({"a", "b"})
    topology = frozenset([
        frozenset(), frozenset({"a"}), frozenset({"b"}), carrier
    ])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


def _indiscrete2():
    carrier = frozenset({"a", "b"})
    topology = frozenset([frozenset(), carrier])
    return FiniteTopologicalSpace(carrier=carrier, topology=topology)


# ---------------------------------------------------------------------------
# is_finite_space / is_infinite_space
# ---------------------------------------------------------------------------

class TestSpaceDetection:
    def test_finite_space_detected(self):
        space = _discrete2()
        assert is_finite_space(space) is True
        assert is_infinite_space(space) is False

    def test_infinite_space_detected(self):
        space = DiscreteInfiniteSpace(carrier="N")
        assert is_infinite_space(space) is True
        assert is_finite_space(space) is False

    def test_dict_is_neither(self):
        assert is_finite_space({"tags": ["compact"]}) is False
        assert is_infinite_space({"tags": ["compact"]}) is False

    def test_none_is_neither(self):
        assert is_finite_space(None) is False
        assert is_infinite_space(None) is False


# ---------------------------------------------------------------------------
# property_registry
# ---------------------------------------------------------------------------

class TestPropertyRegistry:
    def test_returns_dict(self):
        reg = property_registry()
        assert isinstance(reg, dict)

    def test_core_properties_present(self):
        reg = property_registry()
        for prop in ("compact", "connected", "hausdorff", "t0", "t1",
                     "regular", "normal", "lindelof", "path_connected"):
            assert prop in reg, f"Missing: {prop}"

    def test_each_entry_is_pair(self):
        reg = property_registry()
        for name, (finite_fn, inf_fn) in reg.items():
            assert callable(finite_fn), f"{name}: finite_fn not callable"
            assert callable(inf_fn), f"{name}: inf_fn not callable"


# ---------------------------------------------------------------------------
# analyze_property — dict/tag-based input
# ---------------------------------------------------------------------------

class TestAnalyzePropertyDict:
    def test_compact_tag_true(self):
        r = analyze_property({"tags": ["compact"]}, "compact")
        assert r.is_true

    def test_noncompact_tag_false(self):
        r = analyze_property({"tags": ["noncompact"]}, "compact")
        assert r.is_false

    def test_connected_tag_true(self):
        r = analyze_property({"tags": ["connected"]}, "connected")
        assert r.is_true

    def test_hausdorff_tag_true(self):
        r = analyze_property({"tags": ["hausdorff"]}, "hausdorff")
        assert r.is_true

    def test_t2_alias_for_hausdorff(self):
        r1 = analyze_property({"tags": ["hausdorff"]}, "t2")
        r2 = analyze_property({"tags": ["hausdorff"]}, "hausdorff")
        assert r1.is_true == r2.is_true

    def test_path_connected_hyphen_alias(self):
        r = analyze_property({"tags": ["path_connected"]}, "path-connected")
        assert r.is_true

    def test_unknown_property_returns_unknown(self):
        r = analyze_property({}, "frobeniuscompact")
        assert r.is_unknown
        assert "not in the unified dispatch registry" in r.justification[0]

    def test_result_has_value(self):
        r = analyze_property({"tags": ["compact"]}, "compact")
        assert r.value is not None


# ---------------------------------------------------------------------------
# analyze_property — FiniteTopologicalSpace
# ---------------------------------------------------------------------------

class TestAnalyzePropertyFinite:
    def test_finite_compact(self):
        r = analyze_property(_discrete2(), "compact")
        assert r.is_true

    def test_finite_connected_indiscrete(self):
        r = analyze_property(_indiscrete2(), "connected")
        assert r.is_true

    def test_finite_hausdorff_discrete(self):
        r = analyze_property(_discrete2(), "hausdorff")
        assert r.is_true

    def test_finite_hausdorff_indiscrete_false(self):
        r = analyze_property(_indiscrete2(), "hausdorff")
        assert r.is_false

    def test_finite_t0_result_type(self):
        from pytop.result import Result
        r = analyze_property(_discrete2(), "t0")
        assert isinstance(r, Result)

    def test_finite_normal(self):
        r = analyze_property(_discrete2(), "normal")
        assert r.is_true

    def test_finite_lindelof(self):
        r = analyze_property(_discrete2(), "lindelof")
        assert r.is_true


# ---------------------------------------------------------------------------
# analyze_property — InfiniteTopologicalSpace
# ---------------------------------------------------------------------------

class TestAnalyzePropertyInfinite:
    def test_indiscrete_infinite_compact(self):
        space = IndiscreteInfiniteSpace(carrier="R")
        r = analyze_property(space, "compact")
        assert r.is_true

    def test_discrete_infinite_not_compact(self):
        space = DiscreteInfiniteSpace(carrier="N")
        r = analyze_property(space, "compact")
        assert r.is_false

    def test_infinite_space_lindelof(self):
        from pytop.infinite_spaces import CocountableSpace
        space = CocountableSpace(carrier="R")
        r = analyze_property(space, "lindelof")
        assert r.is_true

    def test_t2_alias_dispatches_to_infinite(self):
        space = DiscreteInfiniteSpace(carrier="N")
        r = analyze_property(space, "t2")
        # Discrete infinite space is Hausdorff
        assert r.is_true or r.is_unknown


# ---------------------------------------------------------------------------
# analyze_space
# ---------------------------------------------------------------------------

class TestAnalyzeSpace:
    def test_returns_dict(self):
        result = analyze_space({"tags": ["compact"]})
        assert isinstance(result, dict)

    def test_all_registry_keys_present_by_default(self):
        result = analyze_space({})
        reg = property_registry()
        for key in reg:
            assert key in result

    def test_specific_properties_subset(self):
        result = analyze_space({"tags": ["compact"]}, ["compact", "connected"])
        assert set(result.keys()) == {"compact", "connected"}

    def test_all_values_are_results(self):
        from pytop.result import Result
        result = analyze_space({"tags": ["hausdorff"]})
        for v in result.values():
            assert isinstance(v, Result)


# ---------------------------------------------------------------------------
# Convenience reports
# ---------------------------------------------------------------------------

class TestConvenienceReports:
    def test_unified_compactness_report_keys(self):
        d = unified_compactness_report({"tags": ["compact"]})
        for key in ("compact", "countably_compact", "sequentially_compact",
                    "limit_point_compact", "lindelof"):
            assert key in d

    def test_unified_connectedness_report_keys(self):
        d = unified_connectedness_report({})
        assert "connected" in d
        assert "path_connected" in d

    def test_unified_separation_report_keys(self):
        d = unified_separation_report({})
        for key in ("t0", "t1", "hausdorff", "regular", "normal"):
            assert key in d

    def test_compactness_compact_tag_true(self):
        d = unified_compactness_report({"tags": ["compact"]})
        assert d["compact"].is_true

    def test_separation_hausdorff_tag_true(self):
        d = unified_separation_report({"tags": ["hausdorff"]})
        assert d["hausdorff"].is_true

    def test_convenience_reports_return_dicts(self):
        for fn in (unified_compactness_report, unified_connectedness_report,
                   unified_separation_report):
            assert isinstance(fn({}), dict)
