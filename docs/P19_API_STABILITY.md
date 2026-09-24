# Phase 19: API Stability & Ergonomics

**Status:** ✅ Complete (all three milestones shipped; P19.2 and P19.3 in commit 714b5c6)  
**Date:** 2026-06-23, milestone statuses corrected 2026-09-24  
**Focus:** Error clarity, deprecation policy, API consistency

> **Read the P19.1 caveat.** All three milestones shipped, but P19.1's stated
> target — "zero ambiguous error messages" — is **not met**. See
> *P19.1 target: not met* below for the measurement.

## Phase 19.1: Error Message Improvements ✅

### Policy

All user-facing errors follow the **WHY-HOW-THEN** pattern:

1. **WHAT:** State what went wrong (the assertion that failed)
2. **WHY:** Explain why it matters or what the constraint is
3. **HOW:** Suggest how to fix it with a concrete example

### Example (Before)
```python
raise ValueError("max_dimension must be nonnegative.")
```

### Example (After)
```python
raise ValueError(
    f"max_dimension must be nonnegative (got {max_dimension}). "
    "This sets the highest simplex dimension to include; pass 1 for edges only, "
    "2 for triangles, etc."
)
```

### Implemented in P19.1

| Function | Error | Improvement |
|----------|-------|-------------|
| `vietoris_rips_filtration()` | max_dimension validation | Added parameter explanation + example |
| `vietoris_rips_filtration()` | nonempty point set | Added FiniteMetricSpace construction example |
| `persistent_homology()` | method parameter | Added all three method descriptions + when to use each |

### P19.1 target: not met

The milestone target was "zero ambiguous error messages". It is **not** met, and
this document previously overstated both the coverage and the tests behind it.
Measured on 2026-09-24:

- `src/pytop/*.py` contains roughly **208** `raise ValueError` / `raise TypeError`
  sites. Of those, about **7** follow the WHY-HOW-THEN pattern above — the three
  listed in the table, plus a handful elsewhere. The remaining ~200 are
  single-clause assertions of the "Before" form.
- The test coverage claimed here did not exist. This section previously pointed at
  `test_error_messages_clarity()` in `tests/core/test_persistent_homology.py`, and
  the *Test Coverage* section below pointed at
  `tests/core/test_persistent_homology.py::TestErrorMessages`. **Neither symbol
  exists anywhere in `tests/`** (verified by grep). The three improved messages are
  exercised only incidentally by the surrounding `vietoris_rips_filtration` /
  `persistent_homology` tests.

P19.1 is therefore best read as *a documented pattern plus three worked examples*,
not as an audit that closed. Extending the pattern across the remaining raise
sites, and adding a real test class for it, are open follow-ups.

## Phase 19.2: Deprecation Policy ✅

### Versioning

- **Current:** v1.10.0 (Phase 12 complete; bridge family complete)
- **v2.0.0 window:** 18 months from v2.0.0 release
- **Deprecation ladder:** v1.x series has no breaking changes; v2.0.0 removes deprecated items

### Deprecation Process

1. **v1.n:** Introduce `DeprecationWarning` with replacement path
2. **v1.n+1 through v1.z:** Warning remains; replacement available
3. **v2.0.0:** Remove deprecated function entirely

### What shipped

- **`src/pytop/_deprecation.py`** — a reusable internal `@deprecated` decorator. It
  emits a WHY-HOW-THEN `DeprecationWarning` when the function is called (or the
  class instantiated), prepends a `.. deprecated::` Sphinx note to the docstring,
  and attaches `__deprecated__` metadata for programmatic discovery.
- **Applied to** the four `preservation_legacy` facades.
- **`DEPRECATIONS.md`** (repository root) is the single registry: policy, the
  **Active** table, **Candidates / soft deprecations**, **Removed**, and a
  per-symbol migration guide. There is no `docs/DEPRECATIONS.md`.

### Candidates for v2.0.0 removal

Tracked in the *Candidates / soft deprecations* section of `DEPRECATIONS.md`
rather than duplicated here. The current entry is
`persistent_homology_optimized`, a historical alias of
`persistent_homology(method="auto")` — soft-deprecated by a docstring note, with
no `DeprecationWarning` raised yet; barcodes are identical.

