# API Design & Consistency (P19.3)

This document records the naming and signature conventions of pytop's public API,
the rationale behind them, and a consistency audit with concrete findings. It is
the reference for new public symbols and for the v2.0 cleanup.

## Naming conventions

pytop's public surface follows a small set of patterns. New symbols should match
the closest existing one.

### Computational entry points

| Pattern | Meaning | Examples |
|---------|---------|----------|
| `<source>_filtration(...)` | Build a `FilteredComplex` from input | `vietoris_rips_filtration`, `cech_filtration`, `witness_filtration`, `simplicial_filtration`, `torus_filtration` |
| `persistent_homology(space, ...)` | High-level: input → persistence pairs | `persistent_homology` |
| `persistence_pairs_<method>(filtered)` | Low-level reduction on a built complex | `persistence_pairs`, `persistence_pairs_twist`, `persistence_pairs_cohomology`, `persistence_pairs_fp`, `persistence_pairs_cubical` |
| `persistent_homology_<variant>(...)` | Specialized pipeline | `persistent_homology_cech`, `persistent_homology_fp`, `persistent_homology_bitmap`, `persistent_homology_witness` |
| `<context>_betti_numbers(...)` | Betti numbers in a setting | `betti_numbers`, `cellular_betti_numbers`, `cohomology_betti_numbers`, `relative_betti_numbers`, `persistence_betti_numbers` |

### Method selection vs. dedicated functions

There are two valid ways to choose a reduction algorithm:

- **High level:** `persistent_homology(space, ..., method="twist")` — `method` ∈
  `{"twist", "standard", "cohomology"}` (default `"twist"`, see P17.2). Takes a
  *space*, builds the filtration internally.
- **Low level:** `persistence_pairs_twist(filtered)` etc. — take an
  already-built `FilteredComplex`.

This two-level split is intentional: the high-level function is the ergonomic
default; the low-level functions let advanced users reuse a filtration across
methods (e.g. the oracle parity suite) without rebuilding it.

### Predicates and constructors

- Boolean predicates read as questions: `is_planar`, `is_prime`,
  `has_finite_barcode`, `is_stable_filtration`.
- Dataclasses/types use `PascalCase`: `PersistencePair`, `FilteredComplex`,
  `TDAPipeline`, `MapperComplex`.
- Tag frozensets are `UPPER_SNAKE`: `VIETORIS_RIPS_TAGS`.

## Consistency audit findings

Patterns above are followed consistently across the persistence, homology, knot,
and graph modules. The audit surfaced the following points; all are **documented,
not yet changed** (changes are deferred to the v2.0 window via `DEPRECATIONS.md`).

1. **Betti return types differ by function.** `betti_numbers(complex)` returns a
   `tuple[int, ...]` (indexed by dimension), while `persistence_betti_numbers(pairs)`
   returns a `dict[int, int]`. Both are reasonable in context (a complex has a
   contiguous dimension range; persistence may be sparse), but the divergence is
   worth flagging. *Recommendation:* keep both; document the difference (done
   here). Do **not** silently change a return type — that would break callers.

2. **First positional parameter name varies by domain.** Persistence functions
   take `space` / `filtered`; homology takes `complex_obj`; knot functions take a
   diagram/braid. This reflects genuinely different inputs and is acceptable;
   the rule is *consistency within a domain*, not one universal name.

3. **`persistent_homology` vs `persistent_homology_optimized`.** The base function
   already routes to the twist method by default (and to the size-aware `"auto"`
   router since P17.3), so `_optimized` is effectively a historical alias.
   *Resolution:* a soft-deprecation note now lives on the wrapper's docstring and
   in `DEPRECATIONS.md` → *Candidates* (no `DeprecationWarning` yet; both produce
   identical results). It graduates to an active `@deprecated` when the 1.7.0 line
   opens.

## Rules for new public API

1. Match the closest existing naming pattern above.
2. Type-annotate every parameter and the return; keep `mypy src/pytop` clean.
3. Keyword-only (`*`) for optional/behavioral flags (`include_zero_persistence`,
   `method`); positional only for the primary mathematical input.
4. Return immutable structures (`tuple`, frozen dataclass) where practical.
5. Export from `src/pytop/__init__.py`; never expose `_internal`.
6. Validate inputs with WHY-HOW-THEN error messages (see `docs/P19_API_STABILITY.md`).
7. Any rename/removal goes through `@deprecated` + `DEPRECATIONS.md`.
