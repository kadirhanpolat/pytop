# pytop — Capabilities, Limitations & Roadmap to Research Grade

> An honest assessment of what pytop can and cannot do today (post-v0.6.0), and a
> phased roadmap toward a GAP-scale research-grade topology computation system,
> starting from set-theoretic (point-set) topology.
>
> **Status as of 2026-06-23 (v1.6.0):** Phases 1–15 complete + Phase 16 ✅ P16.1–P16.3 complete + Phase 17 P17.1 ✅ profiling infrastructure complete (11,945 tests). Phase 1
> (set-theoretic topology) substantive; Phase 2–7 computational core (homology,
> cohomology, Mayer–Vietoris, van Kampen, Khovanov, combinatorial topology);
> Phase 8 advanced algebra (6 modules); Phase 9 computable-space expansion (19 reps);
> Phase 10 scale & algorithms (sparse SNF, GPU optional); Phase 11 Lean formal
> verification (11 files, 0 sorry); Phase 12 sheaf cohomology + persistent K-theory;
> Phase 13 homotopy (Eilenberg–MacLane, Massey, Hopf); Phase 14 advanced knot
> homology (Khovanov odd, grid Floer, concordance); Phase 15 4-manifold topology
> (intersection forms, Kirby, Casson, Rohlin). **Phase 16 ✅ AUTONOMOUS**: P16.1 benchmark suite ✅ (37 tests, minimal triangulations, 45-knot table, large graphs); **P16.2 ✅ AUTONOMOUS oracle parity** (45 primes unknot–10_5, GUDHI/Ripser/SnapPy/Sage adapters, OracleAgreementBuilder orchestration, run_p16_2_oracle_agreement.py CLI, JSON+Markdown reports, 11 tests); P16.3 statistical validation ✅ (10K ER 1-skeleta, pytop 100% success, avg 6.26 ms/complex). **Formal verification** (`formal/`): Lean 4 + Mathlib v4.31 proofs — SNF (0 sorry),
> set topology (34 theorems + 24 alt proofs; 0 sorry), metric topology (0 sorry),
> persistence homology (0 sorry). **11 formal files total; 0 sorry throughout.**

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

- Knots, surfaces: largely **hardcoded `*Profile` registries** (known invariants of famous
  objects). They report what is known; they do not analyze *your* object.
- The following modules retain their `*Profile` registries **and** now also expose
  computational engines (v1.0.6–v1.0.8):
  - **v1.0.6**: `covering_spaces` (`CoveringGraph`, `cyclic_voltage_cover`,
    `universal_covering_tree`, …), `fundamental_group` (`pi1_graph`), `three_manifolds`
    (`mapping_torus_h1`, `lens_space_pi1`), `homotopy` (`is_contractible_simplicial`,
    `has_sphere_homology`), `degree_theory` (`map_degree_simplicial`), `manifolds`
    (`euler_characteristic_simplicial`).
  - **v1.0.8**: `shape_theory` (`link_complex`, `is_manifold_triangulation`,
    `has_trivial_shape_sc`, `shape_anr_check_sc`), `coarse_geometry`
    (`growth_function_graph`, `geodesic_distance_graph`, `is_tree_graph`,
    `classify_graph_coarse_growth`), `locale_theory` (`frame_from_finite_topology`,
    `pseudocomplement_in_frame`, `well_inside_relation`, `is_regular_frame`,
    `is_spatial_finite_frame`), `dimension_theory` (`covering_dimension_simplicial`,
    `ind_finite_space`).
- The remaining "advanced" modules (`topos_theory`, `noncommutative_topology`,
  `higher_categories`, `operads`, `topological_field_theory`,
  `derived_categories`): **tag-based classifiers**.
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

**Deferred (long-range):** sheaf cohomology, persistent K-theory.

### Post-Phase 7 improvements (v1.0.6, 2026-06-22)

**Profile→Computational engine upgrades (6 modules):**

Previously Profile-only modules (hardcoded `*Profile` registries) upgraded with live
computational engines that operate on raw simplicial/graph input:

