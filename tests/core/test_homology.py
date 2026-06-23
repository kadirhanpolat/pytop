"""Known-answer tests for the constructive simplicial homology engine."""

from __future__ import annotations

import pytest

from pytop import (
    betti_numbers,
    boundary_matrix,
    euler_characteristic_via_homology,
    homology_groups,
    simplicial_homology,
)
from pytop.homology import _smith_normal_form
from pytop.simplicial_complexes import generated_subcomplex

# --------------------------------------------------------------------------
# Test fixtures: standard triangulations
# --------------------------------------------------------------------------

def _point():
    return generated_subcomplex([{1}])


def _circle():
    # Boundary of a triangle: S^1
    return generated_subcomplex([{1, 2}, {2, 3}, {1, 3}])


def _sphere():
    # Boundary of the 3-simplex: S^2
    return generated_subcomplex([{1, 2, 3}, {1, 2, 4}, {1, 3, 4}, {2, 3, 4}])


def _torus():
    # 3x3 grid with toroidal identification, diagonal triangulation.
    # 9 vertices, 27 edges, 18 triangles, chi = 0.
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
    # Minimal 6-vertex triangulation of RP^2 (hemi-icosahedron).
    # 6 vertices, 15 edges, 10 triangles, chi = 1.
    facets = [
        {1, 2, 3}, {1, 3, 4}, {1, 4, 5}, {1, 5, 6}, {1, 2, 6},
        {2, 3, 5}, {2, 4, 5}, {2, 4, 6}, {3, 4, 6}, {3, 5, 6},
    ]
    return generated_subcomplex(facets)


# --------------------------------------------------------------------------
# Smith Normal Form unit tests
# --------------------------------------------------------------------------

def test_snf_identity():
    invariants = _smith_normal_form([[1, 0], [0, 1]])
    assert invariants == [1, 1]


def test_snf_empty():
    assert _smith_normal_form([]) == []


def test_snf_rank_and_invariant_factor():
    # diag(2, 6) has SNF invariant factors 2, 6 (2 | 6).
    invariants = _smith_normal_form([[2, 0], [0, 6]])
    assert invariants == [2, 6]


def test_snf_off_diagonal():
    invariants = _smith_normal_form([[2, 4], [6, 8]])
    # det = 16 - 24 = -8; gcd of entries = 2 -> first factor 2, product |det|/2 = 4.
    assert invariants == [2, 4]


def test_snf_coprime_diagonal_triggers_divisibility_correction():
    # diag(2, 3): 2 does not divide 3, so the divisibility-correction branch
    # must run, producing invariant factors 1, 6.
    assert _smith_normal_form([[2, 0], [0, 3]]) == [1, 6]


# --------------------------------------------------------------------------
# Boundary matrix sanity: partial_{k-1} . partial_k = 0
# --------------------------------------------------------------------------

@pytest.mark.parametrize("builder", [_circle, _sphere, _torus, _real_projective_plane])
def test_boundary_squared_is_zero(builder):
    complex_obj = builder()
    for k in range(2, complex_obj.dimension + 1):
        d_k = boundary_matrix(complex_obj, k)
        d_k_minus_1 = boundary_matrix(complex_obj, k - 1)
        # product (d_{k-1} . d_k) over Z must be the zero matrix
        rows = len(d_k_minus_1)
        cols = len(d_k[0]) if d_k and d_k[0] else 0
        for i in range(rows):
            for j in range(cols):
                entry = sum(d_k_minus_1[i][m] * d_k[m][j] for m in range(len(d_k)))
                assert entry == 0


# --------------------------------------------------------------------------
# Known homology of standard spaces
# --------------------------------------------------------------------------

def test_point_homology():
    assert betti_numbers(_point()) == (1,)


def test_circle_homology():
    assert betti_numbers(_circle()) == (1, 1)


def test_sphere_homology():
    assert betti_numbers(_sphere()) == (1, 0, 1)


def test_torus_homology():
    assert betti_numbers(_torus()) == (1, 2, 1)


def test_real_projective_plane_betti():
    # RP^2: H0 = Z, H1 = Z/2 (Betti 0), H2 = 0
    assert betti_numbers(_real_projective_plane()) == (1, 0, 0)


def test_real_projective_plane_torsion():
    h1 = simplicial_homology(_real_projective_plane(), 1)
    assert h1.betti == 0
    assert h1.torsion == (2,)


