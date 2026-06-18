"""Differential tests against SageMath — opt-in, Docker-based (Phase 4, P4.7).

SageMath bundles independent, mature implementations that pytop has no other
oracle for: its own knot-polynomial algorithms and **GAP**-backed group theory.
Sage cannot run natively on this platform (Windows / Python 3.14), so it is
invoked through the official ``sagemath/sagemath`` Docker image as a *subprocess*
oracle.

Because each container start costs ~20–30 s, **all** reference values are
computed in a single batched Sage run (one container), parsed, and compared to
pytop. The whole module is **opt-in**: it is skipped unless ``PYTOP_SAGE_ORACLE=1``
is set, so the default test suite is neither slowed nor made to depend on Docker.

Run it with::

    PYTOP_SAGE_ORACLE=1 pytest tests/core/test_sage_oracle.py
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
from fractions import Fraction

import pytest

from pytop import (
    KnotDiagram,
    alexander_polynomial_from_braid,
    jones_polynomial,
    van_kampen_klein_bottle,
    van_kampen_real_projective_plane,
    van_kampen_torus,
    van_kampen_wedge_circles,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("PYTOP_SAGE_ORACLE") != "1",
    reason="set PYTOP_SAGE_ORACLE=1 to run the (slow, Docker-based) SageMath oracle",
)

SAGE_IMAGE = "sagemath/sagemath"

# One batched script: knot polynomials + GAP group abelianisations.
SAGE_SCRIPT = r"""
K31 = Knots().from_table(3, 1); K41 = Knots().from_table(4, 1)
print('ALEX_3_1', dict(K31.alexander_polynomial().dict()))
print('ALEX_4_1', dict(K41.alexander_polynomial().dict()))
for nm, K in [('3_1', K31), ('4_1', K41)]:
    jp = K.jones_polynomial()
    print('JEVAL_' + nm, [str(QQ(jp.subs(t=2))), str(QQ(jp.subs(t=5)))])
G2 = FreeGroup('a,b')
print('AB_KLEIN', sorted((G2 / [G2([1, 2, 1, -2])]).abelian_invariants()))
print('AB_TORUS', sorted((G2 / [G2([1, 2, -1, -2])]).abelian_invariants()))
print('AB_RP2', sorted((FreeGroup('a') / [FreeGroup('a')([1, 1])]).abelian_invariants()))
print('AB_WEDGE3', sorted((FreeGroup('a,b,c') / []).abelian_invariants()))
"""

_KEY = re.compile(r"\b(ALEX_\d+_\d+|JEVAL_\d+_\d+|AB_[A-Z0-9]+)\s+(.*)$")


@pytest.fixture(scope="module")
def sage() -> dict[str, str]:
    """Run the batched Sage script once and return the parsed key→value map."""
    if shutil.which("docker") is None:
        pytest.skip("docker is not available")
    present = subprocess.run(
        ["docker", "images", "-q", SAGE_IMAGE],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if not present.stdout.strip():
        pytest.skip(f"{SAGE_IMAGE} image is not pulled")

    # SageMath's banner contains UTF-8 box-drawing characters; decode explicitly
    # as UTF-8 (not the Windows locale code page) and tolerate stray bytes.
    completed = subprocess.run(
        ["docker", "run", "-i", "--rm", SAGE_IMAGE, "sage"],
        input=SAGE_SCRIPT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    output = completed.stdout + completed.stderr
    results: dict[str, str] = {}
    for line in output.splitlines():
        match = _KEY.search(line)
        if match:
            results[match.group(1)] = match.group(2).strip()
    if "ALEX_3_1" not in results:
        pytest.skip(f"SageMath produced no parseable output:\n{output[-800:]}")
    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _equal_up_to_sign(a: dict[int, int], b: dict[int, int]) -> bool:
    return a == b or a == {exp: -coeff for exp, coeff in b.items()}


def _eval_laurent(laurent, value: int) -> Fraction:
    total = Fraction(0)
    for exponent, coeff in laurent.coeffs.items():
        total += Fraction(coeff) * Fraction(value) ** int(exponent)
    return total


def _sage_invariants(raw: str) -> tuple[int, tuple[int, ...]]:
    invariants = ast.literal_eval(raw)
    free_rank = invariants.count(0)
    torsion = tuple(sorted(x for x in invariants if x != 0))
    return free_rank, torsion


# ---------------------------------------------------------------------------
# Knot polynomials — Sage's independent algorithms
# ---------------------------------------------------------------------------


class TestSageKnotPolynomials:
    def test_alexander_trefoil(self, sage):
        sage_poly = ast.literal_eval(sage["ALEX_3_1"])
        pytop = alexander_polynomial_from_braid([1, 1, 1], 2)
        pytop_poly = {int(e): c for e, c in pytop.coeffs.items()}
        assert _equal_up_to_sign(sage_poly, pytop_poly)

    def test_alexander_figure_eight(self, sage):
        sage_poly = ast.literal_eval(sage["ALEX_4_1"])
        pytop = alexander_polynomial_from_braid([1, -2, 1, -2], 3)
        pytop_poly = {int(e): c for e, c in pytop.coeffs.items()}
        assert _equal_up_to_sign(sage_poly, pytop_poly)

    def test_jones_trefoil(self, sage):
        sage_values = [Fraction(x) for x in ast.literal_eval(sage["JEVAL_3_1"])]
        jp = jones_polynomial(
            KnotDiagram([(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)], signs=(-1, -1, -1))
        )
        assert [_eval_laurent(jp, 2), _eval_laurent(jp, 5)] == sage_values

    def test_jones_figure_eight(self, sage):
        sage_values = [Fraction(x) for x in ast.literal_eval(sage["JEVAL_4_1"])]
        jp = jones_polynomial(
            KnotDiagram(
                [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)],
                signs=(1, -1, 1, -1),
            )
        )
        assert [_eval_laurent(jp, 2), _eval_laurent(jp, 5)] == sage_values


# ---------------------------------------------------------------------------
# Group abelianisation — Sage's GAP backend vs van Kampen
# ---------------------------------------------------------------------------


class TestSageGroupTheory:
    @staticmethod
    def _pytop(result) -> tuple[int, tuple[int, ...]]:
        ab = result.abelianization
        return ab.betti, tuple(sorted(ab.torsion))

    def test_klein_bottle(self, sage):
        assert _sage_invariants(sage["AB_KLEIN"]) == self._pytop(van_kampen_klein_bottle())

    def test_torus(self, sage):
        assert _sage_invariants(sage["AB_TORUS"]) == self._pytop(van_kampen_torus())

    def test_real_projective_plane(self, sage):
        assert _sage_invariants(sage["AB_RP2"]) == self._pytop(
            van_kampen_real_projective_plane()
        )

    def test_wedge_of_three_circles(self, sage):
        assert _sage_invariants(sage["AB_WEDGE3"]) == self._pytop(
            van_kampen_wedge_circles(3)
        )
