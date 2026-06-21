# pytop — Capabilities, Limitations & Roadmap to Research Grade

> An honest assessment of what pytop can and cannot do today (post-v0.6.0), and a
> phased roadmap toward a GAP-scale research-grade topology computation system,
> starting from set-theoretic (point-set) topology.
>
> **Status as of 2026-06-21:** Phase 1 (set-theoretic topology) substantially
> complete; Phase 2 (algebraic topology) **complete** (8 / 8).
> **Phase 3 complete** and merged to **master** via PR #16 (released as **v0.8.0**):
> P3.1 knot/link suite (Seifert + LinkDiagram + HOMFLY-PT + multivariable Alexander),
> P3.2 `dehn_surgery.py` (surgery → H₁, lens space classification), P3.3
> `khovanov.py` (Khovanov homology with torsion). The optional SnapPy bridge (P3.2)
> and Regina-scale normal surfaces (P3.3) remain out of scope / deferred.
> **Phase 4 complete** (P4.1–P4.8; latest release **v0.9.7**): property-based
> testing, an exact-linalg core, complexity discipline, **seven** external
> differential oracles (sympy, networkx, numpy, python-flint, GUDHI, plus
> Docker-based SageMath/GAP and SnapPy), and an optional flint-accelerated SNF
> backend. Since v0.9.3 the CI runs ruff + **(blocking) mypy** + pytest on Python
> 3.11/3.12/3.13, and as of **v0.9.4** `src/pytop` is mypy-clean (361 → 0).
> **v0.9.5** added a measured performance pass (planarity Euler edge-bound +
> genus-0 early termination, Khovanov per-bidegree SNF memoisation; persistence
> profiled and left unchanged). **Phases 5–6 complete** (TDA pipeline, v1.0.0–v1.0.3):
> discrete Morse theory, persistence distances/landscapes, Mapper, Čech complex,
> persistence over Z/p, TDA pipeline builder.
> **Phase 7 complete** (combinatorial topology, **v1.0.5**): P7.1 standard triangulations
> (torus/Klein bottle/RP²), P7.2 simplicial maps + induced homomorphisms, P7.3 nerve
> complex + Čech nerve, P7.4 spectral sequences (E^r pages → E^∞ convergence), P7.5
> surgery theory (handle attachment, trace cobordism), P7.6 Morse complex (gradient
> V-path counting, Morse boundary operator, Morse homology theorem cross-validated).
> **153 new tests; 9 959 core tests passing.**
> **Formal verification** (`formal/`): Lean 4 + Mathlib v4.31 proofs for SNF (0 sorry),
> set topology — 34 theorems (T₀–T₄, closure/interior duality, compactness, diagonal
> characterisation; 0 sorry) + **24 alternative proofs** in 5 strategies (by contradiction,
> contrapositive, direct, interior-closure duality, simp-heavy; `SetTopologyAltProofs.lean`),
> and metric topology (ε-δ ↔ topological continuity, Cauchy, Banach fixed-point).

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
- Knots: needs a PD code (or braid word) you supply; HOMFLY-PT, multivariable
  Alexander, and Khovanov homology are available, but everything is small-diagram
  scale (the Khovanov complex is exponential in the crossing number).
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

### Phase 3 — Geometric & low-dimensional topology ✅ COMPLETE

> P3.1 (knot/link suite), P3.2 (`dehn_surgery`), and P3.3 (`khovanov`) all delivered.
> The only unstarted items are explicitly out of scope for pure-Python pytop: an
> *in-process* SnapPy bridge (P3.2 — superseded by the P4.8 Docker oracle) and
> Regina-scale normal surfaces (P3.3).

**P3.1 — Knot/Link suite (pure Python): ✅ COMPLETE**

