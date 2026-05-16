"""cardinal_functions_framework.py — Cilt IV kardinal fonksiyon çerçevesi (v0.1.70)

Roadmap direktifi: "The framework should separate definition, comparison, and examples."

Bu modül üç katmanlı çerçeve sağlar:
  1. TANIM katmanı  — her kardinal fonksiyonun matematiksel tanımı
  2. KARŞILAŞTIRMA katmanı — fonksiyonlar arası eşitsizlikler ve implication zinciri
  3. ÖRNEK katmanı — her fonksiyon için canonical hesaplanmış örnekler

Sağlanan API:
    CardinalFunctionFrameworkError
    cardinal_function_definition(name) -> Dict       # TANIM
    cardinal_function_comparison(name1, name2) -> Dict  # KARŞILAŞTIRMA
    cardinal_functions_framework_profile(space) -> Dict  # 3 KATMAN BÜTÜNÜ
    analyze_cardinal_functions_framework(space) -> Result
"""

from __future__ import annotations

from typing import Any, Optional

from .result import Result

__all__ = [
    "CardinalFunctionFrameworkError",
    "cardinal_function_definition",
    "cardinal_function_comparison",
    "cardinal_functions_framework_profile",
    "analyze_cardinal_functions_framework",
]

VERSION = "0.1.70"


class CardinalFunctionFrameworkError(ValueError):
    """Raised when an unsupported cardinal function is requested."""


# ═══════════════════════════════════════════════════════════════
# TANIM KATMANI
# ═══════════════════════════════════════════════════════════════

