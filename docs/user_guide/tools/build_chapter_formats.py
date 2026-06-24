"""Regenerate the python (percent-cell) and notebook (.ipynb) mirror formats
from the canonical Markdown chapters.

The Markdown files under ``markdown/`` are the single source of truth. This tool
splits each chapter into cells — prose (incl. ```text output and image refs)
becomes Markdown cells, ```python fences become code cells — and writes the
matching ``python/<name>.py`` (jupytext "percent" style) and
``notebook/<name>.ipynb`` (nbformat 4.5).

Usage:
    py -3.14 docs/user_guide/tools/build_chapter_formats.py            # all chapters
    py -3.14 docs/user_guide/tools/build_chapter_formats.py ch07_compactness
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[1]
MD_DIR = GUIDE / "markdown"
PY_DIR = GUIDE / "python"
NB_DIR = GUIDE / "notebook"

_CODE_FENCE = re.compile(r"^```python\s*$")
_FENCE_END = re.compile(r"^```\s*$")
_HEADING = re.compile(r"^#{1,3} \S")


def split_cells(md: str) -> list[tuple[str, str]]:
    """Return a list of ``(kind, text)`` cells; kind is 'markdown' or 'code'."""
    lines = md.splitlines()
    cells: list[tuple[str, list[str]]] = []
    cur_kind = "markdown"
    cur: list[str] = []

    def flush() -> None:
        text = "\n".join(cur).strip("\n")
        if text.strip():
            cells.append((cur_kind, cur[:]))
        cur.clear()

    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if not in_code and _CODE_FENCE.match(line):
            flush()
            cur_kind = "code"
            in_code = True
            i += 1
            continue
        if in_code and _FENCE_END.match(line):
            flush()
            cur_kind = "markdown"
            in_code = False
            i += 1
            continue
        if not in_code and _HEADING.match(line) and cur and "".join(cur).strip():
            # start a new markdown cell at each heading for section granularity
            flush()
        cur.append(line)
        i += 1
    flush()
    return [(k, "\n".join(v).strip("\n")) for k, v in cells]


def to_percent(cells: list[tuple[str, str]]) -> str:
    out: list[str] = []
    for kind, text in cells:
        if kind == "code":
            out.append("# %%\n" + text + "\n")
        else:
            if '"""' in text:  # avoid breaking the triple-quoted wrapper
                text = text.replace('"""', "'''")
            out.append('# %% [markdown]\n"""\n' + text + '\n"""\n')
    return "\n".join(out).rstrip() + "\n"


def _src(text: str) -> list[str]:
    """nbformat cell source: list of lines, each keeping its trailing newline."""
    lines = text.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + [lines[-1]] if lines else []


def to_notebook(cells: list[tuple[str, str]]) -> dict:
    nb_cells = []
    for kind, text in cells:
        if kind == "code":
            nb_cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": _src(text),
            })
        else:
            nb_cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": _src(text),
            })
    return {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build(md_path: Path) -> None:
    cells = split_cells(md_path.read_text(encoding="utf-8"))
    name = md_path.stem
    (PY_DIR / f"{name}.py").write_text(to_percent(cells), encoding="utf-8")
    (NB_DIR / f"{name}.ipynb").write_text(
        json.dumps(to_notebook(cells), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    n_code = sum(1 for k, _ in cells if k == "code")
    print(f"  {name}: {len(cells)} cells ({n_code} code) -> python/ + notebook/")


def main() -> None:
    wanted = set(sys.argv[1:])
    targets = sorted(MD_DIR.glob("ch*.md")) + [MD_DIR / "solutions.md"]
    if wanted:
        targets = [t for t in targets if t.stem in wanted]
    for md in targets:
        if md.exists():
            build(md)
    print(f"Done: {len(targets)} chapter(s).")


if __name__ == "__main__":
    main()
