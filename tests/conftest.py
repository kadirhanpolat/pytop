from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# ---------------------------------------------------------------------------
# PYTOP_REQUIRE_ORACLES=1 — a skip caused by a missing `oracles` extra package
# becomes a failure. Audit 2026-09-24 (finding 3.5): CI installed only `.[dev]`,
# so every differential-oracle test skipped on every run and a green CI said
# nothing about them. The `oracles` CI job sets this flag so that cannot recur.
# ---------------------------------------------------------------------------

import os  # noqa: E402

import pytest  # noqa: E402

_ORACLE_MARKERS = ("numpy", "sympy", "networkx", "gudhi", "flint")


def _is_missing_oracle_skip(reason: str) -> bool:
    text = reason.lower()
    missing = "not installed" in text or "could not import" in text
    return missing and any(name in text for name in _ORACLE_MARKERS)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # type: ignore[no-untyped-def]
    outcome = yield
    if os.environ.get("PYTOP_REQUIRE_ORACLES") != "1":
        return
    report = outcome.get_result()
    if report.skipped and isinstance(report.longrepr, tuple):
        reason = str(report.longrepr[2])
        if _is_missing_oracle_skip(reason):
            report.outcome = "failed"
            report.longrepr = (
                f"PYTOP_REQUIRE_ORACLES=1 but an oracle is missing: {reason}. "
                'Install it with: pip install -e ".[dev,oracles]"'
            )