_DEFINITIONS: dict[str, dict] = {
    "weight": {
        "symbol": "w(X)",
        "definition": (
            "w(X) = min{|B| : B is a base for X}. "
            "The weight is the minimum cardinality of a base (open cover closed under "
            "finite intersections generating the topology). "
            "w(X) = aleph_0 iff X is second-countable."
        ),
        "type": "global",
        "introduced_by": "Alexandroff–Urysohn (1929)",
        "key_threshold": "aleph_0: second-countable",
        "computation": "Search over all bases; take minimum cardinality.",
        "finite_case": "w(X) <= |topology| for finite X; exact by enumeration.",
    },
    "density": {
        "symbol": "d(X)",
        "definition": (
            "d(X) = min{|D| : D is dense in X} (for infinite X; d(X) = |X| for finite X). "
            "A set D is dense iff every nonempty open set meets D. "
            "d(X) = aleph_0 iff X is separable."
        ),
        "type": "global",
        "introduced_by": "Alexandroff (1926)",
        "key_threshold": "aleph_0: separable",
        "computation": "Search over subsets D; test closure(D) = X.",
        "finite_case": "d(X) <= |carrier| for finite X; often < |carrier|.",
    },
    "character": {
        "symbol": "chi(X)",
        "definition": (
            "chi(X) = sup_{x in X} chi(x,X), where chi(x,X) = min{|B_x| : B_x is a local base at x}. "
            "chi(X) = aleph_0 iff X is first-countable. "
            "Character is a local invariant; weight is global: chi(X) <= w(X)."
        ),
        "type": "local-then-global (sup)",
        "introduced_by": "Alexandroff–Urysohn (1929)",
        "key_threshold": "aleph_0: first-countable",
        "computation": "At each point, find minimum local base; then take sup.",
        "finite_case": "chi(X) <= |topology| for finite X.",
    },
    "lindelof_number": {
        "symbol": "L(X)",
        "definition": (
            "L(X) = min{kappa : every open cover has a subcover of size <= kappa}. "
            "L(X) = aleph_0 iff X is Lindelof (every open cover has a countable subcover). "
            "For compact X, L(X) = aleph_0. For second-countable X, L(X) = aleph_0."
        ),
        "type": "global (covering)",
        "introduced_by": "Alexandroff–Urysohn (1929)",
        "key_threshold": "aleph_0: Lindelof",
        "computation": "For each open cover, find minimum subcover; supremum over all covers.",
        "finite_case": "L(X) = aleph_0 trivially (every cover has finite, hence countable subcover).",
    },
    "cellularity": {
        "symbol": "c(X)",
        "definition": (
            "c(X) = sup{|U| : U is a family of pairwise disjoint nonempty open sets}. "
            "c(X) = aleph_0 is the countable chain condition (ccc). "
            "Separable => ccc (c(X) <= aleph_0). Conversely, ccc does NOT imply separable in general."
        ),
        "type": "global (disjointness)",
        "introduced_by": "Suslin (1920, as hypothesis); Knaster–Kuratowski–Mazurkiewicz",
        "key_threshold": "aleph_0: ccc (countable chain condition)",
        "computation": "Find maximum antichain of disjoint open sets.",
        "finite_case": "c(X) <= |topology| for finite X.",
    },
    "spread": {
        "symbol": "s(X)",
        "definition": (
            "s(X) = sup{|D| : D is a discrete subspace of X}. "
            "A subspace D is discrete iff every point of D is open in D. "
            "s(X) <= d(X): separable spaces have countable spread."
        ),
        "type": "global (subspace)",
        "introduced_by": "Hodel (1984, survey standardization)",
        "key_threshold": "aleph_0: countable spread (hereditarily separable implies s(X) = aleph_0)",
        "computation": "Find supremum of sizes of discrete subspaces.",
        "finite_case": "s(X) <= |carrier| for finite X.",
    },
    "network_weight": {
        "symbol": "nw(X)",
        "definition": (
            "nw(X) = min{|N| : N is a network for X}. "
            "A network is a family N of sets (not necessarily open) such that for each "
            "x in U open, some N in the network satisfies x in N ⊆ U. "
            "nw(X) <= w(X) always; in compact Hausdorff spaces nw(X) = w(X)."
        ),
        "type": "global",
        "introduced_by": "Arhangelskii (1959)",
        "key_threshold": "aleph_0: countable network (implies separable in T1 spaces)",
        "computation": "Find minimum network; every base is a network.",
        "finite_case": "nw(X) <= |topology| <= w(X) for finite X.",
    },
    "tightness": {
        "symbol": "t(X)",
        "definition": (
            "t(X) = sup_{x,A} min{|B| : B ⊆ A, x in closure(B)}, "
            "where the sup is over all x in X and A ⊆ X with x in closure(A). "
            "t(X) = aleph_0 iff X has countable tightness: x in cl(A) implies "
            "x in cl(B) for some countable B ⊆ A. "
            "First-countable => t(X) <= aleph_0. Sequential => t(X) <= aleph_0."
        ),
        "type": "local-then-global (sup)",
        "introduced_by": "Arhangelskii (1969)",
        "key_threshold": "aleph_0: countable tightness",
        "computation": "For each pair (x,A) with x in cl(A), find minimum witness B; then sup.",
        "finite_case": "t(X) = 0 (finite spaces trivially have countable tightness).",
    },
}

_FUNCTION_NAMES = list(_DEFINITIONS.keys())


# ═══════════════════════════════════════════════════════════════
# KARŞILAŞTIRMA KATMANI
# ═══════════════════════════════════════════════════════════════

