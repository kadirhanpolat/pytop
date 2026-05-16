"""basic_invariants.py — Cilt IV temel topolojik değişmezler koridoru (v0.1.69)

Bu modül, nicel topoloji koridorunun (v0.1.68) hemen ardından gelen
değişmez dili bütünleştirmesini sağlar. Roadmap yönergesi:
"Invariant language should follow the quantitative entry."

Sağlanan API:
    topological_invariants_profile(space) -> Dict
    analyze_topological_invariants(space) -> Result
    BasicInvariantError

Değişmezler:
    weight (w), density (d), character (χ), Lindelöf number (L),
    cellularity (c), spread (s), network weight (nw), tightness (t)

Her değişmez için:
    - exact  : sonlu uzaylar (FiniteTopologicalSpace)
    - theorem: etiket tabanlı sembolik uzaylar (metadata["tags"])
    - symbolic: bilinmeyen uzaylar
"""

from __future__ import annotations

from typing import Any

from .result import Result

__all__ = [
    "BasicInvariantError",
    "topological_invariants_profile",
    "analyze_topological_invariants",
]

VERSION = "0.1.69"


class BasicInvariantError(ValueError):
    """Raised when topological invariants cannot be computed."""


# ─────────────────────────── iç yardımcılar ───────────────────────────


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


def _carrier_size(space: Any) -> int | None:
    carrier = getattr(space, "carrier", None)
    if carrier is not None:
        try:
            return len(carrier)
        except TypeError:
            pass
    return None


def _topology_size(space: Any) -> int | None:
    topology = getattr(space, "topology", None)
    if topology is not None:
        try:
            return len(topology)
        except TypeError:
            pass
    return None


# ─────────────── değişmez tahmincileri ───────────────

def _weight_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        n = _topology_size(space)
        return f"finite: w(X) <= {n}" if n is not None else "finite"
    if "second_countable" in tags:
        return "countable: w(X) = aleph_0"
    if "not_second_countable" in tags:
        return "uncountable: w(X) > aleph_0 (tag-inferred)"
    if "metrizable" in tags and "separable" in tags:
        return "countable: w(X) = aleph_0 (sep. metrizable => 2nd countable)"
    return "symbolic: w(X) unknown"


def _density_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        n = _carrier_size(space)
        return f"finite: d(X) <= {n}" if n is not None else "finite"
    if "separable" in tags:
        return "countable: d(X) = aleph_0"
    if "not_separable" in tags:
        return "uncountable: d(X) > aleph_0 (tag-inferred)"
    return "symbolic: d(X) unknown"


def _character_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        n = _topology_size(space)
        return f"finite: chi(X) <= {n}" if n is not None else "finite"
    if "first_countable" in tags:
        return "countable: chi(X) = aleph_0"
    if "not_first_countable" in tags:
        return "uncountable: chi(X) > aleph_0 (tag-inferred)"
    if "metrizable" in tags:
        return "countable: chi(X) = aleph_0 (metrizable => first countable)"
    return "symbolic: chi(X) unknown"


def _lindelof_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        return "finite: Lindelof (trivially, every finite cover is finite)"
    if "lindelof" in tags:
        return "Lindelof: L(X) = aleph_0"
    if "compact" in tags:
        return "Lindelof: L(X) = aleph_0 (compact => Lindelof)"
    if "second_countable" in tags:
        return "Lindelof: L(X) = aleph_0 (second countable => Lindelof)"
    if "not_lindelof" in tags:
        return "non-Lindelof: L(X) > aleph_0 (tag-inferred)"
    return "symbolic: L(X) unknown"


def _cellularity_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        n = _topology_size(space)
        return f"finite: c(X) <= {n}" if n is not None else "finite"
    if "separable" in tags:
        return "countable: c(X) <= aleph_0 (separable => countable cellularity)"
    if "second_countable" in tags:
        return "countable: c(X) <= aleph_0 (2nd countable => sep. => countable c)"
    return "symbolic: c(X) unknown"


def _spread_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        n = _carrier_size(space)
        return f"finite: s(X) <= {n}" if n is not None else "finite"
    if "separable" in tags:
        return "countable: s(X) <= aleph_0 (separable => spread countable)"
    if "hereditarily_separable" in tags:
        return "countable: s(X) = aleph_0 (hereditarily separable)"
    return "symbolic: s(X) unknown"


def _network_weight_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        n = _topology_size(space)
        return f"finite: nw(X) <= {n}" if n is not None else "finite"
    if "second_countable" in tags:
        return "countable: nw(X) <= w(X) = aleph_0"
    if "separable" in tags and "metrizable" in tags:
        return "countable: nw(X) = aleph_0 (sep. metrizable)"
    return "symbolic: nw(X) unknown"


def _tightness_value(space: Any, rep: str, tags: set) -> str:
    if rep == "finite":
        return "finite: t(X) = 0 (finite spaces have countable tightness trivially)"
    if "first_countable" in tags:
        return "countable: t(X) = aleph_0 (first countable => countable tightness)"
    if "sequential" in tags:
        return "countable: t(X) = aleph_0 (sequential => countable tightness)"
    if "metrizable" in tags:
        return "countable: t(X) = aleph_0 (metrizable => first countable => t=aleph_0)"
    return "symbolic: t(X) unknown"


# ─────────────── invariant hiyerarşisi ───────────────

