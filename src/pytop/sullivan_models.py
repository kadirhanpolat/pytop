"""Sullivan minimal models for formal spaces (Phase 13.5).

A Sullivan algebra (ΛV, d) over ℚ is a free commutative graded algebra
on a graded vector space V = ⊕_{n≥1} V^n, equipped with a decomposable
differential d: ΛV → ΛV (d(V^n) ⊆ Λ⁺V · Λ⁺V = (ΛV)^{≥2} in low degrees).

A Sullivan algebra is *minimal* if d(V^n) ⊆ Λ(V^{<n}) (the image of d
involves only generators of strictly smaller degree).

A space X is *formal* if its minimal Sullivan model can be connected to
(H*(X;ℚ), 0) by a zig-zag of quasi-isomorphisms of cdgas (commutative
differential graded algebras).  For formal spaces the minimal model is
determined by the cohomology ring alone.

Key minimal Sullivan models
---------------------------
S^n (n odd):
    ΛV = Λ(e_n),  d(e_n) = 0.
    H*(ΛV, d) = ℚ ⊕ ℚ[-n].  Formal.

S^n (n even):
    ΛV = Λ(e_n, f_{2n-1}),  |e_n|=n, |f_{2n-1}|=2n-1,
    d(e_n)=0,  d(f_{2n-1})=e_n².
    H*(ΛV, d) = ℚ[e_n]/(e_n²) ⊕ ℚ[-n] (top class).  Formal.

T^r (r-torus):
    ΛV = Λ(x_1, …, x_r),  |x_i|=1,  d=0.
    H*(ΛV) = Λ(x_1,…,x_r) = ∧^*(ℚ^r).  Formal (all Massey products vanish).

CP^n:
    ΛV = Λ(e_2, f_{2n+1}),  |e_2|=2, |f_{2n+1}|=2n+1,
    d(e_2)=0, d(f_{2n+1})=e_2^{n+1}.
    H*(ΛV) = ℚ[e_2]/(e_2^{n+1}).  Formal.

CP^∞ = K(ℤ, 2):
    ΛV = ℚ[e_2],  |e_2|=2,  d=0 (polynomial in even degree).
    H*(ΛV) = ℚ[e_2] (power series in cohomological sense).  Formal.

K(ℤ, 1) = S¹:
    ΛV = Λ(e_1),  d=0.  Same as S¹ = S^1 (n=1 odd).

Rational homotopy groups from Sullivan models:
    π_n(X) ⊗ ℚ = (V^n)* for the minimal Sullivan model (ΛV, d) of X.
    The generators in degree n give the rational n-th homotopy group.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

__all__ = [
    "SullivanGenerator",
    "SullivanModel",
    "sullivan_sphere",
    "sullivan_torus",
    "sullivan_complex_projective",
    "sullivan_cp_infinity",
    "sullivan_k_z1",
    "sullivan_wedge_circles",
    "sullivan_product",
    "pi_rational",
    "euler_characteristic_sullivan",
    "poincare_series_sullivan",
    "is_pure_sullivan",
    "sullivan_from_betti",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SullivanGenerator:
    """A single generator of a Sullivan algebra.

    Attributes
    ----------
    name : str
        Symbol (e.g. ``"e_2"``).
    degree : int
        Cohomological degree |x| ≥ 1.
    parity : str
        ``"even"`` if degree is even (polynomial generator),
        ``"odd"`` if degree is odd (exterior generator).
    differential : str
        Human-readable expression for d(x) (e.g. ``"e_2^2"`` or ``"0"``).
    differential_degree : int
        Degree of d(x) = degree + 1.
    """

    name: str
    degree: int
    parity: str
    differential: str
    differential_degree: int

    @classmethod
    def make(cls, name: str, degree: int, differential: str = "0") -> SullivanGenerator:
        return cls(
            name=name,
            degree=degree,
            parity="even" if degree % 2 == 0 else "odd",
            differential=differential,
            differential_degree=degree + 1,
        )


@dataclass(frozen=True)
class SullivanModel:
    """A minimal Sullivan model (ΛV, d) over ℚ.

    Attributes
    ----------
    space_name : str
        Name of the space this models (e.g. ``"S²"``).
    generators : tuple[SullivanGenerator, ...]
        Ordered generators of V, by increasing degree.
    is_formal : bool
        True iff this is a formal space (cohomology determines model).
    cohomology_description : str
        Description of H*(X; ℚ).
    rational_homotopy : dict[int, int]
        Rank of π_n(X) ⊗ ℚ = #{generators in degree n} for each n.
    """

    space_name: str
    generators: tuple[SullivanGenerator, ...]
    is_formal: bool
    cohomology_description: str
    rational_homotopy: dict[int, int]

    def describe(self) -> str:
        gen_str = ", ".join(
            f"{g.name} (deg={g.degree}, d={g.differential})"
            for g in self.generators
        )
        return (
            f"Sullivan model of {self.space_name}:\n"
            f"  Generators: {gen_str or 'none'}\n"
            f"  H*(X;ℚ): {self.cohomology_description}\n"
            f"  Formal: {self.is_formal}\n"
            f"  π_*(X)⊗ℚ: {self.rational_homotopy}"
        )

    def generator_names(self) -> tuple[str, ...]:
        return tuple(g.name for g in self.generators)

    def generators_in_degree(self, n: int) -> list[SullivanGenerator]:
        return [g for g in self.generators if g.degree == n]


# ---------------------------------------------------------------------------
# Standard Sullivan models
# ---------------------------------------------------------------------------


def sullivan_sphere(n: int) -> SullivanModel:
    """Minimal Sullivan model of S^n.

    S^n (n odd): ΛV = Λ(e_n), d=0.  π_n⊗ℚ = ℚ, π_k⊗ℚ = 0 for k ≠ n.

    S^n (n even, n ≥ 2): ΛV = Λ(e_n, f_{2n-1}), d(e_n)=0, d(f)=e_n².
                          π_n⊗ℚ = π_{2n-1}⊗ℚ = ℚ, others 0.

    Parameters
    ----------
    n : int
        Sphere dimension, n ≥ 1.
    """
    if n < 1:
        raise ValueError(f"Sphere dimension must be ≥ 1; got {n}.")
    gens: tuple[SullivanGenerator, ...]
    if n % 2 == 1:
        gens = (SullivanGenerator.make(f"e_{n}", n, "0"),)
        rat_hmtp = {n: 1}
        cohom = f"ℚ ⊕ ℚ[-{n}]  (H^0=ℚ, H^{n}=ℚ, else 0)"
    else:
        e = SullivanGenerator.make(f"e_{n}", n, "0")
        f2 = SullivanGenerator.make(f"f_{2*n-1}", 2 * n - 1, f"e_{n}^2")
        gens = (e, f2)
        rat_hmtp = {n: 1, 2 * n - 1: 1}
        cohom = f"ℚ ⊕ ℚ[-{n}]  (H^0=ℚ, H^{n}=ℚ, else 0)"
    return SullivanModel(
        space_name=f"S^{n}",
        generators=gens,
        is_formal=True,
        cohomology_description=cohom,
        rational_homotopy=rat_hmtp,
    )


def sullivan_torus(r: int) -> SullivanModel:
    """Minimal Sullivan model of the r-torus T^r = (S¹)^r.

    ΛV = Λ(x_1, …, x_r), |x_i|=1, d=0.
    H*(T^r; ℚ) = ∧^*(ℚ^r) with β_k = C(r,k).
    π_1⊗ℚ = ℚ^r, π_k⊗ℚ = 0 for k ≥ 2 (T^r = K(ℤ^r,1) is formal).

    Parameters
    ----------
    r : int
        Number of circle factors, r ≥ 0.
    """
    if r < 0:
        raise ValueError(f"r must be ≥ 0; got {r}.")
    gens = tuple(SullivanGenerator.make(f"x_{i+1}", 1, "0") for i in range(r))
    [comb(r, k) for k in range(r + 1)]
    betti_str = ", ".join(f"β_{k}={comb(r,k)}" for k in range(r + 1))
    rat_hmtp: dict[int, int] = {1: r} if r > 0 else {}
    return SullivanModel(
        space_name=f"T^{r}",
        generators=gens,
        is_formal=True,
        cohomology_description=f"∧*(ℚ^{r}): {betti_str}",
        rational_homotopy=rat_hmtp,
    )


def sullivan_complex_projective(n: int) -> SullivanModel:
    """Minimal Sullivan model of CP^n (complex projective n-space).

    ΛV = Λ(e_2, f_{2n+1}), |e_2|=2, |f|=2n+1.
    d(e_2)=0, d(f_{2n+1})=e_2^{n+1}.
    H*(CP^n; ℚ) = ℚ[e_2]/(e_2^{n+1}).
    π_2⊗ℚ = ℚ, π_{2n+1}⊗ℚ = ℚ, others 0.
    Formal (Kähler manifold).

    Parameters
    ----------
    n : int
        Complex dimension, n ≥ 1.
    """
    if n < 1:
        raise ValueError(f"CP^n requires n ≥ 1; got {n}.")
    e2 = SullivanGenerator.make("e_2", 2, "0")
    f2n1 = SullivanGenerator.make(f"f_{2*n+1}", 2 * n + 1, f"e_2^{n+1}")
    rat_hmtp: dict[int, int] = {2: 1, 2 * n + 1: 1}
    cohom = f"ℚ[e₂]/(e₂^{{n+1}}) = ℚ ⊕ ℚe₂ ⊕ … ⊕ ℚe₂^{n}  (degrees 0, 2, …, 2n)"
    return SullivanModel(
        space_name=f"CP^{n}",
        generators=(e2, f2n1),
        is_formal=True,
        cohomology_description=cohom,
        rational_homotopy=rat_hmtp,
    )


def sullivan_cp_infinity() -> SullivanModel:
    """Minimal Sullivan model of CP^∞ = K(ℤ, 2).

    ΛV = ℚ[e_2], |e_2|=2, d=0.  (Polynomial algebra on one even generator.)
    H*(CP^∞; ℚ) = ℚ[e_2].
    π_2⊗ℚ = ℚ, π_k⊗ℚ = 0 for k ≠ 2.
    Formal (it is K(ℤ,2) hence a K(G,n) space).
    """
    e2 = SullivanGenerator.make("e_2", 2, "0")
    return SullivanModel(
        space_name="CP^∞ = K(ℤ, 2)",
        generators=(e2,),
        is_formal=True,
        cohomology_description="ℚ[e₂]  (polynomial in degree 2)",
        rational_homotopy={2: 1},
    )


def sullivan_k_z1() -> SullivanModel:
    """Minimal Sullivan model of K(ℤ, 1) = S¹.

    Same as sullivan_sphere(1).
    """
    return sullivan_sphere(1)


def sullivan_wedge_circles(r: int) -> SullivanModel:
    """Minimal Sullivan model of ∨_r S¹ = K(F_r, 1).

    ΛV = Λ(x_1, …, x_r, y_{12}, y_{13}, …),  d=0 for generators.
    In fact the Sullivan model of a wedge of circles is more complex
    because H_2 ≠ 0 in general (it contains the commutators).

    For r = 1: same as S¹.
    For r ≥ 2: the minimal Sullivan model requires generators in all degrees
    (it is not finite-dimensional): x_1,…,x_r in degree 1 and infinitely many
    generators in higher degrees for the Massey products / iterated brackets.
    Here we return the *truncated* model keeping only degree-1 generators and
    noting the infinite structure.

    Parameters
    ----------
    r : int
        Number of circles in the wedge.
    """
    if r < 0:
        raise ValueError("r must be ≥ 0.")
    if r == 0:
        return SullivanModel(
            space_name="point",
            generators=(),
            is_formal=True,
            cohomology_description="ℚ",
            rational_homotopy={},
        )
    if r == 1:
        return sullivan_k_z1()
    gens = tuple(SullivanGenerator.make(f"x_{i+1}", 1, "0") for i in range(r))
    return SullivanModel(
        space_name=f"∨_{r} S¹ = K(F_{r},1)",
        generators=gens,
        is_formal=False,
        cohomology_description=(
            f"H⁰=ℚ, H¹=ℚ^{r}, H^k=0 for k≥2  "
            f"(rational; the full Sullivan model has generators in all degrees)"
        ),
        rational_homotopy={1: r},
    )


def sullivan_product(M1: SullivanModel, M2: SullivanModel) -> SullivanModel:
    """Sullivan model of the product space M1 × M2.

    (ΛV₁ ⊗ ΛV₂, d₁ ⊗ 1 + 1 ⊗ d₂): generators are the union of
    generators of M1 and M2 (with d unchanged).
    Formality is preserved under products.

    Parameters
    ----------
    M1, M2 : SullivanModel
        Sullivan models of two spaces.
    """
    # Rename generators if names clash
    names1 = {g.name for g in M1.generators}
    new_gens2: list[SullivanGenerator] = []
    for g in M2.generators:
        name = g.name
        if name in names1:
            name = name + "'"
        new_gens2.append(SullivanGenerator(
            name=name,
            degree=g.degree,
            parity=g.parity,
            differential=g.differential.replace(g.name, name) if g.differential != "0" else "0",
            differential_degree=g.differential_degree,
        ))
    all_gens = tuple(sorted(M1.generators + tuple(new_gens2), key=lambda g: g.degree))
    combined_homotopy: dict[int, int] = {}
    for n, k in M1.rational_homotopy.items():
        combined_homotopy[n] = combined_homotopy.get(n, 0) + k
    for n, k in M2.rational_homotopy.items():
        combined_homotopy[n] = combined_homotopy.get(n, 0) + k

    return SullivanModel(
        space_name=f"({M1.space_name}) × ({M2.space_name})",
        generators=all_gens,
        is_formal=M1.is_formal and M2.is_formal,
        cohomology_description=f"H*({M1.space_name}) ⊗ H*({M2.space_name})",
        rational_homotopy=combined_homotopy,
    )


# ---------------------------------------------------------------------------
# Derived data
# ---------------------------------------------------------------------------


def pi_rational(model: SullivanModel, n: int) -> int:
    """Rank of π_n(X) ⊗ ℚ from the Sullivan model.

    For the minimal Sullivan model (ΛV, d): rank(π_n(X) ⊗ ℚ) = dim V^n.
    """
    return model.rational_homotopy.get(n, 0)


def euler_characteristic_sullivan(model: SullivanModel, max_degree: int) -> int:
    """Euler characteristic from the Sullivan model.

    χ(X) = Σ (-1)^n β_n where β_n = dim H^n(X; ℚ).  We compute the Hilbert
    series of the cohomology ring directly from the free graded-commutative
    algebra (ΛV, d):

    * an *odd*-degree generator contributes an exterior factor (1 + t^|x|);
    * an *even*-degree generator contributes a polynomial factor 1/(1 - t^|x|),
      truncated at the relation imposed by a differential d(f) = x^k
      (so the polynomial ℚ[x] becomes ℚ[x]/(x^k));
    * a generator that *is* such a differential's source (its differential is
      non-trivial) is acyclic and contributes nothing on its own.

    This gives the exact Betti numbers for the standard formal models:
    χ(T^r) = 0 (any odd generator forces a (1 + (-1))=0 factor),
    χ(S^{2k}) = 2, χ(S^{2k+1}) = 0, χ(CP^n) = n + 1.

    Parameters
    ----------
    model : SullivanModel
    max_degree : int
        Truncate the Hilbert series at this cohomological degree.
    """
    # Record polynomial truncations x^k = 0 coming from differentials d(f)=x^k.
    truncations: dict[str, int] = {}
    acyclic: set[str] = set()
    for g in model.generators:
        if g.differential != "0":
            acyclic.add(g.name)
            base, _, power_str = g.differential.rpartition("^")
            if base:
                try:
                    truncations[base] = int(power_str)
                except ValueError:
                    pass

    # Build the Hilbert series (graded dimension) up to max_degree.
    hilbert: dict[int, int] = {0: 1}
    for g in model.generators:
        if g.name in acyclic:
            continue
        d = g.degree
        new: dict[int, int] = {}
        if d % 2 == 1:
            # Exterior generator: factor (1 + t^d).
            for k, v in hilbert.items():
                new[k] = new.get(k, 0) + v
                if k + d <= max_degree:
                    new[k + d] = new.get(k + d, 0) + v
        else:
            # Polynomial generator, possibly truncated by x^limit = 0.
            limit = truncations.get(g.name)
            for k, v in hilbert.items():
                power = 0
                while k + power * d <= max_degree and (limit is None or power < limit):
                    new[k + power * d] = new.get(k + power * d, 0) + v
                    power += 1
        hilbert = new

    return sum((-1) ** n * c for n, c in hilbert.items())


def poincare_series_sullivan(
    model: SullivanModel,
    max_degree: int,
) -> dict[int, int]:
    """Poincaré polynomial (rational Betti numbers) of the Sullivan model.

    Returns {n: β_n} for n = 0, …, max_degree using the number of generators
    in each degree (exact for zero-differential Sullivan models).
    """
    betti: dict[int, int] = {0: 1}
    for g in model.generators:
        if g.degree <= max_degree:
            betti[g.degree] = betti.get(g.degree, 0) + 1
    return betti


def is_pure_sullivan(model: SullivanModel) -> bool:
    """Return True iff the model is *pure*: all generators are in even degree.

    Pure Sullivan algebras correspond to rationally elliptic spaces with only
    even-dimensional cells (e.g. CP^n, HP^n, Sp(n)).
    """
    return all(g.degree % 2 == 0 for g in model.generators)


def sullivan_from_betti(
    betti: list[int],
    space_name: str = "X",
) -> SullivanModel:
    """Construct the Sullivan model of a formal space from its Betti numbers.

    For a formal space with cohomology H*(X;ℚ) described by Betti numbers
    β_0, β_1, …, the minimal Sullivan model has:
      - β_n generators in degree n with d = 0  (for n = 1, or n odd)
      - Additional generators to kill even-degree classes (d ≠ 0) for n even

    This function returns the simplest model consistent with the Betti
    numbers, assuming zero differential (valid for formal spaces where the
    generators represent actual cohomology classes).

    Parameters
    ----------
    betti : list[int]
        Betti numbers β_0, β_1, β_2, … (β_0 should equal 1 for connected).
    space_name : str
        Name of the space.
    """
    gens: list[SullivanGenerator] = []
    rat_hmtp: dict[int, int] = {}
    for n, b in enumerate(betti):
        if n == 0:
            continue
        for i in range(b):
            name = f"x_{n}_{i+1}" if b > 1 else f"x_{n}"
            gens.append(SullivanGenerator.make(name, n, "0"))
        if b > 0:
            rat_hmtp[n] = b
    betti_str = ", ".join(f"β_{n}={b}" for n, b in enumerate(betti))
    return SullivanModel(
        space_name=space_name,
        generators=tuple(sorted(gens, key=lambda g: g.degree)),
        is_formal=True,
        cohomology_description=f"Formal: {betti_str}",
        rational_homotopy=rat_hmtp,
    )
