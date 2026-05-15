# Book source usage notes

This note records how physical books may support the v0.2.x development lane.
It is a source-control surface, not a place for copied book prose.

## Local source evidence

The workspace-level `books/` folder may include these source files during local
development:

- `1965 General Topology.pdf`
- `1989  General Topology - Ryszard Engelking.pdf`
- `1992 Topology - A Geometric Approach - Ryszard Engelking.pdf`
- `2007 Introduction to Topology - Pure and Applied - Colin Adams, Robert Franzosa.pdf`
- `2007 Introduction to Topology - Pure and Applied - Colin Adams, Robert Franzosa.md`
  *(AI-readable Markdown mirror of the Adams & Franzosa book, available for source-guided study.)*

The release zip excludes PDF files. These books are source evidence for
planning, bibliography metadata and example selection; they are not release
artifacts.

## Registered BibTeX keys

The following keys are registered in `manuscript/shared/bibliography.bib` and
are ready for citation. The Adams & Franzosa key is the active source key for
the v0.2.x applied-topology expansion lane.

| Key | Source | Primary use |
|---|---|---|
| `Engelking1978` | Engelking -- Dimension Theory | Dimension-theory support. |
| `Engelking1989GeneralTopology` | Engelking -- General Topology | General-topology reference support. |
| `EngelkingSieklucki1992Topology` | Engelking & Sieklucki -- Topology: A Geometric Approach | Geometric-topology support. |
| `Lipschutz1965GeneralTopology` | Lipschutz -- Schaum's Outline of General Topology | Elementary general-topology support. |
| `AdamsFranzosa2008Topology` | Adams & Franzosa -- Introduction to Topology: Pure and Applied | v0.2.x applied-topology examples and profiles. |

## Adams & Franzosa source-link map

The files below are project-native summaries, examples, profiles or teaching
artifacts derived from the source-guided roadmap. They should cite or point to
`AdamsFranzosa2008Topology` at the lane level, while avoiding direct copied
book prose or exercise text.

| Lane | File | Source range |
|---|---|---|
| DEV-02/APL pilot | `examples_bank/adams_franzosa_pilot_examples.md` | Ch. 1--6 applied examples |
| APL-01 | `examples_bank/applied_topology_intro_examples.md` | Sec. 1.4 and 2.4 |
| APL-02 | `examples_bank/metric_information_biology_examples.md` | Sec. 5.2 |
| APL-03 | `examples_bank/path_connectedness_routing_examples.md` | Sec. 6.5 |
| APL-04 | `examples_bank/configuration_phase_space_examples.md` | Sec. 3.5 |
| DYN | `examples_bank/dynamical_systems_examples.md` | Ch. 8 |
| DEG | `examples_bank/degree_theory_applications_examples.md` | Sec. 9.3--9.4 |
| EMB | `examples_bank/digital_image_topology_examples.md` | Sec. 11.3 |
| KNOT | `examples_bank/knot_theory_examples.md` | Sec. 12.1--12.2 |
| KNOT | `examples_bank/knot_invariants_examples.md` | Sec. 12.3 |
| KNOT | `examples_bank/knot_theory_applications_examples.md` | Sec. 12.4 |
| GTOP | `examples_bank/graph_topology_examples.md` | Sec. 13.1 |
| GTOP | `examples_bank/chemical_graph_theory_examples.md` | Sec. 13.2--13.4 |
| MAN | `examples_bank/surface_classification_examples.md` | Sec. 14.2 |
| MAN | `examples_bank/three_manifold_examples.md` | Sec. 14.3 |
| MAN | `examples_bank/cosmology_topology_examples.md` | Sec. 14.4--14.5 |

## Release rule

- Keep source books outside release packages.
- Keep release examples and modules as rewritten, project-native material.
- Add real BibTeX records before manuscript `\cite{...}` keys are used.
- Regenerate `docs/ai_reading/generated` only through project tools.
- Do not hand-edit generated Markdown mirrors.
