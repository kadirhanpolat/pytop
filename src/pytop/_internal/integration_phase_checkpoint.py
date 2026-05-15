"""Phase checkpoint for the v1.0.306--v1.0.310 integration line.

The checkpoint closes the questionbank/manuscript/notebook integration phase
without importing external Chapter 07--15 wording and without creating active
nested subproject zips. It is intentionally a small coordination layer over
the v1.0.306 questionbank bridge, v1.0.307 manuscript checklist,
v1.0.308 notebook smoke examples, and v1.0.309 integration quality gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .integration_quality_gate import IntegrationQualityGateReport, integration_quality_gate_report
from .result import Result


INTEGRATION_PHASE_SURFACE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "name": "questionbank_bridge",
        "version": "v1.0.306",
        "role": "question family bridge to active core contracts",
        "required_paths": (
            "src/pytop/questionbank_bridge.py",
            "tests/core/test_questionbank_bridge_v306.py",
            "docs/questionbank/questionbank_bridge_map_v1_0_306.md",
        ),
    },
    {
        "name": "manuscript_integration",
        "version": "v1.0.307",
        "role": "manuscript target checklist and cross-reference pass",
        "required_paths": (
            "src/pytop/manuscript_integration.py",
            "tests/core/test_manuscript_integration_v307.py",
            "docs/manuscript/manuscript_integration_checklist_v1_0_307.md",
        ),
    },
    {
        "name": "notebook_smoke_examples",
        "version": "v1.0.308",
        "role": "contract-to-Result-to-rendering notebook smoke examples",
        "required_paths": (
            "src/pytop/notebook_smoke_examples.py",
            "tests/core/test_notebook_smoke_examples_v308.py",
            "notebooks/smoke/contract_to_result_rendering_smoke_v1_0_308.ipynb",
            "docs/notebooks/notebook_smoke_examples_v1_0_308.md",
        ),
    },
    {
        "name": "integration_quality_gate",
        "version": "v1.0.309",
        "role": "cross-surface quality gate for the integration phase",
        "required_paths": (
            "src/pytop/integration_quality_gate.py",
            "tests/core/test_integration_quality_gate_v309.py",
            "docs/quality/integration_quality_gate_v1_0_309.md",
        ),
    },
)


@dataclass(frozen=True, slots=True)
class IntegrationPhaseCheckpointSurface:
    """One surface included in the v1.0.310 phase checkpoint."""

    name: str
    version: str
    role: str
    required_paths: tuple[str, ...]
    missing_paths: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_ready(self) -> bool:
        return not self.missing_paths

    @property
    def blocker_count(self) -> int:
        return len(self.missing_paths)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "role": self.role,
            "is_ready": self.is_ready,
            "blocker_count": self.blocker_count,
            "required_paths": list(self.required_paths),
            "missing_paths": list(self.missing_paths),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class IntegrationPhaseCheckpointReport:
    """Closure report for the v1.0.306--v1.0.310 integration phase."""

    version: str
    phase_range: str
    next_track: str
    surfaces: tuple[IntegrationPhaseCheckpointSurface, ...]
    gate_report: IntegrationQualityGateReport
    policy_notes: tuple[str, ...]
    release_notes: tuple[str, ...] = ()

    @property
    def surface_count(self) -> int:
        return len(self.surfaces)

    @property
    def ready_surface_count(self) -> int:
        return sum(1 for surface in self.surfaces if surface.is_ready)

    @property
    def missing_paths(self) -> tuple[str, ...]:
        return tuple(path for surface in self.surfaces for path in surface.missing_paths)

    @property
    def blocker_count(self) -> int:
        return sum(surface.blocker_count for surface in self.surfaces) + self.gate_report.blocker_count

    @property
    def status(self) -> str:
        return "true" if self.is_ready else "conditional"

    @property
    def is_ready(self) -> bool:
        return self.ready_surface_count == self.surface_count and self.gate_report.is_ready and self.blocker_count == 0

    def to_result(self) -> Result:
        if self.is_ready:
            return Result.true(
                mode="exact",
                value="integration phase checkpoint ready",
                assumptions=(
                    "Chapter 07--15 external zips remain reference inputs only",
                    "active sources remain open folders inside one full package",
                    "the frozen docs/archive bundle is the only permitted nested zip",
                ),
                justification=(
                    f"{self.ready_surface_count}/{self.surface_count} phase surfaces are ready.",
                    f"The upstream gate {self.gate_report.version} is ready with {self.gate_report.blocker_count} blockers.",
                    f"The next track is {self.next_track} permanent release verification tooling.",
                ),
                metadata={
                    "version": self.version,
                    "phase_range": self.phase_range,
                    "next_track": self.next_track,
                    "surface_count": self.surface_count,
                    "ready_surface_count": self.ready_surface_count,
                    "blocker_count": 0,
                },
            )
        return Result.conditional(
            mode="mixed",
            value="integration phase checkpoint has blockers",
            assumptions=("all checkpoint blockers must be resolved before release verification tooling",),
            justification=(
                f"ready_surfaces={self.ready_surface_count}/{self.surface_count}",
                f"missing_paths={list(self.missing_paths)}",
                f"gate_blockers={self.gate_report.blocker_count}",
            ),
            metadata={
                "version": self.version,
                "phase_range": self.phase_range,
                "next_track": self.next_track,
                "surface_count": self.surface_count,
                "ready_surface_count": self.ready_surface_count,
                "blocker_count": self.blocker_count,
                "missing_paths": list(self.missing_paths),
                "gate_report": self.gate_report.to_dict(),
            },
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "phase_range": self.phase_range,
            "next_track": self.next_track,
            "status": self.status,
            "is_ready": self.is_ready,
            "surface_count": self.surface_count,
            "ready_surface_count": self.ready_surface_count,
            "blocker_count": self.blocker_count,
            "missing_paths": list(self.missing_paths),
            "surfaces": [surface.to_dict() for surface in self.surfaces],
            "gate_report": self.gate_report.to_dict(),
            "policy_notes": list(self.policy_notes),
            "release_notes": list(self.release_notes),
        }


def _missing_paths(package_root: Path | None, required_paths: tuple[str, ...]) -> tuple[str, ...]:
    if package_root is None:
        return ()
    return tuple(path for path in required_paths if not (package_root / path).exists())


def _surface_from_spec(spec: Mapping[str, Any], package_root: Path | None) -> IntegrationPhaseCheckpointSurface:
    required_paths = tuple(str(path) for path in spec["required_paths"])
    return IntegrationPhaseCheckpointSurface(
        name=str(spec["name"]),
        version=str(spec["version"]),
        role=str(spec["role"]),
        required_paths=required_paths,
        missing_paths=_missing_paths(package_root, required_paths),
        metadata={"phase_range": "v1.0.306-v1.0.310"},
    )


def integration_phase_checkpoint_report(package_root: str | Path | None = None) -> IntegrationPhaseCheckpointReport:
    """Build the v1.0.310 integration phase checkpoint report."""

    root = Path(package_root) if package_root is not None else None
    surfaces = tuple(_surface_from_spec(spec, root) for spec in INTEGRATION_PHASE_SURFACE_SPECS)
    return IntegrationPhaseCheckpointReport(
        version="v1.0.310",
        phase_range="v1.0.306-v1.0.310",
        next_track="v1.0.311-v1.0.315",
        surfaces=surfaces,
        gate_report=integration_quality_gate_report(root),
        policy_notes=(
            "No external Chapter 07--15 zip is copied into active sources.",
            "No active subproject is converted to a nested zip.",
            "The package remains a full single-root release.",
        ),
        release_notes=(
            "This checkpoint closes the integration phase and prepares the release-verification track.",
            "It verifies evidence paths instead of adding new mathematical claims.",
        ),
    )


def integration_phase_checkpoint_summary(package_root: str | Path | None = None) -> str:
    """Return a compact human-readable v1.0.310 checkpoint summary."""

    report = integration_phase_checkpoint_report(package_root)
    return (
        f"Integration phase checkpoint: {report.version}; "
        f"phase: {report.phase_range}; "
        f"surfaces: {report.ready_surface_count}/{report.surface_count}; "
        f"gate: {report.gate_report.status}; "
        f"blockers: {report.blocker_count}; "
        f"next: {report.next_track}"
    )
