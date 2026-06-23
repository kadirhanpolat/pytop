# pytop Examples Bank

Comprehensive worked examples for **pytop** — organized by topic and difficulty level.

**Total:** 36+ examples spanning homology, knot theory, TDA, manifolds, graph topology, and more.

---

## Quick Start

Run an example:

```bash
cd pytop/examples_bank
python3 homology/01_simplicial_homology_sphere.py
```

View Markdown explanations:

```bash
less knot_theory/03_alexander_polynomial_unknot.md
```

---

## Examples by Category

### Homology (6 examples)

Simplicial, persistent, cellular, and relative homology computations.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_simplicial_homology_sphere.py` | Beginner | S² via boundary of tetrahedron |
| 2 | `02_persistent_homology_circle.py` | Beginner | Rips filtration persistence barcodes |
| 3 | `03_cellular_homology_torus.md` | Intermediate | T² via CW complex |
| 4 | `04_mayer_vietoris_wedge_circles.md` | Intermediate | Mayer-Vietoris long exact sequence |
| 5 | `05_relative_homology_pair.md` | Intermediate | H_*(D², S¹) relative computation |
| 6 | `06_cohomology_cup_product.md` | Advanced | Cohomology ring structure T² |

### Knot Theory (5 examples)

Polynomial invariants, Khovanov homology, concordance, and satellite constructions.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_trefoil_alexander_polynomial.py` | Beginner | Alexander polynomial of 3₁ |
| 2 | `02_jones_polynomial_figure_eight.py` | Beginner | Jones polynomial of 4₁ |
| 3 | `03_alexander_polynomial_unknot.md` | Beginner | Verification unknot = 1 |
| 4 | `04_khovanov_homology_trefoil.md` | Advanced | Categorification of Jones |
| 5 | `05_concordance_invariants.md` | Advanced | τ, s, σ bounds on slice genus |
| 6 | `06_satellite_knots.md` | Advanced | Satellite knot construction |

### TDA Pipelines (5 examples)

Full topological data analysis workflows: Rips, Čech, Mapper, persistence descriptors.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_rips_tda_pipeline.py` | Beginner | End-to-end Rips → barcode |
| 2 | `02_cech_complex_pipeline.md` | Intermediate | Čech complex + refinement |
| 3 | `03_persistence_bottleneck_distance.md` | Intermediate | Diagram distance metrics |
| 4 | `04_mapper_algorithm.md` | Advanced | Singh-Mémoli-Carlsson Mapper |
| 5 | `05_landscape_entropy.md` | Advanced | Persistence descriptors |

### Manifolds & Surfaces (5 examples)

Homology, classification, surgery, and 3-manifold invariants.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_klein_bottle_homology.py` | Beginner | Klein bottle H_* with torsion |
| 2 | `02_projective_plane_homology.md` | Beginner | RP² homology structure |
| 3 | `03_surface_word_classification.md` | Intermediate | Surface from word presentation |
| 4 | `04_three_manifold_invariants.md` | Intermediate | Invariants of 3-manifolds |
| 5 | `05_dehn_surgery.md` | Advanced | Trace cobordism construction |

### Graph Topology (4 examples)

Planarity, genus, covering maps, and topological graph invariants.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_graph_planarity_test.py` | Beginner | K₅, K₃,₃ planarity |
| 2 | `02_graph_genus.md` | Intermediate | Rotation system genus |
| 3 | `03_covering_maps_graph.md` | Intermediate | π₁ via covering maps |
| 4 | `04_complete_bipartite_properties.md` | Advanced | K_{m,n} structure analysis |

### Cardinal Functions (3 examples)

Cardinal invariants (weight, density, character, cellularity) on finite and infinite spaces.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_cardinal_invariants.py` | Beginner | Discrete space invariants |
| 2 | `02_ordinal_numbers.md` | Intermediate | Order topology cardinals |
| 3 | `03_compactness_cardinal_bounds.md` | Advanced | Bounds on compact spaces |

### Combinatorial Topology (5 examples)

Simplicial maps, cone/suspension, nerve theorem, discrete Morse, spectral sequences.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_simplicial_maps.md` | Intermediate | Induced homomorphisms |
| 2 | `02_cone_suspension.md` | Intermediate | Contractibility, homology |
| 3 | `03_nerve_theorem.md` | Intermediate | Nerve = union for good cover |
| 4 | `04_discrete_morse_gradient.md` | Advanced | Morse matching, critical cells |
| 5 | `05_spectral_sequence_homology.md` | Advanced | Leray spectral pages |

### Advanced Algebra (3 examples)

Group presentations, higher homotopy, Eilenberg-MacLane spaces, sheaf cohomology.

| # | Example | Level | Topic |
|---|---------|-------|-------|
| 1 | `01_group_presentation_torus.md` | Intermediate | π₁(T²) = ⟨a, b \| [a,b] = 1⟩ |
| 2 | `02_higher_homotopy_eilenberg_maclane.md` | Advanced | K(Z, n) space classification |
| 3 | `03_sheaf_cohomology.md` | Advanced | Čech cohomology computation |

---

## Running Examples

### Python Examples

Interactive computation:

```bash
python3 examples_bank/homology/01_simplicial_homology_sphere.py
```

Expected output:
```
S² Homology:
  H_0(S²) = Z^1
  H_1(S²) = Z^0
  H_2(S²) = Z^1

Verification:
  χ(S²) = 2 (expected: 2)
```

### Markdown Examples

Reference guides with problem statements, solutions, and expected results:

```bash
cat examples_bank/knot_theory/03_alexander_polynomial_unknot.md
```

Use markdown readers or convert to HTML for visualization.

---

## Difficulty Levels

- **Beginner:** Core API usage, basic examples, immediate interpretation
- **Intermediate:** Multi-step workflows, result interpretation, theorem application
- **Advanced:** Research-grade computations, novel invariant combinations, edge cases

---

## Learning Path (Suggested Order)

1. **Start:** Homology 1 (simplicial), Knot Theory 1 (Alexander)
2. **Next:** Homology 2 (persistent), TDA Pipelines 1 (Rips)
3. **Intermediate:** Cardinal Functions 1, Graph Topology 1
4. **Advanced:** Spectral sequences, Mapper, concordance invariants

---

## Contributing New Examples

Structure:

```
examples_bank/<category>/<number>_<name>.{py,md}
```

Guidelines:

- **Python:** Runnable, no external dependencies (pytop only)
- **Markdown:** Problem/Solution/Expected format
- **Docstring:** Include "Problem," "Solution," "Expected" sections
- **Category:** Choose existing or create new category folder
- **Numbering:** Sequential within category (01_, 02_, ...)

Example template (Python):

```python
"""Example: Title

Problem:
  What are we computing?

Solution:
  How pytop solves it.

Expected:
  What the output should be.
"""

import pytop

# Your code here
```

---

## Documentation Links

- **User Guide:** `docs/user_guide/` (16 chapters: LaTeX, Markdown, Python, Jupyter)
- **API Reference:** `docs/api/` (Sphinx autodoc for 200+ modules)
- **CLAUDE.md:** Project structure, phases, roadmap

---

## License

Examples are part of **pytop** — MIT License.
