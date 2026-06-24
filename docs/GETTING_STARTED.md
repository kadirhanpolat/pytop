# Getting Started with pytop

`pytop` is a standalone, **zero-dependency** mathematical topology library for
Python 3.11+. It computes genuine invariants — homology, persistent homology
(TDA), knot polynomials, graph planarity, and much more — from raw combinatorial
or geometric input.

This guide gets you from `pip install` to four working computations in a few
minutes. Every code block below has been run against the current release and
produces the output shown.

## Install

```bash
pip install pytopology
```

> **Note on the name.** The distribution is published as **`pytopology`** (the
> short `pytop` name was already taken on PyPI by an unrelated project), but the
> **import name is `pytop`** — exactly like `pip install scikit-learn` then
> `import sklearn`.

```python
import pytop
print(pytop.__version__)   # 1.7.0
```

No other packages are required at runtime. Optional accelerators
(`pip install 'pytopology[fast]'` for a FLINT-backed linear-algebra core,
`[gpu]` for CUDA) are available but never necessary.

---

## 1. Homology of a space

Compute the homology groups of the 2-sphere, built as the boundary of a
tetrahedron (4 vertices, 6 edges, 4 triangles). Homology counts connected
components (H₀), loops (H₁), voids (H₂), …

```python
import pytop

# A simplicial complex is a face-closed set of simplices (given as tuples).
vertices  = [(0,), (1,), (2,), (3,)]
edges     = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
triangles = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]

sphere = pytop.SimplicialComplex(vertices + edges + triangles)

for degree in range(3):
    H = pytop.simplicial_homology(sphere, degree)
    print(f"H_{degree}: rank (Betti) = {H.betti}, torsion = {H.torsion}")
```

```
H_0: rank (Betti) = 1, torsion = ()
H_1: rank (Betti) = 0, torsion = ()
H_2: rank (Betti) = 1, torsion = ()
```

This is exactly the homology of S²: one component, no loops, one enclosed void.

---

## 2. Persistent homology (topological data analysis)

Given a point cloud, persistent homology finds the topological features (loops,
voids) that survive across a range of scales — the core tool of TDA. Here we
sample 12 points from a circle and recover its loop.

```python
import math
import pytop
from pytop import FiniteMetricSpace

# 12 points evenly spaced on the unit circle
points = [(math.cos(2 * math.pi * k / 12), math.sin(2 * math.pi * k / 12))
          for k in range(12)]

# Wrap them in a finite metric space (Euclidean distance)
space = FiniteMetricSpace(carrier=tuple(points), distance=math.dist)

# Vietoris–Rips persistence up to dimension 1, scale 2.5
pairs = pytop.persistent_homology(space, max_dimension=1, max_scale=2.5)

h1 = [p for p in pairs if p.dimension == 1]
loop = max(h1, key=lambda p: p.persistence)
print(f"H_1 bars total: {len(h1)} (most are short-lived sampling noise)")
print(f"dominant loop: birth={loop.birth:.3f}, death={loop.death}, "
      f"essential={loop.is_essential}")
```

```
H_1 bars total: 55 (most are short-lived sampling noise)
dominant loop: birth=0.518, death=inf, essential=True
```

The one long-lived (essential) H₁ bar is the circle's loop; the rest are noise.
Each `PersistencePair` carries `dimension`, `birth`, `death`, `persistence`, and
`is_essential`. From here you can build barcodes, diagrams, landscapes, and
bottleneck/Wasserstein distances — see `pytop.persistence_diagram`,
`pytop.persistence_landscape`, and `pytop.persistence_distances`.

---

## 3. Knot invariants

Compute the Alexander polynomial of the **trefoil**, the simplest nontrivial
knot. The trefoil is the (2, 3) torus knot.

```python
import pytop

# Alexander polynomial as {power: coefficient}
alexander = pytop.torus_knot_alexander_poly(2, 3)
print(alexander)
```

```
{1: 1, 0: -1, -1: 1}
```

That is the polynomial **t − 1 + t⁻¹**, the classical Alexander polynomial of the
trefoil. pytop also computes Jones polynomials (`pytop.jones_polynomial`),
Khovanov homology, concordance invariants (τ, s, σ), and more from knot-diagram
input.

---

## 4. Graph planarity

Decide whether a graph can be drawn in the plane without edge crossings. pytop
uses the linear-time left–right planarity test, so it never raises on large
graphs.

```python
import pytop

square = [(0, 1), (1, 2), (2, 3), (3, 0)]
K5     = [(i, j) for i in range(5) for j in range(i + 1, 5)]      # complete graph on 5
K33    = [(a, b) for a in (0, 1, 2) for b in (3, 4, 5)]           # complete bipartite

print("square is planar:", pytop.is_planar(square))
print("K5 is planar:    ", pytop.is_planar(K5))
print("K3,3 is planar:  ", pytop.is_planar(K33))
```

```
square is planar: True
K5 is planar:     False
K3,3 is planar:   False
```

K₅ and K₃,₃ are the two Kuratowski obstructions — the canonical non-planar
graphs. For the minimal genus surface a graph *does* embed in, use
`pytop.graph_genus`.

---

## Where to go next

- **API reference** — every public function is documented via Sphinx autodoc
  (225 modules). Build it locally or browse the generated reference.
- **`examples_bank/`** — a large collection of worked examples organized by topic
  (homology, knot theory, TDA pipelines, manifolds, graph topology, cardinal
  functions, combinatorial topology, advanced algebra).
- **TDA pipeline** — `pytop.TDAPipeline` chains filtration → reduction → barcode
  → diagram → landscape → distances in a single fluent builder.
- **User guide** — a full 16-chapter pedagogical course lives in
  `docs/user_guide/` (currently in Turkish).

A few orientation notes:

- pytop has **two layers**: *constructive* engines that compute invariants from
  raw input (everything in this guide), and *descriptive* `*Profile` registries
  that record curated facts about famous spaces. New computational work lives in
  the constructive layer.
- The runtime is **pure Python with zero dependencies**. Optional extras
  (`[fast]`, `[gpu]`, `[oracles]`) only accelerate or cross-validate; they are
  never required.
