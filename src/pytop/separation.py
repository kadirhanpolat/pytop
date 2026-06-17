"""Separation-axiom support — backward-compatible re-export.

The implementation is split across two modules:

- :mod:`pytop.separation_basic` — shared data, core engine, T0–T2.5 queries,
  all finite and theorem-level helpers
- :mod:`pytop.separation_advanced` — T3–T6 queries, multi-criterion Tychonoff
  check, separation_chain

Import from those modules directly for a finer-grained dependency, or continue
importing from this module for full backward compatibility.
"""

from .separation_advanced import (  # noqa: F401
    check_tychonoff,
    is_completely_normal,
    is_completely_regular,
    is_normal,
    is_perfectly_normal,
    is_regular,
    is_t3,
    is_t4,
    is_t5,
    is_tychonoff,
    separation_chain,
    tychonoff_characterization,
)
from .separation_basic import (  # noqa: F401
    ADVANCED_PROPERTIES,
    BASIC_PROPERTIES,
    DEFAULT_PROFILE_PROPERTIES,
    FALSE_TAGS,
    SEPARATION_CHAIN_ORDER,
    SUPPORTED_PROPERTIES,
    TRUE_TAGS,
    TYCHONOFF_POSITIVE_TAGS,
    SeparationError,
    # private helpers — re-exported for backward compatibility with existing tests
    _finite_basic_separation,
    _finite_closed_sets,
    _finite_normal,
    _finite_open_sets,
    _finite_proof_hint,
    _finite_regular,
    _finite_result,
    _finite_separation,
    _metric_justification,
    _negative_tag_implication,
    _positive_tag_implies,
    _separate_closed_sets,
    _separate_point_and_closed_set,
    _theorem_level_separation,
    advanced_separation_report,
    analyze_separation,
    is_hausdorff,
    is_t0,
    is_t1,
    is_t2,
    is_t2_5,
    is_urysohn,
    normalize_separation_property,
    separation_profile,
)

__all__ = [
    "SeparationError",
    "normalize_separation_property",
    "analyze_separation",
    "separation_profile",
    "advanced_separation_report",
    "is_t0",
    "is_t1",
    "is_hausdorff",
    "is_t2",
    "is_urysohn",
    "is_t2_5",
    "is_regular",
    "is_t3",
    "is_completely_regular",
    "is_tychonoff",
    "is_normal",
    "is_t4",
    "is_completely_normal",
    "is_t5",
    "is_perfectly_normal",
    "TYCHONOFF_POSITIVE_TAGS",
    "SEPARATION_CHAIN_ORDER",
    "check_tychonoff",
    "tychonoff_characterization",
    "separation_chain",
]
