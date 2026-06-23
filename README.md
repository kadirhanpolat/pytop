# pytop

[![CI](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml/badge.svg)](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-1.6.1.dev0-blue)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11--3.14-blue)

A mathematical topology library for Python, covering point-set topology, knot theory, graph topology, surface classification, 3-manifolds, higher categories, operads, spectral sequences, topological field theory, and more.

As of **v1.6.0** (released; development continues at `1.6.1.dev0`), pytop ships **20 phases** with 11,896 tests passing on a ruff-clean and mypy-clean `src/pytop`. **Phases 1–15**: computational core (Phases 1–7), advanced algebra (Phase 8), 19 computable-space representations (Phase 9), scale & algorithms (Phase 10), Lean 4 formal verification (Phase 11), Čech sheaf cohomology + persistent K-theory (Phase 12), homotopy theory (Phase 13), advanced knot homology (Phase 14), 4-manifold topology (Phase 15). **Phase 16** ✅ empirical validation & oracle ecosystem: benchmark suite, statistical validation, and **P16.2 oracle parity now wired** — pytop's persistent Betti numbers cross-checked against **GUDHI** (Betti-at-scale, matching on circle/sphere/multi-component fixtures). **Phase 17** 🔄 **performance & scale**: **P17.1 ✅** profiling infrastructure (86 tests); **P17.2 ✅** algorithm optimization (method selection: 'twist'/'standard'/'cohomology'); **P17.3 🚧** scaling — **inductive Vietoris–Rips construction shipped (~14–19× filtration-build speedup, byte-identical output)**; the Z/2 reduction is now the dominant cost for dense high-n. **Phase 18 ✅** documentation & pedagogy (16-chapter user guide, 225-module API ref, 36+ examples). **Phase 19** 🔄 **API stability**: **P19.1 ✅** error messages (WHY-HOW-THEN); **P19.2 ✅** deprecation policy (`@deprecated` decorator + `DEPRECATIONS.md`, 18-month window); **P19.3 ✅** API consistency audit (`docs/API_DESIGN.md`). **Phase 20** 🔄 **release maturity**: **P20.1 ✅** CI/CD hardening (Python 3.11–3.14 matrix); **P20.2 🚧** PyPI publishing; **P20.3 ✅** community onboarding (`CONTRIBUTING.md`, GitHub issue/PR templates).

## Installation

```bash
pip install -e .
```

Requires Python 3.11+.

## Quick Start

```python
import pytop

# Spaces and maps
from pytop import TopologicalSpace, continuous_map_profile

# Named spaces + catalog
from pytop import cantor_set, torus, n_sphere, catalog
s = cantor_set()
s.has_tag("totally_disconnected")   # True
catalog.get("Sorgenfrey line")       # SpaceRecord(...)
catalog.search(compact=True, metrizable=True)

# Compactness
from pytop import is_compact, CompactnessProfile

# Knot theory
from pytop import KnotProfile, reidemeister_move_profiles

# Surface classification
from pytop import SurfaceProfile, euler_characteristic_profile

# Degree theory
from pytop import get_retraction_degree_profiles, winding_number_profiles

# Experimental (unstable API)
from pytop.experimental import maturity_registry
```

### Computational core (new in v0.6.0)

```python
# Simplicial homology — Betti numbers and torsion, computed from a complex
from pytop import generated_subcomplex, betti_numbers, simplicial_homology
sphere = generated_subcomplex([{1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}])
betti_numbers(sphere)                       # (1, 0, 1)  -> S^2

# Persistent homology / TDA — Vietoris–Rips barcodes from a point cloud
import math
from pytop import persistent_homology
from pytop.metric_spaces import FiniteMetricSpace
pts = [(math.cos(2*math.pi*k/12), math.sin(2*math.pi*k/12)) for k in range(12)]

# Default: Twist algorithm (Chen–Kerber 2011) with Clearing Lemma (~1.1× speedup)
pairs = persistent_homology(FiniteMetricSpace(carrier=tuple(pts), distance=math.dist), max_dimension=2)

# Or choose algorithm explicitly: method='twist' (default), 'standard', or 'cohomology'
pairs_cohomology = persistent_homology(
    FiniteMetricSpace(carrier=tuple(pts), distance=math.dist),
    max_dimension=2,
    method='cohomology'  # Incremental cocycle algorithm (often faster on Rips)

# Knot invariants — Jones / Alexander polynomials from a diagram
from pytop import KnotDiagram, jones_polynomial
trefoil = KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))
jones_polynomial(trefoil)                   # -t^-4 + t^-3 + t^-1

# Surface classification from a polygon gluing word
from pytop import classify_surface_word
classify_surface_word("a b a^-1 b^-1").name   # "torus"

# Exact graph planarity / genus (rotation-system search)
from itertools import combinations
from pytop import is_planar
is_planar(list(combinations(range(5), 2)))  # False  -> K5 is non-planar

# Winding number / map degree
from pytop import winding_number
winding_number(pts)                          # 1

# pi-Base deductive inference (experimental, CC BY 4.0)
from pytop.experimental import deduce, find_counterexamples, property_uid
deduce({property_uid("Compact"): True, property_uid("Hausdorff"): True})  # ... Normal: True
find_counterexamples(has=["Compact"], lacks=["Hausdorff"])                # compact, non-Hausdorff spaces

# Research-grade computable-space protocol (experimental, Phase 1)
from pytop.experimental.spaces import (
    pi_base_space, ProductSpace, derive, SorgenfreyLineSpace, analyze_pi_base_space
)
cantor = pi_base_space("Cantor set")
derive(cantor, "compact").verdict.value           # True  (pi-Base certificate)
derive(ProductSpace([cantor, cantor]), "compact").verdict.value  # True  (Tychonoff)

sorgenfrey2 = ProductSpace([SorgenfreyLineSpace(), SorgenfreyLineSpace()])
derive(sorgenfrey2, "T3").verdict.value            # True  (regular is productive)
derive(sorgenfrey2, "lindelof").verdict.value      # None  (correctly undecided — the plane is not Lindelöf)

analyze_pi_base_space("Long line")                 # 16-property verdict dict
```

## Module Overview

