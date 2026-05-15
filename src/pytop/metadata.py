"""Metadata helpers for spaces, methods, and support levels."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SpaceMetadata:
    representation: str
    support_level: str
    notes: str = ""
    tags: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, object]:
        return {
            "representation": self.representation,
            "support_level": self.support_level,
            "notes": self.notes,
            "tags": sorted(self.tags),
        }
