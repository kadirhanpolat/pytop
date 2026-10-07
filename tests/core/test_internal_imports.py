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

_MODULES = sorted(
    info.name for info in pkgutil.iter_modules(pytop._internal.__path__, "pytop._internal.")
)


def test_internal_package_has_modules() -> None:
    assert len(_MODULES) >= 72


@pytest.mark.parametrize("name", _MODULES)
def test_internal_module_imports(name: str) -> None:
    importlib.import_module(name)
