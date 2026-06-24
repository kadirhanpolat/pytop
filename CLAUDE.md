# CLAUDE.md

## Project

`pytop` is a standalone mathematical topology library for Python 3.11+.
It provides point-set topology, knot theory, graph topology, surface classification,
3-manifolds, degree theory, cardinal functions, and more. As of **v1.0.4** it ships a
**constructive computational core** (simplicial homology with field/relative coefficients,
persistent homology / TDA, optimized persistence with Twist+Clearing, persistent cohomology
(de Silva dual), cubical complexes + bitmap persistence, discrete Morse theory, persistence
distances (bottleneck/Wasserstein), persistence landscapes, Mapper algorithm, Čech complex
(Welzl miniball + circumradius), knot invariant polynomials, winding/degree,
surface-word classification, exact graph planarity), a
**pi-Base–backed deductive inference engine** (`pytop.experimental.pi_base`), and a
**research-grade computable-space protocol** (`pytop.experimental.spaces`) for point-set
topology — Phase 1 complete (S1–S5), **Phase 2 complete (8/8)**: field-coeff homology,
relative homology, Mayer–Vietoris LES, cellular homology, cohomology + cup product,
van Kampen → group presentations, optimized persistence (Twist+Clearing), cubical complexes.
**Phase 5 complete (3/3):** discrete Morse theory, persistence distances, Mapper.

- **GitHub:** https://github.com/kadirhanpolat/pytop
- **License:** MIT
- **Version:** see `pyproject.toml` and `src/pytop/__init__.py` (`__version__`)

---

## Architecture: two layers

pytop has two complementary layers — keep this distinction in mind when extending it:

- **Descriptive** — `*Profile` dataclasses + `get_*_profiles()` registries that record curated,
  referenced facts about famous spaces/theorems (most algebraic/advanced modules). They *know*
  invariants; they do not compute them.
- **Constructive** — engines that *compute* invariants from raw input. The v0.6.0+ computational core:
  `homology` (integer boundary matrices → Smith normal form → Betti + torsion),
  `homology_coefficients` (field-coefficient / relative homology — Gaussian elimination over Q and Z/p),
  `mayer_vietoris` (Mayer–Vietoris LES: extended SNF with transformation matrices → explicit homology
  bases; φ, ψ, δ as integer matrices; exactness verified at every position; `_snf_ext` supports
  `compute_transforms=False` to skip P/Pinv/Q/Qinv updates when only D is needed — `_mat_rank`
  uses this path for ~80% inner-loop saving),
  `cellular_homology` (CW complex chain complex → SNF; standard spaces S^n, RP^n, CP^n, T², Klein
  bottle, lens spaces, Moore spaces; `cw_from_simplicial` cross-validation bridge),
  `cohomology` (cochain complex via δ^k=(∂_{k+1})^T; extended SNF → H^k; UCT verified;
  Alexander-Whitney cup product; `CohomologyRing` with graded-commutativity, torus pairing, and
  `verify_graded_commutativity()` method),
  `persistent_homology` (Vietoris–Rips filtration → Z/2 reduction → barcodes),
  `persistent_homology_optimized` (Twist algorithm, Chen–Kerber 2011: dimension-top-down sweep +
  Clearing Lemma; `ReductionStats` with n_cleared / clearing_ratio / n_column_additions;
  shared `_twist_reduce` kernel used by both simplicial and cubical pipelines; **bigint bitmask**
  column representation — `list[int]` Python bigint replaces `list[set[int]]`, pivot via
  `col.bit_length()-1`; ~6.6× kernel speedup),
  `cubical_homology` (`CubicalComplex` with face-closure + ℤ boundary matrix + SNF homology;
  `circle_cubical`, `disk_cubical`, `interval_complex`; `CubicalFiltration` +
  `bitmap_to_cubical_filtration` — lower-star filtration from 2-D pixel arrays with
  f(face) ≤ f(coface) guaranteed; `persistent_homology_bitmap` via Twist+Clearing),
  `van_kampen` (Seifert–van Kampen: GroupPresentation + GroupHomomorphism; amalgamated free
  product; Tietze elimination with cyclic reduction + inverse-duplicate deduplication;
  abelianization via SNF; group identification (`"free_abelian_rank_2"` for T²); CW1Complex route
  with disconnected 1-skeleton guard (raises ValueError); standard spaces S¹∨⋯∨S¹→Fₙ, S²→1,
  T²→ℤ², Klein→⟨a,b|abab⁻¹⟩, RP²→ℤ/2),
  `knot_invariants` (Kauffman→Jones, reduced Burau→Alexander), `winding_number`,
  `surface_word_classification`, `graph_planarity` (rotation-system genus),
  `discrete_morse` (Forman gradient vector fields, V-path acyclicity guard, Morse inequalities),
  `persistence_distances` (bottleneck + Wasserstein via augmented cost matrix + Hungarian;
  `PersistenceLandscape` Bubenik 2015; `persistence_entropy` Shannon),
  `mapper` (Singh–Mémoli–Carlsson 2007: `IntervalCover`, `single_linkage_labels`,
  `MapperComplex`), and
  `experimental.spaces` (research-grade computable-space protocol — see below).
  New computational work should prefer this constructive style.
