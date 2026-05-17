# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.19] - 2026-05-17

### Added

- **`uniform_convergence.py`** — new module for uniform convergence, equicontinuity, Arzelà-Ascoli, Dini's theorem, and Stone-Weierstrass:
  - `UniformConvergenceProfile` frozen dataclass with `convergence_type`, `is_uniform`, `is_equicontinuous`, `limit_is_continuous`, `is_relatively_compact`, `satisfies_dini`, `presentation_layer`, `chapter_targets` fields
  - 7 named profiles: x^n on [0,1] (pointwise≠uniform, discontinuous limit), geometric series on [-r,r] (uniform, equicontinuous, Dini), Dini's theorem (monotone pointwise→uniform), Arzelà-Ascoli (relatively compact ↔ bounded+equicontinuous), Stone-Weierstrass (dense subalgebras in C(X)), compact-open topology, Lipschitz family (uniform modulus)
  - `is_uniformly_convergent(space)` — uniform convergence; Dini + Arzelà-Ascoli criteria
  - `is_equicontinuous(space)` — equicontinuity; Lipschitz/Hölder families
  - `satisfies_arzela_ascoli(space)` — relative compactness in C(X); bounded+equicontinuous
  - `satisfies_dini(space)` — Dini's theorem applicability check
  - `classify_uniform_convergence(space)` + `uniform_convergence_profile(space)` facade
  - 9 tag constant sets: UNIFORM_CONVERGENCE_TAGS, POINTWISE_ONLY_TAGS, EQUICONTINUOUS_TAGS, NOT_EQUICONTINUOUS_TAGS, ARZELA_ASCOLI_TAGS, DINI_THEOREM_TAGS, STONE_WEIERSTRASS_TAGS, COMPACT_OPEN_TAGS, NOT_RELATIVELY_COMPACT_TAGS
  - 179 tests, all passing; total test count: 6492

## [0.5.18] - 2026-05-17

### Added

- **`noncommutative_topology.py`** — new module for C*-algebras, Gelfand duality, K-theory, spectral triples, and Connes' noncommutative geometry:
  - `NoncommutativeProfile` frozen dataclass with `algebra_type`, `is_commutative`, `is_nuclear`, `is_simple`, `has_classical_gelfand_dual`, `has_spectral_triple`, `k0_group`, `k1_group`, `presentation_layer`, `chapter_targets` fields
  - 7 named profiles: C(X) (Gelfand dual, commutative), M_n(C) (matrix algebra, simple nuclear), A_θ (noncommutative torus, K₀=K₁=Z²), O_n (Cuntz algebra, K₀=Z/(n-1)Z), C*(G) (group C*-algebra, nuclear iff amenable), K(H) (compact operators, simple nuclear), AF-algebra (Elliott classification, K₁=0)
  - `is_commutative_cstar(space)` — Gelfand duality; commutative ↔ C_0(X)
  - `is_nuclear_cstar(space)` — nuclearity; commutative/AF/Cuntz/amenable-group nuclear; B(H) not nuclear
  - `is_simple_cstar(space)` — simplicity; irrational rotation / Cuntz / K(H) simple; AF/C(X) not simple
  - `has_gelfand_dual(space)` — classical Gelfand dual exists iff commutative
  - `has_spectral_triple(space)` — Connes spectral triple; matrix/NC torus/spin^c manifold yes; Cuntz/AF no
  - `classify_noncommutative(space)` + `noncommutative_profile(space)` facade
  - 10 tag constant sets: COMMUTATIVE_CSTAR_TAGS, NONCOMMUTATIVE_CSTAR_TAGS, NUCLEAR_CSTAR_TAGS, SIMPLE_CSTAR_TAGS, SPECTRAL_TRIPLE_TAGS, GELFAND_DUAL_TAGS, NOT_GELFAND_TAGS, MORITA_EQUIVALENCE_TAGS, KTHEORY_TAGS
  - 200 tests, all passing; total test count: 6313

## [0.5.17] - 2026-05-17

### Added

