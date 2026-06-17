# pytop — Capabilities, Limitations & Roadmap to Research Grade

> An honest assessment of what pytop can and cannot do today (post-v0.6.0), and a
> phased roadmap toward a GAP-scale research-grade topology computation system,
> starting from set-theoretic (point-set) topology.
>
> **Status as of 2026-06-18:** Phase 1 (set-theoretic topology) is substantially
> complete; Phase 2 (algebraic topology) is in progress (3 / 7 items done).

---

## Part I — What pytop can and cannot do today

pytop has **broad topic coverage but uneven depth**. Three honest categories:

### ✅ Genuinely computational — computes a result from your input

**Finite point-set topology (the oldest, most solid core).**
Topology generation from a base/subbase; closure / interior / boundary / derived
set; continuity checks; enumeration & counting of topologies on `n` points
(incl. T0/T1/Hausdorff); finite metric spaces; relations & orders; set/family
operations; Alexandroff ↔ preorder correspondence; finite map analysis.

**v0.6.0 constructive core.**
- `homology` — Betti numbers **and torsion** from a finite simplicial complex
- `homology_coefficients` — field-coefficient homology (Q, Z/p) and relative
  homology H_*(K,L; Z); demonstrates coefficient dependence (RP²: H₁(;Q)=0 vs
  H₁(;Z/2)=Z/2)
- `mayer_vietoris` — Mayer–Vietoris long exact sequence for K = A ∪ B:
  extended Smith Normal Form with transformation matrices gives explicit
  homology bases; chain-level inclusion maps + snake lemma yield
  φ, ψ, δ as integer matrices; exactness verified at every position
- `persistent_homology` — Vietoris–Rips barcodes from a finite metric space (Z/2)
- `knot_invariants` — Jones & Alexander polynomials from a diagram
- `winding_number` — winding number, map degree, vector-field index
- `surface_word_classification` — closed-surface type from a gluing word
- `graph_planarity` — exact planarity/genus for **small** graphs

**`experimental.spaces` — computable-space protocol (Phase 1, research grade).**
The research-grade point-set layer: a unified `Space` protocol for finite *and*
infinite spaces, with 16 witness-producing, decidability-honest predicates and a
property-reasoning engine. Key components:
- **16 predicates** (T0, T1, T2/Hausdorff, T3, T3.5/Tychonoff, T4, T5, T6,
  regular, normal, compact, connected, Lindelöf, separable, first/second-countable)
  — on finite spaces computed from the topology; on infinite spaces via mathematical
  certificates; honest `UNDECIDABLE` where no route applies.
- **7 representations**: `FiniteSpace`, `CofiniteSpace`, `OrderTopologySpace` (ℚ),
  `MetricTopologySpace`, `SorgenfreyLineSpace`, `DiscreteCountableSpace`,
  `OpaqueInfiniteSpace`.
- **Construction closure** — `subspace`, `product`, `sum`, `quotient` for finite
  spaces; `ProductSpace`, `SubspaceSpace`, `SumSpace`, `QuotientSpace` provenance
  wrappers for infinite spaces.
- **Property-reasoning engine** (`reasoning.py`) — derives properties of *constructed*
  spaces (including infinite ones, without enumeration) by combining construction-
  preservation theorems (subspace→hereditary, product→productive/Tychonoff,
  sum→coproduct, quotient→image-stable) with the pi-Base implication graph and
  computed/certified leaf verdicts. Returns explained `Derivation` trees.
  Counterexample synthesis via `synthesize(has=…, lacks=…)`.
- **pi-Base atlas bridge** (`pi_base_bridge.py`) — wraps any of the 222 famous
  pi-Base spaces as protocol `Space` objects whose certificates come from pi-Base's
  deduced trait matrix. Famous spaces feed directly into the reasoning engine and
  construction wrappers.
- **Cross-validation** — the preservation table is pin-tested against pi-Base
  meta-properties (hereditary/productive/sum-preserved flags) in the no-contradiction
  direction.

