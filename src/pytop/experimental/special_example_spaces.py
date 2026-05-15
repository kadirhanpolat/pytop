"""Compatibility wrapper for the promoted special-example registry.

The stable named-example surface now lives in :mod:`pytop.special_example_profiles`.
This module stays in place to avoid breaking experimental imports while the
promotion path settles.
"""

from __future__ import annotations

from pytop.special_example_profiles import (
    SpecialExampleProfile,
    get_named_special_example_profiles,
    special_example_chapter_index,
    special_example_role_summary,
    special_example_route_index,
)
