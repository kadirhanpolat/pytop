# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.3] - 2026-05-16

### Fixed
- Added remaining 124 symbols to `__all__` — `pytop/__init__.py` is now complete: every imported symbol is explicitly advertised. Covers `finite_operator_engine`, `finite_basis_engine`, `finite_map_engine`, `chaos_profiles`, `dynamical_systems`, `game_theory_profiles`, `fixed_point_profiles`, `finite_witness_diagnostics`, `subbases`, `alexandroff`, `maps`, `filters`, `order_spaces`, `preservation`, `relations`, `infinite_maps`, `order_lattice`.

## [0.5.2] - 2026-05-16

### Fixed
- Added 34 missing symbols to `__all__` (separation axioms T2–T4, infinite separation predicates, compactness variants, refinement helpers, countability renders, advanced compactification predicates, `arhangelskii_bound`, `is_neighborhood_of_point`)

### Changed
- `experimental/__init__.py`: promoted modules list updated from 4 to 10 entries
- `maturity_registry.py`: `next_action` updated to `promoted_wrapper_complete` for all 10 promoted modules

### Added
- `examples_bank/promoted_profile_modules_examples.py`: working Python examples for all 11 promoted profile modules

## [0.5.1] - 2026-05-16

### Changed
- Coverage tour: added 644 targeted tests across 50+ modules, raising overall coverage from 93% to 99.68%

### Fixed
- Resolved all 321 ruff lint errors across `src/pytop/` and `tests/` (import sorting, unused imports, bare f-strings, ambiguous variable names)
- Removed duplicate `is_totally_disconnected` export from `__init__.py`
- Removed unused `meta` variable in `unified_property.py`
- Removed unused `field` import and bare f-string in `inverse_systems.py`

## [0.5.0] - 2026-05-16

### Added — Inverse Systems (`inverse_systems.py`)
- `InverseSystemDescriptor`: structured dataclass for finite/symbolic inverse systems (spaces, bonding maps, index type)
- `compute_limit_properties`: applies inverse-limit theorems — T_n inheritance, compact Hausdorff, connectedness (surjective), totally disconnected / profinite, metrizable + second-countable
- `pro_finite_completion`: descriptor for the profinite completion of a space/group (compact, Hausdorff, totally disconnected)
- `solenoid_example`: dyadic solenoid descriptor (compact, connected, not path-connected)
- `p_adic_integers_example`: p-adic integers ℤ_p as inverse limit (compact, Hausdorff, totally disconnected, ultrametric)
- Backward-compatible `inverse_system` / `inverse_limit` now include `inferred_tags`, `justifications`, `warnings`

### Added — Uniform Spaces (`uniform_spaces.py`)
- `uniform_equivalence`: decisive check (bool|None) when spaces share an explicit type tag
- `uniform_completion_descriptor`: completion tags; totally-bounded → compact; metric → unique metric completion
- `smirnov_metrization_oracle`: applies Urysohn (second_countable + regular) and Smirnov (paracompact + locally_metrizable) metrization; reports missing conditions
- `uniform_topology_tags`: infers topological tags from uniform structure (completely_regular, separation chain, completeness)

### Added — Symbolic Convergence (`symbolic_convergence.py`) — new module
- `SymbolicNetDescriptor`: net on an infinite space via tags (index_type: chain/uncountable/directed)
- `SymbolicFilterDescriptor`: filter on an infinite space via tags (filter_type: neighborhood/ultrafilter/cofinite/principal/general)
- `net_converges_symbolically`: convergent tag → indiscrete → compact Hausdorff cluster → sequentially compact → first-countable → unknown
- `filter_converges_symbolically`: neighborhood → convergent tag → indiscrete → ultrafilter in compact → cofinite in compact T1 → compact cluster point → unknown
- `ultrafilter_theorem_descriptor`: full descriptor of the ultrafilter theorem (logical strength, Tychonoff connection, Stone-Čech connection)
- `convergence_equivalence_profile`: nets ↔ filters equivalence; sequential sufficiency for first-countable spaces
- `analyze_symbolic_convergence`: combined facade

### Added — Unified Property Dispatch (`unified_property.py`) — new module
- `analyze_property(space, property_name)`: single entry point; auto-detects finite vs infinite space; dispatches to correct analyzer
- `analyze_space(space, properties=None)`: run all or selected properties for any space
- `unified_compactness_report`, `unified_connectedness_report`, `unified_separation_report`: convenience wrappers
- `property_registry()`: returns the full property → (finite_fn, infinite_fn) dispatch map
- `is_finite_space`, `is_infinite_space`: space type detectors
- Dict inputs with `'tags'` key are automatically converted to `TopologicalSpace.symbolic()`

