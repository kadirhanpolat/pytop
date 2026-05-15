"""Cardinal-function example catalog and comparison routes for Cilt IV (v0.1.72).

This module turns the v0.1.70 definition/comparison/example framework into a
small reusable catalog of worked example patterns.  The v0.1.72 extension adds
comparison-exercise routes and notebook-route alignment records.  It remains a
durable source module, not a per-version release/report surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .result import Result

VERSION = "0.1.72"

__all__ = [
    "CardinalFunctionExampleError",
    "CardinalFunctionExample",
    "CardinalFunctionComparisonRoute",
    "cardinal_function_examples_catalog",
    "cardinal_function_example",
    "cardinal_function_examples_by_layer",
    "cardinal_function_workbook_tasks",
    "cardinal_function_comparison_exercises",
    "cardinal_function_notebook_route_alignment",
    "analyze_cardinal_function_examples",
]


class CardinalFunctionExampleError(ValueError):
    """Raised when a cardinal-function example key or layer is unknown."""


@dataclass(frozen=True, slots=True)
class CardinalFunctionExample:
    """A reusable, student-facing cardinal-function example record."""

    key: str
    title: str
    layer: str
    assumptions: tuple[str, ...]
    invariant_values: dict[str, str]
    tasks: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    notebook_tags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "layer": self.layer,
            "assumptions": list(self.assumptions),
            "invariant_values": dict(self.invariant_values),
            "tasks": list(self.tasks),
            "warnings": list(self.warnings),
            "notebook_tags": list(self.notebook_tags),
        }

@dataclass(frozen=True, slots=True)
class CardinalFunctionComparisonRoute:
    """A durable comparison-exercise route tied to notebooks and examples."""

    route_id: str
    title: str
    comparison_pair: tuple[str, str]
    objective: str
    example_keys: tuple[str, ...]
    exploration_notebook: str
    teaching_notebook: str
    examples_bank: str
    manuscript_chapter: str
    task_prompts: tuple[str, ...]
    expected_distinctions: tuple[str, ...]
    warning_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "route_id": self.route_id,
            "title": self.title,
            "comparison_pair": list(self.comparison_pair),
            "objective": self.objective,
            "example_keys": list(self.example_keys),
            "notebook_route": {
                "exploration": self.exploration_notebook,
                "teaching": self.teaching_notebook,
                "examples_bank": self.examples_bank,
                "manuscript_chapter": self.manuscript_chapter,
            },
            "task_prompts": list(self.task_prompts),
            "expected_distinctions": list(self.expected_distinctions),
            "warning_notes": list(self.warning_notes),
        }


_BASE_INVARIANTS = (
    "weight",
    "density",
    "character",
    "lindelof_number",
    "cellularity",
    "spread",
    "network_weight",
    "tightness",
)


def _values(**overrides: str) -> dict[str, str]:
    data = {name: "recorded under stated assumptions" for name in _BASE_INVARIANTS}
    data.update(overrides)
    return data


_EXAMPLES: tuple[CardinalFunctionExample, ...] = (
    CardinalFunctionExample(
        key="finite_discrete_n",
        title="n-point finite discrete space",
        layer="computable_finite",
        assumptions=("X has n points", "topology is discrete"),
        invariant_values=_values(
            weight="n",
            density="n",
            character="1 locally; finite globally",
            lindelof_number="finite",
            cellularity="n",
            spread="n",
            network_weight="n",
            tightness="finite/countable threshold",
        ),
        tasks=(
            "List the singleton base and read w(X) from it.",
            "Show every dense subset must be the whole carrier.",
            "Compare cellularity and spread using singleton witnesses.",
        ),
        warnings=("Do not answer only |X|; name the witness for each invariant.",),
        notebook_tags=("finite", "discrete"),
    ),
    CardinalFunctionExample(
        key="finite_indiscrete_n",
        title="n-point finite indiscrete space",
        layer="computable_finite",
        assumptions=("X is nonempty and finite", "only open sets are empty set and X"),
        invariant_values=_values(
            weight="1",
            density="1",
            character="1",
            lindelof_number="finite/1 threshold",
            cellularity="1",
            spread="1 in the non-T1 pedagogical reading",
            network_weight="1",
            tightness="finite/countable threshold",
        ),
        tasks=(
            "Use X as the single nonempty basic open set.",
            "Explain why any singleton is dense.",
            "Contrast this record with the finite discrete topology.",
        ),
        warnings=("The carrier size alone does not determine cardinal functions.",),
        notebook_tags=("finite", "indiscrete"),
    ),
    CardinalFunctionExample(
        key="countable_discrete",
        title="countably infinite discrete space",
        layer="safe_infinite",
        assumptions=("X is countably infinite", "topology is discrete"),
        invariant_values=_values(
            weight="aleph_0",
            density="aleph_0",
            character="1 locally",
            lindelof_number="aleph_0",
            cellularity="aleph_0",
            spread="aleph_0",
            network_weight="aleph_0",
            tightness="aleph_0 threshold",
        ),
        tasks=(
            "Show the singleton base is countable.",
            "Use the singleton cover to read the Lindelof threshold.",
            "Use X itself as a countable discrete subspace witness.",
        ),
        notebook_tags=("discrete", "countable"),
    ),
    CardinalFunctionExample(
        key="uncountable_discrete_kappa",
        title="uncountable discrete space of size kappa",
        layer="safe_infinite",
        assumptions=("|X| = kappa", "kappa is uncountable", "topology is discrete"),
        invariant_values=_values(
            weight="kappa",
            density="kappa",
            character="1 locally",
            lindelof_number="kappa",
            cellularity="kappa",
            spread="kappa",
            network_weight="kappa",
            tightness="aleph_0 threshold",
        ),
        tasks=(
            "Use the singleton cover to force a large subcover.",
            "Separate local character from global weight.",
            "Compare density, cellularity and spread on the same carrier.",
        ),
        warnings=("Local smallness need not imply global smallness.",),
        notebook_tags=("discrete", "uncountable"),
    ),
    CardinalFunctionExample(
        key="second_countable_metric_safe",
        title="second-countable metric example",
        layer="metric_safe_pattern",
        assumptions=("X is metric", "X is explicitly second-countable"),
        invariant_values=_values(
            weight="aleph_0",
            density="aleph_0",
            character="aleph_0",
            lindelof_number="aleph_0",
            cellularity="at most aleph_0",
            spread="at most aleph_0 in the separable metric setting",
            network_weight="aleph_0",
            tightness="aleph_0",
        ),
        tasks=(
            "Start from the countable base.",
            "State where second-countability is used.",
            "Do not replace the hypothesis by metric alone.",
        ),
        warnings=("Metric does not automatically mean second-countable without a separate hypothesis.",),
        notebook_tags=("metric", "second_countable"),
    ),
    CardinalFunctionExample(
        key="cantor_compact_metric",
        title="Cantor-type compact metric model",
        layer="metric_safe_pattern",
        assumptions=("X is compact", "X is metric", "X is second-countable"),
        invariant_values=_values(
            weight="aleph_0",
            density="aleph_0",
            character="aleph_0",
            lindelof_number="aleph_0 / compact threshold",
            cellularity="at most aleph_0",
            spread="at most aleph_0",
            network_weight="aleph_0",
            tightness="aleph_0",
        ),
        tasks=(
            "Use compactness for cover control.",
            "Separate compactness from metric countability.",
            "Explain why this is an example pattern, not a theorem about every compact space.",
        ),
        notebook_tags=("compact", "metric"),
    ),
    CardinalFunctionExample(
        key="real_line_standard",
        title="real line with the usual topology",
        layer="classical_reference",
        assumptions=("usual topology on R", "rational-interval base"),
        invariant_values=_values(
            weight="aleph_0",
            density="aleph_0",
            character="aleph_0",
            lindelof_number="aleph_0",
            cellularity="aleph_0",
            spread="aleph_0",
            network_weight="aleph_0",
            tightness="aleph_0",
        ),
        tasks=(
            "Write the rational-endpoint interval base.",
            "Use Q as a dense-set witness.",
            "Compare this example with the uncountable discrete example.",
        ),
        notebook_tags=("real_line", "second_countable"),
    ),
    CardinalFunctionExample(
        key="sorgenfrey_line_warning",
        title="Sorgenfrey-line warning pattern",
        layer="classical_reference",
        assumptions=("lower-limit topology is used", "standard real-line intuition is not reused blindly"),
        invariant_values=_values(
            weight="uncountable pattern",
            density="aleph_0 pattern",
            character="aleph_0",
            lindelof_number="aleph_0 pattern for the line; product warnings remain separate",
            cellularity="aleph_0 pattern",
            spread="uncountable subspace warnings depend on context",
            network_weight="not the usual second-countable network",
            tightness="aleph_0 pattern",
        ),
        tasks=(
            "Explain why the usual rational-interval base is not the right base.",
            "Record which claims are pattern-level rather than computed by the finite engine.",
            "Use the example as a warning against replacing topology by carrier set.",
        ),
        warnings=("This record is a reading pattern, not a finite computation.",),
        notebook_tags=("sorgenfrey", "warning"),
    ),
    CardinalFunctionExample(
        key="one_point_compactification_discrete_kappa",
        title="one-point compactification of an uncountable discrete space",
        layer="global_local_warning",
        assumptions=("D is discrete of size kappa", "kappa is uncountable", "X = D union {infinity}"),
        invariant_values=_values(
            weight="kappa pattern",
            density="kappa",
            character="large at infinity; small at isolated points",
            lindelof_number="compact threshold",
            cellularity="kappa",
            spread="kappa",
            network_weight="kappa pattern",
            tightness="depends on the compactification point",
        ),
        tasks=(
            "Compare isolated points with the compactification point.",
            "Use singleton opens in D as cellularity witnesses.",
            "Explain why compactness alone does not force small weight.",
        ),
        warnings=("Record compactness separately from cardinal smallness.",),
        notebook_tags=("compactification", "global_local"),
    ),
)



_COMPARISON_ROUTES: tuple[CardinalFunctionComparisonRoute, ...] = (
    CardinalFunctionComparisonRoute(
        route_id="weight_vs_density",
        title="Weight versus density on shared examples",
        comparison_pair=("weight", "density"),
        objective=(
            "Separate the cost of generating the topology from the cost of choosing "
            "a dense observing set."
        ),
        example_keys=(
            "finite_discrete_n",
            "finite_indiscrete_n",
            "real_line_standard",
            "uncountable_discrete_kappa",
        ),
        exploration_notebook="notebooks/exploration/22_cardinal_functions_framework.ipynb",
        teaching_notebook="notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb",
        examples_bank="examples_bank/cardinal_functions_framework_examples.md",
        manuscript_chapter="manuscript/volume_2/chapters/29_cardinal_functions_framework.tex",
        task_prompts=(
            "For each example, state which witness controls w(X) and which witness controls d(X).",
            "Identify at least one example where topology, not only carrier size, changes the answer.",
            "Explain why d(X) <= w(X) is a comparison theorem rather than a definition.",
        ),
        expected_distinctions=(
            "base witness versus dense-subset witness",
            "finite exact calculation versus theorem-backed infinite pattern",
            "same carrier size does not force same cardinal-function profile",
        ),
        warning_notes=("Do not collapse weight and density merely because they agree in R.",),
    ),
    CardinalFunctionComparisonRoute(
        route_id="character_vs_weight",
        title="Pointwise character versus global weight",
        comparison_pair=("character", "weight"),
        objective=(
            "Show how local base control can stay small while global topological "
            "complexity grows."
        ),
        example_keys=(
            "finite_discrete_n",
            "uncountable_discrete_kappa",
            "one_point_compactification_discrete_kappa",
            "sorgenfrey_line_warning",
        ),
        exploration_notebook="notebooks/exploration/22_cardinal_functions_framework.ipynb",
        teaching_notebook="notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb",
        examples_bank="examples_bank/cardinal_functions_framework_examples.md",
        manuscript_chapter="manuscript/volume_2/chapters/29_cardinal_functions_framework.tex",
        task_prompts=(
            "Mark which data are pointwise and which data are global.",
            "Use an uncountable discrete pattern to separate small local character from large weight.",
            "Explain why chi(X) <= w(X) has a direction."
        ),
        expected_distinctions=(
            "local-base data versus global-base data",
            "isolated points versus compactification point",
            "inequality direction must be justified",
        ),
        warning_notes=("Small local behaviour is not a promise of small global weight.",),
    ),
    CardinalFunctionComparisonRoute(
        route_id="density_vs_cellularity_spread",
        title="Density versus cellularity and spread",
        comparison_pair=("density", "cellularity/spread"),
        objective=(
            "Use witnesses for dense sets, pairwise disjoint open families, and "
            "discrete subspaces without mixing their definitions."
        ),
        example_keys=(
            "finite_discrete_n",
            "countable_discrete",
            "uncountable_discrete_kappa",
            "real_line_standard",
        ),
        exploration_notebook="notebooks/exploration/22_cardinal_functions_framework.ipynb",
        teaching_notebook="notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb",
        examples_bank="examples_bank/cardinal_functions_framework_examples.md",
        manuscript_chapter="manuscript/volume_2/chapters/29_cardinal_functions_framework.tex",
        task_prompts=(
            "For each example, write one dense-set witness and one cellularity/spread witness.",
            "Decide which witness is an open-family witness and which witness is a subset witness.",
            "Explain why separability alone is not a definition of c(X) or s(X).",
        ),
        expected_distinctions=(
            "dense subset versus disjoint open family",
            "cellularity versus spread",
            "equality examples versus warning examples",
        ),
        warning_notes=("The comparison route teaches witness type before theorem memorization.",),
    ),
    CardinalFunctionComparisonRoute(
        route_id="metric_second_countable_guard",
        title="Metric examples with explicit second-countability guard",
        comparison_pair=("metric", "second_countable"),
        objective=(
            "Prevent the unsafe shortcut from 'metric' to 'countable base' by keeping "
            "the second-countability hypothesis visible."
        ),
        example_keys=(
            "second_countable_metric_safe",
            "cantor_compact_metric",
            "real_line_standard",
        ),
        exploration_notebook="notebooks/exploration/22_cardinal_functions_framework.ipynb",
        teaching_notebook="notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb",
        examples_bank="examples_bank/cardinal_functions_framework_examples.md",
        manuscript_chapter="manuscript/volume_2/chapters/29_cardinal_functions_framework.tex",
        task_prompts=(
            "Underline the exact assumption that gives a countable base.",
            "Record which cardinal functions become countably bounded under that assumption.",
            "State what the route refuses to conclude for arbitrary metric spaces."
        ),
        expected_distinctions=(
            "metric structure versus second-countable structure",
            "safe theorem-backed pattern versus overgeneralization",
            "compactness control versus countable-base control",
        ),
        warning_notes=("This is a guard route; its main job is to block an invalid shortcut.",),
    ),
    CardinalFunctionComparisonRoute(
        route_id="compactness_vs_small_cardinals",
        title="Compactness versus small cardinal-function values",
        comparison_pair=("compactness", "small_cardinal_values"),
        objective=(
            "Keep compact open-cover behaviour separate from small weight, density, "
            "network weight, and cellularity claims."
        ),
        example_keys=(
            "cantor_compact_metric",
            "one_point_compactification_discrete_kappa",
        ),
        exploration_notebook="notebooks/exploration/22_cardinal_functions_framework.ipynb",
        teaching_notebook="notebooks/teaching/lesson_11_cardinal_functions_framework.ipynb",
        examples_bank="examples_bank/cardinal_functions_framework_examples.md",
        manuscript_chapter="manuscript/volume_2/chapters/29_cardinal_functions_framework.tex",
        task_prompts=(
            "Write exactly which compactness fact is being used.",
            "Compare compact metric and one-point compactification patterns.",
            "Explain why compactness alone does not force a countable base."
        ),
        expected_distinctions=(
            "cover compactness versus base size",
            "compact metric safe zone versus compactification warning zone",
            "local behaviour at isolated points versus behaviour at infinity",
        ),
        warning_notes=("Compactness is not a synonym for second-countability.",),
    ),
)

def _norm(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def cardinal_function_examples_catalog() -> tuple[dict[str, Any], ...]:
    """Return all cardinal-function example records through v0.1.72."""

    return tuple(example.to_dict() for example in _EXAMPLES)


def cardinal_function_example(key: str) -> dict[str, Any]:
    """Return a single cardinal-function example by key."""

    normalized = _norm(key)
    for example in _EXAMPLES:
        if example.key == normalized:
            return example.to_dict()
    raise CardinalFunctionExampleError(f"Unknown cardinal-function example: {key!r}")


def cardinal_function_examples_by_layer(layer: str | None = None):
    """Group examples by pedagogical layer, or return one layer."""

    grouped: dict[str, list[dict[str, Any]]] = {}
    for example in _EXAMPLES:
        grouped.setdefault(example.layer, []).append(example.to_dict())
    if layer is None:
        return {name: tuple(rows) for name, rows in sorted(grouped.items())}
    normalized = _norm(layer)
    if normalized not in grouped:
        raise CardinalFunctionExampleError(f"Unknown cardinal-function example layer: {layer!r}")
    return tuple(grouped[normalized])


def cardinal_function_workbook_tasks(layer: str | None = None) -> tuple[dict[str, Any], ...]:
    """Flatten catalog records into student workbook tasks."""

    if layer is None:
        rows = cardinal_function_examples_catalog()
    else:
        rows = cardinal_function_examples_by_layer(layer)
    tasks: list[dict[str, Any]] = []
    for row in rows:
        for index, task in enumerate(row["tasks"], start=1):
            tasks.append(
                {
                    "example_key": row["key"],
                    "layer": row["layer"],
                    "task_id": f"{row['key']}::{index}",
                    "task": task,
                    "warnings": list(row["warnings"]),
                }
            )
    return tuple(tasks)


def _example_key_set() -> set[str]:
    return {example.key for example in _EXAMPLES}


def _route_lookup(route_id: str) -> CardinalFunctionComparisonRoute:
    normalized = _norm(route_id)
    for route in _COMPARISON_ROUTES:
        if route.route_id == normalized:
            return route
    raise CardinalFunctionExampleError(f"Unknown cardinal-function comparison route: {route_id!r}")


def _validate_route_examples(route: CardinalFunctionComparisonRoute) -> None:
    missing = sorted(set(route.example_keys) - _example_key_set())
    if missing:
        raise CardinalFunctionExampleError(
            f"Comparison route {route.route_id!r} references unknown examples: {missing!r}"
        )


def cardinal_function_comparison_exercises(route_id: str | None = None):
    """Return comparison-exercise routes, or one route by id.

    The records connect invariant pairs, example keys, expected distinctions and
    notebook surfaces.  They are intentionally stable teaching routes rather
    than per-version report material.
    """

    if route_id is not None:
        route = _route_lookup(route_id)
        _validate_route_examples(route)
        return route.to_dict()
    rows = []
    for route in _COMPARISON_ROUTES:
        _validate_route_examples(route)
        rows.append(route.to_dict())
    return tuple(rows)


def cardinal_function_notebook_route_alignment() -> tuple[dict[str, Any], ...]:
    """Return compact notebook alignment records for v0.1.72 routes."""

    aligned = []
    for route in _COMPARISON_ROUTES:
        _validate_route_examples(route)
        row = route.to_dict()
        aligned.append(
            {
                "route_id": row["route_id"],
                "comparison_pair": row["comparison_pair"],
                "exploration_notebook": row["notebook_route"]["exploration"],
                "teaching_notebook": row["notebook_route"]["teaching"],
                "examples_bank": row["notebook_route"]["examples_bank"],
                "manuscript_chapter": row["notebook_route"]["manuscript_chapter"],
                "example_keys": row["example_keys"],
                "student_checkpoint": row["task_prompts"][0],
                "teacher_checkpoint": row["expected_distinctions"][0],
            }
        )
    return tuple(aligned)


def analyze_cardinal_function_examples(layer: str | None = None) -> Result:
    """Return a structured report for the cardinal-function example catalog."""

    if layer is None:
        value = {
            "examples": cardinal_function_examples_catalog(),
            "layers": cardinal_function_examples_by_layer(),
            "workbook_tasks": cardinal_function_workbook_tasks(),
            "comparison_exercises": cardinal_function_comparison_exercises(),
            "notebook_route_alignment": cardinal_function_notebook_route_alignment(),
        }
        mode = "mixed"
        assumptions = [
            "Finite records are computable example contracts.",
            "Infinite records are theorem-backed reading patterns under stated assumptions.",
        ]
    else:
        normalized = _norm(layer)
        value = {
            "layer": normalized,
            "examples": cardinal_function_examples_by_layer(normalized),
            "workbook_tasks": cardinal_function_workbook_tasks(normalized),
            "comparison_exercises": tuple(
                route for route in cardinal_function_comparison_exercises()
                if any(cardinal_function_example(key)["layer"] == normalized for key in route["example_keys"])
            ),
        }
        mode = "exact" if normalized == "computable_finite" else "theorem"
        assumptions = [f"Layer restricted to {normalized!r}."]

    return Result.true(
        mode=mode,
        value=value,
        assumptions=assumptions,
        justification=[
            "v0.1.71 expanded the v0.1.70 cardinal-function framework with reusable example records.",
            "v0.1.72 aligns comparison exercises with exploration and teaching notebook routes.",
            "The module records witnesses, assumptions and warning notes instead of a per-version release surface.",
        ],
        metadata={
            "version": VERSION,
            "example_count": len(_EXAMPLES),
            "task_count": len(cardinal_function_workbook_tasks(layer)),
            "comparison_route_count": len(_COMPARISON_ROUTES),
            "layers": sorted({example.layer for example in _EXAMPLES}),
        },
    )
