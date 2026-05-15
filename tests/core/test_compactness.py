from pytop.compactness import (
    analyze_compactness,
    is_compact,
    is_lindelof,
    is_sequentially_compact,
)
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import BasisDefinedSpace, MetricLikeSpace


def test_finite_spaces_are_exactly_compact():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1, 2}])
    result = is_compact(space)
    assert result.is_true
    assert result.is_exact
    assert result.metadata["representation"] == "finite"


def test_metric_space_with_noncompact_tag_is_false():
    space = MetricLikeSpace(carrier="R", tags={"not_compact"})
    result = is_compact(space)
    assert result.is_false
    assert result.mode == "theorem"


def test_basis_defined_second_countable_space_is_theorem_lindelof():
    space = BasisDefinedSpace(carrier="X", tags={"second_countable"})
    result = is_lindelof(space)
    assert result.is_true
    assert result.is_theorem_based


def test_symbolic_compactness_without_data_is_unknown():
    result = analyze_compactness({"representation": "symbolic_general"}, "compact")
    assert result.is_unknown


def test_finite_spaces_are_sequentially_compact():
    space = FiniteTopologicalSpace(carrier={1}, topology=[set(), {1}])
    result = is_sequentially_compact(space)
    assert result.is_true
    assert result.is_exact