| Module | New computational functions | Tests |
|--------|-----------------------------|-------|
| `covering_spaces` | `CoveringGraph`, `cyclic_voltage_cover`, `fundamental_group_rank_graph`, `is_graph_covering_map`, `universal_covering_tree` | 32 |
| `fundamental_group` | `pi1_graph` | 14 |
| `three_manifolds` | `mapping_torus_h1`, `lens_space_pi1` | 21 |
| `homotopy` | `is_contractible_simplicial`, `has_sphere_homology` | 26 |
| `degree_theory` | `map_degree_simplicial` | 8 |
| `manifolds` | `euler_characteristic_simplicial` | 18 |

**Critical bug fix — `_snf_ext` infinite loop eliminated:**
`mayer_vietoris._snf_ext` had `q -= 1` corrections for C-style truncation division;
Python's `//` is floor division and already gives the correct floor quotient. The
correction over-adjusted, making remainders exceed the pivot and producing infinite
swap cycles for matrices with negative entries (e.g. seed 3141 in the 150-iteration
property test). Corrections removed; all property tests pass in < 0.5 s.

**Total (v1.0.6): 119 new tests; 10 864 core tests passing (+ 16 opt-in SageMath/SnapPy-oracle tests).**

### Post-Phase 7 improvements (v1.0.7, 2026-06-22)

**Three new `experimental.spaces` representations (10 → 13 canonical representations):**

| Class | Description | Key certificates | Tests |
|-------|-------------|-----------------|-------|
| `ProductMetricSpace` | Product of two metric spaces with sup metric | T0–T6, first-countable, Tychonoff | 20 |
| `LexicographicSquareSpace` | [0,1]² with lex order topology | T5, compact, connected, Lindelöf, NOT second-countable, NOT separable (cellularity=𝔠) | 29 |
| `CantorSpaceRepresentation` | {0,1}^ω product topology | T6, compact, totally disconnected, second-countable, separable, all cardinals=ℵ₀ | 25 |

Factory functions: `rational_plane()` (ℚ²), `lexicographic_square()`, `cantor_space()`.

The lex square and Cantor space are the two canonical compact extremes: connected vs. totally
disconnected; not-second-countable vs. second-countable; cellularity 𝔠 vs. ℵ₀.
The `ProductMetricSpace` enables composition of arbitrary certified metric spaces.

**Total (v1.0.7): 81 new tests; 10 945 core tests passing (+ 16 opt-in SageMath/SnapPy-oracle tests).**

### Post-Phase 7 improvements (v1.0.8, 2026-06-22)

**Profile→Computational engine upgrades (4 modules, 13 functions):**

Previously Profile-only modules upgraded with live computational engines operating on raw
simplicial complexes (`list[list[Any]]`) or graph adjacency dicts (`dict[Any, list[Any]]`):

| Module | New computational functions | Tests |
|--------|-----------------------------|-------|
| `shape_theory` | `link_complex` (lk(K,v) face-closed), `is_manifold_triangulation` (every vertex link ≃ Sⁿ⁻¹ by H_*), `has_trivial_shape_sc` (homological contractibility), `shape_anr_check_sc` (Borsuk ANR theorem: compact polyhedra → ANR/FANR/movable dict + shape class) | 35 |
| `coarse_geometry` | `growth_function_graph` (BFS ball sizes b(r)), `geodesic_distance_graph` (shortest-path length, −1 if unreachable), `is_tree_graph` (connected + \|E\|=\|V\|−1), `classify_graph_coarse_growth` (polynomial/exponential via log-log slope method; Gromov polynomial-growth theorem annotation) | 38 |
| `locale_theory` | `frame_from_finite_topology` (validates ∩/∪ closure, returns sorted frame), `pseudocomplement_in_frame` (b* = ∨{c : c∧b=∅}), `well_inside_relation` (b << a iff b* ∨ a = top), `is_regular_frame` (every a = ∨{b : b << a}), `is_spatial_finite_frame` (∅ and top present) | 40 |
| `dimension_theory` | `covering_dimension_simplicial` (max simplex dim = covering dim of polyhedron), `ind_finite_space` (strict chain length in specialization poset; indiscrete on {0,1} correctly returns 0) | 20 |

**Bug fixes:**
- `ind_finite_space`: strict specialization order now used (x < y requires x ≤ y AND NOT y ≤ x); indiscrete topology was incorrectly returning 1 instead of 0.
- Test fixture TORUS_7: replaced incorrect triangulation (χ=1) with Heawood's Z₇-cyclic triangulation (χ=0, 7 vertices, 21 edges, 14 faces).
- `classify_graph_coarse_growth` polynomial degree: switched from `log(b(r))/log(r)` (biased high for small r) to log-log slope method `log(b(r)/b(r−1))/log(r/(r−1))` averaged across all radii.

