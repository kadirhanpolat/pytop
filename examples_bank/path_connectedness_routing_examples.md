# Path-Connectedness and Vehicle Routing Examples (APL-03)

- Source: `AdamsFranzosa2008Topology`
- Sections: §6.5 (Automated Vehicle Navigation), §6.1–6.2 (Path-Connectedness)
- Version introduced: `v0.2.4`
- Route: `APL-03`
- Rule: Original package explanations only. Book sections guide topic selection and
  fact verification; no problem statements or extended prose are copied verbatim.

---

## Part A — Path-Connectedness: Core Theory

### A.1 Paths and Path-Connectedness

**Definition.** Let X be a topological space and let a, b ∈ X. A **path** from
a to b is a continuous function γ : [0,1] → X such that γ(0) = a and γ(1) = b.
The interval [0,1] carries the subspace topology inherited from ℝ.

A topological space X is **path-connected** if for every pair of points a, b ∈ X
there exists a path from a to b.

**Examples of path-connected spaces.**
- ℝⁿ is path-connected: for any a, b ∈ ℝⁿ the linear path γ(t) = (1−t)a + tb
  is continuous and connects a to b.
- Any convex subset of ℝⁿ is path-connected by the same linear path argument.
- The unit circle S¹ = {(x,y) : x²+y² = 1} is path-connected.
- The torus S¹×S¹ is path-connected (product of path-connected spaces).

**Example of a non-path-connected space.** Let X = {(x,y) ∈ ℝ² : x < 0} ∪ {(x,y) ∈ ℝ² : x > 0}.
No continuous path can cross from the left half-plane to the right half-plane
while remaining in X, because [0,1] is connected and the image of a continuous
map from a connected space is connected.

---

### A.2 Path-Connectedness vs. Connectedness

**Theorem.** Every path-connected space is connected.

*Proof sketch.* Suppose X is path-connected and write X = U ∪ V with U, V
disjoint open sets. Fix a ∈ U and b ∈ V. Let γ : [0,1] → X be a path from
a to b. Then γ⁻¹(U) and γ⁻¹(V) are disjoint open sets covering [0,1], with
0 ∈ γ⁻¹(U) and 1 ∈ γ⁻¹(V). This contradicts the connectedness of [0,1].
So X cannot be written as such a union, hence X is connected.

**The converse fails.** The **Topologist's Sine Curve** is connected but not
path-connected:

    S = {(x, sin(1/x)) : x > 0} ∪ {(0, y) : −1 ≤ y ≤ 1}

The vertical segment {0}×[−1,1] cannot be reached by any continuous path
from a point in the graph portion {(x, sin(1/x)) : x > 0}, because any
approach requires oscillations of unit amplitude with increasing frequency.

**Summary.**

| Property | Holds for path-connected? | Converse? |
|---|---|---|
| Connected | Yes (always) | No (sine curve counterexample) |
| Path-connected | Definition | — |

---

### A.3 Path-Connected Components

**Definition.** A **path-connected component** (or **path component**) of a
topological space X is a maximal path-connected subspace. That is, P ⊆ X is
a path component if:
1. P is path-connected.
2. If P ⊆ Q ⊆ X and Q is path-connected, then P = Q.

**Existence.** Every point x ∈ X belongs to exactly one path component: the
union of all path-connected subsets of X that contain x. This union is itself
path-connected (concatenation of paths), so it is the unique maximal one.

**Properties of path components.**
- Path components partition X (every point belongs to exactly one component).
- Each path component is connected.
- Path components need not be open or closed in general.

**Example.** Let X = ℝ² \ {(0,0)} (the punctured plane). Every pair of points
can be connected by a path avoiding the origin (go around it). So X has exactly
one path component: X itself.

**Example.** Let X = ℝ² \ {(x,0) : 0 ≤ x ≤ 1} (the plane minus a horizontal
segment). The space X is still path-connected: any two points can be connected
by a path that detours above or below the removed segment. So X has one
path component.

**Example.** Let X = ℝ² \ {(x,0) : x ∈ ℝ} (the plane minus the x-axis). Now X
has exactly two path components: the upper half-plane {y > 0} and the lower
half-plane {y < 0}. No path in X can cross from y > 0 to y < 0.

---

### A.4 Concatenation and Reversal of Paths

**Concatenation.** If γ₁ : [0,1] → X is a path from a to b and
γ₂ : [0,1] → X is a path from b to c, their **concatenation** γ₁ * γ₂ is

    (γ₁ * γ₂)(t) = γ₁(2t)       for 0 ≤ t ≤ 1/2
                   γ₂(2t − 1)   for 1/2 ≤ t ≤ 1

