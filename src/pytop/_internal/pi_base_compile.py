"""Compile the pi-Base topology dataset into a compact JSON blob for pytop.

pi-Base (https://topology.pi-base.org, repo ``pi-base/data``) is a community
database of topological spaces by Steven Clontz and James Dabbs, licensed under
Creative Commons Attribution 4.0 (CC BY 4.0). This developer tool reads a local
checkout of that repository and emits a compact, dependency-free JSON file that
``pytop.experimental.pi_base`` loads at runtime (with stdlib ``json`` only).

This module lives in ``_internal`` (developer tooling, not part of the public
API) and may use PyYAML to parse the source frontmatter. The emitted blob does
NOT contain pi-Base prose/proofs -- only structured facts (property names and
aliases, space names and aliases, the implication theorems, and the asserted
space/property traits) plus the required attribution.

Usage::

    py -3.14 -m pytop._internal.pi_base_compile --source <path-to-pi-base/data> \
        --out src/pytop/experimental/_pi_base_data.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml  # developer-only dependency; never imported by shipped runtime code

ATTRIBUTION = (
    "Topological-space facts derived from pi-Base "
    "(https://topology.pi-base.org, repo pi-base/data), "
    "Copyright 2014-2025 Steven Clontz and James Dabbs, "
    "licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). "
    "DOI: 10.5281/zenodo.15850332. Only structured facts are reproduced here."
)


def _frontmatter(path: Path) -> dict[str, Any]:
    """Return the YAML frontmatter of a pi-Base markdown file as a dict."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data = yaml.safe_load(block)
    return data if isinstance(data, dict) else {}


_META_PATTERNS: list[tuple[str, str]] = [
    # check the "with respect to" variants before the plain "hereditary"
    ("hereditary with respect to closed", "hereditary_closed"),
    ("hereditary with respect to open", "hereditary_open"),
    ("hereditary with respect to clopen", "hereditary_clopen"),
    ("hereditary with respect to dense", "hereditary_dense"),
    ("preserved by arbitrary products", "products_arbitrary"),
    ("preserved by finite products", "products_finite"),
    ("preserved by countable products", "products_countable"),
    ("preserved by arbitrary disjoint unions", "sums_arbitrary"),
    ("preserved by finite disjoint unions", "sums_finite"),
    ("preserved by countable disjoint unions", "sums_countable"),
    ("preserved in any coarser topology", "coarser"),
    ("preserved in any finer topology", "finer"),
    ("preserved by quotient maps", "quotients"),
    ("preserved by retractions", "retracts"),
    ("preserved by homotopy equivalences", "homotopy"),
    ("-products", "sigma_products"),  # matches $\Sigma$-products
]


def _meta_flags(text: str) -> list[str]:
    """Extract structured preservation/heredity flags from a property's prose.

    Parses the regular "This property is ..." meta-property bullets. Negated
    statements ("... is not ...") are skipped (silence is not a negative claim).
    """

    flags: set[str] = set()
    marker = "This property is "
    for line in text.splitlines():
        index = line.find(marker)
        if index == -1:
            continue
        phrase = line[index + len(marker):].strip()
        if phrase.startswith("not "):
            continue
        for needle, flag in _META_PATTERNS:
            if needle in phrase:
                flags.add(flag)
        if phrase.startswith("hereditary") and "with respect to" not in phrase:
            flags.add("hereditary")
    return sorted(flags)


def _compile_properties(source: Path) -> dict[str, dict[str, Any]]:
    properties: dict[str, dict[str, Any]] = {}
    for path in sorted((source / "properties").glob("P*.md")):
        front = _frontmatter(path)
        uid = front.get("uid")
        if not uid:
            continue
        properties[uid] = {
            "name": front.get("name", uid),
            "aliases": [str(a) for a in (front.get("aliases") or [])],
            "meta": _meta_flags(path.read_text(encoding="utf-8")),
        }
    return properties


def _normalize_formula(node: Any) -> dict[str, Any]:
    """Normalize a pi-Base property formula, preserving and/or/not structure.

    A formula is either an atom map ``{Pxxxxxx: bool, ...}`` (a conjunction of
    atoms) or a compound ``{and: [...]}`` / ``{or: [...]}`` / ``{not: formula}``.
    """

    if not isinstance(node, dict):
        raise ValueError(f"Unexpected formula node: {node!r}")
    if "and" in node:
        return {"and": [_normalize_formula(child) for child in node["and"]]}
    if "or" in node:
        return {"or": [_normalize_formula(child) for child in node["or"]]}
    if "not" in node:
        return {"not": _normalize_formula(node["not"])}
    return {str(prop): bool(value) for prop, value in node.items()}


def _compile_theorems(source: Path) -> list[dict[str, Any]]:
    theorems: list[dict[str, Any]] = []
    for path in sorted((source / "theorems").glob("T*.md")):
        front = _frontmatter(path)
        uid = front.get("uid")
        hypothesis = front.get("if")
        conclusion = front.get("then")
        if not uid or not isinstance(hypothesis, dict) or not isinstance(conclusion, dict):
            continue
        theorems.append(
            {
                "uid": uid,
                "if": _normalize_formula(hypothesis),
                "then": _normalize_formula(conclusion),
            }
        )
    return theorems


def _compile_spaces(source: Path) -> tuple[dict[str, dict[str, Any]], list[list[Any]]]:
    spaces: dict[str, dict[str, Any]] = {}
    traits: list[list[Any]] = []
    for space_dir in sorted((source / "spaces").glob("S*/")):
        readme = space_dir / "README.md"
        if not readme.exists():
            continue
        front = _frontmatter(readme)
        uid = front.get("uid")
        if not uid:
            continue
        record: dict[str, Any] = {
            "name": front.get("name", uid),
            "aliases": [str(a) for a in (front.get("aliases") or [])],
        }
        if "counterexamples_id" in front:
            record["counterexamples_id"] = front["counterexamples_id"]
        spaces[uid] = record
        for trait_path in sorted((space_dir / "properties").glob("P*.md")):
            trait = _frontmatter(trait_path)
            if "space" in trait and "property" in trait and "value" in trait:
                traits.append([trait["space"], trait["property"], bool(trait["value"])])
    return spaces, traits


def compile_dataset(source: Path) -> dict[str, Any]:
    properties = _compile_properties(source)
    theorems = _compile_theorems(source)
    spaces, traits = _compile_spaces(source)
    return {
        "_attribution": ATTRIBUTION,
        "_counts": {
            "properties": len(properties),
            "theorems": len(theorems),
            "spaces": len(spaces),
            "traits": len(traits),
        },
        "properties": properties,
        "theorems": theorems,
        "spaces": spaces,
        "traits": traits,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile pi-Base data into a pytop JSON blob.")
    parser.add_argument("--source", required=True, help="Path to a pi-base/data checkout.")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    args = parser.parse_args()

    dataset = compile_dataset(Path(args.source))
    out_path = Path(args.out)
    out_path.write_text(
        json.dumps(dataset, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    counts = dataset["_counts"]
    print(
        f"Wrote {out_path} | properties={counts['properties']} "
        f"theorems={counts['theorems']} spaces={counts['spaces']} traits={counts['traits']}"
    )


if __name__ == "__main__":
    main()
