"""Core-strengthening phase checkpoint for the v1.0.300-v1.0.305 sequence.

This module closes the small core helper phase before the project returns to
questionbank, manuscript, and notebook integration.  It is intentionally a
release checkpoint: it does not add new topology theorems; it records whether
the recently added construction, predicate, metric, rendering, and API
consistency surfaces are present and usable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, Mapping

from .api_consistency import APIConsistencyReport, api_consistency_report
from .result import Result


@dataclass(frozen=True, slots=True)
class CoreStrengtheningSurface:
    """One completed surface in the v1.0.300-v1.0.305 phase."""

    version: str
    module_name: str
    role: str
    public_exports: tuple[str, ...]
    status: str = "completed"

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "module_name": self.module_name,
            "role": self.role,
            "public_exports": list(self.public_exports),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class ForwardIntegrationGap:
    """A non-blocking gap intentionally carried into the next integration phase."""

    area: str
    priority: str
    description: str
    next_action: str

    def to_dict(self) -> dict[str, str]:
        return {
            "area": self.area,
            "priority": self.priority,
            "description": self.description,
            "next_action": self.next_action,
        }


CORE_STRENGTHENING_PHASE_SURFACES: tuple[CoreStrengtheningSurface, ...] = (
    CoreStrengtheningSurface(
        "v1.0.300",
        "pytop.construction_contracts",
        "finite product, partition, and quotient construction contracts",
        (
            "FiniteConstructionContract",
            "finite_product_contract",
            "finite_product_summary",
            "finite_partition_contract",
            "finite_quotient_contract",
            "finite_quotient_summary",
        ),
    ),
    CoreStrengtheningSurface(
        "v1.0.301",
        "pytop.predicate_contracts",
        "finite and symbolic subset predicate contracts",
        (
            "SubsetPredicateContract",
            "finite_subset_predicate_contract",
            "symbolic_subset_predicate_contract",
            "subset_predicate_contract",
            "subset_predicate_summary",
        ),
    ),
    CoreStrengtheningSurface(
        "v1.0.302",
        "pytop.metric_contracts",
        "finite metric, bounded transform, product metric, and equivalence contracts",
        (
            "MetricContract",
            "finite_metric_contract",
            "bounded_metric_transform_contract",
            "finite_product_metric_contract",
            "equivalent_metric_contract",
            "metric_contract_summary",
        ),
    ),
    CoreStrengtheningSurface(
        "v1.0.303",
        "pytop.result_rendering",
        "deterministic Result rendering and explanation helpers",
        (
            "ResultExplanation",
            "normalize_result_source",
            "result_status_label",
            "result_mode_label",
            "explain_result",
            "render_result",
            "render_result_collection",
        ),
    ),
    CoreStrengtheningSurface(
        "v1.0.304",
        "pytop.api_consistency",
        "public API consistency checkpoint across the core helper surfaces",
        (
            "APIConsistencyReport",
            "CORE_STRENGTHENING_API_SURFACE",
            "api_consistency_report",
            "api_consistency_summary",
        ),
    ),
)


FORWARD_INTEGRATION_GAPS: tuple[ForwardIntegrationGap, ...] = (
    ForwardIntegrationGap(
        area="questionbank",
        priority="high",
        description="Question templates need explicit bindings to the new construction, predicate, metric, and rendering contracts.",
        next_action="Start v1.0.306 with a questionbank bridge map that uses the stabilized core contracts without copying Chapter 07--15 text.",
    ),
    ForwardIntegrationGap(
        area="manuscript",
        priority="high",
        description="Manuscript cross-references should point to active examples_bank and core helper surfaces rather than historical archive notes.",
        next_action="Add a manuscript integration checklist during the v1.0.306-v1.0.310 phase.",
    ),
    ForwardIntegrationGap(
        area="notebooks",
        priority="medium",
        description="Notebook smoke examples should demonstrate the new contract-to-Result-to-rendering flow.",
        next_action="Add minimal notebook-facing examples after the questionbank bridge is present.",
    ),
    ForwardIntegrationGap(
        area="release_verification",
        priority="medium",
        description="The permanent packaging/release verification toolchain is still planned for v1.0.311-v1.0.315.",
        next_action="Keep current manual delivery protocol until the dedicated release verification tools are introduced.",
    ),
)


@dataclass(frozen=True, slots=True)
class CoreStrengtheningCheckpointReport:
    """Machine-readable closeout report for the core-strengthening phase."""

    version: str
    phase_range: str
    surfaces: tuple[CoreStrengtheningSurface, ...]
    api_report: APIConsistencyReport
    missing_modules: tuple[str, ...] = ()
    missing_public_exports: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    forward_gaps: tuple[ForwardIntegrationGap, ...] = FORWARD_INTEGRATION_GAPS
    notes: tuple[str, ...] = ()

    @property
    def checked_surface_count(self) -> int:
        return len(self.surfaces)

    @property
    def blocker_count(self) -> int:
        api_probe_failures = sum(1 for value in self.api_report.probe_results.values() if value != "ok")
        export_failures = sum(len(values) for values in self.missing_public_exports.values())
        return len(self.missing_modules) + export_failures + len(self.api_report.missing_exports) + api_probe_failures

    @property
    def status(self) -> str:
        return "true" if self.blocker_count == 0 and self.api_report.is_consistent else "false"

    @property
    def is_closed(self) -> bool:
        return self.status == "true"

    def to_result(self) -> Result:
        metadata = {
            "phase_range": self.phase_range,
            "checked_surface_count": self.checked_surface_count,
            "blocker_count": self.blocker_count,
            "missing_modules": list(self.missing_modules),
            "missing_public_exports": {key: list(value) for key, value in self.missing_public_exports.items()},
            "forward_gap_count": len(self.forward_gaps),
            "forward_gaps": [gap.to_dict() for gap in self.forward_gaps],
            "api_report": self.api_report.to_result().to_dict(),
        }
        justification = [
            f"Checked {self.checked_surface_count} core-strengthening surfaces from {self.phase_range}.",
            f"API consistency status: {self.api_report.status}.",
            f"Forward integration gaps recorded for v1.0.306-v1.0.310: {len(self.forward_gaps)}.",
        ]
        justification.extend(self.notes)
        if self.is_closed:
            return Result.true(
                mode="exact",
                value=f"core-strengthening phase closed at {self.version}",
                justification=justification,
                metadata=metadata,
            )
        return Result.false(
            mode="exact",
            value=f"core-strengthening phase has blockers at {self.version}",
            justification=justification,
            metadata=metadata,
        )

    def summary_lines(self) -> list[str]:
        lines = [
            f"Core-strengthening checkpoint: {self.version}",
            f"phase: {self.phase_range}",
            f"status: {self.status}",
            f"checked surfaces: {self.checked_surface_count}",
            f"blockers: {self.blocker_count}",
            f"forward gaps: {len(self.forward_gaps)}",
        ]
        for surface in self.surfaces:
            lines.append(f"- {surface.version}: {surface.module_name} ({surface.status})")
        if self.forward_gaps:
            lines.append("forward integration gaps:")
            for gap in self.forward_gaps:
                lines.append(f"- {gap.area} [{gap.priority}]: {gap.next_action}")
        return lines


def core_strengthening_checkpoint_report() -> CoreStrengtheningCheckpointReport:
    """Return the v1.0.305 closeout report for the core-strengthening phase."""
    surfaces = CORE_STRENGTHENING_PHASE_SURFACES
    missing_modules: list[str] = []
    missing_public_exports: dict[str, tuple[str, ...]] = {}

    public_module = import_module("pytop")
    for surface in surfaces:
        try:
            import_module(surface.module_name)
        except Exception:  # pragma: no cover - defensive release-check branch
            missing_modules.append(surface.module_name)
        missing = tuple(name for name in surface.public_exports if not hasattr(public_module, name))
        if missing:
            missing_public_exports[surface.module_name] = missing

    api_report = api_consistency_report()
    notes = (
        "The v1.0.300-v1.0.305 core-strengthening phase is closed when no blocker is found.",
        "Remaining gaps are forward integration tasks, not evidence of data loss.",
    )
    return CoreStrengtheningCheckpointReport(
        version="v1.0.305",
        phase_range="v1.0.300-v1.0.305",
        surfaces=surfaces,
        api_report=api_report,
        missing_modules=tuple(missing_modules),
        missing_public_exports=missing_public_exports,
        notes=notes,
    )


def core_strengthening_summary(report: CoreStrengtheningCheckpointReport | None = None) -> str:
    """Return a compact text summary of the phase closeout checkpoint."""
    active_report = report or core_strengthening_checkpoint_report()
    return "\n".join(active_report.summary_lines())