**Total (v1.0.8): 120 new tests; 11 065 core tests passing (+ 16 opt-in SageMath/SnapPy-oracle tests).**

### Phase 8 — Profile→Computational: Advanced Algebra ✅ complete (v1.0.9)

Six modules upgraded from `*Profile` registries to genuine computational engines. 171 new tests;
11 236 tests pass total.

| Milestone | Module | New computational functions |
|-----------|--------|-----------------------------|
| **P8.1** ✅ | `derived_categories` | `mapping_cone_complex`, `derived_functor_h`, `triangulated_structure_check` |
| **P8.2** ✅ | `topos_theory` | `site_from_finite_topology`, `sheaf_on_site`, `sheafification_finite`, `topos_check` |
| **P8.3** ✅ | `operads` | `associahedron_complex`, `operad_composition_check`, `bar_construction_sc` |
| **P8.4** ✅ | `higher_categories` | `nerve_of_category`, `kan_fibration_check_sc`, `homotopy_type_finite_cat` |
| **P8.5** ✅ | `noncommutative_topology` | `k0_group_matrix_algebra`, `spectral_dimension_finite`, `k1_group_matrix_algebra` |
| **P8.6** ✅ | `topological_field_theory` | `cobordism_from_handles`, `tqft_dimension_2d`, `handle_signature_tft` |

### Phase 9 — `experimental.spaces` Expansion ✅ complete (v1.1.0)

Grows the computable-space protocol from 13 to 20+ canonical representations, covering the classical
infinite spaces missing from the current suite.

| Milestone | Representation | Key certificates | Notes |
|-----------|---------------|-----------------|-------|
| **P9.1** | `OnePointCompactificationSpace` | Compact; T2 iff original is locally compact T2; Alexandroff extension | Wraps any existing `Space` |
| **P9.2** | `StoneCechSpace` (βℕ) | Compact, T4, separable (ℕ dense), NOT first-countable, NOT T6 | Ultrafilter representation |
| **P9.3** | `HilbertCubeSpace` ([0,1]^ω) | Compact, T6, second-countable; universal compact metrizable space | Cylinder-neighbourhood certificates |
| **P9.4** | `SolenoidSpace` | Compact, connected, NOT locally connected; specialises `InverseLimitSpace` with circle bonding maps | |
| **P9.5** | `UniformSpace` protocol | Uniform covers + completion; Cauchy filter; `UniformProduct`, `UniformSubspace` | New protocol layer |
| **P9.6** | `ProfiniteSpace` | Totally disconnected, compact, T2; inverse limit of finite discrete groups | |

**Actual (v1.1.0): 166 new tests; 11 402 core tests passing (+ 16 opt-in SageMath/SnapPy-oracle tests).**

Six new representations (13 → 19 canonical representations):

| Milestone | Representation | Tests | Key facts |
|-----------|---------------|-------|-----------|
| **P9.1** ✅ | `OnePointCompactificationSpace` | 15 | compact; T2 iff base is locally compact T2; finite base → ∞ isolated |
| **P9.2** ✅ | `StoneCechSpace` (βℕ) | 18 | compact, T4, separable (ℕ dense), NOT first-countable, NOT T6 |
| **P9.3** ✅ | `HilbertCubeSpace` ([0,1]^ω) | 31 | compact, T6, second-countable, connected, universal compact metrizable |
| **P9.4** ✅ | `SolenoidSpace` | 28 | compact, connected, T6, NOT locally connected; `contains()` checks compatibility |
| **P9.5** ✅ | `UniformSpace` + `UniformProduct` + `UniformSubspace` | 40 | metric-derived uniformity; `entourage`, `is_cauchy`, `uniform_neighbourhood` |
| **P9.6** ✅ | `ProfiniteSpace` + `p_adic_integers` | 34 | compact, T6, totally disconnected; ℤ_p as lim← ℤ/pⁿ |

**Note:** The roadmap's P9.2 entry said "NOT separable, T6" — both are incorrect for βℕ.
ℕ is a countable dense subspace (separable = True); βℕ is not metrizable so T6 = False.
Implemented according to mathematical facts.