## [0.4.4] - 2026-05-16

### Added — Separation Axioms (`separation.py`)
- `is_urysohn` / `is_t2_5`: T2.5 (Urysohn) separation; exact for finite spaces (Hausdorff ⟹ Urysohn), theorem for metric spaces
- `is_perfectly_normal`: perfectly normal (T6) spaces; exact for finite T4, theorem for metric spaces
- Updated implication chains: T3 ⟹ T2.5 ⟹ T2, perfectly_normal ⟹ T4
- `separation_profile` now includes `urysohn` and `perfectly_normal` by default

### Added — Compactness Variants (`compactness_variants.py`)
- `is_feebly_compact`: every locally finite open cover is finite; exact for finite spaces
- `is_metacompact`: every open cover has a point-finite refinement; metrizable ⟹ metacompact
- `is_relatively_compact`: closure is compact; exact for finite, tag-based for infinite
- `is_sigma_compact`: countable union of compact sets; locally compact + second-countable ⟹ σ-compact
- `compactness_variant_profile` updated to include all 4 new variants

### Added — Connectedness (`connectedness.py`)
- `is_arc_connected`: exact for finite (only indiscrete or singleton); tag-based for infinite
- `is_totally_disconnected`: exact for finite (T1 ↔ discrete ↔ totally disconnected)
- `is_scattered`: exact for finite (T0 ↔ scattered for finite spaces)

### Added — Cardinal Functions Framework (`cardinal_functions_framework.py`)
- `arhangelskii_bound`: Arhangelskii's theorem |X| ≤ 2^{χ(X)·L(X)} with corollaries
- `_HEREDITARY_DEFINITIONS`: hd(X), hl(X), hc(X), hs(X) with full definitions
- `cardinal_functions_framework_profile` now includes `hereditary_layer`
- Arhangelskii inequality + hd/hl mutual bound added to `_COMPARISONS`

### Added — Finite Basis Engine (`finite_basis_engine.py`)
- `minimal_basis`: computes the unique minimal basis of a finite topological space (minimal open neighborhoods)
- `minimal_basis_report`: dict with topology_size, minimal_basis_size, reduction_ratio

### Added — Alexandroff / Poset Tools (`alexandroff.py`)
- `poset_mobius`: Möbius function μ(x,y) on a finite poset (recursive definition, full matrix)
- `poset_mobius_report`: summary dict with nonzero entries and count
- `poset_isomorphic`: backtracking order-isomorphism checker with degree-sequence pruning

## [0.4.3] - 2026-05-16


### Changed
- Added `__all__` to all remaining 45 public core modules (previously only 9 had it)
- Deleted empty `experimental/research_notes.py` stub

### Tests
- 58 new tests in `test_maps_extended.py`: callable mapping, all `is_*_map` shortcuts,
  `identity_map` paths, `map_taxonomy_profile`, `render_map_taxonomy_report` (both
  warning lines), embedding/quotient analysis, `initial_topology_from_maps` errors
  — `maps.py` coverage: 80% → 99.6%
- 42 new tests in `test_predicates_extended.py`: `PredicateError`, clopen symbolic
  tags, negative tags, `_as_finite_subset` variants, dict-subset tags, fallback paths
  — `predicates.py` coverage: 76% → 95%
- 23 new tests in `test_sequences_extended.py`: symbolic-space fallbacks, empty
  sequence, out-of-carrier terms, invalid topology handling, `analyze_sequences`
  subset path — `sequences.py` coverage: 81% → 99%
- 35 new tests in `test_subspaces_quotients.py`: finite/symbolic subspace (closed,
  open, dense flags), `finite_subspace` TypeError, string/symbolic quotient paths,
  `quotient_space_from_map` finite+symbolic, `make_quotient_map` finite+no-mapping,
  `analyze_quotient_map` finite+symbolic dispatch — both modules reach 100%
- 41 new tests in `test_dimension_theory.py`: `ind`/`Ind`/`dim` retrieval (dict,
  metadata, attribute paths), bool value edge case, benchmark names (Cantor Set,
  R^n, euclidean_N), zero-dimensional tag path, `has_clopen_base` (all 4 explicit
  branches + dim=0 with representation variants), `is_zero_dimensional` (ind=0
  path), `is_totally_disconnected` (tag, zero-dim, metadata, attribute, fallback)
  — `dimension_theory.py` reaches 100%
