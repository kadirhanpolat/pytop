# Applied Topology Introductory Examples — APL-01

- Source: `AdamsFranzosa2008Topology`
- Sections: §1.4 (Digital Topology, Phenotype Spaces), §2.4 (Geographic Information Systems)
- Version introduced: `v0.2.2`
- Route: `APL-01`
- Rule: Original package explanations only. Book sections guide topic selection and
  fact verification; no problem statements or extended prose are copied verbatim.

---

## Part A — Digital Topology (§1.4)

### A.1 The Digital Line

**Motivation.** A one-dimensional digital image display consists of a row of
pixels. Consecutive pixels share a boundary. The *digital line* is a topological
space on ℤ that models both the pixels (odd integers) and the boundaries between
consecutive pixels (even integers).

**Basis.** Define basis elements for each integer n ∈ ℤ:

    B(n) = {n}           if n is odd  (open pixel point)
    B(n) = {n−1, n, n+1} if n is even (boundary point with both neighbours)

The collection {B(n) : n ∈ ℤ} is a basis for a topology on ℤ called the
**Khalimsky topology** (or digital line topology).

**Open and closed sets.**
- Every odd integer is open: {2k+1} is a basis element, hence open.
- Every even integer is closed: its complement is a union of basis elements
  for nearby odd integers, so the complement is open.
- Singleton {2k} is *not* open for any even integer 2k.

**Separation axioms.**
- The digital line is **T₀**: for any two distinct points there is an open set
  containing one but not the other (an odd integer is open; its even neighbour
  is not).
- The digital line is **not T₁**: the point {2k} is not closed from the
  perspective of 2k−1, because every neighbourhood of 2k contains 2k−1.
- The digital line is **not Hausdorff**: there is no pair of disjoint open sets
  separating two adjacent integers n and n+1.

**Pytop module link:** `pytop.finite_spaces`, `pytop.spaces`, `pytop.separation`.

---

### A.2 The Digital Plane

**Motivation.** A two-dimensional digital image display is a rectangular grid of
pixels. Each pixel is an open point; horizontal and vertical boundaries between
adjacent pixels are boundary points; corner points where four pixels meet are
closed corner points.

**Space.** Start with ℤ × ℤ. For each (m, n) ∈ ℤ × ℤ define the basis element:

    B(m,n) = {(m,n)}                              if m, n both odd   → open pixel
    B(m,n) = {(m+a, n) : a ∈ {−1,0,1}}           if m even, n odd   → horiz. edge
    B(m,n) = {(m, n+b) : b ∈ {−1,0,1}}           if m odd, n even   → vert. edge
    B(m,n) = {(m+a, n+b) : a,b ∈ {−1,0,1}}       if m, n both even  → corner (3×3)

The collection {B(m,n)} is a basis for a topology on ℤ × ℤ called the
**digital plane topology**.

**Point types and their topological character.**

| Parity of (m,n) | Role | Topological character |
|---|---|---|
| both odd | Open pixel | Singleton is open |
| mixed (one odd, one even) | Edge between two pixels | Singleton is neither open nor closed |
| both even | Corner boundary point | Singleton is closed |

**Observation.** The digital plane is the product of two copies of the digital
line (ℤ_Kh × ℤ_Kh) with the product topology. This agrees with the basis
construction above.

**Not Hausdorff.** Adjacent pixels (m,n) and (m+2,n) (both odd) share every
open neighbourhood that contains the boundary point (m+1,n), so they cannot
be separated by disjoint open sets.

**Application.** In digital image processing, a *digital image* is a function
f : D → C where D ⊆ ℤ × ℤ is a finite pixel array and C is a colour set.
Topological properties of the sublevel sets {p ∈ D : f(p) ≤ t} (e.g.,
connectedness, number of connected components) are used for image segmentation,
character recognition, and boundary detection.

**Pytop module link:** `pytop.finite_spaces`, `pytop.products`, `pytop.separation`.

---

### A.3 Khalimsky Topology — Key Properties Summary

| Property | Digital Line (ℤ_Kh) | Digital Plane (ℤ²_Kh) |
|---|---|---|
| T₀ | Yes | Yes |
| T₁ | No | No |
| Hausdorff (T₂) | No | No |
| Connected | Yes | Yes |
| Locally finite basis | Yes | Yes |
| Compact | No | No |

**Why non-Hausdorff topology works here.** The classic requirement in analysis
that limit points be unique (which requires T₁ at minimum) is relaxed in the
digital setting. Non-Hausdorff topology correctly captures the fact that a
boundary point and its adjacent pixels are "topologically inseparable" — which
matches the physical adjacency of pixels in a display.

---

### A.4 Phenotype Spaces — RNA Secondary Structures (§1.4)

