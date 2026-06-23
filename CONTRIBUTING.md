# Contributing to pytop

`pytop` is a standalone mathematical topology library for Python 3.11+. Thanks
for considering a contribution — whether it's a bug fix, a new invariant, a
performance improvement, or documentation.

## Development setup

This project uses **Python 3.11+** (the maintainer develops on 3.14).

```bash
git clone https://github.com/kadirhanpolat/pytop
cd pytop
pip install -e ".[dev]"        # editable install + dev tooling
# optional extras: ".[oracles]" (test-only cross-checks), ".[fast]" (flint SNF)
```

Run the test suite:

```bash
pytest tests/ -q                       # full suite
pytest tests/core/ -q                  # core (src/pytop)
pytest tests/experimental/ -q          # research-stage modules
pytest tests/ --cov=pytop --cov-report=term-missing
```

## Architecture: two layers

Keep this distinction in mind — it determines where new code goes.

- **Descriptive** — `*Profile` dataclasses + `get_*_profiles()` registries that
  record curated, referenced facts about famous spaces/theorems. They *know*
  invariants; they don't compute them.
- **Constructive** — engines that *compute* invariants from raw input (homology,
  persistent homology, knot invariants, …). **New computational work should
  prefer this style.**
- **`experimental.spaces`** — the research-grade computable-space protocol.

New experimental code lands in `src/pytop/experimental/` first; promote to core
only once it is stable and tested (then keep a re-export for compatibility).

## Code style

- **PEP 8**, with **type annotations on all public function signatures.**
- Formatting/linting: **ruff** (`ruff check src/ tests/`); types: **mypy**
  (`mypy src/pytop` must be clean — it is blocking in CI).
- Prefer **immutable** data (`@dataclass(frozen=True)`, `NamedTuple`).
- **Many small, focused modules** over a few large ones (≤ ~800 lines).
- Validate inputs at boundaries; raise clear errors following the **WHY-HOW-THEN**
  pattern (what's wrong, how to fix, a concrete example). See
  `docs/P19_API_STABILITY.md`.

## API rules

1. Public API lives in `src/pytop/__init__.py` — every user-facing symbol must be
   explicitly exported there.
2. `_internal/` and underscore-prefixed modules are **not** public and must not
   appear in `__init__.py`.
3. **No runtime dependencies** in `src/pytop/` — the package is dependency-free.
   Optional accelerators (numpy, flint, cupy) must be import-guarded and never
   required. Test-only oracles live behind the `[oracles]` extra and skip when
   absent.
4. `__version__` (in `src/pytop/__init__.py`) and `pyproject.toml` must stay in
   sync.

## Tests

We aim for high coverage and, above all, **correctness you can trust**:

- Add tests in the matching layer: `tests/core/`, `tests/experimental/`, or
  `tests/validation/` (oracle/benchmark/statistical cross-checks).
- Prefer **known-answer** tests (textbook results, hand computations).
- Where possible, **cross-check against an external oracle** (GUDHI, SnapPy,
  Sage, networkx, numpy). See `tests/validation/` for the parity pattern.
- For performance PRs that change an algorithm, assert the new output is
  **byte-identical** to the old one (or matches a brute-force reference).

## Deprecations

Never remove or rename a public symbol without a deprecation. Use the
`@deprecated` decorator (`pytop._deprecation`) and add an entry to
`DEPRECATIONS.md`. The window is 18 months / next major release. See
`DEPRECATIONS.md` for the policy.

## Commits & pull requests

- **Conventional commits:** `feat:`, `fix:`, `perf:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `ci:`. Scope with the milestone when relevant, e.g.
  `perf(P17.3): ...`.
- **Never commit directly to `master`** — branch as `feature/<topic>` and open a
  PR.
- Update `CHANGELOG.md` for any behavior change.
- Fill out the PR template (summary, validation, checklist).

## Reporting issues

Use the issue templates (bug / feature / docs). A minimal reproducible example
and the expected-vs-actual result make everything faster. For open-ended
questions, use GitHub Discussions.
