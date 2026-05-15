from pytop import (
    analyze_net,
    finite_chain_space,
    is_directed_set,
    is_eventually_in,
    is_frequently_in,
    net_cluster_points,
    net_converges_to,
    two_point_discrete_space,
)


def _finite_prefix_relation(indices):
    return {(a, b) for a in indices for b in indices if a <= b}


def test_finite_relation_is_checked_as_directed_preorder():
    indices = ('a', 'b', 'c')
    relation = {
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('a', 'c'),
        ('b', 'c'),
    }

    result = is_directed_set(indices, relation)

    assert result.is_true and result.is_exact
    assert result.metadata['failed_directed_pairs'] == ()
    assert result.metadata['upper_bound_witness_count'] == 9


def test_relation_without_common_upper_bound_is_not_directed():
    indices = ('a', 'b')
    relation = {('a', 'a'), ('b', 'b')}

    result = is_directed_set(indices, relation)

    assert result.is_false and result.is_exact
    assert ('a', 'b') in result.metadata['failed_directed_pairs']


def test_eventually_in_detects_finite_tail_witness():
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 'outside', 1: 'outside', 2: 'inside', 3: 'inside'}

    result = is_eventually_in(indices, relation, values, {'inside'})

    assert result.is_true and result.is_exact
    assert result.metadata['witness_index'] == 2
    assert result.metadata['tail_indices'] == (2, 3)


def test_eventually_in_fails_when_every_tail_has_bad_value():
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 'inside', 1: 'inside', 2: 'inside', 3: 'outside'}

    result = is_eventually_in(indices, relation, values, {'inside'})

    assert result.is_false and result.is_exact
    assert result.metadata['witness_index'] is None
    assert result.metadata['candidate_tail_violations'][-1] == (3, (3,))


def test_net_converges_to_point_by_open_neighborhood_tails():
    space = finite_chain_space(3)
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 3, 1: 1, 2: 1, 3: 1}

    result = net_converges_to(space, indices, relation, values, 1)

    assert result.is_true and result.is_exact
    assert result.metadata['point'] == 1
    assert result.metadata['failed_open_neighborhoods'] == ()
    assert (frozenset({1}), 1) in result.metadata['witness_by_open_neighborhood']


def test_net_convergence_fails_when_small_neighborhood_is_not_eventual():
    space = finite_chain_space(3)
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 1, 1: 1, 2: 1, 3: 3}

    result = net_converges_to(space, indices, relation, values, 1)

    assert result.is_false and result.is_exact
    assert frozenset({1}) in result.metadata['failed_open_neighborhoods']



def test_frequently_in_detects_tail_meeting_witnesses():
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 'outside', 1: 'inside', 2: 'outside', 3: 'inside'}

    result = is_frequently_in(indices, relation, values, {'inside'})

    assert result.is_true and result.is_exact
    assert result.metadata['failed_start_indices'] == ()
    assert result.metadata['witness_by_start_index'][-1] == (3, 3)


def test_frequently_in_fails_when_a_tail_misses_subset():
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 'inside', 1: 'inside', 2: 'inside', 3: 'outside'}

    result = is_frequently_in(indices, relation, values, {'inside'})

    assert result.is_false and result.is_exact
    assert result.metadata['failed_start_indices'] == (3,)


def test_net_cluster_points_use_frequent_open_neighborhood_hits():
    space = two_point_discrete_space()
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 'b', 1: 'a', 2: 'b', 3: 'a'}

    result = net_cluster_points(space, indices, relation, values)

    assert result.is_true and result.is_exact
    assert result.value == frozenset({'a'})
    assert result.metadata['v0_1_52_corridor_record'] is True


def test_analyze_net_combines_subset_and_point_diagnostics():
    space = two_point_discrete_space()
    indices = (0, 1, 2, 3)
    relation = _finite_prefix_relation(indices)
    values = {0: 'b', 1: 'a', 2: 'a', 3: 'a'}

    result = analyze_net(space, indices, relation, values, point='a', subset={'a'})

    assert result.is_true
    assert result.value['eventually_in_subset'] is True
    assert result.value['frequently_in_subset'] is True
    assert result.value['converges_to_point'] is True
    assert result.value['point_is_cluster_point'] is True
    assert result.metadata['v0_1_52_corridor_record'] is True
