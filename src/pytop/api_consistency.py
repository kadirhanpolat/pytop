"""API consistency checkpoint helpers for the v1.0.300-v1.0.303 core surfaces.

The checker is intentionally small and deterministic.  It does not attempt to
prove topology facts; it verifies that the public import surface, contract
objects, result conversion, and rendering layer still agree with one another.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, Mapping, Sequence

from .construction_contracts import finite_product_contract, finite_quotient_contract
from .metric_contracts import bounded_metric_transform_contract, finite_metric_contract, finite_product_metric_contract
from .metric_spaces import FiniteMetricSpace
from .predicate_contracts import finite_subset_predicate_contract, symbolic_subset_predicate_contract
from .result import Result
from .result_rendering import render_result


CORE_STRENGTHENING_API_SURFACE: tuple[str, ...] = (
    "FiniteConstructionContract",
    "finite_product_contract",
    "finite_product_summary",
    "finite_partition_contract",
    "finite_quotient_contract",
    "finite_quotient_summary",
    "SubsetPredicateContract",
    "finite_subset_predicate_contract",
    "symbolic_subset_predicate_contract",
    "subset_predicate_contract",
    "subset_predicate_summary",
    "MetricContract",
    "finite_metric_contract",
    "bounded_metric_transform_contract",
    "finite_product_metric_contract",
    "equivalent_metric_contract",
    "metric_contract_summary",
    "ResultExplanation",
    "normalize_result_source",
    "result_status_label",
    "result_mode_label",
    "explain_result",
    "render_result",
    "render_result_collection",
)


@dataclass(frozen=True, slots=True)
class APIConsistencyReport:
    """Machine-readable checkpoint for the active core public API."""

    version: str
    checked_exports: tuple[str, ...]
    missing_exports: tuple[str, ...] = ()
    probe_results: Mapping[str, str] = field(default_factory=dict)
    notes: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        return "true" if not self.missing_exports and all(value == "ok" for value in self.probe_results.values()) else "false"

    @property
    def is_consistent(self) -> bool:
        return self.status == "true"

    def to_result(self) -> Result:
        metadata = {
            "checked_export_count": len(self.checked_exports),
            "missing_exports": list(self.missing_exports),
            "probe_results": dict(self.probe_results),
        }
        justification = [
            f"Checked {len(self.checked_exports)} public exports from the v1.0.300-v1.0.303 core-strengthening surfaces.",
            f"Executed {len(self.probe_results)} contract/result/rendering probes.",
        ]
        if self.missing_exports:
            justification.append("Missing exports: " + ", ".join(self.missing_exports))
        justification.extend(self.notes)
        if self.is_consistent:
            return Result.true(
                mode="exact",
                value=f"api consistency checkpoint {self.version}",
                justification=justification,
                metadata=metadata,
            )
        return Result.false(
            mode="exact",
            value=f"api consistency checkpoint {self.version}",
            justification=justification,
            metadata=metadata,
        )

    def summary_lines(self) -> list[str]:
        lines = [
            f"API consistency checkpoint: {self.version}",
            f"status: {self.status}",
            f"checked exports: {len(self.checked_exports)}",
            f"missing exports: {len(self.missing_exports)}",
            f"probes: {len(self.probe_results)}",
        ]
        for name, outcome in self.probe_results.items():
            lines.append(f"- {name}: {outcome}")
        return lines


def api_consistency_report(*, expected_exports: Sequence[str] = CORE_STRENGTHENING_API_SURFACE) -> APIConsistencyReport:
    """Check the public API consistency of the recent core-strengthening helpers."""
    public_module = import_module("pytop")
    expected = tuple(expected_exports)
    missing = tuple(name for name in expected if not hasattr(public_module, name))
    probe_results = _run_core_probes()
    notes: list[str] = []
    if not missing:
        notes.append("All expected core-strengthening exports are present on the public pytop import surface.")
    if all(value == "ok" for value in probe_results.values()):
        notes.append("Contract objects, Result conversion, and rendering probes agree.")
    return APIConsistencyReport("v1.0.304", expected, missing, probe_results, tuple(notes))


def api_consistency_summary(report: APIConsistencyReport | None = None) -> str:
    """Return a compact text summary for release notes and smoke checks."""
    active_report = report or api_consistency_report()
    return "\n".join(active_report.summary_lines())


def _run_core_probes() -> dict[str, str]:
    outcomes: dict[str, str] = {}

    product = finite_product_contract([0, 1], ["a", "b"])
    quotient = finite_quotient_contract({0, 1, 2}, [{0, 1}, {2}])
    subset = finite_subset_predicate_contract({0, 1, 2}, {0, 1}, lambda carrier, subset: subset <= carrier, predicate_name="contained")
    symbolic = symbolic_subset_predicate_contract("dense")
    metric_space = FiniteMetricSpace(carrier=(0, 1), distance=lambda x, y: 0.0 if x == y else 1.0)
    metric = finite_metric_contract(metric_space)
    bounded = bounded_metric_transform_contract(metric_space, transform="normalized")
    product_metric = finite_product_metric_contract(metric_space, metric_space)

    probes = {
        "finite_product_contract": product,
        "finite_quotient_contract": quotient,
        "finite_subset_predicate_contract": subset,
        "symbolic_subset_predicate_contract": symbolic,
        "finite_metric_contract": metric,
        "bounded_metric_transform_contract": bounded,
        "finite_product_metric_contract": product_metric,
    }

    for name, contract in probes.items():
        try:
            result = contract.to_result()
            rendered = render_result(contract, label=name)
            if not isinstance(result, Result):
                outcomes[name] = "to_result_not_result"
            elif "[" not in rendered or name not in rendered:
                outcomes[name] = "render_failed"
            elif name == "symbolic_subset_predicate_contract" and not result.is_unknown:
                outcomes[name] = "unexpected_symbolic_status"
            elif name != "symbolic_subset_predicate_contract" and not result.is_true:
                outcomes[name] = f"unexpected_status_{result.status}"
            else:
                outcomes[name] = "ok"
        except Exception as exc:  # pragma: no cover - defensive release-check branch
            outcomes[name] = f"error:{type(exc).__name__}:{exc}"

    return outcomes