- **Research-grade point-set layer** (`experimental.spaces`) — a third layer bridging the two above:
  a `Space` protocol + 16 witness-producing predicates + property-reasoning engine that derives
  and *explains* properties of constructed infinite spaces (preservation theorems + pi-Base
  implication graph). **10 representations**: `FiniteSpace`, `CofiniteSpace`, `OrderTopologySpace`,
  `MetricTopologySpace`, `SorgenfreyLineSpace`, `DiscreteCountableSpace`, `OpaqueInfiniteSpace`,
  `AlexandroffSpace` (upset topology of a preorder), `SubbaseSpace` (subbase-generated topology),
  `InverseLimitSpace` (finite inverse system + bonding maps). **Factory functions**:
  `finite_circle()` (4-pt diamond, π₁=ℤ), `finite_sphere(n)` (2(n+1)-pt suspension tower),
  `finite_wedge_circles(k)` (1+3k pt model of S¹∨⋯∨S¹, π₁=F_k). **Cardinal invariants**
  (`cardinal_invariants.py`): weight, density, character, cellularity — exact for finite spaces;
  `cardinal_certificate` hook on each infinite representation; `AlexandroffSpace.certificate`
  provides structural T0 (antisymmetry test) and connectedness (union-find on order graph) verdicts
  without open-set enumeration; `cardinal_certificate` returns character=1, weight=|X| (T0 case).
  **Urysohn witnesses** (`urysohn.py`): `UrysohnWitness` + `urysohn_function(space, x₀, C)`;
  discrete finite → exact indicator; general finite → BFS chain; `MetricTopologySpace` →
  distance-ratio formula; `SorgenfreyLineSpace` → Euclidean formula (τ_std ⊊ τ_Sorgenfrey);
  `OrderTopologySpace` → order-metric formula; `DiscreteCountableSpace` → discrete metric
  (d(x,y)=0 iff x=y) with `method="discrete_metric"` witness. **π₁ computation** (`pi1.py`): `pi1_space(space)`
  via McCord order complex (specialization order → CW1Complex → spanning-tree algorithm);
  T0 quotient for non-T0 inputs; `ProductSpace` → π₁(A)×π₁(B); `SumSpace` → π₁(first).
  **Tietze improvements** (`van_kampen.py`): `_cyclically_reduce` (prefix/suffix inverse-pair
  removal), `_dedup_relators` (duplicate relators up to cyclic conjugation + inversion),
  applied after every Tietze II elimination. `predicates._decide` checks `certificate` first
  so `AlexandroffSpace` (and future subclasses) give structural reasons without enumeration.
  `persistence_betti_numbers(pairs)` counts essential pairs per dimension.
  See `docs/CAPABILITIES_AND_ROADMAP.md` for Phase 1/2 status.

## pi-Base data

