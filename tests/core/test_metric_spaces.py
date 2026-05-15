from math import isclose, sqrt

import pytest

from pytop.compactness import is_compact
from pytop.countability import is_first_countable
from pytop.metric_spaces import (
    FiniteMetricSpace,
    MetricSpace,
    capped_metric,
    closed_ball,
    diameter_of_subset,
    distance_between_subsets,
    distance_to_subset,
    finite_product_metric_space,
    induced_topological_space,
    is_bounded_subset,
    normalized_metric,
    open_ball,
    validate_metric,
)
from pytop.separation import is_hausdorff



def discrete_metric(x, y):
    return 0.0 if x == y else 1.0



def line_metric(x, y):
    return abs(x - y)



def bad_metric(x, y):
    table = {
        (0, 0): 0.0,
        (1, 1): 0.0,
        (2, 2): 0.0,
        (0, 1): 1.0,
        (1, 0): 1.0,
        (0, 2): 5.0,
        (2, 0): 5.0,
        (1, 2): 1.0,
        (2, 1): 1.0,
    }
    return table[(x, y)]



def diagonal_failure_metric(x, y):
    if x == y == 1:
        return 0.25
    return abs(x - y)



def asymmetric_metric(x, y):
    table = {
        (0, 0): 0.0,
        (1, 1): 0.0,
        (0, 1): 1.0,
        (1, 0): 2.0,
    }
    return table[(x, y)]



def zero_distinct_metric(x, y):
    if x == y:
        return 0.0
    if {x, y} == {0, 1}:
        return 0.0
    return 1.0



def dict_line_metric_space() -> FiniteMetricSpace:
    points = (0, 2, 5)
    table = {(x, y): abs(x - y) for x in points for y in points}
    return FiniteMetricSpace(carrier=points, distance=table)



def test_validate_metric_accepts_finite_discrete_metric():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=discrete_metric)
    result = validate_metric(space)
    assert result.is_true
    assert result.is_exact



def test_validate_metric_rejects_triangle_inequality_failure():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=bad_metric)
    result = validate_metric(space)
    assert result.is_false
    assert result.is_exact



def test_validate_metric_rejects_nonzero_diagonal():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=diagonal_failure_metric)
    result = validate_metric(space)
    assert result.is_false
    assert result.metadata['point'] == 1



def test_validate_metric_rejects_symmetry_failure():
    space = FiniteMetricSpace(carrier=(0, 1), distance=asymmetric_metric)
    result = validate_metric(space)
    assert result.is_false
    assert result.metadata['pair'] == (0, 1)



def test_validate_metric_rejects_zero_distance_for_distinct_points():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=zero_distinct_metric)
    result = validate_metric(space)
    assert result.is_false
    assert result.metadata['pair'] == (0, 1)



def test_validate_metric_rejects_missing_dictionary_pair():
    broken = FiniteMetricSpace(carrier=(0, 1), distance={(0, 0): 0.0, (1, 1): 0.0})
    result = validate_metric(broken)
    assert result.is_false
    assert 'exception' in result.metadata



def test_validate_metric_returns_unknown_for_symbolic_metric_carrier():
    space = MetricSpace(
        carrier='R',
        distance=lambda x, y: abs(x - y),
        metadata={'representation': 'infinite_metric'},
    )
    result = validate_metric(space)
    assert result.is_unknown
    assert result.is_symbolic



def test_open_ball_for_discrete_metric_is_singleton_for_small_radius():
    space = FiniteMetricSpace(carrier=('a', 'b', 'c'), distance=discrete_metric)
    assert open_ball(space, 'a', 0.5) == {'a'}



def test_closed_ball_includes_boundary_points():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=line_metric)
    assert closed_ball(space, 0, 1.0) == {0, 1}



def test_closed_ball_rejects_negative_radius():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=line_metric)
    with pytest.raises(ValueError):
        closed_ball(space, 0, -1)



def test_finite_metric_induces_discrete_finite_topology():
    space = FiniteMetricSpace(carrier=(0, 1), distance=discrete_metric)
    induced = induced_topological_space(space)
    assert induced.metadata['representation'] == 'finite'
    assert len(induced.topology) == 4
    assert is_compact(induced).is_true
    assert is_hausdorff(induced).is_true
    assert is_first_countable(induced).is_true



def test_symbolic_metric_induces_symbolic_metric_topological_space():
    space = MetricSpace(carrier='R', distance=lambda x, y: abs(x - y), metadata={'representation': 'infinite_metric'})
    induced = induced_topological_space(space)
    assert induced.metadata['representation'] == 'infinite_metric'
    assert 'metric' in induced.tags



