"""Uniform convergence: pointwise vs uniform limits, equicontinuity, Arzelà-Ascoli theorem,
Dini's theorem, and the topology of uniform convergence on function spaces.

Key theorems implemented
------------------------
- Pointwise vs uniform convergence: a sequence (f_n) of functions X -> Y converges
  pointwise to f if for every x in X: lim_{n->infty} f_n(x) = f(x). It converges
  uniformly if for every epsilon > 0 there exists N such that n >= N implies
  d(f_n(x), f(x)) < epsilon for ALL x in X simultaneously. Uniform convergence is
  strictly stronger: the modulus of continuity N(epsilon) does not depend on x.
  Key example where they differ: f_n(x) = x^n on [0,1] converges pointwise to the
  indicator of {1} but NOT uniformly (the supremum ||f_n - f||_infty = 1 for all n).
- Uniform limit theorem: if (f_n) is a sequence of continuous functions f_n: X -> Y
  (Y metric) converging uniformly to f, then f is continuous. The converse fails:
  pointwise limits of continuous functions can be discontinuous. Proof: for epsilon > 0,
  choose N so that d(f_n(x), f(x)) < epsilon/3 for all x, then use continuity of f_N
  at x_0 to control d(f_N(x), f_N(x_0)) < epsilon/3, then combine by triangle inequality.
- Dini's theorem (1878): let (f_n) be a sequence of continuous functions on a compact
  space X, converging pointwise to a continuous function f. If the convergence is
  monotone (f_1 >= f_2 >= ... >= f, or f_1 <= f_2 <= ... <= f), then it is uniform.
  Key hypotheses: compactness of X, continuity of the limit f, and monotonicity — all
  three are necessary (counterexamples exist if any one is dropped).
- Equicontinuity (Ascoli 1883): a family F of functions X -> Y is equicontinuous at
  x_0 if for every epsilon > 0 there exists delta > 0 such that d_X(x, x_0) < delta
  implies d_Y(f(x), f(x_0)) < epsilon for ALL f in F simultaneously. F is
  equicontinuous (globally) if equicontinuous at every x_0. Equicontinuity means the
  family shares a uniform modulus of continuity. Key examples:
  - Lipschitz families with uniform constant: |f(x)-f(y)| <= L·d(x,y) for all f in F.
  - Uniformly bounded families of C^1 functions with uniformly bounded derivative.
  - Solutions to an ODE with uniformly bounded right-hand side (Euler equicontinuity).
- Arzelà-Ascoli theorem (1883-1895): let X be a compact metric space (or compact
  Hausdorff space) and (f_n) a sequence of functions X -> R (or R^k). If (f_n) is:
  (1) uniformly bounded: there exists M such that |f_n(x)| <= M for all n, x;
  (2) equicontinuous;
  then (f_n) has a uniformly convergent subsequence.
  In functional-analytic terms: A ⊆ C(X) is relatively compact in the uniform norm
  topology iff A is uniformly bounded and equicontinuous. The Arzelà-Ascoli theorem
  is the compactness criterion for C(X) — the analogue of Heine-Borel for function
  spaces. Key applications: existence of solutions to ODEs (Peano theorem), existence
  of harmonic functions (Montel's theorem in complex analysis), and compactness
  arguments in PDE theory.
- Uniform convergence topology on C(X, Y): for compact X and metric Y, the sup-norm
  d(f,g) = sup_{x in X} d_Y(f(x), g(x)) makes C(X,Y) a metric space. The induced
  topology is the topology of uniform convergence (= compact-open topology when X is
  compact). C(X) = C(X,R) with the sup norm is a Banach space (complete normed space).
  For X compact Hausdorff: C(X) is a commutative unital C*-algebra (Gelfand duality).
- Stone-Weierstrass theorem (1885 / 1937): let X be a compact Hausdorff space and A
  a subalgebra of C(X,R) that: (1) separates points (for x ≠ y, exists f in A with
  f(x) ≠ f(y)); (2) contains the constant functions. Then A is dense in C(X,R) in
  the uniform norm. Weierstrass's original theorem: polynomials are dense in C([a,b]).
  Complex version: A must also be closed under complex conjugation.
- Compact-open topology: on C(X,Y) for topological spaces X, Y, the compact-open
  topology has subbasis sets V(K, U) = {f : f(K) ⊆ U} for K ⊆ X compact, U ⊆ Y open.
  For X locally compact Hausdorff and Y metric, the compact-open topology equals the
  topology of uniform convergence on compact subsets. For X compact and Y metric, the
  compact-open topology equals the uniform topology. The exponential law: if X, Y, Z
  are locally compact Hausdorff, then C(X × Y, Z) ≅ C(X, C(Y, Z)) homeomorphically.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .result import Result


@dataclass(frozen=True)
class UniformConvergenceProfile:
    """A curated uniform convergence / function space example."""

    key: str
    display_name: str
    convergence_type: str
    is_uniform: bool
    is_equicontinuous: bool
    limit_is_continuous: bool
    is_relatively_compact: bool
    satisfies_dini: bool
    presentation_layer: str
    focus: str
    chapter_targets: tuple[str, ...]


# ---------------------------------------------------------------------------
# Tag constants
# ---------------------------------------------------------------------------

UNIFORM_CONVERGENCE_TAGS: frozenset[str] = frozenset({
    "uniform_convergence",
    "uniformly_convergent_sequence",
    "uniform_limit",
    "sup_norm_convergence",
    "uniform_cauchy",
    "uniform_approximation",
})

POINTWISE_ONLY_TAGS: frozenset[str] = frozenset({
    "pointwise_convergence",
    "pointwise_only",
    "not_uniform",
    "pointwise_not_uniform",
    "discontinuous_pointwise_limit",
    "power_function_sequence",
})

EQUICONTINUOUS_TAGS: frozenset[str] = frozenset({
    "equicontinuous",
    "equicontinuous_family",
    "uniformly_equicontinuous",
    "lipschitz_family",
    "holder_family",
    "bounded_derivative_family",
    "uniform_modulus_of_continuity",
})

NOT_EQUICONTINUOUS_TAGS: frozenset[str] = frozenset({
    "not_equicontinuous",
    "no_uniform_modulus",
    "pointwise_only",
    "power_function_sequence",
    "unbounded_family",
})

ARZELA_ASCOLI_TAGS: frozenset[str] = frozenset({
    "arzela_ascoli",
    "relatively_compact_function_space",
    "compact_in_c_of_x",
    "uniformly_bounded_equicontinuous",
    "ascoli_condition",
})

DINI_THEOREM_TAGS: frozenset[str] = frozenset({
    "dini_theorem",
    "monotone_convergence_compact",
    "dini_condition",
    "monotone_pointwise_uniform",
})

STONE_WEIERSTRASS_TAGS: frozenset[str] = frozenset({
    "stone_weierstrass",
    "dense_subalgebra",
    "polynomial_approximation",
    "weierstrass_approximation",
    "separating_algebra",
    "trigonometric_approximation",
})

COMPACT_OPEN_TAGS: frozenset[str] = frozenset({
    "compact_open_topology",
    "topology_of_uniform_convergence",
    "sup_norm_topology",
    "uniform_topology_on_c_of_x",
    "locally_uniform_convergence",
})

NOT_RELATIVELY_COMPACT_TAGS: frozenset[str] = frozenset({
    "not_relatively_compact",
    "no_convergent_subsequence",
    "unbounded_family",
    "not_equicontinuous",
    "non_compact_function_family",
})


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_tags(space: Any) -> set[str]:
    raw = getattr(space, "tags", None) or getattr(space, "_tags", None)
    if isinstance(raw, (set, list, tuple, frozenset)):
        return {str(t).strip().lower() for t in raw}
    return set()


def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _matches_any(tags: set[str], candidates: set[str] | frozenset[str]) -> bool:
    return bool(tags & candidates)


# ---------------------------------------------------------------------------
# Named example registry
# ---------------------------------------------------------------------------

def get_named_uniform_convergence_profiles() -> tuple[UniformConvergenceProfile, ...]:
    """Return the registry of canonical uniform convergence examples."""
    return (
        UniformConvergenceProfile(
            key="power_sequence_on_interval",
            display_name="f_n(x) = x^n on [0,1] — pointwise but not uniform",
            convergence_type="pointwise_only",
            is_uniform=False,
            is_equicontinuous=False,
            limit_is_continuous=False,
            is_relatively_compact=False,
            satisfies_dini=False,
            presentation_layer="main_text",
            focus=(
                "The sequence f_n: [0,1] -> R, f_n(x) = x^n is the canonical example "
                "separating pointwise from uniform convergence. "
                "Pointwise limit: for x in [0,1), x^n -> 0 (geometric decay); for x=1, "
                "1^n = 1 for all n. So f_n -> f pointwise where f(x) = 0 for x < 1 and "
                "f(1) = 1 — the indicator function of {1}. "
                "Not uniform: ||f_n - f||_sup = sup_{x in [0,1]} |x^n - f(x)| = "
                "sup_{x in [0,1)} x^n = 1 for all n (the supremum is approached as x -> 1). "
                "Hence the convergence is NOT uniform. "
                "Discontinuous limit: each f_n is continuous but the limit f is discontinuous "
                "at x = 1 — demonstrating that pointwise limits of continuous functions can be "
                "discontinuous, unlike uniform limits. "
                "Not equicontinuous: for epsilon = 1/2, no single delta works for all n at "
                "x_0 = 1: for any delta > 0, |f_n(1-delta/2) - f_n(1)| = 1 - (1-delta/2)^n -> 1 "
                "as n -> infty. So the family {f_n} is not equicontinuous at x=1. "
                "Dini fails: the convergence is monotone (x^n >= x^{n+1} for x in [0,1]) and "
                "the domain [0,1] is compact, but the limit f is NOT continuous. Hence Dini's "
                "theorem does not apply (the continuity-of-limit hypothesis fails). "
                "Arzelà-Ascoli fails: the family {f_n} is uniformly bounded (|f_n| <= 1) "
                "but NOT equicontinuous, so Arzelà-Ascoli does not guarantee compactness — "
                "and indeed no subsequence converges uniformly."
            ),
            chapter_targets=("8", "18", "32"),
        ),
        UniformConvergenceProfile(
            key="geometric_series_uniform",
            display_name="f_n(x) = sum_{k=0}^{n} x^k on [-r,r] (r<1) — uniform convergence",
            convergence_type="uniform",
            is_uniform=True,
            is_equicontinuous=True,
            limit_is_continuous=True,
            is_relatively_compact=True,
            satisfies_dini=True,
            presentation_layer="main_text",
            focus=(
                "The partial sums f_n(x) = sum_{k=0}^{n} x^k = (1-x^{n+1})/(1-x) on "
                "[-r, r] for fixed 0 < r < 1 converge uniformly to f(x) = 1/(1-x). "
                "Uniform convergence: ||f_n - f||_sup = sup_{|x| <= r} |x^{n+1}/(1-x)| "
                "<= r^{n+1}/(1-r) -> 0 as n -> infty. The geometric factor r^{n+1} "
                "dominates uniformly in x. "
                "The Weierstrass M-test is the key tool: if |a_k(x)| <= M_k for all x and "
                "sum M_k < infty, then sum a_k converges absolutely and uniformly. Here "
                "M_k = r^k and sum r^k = 1/(1-r) < infty. "
                "Continuous limit: each f_n is a polynomial (continuous) and the limit "
                "f(x) = 1/(1-x) is continuous on [-r,r]. This illustrates the uniform "
                "limit theorem: uniform convergence preserves continuity. "
                "Equicontinuous: the partial sums f_n are polynomials with bounded derivative "
                "|f_n'(x)| = |sum_{k=1}^{n} k x^{k-1}| <= sum k r^{k-1} = 1/(1-r)^2 on [-r,r], "
                "so {f_n} is a Lipschitz family with uniform constant L = 1/(1-r)^2. "
                "Dini applies: f_n is monotone increasing (all terms x^k are positive for "
                "x > 0, we can adapt), limit f is continuous, domain [-r,r] is compact. "
                "Arzelà-Ascoli: {f_n} is uniformly bounded and equicontinuous, so relatively "
                "compact in C([-r,r])."
            ),
            chapter_targets=("8", "18", "32"),
        ),
        UniformConvergenceProfile(
            key="dini_theorem_monotone",
            display_name="Dini's theorem — monotone pointwise convergence on compact space",
            convergence_type="uniform",
            is_uniform=True,
            is_equicontinuous=True,
            limit_is_continuous=True,
            is_relatively_compact=True,
            satisfies_dini=True,
            presentation_layer="main_text",
            focus=(
                "Dini's theorem (1878): let X be a compact topological space and (f_n) a "
                "sequence in C(X) converging pointwise to f in C(X). If the convergence is "
                "monotone (f_n(x) >= f_{n+1}(x) for all x, or <= for all x), then f_n -> f "
                "uniformly on X. "
                "Proof sketch: let g_n = f_n - f >= 0 (decreasing to 0 pointwise). Fix "
                "epsilon > 0. For each x in X, by pointwise convergence there exists N(x) "
                "with g_{N(x)}(x) < epsilon. By continuity of g_{N(x)}, there is an open "
                "U_x containing x with g_{N(x)} < epsilon on U_x. Since g_n is decreasing, "
                "g_n < epsilon on U_x for all n >= N(x). Cover X by finitely many U_{x_i} "
                "(compactness), let N = max N(x_i). Then g_n < epsilon on all X for n >= N. "
                "All three hypotheses are essential: "
                "(1) Compactness fails: f_n(x) = 1/(nx+1) on (0,1] — monotone decrease to 0, "
                "f = 0 continuous, but NOT uniform (f_n(1/n) = 1/2 for all n). "
                "(2) Continuity of f fails: f_n(x) = x^n on [0,1] — monotone, compact "
                "domain, but f is discontinuous at 1 and convergence is not uniform. "
                "(3) Monotonicity fails: f_n(x) = sin(nx)/n -> 0 uniformly, but this is "
                "uniform regardless; the non-monotone version g_n(x) = n x (1-x^2)^n on "
                "[0,1] is pointwise to 0 but not uniform (max at x = 1/sqrt(2n) ~ (n/2)^{1/2} "
                "gives g_n -> infty at its maximum normalized). "
                "Applications: convergence of Fourier series, Stone-Weierstrass argument, "
                "and functional analysis."
            ),
            chapter_targets=("8", "18", "32"),
        ),
        UniformConvergenceProfile(
            key="arzela_ascoli_c_of_compact",
            display_name="Arzelà-Ascoli theorem — compactness in C(X)",
            convergence_type="uniform",
            is_uniform=True,
            is_equicontinuous=True,
            limit_is_continuous=True,
            is_relatively_compact=True,
            satisfies_dini=False,
            presentation_layer="main_text",
            focus=(
                "Arzelà-Ascoli theorem: let X be a compact metric space. A subset F ⊆ C(X) "
                "is relatively compact in the sup-norm topology iff F is: "
                "(1) uniformly bounded: exists M > 0 with |f(x)| <= M for all f in F, x in X; "
                "(2) equicontinuous: for all epsilon > 0, exists delta > 0 such that "
                "    d(x,y) < delta implies |f(x)-f(y)| < epsilon for ALL f in F. "
                "Proof (sequential compactness): let (f_n) be a sequence in F. "
                "Step 1 (diagonal argument): let {x_k} be a countable dense set in X "
                "(compactness -> X is separable). By uniform boundedness and Bolzano-Weierstrass, "
                "extract a subsequence converging at x_1, then a further subsequence at x_2, etc. "
                "The diagonal subsequence (f_{n_k}) converges at every x_k. "
                "Step 2 (uniform): by equicontinuity, the convergence extends to all of X "
                "uniformly. For each epsilon > 0, cover X by finitely many delta-balls, "
                "use equicontinuity on each ball and convergence on the center. "
                "Applications: "
                "(1) Peano existence theorem (1890): the ODE y' = f(x,y), y(x_0) = y_0 "
                "    with f continuous has a local solution. Euler approximations form an "
                "    equicontinuous uniformly bounded family; Arzelà-Ascoli gives a convergent "
                "    subsequence. "
                "(2) Montel's theorem (complex analysis): a locally uniformly bounded family "
                "    of holomorphic functions is normal (has a locally uniformly convergent "
                "    subsequence). "
                "(3) Compactness in Sobolev spaces: the Rellich-Kondrachov theorem is an "
                "    Arzelà-Ascoli-type result for Sobolev embeddings."
            ),
            chapter_targets=("8", "18", "32"),
        ),
        UniformConvergenceProfile(
            key="stone_weierstrass",
            display_name="Stone-Weierstrass theorem — density of subalgebras in C(X)",
            convergence_type="uniform_approximation",
            is_uniform=True,
            is_equicontinuous=False,
            limit_is_continuous=True,
            is_relatively_compact=False,
            satisfies_dini=False,
            presentation_layer="main_text",
            focus=(
                "Stone-Weierstrass theorem (1937): let X be a compact Hausdorff space and "
                "A a subalgebra of C(X,R) (closed under addition, multiplication, scalar "
                "multiples) satisfying: "
                "(1) A separates points: for x ≠ y in X, exists f in A with f(x) ≠ f(y); "
                "(2) A contains the constants (or equivalently, 1 in A). "
                "Then A is dense in C(X,R) in the uniform norm — every continuous g: X -> R "
                "is the uniform limit of functions in A. "
                "Weierstrass's original theorem (1885): polynomials are dense in C([a,b]). "
                "Proof: A = {polynomials} separates points (p(x) = x), contains constants. "
                "Stone-Weierstrass generalizes to any compact Hausdorff space. "
                "Complex version: if A ⊆ C(X,C) separates points, contains constants, and "
                "is closed under complex conjugation, then A is dense in C(X,C). "
                "(Without conjugate-closure: C([0,1],C) contains the disc algebra — analytic "
                "functions — which is NOT dense, showing the hypothesis is necessary.) "
                "Applications: "
                "(1) Trigonometric polynomials {sum a_k e^{ikx}} are dense in C(T) where "
                "    T = R/Z — this is the Stone-Weierstrass basis for Fourier series. "
                "(2) Tensor products: if A ⊆ C(X) and B ⊆ C(Y) are dense, then A tensor B "
                "    = span{f tensor g : f in A, g in B} is dense in C(X x Y). "
                "(3) Compact operators: the finite-rank operators are dense in K(H), "
                "    analogous to polynomial approximation in function spaces."
            ),
            chapter_targets=("8", "18", "32"),
        ),
        UniformConvergenceProfile(
            key="compact_open_topology_cx",
            display_name="C(X,Y) with the compact-open topology",
            convergence_type="locally_uniform",
            is_uniform=False,
            is_equicontinuous=False,
            limit_is_continuous=True,
            is_relatively_compact=False,
            satisfies_dini=False,
            presentation_layer="selected_block",
            focus=(
                "The compact-open topology on C(X,Y) has subbasis sets "
                "V(K, U) = {f in C(X,Y) : f(K) ⊆ U} for K ⊆ X compact, U ⊆ Y open. "
                "Key facts: "
                "(1) For X compact and Y metric: the compact-open topology equals the "
                "    uniform topology (sup-norm topology). Proof: V(X, B(f(x), epsilon)) "
                "    for finitely many x cover X by compactness. "
                "(2) For X locally compact Hausdorff and Y metric: the compact-open topology "
                "    equals the topology of uniform convergence on compact subsets. "
                "    E.g., C(R, R) with compact-open = uniform on every [a,b]. "
                "(3) Exponential law: if X and Y are locally compact Hausdorff, then "
                "    C(X x Y, Z) ≅ C(X, C(Y, Z)) as topological spaces (homeomorphism). "
                "    This makes C(-,-) an 'internal hom' in the category of locally "
                "    compact Hausdorff spaces. "
                "(4) The compact-open topology makes composition continuous: "
                "    circ: C(X,Y) x C(Y,Z) -> C(X,Z) is continuous (when X compact). "
                "(5) For G a topological group acting continuously on X, the compact-open "
                "    topology on C(X,Y) is equivariant — the action G x C(X,Y) -> C(X,Y) "
                "    by (g·f)(x) = f(g^{-1}x) is continuous. "
                "The compact-open topology is the natural topology for function spaces in "
                "algebraic topology (path spaces, loop spaces), homotopy theory (homotopies "
                "are paths in C(X,Y)), and functional analysis (TVS of continuous functions)."
            ),
            chapter_targets=("8", "18"),
        ),
        UniformConvergenceProfile(
            key="lipschitz_equicontinuous_family",
            display_name="Lipschitz family with uniform constant — equicontinuity",
            convergence_type="equicontinuous",
            is_uniform=False,
            is_equicontinuous=True,
            limit_is_continuous=True,
            is_relatively_compact=True,
            satisfies_dini=False,
            presentation_layer="selected_block",
            focus=(
                "A family F of functions f: X -> Y between metric spaces is L-Lipschitz "
                "(uniformly) if d_Y(f(x), f(y)) <= L · d_X(x, y) for all f in F and all "
                "x, y in X. Such a family is equicontinuous: for given epsilon > 0, take "
                "delta = epsilon/L — independent of f in F. "
                "Key examples of equicontinuous families: "
                "(1) Solutions to y' = f(x,y) with |f| <= M: by the mean value theorem, "
                "    |y(x_1) - y(x_2)| <= M |x_1 - x_2| — the solution family is M-Lipschitz. "
                "(2) C^1 functions with uniformly bounded derivative: |f'| <= C implies "
                "    f is C-Lipschitz. "
                "(3) Convolutions f * phi_epsilon for approximate identities phi_epsilon: "
                "    the smoothed functions are equicontinuous on compact sets. "
                "(4) Harmonic functions on a domain with uniform L^infty bound: by Harnack's "
                "    inequality, they are equicontinuous on compact interior subsets. "
                "Arzelà-Ascoli for Lipschitz families: if F is uniformly bounded and "
                "L-Lipschitz, then every sequence in F has a uniformly convergent subsequence "
                "on any compact subset. The limit function is also L-Lipschitz (Lipschitz "
                "constant is preserved under uniform limits). "
                "The equicontinuity modulus omega(delta) = L·delta is shared: for all f in F, "
                "sup_{d(x,y)<delta} |f(x)-f(y)| <= L·delta. This is the quantitative version "
                "of equicontinuity used in Arzelà-Ascoli estimates."
            ),
            chapter_targets=("8", "18", "32"),
        ),
    )


def uniform_convergence_layer_summary() -> dict[str, int]:
    """Return a count of profiles by presentation_layer."""
    return dict(Counter(
        p.presentation_layer for p in get_named_uniform_convergence_profiles()
    ))


def uniform_convergence_chapter_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from chapter number to profile keys."""
    chapter_map: dict[str, list[str]] = {}
    for p in get_named_uniform_convergence_profiles():
        for chapter in p.chapter_targets:
            chapter_map.setdefault(chapter, []).append(p.key)
    return {chapter: tuple(keys) for chapter, keys in sorted(chapter_map.items())}


