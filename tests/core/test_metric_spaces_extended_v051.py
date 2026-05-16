"""Coverage-targeted tests for metric_spaces.py (v0.5.1)."""
import pytest
from pytop.metric_spaces import (
    MetricSpace,
    FiniteMetricSpace,
    open_ball,
    closed_ball,
    distance_to_subset,
    is_bounded_subset,
    capped_metric,
    finite_product_metric_space,
    validate_metric,
    induced_topological_space,
    _has_finite_length,
)


def _disc(pts):
    return {(x, y): 0.0 if x == y else 1.0 for x in pts for y in pts}


def _two():
    return FiniteMetricSpace(carrier=[1, 2], distance=_disc([1, 2]))


# ---------------------------------------------------------------------------
# open_ball — negative radius (line 79)
# ---------------------------------------------------------------------------

def test_open_ball_negative_radius():
    with pytest.raises(ValueError, match="nonneg"):
        open_ball(_two(), 1, -0.5)


# ---------------------------------------------------------------------------
# open_ball — carrier=None (line 81)
# ---------------------------------------------------------------------------

def test_open_ball_none_carrier():
    space = MetricSpace(carrier=None, distance=lambda x, y: 0.0)
    with pytest.raises(ValueError, match="explicit carrier"):
        open_ball(space, 1, 0.5)


# ---------------------------------------------------------------------------
# closed_ball — carrier=None (line 95)
# ---------------------------------------------------------------------------

def test_closed_ball_none_carrier():
    space = MetricSpace(carrier=None, distance=lambda x, y: 0.0)
    with pytest.raises(ValueError, match="explicit carrier"):
        closed_ball(space, 1, 0.5)


# ---------------------------------------------------------------------------
# capped_metric — cap <= 0 (line 149)
# ---------------------------------------------------------------------------

def test_capped_metric_nonpositive_cap():
    with pytest.raises(ValueError, match="strictly positive"):
        capped_metric(_disc([1, 2]), cap=0.0)


def test_capped_metric_negative_cap():
    with pytest.raises(ValueError, match="strictly positive"):
        capped_metric(_disc([1, 2]), cap=-1.0)


# ---------------------------------------------------------------------------
# product_distance — wrong-length args (line 195)
# ---------------------------------------------------------------------------

def test_product_distance_wrong_length():
    s = _two()
    prod = finite_product_metric_space(s, s)
    with pytest.raises(ValueError, match="one coordinate per factor"):
        prod.distance_between((1,), (2,))


# ---------------------------------------------------------------------------
# validate_metric — diagonal exception (lines 242-243)
# ---------------------------------------------------------------------------

def test_validate_metric_diagonal_exception():
    def bad_diag(x, y):
        if x == y:
            raise RuntimeError("diagonal boom")
        return 1.0
    space = FiniteMetricSpace(carrier=[1, 2], distance=bad_diag)
    result = validate_metric(space)
    assert result.is_false


# ---------------------------------------------------------------------------
# validate_metric — triangle exception (lines 286-287)
# ---------------------------------------------------------------------------

def test_validate_metric_triangle_exception():
    count = [0]

    def d_fails_after_pairs(x, y):
        if x == y:
            return 0.0
        count[0] += 1
        if count[0] > 2:
            raise RuntimeError("triangle boom")
        return 1.0

    space = FiniteMetricSpace(carrier=[1, 2], distance=d_fails_after_pairs)
    result = validate_metric(space)
    assert result.is_false


# ---------------------------------------------------------------------------
# induced_topological_space — invalid metric (line 328)
# ---------------------------------------------------------------------------

def test_induced_topological_space_invalid_metric():
    bad_d = {(1, 1): 0.0, (1, 2): -1.0, (2, 1): -1.0, (2, 2): 0.0}
    space = FiniteMetricSpace(carrier=[1, 2], distance=bad_d)
    with pytest.raises(ValueError, match="does not define a metric"):
        induced_topological_space(space)


# ---------------------------------------------------------------------------
# _distance_between — None distance (line 363)
# ---------------------------------------------------------------------------

def test_distance_between_none_distance():
    space = MetricSpace(carrier=[1, 2], distance=None)
    with pytest.raises(ValueError, match="requires a distance specification"):
        space.distance_between(1, 2)


# ---------------------------------------------------------------------------
# _normalize_explicit_subset_allow_empty — None subset (line 383)
# ---------------------------------------------------------------------------

def test_distance_to_subset_none_raises():
    with pytest.raises(ValueError, match="explicit iterable"):
        distance_to_subset(_two(), 1, None)


def test_distance_to_subset_str_raises():
    with pytest.raises(ValueError, match="explicit iterable"):
        distance_to_subset(_two(), 1, "points")


# ---------------------------------------------------------------------------
# _normalize_explicit_subset_allow_empty — TypeError (lines 386-387)
# ---------------------------------------------------------------------------

def test_is_bounded_subset_non_iterable():
    class NotIterable:
        def __iter__(self):
            raise TypeError("not iterable")

    with pytest.raises(ValueError, match="explicit iterable"):
        is_bounded_subset(_two(), NotIterable())


# ---------------------------------------------------------------------------
# _normalize_product_factors — single list arg (line 394)
# ---------------------------------------------------------------------------

def test_finite_product_single_list_arg():
    s = _two()
    prod = finite_product_metric_space([s, s])
    assert len(prod.carrier) == 4  # 2×2


# ---------------------------------------------------------------------------
# _normalize_product_factors — empty list (line 398)
# ---------------------------------------------------------------------------

def test_finite_product_empty_list():
    with pytest.raises(ValueError, match="at least one factor"):
        finite_product_metric_space([])


# ---------------------------------------------------------------------------
# _normalize_product_factors — non-MetricSpace factor (line 402)
# ---------------------------------------------------------------------------

def test_finite_product_non_metric_factor():
    with pytest.raises(TypeError, match="is not a MetricSpace"):
        finite_product_metric_space("not_a_metric")


# ---------------------------------------------------------------------------
# _normalize_product_factors — non-finite carrier (line 404)
# ---------------------------------------------------------------------------

def test_finite_product_infinite_carrier():
    space = MetricSpace(carrier="R", distance=lambda x, y: 0.0)
    with pytest.raises(ValueError, match="explicit finite carriers"):
        finite_product_metric_space(space)


# ---------------------------------------------------------------------------
# _has_finite_length — exception path (lines 415-416)
# ---------------------------------------------------------------------------

def test_has_finite_length_no_len_attr():
    class NoLen:
        pass

    assert _has_finite_length(NoLen()) is False


def test_has_finite_length_runtime_error():
    class Explodes:
        def __len__(self):
            raise RuntimeError("kaboom")

    assert _has_finite_length(Explodes()) is False


def test_metric_space_with_no_len_carrier_not_tagged_finite():
    class NoLen:
        pass

    space = MetricSpace(carrier=NoLen(), distance=lambda x, y: 0.0)
    assert not space.has_tag("finite")
