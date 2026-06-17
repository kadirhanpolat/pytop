"""Property-reasoning engine: derive (and explain) properties of constructed spaces.

This is the milestone that ends the "encyclopedia vs calculator" split for the
point-set layer. For a *constructed* space it derives a property by combining:

* **construction-preservation theorems** (subspace → hereditary, product →
  productive, sum → coproduct-stable, quotient → image-stable),
* the **pi-Base implication graph** (to close the derived properties, e.g.
  Hausdorff ⟹ T1 ⟹ T0), and
* **computed / certified** verdicts at the leaves (from :mod:`predicates`).

It returns a :class:`Derivation` carrying the verdict *and a human-readable
explanation tree*, and it works on **infinite** constructions without enumeration.
A small :func:`synthesize` searches for a space meeting a property specification.

The preservation table below records standard theorems of general topology; each
is a mathematical fact (cross-checkable against pi-Base meta-properties).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..pi_base import deduce, property_uid
from .constructed import ProductSpace, SumSpace
from .core import Space, Verdict
from .predicates import (
    is_compact,
    is_connected,
    is_hausdorff,
    is_normal,
    is_regular,
    is_t0,
    is_t1,
)
from .representations import FiniteSpace, discrete_finite_space

PROPERTY_KEYS = ("T0", "T1", "T2", "regular", "normal", "compact", "connected")

_PREDICATES = {
    "T0": is_t0,
    "T1": is_t1,
    "T2": is_hausdorff,
    "regular": is_regular,
    "normal": is_normal,
    "compact": is_compact,
    "connected": is_connected,
}

# Map our property keys to pi-Base property names (for the implication closure).
_PI_NAME = {
    "T0": "T0",
    "T1": "T1",
    "T2": "Hausdorff",
    "regular": "Regular",
    "normal": "Normal",
    "compact": "Compact",
    "connected": "Connected",
}

# Properties preserved by each construction (operands have P ⟹ result has P).
# These are standard preservation theorems for general topology.
PRESERVATION: dict[str, frozenset[str]] = {
    "subspace": frozenset({"T0", "T1", "T2", "regular"}),                 # hereditary
    "product": frozenset({"T0", "T1", "T2", "regular", "compact", "connected"}),  # productive (Tychonoff)
    "sum": frozenset({"T0", "T1", "T2", "regular", "normal", "compact"}),  # finite coproduct
    "quotient": frozenset({"compact", "connected"}),                      # continuous-image stable
}


@dataclass(frozen=True)
class Derivation:
    """A property verdict for a space together with its justification tree."""

    prop: str
    verdict: Verdict
    rule: str
    space: str = ""
    subderivations: tuple[Derivation, ...] = field(default_factory=tuple)

    def explain(self, indent: int = 0) -> str:
        pad = "  " * indent
        status = {True: "holds", False: "fails", None: "undecided"}[self.verdict.value]
        lines = [f"{pad}- {self.prop} {status} for {self.space}: {self.rule}"]
        for sub in self.subderivations:
            lines.append(sub.explain(indent + 1))
        return "\n".join(lines)


def _provable_true_props(space: Space) -> dict[str, Derivation]:
    """Return the properties the space *provably has*, each with a derivation."""

    proven: dict[str, Derivation] = {}
    if space.construction is None:
        for prop, predicate in _PREDICATES.items():
            verdict = predicate(space)
            if verdict.value is True:
                proven[prop] = Derivation(prop, verdict, f"leaf: {verdict.reason}", space=space.name)
        return proven

    kind = space.construction.kind
    operands = space.construction.operands
    operand_props = [_provable_true_props(op) for op in operands]
    for prop in PRESERVATION.get(kind, frozenset()):
        if all(prop in op for op in operand_props):
            subs = tuple(op[prop] for op in operand_props)
            proven[prop] = Derivation(
                prop,
                Verdict.true(reason=f"{prop} is preserved by {kind}"),
                f"{prop} is preserved by {kind}",
                space=space.name,
                subderivations=subs,
            )
    return proven


def _pi_base_closure(props: set[str]) -> set[str]:
    """Close a set of our property keys under the pi-Base implication graph."""

    if not props:
        return set()
    known = {property_uid(_PI_NAME[p]): True for p in props}
    closed = deduce(known)
    result: set[str] = set()
    for our_key, pi_name in _PI_NAME.items():
        if closed.get(property_uid(pi_name)) is True:
            result.add(our_key)
    return result


def _structural_false(space: Space, prop: str) -> Derivation | None:
    construction = space.construction
    if construction is None:
        return None
    if construction.kind == "sum" and prop == "connected" and len(construction.operands) >= 2:
        return Derivation(
            prop,
            Verdict.false(
                reason="a topological sum of two or more nonempty spaces is disconnected",
                counterexample="each summand is a nontrivial clopen set",
            ),
            "a sum of >= 2 nonempty spaces is disconnected",
            space=space.name,
        )
    return None


def derive(space: Space, prop: str) -> Derivation:
    """Derive whether ``space`` has property ``prop``, with an explanation.

    Combines construction-preservation, the pi-Base implication graph, and
    computed/certified leaf verdicts. Returns a :class:`Derivation` (undecided
    when no rule applies and the space cannot be computed directly).
    """

    if prop not in PROPERTY_KEYS:
        raise ValueError(f"Unknown property {prop!r}; expected one of {PROPERTY_KEYS}.")

    proven = _provable_true_props(space)
    if prop in proven:
        return proven[prop]

    if prop in _pi_base_closure(set(proven)):
        return Derivation(
            prop,
            Verdict.true(reason=f"implied via pi-Base from {sorted(proven)}"),
            f"implied by the pi-Base graph from {sorted(proven)}",
            space=space.name,
        )

    structural = _structural_false(space, prop)
    if structural is not None:
        return structural

    if space.construction is None:
        verdict = _PREDICATES[prop](space)
        return Derivation(prop, verdict, f"leaf: {verdict.reason}", space=space.name)

    return Derivation(
        prop,
        Verdict.undecidable(
            reason=f"no preservation rule yields {prop!r} for a {space.construction.kind}"
        ),
        f"no preservation rule for {prop} under {space.construction.kind}",
        space=space.name,
    )


def explain(space: Space, prop: str) -> str:
    """Return the human-readable derivation tree for ``derive(space, prop)``."""

    return derive(space, prop).explain()


def _default_library() -> list[Space]:
    return [
        FiniteSpace("Sierpinski", {0, 1}, [set(), {0}, {0, 1}]),
        discrete_finite_space({0, 1}, name="discrete2"),
        discrete_finite_space({0, 1, 2}, name="discrete3"),
        FiniteSpace("indiscrete2", {0, 1}, [set(), {0, 1}]),
    ]


def synthesize(has=(), lacks=(), library: list[Space] | None = None) -> Space | None:
    """Search for a space that *has* every property in ``has`` and *lacks* each in ``lacks``.

    Searches a base library plus its pairwise products and sums (bounded), using
    :func:`derive`. Returns the first witness, or ``None`` if none is found within
    the search (the bound, not a proof of non-existence).
    """

    has, lacks = tuple(has), tuple(lacks)
    base = list(library) if library is not None else _default_library()
    candidates: list[Space] = list(base)
    for a in base:
        for b in base:
            candidates.append(ProductSpace([a, b]))
            candidates.append(SumSpace([a, b]))

    for space in candidates:
        if all(derive(space, p).verdict.value is True for p in has) and all(
            derive(space, p).verdict.value is False for p in lacks
        ):
            return space
    return None


__all__ = [
    "PROPERTY_KEYS",
    "PRESERVATION",
    "Derivation",
    "derive",
    "explain",
    "synthesize",
]
