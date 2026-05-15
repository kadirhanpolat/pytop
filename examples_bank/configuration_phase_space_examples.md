# Configuration and Phase Space Examples (APL-04)

- Source: `AdamsFranzosa2008Topology`
- Sections: §3.5 (Configuration Spaces and Phase Spaces), §3.1–3.3 (Quotient Topology)
- Version introduced: `v0.2.5`
- Route: `APL-04`
- Rule: Original package explanations only. Book sections guide topic selection and
  fact verification; no problem statements or extended prose are copied verbatim.

---

## Part A — Quotient Topology: The Construction Tool

### A.1 Quotient Spaces

**Definition.** Let X be a topological space and let ~ be an equivalence relation
on X. The **quotient set** X/~ is the set of equivalence classes [x] = {y ∈ X : y ~ x}.
The **quotient map** q : X → X/~ sends each point x to its class [x].

The **quotient topology** on X/~ is the finest topology making q continuous:
a set U ⊆ X/~ is open if and only if q⁻¹(U) is open in X.

**Key property.** A function f : X/~ → Y is continuous if and only if
f ∘ q : X → Y is continuous. This makes the quotient topology the correct
setting whenever a space is built by gluing or identifying parts of another
space.

---

### A.2 Standard Quotient Constructions

**The circle S¹.** Start with the interval [0,1]. Identify the two endpoints
0 ~ 1. The quotient [0,1]/~ is homeomorphic to S¹. The quotient map
q : [0,1] → S¹ is q(t) = (cos 2πt, sin 2πt), which collapses the two
endpoints to the single point (1,0).

**The cylinder.** Start with the rectangle [0,1]×[0,1]. Identify left and
right edges: (0, y) ~ (1, y) for all y ∈ [0,1]. The quotient is homeomorphic
to S¹×[0,1], a finite cylinder.

**The Möbius band.** Same rectangle, but identify left and right edges with
a flip: (0, y) ~ (1, 1−y). The quotient is the Möbius band — a non-orientable
surface with boundary.

**The torus T².** Identify both pairs of opposite edges of [0,1]×[0,1]:
- (0, y) ~ (1, y)    (left ↔ right, wrapping the x-direction into S¹)
- (x, 0) ~ (x, 1)    (bottom ↔ top, wrapping the y-direction into S¹)

The quotient is homeomorphic to S¹×S¹, the torus. The quotient map is
q(x,y) = (e^{2πix}, e^{2πiy}) ∈ S¹×S¹ ⊆ ℂ×ℂ.

**The Klein bottle.** Identify left ↔ right as in the cylinder, but identify
top ↔ bottom with a horizontal flip: (x, 0) ~ (1−x, 1). The quotient is
the Klein bottle — non-orientable and non-embeddable in ℝ³ without
self-intersection.

**Summary table.**

| Starting space | Identifications | Quotient |
|---|---|---|
| [0,1] | 0 ~ 1 | S¹ |
| [0,1]×[0,1] | left ↔ right | S¹ × [0,1] (cylinder) |
| [0,1]×[0,1] | left ↔ right (flipped) | Möbius band |
| [0,1]×[0,1] | left ↔ right, top ↔ bottom | T² = S¹ × S¹ (torus) |
| [0,1]×[0,1] | left ↔ right, top ↔ bottom (flipped) | Klein bottle |
| [0,1]×[0,1] | all four edges to a point | S² |

**Pytop module link:** `pytop.quotients`.

---

### A.3 Why Quotients Arise in Applications

A quotient space arises whenever the natural description of a physical system
involves periodicity or identification:

- An angle θ ∈ [0°, 360°) has 0° and 360° representing the same orientation.
  The correct model is [0°, 360°] with 0° ~ 360°, which is S¹.
- A temperature control dial that wraps around from maximum to minimum is again S¹.
- Two joint angles (θ₁, θ₂), each periodic, give T² = S¹×S¹.
- A particle in a box with periodic boundary conditions lives on a torus.

The quotient construction formalises the identification and endows the resulting
space with the correct topology for continuity arguments.

---

## Part B — Configuration Spaces

### B.1 What Is a Configuration Space?

**Definition.** The **configuration space** C of a mechanical system is the
set of all possible states (positions and orientations) of the system, equipped
with a topology in which nearby configurations correspond to states reachable
by a small motion.

A **configuration** is a complete specification of the system's position —
every joint angle, every translational degree of freedom — at a single instant.
A **motion** of the system is a continuous path γ : [0,1] → C in configuration
space.

