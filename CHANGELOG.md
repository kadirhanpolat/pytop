# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-05-13

### Added
- Initial standalone release extracted from the pytop textbook ecosystem
- Core mathematical topology library: degree theory, embeddings, graph topology,
  digital image topology, surface classification, three-manifolds, cosmology topology,
  knot theory, cardinal functions, compactness variants, metrization
- `pytop.experimental` subpackage for research-stage modules (theorem drafts,
  special example spaces, advanced cardinal functions, research bridge profiles)
- Comprehensive test suite: 1509 tests across `tests/core/` and `tests/experimental/`
- `examples_bank/`: 83 topic-based Markdown example files

### Notes
- `pytop_pedagogy`, `pytop_publish`, and `pytop_questionbank` are intentionally
  excluded — this package contains only the mathematical core