| Domain | Key modules |
|--------|-------------|
| Foundations | `sets`, `relations`, `spaces`, `maps`, `predicates` |
| Metric spaces | `metric_spaces`, `metric_completeness`, `metrization_profiles` |
| Compactness | `compactness`, `compactness_variants`, `local_compactness` |
| Connectivity | `connectedness`, `paths`, `covering_spaces` |
| Separation axioms | `separation`, `countability` |
| Degree theory | `degree_theory`, `degree_theory_applications` |
| Knot theory | `knots`, `invariants` |
| Surfaces & manifolds | `surfaces`, `surface_classification`, `manifolds`, `three_manifolds` |
| Graph topology | `graph_topology` |
| **Computational homology** (v0.6.0+) | `homology`, `persistent_homology`, `homology_coefficients`, `mayer_vietoris`, `cellular_homology`, `cohomology` |
| **Optimized persistence** (v0.6.0+) | `persistent_homology_optimized` — Twist+Clearing (Chen–Kerber 2011), `ReductionStats` |
| **Persistent cohomology** (v0.9.7+) | `persistent_homology` — `persistence_pairs_cohomology` (de Silva dual; ~2–2.5× faster than standard) |
| **Cubical complexes** (v0.6.0+) | `cubical_homology` — `CubicalComplex`, SNF homology, `bitmap_to_cubical_filtration`, `persistent_homology_bitmap` |
| **Fundamental group / van Kampen** (v0.6.0+) | `van_kampen` — `GroupPresentation`, `van_kampen()`, `cw_complex_pi1()`, standard spaces |
| **Knot/link invariants** (v0.6.0+) | `knot_invariants` (Jones, Alexander, linking number/matrix), `seifert` (Seifert circles, genus bound, matrix, signature), `homfly` (HOMFLY-PT `P(a,z)` from braid closures), `multivariable_alexander` (`Δ_L(t₁,…,tₙ)` via Wirtinger + Fox) |
| **3-manifold homology** (v0.7.0+) | `dehn_surgery` — Dehn surgery → `H₁` (SNF cokernel of the framing/linking matrix), lens space homeomorphism/homotopy classification |
| **Khovanov homology** (v0.7.0+) | `khovanov` — bigraded `Kh^{i,j}` (free rank + torsion) categorifying the Jones polynomial |
| **Exact linear algebra** (v0.8.0+) | `exact_linalg` — Smith normal form, integer rank, Bareiss `integer_determinant`, `cokernel` → `AbelianGroup` |
| **TDA pipeline** (v1.0.3+) | `tda_pipeline` — `TDAPipeline` immutable builder; `.rips()/.cech()/.reduce()/.pairs()/.landscape()/.entropy()/.bottleneck()/.wasserstein()` |
| **Čech complex** (v1.0.1+) | `cech_complex` — `cech_filtration`, `persistent_homology_cech` (Welzl miniball) |
| **Persistence over Z/p** (v1.0.2+) | `persistent_homology_fp` — `persistence_pairs_fp(filtered, prime)` |
| **Standard triangulations** (v1.0.4+) | `simplicial_filtration` — `torus_filtration`, `klein_bottle_filtration`, `rp2_filtration` (7–8 vertex minimal triangulations) |
| **Simplicial maps** (v1.0.5+) | `simplicial_maps` — `SimplicialMap`, `chain_map_matrix`, `induced_map_on_homology`, `cone_complex`, `suspension_complex` |
| **Nerve complex** (v1.0.5+) | `nerve_complex` — `nerve_of_cover`, `good_cover_check`, `cech_nerve` (Welzl circumsphere) |
| **Spectral sequences** (v1.0.5+) | `spectral_sequences` — `SpectralPage`, `FilteredChainComplex`, `differential_d_r`, `converges_to` (E^∞ stability) |
| **Surgery theory** (v1.0.5+) | `surgery_theory` — `handle_attachment`, `trace_cobordism`, `trace_homology` |
| **Morse complex** (v1.0.5+) | `morse_complex` — `MorseChainComplex`, `morse_boundary_operator` (gradient V-path counting), `morse_homology` (cross-validated against simplicial H_*) |
| **Discrete Morse theory** (v0.9.8+) | `discrete_morse` — `MorsePair`, `MorseMatching`, `discrete_gradient_matching`, `check_morse_inequalities` |
| **Persistence distances** (v0.9.9+) | `persistence_distances` — `bottleneck_distance`, `wasserstein_distance`, `PersistenceLandscape`, `persistence_entropy` |
| **Mapper algorithm** (v1.0.0+) | `mapper` — Singh–Mémoli–Carlsson (2007): `IntervalCover`, `single_linkage_labels`, `MapperComplex` |
| **Degree / winding** (v0.6.0) | `winding_number` |
| **Surface classification** (v0.6.0) | `surface_word_classification` |
| **Graph planarity** (v0.6.0) | `graph_planarity` — O(V+E) left-right planarity test (Brandes 2009) |
| **Deductive inference** (v0.6.0) | `experimental.pi_base`, `experimental.pi_base_atlas` |
| **Convergence spaces** (v0.6.0) | `experimental.convergence_spaces` |
| **Computable spaces** (experimental) | `experimental.spaces` — protocol, 16 predicates, reasoning engine, pi-Base bridge, **19 representations** (Phase 9) |
| Cardinal functions | `cardinal_functions_framework`, `cardinal_numbers` |
| **Derived categories** (v1.0.9+) | `derived_categories` — `mapping_cone_complex`, `derived_functor_h` (Betti + torsion via SNF), `triangulated_structure_check` |
| **Topos / sheaf theory** (v1.0.9+) | `topos_theory` — `site_from_finite_topology`, `sheaf_on_site`, `sheafification_finite`, `topos_check` (Grothendieck topos) |
| **Operads** (v1.0.9+) | `operads` — `associahedron_complex` (Stasheff K_n, Catalan vertices), `operad_composition_check`, `bar_construction_sc` |
| **Higher categories** (v1.0.9+) | `higher_categories` — `nerve_of_category` N(C), `kan_fibration_check_sc`, `homotopy_type_finite_cat` (BC Betti numbers) |
| **Noncommutative K-theory** (v1.0.9+) | `noncommutative_topology` — `k0_group_matrix_algebra`, `spectral_dimension_finite` (log-log Weyl), `k1_group_matrix_algebra` |
| **Topological field theory** (v1.0.9+) | `topological_field_theory` — `cobordism_from_handles`, `tqft_dimension_2d`, `handle_signature_tft` (4-manifold handles) |
| **Sparse linear algebra** (v1.2.0+) | `sparse_linalg` — `sparse_smith_normal_form` (dict-based sparse SNF; auto-routed for large sparse matrices), `matrix_density` |
| **Parallel Khovanov** (v1.2.0+) | `khovanov` — `khovanov_homology(parallel=True)`; ThreadPoolExecutor over quantum gradings; GIL-limited on pure-Python, truly parallel with `[fast]` flint backend |
| **Witness complex** (v1.2.0+) | `witness_complex` — `landmark_sample` (maxmin/random), `witness_filtration` (strong-witness, de Silva & Carlsson 2004), `persistent_homology_witness` → `WitnessComplex` |
| **Streaming persistence** (v1.2.0+) | `streaming_persistence` — `StreamingPersistence`; incremental Z/2 column reduction; `add_simplex / current_pairs / current_betti / current_essential_pairs` |
| **GPU backend** (v1.2.0+, optional) | `_gpu_backend` — `gpu_twist_reduce`; cupy boolean-array column XOR; `[gpu]` extra in pyproject.toml; graceful CPU fallback |
| **Čech sheaf cohomology** (v1.4.0+) | `sheaf_cohomology` — `FiniteSheaf`, `constant_sheaf`, `skyscraper_sheaf`, `cech_cohomology` (Leray cover → alternating-sign coboundary → SNF), `sheaf_cohomology` (McCord minimal-neighborhood cover; H⁰ = ℤ^components) |
| **Persistent K-theory** (v1.4.0+) | `persistent_ktheory` — `KTheoryGroups` (rational AHSS: K⁰⊗ℚ = ⊕H_{2k}, K¹⊗ℚ = ⊕H_{2k+1}), `KBarcode` (Twist barcode partitioned by parity; χ_K = rank K⁰ − rank K¹), `k_theory_groups`, `k_barcode`, `k0/k1_simplicial`, `k_betti_numbers` |
| Higher algebra | `operads`, `spectral_sequences` |
| Higher categories | `higher_categories`, `topological_field_theory` |
| Cosmology | `cosmology_topology` |
| Named spaces | `named_spaces`, `space_catalog` |
| Experimental | `pytop.experimental` |

## Documentation

A comprehensive user guide (`docs/user_guide/`) covering point-set topology and metric spaces
in **four parallel formats**: Python scripts, Jupyter notebooks, Markdown, and LaTeX (PDF).

| # | Chapter | Topics |
|---|---------|--------|
| 1–3 | Prerequisites | Quick start, propositional logic, set theory & functions |
| 4–13 | Point-set topology | Spaces, predicates, separation, compactness, connectedness, countability, continuous maps, subspace/product, quotient, initial/final topology |
| 14–16 | Metric spaces | Metric spaces, completeness & compactness, metric maps |

```bash
# Run any chapter as a script
py -3.14 docs/user_guide/python/ch04_topological_spaces.py

# Open a notebook
jupyter lab docs/user_guide/notebook/ch07_compactness.ipynb

# Compile the PDF (requires xelatex)
cd docs/user_guide/latex && xelatex main.tex

# Rebuild TikZ figures → PNG
py -3.14 docs/user_guide/tools/build_figures.py
```

Chapters 4 and 6 feature guided proofs, "Ne oldu?" walkthroughs, trace tables, TikZ figures,
and color-coded pedagogical boxes (sezgi / dikkat / nedenonemli / karşı-örnek).
Exercise solutions are in `docs/user_guide/{markdown,python,notebook}/solutions.*` and
`docs/user_guide/latex/appendix/solutions.tex`.

## What's New in v1.6.0

**P16.2 — Oracle parity, now wired to GUDHI.** The persistent-Betti cross-check
that was previously framework-only is now a real, passing comparison. Added
`tests/validation/betti_parity.py`: pytop and GUDHI build the *same* Vietoris–Rips
filtration and agree on the **Betti number at every scale** (bars alive at `s`,
`birth ≤ s < death`) for dimensions the truncated skeleton can represent
faithfully (`H_k` needs simplices up to dim `k+1`). Verified on circle, dense
circle, two disjoint circles (`H₀=H₁=2`), an icosahedral 2-sphere (`H₂=1`), and a
random cloud. This corrected two latent bugs in the old comparison (death-count
instead of Betti-at-scale; spurious `H₂` from a triangle-only complex). Validation
suite 79 → 97 passing.

**P17.3 — Inductive Vietoris–Rips construction (~14–19× faster builds).** Profiling
showed the *filtration build* — not the reduction — dominated the truncated-scale
regime (85–92% of wall-clock at n=100–200). `vietoris_rips_filtration` now uses
**inductive clique expansion** (Zomorodian 2010) over the neighborhood graph
instead of exhaustive `C(n, k+1)` subset enumeration. Build time scales with the
materialized complex, not `C(n, k+1)`: **n=500 went from 22.7 s → 1.65 s**, output
**byte-identical** to before (verified vs. a brute-force reference and the full
test suite). No API change. The Z/2 reduction is now the dominant cost for dense,
high-n complexes (the next, inherently sequential, target).

**P19.2 / P19.3 / P20.3 — API maturity & onboarding.** Reusable `@deprecated`
decorator (`pytop._deprecation`) emitting consistent WHY-HOW-THEN
`DeprecationWarning`s, plus `DEPRECATIONS.md` (18-month / next-major policy +
registry). API naming/consistency audit in `docs/API_DESIGN.md`. Rewritten
`CONTRIBUTING.md` and GitHub issue/PR templates.

