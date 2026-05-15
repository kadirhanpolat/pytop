from pytop.examples import two_point_discrete_space
from pytop.maps import analyze_map_property
from pytop.quotients import make_quotient_map, quotient_space, quotient_space_from_map


def test_finite_partition_quotient_is_singleton_space():
    X = two_point_discrete_space()
    Q = quotient_space(X, [{'a', 'b'}])
    assert Q.is_finite()
    assert len(Q.carrier) == 1
    assert len(Q.topology) == 2


def test_exact_quotient_map_detection_for_surjective_finite_map():
    X = two_point_discrete_space()
    Y = quotient_space(X, [{'a', 'b'}])
    q = make_quotient_map(X, Y, mapping={'a': 0, 'b': 0})
    assert analyze_map_property(q, 'surjective').is_true
    assert analyze_map_property(q, 'quotient').is_true
    Q2 = quotient_space_from_map(q)
    assert tuple(Q2.carrier) == tuple(Y.carrier)
