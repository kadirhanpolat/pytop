"""Preservation analysis for standard topological constructions.

This module provides a compact bridge between map-level information and the
space-level theorem engine. It does not attempt a full preservation theory.
Instead, it covers a small family of high-value statements with structured
results:

- compactness under continuous images
- connectedness under continuous images
- compactness for closed subspaces of compact spaces
- Hausdorff and T1 inheritance to subspaces
"""

from __future__ import annotations

from typing import Any

from .compactness import is_compact
from .connectedness import is_connected
from .maps import analyze_map_property, satisfies_closure_image_inclusion
from .result import Result
from .theorem_engine import infer_feature


def compact_under_continuous_image(map_obj: Any) -> Result:
    domain = getattr(map_obj, "domain", None)
    domain_tags = _extract_tags(domain)
    continuity = analyze_map_property(map_obj, "continuous")
    domain_compact = is_compact(domain) if domain is not None else Result.unknown(mode="symbolic")
    if continuity.is_false:
        return Result.false(
            mode=continuity.mode,
            value="compact",
            justification=["The map is known not to be continuous, so the standard compact-image theorem does not apply."],
            metadata={"preservation": "continuous_image_of_compact_is_compact"},
        )
    if continuity.is_true and ("compact" in domain_tags or domain_compact.is_true):
        image_descriptor = {
            "representation": _representation_of(getattr(map_obj, "codomain", None)),
            "tags": ["continuous_image", "domain_compact", *sorted(_extract_tags(getattr(map_obj, "codomain", None)))],
        }
        theorem = infer_feature("compact", image_descriptor)
        theorem.metadata.setdefault("preservation", "continuous_image_of_compact_is_compact")
        return theorem
    return Result.unknown(
        mode="symbolic",
        value="compact",
        justification=["Compactness of the domain or continuity of the map was not established strongly enough."],
        proof_outline=[
            "Show that the map is continuous.",
            "Show that the domain is compact.",
            "Then apply preservation under continuous images.",
        ],
        metadata={"preservation": "continuous_image_of_compact_is_compact"},
    )



def connected_under_continuous_image(map_obj: Any) -> Result:
    domain = getattr(map_obj, "domain", None)
    domain_tags = _extract_tags(domain)
    continuity = analyze_map_property(map_obj, "continuous")
    domain_connected = is_connected(domain) if domain is not None else Result.unknown(mode="symbolic")
    if continuity.is_false:
        return Result.false(
            mode=continuity.mode,
            value="connected",
            justification=["The map is known not to be continuous, so the standard connected-image theorem does not apply."],
            metadata={"preservation": "continuous_image_of_connected_is_connected"},
        )
    if continuity.is_true and ("connected" in domain_tags or domain_connected.is_true):
        return Result.true(
            mode="theorem",
            value="connected",
            assumptions=["The map is continuous and the domain is connected."],
            justification=["The continuous image of a connected space is connected."],
            proof_outline=[
                "Assume the image were disconnected.",
                "Pull the disconnection back along the continuous map.",
                "This contradicts connectedness of the domain.",
            ],
            metadata={"preservation": "continuous_image_of_connected_is_connected"},
        )
    return Result.unknown(
        mode="symbolic",
        value="connected",
        justification=["Connectedness of the domain or continuity of the map was not established strongly enough."],
        metadata={"preservation": "continuous_image_of_connected_is_connected"},
    )



def compact_closed_subspace(subspace_obj: Any) -> Result:
    tags = _extract_tags(subspace_obj)
    if "closed_subspace" in tags and "ambient_compact" in tags:
        theorem = infer_feature("compact", {"representation": _representation_of(subspace_obj), "tags": sorted(tags)})
        theorem.metadata.setdefault("preservation", "closed_subspace_of_compact_is_compact")
        return theorem
    if "closed_subspace" in tags and "compact" in tags:
        return Result.true(
            mode="mixed",
            value="compact",
            justification=["The object already carries both closed-subspace and compact tags."],
            metadata={"preservation": "closed_subspace_of_compact_is_compact"},
        )
    return Result.unknown(
        mode="symbolic",
        value="compact",
        justification=["Closedness of the subspace or compactness of the ambient space was not encoded."],
        metadata={"preservation": "closed_subspace_of_compact_is_compact"},
    )



