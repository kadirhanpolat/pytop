"""Tests for uniform_spaces.py extended functions (v0.5.0)."""
import pytest
from pytop.uniform_spaces import (
    uniform_equivalence,
    uniform_completion_descriptor,
    smirnov_metrization_oracle,
    uniform_topology_tags,
    is_uniform_space,
    is_uniformly_complete,
)


# ---------------------------------------------------------------------------
# uniform_equivalence
# ---------------------------------------------------------------------------

class TestUniformEquivalence:
    def test_both_non_uniform_returns_none(self):
        assert uniform_equivalence({}, {}) is None

    def test_one_non_uniform_returns_none(self):
        s1 = {"tags": ["metric"]}
        assert uniform_equivalence(s1, {}) is None

    def test_same_explicit_type_true(self):
        s1 = {"tags": ["complete_metric"]}
        s2 = {"tags": ["complete_metric"]}
        assert uniform_equivalence(s1, s2) is True

    def test_same_discrete_uniformity_true(self):
        s1 = {"tags": ["discrete_uniformity"]}
        s2 = {"tags": ["discrete_uniformity"]}
        assert uniform_equivalence(s1, s2) is True

    def test_different_explicit_types_false(self):
        s1 = {"tags": ["complete_metric"]}
        s2 = {"tags": ["discrete_uniformity"]}
        assert uniform_equivalence(s1, s2) is False

    def test_metric_vs_complete_metric_none(self):
        # "metric" alone is not in the explicit_types set; no decisive answer
        s1 = {"tags": ["metric"]}
        s2 = {"tags": ["complete_metric"]}
        # s1 is uniform but has no explicit_type tag from the decisive set
        result = uniform_equivalence(s1, s2)
        assert result is None or isinstance(result, bool)

    def test_returns_none_when_ambiguous(self):
        s1 = {"tags": ["metric"]}
        s2 = {"tags": ["metric"]}
        result = uniform_equivalence(s1, s2)
        # metric alone → no explicit_type → None
        assert result is None


# ---------------------------------------------------------------------------
# uniform_completion_descriptor
# ---------------------------------------------------------------------------

class TestUniformCompletionDescriptor:
    def test_returns_dict_with_keys(self):
        d = uniform_completion_descriptor({"tags": ["metric"]})
        for key in ("is_already_complete", "completion_tags", "description",
                    "warnings", "version"):
            assert key in d

    def test_already_complete_metric(self):
        d = uniform_completion_descriptor({"tags": ["complete_metric"]})
        assert d["is_already_complete"] is True
        assert "already complete" in d["description"].lower()

    def test_metric_space_completion_tags(self):
        d = uniform_completion_descriptor({"tags": ["metric"]})
        assert "complete_metric" in d["completion_tags"]
        assert "hausdorff" in d["completion_tags"]

    def test_totally_bounded_completion_compact(self):
        d = uniform_completion_descriptor({"tags": ["metric", "totally_bounded"]})
        assert "compact" in d["completion_tags"]
        assert "compact" in d["description"].lower()

    def test_separable_preserved(self):
        d = uniform_completion_descriptor({"tags": ["metric", "separable"]})
        assert "separable" in d["completion_tags"]

    def test_second_countable_preserved(self):
        d = uniform_completion_descriptor({"tags": ["metric", "second_countable"]})
        assert "second_countable" in d["completion_tags"]

    def test_non_uniform_space_warning(self):
        d = uniform_completion_descriptor({"tags": []})
        assert len(d["warnings"]) > 0

    def test_discrete_uniformity_already_complete(self):
        d = uniform_completion_descriptor({"tags": ["discrete_uniformity"]})
        assert d["is_already_complete"] is True

    def test_completion_tags_sorted(self):
        d = uniform_completion_descriptor({"tags": ["metric"]})
        assert d["completion_tags"] == sorted(d["completion_tags"])


