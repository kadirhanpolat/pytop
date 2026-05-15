"""Fixed point theorems — topological layer (FPT-01).

Provides teaching-oriented profile dataclasses for the topological fixed-point
theory covered in Adams & Franzosa §9.2 and §10.1.

Three profile families are defined:

* ``NoRetractionProfile``  — the no-retraction theorem (Dⁿ does not retract
                             onto Sⁿ⁻¹) in various dimensions.
* ``BrouwerFPTProfile``    — instances of the Brouwer Fixed-Point Theorem
                             for continuous maps on closed balls.
* ``RetractionProfile``    — positive retraction examples (spaces that DO
                             retract onto subspaces), to contrast with the
                             no-retraction theorem.

Source: AdamsFranzosa2008Topology §9.2, §10.1.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# NoRetractionProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NoRetractionProfile:
    """Teaching profile for the No-Retraction Theorem.

    The No-Retraction Theorem states: there is no continuous retraction
    r : Dⁿ → Sⁿ⁻¹ (from the closed n-ball onto its boundary sphere).

    This is the topological core from which the Brouwer FPT is derived.
    """

    key: str
    display_name: str
    ambient_space: str          # Dⁿ
    boundary_sphere: str        # Sⁿ⁻¹
    dimension: int              # n
    retraction_exists: bool     # always False for the no-retraction theorem
    proof_method: str           # "degree theory", "homology", "elementary (n=1)"
    source_section: str
    notes: str


def get_no_retraction_profiles() -> tuple[NoRetractionProfile, ...]:
    """Return No-Retraction profiles for dimensions 1, 2, and n."""
    return (
        NoRetractionProfile(
            key="no_retraction_D1_S0",
            display_name="No retraction D¹ → S⁰ (dimension 1)",
            ambient_space="D¹ = [−1, 1]",
            boundary_sphere="S⁰ = {−1, +1}",
            dimension=1,
            retraction_exists=False,
            proof_method="elementary (connectedness)",
            source_section="Adams & Franzosa §10.1",
            notes=(
                "The closed interval [−1,1] is connected, but its boundary S⁰ = {−1,+1} "
                "is disconnected. A continuous retraction r : [−1,1] → {−1,+1} would be "
                "a continuous surjection from a connected space to a disconnected space — "
                "impossible. This elementary argument gives the n=1 case without degree theory."
            ),
        ),
        NoRetractionProfile(
            key="no_retraction_D2_S1",
            display_name="No retraction D² → S¹ (dimension 2)",
            ambient_space="D² = closed unit disk in ℝ²",
            boundary_sphere="S¹ = unit circle",
            dimension=2,
            retraction_exists=False,
            proof_method="degree theory",
            source_section="Adams & Franzosa §9.2",
            notes=(
                "Suppose r : D² → S¹ is a continuous retraction (r|_{S¹} = id_{S¹}). "
                "The inclusion i : S¹ ↪ D² induces the zero map on π₁ (since D² is "
                "simply connected). But r ∘ i = id_{S¹} induces the identity on π₁(S¹) = ℤ. "
                "Composing: id = (r ∘ i)_* = r_* ∘ i_* = r_* ∘ 0 = 0. "
                "Contradiction. So no such retraction exists. "
                "Equivalently via degree theory: deg(id_{S¹}) = 1 ≠ 0 = deg(r ∘ i) "
                "since i_* kills the generator of H₁(S¹)."
            ),
        ),
        NoRetractionProfile(
            key="no_retraction_Dn_Sn1",
            display_name="No retraction Dⁿ → Sⁿ⁻¹ (general dimension)",
            ambient_space="Dⁿ = closed unit ball in ℝⁿ",
            boundary_sphere="Sⁿ⁻¹ = unit sphere in ℝⁿ",
            dimension=-1,   # -1 signals "general n"
            retraction_exists=False,
            proof_method="degree theory / homology (Hₙ₋₁)",
            source_section="Adams & Franzosa §9.2",
            notes=(
                "The general no-retraction theorem follows from the fact that "
                "Hₙ₋₁(Sⁿ⁻¹) = ℤ while Hₙ₋₁(Dⁿ) = 0 (Dⁿ is contractible). "
                "A retraction r : Dⁿ → Sⁿ⁻¹ would split the long exact sequence "
                "of the pair (Dⁿ, Sⁿ⁻¹), forcing a non-zero map ℤ → 0 — impossible. "
                "The n=2 case (degree-theory proof) generalises directly: "
                "deg(id_{Sⁿ⁻¹}) = 1 ≠ 0 = deg(r ∘ i_{Sⁿ⁻¹})."
            ),
        ),
    )


def no_retraction_by_dimension(n: int) -> NoRetractionProfile | None:
    """Return the no-retraction profile for dimension n (1 or 2), or the general profile."""
    for p in get_no_retraction_profiles():
        if p.dimension == n:
            return p
    # Fall back to general profile (dimension == -1)
    for p in get_no_retraction_profiles():
        if p.dimension == -1:
            return p
    return None


# ---------------------------------------------------------------------------
# BrouwerFPTProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BrouwerFPTProfile:
    """Teaching profile for an instance of the Brouwer Fixed-Point Theorem.

    Brouwer FPT: Every continuous map f : Dⁿ → Dⁿ has at least one fixed point.
    The theorem holds for any space homeomorphic to Dⁿ.
    """

    key: str
    display_name: str
    domain: str                 # description of the space (homeomorphic to Dⁿ)
    map_description: str        # description of f
    dimension: int              # n
    fixed_point_exists: bool    # always True
    proof_strategy: str         # how the FPT is proved for this case
    application_context: str    # real-world or mathematical motivation
    source_section: str
    notes: str


def get_brouwer_fpt_profiles() -> tuple[BrouwerFPTProfile, ...]:
    """Return Brouwer FPT profiles across dimensions and application contexts."""
    return (
        BrouwerFPTProfile(
            key="brouwer_fpt_D1",
            display_name="Brouwer FPT in dimension 1 — Intermediate Value Theorem",
            domain="D¹ = [0,1]",
            map_description="f : [0,1] → [0,1] continuous",
            dimension=1,
            fixed_point_exists=True,
            proof_strategy=(
                "Apply IVT to g(x) = f(x) − x. "
                "g(0) = f(0) ≥ 0 and g(1) = f(1) − 1 ≤ 0. "
                "By IVT, g(c) = 0 for some c ∈ [0,1], so f(c) = c."
            ),
            application_context=(
                "Any continuous schedule or assignment mapping [0,1] to itself "
                "must have a self-consistent point. "
                "Banach's contraction mapping theorem extends this to a quantitative "
                "version when f is a contraction."
            ),
            source_section="Adams & Franzosa §10.1",
            notes=(
                "The 1D Brouwer FPT is equivalent to the Intermediate Value Theorem, "
                "which follows from connectedness of [0,1]. No degree theory is needed. "
                "This case is the gateway to understanding the higher-dimensional theorem."
            ),
        ),
        BrouwerFPTProfile(
            key="brouwer_fpt_D2",
            display_name="Brouwer FPT in dimension 2",
            domain="D² = closed unit disk in ℝ²",
            map_description="f : D² → D² continuous",
            dimension=2,
            fixed_point_exists=True,
            proof_strategy=(
                "Suppose f has no fixed point. Define r : D² → S¹ by "
                "r(x) = the intersection of the ray from f(x) through x with S¹. "
                "r is continuous and r|_{S¹} = id_{S¹}: a retraction D² → S¹. "
                "This contradicts the No-Retraction Theorem. So f has a fixed point."
            ),
            application_context=(
                "Any continuous stirring of liquid in a disk leaves at least one "
                "point unmoved. Any continuous temperature map on a disk has a "
                "self-consistent point (used in climate modelling)."
            ),
            source_section="Adams & Franzosa §9.2",
            notes=(
                "The proof reduces Brouwer FPT to the No-Retraction Theorem: "
                "a fixed-point-free map would produce a retraction, which is impossible. "
                "The ray construction r is explicit: r(x) = x + t(x − f(x)) for the "
                "unique t ≥ 0 placing r(x) on S¹."
            ),
        ),
        BrouwerFPTProfile(
            key="brouwer_fpt_Dn",
            display_name="Brouwer FPT in dimension n (general)",
            domain="Dⁿ = closed unit ball in ℝⁿ",
            map_description="f : Dⁿ → Dⁿ continuous",
            dimension=-1,   # -1 signals "general n"
            fixed_point_exists=True,
            proof_strategy=(
                "Same ray-retraction argument as in n=2: a fixed-point-free f "
                "yields a retraction r : Dⁿ → Sⁿ⁻¹, contradicting the "
                "No-Retraction Theorem in dimension n."
            ),
            application_context=(
                "Nash equilibrium existence (via Kakutani's fixed-point theorem, "
                "which builds on Brouwer). "
                "Existence theorems in economics, game theory, and nonlinear PDEs."
            ),
            source_section="Adams & Franzosa §9.2",
            notes=(
                "The theorem holds for any compact convex set homeomorphic to Dⁿ. "
                "Generalisations: Schauder FPT (infinite-dimensional Banach spaces), "
                "Kakutani FPT (set-valued maps), Lefschetz FPT (Euler-characteristic "
                "condition). The Brouwer FPT is the finite-dimensional core of all these."
            ),
        ),
        BrouwerFPTProfile(
            key="brouwer_fpt_geographic_map",
            display_name="Brouwer FPT — geographic map on table",
            domain="A planar map of a region R, laid flat on a table covering R",
            map_description=(
                "f : R → R; f(p) = the table point directly beneath map-point p. "
                "f is a continuous map from the region to itself."
            ),
            dimension=2,
            fixed_point_exists=True,
            proof_strategy="Apply Brouwer FPT to f : D² → D² (after homeomorphism with D²).",
            application_context=(
                "A popular illustration of Brouwer FPT: at least one point on the map "
                "lies directly above the actual geographic location it represents."
            ),
            source_section="Adams & Franzosa §10.1",
            notes=(
                "This is a classical popularisation of the theorem. The map f is "
                "continuous because nearby points on the map correspond to nearby "
                "geographic locations (the map is a homeomorphism of compact regions). "
                "The fixed point is the point where 'you are here' is literally accurate."
            ),
        ),
        BrouwerFPTProfile(
            key="brouwer_fpt_coffee_stirring",
            display_name="Brouwer FPT — coffee stirring",
            domain="D² (cross-section of cup)",
            map_description=(
                "f : D² → D²; f(p) = position of the fluid particle initially at p "
                "after one complete stirring motion."
            ),
            dimension=2,
            fixed_point_exists=True,
            proof_strategy="f is a continuous map D² → D²; apply Brouwer FPT.",
            application_context=(
                "After any continuous stirring of a disk-shaped container, "
                "at least one fluid particle returns to its original position."
            ),
            source_section="Adams & Franzosa §10.1",
            notes=(
                "The stirring map is continuous (fluid dynamics with no tearing). "
                "The fixed point need not be at the centre; it can be anywhere. "
                "With vigorous non-planar stirring (a 3D motion), Brouwer FPT in "
                "dimension 3 applies instead."
            ),
        ),
    )


def brouwer_fpt_by_dimension(n: int) -> tuple[BrouwerFPTProfile, ...]:
    """Return all Brouwer FPT profiles of the given dimension (or general, n=-1)."""
    return tuple(p for p in get_brouwer_fpt_profiles() if p.dimension == n)


# ---------------------------------------------------------------------------
# RetractionProfile — positive examples (contrast with no-retraction)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RetractionProfile:
    """Teaching profile for a retraction (a positive example).

    A retraction r : X → A is a continuous map such that r|_A = id_A.
    Positive examples contrast with the No-Retraction Theorem (Dⁿ → Sⁿ⁻¹ fails).
    """

    key: str
    display_name: str
    total_space: str
    retract: str
    retraction_formula: str
    retraction_exists: bool     # always True
    deformation_retract: bool   # whether it is also a deformation retract
    source_section: str
    notes: str


def get_retraction_profiles() -> tuple[RetractionProfile, ...]:
    """Return teaching profiles for valid retractions."""
    return (
        RetractionProfile(
            key="retraction_Rn_to_origin",
            display_name="ℝⁿ retracts onto {0}",
            total_space="ℝⁿ",
            retract="{0} (the origin)",
            retraction_formula="r(x) = 0 for all x ∈ ℝⁿ",
            retraction_exists=True,
            deformation_retract=True,
            source_section="Adams & Franzosa §10.1",
            notes=(
                "The constant map r(x) = 0 is a deformation retraction: "
                "H(x,t) = (1−t)x retracts ℝⁿ to the origin via a straight-line homotopy. "
                "Any convex set deformation retracts to any of its points."
            ),
        ),
        RetractionProfile(
            key="retraction_punctured_plane_to_circle",
            display_name="ℝ²\\ {0} deformation retracts onto S¹",
            total_space="ℝ²\\ {0} (punctured plane)",
            retract="S¹ = unit circle",
            retraction_formula="r(x) = x / |x|",
            retraction_exists=True,
            deformation_retract=True,
            source_section="Adams & Franzosa §10.1",
            notes=(
                "r(x) = x/|x| normalises every non-zero vector to the unit circle. "
                "The deformation retraction is H(x,t) = x / |x|^t (or equivalently "
                "H(x,t) = ((1−t)|x| + t) · x/|x|). "
                "This shows π₁(ℝ²\\ {0}) = π₁(S¹) = ℤ."
            ),
        ),
        RetractionProfile(
            key="retraction_cylinder_to_circle",
            display_name="S¹ × [0,1] deformation retracts onto S¹ × {0}",
            total_space="S¹ × [0,1] (finite cylinder)",
            retract="S¹ × {0} (bottom circle)",
            retraction_formula="r(θ, t) = (θ, 0)",
            retraction_exists=True,
            deformation_retract=True,
            source_section="Adams & Franzosa §10.1",
            notes=(
                "H(θ, t, s) = (θ, (1−s)t) is the deformation retraction. "
                "More generally, any product X × [0,1] deformation retracts onto X × {0}. "
                "This is the model for the cylinder contraction used in homotopy theory."
            ),
        ),
        RetractionProfile(
            key="retraction_Dn_to_point",
            display_name="Dⁿ deformation retracts onto any interior point",
            total_space="Dⁿ = closed unit ball",
            retract="{0} (the origin, or any interior point)",
            retraction_formula="r(x) = 0",
            retraction_exists=True,
            deformation_retract=True,
            source_section="Adams & Franzosa §10.1",
            notes=(
                "H(x,t) = (1−t)x deformation retracts Dⁿ to the origin. "
                "This shows Dⁿ is contractible (homotopy equivalent to a point). "
                "Contrast: Dⁿ does NOT deformation retract onto its boundary Sⁿ⁻¹ "
                "(this is exactly the No-Retraction Theorem)."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# Module-level registry
# ---------------------------------------------------------------------------

def fixed_point_theorem_registry() -> dict[str, int]:
    """Return counts of profiles by category."""
    return {
        "no_retraction_profiles": len(get_no_retraction_profiles()),
        "brouwer_fpt_profiles": len(get_brouwer_fpt_profiles()),
        "retraction_profiles": len(get_retraction_profiles()),
    }