| Item | Status | Delivered |
|------|--------|-----------|
| Seifert algorithm | ✅ | `seifert.py`: `seifert_circles`, `seifert_genus_bound`, `seifert_matrix`, `signature` (LDLT); unknot=0, trefoil=1, figure-8=1 verified |
| Link invariants | ✅ | `knot_invariants.py`: `LinkDiagram`, `linking_number`, `linking_matrix`; Hopf link linking_number=±1 verified |
| HOMFLY-PT polynomial | ✅ | `homfly.py`: `homfly_polynomial(braid_word, n)` via skein recursion `a·P(L₊)−a⁻¹·P(L₋)=z·P(L₀)`; descending-defect termination; `Laurent2` (2-var Laurent); known values (trefoil −a⁻⁴+2a⁻²+a⁻²z², fig-8 a²−1+a⁻²−z², Hopf, unlinks) + Markov(±)/conjugation invariance + Jones/Alexander specialisation differential |
| Multivariable Alexander | ✅ | `multivariable_alexander.py`: `multivariable_alexander(link)` from a `LinkDiagram` via Wirtinger presentation (arcs + intrinsic orientation by component tracing) + Fox calculus over the n-variable Laurent ring; `(c−1)`-minor det `÷ (t_γ−1)`. Verified: knots → braid Alexander (trefoil, fig-8); Hopf → 1; `(2,2k)` torus → `Σ(t₁t₂)ⁱ` (Torres condition + interchange symmetry); split → 0 |

**P3.2 — 3-manifold basics: ✅ COMPLETE** (in-process SnapPy bridge deferred — see P4.8 Docker oracle)
- `dehn_surgery.py` — rational surgery coefficients: ✅ `first_homology_of_surgery`
  (cokernel of ``A_{ii}=pᵢ, A_{ij}=qᵢ·lk_{ij}`` via Smith normal form);
  `first_homology_of_link_surgery` (linking numbers from a `LinkDiagram`);
  `lens_space_first_homology` + lens space homeomorphism/homotopy classification.
  Verified: lens spaces ℤ/p, S¹×S² (0-surgery), T³ (0-surgery on Borromean rings),
  Poincaré homology sphere (E₈ plumbing), L(7,1)≃L(7,2) ≇.
- `experimental/snappy_bridge.py` — in-process SnapPy bridge: ⬜ deferred
  (superseded by the **P4.8** Docker-based SnapPy oracle, which validates
  `dehn_surgery` without an in-process dependency)

**P3.3 — Advanced (long-term):**
- `khovanov.py` — cube-of-resolutions → graded complex → SNF: ✅
  `khovanov_homology(diagram)` builds the Khovanov cochain complex (Frobenius
  algebra ``V = ℤ⟨1,X⟩`` with ``m``/``Δ``, Khovanov sign) and reduces each
  quantum grading over ℤ via SNF → free ranks **and torsion**. Verified:
  ``d²=0``; integral groups for unknot, trefoil (ℤ/2 at ``(−2,−7)``), figure-8
  (ℤ/2 at ``(−1,−3)``, ``(2,3)``), Hopf link; graded Euler characteristic =
  unnormalised Jones (cross-checked against `jones_polynomial`).
- Normal surfaces (Regina-scale): out of scope for pure-Python pytop

### Phase 4 — Performance, correctness, interoperability ✅ COMPLETE

- **P4.1 — Property-based + cross-engine differential testing** ✅
  (`tests/core/test_property_invariants.py`): seeded, reproducible checks of
  mathematical invariants and engine consistency over many random inputs —
  Euler–Poincaré (`χ` via homology = `χ` via face counts); rational Betti =
  integral free rank; `b_i(ℤ/p) ≥ b_i(ℚ)`; HOMFLY-PT Markov (±) and conjugation
  invariance; braid Alexander palindromy for knots; HOMFLY-PT `a=1` = Burau
  Alexander (two independent engines); Dehn-surgery `|H₁| = |det|` (cross-checked
  with an independent fraction-free Bareiss determinant); lens-space
  homeomorphic ⇒ homotopy-equivalent.
- **P4.2 — Exact integer linear algebra core** ✅ (`exact_linalg.py`):
  consolidates the Smith-normal-form / rank / determinant / cokernel primitives
  behind one public, tested module — `smith_normal_form`, `integer_rank`,
  `integer_determinant` (fraction-free **Bareiss**), `cokernel` → `AbelianGroup`.
  The Bareiss determinant and the SNF invariant factors are cross-checked
  (``det = ± ∏ dᵢ`` at full rank); `dehn_surgery` shares this core (DRY).
- **P4.3 — Complexity discipline** ✅ (`docs/COMPLEXITY.md`): an honest reference
  of the asymptotic cost and *practical input limits* of every computational
  engine (Jones/HOMFLY/Khovanov/multivariable Alexander, homology/persistence,
  Smith normal form/determinant, exact genus/planarity), with `Complexity`
  notes added to the engine docstrings. States plainly where exactness costs
  exponential time so callers are never surprised.
