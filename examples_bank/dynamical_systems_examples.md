# Dynamical Systems Examples (DYN-03)

- Source: `AdamsFranzosa2008Topology`
- Sections: §8.1–8.5 (Dynamical Systems, Orbits, Fixed Points, Chaos, Symbolic Dynamics)
- Version introduced: `v0.2.102`
- Route: `DYN-03`
- Rule: Original package explanations only. Book sections guide topic selection and
  fact verification; no problem statements or extended prose are copied verbatim.

---

## Part A — Dynamical Systems: Setup and Orbits

### A.1 Definition of a Dynamical System

**Definition.** A **topological dynamical system** is a pair (X, f) where X is
a topological space and f : X → X is a continuous function. The function f is
the **dynamics**; applying f once represents one time step. Iterates are defined
by f⁰ = id_X and fⁿ = f ∘ fⁿ⁻¹ for n ≥ 1.

**Examples of dynamical systems.**

| System | X | f |
|---|---|---|
| Angle doubling | S¹ | d(θ) = 2θ mod 2π |
| Logistic map | [0,1] | f_r(x) = rx(1−x) |
| Tent map | [0,1] | T(x) = 2x or 2(1−x) |
| Shift map | {0,1}^ℕ | σ(s₁s₂…) = s₂s₃… |
| Rotation | S¹ | R_α(θ) = θ + α mod 2π |
| Identity | Any X | id(x) = x |

**Why topology?** Continuity of f is essential: it ensures that nearby initial
conditions have nearby short-term orbits (though not necessarily long-term ones,
as chaos shows). The topological structure of X determines what orbits are possible.

---

### A.2 Orbits and Their Classification

**Definition.** The **orbit** of a point x ∈ X under f is the sequence

    Orb(x) = {x, f(x), f²(x), f³(x), ...}

or equivalently the set {fⁿ(x) : n ≥ 0}.

**Four orbit types.**

**Type 1: Fixed point.** fⁿ(x) = x for all n ≥ 0 (trivially, since f(x) = x).
The orbit is the singleton {x}.

**Type 2: Periodic orbit of period p.** fᵖ(x) = x for some p ≥ 2, and p is
the minimal such integer. The orbit is the finite cycle {x, f(x), ..., fᵖ⁻¹(x)}
of exactly p distinct points.

**Type 3: Eventually periodic orbit.** There exist m ≥ 1 and p ≥ 1 such that
fᵐ⁺ᵖ(x) = fᵐ(x), but x is not itself periodic. The orbit enters a periodic cycle
after m transient steps. The preperiod is m and the period is p.

**Type 4: Infinite aperiodic orbit.** fⁿ(x) ≠ x for all n ≥ 1, and the orbit
{fⁿ(x) : n ≥ 0} is an infinite set of distinct points. This is the generic case
for chaotic systems.

**Example: Logistic map f₂(x) = 2x(1−x).**
- Fixed points: f₂(x) = x ⟹ 2x−2x² = x ⟹ x(1−2x) = 0 ⟹ x = 0 or x = 1/2.
- x = 0 is unstable (repelling); x = 1/2 is attracting.
- Every orbit in (0,1) converges to x = 1/2: eventually periodic with period 1.

---

### A.3 The Orbit as a Topological Object

The closure of an orbit, Cl(Orb(x)), is a topologically significant object.

- For a fixed point: Cl(Orb(x)) = {x}, a singleton.
- For a periodic orbit: Cl(Orb(x)) = Orb(x), a finite set.
- For an irrational rotation R_α on S¹: Cl(Orb(x)) = S¹ (the orbit is dense
  in S¹). Every orbit is dense, yet none is periodic.
- For the doubling map: some orbits are dense (irrational angles), some are
  periodic (rational angles with odd denominators).

**Minimal systems.** A dynamical system (X, f) is **minimal** if every orbit
is dense in X. Irrational rotations on S¹ are minimal; the logistic map at r=4
is not minimal (fixed points have non-dense orbits).

**Pytop module link:** `pytop.dynamical_systems`.

---

## Part B — Fixed Points and Stability

### B.1 Fixed Points

