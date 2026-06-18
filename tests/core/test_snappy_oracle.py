"""Differential tests against SnapPy — opt-in, Docker-based (Phase 4, P4.8).

SnapPy is the gold-standard software for 3-manifolds — the one independent
oracle for pytop's Dehn-surgery homology (`dehn_surgery`), which no other oracle
(sympy/flint = linear algebra, GUDHI = TDA, networkx = planarity, numpy =
signature, SageMath = knot polynomials + groups) covers. SnapPy cannot be
installed natively on this platform (Windows / Python 3.14), so it runs in a
local ``pytop-snappy`` Docker image (Python 3.12 + ``snappy``) as a *subprocess*
oracle.

All reference values come from a single batched SnapPy run (one container),
parsed, and compared to pytop. Conveniently, SnapPy's ``elementary_divisors``
already returns the invariant-factor (Smith) form — exactly what
``first_homology_of_surgery`` produces from the Smith normal form — so they match
directly (e.g. ``Z/2 ⊕ Z/3`` is reported as ``[6]`` by both).

The module is **opt-in**: skipped unless ``PYTOP_SNAPPY_ORACLE=1``, so the
default suite is neither slowed nor made to depend on Docker. Build the image
once with::

    docker build -t pytop-snappy - <<'EOF'
    FROM python:3.12
    RUN pip install snappy
    EOF

then run ``PYTOP_SNAPPY_ORACLE=1 pytest tests/core/test_snappy_oracle.py``.
"""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess

import pytest

from pytop import first_homology_of_surgery

pytestmark = pytest.mark.skipif(
    os.environ.get("PYTOP_SNAPPY_ORACLE") != "1",
    reason="set PYTOP_SNAPPY_ORACLE=1 to run the (Docker-based) SnapPy oracle",
)

SNAPPY_IMAGE = "pytop-snappy"

# (p, q) Dehn fillings of the figure-eight knot complement m004 → H₁ = ℤ/p,
# matching p/q surgery on a knot.
KNOT_FILLS = [(5, 1), (7, 2), (3, 1), (0, 1), (1, 1)]
# (a, b) means filling the two cusps of the Whitehead link (lk = 0) with
# slopes (a, 1) and (b, 1) → H₁ = ℤ/a ⊕ ℤ/b.
WHITE_FILLS = [(2, 3), (5, 7), (4, 0)]

SNAPPY_SCRIPT = """
import snappy
for (p, q) in {knot}:
    K = snappy.Manifold('m004'); K.dehn_fill((p, q))
    print('KNOT_%d_%d' % (p, q), list(K.homology().elementary_divisors()))
for (a, b) in {white}:
    L = snappy.Manifold('L5a1'); L.dehn_fill([(a, 1), (b, 1)])
    print('WHITE_%d_%d' % (a, b), list(L.homology().elementary_divisors()))
""".format(knot=KNOT_FILLS, white=WHITE_FILLS)

_KEY = re.compile(r"\b(KNOT_\d+_\d+|WHITE_\d+_\d+)\s+(\[.*\])")


@pytest.fixture(scope="module")
def snappy_output() -> dict[str, list[int]]:
    if shutil.which("docker") is None:
        pytest.skip("docker is not available")
    present = subprocess.run(
        ["docker", "images", "-q", SNAPPY_IMAGE],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if not present.stdout.strip():
        pytest.skip(f"{SNAPPY_IMAGE} image is not built")

    completed = subprocess.run(
        ["docker", "run", "--rm", SNAPPY_IMAGE, "python", "-c", SNAPPY_SCRIPT],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    output = completed.stdout + completed.stderr
    results: dict[str, list[int]] = {}
    for line in output.splitlines():
        match = _KEY.search(line)
        if match:
            results[match.group(1)] = ast.literal_eval(match.group(2))
    if "KNOT_5_1" not in results:
        pytest.skip(f"SnapPy produced no parseable output:\n{output[-800:]}")
    return results


def _from_divisors(divisors: list[int]) -> tuple[int, tuple[int, ...]]:
    free_rank = divisors.count(0)
    torsion = tuple(sorted(d for d in divisors if d > 1))
    return free_rank, torsion


def _from_pytop(result) -> tuple[int, tuple[int, ...]]:
    return result.free_rank, tuple(sorted(result.torsion))


class TestSnapPyKnotSurgery:
    @pytest.mark.parametrize("p,q", KNOT_FILLS)
    def test_figure_eight_surgery(self, snappy_output, p, q):
        snappy = _from_divisors(snappy_output[f"KNOT_{p}_{q}"])
        pytop = _from_pytop(first_homology_of_surgery([(p, q)]))
        assert snappy == pytop


class TestSnapPyLinkSurgery:
    @pytest.mark.parametrize("a,b", WHITE_FILLS)
    def test_whitehead_link_surgery(self, snappy_output, a, b):
        # Whitehead link has linking number 0 → H₁ = coker(diag(a, b)).
        snappy = _from_divisors(snappy_output[f"WHITE_{a}_{b}"])
        pytop = _from_pytop(
            first_homology_of_surgery([(a, 1), (b, 1)], [[0, 0], [0, 0]])
        )
        assert snappy == pytop
