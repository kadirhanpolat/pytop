"""Notebook smoke examples for the v1.0.308 integration phase.

The smoke layer demonstrates the intended teaching path:

1. produce a small contract object,
2. convert it into a structured :class:`pytop.result.Result`,
3. render the result into plain notebook-friendly text.

These examples are deliberately tiny and deterministic so that notebooks can
show the contract-to-Result-to-rendering flow without importing external chapter
zip content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

from .construction_contracts import finite_product_contract
from .metric_contracts import finite_metric_contract
from .metric_spaces import FiniteMetricSpace
from .predicate_contracts import finite_subset_predicate_contract, symbolic_subset_predicate_contract
from .result import Result
from .result_rendering import render_result


@dataclass(frozen=True, slots=True)
class NotebookSmokeExample:
    """One deterministic notebook smoke example."""

    name: str
    chapter_hint: str
    notebook_path: str
    contract_family: str
    purpose: str
    runner: Callable[[], Result]
    expected_status: str = "true"
    expected_mode: str | None = None

    def run(self) -> Result:
        result = self.runner()
        if not isinstance(result, Result):
            raise TypeError(f"{self.name} runner must return pytop.result.Result")
        return result

    def render(self) -> str:
        return render_result(self.run(), label=self.name)

    def to_dict(self) -> dict[str, Any]:
        result = self.run()
        return {
            "name": self.name,
            "chapter_hint": self.chapter_hint,
            "notebook_path": self.notebook_path,
            "contract_family": self.contract_family,
            "purpose": self.purpose,
            "expected_status": self.expected_status,
            "expected_mode": self.expected_mode,
            "actual_status": result.status,
            "actual_mode": result.mode,
            "is_passing": self.is_passing(),
        }

    def is_passing(self) -> bool:
        result = self.run()
        if result.status != self.expected_status:
            return False
        if self.expected_mode is not None and result.mode != self.expected_mode:
            return False
        return True


def _finite_product_result() -> Result:
    return finite_product_contract({0, 1}, {"a", "b"}).to_result()


def _finite_subset_predicate_result() -> Result:
    return finite_subset_predicate_contract(
        carrier={0, 1, 2},
        subset={0, 2},
        predicate=lambda carrier, subset: subset <= carrier,
        predicate_name="finite_subset_containment",
    ).to_result()


def _finite_metric_result() -> Result:
    space = FiniteMetricSpace(
        carrier=("x", "y"),
        distance={("x", "x"): 0, ("y", "y"): 0, ("x", "y"): 1, ("y", "x"): 1},
    )
    return finite_metric_contract(space, name="two_point_discrete_metric").to_result()


def _symbolic_predicate_result() -> Result:
    return symbolic_subset_predicate_contract(
        "symbolic_density_check",
        assumptions=("a symbolic ambient space is declared",),
        reason="notebook smoke example records symbolic status without pretending exactness",
    ).to_result()


NOTEBOOK_SMOKE_NOTEBOOK = "notebooks/smoke/contract_to_result_rendering_smoke_v1_0_308.ipynb"


NOTEBOOK_SMOKE_EXAMPLES: tuple[NotebookSmokeExample, ...] = (
    NotebookSmokeExample(
        name="finite product contract smoke",
        chapter_hint="12",
        notebook_path=NOTEBOOK_SMOKE_NOTEBOOK,
        contract_family="construction_contracts",
        purpose="Show an exact finite product contract becoming a rendered Result.",
        runner=_finite_product_result,
        expected_status="true",
        expected_mode="exact",
    ),
    NotebookSmokeExample(
        name="finite subset predicate smoke",
        chapter_hint="09/10",
        notebook_path=NOTEBOOK_SMOKE_NOTEBOOK,
        contract_family="predicate_contracts",
        purpose="Show a finite subset predicate contract with exact status.",
        runner=_finite_subset_predicate_result,
        expected_status="true",
        expected_mode="exact",
    ),
    NotebookSmokeExample(
        name="finite metric contract smoke",
        chapter_hint="08/14",
        notebook_path=NOTEBOOK_SMOKE_NOTEBOOK,
        contract_family="metric_contracts",
        purpose="Show a tiny metric validation contract rendered for notebooks.",
        runner=_finite_metric_result,
        expected_status="true",
        expected_mode="exact",
    ),
    NotebookSmokeExample(
        name="symbolic predicate smoke",
        chapter_hint="09/15",
        notebook_path=NOTEBOOK_SMOKE_NOTEBOOK,
        contract_family="predicate_contracts",
        purpose="Show that notebook examples can report symbolic/unknown status honestly.",
        runner=_symbolic_predicate_result,
        expected_status="unknown",
        expected_mode="symbolic",
    ),
)


@dataclass(frozen=True, slots=True)
class NotebookSmokeReport:
    """Aggregate result for the v1.0.308 notebook smoke surface."""

    version: str
    phase_range: str
    examples: tuple[NotebookSmokeExample, ...]
    missing_paths: tuple[str, ...] = field(default_factory=tuple)

    @property
    def example_count(self) -> int:
        return len(self.examples)

    @property
    def passing_count(self) -> int:
        return sum(1 for example in self.examples if example.is_passing())

    @property
    def failing_examples(self) -> tuple[str, ...]:
        return tuple(example.name for example in self.examples if not example.is_passing())

    @property
    def rendered_outputs(self) -> tuple[str, ...]:
        return tuple(example.render() for example in self.examples)

    @property
    def blocker_count(self) -> int:
        return len(self.failing_examples) + len(self.missing_paths)

    @property
    def is_ready(self) -> bool:
        return self.blocker_count == 0

    @property
    def status(self) -> str:
        return "true" if self.is_ready else "conditional"

    def to_result(self) -> Result:
        if self.is_ready:
            return Result.true(
                mode="exact",
                value="notebook smoke examples ready",
                assumptions=(
                    "smoke examples are deterministic",
                    "external Chapter 07--15 zip wording is not copied",
                    "the notebook is an active open-folder artifact, not a nested zip",
                ),
                justification=(
                    f"{self.example_count} smoke examples passed.",
                    "Each example follows contract -> Result -> render_result.",
                ),
                metadata={
                    "version": self.version,
                    "phase_range": self.phase_range,
                    "example_count": self.example_count,
                    "passing_count": self.passing_count,
                    "blocker_count": 0,
                    "notebook_path": NOTEBOOK_SMOKE_NOTEBOOK,
                },
            )
        return Result.conditional(
            mode="mixed",
            value="notebook smoke examples have blockers",
            assumptions=("failing examples or missing paths must be resolved before release checkpoint",),
            justification=(
                f"failing_examples={list(self.failing_examples)}",
                f"missing_paths={list(self.missing_paths)}",
            ),
            metadata={
                "version": self.version,
                "phase_range": self.phase_range,
                "example_count": self.example_count,
                "passing_count": self.passing_count,
                "blocker_count": self.blocker_count,
                "missing_paths": list(self.missing_paths),
            },
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "phase_range": self.phase_range,
            "status": self.status,
            "is_ready": self.is_ready,
            "example_count": self.example_count,
            "passing_count": self.passing_count,
            "failing_examples": list(self.failing_examples),
            "missing_paths": list(self.missing_paths),
            "examples": [example.to_dict() for example in self.examples],
            "rendered_outputs": list(self.rendered_outputs),
        }


def notebook_smoke_examples() -> tuple[NotebookSmokeExample, ...]:
    """Return the deterministic smoke examples used by the v1.0.308 notebook."""

    return NOTEBOOK_SMOKE_EXAMPLES


def missing_notebook_smoke_paths(package_root: str | Path | None = None) -> tuple[str, ...]:
    """Return missing open-folder notebook smoke files."""

    if package_root is None:
        return ()
    root = Path(package_root)
    required = (
        NOTEBOOK_SMOKE_NOTEBOOK,
        "docs/notebooks/notebook_smoke_examples_v1_0_308.md",
        "docs/integration/chapter_07_15/chapter_07_15_notebook_smoke_examples_v1_0_308.md",
    )
    return tuple(path for path in required if not (root / path).exists())


def notebook_smoke_report(package_root: str | Path | None = None) -> NotebookSmokeReport:
    """Build the v1.0.308 notebook smoke report."""

    return NotebookSmokeReport(
        version="v1.0.308",
        phase_range="v1.0.306-v1.0.310",
        examples=notebook_smoke_examples(),
        missing_paths=missing_notebook_smoke_paths(package_root),
    )


def run_notebook_smoke_examples() -> tuple[Result, ...]:
    """Execute all smoke examples and return their structured results."""

    return tuple(example.run() for example in notebook_smoke_examples())


def render_notebook_smoke_examples() -> tuple[str, ...]:
    """Execute and render all smoke examples."""

    return tuple(example.render() for example in notebook_smoke_examples())


def notebook_smoke_summary(package_root: str | Path | None = None) -> str:
    """Return a compact human-readable summary."""

    report = notebook_smoke_report(package_root)
    return (
        f"Notebook smoke examples: {report.version}; "
        f"phase: {report.phase_range}; "
        f"examples: {report.example_count}; "
        f"passing: {report.passing_count}; "
        f"blockers: {report.blocker_count}"
    )
