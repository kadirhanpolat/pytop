"""Named topological spaces — canonical constructors for well-known examples.

Each function returns a TopologicalSpace (or subclass) instance whose tags and
metadata encode the known topological properties of the space.  Functions that
accept parameters (e.g. carrier size, distinguished point) are noted explicitly.

Batch 1 (v0.5.33): 20 classical spaces.
Batch 2 (v0.5.34): 12 additional spaces.
Batch 3 (v0.5.35): 12 additional spaces.
Batch 4 (v0.5.36): 12 additional spaces.
Batch 5 (v0.5.37): 12 additional spaces.
Batch 6 (v0.5.38): 12 additional spaces.
Batch 7 (v0.5.39): 12 additional spaces.
Batch 8 (v0.5.40): 12 additional spaces.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any

from .finite_spaces import FiniteTopologicalSpace
from .infinite_spaces import (
    BasisDefinedSpace,
    CofiniteSpace,
    CocountableSpace,
    MetricLikeSpace,
    SorgenfreyLikeSpace,
)
from .spaces import TopologicalSpace


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _finite(
    carrier: frozenset,
    topology: set[frozenset],
    name: str,
    description: str,
    tags: list[str],
    extra: dict[str, Any] | None = None,
) -> FiniteTopologicalSpace:
    meta: dict[str, Any] = {"name": name, "description": description, "representation": "finite"}
    if extra:
        meta.update(extra)
    space = FiniteTopologicalSpace(carrier=carrier, topology=topology, metadata=meta)
    space.add_tags(*tags)
    return space


def _symbolic(
    name: str,
    description: str,
    tags: list[str],
    representation: str = "symbolic_general",
) -> TopologicalSpace:
    space = TopologicalSpace.symbolic(
        description=description,
        representation=representation,
        tags=tags,
    )
    space.metadata["name"] = name
    return space


# ---------------------------------------------------------------------------
# Finite named spaces
# ---------------------------------------------------------------------------

def sierpinski_space() -> FiniteTopologicalSpace:
    """Sierpiński space: {0, 1} with topology {∅, {1}, {0,1}}.

    The unique (up to homeomorphism) non-trivial two-point T0 space.
    pi-base: S000003.
    """
    carrier = frozenset({0, 1})
    topology = {frozenset(), frozenset({1}), frozenset({0, 1})}
    return _finite(
        carrier, topology,
        name="Sierpiński space",
        description="Two-point space {0,1} with topology {∅,{1},{0,1}}.",
        tags=[
            "t0", "not_t1", "not_hausdorff",
            "compact", "connected", "path_connected", "hyperconnected",
            "sober",
            "second_countable", "first_countable", "separable",
        ],
        extra={"pi_base_id": "S000003"},
    )


def particular_point_topology(n: int, p: int) -> FiniteTopologicalSpace:
    """Particular point topology on {0, …, n-1} with distinguished point p.

    τ = {∅} ∪ {U ⊆ X : p ∈ U}.
    Hyperconnected, T0, not T1.  Parameterized; for the infinite version see
    :func:`particular_point_topology_on_naturals`.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if not (0 <= p < n):
        raise ValueError(f"p must be in 0..n-1, got p={p}")
    carrier = frozenset(range(n))
    topology: set[frozenset] = {frozenset()}
    for size in range(1, n + 1):
        for subset in combinations(range(n), size):
            if p in subset:
                topology.add(frozenset(subset))
    return _finite(
        carrier, topology,
        name=f"Particular point topology ({n} points, p={p})",
        description=f"Topology on {{0,...,{n-1}}} where U is open iff p∈U (or U=∅).",
        tags=[
            "t0", "not_t1", "not_hausdorff",
            "compact", "connected", "hyperconnected",
            "second_countable", "first_countable", "separable",
        ],
        extra={"particular_point": p},
    )