- **P4.4 — Differential testing against independent oracles** ✅
  (`tests/core/test_external_oracles.py`): pins `exact_linalg` (Smith normal
  form / determinant / rank) against **sympy**, `is_planar` against **networkx**
  (Boyer–Myrvold), and the Sturm/Sylvester `signature` against **numpy**
  eigenvalues — genuinely independent implementations, so a shared-code bug
  cannot hide. Test-only (the `oracles` optional extra); the runtime stays
  dependency-free and each block skips when its oracle is absent.
- **P4.5 — Persistence & exact oracles (GUDHI, python-flint)** ✅
  (`tests/core/test_external_oracles.py`): pytop's Vietoris–Rips persistence is
  validated against **GUDHI** (the gold-standard TDA library) — barcodes agree
  to floating tolerance — and `exact_linalg` against **python-flint**
  (`fmpz_mat`) as a second independent exact route, alongside sympy.
- **P4.6 — Optional accelerated exact backend (python-flint)** ✅: the integer
  Smith normal form (`homology._smith_normal_form`) — hence every homology /
  cohomology / cellular / Khovanov / surgery engine built on it — is routed to
  FLINT above a small size threshold when installed (`pip install -e .[fast]`),
  with the pure-Python routine the default fallback and only hard requirement.
  Identical results (pinned by the oracle tests); even on pytop's *sparse*
  boundary / Khovanov matrices FLINT's exact SNF is ~5–8× faster (measured on
  16×20 … 40×50 matrices). `numpy`/`scipy` are floating-point and cannot
  accelerate the exact core — only a fast exact library (FLINT) can.
- **P4.7 — SageMath oracle (knot polynomials + GAP group theory)** ✅
  (`tests/core/test_sage_oracle.py`; opt-in `PYTOP_SAGE_ORACLE=1`, Docker-based):
  one batched run of the `sagemath/sagemath` image validates pytop's Alexander
  and Jones polynomials against Sage's independent algorithms, and its van Kampen
  abelianisations against **GAP** (Klein bottle ℤ⊕ℤ/2, torus ℤ², ℝP² ℤ/2, wedge
  ℤ³). Sage cannot run natively here, so it is a subprocess oracle; opt-in keeps
  it out of the default suite.
- **P4.8 — SnapPy oracle (3-manifold Dehn-surgery homology)** ✅
  (`tests/core/test_snappy_oracle.py`; opt-in `PYTOP_SNAPPY_ORACLE=1`,
  Docker-based): SnapPy is the gold-standard 3-manifold software and the one
  independent oracle for `dehn_surgery`, which no other oracle covers. A single
  batched run of a local `pytop-snappy` image (Python 3.12 + `snappy`) validates
  `first_homology_of_surgery` against SnapPy's Dehn-filling homology — figure-8
  knot surgeries (`p/q` → ℤ/p) and Whitehead-link surgeries (ℤ/a ⊕ ℤ/b). SnapPy
  cannot run natively here, so it is a subprocess oracle; opt-in keeps it out of
  the default suite. (Both report the invariant-factor form, so they match
  directly — e.g. ℤ/2 ⊕ ℤ/3 is `[6]` in both.)
- **Remaining** (deferred — genuinely unavailable here): **GAP** and **Regina**
  as *native* libraries (only reachable via the Docker SageMath / SnapPy images);
  deeper orchestration / interop bridges; and formal verification of the full
  computational core (SNF proved; topology modules expanding).

### Phase 5 — TDA & computational geometry ✅ COMPLETE (v0.9.8–v1.0.0)

- **P5.1 — Discrete Morse theory** ✅ (`discrete_morse.py`): `MorsePair`, `MorseMatching`,
  `discrete_gradient_matching` (greedy + V-path DFS acyclicity guard), `is_valid_morse_matching`,
  `check_morse_inequalities`. Perfect matchings: S^1 → 2 critical cells, S^2 → 2, torus χ=0.
- **P5.2 — Persistence distances & descriptors** ✅ (`persistence_distances.py`):
  `bottleneck_distance` (binary search + max bipartite matching), `wasserstein_distance`
  (Jonker–Volgenant O(n³) Hungarian, augmented (m+n)×(m+n) cost matrix),
  `PersistenceLandscape` (Bubenik 2015 k-th tent on grid), `persistence_entropy` (Shannon).