- **`combinatorial_topology.py`** — new module for simplicial complexes, CW complexes, Euler characteristic, simplicial homology, nerve theorem, and collapsibility:
  - `CombinatorialProfile` frozen dataclass with `complex_type`, `euler_characteristic`, `is_contractible`, `is_acyclic`, `has_torsion_in_homology`, `is_collapsible`, `betti_numbers`, `presentation_layer`, `chapter_targets` fields
  - 7 named profiles: Δ^n (standard simplex, contractible+collapsible), S^n (sphere, chi=2, Betti=[1,0,1]), T² (torus, chi=0, Betti=[1,2,1]), RP² (projective plane, Z/2Z torsion), dunce hat (contractible but NOT collapsible, Zeeman 1963), nerve of good cover (nerve theorem), Klein bottle (Z⊕Z/2Z torsion)
  - `is_contractible_complex(space)` — contractibility via homotopy equivalence to a point
  - `is_acyclic_complex(space)` — acyclicity (trivial reduced homology); contractible implies acyclic
  - `has_torsion_homology(space)` — torsion in H_k(X;Z); non-orientable surfaces carry Z/2Z torsion
  - `is_collapsible_complex(space)` — collapsibility via elementary collapses; collapsible ⊊ contractible
  - `classify_combinatorial(space)` + `combinatorial_profile(space)` facade
  - 9 tag constant sets: SIMPLICIAL_COMPLEX_TAGS, CW_COMPLEX_TAGS, CONTRACTIBLE_TAGS, ACYCLIC_TAGS, TORSION_TAGS, EULER_CHARACTERISTIC_TAGS, NERVE_THEOREM_TAGS, COLLAPSIBLE_TAGS, NOT_COLLAPSIBLE_TAGS
  - 172 tests, all passing; total test count: 6113

## [0.5.16] - 2026-05-17

### Added

- **`topos_theory.py`** — new module for Grothendieck toposes, sheaves, and classifying toposes:
  - `ToposProfile` frozen dataclass with `topos_type`, `is_grothendieck`, `is_elementary`, `is_boolean`, `is_localic`, `has_natural_number_object`, `has_enough_points`, `presentation_layer`, `chapter_targets` fields
  - 6 named profiles: Set (terminal topos, Boolean), Sh(X) (sheaves on a space, localic, intuitionistic), [C^op, Set] (presheaf topos, Boolean), BG (classifying topos for G-torsors), Sh(X_et) (etale topos, not Boolean, etale cohomology), Eff (effective/realizability topos, elementary but NOT Grothendieck)
  - `is_grothendieck_topos(space)` — 4-layer check; Giraud's theorem; sheaves on a site; effective topos fails
  - `is_boolean_topos(space)` — 5-layer check; classical internal logic; presheaf/Set/BG Boolean; etale/effective not Boolean
  - `is_localic_topos(space)` — 4-layer check; Sh(L); Joyal-Tierney theorem; presheaf/BG not localic
  - `has_enough_points_topos(space)` — 4-layer check; Barr's theorem; effective topos lacks points
  - `classify_topos(space)` — classifies into `set`/`boolean_grothendieck`/`localic`/`grothendieck`/`elementary`/`unknown`
  - `topos_profile(space)` — full profile facade
  - `topos_layer_summary()`, `topos_chapter_index()`, `topos_type_index()` registry helpers
  - Tag constants: `GROTHENDIECK_TOPOS_TAGS`, `ELEMENTARY_TOPOS_TAGS`, `BOOLEAN_TOPOS_TAGS`, `LOCALIC_TOPOS_TAGS`, `ENOUGH_POINTS_TAGS`, `NOT_BOOLEAN_TOPOS_TAGS`, `NOT_GROTHENDIECK_TAGS`, `GEOMETRIC_MORPHISM_TAGS`
  - Key theorems: Giraud's theorem (Grothendieck ↔ sheaves on site), Boolean ↔ classical logic, Joyal-Tierney (every topos covered by localic), Hyland's effective topos (elementary ≠ Grothendieck), Weil conjectures via etale cohomology, classifying toposes for geometric theories
  - 170 tests in `tests/core/test_topos_theory_v0516.py`

## [0.5.15] - 2026-05-17

### Added

