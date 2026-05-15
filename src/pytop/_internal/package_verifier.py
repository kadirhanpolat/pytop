"""Reusable full-package zip verifier for release delivery.

The v1.0.311 verifier formalizes the checks that must be performed before a
short release archive such as ``v311.zip`` is offered as a downloadable full
package.  It verifies the archive itself rather than trusting a previous entry
copy operation: single internal root, duplicate-entry absence, deflate
compression for file entries, readable payloads, active-nested-zip policy, and
frozen archive-bundle integrity.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

from .result import Result


ARCHIVE_BUNDLE_PREFIX = "docs/archive/archive_history_bundle_"
ARCHIVE_BUNDLE_SUFFIX = ".zip"
ARCHIVE_MANIFEST_PREFIX = "docs/archive/archive_history_bundle_manifest_"
ARCHIVE_MANIFEST_SUFFIX = ".json"


def version_to_tag(version: str) -> str:
    """Convert ``v1.0.311`` to ``v1_0_311`` for file names."""

    return version.replace(".", "_")


def expected_root_for_version(version: str) -> str:
    """Return the expected single package root for a release version."""

    tag_without_v = version.removeprefix("v").replace(".", "_")
    return f"topology_book_ecosystem_v{tag_without_v}"


def default_required_paths(version: str) -> tuple[str, ...]:
    """Return the standard top-level release records required for ``version``."""

    tag = version_to_tag(version)
    return (
        "README.md",
        "CHANGELOG.md",
        "MANIFEST.md",
        "PROJECT_ROADMAP.md",
        "docs/current_docs_index.md",
        f"docs/roadmap/current_active_roadmap_{tag}.md",
        f"docs/roadmap/active_versioning_roadmap_{tag}.md",
        f"docs/packaging/subproject_packaging_policy_{tag}.md",
        f"docs/reorganization/docs_reorganization_status_{tag}.md",
        f"docs/releases/{tag}.md",
        "docs/archive/README.md",
        "docs/archive/archive_history_bundle_manifest_v1_0_288.json",
        "docs/archive/archive_history_bundle_v1_0_288.zip",
    )


@dataclass(frozen=True, slots=True)
class ArchiveBundleVerificationReport:
    """Verification result for a frozen evidence/history bundle."""

    path: str
    size_bytes: int
    sha256: str
    manifest_sha256: str | None
    sha256_matches_manifest: bool | None
    entry_count: int
    duplicate_entries: tuple[str, ...] = ()
    bad_test_entry: str | None = None
    unreadable_entries: tuple[str, ...] = ()
    non_deflated_files: tuple[str, ...] = ()
    data_descriptor_entries: tuple[str, ...] = ()
    error: str | None = None

    @property
    def is_ready(self) -> bool:
        return (
            self.error is None
            and self.bad_test_entry is None
            and not self.duplicate_entries
            and not self.unreadable_entries
            and not self.non_deflated_files
            and not self.data_descriptor_entries
            and self.sha256_matches_manifest is not False
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "manifest_sha256": self.manifest_sha256,
            "sha256_matches_manifest": self.sha256_matches_manifest,
            "entry_count": self.entry_count,
            "duplicate_entries": list(self.duplicate_entries),
            "bad_test_entry": self.bad_test_entry,
            "unreadable_entries": list(self.unreadable_entries),
            "non_deflated_files": list(self.non_deflated_files),
            "data_descriptor_entries": list(self.data_descriptor_entries),
            "error": self.error,
            "is_ready": self.is_ready,
        }


@dataclass(frozen=True, slots=True)
class PackageVerificationReport:
    """Full-package zip verification report."""

    version: str
    zip_path: str
    size_bytes: int
    expected_root: str
    root_names: tuple[str, ...]
    entry_count: int
    file_count: int
    folder_count: int
    sha256: str
    duplicate_entries: tuple[str, ...] = ()
    bad_test_entry: str | None = None
    unreadable_entries: tuple[str, ...] = ()
    non_deflated_files: tuple[str, ...] = ()
    data_descriptor_entries: tuple[str, ...] = ()
    missing_required_paths: tuple[str, ...] = ()
    active_nested_zip_violations: tuple[str, ...] = ()
    archive_bundle_reports: tuple[ArchiveBundleVerificationReport, ...] = ()
    error: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def single_root_ok(self) -> bool:
        return self.root_names == (self.expected_root,)

    @property
    def compression_ok(self) -> bool:
        return not self.non_deflated_files and not self.data_descriptor_entries

    @property
    def archive_bundles_ok(self) -> bool:
        return all(report.is_ready for report in self.archive_bundle_reports)

    @property
    def blocker_count(self) -> int:
        return (
            (1 if self.error else 0)
            + (0 if self.single_root_ok else 1)
            + len(self.duplicate_entries)
            + (1 if self.bad_test_entry else 0)
            + len(self.unreadable_entries)
            + len(self.non_deflated_files)
            + len(self.data_descriptor_entries)
            + len(self.missing_required_paths)
            + len(self.active_nested_zip_violations)
            + sum(0 if report.is_ready else 1 for report in self.archive_bundle_reports)
        )

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
                value="package verification ready",
                assumptions=(
                    "the given zip path is the candidate full-package release archive",
                    "active nested zips are forbidden except the frozen docs/archive history bundle",
                ),
                justification=(
                    "archive opened with zipfile and testzip() passed",
                    "all file entries were readable",
                    "single internal root, deflate compression, and archive-bundle checks passed",
                ),
                metadata=self.to_dict(),
            )
        return Result.conditional(
            mode="mixed",
            value="package verification has blockers",
            assumptions=("all blockers must be resolved before release delivery",),
            justification=(
                f"single_root_ok={self.single_root_ok}",
                f"duplicate_entries={list(self.duplicate_entries)}",
                f"bad_test_entry={self.bad_test_entry}",
                f"missing_required_paths={list(self.missing_required_paths)}",
                f"active_nested_zip_violations={list(self.active_nested_zip_violations)}",
                f"blocker_count={self.blocker_count}",
            ),
            metadata=self.to_dict(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "zip_path": self.zip_path,
            "size_bytes": self.size_bytes,
            "expected_root": self.expected_root,
            "root_names": list(self.root_names),
            "single_root_ok": self.single_root_ok,
            "entry_count": self.entry_count,
            "file_count": self.file_count,
            "folder_count": self.folder_count,
            "sha256": self.sha256,
            "duplicate_entries": list(self.duplicate_entries),
            "bad_test_entry": self.bad_test_entry,
            "unreadable_entries": list(self.unreadable_entries),
            "non_deflated_files": list(self.non_deflated_files),
            "data_descriptor_entries": list(self.data_descriptor_entries),
            "missing_required_paths": list(self.missing_required_paths),
            "active_nested_zip_violations": list(self.active_nested_zip_violations),
            "archive_bundle_reports": [report.to_dict() for report in self.archive_bundle_reports],
            "archive_bundles_ok": self.archive_bundles_ok,
            "blocker_count": self.blocker_count,
            "status": self.status,
            "is_ready": self.is_ready,
            "error": self.error,
            "metadata": dict(self.metadata),
        }


def _sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the SHA256 digest of a file."""

    h = sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _duplicates(names: Iterable[str]) -> tuple[str, ...]:
    counts = Counter(names)
    return tuple(sorted(name for name, count in counts.items() if count > 1))


