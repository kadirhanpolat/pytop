"""Compatibility wrapper for the promoted cardinal-function profile registry.

The stable profile families now live in :mod:`pytop.cardinal_function_profiles`.
This module stays in place to avoid breaking experimental imports while the
promotion path settles.
"""

from __future__ import annotations

from pytop.cardinal_function_profiles import (
    CardinalFunctionProfile as InequalityProfile,
    cardinal_function_chapter_index,
    cardinal_function_layer_summary as inequality_profile_layer_summary,
    get_named_cardinal_function_profiles,
)


def get_named_inequality_profiles() -> tuple[InequalityProfile, ...]:
    """Backward-compatible alias for the promoted core registry."""

    return get_named_cardinal_function_profiles()
