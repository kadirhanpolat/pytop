from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import MetricLikeSpace
from pytop.theorem_engine import infer_feature


def test_finite_spaces_are_inferred_compact_by_theorem_rule():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1, 2}])
    result = infer_feature("compactness", space)
    assert result.is_true
    assert result.is_theorem_based
    assert "finite_spaces_are_compact" in result.metadata["matched_rules"]


def test_metric_space_infers_separation_support():
    space = MetricLikeSpace(carrier="R", metadata={"description": "the real line"})
    result = infer_feature("separation", space)
    assert result.is_true
    assert "metric_spaces_are_hausdorff" in result.metadata["matched_rules"]


def test_unknown_when_no_rule_matches():
    space = MetricLikeSpace(carrier="R", metadata={"description": "the real line"})
    result = infer_feature("invariants", space)
    assert result.is_unknown
    assert result.mode in {"symbolic", "mixed"}