## Phase 19.3: API Consistency ✅

### Naming Audit

Consistent naming patterns across similar functions:

| Pattern | Examples | Status |
|---------|----------|--------|
| `persistent_*` | `persistent_homology()`, `persistent_pairs_twist()` | ✅ Consistent |
| `*_filtration` | `vietoris_rips_filtration()`, `cech_filtration()` | ✅ Consistent |
| `*_complex` | `vietoris_rips_complex()?`, `cech_complex()?` | TBD |

### Parameter Ordering

Standard parameter order across persistent homology:
1. Primary input (space, complex, or filtered complex)
2. Configuration (max_dimension, max_scale, include_zero_persistence)
3. Implementation selection (method, parallel, device)

### Return Type Consistency

| Function | Returns | Pattern |
|----------|---------|---------|
| `persistent_homology()` | `tuple[PersistencePair, ...]` | Sorted by (dim, birth, death) |
| `persistence_pairs_twist()` | `tuple[PersistencePair, ...]` | Sorted by (dim, birth, death) |
| `persistence_pairs_cohomology()` | `tuple[PersistencePair, ...]` | Sorted by (dim, birth, death) |
| `*_with_stats()` | `tuple[pairs, stats]` | Stats object for metrics |

✅ **All consistent.**

### What shipped

The full audit lives in **`docs/API_DESIGN.md`**: computational entry points,
method-selection versus dedicated functions, predicates and constructors, seven
rules for new public API, and three audit findings. Findings #1 and #2 are
documented as intentional. Finding #3 — `persistent_homology_optimized` is a
historical alias of `persistent_homology(method="auto")` — was **resolved** with a
soft-deprecation note on the wrapper docstring plus a *Candidates* entry in
`DEPRECATIONS.md`.

## Test Coverage

### Error Message Tests (P19.1) — none

There is no error-message test class. `TestErrorMessages` and
`test_error_messages_clarity` do not exist in `tests/` (grep-verified
2026-09-24); earlier revisions of this document named both. Writing one is an
open follow-up.

### Deprecation Tests (P19.2) ✅

`tests/core/test_deprecation.py` and
`tests/core/test_preservation_legacy_deprecated.py` — 30 tests: the decorator
raises `DeprecationWarning` on call and on instantiation, the message follows
WHY-HOW-THEN, the docstring gains its `.. deprecated::` note, and
`__deprecated__` metadata is attached.

### API Consistency Tests (P19.3) — none

P19.3 shipped as the `docs/API_DESIGN.md` audit and its seven rules, not as an
executable check. Nothing enforces parameter order, return types or naming
patterns at test time.

## Timeline & Roadmap

| Phase | Deliverables | Status |
|-------|--------------|--------|
| **P19.1** | Error message clarity (3 functions) | ✅ Shipped — but the "zero ambiguous error messages" target is **not** met (~7 of ~208 raise sites), and no test class covers it |
| **P19.2** | Deprecation policy doc + decorator | ✅ Complete (commit 714b5c6) — `src/pytop/_deprecation.py`, `DEPRECATIONS.md`, 30 tests |
| **P19.3** | API consistency audit + fixes | ✅ Complete (commit 714b5c6) — `docs/API_DESIGN.md`, 7 rules, 3 findings, finding #3 resolved |
| **v2.0.0 prep** | Removal candidate list + migration guide | ✅ Live in `DEPRECATIONS.md` (Candidates + per-symbol migration guide) |

## Documentation

- **API design rules & audit:** `docs/API_DESIGN.md` ✅ exists
- **Deprecation registry + migration guide:** `DEPRECATIONS.md` at the repository root ✅ exists (there is no `docs/DEPRECATIONS.md`)
- **Error message examples:** This file (reference for contributors)

## Impact

- **User experience:** Clearer error messages with actionable fixes — on the three functions in the P19.1 table; the other ~200 raise sites are unchanged
- **Adoption friction:** Reduced "I got an error, now what?" support burden on the persistence entry points specifically
- **Migration path:** Clear v1→v2 upgrade guidance (v2.0.0 phase)
