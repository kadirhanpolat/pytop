"""Chaos profile module — DYN-02.

Provides teaching-oriented profile dataclasses for chaotic dynamical systems
as covered in Adams & Franzosa §8.3–8.5.

Three complementary profile families are defined:

* ``ChaosProfile``      — captures the three ingredients of Devaney chaos and
                          classifies a system as chaotic or non-chaotic.
* ``ChaoticMapProfile`` — records key properties of named chaotic maps (tent
                          map, logistic map, doubling map, shift map).
* ``SymbolicDynamicsProfile`` — describes the symbolic dynamics / sequence-space
                          model used to analyse chaotic maps via conjugacy.

Profiles are frozen dataclasses: they record teaching metadata only and perform
no numerical computation.

Source: AdamsFranzosa2008Topology §8.3–8.5.
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# ChaosProfile — Devaney's three-ingredient definition
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ChaosProperty:
    """A single ingredient of Devaney chaos for a dynamical system (X, f)."""

    name: str
    formal_statement: str
    intuition: str
    source_section: str


def get_devaney_chaos_properties() -> tuple[ChaosProperty, ...]:
    """Return the three properties that constitute Devaney chaos.

    A continuous map f : X → X on a metric space X is **chaotic** in the sense
    of Devaney (Adams & Franzosa §8.3) if it satisfies all three properties.
    """
    return (
        ChaosProperty(
            name="Sensitive dependence on initial conditions",
            formal_statement=(
                "There exists δ > 0 such that for every x ∈ X and every "
                "neighbourhood U of x there exists y ∈ U and n ≥ 0 with "
                "d(fⁿ(x), fⁿ(y)) > δ."
            ),
            intuition=(
                "No matter how close two starting points are, their orbits "
                "eventually separate by at least δ. Small measurement errors "
                "grow into large prediction errors — the hallmark of chaos."
            ),
            source_section="Adams & Franzosa §8.3",
        ),
        ChaosProperty(
            name="Topological transitivity",
            formal_statement=(
                "For every pair of non-empty open sets U, V ⊆ X there exists "
                "n ≥ 0 such that fⁿ(U) ∩ V ≠ ∅."
            ),
            intuition=(
                "The map mixes every open region with every other: no part of "
                "the space is isolated from the rest under iteration. "
                "Equivalent to the existence of a dense orbit when X is a "
                "complete separable metric space (Birkhoff transitivity theorem)."
            ),
            source_section="Adams & Franzosa §8.3",
        ),
        ChaosProperty(
            name="Dense periodic orbits",
            formal_statement=(
                "The set of periodic points Per(f) = {x ∈ X : fⁿ(x) = x for some n ≥ 1} "
                "is dense in X."
            ),
            intuition=(
                "Every point can be approximated arbitrarily closely by a periodic "
                "orbit. This provides an element of regularity within the overall "
                "unpredictability — an apparent paradox that characterises chaos."
            ),
            source_section="Adams & Franzosa §8.3",
        ),
    )


@dataclass(frozen=True)
class ChaosProfile:
    """Classification of a dynamical system with respect to Devaney chaos."""

    key: str
    display_name: str
    space_description: str
    map_description: str
    is_chaotic: bool
    has_sensitive_dependence: bool
    has_topological_transitivity: bool
    has_dense_periodic_orbits: bool
    topological_entropy: str      # symbolic value or "0", "log 2", "> 0", "unknown"
    source_section: str
    notes: str


def get_chaos_profiles() -> tuple[ChaosProfile, ...]:
    """Return ChaosProfiles for the canonical examples in Adams & Franzosa §8.3–8.5."""
    return (
        ChaosProfile(
            key="tent_map_chaotic",
            display_name="Tent map on [0,1] — chaotic",
            space_description="[0,1] with the standard metric",
            map_description="T(x) = 2x for x ≤ 1/2; T(x) = 2(1−x) for x > 1/2",
            is_chaotic=True,
            has_sensitive_dependence=True,
            has_topological_transitivity=True,
            has_dense_periodic_orbits=True,
            topological_entropy="log 2",
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The tent map is the canonical textbook chaotic map. "
                "Sensitive dependence: nearby points separate at rate 2ⁿ per step. "
                "Dense periodic orbits: dyadic rationals p/2ⁿ are all periodic. "
                "Conjugate to the logistic map f₄(x) = 4x(1−x) via h(x) = sin²(πx/2). "
                "Topological entropy = log 2 (one bit of information destroyed per step)."
            ),
        ),
        ChaosProfile(
            key="logistic_map_r4_chaotic",
            display_name="Logistic map f₄(x) = 4x(1−x) — chaotic",
            space_description="[0,1] with the standard metric",
            map_description="f₄(x) = 4x(1−x)",
            is_chaotic=True,
            has_sensitive_dependence=True,
            has_topological_transitivity=True,
            has_dense_periodic_orbits=True,
            topological_entropy="log 2",
            source_section="Adams & Franzosa §8.5",
            notes=(
                "The logistic map at r=4 is fully chaotic. "
                "Topologically conjugate to the tent map via h(x) = sin²(πx/2): "
                "h ∘ T = f₄ ∘ h. Since conjugacy preserves all dynamical properties, "
                "f₄ inherits the chaos of the tent map. "
                "For r < 3.57... the logistic map is not chaotic (period-doubling route). "
                "Topological entropy = log 2 (same as tent map, as expected from conjugacy)."
            ),
        ),
        ChaosProfile(
            key="logistic_map_r_small_non_chaotic",
            display_name="Logistic map f_r(x) = rx(1−x), r < 3 — non-chaotic",
            space_description="[0,1] with the standard metric",
            map_description="f_r(x) = rx(1−x), 0 < r < 3",
            is_chaotic=False,
            has_sensitive_dependence=False,
            has_topological_transitivity=False,
            has_dense_periodic_orbits=False,
            topological_entropy="0",
            source_section="Adams & Franzosa §8.5",
            notes=(
                "For r ∈ (0, 3), the logistic map has a single stable fixed point "
                "x* = (r−1)/r that attracts all orbits in (0,1). "
                "No sensitive dependence: all nearby orbits converge to x*. "
                "No topological transitivity: orbits do not mix across the interval. "
                "Topological entropy = 0. This parameter regime models population "
                "dynamics with a stable equilibrium."
            ),
        ),
        ChaosProfile(
            key="doubling_map_chaotic",
            display_name="Doubling map on S¹ — chaotic",
            space_description="S¹ = ℝ/ℤ with the quotient metric",
            map_description="d(θ) = 2θ mod 1 (angle doubling)",
            is_chaotic=True,
            has_sensitive_dependence=True,
            has_topological_transitivity=True,
            has_dense_periodic_orbits=True,
            topological_entropy="log 2",
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The doubling map on the circle is chaotic. "
                "Sensitive dependence: angles differing by ε become ε·2ⁿ apart after n steps. "
                "Dense periodic orbits: rational angles p/q (in lowest terms) are periodic of period "
                "equal to the multiplicative order of 2 mod q. "
                "Topologically semi-conjugate to the one-sided shift on {0,1}^ℕ via binary expansion. "
                "Topological entropy = log 2."
            ),
        ),
        ChaosProfile(
            key="irrational_rotation_non_chaotic",
            display_name="Irrational rotation of S¹ — non-chaotic",
            space_description="S¹ = ℝ/ℤ with the quotient metric",
            map_description="R_α(θ) = θ + α mod 1, α ∉ ℚ",
            is_chaotic=False,
            has_sensitive_dependence=False,
            has_topological_transitivity=True,
            has_dense_periodic_orbits=False,
            topological_entropy="0",
            source_section="Adams & Franzosa §8.3",
            notes=(
                "Irrational rotation is topologically transitive (every orbit is dense "
                "by Weyl equidistribution) but has NO periodic points at all, and "
                "NO sensitive dependence (the map is an isometry: d(R_α(x), R_α(y)) = d(x,y)). "
                "It satisfies only one of Devaney's three conditions. "
                "This example demonstrates that transitivity alone does not imply chaos — "
                "all three conditions are needed."
            ),
        ),
    )


def chaos_status_summary() -> dict[str, list[str]]:
    """Return mapping from 'chaotic'/'non_chaotic' to profile keys."""
    result: dict[str, list[str]] = {}
    for p in get_chaos_profiles():
        label = "chaotic" if p.is_chaotic else "non_chaotic"
        result.setdefault(label, []).append(p.key)
    return result


# ---------------------------------------------------------------------------
# ChaoticMapProfile — canonical map families
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ChaoticMapProfile:
    """Teaching profile for a named family of maps studied in chaos theory."""

    key: str
    display_name: str
    domain: str
    formula: str
    parameter_range: str      # e.g. "r ∈ (0, 4]" or "fixed"
    chaotic_parameter_range: str  # sub-range where chaos occurs
    conjugacy: str            # conjugate to what, or "none known"
    topological_entropy_formula: str
    source_section: str
    notes: str


def get_chaotic_map_profiles() -> tuple[ChaoticMapProfile, ...]:
    """Return teaching profiles for the canonical chaotic map families."""
    return (
        ChaoticMapProfile(
            key="tent_map",
            display_name="Tent map",
            domain="[0,1]",
            formula="T(x) = 2x for x ≤ 1/2; T(x) = 2(1−x) for x > 1/2",
            parameter_range="fixed (slope ±2)",
            chaotic_parameter_range="always (for slope 2)",
            conjugacy="Conjugate to logistic map f₄ via h(x)=sin²(πx/2); semi-conjugate to one-sided shift on {0,1}^ℕ via binary expansion",
            topological_entropy_formula="h(T) = log 2",
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The tent map is piecewise linear with slope ±2. Its dynamics are "
                "transparent: periodic points are exactly the dyadic rationals with "
                "denominators of the form 2ⁿ(2ᵏ−1)⁻¹. The binary expansion of x "
                "provides a symbolic coding that makes the tent map a model for "
                "the one-sided shift, the simplest infinite chaotic system."
            ),
        ),
        ChaoticMapProfile(
            key="logistic_map",
            display_name="Logistic map",
            domain="[0,1]",
            formula="f_r(x) = rx(1−x)",
            parameter_range="r ∈ (0, 4]",
            chaotic_parameter_range="r ∈ [r∞, 4] where r∞ ≈ 3.5699... (Feigenbaum point)",
            conjugacy="At r=4: conjugate to tent map via h(x)=sin²(πx/2)",
            topological_entropy_formula="h(f_r) = max(0, log(r/4)) for r ∈ (0,4]; equals log 2 at r=4",
            source_section="Adams & Franzosa §8.5",
            notes=(
                "The logistic map models population dynamics (r = growth rate). "
                "As r increases from 0 to 4, it undergoes a period-doubling cascade: "
                "stable fixed point (r<3) → period 2 (3<r<3.449) → period 4 → ... → chaos. "
                "The ratio of successive period-doubling bifurcation intervals converges to "
                "the Feigenbaum constant δ ≈ 4.669..., a universal constant for this "
                "class of unimodal maps."
            ),
        ),
        ChaoticMapProfile(
            key="doubling_map",
            display_name="Circle doubling map",
            domain="S¹ = ℝ/ℤ",
            formula="d(θ) = 2θ mod 1",
            parameter_range="fixed",
            chaotic_parameter_range="always",
            conjugacy="Semi-conjugate to one-sided shift on {0,1}^ℕ via binary expansion; conjugate to tent map after identification [0,1]/{0~1} ≅ S¹",
            topological_entropy_formula="h(d) = log 2",
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The doubling map is the simplest example of an expanding map on a compact space. "
                "Its periodic points are exactly the rationals with odd denominators. "
                "The binary expansion θ = 0.b₁b₂b₃... maps θ ↦ 0.b₂b₃b₄... under d, "
                "showing that the doubling map is a left shift on binary sequences — "
                "the paradigmatic example of symbolic dynamics."
            ),
        ),
        ChaoticMapProfile(
            key="shift_map",
            display_name="One-sided shift map on {0,1}^ℕ",
            domain="{0,1}^ℕ with the product topology (metric: d(s,t) = Σ |sₙ−tₙ|/2ⁿ)",
            formula="σ(s₁s₂s₃...) = s₂s₃s₄...",
            parameter_range="fixed",
            chaotic_parameter_range="always",
            conjugacy="Semi-conjugate to doubling map via binary expansion; conjugate to tent map symbolically",
            topological_entropy_formula="h(σ) = log 2",
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The shift map on sequence space is the canonical model for chaos: "
                "it is topologically conjugate to the tent map (and the doubling map) "
                "via the binary-expansion semi-conjugacy. "
                "Periodic points = eventually periodic sequences = sequences with periodic tails. "
                "Dense periodic points: any finite block can be extended to a periodic sequence. "
                "Sensitive dependence: sequences differing only in position n are within 1/2ⁿ "
                "but their n-th iterates differ in the first position by 1."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# SymbolicDynamicsProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SymbolicDynamicsProfile:
    """Teaching profile for symbolic dynamics / sequence-space models.

    Symbolic dynamics encodes orbits of a continuous map as sequences over a
    finite alphabet, making combinatorial analysis possible.
    """

    key: str
    display_name: str
    alphabet: tuple[str, ...]
    sequence_space: str
    shift_map: str
    original_system: str
    coding_map: str             # the semi-conjugacy / conjugacy h
    coding_map_properties: tuple[str, ...]
    source_section: str
    notes: str


def get_symbolic_dynamics_profiles() -> tuple[SymbolicDynamicsProfile, ...]:
    """Return teaching profiles for symbolic dynamics constructions."""
    return (
        SymbolicDynamicsProfile(
            key="binary_coding_tent_map",
            display_name="Binary symbolic coding of the tent map",
            alphabet=("0", "1"),
            sequence_space="{0,1}^ℕ with the product topology",
            shift_map="σ(s₁s₂s₃...) = s₂s₃s₄...",
            original_system="Tent map T on [0,1]",
            coding_map=(
                "h : [0,1] → {0,1}^ℕ; h(x)ₙ = 0 if Tⁿ⁻¹(x) ≤ 1/2, else 1. "
                "Equivalently, h(x) is the itinerary of x under T."
            ),
            coding_map_properties=(
                "h is surjective (every binary sequence is an itinerary)",
                "h ∘ T = σ ∘ h (semi-conjugacy)",
                "h is 2-to-1 on dyadic rationals (the only ambiguous points)",
                "h is a homeomorphism on [0,1] \\ {dyadic rationals}",
            ),
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The itinerary map encodes each orbit of T by recording whether "
                "successive iterates land in [0, 1/2] (symbol 0) or (1/2, 1] (symbol 1). "
                "The coding semi-conjugacy h ∘ T = σ ∘ h shows that the tent map is "
                "a model for the shift on binary sequences. This makes the combinatorics "
                "of binary sequences directly applicable to tent map dynamics."
            ),
        ),
        SymbolicDynamicsProfile(
            key="binary_coding_doubling_map",
            display_name="Binary symbolic coding of the doubling map",
            alphabet=("0", "1"),
            sequence_space="{0,1}^ℕ with the product topology",
            shift_map="σ(s₁s₂s₃...) = s₂s₃s₄...",
            original_system="Doubling map d(θ) = 2θ mod 1 on S¹ = ℝ/ℤ",
            coding_map=(
                "h : S¹ → {0,1}^ℕ; h(θ)ₙ = ⌊2ⁿθ⌋ mod 2 "
                "(the n-th binary digit of θ). "
                "Equivalently, h(θ) is the binary expansion of θ."
            ),
            coding_map_properties=(
                "h ∘ d = σ ∘ h (semi-conjugacy)",
                "h is surjective",
                "h is 2-to-1 on dyadic rationals (two binary expansions: finite and infinite)",
                "h is a homeomorphism off the dyadic rationals",
            ),
            source_section="Adams & Franzosa §8.4",
            notes=(
                "The binary expansion θ = 0.b₁b₂b₃... satisfies "
                "d(θ) = 2θ mod 1 = 0.b₂b₃b₄..., which is exactly the shift. "
                "This is the simplest and most explicit semi-conjugacy in symbolic dynamics: "
                "the doubling map IS the shift on binary expansions, modulo the two-expansion "
                "ambiguity at dyadic rationals."
            ),
        ),
        SymbolicDynamicsProfile(
            key="subshift_of_finite_type",
            display_name="Subshift of finite type (SFT)",
            alphabet=("0", "1", "...", "k−1"),
            sequence_space="Σ_A = {s ∈ {0,...,k−1}^ℕ : A_{sₙ, sₙ₊₁} = 1 for all n}",
            shift_map="σ|_{Σ_A}: left shift restricted to Σ_A",
            original_system="Any topological Markov chain with transition matrix A",
            coding_map="Depends on the specific system being modelled",
            coding_map_properties=(
                "Σ_A is a compact, shift-invariant subspace of {0,...,k−1}^ℕ",
                "The restricted shift σ|_{Σ_A} is continuous",
                "Topological entropy h(σ|_{Σ_A}) = log(spectral radius of A)",
            ),
            source_section="Adams & Franzosa §8.4",
            notes=(
                "A subshift of finite type restricts the shift to sequences satisfying "
                "a Markov (nearest-neighbour) constraint encoded by a 0-1 matrix A. "
                "SFTs are the fundamental objects of symbolic dynamics and provide "
                "models for many physical systems with memory. The topological entropy "
                "is computable from the largest eigenvalue of A — a key formula connecting "
                "linear algebra and chaos."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# Module-level registry
# ---------------------------------------------------------------------------

def chaos_profile_registry() -> dict[str, int]:
    """Return counts of profiles by category."""
    return {
        "devaney_chaos_properties": len(get_devaney_chaos_properties()),
        "chaos_profiles": len(get_chaos_profiles()),
        "chaotic_map_profiles": len(get_chaotic_map_profiles()),
        "symbolic_dynamics_profiles": len(get_symbolic_dynamics_profiles()),
    }


__all__ = [
    "ChaosProperty",
    "get_devaney_chaos_properties",
    "ChaosProfile",
    "get_chaos_profiles",
    "chaos_status_summary",
    "ChaoticMapProfile",
    "get_chaotic_map_profiles",
    "SymbolicDynamicsProfile",
    "get_symbolic_dynamics_profiles",
    "chaos_profile_registry",
]
