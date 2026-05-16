"""Experimental and research-facing layer.

Promoted modules
----------------
The following modules were promoted to :mod:`pytop` (stable core) and now live
there as the canonical implementation. The copies in this package are
**compatibility wrappers** that re-export from :mod:`pytop` so that any
existing code using the experimental import path continues to work without
modification:

- ``compactness_strengthened_profiles`` → :mod:`pytop.compactness_strengthened_profiles`
- ``hereditary_local_profiles``         → :mod:`pytop.hereditary_local_profiles`
- ``research_bridge_profiles``          → :mod:`pytop.research_bridge_profiles`
- ``tightness_network_profiles``        → :mod:`pytop.tightness_network_profiles`

New code should import from :mod:`pytop` directly.
"""

from .advanced_cardinal_functions import (
    InequalityProfile,
    get_named_inequality_profiles,
    inequality_profile_layer_summary,
)
from .advanced_metrization import (
    MetrizationProfile,
    get_named_metrization_profiles,
    metrization_chapter_index,
    metrization_layer_summary,
)
from .chapter_experimental_registry import (
    build_chapter_experimental_registry,
    chapter_registry_summary,
    chapter_route_summary,
)
from .compactness_cardinal_bridges import (
    CompactnessBridgeProfile,
    compactness_bridge_chapter_index,
    compactness_bridge_layer_summary,
    get_named_compactness_bridge_profiles,
)
from .compactness_strengthened_profiles import (
    CompactnessStrengthenedProfile,
    compactness_strengthened_chapter_index,
    compactness_strengthened_layer_summary,
    get_named_compactness_strengthened_profiles,
)
from .experimental_inference import (
    TheoremProfileAlignment,
    get_promoted_theorem_profile_alignments,
    theorem_profile_alignment_summary,
    theorem_profile_family_summary,
    theorem_profile_feature_index,
    theorem_profile_index_by_profile_key,
)
from .maturity_registry import (
    ExperimentalMaturityProfile,
    chapter_primary_maturity_summary,
    consolidation_bucket_summary,
    core_counterpart_index,
    experimental_maturity_summary,
    get_experimental_maturity_profiles,
    lookup_experimental_maturity,
    preferred_home_summary,
    retained_research_draft_modules,
    retained_supported_experimental_modules,
)
from .research_bridge_inventory import build_research_bridge_inventory, inventory_layer_summary
from .research_bridge_profiles import (
    ResearchBridgeProfile,
    get_named_research_bridge_profiles,
    research_bridge_chapter_index,
    research_bridge_layer_summary,
)
from .research_notebook_registry import (
    get_research_notebook_profiles,
    notebook_profile_summary,
)
from .research_path_registry import (
    ResearchPathProfile,
    get_named_research_path_profiles,
    research_path_chapter_index,
    research_path_layer_summary,
    research_path_route_index,
)
from .special_example_spaces import (
    SpecialExampleProfile,
    get_named_special_example_profiles,
    special_example_chapter_index,
    special_example_role_summary,
    special_example_route_index,
)
from .theorem_drafts import (
    benchmark_class_summary,
    chapter_draft_summary,
    get_named_theorem_draft_profiles,
)

__all__ = [
    "build_chapter_experimental_registry",
    "chapter_registry_summary",
    "chapter_route_summary",
    "ExperimentalMaturityProfile",
    "chapter_primary_maturity_summary",
    "experimental_maturity_summary",
    "get_experimental_maturity_profiles",
    "lookup_experimental_maturity",
    "preferred_home_summary",
    "core_counterpart_index",
    "retained_supported_experimental_modules",
    "retained_research_draft_modules",
    "consolidation_bucket_summary",
    "build_research_bridge_inventory",
    "inventory_layer_summary",
    "ResearchPathProfile",
    "get_named_research_path_profiles",
    "research_path_chapter_index",
    "research_path_layer_summary",
    "research_path_route_index",
    "benchmark_class_summary",
    "chapter_draft_summary",
    "get_named_theorem_draft_profiles",
    "TheoremProfileAlignment",
    "get_promoted_theorem_profile_alignments",
    "theorem_profile_alignment_summary",
    "theorem_profile_family_summary",
    "theorem_profile_feature_index",
    "theorem_profile_index_by_profile_key",
    "get_research_notebook_profiles",
    "notebook_profile_summary",
    "ResearchBridgeProfile",
    "SpecialExampleProfile",
    "get_named_research_bridge_profiles",
    "research_bridge_chapter_index",
    "research_bridge_layer_summary",
    "get_named_special_example_profiles",
    "special_example_chapter_index",
    "special_example_role_summary",
    "special_example_route_index",
    "InequalityProfile",
    "get_named_inequality_profiles",
    "inequality_profile_layer_summary",
    "MetrizationProfile",
    "get_named_metrization_profiles",
    "metrization_chapter_index",
    "metrization_layer_summary",
    "CompactnessBridgeProfile",
    "compactness_bridge_chapter_index",
    "compactness_bridge_layer_summary",
    "get_named_compactness_bridge_profiles",
    "CompactnessStrengthenedProfile",
    "compactness_strengthened_chapter_index",
    "compactness_strengthened_layer_summary",
    "get_named_compactness_strengthened_profiles",
]