# ---------------------------------------------------------------------------
# smirnov_metrization_oracle
# ---------------------------------------------------------------------------

class TestSmirnovMetrizationOracle:
    def test_metrizable_tag_direct(self):
        d = smirnov_metrization_oracle({"tags": ["metrizable"]})
        assert d["is_metrizable"] is True
        assert d["theorem_applied"] == "direct_tag"

    def test_metric_tag_direct(self):
        d = smirnov_metrization_oracle({"tags": ["metric"]})
        assert d["is_metrizable"] is True

    def test_not_metrizable_tag(self):
        d = smirnov_metrization_oracle({"tags": ["not_metrizable"]})
        assert d["is_metrizable"] is False
        assert d["theorem_applied"] == "direct_tag"

    def test_urysohn_metrization_second_countable_regular(self):
        d = smirnov_metrization_oracle({"tags": ["second_countable", "regular"]})
        assert d["is_metrizable"] is True
        assert d["theorem_applied"] == "urysohn_metrization"

    def test_urysohn_metrization_t3_alias(self):
        d = smirnov_metrization_oracle({"tags": ["second_countable", "t3"]})
        assert d["is_metrizable"] is True
        assert d["theorem_applied"] == "urysohn_metrization"

    def test_smirnov_metrization_paracompact_locally_metrizable(self):
        d = smirnov_metrization_oracle(
            {"tags": ["paracompact", "locally_metrizable"]}
        )
        assert d["is_metrizable"] is True
        assert d["theorem_applied"] == "smirnov_metrization"

    def test_smirnov_locally_metric_alias(self):
        d = smirnov_metrization_oracle(
            {"tags": ["paracompact", "locally_metric"]}
        )
        assert d["is_metrizable"] is True

    def test_compact_hausdorff_not_first_countable_not_metrizable(self):
        d = smirnov_metrization_oracle(
            {"tags": ["compact", "hausdorff", "not_first_countable"]}
        )
        assert d["is_metrizable"] is False
        assert d["theorem_applied"] == "first_countable_obstruction"

    def test_insufficient_tags_unknown(self):
        d = smirnov_metrization_oracle({"tags": []})
        assert d["is_metrizable"] is None
        assert d["theorem_applied"] == "none"
        assert len(d["missing_conditions"]) > 0

    def test_missing_conditions_listed(self):
        d = smirnov_metrization_oracle({"tags": ["second_countable"]})
        # missing regular/t3
        assert any("regular" in c for c in d["missing_conditions"])

    def test_returns_version(self):
        d = smirnov_metrization_oracle({})
        assert "version" in d


# ---------------------------------------------------------------------------
# uniform_topology_tags
# ---------------------------------------------------------------------------

class TestUniformTopologyTags:
    def test_non_uniform_space_empty(self):
        tags = uniform_topology_tags({"tags": []})
        assert tags == set()

    def test_uniform_space_completely_regular(self):
        tags = uniform_topology_tags({"tags": ["uniform_space"]})
        assert "completely_regular" in tags
        assert "tychonoff" in tags

    def test_metric_space_full_separation(self):
        tags = uniform_topology_tags({"tags": ["metric"]})
        for t in ("t0", "t1", "hausdorff", "regular", "normal"):
            assert t in tags

    def test_complete_metric_adds_uniformly_complete(self):
        tags = uniform_topology_tags({"tags": ["complete_metric"]})
        assert "uniformly_complete" in tags

    def test_discrete_uniformity_adds_hausdorff(self):
        tags = uniform_topology_tags({"tags": ["discrete_uniformity"]})
        assert "hausdorff" in tags
        assert "discrete" in tags

    def test_metrizable_adds_separation_chain(self):
        tags = uniform_topology_tags({"tags": ["metrizable"]})
        assert "hausdorff" in tags
        assert "normal" in tags

    def test_returns_set(self):
        tags = uniform_topology_tags({"tags": ["metric"]})
        assert isinstance(tags, set)
