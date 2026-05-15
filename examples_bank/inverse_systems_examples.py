"""Project-local examples for inverse systems and inverse limits.

The examples are deliberately compact symbolic descriptors. They provide
executable anchors for the inverse-system API without copying textbook
examples or OCR-derived exercise prose.
"""
from __future__ import annotations

from typing import Any

from pytop.inverse_systems import inverse_limit, inverse_system

VERSION = "0.3.95"

def example_interval_tower() -> dict[str, Any]:
    """Return a finite tower modelling nested interval retractions."""
    system = inverse_system(["I0", "I1", "I2"], ["r01", "r12"])
    assert system is not None
    return {
        "key": "interval-retraction-tower",
        "example_type": "chain-like inverse system",
        "teaching_role": "first symbolic tower for coherent tuple language",
        "system": system,
        "limit": inverse_limit(system),
        "learning_signal": "the limit is read as coherent tuples constrained by the bonding maps",
    }

def example_cantor_binary_tower() -> dict[str, Any]:
    """Return a symbolic binary tower used for Cantor-style intuition."""
    system = inverse_system(["2^0", "2^1", "2^2", "2^3"], ["p10", "p21", "p32"])
    assert system is not None
    return {
        "key": "binary-prefix-tower",
        "example_type": "chain-like inverse system",
        "teaching_role": "prefix projection and coherent sequence intuition",
        "system": system,
        "limit": inverse_limit(system),
        "learning_signal": "compatibility across projections is the central check",
    }

def example_non_chain_diagnostic() -> dict[str, Any]:
    """Return a deliberately non-chain descriptor for audit diagnostics."""
    system = inverse_system(["X0", "X1", "X2"], ["f20"])
    assert system is not None
    return {
        "key": "non-chain-diagnostic",
        "example_type": "non-chain diagnostic inverse-system descriptor",
        "teaching_role": "warns that a descriptor can be symbolic but not chain-like",
        "system": system,
        "limit": inverse_limit(system),
        "learning_signal": "the API records the bonding-map count so students can notice the structural mismatch",
    }

def inverse_systems_example_catalog() -> tuple[dict[str, Any], ...]:
    """Return all inverse-system examples used by the INV-02 audit."""
    return (
        example_interval_tower(),
        example_cantor_binary_tower(),
        example_non_chain_diagnostic(),
    )

def inverse_systems_example_api_summary() -> dict[str, object]:
    """Validate the example catalog against the inverse-system API."""
    records = inverse_systems_example_catalog()
    systems = [record["system"] for record in records]
    limits = [record["limit"] for record in records]
    return {
        "version": VERSION,
        "record_count": len(records),
        "inverse_system_record_count": sum(1 for system in systems if isinstance(system, dict) and system.get("system_type") == "inverse_system"),
        "inverse_limit_descriptor_count": sum(1 for limit in limits if isinstance(limit, dict) and limit.get("limit_type") == "inverse_limit"),
        "chain_like_record_count": sum(1 for system in systems if system.get("is_chain_like") is True),
        "non_chain_record_count": sum(1 for system in systems if system.get("is_chain_like") is False),
        "catalog_keys": tuple(record["key"] for record in records),
        "learning_signals": tuple(record["learning_signal"] for record in records),
    }

__all__ = [
    "VERSION",
    "example_interval_tower",
    "example_cantor_binary_tower",
    "example_non_chain_diagnostic",
    "inverse_systems_example_catalog",
    "inverse_systems_example_api_summary",
]