`pytop.experimental.pi_base` / `pi_base_atlas` load a compact JSON blob derived from the
[pi-Base](https://topology.pi-base.org) database (CC BY 4.0, Clontz & Dabbs): 243 properties,
902 implication theorems, 222 spaces, 2099 traits. Regenerate it from a local `pi-base/data`
checkout with:

```bash
py -3.14 -m pytop._internal.pi_base_compile --source <path-to-pi-base/data> \
    --out src/pytop/experimental/_pi_base_data.json
```

The compiler may use PyYAML (developer-only); the **runtime loads with stdlib `json`** (no new
dependency). Attribution lives in `PI_BASE_ATTRIBUTION`.

> **Copyright note:** `Topoloji/` holds copyrighted reference textbooks kept for local research
> only. It is git-ignored and must **never** be committed. Likewise, do not vendor the raw
> `pi-base/data` repository — only the derived, attributed JSON blob belongs in the package.

---

## Directory Structure

```
src/pytop/              ← public math API (import from here)
src/pytop/_internal/    ← internal tooling (chapter integration, audit tools, release scripts)
                          NOT exported in __init__.py, NOT part of public API
src/pytop/experimental/ ← research-stage modules (unstable API)
  spaces/               ← computable-space protocol (Phase 1 complete: Space, predicates,
                          reasoning engine, pi-Base bridge — see CAPABILITIES_AND_ROADMAP.md)
tests/core/             ← tests for src/pytop/
tests/experimental/     ← tests for src/pytop/experimental/
examples_bank/          ← topic-based Markdown example files (not importable)
docs/CAPABILITIES_AND_ROADMAP.md  ← honest capabilities assessment + phased roadmap
```

---

## Commands

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest tests/ -q

# Run tests with coverage
pytest tests/ --cov=pytop --cov-report=term-missing

# Run only core tests
pytest tests/core/ -q

# Run only experimental tests
pytest tests/experimental/ -q
```

> **Python interpreter:** Always use `py -3.14` on this machine (not `python` or bare `py`).

---

## User Guide

Located at `docs/user_guide/`. Four parallel formats:

```
docs/user_guide/
  latex/              ← XeLaTeX source (main.tex, chapters/, appendix/, figures/)
  markdown/           ← Markdown files (one per chapter + solutions.md)
  python/             ← Percent-cell scripts (# %% / # %% [markdown])
  notebook/           ← Jupyter notebooks (.ipynb)
  assets/             ← Generated PNGs (ch04/, ch06/, ...)
  tools/              ← build_figures.py (TikZ→PNG pipeline)
```

**TikZ→PNG pipeline:** `py -3.14 docs/user_guide/tools/build_figures.py`
- Reads `.tikz` files from `latex/figures/`
- Compiles with `xelatex` (standalone.cls)
- Rasterizes at 300 dpi via `pdftoppm`
- Writes PNGs to `assets/chNN/`

**Maarif pedagogy blocks** (md + py + ipynb, all 16 chapters):
Every chapter has 5 blockquote blocks after `## 1. Konu`:
`> **Neden bu konu?**` / `> 🔍 **Kendin dene:**` / `> ⚠️ **Sık hata:**` /
`> ↗️ **Bkz.:**` / `> 💭 **Öz-yansıtma:**`
In Python files: `# %% [markdown]\n"""..."""` cell. In notebooks: markdown cell inserted after `## 1. Konu` cell.

**API style rule** (ch10 onwards): use `make_set(...)` / `empty_set()` instead of raw
`frozenset({...})` / `set()` in examples.

**Pedagogical tcolorbox environments** (defined in `latex/main.tex`):

| Environment | Color | Purpose |
|-------------|-------|---------|
| `sezgi` | blue | Intuition / motivating analogy |
| `dikkat` | orange | Common mistakes / warnings |
| `nedenonemli` | green | Why this matters |
| `karsiornek` | violet | Counter-examples |

**`\ipucu{...}` macro** — renders as italic hint text in exercise lists.

**Solutions appendix:** `latex/appendix/solutions.tex` + `markdown/solutions.md` + `python/solutions.py` + `notebook/solutions.ipynb`

**Compile PDF:**
```bash
cd docs/user_guide/latex && xelatex -interaction=nonstopmode main.tex
```

**Run a chapter script:**
```bash
py -3.14 docs/user_guide/python/ch04_topological_spaces.py
```

---

## Branching Strategy

```
master          ← stable releases, tagged (v0.4.0, v0.4.1, ...)
feature/<topic> ← feature branches, merge to master via PR
```

- Never commit directly to `master`
- Tag every release: `git tag vX.Y.Z && git push origin vX.Y.Z`
- **Latest release:** Phase 3 (PR #16, **v0.8.0**); Phase 4 P4.1–P4.6 (PR #17, **v0.9.0**) — property tests (`test_property_invariants.py`), `exact_linalg` core (SNF/rank/Bareiss det/cokernel), complexity discipline (`docs/COMPLEXITY.md`), external differential oracles (`test_external_oracles.py`: sympy/networkx/numpy/python-flint/GUDHI; test-only `oracles` extra, runtime dep-free), optional flint-accelerated SNF backend (`[fast]` extra; **~5–8× faster even on sparse boundary/Khovanov matrices**, identical results)
- **Released v0.9.1:** Phase 4 P4.7 — Docker-based SageMath/GAP oracle (`test_sage_oracle.py`, opt-in `PYTOP_SAGE_ORACLE=1`; Alexander/Jones vs Sage, van Kampen abelianisation vs GAP)
- **Released v0.9.2:** Phase 4 P4.8 — Docker-based SnapPy oracle (`tests/core/test_snappy_oracle.py`, opt-in `PYTOP_SNAPPY_ORACLE=1`; `dehn_surgery` H₁ vs SnapPy Dehn-filling homology — figure-8 & Whitehead-link surgeries; needs a local `pytop-snappy` image)
- **Released v0.9.3:** CI green — fixed 34 ruff lint errors in Phase 1/2 code (PR #20); CI runs ruff + mypy + pytest on Python 3.11/3.12/3.13
- **Released v0.9.4:** `src/pytop` is **mypy-clean** (361 → 0 errors) and **mypy is now blocking in CI** (PR #21); no behaviour change — 9 950 tests pass (+16 opt-in Sage/SnapPy). **Phase 3 & Phase 4 are complete** except explicitly-deferred items: native GAP/Regina (unavailable here — only reachable via the Docker Sage/SnapPy images) and formal verification of the core routines (long-term).
- **Released v0.9.5:** performance/scale pass (PR #22) — `is_planar` Euler edge-bound rejection + genus-0 early termination (`is_planar(K4,4)` 16 624 → 0.019 ms; K6/K7 return `False` instead of raising), and Khovanov per-bidegree SNF memoisation (3× fewer SNF calls; `7_1` 265 → 109 ms). All results identical (networkx + Jones oracles). Persistence profiled but left unchanged — its next gain needs the dual/cohomology algorithm (noted in `docs/COMPLEXITY.md`). 9 955 tests pass.
- **Released v0.9.6:** first "frontier" closed (PR #23) — `is_planar` now uses the `O(V+E)` **left-right planarity test** (Brandes 2009) instead of the exponential rotation-system search, so it decides any graph and **never raises** (`W9…W40`, large grids that used to raise `GraphPlanarityError` now return `True`). `graph_genus` unchanged. Validated against networkx on **all** ≤6-vertex graphs (33 867, 0 disagreements) + random larger. 9 960 tests pass.
- **Released v0.9.7:** second frontier closed (PR #24) — **persistent cohomology** (`persistence_pairs_cohomology`), the de Silva–Morozov–Vejdemo-Johansson incremental dual algorithm (live cocycles + inverted index; youngest-cocycle-dies elder rule). Identical barcodes to the standard/Twist reductions but orders of magnitude fewer column ops on Rips (circle n=40 d=2: 132 vs 178 789; ~2–2.5× wall-clock). Validated against standard reduction + Twist + **GUDHI**. `persistence_pairs_twist` stays the default; cohomology is a faster peer. Both documented frontiers (poly planarity, dual persistence) now closed. 9 975 tests pass.
- **Released v0.9.8:** Phase 5 P5.1 — **Discrete Morse Theory** (`discrete_morse`): `MorsePair`, `MorseMatching`, `MorseInequalities`; `discrete_gradient_matching` (greedy + V-path DFS acyclicity guard); `is_valid_morse_matching`; `check_morse_inequalities`. Perfect matchings: contractible spaces → 1 critical cell, S^1 → 2, S^2 → 2, torus χ=0. 29 new tests.
- **Released v0.9.9:** Phase 5 P5.2 — **Persistence distances & descriptors** (`persistence_distances`): `bottleneck_distance` (binary search + max bipartite matching); `wasserstein_distance` (Jonker-Volgenant O(n³) Hungarian, augmented (m+n)×(m+n) cost matrix); `PersistenceLandscape` (Bubenik 2015, k-th tent on grid); `persistence_entropy` (Shannon entropy of bar lengths). Dependency-free. 39 new tests.
- **Released v1.0.0:** Phase 5 P5.3 — **Mapper algorithm** (`mapper`): Singh–Mémoli–Carlsson (2007) full pipeline — `IntervalCover` (overlapping uniform cover), `single_linkage_labels` (1-D single-linkage), `mapper()` (filter → cover → pullback clustering → nerve complex up to configurable dimension), `MapperComplex` with `connected_components()` / `adjacency()`. Custom `cluster_fn` and `cover` supported. 31 new tests. All Phase 5 TDA frontiers (P5.1–P5.3) closed. **10 074 tests pass.**
- **Released v1.0.1:** Phase 6 P6.1 — **Čech complex** (`cech_complex`): `cech_filtration` + `persistent_homology_cech`. Welzl's miniball (Gaussian elimination circumsphere). Rips–Čech sandwich verified. 29 new tests.
- **Released v1.0.2:** Phase 6 P6.2 — **Persistence over Z/p** (`persistent_homology_fp`): `persistence_pairs_fp(filtered, prime)` over F_p for any prime p. Alternating-sign boundary, Fermat modinv. Torsion detection. `is_prime` helper. 23 new tests.
- **Released v1.0.3:** Phase 6 P6.3 — **TDA Pipeline** (`tda_pipeline`): `TDAPipeline` immutable builder. `.rips()/.cech()/.reduce(method)/.pairs()/.barcode()/.diagram()/.landscape()/.entropy()/.bottleneck()/.wasserstein()/.compare_primes()/.summary()`. All 4 reduction methods (standard/twist/cohomology/fp). 42 new tests.
- **Released v1.0.4:** Phase 7 P7.1 — **Standard Triangulations** (`simplicial_filtration`): `simplicial_filtration()` (generic simplicial complex filtration builder), `torus_filtration()` (7-vertex minimal triangulation of T²), `klein_bottle_filtration()` (8-vertex minimal Klein bottle Δ-complex), `rp2_filtration()` (6-vertex minimal RP² triangulation). All compatible with the full TDA pipeline (Twist, cohomology, Z/p). **Lean 4 formal verification** — `urysohn_lemma` (Sierpinski-target Urysohn, T₄ → separating Bool map), `banach_fixed_point` (contraction iteration + geometric series Cauchy bound). All `sorry` tactics eliminated from project-owned `.lean` files.
- **Released v1.0.5:** Phase 7 P7.2–P7.6 — **Combinatorial topology complete**: simplicial maps (`SimplicialMap`, `induced_map_on_homology`, `cone_complex`, `suspension_complex`), nerve complex (`nerve_of_cover`, `good_cover_check`, `cech_nerve`), spectral sequences (`SpectralPage`, `differential_d_r`, `converges_to`), surgery theory (`handle_attachment`, `trace_cobordism`, `trace_homology`), Morse complex (`MorseChainComplex`, `morse_boundary_operator`, `morse_homology`). 186 new tests; 9 959 tests total.
- **Released v1.0.6:** **Profile→Computational upgrades** (6 modules) + critical `_snf_ext` bug fix. New computational functions: `is_contractible_simplicial`, `has_sphere_homology` (homotopy); `map_degree_simplicial` (degree_theory); `euler_characteristic_simplicial` (manifolds); `pi1_graph` (fundamental_group); `mapping_torus_h1`, `lens_space_pi1` (three_manifolds); `CoveringGraph`, `cyclic_voltage_cover`, `fundamental_group_rank_graph`, `is_graph_covering_map`, `universal_covering_tree` (covering_spaces). Bug fix: `_snf_ext` `q -= 1` correction removed (Python floor division ≠ C truncation division — caused infinite swap cycle for negative matrix entries). 119 new tests; **10 864 tests total**.
- **Released v1.0.7:** **`experimental.spaces` extended representations** (10 → 13). Three new canonical infinite-space representations: `ProductMetricSpace` (sup-metric product of two metric spaces; factory `rational_plane()` = ℚ²); `LexicographicSquareSpace` ([0,1]² with lex order topology — compact, T5, NOT second-countable, cellularity=𝔠; factory `lexicographic_square()`); `CantorSpaceRepresentation` ({0,1}^ω — compact, T6, totally disconnected, second-countable; factory `cantor_space()`). Full `certificate` + `cardinal_certificate` coverage on all three. 81 new tests; **10 945 tests total**.
- **Released v1.0.8:** Phase 8 Profile→Computational upgrades (4 modules, 13 functions): `shape_theory` (link complex, manifold triangulation check, ANR), `coarse_geometry` (growth function, geodesic distance, coarse growth classification), `locale_theory` (frame from topology, pseudocomplement, well-inside, regular frame), `dimension_theory` (covering dimension, ind for finite spaces). 120 new tests; **11 065 tests total**.
- **Released v1.0.9:** Phase 8 Profile→Computational: 6 advanced algebra modules — `derived_categories`, `topos_theory`, `operads`, `higher_categories`, `noncommutative_topology`, `topological_field_theory`. 171 new tests; **11 236 tests total**.
- **Released v1.1.0:** Phase 9 — `experimental.spaces` expansion: 6 new representations (13 → 19) — `OnePointCompactificationSpace`, `StoneCechSpace` (βℕ), `HilbertCubeSpace` ([0,1]^ω), `SolenoidSpace`, `UniformSpace`+`UniformProduct`+`UniformSubspace`, `ProfiniteSpace`+`p_adic_integers`. 166 new tests; **11 402 tests total**.
- **Released v1.2.0:** Phase 10 — Scale & Algorithm (5 milestones): `sparse_linalg` (sparse SNF + auto-routing in `_smith_normal_form`), `khovanov_homology(parallel=True)` (ThreadPoolExecutor), `witness_complex` (landmark_sample + witness_filtration + persistent_homology_witness), `streaming_persistence` (StreamingPersistence incremental Z/2 reduction), `_gpu_backend` (cupy boolean-array Twist+Clearing + `[gpu]` extra). 65 new tests; **11 467 tests total**.
- **Released v1.3.0:** Phase 11 — Lean 4 formal verification expansion (5 new proof files, 0 sorry).
- **Released v1.4.0:** Phase 12 P12.1–P12.2 — `sheaf_cohomology` (Čech cohomology of a sheaf on a finite space via Leray covers) + `persistent_ktheory` (rational AHSS K⁰/K¹ + parity-partitioned barcode). 78 new tests.
- **Released v1.5.0 (latest):** Phases 13–15 — 15 new pure-Python modules. **Phase 13 (Homotopy):** `chain_homotopy`, `eilenberg_maclane`, `massey_products`, `hopf_invariant`, `sullivan_models`. **Phase 14 (Advanced Knot Homology):** `khovanov_odd`, `grid_floer` (HFK̂ over 𝔽₂), `concordance` (τ/s/σ), `satellite_knots` (exact torus-knot Alexander division), `virtual_knots`. **Phase 15 (4-Manifold Topology):** `intersection_forms` (Sylvester congruence signature), `kirby_calculus`, `casson_invariant` (Neumann–Wahl λ=σ(F)/8), `milnor_fibers`, `rohlin_theorem`. 140 new tests; **11 685 tests total**. All 15 modules ruff-clean + mypy-clean.
- **Released v1.6.0 (Phase 16 P16.1–P16.3 Framework Complete):** **Empirical validation & oracle ecosystem** — P16.1 benchmark suite ✅ (37 tests: minimal triangulations, knot tables, large graphs, performance baselines); P16.2 oracle parity framework ✅ (extended knot table 6→40 primes, SnapPy H₁ Dehn surgery, K-theory AHSS validation, 8 oracle tests); P16.3 statistical validation ✅ (10K random ER 1-skeleta, **pytop = GUDHI Betti parity 100.0%** across all 10 000 complexes, 0 outliers, avg 4.35ms/complex, JSON report, outlier analysis). `tests/validation/`: 107 passing, 6 skipped (benchmark+oracle+statistical+betti-parity). **Knot table:** 51 primes (unknot–17_1); 50+ target met — adds a verified torus-knot tail (T(3,5)=10_124, T(2,11..17)) with pytop-computed Alexander + exact closed-form Jones. Also **corrected 7 low-crossing entries** (4_1, 5_1, 5_2, 6_2, 6_3, 7_1, 8_19) whose legacy Alexander/Jones were placeholder/wrong — each recomputed from a braid word via pytop (Burau Alexander + braid-closure→PD Kauffman Jones) and triple-checksummed against the knot determinant (|Δ(−1)| = |V(−1)| = det, V(1)=1); 8_19 genus 4→3 fixed. The **8_x/9_x/10_x Jones (plus 6_1, 7_2–7_7) are now backfilled from the SageMath oracle** (Docker `sagemath/sagemath`, `Knots().from_table(n,k).jones_polynomial()`), transformed to the table convention (mirror-calibrated against 3_1/5_1/7_1) and each verified `|V(−1)|=det` and `V(1)=1`; a universal `test_all_jones_satisfy_v1_equals_one` guard locks every entry. The matching **Alexander** polynomials were also backfilled from Sage (`alexander_polynomial()`, canonical Δ(1)=+1, det-verified — 37 entries were wrong placeholders), locked by `test_all_alexander_satisfy_delta1_unit` (|Δ(1)|=1). Knot **genus** fields were likewise corrected — set to `span(Δ)/2` (the exact 3-genus for alternating/torus knots; 32 entries were wrong, e.g. 8_1 twist knot 3→1), locked by `test_genus_matches_alexander_span` (2·genus = Alexander span). Knot table Jones/Alexander/genus are now fully oracle-verified. **Oracle integration:** ✅ **GUDHI cross-validation wired and passing** — `betti_parity.py` (pytop vs GUDHI/Ripser persistent Betti-at-scale on point clouds) + `test_statistical_validation.py` GUDHI `SimplexTree` path (`compute_persistence(persistence_dim_max=True)` so top-dimension H₁ is computed, not skipped). Ripser is N/A for abstract 1-skeleta (needs point clouds) and is covered on real point clouds in `test_betti_parity.py`. Always-on guard `test_500_random_complexes_gudhi_parity` asserts 100% pytop=GUDHI in the default suite. **Status:** All Phase 16 framework milestones (1–3) complete; GUDHI oracle cross-check live. Knot table expanded to 51 (50+ target met). **Agreement matrix now populated & persisted** — a Docker-free internal oracle (`OracleAgreementBuilder.test_torus_knot_alexander_internal`) cross-checks 9 torus-knot Alexander polynomials computed live by pytop's reduced-Burau engine against the Sage-verified table (matched up to the ±t^k unit by `canonical_alexander`), and GUDHI persistent-Betti rows populate alongside; `generate_oracle_matrix()`/`persist_oracle_matrix()` emit `docs/validation/oracle_matrix.{json,md}` (snapshot 15/15 = 100%). SnapPy/Sage rows attach automatically when their Docker images run.

---

## Phase 7 Roadmap: Combinatorial Topology & Geometric Structures

Phase 7 focuses on combinatorial/geometric topology — richer simplicial structures, algebraic invariants from geometric input, and spectral methods. Six planned milestones:

| Milestone | Module | Description |
|-----------|--------|-------------|
| **P7.1** ✅ | `simplicial_filtration` | Standard triangulations: torus, Klein bottle, RP² (7–8 vertex minimal) |
| **P7.2** | `simplicial_maps` | Simplicial maps + chain-level induced homomorphisms; `SimplicialMap`, `induced_map_on_homology`, `cone_complex`, `suspension_complex` |
| **P7.3** | `nerve_complex` | Nerve theorem utilities: `nerve_of_cover`, `good_cover_check`, `čech_nerve` from open covers; Nerve ≃ union for good covers |
| **P7.4** | `spectral_sequences` | Leray–Serre spectral sequence (filtered chain complex → E^r pages → E^∞); `SpectralPage`, `differential_d_r`, `converges_to` |
| **P7.5** | `surgery_theory` | Handle decomposition: `handle_attachment`, `trace_cobordism`, `trace_homology` (Mayer–Vietoris for handle gluing); Dehn surgery cross-validation |
| **P7.6** | `morse_complex` | Morse complex from discrete gradient: `morse_chain_complex`, `morse_boundary_operator`, `morse_homology`; validates equality with simplicial H_* |

**Deferred (long-range):** sheaf cohomology, persistent K-theory, formal verification of SNF correctness (PersHomology.lean remaining bodies).

---

## Phase 16–20 Roadmap: Validation, Performance & Maturity

Post-Phase-15 development focuses on empirical validation, performance optimization, documentation maturity, and ecosystem readiness. Five planned phases (est. 12–18 months):

### Phase 16: Empirical Validation & Oracle Ecosystem

Validate computational results against established external systems and curated benchmark suites.

| Milestone | Module | Description |
|-----------|--------|-------------|
| **P16.1** ✅ | `benchmark_suite` | Public dataset collection: minimal triangulations (T²/Klein/ℝP² with verified Betti/torsion), 51-knot table (unknot–17_1 with Alexander/Jones), large grid library (3×3–40×40, all confirmed planar). 37 tests; ruff/mypy clean. |
| **P16.2** ✅ | `oracle_parity` | Oracle parity framework: extended knot table (6→51 primes), SnapPy H₁ Dehn surgery oracle, K-theory rational AHSS validation (S¹, S²). **Complete:** OracleAgreement, AgreementMatrix, 51-prime knot table (50+ target met), SnapPy tests, K-theory validation. **Agreement matrix now populated & persisted** — a Docker-free **internal oracle** cross-checks 9 torus-knot Alexander polynomials computed live by pytop's reduced-Burau engine (`torus_knot_alexander_poly`) against the Sage-verified table (`canonical_alexander` quotients out the ±t^k unit), and GUDHI persistent-Betti rows populate alongside. `generate_oracle_matrix()` + `persist_oracle_matrix()` emit `docs/validation/oracle_matrix.{json,md}` (current snapshot **15/15 = 100%**: pytop_internal 9/9 + GUDHI 6/6). 11 oracle tests. SnapPy/Sage rows still add live when their Docker images are present. |
| **P16.3** ✅ | `statistical_validation` | Random complex validation: 10K random Erdős–Rényi 1-skeleta (5–50 vertices), pytop H₀/H₁ **cross-validated against GUDHI** — parity 100.0% on all 10 000 complexes, 0 outliers, avg 4.35ms/complex, JSON report. GUDHI `SimplexTree` path uses `persistence_dim_max=True` (top-dim H₁). Always-on 500-complex GUDHI guard in default suite. Ripser N/A for abstract complexes (point-cloud parity in `test_betti_parity.py`). |

**Current Status:** 
- P16.1 ✅ complete (37 tests: 4 minimal triangulations, 6 small graphs, 8 knot invariants, 5 large graphs, 8 performance benchmarks)
- P16.2 ✅ complete (OracleAgreement/AgreementMatrix, extended knot table 51 primes (50+ target met), SnapPy H₁ oracle, K-theory AHSS validation; 11 oracle tests; 109 validation tests pass, 6 skip). **Agreement matrix populated & persisted** Docker-free via the internal torus-knot Alexander oracle (pytop reduced-Burau vs Sage-verified table, 9/9) + GUDHI persistent Betti (6/6) → `docs/validation/oracle_matrix.{json,md}`, 15/15 = 100%. SnapPy/Sage rows attach automatically when their Docker images run.
- P16.3 ✅ complete — 10K run cross-validated against GUDHI: 10,000/10,000 complexes, **pytop = GUDHI parity 100.0%**, 0 outliers, avg 4.35ms/complex

### Phase 17: Performance & Scale

Profiling-driven optimization and parallel scaling.

| Milestone | Module | Description | Status |
|-----------|--------|-------------|--------|
| **P17.1** ✅ | `profiling_infrastructure` | cProfile + flamegraph hooks. Memory tracking via `tracemalloc`. Identify hotspots in SNF, persistent_homology, khovanov_homology per dataset. Report: top 5 bottlenecks with call graphs in `docs/PERFORMANCE.md`. | **Complete:** `@profile_call` decorator + `context_profile` context manager, ProfileStats/ProfileReport dataclasses, `generate_markdown_report()` + `generate_json_report()`, pytest fixtures w/ ProfileCollector, benchmark_runner CLI, 8 homology/persistence/knot benchmarks, 86 comprehensive tests (ruff/mypy clean), `docs/PROFILING.md` user guide + `docs/PERFORMANCE.md` baseline snapshot. Commits: ee6c420, 4572aa7, 1552d31, fdd037a, be84a1b, 93cf786, 96e56a4. |
| **P17.2** ✅ | `algorithm_optimization` | Method selection in `persistent_homology()`: 'twist' (default, Chen–Kerber 2011 + Clearing Lemma), 'standard' (Z/2 reduction), 'cohomology' (incremental). Bigint bitmask optimization ~5–6× kernel speedup. Speedup: 1.03–1.11× on 30–150pt Rips; clearing ratio 1–3% (higher on structured data). 6 benchmarks; all 190 persistent_homology tests pass. Commits: 3cd3051. |
| **P17.3** ✅ | `parallel_scaling` | Two scaling wins shipped: **(1)** inductive Vietoris–Rips construction (14–19× build speedup, byte-identical output); **(2)** size-aware **auto reduction routing** — `persistence_pairs_auto` / `select_reduction_method` / `AUTO_COHOMOLOGY_THRESHOLD` (=1024) route small complexes to Twist, large Rips to the de Silva dual cohomology (hundreds of cochain adds vs millions of column XORs). `persistent_homology(method="auto")` is now the **default**; output byte-identical to twist/cohomology/standard (universal cross-validation test). **End-to-end speedup 1.7× (n=150) → 12.2× (n=350, 22.4s→1.8s).** Planned SciPy CSR (Strategy 3) superseded — bigint-bitmask XOR already beats it. 11,921 tests pass + GUDHI parity unchanged. Strategy doc: `docs/P17_3_PARALLEL_SCALING.md`. |

**Target:** Rips n=500 in <1s (current ~5s), memory linear in simplex count.

**Phase 17 P17.1 Status (2026-06-23):** All deliverables complete. Infrastructure foundation ready for P17.2 optimization work.

### Phase 18: Documentation & Pedagogy ✅

Complete user guide, auto-generated API reference, and worked-example repository.

| Milestone | Module | Description | Status |
|-----------|--------|-------------|--------|
| **P18.1** ✅ | `user_guide_completion` | All 16 chapters verified (LaTeX, Markdown, Python, Jupyter). Maarif pedagogy blocks (5/chapter): Neden bu konu?, Kendin dene, Sık hata, Bkz., Öz-yansıtma. TikZ→PNG pipeline regenerated 8 figures at 300 dpi. Cross-format consistency verified. | Complete: 85-page PDF, 8 figures, 5 pedagogy blocks/ch |
| **P18.2** ✅ | `api_documentation` | Sphinx autodoc on 225 public modules. Generated 225 HTML pages + modindex + genindex. ReadTheDocs configuration (`.readthedocs.yml`). Search-enabled build. | Complete: 225 module stubs, HTML build green |
| **P18.3** ✅ | `example_bank` | 36+ worked examples: homology (6), knot theory (6), TDA pipelines (5), manifolds (5), graph topology (4), cardinal functions (3), combinatorial topology (5), advanced algebra (3). Problem/Solution/Expected per example. Category index + learning path in `examples_bank/README.md`. | Complete: 36+ examples, 8 categories, comprehensive README |

**Status:** All P18.1–P18.3 milestones complete. `docs/user_guide/` 100% verified; API reference built (225 modules); example bank delivered (36+ examples).

### Phase 19: API Stability & Ergonomics

Deprecation policy, error message clarity, and API surface consistency.

| Milestone | Module | Description | Status |
|-----------|--------|-------------|--------|
| **P19.1** ✅ | `error_messages` | Audit and improve error messages following WHY-HOW-THEN pattern. 3 functions improved: max_dimension validation, empty carrier check, method parameter validation. All error messages provide parameter explanation + concrete examples. 184 tests pass. Commits: 6c6bb6c. | **Complete:** `docs/P19_API_STABILITY.md` policy document. |
| **P19.2** ✅ | `deprecation_policy` | 18-month deprecation window defined (1.x → removed in 2.0.0). Reusable internal `@deprecated` decorator (`src/pytop/_deprecation.py`) emits a WHY-HOW-THEN `DeprecationWarning` on function call / class instantiation and prepends a `.. deprecated::` Sphinx note; attaches `__deprecated__` metadata. Applied to the 4 `preservation_legacy` facades. `DEPRECATIONS.md` is the single registry (policy + Active table + **Candidates / soft deprecations** + Removed + per-symbol migration guide). 30 tests pass (`test_deprecation.py`, `test_preservation_legacy_deprecated.py`). Commit: 714b5c6. | **Complete.** |
| **P19.3** ✅ | `api_consistency` | Naming/param/return audit in `docs/API_DESIGN.md`: computational entry points, method-selection vs dedicated functions, predicates/constructors; 7 rules for new public API; 3 audit findings. Finding #3 (`persistent_homology_optimized` is a historical alias of `persistent_homology(method="auto")`) **resolved** with a soft-deprecation note on the wrapper docstring + a `DEPRECATIONS.md` *Candidates* entry (no `DeprecationWarning` until the 1.7.0 line opens; identical barcodes). Findings #1/#2 documented as intentional. Commit: 714b5c6. | **Complete.** |

**Target:** Zero ambiguous error messages; all public functions follow consistent naming/param conventions; SemVer v2.0.0 migration guide.

### Phase 20: Ecosystem & Release Maturity

PyPI publication, CI/CD hardening, and community onboarding infrastructure.

| Milestone | Module | Description | Status |
|-----------|--------|-------------|--------|
| **P20.1** ✅ | `ci_cd_hardening` | Test matrix: Python 3.11, 3.12, 3.13, 3.14. All checks (ruff, mypy, pytest + coverage, docs) green on Ubuntu CI. Version bumped to 1.6.1-dev; pyproject.toml + classifiers updated. Commits: e27bd87. | **Complete:** `.github/workflows/ci.yml` updated; 4-version test matrix verified. |
| **P20.2** ✅ | `pypi_publishing` | PyPI publishing automated via GitHub Actions **Trusted Publishing** (OIDC, no stored tokens) — `.github/workflows/publish.yml` builds sdist+wheel, runs `twine check`, version-vs-tag guard, publishes to PyPI on `v*` tags + manual TestPyPI dry-run. Version single-sourced in `pyproject.toml`/`__init__.py`. | **Complete (v1.7.0):** `python -m build` clean, `twine check` PASSED on both artifacts, `_pi_base_data.json` ships in wheel+sdist, zero-dependency clean-room import verified. **Only remaining live-repo op:** one-time PyPI pending-publisher registration + pushing the `v1.7.0` tag (see `docs/P20_RELEASE_READINESS.md`). |
| **P20.3** ✅ | `community_onboarding` | `CONTRIBUTING.md` (dev setup, two-layer architecture, code style, API rules, tests, deprecations, conventional commits + PR flow, issue reporting, first-timer pointer). GitHub issue templates: `bug_report.yml`, `feature_request.yml`, `docs.yml` + `config.yml` (+ `PULL_REQUEST_TEMPLATE.md`). `good first issue` label live on GitHub; 12 curated, file-grounded starter tasks in `docs/GOOD_FIRST_ISSUES.md` **opened as labelled issues #35–#46** (10+ target met). Commit: 714b5c6. | **Complete.** 48h issue-response SLA is the only remaining live-repo op. |

**Target:** Published on PyPI; CI green across 4 Python versions; 10+ external contributors; <48h issue response time.

**Release Timeline:**
- **v1.7.0** (Q3 2026): Bundle P17.2 + P19.1 (method selection, error clarity)
- **v2.0.0** (Q2 2027): Break with 18-month deprecation window; drop 3.11 support

---

**Priority order:** P16 (validation foundation) → P18 (docs for adoption) → P17 (performance for scale) → P19 (polish) → P20 (release).

---

## API Design Rules

1. **Public API lives in `src/pytop/__init__.py`** — every symbol intended for users must be explicitly exported there.

2. **`_internal/` is off-limits for users** — modules in `_internal/` must NOT appear in `__init__.py` exports. Prefix with `_` signals internal use.

3. **New experimental code goes to `src/pytop/experimental/` first** — once stable and tested, promote to core `src/pytop/` and re-export from `experimental/` for backward compatibility.

4. **No ecosystem dependencies** — `pytop_questionbank`, `pytop_pedagogy`, `pytop_publish` must NOT be imported anywhere in `src/pytop/` (not even inside try/except blocks in new code).

5. **`__version__` must be in sync** — `pyproject.toml` version and `src/pytop/__init__.py` `__version__` must always match.

---

## `pytop.experimental` Philosophy

`pytop.experimental` is the research buffer zone:
- Modules here may have unstable APIs
- Users import via `from pytop.experimental import ...`
- When a module is promoted to stable, keep it in `experimental/` as a re-export with a deprecation note
- Do not promote a module without tests

---

## Cilt / Corridor Terminology

Test files and `_internal/` modules use terminology from the original textbook
development context. This glossary decodes the key terms:

| Term | Meaning |
|------|---------|
| **Cilt** | Turkish for "volume". Cilt I–IV map to volumes of the source textbook. |
| **Cilt I** | Point-set topology foundations (sets, spaces, maps, compactness, connectedness, separation) |
| **Cilt II** | Metric spaces, completeness, counterexample atlas, preservation tables |
| **Cilt III** | Local compactness, metrization, neighborhood systems, function spaces, compactness variants |
| **Cilt IV** | Cardinal functions, cardinal numbers, ordinals, quantitative topology |
| **Corridor** | A development milestone version (e.g., `v0.1.47`) that added a specific feature set |
| **Route** | A sequence of corridors forming a complete coverage of a topic |
| **Close-out** | The final corridor that completes a cilt's coverage |
| **Route summary** | An `_internal` function that documents which corridors cover a given topic |
| **v0.X.YZ** | Internal milestone versions — not the same as the public package version (v0.4.0+) |

These terms appear in `_internal/` module names and test files (e.g.,
`test_cilt2_undergraduate_route_v050.py`). They are internal metadata only.

---

## Version Bump Checklist

1. Update `version` in `pyproject.toml`
2. Update `__version__` in `src/pytop/__init__.py`
3. Add entry to `CHANGELOG.md`
4. Commit: `git commit -m "chore: bump version to vX.Y.Z"`
5. Tag: `git tag vX.Y.Z`
6. Push: `git push origin master --tags`