**Maintenance — clean baseline.** Repo-wide lint/type debt cleared: `src/pytop`
is ruff-clean **and** mypy-clean (244 files) and the whole `src/`+`tests/` tree
passes ruff (was 236 ruff + 12 mypy errors; a latent `_gpu_backend` crash fixed
along the way). Version handling reconciled (`pyproject` ↔ `__version__` in sync);
backfilled the missing `v1.4.0`/`v1.5.0` release tags and tagged `v1.6.0`.

**Phase 16 — Empirical Validation & Oracle Ecosystem (P16.1–P16.3 complete)**

Cross-validates pytop against independent gold-standard external systems via unified oracle framework.

- **P16.1: Benchmark Suite (37 tests)** — Minimal triangulations (T², Klein, ℝP²), 45-prime knot table (unknot–10_5), large grid graphs (3×3–40×40), performance baselines.

- **P16.2: Oracle Parity Framework ✅ AUTONOMOUS** — Unified adapter system for external systems:
  - **`oracle_integrations.py`** — Abstract `OracleAdapter` with 4 concrete implementations:
    * `GudhiOracleAdapter`: persistent homology Rips/Čech Betti computation
    * `RipserOracleAdapter`: fast R-based persistent homology  
    * `SnapPyOracleAdapter`: Dehn surgery H₁, knot invariants (Docker opt-in `PYTOP_SNAPPY_ORACLE=1`)
    * `SageOracleAdapter`: K-theory rational groups, polynomial computation (Docker opt-in `PYTOP_SAGE_ORACLE=1`)
  - **`oracle_agreement_builder.py`** — Orchestration engine:
    * `OracleAgreementBuilder`: runs cross-oracle tests (polynomials, Betti, K-theory)
    * `AgreementMatrixReport`: aggregates results, exports JSON + Markdown with agreement rates
  - **`run_p16_2_oracle_agreement.py`** — Autonomous CLI runner:
    * `--fast` mode: sample validation (~0.5s)
    * `--full` mode: comprehensive cross-checks (~2–5min with all oracles)
    * Auto-detects available oracles, gracefully skips unavailable systems
    * JSON/Markdown reports with detailed agreement/disagreement breakdown
  - Extended knot table: 40 → 45 primes (added 10-crossing knots 10_1–10_5)
  - **11 new tests**: oracle availability, adapter initialization, persistent Betti agreement (GUDHI/Ripser), polynomial reference validation
  - **Framework ready for**: PyPI publication, CI/CD integration, automated oracle matrix population

- **P16.3: Statistical Validation (10,000 tests)** — Random Erdős–Rényi 1-skeleta (5–50 vertices):
  - `test_10k_random_complexes_vs_oracles`: validates pytop H₀/H₁ on 10K random inputs (100% success, avg 6.26ms/complex)
  - Outlier analysis and JSON report generation
  - Framework ready for larger scales (50K+) and parallelization

**Phase 18 — Documentation & Pedagogy ✅ (P18.1–P18.3 complete)**

Complete user guide and API reference (16 chapters, 225 modules, 36+ examples).

## What's New in v1.2.0

**Phase 10 — Scale & Algorithm: 5 milestones, 65 new tests**

Extends practical input limits of existing engines and adds approximate / streaming TDA — without changing the pure-Python correctness core.

- **`sparse_linalg` (P10.1)** — Column-sparse Smith Normal Form via `_SparseMat` (dual row/col dicts).
  `sparse_smith_normal_form` accepts `list[list[int]]` or any `scipy.sparse` matrix.
  `homology._smith_normal_form` now **auto-routes** matrices with `min(m,n) ≥ 30` and density < 30 %
  through the sparse path — Khovanov and Rips boundary matrices hit this automatically.
  `matrix_density` helper exposes the sparsity fraction.

- **`khovanov_homology(parallel=True)` (P10.2)** — All per-quantum-grading SNF calls are submitted
  to a `ThreadPoolExecutor` and run in parallel.  With the pure-Python SNF backend the GIL limits
  true concurrency; with the optional `[fast]` flint backend (C code, GIL-free) the speedup is
  real.  Results are identical to the sequential path.

- **`witness_complex` (P10.3)** — Approximate persistence for large point clouds.
  `landmark_sample(points, k, method='maxmin')` — greedy farthest-point (maxmin) or uniform random.
  `witness_filtration(points, landmarks, max_dim)` — strong-witness filtration (de Silva & Carlsson
  2004): simplex σ enters at `ε(σ) = min_w max_{l∈σ} d(w,l)`.
  `persistent_homology_witness(points, k, max_dim)` — full pipeline returning a `WitnessComplex`
  (filtration + landmark indices + Twist-reduced pairs).

- **`streaming_persistence` (P10.4)** — Online Z/2 column reduction via `StreamingPersistence`.
  Simplices inserted one at a time with `add_simplex(simplex, birth)` (filtration order required).
  Bitmask-column representation (same as Twist+Clearing); `current_pairs()`, `current_betti()`,
  `current_essential_pairs()`.  Results match `persistence_pairs_twist` on the same filtration.

- **`_gpu_backend` (P10.5)** — Optional cupy-accelerated Twist+Clearing via `gpu_twist_reduce`.
  Columns stored as cupy boolean arrays; XOR is GPU-native.  Falls back silently to `_twist_reduce`
  when cupy is absent or the filtration is below `GPU_MIN_SIZE = 500`.
  Install with `pip install 'pytop[gpu]'`.

```python
from pytop import sparse_smith_normal_form, matrix_density
from pytop import landmark_sample, witness_filtration, persistent_homology_witness
from pytop import StreamingPersistence
from pytop import GPU_AVAILABLE, gpu_twist_reduce

# Sparse SNF — same result as exact_linalg.smith_normal_form, faster on sparse inputs
boundary = [[1,-1,0,1],[0,1,-1,0],[-1,0,1,-1]]
print(matrix_density(boundary))          # 0.75 — dense, stays on dense path
print(sparse_smith_normal_form(boundary))  # [1, 1, 1]

# Witness complex — approximate H1 of a circle
import math, random
pts = [(math.cos(2*math.pi*i/50), math.sin(2*math.pi*i/50)) for i in range(50)]
wc = persistent_homology_witness(pts, k=12, max_dim=1, seed=0)
h1 = [p for p in wc.pairs if p.dimension == 1]
print(len(h1), "H1 bars")     # ≥ 1 (the circle loop)

# Streaming persistence — insert simplices one at a time
sp = StreamingPersistence()
for v in range(3): sp.add_simplex((v,), 0.0)
sp.add_simplex((0,1), 1.0); sp.add_simplex((0,2), 1.5); sp.add_simplex((1,2), 2.0)
print(sp.current_betti())      # {0: 1}  — one component
sp.add_simplex((0,1,2), 3.0)  # fill triangle
print(sp.current_pairs())      # includes the H1 bar [2.0, 3.0)

# Parallel Khovanov
from pytop import khovanov_homology, KnotDiagram
trefoil = KnotDiagram([(1,4,2,5),(3,6,4,1),(5,2,6,3)], signs=(1,1,1))
kh = khovanov_homology(trefoil, parallel=True)   # same groups, faster on large diagrams
```

**65 new tests; 11 467 total.**

---

## What's New in v1.5.0

**Phases 13–15 — Homotopy theory, advanced knot homology, and 4-manifold topology (15 new modules)**

Three full phases, each five modules, all pure-Python and dependency-free, ruff-clean and mypy-clean.

- **Phase 13 — Homotopy Theory:** `chain_homotopy` (∂h+h∂=f−g verification + ℚ-solver),
  `eilenberg_maclane` (H_*(K(G,n)) for cyclic/free/free-abelian/ℤ groups, asphericity),
  `massey_products` (triple products + formality), `hopf_invariant` (Hopf fibrations,
  Adams' theorem, π₃(S²)), `sullivan_models` (minimal models over ℚ; χ via the Hilbert
  series of ΛV → χ(T²)=0, χ(S^{2k})=2, χ(CP^n)=n+1).
- **Phase 14 — Advanced Knot Homology:** `khovanov_odd` (odd Khovanov homology),
  `grid_floer` (grid-diagram HFK̂ over 𝔽₂), `concordance` (τ, s, σ, Tristram–Levine,
  algebraic sliceness), `satellite_knots` (Morton's formula, exact torus-knot Alexander
  polynomial division, cables, Whitehead doubles), `virtual_knots` (Gauss codes, parity,
  odd writhe, arrow polynomial).
- **Phase 15 — 4-Manifold Topology:** `intersection_forms` (Sylvester congruence signature,
  E₈/hyperbolic, Donaldson), `kirby_calculus` (handle moves → intersection form),
  `casson_invariant` (Neumann–Wahl λ(Σ(a,b,c))=σ(Milnor fibre)/8), `milnor_fibers`
  (Brieskorn–Pham μ, signature, ADE), `rohlin_theorem` (spin + smooth ⇒ σ≡0 mod 16,
  Kirby–Siebenmann, Freedman realisation).

**140 new tests; 11 685 tests pass total.**

