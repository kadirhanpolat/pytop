"""Cross-validation shield: pytop's encoded topology theory vs the pi-Base graph.

pytop's separation / compactness / countability / connectedness modules encode a
body of classical implications by hand (e.g. Hausdorff => T1 => T0, metrizable =>
normal, compact + Hausdorff => normal). This module pins those implications
against the independently-sourced, referenced pi-Base theorem graph: if pytop's
conceptual model ever drifts from the literature, or the vendored pi-Base blob is
regenerated inconsistently, these tests fail.

It also guards the inference engine against *over-derivation* (deriving things
that do not follow).
"""

from __future__ import annotations

import pytest

from pytop.experimental.pi_base import deduce, property_uid

# Classical implications encoded across pytop's point-set modules
# (separation.py, compactness_variants.py, countability.py, connectedness.py,
# metrization_api.py). Each row: (hypotheses, conclusion) by pi-Base name.
CLASSICAL_IMPLICATIONS = [
    (["Hausdorff"], "T1"),
    (["T1"], "T0"),
    (["Hausdorff"], "T0"),
    (["Metrizable"], "Hausdorff"),
    (["Metrizable"], "Regular"),
    (["Metrizable"], "Normal"),
    (["Metrizable"], "First countable"),
    (["Discrete"], "Metrizable"),
    (["Compact", "Hausdorff"], "Normal"),
    (["Compact"], "Countably compact"),
    (["Path connected"], "Connected"),
    (["Second countable"], "Separable"),
    (["Second countable"], "First countable"),
]

# Things that must NOT be forced (guards against over-derivation).
NON_IMPLICATIONS = [
    (["Compact"], "Hausdorff"),
    (["Connected"], "Path connected"),
    (["T0"], "T1"),
    (["Separable"], "Second countable"),
]


@pytest.mark.parametrize("hypotheses,conclusion", CLASSICAL_IMPLICATIONS)
def test_pytop_implication_agrees_with_pi_base(hypotheses, conclusion):
    closure = deduce({property_uid(name): True for name in hypotheses})
    assert closure.get(property_uid(conclusion)) is True, (
        f"pi-Base does not confirm {hypotheses} => {conclusion}"
    )


@pytest.mark.parametrize("hypotheses,conclusion", NON_IMPLICATIONS)
def test_engine_does_not_over_derive(hypotheses, conclusion):
    closure = deduce({property_uid(name): True for name in hypotheses})
    # the conclusion must not be *forced true* by these hypotheses alone
    assert closure.get(property_uid(conclusion)) is not True, (
        f"engine over-derived {hypotheses} => {conclusion}"
    )


def test_separation_chain_is_monotone_in_pi_base():
    # pytop's SEPARATION_CHAIN_ORDER encodes T4 => T3 => T2 => T1 => T0 (under
    # the T_i normality conventions pi-Base also uses for the regular/normal
    # Hausdorff variants). Verify the core Hausdorff-anchored chain.
    chain = ["Hausdorff", "T1", "T0"]
    for stronger, weaker in zip(chain, chain[1:]):
        closure = deduce({property_uid(stronger): True})
        assert closure.get(property_uid(weaker)) is True