def _root_names(names: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({name.split("/", 1)[0] for name in names if name and not name.startswith("/")}))


def _rel_without_root(name: str, root: str) -> str:
    prefix = root.rstrip("/") + "/"
    return name[len(prefix):] if name.startswith(prefix) else name


def _is_allowed_archive_bundle(rel: str) -> bool:
    return rel.startswith(ARCHIVE_BUNDLE_PREFIX) and rel.endswith(ARCHIVE_BUNDLE_SUFFIX)


def _active_nested_zip_violations(names: Iterable[str], expected_root: str) -> tuple[str, ...]:
    violations: list[str] = []
    for name in names:
        rel = _rel_without_root(name, expected_root)
        if rel.endswith(".zip") and not _is_allowed_archive_bundle(rel):
            violations.append(rel)
    return tuple(sorted(violations))


def _manifest_sha_for_bundle(bundle_rel: str, manifests: Mapping[str, Mapping[str, Any]]) -> str | None:
    for manifest in manifests.values():
        if manifest.get("bundle_path") == bundle_rel:
            value = manifest.get("bundle_sha256")
            return str(value) if value is not None else None
    return None


def _verify_archive_bundle_from_bytes(
    *,
    bundle_rel: str,
    data: bytes,
    manifest_sha256: str | None,
) -> ArchiveBundleVerificationReport:
    digest = _sha256_bytes(data)
    try:
        with ZipFile(BytesIO(data)) as bundle:
            names = bundle.namelist()
            duplicates = _duplicates(names)
            bad = bundle.testzip()
            unreadable: list[str] = []
            for name in names:
                try:
                    bundle.read(name)
                except Exception as exc:  # pragma: no cover - defensive path
                    unreadable.append(f"{name}: {exc}")
            non_deflated = tuple(
                sorted(info.filename for info in bundle.infolist() if not info.is_dir() and info.compress_type != ZIP_DEFLATED)
            )
            data_descriptor = tuple(
                sorted(info.filename for info in bundle.infolist() if not info.is_dir() and (info.flag_bits & 0x08))
            )
            return ArchiveBundleVerificationReport(
                path=bundle_rel,
                size_bytes=len(data),
                sha256=digest,
                manifest_sha256=manifest_sha256,
                sha256_matches_manifest=(digest == manifest_sha256) if manifest_sha256 else None,
                entry_count=len(names),
                duplicate_entries=duplicates,
                bad_test_entry=bad,
                unreadable_entries=tuple(unreadable),
                non_deflated_files=non_deflated,
                data_descriptor_entries=data_descriptor,
            )
    except BadZipFile as exc:
        return ArchiveBundleVerificationReport(
            path=bundle_rel,
            size_bytes=len(data),
            sha256=digest,
            manifest_sha256=manifest_sha256,
            sha256_matches_manifest=(digest == manifest_sha256) if manifest_sha256 else None,
            entry_count=0,
            error=str(exc),
        )


