"""Compatibility wrapper for the promoted research-bridge profile registry.

The stable bridge-route families now live in :mod:`pytop.research_bridge_profiles`.
This module stays in place to avoid breaking experimental imports while the
promotion path settles.
"""

from __future__ import annotations

from pytop.research_bridge_profiles import (
    ResearchBridgeProfile,
    get_named_research_bridge_profiles,
    research_bridge_chapter_index,
    research_bridge_layer_summary,
)
