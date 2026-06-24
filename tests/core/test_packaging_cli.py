"""Packaging + CLI guards (good-first-issues #3 / #4).

- PEP 561: the ``py.typed`` marker must ship inside the installed package so
  downstream users actually receive pytop's inline type hints.
- ``python -m pytop`` must expose ``--version`` and a bare capability banner.
"""

from __future__ import annotations

from pathlib import Path

import pytop
from pytop.__main__ import main


def test_py_typed_marker_present() -> None:
    """PEP 561 marker ships next to the installed package."""
    marker = Path(pytop.__file__).parent / "py.typed"
    assert marker.is_file(), "py.typed PEP 561 marker missing from the package"


def test_cli_version(capsys) -> None:
    """``python -m pytop --version`` prints exactly the version."""
    rc = main(["--version"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == pytop.__version__


def test_cli_short_version_flag(capsys) -> None:
    rc = main(["-V"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == pytop.__version__


def test_cli_banner(capsys) -> None:
    """Bare ``python -m pytop`` prints a capability banner mentioning the version."""
    rc = main([])
    assert rc == 0
    out = capsys.readouterr().out
    assert pytop.__version__ in out
    assert "topology" in out.lower()


def test_cli_banner_is_ascii(capsys) -> None:
    """Banner must be printable on a non-UTF-8 console (e.g. Windows cp1252)."""
    main([])
    out = capsys.readouterr().out
    out.encode("cp1252")  # raises UnicodeEncodeError if a stray glyph slips in
