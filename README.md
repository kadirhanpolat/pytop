# pytop

[![CI](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml/badge.svg)](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-0.8.0-blue)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

A mathematical topology library for Python, covering point-set topology, knot theory, graph topology, surface classification, 3-manifolds, higher categories, operads, spectral sequences, topological field theory, and more.

As of **v0.6.0+**, alongside its descriptive/profile layer pytop ships a **constructive computational core** (simplicial homology + field/relative coefficients + Mayer–Vietoris LES + cellular homology + cohomology ring with cup product + van Kampen → π₁ group presentations + optimized persistence (Twist+Clearing) + cubical complexes + bitmap persistence — **Phase 2: 8/8 complete**), a **pi-Base–backed deductive inference engine**, and a **research-grade computable-space protocol** (`experimental.spaces`) for point-set topology.

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
persistent_homology(FiniteMetricSpace(carrier=tuple(pts), distance=math.dist), max_dimension=2)

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
| **Cubical complexes** (v0.6.0+) | `cubical_homology` — `CubicalComplex`, SNF homology, `bitmap_to_cubical_filtration`, `persistent_homology_bitmap` |
| **Fundamental group / van Kampen** (v0.6.0+) | `van_kampen` — `GroupPresentation`, `van_kampen()`, `cw_complex_pi1()`, standard spaces |
| **Knot/link invariants** (v0.6.0+) | `knot_invariants` (Jones, Alexander, linking number/matrix), `seifert` (Seifert circles, genus bound, matrix, signature), `homfly` (HOMFLY-PT `P(a,z)` from braid closures), `multivariable_alexander` (`Δ_L(t₁,…,tₙ)` via Wirtinger + Fox) |
| **3-manifold homology** (v0.7.0+) | `dehn_surgery` — Dehn surgery → `H₁` (SNF cokernel of the framing/linking matrix), lens space homeomorphism/homotopy classification |
| **Khovanov homology** (v0.7.0+) | `khovanov` — bigraded `Kh^{i,j}` (free rank + torsion) categorifying the Jones polynomial |
| **Exact linear algebra** (v0.8.0+) | `exact_linalg` — Smith normal form, integer rank, Bareiss `integer_determinant`, `cokernel` → `AbelianGroup` |
| **Degree / winding** (v0.6.0) | `winding_number` |
| **Surface classification** (v0.6.0) | `surface_word_classification` |
| **Graph planarity** (v0.6.0) | `graph_planarity` |
| **Deductive inference** (v0.6.0) | `experimental.pi_base`, `experimental.pi_base_atlas` |
| **Convergence spaces** (v0.6.0) | `experimental.convergence_spaces` |
| **Computable spaces** (experimental) | `experimental.spaces` — protocol, 16 predicates, reasoning engine, pi-Base bridge |
| Cardinal functions | `cardinal_functions_framework`, `cardinal_numbers` |
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
- **9 945 tests passing** across the full suite.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
