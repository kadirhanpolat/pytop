"""Image and preimage helpers for symbolic infinite-space analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .infinite_maps import SymbolicMap, analyze_infinite_map_property
from .infinite_spaces import InfiniteTopologicalSpace


@dataclass
class SymbolicSubset:
    ambient: Any
    label: str
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.metadata = dict(self.metadata)
        self.tags = {str(tag).strip().lower() for tag in self.tags if str(tag).strip()}
        meta_tags = self.metadata.get('tags', [])
        self.tags.update(str(tag).strip().lower() for tag in meta_tags if str(tag).strip())
        self.metadata['tags'] = sorted(self.tags)

    def add_tags(self, *tags: str) -> None:
        for tag in tags:
            text = str(tag).strip().lower()
            if text:
                self.tags.add(text)
        self.metadata['tags'] = sorted(self.tags)

    def has_tag(self, tag: str) -> bool:
        return str(tag).strip().lower() in self.tags


def image_space(map_obj: SymbolicMap, *, metadata: dict[str, Any] | None = None) -> InfiniteTopologicalSpace:
    metadata = dict(metadata or {})
    domain = getattr(map_obj, 'domain', None)
    codomain = getattr(map_obj, 'codomain', None)
    tags = set(getattr(codomain, 'tags', set()))

    if analyze_infinite_map_property(map_obj, 'continuous').is_true:
        if _space_has(domain, 'compact'):
            tags.add('compact')
        if _space_has(domain, 'connected'):
            tags.add('connected')
        if _space_has(domain, 'path_connected'):
            tags.add('path_connected')
        if _space_has(domain, 'lindelof'):
            tags.add('lindelof')
        if _space_has(domain, 'separable'):
            tags.add('separable')
    if analyze_infinite_map_property(map_obj, 'surjective').is_true:
        tags.add('realized_as_codomain')

    metadata.setdefault('description', f'Image of the map {getattr(map_obj, "name", "f")}.')
    metadata.setdefault('construction', 'image')
    metadata.setdefault('map_name', getattr(map_obj, 'name', 'f'))
    return InfiniteTopologicalSpace(carrier=getattr(codomain, 'carrier', None), metadata={**getattr(codomain, 'metadata', {}), **metadata, 'tags': sorted(tags)}, tags=tags)


def preimage_subset(map_obj: SymbolicMap, subset: SymbolicSubset, *, metadata: dict[str, Any] | None = None) -> SymbolicSubset:
    metadata = dict(metadata or {})
    tags = set()
    if analyze_infinite_map_property(map_obj, 'continuous').is_true:
        if subset.has_tag('open'):
            tags.add('open')
        if subset.has_tag('closed'):
            tags.add('closed')
    metadata.setdefault('description', f'Preimage of subset {subset.label!r} under {getattr(map_obj, "name", "f")}.')
    metadata.setdefault('construction', 'preimage')
    metadata.setdefault('map_name', getattr(map_obj, 'name', 'f'))
    return SymbolicSubset(ambient=getattr(map_obj, 'domain', None), label=f'{getattr(map_obj, "name", "f")}^(-1)({subset.label})', metadata={**metadata, 'tags': sorted(tags)}, tags=tags)


def image_subset(map_obj: SymbolicMap, subset: SymbolicSubset, *, metadata: dict[str, Any] | None = None) -> SymbolicSubset:
    metadata = dict(metadata or {})
    tags = set()
    if analyze_infinite_map_property(map_obj, 'continuous').is_true:
        if subset.has_tag('compact'):
            tags.add('compact')
        if subset.has_tag('connected'):
            tags.add('connected')
        if subset.has_tag('path_connected'):
            tags.add('path_connected')
    metadata.setdefault('description', f'Image of subset {subset.label!r} under {getattr(map_obj, "name", "f")}.')
    metadata.setdefault('construction', 'image_subset')
    metadata.setdefault('map_name', getattr(map_obj, 'name', 'f'))
    return SymbolicSubset(ambient=getattr(map_obj, 'codomain', None), label=f'{getattr(map_obj, "name", "f")}({subset.label})', metadata={**metadata, 'tags': sorted(tags)}, tags=tags)


def compact_image_result(map_obj: SymbolicMap):
    image = image_space(map_obj)
    if 'compact' in image.tags:
        from .result import Result
        return Result.true(
            mode='theorem',
            value='compact',
            justification=['The continuous image of a compact space is compact.'],
            proof_outline=['Pull back an open cover along the map and use compactness of the domain.'],
            metadata={'map_name': getattr(map_obj, 'name', 'f')},
        )
    from .result import Result
    return Result.unknown(mode='symbolic', value='compact', justification=['Compactness of the image is not determined from the available data.'])


def connected_image_result(map_obj: SymbolicMap):
    image = image_space(map_obj)
    if 'connected' in image.tags:
        from .result import Result
        return Result.true(
            mode='theorem',
            value='connected',
            justification=['The continuous image of a connected space is connected.'],
            proof_outline=['A separation of the image would pull back to a separation of the domain.'],
            metadata={'map_name': getattr(map_obj, 'name', 'f')},
        )
    from .result import Result
    return Result.unknown(mode='symbolic', value='connected', justification=['Connectedness of the image is not determined from the available data.'])


def _space_has(space: Any, tag: str) -> bool:
    return str(tag).strip().lower() in getattr(space, 'tags', set())


__all__ = [
    'SymbolicSubset',
    'image_space',
    'preimage_subset',
    'image_subset',
    'compact_image_result',
    'connected_image_result',
]
