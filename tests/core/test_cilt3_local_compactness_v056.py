"""Tests for v0.1.56 Cilt III local compactness and compactification corridor.

Covers local_compactness.py:
  - is_locally_compact: finite exact, theorem-level (tagged), conditional (metric), unknown
  - one_point_compactification: topology construction, new point, open sets
  - alexandroff_point_check: finite always false, tagged spaces
  - local_compactness_profile: profile dict shape
  - analyze_local_compactness: single-call facade metadata
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.local_compactness import (
    is_locally_compact,
    one_point_compactification,
    alexandroff_point_check,
    local_compactness_profile,
    analyze_local_compactness,
    LocalCompactnessError,
)
import pytop
import pytest

# ---------------------------------------------------------------------------
# Shared test spaces
# ---------------------------------------------------------------------------

def _discrete2():
    """Two-point discrete space."""
    return FiniteTopologicalSpace(
        carrier=['a', 'b'],
        topology=[frozenset(), frozenset(['a']), frozenset(['b']), frozenset(['a', 'b'])],
    )


def _sierpinski():
    """Sierpiński space {0,1}, open sets: {}, {1}, {0,1}."""
    return FiniteTopologicalSpace(
        carrier=[0, 1],
        topology=[frozenset(), frozenset([1]), frozenset([0, 1])],
    )


def _three_point():
    """Three-point space {a,b,c} with topology {∅, {a}, {a,b}, {a,b,c}}."""
    return FiniteTopologicalSpace(
        carrier=['a', 'b', 'c'],
        topology=[
            frozenset(), frozenset(['a']),
            frozenset(['a', 'b']), frozenset(['a', 'b', 'c']),
        ],
    )


class _Tagged:
    """Minimal space object with tags for theorem-level testing."""
    def __init__(self, tags):
        self.tags = tags
        self.representation = "symbolic_general"


# ---------------------------------------------------------------------------
# is_locally_compact — finite exact
# ---------------------------------------------------------------------------

class TestIsLocallyCompactFinite:
    def test_discrete2_is_locally_compact(self):
        r = is_locally_compact(_discrete2())
        assert r.status == "true"
        assert r.mode == "exact"

    def test_sierpinski_is_locally_compact(self):
        r = is_locally_compact(_sierpinski())
        assert r.status == "true"
        assert r.mode == "exact"

    def test_three_point_is_locally_compact(self):
        r = is_locally_compact(_three_point())
        assert r.status == "true"
        assert r.mode == "exact"

    def test_finite_justification_mentions_finite(self):
        r = is_locally_compact(_discrete2())
        joined = " ".join(r.justification).lower()
        assert "finite" in joined

    def test_finite_result_has_representation_metadata(self):
        r = is_locally_compact(_discrete2())
        assert r.metadata.get("representation") == "finite"


# ---------------------------------------------------------------------------
# is_locally_compact — negative tag
# ---------------------------------------------------------------------------

class TestIsLocallyCompactNegativeTag:
    def test_not_locally_compact_tag_returns_false(self):
        space = _Tagged(["not_locally_compact"])
        r = is_locally_compact(space)
        assert r.status == "false"

    def test_negative_tag_justification_mentions_tag(self):
        space = _Tagged(["not_locally_compact"])
        r = is_locally_compact(space)
        joined = " ".join(r.justification).lower()
        assert "tag" in joined or "negative" in joined


# ---------------------------------------------------------------------------
# is_locally_compact — positive tags (theorem-level)
# ---------------------------------------------------------------------------

class TestIsLocallyCompactPositiveTags:
    def test_locally_compact_tag_returns_true(self):
        space = _Tagged(["locally_compact"])
        r = is_locally_compact(space)
        assert r.status == "true"
        assert r.mode == "theorem"

    def test_lc_hausdorff_tag_returns_true(self):
        space = _Tagged(["locally_compact_hausdorff"])
        r = is_locally_compact(space)
        assert r.status == "true"

    def test_compact_tag_implies_locally_compact(self):
        space = _Tagged(["compact"])
        r = is_locally_compact(space)
        assert r.status == "true"
        assert r.mode == "theorem"

    def test_compact_justification_mentions_compact(self):
        space = _Tagged(["compact"])
        r = is_locally_compact(space)
        joined = " ".join(r.justification).lower()
        assert "compact" in joined


# ---------------------------------------------------------------------------
# is_locally_compact — metric conditional
# ---------------------------------------------------------------------------

class TestIsLocallyCompactMetric:
    def test_metric_tag_is_conditional(self):
        space = _Tagged(["metric"])
        r = is_locally_compact(space)
        assert r.status == "conditional"

    def test_metrizable_tag_is_conditional(self):
        space = _Tagged(["metrizable"])
        r = is_locally_compact(space)
        assert r.status == "conditional"

    def test_conditional_justification_mentions_examples(self):
        space = _Tagged(["metric"])
        r = is_locally_compact(space)
        joined = " ".join(r.justification).lower()
        # Should mention both ℝⁿ / Hilbert or at least refer to counterexamples
        assert any(kw in joined for kw in ["rⁿ", "r^n", "hilbert", "ℝ", "l²", "ℓ", "tag"])


# ---------------------------------------------------------------------------
# is_locally_compact — unknown
# ---------------------------------------------------------------------------

class TestIsLocallyCompactUnknown:
    def test_no_tags_returns_unknown(self):
        space = _Tagged([])
        r = is_locally_compact(space)
        assert r.status == "unknown"


# ---------------------------------------------------------------------------
# one_point_compactification — structure
# ---------------------------------------------------------------------------

class TestOnePointCompactification:
    def test_new_point_added(self):
        ext = one_point_compactification(_discrete2())
        assert "∞" in ext.carrier

    def test_custom_label(self):
        ext = one_point_compactification(_discrete2(), point_label="omega")
        assert "omega" in ext.carrier

    def test_original_points_preserved(self):
        ext = one_point_compactification(_discrete2())
        assert "a" in ext.carrier
        assert "b" in ext.carrier

    def test_point_count_incremented(self):
        orig = _discrete2()
        ext = one_point_compactification(orig)
        assert len(ext.carrier) == len(orig.carrier) + 1

    def test_original_open_sets_present(self):
        orig = _discrete2()
        ext = one_point_compactification(orig)
        ext_top = [frozenset(u) for u in ext.topology]
        for u in orig.topology:
            assert frozenset(u) in ext_top

    def test_whole_space_is_open(self):
        orig = _discrete2()
        ext = one_point_compactification(orig)
        whole = frozenset(ext.carrier)
        ext_top = [frozenset(u) for u in ext.topology]
        assert whole in ext_top

    def test_empty_set_is_open(self):
        ext = one_point_compactification(_discrete2())
        ext_top = [frozenset(u) for u in ext.topology]
        assert frozenset() in ext_top

    def test_infty_union_complement_of_closed_is_open(self):
        """For each closed set C in original, {∞} ∪ (X \ C) must be open in extension."""
        orig = _discrete2()
        orig_points = frozenset(orig.carrier)
        orig_top = [frozenset(u) for u in orig.topology]
        closed_sets = [orig_points - u for u in orig_top]
        ext = one_point_compactification(orig)
        ext_top = [frozenset(u) for u in ext.topology]
        for c in closed_sets:
            expected = frozenset({"∞"}) | (orig_points - c)
            assert expected in ext_top

    def test_requires_finite_topological_space(self):
        with pytest.raises(LocalCompactnessError):
            one_point_compactification("not_a_space")

    def test_duplicate_label_raises(self):
        orig = _discrete2()
        with pytest.raises(LocalCompactnessError):
            one_point_compactification(orig, point_label="a")

    def test_sierpinski_extension_has_three_points(self):
        ext = one_point_compactification(_sierpinski())
        assert len(ext.carrier) == 3

    def test_three_point_extension_has_four_points(self):
        ext = one_point_compactification(_three_point())
        assert len(ext.carrier) == 4


# ---------------------------------------------------------------------------
# alexandroff_point_check
# ---------------------------------------------------------------------------

class TestAlexandroffPointCheck:
    def test_finite_space_always_false(self):
        r = alexandroff_point_check(_discrete2())
        assert r.status == "false"
        assert r.mode == "exact"

    def test_finite_justification_mentions_compact(self):
        r = alexandroff_point_check(_discrete2())
        joined = " ".join(r.justification).lower()
        assert "compact" in joined

    def test_locally_compact_hausdorff_noncompact_eligible(self):
        space = _Tagged(["locally_compact", "hausdorff"])
        r = alexandroff_point_check(space)
        # Non-compact by default (no compact tag) → eligible
        assert r.status == "true"

    def test_compact_space_not_eligible(self):
        space = _Tagged(["locally_compact", "hausdorff", "compact"])
        r = alexandroff_point_check(space)
        assert r.status == "false"

    def test_not_hausdorff_not_eligible(self):
        space = _Tagged(["locally_compact", "not_hausdorff"])
        r = alexandroff_point_check(space)
        assert r.status == "false"

    def test_not_locally_compact_not_eligible(self):
        space = _Tagged(["not_locally_compact"])
        r = alexandroff_point_check(space)
        assert r.status == "false"

    def test_eligible_result_metadata_has_flags(self):
        space = _Tagged(["locally_compact", "hausdorff"])
        r = alexandroff_point_check(space)
        if r.status == "true":
            assert "locally_compact" in r.metadata
            assert "hausdorff" in r.metadata


# ---------------------------------------------------------------------------
# local_compactness_profile
# ---------------------------------------------------------------------------

class TestLocalCompactnessProfile:
    def test_profile_has_four_keys(self):
        p = local_compactness_profile(_discrete2())
        assert set(p.keys()) == {
            "is_locally_compact", "is_hausdorff", "is_compact", "alexandroff_eligible"
        }

    def test_profile_all_results(self):
        from pytop.result import Result
        p = local_compactness_profile(_discrete2())
        for v in p.values():
            assert isinstance(v, Result)

    def test_discrete2_is_locally_compact_in_profile(self):
        p = local_compactness_profile(_discrete2())
        assert p["is_locally_compact"].status == "true"

    def test_discrete2_is_compact_in_profile(self):
        p = local_compactness_profile(_discrete2())
        assert p["is_compact"].status == "true"

    def test_discrete2_alexandroff_false_in_profile(self):
        p = local_compactness_profile(_discrete2())
        assert p["alexandroff_eligible"].status == "false"


# ---------------------------------------------------------------------------
# analyze_local_compactness
# ---------------------------------------------------------------------------

class TestAnalyzeLocalCompactness:
    def test_returns_result(self):
        from pytop.result import Result
        r = analyze_local_compactness(_discrete2())
        assert isinstance(r, Result)

    def test_finite_status_true(self):
        r = analyze_local_compactness(_discrete2())
        assert r.status == "true"

    def test_metadata_has_all_profile_fields(self):
        r = analyze_local_compactness(_discrete2())
        for key in ("is_locally_compact", "is_hausdorff", "is_compact", "alexandroff_eligible"):
            assert key in r.metadata

    def test_metadata_is_locally_compact_true(self):
        r = analyze_local_compactness(_discrete2())
        assert r.metadata["is_locally_compact"] == "true"

    def test_metadata_alexandroff_false_for_finite(self):
        r = analyze_local_compactness(_discrete2())
        assert r.metadata["alexandroff_eligible"] == "false"


# ---------------------------------------------------------------------------
# Public API surface (pytop top-level import)
# ---------------------------------------------------------------------------

class TestPublicAPISurface:
    def test_is_locally_compact_exported(self):
        assert hasattr(pytop, "is_locally_compact")

    def test_one_point_compactification_exported(self):
        assert hasattr(pytop, "one_point_compactification")

    def test_alexandroff_point_check_exported(self):
        assert hasattr(pytop, "alexandroff_point_check")

    def test_local_compactness_profile_exported(self):
        assert hasattr(pytop, "local_compactness_profile")

    def test_analyze_local_compactness_exported(self):
        assert hasattr(pytop, "analyze_local_compactness")

    def test_LocalCompactnessError_exported(self):
        assert hasattr(pytop, "LocalCompactnessError")

    def test_top_level_is_locally_compact_finite(self):
        r = pytop.is_locally_compact(_discrete2())
        assert r.status == "true"

    def test_top_level_one_point_compactification(self):
        ext = pytop.one_point_compactification(_discrete2())
        assert "∞" in ext.carrier
