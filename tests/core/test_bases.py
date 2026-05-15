from pytop import (
    BasisConstructionError,
    FiniteTopologicalSpace,
    finite_intersection_basis,
    generate_topology_from_basis,
    generate_topology_from_subbasis,
    is_basis_for_some_topology,
    is_basis_for_topology,
    is_local_base_at,
)


def _frozen_family(family):
    return {frozenset(member) for member in family}


def _accumulation_via_local_base(point, subset, local_base):
    subset = set(subset)
    return all(((set(neighborhood) - {point}) & subset) for neighborhood in local_base)


def _converges_via_local_base(sequence, local_base):
    sequence = list(sequence)
    return all(
        any(all(term in neighborhood for term in sequence[start:]) for start in range(len(sequence)))
        for neighborhood in local_base
    )


def test_is_basis_for_some_topology_accepts_a_valid_covering_family():
    carrier = {'a', 'b', 'c'}
    basis = [{'a'}, {'b'}, {'c'}]
    assert is_basis_for_some_topology(carrier, basis)



def test_is_basis_for_some_topology_rejects_a_family_that_does_not_cover():
    carrier = {'a', 'b', 'c'}
    basis = [{'a'}, {'b'}]
    assert not is_basis_for_some_topology(carrier, basis)



def test_is_basis_for_some_topology_rejects_bad_overlap_refinement():
    carrier = {'a', 'b', 'c'}
    basis = [{'a', 'b'}, {'b', 'c'}]
    assert not is_basis_for_some_topology(carrier, basis)



def test_is_basis_for_topology_accepts_space_object_input():
    space = generate_topology_from_basis({'a', 'b'}, [{'a'}, {'a', 'b'}])
    assert is_basis_for_topology(space, [{'a'}, {'a', 'b'}])



def test_is_basis_for_topology_rejects_family_with_non_open_member():
    carrier = {'a', 'b'}
    topology = [set(), {'a'}, {'a', 'b'}]
    assert not is_basis_for_topology(carrier, [{'a'}, {'b'}], topology=topology)



def test_finite_intersection_basis_contains_full_carrier_and_refined_overlap():
    carrier = {'a', 'b', 'c'}
    subbasis = [{'a', 'b'}, {'b', 'c'}]
    intersections = finite_intersection_basis(carrier, subbasis)
    assert _frozen_family(intersections) == {
        frozenset({'a', 'b', 'c'}),
        frozenset({'a', 'b'}),
        frozenset({'b', 'c'}),
        frozenset({'b'}),
    }



def test_finite_intersection_basis_accepts_mapping_input_and_deduplicates_members():
    carrier = {'a', 'b', 'c'}
    subbasis = {
        'left': {'a', 'b'},
        'right': {'b', 'c'},
        'duplicate-left': {'a', 'b'},
    }
    intersections = finite_intersection_basis(carrier, subbasis)
    assert len(intersections) == 4
    assert frozenset({'b'}) in _frozen_family(intersections)



def test_generate_topology_from_basis_enumerates_expected_open_sets():
    space = generate_topology_from_basis({'a', 'b'}, [{'a'}, {'a', 'b'}])
    assert isinstance(space, FiniteTopologicalSpace)
    assert _frozen_family(space.topology) == {
        frozenset(),
        frozenset({'a'}),
        frozenset({'a', 'b'}),
    }
    assert space.metadata['construction'] == 'basis_generated'
    assert space.has_tag('basis-generated')



def test_generate_topology_from_basis_raises_for_invalid_basis_candidate():
    carrier = {'a', 'b', 'c'}
    basis = [{'a', 'b'}, {'b', 'c'}]
    try:
        generate_topology_from_basis(carrier, basis)
    except BasisConstructionError:
        pass
    else:
        raise AssertionError('Expected BasisConstructionError for an invalid basis candidate.')



def test_generate_topology_from_subbasis_builds_expected_five_open_set_topology():
    space = generate_topology_from_subbasis({'a', 'b', 'c'}, [{'a', 'b'}, {'b', 'c'}])
    assert _frozen_family(space.topology) == {
        frozenset(),
        frozenset({'b'}),
        frozenset({'a', 'b'}),
        frozenset({'b', 'c'}),
        frozenset({'a', 'b', 'c'}),
    }
    assert space.metadata['construction'] == 'subbasis_generated'
    assert space.metadata['subbasis_size'] == 2
    assert space.has_tag('subbasis-generated')



def test_is_local_base_at_accepts_minimal_local_base_in_generated_space():
    space = generate_topology_from_subbasis({'a', 'b', 'c'}, [{'a', 'b'}, {'b', 'c'}])
    assert is_local_base_at(space, 'b', [{'b'}])



def test_is_local_base_at_rejects_family_that_cannot_refine_every_neighborhood():
    space = generate_topology_from_subbasis({'a', 'b', 'c'}, [{'a', 'b'}, {'b', 'c'}])
    assert not is_local_base_at(space, 'b', [{'a', 'b'}, {'b', 'c'}])



def test_local_base_can_witness_accumulation_point_reading_in_indiscrete_space():
    space = FiniteTopologicalSpace(
        carrier=('a', 'b'),
        topology=[set(), {'a', 'b'}],
        metadata={'description': 'Two-point indiscrete'},
    )
    local_base = [{'a', 'b'}]
    assert is_local_base_at(space, 'a', local_base)
    assert _accumulation_via_local_base('a', {'b'}, local_base)
    assert not _accumulation_via_local_base('a', set(), local_base)



def test_local_base_can_witness_eventual_convergence_reading():
    space = generate_topology_from_basis({0, 1, 2}, [{0, 1}, {0, 1, 2}])
    local_base = [{0, 1}]
    assert is_local_base_at(space, 0, local_base)
    assert _converges_via_local_base([2, 1, 1, 0, 1], local_base)
    assert not _converges_via_local_base([2, 1, 2, 2], local_base)



def test_empty_carrier_construction_stays_honest():
    space = generate_topology_from_basis(set(), [])
    assert _frozen_family(space.topology) == {frozenset()}
    assert is_basis_for_topology(space, [])
