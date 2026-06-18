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
| Exact genus / planarity | `graph_genus`, `is_planar` | `∏_v (deg(v) − 1)!` rotation systems (super-exponential) | small, low-degree graphs (`≲ 8` vertices) |
| Euler edge bound | `satisfies_planar_edge_bound` | `O(1)` | unrestricted (necessary, not sufficient) |

## Notes

- **"Practical limit"** is a rough guide for an interactive (seconds-scale) run
  on a single machine; it is not a hard cap. Memoisation (HOMFLY, multivariable
  Alexander) and the Clearing Lemma (persistence) help substantially on
  structured inputs but do not change the worst case.
- For exact planarity of larger graphs, use the necessary
  `satisfies_planar_edge_bound` filter first; the exponential `is_planar` search
  is only needed when the bound passes.
- Phase 4's deferred workstream — optional `numpy`/`scipy` accelerated backends
  over this exact core — would address the constant factors (not the asymptotics)
  for the linear-algebra-bound engines.
