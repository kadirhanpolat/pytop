"""Known-answer tests for field-coefficient and relative homology."""

from __future__ import annotations

from pytop import (
    betti_numbers,
    betti_numbers_over,
    relative_betti_numbers,
    relative_homology,
)
from pytop.simplicial_complexes import generated_subcomplex


def _sphere():
    return generated_subcomplex([{1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}])


def _torus():
    triangles = []
    for i in range(3):
        for j in range(3):
            a = (i % 3, j % 3)
            b = ((i + 1) % 3, j % 3)
            c = (i % 3, (j + 1) % 3)
            d = ((i + 1) % 3, (j + 1) % 3)
            triangles.append({a, b, c})
            triangles.append({b, d, c})
    return generated_subcomplex(triangles)


def _real_projective_plane():
    facets = [
        {1, 2, 3}, {1, 3, 4}, {1, 4, 5}, {1, 5, 6}, {1, 2, 6},
        {2, 3, 5}, {2, 4, 5}, {2, 4, 6}, {3, 4, 6}, {3, 5, 6},
    ]
    return generated_subcomplex(facets)


# --------------------------------------------------------------------------
# Coefficient dependence — the RP^2 headline
# --------------------------------------------------------------------------

def test_rp2_homology_is_coefficient_dependent():
    rp2 = _real_projective_plane()
    # Over Z: H1 = Z/2 (free rank 0, torsion)
    assert betti_numbers(rp2) == (1, 0, 0)
    # Over Q: torsion vanishes -> same Betti as the integral free ranks
    assert betti_numbers_over(rp2, "Q") == (1, 0, 0)
    # Over Z/2: the torsion becomes a visible class -> b1 = b2 = 1
    assert betti_numbers_over(rp2, 2) == (1, 1, 1)


def test_rp2_over_odd_prime_matches_q():
    rp2 = _real_projective_plane()
    assert betti_numbers_over(rp2, 3) == (1, 0, 0)  # odd prime does not see 2-torsion


# --------------------------------------------------------------------------
# Coefficient independence for torsion-free spaces
# --------------------------------------------------------------------------

def test_sphere_betti_independent_of_coefficients():
    s2 = _sphere()
    assert betti_numbers(s2) == (1, 0, 1)
    assert betti_numbers_over(s2, "Q") == (1, 0, 1)
    assert betti_numbers_over(s2, 2) == (1, 0, 1)
    assert betti_numbers_over(s2, 5) == (1, 0, 1)


def test_torus_betti_independent_of_coefficients():
    t2 = _torus()
    assert betti_numbers_over(t2, "Q") == (1, 2, 1)
    assert betti_numbers_over(t2, 2) == (1, 2, 1)


# --------------------------------------------------------------------------
# Euler characteristic is coefficient independent
# --------------------------------------------------------------------------

def test_euler_characteristic_coefficient_independent():
    for builder in (_sphere, _torus, _real_projective_plane):
        complex_obj = builder()
        chi_q = sum((-1) ** k * b for k, b in enumerate(betti_numbers_over(complex_obj, "Q")))
        chi_2 = sum((-1) ** k * b for k, b in enumerate(betti_numbers_over(complex_obj, 2)))
        assert chi_q == chi_2 == complex_obj.euler_characteristic()


# --------------------------------------------------------------------------
# Relative homology: H_*(D^2, ∂D^2) = Z in degree 2
# --------------------------------------------------------------------------

def test_relative_homology_disk_mod_boundary():
    disk = generated_subcomplex([{1, 2, 3}])           # filled triangle
    boundary = generated_subcomplex([{1, 2}, {2, 3}, {1, 3}])  # its boundary circle
    h2 = relative_homology(disk, boundary, 2)
    assert h2.betti == 1 and h2.torsion == ()
    assert relative_betti_numbers(disk, boundary) == (0, 0, 1)


def test_relative_homology_rejects_non_subcomplex():
    disk = generated_subcomplex([{1, 2, 3}])
    other = generated_subcomplex([{7, 8}])
    import pytest

    with pytest.raises(ValueError):
        relative_homology(disk, other, 1)
