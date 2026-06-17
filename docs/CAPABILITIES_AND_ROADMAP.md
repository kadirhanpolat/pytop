# pytop — Capabilities, Limitations & Roadmap to Research Grade

> An honest assessment of what pytop can and cannot do today (v0.6.0), and a
> phased roadmap toward a GAP-scale research-grade topology computation system,
> starting from set-theoretic (point-set) topology.

---

## Part I — What pytop can and cannot do today (v0.6.0)

pytop has **broad topic coverage but uneven depth**. Three honest categories:

### ✅ Genuinely computational — computes a result from your input

**Finite point-set topology (the oldest, most solid core).**
Topology generation from a base/subbase; closure / interior / boundary / derived
set; continuity checks; enumeration & counting of topologies on `n` points
(incl. T0/T1/Hausdorff); finite metric spaces; relations & orders; set/family
operations; Alexandroff ↔ preorder correspondence; finite map analysis.

**v0.6.0 constructive core.**
- `homology` — Betti numbers **and torsion** from a finite simplicial complex
- `persistent_homology` — Vietoris–Rips barcodes from a finite metric space (ℤ/2)
- `knot_invariants` — Jones & Alexander polynomials from a diagram
- `winding_number` — winding number, map degree, vector-field index
- `surface_word_classification` — closed-surface type from a gluing word
- `graph_planarity` — exact planarity/genus for **small** graphs

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
  construct or analyze the actual mathematical object (no real K-theory of a C\*-algebra, etc.).
- `named_spaces`, `space_catalog`, `counterexample_atlas`, preservation tables,
  cardinal-function profiles: curated reference catalogs.

### ❌ Cannot do (real limits)

- No homology of general/infinite spaces — finite simplicial only; no singular
  homology, cohomology rings, cup products, or spectral-sequence **computation**.
- No general fundamental-group computation (van Kampen → presentation) beyond the
  surface-word genus/Euler case.
- Knots: needs a PD/Gauss code you supply; no HOMFLY/Khovanov; a documented sign
  convention quirk; no diagram extraction from a 3-D embedding.
- Planarity is exact but **small-graph only** (exponential rotation-system search,
  guarded) — not a linear-time test.
- TDA is ℤ/2 and small clouds only (unoptimized reduction).
- pi-Base inference is bounded by the vendored snapshot's vocabulary; not a general
  prover.
- No coordinate/geometric topology, mesh processing, or general homeomorphism
  decision (only finite homeomorphism by enumeration).
- Most engines are finite / brute-force — **does not scale**.

**One-sentence summary.** pytop is a solid finite point-set core + a focused
v0.6.0 computational layer + pi-Base inference, wrapped in a large educational /
reference layer. It is **not** (yet) a GUDHI / SageMath / GAP-scale research system.

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

## Part III — Roadmap

### Phase 0 — Architectural foundations (prerequisite for everything)

- **`Space` protocol** — a `typing.Protocol` defining the *computable topological
  space* interface every representation must implement (point membership; open-set
  / basic-neighborhood membership and enumeration; a declared cardinality/representation
  kind). This is the keystone: generic algorithms target the protocol, not concrete classes.
- **Witness-carrying results** — extend `Result` so predicates return
  `{decided: bool|None, witness|counterexample, decidability: enum}`. Make honesty
  about (un)decidability a type-level contract.
- **Construction closure** — `subspace`, `product`, `quotient`, `sum`, `inverse_limit`
  that consume representable spaces and produce representable spaces.

### Phase 1 — Set-theoretic topology to research grade  ⟵ **our starting point**

1. **Representations beyond finite**: cofinite/cocountable, order topology on a
   computable linear order, metric topology from an *exact/rational* metric,
   Alexandroff topology of a finitely-presented poset, subbase-generated spaces —
   all behind the `Space` protocol, all closed under Phase-0 constructions
   (Tychonoff product via subbasis is the marquee case).
2. **Generic witness-producing predicates** over the protocol, unifying today's
   finite-only and symbolic paths: separation (T0–T6, regular/normal/Tychonoff
   with Urysohn-function witnesses where decidable), compactness / Lindelöf /
   local compactness / paracompactness (subcover or refuting-net witness),
   connectedness / path-connectedness (clopen split or connecting path).
3. **Computed cardinal invariants** (weight, density, character, cellularity,
   Lindelöf number) for representable spaces — turn today's profiles into computations.
4. **Property-reasoning engine** (the bridge that ends the "encyclopedia" era):
   combine the pi-Base implication graph + **construction-preservation rules**
   (hereditary / productive / quotient-stable, already in pi-Base meta-properties)
   + computed witnesses, so the system can *derive and explain* properties of a
   **constructed** space — e.g. "X = ∏ Xᵢ; each Xᵢ is Tychonoff; Tychonoff is
   productive ⟹ X is Tychonoff." This unifies the constructive and descriptive layers.
5. **Counterexample synthesis** — given a target property combination, *construct*
   a witnessing space by searching the construction space (not just looking it up
   in the 222-space atlas).

### Phase 2 — Algebraic topology to research grade

- (Co)homology over an arbitrary PID; optimized persistence (clearing/twist,
  cohomology, Mayer–Vietoris, relative & cellular homology); cubical complexes.
- Real van Kampen on simplicial/CW 2-complexes → group presentations; Tietze /
  abelianization; optional GAP bridge for hard group problems.

### Phase 3 — Geometric & low-dimensional topology

- Full knot/link suite from diagrams (HOMFLY, Khovanov, genus bounds, links);
  3-manifolds / normal surfaces (Regina-scale — very ambitious); SnapPy interop.

### Phase 4 — Performance, correctness, interoperability

- Complexity discipline; **optional** accelerated extras (numpy/scipy) over a
  pure-Python core; property-based + differential testing against SageMath/GUDHI/GAP;
  formal verification of core routines; interop bridges so pytop orchestrates.

---

## Part IV — Hard trade-offs to decide early

- **Dependency policy.** "Research grade + scale" eventually needs fast linear
  algebra / big data structures. Recommendation: keep a **pure-Python correctness
  core** and add **optional** accelerated backends (`pytop[fast]`), never a hard
  runtime dependency.
- **Correctness bar.** Research grade demands witnesses + property-based tests +
  differential testing against established systems — a real, ongoing cost.
- **Decidability honesty.** Many point-set questions are undecidable for general
  representations. The system must say so, not fake an answer. This is a feature.
- **Scope discipline.** Don't reimplement GAP/GUDHI/SnapPy — *interoperate*. pytop's
  edge is the unified point-set core + symbolic property reasoning.

---

## Part V — Immediate next step (proposed)

**Milestone S1 — the computable-space foundation** (Phase 0 + Phase 1.1–1.2):
1. `Space` protocol + a `decidability`-aware `Result`.
2. Re-express the existing finite engine behind the protocol (no behavior change).
3. Add 2–3 infinite representations (cofinite, order topology, exact-metric).
4. One generic, witness-producing predicate end-to-end (e.g. Hausdorff) over all
   representations, with decided/semi-decidable/undecidable honesty.

This is the smallest slice that proves the architecture and immediately makes
infinite spaces first-class. Everything in Phase 1 then builds on it.