- 32 new tests in `test_nets_extended.py`: empty index set, outside pairs,
  missing reflexive, non-transitive triples, callable net values, invalid net
  value type, symbolic space fallthrough, missing values, values-outside-carrier,
  all 4 `analyze_net` dispatch paths (none/subset/space+point/directed-only)
  — `nets.py` coverage: 84% → 100%
- 28 new tests in `test_filters_extended.py`: empty family, empty-set-in-base,
  outside-carrier elements, failed intersection pair, invalid filter (F1/F2/F3
  failures), symbolic space fallthrough, point-not-in-carrier, no open neighborhoods,
  missing coarser members, failed neighborhood-member pairs, `analyze_filter`
  invalid-filter early exit, point+coarser dispatch
  — `filters.py` coverage: 84% → 100%
- 42 new tests in `test_infinite_maps_extended.py` + `test_infinite_image_preimage_extended.py`:
  `EmbeddingMap`/`ConstantMap` constructors, `normalize_map_property` ValueError,
  all 5 uncovered `is_*` shortcuts, `infinite_map_report`, `identity_map`,
  `compose_maps` embedding branch, `initial_topology_descriptor` error paths,
  `_has_positive/negative_tag` via metadata, theorem implications (homeomorphism→open/closed,
  embedding→continuous/injective, quotient→continuous/surjective, bijective+closed→homeomorphism),
  `SymbolicSubset.add_tags`, `image_space` surjective path,
  `preimage_subset` closed tag, `image_subset` connected/path_connected,
  `compact_image_result`/`connected_image_result` unknown returns
  — `infinite_maps.py`: 84% → 100%; `infinite_image_preimage.py`: 86% → 100%
- Total: 2302 tests, 95.05% coverage

### CI / DevOps
- Added `.github/workflows/ci.yml`: runs `pytest --cov` on Python 3.11, 3.12, 3.13
  via GitHub Actions on every push/PR to master
- Added `[project.optional-dependencies] dev` to `pyproject.toml` (`pip install -e ".[dev]"`)
- Raised `fail_under` from 60 → 90 in `[tool.coverage.report]`
- Added CI badge to `README.md`
- Added `ruff>=0.4` and `mypy>=1.10` to `dev` dependencies
- Added `[tool.ruff]` and `[tool.mypy]` config to `pyproject.toml`
- Applied ruff auto-fixes: import sorting, `List[X]→list[X]`, deprecated typing imports
  (`from typing import Callable/Mapping/...` → `from collections.abc import ...`),
  unused `typing.Dict/List` artifacts, f-string modernization, quoted annotation removal
- Fixed 2 genuine `__init__.py` bugs: duplicate `neighborhood_system` import and
  duplicate `homeomorphism_criterion_result`/`initial_topology_descriptor` in import block
- Added `ruff check` step to CI (fails on error); added `mypy` step (continue-on-error)
- Mypy reports 48 type annotations to improve (tracked for future work)

## [0.4.2] - 2026-05-15

### Fixed
- Removed 112 broken `__all__` entries from `__init__.py` that referenced
  `_internal/` audit tools not present in the public namespace

### Changed
- Added explicit `__all__` to 9 core modules: `connectedness`, `countability`,
  `local_compactness`, `compactness_variants`, `dimension_theory`, `invariants`,
  `uniform_spaces`, `inverse_systems`

### Tests
- 204 new tests: `preservation_legacy` (100%), `metric_contracts` (91%),
  `finite_witness_diagnostics` (96%), `metrization_profiles` (98%),
  `uniform_spaces` (98%), `inverse_systems`
- Total: 1929 tests, 92% coverage

## [0.4.1] - 2026-05-15

### Changed
- Removed four empty stub modules (`bases`, `sums`, `exceptions`, `infinite_splittings`)
- Cleaned up stale v0.1.64 version aliases from `preservation_tables` public imports
- Added `examples_bank/` to test sys.path in `conftest.py`
- Added Cilt/corridor terminology glossary to `CLAUDE.md`

### Fixed
- `SyntaxWarning` from invalid escape sequence in `test_cilt3_local_compactness_v056.py`
- Fragile exact-dict equality in `test_theorem_profile_alignment.py` replaced with subset checks

### Tests
- 73 new tests for `metric_completeness`, `result_rendering`, and `predicate_contracts`
- Total: 1578 tests, 86% coverage

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