_COMPARISONS: dict[frozenset, dict] = {
    frozenset({"weight", "density"}): {
        "inequality": "d(X) <= w(X)",
        "direction": "density <= weight",
        "proof_idea": (
            "Given a base B, pick one point from each B in B to form a dense set D. "
            "Then |D| <= |B|, so d(X) <= w(X)."
        ),
        "equality_condition": "Equality d(X) = w(X) holds in many spaces (e.g. metrizable separable). "
                              "Inequality is strict for: e.g. one-point compactification of uncountable discrete space.",
        "examples": ["R: d=w=aleph_0", "Cantor set: d=w=aleph_0", "beta(N): d=aleph_0, w=2^aleph_0"],
    },
    frozenset({"weight", "character"}): {
        "inequality": "chi(X) <= w(X)",
        "direction": "character <= weight",
        "proof_idea": (
            "A base B is a local base at every point. So chi(x,X) <= w(X) for each x."
        ),
        "equality_condition": "chi(X) = w(X) for metrizable spaces. "
                              "Strict inequality for: locally compact spaces where weight > character.",
        "examples": ["R: chi=w=aleph_0", "Sorgenfrey: chi=aleph_0, w=aleph_1"],
    },
    frozenset({"weight", "network_weight"}): {
        "inequality": "nw(X) <= w(X)",
        "direction": "network_weight <= weight",
        "proof_idea": "Every base is a network; so minimum network is at most minimum base.",
        "equality_condition": "nw(X) = w(X) for compact Hausdorff spaces.",
        "examples": ["R: nw=w=aleph_0", "compact Hausdorff X: nw=w"],
    },
    frozenset({"density", "cellularity"}): {
        "inequality": "c(X) <= d(X)",
        "direction": "cellularity <= density (separable => ccc)",
        "proof_idea": (
            "If D is dense and {U_alpha} is a disjoint family of open sets, "
            "each U_alpha contains a point of D. So |{U_alpha}| <= |D|."
        ),
        "equality_condition": "Equality c(X) = d(X) fails: Suslin line (ccc but not separable under CH).",
        "examples": ["R: c=d=aleph_0", "Suslin line (hypothetical): c=aleph_0, d=aleph_1"],
    },
    frozenset({"density", "spread"}): {
        "inequality": "s(X) <= d(X)",
        "direction": "spread <= density",
        "proof_idea": (
            "A discrete subspace D has |D| <= d(X): each point of D can be separated "
            "by an open set, and a dense set must meet each."
        ),
        "equality_condition": "Equality holds in many spaces. Hereditarily separable <=> s(X) = aleph_0.",
        "examples": ["R: s=d=aleph_0", "Niemytzki plane: s=aleph_1, d=aleph_0"],
    },
    frozenset({"character", "tightness"}): {
        "inequality": "t(X) <= chi(X)",
        "direction": "tightness <= character",
        "proof_idea": (
            "If chi(x,X) <= kappa, a local base of size kappa can witness any closure relation. "
            "Hence t(X) <= chi(X)."
        ),
        "equality_condition": "t(X) < chi(X) possible: some compact spaces have t(X)=aleph_0, chi(X)=aleph_1.",
        "examples": ["R: t=chi=aleph_0", "compact F-spaces: t(X) may be < chi(X)"],
    },
    frozenset({"character", "lindelof_number"}): {
        "inequality": "L(X) <= 2^{chi(X)}",
        "direction": "Lindelof number bounded by 2^character",
        "proof_idea": (
            "By Arhangelskii's method: for each open cover, local base at each point of size chi(X) "
            "yields at most 2^{chi(X)} many relevant open sets to choose from."
        ),
        "equality_condition": "Tight for some spaces; equality L = 2^chi occurs in certain scattered spaces.",
        "examples": ["R: L=chi=aleph_0, 2^chi=2^aleph_0 (inequality is strict)"],
    },
    frozenset({"weight", "density_power"}): {
        "inequality": "w(X) <= 2^{d(X)}",
        "direction": "weight bounded by 2^density",
        "proof_idea": (
            "A separating base can be reconstructed from density witnesses: "
            "at most 2^{d(X)} many unions of dense-set traces."
        ),
        "equality_condition": "In compact spaces w(X) = 2^{d(X)} is common.",
        "examples": ["[0,1]: d=aleph_0, w=aleph_0, 2^d=2^aleph_0 (bound not tight)"],
    },
}


def _comparison_key(name1: str, name2: str) -> frozenset:
    return frozenset({name1, name2})


# ═══════════════════════════════════════════════════════════════
# ÖRNEK KATMANI
# ═══════════════════════════════════════════════════════════════