Headline example: the engine distinguishes ℚ² (second-countable → Lindelöf,
regular + 2nd-countable → metrizable → T4 via Urysohn) from the Sorgenfrey
plane (regular but not Lindelöf and not normal) — by preservation + pi-Base
implication, no enumeration.

**`experimental.pi_base`** — deductive property inference (closure, consistency,
counterexample search) over the pi-Base graph (243 properties, 902 theorems,
222 spaces).

### 📚 Knows but does not compute — curated / tag-based (useful, not "computation")

- Knots, fundamental groups, covering spaces, manifolds / 3-manifolds, surfaces,
  degree theory: largely **hardcoded `*Profile` registries** (known invariants
  of famous objects). They report what is known; they do not analyze *your* object.
- The "advanced" modules (`locale_theory`, `topos_theory`, `noncommutative_topology`,
  `spectral_sequences`, `higher_categories`, `operads`, `topological_field_theory`,
  `derived_categories`, `shape_theory`, `coarse_geometry`): **tag-based classifiers**.
  You supply semantic tags; they apply encoded theorems to classify. They do **not**
  construct or analyze the actual mathematical object.
- `named_spaces`, `space_catalog`, `counterexample_atlas`, preservation tables,
  cardinal-function profiles: curated reference catalogs.

### ❌ Cannot do (real limits)

- No cohomology rings or cup products; no spectral-sequence computation.
- No general fundamental-group computation (van Kampen → presentation) beyond the
  surface-word genus/Euler case. **Phase 2 target.**
- Knots: needs a PD/Gauss code you supply; no HOMFLY/Khovanov.
- Planarity is exact but **small-graph only** (exponential rotation-system search).
- TDA is Z/2 and small clouds only (unoptimized reduction).
- pi-Base inference is bounded by the vendored snapshot's vocabulary.
- No coordinate/geometric topology, mesh processing, or general homeomorphism decision.
- Most engines are finite / brute-force — **does not scale**.
- `experimental.spaces` predicates are limited to the 7 bundled representations;
  user-supplied infinite spaces can only be analyzed if they implement `certificate`.

**One-sentence summary.** pytop is a solid finite point-set core + a focused
v0.6.0+ computational layer + a research-grade point-set reasoning system +
pi-Base inference, wrapped in a large educational / reference layer. It is
**not** (yet) a GUDHI / SageMath / GAP-scale research system.

---

## Part II — Definition: what "research grade" means here

Before the roadmap, the bar we are aiming at. A research-grade topology system:

1. **Computes with infinite spaces** via *finite, computable representations*
   (a space is finite data + algorithms, not a hardcoded fact).
2. **Returns witnesses, not just verdicts** — a separating open set, a finite
   subcover, a connecting path, a refuting net — and is **honest about decidability**
   (decided / semi-decidable / undecidable / heuristic), never silently guessing.
3. **Is closed under constructions** — subspace, product (incl. Tychonoff),
   quotient, sum, (inverse) limit of representable spaces are themselves
   representable, so algorithms compose.
4. **Has algorithmic rigor** — known complexity, property-based + differential
   tests, and ideally machine-checkable correctness for core routines.
5. **Interoperates** — orchestrates best-in-class engines (GAP for groups, GUDHI
   for large TDA, SnapPy/Regina for 3-manifolds) rather than reimplementing all.

This is a **multi-year arc**, not a sprint. The roadmap below is honest about that.

---

## Part III — Roadmap & status

### Phase 0 — Architectural foundations ✅ COMPLETE

- `Space` protocol (ABC) + decidability-aware `Verdict` / `Decidability` enum.
- Witness-carrying results: `Verdict.true(witness=…)`, `Verdict.false(counterexample=…)`,
  `Verdict.undecidable(reason=…)`.
- `Construction` provenance wrappers: `ProductSpace`, `SubspaceSpace`, `SumSpace`,
  `QuotientSpace`.

### Phase 1 — Set-theoretic topology to research grade ✅ SUBSTANTIALLY COMPLETE

All five planned milestones delivered:

