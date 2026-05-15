from pytop.connectedness import is_connected, is_locally_connected, is_path_connected
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import MetricLikeSpace


def test_finite_indiscrete_two_point_space_is_connected():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1, 2}])
    result = is_connected(space)
    assert result.is_true
    assert result.is_exact


def test_finite_discrete_two_point_space_is_not_connected():
    space = FiniteTopologicalSpace(carrier={1, 2}, topology=[set(), {1}, {2}, {1, 2}])
    result = is_connected(space)
    assert result.is_false
    assert result.is_exact


def test_path_connected_tag_implies_connected_by_theorem():
    space = MetricLikeSpace(carrier="interval", tags={"path_connected"})
    result = is_connected(space)
    assert result.is_true
    assert result.is_theorem_based
    assert "path-connected" in " ".join(result.justification).lower()


def test_negative_tag_for_path_connected_is_respected():
    space = MetricLikeSpace(carrier="circle-minus-point", tags={"not_path_connected"})
    result = is_path_connected(space)
    assert result.is_false


def test_positive_tag_for_locally_connected_is_used():
    space = MetricLikeSpace(carrier="manifold-chart", tags={"locally_connected"})
    result = is_locally_connected(space)
    assert result.is_true
