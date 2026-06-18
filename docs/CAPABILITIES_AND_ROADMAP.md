# pytop — Capabilities, Limitations & Roadmap to Research Grade

> An honest assessment of what pytop can and cannot do today (post-v0.6.0), and a
> phased roadmap toward a GAP-scale research-grade topology computation system,
> starting from set-theoretic (point-set) topology.
>
> **Status as of 2026-06-18:** Phase 1 (set-theoretic topology) is substantially
> complete; Phase 2 (algebraic topology) is **complete** (8 / 8 items done).
> feat/mayer-vietoris merged to **master** via PR #15 (9 764 tests, 20 correctness fixes,
> ~6.6× Twist+Clearing kernel speedup).
> **Phase 3 in progress** (`feat/phase3-knot-suite`): P3.1 knot/link suite complete
> (Seifert + LinkDiagram + HOMFLY-PT + multivariable Alexander); P3.2 started —
> `dehn_surgery.py` (surgery → H₁, lens space classification) done.

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
- **10 representations**: `FiniteSpace`, `CofiniteSpace`, `OrderTopologySpace` (ℚ),
  `MetricTopologySpace`, `SorgenfreyLineSpace`, `DiscreteCountableSpace`,
  `OpaqueInfiniteSpace`, `AlexandroffSpace` (preorder → upset topology),
  `SubbaseSpace` (subbase-generated topology), `InverseLimitSpace` (finite
  inverse system + bonding maps).
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

- No spectral-sequence computation.
- Knots: needs a PD code (or braid word) you supply; HOMFLY-PT and multivariable
  Alexander are available, but there is no Khovanov homology.
- Planarity is exact but **small-graph only** (exponential rotation-system search).
- TDA is Z/2 and small clouds only (Phase 2 added Twist+Clearing optimisation, but
  still single-machine, no GPU/distributed scale).
- pi-Base inference is bounded by the vendored snapshot's vocabulary.
- No coordinate/geometric topology, mesh processing, or general homeomorphism decision.
- Most engines are finite / brute-force — **does not scale**.
- `experimental.spaces` predicates are limited to the 10 bundled representations;
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
| S1 — Space protocol + representations | ✅ | `Space` ABC, `Verdict`, 10 representations (7 original + Alexandroff + Subbase + InverseLimit), `is_hausdorff` with witnesses |
| S2 — 7 predicates + finite construction closure | ✅ | is_t0/t1/t2/regular/normal/compact/connected; subspace/product/sum/quotient |
| S3 — Property-reasoning engine | ✅ | `reasoning.py`: preservation + pi-Base closure + `Derivation` + `synthesize` |
| S4 — Extended axioms + representations | ✅ | is_t3/t4, Lindelöf/separable/1st-2nd-countable; Sorgenfrey + discrete-ℕ |
| S5 — Full separation hierarchy | ✅ | is_tychonoff/t5/t6; 16-property PRESERVATION table; ℚ² vs Sorgenfrey plane |

Plus: **pi-Base atlas bridge** (222 famous spaces as protocol `Space` objects;
feed into reasoning engine and construction wrappers) and **cross-validation**
(PRESERVATION table pin-tested against pi-Base meta-properties).

**Remaining Phase 1 work (incremental):**
- ~~Computed cardinal invariants (weight, density, character, cellularity)~~ ✅
  `cardinal_invariants.py`: exact computation for finite spaces; `cardinal_certificate`
  hook on each infinite representation; `CardinalValue` type in `core.py`.
- ~~More representations (Alexandroff/poset, subbase-generated, exact limit)~~ ✅
  `AlexandroffSpace` (preorder → Alexandroff topology via upsets),
  `SubbaseSpace` (subbase → finite intersections → topology),
  `InverseLimitSpace` (finite inverse system + bonding maps → explicit limit).
- ~~T3.5 / Urysohn-function witness for infinite spaces where decidable~~ ✅
  `urysohn.py`: `UrysohnWitness` + `urysohn_function(space, x₀, C)`;
  discrete finite spaces → exact indicator; MetricTopologySpace → distance-ratio formula;
  `is_tychonoff` now carries a witness dict for finite T1 and metric spaces.
- ~~van Kampen preparation (π₁ of `experimental.spaces` objects)~~ ✅
  `pi1.py`: `pi1_space(space) → Pi1Result` via McCord order complex
  (specialization order → CW1Complex → spanning-tree algorithm);
  T0 quotient for non-T0 inputs; `ProductSpace` → π₁(A) × π₁(B);
  `SumSpace` → π₁ of first component. Diamond poset verified = ℤ (minimal model of S¹).

### Phase 2 — Algebraic topology to research grade ✅ COMPLETE

| Item | Status | Delivered |
|------|--------|-----------|
| Field-coefficient homology (Q, Z/p) | ✅ | `homology_coefficients`: Gaussian elim; RP² katsayı bağımlılığı |
| Relative homology H_*(K,L; Z) | ✅ | Disk mod boundary H₂(D²,∂D²)=Z |
| Mayer–Vietoris LES | ✅ | `mayer_vietoris`: extended SNF → explicit bases; φ,ψ,δ matrices; exactness verified (S¹,S²,interval) |
| Cellular homology | ✅ | `cellular_homology`: CWComplex + SNF; standard spaces (S^n, RP^n, CP^n, T², Klein, L(p,q), M(Z/n,k)); cross-validated via `cw_from_simplicial` |
| Cohomology + cup product | ✅ | `cohomology`: δ^k=(∂_{k+1})^T via extended SNF; UCT verified; Alexander-Whitney cup product; `CohomologyRing` with graded-commutativity; torus H^1⊗H^1→H^2 non-degenerate |
| van Kampen → group presentations | ✅ | `van_kampen`: GroupPresentation + GroupHomomorphism; amalgamated free product; Tietze elimination; abelianization via SNF; group identification; CW1Complex route (spanning tree → π₁); standard spaces (S¹∨⋯∨S¹→Fₙ, S²→1, T²→ℤ², Klein→⟨a,b\|abab⁻¹⟩, RP²→ℤ/2) |
| Optimized persistence (clearing/twist) | ✅ | `persistent_homology_optimized`: Twist algorithm (Chen–Kerber 2011) + Clearing Lemma; dimension-top-down sweep; `ReductionStats` (n_cleared, clearing_ratio, n_column_additions); cross-validated against standard reduction |
| Cubical complexes | ✅ | `cubical_homology`: `CubicalComplex` (face-closure, boundary ℤ-matrix, SNF homology); standard spaces S¹/D²/interval; `CubicalFiltration` + `bitmap_to_cubical_filtration` (lower-star from 2-D pixel array); `persistence_pairs_cubical` + `persistent_homology_bitmap` via shared Twist+Clearing kernel |

