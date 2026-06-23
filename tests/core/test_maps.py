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


from pytop.maps import (  # noqa: E402
    MapBuilderError,
    constant_function,
    identity_function,
    make_function,
)


def test_make_function_basic():
    f = make_function([1, 2, 3], [4, 5, 6], {1: 4, 2: 5, 3: 6})
    assert f.image_of_point(1) == 4
    assert f.image_of_point(3) == 6


def test_make_function_partial_mapping():
    f = make_function([1, 2, 3], [0, 1], {1: 0, 2: 1, 3: 0})
    assert f.image_of_point(2) == 1


def test_make_function_invalid_key_raises():
    import pytest as _pytest
    with _pytest.raises(MapBuilderError):
        make_function([1, 2], [10, 20], {1: 10, 99: 20})


def test_make_function_invalid_value_raises():
    import pytest as _pytest
    with _pytest.raises(MapBuilderError):
        make_function([1, 2], [10, 20], {1: 10, 2: 99})


def test_identity_function_maps_to_self():
    f = identity_function([1, 2, 3])
    for x in [1, 2, 3]:
        assert f.image_of_point(x) == x


def test_identity_function_bijective_tag():
    f = identity_function([1, 2])
    assert f.has_tag("bijective")


def test_constant_function_maps_all_to_value():
    f = constant_function([1, 2, 3], [0, 1], 0)
    for x in [1, 2, 3]:
        assert f.image_of_point(x) == 0


def test_constant_function_invalid_value_raises():
    import pytest as _pytest
    with _pytest.raises(MapBuilderError):
        constant_function([1, 2], [0, 1], 99)
