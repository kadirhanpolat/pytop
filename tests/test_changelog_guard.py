"""Guard: every stable (>= 1.0.0) release tag has a CHANGELOG section (issue #11).

`CHANGELOG.md` follows Keep a Changelog with ``## [X.Y.Z]`` headings. This test
parses ``git tag`` and asserts that every ``vX.Y.Z`` tag on the stable 1.x line
has a matching heading. Pre-1.0 internal milestones (``v0.*``) are a documented
skip — they predate the public CHANGELOG discipline.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "CHANGELOG.md"


def _git_tags() -> list[str]:
    try:
        out = subprocess.run(
            ["git", "tag"], cwd=REPO_ROOT, capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [t.strip() for t in out.stdout.splitlines() if t.strip()]


def test_every_stable_tag_has_changelog_section() -> None:
    tags = _git_tags()
    if not tags:
        pytest.skip("no git tags available (e.g. shallow CI checkout)")

    headings = set(
        re.findall(r"^## \[(\d+\.\d+\.\d+)\]", CHANGELOG.read_text(encoding="utf-8"), re.M)
    )
    missing = []
    for tag in tags:
        ver = tag.lstrip("v")
        if not re.fullmatch(r"\d+\.\d+\.\d+", ver):
            continue
        if int(ver.split(".")[0]) < 1:
            continue  # pre-1.0 internal milestones: documented skip
        if ver not in headings:
            missing.append(tag)

    assert not missing, (
        f"stable release tags without a CHANGELOG '## [X.Y.Z]' section: {missing}"
    )