### Phase 3 — Geometric & low-dimensional topology 🔄 IN PROGRESS

**P3.1 — Knot/Link suite (pure Python): ✅ COMPLETE**

| Item | Status | Delivered |
|------|--------|-----------|
| Seifert algorithm | ✅ | `seifert.py`: `seifert_circles`, `seifert_genus_bound`, `seifert_matrix`, `signature` (LDLT); unknot=0, trefoil=1, figure-8=1 verified |
| Link invariants | ✅ | `knot_invariants.py`: `LinkDiagram`, `linking_number`, `linking_matrix`; Hopf link linking_number=±1 verified |
| HOMFLY-PT polynomial | ✅ | `homfly.py`: `homfly_polynomial(braid_word, n)` via skein recursion `a·P(L₊)−a⁻¹·P(L₋)=z·P(L₀)`; descending-defect termination; `Laurent2` (2-var Laurent); known values (trefoil −a⁻⁴+2a⁻²+a⁻²z², fig-8 a²−1+a⁻²−z², Hopf, unlinks) + Markov(±)/conjugation invariance + Jones/Alexander specialisation differential |
| Multivariable Alexander | ✅ | `multivariable_alexander.py`: `multivariable_alexander(link)` from a `LinkDiagram` via Wirtinger presentation (arcs + intrinsic orientation by component tracing) + Fox calculus over the n-variable Laurent ring; `(c−1)`-minor det `÷ (t_γ−1)`. Verified: knots → braid Alexander (trefoil, fig-8); Hopf → 1; `(2,2k)` torus → `Σ(t₁t₂)ⁱ` (Torres condition + interchange symmetry); split → 0 |

**P3.2 — 3-manifold basics: 🔄 IN PROGRESS**
- `dehn_surgery.py` — rational surgery coefficients: ✅ `first_homology_of_surgery`
  (cokernel of ``A_{ii}=pᵢ, A_{ij}=qᵢ·lk_{ij}`` via Smith normal form);
  `first_homology_of_link_surgery` (linking numbers from a `LinkDiagram`);
  `lens_space_first_homology` + lens space homeomorphism/homotopy classification.
  Verified: lens spaces ℤ/p, S¹×S² (0-surgery), T³ (0-surgery on Borromean rings),
  Poincaré homology sphere (E₈ plumbing), L(7,1)≃L(7,2) ≇.
- `experimental/snappy_bridge.py` — SnapPy optional bridge: ⬜ not started

**P3.3 — Advanced (long-term):**
- `khovanov.py` — cube-of-resolutions → graded complex → SNF: ⬜ not started
- Normal surfaces (Regina-scale): out of scope for pure-Python pytop

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

## Part V — Summary statistics (2026-06-18)

| Metric | Value |
|--------|-------|
| Tests passing | **9 896** |
| Representations in `experimental.spaces` | 10 |
| Predicates (with witnesses) | 16 |
| pi-Base spaces bridged | 222 |
| pi-Base properties / theorems / traits | 243 / 902 / 2 099 |
| Phase 1 milestones complete | 5 / 5 |
| Phase 2 milestones complete | 8 / 8 ✅ |

### Phase 2 post-completion fixes & optimizations (2026-06-18)

**Correctness (20 bugs fixed):**
- 5 HIGH: `is_hausdorff` certificate bypass; `_close_under_unions` deduplication;
  `_provable_true_props` recursion guard; `_product_pi1` silent exception;
  Mayer–Vietoris torsion-aware exactness (`val % d == 0`).
- 15 MEDIUM: `OrderTopologySpace` midpoint formula; `AlexandroffSpace` union-find
  refactor; `SorgenfreyLineSpace` counterexample witness; `QuotientSpace.contains`
  raises `NotImplementedError`; `DiscreteCountableSpace` Urysohn support;
  `_bfs_urysohn` dead-code; `homology_coefficients` prime-modulus validation;
  `relative_homology` double boundary matrix; `_induced_on_hk` shape for empty target;
  `mayer_vietoris` off-by-one boundary; `CohomologyRing.verify_graded_commutativity()`;
  torus `group_type` → `"free_abelian_rank_2"`; `cw_complex_pi1` disconnected-skeleton
  guard; cubical OOM docstring warnings.

**Performance (Phase 4 preview):**
- `_snf_ext(compute_transforms=False)` — skips P/Pinv/Q/Qinv when only D is needed
  (~80% inner-loop saving); `_mat_rank` now uses this path.
- `_twist_reduce` bigint bitmask — `list[set[int]]` → `list[int]` Python bigint;
  `col.bit_length()-1` pivot (C-level intrinsic); **~6.6× kernel speedup**;
  applied to both `persistent_homology_optimized` and `cubical_homology`.
