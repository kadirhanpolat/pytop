import pytest

from pytop.relations import (
    RelationError,
    compose_relations,
    equivalence_class,
    equivalence_from_partition,
    identity_relation,
    inverse_relation,
    is_antisymmetric,
    is_equivalence_relation,
    is_irreflexive,
    is_linear_order,
    is_partial_order,
    is_preorder,
    is_reflexive,
    is_symmetric,
    is_total_order,
    is_transitive,
    partition_from_equivalence,
    quotient_set,
    canonical_projection_from_equivalence,
    relation_domain,
    relation_profile,
    relation_range,
    validate_relation_between,
    validate_relation_on,
)


EQUALITY_MOD_2 = {
    (0, 0), (0, 2),
    (1, 1), (1, 3),
    (2, 0), (2, 2),
    (3, 1), (3, 3),
}


NON_TRANSITIVE = {
    (0, 0), (1, 1), (2, 2),
    (0, 1), (1, 2),
}


def test_relation_domain_range_inverse_and_composition():
    r = {(1, 'a'), (2, 'b')}
    s = {('a', 10), ('b', 20)}
    assert relation_domain(r) == {1, 2}
    assert relation_range(r) == {'a', 'b'}
    assert inverse_relation(r) == {('a', 1), ('b', 2)}
    assert compose_relations(r, s) == {(1, 10), (2, 20)}


def test_identity_relation_and_irreflexive_detection():
    carrier = {1, 2, 3}
    diagonal = identity_relation(carrier)
    assert diagonal == {(1, 1), (2, 2), (3, 3)}
    assert is_reflexive(carrier, diagonal)
    assert not is_irreflexive(carrier, diagonal)
    strict_part = {(1, 2), (1, 3), (2, 3)}
    assert is_irreflexive(carrier, strict_part)


def test_inverse_relation_is_an_involution_and_swaps_domain_and_range():
    relation = {(1, 'x'), (2, 'x'), (3, 'y')}
    inverse = inverse_relation(relation)
    assert inverse_relation(inverse) == relation
    assert relation_domain(inverse) == relation_range(relation)
    assert relation_range(inverse) == relation_domain(relation)


def test_relation_composition_is_associative_on_compatible_data():
    r = {(1, 'a'), (2, 'b')}
    s = {('a', True), ('b', False)}
    t = {(True, 'yes'), (False, 'no')}
    assert compose_relations(compose_relations(r, s), t) == compose_relations(r, compose_relations(s, t))


def test_relation_validation_rejects_duplicate_carriers_and_outside_pairs():
    with pytest.raises(RelationError):
        validate_relation_on([1, 1, 2], {(1, 1), (2, 2)})
    with pytest.raises(RelationError):
        validate_relation_on({1, 2}, {(1, 1), (2, 3)})


def test_validate_relation_between_supports_heterogeneous_carriers():
    domain, codomain, relation = validate_relation_between({1, 2}, {'x', 'y'}, {(1, 'x'), (2, 'y')})
    assert set(domain) == {1, 2}
    assert set(codomain) == {'x', 'y'}
    assert relation == {(1, 'x'), (2, 'y')}
    with pytest.raises(RelationError):
        validate_relation_between({1, 2}, {'x', 'y'}, {(1, 'x'), (2, 'z')})


def test_equivalence_relation_properties_hold_for_mod_2_example():
    carrier = {0, 1, 2, 3}
    assert is_reflexive(carrier, EQUALITY_MOD_2)
    assert is_symmetric(carrier, EQUALITY_MOD_2)
    assert is_transitive(carrier, EQUALITY_MOD_2)
    assert is_equivalence_relation(carrier, EQUALITY_MOD_2)


def test_non_transitive_relation_fails_equivalence_check():
    carrier = {0, 1, 2}
    assert not is_transitive(carrier, NON_TRANSITIVE)
    assert not is_equivalence_relation(carrier, NON_TRANSITIVE)


