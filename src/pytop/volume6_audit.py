"""Conservative Volume 6 milestone audit helpers.

The v0.1.100 package shipped a placeholder audit that always returned
``True``. For v0.1.101 we replaced that behavior with a real gate. In
v0.1.102 the gate remained conservative, but the advanced compactifications
milestone was expected to be implemented rather than placeholder-only. In
v0.1.103 the same conservative gate also expected the dimension-theory
milestone to be implemented. In v0.1.104 the uniform-spaces milestone is
likewise expected to be implemented rather than placeholder-only. In
v0.1.105 the proximity-spaces milestone is expected to be implemented too.
In v0.1.106 the inverse-systems milestone is expected to be implemented too.
In v0.1.107 the final preservation-table query-helper milestone is expected
to be implemented as well. In v0.1.108 the same conservative gate remains
closed, while the surrounding route/docs cleanup should leave the fixed-surface
record chain synchronized to the new package version.

1. whether the fixed-surface package records are internally consistent,
2. whether the advanced Volume 6 topic modules still look like constant
   stubs rather than implemented surfaces.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_VERSION = "0.1.108"


@dataclass(frozen=True, slots=True)
class Volume6Milestone:
    """One auditable milestone in the advanced roadmap band."""

    key: str
    summary: str
    status: bool
    notes: tuple[str, ...]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_module_ast(path: Path) -> ast.Module:
    return ast.parse(_read_text(path), filename=str(path))


def _function_body_without_docstring(node: ast.FunctionDef) -> list[ast.stmt]:
    body = list(node.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    return body


def _function_node(path: Path, func_name: str) -> ast.FunctionDef | None:
    tree = _load_module_ast(path)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node
    return None


def _is_constant_stub_return(expr: ast.AST, *, allow_false: bool = True) -> bool:
    if isinstance(expr, ast.Constant):
        if expr.value is None:
            return True
        if allow_false and expr.value is False:
            return True
        if expr.value is True:
            return True
    if (
        isinstance(expr, ast.Call)
        and isinstance(expr.func, ast.Name)
        and expr.func.id == "Result"
        and len(expr.args) >= 2
        and isinstance(expr.args[0], ast.Constant)
        and expr.args[0].value is False
        and isinstance(expr.args[1], ast.Constant)
        and expr.args[1].value == "Not implemented yet"
    ):
        return True
    return False


def _function_is_placeholder(
    path: Path,
    func_name: str,
    *,
    allow_false: bool = True,
) -> bool:
    node = _function_node(path, func_name)
    if node is None:
        return True
    body = _function_body_without_docstring(node)
    if len(body) != 1 or not isinstance(body[0], ast.Return):
        return False
    value = body[0].value
    if value is None:
        return True
    return _is_constant_stub_return(value, allow_false=allow_false)


def _fixed_surface_consistency_milestone(root: Path) -> Volume6Milestone:
    notes: list[str] = []
    expected_root = root.name
    version_files = [
        root / "pyproject.toml",
        root / "README.md",
        root / "MANIFEST.md",
        root / "PROJECT_ROADMAP.md",
        root / "docs" / "current_docs_index.md",
        root / "docs" / "status" / "current_status.md",
        root / "docs" / "status" / "test_status.md",
        root / "docs" / "status" / "verification_status.md",
        root / "docs" / "roadmap" / "current_roadmap.md",
        root / "docs" / "roadmap" / "backlog.md",
        root / "docs" / "roadmap" / "completed.md",
        root / "docs" / "roadmap" / "decision_log.md",
    ]
    status = True
    for path in version_files:
        text = _read_text(path)
        if EXPECTED_VERSION not in text:
            status = False
            notes.append(f"{path.relative_to(root)} missing {EXPECTED_VERSION}.")
    root_files = [
        root / "MANIFEST.md",
        root / "docs" / "current_docs_index.md",
        root / "docs" / "status" / "current_status.md",
        root / "docs" / "status" / "test_status.md",
        root / "docs" / "status" / "verification_status.md",
        root / "docs" / "status" / "data_preservation_status.md",
    ]
    for path in root_files:
        text = _read_text(path)
        if expected_root not in text:
            status = False
            notes.append(f"{path.relative_to(root)} missing root label {expected_root}.")
    return Volume6Milestone(
        key="fixed_surface_consistency",
        summary="fixed-surface version/root consistency",
        status=status,
        notes=tuple(notes) if notes else ("Fixed-surface files agree on version and root label.",),
    )


def _placeholder_milestone(
    *,
    root: Path,
    key: str,
    summary: str,
    module_relpath: str,
    function_names: tuple[str, ...],
    allow_false: bool = True,
) -> Volume6Milestone:
    module_path = root / module_relpath
    notes: list[str] = []
    status = True
    if not module_path.exists():
        status = False
        notes.append(f"Missing module: {module_relpath}.")
    else:
        for func_name in function_names:
            if _function_is_placeholder(module_path, func_name, allow_false=allow_false):
                status = False
                notes.append(f"{module_relpath}:{func_name} still looks like a constant stub.")
    if status:
        notes.append(f"{module_relpath} no longer looks placeholder-driven.")
    return Volume6Milestone(
        key=key,
        summary=summary,
        status=status,
        notes=tuple(notes),
    )


def _volume6_milestones(root: Path) -> list[Volume6Milestone]:
    return [
        _fixed_surface_consistency_milestone(root),
        _placeholder_milestone(
            root=root,
            key="advanced_compactifications",
            summary="v0.1.85 advanced compactifications bridge",
            module_relpath="src/pytop/advanced_compactifications.py",
            function_names=("is_cech_complete", "is_realcompact", "is_perfect_map"),
        ),
        _placeholder_milestone(
            root=root,
            key="dimension_theory",
            summary="v0.1.89-v0.1.90 dimension theory core",
            module_relpath="src/pytop/dimension_theory.py",
            function_names=(
                "ind",
                "Ind",
                "dim",
                "is_zero_dimensional",
                "has_clopen_base",
                "is_totally_disconnected",
            ),
        ),
        _placeholder_milestone(
            root=root,
            key="uniform_spaces",
            summary="v0.1.92-v0.1.94 uniform spaces core",
            module_relpath="src/pytop/uniform_spaces.py",
            function_names=(
                "is_uniform_space",
                "entourage_system",
                "is_uniformly_continuous",
                "is_cauchy_filter",
                "is_uniformly_complete",
            ),
        ),
        _placeholder_milestone(
            root=root,
            key="proximity_spaces",
            summary="v0.1.95-v0.1.96 proximity spaces core",
            module_relpath="src/pytop/proximity_spaces.py",
            function_names=("is_proximity_space", "is_close", "smirnov_compactification"),
        ),
        _placeholder_milestone(
            root=root,
            key="inverse_systems",
            summary="v0.1.97 inverse systems core",
            module_relpath="src/pytop/inverse_systems.py",
            function_names=("inverse_system", "inverse_limit"),
        ),
        _placeholder_milestone(
            root=root,
            key="preservation_tables",
            summary="v0.1.99 preservation table queries",
            module_relpath="src/pytop/preservation_tables.py",
            function_names=("get_preservation_by_continuous_maps", "get_preservation_by_products"),
        ),
    ]


def volume6_audit_report() -> dict[str, Any]:
    """Return a structured report for the current advanced milestone state."""
    root = _project_root()
    milestones = _volume6_milestones(root)
    incomplete = [m.key for m in milestones if not m.status]
    return {
        "expected_version": EXPECTED_VERSION,
        "project_root": str(root),
        "all_complete": not incomplete,
        "incomplete_milestones": incomplete,
        "milestones": {
            m.key: {
                "summary": m.summary,
                "status": "true" if m.status else "false",
                "notes": list(m.notes),
            }
            for m in milestones
        },
    }


def volume6_incomplete_milestones() -> list[str]:
    """List the milestone keys that still fail the conservative audit."""
    report = volume6_audit_report()
    return list(report["incomplete_milestones"])


def render_volume6_audit_report() -> str:
    """Render a human-readable summary of the conservative Volume 6 audit."""
    report = volume6_audit_report()
    lines = [
        f"Volume 6 audit for {report['expected_version']}",
        f"Project root: {report['project_root']}",
        "Overall status: " + ("COMPLETE" if report["all_complete"] else "INCOMPLETE"),
    ]
    for key, milestone in report["milestones"].items():
        lines.append(f"- {key}: {milestone['status']} -- {milestone['summary']}")
        for note in milestone["notes"]:
            lines.append(f"  * {note}")
    return "\n".join(lines)


def audit_volume_6_completeness() -> bool:
    """Return ``True`` only when all conservative audit milestones pass."""
    return not volume6_incomplete_milestones()