- **`locale_theory.py`** — new module for frames, locales, and pointfree topology:
  - `LocaleProfile` frozen dataclass with `locale_type`, `is_spatial`, `is_compact`, `is_regular`, `is_completely_regular`, `is_zero_dimensional`, `is_localic_group`, `presentation_layer`, `chapter_targets` fields
  - 6 named profiles: Omega(R) (localic real line, spatial, regular, localic group), B(R)/N (measure algebra locale, NOT spatial, compact, Stone), profinite Stone locale, [0,1] (compact regular spatial), Sierpinski locale (T0 not regular), T^2 (localic torus, localic group)
  - `is_spatial_locale(space)` — 6-layer check; T2 => sober => spatial; Isbell: localic groups are spatial; measure algebra is NOT spatial
  - `is_compact_locale(space)` — 5-layer check; Stone/profinite => compact; complete Boolean algebra => compact locale
  - `is_regular_locale(space)` — 5-layer check; well-inside relation; compact Hausdorff => regular; Boolean algebra => regular; Sierpinski fails
  - `is_stone_locale(space)` — 5-layer check; Stone Loc ≃ Bool^op; measure algebra gives non-spatial Stone locale
  - `is_localic_group(space)` — 3-layer check; Isbell's density theorem: all localic groups are spatial
  - `classify_locale(space)` — classifies into `non_spatial`/`stone`/`localic_group`/`compact_regular`/`spatial`/`unknown`
  - `locale_profile(space)` — full profile facade
  - `locale_layer_summary()`, `locale_chapter_index()`, `locale_type_index()` registry helpers
  - Tag constants: `SPATIAL_LOCALE_TAGS`, `COMPACT_LOCALE_TAGS`, `REGULAR_LOCALE_TAGS`, `COMPLETELY_REGULAR_LOCALE_TAGS`, `ZERO_DIMENSIONAL_LOCALE_TAGS`, `NON_SPATIAL_LOCALE_TAGS`, `LOCALIC_GROUP_TAGS`, `NOT_REGULAR_LOCALE_TAGS`
  - Key theorems: Isbell adjunction (Omega ⊣ pt), spatial ↔ sober duality, Isbell's density theorem (localic groups are spatial), Stone locale duality (Stone Loc ≃ Bool^op), measure algebra as paradigmatic non-spatial locale, well-inside relation and regularity
  - 197 tests in `tests/core/test_locale_theory_v0515.py`

## [0.5.14] - 2026-05-17

### Added

- **`coarse_geometry.py`** — new module for large-scale (coarse) geometry:
  - `CoarseGeometryProfile` frozen dataclass with `geometry_type`, `asymptotic_dimension`, `number_of_ends`, `has_property_a`, `is_gromov_hyperbolic`, `is_quasi_isometric_to_euclidean`, `presentation_layer`, `chapter_targets` fields
  - 6 named profiles: Z (integer line, QI to R, 2 ends), Z^n (euclidean lattice, QI to R^n, 1 end), F_2 (free group, hyperbolic, infinite ends), H^2 (hyperbolic plane, delta-hyperbolic), H_3(Z) (Heisenberg group, nilpotent, NOT QI to R^4), expander families (no Property A)
  - `has_finite_asymptotic_dimension(space)` — 5-layer check; Bell-Dranishnikov theorem for hyperbolic groups; asdim(Z^n) = n; expanders fail
  - `has_property_a(space)` — 5-layer check; amenable => Property A; hyperbolic => Property A (Yu 2000); linear groups (Guentner-Higson-Weinberger); expanders fail
  - `is_gromov_hyperbolic(space)` — 5-layer check; delta-slim triangles; trees (delta=0); CAT(-1); euclidean/nilpotent fail
  - `is_quasi_isometric_to_euclidean(space)` — 5-layer check; virtually abelian <=> QI to R^n; Heisenberg NOT QI to R^4 (Carnot cone)
  - `coarsely_embeds_in_hilbert(space)` — 4-layer check; Property A => coarse embedding; expanders do not embed (Gromov)
  - `classify_coarse_geometry(space)` — classifies into `euclidean`/`hyperbolic`/`nilpotent`/`expander`/`unknown`
  - `coarse_geometry_profile(space)` — full profile facade
  - `coarse_geometry_layer_summary()`, `coarse_geometry_chapter_index()`, `coarse_geometry_type_index()` registry helpers
  - Tag constants: `FINITE_ASYMPTOTIC_DIM_TAGS`, `PROPERTY_A_TAGS`, `HYPERBOLIC_TAGS`, `POLYNOMIAL_GROWTH_TAGS`, `EXPONENTIAL_GROWTH_TAGS`, `TWO_ENDS_TAGS`, `INFINITE_ENDS_TAGS`, `ONE_END_TAGS`, `NOT_PROPERTY_A_TAGS`
  - Key theorems: Gromov's polynomial growth theorem (poly growth <=> virtually nilpotent), Stallings' theorem (ends and group splittings), Yu's Property A theorem (hyperbolic => Property A), Bell-Dranishnikov (hyperbolic => finite asdim), Milnor-Svarc lemma (geometric actions => QI)
  - 212 tests in `tests/core/test_coarse_geometry_v0514.py`

## [0.5.13] - 2026-05-17

### Added

