# Geometric Topology Examples Bank Index -- pytop v0.1.137

This durable index consolidates the geometric topology example-bank surfaces after
the closed bridge band `v0.1.109`--`v0.1.132`. It does **not** delete examples.
It gives each `GEO-*` route one canonical examples entry point and records
supporting alias files that should be read as secondary surfaces.

| Route | Canonical examples file | Main module | Supporting examples |
|---|---|---|---|
| `GEO-01` | `geometric_foundations_examples.md` | `src/pytop/euclidean_topology.py` | `line_plane_examples.md`, `metric_space_examples.md` |
| `GEO-02` | `metric_map_taxonomy_examples.md` | `src/pytop/metric_map_taxonomy.py` | `continuity_map_taxonomy.md`, `metric_topology_bridge_examples.md` |
| `GEO-03` | `simplices_examples.md` | `src/pytop/simplices.py` | -- |
| `GEO-04` | `simplicial_complexes_examples.md` | `src/pytop/simplicial_complexes.py` | `polyhedra_examples.md`, `cell_complexes_examples.md` |
| `GEO-05` | `homotopy_examples.md` | `src/pytop/homotopy.py` | `path_connectedness_examples.md`, `fundamental_group_examples.md`, `covering_space_examples.md` |
| `GEO-06` | `euclidean_topology_examples.md` | `src/pytop/euclidean_topology.py` | `standard_spaces.md` |
| `GEO-07` | `surface_examples.md` | `src/pytop/surfaces.py` | `manifold_examples.md`, `surface_gluing_examples.md` |
| `GEO-08` | `continua_examples.md` | `src/pytop/continua.py` | `hilbert_cube_examples.md`, `retracts_examples.md` |

## Editorial policy

- Add new geometric examples to the route's canonical file first.
- Use supporting files only when a distinct entry angle is needed.
- Do not copy the same example paragraph across multiple files.
- Do not remove example files without explicit user approval.
- Keep the external topology book as a scope reference only; do not copy its
  problems, examples, prose or proofs.
