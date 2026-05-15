from pytop.enumeration import (
    count_topologies_on_n_points,
    enumerate_hausdorff_topologies,
    enumerate_t0_topologies,
    enumerate_topologies_on_n_points,
)


def test_number_of_topologies_on_one_point_is_one():
    spaces = enumerate_topologies_on_n_points(1)
    assert len(spaces) == 1
    assert count_topologies_on_n_points(1) == 1


def test_number_of_topologies_on_two_points_is_four():
    assert count_topologies_on_n_points(2) == 4


def test_t0_topologies_on_two_points_are_three():
    spaces = enumerate_t0_topologies((0, 1))
    assert len(spaces) == 3


def test_hausdorff_topologies_on_two_points_are_discrete_only():
    spaces = enumerate_hausdorff_topologies((0, 1))
    assert len(spaces) == 1