**Why topology matters.** The topology of C determines:
- Which configurations can be continuously connected by motions (path components).
- Whether a motion can be continuously deformed into another (homotopy class).
- Global constraints such as compactness (can all configurations be reached from
  a bounded set of control inputs?).

---

### B.2 Single-Joint Arm: Configuration Space S¹

**Physical description.** A single rigid link is attached to a fixed base at
one end. The link is free to rotate in the plane. The only degree of freedom is
the joint angle θ.

**Configuration space.** Each configuration is an angle θ ∈ [0°, 360°).
Identifying 0° with 360° (since they represent the same physical position)
gives

    C₁ = S¹

The quotient construction: take the interval [0°, 360°] and identify endpoints.
The resulting circle S¹ is compact, connected, and one-dimensional.

**Continuous motion.** A continuous motion of the single-joint arm is a
continuous path γ : [0,1] → S¹. Since S¹ is path-connected, any two
configurations can be connected by a motion. There are no isolated configurations.

**Non-trivial topology.** Although S¹ is path-connected, it is not simply
connected: a loop that winds once around the circle cannot be continuously
contracted to a point. This corresponds to the physical fact that a cable
attached to the link can become tangled after a full rotation.

---

### B.3 Two-Link Arm: Configuration Space T²

**Physical description.** Two rigid links are connected in series:
- Link 1 rotates about a fixed base with joint angle θ₁ ∈ [0°, 360°).
- Link 2 rotates about the distal end of Link 1 with joint angle θ₂ ∈ [0°, 360°).

The configuration of the arm is the ordered pair (θ₁, θ₂).

**Configuration space.** Each pair (θ₁, θ₂) represents one configuration.
Both angles are periodic:

    C₂ = S¹ × S¹ = T²

the **torus**.

**Quotient construction.** Begin with the unit square [0,1]×[0,1], where the
first coordinate represents θ₁/360° and the second θ₂/360°. Identify:
- Left edge with right edge: (0, s) ~ (1, s) for all s (θ₁ periodicity).
- Bottom edge with top edge: (t, 0) ~ (t, 1) for all t (θ₂ periodicity).

The result is exactly T². The quotient map is

    q(t, s) = (e^{2πit}, e^{2πis}) ∈ S¹ × S¹

**Properties of T².**
- T² is compact: the image of the compact square under the continuous quotient map.
- T² is path-connected: any two configurations can be connected by a motion.
- T² is not simply connected: loops winding around either S¹ factor are
  not contractible. This reflects the cable-management problem for both joints.
- The fundamental group π₁(T²) = ℤ × ℤ captures the two independent winding numbers.

**Visualisation.** Embed T² in ℝ³ as a surface of revolution:

    (θ₁, θ₂)  ↦  ((R + r cos θ₂) cos θ₁,  (R + r cos θ₂) sin θ₁,  r sin θ₂)

with R > r > 0. The outer circle (θ₂ fixed) traces a large circle of radius R;
the inner circle (θ₁ fixed) traces a small circle of radius r. Different
values of (θ₁, θ₂) correspond to different points on the torus surface.

---

### B.4 Three-Link Arm and Beyond

**Three-link arm.** Each of the three joints has an independent angle
θ₁, θ₂, θ₃ ∈ S¹. The configuration space is

    C₃ = S¹ × S¹ × S¹ = T³

the **3-torus**, a three-dimensional manifold. It cannot be visualised as a
surface in ℝ³, but its topology is well-defined: compact, path-connected,
and with fundamental group π₁(T³) = ℤ³.

**n-link arm.** The n-link planar arm has configuration space

    Cₙ = (S¹)ⁿ = Tⁿ

the **n-torus**. This is a compact n-dimensional manifold. Motion planning in
Tⁿ is the topological foundation of robot motion planning for serial chains.

**General principle.** Every degree of freedom that is periodic (rotational
joint) contributes one S¹ factor. Translational degrees of freedom with finite
range contribute a bounded interval [a,b]. Unbounded translational degrees of
freedom contribute ℝ. The full configuration space is the product of all these
factor spaces.

| DOF type | Factor space | Topology |
|---|---|---|
| Rotational joint (periodic) | S¹ | Circle |
| Bounded linear slide [a,b] | [a,b] | Compact interval |
| Unbounded linear slide | ℝ | Non-compact line |

**Pytop module link:** `pytop.products`, `pytop.quotients`, `pytop.surfaces`.

---

## Part C — Phase Spaces

### C.1 Configuration Space vs. Phase Space

A **configuration space** specifies where a system is (position). A
**phase space** specifies where a system is and how fast it is moving
(position and velocity, or position and momentum). Phase spaces arise in
classical mechanics and dynamical systems.