**Definition.** A point x₀ ∈ X is a **fixed point** of f if f(x₀) = x₀.
The set of all fixed points is Fix(f) = {x ∈ X : f(x) = x}.

**Characterisation.** Fix(f) is the intersection of the graph of f with the
diagonal in X × X. For continuous f on a metric space, Fix(f) is a closed set
(it is the preimage of the closed set {0} under the continuous map x ↦ d(x, f(x))).

**Finding fixed points: algebraic method.**
For f : ℝ → ℝ, fixed points satisfy f(x) = x. For example:
- f(x) = x³: f(x) = x ⟹ x³ = x ⟹ x(x²−1) = 0 ⟹ Fix(f) = {−1, 0, 1}.
- f(x) = cos(x): f(x) = x has exactly one solution x* ≈ 0.739 (Banach fixed point).

**Periodic points.** A point x is **periodic of period p** if fᵖ(x) = x and p is
minimal. The set Per_p(f) = Fix(fᵖ) \ ⋃_{k|p, k<p} Fix(fᵏ) consists of all points
with exact minimal period p.

---

### B.2 Stability of Fixed Points

**Definition.** A fixed point x₀ of f : (X,d) → (X,d) is:

- **Attracting (Liapunov stable + asymptotically stable):** there exists ε > 0 such
  that d(x, x₀) < ε ⟹ fⁿ(x) → x₀ as n → ∞.
- **Repelling:** there exists ε > 0 such that for all x ≠ x₀ with d(x, x₀) < ε,
  there exists n with d(fⁿ(x), x₀) ≥ ε.
- **Neutral (indifferent):** nearby orbits neither converge to nor diverge from x₀.

**One-dimensional test (derivative criterion for f : ℝ → ℝ smooth).**
If f is differentiable at a fixed point x₀:
- |f'(x₀)| < 1 ⟹ x₀ is attracting.
- |f'(x₀)| > 1 ⟹ x₀ is repelling.
- |f'(x₀)| = 1 ⟹ inconclusive (neutral or weakly attracting/repelling).

**Example: Logistic map f_r(x) = rx(1−x).**
Fixed points: x = 0 and x* = (r−1)/r (for r > 1).
- f_r'(x) = r(1−2x).
- At x = 0: f_r'(0) = r. Attracting iff r < 1; repelling iff r > 1.
- At x*: f_r'(x*) = 2−r. Attracting iff |2−r| < 1 iff 1 < r < 3; repelling iff r > 3.

---

### B.3 The Brouwer Fixed-Point Theorem

**Theorem (Brouwer, special case).** Every continuous function f : D² → D² has at
least one fixed point, where D² = {(x,y) ∈ ℝ² : x²+y² ≤ 1} is the closed unit disk.

**Topological significance.** The theorem is purely topological: it holds for any
space homeomorphic to D². The proof uses the fact that D² is not homeomorphic to
S¹ (no retraction of D² onto its boundary exists — the no-retraction theorem).

**Applications.** Any continuous stirring of a cup of coffee leaves at least one
point in its original position. Any continuous map of a geographic region to itself
(e.g., a map on a table overlying the region it depicts) has a fixed point.

**Adams & Franzosa coverage.** §9–10 prove the Brouwer theorem via degree theory;
§8.2 introduces it as a motivating example for the importance of topological
fixed-point theory in applied mathematics.

**Pytop module link:** `pytop.dynamical_systems` (FixedPointProfile: brouwer_fixed_point).

---

## Part C — Chaos

### C.1 Devaney's Definition of Chaos

A continuous map f : X → X on a metric space X is **chaotic** (in the sense of
Devaney, as presented in Adams & Franzosa §8.3) if it satisfies all three:

1. **Sensitive dependence on initial conditions:** there exists δ > 0 such that
   for every x ∈ X and every neighbourhood U of x, there exists y ∈ U and n ≥ 0
   with d(fⁿ(x), fⁿ(y)) > δ.

2. **Topological transitivity:** for every pair of non-empty open sets U, V ⊆ X,
   there exists n ≥ 0 such that fⁿ(U) ∩ V ≠ ∅.

