# CLAUDE.md

## Project

`pytop` is a standalone mathematical topology library for Python 3.11+.
It provides point-set topology, knot theory, graph topology, surface classification,
3-manifolds, degree theory, cardinal functions, and more.

- **GitHub:** https://github.com/kadirhanpolat/pytop
- **License:** MIT
- **Version:** see `pyproject.toml` and `src/pytop/__init__.py` (`__version__`)

---

## Directory Structure

```
src/pytop/              ← public math API (import from here)
src/pytop/_internal/    ← internal tooling (chapter integration, audit tools, release scripts)
                          NOT exported in __init__.py, NOT part of public API
src/pytop/experimental/ ← research-stage modules (unstable API)
tests/core/             ← tests for src/pytop/
tests/experimental/     ← tests for src/pytop/experimental/
examples_bank/          ← topic-based Markdown example files (not importable)
```

---

## Commands

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest tests/ -q

# Run tests with coverage
pytest tests/ --cov=pytop --cov-report=term-missing

# Run only core tests
pytest tests/core/ -q

# Run only experimental tests
pytest tests/experimental/ -q
```

> **Python interpreter:** Always use `py -3.14` on this machine (not `python` or bare `py`).

---

## User Guide

Located at `docs/user_guide/`. Four parallel formats:

```
docs/user_guide/
  latex/              ← XeLaTeX source (main.tex, chapters/, appendix/, figures/)
  markdown/           ← Markdown files (one per chapter + solutions.md)
  python/             ← Percent-cell scripts (# %% / # %% [markdown])
  notebook/           ← Jupyter notebooks (.ipynb)
  assets/             ← Generated PNGs (ch04/, ch06/, ...)
  tools/              ← build_figures.py (TikZ→PNG pipeline)
```

**TikZ→PNG pipeline:** `py -3.14 docs/user_guide/tools/build_figures.py`
- Reads `.tikz` files from `latex/figures/`
- Compiles with `xelatex` (standalone.cls)
- Rasterizes at 300 dpi via `pdftoppm`
- Writes PNGs to `assets/chNN/`

**Pedagogical tcolorbox environments** (defined in `latex/main.tex`):

| Environment | Color | Purpose |
|-------------|-------|---------|
| `sezgi` | blue | Intuition / motivating analogy |
| `dikkat` | orange | Common mistakes / warnings |
| `nedenonemli` | green | Why this matters |
| `karsiornek` | violet | Counter-examples |

**`\ipucu{...}` macro** — renders as italic hint text in exercise lists.

**Solutions appendix:** `latex/appendix/solutions.tex` + `markdown/solutions.md` + `python/solutions.py` + `notebook/solutions.ipynb`

**Compile PDF:**
```bash
cd docs/user_guide/latex && xelatex -interaction=nonstopmode main.tex
```

**Run a chapter script:**
```bash
py -3.14 docs/user_guide/python/ch04_topological_spaces.py
```

---

## Branching Strategy

```
master          ← stable releases, tagged (v0.4.0, v0.4.1, ...)
feature/<topic> ← feature branches, merge to master via PR
```

- Never commit directly to `master`
- Tag every release: `git tag vX.Y.Z && git push origin vX.Y.Z`

---

## API Design Rules

1. **Public API lives in `src/pytop/__init__.py`** — every symbol intended for users must be explicitly exported there.

2. **`_internal/` is off-limits for users** — modules in `_internal/` must NOT appear in `__init__.py` exports. Prefix with `_` signals internal use.

3. **New experimental code goes to `src/pytop/experimental/` first** — once stable and tested, promote to core `src/pytop/` and re-export from `experimental/` for backward compatibility.

4. **No ecosystem dependencies** — `pytop_questionbank`, `pytop_pedagogy`, `pytop_publish` must NOT be imported anywhere in `src/pytop/` (not even inside try/except blocks in new code).

5. **`__version__` must be in sync** — `pyproject.toml` version and `src/pytop/__init__.py` `__version__` must always match.

---

## `pytop.experimental` Philosophy

`pytop.experimental` is the research buffer zone:
- Modules here may have unstable APIs
- Users import via `from pytop.experimental import ...`
- When a module is promoted to stable, keep it in `experimental/` as a re-export with a deprecation note
- Do not promote a module without tests

---

## Cilt / Corridor Terminology

Test files and `_internal/` modules use terminology from the original textbook
development context. This glossary decodes the key terms:

| Term | Meaning |
|------|---------|
| **Cilt** | Turkish for "volume". Cilt I–IV map to volumes of the source textbook. |
| **Cilt I** | Point-set topology foundations (sets, spaces, maps, compactness, connectedness, separation) |
| **Cilt II** | Metric spaces, completeness, counterexample atlas, preservation tables |
| **Cilt III** | Local compactness, metrization, neighborhood systems, function spaces, compactness variants |
| **Cilt IV** | Cardinal functions, cardinal numbers, ordinals, quantitative topology |
| **Corridor** | A development milestone version (e.g., `v0.1.47`) that added a specific feature set |
| **Route** | A sequence of corridors forming a complete coverage of a topic |
| **Close-out** | The final corridor that completes a cilt's coverage |
| **Route summary** | An `_internal` function that documents which corridors cover a given topic |
| **v0.X.YZ** | Internal milestone versions — not the same as the public package version (v0.4.0+) |

These terms appear in `_internal/` module names and test files (e.g.,
`test_cilt2_undergraduate_route_v050.py`). They are internal metadata only.

---

## Version Bump Checklist

1. Update `version` in `pyproject.toml`
2. Update `__version__` in `src/pytop/__init__.py`
3. Add entry to `CHANGELOG.md`
4. Commit: `git commit -m "chore: bump version to vX.Y.Z"`
5. Tag: `git tag vX.Y.Z`
6. Push: `git push origin master --tags`
