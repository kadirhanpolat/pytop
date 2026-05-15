"""Compatibility wrapper for the promoted compactness-strengthened registry.

The stable comparison families now live in :mod:`pytop.compactness_strengthened_profiles`.
This wrapper preserves the old experimental import path while the promotion path is
made visible across docs and release records.
"""

from __future__ import annotations

from pytop.compactness_strengthened_profiles import (
    CompactnessStrengthenedProfile,
    compactness_strengthened_chapter_index,
    compactness_strengthened_entry_profiles,
    compactness_strengthened_layer_summary,
    compactness_strengthened_lane_summary,
    compactness_strengthened_prerequisite_bridge,
    compactness_strengthened_selected_profiles,
    compactness_strengthened_warning_profiles,
    get_named_compactness_strengthened_profiles,
    render_compactness_strengthened_report,
)