**Definition.** For a mechanical system with configuration space C ⊆ ℝⁿ,
the **phase space** is (locally) C × ℝⁿ: each phase-space point is a pair
(q, v) of a configuration q ∈ C and a velocity vector v ∈ ℝⁿ. The phase
space carries the product topology.

**Example: Particle on S¹.** A particle constrained to move on the circle
S¹ has:
- Configuration space: S¹ (the angle θ).
- Phase space: S¹ × ℝ (angle and angular velocity dθ/dt).

The phase space is a cylinder: the angle is periodic but the velocity is
not bounded.

**Example: Pendulum.** A simple pendulum of fixed length has:
- Configuration space: S¹ (the angle θ from vertical, with 0 ~ 2π).
- Phase space: S¹ × ℝ (angle and angular velocity).

A **phase portrait** is a picture of the vector field on S¹ × ℝ drawn by
Newton's law. For small amplitudes (θ near 0), the trajectories are closed
ellipses. For large amplitudes (enough energy to go over the top), the
trajectories are non-closed curves winding around the cylinder.

---

### C.2 Phase Space of the Two-Link Arm

**Configuration and velocity.** The two-link arm has configuration (θ₁, θ₂) ∈ T²
and velocity (ω₁, ω₂) = (dθ₁/dt, dθ₂/dt) ∈ ℝ². The phase space is

    Phase space = T² × ℝ²

a four-dimensional manifold. A dynamical trajectory is a path in T² × ℝ²
satisfying the arm's equations of motion (Euler–Lagrange equations).

**Compactness.** T² is compact; ℝ² is not. The phase space T² × ℝ² is
not compact. Physical constraints (motor torque limits, collision avoidance)
restrict the system to a compact subset.

**Energy surfaces.** For a conservative system (no friction, no driving),
the total energy E is constant along trajectories. Each energy level
{(θ₁, θ₂, ω₁, ω₂) : H(θ₁, θ₂, ω₁, ω₂) = E} is a three-dimensional
submanifold of the four-dimensional phase space. The topology of these level
sets changes as E varies through critical values.

---

### C.3 Compact Phase Spaces and the Torus

Some physical systems have naturally compact phase spaces.

**Particle on T².** If a particle moves on the torus T² (e.g., a particle
in a periodic lattice with periodic boundary conditions in two directions),
its configuration space is T² and its phase space is T² × T² = T⁴ if the
velocities are also periodic (which occurs in certain lattice models).

**Angle-action variables.** In integrable Hamiltonian systems, the phase
space near a stable equilibrium can be transformed into angle-action
coordinates (φ₁, φ₂, J₁, J₂) where each φᵢ ∈ S¹ and Jᵢ ∈ ℝ. For fixed
action Jᵢ = jᵢ, the trajectory lives on T² = S¹ × S¹ — the invariant torus
of the integrable system. The motion on this torus is quasi-periodic (winding
around both S¹ factors).

---

## Part D — Free Configuration Space and Obstacle Avoidance

### D.1 C-Obstacles and C_free

When obstacles are present in the workspace, not all configurations are
physically realizable. The **C-obstacle region** C_obs is the set of
configurations that place part of the robot in collision with an obstacle.

**Definition.** For a robot with configuration space C and workspace
obstacles O:

    C_obs = {q ∈ C : robot at configuration q intersects O}
    C_free = C \ C_obs

The robot can move from q_start to q_goal without collision if and only if
q_start and q_goal are in the same path-connected component of C_free.

---

### D.2 C-Obstacles for the Single-Joint Arm

**Setup.** A single-link arm of length ℓ rotates about the origin in a
workspace containing a single rectangular obstacle R.

The arm at angle θ sweeps a line segment from the origin to (ℓ cos θ, ℓ sin θ).
This segment intersects R for a range of angles θ ∈ [α, β] ⊆ [0, 2π).

**C-obstacle.** In the configuration space S¹, the C-obstacle is the arc
{e^{iθ} : θ ∈ [α, β]}, a connected closed arc of the circle.

**C_free.** C_free = S¹ \ (C-obstacle arc) is the complementary open arc.
Since S¹ minus a closed arc is homeomorphic to an open interval (0,1), C_free
is path-connected — any two free configurations can be connected by swinging
the arm through the free arc.

**Multiple obstacles.** With k non-overlapping rectangular obstacles, the
C-obstacle on S¹ is a union of k disjoint arcs. If these arcs cover all of S¹,
C_free is empty (no free configuration exists). If some arcs remain, C_free
consists of the complementary arcs. Since each connected arc of S¹ minus a
finite set of arcs is homeomorphic to an open interval, each component of C_free
is path-connected.

