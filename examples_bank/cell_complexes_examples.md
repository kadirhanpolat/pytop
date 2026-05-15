# Cell Complex Examples -- v0.1.117

This examples surface supports the lightweight cell complex bridge. The module
records finite cells, dimensions, attaching descriptions, and a relation to the
simplicial-complex bridge. It is not a full CW-complex validator.

## A disk-like teaching profile

```python
from pytop.cell_complexes import cell, cell_complex_profile

disk = cell_complex_profile(
    "disk_like_profile",
    [
        cell("v", 0, "base 0-cell"),
        cell("e", 1, "1-cell attached with both ends at v"),
        cell("d", 2, "2-cell attached along the loop e"),
    ],
    relation_to_simplicial_complex="A filled triangle complex can also be read as a disk-like 2-cell picture.",
)

assert disk.dimension == 2
assert disk.cell_count == 3
assert disk.cell_counts_by_dimension() == {0: 1, 1: 1, 2: 1}
```

## Simplex mnemonic profile

```python
from pytop.cell_complexes import simplex_as_cell_profile

triangle_profile = simplex_as_cell_profile(2)

assert triangle_profile.dimension == 2
assert triangle_profile.cell_count == 3
assert triangle_profile.certification == "teaching-profile"
```

The simplex mnemonic profile is only a teaching bridge. It does not prove that
an arbitrary topological space is a CW complex, and it does not compute
homology.

## Relationship to simplicial complexes

A finite simplicial complex decomposes a shape into simplexes and all their
faces. A cell complex profile records cells by dimension and attaching language.
The two descriptions often point to the same classroom picture, but the package
keeps them distinct: simplicial-complex helpers validate face closure, while
cell-complex profiles record finite teaching data and deferred assumptions.
