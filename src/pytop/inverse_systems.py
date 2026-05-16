"""Inverse-system benchmark helpers.

This v0.1.106 surface replaces the placeholder returns with a conservative
benchmark layer for:

- inverse-system descriptors
- inverse-limit descriptors
"""

from __future__ import annotations

VERSION = "0.1.106"


def inverse_system(spaces, bonding_maps):
    """Construct a symbolic inverse-system descriptor when explicit data is supplied."""
    if not isinstance(spaces, (list, tuple)) or not isinstance(bonding_maps, (list, tuple)):
        return None
    normalized_spaces = [str(space) for space in spaces]
    normalized_maps = [str(mapping) for mapping in bonding_maps]
    return {
        "system_type": "inverse_system",
        "spaces": normalized_spaces,
        "bonding_maps": normalized_maps,
        "space_count": len(normalized_spaces),
        "bonding_map_count": len(normalized_maps),
        "is_chain_like": len(normalized_maps) == max(0, len(normalized_spaces) - 1),
        "version": VERSION,
    }


def inverse_limit(inv_sys):
    """Return a symbolic inverse-limit descriptor when the system looks usable."""
    if not isinstance(inv_sys, dict):
        return None
    if inv_sys.get("system_type") != "inverse_system":
        return None
    spaces = inv_sys.get("spaces", [])
    bonding_maps = inv_sys.get("bonding_maps", [])
    if not isinstance(spaces, list) or not isinstance(bonding_maps, list):
        return None
    return {
        "limit_type": "inverse_limit",
        "source_system_version": inv_sys.get("version"),
        "space_count": len(spaces),
        "bonding_map_count": len(bonding_maps),
        "compatibility_rule": "f_ij(x_j) = x_i across the bonding maps",
        "carrier_hint": "coherent tuples in the ambient product",
        "version": VERSION,
    }


__all__ = [
    "inverse_system",
    "inverse_limit",
]
