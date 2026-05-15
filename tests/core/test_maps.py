from pytop.examples import two_point_discrete_space, two_point_indiscrete_space
from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.maps import (
    FiniteMap,
    analyze_map_property,
    continuity_via_codomain_basis,
    continuity_via_codomain_subbasis,
    image_of_subset,
    initial_topology_from_maps,
    is_continuous_at_point,
    is_sequentially_continuous_at_point,
    preimage_of_subset,
    satisfies_closure_image_inclusion,
)


def _two_point_discrete():
    return FiniteTopologicalSpace(carrier=(0, 1), topology=[set(), {0}, {1}, {0, 1}])


def test_finite_identity_map_is_homeomorphism():
    X = _two_point_discrete()
    f = FiniteMap(domain=X, codomain=X, mapping={0: 0, 1: 1}, name='id')
    assert analyze_map_property(f, 'continuous').is_true
    assert analyze_map_property(f, 'open').is_true
    assert analyze_map_property(f, 'closed').is_true
    assert analyze_map_property(f, 'homeomorphism').is_true


def test_constant_map_is_continuous_but_not_injective_on_discrete_domain():
    X = _two_point_discrete()
    Y = _two_point_discrete()
    f = FiniteMap(domain=X, codomain=Y, mapping={0: 0, 1: 0}, name='c')
    assert analyze_map_property(f, 'continuous').is_true
    assert analyze_map_property(f, 'injective').is_false
    assert image_of_subset(f, {0, 1}) == {0}
    assert preimage_of_subset(f, {0}) == {0, 1}


def test_pointwise_continuity_and_sequential_continuity_agree_on_finite_spaces():
    X = two_point_discrete_space()
    f = FiniteMap(domain=X, codomain=X, mapping={'a': 'a', 'b': 'b'}, name='id')
    assert is_continuous_at_point(f, 'a').is_true
    assert is_sequentially_continuous_at_point(f, 'a').is_true


def test_basis_and_subbasis_criteria_detect_identity_map_continuity():
    X = two_point_discrete_space()
    f = FiniteMap(domain=X, codomain=X, mapping={'a': 'a', 'b': 'b'}, name='id')
    basis = [{'a'}, {'b'}]
    subbasis = [{'a'}, {'b'}]
    assert continuity_via_codomain_basis(f, basis).is_true
    assert continuity_via_codomain_subbasis(f, subbasis).is_true


def test_closure_image_inclusion_holds_for_continuous_finite_map():
    X = two_point_discrete_space()
    Y = two_point_indiscrete_space()
    f = FiniteMap(domain=X, codomain=Y, mapping={'a': 'a', 'b': 'b'}, name='id_d_to_i')
    assert analyze_map_property(f, 'continuous').is_true
    assert satisfies_closure_image_inclusion(f, {'a'}).is_true


def test_initial_topology_from_identity_map_recovers_discrete_topology():
    carrier = {'a', 'b'}
    domain = two_point_indiscrete_space()
    codomain = two_point_discrete_space()
    id_map = FiniteMap(domain=domain, codomain=codomain, mapping={'a': 'a', 'b': 'b'}, name='id_i_to_d')
    initial = initial_topology_from_maps(carrier, [id_map])
    topology = {frozenset(member) for member in initial.topology}
    assert topology == {frozenset(), frozenset({'a'}), frozenset({'b'}), frozenset({'a', 'b'})}