- **`spectral_spaces.py`** — new module for spectral spaces, sober spaces, Stone duality, and frame-locale correspondence:
  - `SpectralSpaceProfile` frozen dataclass with `space_type`, `is_sober`, `is_spectral`, `is_stone_space`, `is_t0`, `is_t1`, `has_generic_point`, `presentation_layer`, `chapter_targets` fields
  - 6 named profiles: Sierpinski space (sober T0 non-T1), Spec(integral domain) (spectral, generic point), Stone/Boolean space (compact T.D. Hausdorff), Zariski affine line Spec(k[x]), Alexandrov on dcpo (sober), Alexandrov on (N,≤) (T0 NOT sober)
  - `is_sober(space)` — 6-layer check; T2 ⟹ sober; Hochster: Spec(R) always sober; Alexandrov on dcpo ↔ sober
  - `is_spectral(space)` — 5-layer check; Hochster's theorem: spectral ↔ homeomorphic to Spec(R)
  - `is_stone_space(space)` — 5-layer check; Stone duality: Boolean algebras ↔ Stone spaces
  - `frame_is_spatial(space)` — 4-layer check; O(X) spatial ↔ X sober (frame-locale duality)
  - `stone_duality_applies(space)` — 5-layer check; Stone duality requires compact T.D. Hausdorff
  - `classify_spectral_space(space)` — classifies into `stone`/`spectral`/`sober`/`t0_not_sober`/`unknown`
  - `spectral_space_profile(space)` — full profile facade
  - `spectral_space_layer_summary()`, `spectral_space_chapter_index()`, `spectral_space_type_index()` registry helpers
  - Tag constants: `SOBER_POSITIVE_TAGS`, `SPECTRAL_TAGS`, `STONE_SPACE_TAGS`, `SPATIAL_FRAME_TAGS`, `GENERIC_POINT_TAGS`, `NOT_SOBER_TAGS`, `NOT_T1_TAGS`, `NOT_STONE_TAGS`
  - Key theorems: Hochster's theorem (spectral ↔ Spec(R)), Stone representation (Boolean algebras ↔ Stone spaces), frame-locale duality (O(X) spatial ↔ X sober), Alexandrov sobriety (dcpo condition), Sierpinski space as classifier of open sets
  - 179 tests in `tests/core/test_spectral_spaces_v0513.py`

## [0.5.12] - 2026-05-17

### Added

- **`fiber_bundles.py`** — new module for fiber bundle theory, vector bundles, principal bundles, and sections:
  - `FiberBundleProfile` frozen dataclass with `bundle_type`, `is_locally_trivial`, `is_vector_bundle`, `is_principal`, `is_trivial`, `has_nowhere_zero_section`, `is_orientable`, `presentation_layer`, `chapter_targets` fields
  - 6 named profiles: product bundle (trivial), Möbius band (non-trivial line bundle), tangent bundle of even sphere (hairy ball), Hopf fibration S³→S² (principal U(1)-bundle), GL(n) frame bundle, tautological bundle over Grassmannian
  - `is_locally_trivial(space)` — 5-layer check; all vector/principal bundles are locally trivial by definition
  - `is_vector_bundle(space)` — 4-layer check; principal G-bundles (Hopf, frame) are NOT vector bundles
  - `is_trivial_bundle(space)` — 5-layer check; contractible base → trivial; Adams' theorem: S^n parallelizable only for n=1,3,7
  - `has_nowhere_zero_section(space)` — 5-layer check; hairy ball theorem: TS^{2n} has no nowhere-zero section (χ(S^{2n})=2≠0)
  - `is_orientable_bundle(space)` — 5-layer check; complex bundles always orientable; Möbius band: w_1 ≠ 0
  - `classify_bundle(space)` — classifies into `trivial`/`vector_bundle`/`principal`/`locally_trivial`/`unknown`
  - `fiber_bundle_profile(space)` — full profile facade
  - `fiber_bundle_layer_summary()`, `fiber_bundle_chapter_index()`, `fiber_bundle_type_index()` registry helpers
  - Tag constants: `LOCALLY_TRIVIAL_TAGS`, `VECTOR_BUNDLE_TAGS`, `PRINCIPAL_BUNDLE_TAGS`, `TRIVIAL_BUNDLE_TAGS`, `NOWHERE_ZERO_SECTION_TAGS`, `ORIENTABLE_BUNDLE_TAGS`, `NOT_TRIVIAL_TAGS`, `NOT_NOWHERE_ZERO_SECTION_TAGS`
  - Key theorems: hairy ball (Poincaré-Hopf for TS^{2n}), Adams' theorem (parallelizable spheres), Hopf fibration π_3(S²)≅Z, structure group reduction to O(n) via Riemannian metric, classification by [X,BG]
  - 182 tests in `tests/core/test_fiber_bundles_v0512.py`