- **P5.3 — Mapper algorithm** ✅ (`mapper.py`): Singh–Mémoli–Carlsson (2007) full pipeline —
  `IntervalCover` (overlapping uniform cover), `single_linkage_labels` (1-D single-linkage),
  `mapper()` (filter → cover → pullback clustering → nerve complex up to configurable dim),
  `MapperComplex` with `connected_components()` / `adjacency()`.

### Phase 6 — TDA pipeline & advanced filtrations ✅ COMPLETE (v1.0.1–v1.0.3)

- **P6.1 — Čech complex** ✅ (`cech_complex.py`): `cech_filtration` + `persistent_homology_cech`.
  Welzl miniball (Gaussian elimination circumsphere). Rips–Čech sandwich verified.
- **P6.2 — Persistence over Z/p** ✅ (`persistent_homology_fp.py`): `persistence_pairs_fp(filtered, prime)`
  over F_p for any prime p. Alternating-sign boundary, Fermat modinv. Torsion detection.
- **P6.3 — TDA Pipeline** ✅ (`tda_pipeline.py`): `TDAPipeline` immutable builder.
  `.rips()/.cech()/.reduce(method)/.pairs()/.barcode()/.diagram()/.landscape()/.entropy()/.bottleneck()/.wasserstein()/.compare_primes()/.summary()`.
  All 4 reduction methods (standard/twist/cohomology/fp).

### Phase 7 — Combinatorial topology & geometric structures ✅ COMPLETE (v1.0.4–v1.0.5)

| Milestone | Module | Status | Delivered |
|-----------|--------|--------|-----------|
| **P7.1** | `simplicial_filtration` | ✅ | Standard triangulations: `torus_filtration` (7-vertex T²), `klein_bottle_filtration` (8-vertex), `rp2_filtration` (6-vertex RP²). 33 tests. |
| **P7.2** | `simplicial_maps` | ✅ | `SimplicialMap` + validation, `chain_map_matrix` (signed integer matrix), `induced_map_on_homology` (via extended SNF), `cone_complex` (contractible), `suspension_complex` (Σ(Sⁿ)≃Sⁿ⁺¹). 42 tests. |
| **P7.3** | `nerve_complex` | ✅ | `nerve_of_cover`, `good_cover_check` (Nerve theorem preconditions), `cech_nerve` (Welzl miniball circumsphere). 30 tests. |
| **P7.4** | `spectral_sequences` | ✅ | `SpectralPage`, `FilteredChainComplex`, `differential_d_r`, `converges_to` (E^r → E^∞ stability). 25 new tests (205 total). |
| **P7.5** | `surgery_theory` | ✅ | `handle_attachment` (K ∪ cone(Sᵏ⁻¹)), `trace_cobordism`, `trace_homology`. 24 tests. |
| **P7.6** | `morse_complex` | ✅ | `MorseChainComplex`, `morse_boundary_operator` (gradient V-path DFS + Forman signs), `morse_homology` (SNF + Morse theorem cross-validation). 32 tests. |

**Phase 7 total: 186 new tests. All P7.1–P7.6 milestones closed.**

**Deferred (long-range):** sheaf cohomology, persistent K-theory, formal verification of
SNF correctness for the persistence pipelines (`PersHomology.lean` remaining bodies).

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

## Part V — Summary statistics (2026-06-21)

| Metric | Value |
|--------|-------|
| Tests passing | **9 959** (+ 16 opt-in SageMath/SnapPy-oracle tests) |
| Representations in `experimental.spaces` | 10 |
| Predicates (with witnesses) | 16 |
| pi-Base spaces bridged | 222 |
| pi-Base properties / theorems / traits | 243 / 902 / 2 099 |
| Phase 1 milestones complete | 5 / 5 ✅ |
| Phase 2 milestones complete | 8 / 8 ✅ |
| Phase 3 milestones complete | 3 / 3 ✅ |
| Phase 4 milestones complete | 8 / 8 ✅ |
| Phase 5 milestones complete | 3 / 3 ✅ |
| Phase 6 milestones complete | 3 / 3 ✅ |
| Phase 7 milestones complete | 6 / 6 ✅ |
| **Current version** | **v1.0.5** |

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