def uniform_convergence_type_index() -> dict[str, tuple[str, ...]]:
    """Return a mapping from convergence_type to profile keys."""
    index: dict[str, list[str]] = {}
    for p in get_named_uniform_convergence_profiles():
        index.setdefault(p.convergence_type, []).append(p.key)
    return {k: tuple(v) for k, v in sorted(index.items())}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def is_uniformly_convergent(space: Any) -> Result:
    """Check whether the function sequence / family converges uniformly.

    A sequence (f_n) converges uniformly to f if:
    for every epsilon > 0, exists N such that n >= N implies
    d(f_n(x), f(x)) < epsilon for ALL x simultaneously.
    Key facts:
    - Uniform convergence implies pointwise convergence; the converse fails.
    - Uniform limits of continuous functions are continuous.
    - Dominated convergence (Weierstrass M-test): if |f_n(x)| <= M_n and sum M_n < infty,
      then sum f_n converges uniformly and absolutely.

    Decision layers
    ---------------
    1. Explicit 'uniform_convergence' or sup-norm tag -> true.
    2. Dini condition (monotone + compact + continuous limit) -> true.
    3. Arzelà-Ascoli compact family -> true (subsequential uniform convergence).
    4. Pointwise-only or not-uniform tags -> false.
    5. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, UNIFORM_CONVERGENCE_TAGS):
        witness = next(t for t in tags if t in UNIFORM_CONVERGENCE_TAGS)
        return Result.true(
            mode="theorem",
            value="uniform_convergence",
            justification=[
                f"Tag {witness!r}: the sequence converges uniformly — the sup-norm "
                "||f_n - f||_infty -> 0. A single N works for all x simultaneously.",
            ],
            metadata={**base, "criterion": "explicit_uniform", "witness": witness},
        )

    if _matches_any(tags, DINI_THEOREM_TAGS):
        witness = next(t for t in tags if t in DINI_THEOREM_TAGS)
        return Result.true(
            mode="theorem",
            value="uniform_convergence",
            justification=[
                f"Tag {witness!r}: Dini's theorem applies — monotone pointwise convergence "
                "to a continuous limit on a compact space implies uniform convergence.",
            ],
            metadata={**base, "criterion": "dini_theorem", "witness": witness},
        )

    if _matches_any(tags, ARZELA_ASCOLI_TAGS):
        witness = next(t for t in tags if t in ARZELA_ASCOLI_TAGS)
        return Result.true(
            mode="theorem",
            value="uniform_convergence",
            justification=[
                f"Tag {witness!r}: the Arzelà-Ascoli theorem applies — uniformly bounded "
                "and equicontinuous families contain uniformly convergent subsequences.",
            ],
            metadata={**base, "criterion": "arzela_ascoli", "witness": witness},
        )

    if _matches_any(tags, POINTWISE_ONLY_TAGS):
        blocking = next(t for t in tags if t in POINTWISE_ONLY_TAGS)
        return Result.false(
            mode="theorem",
            value="uniform_convergence",
            justification=[
                f"Tag {blocking!r}: convergence is pointwise but NOT uniform. "
                "The canonical example f_n(x) = x^n on [0,1] has sup-norm = 1 for all n.",
            ],
            metadata={**base, "criterion": "pointwise_only"},
        )

    return Result.unknown(
        mode="symbolic",
        value="uniform_convergence",
        justification=[
            "Insufficient tags to determine uniform convergence. "
            "Supply tags such as 'uniform_convergence', 'sup_norm_convergence', "
            "'dini_theorem', 'arzela_ascoli', 'pointwise_only', or 'not_uniform'.",
        ],
        metadata={**base, "criterion": None},
    )


def is_equicontinuous(space: Any) -> Result:
    """Check whether the function family is equicontinuous.

    A family F of functions X -> Y is equicontinuous at x_0 if for every epsilon > 0
    there exists delta > 0 (independent of f in F) such that d(x, x_0) < delta implies
    d(f(x), f(x_0)) < epsilon for ALL f in F. Key examples:
    - Lipschitz families with uniform constant are equicontinuous.
    - Solutions to y' = g(x,y) with |g| <= M are M-Lipschitz, hence equicontinuous.
    - The power sequence f_n(x) = x^n on [0,1] is NOT equicontinuous at x=1.

    Decision layers
    ---------------
    1. Explicit 'equicontinuous' or Lipschitz-family tag -> true.
    2. Not-equicontinuous or pointwise-only tags -> false.
    3. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, EQUICONTINUOUS_TAGS):
        witness = next(t for t in tags if t in EQUICONTINUOUS_TAGS)
        return Result.true(
            mode="theorem",
            value="equicontinuous",
            justification=[
                f"Tag {witness!r}: the family is equicontinuous — a single modulus of "
                "continuity omega(delta) works for all functions in F simultaneously. "
                "Lipschitz families with uniform constant L share omega(delta) = L·delta.",
            ],
            metadata={**base, "criterion": "explicit_equicontinuous", "witness": witness},
        )

    if _matches_any(tags, NOT_EQUICONTINUOUS_TAGS):
        blocking = next(t for t in tags if t in NOT_EQUICONTINUOUS_TAGS)
        return Result.false(
            mode="theorem",
            value="equicontinuous",
            justification=[
                f"Tag {blocking!r}: the family is NOT equicontinuous — no single delta "
                "works for all functions. The sequence f_n(x) = x^n on [0,1] fails "
                "equicontinuity at x=1: for any delta, some f_n oscillates by 1/2 near 1.",
            ],
            metadata={**base, "criterion": "not_equicontinuous"},
        )

    return Result.unknown(
        mode="symbolic",
        value="equicontinuous",
        justification=[
            "Insufficient tags to determine equicontinuity. "
            "Supply tags such as 'equicontinuous', 'lipschitz_family', "
            "'holder_family', 'not_equicontinuous', or 'power_function_sequence'.",
        ],
        metadata={**base, "criterion": None},
    )