### Phase 10 — Scale & Algorithm ✅ complete (v1.2.0)

Extends practical input limits of existing engines without new mathematics. All backends remain
optional; the pure-Python correctness core is never a hard dependency.

| Milestone | Target | Status | Delivered |
|-----------|--------|--------|-----------|
| **P10.1** | Sparse SNF | ✅ | `sparse_linalg.py`: `_SparseMat` (dual row/col dicts) + `_sparse_snf_inner`; `sparse_smith_normal_form` (scipy.sparse input accepted); `matrix_density`; `homology._smith_normal_form` auto-routes `min(m,n) ≥ 30` + density < 30 % |
| **P10.2** | Parallel Khovanov | ✅ | `khovanov_homology(parallel=True)`: `ThreadPoolExecutor` pre-computes per-quantum-grading SNFs; GIL-limited on pure-Python, truly parallel with `[fast]` flint backend; identical results |
| **P10.3** | Approximate persistence | ✅ | `witness_complex.py`: `landmark_sample` (maxmin farthest-point / random), `witness_filtration` (strong-witness definition, de Silva & Carlsson 2004), `persistent_homology_witness` → `WitnessComplex`; pure Python |
| **P10.4** | Streaming TDA | ✅ | `streaming_persistence.py`: `StreamingPersistence` — incremental Z/2 bitmask column reduction; `add_simplex / current_pairs / current_betti / current_essential_pairs`; results match `persistence_pairs_twist` |
| **P10.5** | Optional GPU backend | ✅ | `_gpu_backend.py`: `GPU_AVAILABLE`, `gpu_twist_reduce`; cupy boolean-array column XOR; `[gpu]` extra in `pyproject.toml`; graceful CPU fallback when cupy absent or filtration < `GPU_MIN_SIZE = 500` |

**65 new tests; 11 467 tests pass total.**

### Phase 11 — Formal Verification Expansion ✅ complete (v1.3.0)

Extends the `formal/` Lean 4 proof corpus from SNF + basic set topology + persistence reduction
to the main computational engines. 0-sorry rule holds throughout; corpus grows from 6 to 11 files.

