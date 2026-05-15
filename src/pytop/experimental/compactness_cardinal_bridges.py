"""Compatibility wrapper for the promoted compactness bridge registry.

The stable bridge families now live in :mod:`pytop.compactness_bridges`.  This
wrapper preserves the old experimental import path while the promotion path is
made visible across docs and release records.
"""

from __future__ import annotations

from pytop.compactness_bridges import (
    CompactnessBridgeProfile,
    compactness_bridge_chapter_index,
    compactness_bridge_layer_summary,
    get_named_compactness_bridge_profiles,
)
