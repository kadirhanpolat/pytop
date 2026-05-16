"""Coverage-targeted tests for infinite_constructions.py (v0.5.1)."""
import pytest
from pytop.infinite_constructions import (
    subspace,
    product,
    disjoint_sum,
    _construction_class_for,
)
from pytop.infinite_spaces import (
    BasisDefinedSpace,
    CocountableSpace,
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
    InfiniteTopologicalSpace,
    MetricLikeSpace,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discrete():
    return DiscreteInfiniteSpace(carrier="N", tags={"compact"})


def _indiscrete():
    return IndiscreteInfiniteSpace(carrier="R", tags={"connected", "compact"})


def _metric():
    return MetricLikeSpace(carrier="R", tags={"metric", "connected", "compact"})


def _basis():
    return BasisDefinedSpace(carrier="X", tags={"second_countable"})


# ---------------------------------------------------------------------------
# subspace — open (line 22) and dense (line 24)
# ---------------------------------------------------------------------------

def test_subspace_open_tag():
    space = _indiscrete()
    sub = subspace(space, "U", open=True)
    assert "open_subspace" in sub.tags


def test_subspace_dense_tag():
    space = _indiscrete()
    sub = subspace(space, "D", dense=True)
    assert "dense_subspace" in sub.tags


def test_subspace_closed_tag():
    space = _indiscrete()
    sub = subspace(space, "C", closed=True)
    assert "closed_subspace" in sub.tags


def test_subspace_ambient_tags():
    space = DiscreteInfiniteSpace(carrier="N", tags={"compact"})
    sub = subspace(space, "A")
    assert "ambient_compact" in sub.tags


def test_subspace_connected_ambient():
    space = IndiscreteInfiniteSpace(carrier="R", tags={"connected"})
    sub = subspace(space, "B")
    assert "ambient_connected" in sub.tags


# ---------------------------------------------------------------------------
# product — no args raises ValueError (line 45)
# ---------------------------------------------------------------------------

def test_product_no_args_raises():
    with pytest.raises(ValueError, match="at least one"):
        product()


def test_product_single_space():
    result = product(_indiscrete())
    assert result is not None


def test_product_two_spaces():
    s1 = DiscreteInfiniteSpace(carrier="N", tags={"t0", "hausdorff"})
    s2 = DiscreteInfiniteSpace(carrier="N", tags={"t0", "hausdorff"})
    result = product(s1, s2)
    assert "t0" in result.tags
    assert "hausdorff" in result.tags


# ---------------------------------------------------------------------------
# product — compact tag (line 67)
# ---------------------------------------------------------------------------

def test_product_compact_tag_propagated():
    s1 = IndiscreteInfiniteSpace(carrier="X", tags={"compact"})
    s2 = IndiscreteInfiniteSpace(carrier="Y", tags={"compact"})
    result = product(s1, s2)
    assert "compact" in result.tags


def test_product_compact_not_propagated_when_missing():
    s1 = IndiscreteInfiniteSpace(carrier="X", tags={"compact"})
    s2 = DiscreteInfiniteSpace(carrier="N")  # no compact tag
    result = product(s1, s2)
    assert "compact" not in result.tags


def test_product_metric_class_used():
    s1 = MetricLikeSpace(carrier="R", tags={"metric"})
    s2 = MetricLikeSpace(carrier="R", tags={"metric"})
    result = product(s1, s2)
    assert isinstance(result, MetricLikeSpace)


# ---------------------------------------------------------------------------
# disjoint_sum — no args raises ValueError (line 78)
# ---------------------------------------------------------------------------

def test_disjoint_sum_no_args_raises():
    with pytest.raises(ValueError, match="at least one"):
        disjoint_sum()


def test_disjoint_sum_single_space():
    result = disjoint_sum(_indiscrete())
    assert result is not None


def test_disjoint_sum_two_spaces_not_connected():
    s1 = DiscreteInfiniteSpace(carrier="N")
    s2 = DiscreteInfiniteSpace(carrier="N")
    result = disjoint_sum(s1, s2)
    assert "not_connected" in result.tags


# ---------------------------------------------------------------------------
# disjoint_sum — compact tag (line 86)
# ---------------------------------------------------------------------------

def test_disjoint_sum_compact_tag_propagated():
    s1 = IndiscreteInfiniteSpace(carrier="X", tags={"compact"})
    s2 = IndiscreteInfiniteSpace(carrier="Y", tags={"compact"})
    result = disjoint_sum(s1, s2)
    assert "compact" in result.tags


def test_disjoint_sum_compact_not_propagated_when_missing():
    s1 = IndiscreteInfiniteSpace(carrier="X", tags={"compact"})
    s2 = DiscreteInfiniteSpace(carrier="N")
    result = disjoint_sum(s1, s2)
    assert "compact" not in result.tags


def test_disjoint_sum_first_countable_propagated():
    s1 = DiscreteInfiniteSpace(carrier="N", tags={"first_countable"})
    s2 = DiscreteInfiniteSpace(carrier="N", tags={"first_countable"})
    result = disjoint_sum(s1, s2)
    assert "first_countable" in result.tags


# ---------------------------------------------------------------------------
# _construction_class_for — MetricLikeSpace (line 105) and BasisDefinedSpace (107)
# ---------------------------------------------------------------------------

def test_construction_class_for_metric_like():
    space = MetricLikeSpace(carrier="R", tags={"metric"})
    cls = _construction_class_for(space)
    assert cls is MetricLikeSpace


def test_construction_class_for_metric_tag():
    space = DiscreteInfiniteSpace(carrier="N", tags={"metric"})
    cls = _construction_class_for(space)
    assert cls is MetricLikeSpace


def test_construction_class_for_basis_defined():
    space = BasisDefinedSpace(carrier="X")
    cls = _construction_class_for(space)
    assert cls is BasisDefinedSpace


def test_construction_class_for_generic():
    space = DiscreteInfiniteSpace(carrier="N")
    cls = _construction_class_for(space)
    assert cls is InfiniteTopologicalSpace
