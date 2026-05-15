"""Base abstractions for topological spaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass
class TopologicalSpace:
    carrier: Any
    topology: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.tags = {str(tag).strip().lower() for tag in self.tags if str(tag).strip()}
        self.metadata = dict(self.metadata)
        meta_tags = self.metadata.get("tags")
        if meta_tags:
            self.tags.update(str(tag).strip().lower() for tag in meta_tags if str(tag).strip())
        self.metadata["tags"] = sorted(self.tags)

    def is_finite(self) -> bool:
        if isinstance(self.carrier, (str, bytes)) or self.carrier is None:
            return False
        try:
            len(self.carrier)
        except Exception:
            return False
        return True

    def add_tags(self, *tags: str) -> None:
        for tag in tags:
            text = str(tag).strip().lower()
            if text:
                self.tags.add(text)
        self.metadata["tags"] = sorted(self.tags)

    def has_tag(self, tag: str) -> bool:
        return str(tag).strip().lower() in self.tags

    def describe(self) -> str:
        return self.metadata.get("description", "topological space")

    @classmethod
    def symbolic(
        cls,
        *,
        description: str,
        representation: str = "symbolic_general",
        tags: Iterable[str] = (),
    ) -> "TopologicalSpace":
        return cls(
            carrier=None,
            topology=None,
            metadata={"description": description, "representation": representation, "tags": list(tags)},
            tags=set(tags),
        )
