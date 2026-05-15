from pytop import (
    FiniteTopologicalSpace,
    boundary_of_subset,
    closure_of_subset,
    derived_set_of_subset,
    exterior_of_subset,
    finite_chain_space,
    interior_of_subset,
    is_neighborhood_of_point,
    is_nowhere_dense_subset,
    neighborhood_system_of_point,
)
from pytop.subspaces import finite_subspace


def test_finite_chain_operator_values_are_exact():
    space = finite_chain_space(3)
    subset = {2}

    assert closure_of_subset(space, subset).value == frozenset({2, 3})
    assert interior_of_subset(space, subset).value == frozenset()
    assert boundary_of_subset(space, subset).value == frozenset({2, 3})
    assert exterior_of_subset(space, subset).value == frozenset({1})
    assert derived_set_of_subset(space, subset).value == frozenset({3})


def test_nowhere_dense_detected_exactly_in_finite_chain_space():
    space = finite_chain_space(3)
    assert is_nowhere_dense_subset(space, {2}).is_true
    assert is_nowhere_dense_subset(space, {1}).is_false


def test_neighborhood_system_lists_all_neighborhoods_and_the_open_core():
    space = finite_chain_space(3)
    result = neighborhood_system_of_point(space, 1)
    assert result.is_true and result.is_exact
    assert result.value == (
        frozenset({1}),
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({1, 2, 3}),
    )
    assert result.metadata['minimal_open_neighborhood'] == frozenset({1})
    assert result.metadata['open_neighborhoods'] == (
        frozenset({1}),
        frozenset({1, 2}),
        frozenset({1, 2, 3}),
    )
    assert result.metadata['contains_non_open_neighborhoods'] is True


def test_is_neighborhood_of_point_uses_open_witness_not_openness_of_candidate():
    space = finite_chain_space(3)

    positive = is_neighborhood_of_point(space, 1, {1, 3})
    negative = is_neighborhood_of_point(space, 2, {2, 3})

    assert positive.is_true and positive.is_exact
    assert positive.metadata['witness_open_neighborhoods'] == (frozenset({1}),)
    assert negative.is_false and negative.is_exact
    assert negative.metadata['witness_open_neighborhoods'] == ()


def test_subspace_closure_agrees_with_ambient_intersection_formula():
    ambient = finite_chain_space(4)
    subspace = finite_subspace(ambient, {2, 3, 4})
    subset = {2}

    ambient_closure = set(closure_of_subset(ambient, subset).value)
    subspace_closure = set(closure_of_subset(subspace, subset).value)

    assert subspace_closure == ambient_closure & set(subspace.carrier)


def test_kuratowski_axioms_hold_in_small_finite_space():
    space = FiniteTopologicalSpace(
        carrier=('a', 'b', 'c'),
        topology=[set(), {'a'}, {'a', 'b'}, {'a', 'b', 'c'}],
        metadata={'description': 'A small finite test space.'},
    )
    a = {'b'}
    b = {'c'}

    assert closure_of_subset(space, set()).value == frozenset()
    assert set(closure_of_subset(space, a).value).issuperset(a)
    assert closure_of_subset(space, a | b).value == frozenset(
        set(closure_of_subset(space, a).value) | set(closure_of_subset(space, b).value)
    )
    assert closure_of_subset(space, set(closure_of_subset(space, a).value)).value == closure_of_subset(space, a).value
