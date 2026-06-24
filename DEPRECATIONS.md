# Deprecations

This file is the single registry of deprecated public symbols in pytop, the
policy that governs them, and the migration path for each.

## Policy (P19.2)

pytop follows [Semantic Versioning](https://semver.org/). Deprecation is how we
remove or rename public API without breaking users without warning.

- **Window:** a symbol deprecated in a release stays available for **at least 18
  months** and is only removed in a subsequent **major** release. Concretely,
  symbols deprecated during the 1.x line are scheduled for removal in **2.0.0**.
- **Warning:** every deprecated symbol emits a `DeprecationWarning` on use,
  built by the internal `@deprecated` decorator
  (`src/pytop/_deprecation.py`). The message follows the project WHY-HOW-THEN
  pattern: *what* is deprecated and *since when*, *when* it will be removed, and
  *what to use instead*.
- **Docs:** the decorator prepends a `.. deprecated::` note to the symbol's
  docstring, so the deprecation shows up in `help()` and the Sphinx API
  reference.
- **No silent behavior change:** a deprecated symbol keeps its original behavior
  until removal. We never repurpose a name.

### Marking a deprecation

```python
from pytop._deprecation import deprecated

@deprecated(since="1.7.0", removed_in="2.0.0", alternative="new_function")
def old_function(...):
    ...
```

`@deprecated` works on functions, methods, and classes (warns on instantiation).
It attaches a `__deprecated__` metadata dict to functions for tooling.

### Suppressing the warning (callers)

```python
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    ...  # call deprecated API
```

## Active deprecations

| Symbol | Module | Since | Removal | Replacement |
|--------|--------|-------|---------|-------------|
| `preservation_table_lookup` | `pytop.preservation_legacy` | 1.0.0 | 2.0.0 | `preservation_tables.preservation_table()` |
| `preservation_table_row` | `pytop.preservation_legacy` | 1.0.0 | 2.0.0 | `preservation_tables.preservation_table()` |
| `preservation_table_column` | `pytop.preservation_legacy` | 1.0.0 | 2.0.0 | `preservation_tables.preservation_table()` |
| `analyze_preservation_table` | `pytop.preservation_legacy` | 1.0.0 | 2.0.0 | `preservation_tables.preservation_table()` |

### Migration: `preservation_legacy` → `preservation_tables`

The `preservation_legacy` facade returns `Result` objects for the v0.1.48
undergraduate contract. The richer `preservation_tables` module exposes the same
data directly:

```python
# Deprecated
from pytop.preservation_legacy import preservation_table_lookup
r = preservation_table_lookup("compact", "subspace")   # -> Result

# Preferred
from pytop import preservation_tables
table = preservation_tables.preservation_table()        # direct table/dict access
```

## Candidates (soft deprecations)

Symbols flagged for a *future* deprecation but **not yet** emitting a
`DeprecationWarning`. They carry only a docstring note pointing at the preferred
entry point. They graduate to **Active deprecations** (with `@deprecated`,
`since="1.7.0"`) once the 1.7.0 line opens. No behavior change in the meantime.

| Symbol | Module | Preferred | Rationale |
|--------|--------|-----------|-----------|
| `persistent_homology_optimized` | `pytop.persistent_homology_optimized` | `persistent_homology(space, method="auto")` | `persistent_homology` already defaults to twist and, since P17.3, to the size-aware `"auto"` router; the wrapper is a historical alias (`docs/API_DESIGN.md` finding #3). Identical barcodes. |

## Removed

_None yet._ Symbols removed in a major release are listed here with the version
that removed them, for historical reference.
