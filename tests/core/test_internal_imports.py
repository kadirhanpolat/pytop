"""Every ``pytop._internal`` module must import.

Audit 2026-09-24, finding 3.4: ``_internal`` is excluded from ruff, mypy,
coverage and the doctest step, so 18 of its modules shipped with a broken
``from .result import Result`` and nothing noticed. This test is the gate.
"""

from __future__ import annotations

import importlib
import pkgutil

import pytest

import pytop._internal

# Developer-only third-party dependencies, documented in CLAUDE.md. A module listed
# here is skipped only when that one package is absent; any other import error fails.
_DEV_ONLY_DEPENDENCY = {
    "pytop._internal.pi_base_compile": "yaml",  # PyYAML, for regenerating pi-Base data
}

_MODULES = sorted(
    info.name for info in pkgutil.iter_modules(pytop._internal.__path__, "pytop._internal.")
)


def test_internal_package_has_modules() -> None:
    assert len(_MODULES) >= 72


@pytest.mark.parametrize("name", _MODULES)
def test_internal_module_imports(name: str) -> None:
    if name in _DEV_ONLY_DEPENDENCY:
        pytest.importorskip(_DEV_ONLY_DEPENDENCY[name])
    importlib.import_module(name)