def excluded_point_topology(n: int, p: int) -> FiniteTopologicalSpace:
    """Excluded point topology on {0, …, n-1} with excluded point p.

    τ = {U ⊆ X : p ∉ U} ∪ {X}.
    Connected, T0, not T1.  Parameterized.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if not (0 <= p < n):
        raise ValueError(f"p must be in 0..n-1, got p={p}")
    carrier = frozenset(range(n))
    topology: set[frozenset] = {frozenset(range(n))}
    for size in range(n):
        for subset in combinations(range(n), size):
            if p not in subset:
                topology.add(frozenset(subset))
    return _finite(
        carrier, topology,
        name=f"Excluded point topology ({n} points, p={p})",
        description=f"Topology on {{0,...,{n-1}}} where U is open iff p∉U or U=X.",
        tags=[
            "t0", "not_t1", "not_hausdorff",
            "compact", "connected",
            "second_countable", "first_countable", "separable",
        ],
        extra={"excluded_point": p},
    )


# ---------------------------------------------------------------------------
# Cofinite / cocountable spaces
# ---------------------------------------------------------------------------

def cofinite_topology_on_naturals() -> CofiniteSpace:
    """Cofinite topology on ω = {0, 1, 2, …}: U open iff U=∅ or ω∖U finite."""
    space = CofiniteSpace(
        carrier="omega",
        metadata={
            "name": "Cofinite topology on N",
            "description": "Cofinite topology on the natural numbers.",
            "cardinality": "aleph_0",
        },
    )
    space.add_tags("lindelof")
    return space


def cofinite_topology_on_reals() -> CofiniteSpace:
    """Cofinite topology on R: U open iff U=∅ or R∖U finite."""
    space = CofiniteSpace(
        carrier="R",
        metadata={
            "name": "Cofinite topology on R",
            "description": "Cofinite topology on the real numbers.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags("lindelof")
    return space


def cocountable_topology_on_reals() -> CocountableSpace:
    """Cocountable topology on R: U open iff U=∅ or R∖U countable."""
    return CocountableSpace(
        carrier="R",
        metadata={
            "name": "Cocountable topology on R",
            "description": "Cocountable topology on the real numbers.",
            "cardinality": "uncountable",
        },
    )


# ---------------------------------------------------------------------------
# Classical real-line spaces
# ---------------------------------------------------------------------------

def real_line() -> MetricLikeSpace:
    """Real line R with the standard Euclidean topology (open intervals basis)."""
    space = MetricLikeSpace(
        carrier="R",
        metadata={
            "name": "Real line",
            "description": "R with the metric topology generated by open intervals (a, b).",
            "cardinality": "uncountable",
            "basis": "open_intervals",
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact", "sigma_compact",
        "second_countable", "separable", "lindelof",
        "normal", "completely_normal",
        "metrizable",
        "not_compact",
    )
    return space


def sorgenfrey_line() -> SorgenfreyLikeSpace:
    """Sorgenfrey line: R with lower limit topology, basis {[a, b) : a < b}.

    Lindelöf, separable, first countable, normal, totally disconnected.
    Not second countable, not metrizable, not locally compact.
    pi-base: S000009.
    """
    space = SorgenfreyLikeSpace(
        carrier="R",
        metadata={
            "name": "Sorgenfrey line",
            "description": "R with lower limit topology generated by half-open intervals [a, b).",
            "cardinality": "uncountable",
            "basis": "half_open_intervals",
            "pi_base_id": "S000009",
        },
    )
    space.add_tags(
        "lindelof",
        "normal", "completely_normal",
        "zero_dimensional", "totally_disconnected",
        "not_connected", "not_path_connected", "not_locally_connected",
        "not_compact", "not_locally_compact",
        "not_metrizable", "not_second_countable",
    )
    return space


def rational_numbers() -> MetricLikeSpace:
    """Rational numbers Q with subspace topology from R.

    Metric, separable, second countable, totally disconnected.
    Not locally compact, not complete, not sigma-compact.
    """
    space = MetricLikeSpace(
        carrier="Q",
        metadata={
            "name": "Rational numbers",
            "description": "Q with the subspace topology inherited from R.",
            "cardinality": "aleph_0",
        },
    )
    space.add_tags(
        "second_countable", "separable", "lindelof",
        "metrizable", "normal",
        "zero_dimensional", "totally_disconnected",
        "not_compact", "not_locally_compact",
        "not_connected", "not_path_connected",
    )
    return space


def irrational_numbers() -> MetricLikeSpace:
    """Irrational numbers R∖Q with subspace topology from R.

    Metric, separable, second countable, zero-dimensional, homeomorphic to ω^ω.
    Not locally compact, not sigma-compact.
    """
    space = MetricLikeSpace(
        carrier="irrationals",
        metadata={
            "name": "Irrational numbers",
            "description": "R\\Q with the subspace topology inherited from R.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "second_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_metrizable",
        "zero_dimensional", "totally_disconnected",
        "not_compact", "not_locally_compact", "not_sigma_compact",
        "not_connected", "not_path_connected",
    )
    return space


# ---------------------------------------------------------------------------
# Metric spaces
# ---------------------------------------------------------------------------

def cantor_set() -> MetricLikeSpace:
    """Cantor set: closed nowhere-dense perfect subset of [0, 1].

    Compact, totally disconnected, zero-dimensional.
    Universal compact metrizable zero-dimensional space.
    """
    space = MetricLikeSpace(
        carrier="cantor_set",
        metadata={
            "name": "Cantor set",
            "description": "Standard middle-thirds Cantor set in [0, 1] with subspace topology.",
            "cardinality": "uncountable",
            "ambient": "[0,1]",
        },
    )
    space.add_tags(
        "compact",
        "perfect", "nowhere_dense",
        "zero_dimensional", "totally_disconnected",
        "second_countable", "separable",
        "metrizable", "normal",
        "not_connected", "not_path_connected",
    )
    return space


def hilbert_cube() -> MetricLikeSpace:
    """Hilbert cube [0, 1]^ω: countably infinite product of [0, 1].

    Compact, connected, metrizable.  Universal compact metrizable space.
    """
    space = MetricLikeSpace(
        carrier="[0,1]^omega",
        metadata={
            "name": "Hilbert cube",
            "description": "Countably infinite product of [0, 1] with the product topology.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected", "locally_connected",
        "second_countable", "separable",
        "metrizable", "normal",
    )
    return space


# ---------------------------------------------------------------------------
# Order-topology spaces
# ---------------------------------------------------------------------------

def long_line() -> BasisDefinedSpace:
    """Long line: ω₁ × [0, 1) with lexicographic order topology.

    Connected, locally Euclidean, first countable.
    Not second countable, not metrizable, not paracompact, not Lindelöf.
    """
    space = BasisDefinedSpace(
        carrier="omega_1 x [0,1)",
        metadata={
            "name": "Long line",
            "description": "omega_1 x [0,1) with lexicographic order topology.",
            "cardinality": "uncountable",
            "basis_size": "uncountable",
            "local_base_size": "aleph_0",
        },
    )
    space.add_tags(
        "connected", "locally_connected",
        "path_connected", "locally_path_connected",
        "locally_compact", "locally_metrizable",
        "hausdorff", "t0", "t1", "normal",
        "not_compact", "not_second_countable",
        "not_metrizable", "not_paracompact", "not_lindelof", "not_separable",
    )
    return space


# ---------------------------------------------------------------------------
# Plane topology / counterexample spaces
# ---------------------------------------------------------------------------

def topologists_sine_curve() -> TopologicalSpace:
    """Closed topologist's sine curve: cl({(x, sin(1/x)) : x > 0}) in R².

    Connected but not path-connected, not locally connected.
    Compact, metrizable.
    """
    return _symbolic(
        name="Topologist's sine curve",
        description="Closure of {(x, sin(1/x)) : x > 0} in R².",
        representation="subspace_of_R2",
        tags=[
            "compact", "connected",
            "not_path_connected", "not_locally_connected", "not_locally_path_connected",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
        ],
    )


def comb_space() -> TopologicalSpace:
    """Comb space: [0,1]×{0} ∪ {0}×[0,1] ∪ ({1/n : n≥1}×[0,1]).

    Connected, compact, not locally connected at (0, y) for y > 0.
    """
    return _symbolic(
        name="Comb space",
        description="Horizontal base, vertical spine, and teeth at 1/n in R².",
        representation="subspace_of_R2",
        tags=[
            "compact", "connected",
            "not_locally_connected", "not_path_connected",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
        ],
    )


def warsaw_circle() -> TopologicalSpace:
    """Warsaw circle: closed topologist's sine curve joined by an arc.

    Compact, connected, not locally connected.
    """
    return _symbolic(
        name="Warsaw circle",
        description="Closed topologist's sine curve joined by an arc, forming a loop.",
        representation="subspace_of_R2",
        tags=[
            "compact", "connected",
            "not_locally_connected", "not_locally_path_connected",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
        ],
    )


def infinite_broom() -> TopologicalSpace:
    """Infinite broom: segments from origin to (1, 1/n) for n ≥ 1, plus segment to (1, 0).

    Connected, path-connected from interior, not locally connected at (0, 0).
    """
    return _symbolic(
        name="Infinite broom",
        description="Union of segments from (0,0) to (1, 1/n) for n≥1 and to (1, 0).",
        representation="subspace_of_R2",
        tags=[
            "compact", "connected", "path_connected",
            "not_locally_connected",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
        ],
    )


# ---------------------------------------------------------------------------
# Special topology spaces (basis-defined)
# ---------------------------------------------------------------------------

def moore_plane() -> BasisDefinedSpace:
    """Moore plane (Niemytzki plane): upper half-plane with tangent-disk basis.

    Hausdorff, separable, first countable, regular.
    Not normal, not second countable, not Lindelöf, not metrizable.
    pi-base: S000008.
    """
    space = BasisDefinedSpace(
        carrier="R x [0,inf)",
        metadata={
            "name": "Moore plane",
            "description": "Upper half-plane with tangent-disk neighborhoods at x-axis points.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
            "pi_base_id": "S000008",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "first_countable", "separable",
        "regular", "completely_hausdorff",
        "not_normal", "not_second_countable", "not_lindelof",
        "not_metrizable", "not_compact", "not_paracompact",
    )
    return space


def arens_fort_space() -> BasisDefinedSpace:
    """Arens-Fort space: N×N where only (0,0) is non-isolated.

    (0,0) neighborhoods must be cofinite in each column.
    Hausdorff, separable, zero-dimensional.
    Not first countable, not sequential, not compact.
    pi-base: S000007.
    """
    space = BasisDefinedSpace(
        carrier="N x N",
        metadata={
            "name": "Arens-Fort space",
            "description": "N×N; all points isolated except (0,0) whose neighborhoods are cofinite per column.",
            "cardinality": "aleph_0",
            "local_base_size": "uncountable",
            "basis_size": "uncountable",
            "pi_base_id": "S000007",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "regular", "normal",
        "separable", "zero_dimensional",
        "not_first_countable", "not_second_countable",
        "not_compact", "not_locally_compact",
        "not_sequential",
    )
    return space


def fort_space() -> BasisDefinedSpace:
    """Fort space: N ∪ {∞} — one-point compactification of discrete N.

    Hausdorff, compact, second countable, metrizable.
    Homeomorphic to {0} ∪ {1/n : n ≥ 1} ⊆ R.
    """
    space = BasisDefinedSpace(
        carrier="N union {inf}",
        metadata={
            "name": "Fort space",
            "description": "One-point compactification of discrete N; isolated points plus one accumulation point.",
            "cardinality": "aleph_0",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "compact",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
        "zero_dimensional", "totally_disconnected",
        "not_connected",
    )
    return space


# ---------------------------------------------------------------------------
# Batch 2 — finite discrete / indiscrete, real-line variants, plank spaces,
#            βN, number-theoretic topologies, and pathological continua
# ---------------------------------------------------------------------------

def discrete_space(n: int) -> FiniteTopologicalSpace:
    """Discrete topology on {0, …, n-1}: every subset is open.

    For n=1 the space is trivially discrete and connected.
    For n≥2: totally disconnected, Hausdorff, zero-dimensional.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    carrier = frozenset(range(n))
    topology = {frozenset(S) for k in range(n + 1) for S in combinations(range(n), k)}
    tags = [
        "discrete", "hausdorff", "t0", "t1",
        "metrizable", "normal",
        "second_countable", "first_countable", "separable",
        "compact",
    ]
    if n >= 2:
        tags += ["zero_dimensional", "totally_disconnected", "not_connected", "not_path_connected"]
    else:
        tags += ["connected", "path_connected"]
    return _finite(
        carrier, topology,
        name=f"Discrete space ({n} points)",
        description=f"Discrete topology on {{{', '.join(str(k) for k in range(min(n, 4)))}{',...' if n>4 else ''}}}.",
        tags=tags,
    )