_FRAMEWORK_EXAMPLES = [
    "R (real line): w=d=chi=L=c=s=nw=t = aleph_0. All eight functions coincide at the countable threshold.",
    "Sorgenfrey line: w=aleph_1, d=chi=L=t=s=aleph_0. Weight jumps; others stay countable.",
    "Cantor set (2^omega): w=d=chi=L=c=s=nw=t = aleph_0. Compact metrizable model.",
    "Ordinal space omega_1: w=chi=c=aleph_1, d=L uncountable. Not Lindelof, not separable.",
    "Michael line: d=aleph_0, L=aleph_1. Separable but not Lindelof (Sorgenfrey variant).",
    "Niemytzki (Moore) plane: d=aleph_0, s=aleph_1. Separable but not hereditarily separable.",
    "Discrete space kappa: w=d=c=s=L=kappa, chi=nw=1, t=0.",
    "beta(N) (Stone-Cech): d=aleph_0, w=2^aleph_0, nw=aleph_0 (only metrizable fibers). Shows d << w.",
    "Finite space on n points: all eight invariants finite (bounded by n and |topology|).",
    "Compact Hausdorff X: nw(X) = w(X). Weight and network weight coincide.",
]

_FRAMEWORK_PRINCIPLES = [
    "TANIM ilkesi: Her kardinal fonksiyon minimum bir kardinal olarak tanımlanır (weight, density, character, nw, t) veya supremum olarak (cellularity, spread, L).",
    "KARŞILAŞTIRMA ilkesi: nw <= w, d <= w, chi <= w, c <= d, s <= d, t <= chi zinciri — hiyerarşi alttan üste doğru okunur.",
    "ÖRNEK ilkesi: Her eşitsizlik için (a) eşitlik örneği ve (b) kesin eşitsizlik örneği gösterilmelidir.",
    "DEĞİŞMEZLİK ilkesi: Her kardinal fonksiyon homeomorfizma değişmezidir — tanım homeomorfizmadan bağımsızdır.",
    "EŞİK ilkesi: Her fonksiyon için aleph_0 eşiği bir nitel özelliğe karşılık gelir: w=aleph_0 <=> 2nd countable, d=aleph_0 <=> separable, vb.",
]


# ═══════════════════════════════════════════════════════════════
# İÇ YARDIMCILAR
# ═══════════════════════════════════════════════════════════════

def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", {}) or {}
    rep = metadata.get("representation", None)
    if rep:
        return str(rep).strip().lower()
    if hasattr(space, "carrier") and hasattr(space, "topology"):
        return "finite"
    return "symbolic_general"


def _tags_of(space: Any) -> set:
    tags: set = set()
    metadata = getattr(space, "metadata", {}) or {}
    for t in metadata.get("tags", []):
        tags.add(str(t).strip().lower())
    for t in getattr(space, "tags", set()):
        tags.add(str(t).strip().lower())
    return tags


def _carrier_size(space: Any) -> Optional[int]:
    carrier = getattr(space, "carrier", None)
    if carrier is not None:
        try:
            return len(carrier)
        except TypeError:
            pass
    return None


# ═══════════════════════════════════════════════════════════════
# ANA API — TANIM
# ═══════════════════════════════════════════════════════════════

def cardinal_function_definition(name: str) -> dict:
    """Verilen kardinal fonksiyonun tanım kaydını döndür.

    Args:
        name: 'weight', 'density', 'character', 'lindelof_number',
              'cellularity', 'spread', 'network_weight', 'tightness'

    Returns:
        Dict with keys: symbol, definition, type, introduced_by,
        key_threshold, computation, finite_case
    """
    key = name.strip().lower().replace(" ", "_").replace("-", "_")
    # aliases
    aliases = {
        "w": "weight", "d": "density", "chi": "character",
        "l": "lindelof_number", "lindelof": "lindelof_number",
        "c": "cellularity", "ccc": "cellularity",
        "s": "spread", "nw": "network_weight",
        "t": "tightness",
    }
    key = aliases.get(key, key)
    if key not in _DEFINITIONS:
        raise CardinalFunctionFrameworkError(
            f"Unknown cardinal function {name!r}. "
            f"Supported: {sorted(_DEFINITIONS.keys())}"
        )
    return dict(_DEFINITIONS[key])


