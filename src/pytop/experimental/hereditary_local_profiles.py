"""Compatibility wrapper for the promoted hereditary/local registry.

The stable profile families now live in :mod:`pytop.hereditary_local_profiles`.
This module stays in place to preserve experimental imports while the
promotion path settles across docs and release records.
"""

from __future__ import annotations

from pytop.hereditary_local_profiles import (
    HereditaryLocalProfile,
    get_named_hereditary_local_profiles,
    hereditary_local_chapter32_entry_bridge,
    hereditary_local_chapter_index,
    hereditary_local_entry_profiles,
    hereditary_local_lane_summary,
    hereditary_local_quantifier_summary,
    hereditary_local_warning_profiles,
    render_hereditary_local_strengthening_report,
)
