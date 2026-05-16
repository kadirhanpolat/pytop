"""Exact subset operators for finite topological spaces.

This module turns the Chapter 05 operator corridor into a public API layer.
The current implementation is exact for explicit finite spaces and deliberately
honest for symbolic/infinite inputs: when the repository cannot compute the
operator without additional structure, it returns a structured unknown result.
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import combinations
from typing import Any

from .result import Result


class SubsetOperatorError(ValueError):
    """Raised when a subset operator request is malformed."""


class UnknownFiniteSubsetError(TypeError):
    """Raised when an exact finite subset computation cannot be performed."""


class UnknownFinitePointError(TypeError):
    """Raised when an exact finite point computation cannot be performed."""


EXACT_FINITE_OPERATORS = {
    'closure',
    'interior',
    'boundary',
    'derived_set',
    'exterior',
    'neighborhood_system',
    'is_neighborhood',
    'nowhere_dense',
}


def closure_of_subset(space: Any, subset: Any) -> Result:
    return _analyze_subset_operator(space, 'closure', subset=subset)


def interior_of_subset(space: Any, subset: Any) -> Result:
    return _analyze_subset_operator(space, 'interior', subset=subset)


def boundary_of_subset(space: Any, subset: Any) -> Result:
    return _analyze_subset_operator(space, 'boundary', subset=subset)


def derived_set_of_subset(space: Any, subset: Any) -> Result:
    return _analyze_subset_operator(space, 'derived_set', subset=subset)


def exterior_of_subset(space: Any, subset: Any) -> Result:
    return _analyze_subset_operator(space, 'exterior', subset=subset)


def neighborhood_system_of_point(space: Any, point: Any) -> Result:
    return _analyze_subset_operator(space, 'neighborhood_system', point=point)


def is_neighborhood_of_point(space: Any, point: Any, subset: Any) -> Result:
    """Decide whether ``subset`` is a neighborhood of ``point``.

    For explicit finite spaces this uses the textbook criterion: ``subset`` is
    a neighborhood of ``point`` when it contains at least one open set that
    contains ``point``.  The subset itself need not be open.
    """
    return _analyze_subset_operator(space, 'is_neighborhood', subset=subset, point=point)


def is_nowhere_dense_subset(space: Any, subset: Any) -> Result:
    return _analyze_subset_operator(space, 'nowhere_dense', subset=subset)


def _analyze_subset_operator(space: Any, operator_name: str, *, subset: Any | None = None, point: Any | None = None) -> Result:
    representation = _representation_of(space)

    if _space_is_finite(space) and hasattr(space, 'topology'):
        try:
            finite_data = _finite_space_data(space)
            if operator_name == 'neighborhood_system':
                finite_point = _as_finite_point(space, point)
                return _exact_neighborhood_system_result(finite_data, finite_point)
            if operator_name == 'is_neighborhood':
                finite_point = _as_finite_point(space, point)
                finite_subset = _as_finite_subset(space, subset)
                return _exact_is_neighborhood_result(finite_data, finite_point, finite_subset)
            finite_subset = _as_finite_subset(space, subset)
            return _exact_subset_operator_result(finite_data, operator_name, finite_subset)
        except (UnknownFiniteSubsetError, UnknownFinitePointError):
            pass

    justification = [
        'The requested operator currently has exact support only for explicit finite spaces.'
    ]
    proof_outline = [
        'Provide a finite carrier together with its explicit topology to obtain an exact result.',
        'Symbolic/infinite operator support remains a later phase of the ecosystem.',
    ]
    metadata = {'representation': representation, 'operator': operator_name}
    if subset is not None:
        metadata['subset_repr'] = repr(subset)
    if point is not None:
        metadata['point_repr'] = repr(point)
    return Result.unknown(
        mode='symbolic',
        value=operator_name,
        justification=justification,
        proof_outline=proof_outline,
        metadata=metadata,
    )


def _exact_subset_operator_result(finite_data: dict[str, Any], operator_name: str, subset: set[Any]) -> Result:
    carrier = finite_data['carrier']
    opens = finite_data['opens']
    points = finite_data['points']

    if operator_name == 'closure':
        value = frozenset(_closure(subset, points, opens))
        justification = [
            'Computed exactly by checking, for each point, whether every open neighborhood meets the subset.'
        ]
    elif operator_name == 'interior':
        value = frozenset(_interior(subset, opens))
        justification = [
            'Computed exactly as the union of all open sets contained in the subset.'
        ]
    elif operator_name == 'derived_set':
        value = frozenset(_derived_set(subset, points, opens))
        justification = [
            'Computed exactly by checking deleted-neighborhood intersections in the finite topology.'
        ]
    elif operator_name == 'exterior':
        value = frozenset(_interior(carrier - subset, opens))
        justification = [
            'Computed exactly as the interior of the complement inside the finite ambient space.'
        ]
    elif operator_name == 'boundary':
        closure = _closure(subset, points, opens)
        interior = _interior(subset, opens)
        value = frozenset(closure - interior)
        justification = [
            'Computed exactly from the finite formulas boundary(A)=closure(A)\\setminus interior(A).'
        ]
    elif operator_name == 'nowhere_dense':
        closure = _closure(subset, points, opens)
        interior_of_closure = _interior(closure, opens)
        conclusion = interior_of_closure == set()
        justification = [
            'Computed exactly from the finite criterion interior(closure(A))=emptyset.'
        ]
        return _boolean_result(
            conclusion,
            operator_name,
            justification,
            finite_data,
            subset,
            extra_metadata={'interior_of_closure': tuple(_sorted_frozensets([interior_of_closure]))[0]},
        )
    else:
        raise SubsetOperatorError(f'Unsupported exact subset operator {operator_name!r}.')

    metadata = _metadata_block(finite_data, operator_name, subset)
    return Result.true(
        mode='exact',
        value=value,
        justification=justification,
        metadata=metadata,
    )


def _exact_neighborhood_system_result(finite_data: dict[str, Any], point: Any) -> Result:
    open_neighborhoods = [open_set for open_set in finite_data['opens'] if point in open_set]
    neighborhoods = [
        candidate
        for candidate in _all_subsets(finite_data['points'])
        if any(open_set.issubset(candidate) for open_set in open_neighborhoods)
    ]
    neighborhoods = _sorted_frozensets(neighborhoods)
    open_neighborhoods = _sorted_frozensets(open_neighborhoods)
    minimal_open = frozenset.intersection(*open_neighborhoods) if open_neighborhoods else frozenset()
    return Result.true(
        mode='exact',
        value=tuple(neighborhoods),
        justification=[
            'Computed exactly as all subsets that contain at least one open set containing the selected point.'
        ],
        metadata={
            'operator': 'neighborhood_system',
            'source': 'finite_topology',
            'point': point,
            'carrier': tuple(finite_data['points']),
            'minimal_neighborhood': minimal_open,
            'minimal_open_neighborhood': minimal_open,
            'open_neighborhoods': tuple(open_neighborhoods),
            'open_neighborhood_count': len(open_neighborhoods),
            'neighborhood_count': len(neighborhoods),
            'contains_non_open_neighborhoods': len(neighborhoods) > len(open_neighborhoods),
        },
    )


def _exact_is_neighborhood_result(finite_data: dict[str, Any], point: Any, subset: set[Any]) -> Result:
    open_neighborhoods = [open_set for open_set in finite_data['opens'] if point in open_set]
    witness_open_neighborhoods = [
        open_set for open_set in open_neighborhoods if open_set.issubset(subset)
    ]
    conclusion = bool(witness_open_neighborhoods)
    justification = [
        'A subset is a neighborhood of a point exactly when it contains an open set containing that point.'
    ]
    open_neighborhoods = _sorted_frozensets(open_neighborhoods)
    witnesses = _sorted_frozensets(witness_open_neighborhoods)
    minimal_open = frozenset.intersection(*open_neighborhoods) if open_neighborhoods else frozenset()
    return _boolean_result(
        conclusion,
        'is_neighborhood',
        justification,
        finite_data,
        subset,
        extra_metadata={
            'point': point,
            'minimal_open_neighborhood': minimal_open,
            'witness_open_neighborhoods': tuple(witnesses),
            'open_neighborhood_count': len(open_neighborhoods),
        },
    )


def _boolean_result(
    conclusion: bool,
    operator_name: str,
    justification: list[str],
    finite_data: dict[str, Any],
    subset: set[Any],
    *,
    extra_metadata: dict[str, Any] | None = None,
) -> Result:
    metadata = _metadata_block(finite_data, operator_name, subset)
    if extra_metadata:
        metadata.update(extra_metadata)
    if conclusion:
        return Result.true(mode='exact', value=True, justification=justification, metadata=metadata)
    return Result.false(mode='exact', value=False, justification=justification, metadata=metadata)


def _metadata_block(finite_data: dict[str, Any], operator_name: str, subset: set[Any]) -> dict[str, Any]:
    return {
        'operator': operator_name,
        'source': 'finite_topology',
        'carrier': tuple(finite_data['points']),
        'subset': tuple(sorted(subset, key=repr)),
    }


def _finite_space_data(space: Any) -> dict[str, Any]:
    points = tuple(getattr(space, 'carrier', ()))
    opens = _normalize_topology(getattr(space, 'topology', ()))
    return {'points': points, 'carrier': set(points), 'opens': opens}


def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False


def _as_finite_subset(space: Any, subset: Any) -> set[Any]:
    carrier = set(getattr(space, 'carrier', ()))
    if isinstance(subset, (set, frozenset, list, tuple)):
        candidate = set(subset)
    elif hasattr(subset, 'label'):
        raise UnknownFiniteSubsetError('Symbolic subsets cannot be interpreted exactly on finite spaces.')
    else:
        raise UnknownFiniteSubsetError('Unsupported finite subset representation.')
    if not candidate.issubset(carrier):
        raise UnknownFiniteSubsetError('Subset contains points outside the carrier.')
    return candidate


def _as_finite_point(space: Any, point: Any) -> Any:
    carrier = set(getattr(space, 'carrier', ()))
    if point not in carrier:
        raise UnknownFinitePointError('Point lies outside the finite carrier.')
    return point


def _normalize_topology(topology: Iterable[Iterable[Any]]) -> list[set[Any]]:
    normalized: list[set[Any]] = []
    seen: set[frozenset[Any]] = set()
    for open_set in topology:
        as_set = frozenset(open_set)
        if as_set not in seen:
            seen.add(as_set)
            normalized.append(set(as_set))
    normalized.sort(key=lambda block: (len(block), tuple(sorted(map(repr, block)))))
    return normalized


def _closure(subset: set[Any], points: tuple[Any, ...], opens: list[set[Any]]) -> set[Any]:
    closure: set[Any] = set()
    for point in points:
        neighborhoods = [open_set for open_set in opens if point in open_set]
        if all(open_set & subset for open_set in neighborhoods):
            closure.add(point)
    return closure


def _interior(subset: set[Any], opens: list[set[Any]]) -> set[Any]:
    interior: set[Any] = set()
    for open_set in opens:
        if open_set.issubset(subset):
            interior |= open_set
    return interior


def _derived_set(subset: set[Any], points: tuple[Any, ...], opens: list[set[Any]]) -> set[Any]:
    derived: set[Any] = set()
    for point in points:
        deleted_subset = subset - {point}
        neighborhoods = [open_set for open_set in opens if point in open_set]
        if all(open_set & deleted_subset for open_set in neighborhoods):
            derived.add(point)
    return derived


def _all_subsets(points: tuple[Any, ...]) -> list[set[Any]]:
    point_list = list(points)
    return [
        set(block)
        for size in range(len(point_list) + 1)
        for block in combinations(point_list, size)
    ]


def _sorted_frozensets(family: Iterable[Iterable[Any]]) -> list[frozenset[Any]]:
    return [
        frozenset(block)
        for block in sorted((set(member) for member in family), key=lambda block: (len(block), tuple(sorted(map(repr, block)))))
    ]


def _representation_of(space: Any) -> str:
    metadata = getattr(space, 'metadata', None)
    if isinstance(metadata, dict):
        representation = metadata.get('representation')
        if representation:
            return str(representation)
    if hasattr(space, 'topology') and _space_is_finite(space):
        return 'finite'
    return 'symbolic_general'


__all__ = [
    'SubsetOperatorError',
    'UnknownFiniteSubsetError',
    'UnknownFinitePointError',
    'closure_of_subset',
    'interior_of_subset',
    'boundary_of_subset',
    'derived_set_of_subset',
    'exterior_of_subset',
    'neighborhood_system_of_point',
    'is_neighborhood_of_point',
    'is_nowhere_dense_subset',
]