By the pasting lemma (the two definitions agree at t=1/2 since γ₁(1)=b=γ₂(0)),
γ₁ * γ₂ is continuous. It is a path from a to c.

**Reversal.** The **reverse** of γ is γ̄(t) = γ(1−t), a path from b to a.

**Consequence.** Path-connectedness is an equivalence relation:
- Reflexive: the constant path γ(t) = a connects a to a.
- Symmetric: γ connects a to b ⟹ γ̄ connects b to a.
- Transitive: γ₁ connects a to b and γ₂ connects b to c ⟹ γ₁*γ₂ connects a to c.

The equivalence classes are precisely the path components.

**Pytop module link:** `pytop.connectedness`, `pytop.paths`.

---

## Part B — Free Space and Automated Guided Vehicles

### B.1 The AGV Navigation Problem

**Physical setup.** An **automated guided vehicle** (AGV) is a mobile robot
operating autonomously in an industrial workspace — a factory floor, a
warehouse, or a hospital corridor. The workspace is modelled as a bounded
region W ⊆ ℝ². Within W there are fixed obstacles (walls, machinery, shelving
units) represented by a closed set O ⊆ W.

**The free space.** The **free space** of the AGV is

    F = W \ O

the subset of the workspace the vehicle can actually occupy. As a subspace of
ℝ², F carries the subspace topology.

**The routing question.** Given a starting position p ∈ F and a destination
q ∈ F, can the AGV travel from p to q while remaining in F?

**Topological answer.** The AGV can travel from p to q if and only if there
exists a continuous path γ : [0,1] → F with γ(0) = p and γ(1) = q. In other
words, p and q must lie in the **same path-connected component** of F.

---

### B.2 Three Canonical Obstacle Configurations

The path-structure of F depends entirely on the geometry of O. Three
canonical cases illustrate the range of possibilities.

**Case 1: No obstacles (O = ∅).**
F = W. If W is convex (e.g., a rectangle), F is convex, hence path-connected.
Every position is reachable from every other. There is exactly one path component.

**Case 2: Single interior obstacle.**
Let W = [0,10]² (a 10×10 square room) and let O be the rectangle [3,7]×[2,8]
(a central column). Then F = W \ O is path-connected: the AGV can travel from
any point to any other by navigating around the column. One path component.

    Route from (1,5) to (9,5):
    γ(t) = (1,5) → (2,1) → (8,1) → (9,5)   [go below the column]

Any two points in F can be connected by a path in the "corridor" surrounding
the obstacle.

**Case 3: Wall dividing the workspace.**
Let W = [0,10]² and let O = {5}×[0,9] (a vertical wall from the bottom to
near the top). Then F = W \ O has **two path components**:

    F_L = {(x,y) ∈ F : x < 5}   (left chamber)
    F_R = {(x,y) ∈ F : x > 5}   (right chamber)

and a narrow corridor near the top {(x,y) : 9 < y ≤ 10, x ≠ 5} connecting
the two sides. Whether F is path-connected or has two components depends on
whether the wall reaches all the way to the boundary. If O = {5}×[0,10]
(a wall from floor to ceiling), F has exactly two components with no route
between them.

---

### B.3 Obstacle Addition and Disconnection

**Key monotonicity principle.** Adding obstacles to F can only reduce (or
maintain) the number of reachable positions from any given point — it can
never increase reachability. More precisely:

If O ⊆ O' then F' = W \ O' ⊆ F = W \ O. Any path in F' is also a path in F,
so each path component of F' is a subset of some path component of F.

**Disconnection by obstacle addition.** Adding an obstacle that "cuts across"
a path component splits it into two or more components.

**Example: Splitting a corridor.**
Suppose F is the rectangular corridor [0,10]×[0,2] (path-connected). Add a
new obstacle O' = {5}×[0,2]: a thin wall spanning the full height. Then
F' = F \ O' has two components: {x < 5, 0 ≤ y ≤ 2} and {x > 5, 0 ≤ y ≤ 2}.
The single path-connected space splits into two, and the AGV starting in one
cannot reach the other.

**Topological characterisation of the split.** The obstacle O' = {5}×[0,2]
is a **separator** of the corridor: a closed set whose removal disconnects F
into path components.

---

### B.4 The Free Space as a Union of Path Components

In a real warehouse the obstacle set O may be complex, creating a patchwork
of accessible regions. The path-connected component decomposition makes this
precise.

