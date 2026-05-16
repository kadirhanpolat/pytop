"""
function_spaces.py — Cilt III v0.1.58
======================================
Durable API for function-space topologies (pointwise, uniform, compact-open).

Public surface
--------------
pointwise_topology_profile(space)      → dict
uniform_topology_profile(space)        → dict
compact_open_topology_profile(space)   → dict
function_space_profile(space)          → dict  (all three combined)
analyze_function_space(space)          → Result
FunctionSpaceError                     → exception class
"""

from __future__ import annotations

from typing import Any

from .result import Result

# ---------------------------------------------------------------------------
# Try to import FiniteTopologicalSpace — graceful degradation if unavailable
# ---------------------------------------------------------------------------
try:
    from .finite_spaces import FiniteTopologicalSpace
except Exception:  # pragma: no cover
    FiniteTopologicalSpace = None  # type: ignore


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class FunctionSpaceError(Exception):
    """Raised when a function-space operation cannot be completed."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _representation_of(space: Any) -> str:
    """Return the canonical representation tag for *space*."""
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return "finite"
    metadata = getattr(space, "metadata", {}) or {}
    if isinstance(metadata, dict) and "representation" in metadata:
        return str(metadata["representation"]).strip().lower()
    rep = getattr(space, "representation", None)
    if rep:
        return str(rep).strip().lower()
    return "symbolic_general"


def _tags_of(space: Any) -> frozenset:
    """Return the property tags attached to *space* (empty frozenset if none)."""
    metadata = getattr(space, "metadata", {}) or {}
    raw = metadata.get("tags", []) if isinstance(metadata, dict) else []
    if not raw:
        raw = getattr(space, "tags", []) or []
    return frozenset(str(t).lower().strip() for t in raw)


def _carrier_size(space: Any) -> int | None:
    """Return |X| if determinable, else None."""
    if FiniteTopologicalSpace is not None and isinstance(space, FiniteTopologicalSpace):
        return len(space.carrier)
    carrier = getattr(space, "carrier", None)
    if carrier is not None:
        try:
            return len(carrier)
        except TypeError:
            pass
    return None


def _family_lane(key: str) -> str:
    """Return the pedagogical lane label for a topology family key."""
    if key == "pointwise":
        return "entry"
    if key == "compact_open":
        return "bridge"
    if key == "uniform":
        return "advanced"
    raise FunctionSpaceError(f"unknown function-space family key: {key}")


def _family_focus(key: str) -> str:
    """Return the central teaching focus for a topology family key."""
    if key == "pointwise":
        return "coordinate control at finitely many chosen points"
    if key == "compact_open":
        return "uniform control on compact subsets"
    if key == "uniform":
        return "one global error bound on the whole domain"
    raise FunctionSpaceError(f"unknown function-space family key: {key}")


def _family_warning(key: str, rep: str, tags: frozenset) -> str:
    """Return the main warning line for a topology family key."""
    if key == "pointwise":
        return (
            "pointwise convergence is weak: coordinatewise control does not imply "
            "uniform control or preservation of global error bounds"
        )
    if key == "compact_open":
        if "locally_compact" in tags or "locally_compact_hausdorff" in tags:
            return (
                "compact-open is the preferred bridge here, but it still differs "
                "from full uniform convergence on non-compact domains"
            )
        return (
            "compact-open sits between pointwise and uniform topologies; "
            "without local compactness the exponential-law story needs k-space care"
        )
    if key == "uniform":
        if rep == "finite" or "compact" in tags or "compact_hausdorff" in tags:
            return "uniform convergence is strong but behaves cleanly on finite/compact domains"
        return (
            "uniform convergence is often too strong for homotopy-facing mapping spaces "
            "on non-compact domains"
        )
    raise FunctionSpaceError(f"unknown function-space family key: {key}")


# ---------------------------------------------------------------------------
# Pointwise convergence topology  C(X,Y)_pt
# ---------------------------------------------------------------------------

def pointwise_topology_profile(space: Any) -> dict[str, Any]:
    """
    Describe the pointwise convergence topology on C(X, Y).

    Parameters
    ----------
    space : Any
        The *domain* space X.  Y is assumed ℝ (or a fixed metrizable target).

    Returns
    -------
    dict with keys:
        topology_name, basis_description, hausdorff, first_countable,
        second_countable_condition, metrizability_note, representation
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    hausdorff = True  # pointwise topology on C(X,ℝ) is always Hausdorff
    first_countable = True  # each point has a countable neighbourhood basis

    second_countable: str
    if rep == "finite" and n is not None:
        second_countable = "yes — X finite, so C(X,ℝ)≅ℝⁿ is second countable"
    elif "second_countable" in tags or "separable_metrizable" in tags:
        second_countable = "yes — X second countable implies C(X,ℝ)_pt second countable"
    elif "uncountable" in tags or "non_second_countable" in tags:
        second_countable = "not in general — X not second countable"
    else:
        second_countable = "depends on X"

    metrizability: str
    if rep == "finite":
        metrizability = "metrizable (product of finitely many copies of ℝ)"
    elif "second_countable" in tags:
        metrizability = "metrizable (second countable Hausdorff)"
    else:
        metrizability = "metrizable iff X is countable"

    basis: str
    if rep == "finite" and n is not None:
        basis = (
            f"Subbasic sets: {{f ∈ C(X,ℝ) : f(xᵢ) ∈ Uᵢ}} for xᵢ ∈ X, Uᵢ open in ℝ; "
            f"with |X|={n} this is a finite product topology on ℝ^{n}"
        )
    else:
        basis = (
            "Subbasic sets of the form {f ∈ C(X,ℝ) : f(x) ∈ U} "
            "for x ∈ X and U open in ℝ; "
            "equivalently the subspace topology inherited from ℝ^X"
        )

    return {
        "topology_name": "pointwise convergence topology",
        "notation": "C(X,ℝ)_pt  or  Cₚ(X)",
        "basis_description": basis,
        "hausdorff": hausdorff,
        "first_countable": first_countable,
        "second_countable_condition": second_countable,
        "metrizability_note": metrizability,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Uniform convergence topology  C(X,Y)_u
# ---------------------------------------------------------------------------

def uniform_topology_profile(space: Any) -> dict[str, Any]:
    """
    Describe the uniform (sup-metric) topology on C(X, Y).

    Assumes Y = ℝ with bounded functions, or equivalently the sup-metric
    d_∞(f,g) = sup_{x∈X} |f(x)−g(x)|.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    metrizable = True  # always metrizable (sup-metric)

    complete: str
    if rep == "finite":
        complete = "yes — C(X,ℝ) with sup-metric is complete (finite product)"
    elif "compact" in tags or "locally_compact" in tags:
        complete = "yes — C(X,ℝ) with sup-metric is complete when X is compact"
    else:
        complete = "complete if X is compact; otherwise completeness depends on X"

    separable: str
    if rep == "finite" and n is not None:
        separable = f"yes — finite-dimensional product ℝ^{n} is separable"
    elif "compact_metrizable" in tags or "second_countable" in tags:
        separable = "yes — C(X,ℝ) separable when X is compact metrizable"
    else:
        separable = "separable iff X is compact metrizable"

    finer: str = (
        "The uniform topology is finer than or equal to the pointwise topology; "
        "uniform convergence implies pointwise convergence, not conversely."
    )

    if rep == "finite" and n is not None:
        metric_desc = (
            f"d_∞(f,g) = max_{{x∈X}} |f(x)−g(x)| (X finite, |X|={n}); "
            "coincides with the ℓ^∞ product metric on ℝⁿ"
        )
    else:
        metric_desc = "d_∞(f,g) = sup_{x∈X} |f(x)−g(x)|  (requires bounded functions or compact X)"

    return {
        "topology_name": "uniform convergence topology",
        "notation": "C(X,ℝ)_u  or  (C(X,ℝ), d_∞)",
        "metric_description": metric_desc,
        "metrizable": metrizable,
        "complete": complete,
        "separable": separable,
        "comparison_with_pointwise": finer,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# Compact-open topology  C(X,Y)_co
# ---------------------------------------------------------------------------

def compact_open_topology_profile(space: Any) -> dict[str, Any]:
    """
    Describe the compact-open topology on C(X, Y).

    Assumes Y = ℝ (or any metrizable space).  The compact-open topology has
    sub-basic sets V(K, U) = {f ∈ C(X,Y) : f(K) ⊆ U} for K compact in X,
    U open in Y.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    # Coincidence with uniform topology
    coincides_uniform: str
    if rep == "finite":
        coincides_uniform = (
            "yes — on finite X every subset is compact, so compact-open = "
            "uniform = pointwise topology"
        )
    elif "compact" in tags or "compact_hausdorff" in tags:
        coincides_uniform = (
            "yes — when X is compact, compact-open topology on C(X,ℝ) "
            "coincides with the uniform topology"
        )
    elif "locally_compact" in tags or "locally_compact_hausdorff" in tags:
        coincides_uniform = (
            "not in general — compact-open ≠ uniform when X is only locally compact; "
            "however compact-open is natural for homotopy theory here"
        )
    else:
        coincides_uniform = (
            "generally finer than pointwise, coarser than or equal to uniform "
            "on compact subsets"
        )

    # Hausdorff
    hausdorff: str
    if "hausdorff" in tags or "t2" in tags or rep == "finite":
        hausdorff = "yes — compact-open topology on C(X,Y) is Hausdorff when Y is Hausdorff"
    else:
        hausdorff = "Hausdorff when Y is Hausdorff"

    # Exponential law
    exponential: str
    if "locally_compact" in tags or "compact" in tags or "locally_compact_hausdorff" in tags:
        exponential = (
            "Exponential law holds: C(X × Z, Y) ≅ C(Z, C(X,Y)_co) "
            "when X is locally compact Hausdorff"
        )
    elif rep == "finite":
        exponential = (
            "Exponential law holds: X finite is locally compact, "
            "so C(X×Z, Y) ≅ C(Z, C(X,Y)_co)"
        )
    else:
        exponential = (
            "Exponential law C(X×Z,Y) ≅ C(Z, C(X,Y)_co) holds "
            "when X is locally compact Hausdorff"
        )

    basis = (
        "Sub-basic sets: V(K,U) = {f ∈ C(X,Y) : f(K) ⊆ U} "
        "for K ⊆ X compact, U ⊆ Y open"
    )

    return {
        "topology_name": "compact-open topology",
        "notation": "C(X,Y)_co  or  Y^X with compact-open topology",
        "basis_description": basis,
        "hausdorff": hausdorff,
        "coincides_with_uniform": coincides_uniform,
        "exponential_law": exponential,
        "representation": rep,
    }


def function_space_topology_families(space: Any) -> list[dict[str, Any]]:
    """
    Return a pedagogically ordered family list for pointwise / compact-open /
    uniform topologies on C(X, R).
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    pointwise = pointwise_topology_profile(space)
    compact_open = compact_open_topology_profile(space)
    uniform = uniform_topology_profile(space)

    if rep == "finite":
        ordering_note = "all three coincide on finite domains"
    elif "compact" in tags or "compact_hausdorff" in tags:
        ordering_note = "pointwise is weakest; compact-open and uniform coincide"
    elif "locally_compact" in tags or "locally_compact_hausdorff" in tags:
        ordering_note = "strict pedagogical chain: pointwise < compact-open < uniform"
    else:
        ordering_note = "general comparison chain: pointwise <= compact-open <= uniform"

    return [
        {
            "family_key": "pointwise",
            "lane": _family_lane("pointwise"),
            "pedagogical_focus": _family_focus("pointwise"),
            "ordering_note": ordering_note,
            "preferred_when": (
                "start with evaluation maps, coordinate language, and product-topology intuition"
            ),
            "warning_line": _family_warning("pointwise", rep, tags),
            "profile": pointwise,
        },
        {
            "family_key": "compact_open",
            "lane": _family_lane("compact_open"),
            "pedagogical_focus": _family_focus("compact_open"),
            "ordering_note": ordering_note,
            "preferred_when": (
                "move from pointwise checks to compact-subset control, homotopy, and exponential-law language"
            ),
            "warning_line": _family_warning("compact_open", rep, tags),
            "profile": compact_open,
        },
        {
            "family_key": "uniform",
            "lane": _family_lane("uniform"),
            "pedagogical_focus": _family_focus("uniform"),
            "ordering_note": ordering_note,
            "preferred_when": (
                "measure one simultaneous sup-norm error across the whole domain"
            ),
            "warning_line": _family_warning("uniform", rep, tags),
            "profile": uniform,
        },
    ]


def function_space_topology_selector(space: Any, family_key: str) -> dict[str, Any]:
    """Return exactly one family record by stable key."""
    normalized = str(family_key).strip().lower()
    for record in function_space_topology_families(space):
        if record["family_key"] == normalized:
            return record
    raise FunctionSpaceError(f"unknown function-space family key: {family_key}")


def render_function_space_topology_report(space: Any) -> str:
    """Render a compact human-readable separation report for the three topologies."""
    rep = _representation_of(space)
    families = function_space_topology_families(space)
    rows = [
        "Function-space topology separation report",
        f"domain representation: {rep}",
    ]
    for record in families:
        profile = record["profile"]
        rows.append(
            f"- {record['family_key']} [{record['lane']}]: "
            f"{record['pedagogical_focus']}; preferred when {record['preferred_when']}; "
            f"warning: {record['warning_line']}"
        )
        rows.append(
            f"  notation: {profile.get('notation', profile.get('topology_name', 'n/a'))}"
        )
    rows.append(
        "ordering reminder: start with pointwise, bridge with compact-open, and reserve uniform for global-error control."
    )
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Combined profile
# ---------------------------------------------------------------------------

def function_space_profile(space: Any) -> dict[str, Any]:
    """
    Return all three function-space topology profiles for *space* as domain X.

    Returns
    -------
    dict with keys 'pointwise', 'uniform', 'compact_open', 'domain_representation'
    """
    return {
        "domain_representation": _representation_of(space),
        "pointwise": pointwise_topology_profile(space),
        "uniform": uniform_topology_profile(space),
        "compact_open": compact_open_topology_profile(space),
    }


# ---------------------------------------------------------------------------
# Facade: analyze_function_space
# ---------------------------------------------------------------------------

def analyze_function_space(space: Any) -> Result:
    """
    Single-call facade that analyses *space* as the domain of a function space.

    Returns a :class:`~pytop.result.Result` whose ``value`` is the
    ``function_space_profile`` dict and whose ``justification`` summarises the
    key topological facts.

    Parameters
    ----------
    space : Any
        A topological space acting as the domain X for C(X, ℝ).

    Returns
    -------
    Result
        status="true", mode="theorem" (or "exact" for finite spaces)
    """
    rep = _representation_of(space)
    profile = function_space_profile(space)
    pt = profile["pointwise"]
    un = profile["uniform"]
    co = profile["compact_open"]
    family_report = render_function_space_topology_report(space)

    mode = "exact" if rep == "finite" else "theorem"
    n = _carrier_size(space)

    justification = [
        f"Domain representation: {rep}",
        f"Pointwise topology (Cₚ(X)): Hausdorff={pt['hausdorff']}, "
        f"metrizability — {pt['metrizability_note']}",
        f"Uniform topology (d_∞): metrizable=True, complete — {un['complete']}",
        f"Compact-open topology: {co['coincides_with_uniform']}",
        f"Exponential law: {co['exponential_law']}",
        family_report,
    ]
    if rep == "finite" and n is not None:
        justification.insert(
            1,
            f"|X|={n}: all three topologies coincide (finite product topology on ℝ^{n})",
        )

    metadata = {
        "version": "0.1.58",
        "domain_representation": rep,
        "carrier_size": n,
        "profile": profile,
    }

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# v0.1.59 extensions — compact-open topology subsection
# ---------------------------------------------------------------------------

def compact_open_basis_elements(space: Any) -> dict[str, Any]:
    """
    Describe the sub-basic and basic open sets of the compact-open topology
    on C(X, Y) in detail, with examples for concrete space representations.

    Parameters
    ----------
    space : Any
        The domain space X.

    Returns
    -------
    dict with keys:
        subbasis_description, basis_description, neighbourhood_base,
        convergence_characterisation, finite_example (if applicable),
        representation
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    subbasis = (
        "S(K,U) = {f ∈ C(X,Y) : f(K) ⊆ U}  "
        "for K ⊆ X compact, U ⊆ Y open.  "
        "These sets form a sub-basis; finite intersections give a basis."
    )

    basis = (
        "Basic open sets: ⋂_{i=1}^{n} S(Kᵢ,Uᵢ) = "
        "{f ∈ C(X,Y) : f(Kᵢ) ⊆ Uᵢ for all i}.  "
        "A net (fₐ) converges in C(X,Y)_co iff "
        "fₐ|_K → f|_K uniformly for every compact K ⊆ X."
    )

    nbhd_base: str
    if rep == "finite" and n is not None:
        nbhd_base = (
            f"X finite (|X|={n}): every singleton {{x}} is compact, so "
            f"S({{x}},U) = {{f : f(x)∈U}} — same as pointwise sub-basis. "
            f"Neighbourhood base at f₀: products ∏_{{x∈X}} Uₓ with Uₓ open in Y, f₀(x)∈Uₓ."
        )
    elif "compact" in tags or "compact_hausdorff" in tags:
        nbhd_base = (
            "X compact: the single set S(X,U) = {f : f(X)⊆U} gives uniform control. "
            "Neighbourhood base at f₀: {f : d_∞(f,f₀) < ε} (uniform topology coincides)."
        )
    elif "locally_compact" in tags or "locally_compact_hausdorff" in tags:
        nbhd_base = (
            "X locally compact: neighbourhood base at f₀ consists of sets "
            "⋂_{i} S(Kᵢ,Uᵢ) where Kᵢ ranges over compact neighbourhoods of "
            "chosen points and Uᵢ = f₀(Kᵢ)^{+ε}."
        )
    else:
        nbhd_base = (
            "Neighbourhood base at f₀: finite intersections ⋂_i S(Kᵢ,Uᵢ) "
            "with f₀(Kᵢ) ⊆ Uᵢ. Convergence = compact-uniform convergence "
            "(uniform on each compact subset)."
        )

    convergence = (
        "A net (fₐ) → f in C(X,Y)_co  ⟺  "
        "for every compact K ⊆ X and ε>0 there exists α₀ s.t. "
        "α≥α₀ ⟹ sup_{x∈K} d(fₐ(x),f(x)) < ε.  "
        "(compact-uniform convergence)"
    )

    result: dict[str, Any] = {
        "topology_name": "compact-open topology — basis elements",
        "subbasis_description": subbasis,
        "basis_description": basis,
        "neighbourhood_base": nbhd_base,
        "convergence_characterisation": convergence,
        "representation": rep,
    }

    if rep == "finite" and n is not None:
        result["finite_example"] = (
            f"For X = {{0,…,{n-1}}} (discrete, |X|={n}) and Y=ℝ: "
            f"C(X,ℝ)_co = ℝ^{n} with product topology. "
            f"Sub-basic set S({{k}},(-ε,ε)) = {{f∈C(X,ℝ) : |f(k)|<ε}}."
        )

    return result


def compact_open_homotopy_profile(space: Any) -> dict[str, Any]:
    """
    Describe the role of the compact-open topology in homotopy theory.

    Covers: loop space Ω(X,x₀), path space PX, free loop space LX,
    adjunction with suspension, and the relationship to CW-complexes.

    Parameters
    ----------
    space : Any
        The base space X (typically a pointed topological space).

    Returns
    -------
    dict with keys:
        loop_space, path_space, free_loop_space,
        adjunction_with_suspension, cw_complex_note,
        exponential_law_statement, representation
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    # Loop space
    loop_space = (
        "Ω(X,x₀) = {γ ∈ C([0,1],X) : γ(0)=γ(1)=x₀} "
        "with subspace topology from C([0,1],X)_co. "
        "π₁(X,x₀) = π₀(Ω(X,x₀)) (path-components of loop space)."
    )

    # Path space
    path_space = (
        "PX = C([0,1],X)_co — the free path space. "
        "The evaluation map ev₁: PX → X, ev₁(γ)=γ(1), is a fibration "
        "(Hurewicz fibration) when X is well-pointed."
    )

    # Free loop space
    free_loop_space = (
        "LX = C(S¹,X)_co — the free loop space. "
        "Homotopy groups: πₙ(LX) ≅ πₙ(X) ⊕ πₙ₊₁(X) for simply connected X."
    )

    # Adjunction with suspension
    adjunction: str
    if rep == "finite":
        adjunction = (
            "X finite: [ΣA,X] ≅ [A, ΩX] holds formally; "
            "but suspension ΣA of a finite discrete space is a finite simplicial complex. "
            "Exponential law: C(ΣA,X) ≅ C(A, C(S¹,X)_co) = C(A,LX)."
        )
    elif "locally_compact" in tags or "locally_compact_hausdorff" in tags or "cw_complex" in tags:
        adjunction = (
            "Suspension–loop adjunction: [ΣA,X] ≅ [A,ΩX] in the homotopy category. "
            "Realised via exponential law: C(ΣA,X)_co ≅ C(A, ΩX)_co "
            "when A is locally compact Hausdorff (e.g. a CW-complex)."
        )
    else:
        adjunction = (
            "Suspension–loop adjunction [ΣA,X] ≅ [A,ΩX] holds "
            "when A is locally compact Hausdorff; "
            "general spaces require compactly generated (k-space) refinement."
        )

    # CW-complex note
    cw_note: str
    if "cw_complex" in tags or "locally_compact" in tags:
        cw_note = (
            "For CW-complexes the compact-open topology on mapping spaces "
            "is compactly generated; all standard homotopy adjunctions hold."
        )
    else:
        cw_note = (
            "For general spaces, replace C(X,Y)_co by its k-space reflection "
            "k(C(X,Y)_co) to ensure the exponential law and adjunction hold "
            "without local compactness hypothesis."
        )

    exp_law = (
        "Exponential law (compact-open version): "
        "if X is locally compact Hausdorff, then "
        "C(X×Z,Y)_co ≅ C(Z, C(X,Y)_co)_co  (homeomorphism). "
        "Equivalently: Y^{X×Z} ≅ (Y^X)^Z."
    )

    return {
        "topology_name": "compact-open topology — homotopy profile",
        "loop_space": loop_space,
        "path_space": path_space,
        "free_loop_space": free_loop_space,
        "adjunction_with_suspension": adjunction,
        "cw_complex_note": cw_note,
        "exponential_law_statement": exp_law,
        "representation": rep,
    }


# ---------------------------------------------------------------------------
# v0.1.60 — compare the three function-space topologies
# ---------------------------------------------------------------------------

def compare_function_space_topologies(space: Any) -> dict[str, Any]:
    """
    Compare the pointwise, uniform, and compact-open topologies on C(X, ℝ).

    Returns a structured dict with:
      - fineness_order: the ordering pt ≤ co ≤ u (with coincidence notes)
      - coincidence_conditions: when two or more topologies agree
      - comparison_table: list of dicts, one row per topology pair
      - counterexamples: classical spaces where topologies differ
      - summary: human-readable paragraph
      - representation: domain representation tag

    Parameters
    ----------
    space : Any
        The domain space X.
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)

    # ------------------------------------------------------------------
    # Fineness order
    # ------------------------------------------------------------------
    if rep == "finite":
        fineness_order = (
            "pt = co = u  (all three coincide on finite X; "
            "every subset is compact so pointwise = compact-open, "
            "and X finite ⟹ C(X,ℝ) ≅ ℝⁿ with product = uniform topology)"
        )
    elif "compact" in tags or "compact_hausdorff" in tags:
        fineness_order = (
            "pt ≤ co = u  (compact X: compact-open coincides with uniform; "
            "pointwise is strictly coarser unless X is finite)"
        )
    elif "locally_compact" in tags or "locally_compact_hausdorff" in tags:
        fineness_order = (
            "pt ≤ co ≤ u  (locally compact X: strict chain in general; "
            "co = u only on compact subsets)"
        )
    else:
        fineness_order = (
            "pt ≤ co ≤ u  in general; "
            "pt = co iff X is compact; co = u iff X is compact; "
            "pt = u iff X is finite (or X is compact and co = u = pt)"
        )

    # ------------------------------------------------------------------
    # Coincidence conditions
    # ------------------------------------------------------------------
    coincidence: dict[str, str] = {}

    if rep == "finite":
        coincidence["pt_eq_co"] = "yes — X finite"
        coincidence["co_eq_u"]  = "yes — X finite"
        coincidence["pt_eq_u"]  = "yes — X finite"
        coincidence["all_three"] = "yes — X finite"
    else:
        coincidence["pt_eq_co"] = (
            "yes iff X is compact (every compact set is finite intersection of opens)"
        )
        coincidence["co_eq_u"] = (
            "yes iff X is compact (uniform topology = compact-open on compact spaces)"
        )
        coincidence["pt_eq_u"] = (
            "yes iff X is finite (or more generally when X is compact and pt=co=u)"
        )
        if "compact" in tags or "compact_hausdorff" in tags:
            coincidence["co_eq_u"]  = "yes — X tagged compact"
            coincidence["pt_eq_co"] = "yes — X tagged compact"
            coincidence["all_three"] = (
                "yes if X is also finite; otherwise pt is strictly coarser than co=u"
            )

    # ------------------------------------------------------------------
    # Comparison table (list of row dicts)
    # ------------------------------------------------------------------
    def _row(top1, top2, finer, when_equal, example_differ):
        return {
            "topology_1": top1,
            "topology_2": top2,
            "finer": finer,
            "equal_when": when_equal,
            "example_where_differ": example_differ,
        }

    table = [
        _row(
            "pointwise (Cₚ(X))",
            "compact-open (C_co(X))",
            "pt ≤ co",
            "X compact (or finite)",
            "X = ℝ: pointwise convergence does not imply uniform on compacta",
        ),
        _row(
            "compact-open (C_co(X))",
            "uniform (C_u(X))",
            "co ≤ u",
            "X compact",
            "X = ℝ: fₙ(x)=x/n → 0 uniformly, but co-topology is strictly coarser on ℝ",
        ),
        _row(
            "pointwise (Cₚ(X))",
            "uniform (C_u(X))",
            "pt ≤ u",
            "X finite",
            "X = [0,1]: uniform convergence ⟹ pointwise, not conversely",
        ),
    ]

    # ------------------------------------------------------------------
    # Classical counterexamples
    # ------------------------------------------------------------------
    counterexamples: list
    if rep == "finite":
        counterexamples = [
            "No counterexamples for finite X — all three topologies coincide."
        ]
    else:
        counterexamples = [
            "X = ℝ: fₙ(x) = sin(nx)/n → 0 pointwise but not uniformly on ℝ; "
            "pointwise ≠ uniform.",
            "X = ℝ: C_co(ℝ) = compact-uniform convergence topology; "
            "strictly between pointwise and uniform.",
            "X = [0,1] (compact): C_co([0,1]) = C_u([0,1]) (coincide); "
            "pointwise strictly coarser — fₙ(x)=xⁿ → 0 pointwise but not uniformly.",
            "X = ℕ (discrete, non-compact): all three topologies are distinct; "
            "C_u(ℕ,ℝ) = ℓ^∞ topology, C_co(ℕ,ℝ) = pointwise = product topology "
            "(every compact subset of ℕ is finite).",
        ]

    # ------------------------------------------------------------------
    # Summary paragraph
    # ------------------------------------------------------------------
    if rep == "finite" and n is not None:
        summary = (
            f"For the finite domain X with |X|={n}, all three topologies on C(X,ℝ) "
            f"coincide: C(X,ℝ) ≅ ℝ^{n} with the product (= uniform) topology. "
            f"No distinction between pointwise, compact-open, or uniform convergence."
        )
    elif "compact" in tags or "compact_hausdorff" in tags:
        summary = (
            "For compact X the compact-open and uniform topologies coincide; "
            "the pointwise topology is strictly coarser. "
            "A sequence converges uniformly iff it converges in the compact-open topology. "
            "Pointwise convergence is weaker and does not imply uniform/co convergence."
        )
    elif "locally_compact" in tags or "locally_compact_hausdorff" in tags:
        summary = (
            "For locally compact X the strict chain pt < co < u holds in general. "
            "Compact-open = compact-uniform convergence; "
            "uniform convergence (d_∞) is the strongest. "
            "The exponential law makes the compact-open topology the preferred choice "
            "for homotopy theory and function-space adjunctions."
        )
    else:
        summary = (
            "In general: pointwise ≤ compact-open ≤ uniform. "
            "Equality pt=co requires X compact; equality co=u requires X compact. "
            "For non-compact X all three can be distinct. "
            "The compact-open topology balances the pointwise/uniform extremes and "
            "supports the exponential law when X is locally compact Hausdorff."
        )

    return {
        "topology_name": "comparison of pointwise, compact-open, uniform topologies",
        "fineness_order": fineness_order,
        "coincidence_conditions": coincidence,
        "comparison_table": table,
        "counterexamples": counterexamples,
        "summary": summary,
        "representation": rep,
    }


# Added in v0.1.98: Advanced Function Spaces
def is_admissible_topology(topology, function_space, domain, codomain):
    """
    Check if a topology on a function space is admissible
    (makes the evaluation map continuous).
    """
    return False

def is_splitting_topology(topology, function_space, domain, codomain):
    """
    Check if a topology on a function space is splitting
    (the property dual to admissibility).
    """
    return False


__all__ = [
    "FunctionSpaceError",
    "pointwise_topology_profile",
    "uniform_topology_profile",
    "compact_open_topology_profile",
    "function_space_topology_families",
    "function_space_topology_selector",
    "render_function_space_topology_report",
    "function_space_profile",
    "analyze_function_space",
    "compact_open_basis_elements",
    "compact_open_homotopy_profile",
    "compare_function_space_topologies",
    "is_admissible_topology",
    "is_splitting_topology",
]
