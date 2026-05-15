"""Combined release-packaging checkpoint for v1.0.315+.

This read-only module aggregates the four release-verification tools added in
v1.0.311--v1.0.314: zip package verification, release report standardization,
manifest surface checking, and frozen archive-bundle checking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .archive_bundle_checker import ArchiveBundleCheckReport, verify_archive_bundle
from .manifest_checker import ManifestCheckReport, check_manifest_surfaces
from .package_verifier import PackageVerificationReport, verify_full_package_zip
from .release_report_standard import ReleaseReportResult, run_release_report_standard
from .result import Result


@dataclass(frozen=True, slots=True)
class PackagingCheckpointReport:
    """Combined readiness report for a full-package release."""

    version: str
    zip_path: str
    package_root: str
    package_report: PackageVerificationReport
    release_report: ReleaseReportResult
    manifest_report: ManifestCheckReport
    archive_bundle_report: ArchiveBundleCheckReport
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def tool_statuses(self) -> dict[str, str]:
        return {
            "package_verifier": self.package_report.status,
            "release_report_standard": "true" if self.release_report.is_ready else "conditional",
            "manifest_checker": self.manifest_report.status,
            "archive_bundle_checker": self.archive_bundle_report.status,
        }

    @property
    def is_ready(self) -> bool:
        return all(status == "true" for status in self.tool_statuses.values())

    @property
    def status(self) -> str:
        return "true" if self.is_ready else "conditional"

    @property
    def blocker_count(self) -> int:
        return sum(1 for status in self.tool_statuses.values() if status != "true")

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "zip_path": self.zip_path,
            "package_root": self.package_root,
            "status": self.status,
            "is_ready": self.is_ready,
            "blocker_count": self.blocker_count,
            "tool_statuses": self.tool_statuses,
            "package_report": self.package_report.to_dict(),
            "release_report_summary": self.release_report.summary,
            "manifest_report": self.manifest_report.to_dict(),
            "archive_bundle_report": self.archive_bundle_report.to_dict(),
            "metadata": dict(self.metadata),
        }

    def to_result(self) -> Result:
        return Result(
            status=self.status,
            mode="exact",
            value=self.is_ready,
            justification=[
                "Combined release-packaging checkpoint executed.",
                f"Package verifier status: {self.package_report.status}.",
                f"Release report standard ready: {self.release_report.is_ready}.",
                f"Manifest checker status: {self.manifest_report.status}.",
                f"Archive bundle checker status: {self.archive_bundle_report.status}.",
            ],
            metadata=self.to_dict(),
        )


def run_packaging_checkpoint(
    zip_path: str | Path,
    package_root: str | Path,
    *,
    expected_version: str,
    expected_root: str | None = None,
    required_paths: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> PackagingCheckpointReport:
    """Run the combined packaging checkpoint."""

    zip_path = Path(zip_path)
    package_root = Path(package_root)
    package_report = verify_full_package_zip(
        zip_path,
        expected_version=expected_version,
        expected_root=expected_root,
        required_paths=required_paths,
    )
    release_report = run_release_report_standard(
        zip_path,
        expected_version=expected_version,
        expected_root=expected_root,
        required_paths=required_paths,
        metadata=metadata,
    )
    manifest_report = check_manifest_surfaces(package_root, version=expected_version)
    archive_bundle_report = verify_archive_bundle(package_root, version=expected_version)
    return PackagingCheckpointReport(
        version=expected_version,
        zip_path=str(zip_path),
        package_root=str(package_root),
        package_report=package_report,
        release_report=release_report,
        manifest_report=manifest_report,
        archive_bundle_report=archive_bundle_report,
        metadata=dict(metadata or {}),
    )


def render_packaging_checkpoint_report(report: PackagingCheckpointReport) -> str:
    """Render a Markdown summary of the combined checkpoint."""

    lines = [
        f"# Packaging Checkpoint Report - {report.version}",
        "",
        f"- Zip path: `{report.zip_path}`",
        f"- Package root: `{report.package_root}`",
        f"- Status: `{report.status}`",
        f"- Ready: `{report.is_ready}`",
        f"- Combined blocker count: `{report.blocker_count}`",
        f"- SHA256: `{report.package_report.sha256}`",
        "",
        "## Tool status table",
        "",
        "| Tool | Status | Detail |",
        "|---|---|---|",
        f"| package_verifier | `{report.package_report.status}` | blockers={report.package_report.blocker_count} |",
        f"| release_report_standard | `{'true' if report.release_report.is_ready else 'conditional'}` | checklist={report.release_report.passed_count}/{len(report.release_report.checklist)} |",
        f"| manifest_checker | `{report.manifest_report.status}` | missing={len(report.manifest_report.missing_required_paths)} |",
        f"| archive_bundle_checker | `{report.archive_bundle_report.status}` | metadata_ok={report.archive_bundle_report.metadata_ok} |",
    ]
    return "\n".join(lines) + "\n"


def packaging_checkpoint_summary(
    zip_path: str | Path,
    package_root: str | Path,
    *,
    expected_version: str,
    expected_root: str | None = None,
    required_paths: Iterable[str] | None = None,
) -> str:
    report = run_packaging_checkpoint(
        zip_path,
        package_root,
        expected_version=expected_version,
        expected_root=expected_root,
        required_paths=required_paths,
    )
    return (
        f"{report.version}: status={report.status}; "
        f"tools={report.tool_statuses}; blockers={report.blocker_count}; "
        f"sha256={report.package_report.sha256}"
    )
