"""Uniform-space benchmark helpers.

This v0.1.104 surface replaces the placeholder values with a conservative
boolean API driven by explicit benchmark descriptors, tags, and metadata.
It does not attempt a full symbolic uniformity engine, but it now supports
honest positive/negative checks for the main roadmap corridor:

- uniform-space recognition
- entourage extraction
- uniform continuity
- Cauchy-filter recognition
- uniform completeness
"""

from __future__ import annotations

from typing import Any

VERSION = "0.1.104"

UNIFORM_TRUE_TAGS = {
    "uniform_space",
    "metric_uniformity",
    "discrete_uniformity",
    "metric",
    "metrizable",
    "complete_metric",
}
UNIFORM_COMPLETE_TRUE_TAGS = {
    "complete_metric",
    "discrete_uniformity",
    "finite_uniform_space",
}


def _metadata_of(obj: Any) -> dict[str, Any]:
    if isinstance(obj, dict):
        raw = obj.get("metadata", {})
        return raw if isinstance(raw, dict) else {}
    raw = getattr(obj, "metadata", {}) or {}
    return raw if isinstance(raw, dict) else {}


def _extract_tags(obj: Any) -> set[str]:
    tags: set[str] = set()
    if isinstance(obj, dict):
        raw_tags = obj.get("tags", [])
        if isinstance(raw_tags, (set, list, tuple, frozenset)):
            tags.update(str(tag).strip().lower() for tag in raw_tags)
    metadata = _metadata_of(obj)
    raw_meta_tags = metadata.get("tags", [])
    if isinstance(raw_meta_tags, (set, list, tuple, frozenset)):
        tags.update(str(tag).strip().lower() for tag in raw_meta_tags)
    for attr in ("tags", "_tags"):
        raw = getattr(obj, attr, None)
        if isinstance(raw, (set, list, tuple, frozenset)):
            tags.update(str(tag).strip().lower() for tag in raw)
    return tags


def _explicit_bool(obj: Any, key: str) -> bool | None:
    if isinstance(obj, dict) and isinstance(obj.get(key), bool):
        return obj[key]
    metadata = _metadata_of(obj)
    if isinstance(metadata.get(key), bool):
        return metadata[key]
    value = getattr(obj, key, None)
    if isinstance(value, bool):
        return value
    return None


def _entourage_payload(space: Any):
    if isinstance(space, dict) and "entourages" in space:
        return space["entourages"]
    metadata = _metadata_of(space)
    if "entourages" in metadata:
        return metadata["entourages"]
    return getattr(space, "entourages", None)


def _entourage_list(space: Any) -> list[Any] | None:
    payload = _entourage_payload(space)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, tuple):
        return list(payload)
    return None


def is_uniform_space(space):
    """Check whether the input carries a usable uniform-space witness."""
    if _explicit_bool(space, "is_uniform_space") is not None:
        return bool(_explicit_bool(space, "is_uniform_space"))
    entourages = _entourage_list(space)
    if entourages:
        return True
    tags = _extract_tags(space)
    return bool(tags & UNIFORM_TRUE_TAGS)


def entourage_system(space):
    """Return the entourage list when a benchmark uniformity is available."""
    entourages = _entourage_list(space)
    if entourages is not None:
        return entourages
    tags = _extract_tags(space)
    if "discrete_uniformity" in tags:
        return ["diagonal_subset", "all_supersets_of_diagonal"]
    if "metric_uniformity" in tags or "metric" in tags or "complete_metric" in tags:
        return ["epsilon_ball_entourages"]
    if is_uniform_space(space):
        return ["symbolic_entourage_basis"]
    return None


def is_uniformly_continuous(mapping):
    """Check whether a mapping carries a benchmark uniform-continuity witness."""
    explicit = _explicit_bool(mapping, "is_uniformly_continuous")
    if explicit is not None:
        return explicit
    tags = _extract_tags(mapping)
    if "uniformly_continuous" in tags:
        return True
    if "not_uniformly_continuous" in tags:
        return False
    if isinstance(mapping, dict):
        if mapping.get("lipschitz_constant") is not None:
            return True
        if mapping.get("map_type") in {"identity", "constant"}:
            return True
    metadata = _metadata_of(mapping)
    if metadata.get("lipschitz_constant") is not None:
        return True
    if metadata.get("map_type") in {"identity", "constant"}:
        return True
    return False


