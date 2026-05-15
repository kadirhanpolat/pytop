from pytop.countability import (
    countability_report,
    is_first_countable,
    is_lindelof,
    is_second_countable,
    is_separable,
    render_countability_report,
)
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_countability import (
    is_first_countable_infinite,
    is_second_countable_infinite,
    render_infinite_countability_report,
)
from pytop.infinite_spaces import (
    BasisDefinedSpace,
    CofiniteSpace,
    DiscreteInfiniteSpace,
    MetricLikeSpace,
    SorgenfreyLikeSpace,
)


def test_finite_space_is_second_countable_exactly():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1, 2}])
    result = is_second_countable(space)
    assert result.is_true
    assert result.is_exact


def test_metric_space_is_first_countable_by_theorem():
    space = MetricLikeSpace(carrier="R")
    result = is_first_countable(space)
    assert result.is_true
    assert result.is_theorem_based


def test_second_countable_tag_implies_first_countable_by_theorem():
    space = BasisDefinedSpace(carrier="X", tags={"second_countable"})
    result = is_first_countable(space)
    assert result.is_true
    assert result.is_theorem_based


def test_second_countable_tag_implies_separable():
    space = BasisDefinedSpace(carrier="X", tags={"second_countable"})
    result = is_separable(space)
    assert result.is_true
    assert result.is_theorem_based


def test_separable_metric_space_is_second_countable_by_theorem():
    space = MetricLikeSpace(carrier="R", tags={"separable"})
    result = is_second_countable(space)
    assert result.is_true
    assert result.is_theorem_based


def test_uncountable_discrete_space_is_neither_second_countable_nor_separable():
    space = DiscreteInfiniteSpace(carrier="R")
    assert is_second_countable(space).is_false
    assert is_separable(space).is_false


def test_negative_tag_for_lindelof_is_respected():
    space = BasisDefinedSpace(carrier="X", tags={"not_lindelof"})
    result = is_lindelof(space)
    assert result.is_false


def test_sorgenfrey_like_space_stays_separable_but_not_second_countable():
    space = SorgenfreyLikeSpace(carrier="R")
    assert is_separable(space).is_true
    assert is_second_countable(space).is_false


def test_countability_report_exposes_inference_rule_for_metric_plus_separable():
    space = MetricLikeSpace(carrier="R", tags={"separable"})
    report = countability_report(space)
    assert report["second_countable"].is_true
    assert report["second_countable"].metadata["inference_rule"] == "separable_metric_implies_second_countable"


def test_render_countability_report_lists_theorem_corridor():
    space = MetricLikeSpace(carrier="R", tags={"separable"})
    rendered = render_countability_report(space)
    assert "Countability report for MetricLikeSpace" in rendered
    assert "separable_metric_implies_second_countable" in rendered


def test_basis_size_continuum_does_not_force_second_countable_tag():
    space = BasisDefinedSpace(carrier="X", metadata={"basis_size": "continuum"})
    assert is_second_countable(space).is_unknown


def test_explicit_negative_tag_beats_metric_theorem_line():
    space = BasisDefinedSpace(carrier="X", tags={"metric", "not_first_countable"})
    result = is_first_countable(space)
    assert result.is_false


def test_uncountable_cofinite_space_keeps_exact_negative_classification():
    space = CofiniteSpace(carrier="R", metadata={"basis_size": "aleph_0"})
    first_result = is_first_countable_infinite(space)
    second_result = is_second_countable_infinite(space)
    assert first_result.is_false and first_result.is_exact
    assert second_result.is_false and second_result.is_exact


def test_render_infinite_countability_report_mentions_general_report_mirror():
    space = CofiniteSpace(carrier="R")
    rendered = render_infinite_countability_report(space)
    assert "Infinite-space countability report for CofiniteSpace" in rendered
    assert "General report mirror:" in rendered
