"""Inverse-system and inverse-limit framework.

Provides:
  - ``InverseSystemDescriptor``     — structured descriptor for an inverse system
  - ``compute_limit_properties``    — infer limit-space properties from component tags
  - ``inverse_system``              — backward-compatible dict constructor
  - ``inverse_limit``               — backward-compatible limit dict constructor
  - ``pro_finite_completion``       — pro-finite completion descriptor
  - ``solenoid_example``            — dyadic solenoid inverse-limit example
  - ``p_adic_integers_example``     — p-adic integers as inverse limit of Z/p^n Z

Key theorems implemented:
  - Inverse limit of compact Hausdorff spaces (surjective bonding maps) is compact Hausdorff.
  - Inverse limit of connected spaces (surjective bonding maps) is connected.
  - Inverse limit of T_n spaces is T_n (n ≤ 4).
  - Inverse limit of metrizable second-countable spaces is metrizable second-countable.
  - Pro-finite completion of a discrete group is compact, totally disconnected, Hausdorff.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

VERSION = "0.2.0"

# ---------------------------------------------------------------------------
# Descriptor
# ---------------------------------------------------------------------------

@dataclass
class InverseSystemDescriptor:
    """Structured descriptor for a finite or symbolic inverse system.

    Parameters
    ----------
    spaces:
        List of space descriptors (dicts with 'tags' key, or tag strings).
    bonding_maps:
        List of bonding map descriptors (dicts with 'tags', or tag strings).
        A bonding map f_{ij}: X_j -> X_i (j > i in the directed index set).
    index_type:
        'chain' (totally ordered) or 'directed' (general directed set).
    name:
        Optional human-readable name for the system.
    """

    spaces: list[Any]
    bonding_maps: list[Any]
    index_type: str = "chain"
    name: str = ""

    def __post_init__(self) -> None:
        if self.index_type not in ("chain", "directed"):
            self.index_type = "chain"

    @property
    def space_count(self) -> int:
        return len(self.spaces)

    @property
    def bonding_map_count(self) -> int:
        return len(self.bonding_maps)

    @property
    def is_chain_like(self) -> bool:
        return self.bonding_map_count == max(0, self.space_count - 1)

    def compute_limit_properties(self) -> dict[str, Any]:
        """Infer topological properties of the inverse limit space.

        Applies standard theorems about inverse limits to the tags of the
        component spaces and bonding maps.

        Returns
        -------
        dict with keys: tags (set), justifications (list), warnings (list)
        """
        return compute_limit_properties(self.spaces, self.bonding_maps)

    def as_dict(self) -> dict[str, Any]:
        props = self.compute_limit_properties()
        return {
            "system_type": "inverse_system",
            "name": self.name,
            "spaces": [str(s) for s in self.spaces],
            "bonding_maps": [str(m) for m in self.bonding_maps],
            "space_count": self.space_count,
            "bonding_map_count": self.bonding_map_count,
            "index_type": self.index_type,
            "is_chain_like": self.is_chain_like,
            "limit_properties": props,
            "version": VERSION,
        }


# ---------------------------------------------------------------------------
# Tag extraction helpers
# ---------------------------------------------------------------------------

def _tags_of(obj: Any) -> set[str]:
    if isinstance(obj, str):
        return {obj.strip().lower()}
    if isinstance(obj, set):
        return {str(t).strip().lower() for t in obj}
    if isinstance(obj, dict):
        raw = obj.get("tags", [])
        if isinstance(raw, (list, tuple, set, frozenset)):
            return {str(t).strip().lower() for t in raw}
        return set()
    tags = getattr(obj, "tags", set())
    if isinstance(tags, (set, frozenset, list, tuple)):
        return {str(t).strip().lower() for t in tags}
    return set()


def _all_spaces_have(spaces: list[Any], tag: str) -> bool:
    return all(tag in _tags_of(s) for s in spaces) if spaces else False


def _any_space_has(spaces: list[Any], tag: str) -> bool:
    return any(tag in _tags_of(s) for s in spaces)


def _all_maps_have(bonding_maps: list[Any], tag: str) -> bool:
    return all(tag in _tags_of(m) for m in bonding_maps) if bonding_maps else True


# ---------------------------------------------------------------------------
# Core property computation
# ---------------------------------------------------------------------------

def compute_limit_properties(
    spaces: list[Any],
    bonding_maps: list[Any],
) -> dict[str, Any]:
    """Compute the topological properties of the inverse limit.

    Parameters
    ----------
    spaces:
        Component spaces; each may be a dict with 'tags', a set of tag
        strings, or any object with a 'tags' attribute.
    bonding_maps:
        Bonding maps; same format as spaces.

    Returns
    -------
    dict with:
        tags         — set of inferred property tags for the limit space
        justifications — list of theorem-level justification strings
        warnings     — list of warnings where information was insufficient
    """
    tags: set[str] = set()
    justifications: list[str] = []
    warnings: list[str] = []

    if not spaces:
        warnings.append("No component spaces provided; limit properties unknown.")
        return {"tags": tags, "justifications": justifications, "warnings": warnings}

    maps_surjective = _all_maps_have(bonding_maps, "surjective") or not bonding_maps

    # ── Separation axioms: T_n is hereditary under inverse limits ──────────
    for axiom, label in [
        ("t0", "T0"), ("t1", "T1"), ("hausdorff", "Hausdorff"),
        ("regular", "regular"), ("t3", "T3"), ("normal", "T4"),
    ]:
        if _all_spaces_have(spaces, axiom):
            tags.add(axiom)
            justifications.append(
                f"Inverse limit inherits {label}: subspace of product of {label} spaces."
            )

    # ── Compact + Hausdorff + surjective bonding maps ───────────────────────
    if _all_spaces_have(spaces, "compact") and _all_spaces_have(spaces, "hausdorff"):
        tags.add("compact")
        tags.add("compact_hausdorff")
        if maps_surjective:
            justifications.append(
                "Inverse limit of compact Hausdorff spaces with surjective bonding maps "
                "is compact Hausdorff (closed subspace of compact Hausdorff product)."
            )
        else:
            justifications.append(
                "Inverse limit of compact Hausdorff spaces is compact Hausdorff "
                "(as a closed subspace of the compact Hausdorff product)."
            )

    # ── Connected: requires surjective bonding maps ─────────────────────────
    if _all_spaces_have(spaces, "connected"):
        if maps_surjective:
            tags.add("connected")
            justifications.append(
                "Inverse limit of connected spaces with surjective bonding maps is connected."
            )
        else:
            warnings.append(
                "Component spaces are connected but bonding maps are not tagged 'surjective'; "
                "connectedness of the limit cannot be guaranteed."
            )

    # ── Totally disconnected (pro-finite structure) ──────────────────────────
    if _all_spaces_have(spaces, "totally_disconnected") or _all_spaces_have(spaces, "discrete"):
        tags.add("totally_disconnected")
        justifications.append(
            "Inverse limit of totally disconnected spaces is totally disconnected."
        )
        if "compact" in tags and "hausdorff" in tags:
            tags.add("profinite")
            justifications.append(
                "Compact Hausdorff totally disconnected space = pro-finite space."
            )

    # ── Metrizable + second-countable ────────────────────────────────────────
    if _all_spaces_have(spaces, "metrizable") or _all_spaces_have(spaces, "metric"):
        if _all_spaces_have(spaces, "second_countable") or (
            len(spaces) <= 1 or _all_spaces_have(spaces, "second_countable")
        ):
            # Countable inverse system of metrizable second-countable spaces
            tags.add("metrizable")
            tags.add("second_countable")
            justifications.append(
                "Countable inverse limit of metrizable second-countable spaces "
                "is metrizable second-countable (Urysohn metrization + limit topology)."
            )
        else:
            tags.add("metrizable")
            justifications.append(
                "Inverse limit of metrizable spaces is metrizable "
                "(subspace of metrizable product)."
            )

    # ── Path-connected: NOT preserved by inverse limits in general ───────────
    if _all_spaces_have(spaces, "path_connected"):
        warnings.append(
            "Path-connectedness is NOT generally preserved by inverse limits "
            "(solenoid is connected but not path-connected)."
        )

    # ── Non-empty: if all spaces non-empty and maps surjective ───────────────
    if maps_surjective:
        tags.add("nonempty")
        justifications.append(
            "Surjective bonding maps guarantee a non-empty inverse limit "
            "(by the axiom of choice / König's lemma for countable chains)."
        )

    return {"tags": tags, "justifications": justifications, "warnings": warnings}


# ---------------------------------------------------------------------------
# Backward-compatible dict API
# ---------------------------------------------------------------------------

def inverse_system(spaces: Any, bonding_maps: Any) -> dict | None:
    """Construct a symbolic inverse-system descriptor."""
    if not isinstance(spaces, (list, tuple)) or not isinstance(bonding_maps, (list, tuple)):
        return None
    spaces_list = list(spaces)
    maps_list = list(bonding_maps)
    descriptor = InverseSystemDescriptor(spaces=spaces_list, bonding_maps=maps_list)
    return descriptor.as_dict()


def inverse_limit(inv_sys: Any) -> dict | None:
    """Return a symbolic inverse-limit descriptor with inferred properties."""
    if not isinstance(inv_sys, dict):
        return None
    if inv_sys.get("system_type") != "inverse_system":
        return None
    spaces_raw = inv_sys.get("spaces", [])
    maps_raw = inv_sys.get("bonding_maps", [])
    if not isinstance(spaces_raw, (list, tuple)) or not isinstance(maps_raw, (list, tuple)):
        return None

    props = compute_limit_properties(list(spaces_raw), list(maps_raw))

    return {
        "limit_type": "inverse_limit",
        "source_system_version": inv_sys.get("version"),
        "space_count": len(spaces_raw),
        "bonding_map_count": len(maps_raw),
        "compatibility_rule": "f_ij(x_j) = x_i across the bonding maps",
        "carrier_hint": "coherent tuples in the ambient product",
        "inferred_tags": sorted(props["tags"]),
        "justifications": props["justifications"],
        "warnings": props["warnings"],
        "version": VERSION,
    }


# ---------------------------------------------------------------------------
# Pro-finite completion
# ---------------------------------------------------------------------------

def pro_finite_completion(space: Any) -> dict[str, Any]:
    """Describe the pro-finite completion of *space*.

    A pro-finite completion is the inverse limit of all finite discrete
    quotients.  It is automatically compact, Hausdorff, and totally disconnected.

    Parameters
    ----------
    space:
        Any object with tags or a dict.  Used only for metadata; the
        completion is described symbolically.

    Returns
    -------
    dict with keys: description, tags, properties, examples, version
    """
    space_tags = _tags_of(space)
    name = (
        getattr(space, "carrier", None)
        or (space.get("name") if isinstance(space, dict) else None)
        or "X"
    )
    tags = {"compact", "hausdorff", "totally_disconnected", "profinite", "t1", "t0"}

    if "abelian" in space_tags or "group" in space_tags:
        tags.add("topological_group")
        description = (
            f"Pro-finite completion of {name}: inverse limit of all finite discrete "
            "quotients. For groups: the profinite completion Ĝ = lim_{←} G/N "
            "(N normal, finite index). Canonical examples: ℤ̂ = ∏_p ℤ_p."
        )
    else:
        description = (
            f"Pro-finite completion of {name}: inverse limit of all finite discrete "
            "quotient spaces. Compact, Hausdorff, totally disconnected."
        )

    return {
        "description": description,
        "space": str(name),
        "tags": sorted(tags),
        "properties": {
            "compact": True,
            "hausdorff": True,
            "totally_disconnected": True,
            "profinite": True,
            "connected": False,
            "path_connected": False,
        },
        "examples": [
            "ℤ̂ (profinite integers) = lim_{←} ℤ/nℤ = ∏_p ℤ_p",
            "Absolute Galois group Gal(Q̄/Q) as profinite group",
            "p-adic integers ℤ_p = lim_{←} ℤ/p^n ℤ",
        ],
        "version": VERSION,
    }


# ---------------------------------------------------------------------------
# Standard examples
# ---------------------------------------------------------------------------

def solenoid_example() -> dict[str, Any]:
    """Return a descriptor for the dyadic solenoid as an inverse limit.

    The dyadic solenoid Σ = lim_{←} (S¹ →^{×2} S¹ →^{×2} S¹ → ...)
    is compact, connected, Hausdorff, metrizable, but NOT path-connected.
    """
    component_spaces = [{"tags": ["compact", "connected", "hausdorff", "metrizable", "path_connected"]}] * 3
    bonding_map_tags = [{"tags": ["surjective", "continuous"]}] * 2
    props = compute_limit_properties(component_spaces, bonding_map_tags)

    return {
        "name": "Dyadic Solenoid",
        "description": (
            "Σ = lim_{←} (S¹ →^{×2} S¹ →^{×2} ...): "
            "bonding map is z ↦ z² on the circle S¹ ⊂ ℂ."
        ),
        "component_spaces": "S¹ (circle) repeated",
        "bonding_maps": "degree-2 covering maps z ↦ z²",
        "inferred_tags": sorted(props["tags"]),
        "path_connected": False,
        "path_connected_note": (
            "Path-connectedness is NOT preserved: Σ is connected but not path-connected. "
            "Every path-component is a dense copy of ℝ."
        ),
        "warnings": props["warnings"],
        "version": VERSION,
    }


def p_adic_integers_example(p: int = 2) -> dict[str, Any]:
    """Return a descriptor for the p-adic integers ℤ_p as an inverse limit.

    ℤ_p = lim_{←} (... → ℤ/p³ℤ → ℤ/p²ℤ → ℤ/pℤ)

    Compact, Hausdorff, totally disconnected, metrizable (ultrametric).
    """
    if not (isinstance(p, int) and p >= 2):
        p = 2
    component_spaces = [
        {"tags": ["compact", "hausdorff", "totally_disconnected", "discrete", "metrizable"]}
    ] * 4
    bonding_map_tags = [{"tags": ["surjective", "continuous"]}] * 3
    props = compute_limit_properties(component_spaces, bonding_map_tags)

    return {
        "name": f"p-adic integers ℤ_{p}",
        "description": (
            f"ℤ_{p} = lim_{{←}} ℤ/p^n ℤ: "
            f"inverse limit of cyclic groups Z/{p}^n Z with canonical projections."
        ),
        "component_spaces": f"ℤ/p^n ℤ (n=1,2,3,...) with discrete topology",
        "bonding_maps": "canonical reduction mod p^n",
        "inferred_tags": sorted(props["tags"]),
        "ultrametric": True,
        "version": VERSION,
    }


__all__ = [
    "InverseSystemDescriptor",
    "compute_limit_properties",
    "inverse_system",
    "inverse_limit",
    "pro_finite_completion",
    "solenoid_example",
    "p_adic_integers_example",
]
