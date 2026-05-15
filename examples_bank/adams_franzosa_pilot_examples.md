# Adams & Franzosa Pilot Examples

- Source: `AdamsFranzosa2008Topology` (registered in `manuscript/shared/bibliography.bib`)
- Version introduced: `v0.2.1`
- Route: `DEV-02`
- Rule: All examples are original package explanations. Book sections are used
  to select topics and verify facts; no problem statements or long prose are
  copied from the source.

---

## 1. Digital Topology — The Khalimsky Topology on ℤ

**Source reference:** Adams & Franzosa §1.4 (Digital Topology).

The **Khalimsky topology** on the integers ℤ is a non-Hausdorff topology that
models digital images by treating even integers as closed points and odd
integers as open points.

**Definition.** A subset U ⊆ ℤ is *Khalimsky-open* if whenever an even integer
2k belongs to U, both of its neighbours 2k−1 and 2k+1 also belong to U.

**Standard basis elements.** The Khalimsky topology has a basis consisting of:

- `{2k−1, 2k, 2k+1}` for each even integer 2k (an open neighbourhood of 2k),
- `{2k+1}` for each odd integer 2k+1 (a singleton open set).

**Key properties.**

- Odd integers are open points (their singletons are open).
- Even integers are closed points (their singletons are closed).
- The Khalimsky topology on ℤ is T₀ but not T₁.
- The product topology on ℤ² (Khalimsky plane) is used in digital image
  processing to model the pixel grid with correct adjacency structure.

**Pytop module link:** `pytop.finite_spaces`, `pytop.separation`.

---

## 2. Phenotype Space Topology

**Source reference:** Adams & Franzosa §1.4 (Phenotype Spaces).

In theoretical biology, a *phenotype space* is the set of all observable
characteristics of an organism. A topology on phenotype space captures the
idea that phenotypes which are close in the space are related by small
mutations.

**Construction.** Let P be a finite set of phenotypes. A *mutation graph*
G on P connects two phenotypes by an edge if a single point mutation
transforms one into the other. Define a topology on P by taking as open
sets all unions of *connected subgraphs* of G (together with the empty set).

**Properties.**

- The resulting topology is generally non-Hausdorff.
- Connectedness in the topological sense corresponds to reachability in the
  mutation graph.
- Path-connected components correspond to phenotypes reachable from each other
  by a finite chain of single mutations.

**Pytop module link:** `pytop.finite_spaces`, `pytop.spaces`, `pytop.connectedness`.

---

## 3. Geographic Information Systems — Boundary Queries

**Source reference:** Adams & Franzosa §2.4 (Geographic Information Systems).

A **geographic information system (GIS)** represents geographic features
(lakes, forests, roads, cities) as subsets of the plane ℝ². Topological
operators — interior, closure, and boundary — answer spatial queries
directly.

**Standard spatial predicates via topology.**

Let A, B ⊆ ℝ² be two geographic regions.

| Predicate | Topological condition |
|---|---|
| A is *inside* B | A ⊆ Int(B) |
| A *overlaps* B | Int(A) ∩ Int(B) ≠ ∅, A ⊄ B, B ⊄ A |
| A *touches* B | A ∩ B ≠ ∅ and Int(A) ∩ Int(B) = ∅ |
| A *contains* B | B ⊆ Int(A) |
| A and B are *disjoint* | Cl(A) ∩ Cl(B) = ∅ |

**The 9-intersection model.** The DE-9IM (Dimensionally Extended 9-Intersection
Model) classifies the topological relationship between two regions A and B by
recording which of the nine intersections

    {Int(A), Bd(A), Ext(A)} × {Int(B), Bd(B), Ext(B)}

are non-empty. Each entry is 0 (empty) or 1 (non-empty), producing a 9-bit
signature that uniquely identifies the spatial relationship.

**Pytop module link:** `pytop.subset_operators`, `pytop.spaces`.

---

## 4. Hamming Metric — Error-Correcting Codes

**Source reference:** Adams & Franzosa §5.2 (Metrics and Information).

Let Σ = {0, 1} be the binary alphabet and let Σⁿ be the set of all binary
strings of length n.

**Hamming distance.** For u, v ∈ Σⁿ define

    d_H(u, v) = |{i : uᵢ ≠ vᵢ}|

the number of positions in which u and v differ. The function d_H is a metric
on Σⁿ.

**Metric balls.** The open ball B(u, r) in the Hamming metric consists of all
strings that differ from u in fewer than r positions. A code C ⊆ Σⁿ with
minimum Hamming distance δ can *detect* up to δ−1 errors and *correct* up to
⌊(δ−1)/2⌋ errors.

**Example: Repetition code.** The length-3 repetition code
C = {000, 111} ⊆ Σ³ has minimum distance 3. It corrects any single-bit
error because B(000, 2) ∩ B(111, 2) = ∅ in the Hamming metric on Σ³.

**Pytop module link:** `pytop.metric_spaces`.

---

## 5. DNA Sequence Metric

**Source reference:** Adams & Franzosa §5.2 (DNA Sequences).

A DNA strand is a sequence over the alphabet Σ = {A, C, G, T}. The
*edit distance* (Levenshtein distance) d_edit(u, v) counts the minimum number
of single-character insertions, deletions, or substitutions needed to transform
u into v.

**Properties.**

- d_edit is a metric on the set of all finite DNA sequences.
- Unlike the Hamming metric, d_edit handles sequences of different lengths.
- Open balls B(u, r) in d_edit group sequences that are biologically close to u,
  making the metric useful for phylogenetic clustering.

**Pytop module link:** `pytop.metric_spaces`.

---

## 6. Path-Connectedness and Automated Vehicle Routing

**Source reference:** Adams & Franzosa §6.5 (Automated Guided Vehicles).

An *automated guided vehicle* (AGV) operates in a workspace W ⊆ ℝ². Let O ⊆ W
be the set of obstacles. The *free space* is F = W \ O. The AGV can drive
between two positions p, q ∈ F if and only if p and q lie in the same
*path-connected component* of F.

**Topological formulation.** A continuous path γ : [0,1] → F with γ(0) = p
and γ(1) = q is a collision-free route. The existence of such a path is
exactly the path-connectedness condition.

**Consequences.**

- If F is path-connected, any two positions are reachable from each other.
- Each path-connected component of F is a maximal reachable region.
- Adding an obstacle may disconnect F, splitting one component into several.

**Pytop module link:** `pytop.connectedness`, `pytop.paths`.

---

## 7. Configuration Space of a Two-Link Robotic Arm

**Source reference:** Adams & Franzosa §3.5 (Configuration Spaces and Phase Spaces).

A planar two-link robotic arm has two joints, each rotating freely through a
full 360°. The *configuration* of the arm is the pair of joint angles
(θ₁, θ₂) ∈ [0, 2π) × [0, 2π).

**Configuration space.** Identifying 0 and 2π in each factor gives the torus

    C = S¹ × S¹

as the configuration space of the arm. A continuous motion of the arm is
a continuous path in C. Planning a collision-free motion from one configuration
to another is equivalent to finding a path in the *free configuration space*
C_free = C \ Obstacle, where Obstacle encodes the joint-angle pairs that
place the arm in collision.

**Key observations.**

- C is compact (S¹ × S¹ is compact).
- The topology of C_free can be highly non-trivial even for simple obstacle sets.
- Quotient topology machinery (§3.3) is the natural tool for constructing C
  from the square [0,1]² by identifying opposite edges.

**Pytop module link:** `pytop.products`, `pytop.quotients`, `pytop.surfaces`.
