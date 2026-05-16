"""Subset predicate contract helpers for finite and symbolic workflows."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .result import Result


@dataclass(frozen=True, slots=True)
class SubsetPredicateContract:
    predicate_name: str
    status: str
    mode: str
    carrier_size: int | None = None
    subset_size: int | None = None
    assumptions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_result(self) -> Result:
        payload=dict(self.metadata); payload.update({"predicate_name": self.predicate_name, "carrier_size": self.carrier_size, "subset_size": self.subset_size})
        if self.status == "true":
            return Result.true(mode=self.mode, value=self.predicate_name, assumptions=self.assumptions, justification=self.warnings or (f"predicate {self.predicate_name!r} holds",), metadata=payload)
        if self.status == "false":
            return Result.false(mode=self.mode, value=self.predicate_name, assumptions=self.assumptions, justification=self.warnings or (f"predicate {self.predicate_name!r} fails",), metadata=payload)
        if self.status == "conditional":
            return Result.conditional(mode=self.mode, value=self.predicate_name, assumptions=self.assumptions, justification=self.warnings or (f"predicate {self.predicate_name!r} is conditional",), metadata=payload)
        return Result.unknown(mode=self.mode, value=self.predicate_name, assumptions=self.assumptions, justification=self.warnings or (f"predicate {self.predicate_name!r} requires more data",), metadata=payload)


def finite_subset_predicate_contract(carrier: Iterable[Any], subset: Iterable[Any], predicate: Callable[[set[Any], set[Any]], bool], *, predicate_name: str = "subset_predicate") -> SubsetPredicateContract:
    carrier_set=set(carrier); subset_set=set(subset)
    if not subset_set <= carrier_set:
        return SubsetPredicateContract(predicate_name, "false", "exact", len(carrier_set), len(subset_set), warnings=("subset is not contained in the carrier",))
    value=bool(predicate(carrier_set, subset_set))
    return SubsetPredicateContract(predicate_name, "true" if value else "false", "exact", len(carrier_set), len(subset_set), assumptions=("carrier and subset are explicit finite sets",), metadata={"subset": sorted(subset_set, key=repr)})


def symbolic_subset_predicate_contract(predicate_name: str, *, assumptions: Iterable[str] = (), reason: str = "symbolic subset data are not enough for an exact check") -> SubsetPredicateContract:
    return SubsetPredicateContract(predicate_name, "unknown", "symbolic", assumptions=tuple(assumptions), warnings=(reason,))


def subset_predicate_contract(carrier: Iterable[Any] | None, subset: Iterable[Any] | None, predicate: Callable[[set[Any], set[Any]], bool] | None = None, *, predicate_name: str = "subset_predicate") -> SubsetPredicateContract:
    if carrier is None or subset is None or predicate is None:
        return symbolic_subset_predicate_contract(predicate_name)
    return finite_subset_predicate_contract(carrier, subset, predicate, predicate_name=predicate_name)


def subset_predicate_summary(contract: SubsetPredicateContract) -> str:
    return f"{contract.predicate_name}: status={contract.status}, mode={contract.mode}, subset_size={contract.subset_size}"


__all__ = [
    "SubsetPredicateContract",
    "finite_subset_predicate_contract",
    "symbolic_subset_predicate_contract",
    "subset_predicate_contract",
    "subset_predicate_summary",
]