# ═══════════════════════════════════════════════════════════════
# ANA API — KARŞILAŞTIRMA
# ═══════════════════════════════════════════════════════════════

def cardinal_function_comparison(name1: str, name2: str) -> dict:
    """İki kardinal fonksiyon arasındaki karşılaştırma kaydını döndür.

    Returns:
        Dict with keys: inequality, direction, proof_idea,
        equality_condition, examples
    """
    def _norm(n: str) -> str:
        n = n.strip().lower().replace(" ", "_")
        aliases = {
            "w": "weight", "d": "density", "chi": "character",
            "l": "lindelof_number", "lindelof": "lindelof_number",
            "c": "cellularity", "s": "spread",
            "nw": "network_weight", "t": "tightness",
        }
        return aliases.get(n, n)

    k = frozenset({_norm(name1), _norm(name2)})
    if k in _COMPARISONS:
        return dict(_COMPARISONS[k])
    # fallback: check with density_power
    alt_k = frozenset({_norm(name1), "density_power"})
    if alt_k in _COMPARISONS:
        return dict(_COMPARISONS[alt_k])
    raise CardinalFunctionFrameworkError(
        f"No comparison record for ({name1!r}, {name2!r}). "
        f"Available pairs: weight/density, weight/character, weight/network_weight, "
        f"density/cellularity, density/spread, character/tightness, character/lindelof_number."
    )


# ═══════════════════════════════════════════════════════════════
# ANA API — ÇERÇEVE PROFİLİ
# ═══════════════════════════════════════════════════════════════

def cardinal_functions_framework_profile(space: Any) -> dict:
    """3 katmanlı kardinal fonksiyon çerçeve profilini döndür.

    Anahtarlar:
        definition_layer   — 8 fonksiyonun tanım kayıtları
        comparison_layer   — 7 karşılaştırma kaydı (eşitsizlikler)
        example_layer      — 10 canonical örnek
        framework_principles — 5 çerçeve ilkesi
        representation     — uzay temsili
        space_tags         — etiketler (theorem modu için)
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    return {
        "definition_layer": {
            name: _DEFINITIONS[name] for name in _FUNCTION_NAMES
        },
        "comparison_layer": {
            rec["inequality"]: rec
            for rec in _COMPARISONS.values()
        },
        "example_layer": list(_FRAMEWORK_EXAMPLES),
        "framework_principles": list(_FRAMEWORK_PRINCIPLES),
        "representation": rep,
        "space_tags": sorted(tags),
    }


def analyze_cardinal_functions_framework(space: Any) -> Result:
    """Kardinal fonksiyon çerçevesini Result nesnesi olarak döndür.

    Mod kararı:
        "exact"    — FiniteTopologicalSpace
        "theorem"  — etiket tabanlı sembolik uzay
        "symbolic" — bilinmeyen uzay
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)
    profile = cardinal_functions_framework_profile(space)

    if rep == "finite":
        mode = "exact"
        justification = [
            f"Finite space (n={n}). All 8 cardinal functions are finite and bounded by |topology| or |carrier|.",
            "Definition layer: all 8 functions defined. Comparison layer: all 7 inequalities trivially finite.",
            "Example layer: finite space is the canonical 'all equal' example.",
        ]
    elif tags:
        mode = "theorem"
        justification = [
            f"Tag-identified space ({sorted(tags)}). Framework applied via standard implications.",
            "Definition layer: theoretical. Comparison layer: inequalities govern threshold behavior.",
            "Key: each tag (second_countable, separable, etc.) pins a subset of the 8 functions to aleph_0.",
        ]
    else:
        mode = "symbolic"
        justification = [
            "Unknown space. Cardinal function framework presented in full generality.",
            "Provide metadata['tags'] or use FiniteTopologicalSpace for concrete values.",
        ]

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": VERSION,
            "domain_representation": rep,
            "carrier_size": n,
            "functions_defined": len(_FUNCTION_NAMES),
            "comparisons_recorded": len(_COMPARISONS),
            "examples_count": len(_FRAMEWORK_EXAMPLES),
        },
    )
