from pytop.examples import real_line_metric, reals_cocountable, reals_indiscrete
from pytop.infinite_compactness import is_compact_infinite
from pytop.infinite_connectedness import is_connected_infinite
from pytop.infinite_constructions import disjoint_sum, product, subspace
from pytop.infinite_image_preimage import SymbolicSubset, compact_image_result, connected_image_result, image_space, image_subset, preimage_subset
from pytop.infinite_maps import ContinuousMap, HomeomorphismMap, QuotientMap, SymbolicMap, compose_maps, homeomorphism_criterion_result, initial_topology_descriptor, is_continuous_map, is_homeomorphism_map, is_open_map, is_quotient_map
from pytop.infinite_quotients import quotient_space_from_map


def test_homeomorphism_map_has_exact_core_tags():
    X = real_line_metric()
    h = HomeomorphismMap(domain=X, codomain=X, name='h')
    assert is_homeomorphism_map(h).is_exact and is_homeomorphism_map(h).is_true
    assert is_continuous_map(h).is_exact and is_continuous_map(h).is_true
    assert is_open_map(h).is_exact and is_open_map(h).is_true


def test_bijective_continuous_open_map_yields_theorem_homeomorphism():
    X = real_line_metric()
    f = SymbolicMap(domain=X, codomain=X, name='f', tags={'continuous', 'open', 'bijective'})
    result = is_homeomorphism_map(f)
    assert result.is_true
    assert result.mode == 'theorem'


def test_product_of_metric_connected_spaces_preserves_metric_and_connected_tags():
    X = real_line_metric()
    Y = real_line_metric()
    prod = product(X, Y)
    assert prod.has_tag('metric')
    assert prod.has_tag('connected')
    assert prod.has_tag('path_connected')


def test_closed_subspace_of_compact_space_becomes_theorem_compact():
    X = reals_indiscrete()
    A = subspace(X, 'A', closed=True)
    result = is_compact_infinite(A)
    assert result.is_true
    assert result.mode == 'theorem'


def test_continuous_image_of_compact_space_is_theorem_compact():
    X = reals_indiscrete()
    Y = reals_cocountable()
    f = ContinuousMap(domain=X, codomain=Y, name='f')
    image = image_space(f)
    assert 'compact' in image.tags
    result = compact_image_result(f)
    assert result.is_true
    assert result.mode == 'theorem'


def test_continuous_image_of_connected_space_is_theorem_connected():
    X = real_line_metric()
    Y = reals_cocountable()
    f = ContinuousMap(domain=X, codomain=Y, name='g')
    result = connected_image_result(f)
    assert result.is_true
    assert result.mode == 'theorem'


def test_preimage_of_open_subset_under_continuous_map_is_open():
    X = real_line_metric()
    Y = reals_cocountable()
    f = ContinuousMap(domain=X, codomain=Y, name='f')
    U = SymbolicSubset(ambient=Y, label='U', tags={'open'})
    pre = preimage_subset(f, U)
    assert pre.has_tag('open')


def test_image_of_compact_subset_is_compact_subset():
    X = reals_indiscrete()
    Y = reals_cocountable()
    f = ContinuousMap(domain=X, codomain=Y, name='f')
    K = SymbolicSubset(ambient=X, label='K', tags={'compact'})
    image = image_subset(f, K)
    assert image.has_tag('compact')


def test_quotient_map_builds_quotient_space():
    X = real_line_metric()
    Y = reals_cocountable()
    q = QuotientMap(domain=X, codomain=Y, name='q')
    assert is_quotient_map(q).is_true
    quotient = quotient_space_from_map(q)
    assert quotient.has_tag('quotient_space')
    assert quotient.has_tag('realized_by_quotient_map')


def test_composition_of_homeomorphisms_stays_homeomorphic():
    X = real_line_metric()
    f = HomeomorphismMap(domain=X, codomain=X, name='f')
    g = HomeomorphismMap(domain=X, codomain=X, name='g')
    h = compose_maps(f, g, name='h')
    assert is_homeomorphism_map(h).is_true


def test_disjoint_sum_of_two_nonempty_spaces_is_not_connected_by_tag():
    X = real_line_metric()
    Y = real_line_metric()
    s = disjoint_sum(X, Y)
    assert s.has_tag('not_connected')



def test_explicit_homeomorphism_criterion_helper_reads_open_bijection_case():
    X = real_line_metric()
    f = SymbolicMap(domain=X, codomain=X, name='f', tags={'continuous', 'open', 'bijective'})
    result = homeomorphism_criterion_result(f)
    assert result.is_true
    assert result.mode == 'theorem'


def test_initial_topology_descriptor_records_defining_map_names():
    X = real_line_metric()
    f = ContinuousMap(domain=X, codomain=X, name='pi1')
    g = ContinuousMap(domain=X, codomain=X, name='pi2')
    descriptor = initial_topology_descriptor([f, g])
    assert descriptor['representation'] == 'initial_topology_descriptor'
    assert descriptor['defining_maps'] == ['pi1', 'pi2']
