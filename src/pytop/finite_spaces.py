"""finite_spaces

Finite-space representations and exact computations.
"""

from __future__ import annotations

from dataclasses import dataclass

from .spaces import TopologicalSpace


@dataclass
class FiniteTopologicalSpace(TopologicalSpace):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_tags("finite")
        self.metadata.setdefault("representation", "finite")

    def is_finite(self) -> bool:
        return True
