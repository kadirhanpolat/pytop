"""Compatibility wrapper for the promoted classical-inequality registry.

The stable profile families now live in :mod:`pytop.classical_inequality_profiles`.
This module stays in place to preserve experimental imports while the
promotion path settles across docs and questionbank records.
"""

from __future__ import annotations

from pytop.classical_inequality_profiles import (
    ClassicalInequalityProfile,
    classical_inequality_chapter_index,
    classical_inequality_entry_profiles,
    classical_inequality_lane_summary,
    classical_inequality_layer_summary,
    classical_inequality_prerequisite_bridge,
    classical_inequality_selected_profiles,
    classical_inequality_warning_profiles,
    get_named_classical_inequality_profiles,
    render_classical_inequality_strengthening_report,
)