**Decomposition.** Write F = P₁ ∪ P₂ ∪ ⋯ ∪ Pₖ where each Pᵢ is a
path-connected component of F. The AGV at position p ∈ Pᵢ can reach exactly
the positions in Pᵢ. No path in F connects Pᵢ to Pⱼ for i ≠ j.

**Planning consequence.** Before computing a specific route, a navigation
system must first determine whether the destination is in the same component
as the start. If not, no route exists regardless of planning algorithm used —
this is a topological obstruction, not an algorithmic limitation.

**Example: Warehouse grid.**
Imagine a warehouse W = [0,12]²  with obstacles along a grid:

    O = {3}×[0,9] ∪ {9}×[3,12] ∪ [3,9]×{6}

This creates a maze structure. The free space F = W \ O may have one or more
path components depending on whether gaps in the walls are present. Computing
the path components of F is the prerequisite for any routing plan.

---

### B.5 Collision-Free Paths and Homotopy

**Homotopy of paths.** Two paths γ₀ and γ₁ from p to q in F are
**homotopic relative endpoints** if there is a continuous map
H : [0,1]×[0,1] → F with

    H(s, 0) = γ₀(s),   H(s, 1) = γ₁(s),   H(0, t) = p,   H(1, t) = q

for all s, t ∈ [0,1]. Intuitively, γ₁ is obtained from γ₀ by a continuous
deformation that fixes the start and end points while staying in F.

**Engineering relevance.** Two homotopic paths represent routes the AGV can
continuously transition between without retracing to the start. Non-homotopic
paths are qualitatively different routes (e.g., one goes around an obstacle
on the left, the other on the right) and cannot be continuously deformed
into each other within F.

**Simply connected free space.** If F is **simply connected** (path-connected
and every loop is homotopic to a constant), then any two paths from p to q
in F are homotopic — there is essentially one route class between any pair of
points. A convex free space is always simply connected.

**Non-simply connected free space.** If F contains a hole (an obstacle completely
surrounded by free space), different routes around the hole are homotopically
distinct. The AGV planner may need to choose which side of the obstacle to
favour based on clearance or energy constraints.

---

### B.6 Worked Navigation Example

**Setup.** Let the workspace be W = [0,8]×[0,8]. The obstacle set is:

    O = [2,6]×[2,6] \ [3,5]×[3,5]

That is, O is a square frame (outer boundary [2,6]², inner boundary [3,5]²):
an annular obstacle with a square hole. The free space is:

    F = W \ O = (exterior of the frame in W) ∪ (interior hole [3,5]×[3,5])

**Path-connected components of F.**

- F_outer = {points in W outside the frame [2,6]²}: the region surrounding
  the frame within the room.
- F_inner = [3,5]×[3,5]: the region inside the frame.

These two regions are separated by the frame O. No continuous path in F can
travel from F_outer to F_inner without passing through O. So F has **two
path-connected components**.

**Navigation conclusion.**
- AGV at (1,1) (outside the frame) → AGV at (7,7) (also outside): **reachable**
  (both in F_outer).
- AGV at (1,1) (outside) → AGV at (4,4) (inside the hole): **not reachable**
  (different components).
- AGV at (4,4) → AGV at (3.5, 3.5) (also inside): **reachable** (both in F_inner).

A navigation system querying path-component membership can answer all three
questions without ever computing an explicit route.

**Pytop module link:** `pytop.connectedness`, `pytop.paths`, `pytop.spaces`.

---

## Part C — Configuration Space and Motion Planning

### C.1 From Workspace to Configuration Space

The AGV position example treats the robot as a point particle. Real robots
have shape, orientation, and multiple degrees of freedom. The correct
topological setting is the **configuration space** C, whose points are the
possible states of the entire robot system.

**Point robot.** For an AGV treated as a point, C = W ⊆ ℝ² and the free
configuration space is C_free = F = W \ O (same as the free space above).

**Disk robot.** For an AGV modelled as a disk of radius r, the effective
free space shrinks: a configuration (position of the disk centre) is free
only if the disk does not intersect O. The effective obstacle in configuration
space is the **Minkowski sum** O ⊕ B(0,r), so

    C_free = W \ (O ⊕ B(0,r))

Adding the robot's footprint enlarges the effective obstacle, potentially
creating new disconnections that would not arise for a point robot.

**Rotatable robot.** If the AGV can rotate, each configuration is a triple
(x, y, θ) with (x,y) ∈ W and θ ∈ [0, 2π). Identifying θ=0 and θ=2π gives

    C = W × S¹

