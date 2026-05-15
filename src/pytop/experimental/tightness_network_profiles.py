"""Compatibility wrapper for the promoted tightness/network registry.

The stable profile families now live in :mod:`pytop.tightness_network_profiles`.
This module stays in place to preserve experimental imports while the
promotion path settles across docs and release records.
"""

from __future__ import annotations

from pytop.tightness_network_profiles import (
    TightnessNetworkProfile,
    get_named_tightness_network_profiles,
    render_tightness_network_lane_report,
    tightness_network_advanced_profiles,
    tightness_network_chapter_index,
    tightness_network_entry_advanced_split,
    tightness_network_entry_profiles,
    tightness_network_lane_summary,
    tightness_network_layer_summary,
)
