# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.7.0] — 2026-06-24

First PyPI-published release. Bundles the Phase 16–20 maturity work completed
since v1.6.0 and establishes the automated publishing pipeline.

### Added

- **P20.2 — PyPI publishing pipeline.** Automated release via GitHub Actions
  **Trusted Publishing** (OIDC, no stored API tokens): `.github/workflows/publish.yml`
  builds the sdist + wheel, runs `twine check`, and uploads to PyPI on every
  `v*` tag (with a manual `workflow_dispatch` TestPyPI dry-run path). The package
  builds clean, passes `twine check`, and imports in a zero-dependency clean room
  (runtime stays dependency-free). Release process documented in
  `docs/P20_RELEASE_READINESS.md`.
- **P16.2 — Oracle agreement matrix populated & persisted.** A Docker-free internal
  oracle cross-checks 9 torus-knot Alexander polynomials (pytop reduced-Burau vs the
  Sage-verified table) and GUDHI persistent-Betti rows; `generate_oracle_matrix()` /
  `persist_oracle_matrix()` emit `docs/validation/oracle_matrix.{json,md}` (15/15 = 100%).
- **P16.3 — GUDHI cross-validation wired** into the statistical validation suite
  (`persistence_dim_max=True` so top-dimension H₁ is computed); always-on
  500-complex GUDHI parity guard in the default suite.

### Changed

- **P17.3 — Size-aware auto reduction routing.** `persistent_homology(method="auto")`
  is now the default; small complexes route to Twist, large Rips to the de Silva dual
  cohomology. Output byte-identical to twist/cohomology/standard.
- **Knot table expanded to 51 primes** (unknot–17_1) with Alexander/Jones/genus
  fields backfilled from the SageMath oracle and locked by det/Δ(1)/V(1) guards.
- **Development status** promoted to `Production/Stable` — the 1.x line carries the
  Phase 19 API-stability guarantees (18-month deprecation window).
- **P19/P20 maturity items closed** (deprecation policy, API-consistency audit,
  community onboarding) and roadmap reconciled.

## [1.6.0] — 2026-06-23

### Added

- **Phase 16 — Empirical validation & oracle ecosystem.**
  - **P16.1 — Benchmark suite** (`tests/validation/`): minimal triangulations
    (T²/Klein/ℝP² with verified Betti/torsion), a 40+-prime knot table
    (unknot–9_5 with Alexander/Jones), and a large grid library (3×3–40×40, all
    confirmed planar). 37 tests.
  - **P16.3 — Statistical validation:** 10,000 random Erdős–Rényi 1-skeleta
    (5–50 vertices), pytop H₀/H₁ computed with 100% success (avg ~6 ms/complex),
    outlier analysis, JSON report.

### Changed

- **P17.3 — Inductive Vietoris–Rips construction (~14–19× faster filtration builds).**
  `vietoris_rips_filtration` now uses inductive clique expansion (Zomorodian 2010)
  over the neighborhood graph instead of exhaustive `C(n, k+1)` subset enumeration.
  Build time scales with the materialized complex rather than `C(n, k+1)`
  (n=500: 22.7 s → 1.65 s). **Output is byte-identical** to the previous
  construction — no API or behavior change — verified against a brute-force
  reference and the full test suite.

### Added

- **P16.2 — GUDHI persistent-Betti parity (now wired).** `tests/validation/betti_parity.py`
  cross-checks pytop's Vietoris–Rips persistent homology against GUDHI by Betti
  number at scale (`birth ≤ s < death`), for dimensions the truncated skeleton
  represents faithfully (`H_k` needs simplices up to dim `k+1`), sampled at
  filtration-event midpoints. Passing on circle / dense circle / two circles
  (`H₀=H₁=2`) / icosahedral 2-sphere (`H₂=1`) / random cloud. Validation suite
  79 → 97 passing.
- **P19.2 — Deprecation policy.** `@deprecated` decorator (`pytop._deprecation`)
  emitting consistent WHY-HOW-THEN `DeprecationWarning`s with docstring notes and
  metadata; `preservation_legacy` retrofitted onto it. `DEPRECATIONS.md` documents
  the 18-month / next-major policy and registry.
- **P19.3 — API consistency audit** in `docs/API_DESIGN.md` (naming conventions +
  documented inconsistencies deferred to v2.0).
- **P20.3 — Community onboarding.** Rewritten `CONTRIBUTING.md`; GitHub issue
  templates (bug / feature / docs) and pull-request template under `.github/`.

### Fixed

- Latent `BettiResult.torsion` type bug (`list = None` → `list | None = None`) and
  the previously broken death-count Betti comparison in the oracle agreement builder.
- Latent `_gpu_backend` bug: `ReductionStats` was built with the read-only
  `clearing_ratio` property and missing required fields (would crash if the cupy
  path ran); also removed a dead Clearing-sweep stub.

### Maintenance

- Repo-wide lint/type cleanup: `src/pytop` is ruff-clean **and** mypy-clean
  (244 files) and the full `src/`+`tests/` tree passes ruff (was 236 ruff + 12
  mypy errors). Behavior-preserving.
- Version handling: `pyproject.toml` and `__version__` kept in sync; backfilled
  the missing `v1.4.0` and `v1.5.0` release tags.

## [1.5.0] — 2026-06-23

### Added

- **Phase 13 — Homotopy Theory (5 modules)**

  - **`chain_homotopy.py` (P13.1)** — Chain homotopies and homotopy equivalences.
    `ChainHomotopyResult`, `HomotopyEquivalenceVerdict`; `is_chain_homotopy` (verifies ∂h + h∂ = f−g);
    `find_chain_homotopy` (Gaussian elimination over ℚ via `Fraction`);
    `chain_homotopy_equiv` (splitting theorem: same Betti ↔ chain-homotopy equivalent);
    `homotopy_equivalence_simplicial`.

  - **`eilenberg_maclane.py` (P13.2)** — Eilenberg–MacLane spaces K(G,n).
    `KGnHomology`; `km_homology_cyclic` (K(ℤ/m,1): H_{2k-1}=ℤ/m, H_{2k}=0);
    `km_homology_free` (K(F_r,1)=∨S¹: H_1=ℤ^r);
    `km_homology_free_abelian` (K(ℤ^r,1)=T^r: H_k=ℤ^C(r,k));
    `km_homology_z`, `km_homology_z2`, `km_homology_rational`;
    `is_aspherical_by_homology`, `km_euler_characteristic`.

  - **`massey_products.py` (P13.3)** — Massey triple products and formality.
    `MasseyProduct`; `triple_massey_product` (solves δx=α∪β, δy=β∪γ over ℚ);
    `massey_vanishes`; `is_formal_simplicial` (vanishing of all triple Massey products);
    `all_triple_massey_products`.

  - **`hopf_invariant.py` (P13.4)** — Hopf invariant and fibrations.
    `HopfInvariant`; `hopf_fibration(n)` (valid for n∈{1,2,4,8} — Adams theorem);
    `all_hopf_fibrations`; `adams_hopf_invariant_one`; `pi3_s2` (π₃(S²)=ℤ, generator η₂);
    `hopf_invariant_from_cup`, `hopf_invariant_from_linking`;
    `hopf_invariant_composition`, `hopf_invariant_sum`, `hopf_invariant_degree_map`.

  - **`sullivan_models.py` (P13.5)** — Sullivan minimal models over ℚ.
    `SullivanGenerator`, `SullivanModel`; `sullivan_sphere(n)` (S^n odd: Λ(e_n), d=0;
    S^n even: Λ(e_n,f_{2n-1}), d(f)=e_n²); `sullivan_torus(r)`, `sullivan_complex_projective(n)`,
    `sullivan_cp_infinity`, `sullivan_k_z1`, `sullivan_wedge_circles`, `sullivan_product`;
    `pi_rational`, `euler_characteristic_sullivan`, `poincare_series_sullivan`,
    `is_pure_sullivan`, `sullivan_from_betti`.

