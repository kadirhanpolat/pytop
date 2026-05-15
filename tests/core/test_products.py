from pytop.examples import two_point_discrete_space
from pytop.products import binary_product
from pytop.connectedness import is_connected
from pytop.compactness import is_compact


def test_finite_product_of_two_discrete_spaces_has_four_points():
    X = two_point_discrete_space()
    Y = two_point_discrete_space()
    P = binary_product(X, Y)
    assert P.is_finite()
    assert len(P.carrier) == 4
    assert is_compact(P).is_true
    assert is_connected(P).is_false
