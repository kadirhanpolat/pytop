"""Manifest and active-surface checker for full-package releases.

The v1.0.313 manifest checker complements the zip-level package verifier.  It
works on an extracted package root and verifies that the active source surfaces
expected by the single-package model are present, that key release records exist,
that the manifest mentions the preserved source surfaces, and that no active
nested zip files have entered the open-folder source tree.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .package_verifier import version_to_tag
from .result import Result


_ALLOWED_ARCHIVE_PREFIX = "docs/archive/archive_history_bundle_"
_ALLOWED_ARCHIVE_SUFFIX = ".zip"


@dataclass(frozen=True, slots=True)
class ManifestSurfaceSpec:
    """A required or optional package surface checked by the manifest checker."""

    path: str
    kind: str = "file"
    required: bool = True
    preserve: bool = False
    manifest_reference: bool = False
    note: str = ""


@dataclass(frozen=True, slots=True)
class ManifestSurfaceStatus:
    """Presence result for one surface spec."""

    spec: ManifestSurfaceSpec
    present: bool
    kind_ok: bool

    @property
    def is_ready(self) -> bool:
        return (not self.spec.required) or (self.present and self.kind_ok)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.spec.path,
            "kind": self.spec.kind,
            "required": self.spec.required,
            "preserve": self.spec.preserve,
            "manifest_reference": self.spec.manifest_reference,
            "present": self.present,
            "kind_ok": self.kind_ok,
            "is_ready": self.is_ready,
            "note": self.spec.note,
        }


@dataclass(frozen=True, slots=True)
class ManifestCheckReport:
    """Aggregate result of checking a package root against manifest surfaces."""

    version: str
    package_root: str
    manifest_path: str
    surface_statuses: tuple[ManifestSurfaceStatus, ...]
    missing_manifest_mentions: tuple[str, ...] = ()
    active_nested_zip_violations: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def missing_required_paths(self) -> tuple[str, ...]:
        return tuple(status.spec.path for status in self.surface_statuses if not status.is_ready)

    @property
    def preserved_source_paths(self) -> tuple[str, ...]:
        return tuple(status.spec.path for status in self.surface_statuses if status.spec.preserve)

    @property
    def is_ready(self) -> bool:
        return (
            not self.missing_required_paths
            and not self.missing_manifest_mentions
            and not self.active_nested_zip_violations
        )

    @property
    def status(self) -> str:
        return "true" if self.is_ready else "conditional"

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "package_root": self.package_root,
            "manifest_path": self.manifest_path,
            "surface_statuses": [status.to_dict() for status in self.surface_statuses],
            "missing_required_paths": list(self.missing_required_paths),
            "preserved_source_paths": list(self.preserved_source_paths),
            "missing_manifest_mentions": list(self.missing_manifest_mentions),
            "active_nested_zip_violations": list(self.active_nested_zip_violations),
            "status": self.status,
            "is_ready": self.is_ready,
            "metadata": dict(self.metadata),
        }

    def to_result(self) -> Result:
        if self.is_ready:
            return Result.true(
                mode="exact",
                value="manifest surfaces ready",
                assumptions=(
                    "package_root points to an extracted full-package release root",
                    "active sources must remain open folders rather than nested zips",
                ),
                justification=(
                    "all required active and preserved surfaces are present",
                    "MANIFEST.md mentions the preserved source surfaces",
                    "no active nested zip files were found",
                ),
                metadata=self.to_dict(),
            )
        return Result.conditional(
            mode="mixed",
            value="manifest surfaces have blockers",
            assumptions=("missing paths or active nested zips must be resolved before release",),
            justification=(
                f"missing_required_paths={list(self.missing_required_paths)}",
                f"missing_manifest_mentions={list(self.missing_manifest_mentions)}",
                f"active_nested_zip_violations={list(self.active_nested_zip_violations)}",
            ),
            metadata=self.to_dict(),
        )


def default_manifest_surface_specs(version: str) -> tuple[ManifestSurfaceSpec, ...]:
    """Return the standard active/preserved surfaces for a release version."""

    tag = version_to_tag(version)
    preserved_dirs = (
        "src/pytop/",
        "src/pytop_questionbank/",
        "src/pytop_pedagogy/",
        "src/pytop_publish/",
        "src/pytop_experimental/",
        "tests/",
        "docs/",
        "examples_bank/",
        "manuscript/",
        "notebooks/",
        "tools/",
    )
    release_files = (
        "README.md",
        "CHANGELOG.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "pyproject.toml",
        "docs/current_docs_index.md",
        f"docs/roadmap/current_active_roadmap_{tag}.md",
        f"docs/roadmap/active_versioning_roadmap_{tag}.md",
        f"docs/packaging/subproject_packaging_policy_{tag}.md",
        f"docs/reorganization/docs_reorganization_status_{tag}.md",
        f"docs/releases/{tag}.md",
        f"docs/verification/manifest_checker_{tag}.md",
        f"RELEASE_NOTES_{tag}.md",
        f"TEST_REPORT_{tag}.txt",
        f"UPDATE_REPORT_{tag}.txt",
        f"DATA_PRESERVATION_REPORT_{tag}.txt",
        f"VERIFY_REPORT_{tag}.txt",
    )
    return tuple(
        ManifestSurfaceSpec(path=path, kind="dir", preserve=True, manifest_reference=True)
        for path in preserved_dirs
    ) + tuple(ManifestSurfaceSpec(path=path, kind="file") for path in release_files)


def _surface_status(package_root: Path, spec: ManifestSurfaceSpec) -> ManifestSurfaceStatus:
    target = package_root / spec.path.rstrip("/")
    present = target.exists()
    if spec.kind == "dir":
        kind_ok = target.is_dir()
    elif spec.kind == "file":
        kind_ok = target.is_file()
    else:
        kind_ok = present
    return ManifestSurfaceStatus(spec=spec, present=present, kind_ok=kind_ok)


def _is_allowed_archive_zip(rel_path: str) -> bool:
    return rel_path.startswith(_ALLOWED_ARCHIVE_PREFIX) and rel_path.endswith(_ALLOWED_ARCHIVE_SUFFIX)


def _active_nested_zip_violations(package_root: Path) -> tuple[str, ...]:
    violations: list[str] = []
    for path in package_root.rglob("*.zip"):
        if not path.is_file():
            continue
        rel = path.relative_to(package_root).as_posix()
        if not _is_allowed_archive_zip(rel):
            violations.append(rel)
    return tuple(sorted(violations))


def check_manifest_surfaces(
    package_root: str | Path,
    *,
    version: str,
    surface_specs: Iterable[ManifestSurfaceSpec] | None = None,
) -> ManifestCheckReport:
    """Check active and preserved package surfaces under an extracted root."""

    root = Path(package_root)
    specs = tuple(surface_specs) if surface_specs is not None else default_manifest_surface_specs(version)
    statuses = tuple(_surface_status(root, spec) for spec in specs)
    manifest = root / "MANIFEST.md"
    manifest_text = manifest.read_text(encoding="utf-8") if manifest.is_file() else ""
    missing_mentions = tuple(
        spec.path
        for spec in specs
        if spec.manifest_reference and spec.required and spec.path.rstrip("/") not in manifest_text
    )
    return ManifestCheckReport(
        version=version,
        package_root=str(root),
        manifest_path=str(manifest),
        surface_statuses=statuses,
        missing_manifest_mentions=missing_mentions,
        active_nested_zip_violations=_active_nested_zip_violations(root) if root.exists() else (),
        metadata={
            "surface_count": len(statuses),
            "preserved_surface_count": sum(1 for status in statuses if status.spec.preserve),
        },
    )


def render_manifest_check_report(report: ManifestCheckReport) -> str:
    """Render a Markdown report for a manifest check."""

    lines = [
        f"# Manifest Check Report - {report.version}",
        "",
        f"- Package root: `{report.package_root}`",
        f"- Status: `{report.status}`",
        f"- Ready: `{report.is_ready}`",
        f"- Missing required paths: {len(report.missing_required_paths)}",
        f"- Missing MANIFEST mentions: {len(report.missing_manifest_mentions)}",
        f"- Active nested zip violations: {len(report.active_nested_zip_violations)}",
        "",
        "## Surface status",
        "",
        "| Path | Kind | Required | Preserve | Present | Kind OK |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for status in report.surface_statuses:
        lines.append(
            f"| `{status.spec.path}` | {status.spec.kind} | {status.spec.required} | "
            f"{status.spec.preserve} | {status.present} | {status.kind_ok} |"
        )
    if report.missing_manifest_mentions:
        lines += ["", "## Missing MANIFEST mentions", ""]
        lines.extend(f"- `{path}`" for path in report.missing_manifest_mentions)
    if report.active_nested_zip_violations:
        lines += ["", "## Active nested zip violations", ""]
        lines.extend(f"- `{path}`" for path in report.active_nested_zip_violations)
    return "\n".join(lines) + "\n"


def manifest_checker_summary(package_root: str | Path, *, version: str) -> str:
    """Return a compact manifest-check summary line."""

    report = check_manifest_surfaces(package_root, version=version)
    return (
        f"{report.version}: status={report.status}; "
        f"surfaces={len(report.surface_statuses)}; "
        f"missing={len(report.missing_required_paths)}; "
        f"manifest_mentions_missing={len(report.missing_manifest_mentions)}; "
        f"active_nested_zip_violations={len(report.active_nested_zip_violations)}"
    )
