"""Unified property dispatch for finite and infinite topological spaces.

Routes property queries to the correct finite or infinite analyzer based on
the space type, eliminating the need for callers to know which module to use.

Key functions:
  ``analyze_property``   — single entry point for any space + property name
  ``analyze_space``      — run all detectable properties for a space
  ``is_finite_space``    — detect FiniteTopologicalSpace instances
  ``is_infinite_space``  — detect InfiniteTopologicalSpace instances
  ``property_registry``  — return the property → (finite_fn, infinite_fn) map
"""

from __future__ import annotations

from typing import Any

from .result import Result

VERSION = "0.1.0"


# ---------------------------------------------------------------------------
# Dict pre-processing
# ---------------------------------------------------------------------------

def _to_space(space: Any) -> Any:
    """Convert a plain dict with 'tags' key to a TopologicalSpace.symbolic().

    The core analyzers (compactness.py, separation.py, etc.) use
    ``getattr(space, 'tags', ...)`` and do not support plain dict inputs.
    This function normalises dict inputs before dispatch.
    """
    if not isinstance(space, dict):
        return space
    try:
        from .spaces import TopologicalSpace
        raw_tags = space.get("tags", [])
        if isinstance(raw_tags, (list, tuple, set, frozenset)):
            tags = list(raw_tags)
        else:
            tags = []
        meta = dict(space)
        description = space.get("description", "symbolic space")
        return TopologicalSpace.symbolic(description=description, tags=tags)
    except Exception:
        return space


# ---------------------------------------------------------------------------
# Space type detection
# ---------------------------------------------------------------------------

def is_finite_space(space: Any) -> bool:
    """Return True if *space* is a FiniteTopologicalSpace instance."""
    try:
        from .finite_spaces import FiniteTopologicalSpace
        return isinstance(space, FiniteTopologicalSpace)
    except ImportError:
        return False


def is_infinite_space(space: Any) -> bool:
    """Return True if *space* is an InfiniteTopologicalSpace instance."""
    try:
        from .infinite_spaces import InfiniteTopologicalSpace
        return isinstance(space, InfiniteTopologicalSpace)
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# Property registry
# ---------------------------------------------------------------------------

# Each entry: property_name → (finite_analyzer, infinite_analyzer)
# Both are callables of the form f(space) → Result.
# None means "no dedicated implementation; fall through to generic".

def _build_registry() -> dict[str, tuple[Any, Any]]:
    # Lazy imports inside function to avoid circular deps at module load time.
    from .compactness import analyze_compactness
    from .connectedness import analyze_connectedness
    from .separation import analyze_separation
    from .infinite_compactness import analyze_infinite_compactness
    from .infinite_connectedness import analyze_infinite_connectedness
    from .infinite_separation import analyze_infinite_separation

    def _finite_compact(s):       return analyze_compactness(s, "compact")
    def _finite_cc(s):            return analyze_compactness(s, "countably_compact")
    def _finite_seq(s):           return analyze_compactness(s, "sequentially_compact")
    def _finite_lpc(s):           return analyze_compactness(s, "limit_point_compact")
    def _finite_lindelof(s):      return analyze_compactness(s, "lindelof")
    def _finite_connected(s):     return analyze_connectedness(s, "connected")
    def _finite_path(s):          return analyze_connectedness(s, "path_connected")
    def _finite_t0(s):            return analyze_separation(s, "t0")
    def _finite_t1(s):            return analyze_separation(s, "t1")
    def _finite_hausdorff(s):     return analyze_separation(s, "hausdorff")
    def _finite_regular(s):       return analyze_separation(s, "regular")
    def _finite_normal(s):        return analyze_separation(s, "normal")
    def _finite_completely_regular(s): return analyze_separation(s, "completely_regular")

    def _inf_compact(s):          return analyze_infinite_compactness(s, "compact")
    def _inf_cc(s):               return analyze_infinite_compactness(s, "countably_compact")
    def _inf_seq(s):              return analyze_infinite_compactness(s, "sequentially_compact")
    def _inf_lpc(s):              return analyze_infinite_compactness(s, "limit_point_compact")
    def _inf_lindelof(s):         return analyze_infinite_compactness(s, "lindelof")
    def _inf_connected(s):        return analyze_infinite_connectedness(s, "connected")
    def _inf_path(s):             return analyze_infinite_connectedness(s, "path_connected")
    def _inf_t0(s):               return analyze_infinite_separation(s, "t0")
    def _inf_t1(s):               return analyze_infinite_separation(s, "t1")
    def _inf_hausdorff(s):        return analyze_infinite_separation(s, "hausdorff")
    def _inf_regular(s):          return analyze_infinite_separation(s, "regular")
    def _inf_normal(s):           return analyze_infinite_separation(s, "normal")
    def _inf_completely_regular(s): return analyze_infinite_separation(s, "completely_regular")

    return {
        # Compactness family
        "compact":              (_finite_compact,           _inf_compact),
        "countably_compact":    (_finite_cc,                _inf_cc),
        "sequentially_compact": (_finite_seq,               _inf_seq),
        "limit_point_compact":  (_finite_lpc,               _inf_lpc),
        "lindelof":             (_finite_lindelof,          _inf_lindelof),
        # Connectedness family
        "connected":            (_finite_connected,         _inf_connected),
        "path_connected":       (_finite_path,              _inf_path),
        # Separation family
        "t0":                   (_finite_t0,                _inf_t0),
        "t1":                   (_finite_t1,                _inf_t1),
        "hausdorff":            (_finite_hausdorff,         _inf_hausdorff),
        "t2":                   (_finite_hausdorff,         _inf_hausdorff),
        "regular":              (_finite_regular,           _inf_regular),
        "normal":               (_finite_normal,            _inf_normal),
        "completely_regular":   (_finite_completely_regular, _inf_completely_regular),
    }