**Phase 12 — Research Frontier: Čech sheaf cohomology + persistent K-theory (P12.1–P12.2)**

Two new research-grade engines that push pytop into algebraic K-theory and sheaf theory territory.

- **`sheaf_cohomology` (P12.1)** — Čech cohomology of a sheaf on a finite topological space.
  `FiniteSheaf` (frozen dataclass: `open_sets`, integer-rank `sections`, integer-matrix `restrictions`);
  `constant_sheaf` and `skyscraper_sheaf` factory functions;
  `cech_cohomology(cover, sheaf, max_degree)` — full Čech cochain complex with alternating-sign
  coboundary δ^p, SNF → `AbelianGroup` per degree;
  `sheaf_cohomology(open_sets, universe, sheaf)` — uses the minimal-open-neighborhood Leray cover
  (McCord 1966) so H⁰ counts connected components correctly (e.g. H⁰=ℤ for Sierpiński,
  H⁰=ℤ² for discrete 2-point space).

- **`persistent_ktheory` (P12.2)** — Rational K-theory groups and persistent K-theory barcode.
  `KTheoryGroups` — AHSS collapse: K⁰⊗ℚ = ⊕H_{2k}, K¹⊗ℚ = ⊕H_{2k+1}; verified on
  point (1,0), S¹ (1,1), S² (2,0), torus T² (2,2).
  `KBarcode` — Twist-reduced persistence pairs partitioned by dimension parity;
  `k0_betti_at(ε)`, `k1_betti_at(ε)`, `euler_characteristic_at(ε)` (χ_K = rank K⁰ − rank K¹ = χ).

```python
from pytop import (
    FiniteSheaf, constant_sheaf, skyscraper_sheaf, cech_cohomology, sheaf_cohomology,
    KTheoryGroups, KBarcode, k_theory_groups, k_barcode, k_betti_numbers,
)
from pytop.homology import SimplicialComplex

# Sheaf cohomology: discrete 2-point space with constant sheaf ℤ
opens = [frozenset({0}), frozenset({1}), frozenset({0, 1})]
sheaf = constant_sheaf(opens)
result = sheaf_cohomology(opens, frozenset({0, 1}), sheaf)
print(result["cohomology"][0])  # AbelianGroup(free_rank=2, torsion=()) — two components

# Persistent K-theory of a circle
s1 = SimplicialComplex([(0,),(1,),(2,),(0,1),(1,2),(0,2)])
g = k_theory_groups(s1)
print(g.k0_rank, g.k1_rank)    # 1  1  — K⁰(S¹)=ℤ, K¹(S¹)=ℤ

from pytop.persistent_homology import vietoris_rips_filtration
import math
pts = [(math.cos(2*math.pi*i/8), math.sin(2*math.pi*i/8)) for i in range(8)]

class Cloud:
    carrier = pts
    def distance_between(self, a, b): return math.dist(a, b)

filt = vietoris_rips_filtration(Cloud(), max_dimension=2)
kb = k_barcode(filt)
print(kb.euler_characteristic_at(0.0))   # 8  (8 isolated points)
```

**78 new tests; 11 545 total.**

---

## What's New in v1.3.0

**Phase 11 — Lean 4 Formal Verification Expansion: 5 new proof files, 0 sorry**

Extends the `formal/` corpus from 6 to **11 Lean files**. The zero-sorry rule holds throughout.

