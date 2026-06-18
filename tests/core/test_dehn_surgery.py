"""Known-answer tests for Dehn surgery first homology and lens space classification.

``first_homology_of_surgery`` computes ``H₁(M)`` for surgery on a framed link as
the cokernel of ``A_{ii}=pᵢ, A_{ij}=qᵢ·lk(Lᵢ,Lⱼ)``.  The tests pin standard
3-manifolds (lens spaces, ``S¹×S²``, ``T³``, the Poincaré homology sphere via the
``E₈`` plumbing) and the elementary lens space classifications.
"""

from __future__ import annotations

import pytest

from pytop import (
    FirstHomology,
    LinkDiagram,
    are_lens_spaces_homeomorphic,
    are_lens_spaces_homotopy_equivalent,
    first_homology_of_link_surgery,
    first_homology_of_surgery,
    lens_space_first_homology,
)

HOPF_LINKING = [[0, 1], [1, 0]]


def _e8_plumbing() -> list[list[int]]:
    """E₈ plumbing matrix: branch node with legs of 1, 2, 4 nodes, framing −2."""
    matrix = [[0] * 8 for _ in range(8)]
    for i in range(8):
        matrix[i][i] = -2
    for a, b in [(0, 1), (0, 2), (2, 3), (0, 4), (4, 5), (5, 6), (6, 7)]:
        matrix[a][b] = matrix[b][a] = 1
    return matrix


# ---------------------------------------------------------------------------
# FirstHomology result type
# ---------------------------------------------------------------------------


class TestFirstHomology:
    def test_trivial_group_str(self):
        assert str(FirstHomology(0, ())) == "0"

    def test_free_and_torsion_str(self):
        assert str(FirstHomology(2, (2, 6))) == "Z^2 + Z/2 + Z/6"
        assert str(FirstHomology(1, ())) == "Z"
        assert str(FirstHomology(0, (5,))) == "Z/5"

    def test_order_finite_and_infinite(self):
        assert FirstHomology(0, (2, 6)).order == 12
        assert FirstHomology(0, ()).order == 1
        assert FirstHomology(1, ()).order is None

    def test_homology_sphere_flags(self):
        assert FirstHomology(0, ()).is_homology_sphere
        assert FirstHomology(0, ()).is_rational_homology_sphere
        assert not FirstHomology(0, (5,)).is_homology_sphere
        assert FirstHomology(0, (5,)).is_rational_homology_sphere
        assert not FirstHomology(1, ()).is_rational_homology_sphere


# ---------------------------------------------------------------------------
# Surgery on the unknot / single knots
# ---------------------------------------------------------------------------


class TestSingleComponent:
    def test_lens_space_homology_is_z_mod_p(self):
        assert lens_space_first_homology(5, 1) == FirstHomology(0, (5,))
        assert lens_space_first_homology(7, 2) == FirstHomology(0, (7,))

    def test_zero_surgery_unknot_is_s1_times_s2(self):
        assert lens_space_first_homology(0, 1) == FirstHomology(1, ())

    def test_plus_minus_one_surgery_is_homology_sphere(self):
        assert first_homology_of_surgery([1]).is_homology_sphere
        assert first_homology_of_surgery([-1]).is_homology_sphere

    def test_integer_surgery_on_knot_is_z_mod_n(self):
        # H₁ depends only on the framing, not the knot type.
        assert first_homology_of_surgery([6]) == FirstHomology(0, (6,))

    def test_rational_surgery(self):
        assert first_homology_of_surgery([(7, 2)]) == FirstHomology(0, (7,))
        # q sign is normalised: 7/-2 == -7/2 gives the same |H₁|.
        assert first_homology_of_surgery([(7, -2)]).order == 7

    def test_empty_surgery_is_s3(self):
        assert first_homology_of_surgery([]) == FirstHomology(0, ())


# ---------------------------------------------------------------------------
# Surgery on links (linking numbers matter)
# ---------------------------------------------------------------------------


class TestMultiComponent:
    def test_hopf_link_zero_framings_is_homology_sphere(self):
        assert first_homology_of_surgery([0, 0], HOPF_LINKING).is_homology_sphere

    def test_hopf_link_general_framings(self):
        # det [[2,1],[1,3]] = 5  →  H₁ = ℤ/5
        result = first_homology_of_surgery([2, 3], HOPF_LINKING)
        assert result == FirstHomology(0, (5,))
        assert result.order == 5

    def test_borromean_zero_surgery_is_three_torus(self):
        # Pairwise linking numbers are all zero; 0-surgery → T³, H₁ = ℤ³.
        unlinked = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert first_homology_of_surgery([0, 0, 0], unlinked) == FirstHomology(3, ())

    def test_e8_plumbing_is_poincare_homology_sphere(self):
        result = first_homology_of_surgery([-2] * 8, _e8_plumbing())
        assert result.is_homology_sphere
        assert result.order == 1

    def test_linking_numbers_dimension_validation(self):
        with pytest.raises(ValueError, match="match"):
            first_homology_of_surgery([1, 2], [[0, 1, 0], [1, 0, 0], [0, 0, 0]])

    def test_zero_coefficient_denominator_rejected(self):
        with pytest.raises(ValueError, match="q"):
            first_homology_of_surgery([(3, 0)])


class TestLinkSurgeryIntegration:
    def test_hopf_diagram_surgery_matches_matrix(self):
        hopf = LinkDiagram(
            crossings=[(1, 4, 2, 3), (3, 2, 4, 1)],
            signs=[1, 1],
            n_components=2,
            component_map=[0, 1, 0, 1],
        )
        # lk = ±1 from the diagram; framings (2, 3) → det ±5 → ℤ/5.
        assert first_homology_of_link_surgery(hopf, [2, 3]).order == 5

    def test_coefficient_count_validation(self):
        hopf = LinkDiagram(
            crossings=[(1, 4, 2, 3), (3, 2, 4, 1)],
            signs=[1, 1],
            n_components=2,
            component_map=[0, 1, 0, 1],
        )
        with pytest.raises(ValueError, match="component"):
            first_homology_of_link_surgery(hopf, [1])


# ---------------------------------------------------------------------------
# Lens space classification
# ---------------------------------------------------------------------------


class TestLensSpaceClassification:
    def test_homeomorphism_inverse_and_negation(self):
        assert are_lens_spaces_homeomorphic(7, 1, 6)   # 6 ≡ −1
        assert are_lens_spaces_homeomorphic(7, 2, 4)   # 4 ≡ 2⁻¹
        assert not are_lens_spaces_homeomorphic(7, 1, 2)

    def test_homotopy_equivalent_but_not_homeomorphic(self):
        # The classic example: L(7,1) and L(7,2).
        assert are_lens_spaces_homotopy_equivalent(7, 1, 2)
        assert not are_lens_spaces_homeomorphic(7, 1, 2)

    def test_reflexive(self):
        assert are_lens_spaces_homeomorphic(5, 2, 2)
        assert are_lens_spaces_homotopy_equivalent(5, 2, 2)

    def test_non_coprime_rejected(self):
        with pytest.raises(ValueError, match="coprime"):
            are_lens_spaces_homeomorphic(6, 2, 1)
