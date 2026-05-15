from pytop.alexandroff import (
    alexandroff_space_from_preorder,
    alexandroff_report,
    is_alexandroff_space,
    minimal_open_neighborhood,
    preorder_kernel_relation,
    preorder_t0_reduction_data,
    principal_upset,
    specialization_preorder,
    t0_reduction_profile,
)
from pytop.examples import sierpinski_space, two_point_discrete_space, two_point_indiscrete_space


def test_finite_spaces_are_detected_as_alexandroff_exactly():
    result = is_alexandroff_space(two_point_discrete_space())
    assert result.is_true
    assert result.is_exact


def test_specialization_preorder_of_sierpinski_space():
    space = sierpinski_space()
    relation = specialization_preorder(space)
    assert (0, 0) in relation
    assert (1, 1) in relation
    assert (0, 1) in relation
    assert (1, 0) not in relation


def test_minimal_open_neighborhoods_in_sierpinski_space():
    space = sierpinski_space()
    assert minimal_open_neighborhood(space, 0) == {0, 1}
    assert minimal_open_neighborhood(space, 1) == {1}


def test_preorder_builds_sierpinski_topology():
    space = alexandroff_space_from_preorder((0, 1), {(0, 1)})
    opens = {frozenset(U) for U in space.topology}
    assert opens == {frozenset(), frozenset({1}), frozenset({0, 1})}
    assert principal_upset((0, 1), {(0, 1)}, 0) == {0, 1}


def test_alexandroff_report_contains_preorder_and_neighborhoods():
    report = alexandroff_report(sierpinski_space())
    assert "specialization_preorder" in report
    assert "minimal_open_neighborhoods" in report


def test_preorder_kernel_relation_detects_mutual_reachability_classes():
    carrier = ('a', 'b', 'c')
    relation = {('a', 'b'), ('b', 'a'), ('a', 'c'), ('b', 'c')}
    kernel = preorder_kernel_relation(carrier, relation)
    assert ('a', 'b') in kernel
    assert ('b', 'a') in kernel
    assert ('a', 'c') not in kernel


def test_preorder_t0_reduction_data_and_topological_profile_match_indiscrete_case():
    carrier = (0, 1)
    relation = {(0, 1), (1, 0)}
    data = preorder_t0_reduction_data(carrier, relation)
    assert len(data['quotient_blocks']) == 1
    profile = t0_reduction_profile(two_point_indiscrete_space())
    assert profile['carrier_size'] == 2
    assert profile['quotient_size'] == 1
    assert not profile['is_trivial_reduction']
