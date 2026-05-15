"""Finite net and directed-set helpers for the topology book ecosystem.

The module is intentionally small: it gives Chapter 19 a testable finite
bridge without pretending to solve arbitrary symbolic convergence problems.
A preorder pair ``(a, b)`` is read as ``a <= b``.  Consequently the tail above
``d0`` is the finite set of all ``e`` with ``d0 <= e``.

v0.1.52 strengthens this layer for the Cilt III nets corridor: it keeps the
existing eventual-containment and convergence checks, and adds frequent
containment, finite net cluster diagnostics, and a small ``analyze_net``
facade for notebooks and manuscript examples.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from .result import Result


class NetError(ValueError):
    """Raised when a finite net request has a malformed input shape."""


def is_directed_set(index_set: Iterable[Any], preorder: Iterable[tuple[Any, Any]]) -> Result:
    """Check whether a finite relation is a directed preorder.

    Parameters
    ----------
    index_set:
        Finite collection of indices.
    preorder:
        Iterable of ordered pairs.  A pair ``(a, b)`` means ``a <= b``.

    Returns
    -------
    Result
        An exact structured result.  Failure metadata records which of the
        reflexive, transitive, or upper-bound tests failed.
    """

    indices = _normalize_indices(index_set)
    relation = _normalize_relation(preorder)

    if not indices:
        return Result.false(
            mode='exact',
            value=False,
            justification=['A directed set must be non-empty.'],
            metadata={'operator': 'is_directed_set', 'index_count': 0, 'relation_count': len(relation)},
        )

    index_set_normalized = set(indices)
    outside_pairs = sorted(
        (pair for pair in relation if pair[0] not in index_set_normalized or pair[1] not in index_set_normalized),
        key=_repr_tuple_key,
    )
    missing_reflexive = tuple(index for index in indices if (index, index) not in relation)

    failed_transitive: list[tuple[Any, Any, Any]] = []
    for a in indices:
        for b in indices:
            if (a, b) not in relation:
                continue
            for c in indices:
                if (b, c) in relation and (a, c) not in relation:
                    failed_transitive.append((a, b, c))

    failed_directed: list[tuple[Any, Any]] = []
    upper_bound_witnesses: dict[tuple[Any, Any], Any] = {}
    for a in indices:
        for b in indices:
            upper_bound = _first_upper_bound(indices, relation, a, b)
            if upper_bound is None:
                failed_directed.append((a, b))
            else:
                upper_bound_witnesses[(a, b)] = upper_bound

    metadata = {
        'operator': 'is_directed_set',
        'index_count': len(indices),
        'relation_count': len(relation),
        'outside_pairs': tuple(outside_pairs),
        'missing_reflexive_indices': tuple(missing_reflexive),
        'failed_transitive_triples': tuple(failed_transitive),
        'failed_directed_pairs': tuple(failed_directed),
        'upper_bound_witness_count': len(upper_bound_witnesses),
    }

    if outside_pairs:
        return Result.false(
            mode='exact',
            value=False,
            justification=['The relation mentions at least one index outside the declared index set.'],
            metadata=metadata,
        )
    if missing_reflexive:
        return Result.false(
            mode='exact',
            value=False,
            justification=['The relation is not reflexive on the declared index set.'],
            metadata=metadata,
        )
    if failed_transitive:
        return Result.false(
            mode='exact',
            value=False,
            justification=['The relation is not transitive on the declared index set.'],
            metadata=metadata,
        )
    if failed_directed:
        return Result.false(
            mode='exact',
            value=False,
            justification=['At least one pair of indices has no common upper bound.'],
            metadata=metadata,
        )

    return Result.true(
        mode='exact',
        value=True,
        justification=['The finite relation is a non-empty directed preorder.'],
        proof_outline=[
            'Reflexivity, transitivity, and the common-upper-bound condition were checked by finite enumeration.'
        ],
        metadata=metadata,
    )


def is_eventually_in(
    index_set: Iterable[Any],
    preorder: Iterable[tuple[Any, Any]],
    net_values: Mapping[Any, Any] | Callable[[Any], Any],
    subset: Iterable[Any],
) -> Result:
    """Decide whether a finite net is eventually inside ``subset``.

    This is the finite model of the textbook phrase: there is an index ``d0``
    such that every later value ``x_e`` with ``d0 <= e`` lies in ``subset``.
    """

    indices = _normalize_indices(index_set)
    relation = _normalize_relation(preorder)
    directed = is_directed_set(indices, relation)
    if not directed.is_true:
        return Result.false(
            mode='exact',
            value=False,
            justification=['Eventual containment requires a valid directed index set.'],
            metadata={
                'operator': 'is_eventually_in',
                'directed_status': directed.status,
                'directed_metadata': directed.metadata,
            },
        )

    values_result = _finite_net_values(indices, net_values)
    if values_result.is_false:
        metadata = {'operator': 'is_eventually_in'}
        metadata.update(values_result.metadata)
        return Result.false(
            mode='exact',
            value=False,
            justification=values_result.justification,
            metadata=metadata,
        )

    values = values_result.value
    subset_set = set(subset)
    witness, tail = _eventual_witness(indices, relation, values, subset_set)
    metadata = {
        'operator': 'is_eventually_in',
        'index_count': len(indices),
        'subset': tuple(sorted(subset_set, key=repr)),
        'witness_index': witness,
        'tail_indices': tuple(tail) if tail is not None else (),
        'candidate_tail_violations': _candidate_tail_violations(indices, relation, values, subset_set),
    }

    if witness is None:
        return Result.false(
            mode='exact',
            value=False,
            justification=['No finite tail is entirely contained in the requested subset.'],
            metadata=metadata,
        )

    return Result.true(
        mode='exact',
        value=True,
        justification=['A finite tail of the net is entirely contained in the requested subset.'],
        proof_outline=[
            'The witness index d0 was found by enumerating finite tails {e : d0 <= e}.'
        ],
        metadata=metadata,
    )



def is_frequently_in(
    index_set: Iterable[Any],
    preorder: Iterable[tuple[Any, Any]],
    net_values: Mapping[Any, Any] | Callable[[Any], Any],
    subset: Iterable[Any],
) -> Result:
    """Decide whether a finite net is frequently inside ``subset``.

    A net is frequently in ``A`` when every tail has some value in ``A``.
    In finite directed teaching models this is a diagnostic for the definition,
    not a replacement for infinite cofinality arguments.
    """

    indices = _normalize_indices(index_set)
    relation = _normalize_relation(preorder)
    directed = is_directed_set(indices, relation)
    if not directed.is_true:
        return Result.false(
            mode='exact',
            value=False,
            justification=['Frequent containment requires a valid directed index set.'],
            metadata={
                'operator': 'is_frequently_in',
                'directed_status': directed.status,
                'directed_metadata': directed.metadata,
            },
        )

    values_result = _finite_net_values(indices, net_values)
    if values_result.is_false:
        metadata = {'operator': 'is_frequently_in'}
        metadata.update(values_result.metadata)
        return Result.false(
            mode='exact',
            value=False,
            justification=values_result.justification,
            metadata=metadata,
        )

    values = values_result.value
    subset_set = set(subset)
    witness_by_start, failed_starts = _frequent_witnesses_by_start(
        indices, relation, values, subset_set
    )
    metadata = {
        'operator': 'is_frequently_in',
        'index_count': len(indices),
        'subset': tuple(sorted(subset_set, key=repr)),
        'witness_by_start_index': witness_by_start,
        'failed_start_indices': failed_starts,
    }

    if failed_starts:
        return Result.false(
            mode='exact',
            value=False,
            justification=['At least one finite tail does not meet the requested subset.'],
            proof_outline=[
                'For frequent containment, every tail {e : d0 <= e} must contain at least one value in the subset.'
            ],
            metadata=metadata,
        )

    return Result.true(
        mode='exact',
        value=True,
        justification=['Every finite tail of the net meets the requested subset.'],
        proof_outline=[
            'The check enumerates each finite tail and records a witness index where the value lies in the subset.'
        ],
        metadata=metadata,
    )

def net_converges_to(
    space: Any,
    index_set: Iterable[Any],
    preorder: Iterable[tuple[Any, Any]],
    net_values: Mapping[Any, Any] | Callable[[Any], Any],
    point: Any,
) -> Result:
    """Check finite open-neighborhood convergence of a net.

    For explicit finite spaces this checks the exact criterion: every open
    neighborhood of the proposed limit eventually contains the net.
    """

    indices = _normalize_indices(index_set)
    relation = _normalize_relation(preorder)
    directed = is_directed_set(indices, relation)
    if not directed.is_true:
        return Result.false(
            mode='exact',
            value=False,
            justification=['Net convergence requires a valid directed index set.'],
            metadata={
                'operator': 'net_converges_to',
                'directed_status': directed.status,
                'directed_metadata': directed.metadata,
            },
        )

    try:
        carrier = tuple(getattr(space, 'carrier'))
        topology = getattr(space, 'topology')
    except Exception:
        return Result.unknown(
            mode='symbolic',
            value='net_converges_to',
            justification=['Exact net convergence is currently implemented only for explicit finite topological spaces.'],
            metadata={'operator': 'net_converges_to', 'representation': 'symbolic_general'},
        )

    carrier_set = set(carrier)
    if point not in carrier_set:
        return Result.false(
            mode='exact',
            value=False,
            justification=['The proposed limit point is not in the finite carrier.'],
            metadata={'operator': 'net_converges_to', 'point': point, 'carrier': carrier},
        )

    values_result = _finite_net_values(indices, net_values)
    if values_result.is_false:
        metadata = {'operator': 'net_converges_to'}
        metadata.update(values_result.metadata)
        return Result.false(
            mode='exact',
            value=False,
            justification=values_result.justification,
            metadata=metadata,
        )

    values = values_result.value
    values_outside_carrier = tuple(
        (index, value) for index, value in values.items() if value not in carrier_set
    )
    if values_outside_carrier:
        return Result.false(
            mode='exact',
            value=False,
            justification=['At least one net value lies outside the finite carrier.'],
            metadata={
                'operator': 'net_converges_to',
                'values_outside_carrier': values_outside_carrier,
                'carrier': carrier,
            },
        )

    open_neighborhoods = _open_neighborhoods(topology, point)
    failed_open_neighborhoods: list[frozenset[Any]] = []
    witness_by_open_neighborhood: list[tuple[frozenset[Any], Any]] = []

    for open_set in open_neighborhoods:
        witness, _tail = _eventual_witness(indices, relation, values, set(open_set))
        if witness is None:
            failed_open_neighborhoods.append(open_set)
        else:
            witness_by_open_neighborhood.append((open_set, witness))

    metadata = {
        'operator': 'net_converges_to',
        'source': 'finite_topology',
        'point': point,
        'carrier': carrier,
        'open_neighborhoods': tuple(open_neighborhoods),
        'witness_by_open_neighborhood': tuple(witness_by_open_neighborhood),
        'failed_open_neighborhoods': tuple(failed_open_neighborhoods),
    }

    if failed_open_neighborhoods:
        return Result.false(
            mode='exact',
            value=False,
            justification=['At least one open neighborhood of the proposed limit is not eventually reached.'],
            proof_outline=[
                'Finite convergence was checked by testing eventual containment in every open neighborhood of the point.'
            ],
            metadata=metadata,
        )

    return Result.true(
        mode='exact',
        value=True,
        justification=['Every open neighborhood of the proposed limit eventually contains the net.'],
        proof_outline=[
            'For a finite explicit topology, checking open neighborhoods is equivalent to checking all neighborhoods.'
        ],
        metadata=metadata,
    )



def net_cluster_points(
    space: Any,
    index_set: Iterable[Any],
    preorder: Iterable[tuple[Any, Any]],
    net_values: Mapping[Any, Any] | Callable[[Any], Any],
) -> Result:
    """Compute finite open-neighborhood cluster diagnostics for a net.

    A point is reported as a finite net cluster point when the net is frequently
    in every open neighborhood of that point.  This matches the Cilt III
    definition at the level of explicit finite teaching spaces.
    """

    indices = _normalize_indices(index_set)
    relation = _normalize_relation(preorder)
    directed = is_directed_set(indices, relation)
    if not directed.is_true:
        return Result.false(
            mode='exact',
            value=False,
            justification=['Net cluster diagnostics require a valid directed index set.'],
            metadata={
                'operator': 'net_cluster_points',
                'directed_status': directed.status,
                'directed_metadata': directed.metadata,
            },
        )

    try:
        carrier = tuple(getattr(space, 'carrier'))
        topology = getattr(space, 'topology')
    except Exception:
        return Result.unknown(
            mode='symbolic',
            value='net_cluster_points',
            justification=['Exact net cluster diagnostics are currently implemented only for explicit finite topological spaces.'],
            metadata={'operator': 'net_cluster_points', 'representation': 'symbolic_general'},
        )

    carrier_set = set(carrier)
    values_result = _finite_net_values(indices, net_values)
    if values_result.is_false:
        metadata = {'operator': 'net_cluster_points'}
        metadata.update(values_result.metadata)
        return Result.false(
            mode='exact',
            value=False,
            justification=values_result.justification,
            metadata=metadata,
        )

    values = values_result.value
    values_outside_carrier = tuple(
        (index, value) for index, value in values.items() if value not in carrier_set
    )
    if values_outside_carrier:
        return Result.false(
            mode='exact',
            value=False,
            justification=['At least one net value lies outside the finite carrier.'],
            metadata={
                'operator': 'net_cluster_points',
                'values_outside_carrier': values_outside_carrier,
                'carrier': carrier,
            },
        )

    cluster_points: list[Any] = []
    failed_open_neighborhoods_by_point: list[tuple[Any, tuple[frozenset[Any], ...]]] = []
    witness_by_point: list[tuple[Any, tuple[tuple[frozenset[Any], tuple[tuple[Any, Any], ...]], ...]]] = []

    for point in carrier:
        open_neighborhoods = _open_neighborhoods(topology, point)
        point_failures: list[frozenset[Any]] = []
        point_witnesses: list[tuple[frozenset[Any], tuple[tuple[Any, Any], ...]]] = []
        for open_set in open_neighborhoods:
            witnesses, failed_starts = _frequent_witnesses_by_start(
                indices, relation, values, set(open_set)
            )
            if failed_starts:
                point_failures.append(open_set)
            else:
                point_witnesses.append((open_set, witnesses))
        if point_failures:
            failed_open_neighborhoods_by_point.append((point, tuple(point_failures)))
        else:
            cluster_points.append(point)
        witness_by_point.append((point, tuple(point_witnesses)))

    value = frozenset(cluster_points)
    return Result.true(
        mode='exact',
        value=value,
        justification=['Computed finite net cluster points by frequent containment in open neighborhoods.'],
        proof_outline=[
            'For each carrier point, enumerate open neighborhoods containing it.',
            'For each such neighborhood, test whether every finite tail meets that neighborhood.',
        ],
        metadata={
            'operator': 'net_cluster_points',
            'source': 'finite_topology',
            'carrier': carrier,
            'cluster_points': tuple(cluster_points),
            'failed_open_neighborhoods_by_point': tuple(failed_open_neighborhoods_by_point),
            'witness_by_point': tuple(witness_by_point),
            'v0_1_52_corridor_record': True,
        },
    )


def analyze_net(
    space: Any | None = None,
    index_set: Iterable[Any] | None = None,
    preorder: Iterable[tuple[Any, Any]] | None = None,
    net_values: Mapping[Any, Any] | Callable[[Any], Any] | None = None,
    *,
    point: Any | None = None,
    subset: Iterable[Any] | None = None,
) -> Result:
    """Return a structured finite summary for the Cilt III nets layer.

    Supply ``subset`` to compare eventual and frequent containment.  Supply a
    finite ``space`` and ``point`` to compare convergence to the point with the
    cluster-point set of the net.
    """

    if index_set is None or preorder is None or net_values is None:
        return Result.unknown(
            mode='symbolic',
            value='analyze_net',
            justification=['Provide index_set, preorder, and net_values to run finite net diagnostics.'],
            metadata={'operator': 'analyze_net'},
        )

    payload: dict[str, Any] = {}
    metadata: dict[str, Any] = {'operator': 'analyze_net', 'v0_1_52_corridor_record': True}

    if subset is not None:
        eventual = is_eventually_in(index_set, preorder, net_values, subset)
        frequent = is_frequently_in(index_set, preorder, net_values, subset)
        payload['eventually_in_subset'] = eventual.value
        payload['frequently_in_subset'] = frequent.value
        metadata['eventual_containment'] = eventual.to_dict()
        metadata['frequent_containment'] = frequent.to_dict()

    if space is not None:
        clusters = net_cluster_points(space, index_set, preorder, net_values)
        payload['cluster_points'] = clusters.value if clusters.is_true else None
        metadata['cluster_points'] = clusters.to_dict()
        if point is not None:
            convergence = net_converges_to(space, index_set, preorder, net_values, point)
            payload['converges_to_point'] = convergence.value
            payload['point_is_cluster_point'] = (
                point in clusters.value if clusters.is_true and isinstance(clusters.value, frozenset) else None
            )
            metadata['convergence'] = convergence.to_dict()

    if not payload:
        directed = is_directed_set(index_set, preorder)
        payload['directed_set'] = directed.value
        metadata['directed_set'] = directed.to_dict()

    return Result.true(
        mode='exact' if all(
            isinstance(record, dict) and record.get('mode') == 'exact'
            for key, record in metadata.items()
            if key != 'operator' and key != 'v0_1_52_corridor_record'
        ) else 'mixed',
        value=payload,
        justification=['Finite net diagnostics were evaluated for the supplied data.'],
        metadata=metadata,
    )

def _normalize_indices(index_set: Iterable[Any]) -> tuple[Any, ...]:
    seen: set[Any] = set()
    normalized: list[Any] = []
    for index in index_set:
        if index not in seen:
            seen.add(index)
            normalized.append(index)
    return tuple(normalized)


def _normalize_relation(preorder: Iterable[tuple[Any, Any]]) -> set[tuple[Any, Any]]:
    relation: set[tuple[Any, Any]] = set()
    for pair in preorder:
        try:
            a, b = pair
        except Exception as exc:  # pragma: no cover - defensive malformed-shape guard
            raise NetError('Each preorder entry must be a pair.') from exc
        relation.add((a, b))
    return relation


def _finite_net_values(indices: tuple[Any, ...], net_values: Mapping[Any, Any] | Callable[[Any], Any]) -> Result:
    values: dict[Any, Any] = {}
    missing: list[Any] = []

    if isinstance(net_values, Mapping):
        for index in indices:
            if index in net_values:
                values[index] = net_values[index]
            else:
                missing.append(index)
    elif callable(net_values):
        for index in indices:
            values[index] = net_values(index)
    else:
        return Result.false(
            mode='exact',
            value=False,
            justification=['Finite net values must be supplied as a mapping or callable.'],
            metadata={'missing_indices': (), 'value_source': type(net_values).__name__},
        )

    if missing:
        return Result.false(
            mode='exact',
            value=False,
            justification=['The finite net is missing values for at least one declared index.'],
            metadata={'missing_indices': tuple(missing), 'value_source': type(net_values).__name__},
        )

    return Result.true(
        mode='exact',
        value=values,
        justification=['Finite net values were read for every declared index.'],
        metadata={'missing_indices': (), 'value_source': type(net_values).__name__},
    )


def _first_upper_bound(indices: tuple[Any, ...], relation: set[tuple[Any, Any]], a: Any, b: Any) -> Any | None:
    for candidate in indices:
        if (a, candidate) in relation and (b, candidate) in relation:
            return candidate
    return None


def _tail(indices: tuple[Any, ...], relation: set[tuple[Any, Any]], start: Any) -> tuple[Any, ...]:
    return tuple(index for index in indices if (start, index) in relation)


def _eventual_witness(
    indices: tuple[Any, ...],
    relation: set[tuple[Any, Any]],
    values: Mapping[Any, Any],
    subset: set[Any],
) -> tuple[Any | None, tuple[Any, ...] | None]:
    for candidate in indices:
        tail = _tail(indices, relation, candidate)
        if tail and all(values[index] in subset for index in tail):
            return candidate, tail
    return None, None


def _candidate_tail_violations(
    indices: tuple[Any, ...],
    relation: set[tuple[Any, Any]],
    values: Mapping[Any, Any],
    subset: set[Any],
) -> tuple[tuple[Any, tuple[Any, ...]], ...]:
    violations: list[tuple[Any, tuple[Any, ...]]] = []
    for candidate in indices:
        tail = _tail(indices, relation, candidate)
        bad_tail = tuple(index for index in tail if values[index] not in subset)
        if bad_tail:
            violations.append((candidate, bad_tail))
    return tuple(violations)


def _frequent_witnesses_by_start(
    indices: tuple[Any, ...],
    relation: set[tuple[Any, Any]],
    values: Mapping[Any, Any],
    subset: set[Any],
) -> tuple[tuple[tuple[Any, Any], ...], tuple[Any, ...]]:
    witnesses: list[tuple[Any, Any]] = []
    failed_starts: list[Any] = []
    for start in indices:
        tail = _tail(indices, relation, start)
        witness = next((index for index in tail if values[index] in subset), None)
        if witness is None:
            failed_starts.append(start)
        else:
            witnesses.append((start, witness))
    return tuple(witnesses), tuple(failed_starts)


def _open_neighborhoods(topology: Iterable[Iterable[Any]], point: Any) -> tuple[frozenset[Any], ...]:
    neighborhoods = [frozenset(open_set) for open_set in topology if point in set(open_set)]
    return tuple(sorted(neighborhoods, key=lambda block: (len(block), tuple(sorted(map(repr, block))))))


def _repr_tuple_key(value: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(repr(part) for part in value)


__all__ = [
    'NetError',
    'is_directed_set',
    'is_eventually_in',
    'is_frequently_in',
    'net_converges_to',
    'net_cluster_points',
    'analyze_net',
]