## [0.5.11] - 2026-05-17

### Added

- **`shape_theory.py`** — new module for shape theory, ANR/FANR classification, and Čech invariants:
  - `ShapeProfile` frozen dataclass with `shape_type`, `is_anr`, `is_fanr`, `is_movable`, `is_shape_trivial`, `presentation_layer`, `chapter_targets` fields
  - 6 named profiles: compact polyhedron (ANR), compact AR / closed ball (shape-trivial), compact manifold (ANR), Warsaw circle (not movable), dyadic solenoid (not movable), Hawaiian earring (movable but not FANR/ANR)
  - `is_anr(space)` — 6-layer check; Borsuk's theorem: compact metrizable X is ANR ↔ locally contractible
  - `is_fanr(space)` — 5-layer check; FANR = shape dominated by compact ANR; requires finitely generated Čech homology
  - `is_movable(space)` — 6-layer check; Borsuk's theorem: every Peano continuum is movable; ANR ⊂ FANR ⊂ movable
  - `has_trivial_shape(space)` — 5-layer check; trivial shape ↔ compact AR ↔ contractible ANR
  - `cech_cohomology_applicable(space)` — 4-layer check; Čech = singular for compact ANRs; shape invariant for all compact metrizable spaces
  - `classify_shape(space)` — classifies into `shape_trivial`/`anr`/`fanr`/`movable`/`not_movable`/`unknown`
  - `shape_profile(space)` — full profile facade
  - `shape_layer_summary()`, `shape_chapter_index()`, `shape_type_index()` registry helpers
  - Tag constants: `ANR_POSITIVE_TAGS`, `FANR_POSITIVE_TAGS`, `MOVABLE_POSITIVE_TAGS`, `SHAPE_TRIVIAL_TAGS`, `CECH_COMPUTABLE_TAGS`, `NOT_ANR_TAGS`, `NOT_FANR_TAGS`, `NOT_MOVABLE_TAGS`
  - Key theorems: Borsuk ANR theorem, ANR ⊂ FANR ⊂ movable chain, Whitehead failure in shape theory (Warsaw circle vs S^1), Peano continuum movability, Dugundji extension theorem for compact ARs
  - 199 tests in `tests/core/test_shape_theory_v0511.py`

## [0.5.10] - 2026-05-17

### Added

- **`borel_measures.py`** — new module for Borel measures, Radon measures, regularity, and Riesz representation:
  - `BorelMeasureProfile` frozen dataclass with `measure_type`, `is_radon`, `is_regular`, `is_atomic`, `is_sigma_finite`, `support_type`, `presentation_layer`, `chapter_targets` fields
  - 7 named profiles: Lebesgue measure (Radon, regular, non-atomic), Dirac measure (Radon, atomic), Haar measure on compact group, Haar measure on locally compact group, counting measure (NOT Radon on uncountable space), Cantor measure (singular continuous, Radon), Gaussian measure (absolutely continuous, Radon)
  - `is_radon_measure(space)` — 5-layer check; Radon = locally finite + inner regular
  - `is_regular_measure(space)` — 5-layer check; outer and inner regular; Ulam's theorem for compact metric spaces
  - `riesz_representation_applies(space)` — 4-layer check; Riesz-Markov-Kakutani theorem for compact/locally compact Hausdorff spaces
  - `has_haar_measure(space)` — 5-layer check; every locally compact topological group admits Haar measure
  - `measure_support_is_compact(space)` — 5-layer check; Dirac/compact space → compact support
  - `classify_borel_measure(space)` — classifies into `radon_regular`/`radon`/`regular`/`finite_borel`/`not_radon`/`unknown`
  - `borel_measure_profile(space)` — full profile facade
  - 180 tests in `tests/core/test_borel_measures_v0510.py`

## [0.5.9] - 2026-05-17

### Added

- **`zero_dimensionality.py`** — new module for zero-dimensional spaces and Stone duality:
  - Zero-dimensional spaces (dim = 0), totally disconnected compact Hausdorff spaces, Boolean spaces
  - Stone duality: Boolean algebras ↔ Stone spaces (compact totally disconnected Hausdorff)
  - Cantor set as universal zero-dimensional compact metrizable space

- **`solenoid_profiles.py`** — new module for solenoid topology profiles:
  - Solenoid as inverse limit of circles, dyadic solenoid construction
  - Čech cohomology of solenoids: Ȟ^1(Σ_p;Z) ≅ Z[1/p]
  - Solenoids as compact connected abelian groups without isolated points

