"""Property-based / cross-engine differential tests (Phase 4 — correctness).

Unlike the per-module known-answer tests, these exercise *mathematical
invariants* and *cross-engine consistency* over many randomly generated inputs
(deterministic — every generator is seeded). They are the "correctness bar" of
the roadmap: they catch regressions that a fixed example might miss, and pin
independent engines against each other.

No external dependencies — randomness comes from the stdlib `random` module with
fixed seeds, so failures are reproducible.

Properties checked
------------------
* **Homology** — Euler–Poincaré (`χ` via homology = `χ` via face counts);
  rational Betti numbers = integral free ranks; `b_i(ℤ/p) ≥ b_i(ℚ)`.
* **Knots** — HOMFLY-PT is invariant under Markov stabilisation (±) and braid
  conjugation; the braid Alexander polynomial is palindromic for knots; the
  HOMFLY-PT `a=1` specialisation reproduces the Burau Alexander polynomial.
* **Dehn surgery** — `|H₁| = |det|` of the framing matrix (cross-checked with an
  independent fraction-free determinant); homology sphere ⟺ unimodular.
* **Lens spaces** — homeomorphic ⇒ homotopy equivalent; both relations are
  reflexive and symmetric.
"""

from __future__ import annotations

import random
from math import gcd

import pytest

from pytop import (
    alexander_polynomial_from_braid,
    are_lens_spaces_homeomorphic,
    are_lens_spaces_homotopy_equivalent,
    betti_numbers,
    betti_numbers_over,
    first_homology_of_surgery,
    generated_subcomplex,
    homfly_polynomial,
)
from pytop.homology import euler_characteristic_via_homology
from pytop.knot_invariants import _normalize_alexander


# ---------------------------------------------------------------------------
# Generators and helpers
# ---------------------------------------------------------------------------


def _random_complex(rng: random.Random):
    n_vertices = rng.randint(3, 6)
    vertices = list(range(n_vertices))
    facets = []
    for _ in range(rng.randint(1, 5)):
        size = rng.randint(1, 3)
        facets.append(frozenset(rng.sample(vertices, size)))
    return generated_subcomplex(facets)


def _random_braid(rng: random.Random, n_strands: int, length: int) -> list[int]:
    generators = [g for g in range(-(n_strands - 1), n_strands) if g != 0]
    return [rng.choice(generators) for _ in range(length)]


def _closure_component_count(word: list[int], n_strands: int) -> int:
    permutation = list(range(n_strands))
    for letter in word:
        i = abs(letter) - 1
        permutation[i], permutation[i + 1] = permutation[i + 1], permutation[i]
    seen = [False] * n_strands
    cycles = 0
    for start in range(n_strands):
        if not seen[start]:
            cycles += 1
            node = start
            while not seen[node]:
                seen[node] = True
                node = permutation[node]
    return cycles


def _bareiss_determinant(matrix: list[list[int]]) -> int:
    """Exact integer determinant via fraction-free Bareiss elimination."""
    n = len(matrix)
    if n == 0:
        return 1
    M = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if swap is None:
                return 0
            M[k], M[swap] = M[swap], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // previous
        previous = M[k][k]
    return sign * M[n - 1][n - 1]


def _random_symmetric_matrix(rng: random.Random, n: int, lo: int = -3, hi: int = 3):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            value = rng.randint(lo, hi)
            matrix[i][j] = value
            matrix[j][i] = value
    return matrix


# ---------------------------------------------------------------------------
# Homology invariants
# ---------------------------------------------------------------------------


class TestHomologyProperties:
    def test_euler_poincare(self):
        rng = random.Random(20260618)
        for _ in range(60):
            complex_obj = _random_complex(rng)
            assert euler_characteristic_via_homology(complex_obj) == (
                complex_obj.euler_characteristic()
            )

    def test_rational_betti_equals_integral_free_rank(self):
        rng = random.Random(11)
        for _ in range(60):
            complex_obj = _random_complex(rng)
            assert betti_numbers_over(complex_obj, "Q") == betti_numbers(complex_obj)

    def test_mod_p_betti_dominates_rational(self):
        # Over ℤ/p, torsion can only *raise* a Betti number: b_i(ℤ/p) ≥ b_i(ℚ).
        rng = random.Random(22)
        for _ in range(40):
            complex_obj = _random_complex(rng)
            rational = betti_numbers_over(complex_obj, "Q")
            for p in (2, 3):
                mod_p = betti_numbers_over(complex_obj, p)
                assert all(m >= q for m, q in zip(mod_p, rational))


# ---------------------------------------------------------------------------
# Knot-invariant invariants
# ---------------------------------------------------------------------------