- **`MayerVietoris.lean` (P11.1)** — Short exact sequences + snake lemma.
  `SES` structure (injective `i`, exact at `B`, surjective `p`); `ses_p_zero_of_im`
  (exactness → `p ∘ i = 0`); `delta_well_defined`; `snake_delta_exists`;
  `snake_delta_independent` (connecting class well-defined in A').

- **`VanKampen.lean` (P11.2)** — Group presentations + amalgamated free product.
  `Pres` structure; `TietzeEquiv` inductive relation with `tietze_elim` / `tietze_add_gen`;
  `AmalgamDatum` + `Pushout`; `pushout_universal`; `int_hom_determined_by_one`
  (ℤ is the free abelian group on one generator — uniqueness); `int_hom_exists` (existence).

- **`CohomologyRing.lean` (P11.3)** — Cup product over Bool (ℤ/2).
  Alexander–Whitney `cup` (`⌣`) operator; `cup_value_assoc` (`Bool.and_assoc`);
  `cup_comm_Z2`; `coboundary0`; `leibniz_0cochains` (Leibniz rule δ(f⌣g) = δf⌣g ⊕ f⌣δg,
  verified by 4-way Bool case analysis).

- **`PersistencePairing.lean` (P11.4)** — Persistence pairing perfection.
  `pairing_is_perfect` (= `reduce_is_reduced`); `pairs_have_distinct_births` (birth indices
  are `Nodup`). Key lemma chain: `isReduced_tail` → `filterMap_getLast_nodup_of_isReduced`
  (induction + `List.mem_iff_getElem` for positional index) → `zipWith_range_filterMap_snd_eq`
  → `map_fst_pairs_eq`.

- **`SpectralSequences.lean` (P11.5)** — Abstract spectral sequences.
  `ChainCx α` structure with differential `d : α →+ α` and `sq : ∀ x, d (d x) = 0`;
  `d_sq_zero`; `image_sub_kernel`; `SpectralSeq`; `StabilizesAt`; `Convergent`;
  `const_convergent`; `stabilizes_mono`; `same_diff_implies_same_stab`;
  `const_pages_convergent`.

**0 sorry across all 11 Lean files.**

---

## What's New in v1.1.0

**Phase 9 — `experimental.spaces` expansion: 6 new canonical representations (13 → 19)**

Six new infinite-space representations, all importable from `pytop.experimental.spaces`:

- **`OnePointCompactificationSpace` / `one_point_compactification(space)` (P9.1)** —
  Alexandroff one-point compactification αX = X ∪ {∞}.  For finite X the full topology is
  enumerated: opens(αX) = opens_X ∪ {U ∪ {∞} : U ∈ opens_X}.  Compact always; T2 iff base
  is locally compact Hausdorff; {∞} isolated when X is compact.

- **`StoneCechSpace` / `stone_cech_n()` (P9.2)** — Stone–Čech compactification βℕ.
  Compact T4, separable (ℕ embeds as a countable dense subspace), NOT first-countable (free
  ultrafilter points have no countable local base), NOT T6.
  Cardinals: weight = 𝔠, density = ℵ₀, character = 𝔠.

- **`HilbertCubeSpace` / `hilbert_cube()` (P9.3)** — Hilbert cube [0,1]^ω.
  Compact, connected, T6 (metrizable), second-countable, separable.  Points are finite
  rational tuples; separation via cylinder neighbourhoods.
  By Urysohn: every compact metrizable space embeds into [0,1]^ω.

- **`SolenoidSpace` / `dyadic_solenoid()` (P9.4)** — dyadic solenoid
  Σ = lim←{S¹ ←² S¹ ←² S¹ ←² …}.  Compact, connected, metrizable T6.
  NOT locally connected (local cross-sections are Cantor sets).
  `contains()` checks compatibility: 2·θₖ ≡ θₖ₋₁ (mod 1).

- **`UniformSpace` + `UniformProduct` + `UniformSubspace` (P9.5)** — uniform structure
  backed by a metric.  Methods: `entourage(ε)` (returns the ε-entourage as a callable
  relation), `is_cauchy(seq, ε)` (finite-sample Cauchy test), `uniform_neighbourhood(x, ε)`.
  `UniformProduct` uses sup-metric; `UniformSubspace` uses trace uniformity.
  Factories: `rational_uniform_space()`, `metric_uniform_space(name, d, member)`.

- **`ProfiniteSpace` / `p_adic_integers(p)` (P9.6)** — inverse limit of finite discrete
  groups.  `p_adic_integers(p)` builds ℤ_p = lim← ℤ/p ← ℤ/p² ← ℤ/p³ ← … via reduction
  mod pⁿ.  Compact, T6, totally disconnected, metrizable, second-countable.

```python
from pytop.experimental.spaces import (
    hilbert_cube, dyadic_solenoid, stone_cech_n, p_adic_integers,
    one_point_compactification, rational_uniform_space, UniformProduct,
    is_compact, is_connected, is_t6, is_first_countable, discrete_finite_space,
)
from fractions import Fraction

# Hilbert cube — compact T6, universal compact metrizable space
hc = hilbert_cube()
is_t6(hc).value        # True
is_compact(hc).value   # True

# Dyadic solenoid — compact, connected, NOT locally connected
sol = dyadic_solenoid()
sol.contains((Fraction(1,3), Fraction(2,3)))   # True (2·2/3 mod 1 = 1/3)
sol.certificate("locally_connected").value      # False

# Stone–Čech βℕ — separable but not first-countable
is_first_countable(stone_cech_n()).value   # False

# p-adic integers ℤ₅ — compatible sequences mod 5^k
z5 = p_adic_integers(5)
z5.contains((3, 8, 33))   # True  (8 mod 5 = 3, 33 mod 25 = 8)

# One-point compactification — finite → full topology enumerated
alpha = one_point_compactification(discrete_finite_space({0, 1}))
len(list(alpha.open_sets()))   # 8

# Uniform product with sup-metric
u = rational_uniform_space()
up = UniformProduct(u, u)
v = up.point_separation((Fraction(0), Fraction(0)), (Fraction(3,4), Fraction(1,4)))
v.witness["radius"]   # Fraction(3, 8)
```

**166 new tests; 11 402 total.**

---

## What's New in v1.0.9

**Phase 8 — Profile→Computational upgrade: 6 advanced algebra modules, 16 new functions**

Previously tag-based classifier modules promoted to genuine computational engines:

- **`derived_categories` (P8.1)** — `mapping_cone_complex` (block boundary matrix for C(f)_n = A_{n-1}⊕B_n);
  `derived_functor_h` (H_n from boundary matrices via Betti + torsion through SNF);
  `triangulated_structure_check` (g∘f=0 + cone Betti comparison).
- **`topos_theory` (P8.2)** — `site_from_finite_topology` (Grothendieck site from open-set lattice);
  `sheaf_on_site` (locality + gluing axioms); `sheafification_finite` (one-step F⁺ correction);
  `topos_check` (terminal object + fiber products + Ω → Grothendieck topos verdict).
- **`operads` (P8.3)** — `associahedron_complex(n)` (Stasheff K_n as SimplicialComplex; vertices = full
  binary trees with n leaves, edges = rotation pairs; K₃=interval, K₄=pentagon);
  `operad_composition_check` (µ(µ(a,b),c) = µ(a,µ(b,c)) for all basis triples);
  `bar_construction_sc` (bar complex skeletal model).
- **`higher_categories` (P8.4)** — `nerve_of_category` (N(C) up to dim 2; 2-simplex when composite
  a→c present for chain a→b→c); `kan_fibration_check_sc` (horn-filling condition);
  `homotopy_type_finite_cat` (BC = |N(C)| Betti numbers, is_contractible, is_connected).
- **`noncommutative_topology` (P8.5)** — `k0_group_matrix_algebra(n)` (K₀(Mₙ(ℚ)) ≅ ℤ, identity class = n,
  Morita invariance); `spectral_dimension_finite` (log-log regression on eigenvalue counting → d_s);
  `k1_group_matrix_algebra(n)` (K₁(Mₙ(ℚ)) ≅ ℚ*; torsion = ℤ/2).
- **`topological_field_theory` (P8.6)** — `cobordism_from_handles(n₀,n₁,n₂)` (χ, genus, connectivity);
  `tqft_dimension_2d(genus)` (Boolean TFT dim=1; A₂ TFT: 2/1/0 for g=0/1/≥2);
  `handle_signature_tft(n₀,…,n₄)` (4-manifold handles → Euler char, Betti, π₁ flag).

**171 new tests; 11 236 total.**

---

## What's New in v1.0.8

**Profile→Computational upgrade: 4 modules, 13 new functions**

Previously tag-based classifier modules promoted to genuine computational engines:

- **`shape_theory`** — `link_complex(simplices, vertex)` (lk(K,v) face-closed);
  `is_manifold_triangulation(simplices, n)` (every vertex link ≃ Sⁿ⁻¹ by homology);
  `has_trivial_shape_sc(simplices)` (contractibility via H_*);
  `shape_anr_check_sc(simplices)` (compact polyhedron ANR/FANR/movability + shape class).
- **`coarse_geometry`** — `growth_function_graph(adj, source, r)` (BFS ball sizes b(r));
  `geodesic_distance_graph(adj, u, v)` (shortest-path length or −1);
  `is_tree_graph(adj)` (connected + |E|=|V|−1, 0-Gromov-hyperbolic);
  `classify_graph_coarse_growth` (polynomial/exponential via log-log slope, degree estimate).
- **`locale_theory`** — `frame_from_finite_topology` (closure under ∩ and ∪, sorted frame);
  `pseudocomplement_in_frame` (b* = ∨{c : c∧b=∅});
  `well_inside_relation` (b << a iff b* ∨ a = top);
  `is_regular_frame` (every a = ∨{b : b << a});
  `is_spatial_finite_frame` (∅ and top present, opens separate points).
- **`dimension_theory`** — `covering_dimension_simplicial` (max simplex dim);
  `ind_finite_space` (longest strict chain in specialization poset; indiscrete spaces = 0).

**120 new tests; 11 065 total (pre-v1.0.9).**

---

## What's New in v1.0.7

**`experimental.spaces` extended representations (10 → 13):**

Three new canonical infinite-space representations expand the computable-space protocol:

- **`ProductMetricSpace`** — product of two metric spaces with the sup metric
  `d((x₁,y₁),(x₂,y₂)) = max(d_X(x₁,x₂), d_Y(y₁,y₂))`. Inherits all metric-space separation
  properties (T0–T6, first-countable, Tychonoff). Factory: `rational_plane()` builds ℚ².
- **`LexicographicSquareSpace`** — [0,1]² with the lexicographic order topology (the canonical
  example of a compact T5 space that is NOT metrizable). Certificates: compact, connected, T5,
  Lindelöf, first-countable; NOT second-countable, NOT separable (cellularity = 𝔠).
  `point_separation` splits at a rational midpoint in the first coordinate, or within the fiber
  for equal first coordinates. Factory: `lexicographic_square()`.
- **`CantorSpaceRepresentation`** — {0,1}^ω with the product topology. Points as finite binary
  tuples; `point_separation` returns the clopen cylinder at the first differing bit
  (undecidable when one tuple is a prefix of the other — honest!). Certificates: compact, T6,
  totally disconnected, second-countable, separable; weight = density = character = cellularity = ℵ₀.
  Brouwer's theorem: every compact metrizable zero-dimensional perfect space is homeomorphic to
  the Cantor space. Factory: `cantor_space()`.

```python
from pytop.experimental.spaces import (
    rational_plane, lexicographic_square, cantor_space,
    is_hausdorff, is_compact, is_connected, is_second_countable, is_separable,
    is_t5, is_t6,
)
from pytop.experimental.spaces.cardinal_invariants import cellularity, character
from pytop.experimental.spaces.core import CardinalValue

# ℚ² — product metric space
q2 = rational_plane()
is_hausdorff(q2).value                          # True  (metric space)
is_t6(q2).value                                 # True  (metrizable → perfectly normal)
q2.point_separation((0, 0), (1, 0)).witness[0][1]  # Fraction(1, 2)  (sup-ball radius)

# Lex square — compact T5 but NOT second-countable
lex = lexicographic_square()
is_compact(lex).value                           # True
is_connected(lex).value                         # True
is_t5(lex).value                                # True
is_second_countable(lex).value                  # False  (uncountable cellularity)
is_separable(lex).value                         # False
cellularity(lex)                                # CardinalValue(symbol='𝔠')
character(lex)                                  # CardinalValue(symbol='ℵ₀')

# Cantor space — compact, totally disconnected, perfect
cs = cantor_space()
is_compact(cs).value                            # True
is_connected(cs).value                          # False  (totally disconnected)
is_t6(cs).value                                 # True
is_second_countable(cs).value                   # True
character(cs)                                   # CardinalValue(symbol='ℵ₀')

# Separation: clopen cylinder at first differing bit
cs.point_separation((0, 1, 0), (0, 1, 1)).witness  # {'bit_position': 2, 'value': 0}

# Prefix → honest undecidable
from pytop.experimental.spaces.core import Decidability
cs.point_separation((0, 1), (0, 1, 0)).decidability  # Decidability.UNDECIDABLE
```

**10 945 tests passing when released** (+ 16 opt-in SageMath/SnapPy-oracle tests).

---

## What's New in v1.0.6

**Profile→Computational engine upgrades (6 modules) + critical `_snf_ext` bug fix:**

- **Covering spaces** (`covering_spaces.py`): `CoveringGraph`, `cyclic_voltage_cover` (voltage
  construction for cyclic covers), `fundamental_group_rank_graph` (first Betti number β₁ via Euler
  characteristic), `is_graph_covering_map` (sheet-count + uniform-degree check),
  `universal_covering_tree` (BFS spanning tree). 32 tests.
- **Fundamental group** (`fundamental_group.py`): `pi1_graph(edges)` — fundamental group of a
  1-complex via van Kampen + spanning-tree; k-cycle graph → free group Fₖ. 14 tests.
- **Three-manifolds** (`three_manifolds.py`): `mapping_torus_h1(monodromy)` — H₁ of the mapping
  torus via Wang sequence cokernel (SNF); `lens_space_pi1(p, q)` → ℤ/p. 21 tests.
- **Homotopy** (`homotopy.py`): `is_contractible_simplicial(simplices)` — contractibility via
  H_*(X;ℤ) ≅ H_*(pt;ℤ); `has_sphere_homology(simplices, n)` — sphere homology type test
  (H_*(X;ℤ) ≅ H_*(Sⁿ;ℤ)). Auto face-closure before boundary matrix. 26 tests.
- **Degree theory** (`degree_theory.py`): `map_degree_simplicial(sim_map, n)` — topological degree
  of f: Sⁿ → Sⁿ from the 1×1 matrix of `induced_map_on_homology` on H_n. 8 tests.
- **Manifolds** (`manifolds.py`): `euler_characteristic_simplicial(simplices)` — χ = Σ(−1)^k f_k
  computed combinatorially; correct for torus (χ=0), RP² (χ=1), disjoint unions (additive). 18 tests.
- **Critical bug fix** (`mayer_vietoris.py`): `_snf_ext` no longer hangs on matrices with negative
  entries. The `q -= 1` corrections assumed C-style truncation division; Python's `//` is floor
  division and already gives the correct quotient — the adjustment over-corrected, making the
  remainder exceed the pivot and triggering infinite swap cycles. Removed. All 150-iteration
  property tests now pass in < 0.5 s.

**10 864 tests passing when released** (+ 16 opt-in SageMath/SnapPy-oracle tests).

---

## What's New in v1.0.5 (Phase 7 complete)

**Phase 7 — Combinatorial topology & geometric structures (P7.2–P7.6):**

- **Simplicial maps** (`simplicial_maps.py`, P7.2): `SimplicialMap` dataclass with vertex-map
  validation, `chain_map_matrix` (integer matrix f#_k: C_k(K) → C_k(L) with correct signs),
  `induced_map_on_homology` (f_*: H_k(K;Z) → H_k(L;Z) via extended SNF), `cone_complex`
  (contractible CK = K * {apex}), `suspension_complex` (ΣK = K * S⁰; Σ(Sⁿ) ≃ Sⁿ⁺¹). 42 tests.
- **Nerve complex** (`nerve_complex.py`, P7.3): `nerve_of_cover` (nerve N(U) of a finite open
  cover), `good_cover_check` (verifies Nerve theorem preconditions — covers space, pairwise
  intersections, nonempty sets), `cech_nerve` (Čech complex at fixed radius via Welzl miniball
  least-squares circumsphere). 30 tests.
- **Spectral sequences (computational)** (`spectral_sequences.py`, P7.4): `SpectralPage`
  (bigraded Betti/torsion groups at page r), `FilteredChainComplex`, `filtered_chain_complex_from_simplices`,
  `differential_d_r` (E^r page differentials d^r: E^r_{p,q} → E^r_{p−r,q+r−1}),
  `converges_to` (iterates pages until E^{r+1} = E^r stability → E^∞). 25 new tests.
- **Surgery theory** (`surgery_theory.py`, P7.5): `handle_attachment` (K ∪ cone(Sᵏ⁻¹),
  homotopy-type of K with a k-cell attached), `trace_cobordism`, `trace_homology`
  (H_*(W;Z) via direct simplicial homology with Mayer–Vietoris interpretation). 24 tests.
- **Morse complex** (`morse_complex.py`, P7.6): `MorseChainComplex` (critical simplices +
  Morse boundary matrices from a discrete gradient matching), `morse_boundary_operator`
  (gradient V-path counting with Forman signs — DFS on the acyclic gradient graph),
  `morse_homology` (H_*(C^M;Z) via Smith normal form + automatic cross-validation against
  simplicial H_*(K;Z): **Morse homology theorem verified**). 32 tests.

**9 959 core tests passing when released (+ opt-in SageMath/SnapPy-oracle tests). All phases 1–7 complete.**

---

## What's New (post-v0.6.0, now on master — PR #15)

- **Phase 1/2 incremental improvements** (latest):
  - **Alexandroff factory functions**: `finite_circle()` (4-pt diamond, π₁=ℤ), `finite_sphere(n)`
    (2(n+1)-pt McCord model via iterated suspension, π₁=trivial for n≥2), `finite_wedge_circles(k)`
    (1+3k-pt model of S¹∨⋯∨S¹, π₁=F_k).
  - **AlexandroffSpace structural certificates**: `certificate("T0")` checks antisymmetry of the
    order relation (no open-set enumeration needed); `certificate("connected")` uses union-find on
    the strict-order graph. `cardinal_certificate("character")` = 1 (principal upset is the unique
    minimal neighbourhood); `cardinal_certificate("weight")` = |X| for T0 Alexandroff spaces.
  - **Urysohn witnesses for all infinite Tychonoff representations**:
    `SorgenfreyLineSpace` → Euclidean distance-ratio formula (valid because τ_std ⊊ τ_Sorgenfrey);
    `OrderTopologySpace` → order-metric formula (order topology on ℚ = metric topology).
  - **Stronger Tietze simplification**: `_cyclically_reduce` removes outer inverse-pair letters from
    relators; `_dedup_relators` eliminates duplicate relators up to cyclic conjugation + inversion.
    Applied after every Tietze II elimination.
  - **`predicates._decide` certificate-first**: structural certificates checked before finite-topology
    enumeration — allows subclasses to short-circuit without enumerating all open sets.
  - **`persistence_betti_numbers(pairs)`**: counts essential (death=∞) persistence pairs per dimension.
- **Research-grade computable-space protocol** (`experimental.spaces`) — Phase 1 complete (S1–S5):
  unified `Space` ABC with 16 witness-producing, decidability-honest predicates (T0–T6/Tychonoff,
  regular/normal, compact/connected, Lindelöf/separable, first/second-countable), **10 representations**
  (Finite, Cofinite, Order-ℚ, Metric, Sorgenfrey, Discrete-ℕ, Opaque, Alexandroff, Subbase,
  InverseLimit), finite+infinite construction closure (`ProductSpace`, `SubspaceSpace`, `SumSpace`,
  `QuotientSpace`), cardinal invariants (weight/density/character/cellularity), Urysohn witnesses,
  π₁ via McCord order complex, and a property-reasoning engine that derives and *explains* properties
  of constructed infinite spaces via preservation theorems + the pi-Base implication graph — no
  enumeration. `synthesize(has=…, lacks=…)` finds example spaces. Preservation table
  cross-validated against pi-Base meta-properties.
- **pi-Base atlas bridge** — `pi_base_space("Cantor set")` wraps any of 222 famous spaces as a
  protocol `Space`; feeds directly into the reasoning engine and construction wrappers.
- **Field-coefficient & relative homology** — `betti_numbers_over(K, "Q")` / `betti_numbers_over(K, p)`
  and `relative_homology(K, L)` / `relative_betti_numbers(K, L)`. Demonstrates coefficient
  dependence: RP² → H₁(;Q)=0 but H₁(;Z/2)=Z/2 (2-torsion visible over Z/2 only).
- **Mayer–Vietoris long exact sequence** — `mayer_vietoris(A, B)` computes the full LES for K = A ∪ B:
  extended Smith Normal Form yields explicit homology bases and cycle representatives;
  inclusion maps and the snake-lemma connecting homomorphism δ are returned as integer matrices;
  exactness verified at every position (S¹, S², interval). 30 new tests.
- **Cellular homology** — `cellular_homology(cw, k)` computes H_k(X; Z) from a CW complex specified
  by cell counts and integer boundary matrices. Convenience constructors cover the standard spaces:
  `cw_sphere(n)`, `cw_real_projective_space(n)`, `cw_complex_projective_space(n)`, `cw_torus()`,
  `cw_klein_bottle()`, `cw_lens_space(p)`, `cw_moore_space(n, k)`. `cw_from_simplicial(K)` bridges
  CW and simplicial homology for cross-validation. Chain-complex condition d∘d=0 verified on
  construction. 65 new tests.
- **Cohomology + cup product** — `simplicial_cohomology(K, k)` computes H^k(K; Z) via the cochain
  complex δ^k = (∂_{k+1})^T and extended Smith Normal Form. UCT (H^k torsion = H_{k-1} torsion)
  verified against homology. `simplicial_cohomology_ring(K)` returns a `CohomologyRing` with the
  Alexander-Whitney cup product on cohomology generators — torus H^1 ⊗ H^1 → H^2 pairing is
  non-degenerate and graded-commutative; RP² H^2 = Z/2 from UCT. 53 new tests.
- **Seifert–van Kampen theorem** — `van_kampen(π₁A, π₁B, π₁(A∩B), φ_A, φ_B)` computes π₁(A∪B) as
  the amalgamated free product via `GroupPresentation` + `GroupHomomorphism`. Tietze elimination
  reduces the raw presentation; abelianization (H₁ = π₁^ab) is computed via Smith Normal Form.
  `cw_complex_pi1(cw)` derives π₁ directly from a `CW1Complex` using a BFS spanning tree.
  Convenience constructors cover the standard spaces: `van_kampen_sphere()` → trivial,
  `van_kampen_torus()` → ⟨a,b | aba⁻¹b⁻¹⟩ ≅ ℤ², `van_kampen_klein_bottle()` → ⟨a,b | abab⁻¹⟩
  (H₁ = ℤ⊕ℤ/2), `van_kampen_real_projective_plane()` → ⟨a | a²⟩ ≅ ℤ/2,
  `van_kampen_wedge_circles(n)` → Fₙ. Group type identified automatically. 59 new tests.
- **Optimized persistence (Twist+Clearing)** — `persistent_homology_optimized` implements the
  Chen–Kerber 2011 Twist algorithm: columns processed dimension-top-down; the Clearing Lemma
  immediately skips every creator whose reduction is guaranteed to be zero. Returns identical
  results to the standard L→R sweep, typically with significantly fewer column additions.
  `persistence_pairs_twist_with_stats` exposes `ReductionStats` (n_cleared, clearing_ratio,
  n_column_additions). Shared `_twist_reduce` kernel reused by the cubical pipeline. 46 new tests.
- **Cubical complexes** — `cubical_homology` provides a complete cubical TDA stack:
  `CubicalComplex` (face-closure under ∂, ℤ boundary matrices, SNF-based homology — S¹: H₁=ℤ,
  D²: contractible, verified); `circle_cubical`, `disk_cubical`, `interval_complex` standard
  spaces; `CubicalFiltration` + `bitmap_to_cubical_filtration` (lower-star filtration from a
  2-D pixel array with f(face) ≤ f(coface) guaranteed); `persistence_pairs_cubical` +
  `persistent_homology_bitmap` via the shared Twist+Clearing kernel — 3×3 annular image
  correctly yields H₁ bar [0, 1). 74 new tests.
- **Phase 1/2 correctness fixes** (current):
  - **5 HIGH fixes**: `is_hausdorff` certificate bypass; `_close_under_unions` deduplication
    (constructions.py → imports from representations.py); `_provable_true_props` recursion guard
    (depth limit 100); `_product_pi1` bare `except Exception` removed; Mayer–Vietoris
    `_check_exact_at_middle` torsion-aware composition (`val % d == 0` for torsion generators).
  - **15 MEDIUM fixes**: `OrderTopologySpace` midpoint formula (`(lo+hi)/2`); `AlexandroffSpace`
    union-find refactored to `_order_graph_component_count()`; `SorgenfreyLineSpace` counterexample
    in certificate; `QuotientSpace.contains` raises `NotImplementedError`; `DiscreteCountableSpace`
    Urysohn support (discrete metric); `_bfs_urysohn` dead-code path fixed; `homology_coefficients`
    prime modulus validation; `relative_homology` double boundary matrix computation; `_induced_on_hk`
    zero-row shape for empty target; `mayer_vietoris` off-by-one boundary (max_dim+2→max_dim+1);
    `CohomologyRing.verify_graded_commutativity()` added; torus `group_type` corrected to
    `"free_abelian_rank_2"`; `cw_complex_pi1` disconnected 1-skeleton guard; cubical OOM warnings.
- **Performance optimizations** (current):
  - `_snf_ext(compute_transforms=False)` — skips all row/column transform matrix updates when only
    the diagonal D is needed; `_mat_rank` now uses this path (~80% inner-loop saving for rank queries).
  - `_twist_reduce` bigint bitmask — `list[set[int]]` → `list[int]` Python bigint column
    representation; pivot detection via `col.bit_length()-1` (C-level intrinsic); **~6.6× kernel
    speedup** applied to both `persistent_homology_optimized` and `cubical_homology`.
- **Phase 3 P3.1 — Knot/Link suite** (`feat/phase3-knot-suite`):
  - `seifert.py`: `seifert_circles`, `seifert_genus_bound`, `seifert_matrix`, `signature`
    (Sylvester LDLT, no numpy); unknot=0, trefoil=1, figure-8=1 verified.
  - `knot_invariants.py` extended: `LinkDiagram`, `linking_number`, `linking_matrix`;
    Hopf link linking number ±1 verified.
  - **HOMFLY-PT** (`homfly.py` + `Laurent2`): `homfly_polynomial(braid_word, n_strands)`
    computes the 2-variable invariant `P(a, z)` from a braid closure via skein recursion
    `a·P(L₊) − a⁻¹·P(L₋) = z·P(L₀)`. Termination is guaranteed by a descending-defect
    measure (under-first crossings → 0 ⇒ unlink). Verified against known values (unknot,
    unlinks, Hopf, trefoil −a⁻⁴+2a⁻²+a⁻²z², figure-8 a²−1+a⁻²−z²) and certified a genuine
    invariant via Markov-stabilisation (±) and conjugation invariance. `Laurent2.to_jones()`
    (a=t⁻¹) and `.to_alexander()` (a=1) reproduce pytop's existing Jones/Alexander exactly.
  - **Multivariable Alexander** (`multivariable_alexander.py`): `multivariable_alexander(link)`
    computes `Δ_L(t₁, …, tₙ)` from a `LinkDiagram` via a Wirtinger presentation (arcs +
    intrinsic orientation by component tracing) and Fox calculus over the n-variable Laurent
    ring, then the `(c−1)`-minor determinant `÷ (t_γ − 1)` for links. Verified: knots reproduce
    the braid Alexander (trefoil 1−t+t², figure-8 1−3t+t²); Hopf → 1; `(2,2k)` torus links →
    `Σ(t₁t₂)ⁱ` satisfying the Torres condition `Δ(t₁,1)=(t₁ᵏ−1)/(t₁−1)` and interchange
    symmetry; split links → 0.
- **Phase 3 P3.2 — 3-manifold basics** (`feat/phase3-knot-suite`, in progress):
  - **Dehn surgery → H₁** (`dehn_surgery.py`): `first_homology_of_surgery(coefficients,
    linking_numbers)` computes `H₁(M)` of rational/integral surgery on a framed link as the
    cokernel of `A_{ii}=pᵢ, A_{ij}=qᵢ·lk(Lᵢ,Lⱼ)` via Smith normal form;
    `first_homology_of_link_surgery(link, coefficients)` reads the linking numbers from a
    `LinkDiagram`. `lens_space_first_homology(p, q)` plus exact lens-space homeomorphism
    (`q'≡±q^±¹ mod p`) and homotopy-equivalence (`qq'≡±n² mod p`) classification. Verified:
    lens spaces ℤ/p, S¹×S² (0-surgery), T³ (0-surgery on Borromean rings), the Poincaré
    homology sphere (E₈ plumbing), and L(7,1)≃L(7,2) (homotopy-equivalent yet not homeomorphic).
- **Phase 3 P3.3 — Khovanov homology** (`feat/phase3-knot-suite`, in progress):
  - **Khovanov homology** (`khovanov.py`): `khovanov_homology(diagram)` builds the cube of
    resolutions from a PD code, the Frobenius algebra `V = ℤ⟨1,X⟩` (with `m`/`Δ` and the
    Khovanov sign), and reduces each quantum grading over ℤ by Smith normal form to give the
    bigraded `Kh^{i,j}` with **free ranks and torsion**. Verified: `d²=0`; the integral groups
    of the unknot, trefoil (ℤ/2 at (−2,−7)), figure-8 (ℤ/2 at (−1,−3),(2,3)) and Hopf link;
    and the graded Euler characteristic = unnormalised Jones (cross-checked against
    `jones_polynomial`).
- **Phase 4 P4.1 — property-based + cross-engine differential testing**
  (`tests/core/test_property_invariants.py`): seeded, reproducible checks of mathematical
  invariants and engine consistency over many random inputs — Euler–Poincaré, rational Betti =
  integral free rank, `b_i(ℤ/p) ≥ b_i(ℚ)`, HOMFLY-PT Markov(±)/conjugation invariance, HOMFLY-PT
  `a=1` = Burau Alexander (two independent engines), Dehn-surgery `|H₁| = |det|` (vs an independent
  Bareiss determinant), and lens-space homeomorphic ⇒ homotopy-equivalent.
- **Phase 4 P4.2 — exact integer linear algebra core** (`exact_linalg.py`): consolidates
  `smith_normal_form`, `integer_rank`, `integer_determinant` (fraction-free Bareiss), and
  `cokernel` → `AbelianGroup` behind one public, tested module. The Bareiss determinant and the
  Smith invariant factors cross-check each other (`det = ±∏ dᵢ` at full rank); `dehn_surgery`
  shares this core (DRY).
- **Phase 4 P4.3 — complexity discipline** (`docs/COMPLEXITY.md`): an honest reference of the
  asymptotic cost and *practical input limits* of every computational engine, plus `Complexity`
  notes on the heavy docstrings — stating plainly where exactness costs exponential time.
- **Phase 4 P4.4 — differential testing against independent oracles**
  (`tests/core/test_external_oracles.py`): pins `exact_linalg` against **sympy** (SNF/det/rank),
  `is_planar` against **networkx** (Boyer–Myrvold), and `signature` against **numpy** eigenvalues —
  truly independent implementations. Test-only (`pip install -e .[oracles]`); the runtime stays
  dependency-free and each block skips when its oracle is absent.
- **Phase 4 P4.5 / P4.6 — GUDHI & python-flint**: pytop's Vietoris–Rips persistence is validated
  against **GUDHI** (the gold-standard TDA library) and `exact_linalg` against **python-flint**; and
  with the optional `[fast]` extra, the integer Smith normal form — hence every homology / Khovanov /
  surgery engine built on it — is routed to **FLINT**, which is **~5–8× faster** even on pytop's
  *sparse* boundary/Khovanov matrices (identical results). The pure-Python core stays the default and
  the only hard requirement (`dependencies = []`).
- **Phase 4 P4.7 — SageMath oracle** (`tests/core/test_sage_oracle.py`, opt-in `PYTOP_SAGE_ORACLE=1`,
  Docker): one batched `sagemath/sagemath` run validates pytop's Alexander/Jones polynomials against
  Sage's independent algorithms and its van Kampen abelianisations against **GAP** (Klein ℤ⊕ℤ/2,
  torus ℤ², ℝP² ℤ/2, wedge ℤ³).
- **Phase 4 P4.8 — SnapPy oracle** (`tests/core/test_snappy_oracle.py`, opt-in
  `PYTOP_SNAPPY_ORACLE=1`, Docker): SnapPy is the gold-standard 3-manifold software and the one
  independent oracle for `dehn_surgery` — a batched run of a local `pytop-snappy` image validates
  `first_homology_of_surgery` against SnapPy's Dehn-filling homology (figure-8 knot surgeries → ℤ/p,
  Whitehead-link surgeries → ℤ/a ⊕ ℤ/b).
