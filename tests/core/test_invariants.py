from pytop.finite_spaces import FiniteTopologicalSpace
from pytop.infinite_spaces import BasisDefinedSpace, MetricLikeSpace
from pytop.invariants import analyze_invariant, weight, density, character, lindelof_number, cellularity


def test_finite_invariants_on_sierpinski_space_are_exact():
    space = FiniteTopologicalSpace(
        carrier=(0, 1),
        topology=[set(), {1}, {0, 1}],
        metadata={'description': 'Sierpinski space'},
    )

    assert weight(space).value == 2
    assert density(space).value == 1
    assert character(space).value == 1
    assert lindelof_number(space).value == 1
    assert cellularity(space).value == 1

    assert weight(space).is_exact
    assert density(space).is_exact


def test_finite_invariants_on_two_point_discrete_space_are_exact():
    space = FiniteTopologicalSpace(
        carrier=('a', 'b'),
        topology=[set(), {'a'}, {'b'}, {'a', 'b'}],
        metadata={'description': 'Two-point discrete'},
    )

    assert weight(space).value == 2
    assert density(space).value == 2
    assert character(space).value == 1
    assert lindelof_number(space).value == 2
    assert cellularity(space).value == 2


def test_metric_space_character_is_theorem_countable():
    space = MetricLikeSpace(carrier='R', metadata={'description': 'Real line'})
    result = character(space)
    assert result.is_true
    assert result.is_theorem_based
    assert result.value == 'aleph_0'


def test_second_countable_space_gets_countable_weight_and_density():
    space = BasisDefinedSpace(
        carrier='X',
        metadata={'description': 'basis-defined example', 'tags': ['second_countable']},
    )
    assert weight(space).value == 'aleph_0'
    assert density(space).value == 'aleph_0'
    assert lindelof_number(space).value == 'aleph_0'


def test_metadata_backed_invariant_value_is_returned():
    space = BasisDefinedSpace(
        carrier='X',
        metadata={'description': 'explicit basis size', 'basis_size': 7, 'local_base_size': 3},
    )
    assert weight(space).value == 7
    assert character(space).value == 3


def test_unknown_invariant_support_stays_honest():
    space = MetricLikeSpace(carrier='M', metadata={'description': 'metric without extra tags'})
    result = cellularity(space)
    assert result.is_unknown


def test_order_and_limit_examples_surface_metadata_backed_invariants():
    from pytop.examples import lower_limit_line_like, real_line_order_topology, upper_limit_line_like

    order_line = real_line_order_topology()
    lower = lower_limit_line_like()
    upper = upper_limit_line_like()

    assert weight(order_line).value == 'aleph_0'
    assert character(lower).value == 'aleph_0'
    assert density(lower).value == 'aleph_0'
    assert character(upper).value == 'aleph_0'