The configuration space is three-dimensional, and C_free ⊆ W × S¹ is the
set of collision-free configurations. Path-connectedness in C_free means the
robot can continuously translate and rotate from one pose to another without
collision.

---

### C.2 The Two-Link Arm as Configuration Space

**Setup.** A two-link planar robotic arm has a fixed base. Link 1 rotates
at the base with angle θ₁ ∈ [0, 2π). Link 2 rotates relative to Link 1 with
angle θ₂ ∈ [0, 2π). The pair (θ₁, θ₂) completely specifies the arm's
configuration.

**Configuration space.** Identifying θᵢ = 0 with θᵢ = 2π in each factor
gives

    C = S¹ × S¹ = T²

the **torus**. This is a compact surface constructed from the square
[0,2π]×[0,2π] by the quotient identification that glues opposite edges.

**Quotient construction.** The projection [0,2π]×[0,2π] → T² is the
map (θ₁, θ₂) ↦ (e^{iθ₁}, e^{iθ₂}) ∈ S¹×S¹. The quotient topology on T²
makes this map continuous, and it is the natural topology for motion planning:
a path in T² is a continuous motion of the arm.

**Free configuration space.** If the workspace contains obstacles, certain
joint-angle pairs place the arm in collision. The forbidden configurations form
the **obstacle region** C_obs ⊆ T². The free configuration space is

    C_free = T² \ C_obs

**Path-connectivity of C_free.**
- If C_obs is empty, C_free = T² is path-connected (the torus is connected).
- If C_obs is a single closed curve on T², it may separate T² into two regions,
  meaning some arm configurations cannot be reached from others without
  colliding.
- If C_obs consists of isolated points, C_free remains path-connected (removing
  a finite set of points from T² does not disconnect it).

**Pytop module link:** `pytop.connectedness`, `pytop.paths`, `pytop.products`,
`pytop.quotients`, `pytop.surfaces`.

---

### C.3 Path Components and Motion Planning Feasibility

**The planning problem.** Given start configuration q_start ∈ C_free and
goal configuration q_goal ∈ C_free, does a collision-free motion exist?

**Topological answer.** A collision-free motion exists if and only if q_start
and q_goal lie in the same path-connected component of C_free.

**Complexity.** Computing the path components of C_free is generally hard
(the space is high-dimensional and the obstacle geometry complex). For the
two-link arm in 2D, C_free ⊆ T² is two-dimensional, making analysis tractable.
For n-link arms, C ≅ (S¹)ⁿ is n-dimensional.

**Algorithmic approaches.** Motion planning algorithms (roadmap methods,
potential fields, RRT/PRM sampling) are essentially heuristics for
discovering paths within a single component of C_free. Topology determines
whether a solution can exist; algorithms find the solution when it does.

---

## Part D — Summary and Cross-References

### D.1 Key Principles

| Principle | Statement |
|---|---|
| Path ↔ route | A collision-free route is a path in C_free |
| Reachability ↔ path component | Two configurations are connected iff same path component |
| Obstacle addition | Can only decrease path component size, never increase |
| Simply connected C_free | All routes homotopically equivalent; no topological routing choice |
| Non-simply connected C_free | Qualitatively distinct route classes around holes |

### D.2 Relationship Between Space Types

| Space | Dimension | Example robot |
|---|---|---|
| W ⊆ ℝ² | 2 | Point AGV |
| W × S¹ | 3 | AGV with heading |
| S¹ × S¹ = T² | 2 | Two-link planar arm |
| (S¹)ⁿ | n | n-link planar arm |

As the configuration space dimension grows, path-connectedness of C_free
becomes harder to compute but remains the fundamental feasibility criterion.

### D.3 Connections to Other Topics

- **Quotient topology (§3.3/§3.5):** The torus C = T² is constructed via
  quotient identification; the free configuration space inherits its topology.
- **Connectedness vs. path-connectedness (§6.1–6.2):** C_free may be connected
  but not path-connected (rare in practice for smooth obstacles, but possible).
- **Homotopy (§9.1):** Route classes in a non-simply-connected C_free are
  elements of the fundamental group π₁(C_free).
- **Compact surfaces (§14.2):** The configuration spaces of standard robot
  arms are compact surfaces or their products.

---

## Cross-reference to Pilot Examples

| Pilot example (adams_franzosa_pilot_examples.md) | Expanded here |
|---|---|
| Example 6 (AGV free-space routing) | §B.1–B.6 |
| Example 7 (two-link robotic arm torus) | §C.2 |