3. **Dense periodic orbits:** Per(f) = ⋃_{p≥1} Fix(fᵖ) is dense in X.

**Remark.** It is a theorem that (2) and (3) together imply (1) for metric spaces
with no isolated points. So sensitive dependence is in a sense automatic once the
other two conditions hold.

**Why all three?** The irrational rotation R_α on S¹ satisfies (2) (every orbit
is dense, so transitivity holds) but NOT (1) (R_α is an isometry, d(Rⁿ_α(x), Rⁿ_α(y)) = d(x,y))
and NOT (3) (no periodic orbits at all). Transitivity alone is not chaos.

---

### C.2 The Tent Map: A Complete Analysis

**Definition.** The tent map T : [0,1] → [0,1] is

    T(x) = 2x        for 0 ≤ x ≤ 1/2
    T(x) = 2(1−x)   for 1/2 < x ≤ 1

**Fixed points.** T(x) = x ⟹ x = 0 or x = 2/3. Two fixed points.

**Period-2 points.** T²(x) = x but T(x) ≠ x.
T maps [0,1/2] linearly onto [0,1] with slope 2, and [1/2,1] onto [0,1] with slope −2.
T² is piecewise linear with slope ±4. Fixed points of T² beyond those of T:
x = 2/5 and x = 4/5 form a 2-cycle: T(2/5) = 4/5, T(4/5) = 2/5.

**Sensitive dependence.** For any two distinct points x ≠ y with |x−y| < ε,
after at most n ≈ log₂(1/ε) iterates, their images are distance ≥ 1/2 apart.
(Each iterate multiplies the distance by 2, until it exceeds 1/2.) So δ = 1/2
witnesses sensitive dependence.

**Dense periodic points.** All dyadic rationals k/2ⁿ are eventually periodic under T.
More precisely, every rational with denominator a power of 2 times an odd number
is periodic or preperiodic. The periodic points are dense in [0,1].

**Topological transitivity.** For any two non-empty open intervals (a,b) and (c,d)
in [0,1], there exists n such that Tⁿ(a,b) ⊇ (c,d). (The image of any non-trivial
interval expands by factor 2 per step until it covers all of [0,1].)

**Conclusion.** T is chaotic. Topological entropy h(T) = log 2.

---

### C.3 The Logistic Map

**Family.** The logistic map f_r : [0,1] → [0,1] is f_r(x) = rx(1−x) for r ∈ (0,4].

**Route to chaos (period-doubling cascade).**

| Parameter range | Behaviour |
|---|---|
| 0 < r < 1 | Unique attracting fixed point x = 0; all orbits → 0 |
| 1 < r < 3 | Attracting fixed point x* = (r−1)/r |
| r = 3 | First bifurcation: x* loses stability |
| 3 < r < 3.449... | Attracting 2-cycle |
| 3.449... < r < 3.544... | Attracting 4-cycle |
| 3.544... < r < 3.5644... | Attracting 8-cycle |
| ... | Period-doubling continues |
| r = r∞ ≈ 3.5699... | Onset of chaos (Feigenbaum point) |
| r∞ < r ≤ 4 | Chaotic behaviour (with periodic windows) |
| r = 4 | Fully chaotic; conjugate to tent map |

**Feigenbaum universality.** The ratios of successive bifurcation parameter values
converge to the **Feigenbaum constant** δ ≈ 4.6692..., which is the same for all
smooth unimodal maps. This universality is a remarkable topological/analytic fact.

**Conjugacy at r = 4.** The map f₄(x) = 4x(1−x) is topologically conjugate to
the tent map T via h(x) = sin²(πx/2):

    h ∘ T = f₄ ∘ h

Since h is a homeomorphism [0,1] → [0,1] and the conjugacy intertwines the dynamics,
f₄ is chaotic (it has the same orbit structure as T up to homeomorphism).

**Pytop module link:** `pytop.chaos_profiles`.

---

## Part D — Topological Conjugacy

### D.1 Definition and Basic Properties

**Definition.** Two dynamical systems (X, f) and (Y, g) are **topologically
conjugate** if there exists a homeomorphism h : X → Y such that

    h ∘ f = g ∘ h   (equivalently, g = h ∘ f ∘ h⁻¹)