- **9 959 tests passing** across the core suite when released (+ 16 opt-in SageMath/SnapPy-oracle tests).

## What's New in v0.6.0

- **Constructive computational core** — invariants computed from raw input, not looked up:
  `homology` (integer boundary matrices → Smith normal form → Betti + torsion; S², T² = ℤ²,
  ℝP² = ℤ/2 verified), `persistent_homology` (Vietoris–Rips filtration → Z/2 reduction → barcodes),
  `knot_invariants` (Kauffman → Jones, reduced Burau → Alexander), `winding_number`,
  `surface_word_classification` (closed-surface type from a gluing word), and exact `graph_planarity`
  (rotation-system genus)
- **pi-Base deductive inference** (`pytop.experimental.pi_base` / `pi_base_atlas`) — a real
  property-inference engine over the pi-Base database (243 properties, 902 implication theorems,
  222 spaces, 2099 traits; CC BY 4.0, Clontz & Dabbs): `deduce` closes a trait set under the
  implication graph and detects contradictions, and `find_counterexamples(has=…, lacks=…)` searches
  the atlas. A cross-validation suite pins pytop's hand-encoded implications against the pi-Base graph
- **9 032 tests passing**; new modules at ≥ 90% coverage; dependency-free at runtime
- **`named_spaces` + `space_catalog`** — 104 canonical named topological spaces (Sierpiński space,
  Cantor set, Hilbert cube, Sorgenfrey line, p-adic numbers, lens spaces, solenoid, …) with a
  queryable `SpaceCatalog` registry; `from pytop import catalog` gives instant lookup by name or
  property
