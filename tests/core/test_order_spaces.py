from pytop.order_spaces import (
    FinitePosetSpace,
    analyze_order_space,
    lower_space_from_order,
    neighborhood_profile,
    poset_space,
    preorder_reduction_report,
    preorder_space,
    preorder_t0_reduction,
    specialization_poset,
    upper_space_from_order,
)
from pytop.examples import two_point_indiscrete_space
from pytop.separation import is_t0


CHAIN = {(1, 2), (2, 3), (1, 3)}


def test_poset_space_has_expected_tags_and_exact_order_report():
    space = poset_space((1, 2, 3), CHAIN)
    assert isinstance(space, FinitePosetSpace)
    assert "alexandroff" in space.tags
    assert "poset" in space.tags
    assert "t0" in space.tags
    result = analyze_order_space(space)
    assert result.is_true
    assert result.is_exact


def test_upper_space_neighborhoods_follow_principal_upsets():
    space = upper_space_from_order((1, 2, 3), CHAIN)
    neighborhoods = neighborhood_profile(space)
    assert neighborhoods[1] == {1, 2, 3}
    assert neighborhoods[2] == {2, 3}
    assert neighborhoods[3] == {3}


def test_lower_space_reverses_neighborhood_direction():
    space = lower_space_from_order((1, 2, 3), CHAIN)
    neighborhoods = neighborhood_profile(space)
    assert neighborhoods[1] == {1}
    assert neighborhoods[2] == {1, 2}
    assert neighborhoods[3] == {1, 2, 3}


def test_poset_spaces_are_t0_exactly():
    space = poset_space((1, 2, 3), CHAIN)
    result = is_t0(space)
    assert result.is_true
    assert result.is_exact


def test_preorder_space_without_antisymmetry_is_not_poset_tagged():
    space = preorder_space(("a", "b"), {("a", "b"), ("b", "a")})
    assert "poset" not in space.tags


def test_preorder_t0_reduction_collapses_kernel_classes_to_a_poset():
    carrier = ('a', 'b', 'c')
    relation = {('a', 'b'), ('b', 'a'), ('a', 'c'), ('b', 'c')}
    reduced = preorder_t0_reduction(carrier, relation)
    assert len(reduced.carrier) == 2
    assert any(set(block) == {'a', 'b'} for block in reduced.carrier)
    assert any(set(block) == {'c'} for block in reduced.carrier)
    assert 't0_reduction' in reduced.tags


def test_preorder_reduction_report_tracks_kernel_block_count():
    carrier = ('a', 'b', 'c')
    relation = {('a', 'b'), ('b', 'a'), ('a', 'c'), ('b', 'c')}
    report = preorder_reduction_report(carrier, relation)
    assert report['carrier_size'] == 3
    assert report['quotient_size'] == 2
    assert not report['is_trivial_reduction']


def test_specialization_poset_reduces_indiscrete_two_point_space_to_one_point():
    reduced = specialization_poset(two_point_indiscrete_space())
    assert len(reduced.carrier) == 1
    assert reduced.metadata['construction'] == 'preorder_t0_reduction'