def satisfies_arzela_ascoli(space: Any) -> Result:
    """Check whether the function family satisfies the Arzelà-Ascoli conditions.

    The Arzelà-Ascoli theorem states that F ⊆ C(X) is relatively compact iff:
    (1) F is uniformly bounded (exists M: |f(x)| <= M for all f in F, x in X);
    (2) F is equicontinuous.
    When these hold, every sequence in F has a uniformly convergent subsequence.

    Decision layers
    ---------------
    1. Explicit 'arzela_ascoli' or 'uniformly_bounded_equicontinuous' tag -> true.
    2. Lipschitz family on compact domain (bounded + equicontinuous) -> true.
    3. Not-equicontinuous or not-relatively-compact tags -> false.
    4. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, ARZELA_ASCOLI_TAGS):
        witness = next(t for t in tags if t in ARZELA_ASCOLI_TAGS)
        return Result.true(
            mode="theorem",
            value="arzela_ascoli",
            justification=[
                f"Tag {witness!r}: the Arzelà-Ascoli conditions hold — the family is "
                "uniformly bounded and equicontinuous on a compact domain. Every sequence "
                "has a uniformly convergent subsequence (relative compactness in C(X)).",
            ],
            metadata={**base, "criterion": "explicit_arzela_ascoli", "witness": witness},
        )

    if _matches_any(tags, EQUICONTINUOUS_TAGS) and _matches_any(
        tags, {"uniformly_bounded", "bounded_family", "lipschitz_family",
               "holder_family", "bounded_derivative_family"}
    ):
        witness = next(t for t in tags if t in EQUICONTINUOUS_TAGS)
        return Result.true(
            mode="theorem",
            value="arzela_ascoli",
            justification=[
                f"Tag {witness!r} with bounded family: equicontinuous + uniformly bounded "
                "implies Arzelà-Ascoli — the family is relatively compact in C(X).",
            ],
            metadata={**base, "criterion": "equicontinuous_and_bounded"},
        )

    if _matches_any(tags, NOT_RELATIVELY_COMPACT_TAGS):
        blocking = next(t for t in tags if t in NOT_RELATIVELY_COMPACT_TAGS)
        return Result.false(
            mode="theorem",
            value="arzela_ascoli",
            justification=[
                f"Tag {blocking!r}: Arzelà-Ascoli conditions fail. The family is either "
                "not equicontinuous or not uniformly bounded — no convergent subsequence "
                "is guaranteed. Example: f_n(x) = x^n on [0,1] fails equicontinuity.",
            ],
            metadata={**base, "criterion": "not_arzela_ascoli"},
        )

    return Result.unknown(
        mode="symbolic",
        value="arzela_ascoli",
        justification=[
            "Insufficient tags to determine Arzelà-Ascoli conditions. "
            "Supply tags such as 'arzela_ascoli', 'equicontinuous', 'uniformly_bounded', "
            "'lipschitz_family', 'not_equicontinuous', or 'not_relatively_compact'.",
        ],
        metadata={**base, "criterion": None},
    )


def satisfies_dini(space: Any) -> Result:
    """Check whether Dini's theorem applies (monotone pointwise → uniform).

    Dini's theorem: (f_n) ⊆ C(X), X compact, f_n -> f pointwise with f in C(X),
    and convergence is monotone (f_n >= f_{n+1} >= f, or <=) implies f_n -> f uniformly.
    All three conditions (compactness, continuity of f, monotonicity) are necessary.

    Decision layers
    ---------------
    1. Explicit 'dini_theorem' or 'monotone_convergence_compact' tag -> true.
    2. Discontinuous limit or non-compact domain -> false.
    3. Unknown otherwise.
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)
    base: dict[str, Any] = {"representation": representation, "tags": sorted(tags)}

    if _matches_any(tags, DINI_THEOREM_TAGS):
        witness = next(t for t in tags if t in DINI_THEOREM_TAGS)
        return Result.true(
            mode="theorem",
            value="dini_theorem",
            justification=[
                f"Tag {witness!r}: Dini's theorem applies — monotone pointwise convergence "
                "to a continuous limit on a compact space implies uniform convergence.",
            ],
            metadata={**base, "criterion": "explicit_dini", "witness": witness},
        )

    dini_fails = {
        "discontinuous_pointwise_limit",
        "non_compact_domain",
        "not_monotone_convergence",
        "power_function_sequence",
        "pointwise_not_uniform",
    }
    if _matches_any(tags, dini_fails):
        blocking = next(t for t in tags if t in dini_fails)
        return Result.false(
            mode="theorem",
            value="dini_theorem",
            justification=[
                f"Tag {blocking!r}: Dini's theorem does NOT apply. A necessary condition "
                "fails: either the limit is discontinuous, the domain is non-compact, or "
                "the convergence is not monotone.",
            ],
            metadata={**base, "criterion": "dini_fails"},
        )

    return Result.unknown(
        mode="symbolic",
        value="dini_theorem",
        justification=[
            "Insufficient tags to determine Dini applicability. "
            "Supply tags such as 'dini_theorem', 'monotone_convergence_compact', "
            "'discontinuous_pointwise_limit', 'non_compact_domain', or 'not_monotone_convergence'.",
        ],
        metadata={**base, "criterion": None},
    )