## [0.5.8] - 2026-05-17

### Added

- **`hyperspaces.py`** — new module for hyperspace topology:
  - `HyperspaceProfile` frozen dataclass with `hyperspace_type`, `base_space_class`, `is_compact`, `is_polish`, `presentation_layer`, `chapter_targets` fields
  - 5 named profiles: K([0,1]) (compact Polish, ≅ Hilbert cube), K(Cantor) (compact Polish, ≅ Cantor set), K(R) (Polish not compact), 2^X Vietoris (compact X), K(Polish X) (Polish)
  - `hausdorff_metric_applicable(space)` — 4-layer check (Polish, compact metrizable, locally compact metrizable, metrizable)
  - `hyperspace_is_compact(space)` — 6-layer check; Blaschke selection theorem: K(X) compact ↔ X compact metrizable
  - `hyperspace_is_polish(space)` — 4-layer check; K(X) Polish theorem: X Polish → K(X) Polish
  - `vietoris_topology_hausdorff(space)` — 3-layer check; 2^X Hausdorff ↔ X Hausdorff
  - `hyperspace_is_connected(space)` — 3-layer check; K(X) connected ↔ X connected
  - `classify_hyperspace(space)` — classifies into `compact_polish`/`polish`/`compact`/`metrizable`/`unknown`
  - `hyperspace_profile(space)` — full profile facade
  - `hyperspace_layer_summary()`, `hyperspace_chapter_index()`, `hyperspace_type_index()` registry helpers
  - Tag constants: `COMPACT_METRIZABLE_TAGS`, `POLISH_BASE_TAGS`, `LOCALLY_COMPACT_METRIZABLE_TAGS`, `METRIZABLE_BASE_TAGS`, `CONNECTED_BASE_TAGS`, `HAUSDORFF_METRIC_TAGS`, `NOT_HYPERSPACE_COMPACT_TAGS`, `VIETORIS_COMPACT_TAGS`
  - Key theorems: Blaschke selection, K(X) Polish theorem, Curtis-Schori-West (K([0,1])≅[0,1]^ω), K(Cantor)≅Cantor
  - 113 tests in `tests/core/test_hyperspaces_v058.py`

## [0.5.7] - 2026-05-17

### Added

- **`topological_vector_spaces.py`** — new module for TVS analysis:
  - `TVSProfile` frozen dataclass with `tvs_type`, `is_locally_convex`, `is_complete`, `presentation_layer`, `chapter_targets` fields
  - 5 named profiles: L²[0,1] (Hilbert), L^p/1≤p<∞ (Banach), C^∞(R) (Fréchet), D'(R) distributions (locally convex, not metrizable), L^p/0<p<1 (TVS, NOT locally convex)
  - `is_locally_convex(space)` — 6-layer check with full TVS hierarchy (Hilbert→Banach→Fréchet→locally convex)
  - `is_frechet_space(space)` — 5-layer check; Fréchet = completely metrizable locally convex TVS
  - `is_banach_space(space)` — 5-layer check; Banach = complete normed (Fréchet with one norm)
  - `hahn_banach_applicable(space)` — 4-layer check; requires local convexity; fails for L^p (0<p<1)
  - `open_mapping_theorem_holds(space)` — 4-layer check; requires Fréchet (BCT-based proof)
  - `classify_tvs(space)` — classifies into `hilbert`/`banach`/`frechet`/`locally_convex`/`tvs`/`unknown`
  - `tvs_profile(space)` — full profile facade
  - `tvs_layer_summary()`, `tvs_chapter_index()`, `tvs_type_index()` registry helpers
  - Tag constants: `TVS_POSITIVE_TAGS`, `TVS_NEGATIVE_TAGS`, `LOCALLY_CONVEX_TAGS`, `NOT_LOCALLY_CONVEX_TAGS`, `FRECHET_TAGS`, `BANACH_TAGS`, `HILBERT_TAGS`, `HAHN_BANACH_TAGS`, `OPEN_MAPPING_TAGS`
  - Tag hierarchy enforced: HILBERT_TAGS ⊆ BANACH_TAGS ⊆ FRECHET_TAGS ⊆ LOCALLY_CONVEX_TAGS
  - 130 tests in `tests/core/test_topological_vector_spaces_v057.py`

### Changed

- Coverage patches (9 tests in `tests/core/test_coverage_patches_v057.py`):
  - `descriptive_set_theory.py:104` — `_extract_tags` fallback for tagless objects
  - `normal_spaces.py:97` — `_representation_of` attribute path
  - `baire_category.py:97` — `_representation_of` attribute path
  - `topological_vector_spaces.py:121` — `_extract_tags` fallback (new module, patched immediately)
