"""Command-line entry point: ``python -m pytop``.

``python -m pytop --version`` prints the installed version; a bare
``python -m pytop`` prints a short capability banner.
"""

from __future__ import annotations

import sys

from . import __version__

_BANNER = f"""\
pytop {__version__} - mathematical topology for Python

Constructive core:
  homology / cohomology, persistent homology (TDA), cubical & Cech complexes,
  discrete Morse theory, persistence distances & landscapes, Mapper,
  knot invariants (Alexander/Jones/Khovanov), graph planarity, surface
  classification, 3-manifolds.
Research layers:
  experimental.spaces (computable point-set topology),
  experimental.pi_base (pi-Base deductive inference).

Usage:
  python -m pytop --version   show the installed version
  python -m pytop             show this banner
Docs: https://github.com/kadirhanpolat/pytop
"""


def main(argv: list[str] | None = None) -> int:
    """Run the ``python -m pytop`` CLI. Returns a process exit code."""
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] in ("--version", "-V"):
        print(__version__)
        return 0
    print(_BANNER, end="")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
