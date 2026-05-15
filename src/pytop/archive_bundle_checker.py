"""Archive-bundle checker for frozen evidence/history bundles.

The v1.0.314 checker focuses on the only nested zip that the single-package
model permits: ``docs/archive/archive_history_bundle_v1_0_288.zip``.  It works
on an extracted package root and verifies the frozen bundle against its JSON
manifest and SHA256 sidecar without treating it as an active source surface.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

from .result import Result


DEFAULT_BUNDLE_REL = "docs/archive/archive_history_bundle_v1_0_288.zip"
DEFAULT_MANIFEST_REL = "docs/archive/archive_history_bundle_manifest_v1_0_288.json"
DEFAULT_SHA256_REL = "docs/archive/archive_history_bundle_sha256_v1_0_288.txt"


@dataclass(frozen=True, slots=True)
class ArchiveBundleCheckReport:
    """Verification report for a frozen archive/evidence bundle."""

    version: str
    package_root: str
    bundle_rel: str
    manifest_rel: str
    sha256_rel: str
    bundle_exists: bool
    manifest_exists: bool
    sha256_file_exists: bool
    bundle_size_bytes: int = 0
    bundle_sha256: str = ""
    sha256_file_value: str | None = None
    manifest: Mapping[str, Any] = field(default_factory=dict)
    entry_count: int = 0
    file_count: int = 0
    dir_entry_count: int = 0
    duplicate_entries: tuple[str, ...] = ()
    bad_test_entry: str | None = None
    unreadable_entries: tuple[str, ...] = ()
    compression_methods_for_files: tuple[int, ...] = ()
    non_deflated_files: tuple[str, ...] = ()
    data_descriptor_entries: tuple[str, ...] = ()
    error: str | None = None

    @property
    def manifest_bundle_path(self) -> str | None:
        value = self.manifest.get("bundle_path")
        return str(value) if value is not None else None

    @property
    def manifest_bundle_sha256(self) -> str | None:
        value = self.manifest.get("bundle_sha256")
        return str(value) if value is not None else None

    @property
    def manifest_bundle_size_bytes(self) -> int | None:
        value = self.manifest.get("bundle_size_bytes")
        return int(value) if isinstance(value, int) else None

    @property
    def manifest_bundle_file_count(self) -> int | None:
        value = self.manifest.get("bundle_file_count")
        return int(value) if isinstance(value, int) else None

    @property
    def manifest_dir_entry_count(self) -> int | None:
        value = self.manifest.get("bundle_dir_entry_count")
        return int(value) if isinstance(value, int) else None

    @property
    def manifest_duplicate_count(self) -> int | None:
        value = self.manifest.get("inner_duplicate_entries")
        return int(value) if isinstance(value, int) else None

    @property
    def manifest_data_descriptor_count(self) -> int | None:
        value = self.manifest.get("inner_data_descriptor_flag_count")
        return int(value) if isinstance(value, int) else None

    @property
    def manifest_compression_methods(self) -> tuple[int, ...] | None:
        value = self.manifest.get("inner_compression_methods_for_files")
        if isinstance(value, list) and all(isinstance(item, int) for item in value):
            return tuple(sorted(set(value)))
        return None

    @property
    def bundle_path_matches_manifest(self) -> bool:
        return self.manifest_bundle_path == self.bundle_rel

    @property
    def sha256_matches_manifest(self) -> bool:
        return self.manifest_bundle_sha256 == self.bundle_sha256

    @property
    def sha256_matches_sidecar(self) -> bool:
        return self.sha256_file_value == self.bundle_sha256

    @property
    def size_matches_manifest(self) -> bool:
        return self.manifest_bundle_size_bytes == self.bundle_size_bytes

    @property
    def file_count_matches_manifest(self) -> bool:
        return self.manifest_bundle_file_count == self.file_count

    @property
    def dir_count_matches_manifest(self) -> bool:
        return self.manifest_dir_entry_count == self.dir_entry_count

    @property
    def duplicate_count_matches_manifest(self) -> bool:
        return self.manifest_duplicate_count == len(self.duplicate_entries)

    @property
    def data_descriptor_count_matches_manifest(self) -> bool:
        return self.manifest_data_descriptor_count == len(self.data_descriptor_entries)

    @property
    def compression_methods_match_manifest(self) -> bool:
        return self.manifest_compression_methods == self.compression_methods_for_files

    @property
    def zip_payload_ok(self) -> bool:
        return (
            self.error is None
            and self.bundle_exists
            and self.bad_test_entry is None
            and not self.unreadable_entries
            and not self.duplicate_entries
            and not self.non_deflated_files
            and not self.data_descriptor_entries
        )

    @property
    def metadata_ok(self) -> bool:
        return (
            self.manifest_exists
            and self.sha256_file_exists
            and self.bundle_path_matches_manifest
            and self.sha256_matches_manifest
            and self.sha256_matches_sidecar
            and self.size_matches_manifest
            and self.file_count_matches_manifest
            and self.dir_count_matches_manifest
            and self.duplicate_count_matches_manifest
            and self.data_descriptor_count_matches_manifest
            and self.compression_methods_match_manifest
        )

    @property
    def is_ready(self) -> bool:
        return self.zip_payload_ok and self.metadata_ok

    @property
    def status(self) -> str:
        return "true" if self.is_ready else "conditional"

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "package_root": self.package_root,
            "bundle_rel": self.bundle_rel,
            "manifest_rel": self.manifest_rel,
            "sha256_rel": self.sha256_rel,
            "bundle_exists": self.bundle_exists,
            "manifest_exists": self.manifest_exists,
            "sha256_file_exists": self.sha256_file_exists,
            "bundle_size_bytes": self.bundle_size_bytes,
            "bundle_sha256": self.bundle_sha256,
            "sha256_file_value": self.sha256_file_value,
            "entry_count": self.entry_count,
            "file_count": self.file_count,
            "dir_entry_count": self.dir_entry_count,
            "duplicate_entries": list(self.duplicate_entries),
            "bad_test_entry": self.bad_test_entry,
            "unreadable_entries": list(self.unreadable_entries),
            "compression_methods_for_files": list(self.compression_methods_for_files),
            "non_deflated_files": list(self.non_deflated_files),
            "data_descriptor_entries": list(self.data_descriptor_entries),
            "manifest_bundle_path": self.manifest_bundle_path,
            "manifest_bundle_sha256": self.manifest_bundle_sha256,
            "manifest_bundle_size_bytes": self.manifest_bundle_size_bytes,
            "manifest_bundle_file_count": self.manifest_bundle_file_count,
            "manifest_dir_entry_count": self.manifest_dir_entry_count,
            "manifest_duplicate_count": self.manifest_duplicate_count,
            "manifest_data_descriptor_count": self.manifest_data_descriptor_count,
            "manifest_compression_methods": (
                list(self.manifest_compression_methods)
                if self.manifest_compression_methods is not None
                else None
            ),
            "bundle_path_matches_manifest": self.bundle_path_matches_manifest,
            "sha256_matches_manifest": self.sha256_matches_manifest,
            "sha256_matches_sidecar": self.sha256_matches_sidecar,
            "size_matches_manifest": self.size_matches_manifest,
            "file_count_matches_manifest": self.file_count_matches_manifest,
            "dir_count_matches_manifest": self.dir_count_matches_manifest,
            "duplicate_count_matches_manifest": self.duplicate_count_matches_manifest,
            "data_descriptor_count_matches_manifest": self.data_descriptor_count_matches_manifest,
            "compression_methods_match_manifest": self.compression_methods_match_manifest,
            "zip_payload_ok": self.zip_payload_ok,
            "metadata_ok": self.metadata_ok,
            "status": self.status,
            "is_ready": self.is_ready,
            "error": self.error,
        }

    def to_result(self) -> Result:
        if self.is_ready:
            return Result.true(
                mode="exact",
                value="archive bundle verification ready",
                assumptions=(
                    "the checked nested zip is a frozen docs/archive evidence bundle",
                    "the JSON manifest and SHA256 sidecar are the reference metadata",
                ),
                justification=(
                    "bundle opens, testzip() passes, and all entries are readable",
                    "bundle SHA256, size, counts, duplicate status, compression method, and data-descriptor status match manifest metadata",
                ),
                metadata=self.to_dict(),
            )
        return Result.conditional(
            mode="mixed",
            value="archive bundle verification has blockers",
            assumptions=("all archive metadata and payload blockers must be resolved before release delivery",),
            justification=(
                f"zip_payload_ok={self.zip_payload_ok}",
                f"metadata_ok={self.metadata_ok}",
                f"bad_test_entry={self.bad_test_entry}",
                f"duplicate_entries={list(self.duplicate_entries)}",
                f"data_descriptor_entries={list(self.data_descriptor_entries)}",
            ),
            metadata=self.to_dict(),
        )


def _sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _duplicates(names: Iterable[str]) -> tuple[str, ...]:
    counts = Counter(names)
    return tuple(sorted(name for name, count in counts.items() if count > 1))


def _parse_sha256_sidecar(text: str) -> str | None:
    first = text.strip().split()[0] if text.strip() else ""
    if len(first) == 64 and all(ch in "0123456789abcdefABCDEF" for ch in first):
        return first.lower()
    return None


def verify_archive_bundle(
    package_root: str | Path,
    *,
    version: str = "v1.0.314",
    bundle_rel: str = DEFAULT_BUNDLE_REL,
    manifest_rel: str = DEFAULT_MANIFEST_REL,
    sha256_rel: str = DEFAULT_SHA256_REL,
) -> ArchiveBundleCheckReport:
    """Verify the frozen archive bundle inside an extracted package root."""

    root = Path(package_root)
    bundle_path = root / bundle_rel
    manifest_path = root / manifest_rel
    sha_path = root / sha256_rel

    bundle_exists = bundle_path.is_file()
    manifest_exists = manifest_path.is_file()
    sha_exists = sha_path.is_file()

    manifest: Mapping[str, Any] = {}
    sha_text_value: str | None = None

    if manifest_exists:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            return ArchiveBundleCheckReport(
                version=version,
                package_root=str(root),
                bundle_rel=bundle_rel,
                manifest_rel=manifest_rel,
                sha256_rel=sha256_rel,
                bundle_exists=bundle_exists,
                manifest_exists=manifest_exists,
                sha256_file_exists=sha_exists,
                error=f"manifest read/parse error: {exc}",
            )

    if sha_exists:
        sha_text_value = _parse_sha256_sidecar(sha_path.read_text(encoding="utf-8"))

    if not bundle_exists:
        return ArchiveBundleCheckReport(
            version=version,
            package_root=str(root),
            bundle_rel=bundle_rel,
            manifest_rel=manifest_rel,
            sha256_rel=sha256_rel,
            bundle_exists=False,
            manifest_exists=manifest_exists,
            sha256_file_exists=sha_exists,
            sha256_file_value=sha_text_value,
            manifest=manifest,
            error="bundle path does not exist",
        )

    bundle_size = bundle_path.stat().st_size
    bundle_digest = _sha256_file(bundle_path)

    try:
        with ZipFile(bundle_path) as bundle:
            names = bundle.namelist()
            infos = bundle.infolist()
            bad = bundle.testzip()
            unreadable: list[str] = []
            for name in names:
                try:
                    bundle.read(name)
                except Exception as exc:  # pragma: no cover - defensive path
                    unreadable.append(f"{name}: {exc}")
            methods = tuple(sorted({info.compress_type for info in infos if not info.is_dir()}))
            non_deflated = tuple(
                sorted(info.filename for info in infos if not info.is_dir() and info.compress_type != ZIP_DEFLATED)
            )
            data_descriptor = tuple(
                sorted(info.filename for info in infos if not info.is_dir() and (info.flag_bits & 0x08))
            )
            return ArchiveBundleCheckReport(
                version=version,
                package_root=str(root),
                bundle_rel=bundle_rel,
                manifest_rel=manifest_rel,
                sha256_rel=sha256_rel,
                bundle_exists=True,
                manifest_exists=manifest_exists,
                sha256_file_exists=sha_exists,
                bundle_size_bytes=bundle_size,
                bundle_sha256=bundle_digest,
                sha256_file_value=sha_text_value,
                manifest=manifest,
                entry_count=len(names),
                file_count=sum(1 for info in infos if not info.is_dir()),
                dir_entry_count=sum(1 for info in infos if info.is_dir()),
                duplicate_entries=_duplicates(names),
                bad_test_entry=bad,
                unreadable_entries=tuple(unreadable),
                compression_methods_for_files=methods,
                non_deflated_files=non_deflated,
                data_descriptor_entries=data_descriptor,
            )
    except BadZipFile as exc:
        return ArchiveBundleCheckReport(
            version=version,
            package_root=str(root),
            bundle_rel=bundle_rel,
            manifest_rel=manifest_rel,
            sha256_rel=sha256_rel,
            bundle_exists=True,
            manifest_exists=manifest_exists,
            sha256_file_exists=sha_exists,
            bundle_size_bytes=bundle_size,
            bundle_sha256=bundle_digest,
            sha256_file_value=sha_text_value,
            manifest=manifest,
            error=str(exc),
        )


def render_archive_bundle_check_report(report: ArchiveBundleCheckReport) -> str:
    """Render a compact Markdown report for archive-bundle verification."""

    checks = [
        ("Bundle exists", report.bundle_exists),
        ("Manifest exists", report.manifest_exists),
        ("SHA256 sidecar exists", report.sha256_file_exists),
        ("Bundle path matches manifest", report.bundle_path_matches_manifest),
        ("SHA256 matches manifest", report.sha256_matches_manifest),
        ("SHA256 matches sidecar", report.sha256_matches_sidecar),
        ("Size matches manifest", report.size_matches_manifest),
        ("File count matches manifest", report.file_count_matches_manifest),
        ("Directory-entry count matches manifest", report.dir_count_matches_manifest),
        ("Duplicate count matches manifest", report.duplicate_count_matches_manifest),
        ("Data-descriptor count matches manifest", report.data_descriptor_count_matches_manifest),
        ("Compression methods match manifest", report.compression_methods_match_manifest),
        ("Zip payload OK", report.zip_payload_ok),
    ]
    lines = [
        f"# Archive Bundle Check Report - {report.version}",
        "",
        f"- Package root: `{report.package_root}`",
        f"- Bundle: `{report.bundle_rel}`",
        f"- Status: `{report.status}`",
        f"- Ready: `{report.is_ready}`",
        f"- SHA256: `{report.bundle_sha256}`",
        f"- Entry count: `{report.entry_count}`",
        f"- File count: `{report.file_count}`",
        f"- Directory entries: `{report.dir_entry_count}`",
        "",
        "## Checks",
        "",
        "| Check | Passed |",
        "|---|---:|",
    ]
    lines.extend(f"| {name} | {passed} |" for name, passed in checks)
    if report.error:
        lines += ["", "## Error", "", report.error]
    if report.duplicate_entries:
        lines += ["", "## Duplicate entries", ""]
        lines.extend(f"- `{name}`" for name in report.duplicate_entries)
    if report.unreadable_entries:
        lines += ["", "## Unreadable entries", ""]
        lines.extend(f"- `{name}`" for name in report.unreadable_entries)
    if report.non_deflated_files:
        lines += ["", "## Non-deflated files", ""]
        lines.extend(f"- `{name}`" for name in report.non_deflated_files)
    if report.data_descriptor_entries:
        lines += ["", "## Data-descriptor entries", ""]
        lines.extend(f"- `{name}`" for name in report.data_descriptor_entries)
    return "\n".join(lines) + "\n"


def archive_bundle_checker_summary(package_root: str | Path, *, version: str = "v1.0.314") -> str:
    """Return a one-line human-readable archive-bundle verification summary."""

    report = verify_archive_bundle(package_root, version=version)
    return (
        f"archive_bundle_checker version={version} status={report.status} "
        f"ready={report.is_ready} sha256={report.bundle_sha256} "
        f"files={report.file_count} metadata_ok={report.metadata_ok}"
    )
