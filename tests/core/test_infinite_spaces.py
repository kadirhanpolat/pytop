from pytop.infinite_spaces import (
    CocountableSpace,
    CofiniteSpace,
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
)


def test_discrete_infinite_space_adds_expected_tags():
    space = DiscreteInfiniteSpace(carrier='N', metadata={'countability': 'countable'})
    assert space.has_tag('discrete')
    assert space.has_tag('hausdorff')
    assert space.has_tag('second_countable')
    assert space.metadata['representation'] == 'infinite_discrete'


def test_indiscrete_infinite_space_adds_expected_tags():
    space = IndiscreteInfiniteSpace(carrier='R', metadata={'countability': 'uncountable'})
    assert space.has_tag('compact')
    assert space.has_tag('connected')
    assert space.has_tag('not_hausdorff')
    assert space.metadata['representation'] == 'infinite_indiscrete'


def test_cofinite_space_tracks_countability_sensitive_tags():
    countable = CofiniteSpace(carrier='N', metadata={'countability': 'countable'})
    uncountable = CofiniteSpace(carrier='R', metadata={'countability': 'uncountable'})
    assert countable.has_tag('first_countable')
    assert countable.has_tag('second_countable')
    assert uncountable.has_tag('not_first_countable')
    assert uncountable.has_tag('not_second_countable')


def test_cocountable_space_marks_standard_uncountable_behaviour():
    space = CocountableSpace(carrier='R', metadata={'countability': 'uncountable'})
    assert space.has_tag('cocountable')
    assert space.has_tag('not_compact')
    assert space.has_tag('not_separable')
