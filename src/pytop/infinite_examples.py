"""Ready-made infinite examples for the core package."""

from __future__ import annotations

from .infinite_spaces import (
    BasisDefinedSpace,
    CocountableSpace,
    CofiniteSpace,
    DiscreteInfiniteSpace,
    IndiscreteInfiniteSpace,
    SorgenfreyLikeSpace,
)
from .metric_spaces import SymbolicMetricSpace


def naturals_discrete() -> DiscreteInfiniteSpace:
    return DiscreteInfiniteSpace(
        carrier='N',
        metadata={
            'description': 'The natural numbers with the discrete topology.',
            'countability': 'countable',
        },
    )


def integers_discrete() -> DiscreteInfiniteSpace:
    return DiscreteInfiniteSpace(
        carrier='Z',
        metadata={
            'description': 'The integers with the discrete topology.',
            'countability': 'countable',
        },
    )


def naturals_cofinite() -> CofiniteSpace:
    return CofiniteSpace(
        carrier='N',
        metadata={
            'description': 'The natural numbers with the cofinite topology.',
            'countability': 'countable',
        },
    )


def reals_indiscrete() -> IndiscreteInfiniteSpace:
    return IndiscreteInfiniteSpace(
        carrier='R',
        metadata={
            'description': 'The real line with the indiscrete topology.',
            'countability': 'uncountable',
        },
    )


def reals_cocountable() -> CocountableSpace:
    return CocountableSpace(
        carrier='R',
        metadata={
            'description': 'The real line with the cocountable topology.',
            'countability': 'uncountable',
        },
    )


def real_line_metric() -> SymbolicMetricSpace:
    return SymbolicMetricSpace(
        carrier='R',
        metadata={
            'description': 'The real line with the usual metric topology.',
            'countability': 'uncountable',
            'basis_size': 'aleph_0',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'tags': [
                'metric',
                'connected',
                'path_connected',
                'second_countable',
                'separable',
                'lindelof',
                'complete',
                'not_compact',
            ],
        },
        tags={'connected', 'path_connected', 'second_countable', 'separable', 'lindelof', 'complete', 'not_compact'},
    )


def rationals_metric() -> SymbolicMetricSpace:
    return SymbolicMetricSpace(
        carrier='Q',
        metadata={
            'description': 'The rational line with the inherited Euclidean metric topology.',
            'countability': 'countable',
            'basis_size': 'aleph_0',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'tags': ['metric', 'second_countable', 'separable', 'not_complete', 'not_compact'],
        },
        tags={'second_countable', 'separable', 'not_complete', 'not_compact'},
    )


def closed_unit_interval_metric() -> SymbolicMetricSpace:
    return SymbolicMetricSpace(
        carrier='[0,1]',
        metadata={
            'description': 'The closed unit interval with the inherited Euclidean metric topology.',
            'countability': 'uncountable',
            'basis_size': 'aleph_0',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'tags': [
                'metric',
                'compact',
                'connected',
                'path_connected',
                'second_countable',
                'separable',
                'complete',
            ],
        },
        tags={'compact', 'connected', 'path_connected', 'second_countable', 'separable', 'complete'},
    )


def real_plane_metric() -> SymbolicMetricSpace:
    return SymbolicMetricSpace(
        carrier='R^2',
        metadata={
            'description': 'The Euclidean plane with the usual metric topology.',
            'countability': 'uncountable',
            'basis_size': 'aleph_0',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'model_neighborhoods': 'open_disks',
            'tags': [
                'metric',
                'connected',
                'path_connected',
                'second_countable',
                'separable',
                'lindelof',
                'complete',
                'not_compact',
            ],
        },
        tags={'connected', 'path_connected', 'second_countable', 'separable', 'lindelof', 'complete', 'not_compact'},
    )


def real_line_order_topology() -> SymbolicMetricSpace:
    return SymbolicMetricSpace(
        carrier='R',
        metadata={
            'description': 'The real line with its usual order topology.',
            'countability': 'uncountable',
            'basis_size': 'aleph_0',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'construction': 'order_topology',
            'order_type': 'usual_linear_order',
            'basis_model': '(a,b)',
            'local_base_model': '(x-1/n,x+1/n)',
            'model_neighborhoods': 'open_intervals',
            'tags': [
                'metric',
                'order_topology',
                'connected',
                'path_connected',
                'second_countable',
                'separable',
                'lindelof',
                'not_compact',
            ],
        },
        tags={
            'order_topology',
            'connected',
            'path_connected',
            'second_countable',
            'separable',
            'lindelof',
            'not_compact',
        },
    )


