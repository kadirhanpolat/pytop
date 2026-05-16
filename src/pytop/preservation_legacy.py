"""Legacy Result-based preservation table facade (v0.1.48 contract).

This module keeps the undergraduate Cilt II API stable while the richer
Cilt III ``preservation_tables`` module exposes direct table/list/dict helpers.
The functions here deliberately return ``Result`` objects.
"""

from __future__ import annotations

import warnings
from typing import Any

from .result import Result

_PROPERTY_ALIASES = {
    "compact": "compactness",
    "compactness": "compactness",
    "connected": "connectedness",
    "connectedness": "connectedness",
    "hausdorff": "hausdorff",
    "t2": "hausdorff",
    "t_2": "hausdorff",
    "t1": "t1",
    "t_1": "t1",
    "second_countable": "second_countability",
    "second_countability": "second_countability",
}

_CONSTRUCTION_ALIASES = {
    "subspace": "subspace",
    "closed_subspace": "subspace",
    "open_subspace": "subspace",
    "finite_product": "finite_product",
    "countable_product": "countable_product",
    "arbitrary_product": "countable_product",
    "quotient": "quotient",
    "continuous_image": "continuous_image",
    "image": "continuous_image",
}

_TABLE: dict[str, dict[str, Any]] = {
    "connectedness": {
        "subspace": False,
        "finite_product": True,
        "countable_product": True,
        "quotient": True,
        "continuous_image": True,
    },
    "compactness": {
        "subspace": "conditional",
        "finite_product": True,
        "countable_product": True,
        "quotient": True,
        "continuous_image": True,
    },
    "hausdorff": {
        "subspace": True,
        "finite_product": True,
        "countable_product": True,
        "quotient": False,
        "continuous_image": False,
    },
    "t1": {
        "subspace": True,
        "finite_product": True,
        "countable_product": True,
        "quotient": False,
        "continuous_image": False,
    },
    "second_countability": {
        "subspace": True,
        "finite_product": True,
        "countable_product": True,
        "quotient": False,
        "continuous_image": False,
    },
}


def _normalize_property(property_name: str) -> str:
    key = str(property_name).strip().lower().replace(" ", "_").replace("-", "_")
    if key not in _PROPERTY_ALIASES:
        raise ValueError(f"Unknown preservation-table property: {property_name!r}")
    return _PROPERTY_ALIASES[key]


def _normalize_construction(construction: str) -> str:
    key = str(construction).strip().lower().replace(" ", "_").replace("-", "_")
    if key not in _CONSTRUCTION_ALIASES:
        raise ValueError(f"Unknown preservation-table construction: {construction!r}")
    return _CONSTRUCTION_ALIASES[key]


def _result_for_value(value: Any, *, property_name: str, construction: str) -> Result:
    metadata = {
        "property": property_name,
        "construction": construction,
        "v0_1_48_corridor_record": True,
    }
    if value is True:
        return Result.true(
            mode="exact",
            value=True,
            justification=["Recorded in the v0.1.48 basic preservation table."],
            metadata=metadata,
        )
    if value is False:
        return Result.false(
            mode="exact",
            value=False,
            justification=["Recorded as not preserved in general in the v0.1.48 basic preservation table."],
            metadata=metadata,
        )
    return Result(
        status="conditional",
        mode="exact",
        value=value,
        justification=["The v0.1.48 basic preservation table records this case as conditional."],
        metadata={**metadata, "condition_required": True},
    )


def preservation_table_lookup(property_name: str, construction: str) -> Result:
    warnings.warn(
        "preservation_table_lookup is deprecated; use preservation_tables.preservation_table() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    prop = _normalize_property(property_name)
    cons = _normalize_construction(construction)
    return _result_for_value(_TABLE[prop][cons], property_name=prop, construction=cons)


def preservation_table_row(property_name: str) -> Result:
    warnings.warn(
        "preservation_table_row is deprecated; use preservation_tables.preservation_table() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    prop = _normalize_property(property_name)
    return Result.true(
        mode="exact",
        value=dict(_TABLE[prop]),
        justification=["v0.1.48 basic preservation table row."],
        metadata={"property": prop, "v0_1_48_corridor_record": True},
    )


def preservation_table_column(construction: str) -> Result:
    warnings.warn(
        "preservation_table_column is deprecated; use preservation_tables.preservation_table() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    cons = _normalize_construction(construction)
    return Result.true(
        mode="exact",
        value={prop: row[cons] for prop, row in _TABLE.items()},
        justification=["v0.1.48 basic preservation table column."],
        metadata={"construction": cons, "v0_1_48_corridor_record": True},
    )


def analyze_preservation_table(property_name: str | None = None, construction: str | None = None) -> Result:
    warnings.warn(
        "analyze_preservation_table is deprecated; use preservation_tables.preservation_table() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    if property_name is not None and construction is not None:
        return preservation_table_lookup(property_name, construction)
    if property_name is not None:
        return preservation_table_row(property_name)
    if construction is not None:
        return preservation_table_column(construction)
    return Result.true(
        mode="exact",
        value={prop: dict(row) for prop, row in _TABLE.items()},
        justification=["Full v0.1.48 basic preservation table."],
        metadata={"v0_1_48_corridor_record": True},
    )


__all__ = [
    "preservation_table_lookup",
    "preservation_table_row",
    "preservation_table_column",
    "analyze_preservation_table",
]