- **User guide enrichment pilot (ch04 + ch06)** — guided proofs, "Ne oldu?" example walkthroughs,
  trace tables, 8 TikZ figures (→ PNG), 4 pedagogical tcolorbox environments, exercise hints,
  and a complete solutions appendix across all 4 formats
- **Maarif pedagogy blocks — all 16 chapters × 3 formats** — every chapter now opens with
  5 pedagogical blockquotes (Neden/Keşif/Hata/Bkz./Öz-yansıtma) in Markdown, Python, and
  Jupyter Notebook formats; chapter-specific content guides motivation, common mistakes, and
  cross-references
- **User guide API hygiene** — ch10 raw `frozenset()`/`set()` patterns replaced with `make_set`/
  `empty_set`; ch03 extended with `compose_relations`, `equivalence_class`,
  `partition_from_equivalence`, and `total_order_from_list` examples across all 3 formats

## What's New in v0.5.33

- **`topological_field_theory`** — Atiyah-Segal axioms, cobordism hypothesis, Frobenius algebras, Chern-Simons, Donaldson, factorization algebras (196 tests)
- **`higher_categories`** — quasi-categories, Kan complexes, complete Segal spaces, stable ∞-categories, ∞-toposes (200 tests)
- **`spectral_sequences`** — Serre, Adams, AHSS, Leray-Hirsch, LHS, Grothendieck (170 tests)
- **`operads`** — Ass/Com/Lie/A∞/L∞/E_n, Koszul duality, bar-cobar (170 tests)
- **User guide** — 16-chapter guide in 4 formats, 73-page compiled PDF
- **8 914 tests passing**, 98.74% coverage