- **Phase 14 — Advanced Knot Homology (5 modules)**

  - **`khovanov_odd.py` (P14.1)** — Odd Khovanov homology (Ozsváth–Rasmussen–Szabó 2013).
    `OddKhovanovHomology`; `khovanov_homology_odd` (cube-of-resolutions with ORS odd sign
    assignment: (−1)^{#{j<i: v[j]=1}}); `compare_khovanov_parities`; `_odd_sign`.
    Identical to even Khovanov over ℤ/2; functorial for oriented link cobordisms.

  - **`grid_floer.py` (P14.2)** — Grid diagram Floer homology HFK̂.
    `GridDiagram`, `GridState`, `HFKHat`; `grid_diagram_from_permutations`;
    `unknot_grid`, `trefoil_grid`, `hopf_link_grid`;
    `hfk_hat` (grid states = permutations; empty rectangle differential; Maslov/Alexander gradings;
    constrained to n≤5); `alexander_polynomial_from_hfk`.

  - **`concordance.py` (P14.3)** — Concordance invariants (τ, s, σ).
    `ConcordanceInvariants`; `tau_torus_knot` (τ(T(p,q))=(p-1)(q-1)/2);
    `s_invariant_torus_knot` (s(T(p,q))=(p-1)(q-1));
    `signature_torus_knot` (σ(T(2,q))=-(q-1));
    `tristram_levine_signature`, `concordance_data`, `is_algebraically_slice`,
    `concordance_order`, `is_concordant_to_unknot`, `tau_from_alexander_degree`.
    Database: unknot, trefoil, figure-eight, T(2,5), T(3,4), T(2,7).

  - **`satellite_knots.py` (P14.4)** — Satellite and cable knot invariants.
    `SatelliteKnot`, `CableKnot`; `satellite_alexander_poly` (Morton's formula:
    Δ_{S(P,K)}(t)=Δ_P(t)·Δ_K(t^w)); `cable_alexander_poly`, `cable_genus`
    (Gabai: p·g(K)+(p-1)(q-1)/2); `cable_tau` (Hedden's formula);
    `cable_signature`, `whitehead_double`, `torus_knot_alexander_poly`,
    `satellite_data`, `longitudinal_cable`.

  - **`virtual_knots.py` (P14.5)** — Virtual knot theory and invariants.
    `GaussCode`, `VirtualKnotDiagram`, `VirtualInvariants`; `gauss_code_from_string`;
    `parity_of_crossing` (odd/even via inter-crossing count); `odd_writhe` (J(K) — Kauffman 1999);
    `writhe`; `is_classical` (J(K)=0 necessary condition); `virtual_genus_lower_bound`;
    `arrow_polynomial_bracket` (Dye–Kauffman 2009, simplified); `virtual_knot_invariants`;
    `VIRTUAL_KNOT_DATA` (unknot, virtual trefoil, Kishino's knot).

- **Phase 15 — 4-Manifold Topology (5 modules)**

  - **`intersection_forms.py` (P15.1)** — Intersection forms of 4-manifolds.
    `IntersectionForm`; `intersection_form`, `form_rank`, `form_signature`, `form_type`,
    `is_unimodular`, `is_definite`, `classify_indefinite_form` (Serre: odd→⟨1⟩^p⊕⟨-1⟩^q,
    even→aE8⊕bH); `e8_form`, `hyperbolic_form`, `diagonal_form`, `connected_sum_form`;
    `donaldson_theorem` (definite smooth 4-manifolds must have diagonal form);
    `STANDARD_FORMS` (CP², S²×S², K3, E₈ manifold).

  - **`kirby_calculus.py` (P15.2)** — Kirby diagrams and handle calculus.
    `KirbyComponent`, `KirbyDiagram`, `KirbyMove`; `kirby_diagram`, `linking_matrix`;
    `kirby_stabilize` (K1 move: add ±1-framed unknot);
    `kirby_handle_slide` (K2 move: row/column operations on linking matrix);
    `kirby_to_intersection_form`, `euler_characteristic_kirby`, `signature_kirby`, `b2_kirby`,
    `is_kirby_equivalent`; `kirby_diagram_cp2`, `kirby_diagram_s2xs2`,
    `kirby_diagram_k3_fiber` (E₈ plumbing + 3H); `dehn_surgery_matrix`.

  - **`casson_invariant.py` (P15.3)** — Casson invariant for integer homology spheres.
    `CassonInvariant`; `casson_s3` (λ(S³)=0); `casson_invariant_brieskorn`
    (Neumann–Wahl theorem λ(Σ(a,b,c)) = σ(Milnor fibre)/8, via the Brieskorn
    eigenvalue count of i/a+j/b+k/c mod 2);
    `casson_invariant_surgery` (Walker's formula via Δ''(1));
    `casson_invariant_connected_sum` (additivity); `casson_invariant_lens_space`;
    `dedekind_sum` (sawtooth-function formula with reciprocity);
    `alexander_second_derivative`, `rohlin_mod2`, `is_integer_homology_sphere`, `casson_data`;
    `CASSON_DATABASE` (S³, Poincaré sphere Σ(2,3,5) λ=−1, Σ(2,3,7) λ=−1).

  - **`milnor_fibers.py` (P15.4)** — Milnor fibers and singularity topology.
    `MilnorFiber`; `milnor_fiber_brieskorn` (Brieskorn–Pham z₀^a+z₁^b+z₂^c);
    `milnor_number` (μ=(a-1)(b-1)(c-1)); `milnor_fiber_signature` (cosine formula);
    `milnor_fiber_euler` (χ=1+μ); `seifert_form_trace`; `monodromy_order` (lcm(a,b,c));
    `milnor_fiber_ade` (ADE singularities); `ade_singularity_data`;
    `characteristic_polynomial_monodromy`, `zeta_function_monodromy`, `brieskorn_fiber_homology`;
    `ADE_DATABASE` (E₆ μ=6, E₇ μ=7, E₈ μ=8).

  - **`rohlin_theorem.py` (P15.5)** — Rohlin's theorem and spin structures.
    `SpinStructureResult`, `RohlinCheck`; `check_rohlin_theorem` (spin + smooth → σ≡0 mod 16);
    `is_spin_manifold` (form is even ↔ w₂=0); `kirby_siebenmann_obstruction` (σ/8 mod 2);
    `n_spin_structures` (2^|H¹(X;ℤ/2)|); `check_freedman_realization` (every form topologically
    realizable; smooth obstruction from Rohlin + Donaldson);
    `rohlin_invariant_from_signature` (σ/8 mod 2 for spin manifolds);
    `spin_cobordism_group`, `spin_structure_result`; `ROHLIN_EXAMPLES`
    (S⁴, CP², K3, E₈ manifold, S²×S²).

  **140 new tests across 3 files (Phase 13/14/15); 11 685 tests pass total.**
  All 15 new modules are ruff-clean and mypy-clean.

## [1.4.0] — 2026-06-23

### Added

- **Phase 12 (partial) — Research Frontier: Sheaf Cohomology + Persistent K-Theory**

  First two milestones of Phase 12, opening the research-frontier tier.

  - **`sheaf_cohomology.py` (P12.1)** — Čech sheaf cohomology on finite topological spaces.
    `FiniteSheaf` (frozen dataclass: `open_sets`, `sections`, `restrictions`, `name`);
    `constant_sheaf(open_sets)` — constant ℤ-sheaf (F(U)=ℤ for U≠∅);
    `skyscraper_sheaf(open_sets, stalk_open, rank)` — supported at one open;
    `cech_cohomology(cover, sheaf, max_degree)` — Čech cochain complex (alternating-sum
    coboundary δ^p via restriction maps, SNF → `AbelianGroup` per degree);
    `sheaf_cohomology(open_sets, universe, sheaf)` — convenience wrapper using the
    minimal-open-neighborhood cover {U_x : x ∈ X} (Leray cover for constant sheaf, McCord
    1966: Čech H* equals singular H* of the geometric realisation of the order complex).
    Verified: Sierpiński space → H^0=ℤ; 2-point discrete → H^0=ℤ²; skyscraper → H^0=ℤ.
    41 new tests.

  - **`persistent_ktheory.py` (P12.2)** — Persistent K-theory via Atiyah-Hirzebruch.
    `KTheoryGroups` (frozen dataclass: `k0_rank`, `k1_rank`, rational strings, Betti tuple);
    `KBarcode` (frozen dataclass: `k0_pairs`, `k1_pairs`, `all_pairs`;
    `.k0_betti_at(scale)`, `.k1_betti_at(scale)`, `.euler_characteristic_at(scale)`);
    `k_theory_groups(K)` — rational K⁰/K¹ via AHSS collapse: K⁰⊗ℚ ≅ ⊕H_{2k}⊗ℚ,
    K¹⊗ℚ ≅ ⊕H_{2k+1}⊗ℚ;
    `k0_simplicial`, `k1_simplicial`, `k_betti_numbers` — convenience accessors;
    `k_barcode(filtered, max_dimension)` — runs Twist persistence and partitions bars by
    dimension parity (K⁰=even, K¹=odd). χ_K = rank K⁰ − rank K¹ = χ (topological).
    Verified: point(1,0), S¹(1,1), S²(2,0), T²(2,2); circle 8-pt cloud K⁰+K¹ bars.
    37 new tests.

  **78 new tests; 11 545 core tests passing.**

## [1.3.0] — 2026-06-23

### Added

- **Phase 11 — Lean 4 Formal Verification Expansion (5 new proof files)**

  Extends the `formal/` corpus from 8 to 13 files (0 sorry across all).

  - **`MayerVietoris.lean` (P11.1)** — Short exact sequences + snake lemma.
    `SES` structure (i_inj, exact_at_B, p_surj); `delta_well_defined`; `ses_p_zero_of_im`;
    `snake_delta_exists`; `snake_delta_independent` (connecting class well-defined in A').

  - **`VanKampen.lean` (P11.2)** — Group presentations + amalgamated free product UP.
    `Pres` + `TietzeEquiv` inductive relation; `tietze_elim / add_gen`; `tietze_equiv_symm`;
    `AmalgamDatum` + `Pushout`; `pushout_universal`; `int_hom_determined_by_one`
    (ℤ is the free abelian group on one generator); `int_hom_exists`.

  - **`CohomologyRing.lean` (P11.3)** — Cup product over Bool (ℤ/2).
    Alexander–Whitney `cup` product; `cup_value_assoc` (Bool.and_assoc); `cup_comm_Z2`;
    `coboundary0`; `leibniz_0cochains` (Leibniz rule verified by case analysis).

  - **`PersistencePairing.lean` (P11.4)** — Persistence pairing perfection.
    `pairing_is_perfect` (= `reduce_is_reduced`); `pairs_have_distinct_births` (birth
    indices Nodup); key chain: `isReduced_tail` → `filterMap_getLast_nodup_of_isReduced` →
    `zipWith_range_filterMap_snd_eq` → `map_fst_pairs_eq`.

  - **`SpectralSequences.lean` (P11.5)** — Abstract spectral sequences.
    `ChainCx` structure (d sq = 0 by construction); `d_sq_zero`; `image_sub_kernel`;
    `SpectralSeq`; `const_convergent`; `stabilizes_mono`; `same_diff_implies_same_stab`;
    `const_pages_convergent`.

  **Formal.lean** updated with 5 new imports. **formal/ROADMAP.md** updated.

## [1.2.0] — 2026-06-23

### Added

- **Phase 10 — Scale & Algorithm (5 milestones)**
  - `sparse_linalg`: sparse SNF + auto-routing in `_smith_normal_form`
  - `khovanov_homology(parallel=True)`: ThreadPoolExecutor per bidegree
  - `witness_complex`: `landmark_sample`, `witness_filtration`, `persistent_homology_witness`
  - `streaming_persistence`: `StreamingPersistence` incremental Z/2 reduction
  - `_gpu_backend`: cupy boolean-array Twist+Clearing + `[gpu]` extra
  65 new tests; **11 467 tests total**.

## [1.1.0] — 2026-06-23

### Added

- **Phase 9 — `experimental.spaces` expansion: 6 new canonical representations (13 → 19)** (v1.1.0)

  All implementations live in `src/pytop/experimental/spaces/representations_p9.py`
  and are re-exported from `pytop.experimental.spaces`.

  - **`OnePointCompactificationSpace` (P9.1)** — Alexandroff one-point compactification αX.
    Wraps any `Space`; for finite X the full topology is enumerated (opens of X ∪ opens ∪ {∞}).
    Certificate: compact always; T2 iff base is Hausdorff; connected False when base is compact.
    Factory: `one_point_compactification(space)`.

  - **`StoneCechSpace` / `stone_cech_n()` (P9.2)** — Stone–Čech compactification βℕ.
    Compact T4, separable (ℕ is a countable dense subspace), NOT first-countable (free
    ultrafilter points), NOT T6 (compact Hausdorff is T6 iff metrizable; βℕ not metrizable).
    Cardinals: weight=𝔠, density=ℵ₀, character=𝔠, cellularity=𝔠.

  - **`HilbertCubeSpace` / `hilbert_cube()` (P9.3)** — Hilbert cube [0,1]^ω.
    Points = finite rational tuples; cylinder-neighbourhood separation; T6, compact,
    connected, second-countable, separable.  Cardinals: all ℵ₀.

  - **`SolenoidSpace` / `dyadic_solenoid()` (P9.4)** — dyadic solenoid
    Σ = lim←{S¹ ←² S¹ ←² …}.  Compact, connected, metrizable T6, NOT locally connected.
    `contains()` checks angle compatibility (2θₖ ≡ θₖ₋₁ mod 1).

  - **`UniformSpace` / `UniformProduct` / `UniformSubspace` (P9.5)** — uniform structure
    via metric ε-entourages.  Methods: `entourage(ε)`, `is_cauchy(seq, ε)`,
    `uniform_neighbourhood(x, ε)`.  Factories: `rational_uniform_space()`,
    `metric_uniform_space(name, d, member)`.

  - **`ProfiniteSpace` / `p_adic_integers(p)` (P9.6)** — inverse limit of finite discrete
    groups.  Compact, T6, totally disconnected, metrizable, second-countable.
    `p_adic_integers(p)` builds ℤ_p = lim← ℤ/pⁿ.

- **166 new tests** in `tests/experimental/test_spaces_phase9_representations.py`;
  **11 402 core tests** total.

## [1.0.9] — 2026-06-23

### Added

- **Phase 8 — Profile→Computational upgrade: 6 advanced algebra modules, 16 new functions** (v1.0.9)

  - **`derived_categories` (P8.1)** — `mapping_cone_complex` (cone C(f) of a chain map with
    explicit ∂^C block matrix); `derived_functor_h` (H_n of a chain complex from boundary
    matrices, Betti + torsion via SNF); `triangulated_structure_check` (g∘f=0 + cone Betti
    vs C comparison).

  - **`topos_theory` (P8.2)** — `site_from_finite_topology` (Grothendieck site from a finite
    open-set lattice); `sheaf_on_site` (locality + gluing checks); `sheafification_finite`
    (one-step F⁺ correction for finite sites); `topos_check` (terminal + fiber products +
    subobject classifier → Grothendieck topos verdict).

  - **`operads` (P8.3)** — `associahedron_complex(n)` (K_n Stasheff associahedron as a
    SimplicialComplex; vertices = full binary trees, edges = tree-rotation pairs; Catalan(n−2)
    vertices); `operad_composition_check` (tests µ(µ(a,b),c)=µ(a,µ(b,c)) for all basis
    elements); `bar_construction_sc` (bar complex skeletal model over generators + relations).

  - **`higher_categories` (P8.4)** — `nerve_of_category` (N(C) up to dim 2; 2-simplex for
    composable triples a→b→c with composite a→c present); `kan_fibration_check_sc` (horn-filling
    condition up to max_dim); `homotopy_type_finite_cat` (BC = |N(C)| via Betti numbers, reports
    is_contractible / is_connected).

  - **`noncommutative_topology` (P8.5)** — `k0_group_matrix_algebra(n)` (K₀(M_n(ℚ)) ≅ ℤ by
    Morita invariance; identity_class = n); `spectral_dimension_finite` (log-log regression on
    eigenvalue counting function → d_s); `k1_group_matrix_algebra(n)` (K₁(M_n(ℚ)) ≅ ℚ* by
    Morita; torsion = ℤ/2, free part via p-adic valuations).

  - **`topological_field_theory` (P8.6)** — `cobordism_from_handles(n₀,n₁,n₂)` (χ = n₀−n₁+n₂,
    genus, connectedness); `tqft_dimension_2d(genus)` (Boolean TFT dim=1; A₂ TFT dim=2,1,0 for
    g=0,1,≥2); `handle_signature_tft(n₀,…,n₄)` (4-manifold handles → Euler char, Betti numbers,
    simply-connected flag).

- **Bug fixes:** `_snf_ext` API alignment in `derived_functor_h` (uses `smith_normal_form →
  list[int]` correctly); `nerve_of_category` composability condition fixed (was always-True due to
  `or (b,c) in morph_set`); `betti_numbers` API used in `homotopy_type_finite_cat`.

- **171 new tests** across 6 modules; **11 236 tests pass** total.

## [1.0.8] — 2026-06-22

### Added

- **Profile→Computational upgrade: 4 modules, 13 new functions** — promotes
  "knows but doesn't compute" classifier modules to genuine computational engines:

  - **`shape_theory`** — `link_complex(simplices, vertex)` (lk(K,v) face-closed);
    `is_manifold_triangulation(simplices, n)` (every vertex link ≃ S^{n-1} by
    homology); `has_trivial_shape_sc(simplices)` (contractibility via H_*);
    `shape_anr_check_sc(simplices)` (compact polyhedron ANR/FANR/movability dict).

  - **`coarse_geometry`** — `growth_function_graph(adj, source, max_radius)` (BFS
    ball sizes b(r)); `geodesic_distance_graph(adj, u, v)` (shortest-path length
    or −1); `is_tree_graph(adj)` (connected + |E|=|V|−1); `classify_graph_coarse_growth`
    (polynomial/exponential classification via log-log slope, estimated degree).

  - **`locale_theory`** — `frame_from_finite_topology(open_sets)` (validates closure
    under ∩ and ∪, returns sorted frame); `pseudocomplement_in_frame(open_sets, b)`
    (b* = ∨{c : c∧b=∅}); `well_inside_relation(open_sets)` (b << a iff b* ∨ a = top);
    `is_regular_frame(open_sets)` (every a = ∨{b : b << a}); `is_spatial_finite_frame`
    (∅ and top present, opens separate points).

  - **`dimension_theory`** — `covering_dimension_simplicial(simplices)` (max simplex
    dim); `ind_finite_space(open_sets)` (longest strict chain in specialization poset;
    indiscrete spaces correctly return 0).

- **120 new tests** across 4 new test files; **11 065 tests total**.

## [1.0.7] — 2026-06-22

### Added

- **Three new `experimental.spaces` representations** — expands the protocol from 10 to 13
  canonical representations, each with full `certificate` / `cardinal_certificate` coverage:

  - **`ProductMetricSpace`** — product of two independent metric spaces with the sup metric
    `d((x₁,y₁),(x₂,y₂)) = max(d_X(x₁,x₂), d_Y(y₁,y₂))`. Inherits all metric-space
    separation properties (T0–T6, first-countable, Tychonoff). Factory: `rational_plane()`
    (ℚ²). 20 new tests.

  - **`LexicographicSquareSpace`** — [0,1]² with the lexicographic order topology.
    Certificates: compact, connected, T5, Lindelöf, first-countable; NOT second-countable,
    NOT separable (uncountable cellularity = 𝔠). A key counterexample to the
    "compact T2 ⟹ metrizable" misconception. Factory: `lexicographic_square()`. 29 new tests.

  - **`CantorSpaceRepresentation`** — {0,1}^ω with the product topology. Points as finite
    binary tuples; separation by clopen cylinders at the first differing bit.
    Certificates: compact, T6, totally disconnected, second-countable, separable,
    weight/density/character/cellularity = ℵ₀. Factory: `cantor_space()`. 25 new tests.

- **7 new factory functions** (exported from `pytop.experimental.spaces`):
  `rational_plane`, `lexicographic_square`, `cantor_space`, plus the three class
  constructors `ProductMetricSpace`, `LexicographicSquareSpace`, `CantorSpaceRepresentation`.

- **7 new cross-representation contrast tests** verifying mathematical distinctions
  (connected vs. totally disconnected, second-countable vs. not, T6 vs. undecided, etc.).

**Total: 81 new tests; 10 945 core tests passing (+ 16 opt-in SageMath/SnapPy-oracle tests).**

## [1.0.6] — 2026-06-22

### Added

- **Covering spaces — computational** (`covering_spaces.py`): `CoveringGraph` dataclass,
  `cyclic_voltage_cover` (voltage construction for cyclic covers), `fundamental_group_rank_graph`
  (first Betti number β₁ = |E|−|V|+1 via Euler characteristic), `is_graph_covering_map`
  (sheet-count + uniform-degree check), `universal_covering_tree` (BFS spanning tree). 32 new tests.

- **Fundamental group — computational** (`fundamental_group.py`): `pi1_graph(edges)` —
  fundamental group of a 1-complex via van Kampen + spanning-tree algorithm; first Betti
  number k → free group Fₖ. 14 new tests.

- **Three-manifolds — computational** (`three_manifolds.py`): `mapping_torus_h1(monodromy)` —
  H₁ of the mapping torus of a surface automorphism via Wang sequence cokernel (SNF);
  `lens_space_pi1(p, q)` → ℤ/p. 21 new tests.

- **Homotopy — computational** (`homotopy.py`): `is_contractible_simplicial(simplices)` —
  homology-based contractibility test (H_*(X;ℤ) ≅ H_*(pt;ℤ)); `has_sphere_homology(simplices, n)` —
  sphere homology type check (H_*(X;ℤ) ≅ H_*(Sⁿ;ℤ)). Auto face-closure before boundary matrix. 26 new tests.

- **Degree theory — computational** (`degree_theory.py`): `map_degree_simplicial(sim_map, n)` —
  topological degree of f: Sⁿ → Sⁿ from the 1×1 matrix of `induced_map_on_homology` on H_n. 8 new tests.

- **Manifolds — computational** (`manifolds.py`): `euler_characteristic_simplicial(simplices)` —
  χ = Σ(−1)^k f_k computed combinatorially from any simplicial complex; handles auto face-closure,
  disjoint unions (additivity), and non-manifold inputs. 18 new tests.

### Fixed

- **`mayer_vietoris._snf_ext` infinite-loop on negative matrix entries** — the inner loop had
  `q -= 1` corrections written for C-style truncation division; Python's `//` operator is floor
  division and already gives the correct quotient, so the correction over-adjusted, producing a
  remainder that exceeded the pivot and triggering an infinite swap cycle. Corrections removed.
  All 150-iteration seeded property tests pass in < 0.5 s.

## [1.0.5] — 2026-06-21

### Added

- **Simplicial maps** (`simplicial_maps.py`, P7.2): `SimplicialMap` dataclass + validation,
  `chain_map_matrix` (integer matrix f#_k: C_k(K) → C_k(L)), `induced_map_on_homology`
  (f_*: H_k(K;Z) → H_k(L;Z) via extended SNF), `cone_complex` (contractible CK),
  `suspension_complex` (ΣK with Σ(Sⁿ) ≃ Sⁿ⁺¹). 42 new tests.

- **Nerve complex** (`nerve_complex.py`, P7.3): `nerve_of_cover` (nerve N(U) of finite open
  cover), `good_cover_check` (Nerve theorem preconditions), `cech_nerve` (Čech complex at
  fixed radius via Welzl miniball circumsphere). 30 new tests.

- **Spectral sequences** (`spectral_sequences.py`, P7.4): `SpectralPage` (bigraded Betti/torsion
  groups), `FilteredChainComplex`, `filtered_chain_complex_from_simplices`, `differential_d_r`
  (E^r page differentials), `converges_to` (iterates to E^∞ stability). 25 new tests added
  to existing suite (205 total).

- **Surgery theory** (`surgery_theory.py`, P7.5): `handle_attachment` (K ∪ cone(Sᵏ⁻¹),
  k-handle), `trace_cobordism` (trace W = K ∪ Dᵏ), `trace_homology` (H_*(W;Z) direct
  simplicial computation + Mayer–Vietoris interpretation). 24 new tests.

- **Morse complex** (`morse_complex.py`, P7.6): `MorseChainComplex` (critical simplices +
  Morse boundary matrices), `morse_boundary_operator` (gradient V-path counting with signs,
  DFS on acyclic matching), `morse_chain_complex`, `morse_homology` (H_*(C^M;Z) via SNF +
  cross-validation against simplicial H_*(K;Z) — Morse homology theorem verified). 32 new
  tests. **Phase 7 complete (P7.1–P7.6).**

## [1.0.4] — 2026-06-19

### Added

- **Standard triangulations** (`simplicial_filtration.py`, P7.1): `simplicial_filtration`
  generic builder (face closure, all births = 0, sorted by dimension then lex), plus
  three standard closed-surface triangulations as `FilteredComplex` objects:
  `torus_filtration` (9 vertices, 27 edges, 18 triangles; T² has no torsion, β=(1,2,1)
  for all primes), `klein_bottle_filtration` (9 vertices, 18 triangles; H_1(K;Z)=Z⊕Z/2
  detected: β_1=2 over F_2, β_1=1 over F_3), `rp2_filtration` (6 vertices, 10 triangles;
  minimal Banchoff–Kühnel triangulation; H_1(RP²;Z)=Z/2 detected: β_1=1 over F_2,
  β_1=0 over F_3). UCT torsion-detection confirmed for Klein bottle and RP² (β_2=1 over
  F_2 from Tor(Z/2, Z/2), β_2=0 over odd primes). 33 new tests.

## [1.0.3] — 2026-06-19

### Added

- **TDA Pipeline** (`tda_pipeline.py`, P6.3): `TDAPipeline` — immutable builder for
  composing filtration, reduction, and analysis.  Methods: `.rips()`, `.cech()`,
  `.reduce(method, prime)` (methods: `standard`, `twist`, `cohomology`, `fp`),
  `.pairs()`, `.barcode()`, `.diagram()`, `.landscape()`, `.entropy()`,
  `.bottleneck()`, `.wasserstein()`, `.compare_primes()`, `.summary()`.
  Factory classmethods: `from_points()`, `from_filtration()`. 42 new tests.

## [1.0.2] — 2026-06-19

### Added

- **Persistent homology over Z/p** (`persistent_homology_fp.py`, P6.2):
  `persistence_pairs_fp(filtered, prime)` — standard column reduction over the
  finite field F_p for any prime p ≥ 2.  Alternating-sign boundary operator
  (`(-1)^i` coefficients), modular inverse via Fermat's little theorem.
  For p = 2 the output matches `persistence_pairs` exactly.  Higher primes
  detect Z-homology torsion invisible over F_2 (e.g., RP² torsion classes).
  `is_prime` helper exported publicly. 23 new tests.

## [1.0.1] — 2026-06-19

### Added

- **Čech complex** (`cech_complex.py`, P6.1): `cech_filtration` builds the Čech filtration
  of a finite R^d point cloud via Welzl's miniball algorithm (Gaussian elimination for
  circumsphere, O(d! · n) expected). `persistent_homology_cech` convenience wrapper.
  Rips–Čech sandwich satisfied: each edge birth equals its Rips counterpart divided by 2.
  Pure-Python, zero new dependencies, compatible with all pytop persistence pipelines
  (standard, Twist, cohomology). 29 new tests.

## [1.0.0] — 2026-06-19

### Added

- **Mapper algorithm** (`mapper.py`): `mapper(data, filter_fn, cover)` — constructs the
  Mapper simplicial complex (Singh–Mémoli–Carlsson 2007). `IntervalCover` (uniform
  overlapping interval cover of the filter image), `single_linkage_labels` (built-in
  1-D single-linkage clustering with configurable gap threshold), `MapperNode` (cluster with
  member indices), `MapperComplex` (nodes + simplices + adjacency + connected components).
  Custom `cover`, `cluster_fn`, `gap_threshold`, and `max_simplex_dim` supported.
  Dependency-free. 31 new tests.

## [0.9.9] — 2026-06-19

### Added

- **Persistence diagram distances** (`persistence_distances.py`): `bottleneck_distance`
  (min-max L∞ matching via sorted-threshold binary search + bipartite matching),
  `wasserstein_distance` (p-Wasserstein via Jonker-Volgenant O(n³) Hungarian assignment),
  `persistence_entropy` (Shannon entropy of the persistence distribution),
  `persistence_landscape` / `PersistenceLandscape` (sampled k-th landscape functions on
  uniform time grid). All functions accept `tuple[PersistencePair, ...]` directly and
  support per-degree filtering. Essential bars excluded from metric computations. Dependency-
  free pure Python implementation. 39 new tests.

## [0.9.8] — 2026-06-19

### Added

- **Discrete Morse theory** (`discrete_morse.py`): `discrete_gradient_matching` computes
  an acyclic discrete gradient vector field (Forman 1998) on a finite simplicial complex
  using a greedy cycle-detection algorithm (DFS on V-paths). Produces perfect Morse
  matchings on contractible subcomplexes (one critical 0-cell). `MorsePair` / `MorseMatching`
  data structures, `is_valid_morse_matching` (acyclicity + partition check),
  `check_morse_inequalities` (weak Morse inequalities m_p ≥ β_p and Euler identity via
  integral simplicial homology). Validated on interval, circle (S¹), filled triangle,
  tetrahedron, S², and the 9-vertex torus triangulation. 29 new tests.

## [0.9.7] — 2026-06-19

### Added

- **Persistent cohomology** (`persistent_homology_optimized.py`):
  `persistence_pairs_cohomology` / `persistence_pairs_cohomology_with_stats` — the
  dual algorithm of de Silva–Morozov–Vejdemo-Johansson (2011). It processes
  simplices in filtration order while maintaining the live cocycles (Z/2 cochains)
  with an inverted index, so each new simplex is tested only against cocycles that
  share one of its facets; the youngest cocycle it cobounds dies (elder rule).
  Produces **identical barcodes** to `persistence_pairs` / `persistence_pairs_twist`,
  but on Vietoris–Rips filtrations — where nearly all pairs are *apparent* — it
  does orders of magnitude fewer column operations (40-point circle to dim 2:
  ~130 cochain additions vs ~180 000 for the boundary reduction; ~2–2.5× wall-clock,
  growing with size). Validated against the standard reduction, the Twist algorithm,
  and **GUDHI**. `persistence_pairs_twist` remains the default for
  `persistent_homology_optimized`; cohomology is exposed as a faster peer.

## [0.9.6] — 2026-06-18

### Added / Changed

- **Linear-time planarity** (`graph_planarity.py`): `is_planar` now decides
  planarity via the `O(V+E)` **left-right planarity test** (de Fraysseix–
  Rosenstiehl; Brandes 2009) instead of the exponential rotation-system genus
  search. It decides graphs of *any* size and **never raises** — sparse but
  high-degree planar graphs (e.g. wheels `W9…W40`, large grids) that used to
  exceed the search cap and raise `GraphPlanarityError` now return `True`
  instantly. `graph_genus` is unchanged (it still computes the exact minimum
  genus by rotation-system search). A cheap Euler edge bound pre-rejects dense
  graphs and double-checks the LR verdict on them. Validated against networkx's
  independent planarity test on **all** labelled graphs up to 6 vertices
  (33 867 graphs, 0 disagreements) plus thousands of random larger graphs;
  the committed differential test is gated on networkx.

## [0.9.5] — 2026-06-18

### Performance

- **Planarity scale pass** (`graph_planarity.py`): `is_planar` now rejects dense
  graphs by the Euler edge bound (`E ≤ 3V−6`, or `E ≤ 2V−4` for bipartite graphs,
  detected by 2-colouring) per connected component and *before* the rotation-system
  search cap, and the genus search early-terminates at the first genus-0 embedding.
  `is_planar(K4,4)` 16 624 ms → 0.019 ms; dense `Kₙ` / `K_{m,n}` decide in `O(V+E)`.
  Every verdict is identical (pinned by the networkx Boyer–Myrvold oracle).
- **Khovanov SNF memoisation** (`khovanov.py`): each differential's Smith normal
  form was computed three times (outgoing rank, incoming rank, incoming torsion);
  caching it per bidegree cuts SNF work to exactly 1× — 3× fewer SNF calls, `7_1`
  (the (2,7) torus knot) 265 ms → 109 ms. Identical homology (cross-checked against
  the Jones engine for the new 5_1 case).

### Fixed

- `is_planar(K6)` / `is_planar(K7)` (and any graph whose rotation-system space
  exceeds the search cap but which the Euler edge bound rejects) now return `False`
  instead of raising `GraphPlanarityError`.

### Notes

- Persistence was profiled but left unchanged: the Twist+Clearing kernel is already
  bigint-optimised and the reduction (not the filtration) dominates; the next gain
  needs the dual / persistent-cohomology algorithm. The remaining frontiers
  (polynomial planarity, dual persistence) are documented in `docs/COMPLEXITY.md`.

## [0.9.4] — 2026-06-18

### Fixed
- **The codebase is now mypy-clean and mypy is enforced in CI.** `mypy src/pytop/`
  reported 361 errors (57 files) under the existing lenient config; all are
  resolved. The dominant pattern (301) was the copy-pasted `_matches_any` helper
  declaring `candidates: set[str]` while callers pass `frozenset` constants and
  `set` literals interchangeably — widened to `set[str] | frozenset[str]`. Also:
  `nets.py` metadata dicts annotated `dict[str, Any]`; empty-collection locals
  annotated; a `BasisAnalysis`/`FiniteMapAnalysis` variable-reuse renamed; the
  optional `python-flint` import switched to the `importlib` idiom (version-agnostic,
  no `type: ignore`); and ~16 targeted `type: ignore[code]` for descriptive/
  experimental-layer cases mypy cannot follow (runtime covered by the test suite).
  The CI `mypy` step is now blocking (`continue-on-error` removed). No behaviour
  change; suite unchanged (9 950 passed, 16 opt-in oracle tests skipped).

## [0.9.3] — 2026-06-18

### Fixed
- **CI is green again.** The `ruff check src/pytop/` step had been failing since
  ~v0.8.0 on 34 accumulated lint errors in the Phase 1/2 code (none in the
  Phase 3/4 modules): import sorting (I001), unused imports (F401), quoted
  annotations (UP037), a deprecated import (UP035), dead local variables (F841),
  two undefined annotation names (F821 — `Sequence`, `MetricTopologySpace`), and
  ambiguous loop variables `l` → `row` (E741). No behaviour change; the full
  suite is unchanged (9 950 passed, 16 opt-in oracle tests skipped). This is the
  first release with a passing CI run on Python 3.11 / 3.12 / 3.13.

## [0.9.2] — 2026-06-18

### Added
- **P4.8 — SnapPy 3-manifold differential oracle** (`tests/core/test_snappy_oracle.py`,
  opt-in `PYTOP_SNAPPY_ORACLE=1`, Docker-based): SnapPy — the gold-standard 3-manifold
  software — is the one independent oracle for `dehn_surgery`. A single batched run of a
  local `pytop-snappy` image (Python 3.12 + `snappy`) validates `first_homology_of_surgery`
  against SnapPy's Dehn-filling homology: figure-8 knot surgeries (`p/q` → ℤ/p) and
  Whitehead-link surgeries (ℤ/a ⊕ ℤ/b). Both report the invariant-factor form, so they
  match directly. Skipped by default, so the suite stays fast and Docker-free.

### Tests
- **9 950 passing** (+ 16 opt-in SageMath/SnapPy-oracle tests). Runtime stays
  dependency-free (`dependencies = []`).

## [0.9.1] — 2026-06-18

### Added
- **P4.7 — SageMath/GAP differential oracle** (`tests/core/test_sage_oracle.py`,
  opt-in `PYTOP_SAGE_ORACLE=1`, Docker-based): a single batched run of the
  `sagemath/sagemath` image validates pytop's Alexander and Jones polynomials
  against Sage's independent algorithms, and its van Kampen group abelianisations
  against **GAP** (Klein bottle ℤ⊕ℤ/2, torus ℤ², ℝP² ℤ/2, wedge ℤ³). Skipped by
  default, so the suite stays fast and Docker-free.

### Changed
- Corrected the P4.6 flint-backend documentation: a clean re-measurement (the
  earlier apparent slowdown was concurrent machine load) shows FLINT's exact
  Smith normal form is **~5–8× faster** than the pure-Python routine even on
  pytop's *sparse* boundary/Khovanov matrices. The optional `[fast]` backend is
  kept; `docs/COMPLEXITY.md`, the roadmap and README updated accordingly.

### Tests
- **9 950 passing** (+ 8 opt-in SageMath-oracle tests). Runtime stays
  dependency-free (`dependencies = []`).

## [0.9.0] — 2026-06-18

### Added
- **Phase 4 — performance, correctness, interoperability** (merged via PR #17):
  - `exact_linalg` — public exact integer linear algebra: `smith_normal_form`,
    `integer_rank`, `integer_determinant` (fraction-free Bareiss), `cokernel` →
    `AbelianGroup`. `dehn_surgery` shares this core (DRY).
  - **`docs/COMPLEXITY.md`** — an honest reference of the asymptotic cost and
    practical input limits of every computational engine, plus `Complexity`
    notes on the heavy docstrings.

### Testing
- **Property-based + cross-engine differential test suite**
  (`tests/core/test_property_invariants.py`): Euler–Poincaré; rational Betti =
  integral free rank; `b_i(ℤ/p) ≥ b_i(ℚ)`; HOMFLY-PT Markov (±) / conjugation
  invariance; braid Alexander palindromy; HOMFLY-PT `a=1` = Burau Alexander;
  Dehn-surgery `|H₁| = |det|`; lens-space homeomorphic ⇒ homotopy-equivalent.
- **Differential testing against five independent external oracles**
  (`tests/core/test_external_oracles.py`, test-only `oracles` extra; each block
  skips when its oracle is absent): **sympy** and **python-flint** (exact linear
  algebra), **networkx** (Boyer–Myrvold planarity), **numpy** (signature), and
  **GUDHI** (Vietoris–Rips persistence — first external validation of the TDA
  engine against the gold standard).

### Performance
- **Optional flint-accelerated exact Smith normal form** (`fast` extra): when
  `python-flint` is installed, large dense integer SNFs route to FLINT — identical
  results (the pure-Python routine remains the default and only hard requirement),
  but a dense 30×30 SNF drops from a multi-second coefficient blow-up to ~2 ms,
  speeding up every homology / cohomology / cellular / Khovanov / surgery engine
  built on the SNF. `numpy`/`scipy` are floating-point and cannot accelerate the
  exact core; only a fast exact library (FLINT) can.

### Tests
- **9 950 tests passing** (+42 since v0.8.0). Runtime stays dependency-free
  (`dependencies = []`); the oracle/accelerator libraries are optional extras.

## [0.8.0] — 2026-06-18

### Added
- **Phase 3 geometric & low-dimensional topology** (merged via PR #16). Five new pure-Python,
  dependency-free computational modules:
  - `seifert` — Seifert algorithm from an oriented PD code: `seifert_circles`,
    `seifert_genus_bound`, `seifert_matrix`, `signature` (Sylvester LDLT, no numpy).
  - `LinkDiagram` + `linking_number` / `linking_matrix` (`knot_invariants`) — multi-component
    link diagrams and integer linking invariants.
  - `homfly` — HOMFLY-PT `P(a, z)` from a braid closure via skein recursion
    `a·P(L₊) − a⁻¹·P(L₋) = z·P(L₀)` (descending-defect termination); `Laurent2` two-variable
    Laurent ring; `to_jones()` / `to_alexander()` specialisations. Certified a genuine invariant
    via Markov stabilisation (±) and conjugation.
  - `multivariable_alexander` — `Δ_L(t₁,…,tₙ)` from a `LinkDiagram` via a Wirtinger presentation
    (arcs + intrinsic orientation by component tracing) and Fox calculus over the n-variable
    Laurent ring; `(c−1)`-minor determinant `÷ (t_γ−1)` for links. Replaces the prior stub.
  - `dehn_surgery` — `H₁(M)` of rational/integral Dehn surgery as the SNF cokernel of
    `A_{ii}=pᵢ, A_{ij}=qᵢ·lk(Lᵢ,Lⱼ)`; `first_homology_of_link_surgery`;
    `lens_space_first_homology` + lens-space homeomorphism/homotopy classification;
    `FirstHomology` result type.
  - `khovanov` — Khovanov homology `Kh^{i,j}` with integral **torsion** (cube of resolutions →
    Frobenius algebra `ℤ⟨1,X⟩` with `m`/`Δ` → per-quantum-grading SNF); `KhovanovHomology` with
    graded Euler characteristic.

### Validation
- Differential tests against existing engines (HOMFLY → Jones/Alexander; multivariable Alexander →
  braid Alexander; Khovanov graded Euler characteristic → `jones_polynomial`); known 3-manifolds
  (lens spaces, S¹×S², T³, the Poincaré homology sphere via the E₈ plumbing, L(7,1)≃L(7,2));
  published integral Khovanov groups (trefoil ℤ/2 at (−2,−7), figure-8, Hopf); and `d²=0`.

### Tests
- **9 908 tests passing** (+144 since v0.7.0).

## [0.7.0] — 2026-06-18

### Added
- **Phase 2 algebraic topology — complete (8/8)** (merged via PR #15):
  - `mayer_vietoris` — Mayer–Vietoris LES; extended SNF with transformation matrices;
    φ, ψ, δ as integer matrices; exactness verified at every position.
  - `cellular_homology` — CW complex chain complex → SNF; standard spaces S^n, RP^n,
    CP^n, T², Klein bottle, lens spaces, Moore spaces; `cw_from_simplicial` bridge.
  - `cohomology` — cochain complex δ^k=(∂_{k+1})^T; UCT verified; Alexander-Whitney
    cup product; `CohomologyRing` with `verify_graded_commutativity()`.
  - `van_kampen` — Seifert–van Kampen; GroupPresentation + GroupHomomorphism; amalgamated
    free product; Tietze elimination (cyclic reduction + deduplication); abelianization via
    SNF; `cw_complex_pi1` with disconnected-skeleton guard.
  - `persistent_homology_optimized` — Twist algorithm (Chen–Kerber 2011) + Clearing Lemma;
    `ReductionStats`; shared `_twist_reduce` kernel; **bigint bitmask (~6.6× kernel speedup)**.
  - `cubical_homology` — `CubicalComplex`; `bitmap_to_cubical_filtration`; `persistent_homology_bitmap`.
  - `homology_coefficients` — field-coefficient (Q, Z/p) and relative homology; prime-modulus validation.
- **Phase 1 extensions**: `AlexandroffSpace`, `SubbaseSpace`, `InverseLimitSpace`; cardinal invariants;
  Urysohn witnesses (`DiscreteCountableSpace` → discrete metric); π₁ via McCord order complex.
- **`_snf_ext(compute_transforms=False)`** — skips P/Pinv/Q/Qinv when only D is needed (~80% saving).

### Fixed
- 5 HIGH correctness bugs: `is_hausdorff` certificate bypass; `_close_under_unions` deduplication;
  `_provable_true_props` recursion guard; `_product_pi1` silent exception; Mayer–Vietoris
  torsion-aware exactness check.
- 15 MEDIUM bugs across all Phase 1/2 modules (midpoint formula, union-find refactor, torus
  `group_type` → `"free_abelian_rank_2"`, `QuotientSpace.contains` raises `NotImplementedError`, etc.).

### Tests
- **9 764 tests passing** (+729 since v0.6.0).

### Added
- **Computable space protocol (Milestone S1, experimental)** — `pytop.experimental.spaces`:
  a `Space` representation protocol unifying finite and finitely-presented infinite spaces
  (cofinite, order topology on ℚ, exact metric, opaque), a decidability-honest `Verdict`
  (decided / semi-decidable / undecidable, with witness or counterexample), and a generic
  `is_hausdorff` that computes on finite spaces, uses construction certificates on infinite
  ones, and honestly reports undecidable otherwise. First step of the research-grade roadmap
  (see `docs/CAPABILITIES_AND_ROADMAP.md`).
- **Space predicates & construction closure (Milestone S2, experimental)** — generalized the
  `certificate` interface to any property and added witness-producing predicates `is_t0`, `is_t1`,
  `is_regular`, `is_normal`, `is_compact`, `is_connected` (finite spaces computed from the topology;
  infinite spaces via construction certificates; honest `UNDECIDABLE` otherwise — e.g. compactness
  of a generic metric space). Added finite construction closure — `subspace`, `binary_product`,
  `disjoint_sum`, `quotient` — each returning a `FiniteSpace`, so predicates compose on constructed
  spaces (a product of Hausdorff spaces is computed and verified Hausdorff).
- **Property-reasoning engine (Milestone S3, experimental)** — `pytop.experimental.spaces.reasoning`:
  derives properties of *constructed* spaces — including **infinite** ones, without enumeration — by
  combining construction-preservation theorems (subspace→hereditary, product→productive/Tychonoff,
  sum→coproduct-stable, quotient→image-stable), the pi-Base implication graph, and computed/certified
  leaf verdicts. `derive(space, prop)` returns a `Derivation` with a human-readable explanation tree;
  `explain` renders it; `synthesize(has=…, lacks=…)` searches for a space meeting a property spec.
  E.g. a product of a cofinite and an order space is derived T1; a subspace of an infinite metric
  space is derived regular — each with a proof, no points enumerated.
- **Preservation table cross-validation (experimental)** — the pi-Base ETL now also extracts
  property **meta-properties** (heredity / productivity / disjoint-union flags), exposed via
  `pi_base.property_meta`. A test suite cross-validates the reasoning engine's hand-curated
  `PRESERVATION` table against them in the no-contradiction direction (pi-Base's meta-properties
  are sparse, so they confirm but do not drive the table). Grounds the preservation theorems in
  the referenced database.
- **Extended axioms & representations (Milestone S4, experimental)** — added composite separation
  predicates `is_t3` (regular + T1) and `is_t4` (normal + T1), and the countability/covering
  predicates `is_lindelof`, `is_separable`, `is_second_countable`, `is_first_countable` (trivially
  true on finite spaces; via certificates on infinite ones). Added two representations:
  `SorgenfreyLineSpace` (separable, first-countable, Lindelöf, **not** second-countable, normal) and
  `DiscreteCountableSpace`; extended the cofinite/order/metric certificates accordingly (a generic
  metric space is first-countable but its separability stays honestly undecided).
- **Full separation hierarchy & reasoning extension (Milestone S5, experimental)** — added the
  predicates `is_tychonoff` (T3.5), `is_t5`, `is_t6` (on finite spaces these collapse to T1 = discrete;
  on infinite spaces they use certificates). Extended the reasoning engine's property vocabulary and
  `PRESERVATION` table to all 16 properties with correct construction rules (e.g. Lindelöf and normal
  are **not** productive; second-countable and Tychonoff are hereditary/productive). The engine now
  distinguishes the rational plane Q² (second-countable ⟹ Lindelöf and, via Urysohn metrization,
  normal/T4) from the **Sorgenfrey plane** (regular but famously not Lindelöf and not normal) — by
  preservation plus the pi-Base implication graph, with no enumeration. This completes the core of
  Phase 1 (set-theoretic topology) of the research-grade roadmap.
- **pi-Base atlas ↔ reasoning bridge (experimental)** — `pytop.experimental.spaces.pi_base_space`
  wraps any of the 222 famous pi-Base spaces as a protocol `Space` whose property certificates come
  from pi-Base's deduced trait matrix. The reasoning engine's predicates and `derive` now work on
  famous spaces (Cantor set, long line, real line, …), and those spaces feed into the construction
  wrappers — e.g. `ProductSpace([pi_base_space("Cantor set"), pi_base_space("Cantor set")])` is
  derived compact (Tychonoff). `analyze_pi_base_space(name)` reports all 16 property verdicts.
- **Homology with field coefficients & relative homology (Phase 2, algebraic topology)** —
  `homology_with_coefficients` / `betti_numbers_over` compute ``H_*(K; F)`` over `Q` or `Z/p` by
  Gaussian elimination over the field, and `relative_homology` / `relative_betti_numbers` compute
  ``H_*(K, L; Z)`` for a subcomplex `L`. Demonstrates coefficient dependence — the real projective
  plane has ``H_1(RP^2; Q) = 0`` but ``H_1(RP^2; Z/2) = Z/2`` — and relative homology
  ``H_2(D^2, ∂D^2) = Z``. First step of Phase 2 of the research-grade roadmap.

## [0.6.0] - 2026-06-17

### Added
- **Constructive computational core** — genuine invariant computation from
  raw input, complementing the descriptive profile layer:
  - `homology.py` — integral simplicial homology of a finite `SimplicialComplex`:
    oriented `boundary_matrix`, integer Smith normal form, `simplicial_homology` /
    `homology_groups` / `betti_numbers` (free rank **and** torsion coefficients),
    `reduced_homology`, and `euler_characteristic_via_homology` (cross-checks the
    combinatorial Euler characteristic). Verified on S¹, S², T² (H₁ = ℤ²) and
    ℝP² (H₁ = ℤ/2 torsion).
  - `persistent_homology.py` — real TDA engine added alongside the existing profiles:
    `vietoris_rips_filtration` of a finite metric space, `persistence_pairs` via the
    standard ℤ/2 column reduction, plus `barcode`, `persistence_diagram` and
    `euler_characteristic_curve`.
  - `knot_invariants.py` — `kauffman_bracket` and `jones_polynomial` from a planar-diagram
    code, `alexander_polynomial_from_braid` via the reduced Burau representation, `writhe`,
    `linking_number`, and `is_valid_pd_code`. Verified: trefoil Jones = −t⁻⁴+t⁻³+t⁻¹,
    figure-eight Jones = t⁻²−t⁻¹+1−t+t², Alexander(trefoil) = t−1+t⁻¹.
  - `experimental/convergence_spaces.py` — finite convergence spaces (Dolecki's "royal road"):
    `ConvergenceSpace` with `is_convergence_space` / `is_pretopology` / `is_pseudotopology` /
    `is_topological`, the mutually inverse `convergence_from_topology` ↔
    `topology_from_convergence` bridges, `is_continuous_convergence_map`, and `grill_of_filter`.
  - **pi-Base deductive inference** (`experimental/pi_base.py` + `pi_base_atlas.py`) — a real
    deductive property-inference engine over the pi-Base database (243 properties, 902 implication
    theorems, 222 spaces / 2099 traits; CC BY 4.0, Clontz & Dabbs). `deduce` computes the closure of
    known traits (forward chaining + contrapositive over compound and/or/not formulas) and detects
    contradictions; `find_counterexamples(has=…, lacks=…)` searches the atlas (e.g. compact but not
    Hausdorff); `steen_seebach_index` links to *Counterexamples in Topology* numbers. Data compiled
    by `_internal/pi_base_compile.py`; loaded with stdlib `json` only (no runtime dependency). A
    cross-validation test suite pins pytop's hand-encoded implications against the pi-Base graph.
  - `winding_number.py` — `winding_number`, `circle_map_degree` (degree of S¹→S¹ maps), and
    `vector_field_index` (index of an isolated planar zero) from sampled geometric data.
  - `surface_word_classification.py` — `classify_surface_word`: closed-surface classification from a
    polygon gluing word via corner identification → Euler characteristic, orientability, genus
    (sphere / torus / ℝP² / Klein bottle / genus-g). Verified incl. genus-2 and ℝP²#ℝP² = Klein.
  - `graph_planarity.py` — exact `is_planar` / `graph_genus` for small graphs via rotation-system
    search (K5, K3,3, Petersen non-planar; genus additive over components), plus the Euler edge bound.
- `named_spaces.py` + `space_catalog.py` — 104 canonical named topological spaces across 8 batches:
  - **Batch 1 (20):** Sierpiński space, particular/excluded point topologies, cofinite/cocountable
    topologies, real line, Sorgenfrey line, ℚ, irrationals, Cantor set, Hilbert cube, long line,
    topologist's sine curve, comb space, Warsaw circle, infinite broom, Moore plane, Arens-Fort, Fort space
  - **Batch 2 (12):** discrete/indiscrete/countable-discrete spaces, particular/excluded point on ℕ,
    double origin topology, Michael line, Tychonoff plank, deleted Tychonoff plank, β ℕ,
    Furstenberg topology, pseudo-arc
  - **Batch 3 (12):** unit interval, unit circle, closed unit disk, torus, Cantor cube, Baire space,
    lexicographic square, one-point compactification of ℝ, Cantor fan, Knaster-Kuratowski fan,
    Hilbert space, p-adic integers
  - **Batch 4 (12):** half-open interval, open interval, half-open real line, ℝP², Klein bottle,
    Möbius band, dunce hat, Hawaiian earring, ω₁, ω₁+1, Stone-Čech remainder, one-point
    compactification of ℚ
  - **Batch 5 (12):** ℝ², punctured plane, S², S³, S^n, Sierpiński carpet, Menger curve,
    open cylinder, tube, open topologist's sine curve, Erdős space, complete Erdős space
  - **Batch 6 (12):** ℝ^n, Sorgenfrey plane, one-point compactification of ℕ, ω+1, rational
    sequence topology, particular/excluded point on ℝ, divisor topology, uncountable discrete space,
    double arrow space, annulus, wedge of circles
  - **Batch 7 (12):** upper half-plane, closed upper half-plane, p-adic numbers, Sierpiński triangle,
    ℝP^n, cofinite topology on ℤ, long ray, Knaster continuum, ℂP², ℝ^ω, T^n, open unit disk
  - **Batch 8 (12):** genus-g surface, n-ball, K-topology on ℝ, dyadic solenoid, extended real
    line, {0,1}^c, S²∨S², suspension of Cantor set, quarter plane, punctured torus,
    countable disjoint union of circles, lens space L(p,q)
- `SpaceCatalog` — queryable registry with 99 `SpaceRecord` entries; supports `.get(name)`,
  `.search(**props)`, `.list_all()`, and case-insensitive alias lookup
- `catalog` — module-level singleton (`from pytop import catalog`)

### Documentation
- `docs/user_guide/` — comprehensive 16-chapter user guide in four parallel formats
  (Python scripts, Jupyter notebooks, Markdown, LaTeX/PDF):
  - **Part 0 — Prerequisites (ch01–ch03):** pytop quick start, propositional logic
    (`pytop.logic`), set theory & function fundamentals
  - **Part I — Point-set topology (ch04–ch13):** topological spaces, predicates &
    subset operators, separation axioms (T0–T4), compactness, connectedness,
    countability, continuous maps & homeomorphisms, subspace & product topology,
    quotient topology, initial & final topology
  - **Part II — Metric spaces (ch14–ch16):** metric spaces, metric completeness &
    compactness, metric maps & contracts
  - LaTeX source compiles to a 73-page PDF (`xelatex main.tex`); all listings
    styles (`output`) and chapter cross-references verified

## [0.5.33] - 2026-05-30

### Added
- `topological_field_theory.py` — Atiyah-Segal TFT axioms, cobordism hypothesis, Frobenius algebras,
  Chern-Simons theory, Donaldson theory, factorization algebras, topological strings:
  - `TFTProfile` dataclass with 8 tag frozenset constants
    (`ATIYAH_SEGAL_TAGS`, `COBORDISM_HYPOTHESIS_TAGS`, `FROBENIUS_ALGEBRA_TAGS`,
    `EXTENDED_TFT_TAGS`, `CHERN_SIMONS_TAGS`, `FACTORIZATION_ALGEBRA_TAGS`,
    `DONALDSON_TAGS`, `TOPOLOGICAL_STRING_TAGS`)
  - `get_named_tft_profiles()` — 8 canonical profiles (Atiyah-Segal TFT, cobordism hypothesis TFT,
    2D Frobenius TFT, Chern-Simons TFT, once-extended TFT, factorization algebra TFT,
    Donaldson TFT, topological string TFT)
  - `tft_summary()`, `tft_type_registry()`, `tft_dimension_registry()`
  - `is_extended_tft()`, `satisfies_atiyah_segal_axioms()`,
    `has_frobenius_algebra_structure()`, `admits_higher_categorical_formulation()` — `Result`-returning
    analysis functions
  - `classify_tft()`, `tft_profile_report()` — facade functions
  - 196 tests in `tests/core/test_topological_field_theory.py`

### Fixed
- `__init__.py`: `higher_categories` symbols added to `__all__` (omitted in v0.5.32)

## [0.5.32] - 2026-05-19

### Added
- `higher_categories.py` — quasi-categories, Kan complexes, complete Segal spaces,
  stable ∞-categories, ∞-toposes, dg-categories, Quillen model categories:
  - `HigherCategoryProfile` dataclass with 8 tag frozenset constants
    (`QUASI_CATEGORY_TAGS`, `KAN_COMPLEX_TAGS`, `SEGAL_SPACE_TAGS`, `STABLE_INFINITY_TAGS`,
    `INFINITY_TOPOS_TAGS`, `ADJUNCTION_TAGS`, `MODEL_CATEGORY_TAGS`, `ENRICHED_CATEGORY_TAGS`)
  - `get_named_higher_category_profiles()` — 8 canonical profiles (quasi-category, Kan complex
    / ∞-groupoid, complete Segal space, stable ∞-category, presentable ∞-category,
    ∞-topos, dg-category, Quillen model category)
  - `higher_category_layer_summary()`, `higher_category_chapter_index()`,
    `higher_category_type_index()`
  - `is_infinity_categorical()`, `is_stable_infinity_category()`,
    `has_all_limits_and_colimits()`, `is_presentable_infinity_category()` — `Result`-returning
    analysis functions
  - `classify_higher_category()`, `higher_category_profile()` — facade functions
  - 200 tests in `tests/core/test_higher_categories.py`

## [0.5.31] - 2026-05-19

### Added
- `spectral_sequences.py` — Serre, Adams, Eilenberg-Moore, Atiyah-Hirzebruch, Leray-Hirsch,
  Lyndon-Hochschild-Serre, Bockstein, Grothendieck spectral sequences:
  - `SpectralSequenceProfile` dataclass with 8 tag frozenset constants
    (`SERRE_SS_TAGS`, `ADAMS_SS_TAGS`, `EILENBERG_MOORE_SS_TAGS`, `ATIYAH_HIRZEBRUCH_SS_TAGS`,
    `LERAY_SS_TAGS`, `CONVERGENCE_TAGS`, `DIFFERENTIAL_TAGS`, `FILTRATION_TAGS`)
  - `get_named_spectral_sequence_profiles()` — 8 canonical profiles (Serre fibration SS,
    Adams SS, Eilenberg-Moore SS, Atiyah-Hirzebruch SS, Leray-Hirsch theorem,
    LHS group extension SS, Bockstein SS, Grothendieck SS)
  - `spectral_sequence_layer_summary()`, `spectral_sequence_chapter_index()`,
    `spectral_sequence_type_index()`
  - `is_multiplicative_spectral_sequence()`, `converges_strongly()`,
    `has_collapse_at_e2()`, `is_first_quadrant_spectral_sequence()` — `Result`-returning
    analysis functions
  - `classify_spectral_sequence()`, `spectral_sequence_profile()` — facade functions
  - 170 tests in `tests/core/test_spectral_sequences.py`

## [0.5.30] - 2026-05-19

### Added
- `operads.py` — symmetric/non-symmetric operads, Koszul duality, bar-cobar, A_infty/L_infty/E_n:
  - `OperadProfile` dataclass with 8 tag frozenset constants
    (`ASSOC_OPERAD_TAGS`, `COMM_OPERAD_TAGS`, `LIE_OPERAD_TAGS`, `KOSZUL_DUALITY_TAGS`,
    `INFINITY_ALGEBRA_TAGS`, `LITTLE_DISKS_TAGS`, `TREE_COMPOSITION_TAGS`, `BAR_COBAR_TAGS`)
  - `get_named_operad_profiles()` — 8 canonical profiles (Ass, Com, Lie, A_infty, L_infty,
    little 2-disks E_2, Koszul duality example, colored operad)
  - `operad_layer_summary()`, `operad_chapter_index()`, `operad_type_index()`
  - `is_koszul_operad()`, `has_infinity_algebra_structure()`, `admits_koszul_dual()`,
    `is_binary_quadratic_operad()` — `Result`-returning analysis functions
  - `classify_operad()`, `operad_profile_report()` — facade functions
  - 170 tests in `tests/core/test_operads.py`

## [0.5.29] - 2026-05-19

### Added
- `motivic_homotopy.py` — A¹-homotopy theory, Nisnevich topology, motivic cohomology,
  algebraic K-theory, Milnor K-theory, stable motivic homotopy category, Voevodsky theorems:
  - `MotivicHomotopyProfile` dataclass with 8 tag frozenset constants
    (`A1_HOMOTOPY_TAGS`, `NISNEVICH_TOPOLOGY_TAGS`, `MOTIVIC_COHOMOLOGY_TAGS`,
    `ALGEBRAIC_K_THEORY_TAGS`, `MILNOR_K_THEORY_TAGS`, `STABLE_MOTIVIC_TAGS`,
    `VOEVODSKY_TAGS`, `MOTIVIC_SPHERE_TAGS`)
  - `get_named_motivic_profiles()` — 7 canonical profiles (A¹-homotopy space, Nisnevich
    sheaf, motivic cohomology HZ, algebraic K-theory KGL, Milnor K-theory, S^{1,1}
    motivic sphere, Chow groups, algebraic cobordism MGL)
  - `motivic_layer_summary()`, `motivic_chapter_index()`, `motivic_type_index()`
  - `is_a1_invariant()`, `has_nisnevich_descent()`, `is_motivic_cohomology_theory()`,
    `has_algebraic_k_theory_structure()` — `Result`-returning analysis functions
  - `classify_motivic()`, `motivic_profile()` — facade functions
  - 173 tests in `tests/core/test_motivic_homotopy.py`

## [0.5.28] - 2026-05-19

### Added
- `symplectic_topology.py` — symplectic manifolds, Darboux theorem, Hamiltonian dynamics,
  Lagrangian submanifolds, Kahler manifolds, Moser stability, Gromov non-squeezing:
  - `SymplecticProfile` dataclass with 8 tag frozenset constants
  - `get_named_symplectic_profiles()` — 8 canonical profiles (R^{2n}, T*M, S^2, CP^n,
    T^{2n}, coadjoint orbit SU(2), Gromov non-squeezing, Moser stability)
  - `symplectic_layer_summary()`, `symplectic_chapter_index()`, `symplectic_type_index()`
  - `is_symplectic_manifold()`, `is_lagrangian_submanifold()`, `has_hamiltonian_structure()`,
    `admits_kahler_structure()` — `Result`-returning analysis functions
  - `classify_symplectic()`, `symplectic_profile()` — facade functions
  - 162 tests in `tests/core/test_symplectic_topology.py`

## [0.5.27] - 2026-05-18

### Added
- `predicate_sets.py` — sets defined by membership predicates:
  - `MathSet` dataclass with `contains`, `where` (comprehension), `intersection`, `union`,
    `complement_in`, `to_frozenset`, `sample`; `__and__`/`__or__` operator shortcuts.
  - Base set constants: `N` (ℕ), `Z` (ℤ), `Q` (ℚ), `R` (ℝ), `C` (ℂ), `Sigma` (Σ).
  - Derived constants: `N_plus` (ℕ⁺), `Z_plus` (ℤ⁺), `R_plus` (ℝ⁺).
  - Word aliases: `natural_numbers`, `integers`, `rationals`, `reals`, `complex_numbers`,
    `alphabet`, `positive_naturals`, `positive_integers`, `positive_reals`.
  - Constructor `set_of(base, predicate, name, description)` (alias for `base.where`).
- `predicate_relations.py` — binary relations defined by predicates over two `MathSet`s:
  - `MathRelation` dataclass with `holds`, `restrict_to`, `restrict_between`, `inverse`,
    `compose`; structural tests: `is_reflexive_on`, `is_symmetric_on`, `is_transitive_on`,
    `is_antisymmetric_on`, `is_partial_order_on`, `is_total_order_on`, `is_equivalence_on`.
  - Pre-built constants: `leq` (≤), `lt` (<), `geq` (≥), `gt` (>), `divides` (∣).
  - Constructors: `relation_on` (homogeneous), `relation_between` (heterogeneous).
- `predicate_functions.py` — functions defined by rules with domain/codomain validation:
  - `MathFunction` dataclass with `apply`, `restrict_to`, `compose`; structural tests:
    `is_injective_on`, `is_surjective_on`, `is_bijective_on`.
  - Pre-built constants: `successor`, `square`, `double`, `abs_value`, `negate_fn`.
  - Constructor `function_from(domain, codomain, rule, name, description)`.
- 146 new tests across `test_predicate_sets.py`, `test_predicate_relations.py`,
  `test_predicate_functions.py`.

## [0.5.26] - 2026-05-18

### Added
- `random_relations.py` — structured random relation generators:
  - `random_reflexive_relation` — diagonal forced, Bernoulli off-diagonal.
  - `random_symmetric_relation` — pair-mirroring via upper-triangle Bernoulli.
  - `random_transitive_relation` — Bernoulli start + Warshall transitive closure.
  - `random_partial_order` — DAG construction (random permutation + forward-edge Bernoulli)
    + transitive closure + diagonal; always produces a valid partial order.
  - `random_total_order` — random permutation → reflexive linear order; n(n+1)/2 pairs.
  - `random_equivalence_relation` — random partition into k classes; always satisfies
    reflexivity, symmetry, transitivity.
- `random_functions.py` — structured random function generators:
  - `random_injective_function` — `rng.sample` guarantees distinct values.
  - `random_surjective_function` — coverage-guaranteed construction.
  - `random_bijection` — permutation via `rng.sample`.
  - `random_continuous_function` — rejection sampling with basis preimage criterion;
    supports `FiniteTopologicalSpace` and `LazyTopology`.
  - `random_open_map` — rejection sampling with basis image criterion.
  - `random_closed_map` — rejection sampling with closed-set image criterion.
  - `random_homeomorphism` — random bijections checked for continuous + open.
- `random_generators.py` re-exports all 13 new names; `__init__.py` updated.
- 79 new tests in `test_random_relations.py` and `test_random_functions.py`.

## [0.5.25] - 2026-05-18

### Added
- `random_generators.py` — random and semi-random structure generators:
  - `random_set` with `size`/`min_size`/`max_size`, `element_type` (`int`/`char`/`str`/custom pool),
    `random_order` (shuffle vs sequential), and `seed` for reproducibility.
  - `LazyTopology` — subbasis-backed topology with bitmask UID; no full open-set enumeration.
    Supports `is_open`, `contains_open`, `random_open_set`, `sample_open_sets`, `from_uid`.
  - `random_topology` — returns `FiniteTopologicalSpace` for |carrier| ≤ 5, `LazyTopology` for larger.
  - `random_relation` — Bernoulli density sampling over carrier × carrier.
  - `random_function` — uniform random dict from domain to codomain.
  - `RandomGeneratorError` — validation error for all generators.
- 57 new tests in `tests/core/test_random_generators.py`.

## [0.5.24] - 2026-05-18

### Added
- `logic.py` — propositional logic foundations: `Proposition`, `negate`, `conjunction`, `disjunction`,
  `implies`, `iff`, `for_all`, `there_exists`, `unique_exists`.
- `topology_builders.py` — high-level topology constructors: `make_topology`, `discrete_topology`,
  `indiscrete_topology`, `cofinite_topology`, `sierpinski_space`, `topology_from_basis`,
  `topology_from_subbasis`.
- `sets.py` additions: `make_set`, `empty_set`, `make_family` — ergonomic frozenset constructors.
- `relations.py` additions: `make_relation`, `total_order_from_list`, `equivalence_from_classes`.
- `maps.py` additions: `make_function`, `identity_function`, `constant_function`, `MapBuilderError`.
- `notebooks/spaces_and_predicates.ipynb` updated — frozenset/itertools code replaced with new API.
- 2 new test files (`test_logic.py`, `test_topology_builders.py`); builder tests added to
  `test_sets.py`, `test_relations.py`, `test_maps.py`.

## [0.5.23] - 2026-05-17

### Added
- `derived_categories.py` — derived categories: triangulated structure (TR1-TR4), t-structures
  (BBD 1982, perverse sheaves, heart), semiorthogonal decompositions (Beilinson's exceptional
  collection on P^n, Bondal-Orlov, Fourier-Mukai transforms), dg-enhancements (Lunts-Orlov
  uniqueness), and D^b(Coh(X)) geometry.
  7 named examples, 4 predicates: `is_triangulated`, `has_t_structure`,
  `has_semiorthogonal_decomposition`, `is_dg_enhanced`. Facades: `classify_derived_category`,
  `derived_category_profile`.
- 207 new tests

### Tests
- Total: 7258 tests, all passing

## [0.5.22] - 2026-05-17

### Added
- `foliations.py` — foliation theory: Frobenius integrability, Reeb foliation of S^3
  (Novikov's theorem), Kronecker foliation of T^2 (non-Hausdorff leaf space), taut foliations
  (Sullivan-Thurston-Gabai), Riemannian foliations (Molino), Godbillon-Vey invariant,
  and Haefliger classifying space BΓ_q.
  7 named examples, 4 predicates: `is_frobenius_integrable`, `has_compact_leaf`,
  `is_taut_foliation`, `has_trivial_holonomy`. Facades: `classify_foliation`, `foliation_profile`.
- 209 new tests

### Tests
- Total: 7051 tests, all passing

## [0.5.21] - 2026-05-17

### Added
- `abstract_homotopy.py` — model categories (Quillen axioms, weak equivalences/fibrations/cofibrations),
  homotopy pushouts/pullbacks (derived pushout via cofibrant replacement), ∞-categories (quasi-categories,
  Joyal model structure), stable model categories (spectra), and Bousfield localization.
  7 named examples: Top (Quillen), sSet (Kan-Quillen), Ch(R) (projective), quasi-categories (Joyal),
  spectra (Bousfield-Friedlander), homotopy pushout, left Bousfield localization.
  4 predicates: `is_proper_model_category`, `has_homotopy_limits`, `is_stable_model_category`,
  `admits_bousfield_localization`. Facades: `classify_abstract_homotopy`, `abstract_homotopy_profile`.
- 216 new tests

### Tests
- Total: 6842 tests, all passing

## [0.5.20] - 2026-05-17

### Added

- **`persistent_homology.py`** — new module for TDA, Vietoris-Rips filtration, Čech complexes, persistence diagrams, barcodes, and the structure theorem:
  - `PersistenceProfile` frozen dataclass with `complex_type`, `filtration_type`, `has_finite_barcode`, `is_stable`, `has_essential_classes`, `computable_over_field`, `presentation_layer`, `chapter_targets` fields
  - 7 named profiles: Vietoris-Rips point cloud (finite barcode, Rips-Čech stability), sublevel-set filtration (Morse functions, H_0-barcode), persistence diagram bottleneck (isometry theorem), structure theorem for persistence modules (interval decomposition over fields), Čech/alpha complex (optimal stability), circle point cloud (essential H_1 generator), Mapper algorithm (cover-dependent, not stable)
  - `has_finite_barcode(space)` — persistence barcode finiteness; Rips/Čech/sublevel criteria
  - `is_stable_filtration(space)` — stability theorem applicability; bottleneck-stable families
  - `has_essential_classes(space)` — essential (infinite-persistence) homology classes
  - `has_structure_theorem(space)` — interval-decomposition over a field; Crawley-Boevey theorem
  - `classify_persistence(space)` + `persistence_profile(space)` facade
  - 9 tag constant sets: VIETORIS_RIPS_TAGS, CECH_COMPLEX_TAGS, PERSISTENCE_DIAGRAM_TAGS, STABLE_FILTRATION_TAGS, UNSTABLE_OR_SENSITIVE_TAGS, ESSENTIAL_CLASS_TAGS, SUBLEVEL_SET_TAGS, FIELD_COEFFICIENTS_TAGS, STRUCTURE_THEOREM_TAGS
  - 184 tests, all passing; total test count: 6676

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
