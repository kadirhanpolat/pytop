"""Finite construction contracts for product and quotient examples."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from itertools import product as cartesian_product
from typing import Any

from .result import Result


@dataclass(frozen=True, slots=True)
class FiniteConstructionContract:
    """Machine-readable contract for a finite construction request."""

    kind: str
    status: str
    carrier_size: int | None = None
    factor_count: int | None = None
    block_count: int | None = None
    assumptions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_result(self) -> Result:
        payload = dict(self.metadata)
        payload.update({"carrier_size": self.carrier_size, "factor_count": self.factor_count, "block_count": self.block_count})
        if self.status == "true":
            return Result.true(mode="exact", value=self.kind, assumptions=self.assumptions, justification=(f"Finite {self.kind} construction contract is exact.",), metadata=payload)
        if self.status == "false":
            return Result.false(mode="exact", value=self.kind, assumptions=self.assumptions, justification=self.warnings or (f"Finite {self.kind} construction contract failed.",), metadata=payload)
        return Result.unknown(mode="symbolic", value=self.kind, assumptions=self.assumptions, justification=self.warnings or ("Construction requires more data.",), metadata=payload)


def finite_product_contract(*factors: Iterable[Any]) -> FiniteConstructionContract:
    """Return an exact finite product construction contract."""
    if len(factors) == 1 and isinstance(factors[0], (list, tuple)):
        factors = tuple(factors[0])
    if not factors:
        return FiniteConstructionContract(kind="product", status="false", warnings=("finite product requires at least one factor",))
    normalized=[]
    for idx, factor in enumerate(factors):
        try:
            values=tuple(factor)
        except TypeError:
            return FiniteConstructionContract(kind="product", status="unknown", factor_count=len(factors), warnings=("factor is not an explicit finite iterable",), metadata={"factor_index": idx})
        if not values:
            return FiniteConstructionContract(kind="product", status="false", factor_count=len(factors), warnings=("empty factor is not allowed",), metadata={"factor_index": idx})
        normalized.append(values)
    size=1
    for values in normalized:
        size*=len(values)
    sample=tuple(cartesian_product(*normalized))[:5]
    return FiniteConstructionContract(kind="product", status="true", carrier_size=size, factor_count=len(normalized), assumptions=("all factors are explicit finite iterables",), metadata={"factor_sizes":[len(v) for v in normalized], "sample": sample})


def finite_product_summary(*factors: Iterable[Any]) -> str:
    c=finite_product_contract(*factors)
    return f"{c.kind}: status={c.status}, factors={c.factor_count}, size={c.carrier_size}"


def finite_partition_contract(carrier: Iterable[Any], partition: Iterable[Iterable[Any]]) -> FiniteConstructionContract:
    """Validate a finite partition contract without building a topology."""
    points=tuple(carrier); point_set=set(points); blocks=[tuple(block) for block in partition]; seen=set()
    for idx, block in enumerate(blocks):
        if not block:
            return FiniteConstructionContract(kind="partition", status="false", warnings=("empty block is not allowed",), metadata={"block_index": idx})
        block_set=set(block)
        if not block_set <= point_set:
            return FiniteConstructionContract(kind="partition", status="false", warnings=("block contains point outside carrier",), metadata={"block_index": idx})
        if seen & block_set:
            return FiniteConstructionContract(kind="partition", status="false", warnings=("partition blocks overlap",), metadata={"block_index": idx})
        seen |= block_set
    if seen != point_set:
        return FiniteConstructionContract(kind="partition", status="false", warnings=("partition does not cover carrier",), metadata={"missing": sorted(point_set-seen, key=repr)})
    return FiniteConstructionContract(kind="partition", status="true", carrier_size=len(points), block_count=len(blocks), assumptions=("partition is explicit and finite",), metadata={"block_sizes":[len(b) for b in blocks]})


def finite_quotient_contract(carrier: Iterable[Any], partition: Iterable[Iterable[Any]]) -> FiniteConstructionContract:
    """Return a finite quotient contract induced by a partition."""
    base=finite_partition_contract(carrier, partition)
    if base.status != "true":
        return FiniteConstructionContract(kind="quotient", status="false", warnings=base.warnings, metadata=dict(base.metadata))
    return FiniteConstructionContract(kind="quotient", status="true", carrier_size=base.carrier_size, block_count=base.block_count, assumptions=("quotient is induced by an explicit finite partition",), metadata=dict(base.metadata))


def finite_quotient_summary(carrier: Iterable[Any], partition: Iterable[Iterable[Any]]) -> str:
    c=finite_quotient_contract(carrier, partition)
    return f"{c.kind}: status={c.status}, carrier={c.carrier_size}, blocks={c.block_count}"


__all__ = [
    "FiniteConstructionContract",
    "finite_product_contract",
    "finite_product_summary",
    "finite_partition_contract",
    "finite_quotient_contract",
    "finite_quotient_summary",
]