def classify_uniform_convergence(space: Any) -> dict[str, Any]:
    """Classify the convergence type of the function sequence / family.

    Keys
    ----
    convergence_class : str
        One of ``"uniform"``, ``"dini"``, ``"arzela_ascoli"``,
        ``"equicontinuous_only"``, ``"pointwise_only"``, ``"unknown"``.
    is_uniformly_convergent : Result
    is_equicontinuous : Result
    satisfies_arzela_ascoli : Result
    satisfies_dini : Result
    key_properties : list[str]
    representation : str
    tags : list[str]
    """
    tags = _extract_tags(space)
    representation = _representation_of(space)

    uniform_r = is_uniformly_convergent(space)
    equi_r = is_equicontinuous(space)
    ascoli_r = satisfies_arzela_ascoli(space)
    dini_r = satisfies_dini(space)

    if dini_r.is_true:
        convergence_class = "dini"
    elif uniform_r.is_true and ascoli_r.is_true:
        convergence_class = "arzela_ascoli"
    elif uniform_r.is_true:
        convergence_class = "uniform"
    elif equi_r.is_true and not uniform_r.is_true:
        convergence_class = "equicontinuous_only"
    elif uniform_r.is_false:
        convergence_class = "pointwise_only"
    else:
        convergence_class = "unknown"

    key_properties: list[str] = []
    if uniform_r.is_true:
        key_properties.append("uniform_convergence")
    if uniform_r.is_false:
        key_properties.append("not_uniform")
    if equi_r.is_true:
        key_properties.append("equicontinuous")
    if equi_r.is_false:
        key_properties.append("not_equicontinuous")
    if ascoli_r.is_true:
        key_properties.append("relatively_compact")
    if dini_r.is_true:
        key_properties.append("dini_applicable")
    if _matches_any(tags, STONE_WEIERSTRASS_TAGS):
        key_properties.append("stone_weierstrass")
    if _matches_any(tags, COMPACT_OPEN_TAGS):
        key_properties.append("compact_open_topology")

    return {
        "convergence_class": convergence_class,
        "is_uniformly_convergent": uniform_r,
        "is_equicontinuous": equi_r,
        "satisfies_arzela_ascoli": ascoli_r,
        "satisfies_dini": dini_r,
        "key_properties": key_properties,
        "representation": representation,
        "tags": sorted(tags),
    }


