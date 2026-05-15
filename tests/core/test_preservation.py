from pytop.examples import naturals_cofinite, two_point_discrete_space, two_point_indiscrete_space
from pytop.maps import FiniteMap
from pytop.preservation import (
    closure_image_behavior,
    compact_closed_subspace,
    compact_under_continuous_image,
    connected_under_continuous_image,
    homeomorphic_invariant_transfer,
    separation_inherited_by_subspace,
)
from pytop.subspaces import subspace


def test_compactness_is_preserved_under_continuous_image():
    domain = two_point_discrete_space()
    codomain = two_point_discrete_space()
    f = FiniteMap(domain=domain, codomain=codomain, mapping={'a': 'a', 'b': 'a'}, name='collapse')
    result = compact_under_continuous_image(f)
    assert result.is_true and result.is_theorem_based


def test_connectedness_is_preserved_under_continuous_image():
    domain = two_point_indiscrete_space()
    codomain = two_point_discrete_space()
    f = FiniteMap(domain=domain, codomain=codomain, mapping={'a': 'a', 'b': 'a'}, name='constant')
    result = connected_under_continuous_image(f)
    assert result.is_true and result.is_theorem_based


def test_closed_subspace_of_compact_symbolic_space_is_compact():
    ambient = naturals_cofinite()
    A = subspace(ambient, 'A', closed=True)
    result = compact_closed_subspace(A)
    assert result.is_true


def test_subspace_inherits_t1_when_tagged_from_ambient():
    ambient = naturals_cofinite()
    A = subspace(ambient, 'A', closed=True)
    result = separation_inherited_by_subspace(A, 't1')
    assert result.is_true



def test_homeomorphic_invariant_transfer_accepts_connectedness():
    X = two_point_discrete_space()
    h = FiniteMap(domain=X, codomain=X, mapping={'a': 'a', 'b': 'b'}, name='id')
    result = homeomorphic_invariant_transfer(h, 'connected')
    assert result.is_true
    assert result.is_theorem_based


def test_closure_image_behavior_wraps_map_level_inclusion_check():
    domain = two_point_discrete_space()
    codomain = two_point_indiscrete_space()
    f = FiniteMap(domain=domain, codomain=codomain, mapping={'a': 'a', 'b': 'b'}, name='id_d_to_i')
    result = closure_image_behavior(f, {'a'})
    assert result.is_true