**Biological setting.** An RNA molecule is a chain of nucleotides over the
alphabet {G, C, A, U}. The primary structure is the nucleotide sequence
(the *genotype*). The molecule folds into a stable shape determined by hydrogen
bonding between complementary nucleotide pairs (G–C and A–U). The resulting
folded shape is the *phenotype* (also called *secondary structure* or
*RNA shape*).

Multiple genotype sequences can fold into the same shape. The set of all
genotype sequences yielding shape s is the **neutral network** N(s).

**Mutation probability.** For RNA shapes r and s, define:

    m_{r,s} = number of single-nucleotide mutations from N(r) into N(s)
    m_{r,*} = total single-nucleotide mutations out of N(r)
    p_{r,s} = m_{r,s} / m_{r,*}   (mutation probability from r to s)

The probability p_{r,s} is generally **asymmetric**: p_{r,s} ≠ p_{s,r}
because the neutral networks have different sizes and boundary structures.
This asymmetry prevents using a metric (which must be symmetric); a topology
is the natural framework instead.

**Constructing the phenotype topology.** Given a set S of RNA shapes and a
probability threshold θ, define:

    R_i = {s_i} ∪ {s_j : p_{i,j} > θ}    (shapes to which s_i readily mutates)

Let T_θ be the minimal topology on S containing all sets R_i. Its minimal
basis element at s_i is:

    B_i = ∩{R_j : s_i ∈ R_j}    (intersection of all R_j's that contain s_i)

**Example: GC₁₀ with threshold θ = 1/7.** The set GC₁₀ consists of 8 RNA
shapes {s₁,…,s₈} arising from genotype sequences of length 10 over {G,C}
(total 1024 sequences). With threshold 1/7 (average probability for 7
non-self shapes), the basis elements are:

    B₁ = {s₁, s₃, s₈}
    B₂ = {s₂, s₃, s₆, s₈}
    B₃ = {s₃, s₈}            (intersection of R₁, R₂, R₃, R₄, R₅, R₇, R₈)
    B₄ = {s₁, s₄, s₈}
    B₅ = {s₂, s₅, s₈}
    B₆ = {s₂, s₆, s₈}
    B₇ = {s₇, s₈}
    B₈ = {s₈}

**Key observation.** Shape s₈ has the largest neutral network (431 out of 1024
sequences). Every other shape mutates to s₈ with above-average probability, so
s₈ belongs to every basis element B_i. Conversely, B₈ = {s₈} is a singleton,
meaning s₈ is "topologically far" from all others — the topology reflects the
biological reality that mutation *into* s₈ is common while mutation *out of*
s₈ is relatively rare.

**Effect of threshold.** Increasing the threshold θ shrinks the sets R_i,
making the topology finer. At sufficiently high θ, the topology becomes
discrete (all singletons open). At θ = 0, R_i = S for all i, yielding the
indiscrete topology.

**Pytop module link:** `pytop.finite_spaces`, `pytop.spaces`, `pytop.bases`.

---

## Part B — Geographic Information Systems (§2.4)

### B.1 The Intersection Value

**Setting.** Let A and B be closed subsets of a topological space X
(typically X = ℝ²). The **intersection value** I(A,B) is a 4-bit signature:

    I(A,B) = (C_{∂A ∩ ∂B},  C_{Int(A) ∩ Int(B)},  C_{∂A ∩ Int(B)},  C_{Int(A) ∩ ∂B})

where C_Y = 1 if Y ≠ ∅ and C_Y = 0 if Y = ∅.

There are 2⁴ = 16 possible intersection values. All 16 can be realized by
suitable pairs of closed sets in the plane.

**Interpretation of each bit.**

| Bit position | Intersection tested | Meaning when = 1 |
|---|---|---|
| 1st | ∂A ∩ ∂B | A and B share a boundary point |
| 2nd | Int(A) ∩ Int(B) | A and B have overlapping interiors |
| 3rd | ∂A ∩ Int(B) | Part of A's boundary lies strictly inside B |
| 4th | Int(A) ∩ ∂B | Part of B's boundary lies strictly inside A |

**Example values in ℝ².**

| Pair configuration | I(A,B) |
|---|---|
| A and B are disjoint (no shared points at all) | (0,0,0,0) |
| A and B touch at a boundary point only | (1,0,0,0) |
| A and B are equal | (1,1,0,0) |
| A overlaps B (partial overlap, neither contains the other) | (1,1,1,1) |
| A is strictly inside Int(B) | (0,1,1,0) |
| A ⊆ B with ∂A touching ∂B | (1,1,1,0) |

---

### B.2 Regularly Closed Sets

**Definition.** A set A is **regularly closed** if A = Cl(Int(A)).

Intuitively, a regularly closed set has no "whiskers" (isolated line segments
or points attached to its boundary). Every boundary point of a regularly closed
set is a limit of interior points.

**Examples in ℝ².**
- Regularly closed: closed disk, closed rectangle, closed annulus, closed
  convex polygon.
- Not regularly closed: a closed disk with a line segment attached (whisker),
  a finite set of isolated points, a closed square with a diagonal segment
  bridging two corners.

**Why this matters for GIS.** Geographic regions (lakes, forests, parcels)
are naturally regularly closed: they have genuine two-dimensional interiors,
and their boundaries do not include whisker-thin appendages.

**Theorem (Adams & Franzosa §2.4).** Let A and B be regularly closed. If
∂A ∩ Int(B) ≠ ∅, then Int(A) ∩ Int(B) ≠ ∅.

*Reason.* Since A is regularly closed, ∂A ⊆ Cl(Int(A)). Any point in
∂A ∩ Int(B) lies in Cl(Int(A)), so every neighbourhood of it meets Int(A).
But Int(B) is itself a neighbourhood of that point, so Int(A) ∩ Int(B) ≠ ∅.

**Consequence.** For regularly closed A and B, bits 3 and 4 can only be 1 if
bit 2 is also 1. This eliminates 6 of the 16 possible values, leaving 10
achievable intersection values for regularly closed pairs.

---

### B.3 Planar Spatial Regions and the OGC Standard

**Definition.** A **planar spatial region** is a nonempty proper closed subset
C ⊆ ℝ² such that:
1. C is regularly closed.
2. Int(C) is *connected* (cannot be split into two disjoint nonempty open parts).

Closed disks, closed rectangles, and closed convex polygons are all planar
spatial regions. A figure-eight shape (two disks touching at one point) is not,
because its interior consists of two disjoint open parts.

**Theorem (Adams & Franzosa §2.4).** For two planar spatial regions A and B,
only 9 intersection values are possible, and each uniquely determines the
geometric relationship:

| I(A,B) | OGC Expression | Meaning |
|---|---|---|
| (0,0,0,0) | **disjoint** | A ∩ B = ∅ |
| (1,0,0,0) | **touches** | A ∩ B = ∂A ∩ ∂B (boundary contact only) |
| (1,1,0,0) | **equals** | A = B |
| (0,1,1,0) | **within** (strict) | A ⊆ Int(B) |
| (1,1,1,0) | **within** (boundary) | A ⊆ B, ∂A touches ∂B |
| (0,1,0,1) | **contains** (strict) | B ⊆ Int(A) |
| (1,1,0,1) | **contains** (boundary) | B ⊆ A, ∂B touches ∂A |
| (0,1,1,1) | **overlaps** (no boundary) | Int(A)∩Int(B)≠∅, A⊄B, B⊄A |
| (1,1,1,1) | **overlaps** (with boundary) | Int(A)∩Int(B)≠∅, A⊄B, B⊄A |

These 9 expressions (with "within" and "contains" each covering 2 values, and
"overlaps" covering 2 values, giving 6 named relations total) form the
**Open Geospatial Consortium (OGC) standard** spatial predicates. GIS software
uses these to answer queries such as:

> "Return all wetland areas A that overlap or lie within a state park B."

Answer: return pairs (A,B) where I(A,B) ∈ {(0,1,1,1), (1,1,1,1), (0,1,1,0), (1,1,1,0)}.

---

### B.4 GIS Query Examples

**Query 1 — Wetlands in parks.** Let A = wetland, B = state park.
Return pairs where "A is within B" or "A overlaps B":

    Condition: bit 2 of I(A,B) = 1  AND  bit 3 of I(A,B) = 1
    (equivalently: I(A,B) ∈ {(0,1,1,0), (1,1,1,0), (0,1,1,1), (1,1,1,1)})

**Query 2 — Shared boundaries.** Find pairs of municipalities that share a
common boundary segment (but whose interiors are disjoint):

    Condition: I(A,B) = (1,0,0,0)  →  "A touches B"

**Query 3 — Containment check.** Determine whether a proposed building footprint
B lies entirely within a zoning area A:

    If I(A,B) ∈ {(0,1,0,1), (1,1,0,1)}: B is within A  → permit may proceed
    Otherwise: B crosses the zoning boundary  → permit denied

**Pytop module link:** `pytop.subset_operators`, `pytop.spaces`,
`pytop.connectedness`.

---

## Cross-reference to Pilot Examples

The examples in this file expand on the pilot examples in
`adams_franzosa_pilot_examples.md`:

| Pilot example | Expanded here |
|---|---|
| Example 1 (Khalimsky topology on ℤ) | §A.1, A.3 |
| Example 2 (Phenotype spaces) | §A.4 |
| Example 3 (GIS boundary queries, DE-9IM) | §B.1, B.2, B.3, B.4 |
