"""Guard: every runnable example in ``examples_bank/`` must execute cleanly.

The example bank is the first thing a new user runs, so a snippet that no longer
matches the public API is a real defect.  This test discovers every
``examples_bank/**/*.py`` file and runs it in a subprocess, asserting a clean exit.

It deliberately covers only the executable ``.py`` examples — Markdown code blocks
are illustrative and are not run here.  The examples are dependency-free (pure
``pytop`` + stdlib), so this stays green on the minimal CI environment.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples_bank"

EXAMPLE_SCRIPTS = sorted(EXAMPLES_DIR.rglob("*.py"))


@pytest.mark.skipif(not EXAMPLE_SCRIPTS, reason="no example scripts found")
@pytest.mark.parametrize("script", EXAMPLE_SCRIPTS, ids=lambda p: str(p.relative_to(EXAMPLES_DIR)))
def test_example_runs(script: Path) -> None:
    """Each example script runs to completion with exit code 0."""
    # Force UTF-8 I/O in the child so example output (e.g. "·", "²") is captured
    # consistently regardless of the host console encoding (Windows cp1252).
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
        cwd=REPO_ROOT,
        env=env,
    )
    assert result.returncode == 0, (
        f"{script.relative_to(REPO_ROOT)} failed (exit {result.returncode}):\n"
        f"{result.stderr.strip()}"
    )
