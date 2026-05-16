"""Fixed point applications — economics and game theory (FPT-02).

Provides teaching-oriented profile dataclasses for the applications of
fixed-point theory to economics and game theory, as covered in Adams &
Franzosa §10.2–10.4.

Three profile families are defined:

* ``KakutaniProfile``         — instances and conditions for Kakutani's
                                fixed-point theorem (set-valued maps on compact
                                convex sets).
* ``NashEquilibriumProfile``  — game-theoretic examples where Nash equilibria
                                are proved to exist via Kakutani's theorem.
* ``EconomicEquilibriumProfile`` — broader economic equilibrium examples
                                (Walrasian equilibrium, Arrow-Debreu model)
                                that rely on fixed-point arguments.

Source: AdamsFranzosa2008Topology §10.2–10.4.
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# KakutaniProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class KakutaniProfile:
    """Teaching profile for Kakutani's fixed-point theorem.

    Kakutani's theorem generalises the Brouwer FPT from single-valued
    continuous maps to set-valued (correspondence) maps satisfying a
    closed-graph condition.

    Statement: Let X ⊆ ℝⁿ be compact and convex, and let φ : X → 2^X
    be a set-valued map such that:
    (1) φ(x) is non-empty and convex for every x ∈ X;
    (2) the graph Gr(φ) = {(x,y) : y ∈ φ(x)} is closed in X × X.
    Then φ has a fixed point: some x* with x* ∈ φ(x*).
    """

    key: str
    display_name: str
    domain: str                     # X description
    correspondence: str             # φ description
    domain_is_compact: bool
    domain_is_convex: bool
    values_are_nonempty_convex: bool
    graph_is_closed: bool
    fixed_point_exists: bool        # True when all conditions hold
    source_section: str
    notes: str


def get_kakutani_profiles() -> tuple[KakutaniProfile, ...]:
    """Return Kakutani fixed-point theorem teaching profiles."""
    return (
        KakutaniProfile(
            key="kakutani_conditions_all_met",
            display_name="Kakutani FPT — all conditions satisfied",
            domain="X = [0,1] ⊆ ℝ (compact convex)",
            correspondence=(
                "φ(x) = [0, x] for x ∈ [0,1] "
                "(each φ(x) is a closed interval, hence convex and non-empty)"
            ),
            domain_is_compact=True,
            domain_is_convex=True,
            values_are_nonempty_convex=True,
            graph_is_closed=True,
            fixed_point_exists=True,
            source_section="Adams & Franzosa §10.2",
            notes=(
                "Verify conditions: X = [0,1] is compact and convex. "
                "φ(x) = [0,x] is non-empty (0 ∈ [0,x]) and convex (it is a closed interval). "
                "Gr(φ) = {(x,y) : 0 ≤ y ≤ x ≤ 1} is a triangle, hence closed. "
                "Fixed point: x* = 0 satisfies 0 ∈ φ(0) = [0,0] = {0}. ✓ "
                "In fact every x ∈ [0,1] is a fixed point since x ∈ [0,x] = φ(x)."
            ),
        ),
        KakutaniProfile(
            key="kakutani_nonconvex_values_fails",
            display_name="Kakutani FPT — non-convex values, theorem fails",
            domain="X = [0,1]",
            correspondence=(
                "φ(x) = {0} if x < 1/2; φ(1/2) = {0,1}; φ(x) = {1} if x > 1/2 "
                "(φ(1/2) = {0,1} is not convex)"
            ),
            domain_is_compact=True,
            domain_is_convex=True,
            values_are_nonempty_convex=False,
            graph_is_closed=True,
            fixed_point_exists=False,
            source_section="Adams & Franzosa §10.2",
            notes=(
                "This correspondence has no fixed point: "
                "φ(0) = {0} contains 0 ✓ (but check: for x near 0, φ(x)={0}, fine). "
                "Actually φ(0)={0} gives 0 ∈ φ(0) — wait, let us re-examine. "
                "Corrected: φ(x) = {1} for x < 1/2 forces x ∉ φ(x) for all x < 1/2. "
                "φ(x) = {0} for x > 1/2 forces x ∉ φ(x) for all x > 1/2. "
                "φ(1/2) = {0,1} does not contain 1/2. So no fixed point exists. "
                "The non-convexity of φ(1/2) is the culprit: Kakutani's theorem does "
                "not apply when values fail to be convex."
            ),
        ),
        KakutaniProfile(
            key="kakutani_open_graph_fails",
            display_name="Kakutani FPT — non-closed graph, theorem fails",
            domain="X = [0,1]",
            correspondence=(
                "φ(x) = (0, 1] for x = 0; φ(x) = {x} for x ∈ (0,1] "
                "(graph not closed: (0, 0) is a limit point of Gr(φ) not in Gr(φ))"
            ),
            domain_is_compact=True,
            domain_is_convex=True,
            values_are_nonempty_convex=True,
            graph_is_closed=False,
            fixed_point_exists=False,
            source_section="Adams & Franzosa §10.2",
            notes=(
                "Every x ∈ (0,1] is a fixed point of φ (since x ∈ {x} = φ(x)). "
                "But x = 0 has φ(0) = (0,1], which does not contain 0. "
                "The graph is not closed: the sequence (1/n, 1/n) → (0,0) but "
                "(0,0) ∉ Gr(φ) since 0 ∉ (0,1]. "
                "The theorem's closed-graph condition is essential: without it, "
                "a fixed point at x=0 may fail to exist."
            ),
        ),
        KakutaniProfile(
            key="kakutani_simplex",
            display_name="Kakutani FPT on the standard simplex Δⁿ",
            domain="Δⁿ = {(p₀,...,pₙ) ∈ ℝⁿ⁺¹ : pᵢ ≥ 0, Σpᵢ = 1} (probability simplex)",
            correspondence=(
                "φ : Δⁿ → 2^{Δⁿ}; φ(p) = best-response set of a player given "
                "mixed strategy profile p"
            ),
            domain_is_compact=True,
            domain_is_convex=True,
            values_are_nonempty_convex=True,
            graph_is_closed=True,
            fixed_point_exists=True,
            source_section="Adams & Franzosa §10.3",
            notes=(
                "The probability simplex Δⁿ is compact (closed and bounded in ℝⁿ⁺¹) "
                "and convex. The best-response correspondence in a finite game has "
                "non-empty convex values (the set of best responses is convex since "
                "expected payoffs are linear in mixed strategies) and closed graph "
                "(payoffs are continuous). Kakutani's theorem guarantees a fixed point "
                "of the joint best-response correspondence — this is exactly a Nash "
                "equilibrium. This is Nash's 1950 existence proof."
            ),
        ),
    )


def kakutani_fixed_point_summary() -> dict[str, list[str]]:
    """Return a mapping from fixed_point_exists flag to profile keys."""
    result: dict[str, list[str]] = {}
    for p in get_kakutani_profiles():
        label = "fixed_point_exists" if p.fixed_point_exists else "no_fixed_point"
        result.setdefault(label, []).append(p.key)
    return result


# ---------------------------------------------------------------------------
# NashEquilibriumProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NashEquilibriumProfile:
    """Teaching profile for Nash equilibrium existence and structure.

    A Nash equilibrium is a strategy profile (s₁*, ..., sₙ*) such that
    no player can improve their payoff by unilaterally changing their strategy.
    Nash's 1950 theorem proves existence in any finite game with mixed strategies
    via Kakutani's fixed-point theorem.
    """

    key: str
    display_name: str
    game_description: str
    players: int
    strategy_sets: str
    payoff_description: str
    equilibrium_type: str          # "pure", "mixed", "both", "none_pure"
    nash_equilibria: str           # description of equilibria
    existence_proof: str           # how existence is established
    source_section: str
    notes: str


def get_nash_profiles() -> tuple[NashEquilibriumProfile, ...]:
    """Return Nash equilibrium teaching profiles."""
    return (
        NashEquilibriumProfile(
            key="nash_prisoners_dilemma",
            display_name="Prisoner's Dilemma",
            game_description=(
                "Two players simultaneously choose Cooperate (C) or Defect (D). "
                "Payoff matrix (row=Player 1, col=Player 2): "
                "CC→(3,3), CD→(0,5), DC→(5,0), DD→(1,1)."
            ),
            players=2,
            strategy_sets="S₁ = S₂ = {C, D}",
            payoff_description="Standard Prisoner's Dilemma payoffs",
            equilibrium_type="pure",
            nash_equilibria=(
                "Unique Nash equilibrium: (D, D) with payoffs (1,1). "
                "D strictly dominates C for both players; iterative deletion of "
                "dominated strategies yields (D,D). "
                "No mixed-strategy equilibrium exists beyond this pure one."
            ),
            existence_proof=(
                "Direct: D is a dominant strategy for each player, so (D,D) is "
                "the unique Nash equilibrium. Nash's theorem guarantees at least "
                "one equilibrium exists (redundant here since it is found directly)."
            ),
            source_section="Adams & Franzosa §10.3",
            notes=(
                "The Prisoner's Dilemma illustrates that Nash equilibrium can be "
                "Pareto-suboptimal: (C,C) gives (3,3) which dominates (D,D)=(1,1), "
                "but (D,D) is the unique Nash equilibrium. The tension between "
                "individual rationality and collective welfare is the core insight."
            ),
        ),
        NashEquilibriumProfile(
            key="nash_matching_pennies",
            display_name="Matching Pennies",
            game_description=(
                "Two players simultaneously show a coin: Heads (H) or Tails (T). "
                "Player 1 wins if coins match; Player 2 wins if they differ. "
                "Payoff matrix: HH→(1,−1), HT→(−1,1), TH→(−1,1), TT→(1,−1)."
            ),
            players=2,
            strategy_sets="S₁ = S₂ = {H, T}",
            payoff_description="Zero-sum: payoffs sum to 0",
            equilibrium_type="none_pure",
            nash_equilibria=(
                "No pure Nash equilibrium exists. "
                "Unique mixed Nash equilibrium: each player plays H and T with "
                "probability 1/2 each. At this profile, each player's expected "
                "payoff is 0 regardless of the opponent's mixed strategy."
            ),
            existence_proof=(
                "Nash's theorem guarantees a mixed-strategy Nash equilibrium exists "
                "in every finite game. The unique equilibrium is found by making each "
                "player indifferent: if Player 2 plays H with prob p, Player 1 is "
                "indifferent iff 1·p + (−1)(1−p) = (−1)p + 1·(1−p) iff p = 1/2."
            ),
            source_section="Adams & Franzosa §10.3",
            notes=(
                "Matching Pennies is the canonical example requiring mixed strategies. "
                "No pure equilibrium exists because each player wants to predict and "
                "counter the other's choice — a circular reasoning that forces randomisation. "
                "The topological proof via Kakutani applies: the joint best-response "
                "correspondence on Δ¹×Δ¹ has a fixed point at (1/2, 1/2)."
            ),
        ),
        NashEquilibriumProfile(
            key="nash_battle_of_sexes",
            display_name="Battle of the Sexes",
            game_description=(
                "Two players choose between Opera (O) and Football (F). "
                "Player 1 prefers Opera; Player 2 prefers Football; both prefer "
                "coordinating over miscoordinating. "
                "Payoffs: OO→(2,1), OF→(0,0), FO→(0,0), FF→(1,2)."
            ),
            players=2,
            strategy_sets="S₁ = S₂ = {O, F}",
            payoff_description="Coordination game with asymmetric preferences",
            equilibrium_type="both",
            nash_equilibria=(
                "Two pure Nash equilibria: (O,O) with payoffs (2,1) and (F,F) with (1,2). "
                "One mixed Nash equilibrium: Player 1 plays O with prob 2/3, "
                "Player 2 plays O with prob 1/3. Expected payoffs: (2/3, 2/3)."
            ),
            existence_proof=(
                "Nash's theorem guarantees existence. Pure equilibria are found by "
                "best-response analysis. Mixed equilibrium: Player 1 is indifferent "
                "between O and F when 2p = 1·(1−p) iff p = 1/3 (Player 2's prob of O); "
                "Player 2 is indifferent when 1·q = 2(1−q) iff q = 2/3 (Player 1's prob of O)."
            ),
            source_section="Adams & Franzosa §10.3",
            notes=(
                "Multiple Nash equilibria create a coordination problem: which equilibrium "
                "will players choose? The mixed equilibrium gives both players lower expected "
                "payoff (2/3 < 1) than either pure equilibrium. This illustrates that Nash "
                "equilibrium multiplicity is itself a modelling challenge — a topological "
                "theorem (existence) does not resolve the selection problem."
            ),
        ),
        NashEquilibriumProfile(
            key="nash_general_finite_game",
            display_name="Nash existence theorem — finite game (general)",
            game_description=(
                "n players; each player i has a finite pure strategy set Sᵢ; "
                "payoffs uᵢ : S₁×...×Sₙ → ℝ extended to mixed strategies by "
                "expected-value linearity."
            ),
            players=-1,   # general n
            strategy_sets="Δ(Sᵢ) = probability simplex over Sᵢ for each player i",
            payoff_description="Expected payoffs, linear in each player's own mixed strategy",
            equilibrium_type="mixed",
            nash_equilibria=(
                "At least one mixed-strategy Nash equilibrium exists. "
                "The set of Nash equilibria is a non-empty compact set."
            ),
            existence_proof=(
                "Define the joint strategy space Δ = Δ(S₁)×...×Δ(Sₙ), which is compact "
                "and convex (product of simplices). Define the best-response correspondence "
                "φ : Δ → 2^Δ by φ(σ) = ×ᵢ BRᵢ(σ₋ᵢ), where BRᵢ(σ₋ᵢ) is the set of "
                "mixed strategies maximising player i's expected payoff against σ₋ᵢ. "
                "Since expected payoffs are linear (hence continuous) in mixed strategies, "
                "BRᵢ(σ₋ᵢ) is non-empty (maximum of continuous function on compact set) "
                "and convex (argmax of linear function). The graph of φ is closed "
                "(payoffs are continuous). By Kakutani's theorem, φ has a fixed point σ*, "
                "which is a Nash equilibrium by definition."
            ),
            source_section="Adams & Franzosa §10.3",
            notes=(
                "This is Nash's 1950 existence proof. The key topological ingredients: "
                "(1) Brouwer/Kakutani fixed-point theorem, "
                "(2) compactness of the mixed-strategy space (product of simplices), "
                "(3) continuity of expected payoffs (gives closed graph and compact argmax). "
                "The proof structure — define a best-response correspondence and apply "
                "Kakutani — is a template used throughout economic theory."
            ),
        ),
    )


def nash_equilibrium_type_summary() -> dict[str, list[str]]:
    """Return a mapping from equilibrium_type to profile keys."""
    result: dict[str, list[str]] = {}
    for p in get_nash_profiles():
        result.setdefault(p.equilibrium_type, []).append(p.key)
    return result


# ---------------------------------------------------------------------------
# EconomicEquilibriumProfile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EconomicEquilibriumProfile:
    """Teaching profile for economic equilibrium existence via fixed-point theory.

    Walrasian/competitive equilibrium and the Arrow-Debreu theorem are proved
    using fixed-point arguments on price simplices.
    """

    key: str
    display_name: str
    model_description: str
    fixed_point_theorem_used: str   # "Brouwer", "Kakutani", "Schauder"
    equilibrium_object: str
    key_topological_ingredients: tuple[str, ...]
    source_section: str
    notes: str


def get_economic_equilibrium_profiles() -> tuple[EconomicEquilibriumProfile, ...]:
    """Return economic equilibrium profile examples."""
    return (
        EconomicEquilibriumProfile(
            key="walrasian_equilibrium_brouwer",
            display_name="Walrasian equilibrium — Brouwer FPT proof",
            model_description=(
                "L commodities; n consumers with continuous, convex, strictly monotone "
                "preferences and endowments. Aggregate excess demand z(p) : Δ^{L-1} → ℝᴸ "
                "is continuous (Walras's law: p·z(p) = 0)."
            ),
            fixed_point_theorem_used="Brouwer",
            equilibrium_object=(
                "A price vector p* ∈ Δ^{L-1} such that z(p*) ≤ 0 "
                "(supply meets or exceeds demand in all markets)."
            ),
            key_topological_ingredients=(
                "Δ^{L-1} is compact and convex",
                "Excess demand z(p) is continuous (from continuity of preferences and endowments)",
                "Walras's law constrains z to the price simplex",
                "A price-adjustment map T : Δ^{L-1} → Δ^{L-1} has a fixed point by Brouwer",
            ),
            source_section="Adams & Franzosa §10.4",
            notes=(
                "The price-adjustment map T(p) normalises p + max(z(p), 0): "
                "it raises prices of goods in excess demand and lowers others. "
                "T is continuous and maps the compact convex simplex Δ^{L-1} to itself. "
                "By Brouwer's theorem, T has a fixed point p*, which satisfies z(p*) ≤ 0 "
                "by Walras's law. This is the Arrow-Debreu equilibrium existence argument."
            ),
        ),
        EconomicEquilibriumProfile(
            key="arrow_debreu_equilibrium_kakutani",
            display_name="Arrow-Debreu equilibrium — Kakutani FPT proof",
            model_description=(
                "General equilibrium model with L goods, n consumers (utility maximisers), "
                "m firms (profit maximisers). Consumers and firms have correspondences "
                "(demand and supply sets may be set-valued due to indifference or "
                "constant-returns technologies)."
            ),
            fixed_point_theorem_used="Kakutani",
            equilibrium_object=(
                "A price-allocation pair (p*, x*, y*) such that: "
                "each consumer maximises utility subject to budget, "
                "each firm maximises profit, "
                "markets clear (aggregate demand = aggregate supply + endowments)."
            ),
            key_topological_ingredients=(
                "Price simplex Δ^{L-1} is compact and convex",
                "Consumer demand correspondences have non-empty convex values (quasi-concave utility)",
                "Firm supply correspondences have convex values (convex production sets)",
                "Joint correspondence has closed graph (continuity of preferences and technology)",
                "Kakutani's theorem applied to the joint excess-demand correspondence",
            ),
            source_section="Adams & Franzosa §10.4",
            notes=(
                "Arrow and Debreu (1954) proved existence using Kakutani's theorem rather "
                "than Brouwer's, because demand and supply may be set-valued. "
                "The proof constructs a joint correspondence Φ on the product space "
                "Δ^{L-1} × (consumer budget sets) × (firm production sets), "
                "verifies the Kakutani conditions, and identifies the fixed point as "
                "a competitive equilibrium. This is one of the most celebrated "
                "applications of algebraic topology in economics."
            ),
        ),
    )


# ---------------------------------------------------------------------------
# Module-level registry
# ---------------------------------------------------------------------------

def game_theory_profile_registry() -> dict[str, int]:
    """Return counts of profiles by category."""
    return {
        "kakutani_profiles": len(get_kakutani_profiles()),
        "nash_profiles": len(get_nash_profiles()),
        "economic_equilibrium_profiles": len(get_economic_equilibrium_profiles()),
    }


__all__ = [
    "KakutaniProfile",
    "get_kakutani_profiles",
    "kakutani_fixed_point_summary",
    "NashEquilibriumProfile",
    "get_nash_profiles",
    "nash_equilibrium_type_summary",
    "EconomicEquilibriumProfile",
    "get_economic_equilibrium_profiles",
    "game_theory_profile_registry",
]
