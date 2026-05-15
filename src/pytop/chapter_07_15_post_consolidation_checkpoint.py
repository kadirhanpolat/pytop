"""Chapter 07--15 post-consolidation release checkpoint for v1.0.333.

This module closes the first Chapter 07--15 integration wave after the notebook
and smoke-demo synchronization layer. It verifies that the active open-folder
surfaces created in v1.0.326--v1.0.332 are present and that no active nested zip
is introduced outside the historical ``docs/archive`` evidence area.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

POST_CONSOLIDATION_CHECKPOINT_VERSION = "v1.0.333"
SOURCE_SYNC_VERSION = "v1.0.332"
CHECKPOINT_SCOPE = "Chapter 07--15 post-consolidation release checkpoint"
NEXT_EXPECTED_VERSION = "v1.0.334 first post-checkpoint insertion pass"

REQUIRED_ROOT_RECORDS = (
    "README.md",
    "MANIFEST.md",
    "PROJECT_ROADMAP.md",
    "CHANGELOG.md",
    "docs/current_docs_index.md",
)

REQUIRED_RELEASE_WAVE_RECORDS = (
    "docs/integration/chapter_07_15/chapter_12_product_spaces_integration_v1_0_326.md",
    "docs/integration/chapter_07_15/chapter_13_connectedness_integration_v1_0_327.md",
    "docs/integration/chapter_07_15/chapter_14_complete_metric_integration_v1_0_328.md",
    "docs/integration/chapter_07_15/chapter_15_function_spaces_integration_v1_0_329.md",
    "docs/integration/chapter_07_15/chapter_07_15_cross_chapter_consolidation_v1_0_330.md",
    "docs/integration/chapter_07_15/chapter_07_15_insertion_queue_v1_0_331.md",
    "docs/integration/chapter_07_15/chapter_07_15_notebook_smoke_sync_v1_0_332.md",
)

REQUIRED_ACTIVE_MODULES_AND_TESTS = (
    "src/pytop/chapter_12_product_spaces_integration.py",
    "tests/core/test_chapter_12_product_spaces_integration_v326.py",
    "src/pytop/chapter_13_connectedness_integration.py",
    "tests/core/test_chapter_13_connectedness_integration_v327.py",
    "src/pytop/chapter_14_complete_metric_integration.py",
    "tests/core/test_chapter_14_complete_metric_integration_v328.py",
    "src/pytop/chapter_15_function_spaces_integration.py",
    "tests/core/test_chapter_15_function_spaces_integration_v329.py",
    "src/pytop/chapter_07_15_cross_chapter_quality_gate.py",
    "tests/core/test_chapter_07_15_cross_chapter_quality_gate_v330.py",
    "src/pytop/chapter_07_15_insertion_queue.py",
    "tests/core/test_chapter_07_15_insertion_queue_v331.py",
    "src/pytop/chapter_07_15_notebook_smoke_sync.py",
    "tests/core/test_chapter_07_15_notebook_smoke_sync_v332.py",
)

REQUIRED_ACTIVE_SURFACE_DIRS = (
    "src/pytop",
    "tests/core",
    "docs/integration/chapter_07_15",
    "docs/verification",
    "examples_bank",
    "manuscript",
    "notebooks",
)


@dataclass(frozen=True)
class CheckpointTarget:
    path: str
    category: str
    exists: bool
    open_folder_target: bool


@dataclass(frozen=True)
class CheckpointReport:
    version: str
    source_sync_version: str
    scope: str
    required_target_count: int
    existing_target_count: int
    missing_target_count: int
    active_nested_zip_count: int
    active_surface_dir_count: int
    release_ready: bool
    targets: Tuple[CheckpointTarget, ...]
    active_nested_zips: Tuple[str, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "source_sync_version": self.source_sync_version,
            "scope": self.scope,
            "required_target_count": self.required_target_count,
            "existing_target_count": self.existing_target_count,
            "missing_target_count": self.missing_target_count,
            "active_nested_zip_count": self.active_nested_zip_count,
            "active_surface_dir_count": self.active_surface_dir_count,
            "release_ready": self.release_ready,
            "targets": [asdict(target) for target in self.targets],
            "active_nested_zips": list(self.active_nested_zips),
            "metadata": dict(self.metadata),
        }


def _is_open_folder_target(path: str) -> bool:
    normalized = f"/{path}"
    return not path.endswith(".zip") and "/docs/archive/" not in normalized


def _active_nested_zips(root: Path) -> Tuple[str, ...]:
    zips = []
    for path in root.rglob("*.zip"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("docs/archive/"):
            continue
        zips.append(rel)
    return tuple(sorted(zips))


def _make_target(root: Path, path: str, category: str) -> CheckpointTarget:
    return CheckpointTarget(
        path=path,
        category=category,
        exists=(root / path).exists(),
        open_folder_target=_is_open_folder_target(path),
    )


def build_chapter_07_15_post_consolidation_checkpoint(root: str | Path = ".") -> CheckpointReport:
    root_path = Path(root)
    targets = []
    for path in REQUIRED_ROOT_RECORDS:
        targets.append(_make_target(root_path, path, "root-record"))
    for path in REQUIRED_RELEASE_WAVE_RECORDS:
        targets.append(_make_target(root_path, path, "release-wave-record"))
    for path in REQUIRED_ACTIVE_MODULES_AND_TESTS:
        targets.append(_make_target(root_path, path, "module-or-test"))
    for path in REQUIRED_ACTIVE_SURFACE_DIRS:
        targets.append(_make_target(root_path, path, "active-surface-dir"))

    existing = sum(1 for target in targets if target.exists and target.open_folder_target)
    missing = len(targets) - existing
    nested_zips = _active_nested_zips(root_path)
    active_dirs = sum(1 for path in REQUIRED_ACTIVE_SURFACE_DIRS if (root_path / path).is_dir())
    metadata = {
        "completed_wave": "v1.0.326--v1.0.332",
        "checkpoint_role": "confirm post-consolidation release readiness before starting new insertion passes",
        "archive_policy": "docs/archive bundles are evidence-only and are excluded from active nested zip counts",
        "next_expected_version": NEXT_EXPECTED_VERSION,
    }
    return CheckpointReport(
        version=POST_CONSOLIDATION_CHECKPOINT_VERSION,
        source_sync_version=SOURCE_SYNC_VERSION,
        scope=CHECKPOINT_SCOPE,
        required_target_count=len(targets),
        existing_target_count=existing,
        missing_target_count=missing,
        active_nested_zip_count=len(nested_zips),
        active_surface_dir_count=active_dirs,
        release_ready=(missing == 0 and not nested_zips),
        targets=tuple(targets),
        active_nested_zips=nested_zips,
        metadata=metadata,
    )


def render_chapter_07_15_post_consolidation_checkpoint(report: CheckpointReport) -> str:
    lines = [
        f"# Chapter 07--15 Post-Consolidation Release Checkpoint ({report.version})",
        "",
        "This checkpoint closes the current Chapter 07--15 integration wave and records whether the package is ready for the next insertion pass.",
        "",
        f"- Source sync version: `{report.source_sync_version}`",
        f"- Required targets: `{report.required_target_count}`",
        f"- Existing open-folder targets: `{report.existing_target_count}`",
        f"- Missing targets: `{report.missing_target_count}`",
        f"- Active nested zip count: `{report.active_nested_zip_count}`",
        f"- Active surface directories: `{report.active_surface_dir_count}`",
        f"- Release ready: `{report.release_ready}`",
        "",
        "## Target groups",
    ]
    groups = {}
    for target in report.targets:
        groups.setdefault(target.category, []).append(target)
    for category, targets in sorted(groups.items()):
        ok = sum(1 for target in targets if target.exists and target.open_folder_target)
        lines.append(f"- `{category}`: `{ok}/{len(targets)}` ready")
    lines.extend([
        "",
        "## Guardrail",
        "Uploaded Chapter 07--15 zip files and `docs/archive/` bundles remain historical/evidence inputs only; active code, tests, docs, manuscript, examples_bank, and notebooks remain open-folder resources.",
        "",
        "## Next",
        f"{NEXT_EXPECTED_VERSION}.",
    ])
    return "\n".join(lines) + "\n"


__all__ = [
    "CHECKPOINT_SCOPE",
    "NEXT_EXPECTED_VERSION",
    "POST_CONSOLIDATION_CHECKPOINT_VERSION",
    "SOURCE_SYNC_VERSION",
    "CheckpointReport",
    "CheckpointTarget",
    "build_chapter_07_15_post_consolidation_checkpoint",
    "render_chapter_07_15_post_consolidation_checkpoint",
]