def separation_inherited_by_subspace(subspace_obj: Any, feature: str = "hausdorff") -> Result:
    normalized = _normalize_separation_feature(feature)
    tags = _extract_tags(subspace_obj)
    if f"not_{normalized}" in tags:
        return Result.false(
            mode="symbolic",
            value=normalized,
            justification=[f"The subspace carries an explicit negative tag for {normalized}."],
            metadata={"preservation": "subspace_inheritance", "feature": normalized},
        )
    if normalized in tags:
        return Result.true(
            mode="mixed",
            value=normalized,
            justification=[f"The subspace already carries the inherited separation tag {normalized}."],
            metadata={"preservation": "subspace_inheritance", "feature": normalized},
        )
    if "subspace" in tags or "closed_subspace" in tags or "open_subspace" in tags:
        ambient_tag = f"ambient_{normalized}"
        if ambient_tag in tags:
            return Result.true(
                mode="theorem",
                value=normalized,
                assumptions=[f"The ambient space is {normalized.replace('_', ' ')}."],
                justification=[f"Subspaces of {normalized.replace('_', ' ')} spaces remain {normalized.replace('_', ' ')}."],
                metadata={"preservation": "subspace_inheritance", "feature": normalized},
            )
    return Result.unknown(
        mode="symbolic",
        value=normalized,
        justification=["No decisive inherited separation data was available."],
        metadata={"preservation": "subspace_inheritance", "feature": normalized},
    )





def homeomorphic_invariant_transfer(map_obj: Any, feature: str) -> Result:
    normalized = str(feature).strip().lower().replace('-', '_').replace(' ', '_')
    supported = {'compact', 'connected', 't0', 't1', 'hausdorff'}
    if normalized not in supported:
        return Result.unknown(
            mode='symbolic',
            value=normalized,
            justification=['This helper currently tracks only a small core family of standard topological invariants.'],
            metadata={'preservation': 'homeomorphic_invariant_transfer', 'feature': normalized},
        )
    homeo = analyze_map_property(map_obj, 'homeomorphism')
    if homeo.is_false:
        return Result.false(
            mode=homeo.mode,
            value=normalized,
            justification=['The map is known not to be a homeomorphism, so invariant transfer along homeomorphic equivalence does not apply.'],
            metadata={'preservation': 'homeomorphic_invariant_transfer', 'feature': normalized},
        )
    if homeo.is_true:
        return Result.true(
            mode='theorem',
            value=normalized,
            assumptions=['The map is a homeomorphism.'],
            justification=['Standard topological invariants are preserved under homeomorphism.'],
            proof_outline=['Transport the defining open-set statement (or its equivalent formulation) along the homeomorphism.'],
            metadata={'preservation': 'homeomorphic_invariant_transfer', 'feature': normalized},
        )
    return Result.unknown(
        mode='symbolic',
        value=normalized,
        justification=['Invariant transfer requires first establishing that the map is a homeomorphism.'],
        metadata={'preservation': 'homeomorphic_invariant_transfer', 'feature': normalized},
    )



def closure_image_behavior(map_obj: Any, subset: Any) -> Result:
    result = satisfies_closure_image_inclusion(map_obj, subset)
    result.metadata.setdefault('preservation', 'closure_image_behavior')
    return result

def analyze_preservation(context: str, obj: Any, feature: str | None = None) -> Result:
    normalized = str(context).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in {"compact_under_continuous_image", "continuous_image_compact"}:
        return compact_under_continuous_image(obj)
    if normalized in {"connected_under_continuous_image", "continuous_image_connected"}:
        return connected_under_continuous_image(obj)
    if normalized in {"compact_closed_subspace", "closed_subspace_compact"}:
        return compact_closed_subspace(obj)
    if normalized in {"subspace_separation", "separation_inherited_by_subspace"}:
        return separation_inherited_by_subspace(obj, feature or "hausdorff")
    if normalized in {"homeomorphic_invariant", "homeomorphic_invariant_transfer"}:
        return homeomorphic_invariant_transfer(obj, feature or "connected")
    if normalized in {"closure_image_behavior", "closure_preservation"}:
        return closure_image_behavior(obj, feature)
    raise ValueError(f"Unknown preservation context {context!r}.")



def _extract_tags(obj: Any) -> set[str]:
    tags: set[str] = set()
    raw = getattr(obj, "tags", None)
    if raw is not None:
        tags.update(str(tag).strip().lower() for tag in raw if str(tag).strip())
    metadata = getattr(obj, "metadata", None)
    if isinstance(metadata, dict):
        tags.update(str(tag).strip().lower() for tag in metadata.get("tags", []) if str(tag).strip())
    if isinstance(obj, dict):
        tags.update(str(tag).strip().lower() for tag in obj.get("tags", []) if str(tag).strip())
    return tags



def _representation_of(obj: Any) -> str:
    metadata = getattr(obj, "metadata", None)
    if isinstance(metadata, dict) and metadata.get("representation"):
        return str(metadata["representation"]).strip().lower()
    return "symbolic_general"



def _normalize_separation_feature(feature: str) -> str:
    text = str(feature).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {"t2": "hausdorff", "kolmogorov": "t0"}
    text = aliases.get(text, text)
    if text not in {"t0", "t1", "hausdorff"}:
        raise ValueError("Expected one of 't0', 't1', or 'hausdorff'.")
    return text


__all__ = [
    "analyze_preservation",
    "compact_under_continuous_image",
    "connected_under_continuous_image",
    "compact_closed_subspace",
    "separation_inherited_by_subspace",
    "homeomorphic_invariant_transfer",
    "closure_image_behavior",
]