def test_equivalence_classes_and_partition_round_trip():
    carrier = {0, 1, 2, 3}
    assert equivalence_class(carrier, EQUALITY_MOD_2, 0) == {0, 2}
    partition = partition_from_equivalence(carrier, EQUALITY_MOD_2)
    assert partition == {frozenset({0, 2}), frozenset({1, 3})}
    rebuilt = equivalence_from_partition(carrier, partition)
    assert rebuilt == EQUALITY_MOD_2


def test_equivalence_from_named_partition_rebuilds_expected_relation():
    carrier = {'a', 'b', 'c'}
    partition = {'first': {'a', 'c'}, 'second': {'b'}}
    relation = equivalence_from_partition(carrier, partition)
    assert relation == {
        ('a', 'a'), ('a', 'c'), ('c', 'a'), ('c', 'c'),
        ('b', 'b'),
    }


def test_antisymmetry_detects_non_partial_order_pattern():
    carrier = {1, 2}
    relation = {(1, 1), (2, 2), (1, 2), (2, 1)}
    assert not is_antisymmetric(carrier, relation)
    assert is_preorder(carrier, relation)
    assert not is_partial_order(carrier, relation)


def test_partial_and_linear_order_detection():
    chain_carrier = {1, 2, 3}
    chain_relation = {(1, 1), (2, 2), (3, 3), (1, 2), (1, 3), (2, 3)}
    assert is_partial_order(chain_carrier, chain_relation)
    assert is_linear_order(chain_carrier, chain_relation)
    assert is_total_order(chain_carrier, chain_relation)

    divisibility_carrier = {1, 2, 3, 6}
    divisibility_relation = {
        (1, 1), (2, 2), (3, 3), (6, 6),
        (1, 2), (1, 3), (1, 6), (2, 6), (3, 6),
    }
    assert is_partial_order(divisibility_carrier, divisibility_relation)
    assert not is_linear_order(divisibility_carrier, divisibility_relation)


def test_relation_profile_summarizes_basic_structure():
    carrier = {1, 2, 3, 6}
    divisibility_relation = {
        (1, 1), (2, 2), (3, 3), (6, 6),
        (1, 2), (1, 3), (1, 6), (2, 6), (3, 6),
    }
    profile = relation_profile(carrier, divisibility_relation)
    assert profile['carrier_size'] == 4
    assert profile['relation_size'] == 9
    assert profile['domain'] == {1, 2, 3, 6}
    assert profile['range'] == {1, 2, 3, 6}
    assert profile['is_reflexive']
    assert not profile['is_irreflexive']
    assert profile['is_transitive']
    assert profile['is_antisymmetric']
    assert profile['is_preorder']
    assert profile['is_partial_order']
    assert not profile['is_linear_order']
    assert (2, 3) in profile['incomparable_pairs']
    assert (3, 2) in profile['incomparable_pairs']


def test_invalid_partition_and_invalid_point_raise_errors():
    with pytest.raises(RelationError):
        equivalence_from_partition({1, 2, 3}, [{1, 2}, {2, 3}])
    with pytest.raises(RelationError):
        equivalence_class({0, 1}, {(0, 0), (1, 1)}, 3)


def test_non_equivalence_relation_is_rejected_for_class_and_partition_generation():
    carrier = {0, 1, 2}
    with pytest.raises(RelationError):
        equivalence_class(carrier, NON_TRANSITIVE, 0)
    with pytest.raises(RelationError):
        partition_from_equivalence(carrier, NON_TRANSITIVE)


def test_quotient_set_and_canonical_projection_are_stable_for_equivalence_relations():
    carrier = {0, 1, 2, 3}
    blocks = quotient_set(carrier, EQUALITY_MOD_2)
    assert set(blocks) == {frozenset({0, 2}), frozenset({1, 3})}
    projection = canonical_projection_from_equivalence(carrier, EQUALITY_MOD_2)
    assert projection[0] == frozenset({0, 2})
    assert projection[2] == frozenset({0, 2})
    assert projection[1] == frozenset({1, 3})
    assert projection[3] == frozenset({1, 3})
