"""Compatibility wrapper for the promoted theorem-profile alignment surface.

The stable theorem-facing alignment helpers now live in
:mod:`pytop.theorem_profile_alignment`. This wrapper remains in place so older
experimental imports keep working while the active line moves the reusable
inference vocabulary into ``pytop``.
"""

from pytop.theorem_profile_alignment import (
    TheoremProfileAlignment,
    get_promoted_theorem_profile_alignments,
    theorem_profile_alignment_summary,
    theorem_profile_family_summary,
    theorem_profile_feature_index,
    theorem_profile_index_by_profile_key,
)

__all__ = [
    'TheoremProfileAlignment',
    'get_promoted_theorem_profile_alignments',
    'theorem_profile_alignment_summary',
    'theorem_profile_family_summary',
    'theorem_profile_feature_index',
    'theorem_profile_index_by_profile_key',
]