| Milestone | Lean file | Delivered |
|-----------|-----------|-----------|
| **P11.1** ✅ | `MayerVietoris.lean` | `SES` structure; `ses_p_zero_of_im`; `delta_well_defined`; `snake_delta_exists`; `snake_delta_independent` (connecting class well-defined in A') |
| **P11.2** ✅ | `VanKampen.lean` | `Pres` + `TietzeEquiv`; `tietze_elim / add_gen`; `AmalgamDatum` + `Pushout`; `pushout_universal`; `int_hom_determined_by_one` (ℤ is initial); `int_hom_exists` |
| **P11.3** ✅ | `CohomologyRing.lean` | Alexander–Whitney `cup` product; `cup_value_assoc` (Bool.and_assoc); `cup_comm_Z2`; `coboundary0`; `leibniz_0cochains` |
| **P11.4** ✅ | `PersistencePairing.lean` | `pairing_is_perfect` (= `reduce_is_reduced`); `pairs_have_distinct_births` (birth indices Nodup); key chain: `isReduced_tail` → `filterMap_getLast_nodup_of_isReduced` → `zipWith_range_filterMap_snd_eq` → `map_fst_pairs_eq` |
| **P11.5** ✅ | `SpectralSequences.lean` | `ChainCx` (d² = 0 by construction); `d_sq_zero`; `image_sub_kernel`; `SpectralSeq`; `const_convergent`; `stabilizes_mono`; `const_pages_convergent` |

**0 sorry across all 11 Lean files.**

### Phase 12 — Research Frontier (v1.4.0+)

| Milestone | Topic | Status | Delivered |
|-----------|-------|--------|-----------|
| **P12.1** | Sheaf cohomology (Čech) | ✅ | `sheaf_cohomology.py`: `FiniteSheaf`, `constant_sheaf`, `skyscraper_sheaf`, `cech_cohomology`, `sheaf_cohomology`. Čech cochain complex with alternating-sum coboundary δ^p; minimal-neighborhood Leray cover; SNF → AbelianGroup per degree. 41 tests. |
| **P12.2** | Persistent K-theory | ✅ | `persistent_ktheory.py`: `KTheoryGroups`, `KBarcode`, `k_theory_groups`, `k_barcode`. Rational AHSS: K⁰⊗ℚ=⊕H_{2k}, K¹⊗ℚ=⊕H_{2k+1}; persistent barcode partitioned by dimension parity. 37 tests. |
| **P12.3** | Homeomorphism heuristics | ⬜ | Undecidable in general; subclass algorithms require substantial new machinery |
| **P12.4** | Native GAP / Regina integration | ⬜ | Currently only Docker oracles; in-process FFI or persistent subprocess bridge |
| **P12.5** | Countably infinite simplicial complexes | ⬜ | Convergence algorithms for infinite Rips / infinite CW complexes |

### Phase 13 — Homotopy Theory (v1.5.0)

| Milestone | Topic | Status | Delivered |
|-----------|-------|--------|-----------|
| **P13.1** | Chain homotopy | ✅ | `chain_homotopy.py`: `is_chain_homotopy` (∂h+h∂=f−g), `find_chain_homotopy` (ℚ-Gaussian elimination), `chain_homotopy_equiv`, `homotopy_equivalence_simplicial`. |
| **P13.2** | Eilenberg–MacLane spaces | ✅ | `eilenberg_maclane.py`: `km_homology_{cyclic,free,free_abelian,z,z2,rational}`, `is_aspherical_by_homology` (complex or explicit homology), `km_euler_characteristic`. |
| **P13.3** | Massey products / formality | ✅ | `massey_products.py`: `triple_massey_product`, `massey_vanishes`, `is_formal_simplicial`, `all_triple_massey_products`. |
| **P13.4** | Hopf invariant | ✅ | `hopf_invariant.py`: `hopf_fibration` (n=1,2,4,8), `adams_hopf_invariant_one`, `hopf_invariant_from_{linking,cup}`, `pi3_s2`. |
| **P13.5** | Sullivan minimal models | ✅ | `sullivan_models.py`: `sullivan_{sphere,torus,complex_projective,product,from_betti}`, `pi_rational`, `euler_characteristic_sullivan` (Hilbert series of ΛV), `is_pure_sullivan`. |

### Phase 14 — Advanced Knot Homology (v1.5.0)

| Milestone | Topic | Status | Delivered |
|-----------|-------|--------|-----------|
| **P14.1** | Odd Khovanov homology | ✅ | `khovanov_odd.py`: `khovanov_homology_odd`, `OddKhovanovHomology`, `compare_khovanov_parities`. |
| **P14.2** | Grid diagram Floer (HFK̂) | ✅ | `grid_floer.py`: `GridDiagram`, `GridState`, `HFKHat`, `hfk_hat` (𝔽₂ rectangle differential), `trefoil_grid`, `alexander_polynomial_from_hfk`. |
| **P14.3** | Concordance invariants | ✅ | `concordance.py`: `tau_torus_knot`, `s_invariant_torus_knot`, `signature_torus_knot`, `tristram_levine_signature`, `is_algebraically_slice`, `concordance_order`. |
| **P14.4** | Satellite / cable knots | ✅ | `satellite_knots.py`: `satellite_alexander_poly` (Morton), `cable_alexander_poly`, `torus_knot_alexander_poly` (exact polynomial division), `cable_genus`, `whitehead_double`. |
| **P14.5** | Virtual knots | ✅ | `virtual_knots.py`: `gauss_code_from_string`, `parity_of_crossing`, `odd_writhe`, `arrow_polynomial_bracket`, `virtual_knot_invariants`. |

### Phase 15 — 4-Manifold Topology (v1.5.0)

| Milestone | Topic | Status | Delivered |
|-----------|-------|--------|-----------|
| **P15.1** | Intersection forms | ✅ | `intersection_forms.py`: `intersection_form`, `form_signature` (Sylvester congruence diagonalisation), `e8_form`, `hyperbolic_form`, `donaldson_theorem`, `STANDARD_FORMS`. |
| **P15.2** | Kirby calculus | ✅ | `kirby_calculus.py`: `kirby_diagram`, `kirby_stabilize`, `kirby_handle_slide`, `kirby_to_intersection_form`, `kirby_diagram_{cp2,s2xs2,k3_fiber}`, `dehn_surgery_matrix`. |
| **P15.3** | Casson invariant | ✅ | `casson_invariant.py`: `casson_invariant_brieskorn` (Neumann–Wahl λ=σ(F)/8), `casson_invariant_surgery`, `casson_invariant_lens_space`, `dedekind_sum`, `CASSON_DATABASE`. |
| **P15.4** | Milnor fibers | ✅ | `milnor_fibers.py`: `milnor_number`, `milnor_fiber_brieskorn`, `milnor_fiber_signature`, `monodromy_order`, `milnor_fiber_ade`, `ADE_DATABASE`. |
| **P15.5** | Rohlin's theorem | ✅ | `rohlin_theorem.py`: `check_rohlin_theorem` (spin+smooth → σ≡0 mod 16), `is_spin_manifold`, `kirby_siebenmann_obstruction`, `check_freedman_realization`, `ROHLIN_EXAMPLES`. |

### Phase 16 — Empirical Validation & Oracle Ecosystem ✅ AUTONOMOUS (v1.6.0, 2026-06-23)

Cross-validates pytop against independent gold-standard external systems via unified oracle framework.

| Milestone | Target | Status | Delivered |
|-----------|--------|--------|-----------|
| **P16.1** ✅ | Benchmark suite | ✅ | `tests/validation/fixtures.py`: `MinimalTriangulations` (T², Klein, ℝP²), `KnotTable` (45 primes unknot–10_5), `GridGraphLibrary` (3×3–40×40), `BaselineResults` (reference Betti/Euler). 37 tests. |
| **P16.2** ✅ **AUTONOMOUS** | Oracle parity framework | ✅ | `tests/validation/oracle_integrations.py` — `OracleAdapter` ABC + 4 adapters: `GudhiOracleAdapter` (Rips/Čech Betti), `RipserOracleAdapter` (fast persistent homology), `SnapPyOracleAdapter` (Dehn H₁, opt-in Docker), `SageOracleAdapter` (K-theory, opt-in Docker). `tests/validation/oracle_agreement_builder.py` — `OracleAgreementBuilder` orchestration engine, `AgreementMatrixReport` (JSON + Markdown export). `_scripts/run_p16_2_oracle_agreement.py` — autonomous CLI runner (--fast/--full modes, auto-detect oracles, JSON+Markdown reports). Knot table expansion 40→45. **11 new tests** (oracle availability, persistent Betti agreement, polynomial validation). |
| **P16.3** ✅ | Statistical validation | ✅ | `tests/validation/test_statistical_validation.py`: 10,000 random Erdős–Rényi 1-skeleta (5–50 vertices), pytop H₀/H₁ 100% success rate, avg 6.26 ms/complex. JSON report + outlier analysis. Framework ready for 50K+ scale. |

**Framework ready for:** PyPI publication, CI/CD matrix integration, automated cross-oracle matrix population (GUDHI vs Ripser vs SnapPy vs Sage agreement pipeline).

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

## Part V — Summary statistics (2026-06-23)

| Metric | Value |
|--------|-------|
| Tests passing | **11 945** (+ 16 opt-in SageMath/SnapPy-oracle tests + 79 validation tests + 86 profiling tests) |
| Representations in `experimental.spaces` | 19 |
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
| Phase 8 milestones complete | 6 / 6 ✅ (Profile→Computational: advanced algebra) |
| Phase 9 milestones complete | 6 / 6 ✅ (`experimental.spaces` expansion) |
| Phase 10 milestones complete | 5 / 5 ✅ (scale & algorithm) |
| Phase 11 milestones complete | 5 / 5 ✅ (Lean formal verification expansion) |
| Phase 12 milestones complete | 2 / 5 ✅⬜ (sheaf cohomology, persistent K-theory done) |
| Phase 13 milestones complete | 5 / 5 ✅ (homotopy theory) |
| Phase 14 milestones complete | 5 / 5 ✅ (advanced knot homology) |
| Phase 15 milestones complete | 5 / 5 ✅ (4-manifold topology) |
| Phase 16 milestones complete | 3 / 3 ✅ (P16.1–P16.3 AUTONOMOUS: benchmark, oracle parity framework, statistical validation) |
| Phase 17 milestones complete | 1 / 3 ✅⬜ (P17.1 profiling infrastructure done; P17.2–P17.3 optimization pending) |
| **Current version** | **v1.6.0** |

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
