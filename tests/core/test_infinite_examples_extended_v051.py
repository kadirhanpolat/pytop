"""Coverage-targeted tests for infinite_examples.py (v0.5.1)."""
from pytop.infinite_examples import (
    basis_defined_second_countable,
    closed_unit_interval_metric,
    integers_discrete,
    lower_limit_line_like,
    naturals_cofinite,
    naturals_discrete,
    rationals_metric,
    real_line_metric,
    real_line_order_topology,
    real_plane_metric,
    reals_cocountable,
    reals_indiscrete,
    sorgenfrey_line_like,
    upper_limit_line_like,
)
from pytop.infinite_spaces import (
    BasisDefinedSpace,
    CocountableSpace,
    CofiniteSpace,
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
    SorgenfreyLikeSpace,
)
from pytop.metric_spaces import SymbolicMetricSpace

# ---------------------------------------------------------------------------
# integers_discrete  (line 27)
# ---------------------------------------------------------------------------

def test_integers_discrete_type():
    space = integers_discrete()
    assert isinstance(space, DiscreteInfiniteSpace)


def test_integers_discrete_carrier():
    space = integers_discrete()
    assert space.carrier == "Z"


def test_integers_discrete_description():
    space = integers_discrete()
    assert "integer" in space.metadata["description"].lower()


# ---------------------------------------------------------------------------
# rationals_metric  (line 91)
# ---------------------------------------------------------------------------

def test_rationals_metric_type():
    space = rationals_metric()
    assert isinstance(space, SymbolicMetricSpace)


def test_rationals_metric_carrier():
    space = rationals_metric()
    assert space.carrier == "Q"


def test_rationals_metric_tags():
    space = rationals_metric()
    assert "second_countable" in space.tags


# ---------------------------------------------------------------------------
# sorgenfrey_line_like  (line 248)
# ---------------------------------------------------------------------------

def test_sorgenfrey_line_like_type():
    space = sorgenfrey_line_like()
    assert isinstance(space, SorgenfreyLikeSpace)


def test_sorgenfrey_line_like_same_as_lower_limit():
    s1 = sorgenfrey_line_like()
    s2 = lower_limit_line_like()
    assert type(s1) is type(s2)
    assert s1.carrier == s2.carrier


# ---------------------------------------------------------------------------
# basis_defined_second_countable  (line 252)
# ---------------------------------------------------------------------------

def test_basis_defined_second_countable_type():
    space = basis_defined_second_countable()
    assert isinstance(space, BasisDefinedSpace)


def test_basis_defined_second_countable_tags():
    space = basis_defined_second_countable()
    assert "second_countable" in space.tags


# ---------------------------------------------------------------------------
# All other factory functions — smoke tests
# ---------------------------------------------------------------------------

def test_naturals_discrete():
    space = naturals_discrete()
    assert isinstance(space, DiscreteInfiniteSpace)
    assert space.carrier == "N"


def test_naturals_cofinite():
    space = naturals_cofinite()
    assert isinstance(space, CofiniteSpace)


def test_reals_indiscrete():
    space = reals_indiscrete()
    assert isinstance(space, IndiscreteInfiniteSpace)


def test_reals_cocountable():
    space = reals_cocountable()
    assert isinstance(space, CocountableSpace)


def test_real_line_metric():
    space = real_line_metric()
    assert isinstance(space, SymbolicMetricSpace)
    assert "connected" in space.tags


def test_closed_unit_interval_metric():
    space = closed_unit_interval_metric()
    assert isinstance(space, SymbolicMetricSpace)
    assert "compact" in space.tags


def test_real_plane_metric():
    space = real_plane_metric()
    assert isinstance(space, SymbolicMetricSpace)
    assert space.carrier == "R^2"


def test_real_line_order_topology():
    space = real_line_order_topology()
    assert isinstance(space, SymbolicMetricSpace)
    assert "order_topology" in space.tags


def test_lower_limit_line_like():
    space = lower_limit_line_like()
    assert isinstance(space, SorgenfreyLikeSpace)
    assert "sorgenfrey" in space.tags


def test_upper_limit_line_like():
    space = upper_limit_line_like()
    assert isinstance(space, SorgenfreyLikeSpace)
    assert "upper_limit_topology" in space.tags
