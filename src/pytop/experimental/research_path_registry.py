"""Compatibility wrapper for research-path profiles.

The canonical implementation lives in :mod:`pytop.research_path_profiles`.
This module exists to keep the experimental import path stable without
duplicating implementation logic.
"""

from pytop.research_path_profiles import (
    ResearchPathProfile,
    get_named_research_path_profiles,
    research_path_chapter_index,
    research_path_layer_summary,
    research_path_route_index,
)

__all__ = [
    "ResearchPathProfile",
    "get_named_research_path_profiles",
    "research_path_chapter_index",
    "research_path_layer_summary",
    "research_path_route_index",
]
