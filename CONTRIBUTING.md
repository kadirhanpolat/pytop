# Contributing

## General rules
- Keep package, module, class, and function names in English.
- Keep manuscript-facing prose clear and consistent.
- Avoid mixing structural logic, pedagogy, and export concerns in the same module.
- Prefer explicit support-level reporting over silent assumptions.

## Commit discipline
- Update `CHANGELOG.md` when behavior changes.
- Update `TERMINOLOGY_GUIDE.md` when a term decision becomes stable.
- Keep `MANIFEST.md` aligned with any structural change.

## Tests
- Add or update tests in the matching layer:
  - `tests/core`
  - `tests/pedagogy`
  - `tests/publishing`
  - `tests/experimental`