def verify_full_package_zip(
    zip_path: str | Path,
    *,
    expected_version: str,
    expected_root: str | None = None,
    required_paths: Iterable[str] | None = None,
) -> PackageVerificationReport:
    """Verify a full-package release zip before delivery.

    Parameters
    ----------
    zip_path:
        Candidate archive path.
    expected_version:
        Release version label such as ``v1.0.311``.
    expected_root:
        Expected single internal root. If omitted, it is derived from the
        version label.
    required_paths:
        Paths that must exist under the internal root. If omitted, the standard
        v1.0.x release record set is required.
    """

    path = Path(zip_path)
    root = expected_root or expected_root_for_version(expected_version)
    req_paths = tuple(required_paths) if required_paths is not None else default_required_paths(expected_version)

    if not path.exists():
        return PackageVerificationReport(
            version=expected_version,
            zip_path=str(path),
            size_bytes=0,
            expected_root=root,
            root_names=(),
            entry_count=0,
            file_count=0,
            folder_count=0,
            sha256="",
            error="zip path does not exist",
        )

    size = path.stat().st_size
    digest = sha256_file(path) if size else ""
    if size <= 0:
        return PackageVerificationReport(
            version=expected_version,
            zip_path=str(path),
            size_bytes=size,
            expected_root=root,
            root_names=(),
            entry_count=0,
            file_count=0,
            folder_count=0,
            sha256=digest,
            error="zip path is empty",
        )

    try:
        with ZipFile(path) as zf:
            names = zf.namelist()
            roots = _root_names(names)
            infos = zf.infolist()
            duplicates = _duplicates(names)
            bad = zf.testzip()
            unreadable: list[str] = []
            for name in names:
                try:
                    zf.read(name)
                except Exception as exc:  # pragma: no cover - defensive path
                    unreadable.append(f"{name}: {exc}")
            non_deflated = tuple(
                sorted(info.filename for info in infos if not info.is_dir() and info.compress_type != ZIP_DEFLATED)
            )
            data_descriptor = tuple(
                sorted(info.filename for info in infos if not info.is_dir() and (info.flag_bits & 0x08))
            )
            required_full = tuple(f"{root}/{rel}" for rel in req_paths)
            missing = tuple(rel for rel, full in zip(req_paths, required_full) if full not in names)
            nested_violations = _active_nested_zip_violations(names, root)

            manifests: dict[str, Mapping[str, Any]] = {}
            for name in names:
                rel = _rel_without_root(name, root)
                if rel.startswith(ARCHIVE_MANIFEST_PREFIX) and rel.endswith(ARCHIVE_MANIFEST_SUFFIX):
                    try:
                        manifests[rel] = json.loads(zf.read(name).decode("utf-8"))
                    except Exception:
                        manifests[rel] = {}

            bundle_reports: list[ArchiveBundleVerificationReport] = []
            for name in names:
                rel = _rel_without_root(name, root)
                if _is_allowed_archive_bundle(rel):
                    data = zf.read(name)
                    bundle_reports.append(
                        _verify_archive_bundle_from_bytes(
                            bundle_rel=rel,
                            data=data,
                            manifest_sha256=_manifest_sha_for_bundle(rel, manifests),
                        )
                    )

            return PackageVerificationReport(
                version=expected_version,
                zip_path=str(path),
                size_bytes=size,
                expected_root=root,
                root_names=roots,
                entry_count=len(names),
                file_count=sum(1 for info in infos if not info.is_dir()),
                folder_count=len({str(Path(name).parent) for name in names if name and not name.endswith("/")}),
                sha256=digest,
                duplicate_entries=duplicates,
                bad_test_entry=bad,
                unreadable_entries=tuple(unreadable),
                non_deflated_files=non_deflated,
                data_descriptor_entries=data_descriptor,
                missing_required_paths=missing,
                active_nested_zip_violations=nested_violations,
                archive_bundle_reports=tuple(bundle_reports),
                metadata={"required_path_count": len(req_paths)},
            )
    except BadZipFile as exc:
        return PackageVerificationReport(
            version=expected_version,
            zip_path=str(path),
            size_bytes=size,
            expected_root=root,
            root_names=(),
            entry_count=0,
            file_count=0,
            folder_count=0,
            sha256=digest,
            error=str(exc),
        )


def package_verifier_summary(
    zip_path: str | Path,
    *,
    expected_version: str,
    expected_root: str | None = None,
    required_paths: Iterable[str] | None = None,
) -> str:
    """Return a compact delivery-verification summary."""

    report = verify_full_package_zip(
        zip_path,
        expected_version=expected_version,
        expected_root=expected_root,
        required_paths=required_paths,
    )
    return (
        f"{report.version}: status={report.status}; "
        f"root={list(report.root_names)}; "
        f"entries={report.entry_count}; files={report.file_count}; folders={report.folder_count}; "
        f"blockers={report.blocker_count}; sha256={report.sha256}"
    )
