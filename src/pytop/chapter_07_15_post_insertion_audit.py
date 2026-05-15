"""Chapter 07--15 post-insertion audit and release stabilization for v1.0.337.

The v334--v336 insertion passes moved the Chapter 07--15 sequence from a
post-consolidation checkpoint into active manuscript, examples-bank, and
questionbank target queues. This module audits that the three passes form a
contiguous release sequence, that their active code/test/doc surfaces exist,
and that no active target depends on nested zip sources or ``docs/archive``
evidence bundles.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Mapping, Tuple

POST_INSERTION_AUDIT_VERSION = "v1.0.337"
SOURCE_SEQUENCE = ("v1.0.334", "v1.0.335", "v1.0.336")
PREVIOUS_VERSION = "v1.0.336"
AUDIT_LABEL = "Chapter 07--15 post-insertion audit and release stabilization"
NEXT_EXPECTED_VERSION = "v1.0.338 release-facing manuscript/examples/questionbank stabilization"
ACTIVE_SURFACES = ("manuscript", "examples_bank", "questionbank")
EXPECTED_CHAPTER_BLOCKS = ((7, 8, 9), (10, 11, 12), (13, 14, 15))


@dataclass(frozen=True)
class AuditTarget:
    role: str
    path: str
    exists: bool
    open_folder_target: bool


@dataclass(frozen=True)
class InsertionPassAudit:
    version: str
    chapter_block: Tuple[int, ...]
    label: str
    module: AuditTarget
    test: AuditTarget
    integration_doc: AuditTarget
    verification_doc: AuditTarget
    ready: bool


@dataclass(frozen=True)
class PostInsertionAuditReport:
    version: str
    previous_version: str
    audit_label: str
    audited_versions: Tuple[str, ...]
    pass_count: int
    chapter_count: int
    target_count: int
    missing_target_count: int
    all_open_folder_targets: bool
    contiguous_chapter_blocks: bool
    release_stabilized: bool
    pass_audits: Tuple[InsertionPassAudit, ...]
    metadata: Mapping[str, object]

    def to_dict(self) -> Dict[str, object]:
        return {
            "version": self.version,
            "previous_version": self.previous_version,
            "audit_label": self.audit_label,
            "audited_versions": self.audited_versions,
            "pass_count": self.pass_count,
            "chapter_count": self.chapter_count,
            "target_count": self.target_count,
            "missing_target_count": self.missing_target_count,
            "all_open_folder_targets": self.all_open_folder_targets,
            "contiguous_chapter_blocks": self.contiguous_chapter_blocks,
            "release_stabilized": self.release_stabilized,
            "pass_audits": [asdict(item) for item in self.pass_audits],
            "metadata": dict(self.metadata),
        }


def _is_open_folder_target(path: str) -> bool:
    normalized = f"/{path}"
    return not path.endswith(".zip") and "/docs/archive/" not in normalized


def _target(root: Path, role: str, path: str) -> AuditTarget:
    return AuditTarget(
        role=role,
        path=path,
        exists=(root / path).exists(),
        open_folder_target=_is_open_folder_target(path),
    )


def default_post_insertion_pass_specs() -> Tuple[Mapping[str, object], ...]:
    """Return the three post-checkpoint insertion passes that v337 audits."""
    return (
        {
            "version": "v1.0.334",
            "chapter_block": (7, 8, 9),
            "label": "Chapter 07--09 first post-checkpoint insertion pass",
            "module": "src/pytop/chapter_07_09_first_insertion_pass.py",
            "test": "tests/core/test_chapter_07_09_first_insertion_pass_v334.py",
            "integration_doc": "docs/integration/chapter_07_15/chapter_07_09_first_insertion_pass_v1_0_334.md",
            "verification_doc": "docs/verification/chapter_07_09_first_insertion_pass_v1_0_334.md",
        },
        {
            "version": "v1.0.335",
            "chapter_block": (10, 11, 12),
            "label": "Chapter 10--12 second post-checkpoint insertion pass",
            "module": "src/pytop/chapter_10_12_second_insertion_pass.py",
            "test": "tests/core/test_chapter_10_12_second_insertion_pass_v335.py",
            "integration_doc": "docs/integration/chapter_07_15/chapter_10_12_second_insertion_pass_v1_0_335.md",
            "verification_doc": "docs/verification/chapter_10_12_second_insertion_pass_v1_0_335.md",
        },
        {
            "version": "v1.0.336",
            "chapter_block": (13, 14, 15),
            "label": "Chapter 13--15 third post-checkpoint insertion pass",
            "module": "src/pytop/chapter_13_15_third_insertion_pass.py",
            "test": "tests/core/test_chapter_13_15_third_insertion_pass_v336.py",
            "integration_doc": "docs/integration/chapter_07_15/chapter_13_15_third_insertion_pass_v1_0_336.md",
            "verification_doc": "docs/verification/chapter_13_15_third_insertion_pass_v1_0_336.md",
        },
    )


def build_post_insertion_audit_report(root: Path) -> PostInsertionAuditReport:
    pass_audits = []
    for spec in default_post_insertion_pass_specs():
        targets = {
            "module": _target(root, "module", str(spec["module"])),
            "test": _target(root, "test", str(spec["test"])),
            "integration_doc": _target(root, "integration_doc", str(spec["integration_doc"])),
            "verification_doc": _target(root, "verification_doc", str(spec["verification_doc"])),
        }
        ready = all(target.exists and target.open_folder_target for target in targets.values())
        pass_audits.append(
            InsertionPassAudit(
                version=str(spec["version"]),
                chapter_block=tuple(int(chapter) for chapter in spec["chapter_block"]),
                label=str(spec["label"]),
                module=targets["module"],
                test=targets["test"],
                integration_doc=targets["integration_doc"],
                verification_doc=targets["verification_doc"],
                ready=ready,
            )
        )

    flat_targets = [
        target
        for audit in pass_audits
        for target in (audit.module, audit.test, audit.integration_doc, audit.verification_doc)
    ]
    missing_target_count = sum(1 for target in flat_targets if not target.exists)
    all_open_folder_targets = all(target.open_folder_target for target in flat_targets)
    contiguous_chapter_blocks = tuple(audit.chapter_block for audit in pass_audits) == EXPECTED_CHAPTER_BLOCKS
    version_sequence = tuple(audit.version for audit in pass_audits)
    release_stabilized = (
        version_sequence == SOURCE_SEQUENCE
        and len(pass_audits) == 3
        and contiguous_chapter_blocks
        and missing_target_count == 0
        and all_open_folder_targets
        and all(audit.ready for audit in pass_audits)
    )
    return PostInsertionAuditReport(
        version=POST_INSERTION_AUDIT_VERSION,
        previous_version=PREVIOUS_VERSION,
        audit_label=AUDIT_LABEL,
        audited_versions=version_sequence,
        pass_count=len(pass_audits),
        chapter_count=sum(len(audit.chapter_block) for audit in pass_audits),
        target_count=len(flat_targets),
        missing_target_count=missing_target_count,
        all_open_folder_targets=all_open_folder_targets,
        contiguous_chapter_blocks=contiguous_chapter_blocks,
        release_stabilized=release_stabilized,
        pass_audits=tuple(pass_audits),
        metadata={
            "active_surfaces": ACTIVE_SURFACES,
            "expected_chapter_blocks": EXPECTED_CHAPTER_BLOCKS,
            "next_expected_version": NEXT_EXPECTED_VERSION,
            "archive_policy": "docs/archive bundles remain evidence-only and are excluded from active insertion targets",
            "packaging_policy": "single full package; active sources remain open folders",
        },
    )


def render_post_insertion_audit_report(report: PostInsertionAuditReport) -> str:
    lines = [
        "# Chapter 07--15 Post-Insertion Audit and Release Stabilization (v1.0.337)",
        "",
        "This audit checks the three post-checkpoint insertion passes before the next release-facing stabilization step.",
        "",
        "## Summary",
        f"- Previous version: `{report.previous_version}`",
        f"- Audited versions: `{', '.join(report.audited_versions)}`",
        f"- Passes: `{report.pass_count}`",
        f"- Chapters covered: `{report.chapter_count}`",
        f"- Active audit targets: `{report.target_count}`",
        f"- Missing targets: `{report.missing_target_count}`",
        f"- Open-folder targets only: `{report.all_open_folder_targets}`",
        f"- Contiguous chapter blocks: `{report.contiguous_chapter_blocks}`",
        f"- Release stabilized: `{report.release_stabilized}`",
        "",
        "## Audited insertion passes",
    ]
    for audit in report.pass_audits:
        chapters = f"{audit.chapter_block[0]:02d}--{audit.chapter_block[-1]:02d}"
        lines.append(f"- `{audit.version}` Chapter {chapters}: {audit.label}.")
        for target in (audit.module, audit.test, audit.integration_doc, audit.verification_doc):
            state = "ready" if target.exists and target.open_folder_target else "missing-or-blocked"
            lines.append(f"  - `{target.role}`: `{target.path}` ({state})")
    lines.extend([
        "",
        "## Stabilization policy",
        "The audit does not promote uploaded chapter zip files or archive bundles into active sources. Active stabilization continues through open-folder manuscript, examples_bank, questionbank, source, test, and documentation surfaces.",
        "",
        "## Next",
        "v1.0.338 release-facing manuscript/examples/questionbank stabilization.",
        "",
    ])
    return "\n".join(lines)


__all__ = [
    "ACTIVE_SURFACES",
    "AUDIT_LABEL",
    "EXPECTED_CHAPTER_BLOCKS",
    "NEXT_EXPECTED_VERSION",
    "POST_INSERTION_AUDIT_VERSION",
    "PREVIOUS_VERSION",
    "SOURCE_SEQUENCE",
    "AuditTarget",
    "InsertionPassAudit",
    "PostInsertionAuditReport",
    "build_post_insertion_audit_report",
    "default_post_insertion_pass_specs",
    "render_post_insertion_audit_report",
]
