# Good First Issues (P20.3)

A curated backlog of newcomer-friendly tasks. Each is **small, self-contained,
and grounded in a real file** — no architecture knowledge required. Maintainers:
open these as GitHub issues and apply the existing `good first issue` label
(`gh issue create --label "good first issue" --title ... --body ...`).

Each entry lists **where**, **why**, and a concrete **acceptance check** so a
first-time contributor can finish it in one sitting.

| # | Title | Area |
|---|-------|------|
| 1 | Document `betti_numbers` vs `persistence_betti_numbers` return types | docs/docstring |
| 2 | Add `auto` reduction-router example to the example bank | examples |
| 3 | Verify PEP 561 `py.typed` marker ships in the wheel | packaging |
| 4 | Add `python -m pytop --version` capability banner | CLI/UX |
| 5 | Parametrize the knot-table determinant checksum over all 51 primes | tests |
| 6 | Hand-computed `persistence_entropy` regression test | tests |
| 7 | Extend WHY-HOW-THEN error messages beyond the P19.1 trio | error UX |
| 8 | Add a `cech_filtration` micro-benchmark to the benchmark suite | benchmarks |
| 9 | Run docstring doctests in CI | CI |
| 10 | Fill Sphinx "undocumented" gaps flagged by the API build | docs |
| 11 | Add a CHANGELOG entry guard test (every tag has a section) | tests |
| 12 | Cross-link `DEPRECATIONS.md` candidates in module docstrings | docs |

---

### 1. Document the Betti return-type difference
- **Where:** `betti_numbers` and `persistence_betti_numbers` docstrings.
- **Why:** `docs/API_DESIGN.md` finding #1 — one returns `tuple[int, ...]`, the
  other `dict[int, int]`. The divergence is intentional but undocumented at the
  call site.
- **Acceptance:** each docstring states its return type and *why* (contiguous vs
  sparse dimensions), cross-referencing the other.

### 2. `auto` reduction-router example
- **Where:** `examples_bank/` (TDA pipelines category).
- **Why:** P17.3 made `method="auto"` the default but there's no worked example
  showing the size-aware routing and that output is byte-identical to twist.
- **Acceptance:** a Problem/Solution/Expected example asserting identical
  barcodes for `method="auto"` vs `method="twist"` on a small Rips complex.

### 3. Confirm `py.typed` ships
- **Where:** `pyproject.toml` package-data / `src/pytop/py.typed`.
- **Why:** PEP 561 — downstream users only get pytop's type hints if the marker
  is in the built wheel.
- **Acceptance:** `py.typed` exists and a test (or `python -m build` inspection)
  confirms it is included in the sdist/wheel.

### 4. `python -m pytop --version` banner
- **Where:** new `src/pytop/__main__.py`.
- **Why:** there is no quick way to print the installed version + a one-line
  capability summary.
- **Acceptance:** `python -m pytop --version` prints `__version__`; bare
  `python -m pytop` prints a short capability banner. Covered by a test.

### 5. Parametrize the knot determinant checksum
- **Where:** `tests/validation/` knot-table tests.
- **Why:** the table has 51 primes with the invariant `|Δ(-1)| = |V(-1)| = det`.
  Existing guards check `V(1)=1` and `|Δ(1)|=1`; the determinant identity should
  be a parametrized test over **every** entry.
- **Acceptance:** one `@pytest.mark.parametrize` test iterating all 51 entries.

### 6. `persistence_entropy` regression
- **Where:** `tests/core/` persistence-distances tests.
- **Why:** lock the Shannon formula against a hand-computed value.
- **Acceptance:** a test with a 3-bar diagram whose entropy is computed by hand
  in the test comment and asserted to `pytest.approx`.

### 7. More WHY-HOW-THEN error messages
- **Where:** public functions raising `ValueError`/`TypeError`.
- **Why:** P19.1 upgraded 3 functions; `docs/P19_API_STABILITY.md` sets the
  pattern. Many validators still raise terse messages.
- **Acceptance:** pick 3–5 more validators, rewrite their messages to
  WHY-HOW-THEN with a concrete example, add/adjust tests.

### 8. `cech_filtration` micro-benchmark
- **Where:** `tests/validation/` benchmark suite (P16.1).
- **Why:** Čech (P6.1) has no performance baseline alongside Rips.
- **Acceptance:** one benchmark on a small point cloud, recorded like the
  existing Rips baselines.

### 9. Doctests in CI
- **Where:** `.github/workflows/ci.yml` + `pyproject.toml` pytest config.
- **Why:** docstring `>>>` examples are not currently executed.
- **Acceptance:** `pytest --doctest-modules src/pytop` (or a curated subset)
  runs green in CI.

### 10. Close Sphinx documentation gaps
- **Where:** docstrings flagged by the P18.2 Sphinx build.
- **Why:** some of the 225 public modules have stub or missing summaries.
- **Acceptance:** add a one-line summary + parameter docs to 5 flagged symbols.

### 11. CHANGELOG entry guard
- **Where:** `tests/` + `CHANGELOG.md`.
- **Why:** ensure every released tag has a CHANGELOG section.
- **Acceptance:** a test parsing `git tag` vs `CHANGELOG.md` headings (allow a
  documented skip-list for pre-1.0 internal milestones).

### 12. Cross-link deprecation candidates
- **Where:** module docstrings of symbols listed in `DEPRECATIONS.md`.
- **Why:** the *Candidates* table (e.g. `persistent_homology_optimized`) should
  be discoverable from the code, not only the registry.
- **Acceptance:** each candidate's module/docstring links back to
  `DEPRECATIONS.md`.