def lower_limit_line_like() -> SorgenfreyLikeSpace:
    space = SorgenfreyLikeSpace(
        carrier='R',
        metadata={
            'description': 'A symbolic lower-limit line (Sorgenfrey-line style) space.',
            'countability': 'uncountable',
            'basis_size': 'continuum',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'construction': 'order_topology',
            'order_type': 'lower_limit',
            'basis_model': '[a,b)',
            'local_base_model': '[x,x+1/n)',
            'tags': [
                'order_topology',
                'lower_limit_topology',
                'sorgenfrey',
                'first_countable',
                'separable',
                'lindelof',
                'not_second_countable',
                'not_metrizable',
            ],
        },
    )
    space.add_tags('lower_limit_topology', 'sorgenfrey', 'lindelof', 'not_metrizable')
    return space


def upper_limit_line_like() -> SorgenfreyLikeSpace:
    space = SorgenfreyLikeSpace(
        carrier='R',
        metadata={
            'description': 'A symbolic upper-limit line space, order-dual to the Sorgenfrey line.',
            'countability': 'uncountable',
            'basis_size': 'continuum',
            'local_base_size': 'aleph_0',
            'dense_subset_size': 'aleph_0',
            'construction': 'order_topology',
            'order_type': 'upper_limit',
            'basis_model': '(a,b]',
            'local_base_model': '(x-1/n,x]',
            'tags': [
                'order_topology',
                'upper_limit_topology',
                'first_countable',
                'separable',
                'lindelof',
                'not_second_countable',
                'not_metrizable',
            ],
        },
    )
    space.add_tags('upper_limit_topology', 'lindelof', 'not_metrizable')
    return space


def sorgenfrey_line_like() -> SorgenfreyLikeSpace:
    return lower_limit_line_like()


def basis_defined_second_countable() -> BasisDefinedSpace:
    return BasisDefinedSpace(
        carrier='X',
        metadata={
            'description': 'A symbolic basis-defined second-countable space.',
            'basis_size': 'aleph_0',
            'local_base_size': 'aleph_0',
            'tags': ['second_countable', 'separable', 'lindelof'],
        },
    )


def infinite_examples_catalog() -> dict[str, dict[str, object]]:
    return {
        'naturals_discrete': {
            'constructor': naturals_discrete,
            'description': 'Countable discrete example.',
        },
        'naturals_cofinite': {
            'constructor': naturals_cofinite,
            'description': 'Countable cofinite example.',
        },
        'reals_indiscrete': {
            'constructor': reals_indiscrete,
            'description': 'Indiscrete uncountable example.',
        },
        'reals_cocountable': {
            'constructor': reals_cocountable,
            'description': 'Uncountable cocountable example.',
        },
        'real_line_metric': {
            'constructor': real_line_metric,
            'description': 'The real line in its usual metric topology.',
        },
        'real_line_order_topology': {
            'constructor': real_line_order_topology,
            'description': 'The real line in its usual order topology.',
        },
        'rationals_metric': {
            'constructor': rationals_metric,
            'description': 'The rational line with Euclidean metric topology.',
        },
        'closed_unit_interval_metric': {
            'constructor': closed_unit_interval_metric,
            'description': 'The closed unit interval with Euclidean metric topology.',
        },
        'real_plane_metric': {
            'constructor': real_plane_metric,
            'description': 'The Euclidean plane with its usual metric topology.',
        },
        'lower_limit_line_like': {
            'constructor': lower_limit_line_like,
            'description': 'A symbolic lower-limit style order-topology example.',
        },
        'upper_limit_line_like': {
            'constructor': upper_limit_line_like,
            'description': 'A symbolic upper-limit style order-topology example.',
        },
        'sorgenfrey_line_like': {
            'constructor': sorgenfrey_line_like,
            'description': 'Backward-compatible alias for the symbolic lower-limit line.',
        },
        'basis_defined_second_countable': {
            'constructor': basis_defined_second_countable,
            'description': 'A symbolic basis-defined second-countable example.',
        },
    }


__all__ = [
    "naturals_discrete",
    "integers_discrete",
    "naturals_cofinite",
    "reals_indiscrete",
    "reals_cocountable",
    "real_line_metric",
    "rationals_metric",
    "closed_unit_interval_metric",
    "real_plane_metric",
    "real_line_order_topology",
    "lower_limit_line_like",
    "upper_limit_line_like",
    "sorgenfrey_line_like",
    "basis_defined_second_countable",
    "infinite_examples_catalog",
]