---

### D.3 C-Obstacles for the Two-Link Arm on T²

**Setup.** The two-link arm has configuration space T², parameterised by the
unit square [0,1]² with opposite edges identified. A single obstacle in the
workspace maps to a C-obstacle C_obs ⊆ T².

**Shape of C_obs.** For generic obstacles, C_obs is a connected region in T²
whose boundary is a curve (or collection of curves) on the torus. The topology
of C_free = T² \ C_obs depends on whether C_obs separates T²:

- **Case 1: C_obs is a topological disk** (simply connected region). Removing
  a disk from T² leaves a path-connected space (T² remains in one piece).
  Any two free configurations are reachable from each other.

- **Case 2: C_obs contains a non-contractible curve** (a curve that winds around
  one S¹ factor of T²). Removing such a region can disconnect T², creating two
  or more path components of C_free. Some arm configurations become unreachable
  from others.

- **Case 3: C_obs contains curves winding around both S¹ factors.** The free
  configuration space may fragment into many components.

**Practical consequence.** Before planning a trajectory for the two-link arm,
a motion planner must determine the path-component structure of C_free ⊆ T².
This is a topological question about a surface, and its answer governs whether
a collision-free motion from q_start to q_goal exists at all.

---

### D.4 Worked Example: Two-Link Arm with One Obstacle

**Setup.** Link 1 has length 3, Link 2 has length 2. The workspace is ℝ² with
a single circular obstacle centered at (3, 0) with radius 0.5.

**C-obstacle structure.** The tip of Link 2 lies at

    (3 cos θ₁ + 2 cos(θ₁+θ₂), 3 sin θ₁ + 2 sin(θ₁+θ₂))

The arm is in collision when any part of either link intersects the disk
B((3,0), 0.5). In configuration space T², the C-obstacle consists of the
pairs (θ₁, θ₂) for which this intersection occurs. Generically, C_obs is a
connected region bounded by smooth curves on T².

**Visualisation on the square.** Drawing T² as the unit square [0,1]² with
identified edges, C_obs appears as a blob (possibly wrapping around the edges
due to the identifications). C_free is the complement.

**Path connectivity.** If C_obs is a topological disk (simply connected and
not wrapping around any non-contractible loop in T²), then C_free = T² \ disk
is path-connected. This means any two collision-free configurations can be
reached from each other — the obstacle does not divide the arm's configuration
space.

**Pytop module link:** `pytop.connectedness`, `pytop.quotients`, `pytop.surfaces`.

---

## Part E — Summary and Design Principles

### E.1 Configuration Space Construction Principles

| System | DOF | C | Topology |
|---|---|---|---|
| Single rotational joint | 1 | S¹ | Circle |
| Two rotational joints | 2 | T² = S¹×S¹ | Torus |
| n rotational joints | n | Tⁿ | n-torus |
| Point robot in W ⊆ ℝ² | 2 | W | Planar region |
| Rotatable disk in W | 3 | W × S¹ | 3D manifold |
| Particle on S¹ + velocity | 2 | S¹ × ℝ | Cylinder |

### E.2 Key Topological Facts Used in Applications

- **Quotient construction:** periodic DOFs produce S¹ factors via the
  identification [0,1]/{0~1}.
- **Compactness:** Tⁿ is compact (finite control input suffices to reach
  any configuration); ℝⁿ factors make the phase space non-compact.
- **Path-connectedness:** Tⁿ is path-connected; C_free may not be, depending
  on the obstacle set.
- **Fundamental group:** π₁(S¹) = ℤ, π₁(Tⁿ) = ℤⁿ; homotopy classes of
  motions correspond to winding numbers around each joint.
- **Feasibility criterion:** A motion from q_start to q_goal exists iff they
  lie in the same path component of C_free.

### E.3 Cross-Reference to Other APL Files

| Topic | Covered in |
|---|---|
| Path-connected components as reachable regions | APL-03 (§B) |
| Homotopy of collision-free routes | APL-03 (§B.5) |
| Free-space point AGV model | APL-03 (§B.1–B.3) |
| Quotient space definition | APL-04 (§A) — this file |
| Torus from square identification | APL-04 (§B.3) — this file |
| Free configuration space C_free | APL-04 (§D) — this file |

---

## Cross-reference to Pilot Examples

| Pilot example (adams_franzosa_pilot_examples.md) | Expanded here |
|---|---|
| Example 7 (two-link robotic arm torus, §3.5) | §B.3, §D.3–D.4 |
| Example 6 (AGV configuration space link, §6.5) | §D.1, §D.2 |