- Coverage: 99.68% → 99.70% (35 remaining missed lines are unreachable dead code)

## [0.5.6] - 2026-05-17

### Added

- **`descriptive_set_theory.py`** — new module for descriptive set theory:
  - `DescriptiveSetProfile` frozen dataclass with `borel_class`, `has_baire_property`, `is_perfect`, `presentation_layer`, `chapter_targets` fields
  - 5 named profiles: irrationals (G_delta, perfect, Polish), rationals Q (F_sigma, meager, NOT G_delta), Cantor set (perfect, compact), open interval (G_delta and F_sigma), countable successor ordinal (scattered)
  - `is_g_delta(space)` — 6-layer check; includes Alexandrov's theorem (completely metrizable ↔ G_delta in metric completion) and BCT proof that Q is not G_delta
  - `is_f_sigma(space)` — 5-layer check (closed, open in metrizable, sigma-compact, countable T1)
  - `is_perfect_set(space)` — 7-layer check with Cantor-Bendixson decomposition context
  - `has_baire_property(space)` — 5-layer check (Bernstein/Vitali negative, open/closed, G_delta/F_sigma, Borel/analytic, metrizable)
  - `cantor_bendixson_analysis(space)` — 4-layer Cantor-Bendixson theorem application
  - `classify_descriptive_complexity(space)` — classifies into `open`, `closed`, `g_delta`, `f_sigma`, `borel`, `unknown` with full `key_properties` list
  - `descriptive_set_profile(space)` — full profile facade
  - `descriptive_layer_summary()`, `descriptive_chapter_index()`, `descriptive_type_index()` registry helpers
  - Tag constants: `G_DELTA_TAGS`, `F_SIGMA_TAGS`, `PERFECT_SET_TAGS`, `SCATTERED_TAGS`, `BAIRE_PROPERTY_TAGS`, `BOREL_NEGATIVE_TAGS`, `G_DELTA_NEGATIVE_TAGS`, `CLOSED_IN_METRIZABLE_TAGS`, `OPEN_IN_METRIZABLE_TAGS`
  - 128 tests in `tests/core/test_descriptive_set_theory_v056.py`

- **`normal_spaces.py`** — new module for normality analysis and theorems:
  - `NormalSpaceProfile` frozen dataclass with `normality_type`, `presentation_layer`, `chapter_targets` fields
  - 5 named profiles: metrizable (perfectly normal), compact Hausdorff, CW-complex, Niemytzki plane (normal, not perfectly normal), Sorgenfrey plane (not normal)
  - `urysohn_function_exists(space)` — 7-layer check (negative tags, metrizable, compact Hausdorff, paracompact Hausdorff, perfectly normal, normal tag, unknown); Urysohn's Lemma: X normal ↔ continuous separation functions exist
  - `tietze_extension_applicable(space)` — 6-layer check; Tietze Extension Theorem: X is T4 ↔ every f: C → R on closed C extends to X
  - `classify_normality(space)` — classifies into `perfectly_normal`, `normal`, `not_normal`, `unknown`
  - `normal_space_profile(space)` — full profile facade
  - `normal_layer_summary()`, `normal_chapter_index()`, `normal_type_index()` registry helpers
  - Tag constants: `NORMAL_POSITIVE_TAGS`, `NORMAL_NEGATIVE_TAGS`, `PERFECTLY_NORMAL_TAGS`, `METRIZABLE_NORMAL_TAGS`, `COMPACT_HAUSDORFF_TAGS`, `PARACOMPACT_HAUSDORFF_TAGS`, `URYSOHN_CONFIRMING_TAGS`, `TIETZE_CONFIRMING_TAGS`
  - 115 tests in `tests/core/test_normal_spaces_v056.py`

## [0.5.5] - 2026-05-17

### Added

