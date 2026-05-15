"""Topological invariants and basic cardinal-function support.

The current implementation focuses on a small but useful family of invariants:
weight, density, character, Lindelöf number, and cellularity.

On explicit finite spaces these are computed exactly. On selected infinite
representations the module uses theorem-backed or metadata-backed answers.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable

from .capabilities import DEFAULT_REGISTRY, normalize_feature_name
from .result import Result
from .theorem_engine import infer_feature

FINITE_INVARIANTS = {'weight', 'density', 'character', 'lindelof_number', 'cellularity'}


class InvariantError(ValueError):
    """Raised when an unsupported invariant is requested."""


def normalize_invariant_name(name: str) -> str:
    normalized = normalize_feature_name(name)
    aliases = {
        'w': 'weight',
        'd': 'density',
        'chi': 'character',
        'local_character': 'character',
        'lindelofnumber': 'lindelof_number',
        'lindelof_no': 'lindelof_number',
        'cell': 'cellularity',
    }
    normalized = aliases.get(normalized, normalized)
    valid = set(FINITE_INVARIANTS)
    if normalized not in valid:
        raise InvariantError(
            f"Unsupported invariant {name!r}. Expected one of {sorted(valid)}."
        )
    return normalized


def analyze_invariant(space: Any, invariant_name: str = 'weight') -> Result:
    invariant_name = normalize_invariant_name(invariant_name)
    tags = _extract_tags(space)
    representation = _representation_of(space)
    capability = DEFAULT_REGISTRY.support_for(representation, invariant_name)

    if representation == 'finite' and hasattr(space, 'topology'):
        exact_value = _finite_invariant(space, invariant_name)
        if exact_value is not None:
            return Result.true(
                mode='exact',
                value=exact_value,
                justification=[f'Computed the invariant {invariant_name} from the explicit finite topology.'],
                proof_outline=[_proof_hint_for_finite_invariant(invariant_name)],
                metadata={
                    'representation': representation,
                    'invariant': invariant_name,
                    'tags': sorted(tags),
                },
            )

    metadata_result = _metadata_backed_invariant(space, invariant_name, capability.support)
    if metadata_result is not None:
        metadata_result.metadata.setdefault('representation', representation)
        metadata_result.metadata.setdefault('invariant', invariant_name)
        metadata_result.metadata.setdefault('tags', sorted(tags))
        return metadata_result

    theorem_result = infer_feature(invariant_name, space)
    if not theorem_result.is_unknown:
        theorem_result.metadata.setdefault('invariant', invariant_name)
        return theorem_result

    return Result.unknown(
        mode=_mode_from_support(capability.support),
        value=invariant_name,
        justification=[capability.notes or f'No decisive invariant information available for {representation}.'],
        metadata={
            'representation': representation,
            'invariant': invariant_name,
            'tags': sorted(tags),
        },
    )


def weight(space: Any) -> Result:
    return analyze_invariant(space, 'weight')


def density(space: Any) -> Result:
    return analyze_invariant(space, 'density')


def character(space: Any) -> Result:
    return analyze_invariant(space, 'character')


def lindelof_number(space: Any) -> Result:
    return analyze_invariant(space, 'lindelof_number')


def cellularity(space: Any) -> Result:
    return analyze_invariant(space, 'cellularity')


def invariants_summary(space: Any) -> dict[str, Result]:
    return {name: analyze_invariant(space, name) for name in sorted(FINITE_INVARIANTS)}


# ----------------------- finite exact computations -----------------------

def _finite_invariant(space: Any, invariant_name: str) -> int | str | None:
    topology = getattr(space, 'topology', None)
    carrier = getattr(space, 'carrier', None)
    if topology is None or carrier is None:
        return None
    opens = _normalize_topology(topology)
    points = tuple(carrier)

    if invariant_name == 'weight':
        return _finite_weight(points, opens)
    if invariant_name == 'density':
        return _finite_density(points, opens)
    if invariant_name == 'character':
        return _finite_character(points, opens)
    if invariant_name == 'lindelof_number':
        return _finite_lindelof_number(points, opens)
    if invariant_name == 'cellularity':
        return _finite_cellularity(opens)
    return None


def _finite_weight(points: tuple[Any, ...], opens: list[set[Any]]) -> int:
    nonempty_opens = [U for U in opens if U]
    for size in range(0, len(nonempty_opens) + 1):
        for family in combinations(nonempty_opens, size):
            if _is_basis(points, opens, family):
                return size
    return len(nonempty_opens)


def _finite_density(points: tuple[Any, ...], opens: list[set[Any]]) -> int:
    for size in range(0, len(points) + 1):
        for subset in combinations(points, size):
            D = set(subset)
            if _closure(D, points, opens) == set(points):
                return size
    return len(points)


def _finite_character(points: tuple[Any, ...], opens: list[set[Any]]) -> int:
    local_values = [_local_character(x, opens) for x in points]
    return max(local_values, default=0)


def _finite_lindelof_number(points: tuple[Any, ...], opens: list[set[Any]]) -> int:
    nonempty_opens = [U for U in opens if U]
    if not points:
        return 0
    cover_families = [family for size in range(1, len(nonempty_opens) + 1) for family in combinations(nonempty_opens, size) if set().union(*family) == set(points)]
    best_bounds: list[int] = []
    for family in cover_families:
        min_size = len(family)
        for size in range(1, len(family) + 1):
            for subfamily in combinations(family, size):
                if set().union(*subfamily) == set(points):
                    min_size = size
                    break
            if min_size == size:
                break
        best_bounds.append(min_size)
    return max(best_bounds, default=0)


def _finite_cellularity(opens: list[set[Any]]) -> int:
    nonempty_opens = [U for U in opens if U]
    max_size = 0
    for size in range(1, len(nonempty_opens) + 1):
        for family in combinations(nonempty_opens, size):
            if _pairwise_disjoint(family):
                max_size = max(max_size, size)
    return max_size


def _is_basis(points: tuple[Any, ...], opens: list[set[Any]], family: Iterable[set[Any]]) -> bool:
    basis = [set(U) for U in family]
    for O in opens:
        if not O:
            continue
        for x in O:
            if not any(x in B and B.issubset(O) for B in basis):
                return False
    return True


def _closure(subset: set[Any], points: tuple[Any, ...], opens: list[set[Any]]) -> set[Any]:
    closure: set[Any] = set()
    for x in points:
        neighborhoods = [U for U in opens if x in U]
        if all(U & subset for U in neighborhoods):
            closure.add(x)
    return closure


def _local_character(point: Any, opens: list[set[Any]]) -> int:
    neighborhoods = [U for U in opens if point in U]
    if not neighborhoods:
        return 0
    for size in range(1, len(neighborhoods) + 1):
        for family in combinations(neighborhoods, size):
            if all(any(point in V and V.issubset(U) for V in family) for U in neighborhoods):
                return size
    return len(neighborhoods)


def _pairwise_disjoint(family: Iterable[set[Any]]) -> bool:
    items = list(family)
    return all(items[i].isdisjoint(items[j]) for i in range(len(items)) for j in range(i + 1, len(items)))


def _normalize_topology(topology: Iterable[Iterable[Any]]) -> list[set[Any]]:
    normalized = []
    seen: set[frozenset[Any]] = set()
    for open_set in topology:
        as_set = frozenset(open_set)
        if as_set not in seen:
            seen.add(as_set)
            normalized.append(set(as_set))
    return normalized


# ---------------- metadata / theorem support helpers ----------------

def _metadata_backed_invariant(space: Any, invariant_name: str, support: str) -> Result | None:
    metadata = getattr(space, 'metadata', {}) or {}
    key_map = {
        'weight': ('weight', 'basis_size'),
        'density': ('density', 'dense_subset_size'),
        'character': ('character', 'local_base_size'),
        'lindelof_number': ('lindelof_number',),
        'cellularity': ('cellularity',),
    }
    for key in key_map[invariant_name]:
        if key in metadata:
            return Result.true(
                mode='exact' if support == 'exact' else 'mixed',
                value=metadata[key],
                justification=[f'Metadata field {key!r} supplies the invariant value for {invariant_name}.'],
                metadata={'source': 'metadata', 'metadata_key': key},
            )
    return None


def _proof_hint_for_finite_invariant(invariant_name: str) -> str:
    hints = {
        'weight': 'Search over finite subfamilies of open sets and test the basis condition.',
        'density': 'Search over subsets of the carrier and test whether their closure equals the whole space.',
        'character': 'At each point, search for a smallest local base; then take the maximum over points.',
        'lindelof_number': 'Enumerate open covers and record the largest minimum subcover size.',
        'cellularity': 'Search for a largest family of pairwise disjoint nonempty open sets.',
    }
    return hints[invariant_name]


def _representation_of(space: Any) -> str:
    metadata = getattr(space, 'metadata', {}) or {}
    return str(metadata.get('representation', 'symbolic_general')).strip().lower()



def _extract_tags(space: Any) -> set[str]:
    tags: set[str] = set()
    raw_tags = getattr(space, 'tags', set())
    tags.update(str(tag).strip().lower() for tag in raw_tags if str(tag).strip())
    metadata = getattr(space, 'metadata', {}) or {}
    for tag in metadata.get('tags', []):
        text = str(tag).strip().lower()
        if text:
            tags.add(text)
    return tags



def _mode_from_support(support: str) -> str:
    return {
        'exact': 'exact',
        'theorem': 'theorem',
        'symbolic': 'symbolic',
        'mixed': 'mixed',
        'none': 'symbolic',
    }[support]


__all__ = [
    "InvariantError",
    "normalize_invariant_name",
    "analyze_invariant",
    "weight",
    "density",
    "character",
    "lindelof_number",
    "cellularity",
    "invariants_summary",
]
