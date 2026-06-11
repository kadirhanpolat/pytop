# pytop

[![CI](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml/badge.svg)](https://github.com/kadirhanpolat/pytop/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-0.5.33-blue)
![Coverage](https://img.shields.io/badge/coverage-98.74%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

A mathematical topology library for Python, covering point-set topology, knot theory, graph topology, surface classification, 3-manifolds, higher categories, operads, spectral sequences, topological field theory, and more.

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

## What's New (Unreleased)

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
