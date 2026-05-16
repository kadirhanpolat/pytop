"""Metric contract helpers for finite exact and symbolic-safe workflows."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .metric_spaces import (
    FiniteMetricSpace,
    MetricSpace,
    capped_metric,
    finite_product_metric_space,
    normalized_metric,
    validate_metric,
)
from .result import Result, merge_results


@dataclass(frozen=True, slots=True)
class MetricContract:
    name: str
    status: str
    mode: str
    carrier_size: int | None = None
    metric_kind: str = "unspecified"
    assumptions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_result(self) -> Result:
        payload={**dict(self.metadata), "carrier_size": self.carrier_size, "metric_kind": self.metric_kind}
        if self.status == "true":
            return Result.true(mode=self.mode, value=self.name, assumptions=self.assumptions, justification=self.warnings or (f"metric contract {self.name!r} holds",), metadata=payload)
        if self.status == "false":
            return Result.false(mode=self.mode, value=self.name, assumptions=self.assumptions, justification=self.warnings or (f"metric contract {self.name!r} failed",), metadata=payload)
        if self.status == "conditional":
            return Result.conditional(mode=self.mode, value=self.name, assumptions=self.assumptions, justification=self.warnings or (f"metric contract {self.name!r} is conditional",), metadata=payload)
        return Result.unknown(mode=self.mode, value=self.name, assumptions=self.assumptions, justification=self.warnings or (f"metric contract {self.name!r} is unknown",), metadata=payload)


def finite_metric_contract(space: MetricSpace, *, name: str = "finite_metric") -> MetricContract:
    carrier=getattr(space, "carrier", None)
    if carrier is None:
        return MetricContract(name, "unknown", "symbolic", metric_kind="metric", warnings=("metric validation requires an explicit finite carrier",))
    try:
        carrier_tuple=tuple(carrier)
    except TypeError:
        return MetricContract(name, "unknown", "symbolic", metric_kind="metric", warnings=("carrier is not an explicit finite iterable",))
    validation=validate_metric(space)
    return MetricContract(name, validation.status, validation.mode, len(carrier_tuple), "finite", ("carrier is explicit and finite",), tuple(validation.justification), {"validation": validation.to_dict()})


def bounded_metric_transform_contract(space: MetricSpace, *, transform: str = "normalized", name: str = "bounded_metric_transform") -> MetricContract:
    base=finite_metric_contract(space, name=f"{name}:base")
    if base.status != "true":
        return MetricContract(name, base.status, base.mode, base.carrier_size, "bounded_transform", warnings=base.warnings, metadata={"base": base.to_result().to_dict()})
    if transform == "normalized":
        distance=normalized_metric(space.distance)
    elif transform == "capped":
        distance=capped_metric(space.distance, cap=1.0)
    else:
        return MetricContract(name, "false", "exact", base.carrier_size, "bounded_transform", warnings=("transform must be 'normalized' or 'capped'",), metadata={"transform": transform})
    transformed=FiniteMetricSpace(carrier=tuple(space.carrier), distance=distance, metadata={"source": transform})
    check=finite_metric_contract(transformed, name=f"{name}:{transform}")
    return MetricContract(name, check.status, check.mode, check.carrier_size, "bounded_transform", ("standard bounded metric transform applied to explicit finite metric",), check.warnings, {"transform": transform, "base": base.to_result().to_dict(), "transformed": check.to_result().to_dict()})


def finite_product_metric_contract(*spaces: MetricSpace, mode: str = "max", name: str = "finite_product_metric") -> MetricContract:
    if not spaces:
        return MetricContract(name, "false", "exact", metric_kind="product", warnings=("finite product metric requires at least one factor",))
    factor_contracts=[finite_metric_contract(space, name=f"factor_{idx}") for idx, space in enumerate(spaces)]
    if any(c.status != "true" for c in factor_contracts):
        merged=merge_results(*(c.to_result() for c in factor_contracts))
        return MetricContract(name, merged.status, merged.mode, metric_kind="product", warnings=tuple(merged.justification), metadata={"factors": [c.to_result().to_dict() for c in factor_contracts]})
    product_space=finite_product_metric_space(*spaces, mode=mode)
    product_contract=finite_metric_contract(product_space, name=name)
    return MetricContract(name, product_contract.status, product_contract.mode, product_contract.carrier_size, "product", ("all factors are explicit finite metric spaces",), product_contract.warnings, {"mode": mode, "factor_count": len(spaces), "factors": [c.to_result().to_dict() for c in factor_contracts]})


def equivalent_metric_contract(left: MetricSpace | None, right: MetricSpace | None, *, witness: Callable[[MetricSpace, MetricSpace], bool] | None = None, name: str = "equivalent_metric_topology") -> MetricContract:
    if left is None or right is None or witness is None:
        return MetricContract(name, "unknown", "symbolic", metric_kind="equivalence", warnings=("equivalence of induced topologies requires a witness or theorem assumptions",))
    left_contract=finite_metric_contract(left, name="left_metric"); right_contract=finite_metric_contract(right, name="right_metric")
    if left_contract.status != "true" or right_contract.status != "true":
        return MetricContract(name, "unknown", "mixed", metric_kind="equivalence", warnings=("both metrics must validate before comparing induced topologies",), metadata={"left": left_contract.to_result().to_dict(), "right": right_contract.to_result().to_dict()})
    value=bool(witness(left, right))
    return MetricContract(name, "true" if value else "false", "exact", left_contract.carrier_size, "equivalence", ("both metrics are finite and an explicit witness was supplied",), ("witness reports equality of induced topologies",) if value else ("witness reports different induced topologies",), {"witness_value": value})


def metric_contract_summary(contract: MetricContract) -> str:
    return f"{contract.name}: status={contract.status}, mode={contract.mode}, kind={contract.metric_kind}, carrier_size={contract.carrier_size}"


__all__ = [
    "MetricContract",
    "finite_metric_contract",
    "bounded_metric_transform_contract",
    "finite_product_metric_contract",
    "equivalent_metric_contract",
    "metric_contract_summary",
]
