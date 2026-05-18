"""Infinite-space representations with explicit family-level semantics.

The goal of this module is not to provide a universal decision procedure for
all infinite topological spaces. Instead, it offers a small collection of
symbolic space classes that carry enough structure and tags to support exact,
theorem-based, or metadata-backed reasoning in other parts of ``pytop``.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

from ._infinite_helpers import (
    STANDARD_COUNTABLE_CARRIERS,
    STANDARD_UNCOUNTABLE_CARRIERS,
    VALID_CARDINALITY_TOKENS,
    _has_standard_countable_subset,
    _infer_size_tags,
    _is_countable_family_size,
)
from .spaces import TopologicalSpace


@dataclass
class InfiniteTopologicalSpace(TopologicalSpace):
    """Base class for symbolic infinite topological spaces."""

    def is_infinite(self) -> bool:
        return True

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("infinite")
        for tag in sorted(_infer_size_tags(self.carrier, self.metadata)):
            self.add_tags(tag)
        self.metadata.setdefault("representation", "symbolic_general")
        cardinality = str(self.metadata.get("cardinality", "")).strip().lower()
        if cardinality and cardinality not in VALID_CARDINALITY_TOKENS:
            warnings.warn(
                f"Unrecognised cardinality value {cardinality!r}. "
                f"Expected one of {sorted(VALID_CARDINALITY_TOKENS)}.",
                UserWarning,
                stacklevel=3,
            )
        if "countable" in self.tags and "uncountable" in self.tags:
            warnings.warn(
                "Space carries both 'countable' and 'uncountable' tags simultaneously.",
                UserWarning,
                stacklevel=3,
            )


@dataclass
class MetricLikeSpace(InfiniteTopologicalSpace):
    """A symbolic infinite space known to arise from a metric."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("metric", "t0", "t1", "hausdorff", "first_countable")
        self.metadata["representation"] = "infinite_metric"


@dataclass
class BasisDefinedSpace(InfiniteTopologicalSpace):
    """A symbolic infinite space represented by basis-level metadata."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("basis_defined")
        if _is_countable_family_size(self.metadata.get("basis_size")):
            self.add_tags("second_countable")
        if _is_countable_family_size(self.metadata.get("local_base_size")):
            self.add_tags("first_countable")
        self.metadata["representation"] = "basis_defined"


@dataclass
class DiscreteInfiniteSpace(InfiniteTopologicalSpace):
    """An infinite discrete space with family-level exact semantics."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags(
            "discrete",
            "t0",
            "t1",
            "hausdorff",
            "first_countable",
            "not_compact",
            "not_connected",
            "not_path_connected",
        )
        if self.has_tag("countable"):
            self.add_tags("second_countable", "separable", "lindelof")
        if self.has_tag("uncountable"):
            self.add_tags("not_second_countable", "not_separable", "not_lindelof")
        self.metadata["representation"] = "infinite_discrete"


@dataclass
class IndiscreteInfiniteSpace(InfiniteTopologicalSpace):
    """An infinite indiscrete space."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags(
            "indiscrete",
            "compact",
            "connected",
            "path_connected",
            "first_countable",
            "second_countable",
            "separable",
            "lindelof",
            "not_t0",
            "not_t1",
            "not_hausdorff",
        )
        self.metadata["representation"] = "infinite_indiscrete"


@dataclass
class CofiniteSpace(InfiniteTopologicalSpace):
    """An infinite cofinite-topology space."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("cofinite", "compact", "connected", "t0", "t1", "not_hausdorff")
        if _has_standard_countable_subset(self.carrier, self.metadata):
            self.add_tags("separable")
            self.metadata.setdefault("dense_subset_size", "aleph_0")
        if self.has_tag("countable"):
            self.add_tags("first_countable", "second_countable")
            self.metadata.setdefault("basis_size", "aleph_0")
            self.metadata.setdefault("local_base_size", "aleph_0")
        else:
            self.add_tags("not_first_countable", "not_second_countable")
        self.metadata["representation"] = "infinite_cofinite"


@dataclass
class CocountableSpace(InfiniteTopologicalSpace):
    """An infinite cocountable-topology space.

    The intended mathematical use is an uncountable carrier, where the space is
    T1, connected, Lindelöf, nonseparable, noncompact, and non-first-countable.
    On countable carriers this class would collapse to the discrete topology, so
    examples should normally use an uncountable symbolic carrier such as ``"R"``.
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("cocountable", "connected", "t0", "t1", "lindelof", "not_compact", "not_hausdorff")
        if self.has_tag("uncountable"):
            self.add_tags("not_first_countable", "not_second_countable", "not_separable")
        if self.has_tag("countable"):
            self.add_tags(
                "discrete",
                "hausdorff",
                "first_countable",
                "second_countable",
                "separable",
                "not_connected",
                "not_path_connected",
            )
        self.metadata["representation"] = "infinite_cocountable"


@dataclass
class SorgenfreyLikeSpace(BasisDefinedSpace):
    """A symbolic stand-in for lower-limit style order-topology examples."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("order_topology", "hausdorff", "t0", "t1", "first_countable", "separable", "not_second_countable")
        self.metadata["representation"] = "basis_defined"


__all__ = [
    "STANDARD_COUNTABLE_CARRIERS",
    "STANDARD_UNCOUNTABLE_CARRIERS",
    "VALID_CARDINALITY_TOKENS",
    "InfiniteTopologicalSpace",
    "MetricLikeSpace",
    "BasisDefinedSpace",
    "DiscreteInfiniteSpace",
    "IndiscreteInfiniteSpace",
    "CofiniteSpace",
    "CocountableSpace",
    "SorgenfreyLikeSpace",
]