def test_distance_to_subset_is_zero_for_membership():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    assert distance_to_subset(space, 2, {1, 2}) == 0.0



def test_distance_to_subset_computes_minimum_distance():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    assert distance_to_subset(space, 3, {0, 1}) == 2.0



def test_distance_to_subset_accepts_dictionary_backed_distance_data():
    space = dict_line_metric_space()
    assert distance_to_subset(space, 5, {0, 2}) == 3.0



def test_distance_to_subset_rejects_empty_subset():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=line_metric)
    with pytest.raises(ValueError):
        distance_to_subset(space, 1, set())



def test_distance_between_subsets_is_zero_for_intersection():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    assert distance_between_subsets(space, {0, 1}, {1, 3}) == 0.0



def test_distance_between_subsets_computes_minimum_pair_distance():
    space = dict_line_metric_space()
    assert distance_between_subsets(space, {0}, {2, 5}) == 2.0



def test_distance_between_subsets_rejects_empty_input():
    space = FiniteMetricSpace(carrier=(0, 1, 2), distance=line_metric)
    with pytest.raises(ValueError):
        distance_between_subsets(space, set(), {1})



def test_diameter_of_subset_is_zero_for_singleton():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    assert diameter_of_subset(space, {2}) == 0.0



def test_diameter_of_subset_returns_maximum_pair_distance():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    assert diameter_of_subset(space, {0, 1, 3}) == 3.0



def test_diameter_of_subset_rejects_empty_subset():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    with pytest.raises(ValueError):
        diameter_of_subset(space, [])



def test_is_bounded_subset_accepts_empty_and_finite_subsets():
    space = FiniteMetricSpace(carrier=(0, 1, 2, 3), distance=line_metric)
    assert is_bounded_subset(space, []) is True
    assert is_bounded_subset(space, {0, 3}) is True



def test_capped_metric_caps_large_distances():
    transformed = capped_metric(line_metric, cap=1.0)
    assert transformed(0, 5) == 1.0
    assert transformed(2, 2) == 0.0



def test_normalized_metric_stays_in_unit_interval_and_preserves_zero():
    transformed = normalized_metric(line_metric)
    assert transformed(2, 2) == 0.0
    assert 0.0 < transformed(0, 3) < 1.0
    assert isclose(transformed(0, 3), 3.0 / 4.0)



def test_transformed_metrics_still_validate_on_finite_carriers():
    carrier = (0, 1, 2)
    capped_space = FiniteMetricSpace(carrier=carrier, distance=capped_metric(line_metric, cap=1.0))
    normalized_space = FiniteMetricSpace(carrier=carrier, distance=normalized_metric(line_metric))
    assert validate_metric(capped_space).is_true
    assert validate_metric(normalized_space).is_true



def test_finite_product_metric_space_supports_max_mode():
    left = FiniteMetricSpace(carrier=(0, 1), distance=line_metric)
    right = FiniteMetricSpace(carrier=(0, 2), distance=line_metric)
    product_space = finite_product_metric_space(left, right, mode='max')
    assert len(product_space.carrier) == 4
    assert product_space.distance_between((0, 0), (1, 2)) == 2.0



def test_finite_product_metric_space_supports_sum_mode():
    left = FiniteMetricSpace(carrier=(0, 1), distance=line_metric)
    right = FiniteMetricSpace(carrier=(0, 2), distance=line_metric)
    product_space = finite_product_metric_space(left, right, mode='sum')
    assert product_space.distance_between((0, 0), (1, 2)) == 3.0



def test_finite_product_metric_space_supports_euclidean_mode():
    left = FiniteMetricSpace(carrier=(0, 1), distance=line_metric)
    right = FiniteMetricSpace(carrier=(0, 2), distance=line_metric)
    product_space = finite_product_metric_space(left, right, mode='euclidean')
    assert isclose(product_space.distance_between((0, 0), (1, 2)), sqrt(5.0))



def test_finite_product_metric_space_rejects_invalid_mode():
    left = FiniteMetricSpace(carrier=(0, 1), distance=line_metric)
    with pytest.raises(ValueError):
        finite_product_metric_space(left, mode='taxicab_maxish')



def test_finite_product_metric_space_validates_as_metric():
    left = FiniteMetricSpace(carrier=(0, 1), distance=line_metric)
    right = FiniteMetricSpace(carrier=(0, 2), distance=line_metric)
    product_space = finite_product_metric_space(left, right, mode='max')
    result = validate_metric(product_space)
    assert result.is_true
    assert result.is_exact
