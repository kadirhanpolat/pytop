"""Compatibility wrapper for the promoted metrization profile registry.

The stable profile families now live in :mod:`pytop.metrization_profiles`.
This module remains available to avoid breaking the old experimental import
path while the promotion settles.
"""

from __future__ import annotations

from pytop.metrization_profiles import (
    MetrizationProfile,
    get_named_metrization_profiles,
    metrization_chapter_index,
    metrization_layer_summary,
)