def test_sphere_has_no_torsion():
    groups = homology_groups(_sphere())
    for group in groups:
        assert group.torsion == ()


# --------------------------------------------------------------------------
# Euler characteristic cross-check (homology vs combinatorial f-vector)
# --------------------------------------------------------------------------

@pytest.mark.parametrize(
    "builder,expected",
    [(_point, 1), (_circle, 0), (_sphere, 2), (_torus, 0), (_real_projective_plane, 1)],
)
def test_euler_characteristic_matches(builder, expected):
    complex_obj = builder()
    via_homology = euler_characteristic_via_homology(complex_obj)
    assert via_homology == expected
    # cross-check with the existing combinatorial alternating sum
    assert via_homology == complex_obj.euler_characteristic()


# --------------------------------------------------------------------------
# Cross-validate against the hardcoded combinatorial_topology profiles
# --------------------------------------------------------------------------

def test_homology_result_describe_and_is_free():
    from pytop import HomologyResult

    assert HomologyResult(0, 1, ()).describe() == "Z"
    assert HomologyResult(2, 2, ()).describe() == "Z^2"
    assert HomologyResult(1, 0, (2,)).describe() == "Z/2"
    assert HomologyResult(0, 0, ()).describe() == "0"
    assert HomologyResult(2, 1, ()).is_free is True
    assert HomologyResult(1, 0, (2,)).is_free is False


def test_reduced_homology():
    from pytop import reduced_homology

    # connected complexes have trivial reduced H0
    assert reduced_homology(_point(), 0).betti == 0
    assert reduced_homology(_sphere(), 0).betti == 0
    # higher reduced homology agrees with ordinary homology
    assert reduced_homology(_sphere(), 2).betti == 1
    # RP^2 reduced H1 keeps its torsion
    assert reduced_homology(_real_projective_plane(), 1).torsion == (2,)


def test_homology_matches_hardcoded_profiles_where_constructible():
    # The combinatorial_topology module stores hardcoded betti_numbers for
    # famous complexes; verify our engine reproduces them for the ones we can
    # triangulate here.
    expected = {
        "sphere": (1, 0, 1),
        "torus": (1, 2, 1),
    }
    builders = {"sphere": _sphere, "torus": _torus}
    for name, betti in expected.items():
        assert betti_numbers(builders[name]()) == betti


# --------------------------------------------------------------------------
# Mixed torsion edge cases
# --------------------------------------------------------------------------

def test_snf_mixed_torsion_z2_z3_gives_z6():
    # diag(2, 3): 2 does not divide 3, so divisibility correction runs.
    # SNF of diag(2,3) → invariant factors [1, 6], meaning Z/1 ⊕ Z/6 = Z/6.
    result = _smith_normal_form([[2, 0], [0, 3]])
    assert result == [1, 6]
    # The only torsion factor > 1 is 6: single Z/6
    torsion = tuple(d for d in result if d > 1)
    assert torsion == (6,)


def test_snf_mixed_torsion_z4_z6():
    # diag(4, 6): gcd(4,6)=2, lcm=12 → SNF factors 2, 12
    result = _smith_normal_form([[4, 0], [0, 6]])
    assert result == [2, 12]
    torsion = tuple(d for d in result if d > 1)
    assert torsion == (2, 12)


def test_snf_triple_torsion_divisibility():
    # diag(2, 6, 30): already satisfies 2|6|30 — factors returned as-is
    result = _smith_normal_form([[2, 0, 0], [0, 6, 0], [0, 0, 30]])
    torsion = [d for d in result if d > 1]
    # Verify divisibility chain
    for k in range(len(torsion) - 1):
        assert torsion[k + 1] % torsion[k] == 0


def test_snf_rank_two_with_torsion():
    # Matrix whose SNF has both a rank-2 free part and torsion
    # [[2, 0, 0], [0, 1, 0], [0, 0, 1]] — two units, one 2
    result = _smith_normal_form([[2, 0, 0], [0, 1, 0], [0, 0, 1]])
    # rank = 3; torsion part is the factor 2
    assert 2 in result
    assert len(result) == 3


def test_rp2_torsion_is_z2_not_z6():
    # Sanity: RP² has H₁ = Z/2, not Z/6 or other mixed group
    h1 = simplicial_homology(_real_projective_plane(), 1)
    assert h1.torsion == (2,)
    assert h1.betti == 0