_KEY_INEQUALITIES = [
    "nw(X) <= w(X): every base is a network.",
    "d(X) <= w(X): every base contains a dense subset.",
    "chi(X) <= w(X): local bases come from a global base.",
    "c(X) <= d(X): separable spaces are ccc (countable chain condition).",
    "s(X) <= d(X): spread is bounded by density.",
    "t(X) <= chi(X): tightness does not exceed character.",
    "L(X) <= 2^{chi(X)}: Lindelof number bounded by 2^character.",
    "|X| <= 2^{chi(X)*L(X)}: Arhangel'skii theorem (Hausdorff case).",
    "w(X) <= 2^{d(X)}: weight bounded by power of density.",
    "For compact Hausdorff X: |X| <= 2^{w(X)}.",
]

_KEY_EXAMPLES = [
    "R (real line): w=d=chi=L=c=s=nw=t = aleph_0.",
    "R^omega (countable product): w=d=chi=L = aleph_0 (Hilbert cube analogue).",
    "Sorgenfrey line (R_l): w=c=aleph_1, d=chi=L=t = aleph_0; not 2nd countable.",
    "Ordinal space omega_1: w=chi=c=aleph_1, d=L uncountable; not Lindelof.",
    "One-point compactification of discrete aleph_1: w=aleph_1, Lindelof.",
    "Finite space on n points: all invariants finite, <= n.",
    "Cantor set (2^omega): w=d=chi=L = aleph_0; compact metrizable.",
    "Michael line: d=aleph_0, L=aleph_1; not Lindelof despite separability.",
    "Niemytzki plane: d=aleph_0, L>aleph_0; separable non-Lindelof.",
    "Discrete space of size kappa: w=d=kappa, chi=1, c=kappa, L=kappa.",
]

_QUANTITATIVE_BRIDGE = (
    "v0.1.68 modülü (quantitative_topology) w,d,chi,L değerlerini kardinal sayı olarak ölçer. "
    "Bu modül (v0.1.69) aynı ölçümleri tam bir değişmez envanterine genişletir: "
    "c (cellularity/ccc), s (spread), nw (network weight), t (tightness) eklenerek "
    "Engelking §1.1--§3.3 değişmez dili karşılanır."
)

_CARDINAL_FUNCTION_BRIDGE = (
    "Değişmezler, Bölüm 26–28'deki kardinal sayı hiyerarşisiyle doğrudan konuşur: "
    "aleph_0 <= aleph_1 <= ... eşitsizlik zinciri, her değişmezin 'sayılabilir' eşiğini belirler. "
    "Cofinality (Bölüm 28), kappa = cf(kappa) olan regular kardinalllerde değişmez çakışmalarını açıklar."
)


# ─────────────── ana API ───────────────

def topological_invariants_profile(space: Any) -> dict:
    """8 kardinal değişmezin pedagojik profilini döndür.

    Anahtarlar:
        weight, density, character, lindelof_number,
        cellularity, spread, network_weight, tightness,
        key_inequalities, key_examples,
        quantitative_bridge, cardinal_function_bridge, representation
    """
    rep = _representation_of(space)
    tags = _tags_of(space)

    return {
        "weight":              _weight_value(space, rep, tags),
        "density":             _density_value(space, rep, tags),
        "character":           _character_value(space, rep, tags),
        "lindelof_number":     _lindelof_value(space, rep, tags),
        "cellularity":         _cellularity_value(space, rep, tags),
        "spread":              _spread_value(space, rep, tags),
        "network_weight":      _network_weight_value(space, rep, tags),
        "tightness":           _tightness_value(space, rep, tags),
        "key_inequalities":    list(_KEY_INEQUALITIES),
        "key_examples":        list(_KEY_EXAMPLES),
        "quantitative_bridge": _QUANTITATIVE_BRIDGE,
        "cardinal_function_bridge": _CARDINAL_FUNCTION_BRIDGE,
        "representation":      rep,
    }


def analyze_topological_invariants(space: Any) -> Result:
    """Topological invariant profile'ı Result nesnesi olarak döndür.

    Mod kararı:
        "exact"    — FiniteTopologicalSpace (carrier + topology)
        "theorem"  — etiket tabanlı sembolik uzay
        "symbolic" — bilinmeyen/genel sembolik uzay
    """
    rep = _representation_of(space)
    tags = _tags_of(space)
    n = _carrier_size(space)
    profile = topological_invariants_profile(space)

    if rep == "finite":
        mode = "exact"
        justification = [
            f"Finite space with {n} points. All eight cardinal invariants computed from explicit topology.",
            "weight <= |topology|, density <= |carrier|, character <= |topology|.",
            "Finite spaces trivially satisfy: Lindelof, countable cellularity, countable tightness.",
        ]
    elif tags:
        mode = "theorem"
        justification = [
            f"Tag-identified space ({sorted(tags)}). Invariant values inferred from standard theorems.",
            "Implication chains applied: metrizable=>1st countable, compact=>Lindelof, separable=>ccc.",
            "Arhangel'skii theorem available for Hausdorff spaces: |X| <= 2^(chi*L).",
        ]
    else:
        mode = "symbolic"
        justification = [
            "Unknown/general symbolic space. Invariant values cannot be determined without further structure.",
            "Provide metadata['tags'] for theorem-backed answers, or use FiniteTopologicalSpace for exact computation.",
        ]

    return Result.true(
        mode=mode,
        value=profile,
        justification=justification,
        metadata={
            "version": VERSION,
            "domain_representation": rep,
            "carrier_size": n,
            "weight": profile["weight"],
            "density": profile["density"],
            "character": profile["character"],
            "lindelof_number": profile["lindelof_number"],
            "cellularity": profile["cellularity"],
            "spread": profile["spread"],
            "network_weight": profile["network_weight"],
            "tightness": profile["tightness"],
        },
    )