class TestKnotInvariantProperties:
    def test_homfly_markov_stabilisation(self):
        # closure(β in Bₙ) = closure(β·σₙ^{±1} in Bₙ₊₁)
        rng = random.Random(101)
        for _ in range(12):
            n = rng.randint(2, 3)
            word = _random_braid(rng, n, rng.randint(0, 4))
            base = homfly_polynomial(word, n)
            assert homfly_polynomial(word + [n], n + 1) == base
            assert homfly_polynomial(word + [-n], n + 1) == base

    def test_homfly_conjugation_invariance(self):
        # closure(αβ) = closure(βα)
        rng = random.Random(202)
        for _ in range(12):
            n = rng.randint(2, 3)
            a = _random_braid(rng, n, rng.randint(1, 3))
            b = _random_braid(rng, n, rng.randint(1, 3))
            assert homfly_polynomial(a + b, n) == homfly_polynomial(b + a, n)

    def test_braid_alexander_is_palindromic_for_knots(self):
        # Δ_K(t) ≐ Δ_K(t⁻¹): the normalised representative is symmetric.
        rng = random.Random(303)
        checked = 0
        for _ in range(60):
            n = rng.randint(2, 4)
            word = _random_braid(rng, n, rng.randint(1, 6))
            if _closure_component_count(word, n) != 1:
                continue  # restrict to knots
            poly = alexander_polynomial_from_braid(word, n)
            for exponent, coeff in poly.coeffs.items():
                assert poly.coeffs.get(-exponent, 0) == coeff
            checked += 1
        assert checked >= 5  # the seed actually exercises the property

    def test_homfly_specialises_to_braid_alexander(self):
        # Two independent engines: skein HOMFLY (a=1) vs reduced Burau.
        rng = random.Random(404)
        checked = 0
        for _ in range(40):
            n = rng.randint(2, 3)
            word = _random_braid(rng, n, rng.randint(1, 5))
            if _closure_component_count(word, n) != 1:
                continue
            from_homfly = _normalize_alexander(homfly_polynomial(word, n).to_alexander())
            from_burau = alexander_polynomial_from_braid(word, n)
            assert from_homfly == from_burau
            checked += 1
        assert checked >= 5


# ---------------------------------------------------------------------------
# Dehn surgery invariants
# ---------------------------------------------------------------------------


class TestSurgeryProperties:
    def test_order_equals_abs_determinant(self):
        rng = random.Random(505)
        for _ in range(50):
            n = rng.randint(1, 4)
            matrix = _random_symmetric_matrix(rng, n)
            determinant = _bareiss_determinant(matrix)
            framings = [matrix[i][i] for i in range(n)]
            result = first_homology_of_surgery(framings, matrix)
            if determinant == 0:
                assert result.free_rank > 0
                assert result.order is None
            else:
                assert result.order == abs(determinant)

    def test_homology_sphere_iff_unimodular(self):
        rng = random.Random(606)
        for _ in range(50):
            n = rng.randint(1, 4)
            matrix = _random_symmetric_matrix(rng, n)
            determinant = _bareiss_determinant(matrix)
            framings = [matrix[i][i] for i in range(n)]
            result = first_homology_of_surgery(framings, matrix)
            assert result.is_homology_sphere == (abs(determinant) == 1)


# ---------------------------------------------------------------------------
# Lens space classification invariants
# ---------------------------------------------------------------------------


class TestLensSpaceProperties:
    def _random_pq(self, rng: random.Random) -> tuple[int, int]:
        p = rng.randint(2, 30)
        q = rng.choice([x for x in range(1, p) if gcd(x, p) == 1])
        return p, q

    def test_homeomorphic_implies_homotopy_equivalent(self):
        rng = random.Random(707)
        for _ in range(80):
            p, q1 = self._random_pq(rng)
            q2 = rng.choice([x for x in range(1, p) if gcd(x, p) == 1])
            if are_lens_spaces_homeomorphic(p, q1, q2):
                assert are_lens_spaces_homotopy_equivalent(p, q1, q2)

    def test_relations_reflexive_and_symmetric(self):
        rng = random.Random(808)
        for _ in range(80):
            p, q1 = self._random_pq(rng)
            q2 = rng.choice([x for x in range(1, p) if gcd(x, p) == 1])
            assert are_lens_spaces_homeomorphic(p, q1, q1)
            assert are_lens_spaces_homotopy_equivalent(p, q1, q1)
            assert are_lens_spaces_homeomorphic(p, q1, q2) == are_lens_spaces_homeomorphic(
                p, q2, q1
            )
            assert are_lens_spaces_homotopy_equivalent(
                p, q1, q2
            ) == are_lens_spaces_homotopy_equivalent(p, q2, q1)