The homeomorphism h is called a **conjugacy**. Topological conjugacy is the natural
notion of isomorphism for dynamical systems: it says that (X, f) and (Y, g) are
"the same dynamical system, written in different coordinates."

**Conjugacy invariants.** Any property that is preserved under homeomorphism and
respects the dynamics is a **conjugacy invariant**:

- Number of fixed points (and their stability type).
- Set of periods of periodic orbits.
- Topological entropy h(f) (= h(g) when h ∘ f = g ∘ h).
- Transitivity, minimality, chaos (all three Devaney properties).

**Non-example.** The map f : {1,2,3} → {1,2,3} with f(1)=1, f(2)=2, f(3)=3 (3 fixed
points) is NOT conjugate to g : {1,2,3} → {1,2,3} with g(1)=1, g(2)=3, g(3)=2 (1
fixed point, one 2-cycle). Any conjugacy h must map fixed points of f to fixed points
of g bijectively, but |Fix(f)| = 3 ≠ 1 = |Fix(g)|.

---

### D.2 Symbolic Dynamics and the Shift Map

**Setup.** Let Σ = {0,1}^ℕ be the space of one-sided binary sequences
s = (s₁, s₂, s₃, ...) with sᵢ ∈ {0,1}. Equip Σ with the product topology
(or equivalently the metric d(s,t) = Σ_{n≥1} |sₙ−tₙ|/2ⁿ).

**The shift map.** σ : Σ → Σ is defined by σ(s₁s₂s₃...) = s₂s₃s₄...: it
discards the first symbol. σ is continuous and surjective but not injective.

**Properties of (Σ, σ).**
- Periodic points: sequences with periodic tails. Dense in Σ.
- Topological transitivity: a sequence containing every finite block as a subword
  (a de Bruijn sequence) has a dense orbit.
- Sensitive dependence: two sequences differing at position n are distance ≤ 1/2ⁿ
  apart, but after n steps they differ in the first symbol (distance ≥ 1).

**Conclusion.** (Σ, σ) is chaotic. h(σ) = log 2.

**Semi-conjugacy to the tent map.** Define h : [0,1] → Σ by
h(x)ₙ = 0 if Tⁿ⁻¹(x) ≤ 1/2, else 1 (the itinerary of x). Then h ∘ T = σ ∘ h.
This semi-conjugacy (h is continuous and surjective but 2-to-1 on dyadic rationals)
shows that the tent map is a "quotient" of the shift, and inherits the shift's chaos.

---

### D.3 Summary: Orbit Structure Comparison

| System | Fixed pts | Periodic pts | Dense orbit? | Chaotic? | Entropy |
|---|---|---|---|---|---|
| Identity on [0,1] | All points | All points | No | No | 0 |
| Rotation R_α, α irrational | None | None | Yes (every orbit) | No | 0 |
| Rotation R_{p/q}, α=p/q | None | All | No | No | 0 |
| Logistic f_r, r < 3 | 2 | None | No | No | 0 |
| Tent map T | 2 | Dense | Yes | Yes | log 2 |
| Logistic f₄ | 2 | Dense | Yes | Yes | log 2 |
| Shift σ on {0,1}^ℕ | Const. seqs | Dense | Yes | Yes | log 2 |
| Doubling map d on S¹ | 1 (θ=0) | Dense | Yes | Yes | log 2 |

---

## Cross-reference to Profile Modules

| Concept | Pytop module | Profile class |
|---|---|---|
| Orbit types (fixed/periodic/etc.) | `pytop.dynamical_systems` | `OrbitProfile` |
| Fixed-point stability | `pytop.dynamical_systems` | `FixedPointProfile` |
| Topological conjugacy | `pytop.dynamical_systems` | `TopologicalConjugacyProfile` |
| Devaney chaos ingredients | `pytop.chaos_profiles` | `ChaosProperty` |
| Tent / logistic / shift map | `pytop.chaos_profiles` | `ChaoticMapProfile` |
| Symbolic dynamics / SFT | `pytop.chaos_profiles` | `SymbolicDynamicsProfile` |
