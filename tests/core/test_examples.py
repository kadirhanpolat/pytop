from pytop.examples import (
    closed_unit_interval_metric,
    examples_catalog,
    finite_chain_space,
    lower_limit_line_like,
    naturals_cofinite,
    real_line_metric,
    real_line_order_topology,
    real_plane_metric,
    sierpinski_space,
    two_point_discrete_space,
    upper_limit_line_like,
)
from pytop.invariants import character, weight


def test_examples_catalog_contains_finite_and_infinite_sections():
    catalog = examples_catalog()
    assert 'finite' in catalog and 'infinite' in catalog
    assert 'sierpinski_space' in catalog['finite']
    assert 'real_line_metric' in catalog['infinite']


def test_sierpinski_and_two_point_discrete_examples_are_constructed():
    sierpinski = sierpinski_space()
    discrete = two_point_discrete_space()
    assert sierpinski.metadata['representation'] == 'finite'
    assert discrete.metadata['representation'] == 'finite'
    assert weight(discrete).value == 2


def test_finite_chain_space_has_expected_carrier_size():
    chain = finite_chain_space(4)
    assert len(chain.carrier) == 4
    assert chain.has_tag('finite')


def test_real_line_metric_example_carries_metric_and_second_countable_tags():
    line = real_line_metric()
    assert line.has_tag('metric')
    assert line.has_tag('second_countable')
    assert line.metadata['representation'] == 'infinite_metric'


def test_naturals_cofinite_example_is_symbolic_but_semantically_enriched():
    space = naturals_cofinite()
    assert space.has_tag('cofinite')
    assert space.has_tag('compact')


def test_new_metric_benchmarks_are_exposed_in_examples_catalog_and_tags():
    catalog = examples_catalog()['infinite']
    assert 'closed_unit_interval_metric' in catalog
    assert 'real_plane_metric' in catalog

    interval = closed_unit_interval_metric()
    plane = real_plane_metric()
    assert interval.has_tag('compact')
    assert plane.has_tag('not_compact')
    assert plane.metadata['model_neighborhoods'] == 'open_disks'


def test_order_and_limit_examples_are_exposed_with_expected_tags_and_models():
    catalog = examples_catalog()['infinite']
    assert 'real_line_order_topology' in catalog
    assert 'lower_limit_line_like' in catalog
    assert 'upper_limit_line_like' in catalog

    order_line = real_line_order_topology()
    lower = lower_limit_line_like()
    upper = upper_limit_line_like()

    assert order_line.has_tag('order_topology')
    assert order_line.has_tag('metric')
    assert order_line.metadata['model_neighborhoods'] == 'open_intervals'
    assert character(order_line).value == 'aleph_0'

    assert lower.has_tag('lower_limit_topology')
    assert lower.has_tag('not_second_countable')
    assert lower.has_tag('lindelof')
    assert lower.metadata['basis_model'] == '[a,b)'

    assert upper.has_tag('upper_limit_topology')
    assert upper.has_tag('not_second_countable')
    assert upper.metadata['basis_model'] == '(a,b]'