- **`baire_category.py`** — new module for Baire category theory:
  - `BaireCategoryProfile` frozen dataclass with `is_baire`, `category_type`, `presentation_layer`, `chapter_targets` fields
  - 5 named examples: real line (complete metric), [0,1] (compact Hausdorff), Cantor set, ω^ω (Polish/irrationals), ℚ (NOT Baire)
  - `is_baire_space(space)` — 7-layer theorem check (negative tags, complete metric BCT, locally compact Hausdorff BCT, open dense subspace, countable T1 no isolated points, direct tags, unknown)
  - `is_meager_space(space)` — 3-layer check (direct tags, countable T1 no isolated points, Baire contradiction)
  - `baire_category_theorem_check(space)` — explicit BCT form identification (metric / topological / Polish)
  - `classify_baire_category(space)` — classifies into `complete_metric`, `locally_compact_hausdorff`, `polish`, `baire`, `not_baire`, `unknown`
  - `baire_category_profile(space)` — full profile facade combining classification and named examples
  - `baire_layer_summary()`, `baire_chapter_index()`, `baire_type_index()` registry helpers
  - Tag constants: `BAIRE_POSITIVE_TAGS`, `BAIRE_NEGATIVE_TAGS`, `BAIRE_COMPLETE_METRIC_TAGS`, `LCH_TAGS`, `POLISH_TAGS`, `MEAGER_SPACE_TAGS`, `COMEAGER_TAGS`, `OPEN_DENSE_TAGS`
  - 108 tests in `tests/core/test_baire_category_v055.py`

### Fixed

- `tests/experimental/test_advanced_metrization.py` — updated `metrization_layer_summary` assertion from `advanced_note: 1` to `advanced_note: 3` to match the two new profiles added in v0.5.4

### Changed

- Coverage patches (20 tests in `tests/core/test_coverage_patches_v055.py`):
  - `topological_groups.py` lines 71, 74 (`_representation_of` metadata and attribute paths) and 418 (`compact` group type)
  - `stone_cech.py` lines 85, 88 (`_representation_of` paths)
  - `cell_complexes.py` lines 112–113 (`validate_finite_cell_profile` CellComplexError path)
  - `cardinal_functions_framework.py` line 344 (`_comparison_key`)
  - `maps.py` line 440 (`_analyze_finite_map_property` unknown-property `None` return)

## [0.5.4] - 2026-05-16

### Added

- **`metrization_profiles.py`** — Nagata-Smirnov and Bing metrization criteria:
  - `REGULAR_TAGS`, `NAGATA_SMIRNOV_TAGS`, `BING_TAGS` tag constants
  - `check_nagata_smirnov(space)` — T3 + σ-locally finite base → Tychonoff (criterion: `nagata_smirnov`)
  - `check_bing_metrization(space)` — T3 + σ-discrete base → metrizable (criterion: `bing_metrization`)
  - `metrization_theorem_check(space)` — runs Urysohn + Nagata-Smirnov + Bing and returns combined verdict
  - `is_metrizable` extended with Layer 5 (Nagata-Smirnov) and Layer 6 (Bing)
  - Registry now contains 5 named profiles (added `nagata_smirnov_sigma_lf_base_route` and `bing_sigma_discrete_base_route`)

- **`separation.py`** — T3.5 / Tychonoff characterization:
  - `TYCHONOFF_POSITIVE_TAGS`, `SEPARATION_CHAIN_ORDER` constants
  - `check_tychonoff(space)` — 7-layer multi-criterion check (metric, direct_tag, cr_t1, normal_t1, perfectly_normal)
  - `tychonoff_characterization(space)` — structured report: `{is_tychonoff, criterion, is_completely_regular, is_t1, note}`
  - `separation_chain(space)` — full T0 → T6 hierarchy as an ordered dict of `Result` values

- **`topological_groups.py`** — new module for topological group analysis:
  - `TopologicalGroupProfile` frozen dataclass with `separation_level` field
  - 5 named profiles: real Lie group, compact Lie group, profinite group, LCA group, discrete group
  - `is_topological_group(space)` — 7-layer check (Lie, profinite, compact/LC, direct tag, axioms via T0+ops)
  - `topological_group_separation(space)` — T0-group-is-Tychonoff theorem with special cases for Lie, profinite, compact, discrete
  - `classify_topological_group(space)` — classifies into lie/compact_lie/profinite/compact_abelian/LCA/discrete/general
  - `topological_group_profile(space)` — full profile facade

- **`stone_cech.py`** — new module for Stone-Čech compactification analysis:
  - `StoneCechDescriptor` frozen dataclass
  - 5 named examples: βN, βR, βX (compact Hausdorff), βQ, βX (discrete)
  - `is_stone_cech_compactifiable(space)` — 7-layer check (compact_hausdorff, tychonoff, T4, metric, Lie/profinite)
  - `stone_cech_embedding(space)` — embedding type: `homeomorphism` (X = βX) or `proper_dense`
  - `stone_cech_extension(space)` — universal property: bounded continuous functions extend to βX
  - `classify_stone_cech(space)` — relationship: homeomorphism / proper_compactification / non_existent / unknown
  - `stone_cech_profile(space)` — full profile facade

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
