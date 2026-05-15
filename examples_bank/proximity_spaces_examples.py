"""Project-local examples for proximity spaces.

The records are deliberately compact and original to the pytop package. They
provide executable anchors for the proximity API without copying textbook
example text.
"""
from __future__ import annotations

from typing import Any

from pytop.proximity_spaces import is_close, is_proximity_space, smirnov_compactification

VERSION = "0.3.89"

def example_metric_proximity() -> dict[str, Any]:
    """Return a small metric-proximity descriptor with an explicit closeness map."""
    return {
        "key": "metric-proximity-three-point",
        "space_type": "Metric Proximity",
        "carrier": ("a", "b", "c"),
        "tags": ("metric_proximity", "proximity_space"),
        "is_proximity_space": True,
        "closeness_map": {
            ("{a}", "{a,b}"): True,
            ("{a}", "{c}"): False,
            ("{b}", "{a,b}"): True,
        },
        "learning_signal": "closeness may be tested by the API before discussing compactification language",
    }

def example_discrete_proximity() -> dict[str, Any]:
    """Return a finite discrete-proximity descriptor."""
    return {
        "key": "finite-discrete-proximity",
        "space_type": "Discrete Proximity",
        "carrier": ("0", "1"),
        "tags": ("proximity_space",),
        "is_proximity_space": True,
        "closeness_map": {
            ("{0}", "{0}"): True,
            ("{0}", "{1}"): False,
            ("{1}", "{1}"): True,
        },
        "learning_signal": "discrete examples separate equality-like closeness from arbitrary intersection language",
    }

def example_smirnov_descriptor() -> dict[str, Any]:
    """Return a symbolic Smirnov compactification example."""
    return {
        "key": "symbolic-smirnov-compactification",
        "space_type": "Symbolic Proximity Space",
        "tags": ("efremovich_proximity", "proximity_space"),
        "is_proximity_space": True,
        "smirnov_compactification": {
            "compactification_type": "Smirnov compactification",
            "boundary_signal": "clusters encode compatible proximity data",
        },
        "learning_signal": "compactification language is tied to proximity rather than to an arbitrary embedding",
    }

def proximity_spaces_example_catalog() -> tuple[dict[str, Any], ...]:
    """Return all proximity examples used by the support audit."""
    return (
        example_metric_proximity(),
        example_discrete_proximity(),
        example_smirnov_descriptor(),
    )

def proximity_spaces_example_api_summary() -> dict[str, object]:
    """Validate the example catalog against the proximity API."""
    records = proximity_spaces_example_catalog()
    close_checks = [is_close({"a"}, {"a", "b"}, records[0]), is_close({"0"}, {"1"}, records[1])]
    compactifications = [smirnov_compactification(record) for record in records]
    return {
        "version": VERSION,
        "record_count": len(records),
        "proximity_record_count": sum(1 for record in records if is_proximity_space(record)),
        "positive_closeness_checks": sum(1 for value in close_checks if value is True),
        "negative_closeness_checks": sum(1 for value in close_checks if value is False),
        "compactification_descriptor_count": sum(1 for item in compactifications if isinstance(item, dict)),
        "catalog_keys": tuple(record["key"] for record in records),
    }

__all__ = [
    "VERSION",
    "example_metric_proximity",
    "example_discrete_proximity",
    "example_smirnov_descriptor",
    "proximity_spaces_example_catalog",
    "proximity_spaces_example_api_summary",
]