_REGISTRY: dict[str, tuple[Any, Any]] | None = None


def property_registry() -> dict[str, tuple[Any, Any]]:
    """Return the canonical property → (finite_fn, infinite_fn) map."""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _build_registry()
    return _REGISTRY


# ---------------------------------------------------------------------------
# Core dispatch
# ---------------------------------------------------------------------------

_ALIASES: dict[str, str] = {
    "compactness": "compact",
    "t2": "hausdorff",
    "t2_5": "hausdorff",          # urysohn — fall back to hausdorff for dispatch
    "urysohn": "hausdorff",
    "t3": "regular",
    "t4": "normal",
    "perfectly_normal": "normal",
    "path-connected": "path_connected",
    "pathconnected": "path_connected",
    "countably-compact": "countably_compact",
    "sequentially-compact": "sequentially_compact",
    "limit-point-compact": "limit_point_compact",
}


def _normalize(name: str) -> str:
    key = name.strip().lower().replace("-", "_").replace(" ", "_")
    return _ALIASES.get(key, key)


def analyze_property(space: Any, property_name: str) -> Result:
    """Analyze *property_name* for *space*, dispatching to the correct layer.

    Automatically detects whether *space* is finite or infinite and calls
    the appropriate analyzer.  For generic objects (dicts, tag-bearing objects)
    that are neither, falls back to the finite analyzer which supports tags.

    Parameters
    ----------
    space:
        A FiniteTopologicalSpace, InfiniteTopologicalSpace, dict with 'tags',
        or any object carrying a 'tags' attribute.
    property_name:
        One of: compact, countably_compact, sequentially_compact,
        limit_point_compact, lindelof, connected, path_connected,
        t0, t1, hausdorff/t2, regular/t3, normal/t4, completely_regular.
        Aliases and hyphenated forms are accepted.

    Returns
    -------
    Result
        A Result with fields: holds, mode, value, justification, metadata.
    """
    key = _normalize(property_name)
    registry = property_registry()

    if key not in registry:
        return Result.unknown(
            mode="symbolic",
            value=key,
            justification=[
                f"Property {property_name!r} is not in the unified dispatch registry. "
                f"Supported: {sorted(registry)}."
            ],
            metadata={"version": VERSION, "property": property_name},
        )

    finite_fn, infinite_fn = registry[key]

    space = _to_space(space)

    if is_infinite_space(space):
        return infinite_fn(space)
    # Both FiniteTopologicalSpace and generic tag-bearing objects go to finite_fn,
    # because the finite analyzers handle TopologicalSpace objects with tags.
    return finite_fn(space)


def analyze_space(
    space: Any,
    properties: list[str] | None = None,
) -> dict[str, Result]:
    """Run multiple property analyses for *space*.

    Parameters
    ----------
    space:
        Any supported space object.
    properties:
        List of property names to analyze.  Defaults to all registered
        properties.

    Returns
    -------
    dict mapping property_name → Result
    """
    if properties is None:
        properties = list(property_registry())
    return {p: analyze_property(space, p) for p in properties}


# ---------------------------------------------------------------------------
# Convenience shorthands
# ---------------------------------------------------------------------------

def unified_compactness_report(space: Any) -> dict[str, Result]:
    """Return Results for all compactness-family properties."""
    props = ["compact", "countably_compact", "sequentially_compact",
             "limit_point_compact", "lindelof"]
    return analyze_space(space, props)


def unified_connectedness_report(space: Any) -> dict[str, Result]:
    """Return Results for all connectedness-family properties."""
    return analyze_space(space, ["connected", "path_connected"])


def unified_separation_report(space: Any) -> dict[str, Result]:
    """Return Results for all separation-family properties."""
    props = ["t0", "t1", "hausdorff", "regular", "completely_regular", "normal"]
    return analyze_space(space, props)


__all__ = [
    "analyze_property",
    "analyze_space",
    "unified_compactness_report",
    "unified_connectedness_report",
    "unified_separation_report",
    "property_registry",
    "is_finite_space",
    "is_infinite_space",
]
