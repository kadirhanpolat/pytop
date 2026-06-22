"""Phase-9 Space representations.

Six new canonical infinite-space representations expanding the computable-space
protocol from 13 to 19 representations:

* :class:`OnePointCompactificationSpace` — Alexandroff extension αX = X ∪ {∞}
* :class:`StoneCechSpace` — Stone–Čech compactification βℕ
* :class:`HilbertCubeSpace` — the Hilbert cube [0,1]^ω
* :class:`SolenoidSpace` — the dyadic solenoid Σ = lim←{S¹ ←² S¹ ←² …}
* :class:`UniformSpace` — uniform structure via ε-entourages; with
  :class:`UniformProduct` and :class:`UniformSubspace` construction wrappers
* :class:`ProfiniteSpace` — inverse limit of finite discrete groups;
  factory :func:`p_adic_integers` builds ℤ_p
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from fractions import Fraction
from typing import Any

from .core import CardinalValue, CarrierKind, NotEnumerableError, Space, Verdict

# ---------------------------------------------------------------------------
# P9.1  OnePointCompactificationSpace
# ---------------------------------------------------------------------------


class OnePointCompactificationSpace(Space):
    """The Alexandroff one-point compactification αX = X ∪ {∞}.

    Open sets of αX:
    - Every open set U of the base space X (not containing ∞).
    - Every set U ∪ {∞} where U is open in X — equivalently (X \\ K) ∪ {∞}
      for each compact-and-closed K ⊆ X.  For finite X every closed set is
      compact, so every open U of X gives an open neighbourhood U ∪ {∞} of ∞.

    When X is compact (including all finite spaces) the point ∞ is isolated:
    {∞} is open (taking K = X) and X = αX \\ {∞} is open, so αX = X ⊔ {∞}.

    Key facts:
    - compact: always (by construction)
    - T2: iff X is locally compact Hausdorff
    - T0/T1: inherited from X
    - Lindelöf: compact implies Lindelöf
    """

    INFINITY: str = "∞"

    def __init__(self, base: Space, name: str | None = None) -> None:
        self._base = base
        self.name = name or f"α({base.name})"
        self.carrier_kind = base.carrier_kind

        if base.is_finite():
            base_opens = list(base.open_sets())
            base_pts: frozenset[Any] = frozenset(base.points())
            opens: set[frozenset[Any]] = set()
            for u in base_opens:
                u_fs = frozenset(u)
                opens.add(u_fs)
                opens.add(u_fs | frozenset([self.INFINITY]))
            self._opens: frozenset[frozenset[Any]] = frozenset(opens)
            self._carrier: frozenset[Any] = base_pts | frozenset([self.INFINITY])
        else:
            self._opens = frozenset()
            self._carrier = frozenset()

    def contains(self, point: Any) -> bool:
        if point == self.INFINITY:
            return True
        return bool(self._base.contains(point))

    def points(self) -> Iterable[Any]:
        if not self._base.is_finite():
            raise NotEnumerableError(f"{self.name!r}: base space is not finite")
        return tuple(self._carrier)

    def open_sets(self) -> frozenset[frozenset[Any]]:
        if not self._base.is_finite():
            raise NotEnumerableError(f"{self.name!r}: base space is not finite")
        return self._opens

    def point_separation(self, x: Any, y: Any) -> Verdict:
        if x == self.INFINITY:
            x, y = y, x
        if y == self.INFINITY:
            if self._base.is_finite():
                return Verdict.true(
                    reason=(
                        f"X is compact (finite): ∞ is isolated; {x!r} ∈ X and ∞ "
                        "are separated by the disjoint open sets X and {∞}"
                    ),
                    witness={"x_neighbourhood": "X (open in αX)", "inf_neighbourhood": "{∞}"},
                )
            base_t2 = self._base.certificate("T2")
            if base_t2 is not None and base_t2.value:
                return Verdict.true(
                    reason=(
                        f"X is Hausdorff: a compact K with {x!r} ∈ int(K) gives "
                        "int(K) and (X\\K)∪{∞} as disjoint open neighbourhoods"
                    ),
                    witness={"x": x},
                )
            return Verdict.undecidable(
                f"Cannot certify separation of ∞ and {x!r}: need locally-compact-T2 certificate"
            )
        return self._base.point_separation(x, y)

    def certificate(self, prop: str) -> Verdict | None:
        if prop == "compact":
            return Verdict.true(
                reason="Alexandroff one-point compactification is compact by construction"
            )
        if prop == "lindelof":
            return Verdict.true(reason="compact implies Lindelöf")
        if prop in {"T0", "T1"}:
            base_cert = self._base.certificate(prop)
            if base_cert is not None and base_cert.value:
                return Verdict.true(
                    reason=f"X is {prop} and ∞ acquires the same separation property"
                )
            if base_cert is not None and not base_cert.value:
                return Verdict.false(
                    reason=f"X is not {prop}, so αX is not {prop}",
                    counterexample=base_cert.counterexample,
                )
            if self._base.is_finite():
                return None
            return None
        if prop == "T2":
            base_t2 = self._base.certificate("T2")
            if base_t2 is not None and base_t2.value:
                return Verdict.true(
                    reason=(
                        "αX is T2: X is (locally compact) Hausdorff — "
                        "the Alexandroff extension of a locally compact T2 space is T2"
                    )
                )
            if base_t2 is not None and not base_t2.value:
                return Verdict.false(
                    reason="X is not Hausdorff so αX is not T2",
                    counterexample=base_t2.counterexample,
                )
            return None
        if prop == "connected":
            # Finite spaces are always compact → ∞ is isolated → αX disconnected.
            base_is_compact = self._base.is_finite()
            if not base_is_compact:
                base_compact = self._base.certificate("compact")
                base_is_compact = base_compact is not None and bool(base_compact.value)
            if base_is_compact:
                return Verdict.false(
                    reason="X is already compact: ∞ is isolated, disconnecting αX",
                    counterexample="{∞} and X form a disconnection of αX",
                )
            base_connected = self._base.certificate("connected")
            if base_connected is not None and not base_connected.value:
                return Verdict.false(
                    reason="X is disconnected, so αX is disconnected",
                    counterexample=base_connected.counterexample,
                )
            return None
        return None

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        return None


def one_point_compactification(
    space: Space, name: str | None = None
) -> OnePointCompactificationSpace:
    """Alexandroff one-point compactification αX of any Space X."""
    return OnePointCompactificationSpace(space, name)


# ---------------------------------------------------------------------------
# P9.2  StoneCechSpace (βℕ)
# ---------------------------------------------------------------------------


class StoneCechSpace(Space):
    """The Stone–Čech compactification βℕ of the natural numbers.

    βℕ is the unique compact Hausdorff space containing ℕ as a dense discrete
    subspace such that every bounded real-valued function on ℕ extends uniquely
    to a continuous function on βℕ.

    Points in βℕ \\ ℕ are free ultrafilters on ℕ (not finitely enumerable);
    the carrier has cardinality 2^𝔠.  Natural numbers embed into βℕ as a
    countable dense discrete subspace.

    Key facts:
    - compact Hausdorff (T2, T4) by the universal property construction
    - separable: ℕ is a countable dense subspace (density = ℵ₀)
    - NOT first-countable: free ultrafilter points 𝒰 ∈ βℕ \\ ℕ have no
      countable neighbourhood base (any countable base would generate a
      countable filter, contradicting 𝒰 being a non-principal ultrafilter)
    - NOT second-countable: not first-countable at ultrafilter points
    - totally disconnected: the clopen sets are exactly the βℕ-closures of
      subsets of ℕ (Stone duality with the Boolean algebra P(ℕ))
    - NOT T6 (perfectly normal): compact Hausdorff is T6 iff metrizable;
      βℕ is not metrizable (not first-countable everywhere)
    """

    _CERTS: dict[str, bool] = {
        "T0": True,
        "T1": True,
        "T2": True,
        "regular": True,
        "normal": True,
        "tychonoff": True,
        "T6": False,
        "compact": True,
        "connected": False,
        "lindelof": True,
        "separable": True,
        "first_countable": False,
        "second_countable": False,
    }

    _REASONS: dict[str, str] = {
        "T0": "βℕ is compact Hausdorff, hence T0",
        "T1": "βℕ is compact Hausdorff, hence T1",
        "T2": "Stone–Čech compactification is compact Hausdorff",
        "regular": "compact Hausdorff spaces are regular (T3)",
        "normal": "compact Hausdorff spaces are normal (T4)",
        "tychonoff": "compact Hausdorff spaces are completely regular (T3.5)",
        "T6": (
            "βℕ is NOT T6: a compact Hausdorff space is perfectly normal iff "
            "metrizable (Urysohn), but βℕ is not metrizable"
        ),
        "compact": "Stone–Čech compactification is compact by the universal property",
        "connected": (
            "βℕ is totally disconnected: clopen sets correspond to subsets of ℕ "
            "via Stone duality with the Boolean algebra P(ℕ)"
        ),
        "lindelof": "compact implies Lindelöf",
        "separable": "ℕ embeds as a countable dense discrete subspace of βℕ",
        "first_countable": (
            "free ultrafilter points 𝒰 ∈ βℕ \\ ℕ have no countable local base: "
            "any countable base would generate a countable filter, contradicting "
            "𝒰 being a free (non-principal) ultrafilter"
        ),
        "second_countable": "βℕ is not first-countable at ultrafilter points",
    }

    _COUNTEREXAMPLES: dict[str, Any] = {
        "T6": "the subspace βℕ \\ ℕ is a Gδ but not every closed set in βℕ is a Gδ",
        "connected": (
            "the clopen set cl_βℕ(2ℕ) (closure of even naturals) "
            "and its complement partition βℕ"
        ),
        "first_countable": (
            "any free ultrafilter 𝒰 ∈ βℕ \\ ℕ: "
            "a countable base {Uₙ} would give ⋂Uₙ = {𝒰} (singleton), "
            "forcing 𝒰 to be principal — contradiction"
        ),
        "second_countable": "not first-countable (see first_countable certificate)",
    }

    def __init__(self, name: str = "βℕ") -> None:
        self.name = name
        self.carrier_kind = CarrierKind.UNCOUNTABLE

    def contains(self, point: Any) -> bool:
        return isinstance(point, int) and point >= 0

    def point_separation(self, x: Any, y: Any) -> Verdict:
        if isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0 and x != y:
            return Verdict.true(
                reason=(
                    f"the clopen set cl_βℕ({{{x}}}) = {{{x}}} contains {x} but "
                    f"not {y} (ℕ embeds as a discrete subspace: each {{n}} is clopen in βℕ)"
                ),
                witness={"clopen": f"{{{x}}}", "x_in": x, "y_not_in": y},
            )
        return Verdict.undecidable(
            "free ultrafilter points cannot be explicitly exhibited; "
            "separation requires ultrafilter arithmetic"
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop not in self._CERTS:
            return None
        val = self._CERTS[prop]
        reason = self._REASONS.get(prop, f"βℕ: {prop} = {val}")
        if val:
            return Verdict.true(reason=reason)
        return Verdict.false(
            reason=reason,
            counterexample=self._COUNTEREXAMPLES.get(prop),
        )

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        return {
            "weight": CardinalValue.continuum(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.continuum(),
            "cellularity": CardinalValue.continuum(),
        }.get(invariant)


def stone_cech_n(name: str = "βℕ") -> StoneCechSpace:
    """Stone–Čech compactification of ℕ: compact, separable, not first-countable."""
    return StoneCechSpace(name)


# ---------------------------------------------------------------------------
# P9.3  HilbertCubeSpace ([0,1]^ω)
# ---------------------------------------------------------------------------


class HilbertCubeSpace(Space):
    """The Hilbert cube [0,1]^ω with the product topology.

    Points are represented as finite tuples (x₀, x₁, …, xₙ₋₁) of
    :class:`~fractions.Fraction` values in [0, 1].  A cylinder neighbourhood
    C(k, x, ε) = {y : |yₖ − xₖ| < ε} gives a base for the product topology.

    Key facts:
    - compact (Tychonoff product of compact [0,1])
    - metrizable: d(x,y) = Σ |xₙ−yₙ|/2ⁿ converges and induces the product topology
    - T6 (metrizable → perfectly normal)
    - second-countable (countable product of second-countable spaces)
    - separable (metrizable + compact → separable by Urysohn metrisation)
    - connected (product of connected spaces)
    - path-connected (each [0,1] is path-connected)

    By the Urysohn embedding theorem: every compact metrizable space embeds
    homeomorphically into [0,1]^ω.
    """

    _CERTS: dict[str, bool] = {
        "T0": True,
        "T1": True,
        "T2": True,
        "regular": True,
        "normal": True,
        "tychonoff": True,
        "T5": True,
        "T6": True,
        "compact": True,
        "connected": True,
        "lindelof": True,
        "separable": True,
        "second_countable": True,
        "first_countable": True,
    }

    _REASONS: dict[str, str] = {
        "T0": "Hilbert cube is metrizable, hence T0",
        "T1": "Hilbert cube is metrizable, hence T1",
        "T2": "Hilbert cube is metrizable, hence Hausdorff (T2)",
        "regular": "Hilbert cube is metrizable, hence regular (T3)",
        "normal": "Hilbert cube is metrizable, hence normal (T4)",
        "tychonoff": "Hilbert cube is metrizable, hence completely regular (T3.5)",
        "T5": "Hilbert cube is metrizable, hence completely normal (T5)",
        "T6": "Hilbert cube is metrizable compact, hence perfectly normal (T6)",
        "compact": "Tychonoff: product of compact [0,1] factors is compact",
        "connected": "product of connected spaces [0,1] is connected",
        "lindelof": "compact implies Lindelöf",
        "separable": "metrizable compact space is separable",
        "second_countable": "countable product of second-countable [0,1] is second-countable",
        "first_countable": "second-countable implies first-countable",
    }

    def __init__(self, name: str = "[0,1]^ω") -> None:
        self.name = name
        self.carrier_kind = CarrierKind.UNCOUNTABLE

    def contains(self, point: Any) -> bool:
        if not isinstance(point, tuple):
            return False
        try:
            return all(Fraction(0) <= Fraction(c) <= Fraction(1) for c in point)
        except (TypeError, ValueError):
            return False

    def point_separation(self, x: Any, y: Any) -> Verdict:
        """Separate by the first coordinate where the values differ."""
        min_len = min(len(x), len(y))
        for k in range(min_len):
            fx, fy = Fraction(x[k]), Fraction(y[k])
            if fx != fy:
                radius = abs(fx - fy) / 2
                return Verdict.true(
                    reason=(
                        f"cylinder neighbourhoods at coordinate {k}: "
                        f"x[{k}]={fx} and y[{k}]={fy} lie in disjoint balls of radius {radius}"
                    ),
                    witness={"coord": k, "x_val": fx, "y_val": fy, "radius": radius},
                )
        return Verdict.undecidable(
            f"all provided coordinates of {x!r} and {y!r} agree; "
            "separation requires more coordinates of the infinite sequence"
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop not in self._CERTS:
            return None
        val = self._CERTS[prop]
        reason = self._REASONS.get(prop, f"Hilbert cube: {prop} = {val}")
        return Verdict.true(reason=reason) if val else Verdict.false(reason=reason)

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.aleph_0(),
            "cellularity": CardinalValue.aleph_0(),
        }.get(invariant)


def hilbert_cube(name: str = "[0,1]^ω") -> HilbertCubeSpace:
    """The Hilbert cube [0,1]^ω: compact, metrizable, T6, universal compact metrizable."""
    return HilbertCubeSpace(name)


# ---------------------------------------------------------------------------
# P9.4  SolenoidSpace (dyadic solenoid)
# ---------------------------------------------------------------------------


class SolenoidSpace(Space):
    """The dyadic solenoid Σ = lim←{S¹ ←² S¹ ←² S¹ ←² …}.

    The dyadic solenoid is the inverse limit of S¹ under the doubling map
    z ↦ z² (angle doubling θ ↦ 2θ mod 2π).  It is an abelian topological
    group — a compact subgroup of (S¹)^ℕ.

    Points are represented as finite compatible angle sequences
    (θ₀, θ₁, …, θₙ₋₁) in [0, 1) satisfying the compatibility condition
    2·θₖ ≡ θₖ₋₁ (mod 1) for each k.

    Key facts:
    - compact (inverse limit of compact S¹ under continuous surjections)
    - connected (inverse limit of connected S¹ under surjections)
    - metrizable: d(x,y) = Σ |θₙ(x)−θₙ(y)|_circ / 2ⁿ  (circular distance)
    - T6 (metrizable compact → perfectly normal)
    - second-countable and separable (metrizable compact)
    - NOT locally connected: each local cross-section is homeomorphic to the
      Cantor space (the connected components are dense winding lines, but no
      neighbourhood is connected — local structure = Cantor × interval)
    - π₁(Σ) ≅ ℤ[1/2] (the dyadic rationals, not finitely generated)
    """

    _CERTS: dict[str, bool] = {
        "T0": True,
        "T1": True,
        "T2": True,
        "regular": True,
        "normal": True,
        "tychonoff": True,
        "T5": True,
        "T6": True,
        "compact": True,
        "connected": True,
        "lindelof": True,
        "separable": True,
        "second_countable": True,
        "first_countable": True,
    }

    _REASONS: dict[str, str] = {
        "T0": "dyadic solenoid is metrizable, hence T0",
        "T1": "dyadic solenoid is metrizable, hence T1",
        "T2": "dyadic solenoid is metrizable, hence Hausdorff (T2)",
        "regular": "dyadic solenoid is metrizable, hence regular (T3)",
        "normal": "dyadic solenoid is metrizable, hence normal (T4)",
        "tychonoff": "dyadic solenoid is metrizable, hence completely regular (T3.5)",
        "T5": "dyadic solenoid is metrizable, hence completely normal (T5)",
        "T6": "dyadic solenoid is metrizable compact, hence perfectly normal (T6)",
        "compact": (
            "inverse limit of compact spaces S¹ under continuous maps is compact "
            "(closed subgroup of the compact group (S¹)^ℕ)"
        ),
        "connected": (
            "inverse limit of connected S¹ under surjective (covering) maps is connected"
        ),
        "lindelof": "compact implies Lindelöf",
        "separable": "metrizable compact space is separable",
        "second_countable": "metrizable compact space is second-countable",
        "first_countable": "metrizable implies first-countable",
    }

    def __init__(self, name: str = "Σ_dyadic") -> None:
        self.name = name
        self.carrier_kind = CarrierKind.UNCOUNTABLE

    def contains(self, point: Any) -> bool:
        """Finite compatible angle sequence (θ₀, …, θₙ₋₁) with θₖ ∈ [0,1)."""
        if not isinstance(point, tuple) or len(point) == 0:
            return False
        try:
            angles = [Fraction(a) for a in point]
        except (TypeError, ValueError):
            return False
        for a in angles:
            if not (Fraction(0) <= a < Fraction(1)):
                return False
        for k in range(1, len(angles)):
            two_k = 2 * angles[k]
            residue = two_k - int(two_k)
            if residue != angles[k - 1]:
                return False
        return True

    def point_separation(self, x: Any, y: Any) -> Verdict:
        """Separate at the first level where the angles disagree."""
        min_len = min(len(x), len(y))
        for k in range(min_len):
            ax, ay = Fraction(x[k]), Fraction(y[k])
            if ax != ay:
                diff = abs(ax - ay)
                radius = diff / 3
                return Verdict.true(
                    reason=(
                        f"level-{k} cylinder neighbourhoods of radius {radius} "
                        f"around angle {ax} and {ay} in S¹ are disjoint"
                    ),
                    witness={"level": k, "angle_x": ax, "angle_y": ay, "radius": radius},
                )
        return Verdict.undecidable(
            f"all provided levels of {x!r} and {y!r} agree; "
            "need more levels of the infinite compatible sequence"
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop == "locally_connected":
            return Verdict.false(
                reason=(
                    "dyadic solenoid is NOT locally connected: "
                    "each small neighbourhood intersects uncountably many "
                    "dense winding-line path-components; the local cross-section "
                    "at any point is homeomorphic to the Cantor space"
                ),
                counterexample=(
                    "local cross-section: the pre-image of a small arc in S¹ "
                    "under the level-0 projection is a Cantor set"
                ),
            )
        if prop not in self._CERTS:
            return None
        val = self._CERTS[prop]
        reason = self._REASONS.get(prop, f"solenoid: {prop} = {val}")
        return Verdict.true(reason=reason) if val else Verdict.false(reason=reason)

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.aleph_0(),
            "cellularity": CardinalValue.aleph_0(),
        }.get(invariant)


def dyadic_solenoid(name: str = "Σ_dyadic") -> SolenoidSpace:
    """Dyadic solenoid: compact, connected, metrizable T6, NOT locally connected."""
    return SolenoidSpace(name)


# ---------------------------------------------------------------------------
# P9.5  UniformSpace (+ UniformProduct, UniformSubspace)
# ---------------------------------------------------------------------------


class UniformSpace(Space):
    """A topological space equipped with a uniform structure from a metric.

    A uniformity on X is a filter of entourages (symmetric neighbourhoods of
    the diagonal in X × X) satisfying:
    1. Every entourage contains the diagonal.
    2. For every entourage E there is a symmetric E' ⊆ E (already symmetric here).
    3. For every E there is E' with E' ∘ E' ⊆ E (triangle inequality).

    This implementation derives the uniformity from a metric d: the ε-entourage
    E_ε = {(x, y) : d(x, y) < ε} is symmetric and satisfies (3) because
    d(x, z) < ε/2 and d(z, y) < ε/2 imply d(x, y) < ε.

    Key additional methods:
    - :meth:`entourage` — the ε-entourage as a callable relation
    - :meth:`is_cauchy` — approximate Cauchy test on a finite sequence
    - :meth:`uniform_neighbourhood` — describe the uniform ball B(x, ε)
    """

    def __init__(
        self,
        name: str,
        distance: Callable[[Any, Any], Any],
        member: Callable[[Any], bool],
        carrier_kind: CarrierKind = CarrierKind.COUNTABLE,
    ) -> None:
        self.name = name
        self.carrier_kind = carrier_kind
        self._distance = distance
        self._member = member

    def contains(self, point: Any) -> bool:
        return bool(self._member(point))

    def entourage(self, eps: Any) -> Callable[[Any, Any], bool]:
        """Return the ε-entourage E_ε: (x,y) ↦ (d(x,y) < ε)."""
        eps_f = Fraction(eps)

        def _in_entourage(x: Any, y: Any) -> bool:
            return Fraction(self._distance(x, y)) < eps_f

        return _in_entourage

    def uniform_neighbourhood(self, x: Any, eps: Any) -> dict[str, Any]:
        """Describe the ε-ball B(x, ε) centred at x."""
        return {"centre": x, "radius": Fraction(eps), "description": f"B({x!r}, {eps})"}

    def is_cauchy(self, sequence: Sequence[Any], eps: Any = Fraction(1, 100)) -> bool:
        """Check whether a finite sequence is approximately Cauchy.

        Returns True iff all pairwise distances are < ε.
        This is a finite-sample approximation; true Cauchy-ness is a property
        of the full infinite sequence.
        """
        eps_f = Fraction(eps)
        for i in range(len(sequence)):
            for j in range(i + 1, len(sequence)):
                if Fraction(self._distance(sequence[i], sequence[j])) >= eps_f:
                    return False
        return True

    def point_separation(self, x: Any, y: Any) -> Verdict:
        try:
            d = Fraction(self._distance(x, y))
        except (TypeError, ValueError):
            return Verdict.undecidable(f"distance({x!r}, {y!r}) could not be computed")
        if d > 0:
            radius = d / 2
            return Verdict.true(
                reason=(
                    f"uniform balls B({x!r},{radius}) and B({y!r},{radius}) are disjoint "
                    f"(d(x,y)={d}, entourage E_{{{radius}}} separates them)"
                ),
                witness={"radius": radius, "distance": d},
            )
        return Verdict.false(
            reason=f"d({x!r},{y!r}) = 0: the metric does not separate these points",
            counterexample=(x, y),
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop in {"T0", "T1", "T2", "regular", "normal"}:
            return Verdict.true(
                reason=f"metric uniformity induces a metrizable topology, hence {prop}"
            )
        if prop in {"tychonoff", "T5", "T6"}:
            return Verdict.true(
                reason=f"metrizable uniform space is perfectly normal, hence {prop}"
            )
        if prop == "first_countable":
            return Verdict.true(
                reason="ε-entourages for ε = 1/n give a countable local base"
            )
        return None

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        if invariant == "character":
            return CardinalValue.aleph_0()
        return None


class UniformProduct(UniformSpace):
    """Product of two uniform spaces with the sup-metric uniformity.

    The product uniformity on X × Y has entourages
    E_{ε} = {((x,y),(x',y')) : d_X(x,x') < ε and d_Y(y,y') < ε},
    equivalent to the sup-metric max(d_X, d_Y).
    """

    def __init__(
        self,
        u1: UniformSpace,
        u2: UniformSpace,
        name: str | None = None,
    ) -> None:
        def _dist(a: Any, b: Any) -> Fraction:
            if not (isinstance(a, tuple) and len(a) == 2):
                return Fraction(0)
            if not (isinstance(b, tuple) and len(b) == 2):
                return Fraction(0)
            return max(
                Fraction(u1._distance(a[0], b[0])),
                Fraction(u2._distance(a[1], b[1])),
            )

        def _member(p: Any) -> bool:
            return (
                isinstance(p, tuple)
                and len(p) == 2
                and bool(u1._member(p[0]))
                and bool(u2._member(p[1]))
            )

        ck = (
            CarrierKind.UNCOUNTABLE
            if CarrierKind.UNCOUNTABLE in (u1.carrier_kind, u2.carrier_kind)
            else CarrierKind.COUNTABLE
        )
        super().__init__(
            name=name or f"({u1.name} ×_u {u2.name})",
            distance=_dist,
            member=_member,
            carrier_kind=ck,
        )
        self._u1 = u1
        self._u2 = u2
        self.construction = ("uniform_product", u1, u2)


class UniformSubspace(UniformSpace):
    """Subspace of a uniform space with the induced (trace) uniformity.

    The trace uniformity on A ⊆ X has entourages {E ∩ (A × A) : E ∈ 𝒰_X}.
    With a metric, this is simply the restriction of d to A × A.
    """

    def __init__(
        self,
        base: UniformSpace,
        pred: Callable[[Any], bool],
        name: str | None = None,
    ) -> None:
        def _member(p: Any) -> bool:
            return bool(base._member(p)) and bool(pred(p))

        super().__init__(
            name=name or f"sub({base.name})",
            distance=base._distance,
            member=_member,
            carrier_kind=base.carrier_kind,
        )
        self._base_uniform = base
        self.construction = ("uniform_subspace", base)


def metric_uniform_space(
    name: str,
    distance: Callable[[Any, Any], Any],
    member: Callable[[Any], bool],
    carrier_kind: CarrierKind = CarrierKind.COUNTABLE,
) -> UniformSpace:
    """Build a :class:`UniformSpace` from a metric distance function."""
    return UniformSpace(name, distance, member, carrier_kind)


def rational_uniform_space(name: str = "uniform(ℚ)") -> UniformSpace:
    """The uniform space structure on ℚ from the standard metric |x − y|."""
    return UniformSpace(
        name,
        distance=lambda a, b: abs(Fraction(a) - Fraction(b)),
        member=lambda p: isinstance(p, (int, Fraction)),
        carrier_kind=CarrierKind.COUNTABLE,
    )


# ---------------------------------------------------------------------------
# P9.6  ProfiniteSpace
# ---------------------------------------------------------------------------


class ProfiniteSpace(Space):
    """An inverse limit of finite discrete spaces (a profinite space).

    A profinite space is exactly a compact, Hausdorff, totally disconnected
    space (Stone duality: profinite spaces ↔ Boolean algebras ↔ Stone spaces).

    The representation is given by:
    - ``moduli``: [n₀, n₁, n₂, …] — the size of ℤ/nₖ at level k.
    - ``bonding_map(a, k)``: the bonding map nₖ₊₁ → nₖ, sending
      a ∈ {0, …, nₖ₊₁ − 1} to its image in {0, …, nₖ − 1}.

    Points are finite compatible sequences (a₀, a₁, …, aₘ₋₁) with
    aₖ ∈ {0, …, nₖ − 1} and bonding_map(aₖ₊₁, k) = aₖ for all k.

    The principal example is the ring of p-adic integers:
    ℤ_p = lim← {ℤ/p ← ℤ/p² ← ℤ/p³ ← …} via reduction modulo pⁿ.
    Factory: :func:`p_adic_integers`.

    Key facts:
    - compact (inverse limit of compact finite discrete spaces)
    - T2 (inverse limit of Hausdorff discrete spaces)
    - totally disconnected: clopen preimage cylinders separate any two points
    - metrizable: d(x,y) = 1/nₖ where k = first level of disagreement
    - T6 (metrizable compact → perfectly normal)
    - second-countable and separable (metrizable compact)
    - first-countable: preimage cylinders form a countable local base
    - NOT connected (totally disconnected + more than one point)
    """

    _CERTS: dict[str, bool] = {
        "T0": True,
        "T1": True,
        "T2": True,
        "regular": True,
        "normal": True,
        "tychonoff": True,
        "T5": True,
        "T6": True,
        "compact": True,
        "connected": False,
        "lindelof": True,
        "separable": True,
        "second_countable": True,
        "first_countable": True,
    }

    _REASONS: dict[str, str] = {
        "T0": "profinite space is metrizable, hence T0",
        "T1": "profinite space is metrizable, hence T1",
        "T2": "inverse limit of Hausdorff (finite discrete) spaces is Hausdorff",
        "regular": "profinite space is metrizable, hence regular (T3)",
        "normal": "profinite space is metrizable, hence normal (T4)",
        "tychonoff": "profinite space is metrizable, hence completely regular (T3.5)",
        "T5": "profinite space is metrizable, hence completely normal (T5)",
        "T6": "profinite space is metrizable compact, hence perfectly normal (T6)",
        "compact": (
            "inverse limit of compact (finite discrete) spaces is compact; "
            "equivalently: closed subgroup of a product of compact groups"
        ),
        "connected": (
            "profinite space is totally disconnected: "
            "the clopen preimage cylinders πₖ⁻¹({aₖ}) separate any two points"
        ),
        "lindelof": "compact implies Lindelöf",
        "separable": "metrizable compact space is separable",
        "second_countable": "metrizable compact space is second-countable",
        "first_countable": (
            "the nested clopen cylinders πₖ⁻¹({aₖ}) (k = 0, 1, 2, …) "
            "form a countable neighbourhood base at each point"
        ),
    }

    def __init__(
        self,
        name: str,
        moduli: Sequence[int],
        bonding_map: Callable[[int, int], int],
    ) -> None:
        self.name = name
        self.carrier_kind = CarrierKind.UNCOUNTABLE
        self._moduli: list[int] = list(moduli)
        self._bonding_map = bonding_map

    def contains(self, point: Any) -> bool:
        """Check membership: finite compatible sequence within the given moduli."""
        if not isinstance(point, tuple) or len(point) == 0:
            return False
        if len(point) > len(self._moduli):
            return False
        for k, a in enumerate(point):
            if not (isinstance(a, int) and 0 <= a < self._moduli[k]):
                return False
        for k in range(len(point) - 1):
            if self._bonding_map(point[k + 1], k) != point[k]:
                return False
        return True

    def point_separation(self, x: Any, y: Any) -> Verdict:
        """Separate by the clopen preimage cylinder at the first differing level."""
        min_len = min(len(x), len(y))
        for k in range(min_len):
            if x[k] != y[k]:
                return Verdict.true(
                    reason=(
                        f"clopen preimage cylinder π_{k}⁻¹({{{x[k]}}}) contains x "
                        f"but not y (they differ at level {k} in ℤ/{self._moduli[k]})"
                    ),
                    witness={"level": k, "x_val": x[k], "y_val": y[k], "modulus": self._moduli[k]},
                )
        return Verdict.undecidable(
            f"all provided levels of {x!r} and {y!r} agree; "
            "need more levels of the infinite compatible sequence"
        )

    def certificate(self, prop: str) -> Verdict | None:
        if prop not in self._CERTS:
            return None
        val = self._CERTS[prop]
        reason = self._REASONS.get(prop, f"profinite space: {prop} = {val}")
        if val:
            return Verdict.true(reason=reason)
        _counterexamples: dict[str, Any] = {
            "connected": (
                f"the preimage π₀⁻¹({{0}}) is a proper clopen set "
                f"(assuming n₀ = {self._moduli[0] if self._moduli else '?'} ≥ 2)"
            ),
        }
        return Verdict.false(reason=reason, counterexample=_counterexamples.get(prop))

    def cardinal_certificate(self, invariant: str) -> CardinalValue | None:
        return {
            "weight": CardinalValue.aleph_0(),
            "density": CardinalValue.aleph_0(),
            "character": CardinalValue.aleph_0(),
            "cellularity": CardinalValue.aleph_0(),
        }.get(invariant)


def p_adic_integers(p: int, levels: int = 20) -> ProfiniteSpace:
    """The p-adic integers ℤ_p = lim← {ℤ/p ← ℤ/p² ← ℤ/p³ ← …}.

    The bonding map πₖ : ℤ/p^{k+2} → ℤ/p^{k+1} is reduction modulo p^{k+1}.

    Parameters
    ----------
    p : int
        A prime ≥ 2.
    levels : int
        Number of levels to store (default 20; more gives finer point membership).
    """
    if p < 2:
        raise ValueError(f"p must be a prime ≥ 2, got {p}")
    moduli = [p ** (k + 1) for k in range(levels)]

    def _bonding(a: int, k: int) -> int:
        return a % (p ** (k + 1))

    return ProfiniteSpace(f"ℤ_{p}", moduli, _bonding)


def profinite_space(
    name: str,
    moduli: Sequence[int],
    bonding_map: Callable[[int, int], int],
) -> ProfiniteSpace:
    """Build a :class:`ProfiniteSpace` from a moduli sequence and bonding maps."""
    return ProfiniteSpace(name, moduli, bonding_map)


__all__ = [
    "HilbertCubeSpace",
    "OnePointCompactificationSpace",
    "ProfiniteSpace",
    "SolenoidSpace",
    "StoneCechSpace",
    "UniformProduct",
    "UniformSpace",
    "UniformSubspace",
    # factories
    "dyadic_solenoid",
    "hilbert_cube",
    "metric_uniform_space",
    "one_point_compactification",
    "p_adic_integers",
    "profinite_space",
    "rational_uniform_space",
    "stone_cech_n",
]
