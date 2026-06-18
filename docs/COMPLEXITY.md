# Complexity & scale reference

> Phase 4 (P4.3) — complexity discipline. An honest summary of the asymptotic
> cost and the **practical input limits** of pytop's computational engines.
>
> pytop's design choice is a **pure-Python, exact correctness core** (no
> floating-point homology, no hidden approximations). Exactness has a price:
> several engines are exponential in the natural size parameter and are intended
> for the *small, tabulated* inputs of textbooks and knot/link tables — not for
> large-scale computation. Where an engine is exponential, that is a property of
> the problem (or of the brute-force-but-correct approach), and is stated below
> so you are never surprised.

## Knot & link invariants

| Engine | Entry point | Complexity | Practical limit |
|--------|-------------|-----------|-----------------|
| Jones (Kauffman state sum) | `jones_polynomial` | `O(2ⁿ)` states, `n` = crossings | `n ≲ 18–20` |
| HOMFLY-PT (braid skein) | `homfly_polynomial` | `O(2ᵏ)` skein tree in word length `k`, memoised on the word | braids `≲ 12–15` crossings |
| Multivariable Alexander | `multivariable_alexander` | `O(2ᶜ)` memoised Laplace minor over the `n`-variable Laurent ring, `c` = crossings | links `≲ 10` crossings |
| Alexander (reduced Burau) | `alexander_polynomial_from_braid` | `O(k · (s−1)²)` matrix products + `O((s−1)!)` cofactor determinant, `s` = strands | strands `≲ 8` |
| Khovanov homology | `khovanov_homology` | chain dimension `Σ_v 2^{circles(v)}` (worst `~3ⁿ`), then SNF per quantum grading | knots `≲ 8–10` crossings |
| Seifert genus/signature | `seifert_genus_bound`, `signature` | `O(c)` smoothing + `O((2g)³)` LDLT, `g` = genus | unrestricted in practice |

## Homology, surgery & linear algebra

| Engine | Entry point | Complexity | Practical limit |
|--------|-------------|-----------|-----------------|
| Simplicial homology | `betti_numbers` | SNF of boundary matrices, polynomial in the number of simplices | moderate complexes |
| Persistent homology (Vietoris–Rips) | `persistent_homology` | `O(n^{d+2})` simplices to dimension `d`; reduction `O(m³)` in `m` = simplices | clouds `n ≲ 20–30` (small `d`) |
| Cubical persistence (Twist+Clearing) | `persistent_homology_bitmap` | shared Twist+Clearing kernel; `O(m³)` worst case, near-linear typical | moderate 2-D bitmaps |
| Smith normal form | `smith_normal_form` | iterative pivot reduction, polynomial; integer growth bounded by divisibility | a few hundred rows |
| Integer determinant (Bareiss) | `integer_determinant` | `O(n³)` fraction-free, exact (bounded coefficient growth) | a few hundred rows |
| Dehn surgery `H₁` | `first_homology_of_surgery` | one SNF of the `n × n` framing/linking matrix | unrestricted in practice |

## Graph topology

| Engine | Entry point | Complexity | Practical limit |
|--------|-------------|-----------|-----------------|
| Exact genus | `graph_genus` | `∏_v (deg(v) − 1)!` rotation systems (super-exponential); **early-terminates at the first genus-0 embedding** | small, low-degree graphs (`≲ 8` vertices) |
| Planarity decision | `is_planar` | `O(V+E)` Euler edge-bound reject first (handles any dense `Kₙ`/`K_{m,n}` instantly); otherwise the `graph_genus` search with genus-0 early termination | dense graphs: unrestricted; sparse high-degree graphs: as `graph_genus` |
| Euler edge bound | `satisfies_planar_edge_bound` | `O(1)` | unrestricted (necessary, not sufficient) |
| Bipartite test | `_is_bipartite` (internal) | `O(V+E)` 2-colouring | unrestricted |

## Notes

- **"Practical limit"** is a rough guide for an interactive (seconds-scale) run
  on a single machine; it is not a hard cap. Memoisation (HOMFLY, multivariable
  Alexander) and the Clearing Lemma (persistence) help substantially on
  structured inputs but do not change the worst case.
- `is_planar` now applies the Euler edge bound (`E ≤ 3V−6`, or `E ≤ 2V−4` for
  bipartite graphs, detected by 2-colouring) **internally and per component**, so
  any sufficiently dense non-planar graph (every `Kₙ`, `n ≥ 5`; dense `K_{m,n}`)
  is rejected in `O(V+E)` with no rotation-system search — these used to either
  enumerate or exceed the search cap. The remaining hard case is a **sparse but
  high-degree planar graph** (e.g. a wheel with a degree-9 hub): it passes the
  edge bound yet has a rotation-system space over the cap, so it still raises
  `GraphPlanarityError`. Deciding those in polynomial time needs a dedicated
  planarity algorithm (Boyer–Myrvold / left–right / DMP); that is the natural
  next step beyond this rotation-system core.
- Genus-0 **early termination**: because a connected graph's face count satisfies
  `F ≤ E−V+2` with equality iff the embedding is planar, both `graph_genus` and
  `is_planar` stop at the first genus-0 rotation system found. This never changes
  the result and never does more work than a full enumeration, but the speedup is
  enumeration-order dependent (large when a planar embedding is found early).
- **Optional accelerated exact backend (`pip install -e .[fast]`):** when
  [`python-flint`](https://pypi.org/project/python-flint/) is installed, the
  integer Smith normal form — and therefore every homology / cohomology /
  cellular / Khovanov / surgery engine built on it — is routed to FLINT above a
  small size threshold. Even on pytop's *sparse* boundary / Khovanov matrices
  (entries in `{−1, 0, 1}`), FLINT's compiled exact SNF is **~5–8× faster** than
  the pure-Python routine (measured on 16×20 … 40×50 matrices), with identical
  results (pinned by the differential tests). `numpy`/`scipy` are floating-point
  and cannot accelerate the *exact* core — only a fast exact library such as
  FLINT can. (The pure-Python core stays the default and the only hard
  requirement.)
