from pytop import (
    analyze_sequences,
    finite_chain_space,
    sequence_cluster_point,
    sequence_converges_to,
    sequential_closure,
)


def test_sequence_converges_to_point_by_open_neighborhood_tails():
    space = finite_chain_space(3)
    result = sequence_converges_to(space, [3, 1, 1, 1], 1)

    assert result.is_true and result.is_exact
    assert result.metadata["point"] == 1
    assert result.metadata["failed_open_neighborhoods"] == ()
    assert (frozenset({1}), 1) in result.metadata["witness_by_open_neighborhood"]


def test_sequence_convergence_fails_when_small_neighborhood_is_not_eventual():
    space = finite_chain_space(3)
    result = sequence_converges_to(space, [1, 1, 1, 3], 1)

    assert result.is_false and result.is_exact
    assert frozenset({1}) in result.metadata["failed_open_neighborhoods"]


def test_sequence_cluster_point_uses_observed_neighborhood_visits():
    space = finite_chain_space(3)
    positive = sequence_cluster_point(space, [3, 2, 1], 1)
    negative = sequence_cluster_point(space, [2, 3], 1)

    assert positive.is_true and positive.is_exact
    assert negative.is_false and negative.is_exact
    assert frozenset({1}) in negative.metadata["failed_open_neighborhoods"]


def test_sequential_closure_uses_minimal_open_neighborhood_intersection():
    space = finite_chain_space(3)
    result = sequential_closure(space, {2})

    assert result.is_true and result.is_exact
    assert result.value == frozenset({2, 3})


def test_analyze_sequences_delegates_to_finite_helpers():
    space = finite_chain_space(3)
    result = analyze_sequences(space, sequence=[3, 1, 1], point=1)

    assert result.is_true
    assert result.value["converges_to_point"] is True
    assert result.value["cluster_point"] is True
