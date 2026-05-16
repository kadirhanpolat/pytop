"""Dynamical systems profile module — basics.

Provides teaching-oriented profile dataclasses for the foundational concepts
of topological dynamical systems as covered in Adams & Franzosa §8.1–8.2.

Profiles record teaching metadata (source references, key properties, examples)
and stable named families for notebook references and manuscript integration.
They do not perform symbolic computation.

Source: AdamsFranzosa2008Topology §8.1–8.2.
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# OrbitProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OrbitProfile:
    """Teaching profile for the orbit of a point under a dynamical system.

    A dynamical system is a pair (X, f) where X is a topological space and
    f : X → X is a continuous function.  The orbit of a point x ∈ X records
    all iterates of f starting from x.
    """

    key: str
    display_name: str
    space_description: str
    map_description: str
    orbit_type: str          # "infinite", "periodic", "eventually_periodic", "fixed"
    period: int | None       # None if not periodic; 1 if fixed point
    preperiod: int | None    # None if not eventually periodic
    source_section: str      # e.g. "Adams & Franzosa §8.1"
    notes: str


def get_orbit_profiles() -> tuple[OrbitProfile, ...]:
    """Return the standard orbit-type teaching profiles.

    These cover the four qualitatively distinct orbit behaviours described in
    Adams & Franzosa §8.1: infinite (non-periodic), periodic, eventually
    periodic, and fixed.
    """
    return (
        OrbitProfile(
            key="fixed_point_orbit",
            display_name="Fixed-point orbit",
            space_description="Any topological space X",
            map_description="f : X → X continuous, f(x) = x",
            orbit_type="fixed",
            period=1,
            preperiod=0,
            source_section="Adams & Franzosa §8.1",
            notes=(
                "The orbit {x, f(x), f²(x), ...} collapses to the singleton {x}. "
                "Fixed points are the simplest periodic orbits (period 1). "
                "Example: f(x) = x on ℝ; every point is fixed."
            ),
        ),
        OrbitProfile(
            key="periodic_orbit",
            display_name="Periodic orbit (period n ≥ 2)",
            space_description="Any topological space X",
            map_description="f : X → X continuous, fⁿ(x) = x, fᵏ(x) ≠ x for 1 ≤ k < n",
            orbit_type="periodic",
            period=None,   # period is n, recorded generically
            preperiod=0,
            source_section="Adams & Franzosa §8.1",
            notes=(
                "The orbit {x, f(x), ..., fⁿ⁻¹(x)} is a finite cycle of length n. "
                "The minimal period is the smallest n ≥ 1 with fⁿ(x) = x. "
                "Example: rotation of S¹ by a rational multiple of 2π; every point "
                "has a periodic orbit whose period divides the denominator."
            ),
        ),
        OrbitProfile(
            key="eventually_periodic_orbit",
            display_name="Eventually periodic orbit",
            space_description="Any topological space X",
            map_description="f : X → X continuous; fᵐ⁺ⁿ(x) = fᵐ(x) for some m ≥ 1, n ≥ 1",
            orbit_type="eventually_periodic",
            period=None,   # period n
            preperiod=None,  # preperiod m
            source_section="Adams & Franzosa §8.1",
            notes=(
                "The orbit is infinite but eventually enters a periodic cycle. "
                "The preperiod m is the number of iterates before the cycle is reached; "
                "the period n is the length of the cycle itself. "
                "Example: f(x) = x² on [0,1]; the orbit of any x ∈ (0,1) "
                "converges to the fixed point 0 (attracting) or 1 (repelling)."
            ),
        ),
        OrbitProfile(
            key="infinite_aperiodic_orbit",
            display_name="Infinite aperiodic orbit",
            space_description="Any topological space X",
            map_description="f : X → X continuous; fⁿ(x) ≠ x for all n ≥ 1",
            orbit_type="infinite",
            period=None,
            preperiod=None,
            source_section="Adams & Franzosa §8.1",
            notes=(
                "The orbit {x, f(x), f²(x), ...} is an infinite set of distinct points. "
                "Aperiodic orbits arise in irrational rotations and in chaotic systems. "
                "Example: rotation of S¹ by an irrational multiple α of 2π; "
                "the orbit of any point is dense in S¹ (Weyl equidistribution)."
            ),
        ),
    )


def orbit_type_summary() -> dict[str, list[str]]:
    """Return a mapping from orbit_type to profile keys."""
    result: dict[str, list[str]] = {}
    for p in get_orbit_profiles():
        result.setdefault(p.orbit_type, []).append(p.key)
    return result


# ---------------------------------------------------------------------------
# FixedPointProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FixedPointProfile:
    """Teaching profile for fixed-point and periodic-point theory.

    Covers the definitions, stability classification, and topological existence
    results for fixed points as in Adams & Franzosa §8.1–8.2.
    """

    key: str
    display_name: str
    space_description: str
    map_description: str
    stability: str           # "stable", "unstable", "neutral", "not_applicable"
    existence_theorem: str   # name of theorem guaranteeing existence, or "none"
    source_section: str
    notes: str


def get_fixed_point_profiles() -> tuple[FixedPointProfile, ...]:
    """Return teaching profiles for fixed-point and periodic-point concepts."""
    return (
        FixedPointProfile(
            key="attracting_fixed_point",
            display_name="Attracting (stable) fixed point",
            space_description="Metric space (X, d)",
            map_description="f : X → X; f(x₀) = x₀; nearby orbits converge to x₀",
            stability="stable",
            existence_theorem="Banach contraction mapping theorem",
            source_section="Adams & Franzosa §8.2",
            notes=(
                "A fixed point x₀ is attracting if there exists a neighbourhood U "
                "of x₀ such that fⁿ(x) → x₀ for all x ∈ U. "
                "Topological characterisation: x₀ is in the interior of its own "
                "basin of attraction. "
                "Example: f(x) = x/2 on ℝ; x₀ = 0 is attracting."
            ),
        ),
        FixedPointProfile(
            key="repelling_fixed_point",
            display_name="Repelling (unstable) fixed point",
            space_description="Metric space (X, d)",
            map_description="f : X → X; f(x₀) = x₀; nearby orbits diverge from x₀",
            stability="unstable",
            existence_theorem="none",
            source_section="Adams & Franzosa §8.2",
            notes=(
                "A fixed point x₀ is repelling if nearby orbits move away from x₀: "
                "for every neighbourhood U of x₀ there exists x ∈ U such that "
                "fⁿ(x) ∉ U for some n. "
                "Example: f(x) = 2x on ℝ; x₀ = 0 is repelling (all orbits diverge)."
            ),
        ),
        FixedPointProfile(
            key="neutral_fixed_point",
            display_name="Neutral (indifferent) fixed point",
            space_description="Metric space (X, d)",
            map_description="f : X → X; f(x₀) = x₀; nearby orbits neither converge nor diverge",
            stability="neutral",
            existence_theorem="none",
            source_section="Adams & Franzosa §8.2",
            notes=(
                "Nearby orbits remain at a bounded distance from x₀ but do not "
                "converge. Common in conservative (area-preserving) systems. "
                "Example: rigid rotation of S¹ by an irrational angle; the fixed "
                "point structure is trivial but nearby orbits stay nearby."
            ),
        ),
        FixedPointProfile(
            key="brouwer_fixed_point",
            display_name="Brouwer fixed-point theorem instance",
            space_description="Closed unit disk D² ⊆ ℝ²",
            map_description="f : D² → D² continuous",
            stability="not_applicable",
            existence_theorem="Brouwer Fixed Point Theorem",
            source_section="Adams & Franzosa §8.2",
            notes=(
                "Every continuous map f : Dⁿ → Dⁿ has at least one fixed point. "
                "The result is topological: it holds for any space homeomorphic to Dⁿ. "
                "The proof (via degree theory or the no-retraction theorem) appears "
                "in Adams & Franzosa §9–10; §8.2 introduces it as a motivating example "
                "for the importance of fixed-point theory in applied topology."
            ),
        ),
        FixedPointProfile(
            key="periodic_point_n",
            display_name="Period-n periodic point",
            space_description="Any topological space X",
            map_description="f : X → X continuous; fⁿ(x) = x, minimal period n",
            stability="not_applicable",
            existence_theorem="Sharkovskii's theorem (interval maps)",
            source_section="Adams & Franzosa §8.1",
            notes=(
                "A point x is periodic of period n if fⁿ(x) = x and n is the "
                "smallest such positive integer. The set of period-n points of f "
                "is the fixed-point set of fⁿ. "
                "Sharkovskii's theorem (for continuous f : ℝ → ℝ) states that the "
                "existence of a period-3 orbit implies the existence of orbits of "
                "every period — a landmark result connecting combinatorics and topology."
            ),
        ),
    )


def fixed_point_stability_summary() -> dict[str, list[str]]:
    """Return a mapping from stability class to profile keys."""
    result: dict[str, list[str]] = {}
    for p in get_fixed_point_profiles():
        result.setdefault(p.stability, []).append(p.key)
    return result


# ---------------------------------------------------------------------------
# TopologicalConjugacyProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TopologicalConjugacyProfile:
    """Teaching profile for topological conjugacy of dynamical systems.

    Two dynamical systems (X, f) and (Y, g) are topologically conjugate if
    there is a homeomorphism h : X → Y with h ∘ f = g ∘ h.  Conjugacy is
    the natural notion of isomorphism for dynamical systems.
    """

    key: str
    display_name: str
    system_f: str            # description of (X, f)
    system_g: str            # description of (Y, g)
    conjugacy_map: str       # description of h, or "unknown" / "does not exist"
    conjugacy_exists: bool
    invariants_preserved: tuple[str, ...]
    source_section: str
    notes: str


def get_conjugacy_profiles() -> tuple[TopologicalConjugacyProfile, ...]:
    """Return teaching profiles illustrating topological conjugacy."""
    return (
        TopologicalConjugacyProfile(
            key="doubling_map_conjugacy",
            display_name="Doubling map conjugate to tent map",
            system_f="Doubling map d : S¹ → S¹, d(θ) = 2θ mod 2π",
            system_g="Tent map T : [0,1] → [0,1], T(x) = 2x for x ≤ 1/2, 2(1−x) for x > 1/2",
            conjugacy_map="h : [0,1] → S¹, h(x) = e^{2πix} (after appropriate identification)",
            conjugacy_exists=True,
            invariants_preserved=(
                "topological entropy",
                "number of periodic points of each period",
                "existence of dense orbit",
                "sensitive dependence on initial conditions",
            ),
            source_section="Adams & Franzosa §8.2",
            notes=(
                "The doubling map on S¹ and the tent map on [0,1] are topologically "
                "conjugate; they have the same dynamical behaviour up to homeomorphism. "
                "Both are chaotic: they have sensitive dependence on initial conditions, "
                "dense periodic points, and topological transitivity."
            ),
        ),
        TopologicalConjugacyProfile(
            key="conjugacy_invariance_example",
            display_name="Conjugacy preserves periodic-orbit structure",
            system_f="f : X → X with period-n orbit {x, f(x), ..., fⁿ⁻¹(x)}",
            system_g="g : Y → Y conjugate to f via h",
            conjugacy_map="h : X → Y homeomorphism, h ∘ f = g ∘ h",
            conjugacy_exists=True,
            invariants_preserved=(
                "set of periods of periodic orbits",
                "topological entropy",
                "connectedness of non-wandering set",
                "transitivity",
            ),
            source_section="Adams & Franzosa §8.2",
            notes=(
                "If h ∘ f = g ∘ h and {x, f(x), ..., fⁿ⁻¹(x)} is a period-n orbit "
                "of f, then {h(x), h(f(x)), ..., h(fⁿ⁻¹(x))} is a period-n orbit of g. "
                "Proof: g(h(x)) = h(f(x)), so gⁿ(h(x)) = h(fⁿ(x)) = h(x). "
                "Conjugacy is thus an isomorphism of orbit structures."
            ),
        ),
        TopologicalConjugacyProfile(
            key="non_conjugate_example",
            display_name="Non-conjugate systems: different fixed-point counts",
            system_f="f : {1,2,3} → {1,2,3} (discrete), f has 2 fixed points",
            system_g="g : {1,2,3} → {1,2,3} (discrete), g has 1 fixed point",
            conjugacy_map="does not exist",
            conjugacy_exists=False,
            invariants_preserved=(),
            source_section="Adams & Franzosa §8.2",
            notes=(
                "The number of fixed points is a topological conjugacy invariant. "
                "If f has 2 fixed points and g has 1, no homeomorphism h can satisfy "
                "h ∘ f = g ∘ h, since h would have to map fixed points of f to fixed "
                "points of g bijectively (h is a bijection and g(h(x)) = h(f(x)) = h(x))."
            ),
        ),
        TopologicalConjugacyProfile(
            key="semi_conjugacy",
            display_name="Semi-conjugacy (factor map)",
            system_f="f : X → X (more complex system)",
            system_g="g : Y → Y (simpler quotient system)",
            conjugacy_map="h : X → Y continuous surjection (not necessarily injective), h ∘ f = g ∘ h",
            conjugacy_exists=True,
            invariants_preserved=(
                "topological entropy (h(f) ≥ h(g))",
                "existence of periodic orbits (in quotient)",
            ),
            source_section="Adams & Franzosa §8.2",
            notes=(
                "A semi-conjugacy (or factor map) is a continuous surjection h with "
                "h ∘ f = g ∘ h, but h need not be a homeomorphism. The system (Y, g) "
                "is a topological factor of (X, f). Entropy cannot increase under "
                "a factor map. Semi-conjugacy is weaker than conjugacy and is used "
                "when full conjugacy is unattainable."
            ),
        ),
    )


def conjugacy_exists_summary() -> dict[bool, list[str]]:
    """Return a mapping from conjugacy_exists flag to profile keys."""
    result: dict[bool, list[str]] = {}
    for p in get_conjugacy_profiles():
        result.setdefault(p.conjugacy_exists, []).append(p.key)
    return result


# ---------------------------------------------------------------------------
# Module-level registry
# ---------------------------------------------------------------------------

def dynamical_systems_profile_registry() -> dict[str, int]:
    """Return counts of profiles by category."""
    return {
        "orbit_profiles": len(get_orbit_profiles()),
        "fixed_point_profiles": len(get_fixed_point_profiles()),
        "conjugacy_profiles": len(get_conjugacy_profiles()),
    }


__all__ = [
    "OrbitProfile",
    "get_orbit_profiles",
    "orbit_type_summary",
    "FixedPointProfile",
    "get_fixed_point_profiles",
    "fixed_point_stability_summary",
    "TopologicalConjugacyProfile",
    "get_conjugacy_profiles",
    "conjugacy_exists_summary",
    "dynamical_systems_profile_registry",
]