def indiscrete_space(n: int) -> FiniteTopologicalSpace:
    """Indiscrete topology on {0, …, n-1}: only ∅ and X are open.

    For n=1 trivially everything. For n≥2: not T0, hyperconnected.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    carrier = frozenset(range(n))
    topology = {frozenset(), carrier}
    tags = ["compact", "connected", "path_connected", "hyperconnected",
            "second_countable", "first_countable", "separable"]
    if n >= 2:
        tags += ["not_t0", "not_t1", "not_hausdorff", "not_metrizable"]
    else:
        tags += ["t0", "t1", "hausdorff", "metrizable", "zero_dimensional"]
    return _finite(
        carrier, topology,
        name=f"Indiscrete space ({n} points)",
        description=f"Indiscrete topology on {n} points.",
        tags=tags,
    )


def discrete_countable_space() -> MetricLikeSpace:
    """Countably infinite discrete space ℕ.

    Metrizable, locally compact, zero-dimensional, not compact.
    """
    space = MetricLikeSpace(
        carrier="N",
        metadata={
            "name": "Discrete countable space",
            "description": "Natural numbers N with the discrete topology.",
            "cardinality": "aleph_0",
        },
    )
    space.add_tags(
        "second_countable", "separable", "lindelof",
        "zero_dimensional", "totally_disconnected",
        "locally_compact", "metrizable",
        "not_compact", "not_connected", "not_path_connected",
    )
    return space


def particular_point_topology_on_naturals() -> BasisDefinedSpace:
    """Particular point topology on ℕ with distinguished point 0.

    τ = {∅} ∪ {U ⊆ ℕ : 0 ∈ U}.
    Hyperconnected, T0, not T1.  Infinite version of :func:`particular_point_topology`.
    """
    space = BasisDefinedSpace(
        carrier="N",
        metadata={
            "name": "Particular point topology on N",
            "description": "Topology on N where U is open iff 0∈U (or U=∅).",
            "cardinality": "aleph_0",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
            "particular_point": 0,
        },
    )
    space.add_tags(
        "t0", "not_t1", "not_hausdorff",
        "connected", "hyperconnected",
        "not_compact",
        "second_countable", "first_countable", "separable",
    )
    return space


def excluded_point_topology_on_naturals() -> BasisDefinedSpace:
    """Excluded point topology on ℕ with excluded point 0.

    τ = {U ⊆ ℕ : 0 ∉ U} ∪ {ℕ}.
    Connected, T0, not T1.  Infinite version of :func:`excluded_point_topology`.
    """
    space = BasisDefinedSpace(
        carrier="N",
        metadata={
            "name": "Excluded point topology on N",
            "description": "Topology on N where U is open iff 0∉U or U=N.",
            "cardinality": "aleph_0",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
            "excluded_point": 0,
        },
    )
    space.add_tags(
        "t0", "not_t1", "not_hausdorff",
        "connected",
        "not_compact",
        "second_countable", "first_countable", "separable",
    )
    return space


def double_origin_topology() -> BasisDefinedSpace:
    """Double origin topology: ℝ with two copies of 0, denoted 0 and 0'.

    Neighborhoods of 0 (resp. 0') exclude 0' (resp. 0); all other points
    are standard.  Hausdorff but not regular.
    pi-base: S000010.
    """
    space = BasisDefinedSpace(
        carrier="R union {0'}",
        metadata={
            "name": "Double origin topology",
            "description": "Real line with a second copy of 0; neighborhoods of each origin exclude the other.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
            "pi_base_id": "S000010",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "second_countable", "first_countable", "separable",
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact",
        "not_regular", "not_normal",
        "not_compact", "not_metrizable",
    )
    return space


def michael_line() -> BasisDefinedSpace:
    """Michael line: ℝ with irrationals isolated (singleton open sets).

    Open sets: U ∪ S where U is standard-open in ℝ and S ⊆ ℝ\\ℚ.
    Normal, first countable, not Lindelöf, not separable.
    """
    space = BasisDefinedSpace(
        carrier="R",
        metadata={
            "name": "Michael line",
            "description": "R with irrationals as isolated points; rationals retain standard topology.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "regular", "normal",
        "first_countable",
        "not_second_countable", "not_separable", "not_lindelof",
        "not_locally_compact",
        "not_compact",
    )
    return space


def tychonoff_plank() -> BasisDefinedSpace:
    """Tychonoff plank: (ω₁+1)×(ω+1) with the product order topology.

    Compact, Hausdorff, normal (compact Hausdorff ⇒ normal).
    Not first countable at the corner (ω₁, ω), not separable.
    """
    space = BasisDefinedSpace(
        carrier="(omega_1+1) x (omega+1)",
        metadata={
            "name": "Tychonoff plank",
            "description": "(omega_1+1) x (omega+1) with the product of order topologies.",
            "cardinality": "uncountable",
            "local_base_size": "uncountable",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "compact", "hausdorff", "t0", "t1",
        "normal",
        "connected",
        "not_first_countable", "not_second_countable", "not_separable",
        "not_metrizable",
    )
    return space


def deleted_tychonoff_plank() -> BasisDefinedSpace:
    """Deleted Tychonoff plank: Tychonoff plank minus the corner point (ω₁, ω).

    Classic example of a Hausdorff space that is NOT normal:
    the sets {ω₁}×ω and ω₁×{ω} are disjoint closed sets with no separating open sets.
    """
    space = BasisDefinedSpace(
        carrier="(omega_1+1) x (omega+1) \\ {(omega_1, omega)}",
        metadata={
            "name": "Deleted Tychonoff plank",
            "description": "Tychonoff plank minus the corner point (omega_1, omega).",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "not_normal", "not_compact",
        "not_second_countable", "not_separable",
        "not_metrizable",
    )
    return space


def stone_cech_compactification_of_N() -> TopologicalSpace:
    """Stone-Čech compactification βN of the discrete space ℕ.

    Compact, Hausdorff, extremally disconnected, separable (ℕ dense), zero-dimensional.
    Not metrizable, not first countable at points of βN\\N.
    """
    return _symbolic(
        name="Stone-Čech compactification of N",
        description="The Stone-Cech compactification beta_N of the discrete space N.",
        representation="symbolic_compactification",
        tags=[
            "compact", "hausdorff", "t0", "t1",
            "normal", "extremally_disconnected",
            "zero_dimensional", "totally_disconnected",
            "separable",
            "not_first_countable", "not_second_countable",
            "not_metrizable", "not_connected", "not_path_connected",
        ],
    )


def furstenberg_topology() -> BasisDefinedSpace:
    """Furstenberg topology on ℤ: basis of arithmetic progressions {a + bℤ : b ≥ 1}.

    Every arithmetic progression is clopen.  Used in Furstenberg's topological
    proof that there are infinitely many primes.
    Hausdorff, metrizable, zero-dimensional, not compact.
    """
    space = BasisDefinedSpace(
        carrier="Z",
        metadata={
            "name": "Furstenberg topology",
            "description": "Z with basis {a + bZ : b >= 1}; arithmetic progressions are clopen.",
            "cardinality": "aleph_0",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "regular", "normal",
        "metrizable",
        "zero_dimensional", "totally_disconnected",
        "second_countable", "first_countable", "separable", "lindelof",
        "not_compact", "not_connected", "not_path_connected",
    )
    return space


def pseudo_arc() -> TopologicalSpace:
    """Pseudo-arc: hereditarily indecomposable chainable continuum.

    Compact, connected, metrizable.  Homogeneous among continua.
    Not locally connected, not path-connected.
    """
    return _symbolic(
        name="Pseudo-arc",
        description="Hereditarily indecomposable chainable compact connected metrizable space.",
        representation="symbolic_continuum",
        tags=[
            "compact", "connected",
            "not_locally_connected", "not_path_connected", "not_locally_path_connected",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "homogeneous",
        ],
    )


# ---------------------------------------------------------------------------
# Batch 3 — standard geometric spaces, function spaces, ordered squares,
#            Cantor-based spaces, and p-adic integers
# ---------------------------------------------------------------------------

def unit_interval() -> MetricLikeSpace:
    """Closed unit interval [0, 1] with subspace topology from ℝ.

    The standard compact connected metric space; universal separable metrizable
    compact space (Hahn-Mazurkiewicz theorem).
    """
    space = MetricLikeSpace(
        carrier="[0,1]",
        metadata={
            "name": "Unit interval",
            "description": "Closed unit interval [0,1] with subspace topology from R.",
            "cardinality": "uncountable",
            "ambient": "R",
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected",
        "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
        "simply_connected",
    )
    return space


def unit_circle() -> MetricLikeSpace:
    """Unit circle S¹ = {(x,y) ∈ ℝ² : x² + y² = 1}.

    Compact, connected, path-connected, locally Euclidean (1-manifold).
    """
    space = MetricLikeSpace(
        carrier="S^1",
        metadata={
            "name": "Unit circle",
            "description": "S^1 = {(x,y) in R^2 : x^2 + y^2 = 1} with subspace topology.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 1,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
    )
    return space


def closed_unit_disk() -> MetricLikeSpace:
    """Closed unit disk D² = {(x,y) ∈ ℝ² : x² + y² ≤ 1}.

    Compact, contractible, simply connected.
    """
    space = MetricLikeSpace(
        carrier="D^2",
        metadata={
            "name": "Closed unit disk",
            "description": "D^2 = {(x,y) in R^2 : x^2+y^2 <= 1} with subspace topology.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 2,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
        "simply_connected", "contractible",
    )
    return space


def torus() -> MetricLikeSpace:
    """Torus T² = S¹ × S¹ with the product topology.

    Compact, connected, path-connected.  Fundamental group ℤ × ℤ.
    """
    space = MetricLikeSpace(
        carrier="T^2",
        metadata={
            "name": "Torus",
            "description": "T^2 = S^1 x S^1 with the product topology.",
            "cardinality": "uncountable",
            "dimension": 2,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
    )
    return space


def cantor_cube() -> MetricLikeSpace:
    """Cantor cube {0, 1}^ω: countable product of the discrete two-point space.

    Compact, Hausdorff, zero-dimensional.  Homeomorphic to the Cantor set.
    Universal compact metrizable zero-dimensional perfect space.
    """
    space = MetricLikeSpace(
        carrier="{0,1}^omega",
        metadata={
            "name": "Cantor cube",
            "description": "Countably infinite product of the discrete two-point space {0,1}.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "compact", "perfect",
        "zero_dimensional", "totally_disconnected",
        "not_connected", "not_path_connected",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
    )
    return space


def baire_space() -> MetricLikeSpace:
    """Baire space ω^ω: countable product of the discrete space ℕ.

    Completely metrizable, zero-dimensional.  Homeomorphic to the irrationals.
    Not locally compact, not sigma-compact.
    """
    space = MetricLikeSpace(
        carrier="N^omega",
        metadata={
            "name": "Baire space",
            "description": "Countably infinite product of the discrete space N; homeomorphic to the irrationals.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "completely_metrizable",
        "zero_dimensional", "totally_disconnected",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact", "not_locally_compact", "not_sigma_compact",
        "not_connected", "not_path_connected",
    )
    return space


def lexicographic_square() -> BasisDefinedSpace:
    """Lexicographic square: [0, 1]² with the lexicographic order topology.

    Compact, connected (ordered continuum), first countable.
    Not separable (uncountably many disjoint open sets), not metrizable.
    """
    space = BasisDefinedSpace(
        carrier="[0,1]^2 lex",
        metadata={
            "name": "Lexicographic square",
            "description": "[0,1]^2 with lexicographic order topology.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "normal",
        "compact", "connected",
        "first_countable",
        "not_separable", "not_second_countable",
        "not_metrizable",
    )
    return space


def one_point_compactification_of_reals() -> MetricLikeSpace:
    """One-point compactification ℝ ∪ {∞}: the real projective circle.

    Compact, connected, metrizable (homeomorphic to S¹).
    """
    space = MetricLikeSpace(
        carrier="R union {inf}",
        metadata={
            "name": "One-point compactification of R",
            "description": "R union {inf} with the one-point compactification topology; homeomorphic to S^1.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
    )
    return space


def cantor_fan() -> TopologicalSpace:
    """Cantor fan: cone over the Cantor set — (C × [0, 1]) / (C × {0}).

    Compact, path-connected, not locally connected at non-apex points.
    """
    return _symbolic(
        name="Cantor fan",
        description="Cone over the Cantor set; quotient of C x [0,1] collapsing C x {0} to the apex.",
        representation="symbolic_continuum",
        tags=[
            "compact", "connected", "path_connected",
            "not_locally_connected", "not_locally_path_connected",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
        ],
    )


def knaster_kuratowski_fan() -> TopologicalSpace:
    """Knaster-Kuratowski fan (Cantor's teepee): connected space that becomes
    totally disconnected when the apex is removed.

    Connected, not locally connected, not compact, metrizable (subspace of ℝ²).
    """
    return _symbolic(
        name="Knaster-Kuratowski fan",
        description="Cantor-based fan in R^2; connected with apex, totally disconnected without it.",
        representation="subspace_of_R2",
        tags=[
            "connected",
            "not_locally_connected", "not_path_connected",
            "not_compact",
            "second_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
        ],
    )


def hilbert_space() -> MetricLikeSpace:
    """Separable Hilbert space ℓ²: square-summable real sequences with ℓ² norm.

    Completely metrizable, separable, connected.
    Not locally compact (closed unit ball not compact).
    """
    space = MetricLikeSpace(
        carrier="ell_2",
        metadata={
            "name": "Hilbert space",
            "description": "Separable Hilbert space l^2 of square-summable sequences with the norm topology.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "completely_metrizable",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "not_compact", "not_locally_compact",
    )
    return space


def p_adic_integers() -> MetricLikeSpace:
    """p-adic integers ℤ_p with the p-adic topology.

    Compact, zero-dimensional, metrizable.  Homeomorphic to the Cantor set.
    """
    space = MetricLikeSpace(
        carrier="Z_p",
        metadata={
            "name": "p-adic integers",
            "description": "p-adic integers Z_p with the p-adic metric topology.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "compact", "perfect",
        "zero_dimensional", "totally_disconnected",
        "not_connected", "not_path_connected",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal", "completely_metrizable",
    )
    return space


# ---------------------------------------------------------------------------
# Batch 4 — subsets of ℝ, compact surfaces, ordinal spaces,
#            Stone-Čech remainder, and pathological constructions
# ---------------------------------------------------------------------------

def half_open_interval() -> MetricLikeSpace:
    """Half-open interval [0, 1) with subspace topology from ℝ.

    Connected, locally compact, not compact.
    Homeomorphic to [0, ∞) and to ℝ × {0} in a product.
    """
    space = MetricLikeSpace(
        carrier="[0,1)",
        metadata={
            "name": "Half-open interval",
            "description": "Half-open interval [0,1) with subspace topology from R.",
            "cardinality": "uncountable",
            "ambient": "R",
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact",
    )
    return space


def open_interval() -> MetricLikeSpace:
    """Open unit interval (0, 1) with subspace topology from ℝ.

    Homeomorphic to ℝ.  Connected, locally compact, not compact.
    """
    space = MetricLikeSpace(
        carrier="(0,1)",
        metadata={
            "name": "Open interval",
            "description": "Open unit interval (0,1) with subspace topology from R; homeomorphic to R.",
            "cardinality": "uncountable",
            "ambient": "R",
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact",
    )
    return space


def half_open_real_line() -> MetricLikeSpace:
    """Half-open real line [0, ∞) with subspace topology from ℝ.

    Connected, locally compact, contractible, not compact.
    """
    space = MetricLikeSpace(
        carrier="[0,inf)",
        metadata={
            "name": "Half-open real line",
            "description": "Half-open ray [0, inf) with subspace topology from R.",
            "cardinality": "uncountable",
            "ambient": "R",
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact", "simply_connected", "contractible",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact",
    )
    return space


def real_projective_plane() -> TopologicalSpace:
    """Real projective plane RP²: S² with antipodal points identified.

    Compact, connected, non-orientable 2-manifold.
    π₁(RP²) = ℤ/2ℤ.  Not simply connected.
    """
    return _symbolic(
        name="Real projective plane",
        description="RP^2 = S^2 / (x ~ -x); quotient of S^2 by antipodal map.",
        representation="symbolic_manifold",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected", "locally_compact",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected",
        ],
    )


def klein_bottle() -> TopologicalSpace:
    """Klein bottle K: compact non-orientable surface without boundary.

    π₁(K) = ⟨a, b | abab⁻¹ = 1⟩.  Not embeddable in ℝ³.
    """
    return _symbolic(
        name="Klein bottle",
        description="Compact non-orientable surface; quotient of [0,1]^2 with one pair of edges reversed.",
        representation="symbolic_manifold",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected", "locally_compact",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected",
        ],
    )


def mobius_band() -> TopologicalSpace:
    """Möbius band: compact non-orientable surface with boundary.

    Boundary is a single circle.  Retracts onto its core circle S¹.
    """
    return _symbolic(
        name="Möbius band",
        description="[0,1] x [0,1] with (0,t) ~ (1, 1-t); compact non-orientable with boundary.",
        representation="symbolic_manifold",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected", "locally_compact",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected",
        ],
    )


def dunce_hat() -> TopologicalSpace:
    """Dunce hat: quotient of a triangle by identifying boundary edges a·a·a⁻¹.

    Contractible but not locally contractible at the singular vertex.
    """
    return _symbolic(
        name="Dunce hat",
        description="Quotient of a disk by boundary identification; contractible, not locally contractible.",
        representation="symbolic_cw_complex",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected",
            "simply_connected", "contractible",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_locally_contractible",
        ],
    )


def hawaiian_earring() -> TopologicalSpace:
    """Hawaiian earring: countably infinite bouquet of circles of radii 1/n.

    Compact, path-connected, not semi-locally simply connected at the origin.
    """
    return _symbolic(
        name="Hawaiian earring",
        description="Union of circles of radius 1/n (n >= 1) tangent to the origin in R^2.",
        representation="subspace_of_R2",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected", "not_semi_locally_simply_connected",
        ],
    )


def omega_1() -> BasisDefinedSpace:
    """First uncountable ordinal space [0, ω₁) with the order topology.

    Connected, locally compact, first countable, normal.
    Not compact, not separable, not second countable.
    """
    space = BasisDefinedSpace(
        carrier="[0, omega_1)",
        metadata={
            "name": "omega_1",
            "description": "First uncountable ordinal [0, omega_1) with the order topology.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "regular", "normal",
        "connected", "locally_compact",
        "first_countable",
        "not_compact", "not_second_countable", "not_separable", "not_lindelof",
        "not_metrizable",
    )
    return space


def omega_1_plus_1() -> BasisDefinedSpace:
    """Extended ordinal space [0, ω₁] = ω₁ + 1 with the order topology.

    Compact, connected, normal (compact Hausdorff).
    Not first countable at ω₁ (uncountable cofinality).
    """
    space = BasisDefinedSpace(
        carrier="[0, omega_1]",
        metadata={
            "name": "omega_1 + 1",
            "description": "Successor ordinal space [0, omega_1] with the order topology.",
            "cardinality": "uncountable",
            "local_base_size": "uncountable",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "normal",
        "compact", "connected",
        "not_first_countable", "not_second_countable", "not_separable",
        "not_metrizable",
    )
    return space


def stone_cech_remainder() -> TopologicalSpace:
    """Stone-Čech remainder N* = βN \\ N.

    Compact, Hausdorff, normal, zero-dimensional.
    Not separable, not metrizable, not first countable.
    """
    return _symbolic(
        name="Stone-Čech remainder",
        description="Stone-Cech remainder beta_N \\ N; the 'remainder' of the compactification.",
        representation="symbolic_compactification",
        tags=[
            "compact", "hausdorff", "t0", "t1",
            "normal",
            "zero_dimensional", "totally_disconnected",
            "not_separable", "not_first_countable", "not_second_countable",
            "not_metrizable", "not_connected",
            "extremally_disconnected",
        ],
    )


def one_point_compactification_of_Q() -> BasisDefinedSpace:
    """One-point compactification ℚ ∪ {∞} of the rational numbers.

    Compact, T1, connected.
    NOT Hausdorff (ℚ is not locally compact, so the compactification fails Hausdorff).
    """
    space = BasisDefinedSpace(
        carrier="Q union {inf}",
        metadata={
            "name": "One-point compactification of Q",
            "description": "One-point compactification of Q; compact and T1 but not Hausdorff.",
            "cardinality": "aleph_0",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
        },
    )
    space.add_tags(
        "t0", "t1", "not_hausdorff",
        "compact", "connected",
        "not_metrizable", "not_regular",
        "separable", "second_countable", "first_countable",
    )
    return space


# ---------------------------------------------------------------------------
# Batch 5 — Euclidean subsets, spheres (parameterized), fractal continua,
#            products, Erdős spaces, and the open sine curve
# ---------------------------------------------------------------------------

def real_plane() -> MetricLikeSpace:
    """Real plane ℝ² with the standard Euclidean topology.

    Connected, simply connected, locally compact, not compact.
    """
    space = MetricLikeSpace(
        carrier="R^2",
        metadata={
            "name": "Real plane",
            "description": "R^2 with the standard Euclidean topology.",
            "cardinality": "uncountable",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact", "simply_connected",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
        "not_compact",
    )
    return space


def punctured_plane() -> MetricLikeSpace:
    """Punctured plane ℝ² \\ {0}: plane with the origin removed.

    Connected, not simply connected (π₁ = ℤ).  Homotopy equivalent to S¹.
    """
    space = MetricLikeSpace(
        carrier="R^2 \\ {0}",
        metadata={
            "name": "Punctured plane",
            "description": "R^2 minus the origin; homotopy equivalent to S^1.",
            "cardinality": "uncountable",
            "ambient": "R^2",
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact", "not_simply_connected",
    )
    return space


def two_sphere() -> MetricLikeSpace:
    """2-sphere S² = {x ∈ ℝ³ : |x| = 1}.

    Compact, simply connected (π₁(S²) = 0, π₂(S²) = ℤ).
    """
    space = MetricLikeSpace(
        carrier="S^2",
        metadata={
            "name": "2-sphere",
            "description": "S^2 = {x in R^3 : |x| = 1} with subspace topology.",
            "cardinality": "uncountable",
            "ambient": "R^3",
            "dimension": 2,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "simply_connected",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
    )
    return space


def three_sphere() -> MetricLikeSpace:
    """3-sphere S³ = {x ∈ ℝ⁴ : |x| = 1}.

    Compact, simply connected (π₁(S³) = 0).  Carries a Lie group structure.
    """
    space = MetricLikeSpace(
        carrier="S^3",
        metadata={
            "name": "3-sphere",
            "description": "S^3 = {x in R^4 : |x| = 1} with subspace topology.",
            "cardinality": "uncountable",
            "ambient": "R^4",
            "dimension": 3,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "simply_connected",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
    )
    return space


def n_sphere(n: int) -> TopologicalSpace:
    """n-sphere S^n = {x ∈ ℝ^(n+1) : |x| = 1}.

    Compact, connected (n≥1), path-connected (n≥1).
    Simply connected for n≥2; π₁(S¹) = ℤ.
    For n=0: discrete two-point space.
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    tags = [
        "compact",
        "second_countable", "first_countable", "separable",
        "metrizable", "hausdorff", "t0", "t1", "normal",
        "locally_compact",
    ]
    if n == 0:
        tags += ["not_connected", "totally_disconnected", "zero_dimensional"]
    elif n == 1:
        tags += ["connected", "path_connected", "locally_connected",
                 "locally_path_connected", "not_simply_connected"]
    else:
        tags += ["connected", "path_connected", "locally_connected",
                 "locally_path_connected", "simply_connected"]
    space = TopologicalSpace.symbolic(
        description=f"S^{n} = {{x in R^{n+1} : |x| = 1}} with subspace topology.",
        representation="symbolic_manifold",
        tags=tags,
    )
    space.metadata["name"] = f"{n}-sphere"
    space.metadata["n"] = n
    space.metadata["dimension"] = n
    return space


def sierpinski_carpet() -> MetricLikeSpace:
    """Sierpiński carpet: fractal subset of [0, 1]² obtained by repeatedly
    removing open middle thirds.

    Compact, connected, locally connected, metrizable.
    Universal compact planar 1-dimensional continuum.
    """
    space = MetricLikeSpace(
        carrier="sierpinski_carpet",
        metadata={
            "name": "Sierpinski carpet",
            "description": "Fractal subset of [0,1]^2; universal compact planar locally connected continuum.",
            "cardinality": "uncountable",
            "ambient": "[0,1]^2",
        },
    )
    space.add_tags(
        "compact", "connected", "locally_connected",
        "path_connected", "locally_path_connected",
        "nowhere_dense",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
        "not_simply_connected",
    )
    return space


def menger_curve() -> MetricLikeSpace:
    """Menger curve (Menger sponge boundary): compact 1-dimensional universal curve.

    Every compact metrizable 1-dimensional locally connected space embeds in the
    Menger curve.  Compact, locally connected, path-connected.
    """
    space = MetricLikeSpace(
        carrier="menger_curve",
        metadata={
            "name": "Menger curve",
            "description": "Universal compact metrizable 1-dimensional locally connected continuum.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "compact", "connected", "locally_connected",
        "path_connected", "locally_path_connected",
        "nowhere_dense",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
        "not_simply_connected",
    )
    return space


def open_cylinder() -> MetricLikeSpace:
    """Open cylinder ℝ × S¹.

    Connected, not simply connected (π₁ = ℤ), not compact.
    Locally compact, locally Euclidean (2-manifold without boundary).
    """
    space = MetricLikeSpace(
        carrier="R x S^1",
        metadata={
            "name": "Open cylinder",
            "description": "R x S^1 with the product topology.",
            "cardinality": "uncountable",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact", "not_simply_connected",
    )
    return space


def tube() -> MetricLikeSpace:
    """Tube (closed cylinder) S¹ × [0, 1].

    Compact, connected, not simply connected (π₁ = ℤ).
    """
    space = MetricLikeSpace(
        carrier="S^1 x [0,1]",
        metadata={
            "name": "Tube",
            "description": "Closed cylinder S^1 x [0,1] with product topology.",
            "cardinality": "uncountable",
            "dimension": 2,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
        "not_simply_connected",
    )
    return space


def open_topologists_sine_curve() -> MetricLikeSpace:
    """Open topologist's sine curve: {(x, sin(1/x)) : x > 0}.

    The graph of sin(1/x) on (0,∞).  Homeomorphic to ℝ (hence simply connected,
    path-connected).  Contrast with its closure (:func:`topologists_sine_curve`).
    """
    space = MetricLikeSpace(
        carrier="{(x,sin(1/x)) : x>0}",
        metadata={
            "name": "Open topologist's sine curve",
            "description": "Graph of sin(1/x) for x > 0; homeomorphic to R.",
            "cardinality": "uncountable",
            "ambient": "R^2",
        },
    )
    space.add_tags(
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "locally_compact", "simply_connected",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact",
    )
    return space


def erdos_space() -> TopologicalSpace:
    """Erdős space ℰ = {x ∈ ℓ² : x_n ∈ ℚ for all n}.

    Totally disconnected but NOT zero-dimensional (dim ℰ = 1).
    Metrizable, separable, not locally compact.
    """
    return _symbolic(
        name="Erdős space",
        description="Subspace of l^2 with rational coordinates; totally disconnected, dim = 1.",
        representation="symbolic_function_space",
        tags=[
            "hausdorff", "t0", "t1",
            "metrizable", "normal",
            "separable", "first_countable", "second_countable", "lindelof",
            "totally_disconnected",
            "not_zero_dimensional", "not_locally_compact", "not_compact",
            "not_connected",
        ],
    )


def complete_erdos_space() -> TopologicalSpace:
    """Complete Erdős space ℰ_c = {x ∈ ℓ² : x_n ∈ ℝ\\ℚ for all n}.

    Completely metrizable, totally disconnected, not zero-dimensional (dim = 1).
    """
    return _symbolic(
        name="Complete Erdős space",
        description="Subspace of l^2 with irrational coordinates; completely metrizable, dim = 1.",
        representation="symbolic_function_space",
        tags=[
            "hausdorff", "t0", "t1",
            "metrizable", "completely_metrizable", "normal",
            "separable", "first_countable", "second_countable", "lindelof",
            "totally_disconnected",
            "not_zero_dimensional", "not_locally_compact", "not_compact",
            "not_connected",
        ],
    )


# ---------------------------------------------------------------------------
# Batch 6 — parameterized Euclidean spaces, product counterexamples,
#            order topologies, combinatorial topologies, geometric shapes
# ---------------------------------------------------------------------------

def real_n_space(n: int) -> TopologicalSpace:
    """Euclidean n-space ℝ^n with the standard topology.

    Simply connected, locally compact, not compact.
    For n=1 homeomorphic to :func:`real_line`.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    space = TopologicalSpace.symbolic(
        description=f"R^{n} with the standard Euclidean topology.",
        representation="symbolic_general",
        tags=[
            "connected", "path_connected", "locally_connected", "locally_path_connected",
            "locally_compact", "simply_connected",
            "second_countable", "first_countable", "separable", "lindelof",
            "metrizable", "normal", "completely_normal",
            "not_compact",
        ],
    )
    space.metadata["name"] = f"R^{n}"
    space.metadata["n"] = n
    space.metadata["cardinality"] = "uncountable"
    space.metadata["dimension"] = n
    return space


def sorgenfrey_plane() -> BasisDefinedSpace:
    """Sorgenfrey plane S_ℓ × S_ℓ: product of two Sorgenfrey lines.

    Separable (ℚ×ℚ is dense), Hausdorff, regular, NOT normal (Jones's lemma).
    The anti-diagonal {(x, −x) : x ∈ ℝ} is a closed discrete uncountable subspace.
    """
    space = BasisDefinedSpace(
        carrier="R x R (sorgenfrey)",
        metadata={
            "name": "Sorgenfrey plane",
            "description": "S_l x S_l; product of two Sorgenfrey lines. Separable Hausdorff but not normal.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "regular",
        "not_normal", "not_metrizable",
        "separable",
        "first_countable",
        "not_second_countable",
        "not_compact", "not_lindelof",
    )
    return space


def one_point_compactification_of_N() -> MetricLikeSpace:
    """One-point compactification of ℕ: the convergent sequence space.

    Realized as {0} ∪ {1/n : n ≥ 1} ⊂ ℝ.  Homeomorphic to ω+1.
    Compact, metrizable, second countable, totally disconnected.
    """
    space = MetricLikeSpace(
        carrier="{0} union {1/n : n>=1}",
        metadata={
            "name": "One-point compactification of N",
            "description": "Convergent sequence space {1/n : n>=1} union {0}; homeomorphic to omega+1.",
            "cardinality": "aleph_0",
        },
    )
    space.add_tags(
        "compact", "locally_compact",
        "metrizable", "normal", "completely_metrizable",
        "second_countable", "first_countable", "separable",
        "zero_dimensional", "totally_disconnected",
        "not_connected", "not_path_connected",
    )
    return space


def omega_plus_1() -> BasisDefinedSpace:
    """Ordinal space ω+1 = {0, 1, 2, ..., ω} with the order topology.

    Finite ordinals are isolated; ω is the unique accumulation point.
    Compact, metrizable (homeomorphic to {0}∪{1/n : n≥1}).
    """
    space = BasisDefinedSpace(
        carrier="{0,1,...,omega}",
        metadata={
            "name": "omega+1",
            "description": "Successor ordinal {0,1,...,omega} with the order topology.",
            "cardinality": "aleph_0",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "normal",
        "compact",
        "first_countable", "second_countable", "separable",
        "zero_dimensional", "totally_disconnected",
        "metrizable",
        "not_connected", "not_path_connected",
    )
    return space


def rational_sequence_topology() -> BasisDefinedSpace:
    """Rational sequence topology on ℝ.

    Each irrational x has a fixed rational sequence converging to it; neighborhoods
    of x are sets containing x and a tail of that sequence.  Rationals keep their
    standard interval neighborhoods.  T2 (Hausdorff) but NOT regular.
    """
    space = BasisDefinedSpace(
        carrier="R",
        metadata={
            "name": "Rational sequence topology",
            "description": "R with rational-sequence neighborhoods at irrationals; T2 but not T3.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "t0", "t1", "hausdorff",
        "separable", "first_countable",
        "not_regular", "not_normal",
        "not_second_countable", "not_metrizable",
        "not_compact",
    )
    return space


def particular_point_topology_on_R() -> BasisDefinedSpace:
    """Particular point topology on ℝ with distinguished point 0.

    τ = {∅} ∪ {U ⊆ ℝ : 0 ∈ U}.  Uncountable analogue of
    :func:`particular_point_topology_on_naturals`.
    Hyperconnected, T0, not T1.  {0} alone is a dense subset.
    """
    space = BasisDefinedSpace(
        carrier="R (PPT)",
        metadata={
            "name": "Particular point topology on R",
            "description": "Topology on R where U is open iff 0 in U (or U=empty); uncountable PPT.",
            "cardinality": "uncountable",
            "local_base_size": "2",
            "basis_size": "uncountable",
            "particular_point": 0,
        },
    )
    space.add_tags(
        "t0", "not_t1", "not_hausdorff",
        "connected", "hyperconnected",
        "separable", "first_countable",
        "not_second_countable",
        "not_compact",
    )
    return space


def excluded_point_topology_on_R() -> BasisDefinedSpace:
    """Excluded point topology on ℝ with excluded point 0.

    τ = {U ⊆ ℝ : 0 ∉ U} ∪ {ℝ}.  Uncountable analogue of
    :func:`excluded_point_topology_on_naturals`.
    Connected, T0, not T1.  Every dense subset must contain all non-zero reals.
    """
    space = BasisDefinedSpace(
        carrier="R (EPT)",
        metadata={
            "name": "Excluded point topology on R",
            "description": "Topology on R where U is open iff 0 not in U or U=R; uncountable EPT.",
            "cardinality": "uncountable",
            "local_base_size": "2",
            "basis_size": "uncountable",
            "excluded_point": 0,
        },
    )
    space.add_tags(
        "t0", "not_t1", "not_hausdorff",
        "connected",
        "first_countable",
        "not_separable", "not_second_countable",
        "not_compact",
    )
    return space


def divisor_topology() -> BasisDefinedSpace:
    """Divisor topology on ℕ+ = {1, 2, 3, ...}.

    U ⊆ ℕ+ is open iff it is downward-closed under divisibility:
    n ∈ U and d | n implies d ∈ U.  Smallest open set containing n is
    div(n) = {d : d | n}.  T0, not T1 (1 lies in every non-empty open set).
    Connected.
    """
    space = BasisDefinedSpace(
        carrier="N+",
        metadata={
            "name": "Divisor topology",
            "description": "Topology on N+ where open sets are downward-closed under divisibility.",
            "cardinality": "aleph_0",
            "local_base_size": "1",
            "basis_size": "aleph_0",
        },
    )
    space.add_tags(
        "t0", "not_t1", "not_hausdorff",
        "connected",
        "first_countable",
        "second_countable", "separable",
        "not_compact",
    )
    return space


def uncountable_discrete_space() -> MetricLikeSpace:
    """Uncountable discrete space: an uncountable set with the discrete topology.

    Metrizable (discrete metric), locally compact (each singleton is open and compact).
    Not compact, not separable, not second countable, not Lindelöf.
    Realized as ℝ with the discrete topology.
    """
    space = MetricLikeSpace(
        carrier="R (discrete)",
        metadata={
            "name": "Uncountable discrete space",
            "description": "R with the discrete topology; metrizable, locally compact, not separable.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "discrete",
        "metrizable", "normal", "completely_metrizable",
        "zero_dimensional", "totally_disconnected",
        "locally_compact",
        "not_compact", "not_connected", "not_path_connected",
        "not_separable", "not_second_countable", "not_lindelof",
    )
    return space


def double_arrow_space() -> BasisDefinedSpace:
    """Double arrow space: [0, 1] × {0, 1} with the lexicographic order topology.

    Homeomorphic to the Cantor set.
    Compact, perfect, zero-dimensional, second countable, metrizable.
    """
    space = BasisDefinedSpace(
        carrier="[0,1] x {0,1} lex",
        metadata={
            "name": "Double arrow space",
            "description": "[0,1] x {0,1} with lex order topology; homeomorphic to the Cantor set.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "normal",
        "compact", "perfect",
        "zero_dimensional", "totally_disconnected",
        "second_countable", "first_countable", "separable",
        "metrizable",
        "not_connected", "not_path_connected",
    )
    return space


def annulus() -> MetricLikeSpace:
    """Closed annulus A = {(x, y) ∈ ℝ² : 1/4 ≤ x² + y² ≤ 1}.

    Compact, connected, not simply connected (π₁(A) = ℤ).
    Deformation retracts onto S¹.
    """
    space = MetricLikeSpace(
        carrier="annulus",
        metadata={
            "name": "Annulus",
            "description": "Closed annulus {(x,y) in R^2 : 1/4 <= x^2+y^2 <= 1}; retracts to S^1.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 2,
        },
    )
    space.add_tags(
        "compact", "locally_compact",
        "connected", "path_connected",
        "locally_connected", "locally_path_connected",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
        "not_simply_connected",
    )
    return space


def wedge_sum_of_circles(n: int = 2) -> TopologicalSpace:
    """Wedge sum of n circles S¹ ∨ ... ∨ S¹ (n ≥ 1).

    Compact, path-connected.  Fundamental group is the free group on n generators.
    Not simply connected for all n ≥ 1 (π₁(S¹) = ℤ, free group on n gens for n≥2).
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    space = TopologicalSpace.symbolic(
        description=f"Wedge of {n} circles at a common basepoint.",
        representation="symbolic_cw_complex",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected",
        ],
    )
    space.metadata["name"] = f"Wedge of {n} circles"
    space.metadata["n"] = n
    return space


# ---------------------------------------------------------------------------
# Batch 7 — half-planes, p-adic numbers, fractal continua, parameterized
#            manifolds, ordinal spaces, and function spaces
# ---------------------------------------------------------------------------

def upper_half_plane() -> MetricLikeSpace:
    """Upper half-plane ℍ = {(x, y) ∈ ℝ² : y > 0}.

    Open 2-manifold homeomorphic to ℝ².
    Simply connected, locally compact, not compact.
    """
    space = MetricLikeSpace(
        carrier="H",
        metadata={
            "name": "Upper half-plane",
            "description": "H = {(x,y) in R^2 : y > 0}; open 2-manifold homeomorphic to R^2.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected", "simply_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
        "not_compact",
    )
    return space


def closed_upper_half_plane() -> MetricLikeSpace:
    """Closed upper half-plane ℍ̄ = {(x, y) ∈ ℝ² : y ≥ 0}.

    2-manifold with boundary (∂ = ℝ × {0}).
    Contractible (hence simply connected), locally compact, not compact.
    """
    space = MetricLikeSpace(
        carrier="H_closed",
        metadata={
            "name": "Closed upper half-plane",
            "description": "H_closed = {(x,y) in R^2 : y >= 0}; 2-manifold with boundary, contractible.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected", "simply_connected", "contractible",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
        "not_compact",
    )
    return space


def p_adic_numbers() -> MetricLikeSpace:
    """p-adic number field ℚ_p with the p-adic metric topology.

    Locally compact, totally disconnected, zero-dimensional.
    Not compact (unlike ℤ_p).  Completion of ℚ w.r.t. the p-adic absolute value.
    """
    space = MetricLikeSpace(
        carrier="Q_p",
        metadata={
            "name": "p-adic numbers",
            "description": "p-adic field Q_p with the p-adic metric; locally compact, totally disconnected.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "locally_compact",
        "metrizable", "normal", "completely_metrizable",
        "second_countable", "first_countable", "separable",
        "zero_dimensional", "totally_disconnected",
        "not_compact", "not_connected", "not_path_connected",
    )
    return space


def sierpinski_triangle() -> MetricLikeSpace:
    """Sierpiński triangle (gasket): self-similar fractal compact continuum.

    Constructed by repeatedly removing open middle triangles from [0,1]².
    Compact, path-connected, locally connected.  Not simply connected
    (infinitely many holes; fundamental group is complicated).
    """
    space = MetricLikeSpace(
        carrier="sierpinski_triangle",
        metadata={
            "name": "Sierpinski triangle",
            "description": "Self-similar fractal gasket in R^2; compact, path-connected, infinitely many holes.",
            "cardinality": "uncountable",
            "ambient": "R^2",
        },
    )
    space.add_tags(
        "compact",
        "connected", "path_connected", "locally_connected", "locally_path_connected",
        "nowhere_dense",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
        "not_simply_connected",
    )
    return space


def real_projective_n_space(n: int) -> TopologicalSpace:
    """Real projective n-space RP^n = S^n / (x ~ −x).

    Compact n-manifold.  For n=1 homeomorphic to S¹.
    π₁(RP^n) = ℤ for n=1, ℤ/2ℤ for n≥2 — not simply connected.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    space = TopologicalSpace.symbolic(
        description=f"RP^{n} = S^{n} / antipodal map; compact {n}-manifold.",
        representation="symbolic_manifold",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected", "locally_compact",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected",
        ],
    )
    space.metadata["name"] = f"RP^{n}"
    space.metadata["n"] = n
    space.metadata["dimension"] = n
    return space


def cofinite_topology_on_integers() -> CofiniteSpace:
    """Cofinite topology on ℤ: open sets are ∅ and all cofinite subsets.

    Homeomorphic to :func:`cofinite_topology_on_naturals`.
    T1, compact, connected (hyperconnected), not Hausdorff.
    """
    space = CofiniteSpace(
        carrier="Z",
        metadata={
            "name": "Cofinite topology on Z",
            "description": "Integers with cofinite topology; T1, compact, hyperconnected.",
            "cardinality": "aleph_0",
        },
    )
    space.add_tags(
        "t1", "not_hausdorff",
        "compact", "connected", "hyperconnected",
        "lindelof",
        "second_countable", "first_countable", "separable",
        "not_metrizable",
    )
    return space


def long_ray() -> BasisDefinedSpace:
    """Long ray L = [0, ω₁) × [0, 1) with the lexicographic order topology.

    The "positive half" of the long line.  A connected locally compact
    1-manifold with boundary that is not second countable.
    """
    space = BasisDefinedSpace(
        carrier="[0,omega_1) x [0,1) lex",
        metadata={
            "name": "Long ray",
            "description": "[0,omega_1) x [0,1) with lex order topology; half of the long line.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "uncountable",
        },
    )
    space.add_tags(
        "hausdorff", "t0", "t1",
        "normal",
        "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "first_countable",
        "not_compact", "not_second_countable", "not_separable",
        "not_metrizable", "not_lindelof",
    )
    return space


def knaster_continuum() -> TopologicalSpace:
    """Knaster continuum (bucket handle): arc-like indecomposable continuum.

    Constructed from the Cantor set by attaching semicircular arcs over the
    removed intervals.  Compact, connected, metrizable, NOT locally connected.
    """
    return _symbolic(
        name="Knaster continuum",
        description="Bucket-handle arc-like continuum over the Cantor set; compact, not locally connected.",
        representation="symbolic_continuum",
        tags=[
            "compact", "connected",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_locally_connected", "not_path_connected",
            "not_locally_path_connected",
        ],
    )


def complex_projective_plane() -> MetricLikeSpace:
    """Complex projective plane ℂP²: the space of complex lines through the
    origin in ℂ³.

    Compact 4-manifold (real dimension 4), simply connected.
    π₁(ℂP²) = 0, π₂(ℂP²) = ℤ.
    """
    space = MetricLikeSpace(
        carrier="CP^2",
        metadata={
            "name": "Complex projective plane",
            "description": "CP^2 = (C^3 \\ {0}) / (z ~ lambda*z); compact 4-manifold, simply connected.",
            "cardinality": "uncountable",
            "dimension": 4,
        },
    )
    space.add_tags(
        "compact", "locally_compact",
        "connected", "path_connected", "simply_connected",
        "locally_connected", "locally_path_connected",
        "second_countable", "first_countable", "separable",
        "metrizable", "normal",
    )
    return space


def infinite_product_of_reals() -> MetricLikeSpace:
    """Countable infinite product ℝ^ω = ∏_{n≥1} ℝ with the product topology.

    Metrizable (by d(x,y) = ∑ 2^{-n} min(|x_n − y_n|, 1)),
    separable (ℚ^ω is dense), second countable.  Contractible.
    NOT locally compact (closed unit ball is not compact in infinite dimensions).
    """
    space = MetricLikeSpace(
        carrier="R^omega",
        metadata={
            "name": "Infinite product of reals",
            "description": "R^omega = product of countably many copies of R with product topology.",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "connected", "path_connected", "simply_connected", "contractible",
        "locally_connected", "locally_path_connected",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "completely_normal",
        "not_compact", "not_locally_compact",
    )
    return space


def n_torus(n: int) -> TopologicalSpace:
    """n-torus T^n = S¹ × ... × S¹ (n factors).

    Compact n-manifold.  π₁(T^n) = ℤ^n — not simply connected for n≥1.
    For n=1 homeomorphic to S¹; for n=2 homeomorphic to :func:`torus`.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    space = TopologicalSpace.symbolic(
        description=f"T^{n} = (S^1)^{n}; compact {n}-manifold with pi_1 = Z^{n}.",
        representation="symbolic_manifold",
        tags=[
            "compact", "connected", "path_connected",
            "locally_connected", "locally_path_connected", "locally_compact",
            "second_countable", "first_countable", "separable",
            "metrizable", "hausdorff", "t0", "t1", "normal",
            "not_simply_connected",
        ],
    )
    space.metadata["name"] = f"T^{n}"
    space.metadata["n"] = n
    space.metadata["dimension"] = n
    return space


def open_unit_disk() -> MetricLikeSpace:
    """Open unit disk B² = {(x, y) ∈ ℝ² : x² + y² < 1}.

    Simply connected, homeomorphic to ℝ² and to the upper half-plane.
    Locally compact, not compact.
    """
    space = MetricLikeSpace(
        carrier="B^2",
        metadata={
            "name": "Open unit disk",
            "description": "B^2 = {(x,y) in R^2 : x^2+y^2 < 1}; homeomorphic to R^2.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected", "simply_connected", "contractible",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal",
        "not_compact",
    )
    return space


# ---------------------------------------------------------------------------
# Batch 8 — genus-g surfaces, n-ball, K-topology, solenoid, lens spaces, …
# ---------------------------------------------------------------------------

def genus_g_surface(g: int = 1) -> TopologicalSpace:
    """Closed orientable surface Σ_g of genus g ≥ 0.

    Σ_0 = S², Σ_1 = torus, Σ_g (g ≥ 2) = connected sum of g tori.
    π₁ is trivial for g = 0; has 2g generators for g ≥ 1.
    """
    if g < 0:
        raise ValueError("g must be a non-negative integer")
    tags = [
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "metrizable", "hausdorff", "t1", "t0", "normal",
        "second_countable", "first_countable", "separable",
    ]
    if g == 0:
        tags.append("simply_connected")
    space = TopologicalSpace.symbolic(
        description=f"Sigma_{g}: closed orientable surface of genus {g}",
        representation="symbolic_manifold",
        tags=tags,
    )
    space.metadata["name"] = f"Genus-{g} surface"
    space.metadata["genus"] = g
    space.metadata["dimension"] = 2
    return space


def n_ball(n: int = 3) -> MetricLikeSpace:
    """Closed n-ball D^n = {x ∈ ℝ^n : |x| ≤ 1}.

    Compact, contractible, simply connected. Boundary is S^(n-1).
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    space = MetricLikeSpace(
        carrier=f"D^{n}",
        metadata={
            "name": f"{n}-ball",
            "description": f"D^{n} = closed unit ball in R^{n}; compact, contractible.",
            "cardinality": "uncountable",
            "ambient": f"R^{n}",
            "dimension": n,
            "n": n,
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected", "simply_connected", "contractible",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "hausdorff", "t1", "t0",
    )
    return space


def k_topology_on_R() -> BasisDefinedSpace:
    """K-topology on ℝ: standard open intervals plus sets (a, b) \\ K where K = {1/n : n ∈ ℕ⁺}.

    Strictly finer than the standard topology. Hausdorff (T2) but not regular (T3).
    Connected, second countable, separable, not compact, not metrizable.
    """
    space = BasisDefinedSpace(
        carrier="R",
        metadata={
            "name": "K-topology on R",
            "description": "R with K-topology: (a,b) and (a,b)\\K as basis; T2 but not T3.",
            "cardinality": "uncountable",
            "local_base_size": "aleph_0",
            "basis_size": "aleph_0",
            "K_set": "{1/n : n in N+}",
        },
    )
    space.add_tags(
        "connected",
        "hausdorff", "t1", "t0",
        "first_countable", "second_countable", "separable", "lindelof",
        "not_regular", "not_compact", "not_metrizable",
    )
    return space


def solenoid() -> TopologicalSpace:
    """Dyadic solenoid: inverse limit of S¹ under the doubling map x ↦ 2x (mod 1).

    Compact, connected, metrizable. Neither locally connected nor path-connected.
    """
    space = _symbolic(
        "Dyadic solenoid",
        "Inverse limit of S^1 under 2x maps; compact, connected, not locally connected.",
        [
            "compact", "connected", "metrizable",
            "hausdorff", "t1", "t0", "normal",
            "first_countable", "second_countable", "separable",
            "not_path_connected", "not_locally_connected",
        ],
    )
    return space


def extended_real_line() -> MetricLikeSpace:
    """Extended real line [-∞, +∞] = ℝ ∪ {-∞, +∞} with the order topology.

    Compact, connected, path-connected. Homeomorphic to the closed unit interval [0, 1].
    """
    space = MetricLikeSpace(
        carrier="[-inf, +inf]",
        metadata={
            "name": "Extended real line",
            "description": "R union {-inf,+inf} with order topology; homeomorphic to [0,1].",
            "cardinality": "uncountable",
        },
    )
    space.add_tags(
        "compact", "connected", "path_connected", "simply_connected", "contractible",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "hausdorff", "t1", "t0",
    )
    return space


def uncountable_product_of_two_point_spaces() -> TopologicalSpace:
    """{0, 1}^c — product of c = |ℝ| many copies of the two-point discrete space.

    Compact (Tychonoff) and Hausdorff. Separable (HMP theorem).
    Not metrizable, not first countable, totally disconnected.
    """
    space = _symbolic(
        "{0,1}^c",
        "{0,1}^c: uncountable product; compact, Hausdorff, separable, not metrizable.",
        [
            "compact", "hausdorff", "t1", "t0", "normal",
            "separable", "zero_dimensional", "totally_disconnected",
            "not_connected", "not_metrizable", "not_first_countable", "not_second_countable",
        ],
    )
    return space


def wedge_of_two_spheres() -> TopologicalSpace:
    """Wedge sum S² ∨ S²: two 2-spheres identified at a single basepoint.

    Simply connected (π₁ = 1 by van Kampen), compact, path-connected.
    π₂ ≅ ℤ ⊕ ℤ; not contractible.
    """
    space = _symbolic(
        "S^2 v S^2",
        "S^2 v S^2: wedge of two 2-spheres; simply connected, compact, not contractible.",
        [
            "compact", "connected", "path_connected", "simply_connected",
            "locally_connected", "locally_path_connected", "locally_compact",
            "metrizable", "hausdorff", "t1", "t0", "normal",
            "second_countable", "first_countable", "separable",
            "not_contractible",
        ],
    )
    return space


def suspension_of_cantor_set() -> TopologicalSpace:
    """Suspension of the Cantor set SC = (C × [0,1]) / (C×{0} ~ pt, C×{1} ~ pt).

    Compact, path-connected. Not locally connected away from the two suspension vertices.
    """
    space = _symbolic(
        "Suspension of Cantor set",
        "SC: suspension of the Cantor set; compact, path-connected, not locally connected.",
        [
            "compact", "connected", "path_connected",
            "metrizable", "hausdorff", "t1", "t0", "normal",
            "second_countable", "first_countable", "separable",
            "not_locally_connected",
        ],
    )
    return space


def quarter_plane() -> MetricLikeSpace:
    """Closed quarter-plane [0, ∞) × [0, ∞) with the subspace topology from ℝ².

    Contractible, simply connected, locally compact. Not compact.
    """
    space = MetricLikeSpace(
        carrier="[0,inf)^2",
        metadata={
            "name": "Quarter plane",
            "description": "[0,inf)x[0,inf): contractible, simply connected, locally compact.",
            "cardinality": "uncountable",
            "ambient": "R^2",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected", "simply_connected", "contractible",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "normal", "hausdorff", "t1", "t0",
        "not_compact",
    )
    return space


def punctured_torus() -> MetricLikeSpace:
    """Torus with one point removed: T² \\ {pt}.

    Homotopy equivalent to S¹ ∨ S¹; π₁ = free group on 2 generators.
    Locally compact, not compact, not simply connected.
    """
    space = MetricLikeSpace(
        carrier="T^2 \\ {pt}",
        metadata={
            "name": "Punctured torus",
            "description": "T^2 minus a point; homotopy equiv to S^1 v S^1, pi_1 = F_2.",
            "cardinality": "uncountable",
            "dimension": 2,
        },
    )
    space.add_tags(
        "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "second_countable", "first_countable", "separable", "lindelof",
        "metrizable", "hausdorff", "t1", "t0", "normal",
        "not_compact", "not_simply_connected",
    )
    return space


def discrete_sum_of_circles() -> TopologicalSpace:
    """Countable disjoint union ⊔_{n ≥ 1} S¹ of circles.

    Locally compact, sigma-compact, metrizable, second countable.
    Not compact (infinitely many components), not connected.
    """
    space = _symbolic(
        "Countable disjoint union of circles",
        "Disjoint union of countably many S^1; locally compact, sigma-compact, not connected.",
        [
            "locally_compact", "locally_connected", "locally_path_connected",
            "metrizable", "hausdorff", "t1", "t0", "normal",
            "second_countable", "first_countable", "separable",
            "sigma_compact",
            "not_compact", "not_connected",
        ],
    )
    return space


def lens_space(p: int = 2, q: int = 1) -> TopologicalSpace:
    """Lens space L(p, q): compact 3-manifold obtained as S³ / (ℤ/pℤ).

    π₁ = ℤ/pℤ for p ≥ 2; L(1, q) ≅ S³ (simply connected).
    """
    if p < 1:
        raise ValueError("p must be a positive integer")
    tags = [
        "compact", "connected", "path_connected",
        "locally_connected", "locally_path_connected", "locally_compact",
        "metrizable", "hausdorff", "t1", "t0", "normal",
        "second_countable", "first_countable", "separable",
    ]
    if p == 1:
        tags.append("simply_connected")
    space = TopologicalSpace.symbolic(
        description=f"L({p},{q}): lens space, compact 3-manifold, pi_1 = Z/{p}Z",
        representation="symbolic_manifold",
        tags=tags,
    )
    space.metadata["name"] = f"Lens space L({p},{q})"
    space.metadata["p"] = p
    space.metadata["q"] = q
    space.metadata["dimension"] = 3
    return space


__all__ = [
    # Batch 1
    "sierpinski_space",
    "particular_point_topology",
    "excluded_point_topology",
    "cofinite_topology_on_naturals",
    "cofinite_topology_on_reals",
    "cocountable_topology_on_reals",
    "real_line",
    "sorgenfrey_line",
    "rational_numbers",
    "irrational_numbers",
    "cantor_set",
    "hilbert_cube",
    "long_line",
    "topologists_sine_curve",
    "comb_space",
    "warsaw_circle",
    "infinite_broom",
    "moore_plane",
    "arens_fort_space",
    "fort_space",
    # Batch 2
    "discrete_space",
    "indiscrete_space",
    "discrete_countable_space",
    "particular_point_topology_on_naturals",
    "excluded_point_topology_on_naturals",
    "double_origin_topology",
    "michael_line",
    "tychonoff_plank",
    "deleted_tychonoff_plank",
    "stone_cech_compactification_of_N",
    "furstenberg_topology",
    "pseudo_arc",
    # Batch 5
    "real_plane",
    "punctured_plane",
    "two_sphere",
    "three_sphere",
    "n_sphere",
    "sierpinski_carpet",
    "menger_curve",
    "open_cylinder",
    "tube",
    "open_topologists_sine_curve",
    "erdos_space",
    "complete_erdos_space",
    # Batch 4
    "half_open_interval",
    "open_interval",
    "half_open_real_line",
    "real_projective_plane",
    "klein_bottle",
    "mobius_band",
    "dunce_hat",
    "hawaiian_earring",
    "omega_1",
    "omega_1_plus_1",
    "stone_cech_remainder",
    "one_point_compactification_of_Q",
    # Batch 3
    "unit_interval",
    "unit_circle",
    "closed_unit_disk",
    "torus",
    "cantor_cube",
    "baire_space",
    "lexicographic_square",
    "one_point_compactification_of_reals",
    "cantor_fan",
    "knaster_kuratowski_fan",
    "hilbert_space",
    "p_adic_integers",
    # Batch 6
    "real_n_space",
    "sorgenfrey_plane",
    "one_point_compactification_of_N",
    "omega_plus_1",
    "rational_sequence_topology",
    "particular_point_topology_on_R",
    "excluded_point_topology_on_R",
    "divisor_topology",
    "uncountable_discrete_space",
    "double_arrow_space",
    "annulus",
    "wedge_sum_of_circles",
    # Batch 7
    "upper_half_plane",
    "closed_upper_half_plane",
    "p_adic_numbers",
    "sierpinski_triangle",
    "real_projective_n_space",
    "cofinite_topology_on_integers",
    "long_ray",
    "knaster_continuum",
    "complex_projective_plane",
    "infinite_product_of_reals",
    "n_torus",
    "open_unit_disk",
    # Batch 8
    "genus_g_surface",
    "n_ball",
    "k_topology_on_R",
    "solenoid",
    "extended_real_line",
    "uncountable_product_of_two_point_spaces",
    "wedge_of_two_spheres",
    "suspension_of_cantor_set",
    "quarter_plane",
    "punctured_torus",
    "discrete_sum_of_circles",
    "lens_space",
]