| Milestone | Status | Delivered |
|-----------|--------|-----------|
| S1 — Space protocol + representations | ✅ | `Space` ABC, `Verdict`, 7 representations, `is_hausdorff` with witnesses |
| S2 — 7 predicates + finite construction closure | ✅ | is_t0/t1/t2/regular/normal/compact/connected; subspace/product/sum/quotient |
| S3 — Property-reasoning engine | ✅ | `reasoning.py`: preservation + pi-Base closure + `Derivation` + `synthesize` |
| S4 — Extended axioms + representations | ✅ | is_t3/t4, Lindelöf/separable/1st-2nd-countable; Sorgenfrey + discrete-ℕ |
| S5 — Full separation hierarchy | ✅ | is_tychonoff/t5/t6; 16-property PRESERVATION table; ℚ² vs Sorgenfrey plane |

Plus: **pi-Base atlas bridge** (222 famous spaces as protocol `Space` objects;
feed into reasoning engine and construction wrappers) and **cross-validation**
(PRESERVATION table pin-tested against pi-Base meta-properties).

**Remaining Phase 1 work (incremental):**
- Computed cardinal invariants (weight, density, character, cellularity) for
  representable spaces — turn today's profiles into computations.
- More representations (Alexandroff/poset, subbase-generated, exact limit).
- T3.5 / Urysohn-function witness for infinite spaces where decidable.
- van Kampen preparation (π₁ of `experimental.spaces` objects).

### Phase 2 — Algebraic topology to research grade 🔄 STARTED

| Item | Status | Delivered |
|------|--------|-----------|
| Field-coefficient homology (Q, Z/p) | ✅ | `homology_coefficients`: Gaussian elim; RP² katsayı bağımlılığı |
| Relative homology H_*(K,L; Z) | ✅ | Disk mod boundary H₂(D²,∂D²)=Z |
| Mayer–Vietoris LES | ✅ | `mayer_vietoris`: extended SNF → explicit bases; φ,ψ,δ matrices; exactness verified (S¹,S²,interval) |
| Cellular homology | ⬜ | — |
| Cohomology + cup product | ⬜ | — |
| van Kampen → group presentations | ⬜ | Major item; GAP bridge candidate |
| Optimized persistence (clearing/twist) | ⬜ | — |
| Cubical complexes | ⬜ | — |

### Phase 3 — Geometric & low-dimensional topology ⬜ NOT STARTED

- Full knot/link suite from diagrams (HOMFLY, Khovanov, genus bounds, links);
  3-manifolds / normal surfaces (Regina-scale — very ambitious); SnapPy interop.

### Phase 4 — Performance, correctness, interoperability ⬜ NOT STARTED

- Complexity discipline; **optional** accelerated extras (numpy/scipy) over a
  pure-Python core; property-based + differential testing against SageMath/GUDHI/GAP;
  formal verification of core routines; interop bridges so pytop orchestrates.

---

## Part IV — Hard trade-offs to decide early

- **Dependency policy.** Recommendation: keep a **pure-Python correctness core** and
  add **optional** accelerated backends (`pytop[fast]`), never a hard runtime dependency.
- **Correctness bar.** Research grade demands witnesses + property-based tests +
  differential testing against established systems — a real, ongoing cost.
- **Decidability honesty.** Many point-set questions are undecidable for general
  representations. The system must say so, not fake an answer. This is a feature.
- **Scope discipline.** Don't reimplement GAP/GUDHI/SnapPy — *interoperate*. pytop's
  edge is the unified point-set core + symbolic property reasoning.

---

## Part V — Summary statistics (2026-06-19)

| Metric | Value |
|--------|-------|
| Tests passing | **9 185** |
| New PRs this arc | 14 (PR #1 → #14) |
| Representations in `experimental.spaces` | 7 |
| Predicates (with witnesses) | 16 |
| pi-Base spaces bridged | 222 |
| pi-Base properties / theorems / traits | 243 / 902 / 2 099 |
| Phase 1 milestones complete | 5 / 5 |
| Phase 2 milestones complete | 3 / 8 |