def uniform_convergence_profile(space: Any) -> dict[str, Any]:
    """Full uniform convergence profile combining classification and named examples.

    Keys
    ----
    classification : dict
        Output of :func:`classify_uniform_convergence`.
    named_profiles : tuple[UniformConvergenceProfile, ...]
        Registry of canonical uniform convergence examples.
    layer_summary : dict[str, int]
        Profile count by presentation_layer.
    """
    return {
        "classification": classify_uniform_convergence(space),
        "named_profiles": get_named_uniform_convergence_profiles(),
        "layer_summary": uniform_convergence_layer_summary(),
    }


__all__ = [
    "UniformConvergenceProfile",
    "UNIFORM_CONVERGENCE_TAGS",
    "POINTWISE_ONLY_TAGS",
    "EQUICONTINUOUS_TAGS",
    "NOT_EQUICONTINUOUS_TAGS",
    "ARZELA_ASCOLI_TAGS",
    "DINI_THEOREM_TAGS",
    "STONE_WEIERSTRASS_TAGS",
    "COMPACT_OPEN_TAGS",
    "NOT_RELATIVELY_COMPACT_TAGS",
    "get_named_uniform_convergence_profiles",
    "uniform_convergence_layer_summary",
    "uniform_convergence_chapter_index",
    "uniform_convergence_type_index",
    "is_uniformly_convergent",
    "is_equicontinuous",
    "satisfies_arzela_ascoli",
    "satisfies_dini",
    "classify_uniform_convergence",
    "uniform_convergence_profile",
]