See [CHANGELOG.md](CHANGELOG.md) for full details.

## Formal Verification (`formal/`)

The `formal/` directory contains **Lean 4 + Mathlib v4.31** machine-checked proofs
for the core algorithms and topological foundations.  
Build: `cd formal && lake build`

### Verified paths

| File | Content | Sorry |
|------|---------|-------|
| `SNF/` | Smith Normal Form correctness — clearPass residues, pivot positivity, fuel-independence, divisibility chain, all 5 branch theorems | **0** |
| `Homology.lean` | Boundary operator ∂∘∂=0, Euler–Poincaré theorem via alternating-sum telescope | 0 |
| `EulerChar.lean` | Euler characteristic = alternating Betti sum | 0 |
| `PersHomology.lean` | Z/2 persistence reduction, `symmDiff_comm/self/assoc`, `reduce_is_reduced` (fuel-based `reduceColFuel` + `reduceInv_step` invariant), `pairs_have_distinct_deaths`, `pairs_birth_lt_death` | **0** |
| `PiBase.lean` | Pi-Base implication graph load & traversal | 0 |
| `SetTopology.lean` | Open-set axioms, closure/interior/boundary, Kuratowski, subspace & product topologies, homeomorphism, T₃/T₄ chain, `compact_union`, `compact_closed_subset`, Urysohn lemma | **0** |
| `MetricTopology.lean` | Metric space, open balls, ε-δ ↔ topological continuity, Cauchy sequences, completeness, `fixedPoint_unique`, Banach fixed-point theorem | **0** |
| `MayerVietoris.lean` _(Phase 11)_ | `SES` structure; `ses_p_zero_of_im`; `delta_well_defined`; `snake_delta_exists`; `snake_delta_independent` | **0** |
| `VanKampen.lean` _(Phase 11)_ | `Pres` + `TietzeEquiv`; `tietze_elim/add_gen`; `AmalgamDatum` + `Pushout`; `pushout_universal`; `int_hom_determined_by_one`; `int_hom_exists` | **0** |
| `CohomologyRing.lean` _(Phase 11)_ | Alexander–Whitney `cup` (`⌣`); `cup_value_assoc`; `cup_comm_Z2`; `coboundary0`; `leibniz_0cochains` | **0** |
| `PersistencePairing.lean` _(Phase 11)_ | `pairing_is_perfect`; `pairs_have_distinct_births`; lemma chain via `isReduced_tail` + `filterMap_getLast_nodup_of_isReduced` + `List.mem_iff_getElem` | **0** |
| `SpectralSequences.lean` _(Phase 11)_ | `ChainCx` (d²=0); `d_sq_zero`; `image_sub_kernel`; `SpectralSeq`; `const_convergent`; `stabilizes_mono`; `const_pages_convergent` | **0** |

### Key theorems (selected)

```lean
-- Smith Normal Form
theorem pytopSNF_positive      : ∀ i, 0 ≤ (pytopSNF M).diag i
theorem pytopSNF_fuel_independent : pytopSNF M = pytopSNF' M   -- fuel doesn't matter
theorem pytopSNF_divisibilityChain : isDivisibilityChain (pytopSNF M).diag

-- Set topology
theorem t4_implies_t3 (τ : Topology α) : isT4 τ → isT3 τ
theorem t3_implies_t2 (τ : Topology α) : isT3 τ → isT2 τ
theorem compact_union  (τ : Topology α) : isCompact τ K₁ → isCompact τ K₂ → isCompact τ (K₁ ∪ K₂)
theorem compact_closed_subset (τ : Topology α) : isCompact τ K → A ⊆ K → isClosed τ A → isCompact τ A

-- Metric topology
theorem openBall_isOpen   (M : MetricSpace α) : (metricTopology M).isOpen (openBall M x r)
theorem epsDelta_implies_topoCont : epsilonDeltaContinuous M N f x₀ → topological continuity at x₀
theorem topoCont_implies_epsDelta : topological continuity at x₀ → epsilonDeltaContinuous M N f x₀
theorem convergent_is_cauchy      : convergesTo M seq L → isCauchy M seq
theorem limit_unique              : convergesTo M seq L₁ → convergesTo M seq L₂ → L₁ = L₂
theorem fixedPoint_unique         : isContraction M f → f p = p → f q = q → p = q

-- Persistence homology (PersHomology.lean)
theorem symmDiff_assoc            : symmDiff (symmDiff a b) c = symmDiff a (symmDiff b c)
theorem reduce_is_reduced          : isReduced (reduce M)  -- fuel-based termination proof
theorem pairs_have_distinct_deaths : ((persistencePairs M).map Prod.snd).Nodup
theorem pairs_birth_lt_death       : (∀ jcol ∈ zipWith … (reduce M), ∀ x ∈ jcol.2, x < jcol.1)
                                     → ∀ p ∈ persistencePairs M, p.1 < p.2
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
