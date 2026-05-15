"""Structured result objects for exact, theorem-based, symbolic, and conditional output.

This module provides a small but usable reporting model for the core package.
The aim is to keep the result contract explicit:

- what was concluded,
- how it was concluded,
- under which assumptions,
- and with what degree of mathematical strength.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

VALID_STATUS = {"true", "false", "unknown", "conditional"}
VALID_MODE = {"exact", "theorem", "symbolic", "mixed"}


@dataclass(slots=True)
class Result:
    """A structured answer returned by `pytop` components.

    Parameters
    ----------
    status:
        One of ``true``, ``false``, ``unknown``, or ``conditional``.
    mode:
        One of ``exact``, ``theorem``, ``symbolic``, or ``mixed``.
    value:
        Optional payload. This may be a boolean, a statement string, or a
        richer structure supplied by the caller.
    assumptions:
        Assumptions under which the answer is valid.
    justification:
        Short justification lines explaining the answer.
    proof_outline:
        A lightweight proof sketch or reasoning trace.
    metadata:
        Extra machine-readable data.
    """

    status: str
    mode: str
    value: Any = None
    assumptions: list[str] = field(default_factory=list)
    justification: list[str] = field(default_factory=list)
    proof_outline: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUS:
            raise ValueError(
                f"Invalid status {self.status!r}. Expected one of {sorted(VALID_STATUS)}."
            )
        if self.mode not in VALID_MODE:
            raise ValueError(
                f"Invalid mode {self.mode!r}. Expected one of {sorted(VALID_MODE)}."
            )
        self.assumptions = _normalize_lines(self.assumptions)
        self.justification = _normalize_lines(self.justification)
        self.proof_outline = _normalize_lines(self.proof_outline)

    @property
    def is_true(self) -> bool:
        return self.status == "true"

    @property
    def is_false(self) -> bool:
        return self.status == "false"

    @property
    def is_unknown(self) -> bool:
        return self.status == "unknown"

    @property
    def is_conditional(self) -> bool:
        return self.status == "conditional"

    @property
    def is_exact(self) -> bool:
        return self.mode == "exact"

    @property
    def is_theorem_based(self) -> bool:
        return self.mode == "theorem"

    @property
    def is_symbolic(self) -> bool:
        return self.mode == "symbolic"

    def summary(self) -> str:
        details = []
        if self.assumptions:
            details.append(f"assumptions={len(self.assumptions)}")
        if self.justification:
            details.append(f"justification={len(self.justification)}")
        suffix = f" [{', '.join(details)}]" if details else ""
        return f"{self.status} ({self.mode}){suffix}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "mode": self.mode,
            "value": self.value,
            "assumptions": list(self.assumptions),
            "justification": list(self.justification),
            "proof_outline": list(self.proof_outline),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Result":
        return cls(
            status=data["status"],
            mode=data["mode"],
            value=data.get("value"),
            assumptions=list(data.get("assumptions", [])),
            justification=list(data.get("justification", [])),
            proof_outline=list(data.get("proof_outline", [])),
            metadata=dict(data.get("metadata", {})),
        )

    @classmethod
    def true(
        cls,
        *,
        mode: str,
        value: Any = True,
        assumptions: Iterable[str] = (),
        justification: Iterable[str] = (),
        proof_outline: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> "Result":
        return cls(
            status="true",
            mode=mode,
            value=value,
            assumptions=list(assumptions),
            justification=list(justification),
            proof_outline=list(proof_outline),
            metadata=dict(metadata or {}),
        )

    @classmethod
    def false(
        cls,
        *,
        mode: str,
        value: Any = False,
        assumptions: Iterable[str] = (),
        justification: Iterable[str] = (),
        proof_outline: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> "Result":
        return cls(
            status="false",
            mode=mode,
            value=value,
            assumptions=list(assumptions),
            justification=list(justification),
            proof_outline=list(proof_outline),
            metadata=dict(metadata or {}),
        )

    @classmethod
    def unknown(
        cls,
        *,
        mode: str = "symbolic",
        value: Any = None,
        assumptions: Iterable[str] = (),
        justification: Iterable[str] = (),
        proof_outline: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> "Result":
        return cls(
            status="unknown",
            mode=mode,
            value=value,
            assumptions=list(assumptions),
            justification=list(justification),
            proof_outline=list(proof_outline),
            metadata=dict(metadata or {}),
        )

    @classmethod
    def conditional(
        cls,
        *,
        mode: str,
        value: Any,
        assumptions: Iterable[str] = (),
        justification: Iterable[str] = (),
        proof_outline: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> "Result":
        return cls(
            status="conditional",
            mode=mode,
            value=value,
            assumptions=list(assumptions),
            justification=list(justification),
            proof_outline=list(proof_outline),
            metadata=dict(metadata or {}),
        )


def merge_results(*results: Result) -> Result:
    """Merge several results conservatively.

    The merged result keeps the weakest status among the inputs:
    unknown > conditional > false/true exact agreement.
    If incompatible truth values appear, the merged result becomes conditional.
    """
    if not results:
        raise ValueError("merge_results requires at least one Result.")

    statuses = {r.status for r in results}
    modes = {r.mode for r in results}

    if "unknown" in statuses:
        status = "unknown"
    elif statuses == {"true"}:
        status = "true"
    elif statuses == {"false"}:
        status = "false"
    else:
        status = "conditional"

    mode = modes.pop() if len(modes) == 1 else "mixed"

    assumptions: list[str] = []
    justification: list[str] = []
    proof_outline: list[str] = []
    metadata: dict[str, Any] = {"merged": True}
    values: list[Any] = []

    for result in results:
        assumptions.extend(x for x in result.assumptions if x not in assumptions)
        justification.extend(x for x in result.justification if x not in justification)
        proof_outline.extend(x for x in result.proof_outline if x not in proof_outline)
        values.append(result.value)

    metadata["value_trace"] = values
    return Result(
        status=status,
        mode=mode,
        value=values[-1],
        assumptions=assumptions,
        justification=justification,
        proof_outline=proof_outline,
        metadata=metadata,
    )



def _normalize_lines(lines: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for line in lines:
        text = str(line).strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized
