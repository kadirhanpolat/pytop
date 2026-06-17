# pytop

[![CI](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml/badge.svg)](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-0.6.0-blue)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

A mathematical topology library for Python, covering point-set topology, knot theory, graph topology, surface classification, 3-manifolds, higher categories, operads, spectral sequences, topological field theory, and more.

As of **v0.6.0+**, alongside its descriptive/profile layer pytop ships a **constructive computational core** (simplicial homology + field/relative coefficients + Mayer–Vietoris LES + cellular homology, persistent homology, knot polynomials, winding number, surface classification, graph planarity), a **pi-Base–backed deductive inference engine**, and a **research-grade computable-space protocol** (`experimental.spaces`) for point-set topology.

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
| **Computational homology** (v0.6.0+) | `homology`, `persistent_homology`, `homology_coefficients`, `mayer_vietoris`, `cellular_homology` |
| **Knot invariants** (v0.6.0) | `knot_invariants` |
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

## What's New (post-v0.6.0)

- **Research-grade computable-space protocol** (`experimental.spaces`) — Phase 1 complete (S1–S5):
  unified `Space` ABC with 16 witness-producing, decidability-honest predicates (T0–T6/Tychonoff,
  regular/normal, compact/connected, Lindelöf/separable, first/second-countable), 7 representations
  (Finite, Cofinite, Order-ℚ, Metric, Sorgenfrey, Discrete-ℕ, Opaque), finite+infinite construction
  closure (`ProductSpace`, `SubspaceSpace`, `SumSpace`, `QuotientSpace`), and a property-reasoning
  engine that derives and *explains* properties of constructed infinite spaces via preservation
  theorems + the pi-Base implication graph — no enumeration. `synthesize(has=…, lacks=…)` finds
  example spaces. Preservation table cross-validated against pi-Base meta-properties.
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
- **9 250 tests passing** across the full suite.

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
