"""Rendering helpers for structured topology results and contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable

from .result import Result


@runtime_checkable
class SupportsResult(Protocol):
    """Protocol for contract objects that expose ``to_result``."""
    def to_result(self) -> Result: ...


_STATUS_LABELS: Mapping[str, str] = {"true":"TRUE", "false":"FALSE", "unknown":"UNKNOWN", "conditional":"CONDITIONAL"}
_MODE_LABELS: Mapping[str, str] = {"exact":"exact", "theorem":"theorem-based", "symbolic":"symbolic", "mixed":"mixed"}
_STATUS_HEADLINES: Mapping[str, str] = {
    "true":"The requested statement holds.",
    "false":"The requested statement fails.",
    "unknown":"The available data do not determine the statement.",
    "conditional":"The statement is conditional on the listed assumptions.",
}


def normalize_result_source(source: Result | SupportsResult) -> Result:
    """Return a ``Result`` from either a ``Result`` or a contract-like object."""
    if isinstance(source, Result):
        return source
    if isinstance(source, SupportsResult):
        result=source.to_result()
        if not isinstance(result, Result):
            raise TypeError("to_result() must return a pytop.result.Result instance")
        return result
    raise TypeError("Expected a Result or an object implementing to_result().")


def result_status_label(source: Result | SupportsResult) -> str:
    return _STATUS_LABELS[normalize_result_source(source).status]


def result_mode_label(source: Result | SupportsResult) -> str:
    return _MODE_LABELS[normalize_result_source(source).mode]


@dataclass(frozen=True, slots=True)
class ResultExplanation:
    """Normalized, human-readable view of a ``Result``."""
    status: str
    mode: str
    label: str | None = None
    headline: str = ""
    value: str | None = None
    assumptions: tuple[str, ...] = ()
    justification: tuple[str, ...] = ()
    proof_outline: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def badge(self) -> str:
        return f"[{_STATUS_LABELS[self.status]}/{_MODE_LABELS[self.mode]}]"

    def to_dict(self) -> dict[str, Any]:
        return {"status": self.status, "mode": self.mode, "label": self.label, "badge": self.badge, "headline": self.headline, "value": self.value, "assumptions": list(self.assumptions), "justification": list(self.justification), "proof_outline": list(self.proof_outline), "metadata": dict(self.metadata)}

    def plain_lines(self, *, include_metadata: bool = False) -> list[str]:
        title=f"{self.label}: {self.headline}" if self.label else self.headline
        lines=[f"{self.badge} {title}"]
        if self.value is not None: lines.append(f"value: {self.value}")
        _extend_section(lines, "assumptions", self.assumptions)
        _extend_section(lines, "justification", self.justification)
        _extend_section(lines, "proof outline", self.proof_outline)
        if include_metadata and self.metadata: lines.append(f"metadata: {dict(self.metadata)!r}")
        return lines

    def markdown_lines(self, *, include_metadata: bool = False) -> list[str]:
        lines=[f"### {self.badge} {self.label or 'Result'}", "", self.headline]
        if self.value is not None: lines.extend(["", f"- **Value:** `{self.value}`"])
        _extend_markdown_section(lines, "Assumptions", self.assumptions)
        _extend_markdown_section(lines, "Justification", self.justification)
        _extend_markdown_section(lines, "Proof outline", self.proof_outline)
        if include_metadata and self.metadata: lines.extend(["", f"- **Metadata:** `{dict(self.metadata)!r}`"])
        return lines


def explain_result(source: Result | SupportsResult, *, label: str | None = None, include_metadata: bool = False) -> ResultExplanation:
    result=normalize_result_source(source)
    return ResultExplanation(result.status, result.mode, _clean_optional(label), _STATUS_HEADLINES[result.status], None if result.value is None else repr(result.value), tuple(result.assumptions), tuple(result.justification) or _default_justification(result), tuple(result.proof_outline), dict(result.metadata) if include_metadata else {})


def render_result(source: Result | SupportsResult, *, label: str | None = None, style: str = "plain", include_metadata: bool = False) -> str:
    e=explain_result(source, label=label, include_metadata=include_metadata)
    if style == "plain": return "\n".join(e.plain_lines(include_metadata=include_metadata))
    if style == "markdown": return "\n".join(e.markdown_lines(include_metadata=include_metadata))
    raise ValueError("style must be 'plain' or 'markdown'")


def render_result_collection(sources: Iterable[Result | SupportsResult], *, labels: Iterable[str] | None = None, style: str = "plain", include_metadata: bool = False) -> str:
    source_list=list(sources); label_list=list(labels) if labels is not None else [None]*len(source_list)
    if len(label_list) != len(source_list): raise ValueError("labels length must match sources length")
    sep="\n\n---\n\n" if style == "markdown" else "\n---\n"
    return sep.join(render_result(source, label=label, style=style, include_metadata=include_metadata) for source, label in zip(source_list, label_list))


def _default_justification(result: Result) -> tuple[str, ...]:
    if result.status == "unknown": return ("No exact witness or theorem assumptions were supplied.",)
    if result.status == "conditional": return ("The conclusion must be read together with its assumptions.",)
    if result.mode == "theorem": return ("The conclusion is recorded as theorem-based.",)
    return ("The conclusion is recorded by the result contract.",)


def _clean_optional(value: str | None) -> str | None:
    if value is None: return None
    text=str(value).strip(); return text or None


def _extend_section(lines: list[str], title: str, values: Iterable[str]) -> None:
    items=[str(v).strip() for v in values if str(v).strip()]
    if items:
        lines.append(f"{title}:"); lines.extend(f"- {item}" for item in items)


def _extend_markdown_section(lines: list[str], title: str, values: Iterable[str]) -> None:
    items=[str(v).strip() for v in values if str(v).strip()]
    if items:
        lines.extend(["", f"**{title}**"]); lines.extend(f"- {item}" for item in items)