def is_cauchy_filter(filter_obj, uniform_space):
    """Check whether a filter object carries a benchmark Cauchy witness."""
    explicit = _explicit_bool(filter_obj, "is_cauchy_filter")
    if explicit is not None:
        return explicit
    if not is_uniform_space(uniform_space):
        return False
    if isinstance(filter_obj, dict):
        if filter_obj.get("filter_type") == "principal":
            return True
        if filter_obj.get("meets_every_entourage") is True:
            return True
    metadata = _metadata_of(filter_obj)
    if metadata.get("filter_type") == "principal":
        return True
    if metadata.get("meets_every_entourage") is True:
        return True
    return False


def is_uniformly_complete(uniform_space):
    """Check completeness on the benchmark uniform-space corridor."""
    explicit = _explicit_bool(uniform_space, "is_uniformly_complete")
    if explicit is not None:
        return explicit
    if not is_uniform_space(uniform_space):
        return False
    tags = _extract_tags(uniform_space)
    if tags & UNIFORM_COMPLETE_TRUE_TAGS:
        return True
    if isinstance(uniform_space, dict):
        if uniform_space.get("space_type") == "Metric Uniformity":
            return True
        if uniform_space.get("space_type") == "Discrete Uniformity":
            return True
    metadata = _metadata_of(uniform_space)
    if metadata.get("space_type") == "Metric Uniformity":
        return True
    if metadata.get("space_type") == "Discrete Uniformity":
        return True
    return False


# ---------------------------------------------------------------------------
# Uniform equivalence
# ---------------------------------------------------------------------------

def uniform_equivalence(space1: Any, space2: Any) -> bool | None:
    """Check whether two uniform spaces are uniformly equivalent.

    Two uniform spaces are uniformly equivalent if there is a bijective
    uniformly continuous map whose inverse is also uniformly continuous.
    Returns True/False if decisive from tags; None if unknown.
    """
    if not is_uniform_space(space1) or not is_uniform_space(space2):
        return None
    tags1 = _extract_tags(space1)
    tags2 = _extract_tags(space2)
    # Both complete metric separable ↔ Polish; two Polish spaces of the same
    # cardinality are Borel isomorphic but not necessarily uniformly equivalent.
    # Only trivially decisive case: same explicit type tag.
    explicit_types = {
        "complete_metric", "discrete_uniformity", "finite_uniform_space"
    }
    types1 = tags1 & explicit_types
    types2 = tags2 & explicit_types
    if types1 and types2 and types1 == types2:
        return True
    if types1 and types2 and types1 != types2:
        return False
    return None


# ---------------------------------------------------------------------------
# Uniform completion descriptor
# ---------------------------------------------------------------------------

def uniform_completion_descriptor(space: Any) -> dict[str, Any]:
    """Describe the uniform completion of *space*.

    Every uniform space embeds densely in a (up to uniform equivalence)
    unique complete Hausdorff uniform space: its completion.

    Returns
    -------
    dict with keys: is_already_complete, completion_tags, description,
    version, warnings
    """
    tags = _extract_tags(space)
    warnings: list[str] = []

    already_complete = is_uniformly_complete(space)
    completion_tags: set[str] = set(tags)

    # Completion always gives a complete Hausdorff uniform space
    completion_tags.add("complete_metric" if ("metric" in tags or "metrizable" in tags) else "uniformly_complete")
    completion_tags.add("hausdorff")

    if "separable" in tags:
        completion_tags.add("separable")
    if "second_countable" in tags:
        completion_tags.add("second_countable")

    # Totally bounded ↔ compact completion
    if "totally_bounded" in tags:
        completion_tags.add("compact")
        description = (
            "Totally bounded uniform space: completion is compact "
            "(generalized Heine-Borel; completion of totally bounded = compact)."
        )
    elif "metric" in tags or "metrizable" in tags:
        description = (
            "Metric space: completion is the unique (up to isometry) complete "
            "metric space in which this space embeds densely."
        )
    else:
        description = (
            "Uniform space: completion is the unique (up to uniform equivalence) "
            "complete Hausdorff uniform space containing this as a dense subspace."
        )
        if not is_uniform_space(space):
            warnings.append("Input does not appear to be a uniform space; completion may not apply.")

    if already_complete:
        description = "Space is already complete; completion = space itself."

    return {
        "is_already_complete": already_complete,
        "completion_tags": sorted(completion_tags),
        "description": description,
        "warnings": warnings,
        "version": VERSION,
    }


# ---------------------------------------------------------------------------
# Smirnov metrization oracle
# ---------------------------------------------------------------------------

def smirnov_metrization_oracle(space: Any) -> dict[str, Any]:
    """Apply the Smirnov-Čech metrization theorem to *space*.

    Theorem (Smirnov, 1951): A topological space X is metrizable if and
    only if it is paracompact and locally metrizable.

    Equivalently via the Urysohn metrization theorem:
    Second-countable + regular (T3) ↔ metrizable.

    Returns
    -------
    dict with keys: is_metrizable (bool|None), theorem_applied,
    justification, missing_conditions, version
    """
    tags = _extract_tags(space)

    # Already metrizable
    if "metrizable" in tags or "metric" in tags:
        return {
            "is_metrizable": True,
            "theorem_applied": "direct_tag",
            "justification": "Space is explicitly tagged as metrizable/metric.",
            "missing_conditions": [],
            "version": VERSION,
        }

    if "not_metrizable" in tags:
        return {
            "is_metrizable": False,
            "theorem_applied": "direct_tag",
            "justification": "Space is explicitly tagged not_metrizable.",
            "missing_conditions": [],
            "version": VERSION,
        }

    # Urysohn metrization: second-countable + regular (T3) → metrizable
    is_second_countable = "second_countable" in tags
    is_regular = "regular" in tags or "t3" in tags
    if is_second_countable and is_regular:
        return {
            "is_metrizable": True,
            "theorem_applied": "urysohn_metrization",
            "justification": (
                "Urysohn metrization theorem: second-countable + regular (T3) ⟹ metrizable. "
                "Space satisfies both conditions."
            ),
            "missing_conditions": [],
            "version": VERSION,
        }

    # Smirnov metrization: paracompact + locally metrizable → metrizable
    is_paracompact = "paracompact" in tags
    is_locally_metrizable = "locally_metrizable" in tags or "locally_metric" in tags
    if is_paracompact and is_locally_metrizable:
        return {
            "is_metrizable": True,
            "theorem_applied": "smirnov_metrization",
            "justification": (
                "Smirnov metrization theorem (1951): paracompact + locally metrizable ⟹ metrizable."
            ),
            "missing_conditions": [],
            "version": VERSION,
        }

    # Negative: compact + hausdorff + not_first_countable → not metrizable
    if "compact" in tags and "hausdorff" in tags and "not_first_countable" in tags:
        return {
            "is_metrizable": False,
            "theorem_applied": "first_countable_obstruction",
            "justification": (
                "Metrizable ⟹ first-countable, but space is tagged not_first_countable."
            ),
            "missing_conditions": [],
            "version": VERSION,
        }

    # Report what's missing for each theorem
    missing: list[str] = []
    if not is_second_countable:
        missing.append("second_countable (for Urysohn metrization)")
    if not is_regular:
        missing.append("regular/t3 (for Urysohn metrization)")
    if not is_paracompact:
        missing.append("paracompact (for Smirnov metrization)")
    if not is_locally_metrizable:
        missing.append("locally_metrizable (for Smirnov metrization)")

    return {
        "is_metrizable": None,
        "theorem_applied": "none",
        "justification": "Insufficient tags to apply metrization theorems.",
        "missing_conditions": missing,
        "version": VERSION,
    }


# ---------------------------------------------------------------------------
# Uniform topology tags
# ---------------------------------------------------------------------------

def uniform_topology_tags(space: Any) -> set[str]:
    """Infer topological property tags from a uniform structure.

    Every uniform space carries a natural topology (generated by entourage
    neighborhoods).  This function returns the property tags that follow
    from the uniform structure.

    Returns
    -------
    set of tag strings
    """
    tags = _extract_tags(space)
    inferred: set[str] = set()

    if not is_uniform_space(space):
        return inferred

    # Every uniform space is completely regular (Tychonoff)
    inferred.add("completely_regular")
    inferred.add("tychonoff")

    if "metric" in tags or "metrizable" in tags:
        inferred.update({"t0", "t1", "hausdorff", "regular", "t3", "normal", "t4"})

    if is_uniformly_complete(space):
        inferred.add("uniformly_complete")
        if "metric" in tags or "metrizable" in tags:
            inferred.add("complete_metric")

    if "discrete_uniformity" in tags:
        inferred.update({"discrete", "t0", "t1", "hausdorff"})

    return inferred


__all__ = [
    "is_uniform_space",
    "entourage_system",
    "is_uniformly_continuous",
    "is_cauchy_filter",
    "is_uniformly_complete",
    "uniform_equivalence",
    "uniform_completion_descriptor",
    "smirnov_metrization_oracle",
    "uniform_topology_tags",
]
