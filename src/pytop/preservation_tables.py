"""Preservation and invariance table helpers.

This module now carries two distinct historical surfaces:

- the richer v0.1.64 teaching/research table helpers that much of the
  package still imports directly,
- the v0.1.99 query helpers, now upgraded to return real benchmark booleans
  for continuous-image and arbitrary-product preservation.
"""

from __future__ import annotations

from typing import Any

from .result import Result


class PreservationError(Exception):
    """Raised when a preservation-table query cannot be resolved."""


_CONTEXTS = [
    "arbitrary_subspace",
    "closed_subspace",
    "open_subspace",
    "finite_product",
    "arbitrary_product",
    "quotient",
    "continuous_image",
    "homeomorphism",
]

_KNOWN_PROPERTIES = (
    "compactness",
    "hausdorff",
    "lindelof",
    "paracompactness",
    "metrizability",
    "normality",
    "connectedness",
)

_TABLE_DATA: dict[str, dict[str, Any]] = {
    "compactness": {
        "rows": {
            "arbitrary_subspace": "No in general.",
            "closed_subspace": "Yes for closed subspaces of compact spaces.",
            "open_subspace": "No in general.",
            "finite_product": "Yes.",
            "arbitrary_product": "Yes by Tychonoff.",
            "quotient": "Yes.",
            "continuous_image": "Yes.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "The interval (0,1) inside [0,1] is open but not compact.",
    },
    "hausdorff": {
        "rows": {
            "arbitrary_subspace": "Yes.",
            "closed_subspace": "Yes.",
            "open_subspace": "Yes.",
            "finite_product": "Yes.",
            "arbitrary_product": "Yes.",
            "quotient": "No in general.",
            "continuous_image": "No in general.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "A quotient that identifies all of [0,1] to one point destroys Hausdorff separation.",
    },
    "lindelof": {
        "rows": {
            "arbitrary_subspace": "No in general.",
            "closed_subspace": "Yes.",
            "open_subspace": "Yes in regular common examples, but not as a blanket theorem here.",
            "finite_product": "No in general.",
            "arbitrary_product": "No in general.",
            "quotient": "Yes.",
            "continuous_image": "Yes.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "The Sorgenfrey plane witnesses product failure phenomena for Lindelof-type properties.",
    },
    "paracompactness": {
        "rows": {
            "arbitrary_subspace": "No in general.",
            "closed_subspace": "Yes.",
            "open_subspace": "Yes.",
            "finite_product": "No in general.",
            "arbitrary_product": "No in general.",
            "quotient": "No in general.",
            "continuous_image": "No in general.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "The Sorgenfrey plane is a classical warning for product behavior.",
    },
    "metrizability": {
        "rows": {
            "arbitrary_subspace": "Yes.",
            "closed_subspace": "Yes.",
            "open_subspace": "Yes.",
            "finite_product": "Yes.",
            "arbitrary_product": "No in general.",
            "quotient": "No in general.",
            "continuous_image": "No in general.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "Quotients of metric spaces need not remain metrizable.",
    },
    "normality": {
        "rows": {
            "arbitrary_subspace": "No in general.",
            "closed_subspace": "Yes.",
            "open_subspace": "Yes.",
            "finite_product": "No in general.",
            "arbitrary_product": "No in general.",
            "quotient": "No in general.",
            "continuous_image": "No in general.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "The Sorgenfrey plane is not normal although each factor is.",
    },
    "connectedness": {
        "rows": {
            "arbitrary_subspace": "No in general.",
            "closed_subspace": "No in general.",
            "open_subspace": "No in general.",
            "finite_product": "Yes.",
            "arbitrary_product": "Yes.",
            "quotient": "Yes.",
            "continuous_image": "Yes.",
            "homeomorphism": "Yes.",
        },
        "counterexample": "A connected interval can contain disconnected subspaces such as two separated points.",
    },
}

_LEGACY_CONTEXT_ALIASES = {
    "subspace": "arbitrary_subspace",
    "arbitrary_subspace": "arbitrary_subspace",
    "closed_subspace": "closed_subspace",
    "open_subspace": "open_subspace",
    "finite_product": "finite_product",
    "arbitrary_product": "arbitrary_product",
    "countable_product": "arbitrary_product",
    "quotient": "quotient",
    "continuous_image": "continuous_image",
    "homeomorphism": "homeomorphism",
}


def _normalize_property(property_name: str) -> str:
    key = str(property_name).strip().lower().replace("-", "_").replace(" ", "_")
    if key not in _TABLE_DATA:
        raise PreservationError(f"Unknown property: {property_name!r}")
    return key


def _normalize_context(context: str) -> str:
    key = str(context).strip().lower().replace("-", "_").replace(" ", "_")
    if key not in _LEGACY_CONTEXT_ALIASES:
        raise PreservationError(f"Unknown construction/context: {context!r}")
    return _LEGACY_CONTEXT_ALIASES[key]


def _row_list(property_name: str) -> list[dict[str, str]]:
    prop = _normalize_property(property_name)
    return [
        {"context": context, "verdict": _TABLE_DATA[prop]["rows"][context]}
        for context in _CONTEXTS
    ]


def _verdict_to_bool(property_name: str, context: str) -> bool:
    prop = _normalize_property(property_name)
    normalized = _normalize_context(context)
    verdict = _TABLE_DATA[prop]["rows"][normalized].lower()
    if verdict.startswith("yes"):
        return True
    if verdict.startswith("no"):
        return False
    raise PreservationError(
        f"The verdict for property={prop!r}, context={normalized!r} is not boolean-like."
    )


def preservation_table(property_name: str) -> dict[str, Any]:
    prop = _normalize_property(property_name)
    return {
        "property": prop,
        "rows": _row_list(prop),
        "counterexample": _TABLE_DATA[prop]["counterexample"],
        "always_invariant": True,
        "known_property": True,
        "version": "0.1.64",
    }


def preservation_table_lookup(property_name: str, construction: str) -> bool:
    return _verdict_to_bool(property_name, construction)


def preservation_table_row(property_name: str) -> list[dict[str, str]]:
    return _row_list(property_name)


def preservation_table_column(construction: str) -> list[dict[str, str]]:
    normalized = _normalize_context(construction)
    return [
        {
            "property": prop,
            "context": normalized,
            "verdict": _TABLE_DATA[prop]["rows"][normalized],
        }
        for prop in _KNOWN_PROPERTIES
    ]


def analyze_preservation_table(property_name: str) -> dict[str, Any]:
    prop = _normalize_property(property_name)
    summary = {
        "property": prop,
        "counterexample": _TABLE_DATA[prop]["counterexample"],
        "version": "0.1.64",
    }
    for context in ("continuous_image", "closed_subspace", "open_subspace"):
        summary[context] = preservation_table_lookup(prop, context)
    return summary


def invariance_profile(space: Any) -> dict[str, Any]:
    representation = getattr(space, "representation", "symbolic_general")
    return {
        "representation": representation,
        "topological_invariants": [
            "compactness",
            "connectedness",
            "path_connectedness",
            "hausdorff",
            "t1",
            "normality",
            "regularity",
            "first_countability",
            "second_countability",
            "metrizability",
            "lindelof",
        ],
        "preservation_summary": {
            "best_behaved": ["compactness", "connectedness", "hausdorff"],
            "tricky_products": ["lindelof", "paracompactness", "normality"],
            "continuous_image_yes": ["compactness", "connectedness", "lindelof"],
            "continuous_image_no": ["hausdorff", "metrizability", "normality"],
        },
        "difficult_cases": [
            "Sorgenfrey line vs product behavior",
            "Michael line style counterexamples",
            "Quotients that break Hausdorff separation",
            "Arbitrary products and Tychonoff-level subtleties",
        ],
        "version": "0.1.64",
    }


def analyze_preservation(property_name: str) -> Result:
    table = preservation_table(property_name)
    return Result.true(
        mode="theorem",
        value=table,
        justification=[
            "The preservation table records this property across standard constructions.",
            "Homeomorphism invariance is treated as unconditional in this surface.",
            "Product, quotient, and image behavior are summarized in theorem-style rows.",
            "Named counterexamples are attached for the non-preserved contexts.",
        ],
        metadata={
            "property": table["property"],
            "always_invariant": table["always_invariant"],
            "version": table["version"],
        },
    )


def get_preservation_by_continuous_maps(property_name):
    """
    Returns whether the given topological property is preserved under continuous maps.
    For instance, 'compactness' -> True, 'Hausdorff' -> False.
    """
    return _verdict_to_bool(property_name, "continuous_image")


def get_preservation_by_products(property_name):
    """
    Returns whether the given topological property is preserved under arbitrary products.
    For instance, 'compactness' -> True (Tychonoff), 'first_countability' -> False.
    """
    return _verdict_to_bool(property_name, "arbitrary_product")


__all__ = [
    "PreservationError",
    "preservation_table",
    "preservation_table_lookup",
    "preservation_table_row",
    "preservation_table_column",
    "analyze_preservation_table",
    "invariance_profile",
    "analyze_preservation",
    "get_preservation_by_continuous_maps",
    "get_preservation_by_products",
]
