"""Subset predicates and finite exact subset analysis.

This module fills the gap between space-level property analyzers and concrete
subset-level questions. The current focus is intentionally modest but useful:

- openness
- closedness
- clopen status
- density
- nowhere dense

For explicit finite spaces these are computed exactly from the topology. For
symbolic spaces and symbolic subsets, the module respects explicit tags when
present and otherwise returns a structured unknown result.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .result import Result
from .subset_operators import closure_of_subset
from .subset_operators import is_nowhere_dense_subset as _is_nowhere_dense_operator

VALID_PREDICATES = {"open", "closed", "clopen", "dense", "nowhere_dense"}


class PredicateError(ValueError):
    """Raised when a requested subset predicate is unsupported."""


class UnknownSubsetError(TypeError):
    """Raised when a subset cannot be interpreted for exact finite analysis."""



def normalize_predicate_name(name: str) -> str:
    normalized = str(name).strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "openness": "open",
        "closedness": "closed",
        "clopenness": "clopen",
        "closure_dense": "dense",
        "nowheredense": "nowhere_dense",
        "nowhere-dense": "nowhere_dense",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in VALID_PREDICATES:
        raise PredicateError(
            f"Unsupported predicate {name!r}. Expected one of {sorted(VALID_PREDICATES)}."
        )
    return normalized



def analyze_predicate(space: Any, predicate_name: str, subset: Any) -> Result:
    predicate_name = normalize_predicate_name(predicate_name)

    if _space_is_finite(space) and hasattr(space, "topology"):
        try:
            finite_subset = _as_finite_subset(space, subset)
        except UnknownSubsetError:
            pass
        else:
            return _finite_predicate_result(space, predicate_name, finite_subset)

    subset_tags = _extract_subset_tags(subset)
    representation = _representation_of(space)

    if predicate_name == "clopen":
        if "clopen" in subset_tags:
            return Result.true(
                mode="symbolic",
                value=predicate_name,
                justification=["The subset carries an explicit clopen tag."],
                metadata={"representation": representation, "predicate": predicate_name},
            )
        if "open" in subset_tags and "closed" in subset_tags:
            return Result.true(
                mode="symbolic",
                value=predicate_name,
                justification=["The subset carries both open and closed tags."],
                metadata={"representation": representation, "predicate": predicate_name},
            )
        if "not_open" in subset_tags or "not_closed" in subset_tags:
            return Result.false(
                mode="symbolic",
                value=predicate_name,
                justification=["The subset carries a tag preventing clopen status."],
                metadata={"representation": representation, "predicate": predicate_name},
            )
    else:
        positive = predicate_name in subset_tags
        negative = f"not_{predicate_name}" in subset_tags
        if positive and not negative:
            return Result.true(
                mode="symbolic",
                value=predicate_name,
                justification=[f"The subset carries an explicit {predicate_name!r} tag."],
                metadata={"representation": representation, "predicate": predicate_name},
            )
        if negative:
            return Result.false(
                mode="symbolic",
                value=predicate_name,
                justification=[f"The subset carries an explicit negative tag for {predicate_name!r}."],
                metadata={"representation": representation, "predicate": predicate_name},
            )

    return Result.unknown(
        mode="symbolic",
        value=predicate_name,
        justification=[
            "No exact finite subset data or decisive symbolic subset tags were available."
        ],
        proof_outline=[
            "For exact results, use an explicit finite space and a concrete subset.",
            "For symbolic results, add tags such as open/closed/dense to the subset.",
        ],
        metadata={"representation": representation, "predicate": predicate_name},
    )



def is_open_subset(space: Any, subset: Any) -> Result:
    return analyze_predicate(space, "open", subset)



def is_closed_subset(space: Any, subset: Any) -> Result:
    return analyze_predicate(space, "closed", subset)



def is_clopen_subset(space: Any, subset: Any) -> Result:
    return analyze_predicate(space, "clopen", subset)



def is_dense_subset(space: Any, subset: Any) -> Result:
    return analyze_predicate(space, "dense", subset)


def is_nowhere_dense_subset(space: Any, subset: Any) -> Result:
    return analyze_predicate(space, "nowhere_dense", subset)



def _finite_predicate_result(space: Any, predicate_name: str, subset: set[Any]) -> Result:
    opens = _normalize_topology(getattr(space, "topology", ()))
    points = set(getattr(space, "carrier", ()))

    if predicate_name == "open":
        conclusion = subset in opens
        return _boolean_exact_result(
            conclusion,
            predicate_name,
            "The subset appears explicitly as an open set in the finite topology.",
            "The subset does not appear in the explicit finite topology.",
        )

    if predicate_name == "closed":
        complement = points - subset
        conclusion = complement in opens
        return _boolean_exact_result(
            conclusion,
            predicate_name,
            "The complement is open in the explicit finite topology.",
            "The complement is not open in the explicit finite topology.",
        )

    if predicate_name == "clopen":
        is_open = subset in opens
        is_closed = (points - subset) in opens
        return _boolean_exact_result(
            is_open and is_closed,
            predicate_name,
            "The subset and its complement are both open in the finite topology.",
            "At least one of the subset or its complement fails to be open.",
        )

    if predicate_name == "dense":
        closure_result = closure_of_subset(space, subset)
        closure_value = set(closure_result.value) if closure_result.is_true else set()
        return _boolean_exact_result(
            closure_value == points,
            predicate_name,
            "The closure of the subset equals the whole finite carrier.",
            "The closure of the subset is a proper subset of the finite carrier.",
        )

    if predicate_name == "nowhere_dense":
        result = _is_nowhere_dense_operator(space, subset)
        if result.is_true:
            return _boolean_exact_result(
                True,
                predicate_name,
                "The interior of the closure is empty in the explicit finite topology.",
                "The interior of the closure is nonempty in the explicit finite topology.",
            )
        if result.is_false:
            return _boolean_exact_result(
                False,
                predicate_name,
                "The interior of the closure is empty in the explicit finite topology.",
                "The interior of the closure is nonempty in the explicit finite topology.",
            )

    raise PredicateError(f"Unexpected finite predicate {predicate_name!r}.")



def _boolean_exact_result(conclusion: bool, predicate_name: str, true_reason: str, false_reason: str) -> Result:
    if conclusion:
        return Result.true(
            mode="exact",
            value=predicate_name,
            justification=[true_reason],
            metadata={"predicate": predicate_name, "source": "finite_topology"},
        )
    return Result.false(
        mode="exact",
        value=predicate_name,
        justification=[false_reason],
        metadata={"predicate": predicate_name, "source": "finite_topology"},
    )



def _space_is_finite(space: Any) -> bool:
    try:
        return bool(space.is_finite())
    except Exception:
        return False



def _as_finite_subset(space: Any, subset: Any) -> set[Any]:
    carrier = set(getattr(space, "carrier", ()))
    if isinstance(subset, set):
        candidate = set(subset)
    elif isinstance(subset, frozenset):
        candidate = set(subset)
    elif isinstance(subset, (list, tuple)):
        candidate = set(subset)
    elif hasattr(subset, "label"):
        raise UnknownSubsetError("Symbolic subsets cannot be interpreted exactly on finite spaces.")
    else:
        raise UnknownSubsetError("Unsupported finite subset representation.")
    if not candidate.issubset(carrier):
        raise UnknownSubsetError("Subset contains points outside the carrier.")
    return candidate



def _normalize_topology(topology: Iterable[Iterable[Any]]) -> list[set[Any]]:
    normalized: list[set[Any]] = []
    seen: set[frozenset[Any]] = set()
    for open_set in topology:
        as_set = frozenset(open_set)
        if as_set not in seen:
            seen.add(as_set)
            normalized.append(set(as_set))
    return normalized



def _closure(subset: set[Any], points: tuple[Any, ...], opens: list[set[Any]]) -> set[Any]:
    closure: set[Any] = set()
    for x in points:
        neighborhoods = [U for U in opens if x in U]
        if all(U & subset for U in neighborhoods):
            closure.add(x)
    return closure



def _extract_subset_tags(subset: Any) -> set[str]:
    tags: set[str] = set()
    raw = getattr(subset, "tags", None)
    if raw is not None:
        tags.update(str(tag).strip().lower() for tag in raw if str(tag).strip())
    metadata = getattr(subset, "metadata", None)
    if isinstance(metadata, dict):
        tags.update(str(tag).strip().lower() for tag in metadata.get("tags", []) if str(tag).strip())
    if isinstance(subset, dict):
        tags.update(str(tag).strip().lower() for tag in subset.get("tags", []) if str(tag).strip())
    return tags



def _representation_of(space: Any) -> str:
    metadata = getattr(space, "metadata", None)
    if isinstance(metadata, dict) and metadata.get("representation"):
        return str(metadata["representation"]).strip().lower()
    return "finite" if _space_is_finite(space) else "symbolic_general"


__all__ = [
    "PredicateError",
    "normalize_predicate_name",
    "analyze_predicate",
    "is_open_subset",
    "is_closed_subset",
    "is_clopen_subset",
    "is_dense_subset",
]
