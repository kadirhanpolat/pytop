"""Structured map support for infinite and symbolic topological settings.

This module does not try to solve arbitrary continuity or quotient questions by
inspection. Instead, it provides a small symbolic map layer that integrates with
`Result`, explicit tags, and theorem-style implications.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .capabilities import normalize_feature_name
from .result import Result

MAP_PROPERTIES = {
    'continuous',
    'open',
    'closed',
    'injective',
    'surjective',
    'bijective',
    'embedding',
    'quotient',
    'homeomorphism',
}


@dataclass
class SymbolicMap:
    """A symbolic map between topological spaces.

    The class is intentionally lightweight. The `tags` field encodes exact map
    facts already known about the map. The analysis helpers in this module then
    use these exact tags together with a few standard theorem implications.
    """

    domain: Any
    codomain: Any
    name: str = 'f'
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.metadata = dict(self.metadata)
        self.tags = {str(tag).strip().lower() for tag in self.tags if str(tag).strip()}
        meta_tags = self.metadata.get('tags', [])
        self.tags.update(str(tag).strip().lower() for tag in meta_tags if str(tag).strip())
        self.metadata.setdefault('representation', 'symbolic_map')
        self.metadata['tags'] = sorted(self.tags)

    def add_tags(self, *tags: str) -> None:
        for tag in tags:
            text = str(tag).strip().lower()
            if text:
                self.tags.add(text)
        self.metadata['tags'] = sorted(self.tags)

    def has_tag(self, tag: str) -> bool:
        return str(tag).strip().lower() in self.tags


@dataclass
class ContinuousMap(SymbolicMap):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('continuous')
        self.metadata['representation'] = 'continuous_map'


@dataclass
class EmbeddingMap(SymbolicMap):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('embedding', 'continuous', 'injective')
        self.metadata['representation'] = 'embedding_map'


@dataclass
class QuotientMap(SymbolicMap):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('quotient', 'continuous', 'surjective')
        self.metadata['representation'] = 'quotient_map'


@dataclass
class HomeomorphismMap(SymbolicMap):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags(
            'homeomorphism', 'continuous', 'open', 'closed', 'bijective',
            'injective', 'surjective', 'embedding', 'quotient'
        )
        self.metadata['representation'] = 'homeomorphism_map'


@dataclass
class ConstantMap(SymbolicMap):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags('constant', 'continuous')
        self.metadata['representation'] = 'constant_map'


def normalize_map_property(name: str) -> str:
    name = normalize_feature_name(name)
    aliases = {
        'one_to_one': 'injective',
        'onto': 'surjective',
        'quotient_map': 'quotient',
        'open_map': 'open',
        'closed_map': 'closed',
    }
    name = aliases.get(name, name)
    if name not in MAP_PROPERTIES:
        raise ValueError(f'Unsupported map property {name!r}. Expected one of {sorted(MAP_PROPERTIES)}.')
    return name


def analyze_infinite_map_property(map_obj: SymbolicMap, property_name: str = 'continuous') -> Result:
    property_name = normalize_map_property(property_name)

    if _has_positive_tag(map_obj, property_name):
        return Result.true(
            mode='exact',
            value=property_name,
            justification=[f'Map tag {property_name!r} is explicitly present.'],
            metadata=_map_metadata(map_obj, property_name, source='tags'),
        )
    if _has_negative_tag(map_obj, property_name):
        return Result.false(
            mode='exact',
            value=property_name,
            justification=[f'Map tag not_{property_name!r} is explicitly present.'],
            metadata=_map_metadata(map_obj, property_name, source='tags'),
        )

    theorem = _theorem_map_property(map_obj, property_name)
    if theorem is not None:
        return theorem

    return Result.unknown(
        mode='symbolic',
        value=property_name,
        justification=[
            f'No exact tag or theorem implication determined {property_name!r} for this map.',
        ],
        proof_outline=[
            'Add explicit map tags such as continuous/open/quotient/homeomorphism.',
            'Or supply enough structural data so a theorem implication can be applied.',
        ],
        metadata=_map_metadata(map_obj, property_name, source='unknown'),
    )


def is_continuous_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'continuous')


def is_open_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'open')


def is_closed_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'closed')


def is_injective_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'injective')


def is_surjective_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'surjective')


def is_bijective_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'bijective')


def is_embedding_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'embedding')


def is_quotient_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'quotient')


def is_homeomorphism_map(map_obj: SymbolicMap) -> Result:
    return analyze_infinite_map_property(map_obj, 'homeomorphism')


def infinite_map_report(map_obj: SymbolicMap) -> dict[str, Result]:
    return {name: analyze_infinite_map_property(map_obj, name) for name in sorted(MAP_PROPERTIES)}


def identity_map(space: Any, *, name: str = 'id') -> HomeomorphismMap:
    return HomeomorphismMap(
        domain=space,
        codomain=space,
        name=name,
        metadata={'description': 'Identity map.'},
    )


def compose_maps(first: SymbolicMap, second: SymbolicMap, *, name: str | None = None) -> SymbolicMap:
    """Compose `second ∘ first` symbolically.

    The implementation is deliberately conservative. Only standard stable map
    properties are propagated automatically.
    """
    composite = SymbolicMap(
        domain=first.domain,
        codomain=second.codomain,
        name=name or f'{second.name}∘{first.name}',
        metadata={'representation': 'symbolic_map', 'composed_from': [first.name, second.name]},
    )

    for feature in ('continuous', 'open', 'closed', 'injective', 'surjective', 'bijective'):
        r1 = analyze_infinite_map_property(first, feature)
        r2 = analyze_infinite_map_property(second, feature)
        if r1.is_true and r2.is_true:
            composite.add_tags(feature)

    if is_homeomorphism_map(first).is_true and is_homeomorphism_map(second).is_true:
        composite.add_tags('homeomorphism', 'embedding', 'quotient')
    elif is_embedding_map(first).is_true and is_embedding_map(second).is_true:
        composite.add_tags('embedding')

    return composite




def homeomorphism_criterion_result(map_obj: SymbolicMap) -> Result:
    """Return the best available homeomorphism criterion result for *map_obj*."""
    return analyze_infinite_map_property(map_obj, 'homeomorphism')



def initial_topology_descriptor(defining_maps: Iterable[SymbolicMap]) -> dict[str, Any]:
    defining_maps = list(defining_maps)
    if not defining_maps:
        raise ValueError('initial_topology_descriptor requires at least one defining map.')
    domain = defining_maps[0].domain
    if any(candidate.domain is not domain for candidate in defining_maps[1:]):
        raise ValueError('All defining maps must share the same domain object.')
    return {
        'representation': 'initial_topology_descriptor',
        'domain_description': getattr(getattr(domain, 'metadata', {}), 'get', lambda *_: None)('description') if hasattr(getattr(domain, 'metadata', {}), 'get') else None,
        'defining_maps': [getattr(candidate, 'name', 'f') for candidate in defining_maps],
        'tags': ['initial_topology', 'coarsest_for_continuity'],
    }

def _has_positive_tag(map_obj: SymbolicMap, property_name: str) -> bool:
    metadata = getattr(map_obj, 'metadata', {}) or {}
    if metadata.get(property_name) is True:
        return True
    return getattr(map_obj, 'has_tag', lambda _: False)(property_name)


def _has_negative_tag(map_obj: SymbolicMap, property_name: str) -> bool:
    metadata = getattr(map_obj, 'metadata', {}) or {}
    if metadata.get(property_name) is False:
        return True
    return getattr(map_obj, 'has_tag', lambda _: False)(f'not_{property_name}')


def _theorem_map_property(map_obj: SymbolicMap, property_name: str) -> Result | None:
    tags = getattr(map_obj, 'tags', set())
    if 'homeomorphism' in tags and property_name in {'continuous', 'open', 'closed', 'bijective', 'embedding', 'quotient'}:
        return Result.true(
            mode='theorem',
            value=property_name,
            justification=['Every homeomorphism is continuous, open, closed, bijective, an embedding, and a quotient map.'],
            proof_outline=['Apply the standard characterization of homeomorphisms.'],
            metadata=_map_metadata(map_obj, property_name, source='theorem_homeomorphism'),
        )
    if 'embedding' in tags and property_name in {'continuous', 'injective'}:
        return Result.true(
            mode='theorem',
            value=property_name,
            justification=['Every embedding is continuous and injective.'],
            proof_outline=['Use the definition of embedding.'],
            metadata=_map_metadata(map_obj, property_name, source='theorem_embedding'),
        )
    if 'quotient' in tags and property_name in {'continuous', 'surjective'}:
        return Result.true(
            mode='theorem',
            value=property_name,
            justification=['Every quotient map is continuous and surjective.'],
            proof_outline=['Use the definition of quotient map.'],
            metadata=_map_metadata(map_obj, property_name, source='theorem_quotient'),
        )
    if property_name == 'homeomorphism':
        if {'continuous', 'bijective', 'open'}.issubset(tags):
            return Result.true(
                mode='theorem',
                value='homeomorphism',
                justification=['A bijective continuous open map is a homeomorphism.'],
                proof_outline=['Show that the inverse map sends open sets to open sets.'],
                metadata=_map_metadata(map_obj, property_name, source='theorem_open_inverse'),
            )
        if {'continuous', 'bijective', 'closed'}.issubset(tags):
            return Result.true(
                mode='theorem',
                value='homeomorphism',
                justification=['A bijective continuous closed map is a homeomorphism.'],
                proof_outline=['A closed bijection with continuous forward map has continuous inverse.'],
                metadata=_map_metadata(map_obj, property_name, source='theorem_closed_inverse'),
            )
    return None


def _map_metadata(map_obj: SymbolicMap, property_name: str, *, source: str) -> dict[str, Any]:
    return {
        'property': property_name,
        'source': source,
        'representation': getattr(map_obj, 'metadata', {}).get('representation', 'symbolic_map'),
        'map_name': getattr(map_obj, 'name', 'f'),
    }


__all__ = [
    'SymbolicMap',
    'ContinuousMap',
    'EmbeddingMap',
    'QuotientMap',
    'HomeomorphismMap',
    'ConstantMap',
    'analyze_infinite_map_property',
    'is_continuous_map',
    'is_open_map',
    'is_closed_map',
    'is_injective_map',
    'is_surjective_map',
    'is_bijective_map',
    'is_embedding_map',
    'is_quotient_map',
    'is_homeomorphism_map',
    'infinite_map_report',
    'identity_map',
    'compose_maps',
    'homeomorphism_criterion_result',
    'initial_topology_descriptor',
]
