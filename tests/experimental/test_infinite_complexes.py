"""Tests for :mod:`pytop.experimental.infinite_complexes`.

Several tests here are regression guards for defects found during design review;
each names the register entry it guards so it is not "simplified away" later.
"""

from __future__ import annotations

import math

import pytest

from pytop import (
    CWComplex,
    cellular_homology,
    cw_complex_projective_space,
    cw_lens_space,
    cw_moore_space,
    cw_real_projective_space,
)
from pytop.experimental.infinite_complexes import (
    Assumptions,
    ConditionalHomology,
    InsufficientStagesError,
    NotATowerError,
    ProperMetric,
    RipsBettiScan,
    ScanStop,
    StageInclusion,
    TailAssumption,
    _inclusion_matrix,
    _lens_skeleton,
    _s_infinity_skeleton,
    _verify_chain_map,
    colimit_homology,
    cp_infinity_homology,
    infinite_lens_homology,
    rips_betti_scan,
    rp_infinity_homology,
    s_infinity_homology,
    z_lattice,
)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _identity_inclusion(complex_: CWComplex) -> StageInclusion:
    """The inclusion sending each cell to the same index with sign +1."""
    return StageInclusion(
        images=tuple(
            (k, tuple((j, 1) for j in range(n)))
            for k, n in sorted(complex_.cell_counts.items())
        )
    )


def _tower(stages: list[CWComplex]) -> tuple[list[CWComplex], list[StageInclusion]]:
    return stages, [_identity_inclusion(s) for s in stages[:-1]]


# ---------------------------------------------------------------------------
# Task 1 -- errors
# ---------------------------------------------------------------------------


def test_errors_are_value_errors() -> None:
    assert issubclass(NotATowerError, ValueError)
    assert issubclass(InsufficientStagesError, ValueError)


# ---------------------------------------------------------------------------
# Task 2 -- skeleton builders
# ---------------------------------------------------------------------------


def test_lens_skeleton_matches_rp_byte_for_byte_at_p_2() -> None:
    for n in range(8):
        got = _lens_skeleton(2, n)
        want = cw_real_projective_space(n)
        assert got.cell_counts == want.cell_counts
        assert got.boundary_maps == want.boundary_maps


def test_lens_skeleton_truncation_matches_shipped_lens_space() -> None:
    assert _lens_skeleton(5, 3).boundary_maps == cw_lens_space(5).boundary_maps


@pytest.mark.parametrize("p", [2, 3, 5])
def test_lens_skeleton_homology_at_evaluation_index(p: int) -> None:
    # "at the evaluation index" is load-bearing: on a FIXED skeleton the top
    # degree is ker(d_n), so H_5(_lens_skeleton(5, 5)) is Z, not Z/5.
    for k in range(7):
        h = cellular_homology(_lens_skeleton(p, k + 1), k)
        if k == 0:
            assert (h.betti, h.torsion) == (1, ())
        elif k % 2 == 1:
            assert (h.betti, h.torsion) == (0, (p,))
        else:
            assert (h.betti, h.torsion) == (0, ())


def test_s_infinity_skeleton_sphere_homology() -> None:
    # S^0 is two points -- the n = 0 exception.
    assert cellular_homology(_s_infinity_skeleton(0), 0).betti == 2
    for n in range(1, 6):
        betti = [cellular_homology(_s_infinity_skeleton(n), k).betti for k in range(n + 1)]
        assert betti == [1] + [0] * (n - 1) + [1]


def test_s_infinity_all_zero_boundaries_would_be_wrong() -> None:
    """Guard: the all-zero variant passes d.d == 0 and yields Z^2 everywhere."""
    bogus = CWComplex({k: 2 for k in range(4)}, {})
    assert cellular_homology(bogus, 2).betti == 2
    assert cellular_homology(_s_infinity_skeleton(3), 2).betti == 0


# ---------------------------------------------------------------------------
# Task 3 -- Part A public functions (blocking literals)
# ---------------------------------------------------------------------------

RP_INF = [(1, ()), (0, (2,)), (0, ()), (0, (2,)), (0, ()), (0, (2,)), (0, ()), (0, (2,)), (0, ())]
CP_INF = [(1, ()), (0, ()), (1, ()), (0, ()), (1, ()), (0, ()), (1, ()), (0, ()), (1, ())]
S_INF: list[tuple[int, tuple[int, ...]]] = [(1, ())] + [(0, ())] * 8


@pytest.mark.parametrize(("k", "want"), list(enumerate(RP_INF)))
def test_rp_infinity_blocking_literals(k: int, want: tuple[int, tuple[int, ...]]) -> None:
    h = rp_infinity_homology(k)
    assert (h.betti, h.torsion) == want


@pytest.mark.parametrize(("k", "want"), list(enumerate(CP_INF)))
def test_cp_infinity_blocking_literals(k: int, want: tuple[int, tuple[int, ...]]) -> None:
    h = cp_infinity_homology(k)
    assert (h.betti, h.torsion) == want


@pytest.mark.parametrize(("k", "want"), list(enumerate(S_INF)))
def test_s_infinity_blocking_literals(k: int, want: tuple[int, tuple[int, ...]]) -> None:
    h = s_infinity_homology(k)
    assert (h.betti, h.torsion) == want


def test_infinite_lens_agrees_with_rp_at_p_2() -> None:
    for k in range(9):
        a, b = infinite_lens_homology(2, k), rp_infinity_homology(k)
        assert (a.betti, a.torsion) == (b.betti, b.torsion)


@pytest.mark.parametrize("bad_p", [0, -1, -5])
def test_infinite_lens_rejects_p_below_one(bad_p: int) -> None:
    """Guard R3-C-02: p = 0 gives all-zero boundaries and would report Z everywhere."""
    with pytest.raises(ValueError, match="p must be at least 1"):
        infinite_lens_homology(bad_p, 3)


@pytest.mark.parametrize(
    "fn", [rp_infinity_homology, cp_infinity_homology, s_infinity_homology]
)
def test_negative_degree_rejected(fn) -> None:  # noqa: ANN001
    with pytest.raises(ValueError, match="degree must be >= 0"):
        fn(-1)


def test_infinite_lens_rejects_negative_degree() -> None:
    with pytest.raises(ValueError, match="degree must be >= 0"):
        infinite_lens_homology(3, -1)


# ---------------------------------------------------------------------------
# Task 4 -- Part B data types
# ---------------------------------------------------------------------------


def test_stage_inclusion_is_hashable() -> None:
    a = StageInclusion(images=((0, ((0, 1),)), (1, ((0, -1),))))
    b = StageInclusion(images=((0, ((0, 1),)), (1, ((0, -1),))))
    assert hash(a) == hash(b)
    assert len({a, b}) == 1


def test_stage_inclusion_lookup() -> None:
    inc = StageInclusion(images=((0, ((0, 1), (1, 1))), (2, ((3, -1),))))
    assert inc.at(0) == ((0, 1), (1, 1))
    assert inc.at(2) == ((3, -1),)
    assert inc.at(5) == ()


def test_conditional_homology_truthiness() -> None:
    group = cellular_homology(cw_real_projective_space(2), 1)
    everything = Assumptions(
        assumed=frozenset(TailAssumption),
        min_tail_cell_dimension=3,
        evaluated_stage=1,
        verified_steps=(1, 2),
    )
    nothing = Assumptions(
        assumed=frozenset(),
        min_tail_cell_dimension=3,
        evaluated_stage=1,
        verified_steps=(1,),
    )
    assert not ConditionalHomology(group=group, assumptions=everything)
    assert ConditionalHomology(group=group, assumptions=nothing)


# ---------------------------------------------------------------------------
# Task 5 -- chain-map verification
# ---------------------------------------------------------------------------


def test_inclusion_matrix_shape_and_signs() -> None:
    inc = StageInclusion(images=((1, ((0, 1), (2, -1))),))
    m = _inclusion_matrix(inc, degree=1, source_cells=2, target_cells=3)
    assert m == [[1, 0], [0, 0], [0, -1]]


def test_inclusion_matrix_rejects_non_injective() -> None:
    inc = StageInclusion(images=((0, ((0, 1), (0, 1))),))
    with pytest.raises(NotATowerError, match="not injective"):
        _inclusion_matrix(inc, degree=0, source_cells=2, target_cells=2)


def test_inclusion_matrix_rejects_bad_sign() -> None:
    inc = StageInclusion(images=((0, ((0, 2),)),))
    with pytest.raises(NotATowerError, match="sign"):
        _inclusion_matrix(inc, degree=0, source_cells=1, target_cells=1)


def test_moore_tower_is_rejected() -> None:
    """Guard R2-C-02: constant cell counts, pairwise non-nested.

    A cell-count check would pass this vacuously; the chain-map law bites
    because d_2 = [[k+2]] differs between consecutive stages.
    """
    stages = [cw_moore_space(k + 2, 1) for k in range(4)]
    for i in range(3):
        with pytest.raises(NotATowerError):
            _verify_chain_map(
                stages[i], stages[i + 1], _identity_inclusion(stages[i]), step=i
            )


def test_genuine_skeletal_inclusion_is_accepted() -> None:
    a, b = cw_real_projective_space(2), cw_real_projective_space(3)
    _verify_chain_map(a, b, _identity_inclusion(a), step=0)


def test_orientation_reversing_inclusion_needs_signs() -> None:
    """Guard R3-H-02: an unsigned map cannot express a legitimate inclusion."""
    rp2 = CWComplex({0: 1, 1: 1, 2: 1}, {1: [[0]], 2: [[2]]})
    rp3_flipped = CWComplex({0: 1, 1: 1, 2: 1, 3: 1}, {1: [[0]], 2: [[-2]], 3: [[0]]})
    with pytest.raises(NotATowerError):
        _verify_chain_map(rp2, rp3_flipped, _identity_inclusion(rp2), step=0)
    signed = StageInclusion(images=((0, ((0, 1),)), (1, ((0, 1),)), (2, ((0, -1),))))
    _verify_chain_map(rp2, rp3_flipped, signed, step=0)


# ---------------------------------------------------------------------------
# Task 6 -- window search and colimit_homology
# ---------------------------------------------------------------------------


def test_vacuity_discrete_points_raises() -> None:
    """Guard R3-C-01(a): an empty window made this return Z^5."""
    stages, incs = _tower([CWComplex({0: i + 1}, {}) for i in range(1, 6)])
    with pytest.raises(InsufficientStagesError):
        colimit_homology(stages, incs, degree=0)


def test_vacuity_wedge_of_circles_raises() -> None:
    """Guard R3-C-01(b): an empty window made this return betti 3/5/11/39."""
    stages, incs = _tower(
        [CWComplex({0: 1, 1: i}, {1: [[0] * i]}) for i in range(1, 5)]
    )
    with pytest.raises(InsufficientStagesError):
        colimit_homology(stages, incs, degree=1)


def test_no_spurious_floor_wedge_of_spheres() -> None:
    """Guard R3-H-01: the removed `N >= degree+1` floor rejected this."""
    stages, incs = _tower([CWComplex({0: 1, 2: i}, {}) for i in range(1, 5)])
    result = colimit_homology(stages, incs, degree=0)
    assert result.assumptions.evaluated_stage == 0
    assert result.group.betti == 1


def test_no_spurious_floor_high_dimensional_cells() -> None:
    stages, incs = _tower([CWComplex({0: 1, 3: 1, 5: j}, {}) for j in range(1, 5)])
    result = colimit_homology(stages, incs, degree=3)
    assert result.assumptions.evaluated_stage == 0
    assert result.group.betti == 1


@pytest.mark.parametrize(("degree", "want_stage"), [(1, 2), (3, 4)])
def test_rp_tower_evaluates_at_degree_plus_one(degree: int, want_stage: int) -> None:
    stages, incs = _tower([cw_real_projective_space(n) for n in range(degree + 4)])
    result = colimit_homology(stages, incs, degree=degree)
    assert result.assumptions.evaluated_stage == want_stage
    assert (result.group.betti, result.group.torsion) == (0, (2,))


def test_result_is_falsy_and_names_every_tail_assumption() -> None:
    stages, incs = _tower([cw_real_projective_space(n) for n in range(5)])
    result = colimit_homology(stages, incs, degree=1)
    assert not result
    assert result.assumptions.assumed == frozenset(TailAssumption)
    assert result.assumptions.min_tail_cell_dimension == 3
    assert result.assumptions.verified_steps


def test_chain_embedding_that_is_not_a_subcomplex_is_accepted() -> None:
    """Pins the documented scope (R3-M-01).

    ``{e^0, e^4}`` is not a subcomplex of CP^2 -- e^4 is attached by the Hopf
    map -- yet the chain-map law holds trivially because all boundaries vanish.
    The algebra is sound; the topological reading is the caller's job.
    """
    s4 = CWComplex({0: 1, 4: 1}, {})
    cp2 = cw_complex_projective_space(2)
    inc = StageInclusion(images=((0, ((0, 1),)), (4, ((0, 1),))))
    result = colimit_homology([s4, cp2], [inc], degree=0)
    assert result.group.betti == 1


def test_colimit_requires_two_stages() -> None:
    one = cw_real_projective_space(2)
    with pytest.raises(InsufficientStagesError, match="at least 2 stages"):
        colimit_homology([one], [], degree=0)


def test_colimit_requires_matching_inclusion_count() -> None:
    stages = [cw_real_projective_space(n) for n in range(3)]
    with pytest.raises(NotATowerError, match="inclusions"):
        colimit_homology(stages, [_identity_inclusion(stages[0])], degree=0)


def test_colimit_rejects_negative_degree() -> None:
    stages, incs = _tower([cw_real_projective_space(n) for n in range(3)])
    with pytest.raises(ValueError, match="degree must be >= 0"):
        colimit_homology(stages, incs, degree=-1)


# ---------------------------------------------------------------------------
# Task 7 -- ProperMetric and the lattice helper
# ---------------------------------------------------------------------------


def test_z_lattice_ball_sizes_euclidean() -> None:
    lat = z_lattice(2)
    assert [len(lat.ball((0, 0), r)) for r in (1, 2, 3, 4, 5)] == [5, 13, 29, 49, 81]


def test_z_lattice_norms_differ() -> None:
    assert len(z_lattice(2, norm="linf").ball((0, 0), 1)) == 9
    assert len(z_lattice(2, norm="l1").ball((0, 0), 1)) == 5


def test_z_lattice_distance() -> None:
    assert z_lattice(2).distance((0, 0), (1, 1)) == pytest.approx(math.sqrt(2))
    assert z_lattice(2, norm="l1").distance((0, 0), (1, 1)) == 2
    assert z_lattice(2, norm="linf").distance((0, 0), (1, 1)) == 1


def test_z_lattice_satisfies_protocol() -> None:
    assert isinstance(z_lattice(2), ProperMetric)


def test_z_lattice_rejects_bad_dimension() -> None:
    with pytest.raises(ValueError, match="n must be >= 1"):
        z_lattice(0)


def test_z_lattice_rejects_bad_norm() -> None:
    with pytest.raises(ValueError, match="norm must be"):
        z_lattice(2, norm="l7")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Task 8 -- claim-free Rips scan
# ---------------------------------------------------------------------------


def test_scan_epsilon_one_euclidean_matches_measured_values() -> None:
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=1.0, radii=[1, 2, 3, 4, 5], max_degree=1
    )
    assert [row[1] for row in scan.betti_z] == [0, 4, 16, 32, 60]
    assert all(row[0] == 1 for row in scan.betti_z)
    assert scan.stopped_reason is None


def test_scan_rows_are_normalised_across_ragged_radii() -> None:
    """Guard R3-H-04: R=1 has dimension 2 (raw 3-tuple); R>=2 has dimension 3."""
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=math.sqrt(2), radii=[1, 2, 3], max_degree=3
    )
    assert all(len(row) == 4 for row in scan.betti_z)
    assert scan.betti_z[0] == (1, 0, 0, 0)
    assert scan.betti_z[1] == (1, 0, 0, 0)
    assert scan.betti_z[2] == (1, 0, 0, 0)


def test_scan_stops_on_point_cap_and_keeps_partial_results() -> None:
    """Guard R3-H-03: the ball is capped before the complex is built."""
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=1.0, radii=[1, 2, 10], max_degree=1, max_points=30
    )
    assert scan.stopped_reason is ScanStop.POINT_CAP
    assert scan.stopped_at_radius == 10
    assert len(scan.radii) == 2
    assert len(scan.betti_z) == len(scan.radii)


def test_scan_stops_on_boundary_cap() -> None:
    scan = rips_betti_scan(
        z_lattice(2),
        (0, 0),
        eps=math.sqrt(2),
        radii=[1, 6],
        max_degree=3,
        max_boundary_dim=50,
    )
    assert scan.stopped_reason is ScanStop.BOUNDARY_CAP
    assert scan.stopped_at_radius == 6
    assert len(scan.radii) == 1


def test_scan_makes_no_colimit_claim_in_its_fields() -> None:
    fields = RipsBettiScan.__dataclass_fields__
    assert not any(
        word in name
        for name in fields
        for word in ("colimit", "converge", "stable", "limit")
    )


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"radii": [2, 1]}, "strictly increasing"),
        ({"radii": [1, 1]}, "strictly increasing"),
        ({"eps": 0.0}, "eps must be > 0"),
        ({"max_degree": -1}, "max_degree must be >= 0"),
    ],
)
def test_scan_preconditions(kwargs: dict, match: str) -> None:
    base = {
        "metric": z_lattice(2),
        "center": (0, 0),
        "eps": 1.0,
        "radii": [1, 2],
        "max_degree": 1,
    }
    with pytest.raises(ValueError, match=match):
        rips_betti_scan(**{**base, **kwargs})


# ---------------------------------------------------------------------------
# Anti-regression: no observational stabilisation knob may reappear
# ---------------------------------------------------------------------------


def test_no_patience_like_parameter_in_public_surface() -> None:
    """Behavioural half lives in the vacuity tests; this guards the surface."""
    import inspect as _inspect

    for fn in (colimit_homology, rips_betti_scan):
        names = set(_inspect.signature(fn).parameters)
        assert not names & {"patience", "budget", "tolerance", "stabilize_after"}


def test_supplying_more_stages_never_upgrades_the_claim() -> None:
    """More evidence must not change the epistemic status (round 2, R2-M-08)."""
    short, short_inc = _tower([cw_real_projective_space(n) for n in range(4)])
    long, long_inc = _tower([cw_real_projective_space(n) for n in range(9)])
    a = colimit_homology(short, short_inc, degree=1)
    b = colimit_homology(long, long_inc, degree=1)
    assert a.assumptions.assumed == b.assumptions.assumed
    assert (a.group.betti, a.group.torsion) == (b.group.betti, b.group.torsion)
    assert not a and not b


# ---------------------------------------------------------------------------
# Non-blocking consistency note -- eilenberg_maclane is NOT an oracle
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    reason=(
        "consistency note, not an oracle: eilenberg_maclane is a curated "
        "transcription of known values, so a divergence is a prompt to "
        "investigate rather than a gate"
    ),
    strict=False,
)
@pytest.mark.parametrize("p", [2, 3, 5])
def test_consistency_with_eilenberg_maclane(p: int) -> None:
    from pytop import km_homology_cyclic

    curated = km_homology_cyclic(p, 8)
    for k in range(9):
        ours = infinite_lens_homology(p, k)
        assert ours.betti == curated.betti[k]
        assert tuple(ours.torsion) == tuple(curated.torsion[k])


# ---------------------------------------------------------------------------
# Export surface
# ---------------------------------------------------------------------------


def test_all_public_names_exported_from_experimental() -> None:
    import pytop.experimental as ex

    for name in (
        "rp_infinity_homology",
        "cp_infinity_homology",
        "s_infinity_homology",
        "infinite_lens_homology",
        "colimit_homology",
        "StageInclusion",
        "TailAssumption",
        "Assumptions",
        "ConditionalHomology",
        "rips_betti_scan",
        "ProperMetric",
        "ScanStop",
        "RipsBettiScan",
        "z_lattice",
        "NotATowerError",
        "InsufficientStagesError",
    ):
        assert hasattr(ex, name), name
        assert name in ex.__all__, name


def test_nothing_added_to_top_level_pytop() -> None:
    import pytop

    assert not hasattr(pytop, "colimit_homology")
    assert not hasattr(pytop, "rips_betti_scan")


def test_scan_stops_on_density_cap_for_a_clique_ball() -> None:
    """Guard R3-H-03: the ball that a point cap alone cannot stop.

    The Euclidean disk of radius 5 has 81 points and diameter 10, so at eps=10 it
    is a single clique whose Rips complex truncated at dimension 4 would have
    ~2.7e7 simplices. 81 is under any sane point cap, and the boundary-matrix
    guard fires only after construction -- so the density bound is the one that
    has to catch this, before any enumeration happens.
    """
    import time

    start = time.perf_counter()
    scan = rips_betti_scan(
        z_lattice(2), (0, 0), eps=10.0, radii=[1.0, 5.0], max_degree=3
    )
    assert time.perf_counter() - start < 5.0
    assert scan.stopped_reason is ScanStop.DENSITY_CAP
    assert scan.stopped_at_radius == 5.0
    assert len(scan.radii) == 1


def test_scan_density_bound_allows_the_documented_lattice_rows() -> None:
    """The density guard must not reject the validation rows in the spec."""
    sparse = rips_betti_scan(
        z_lattice(2), (0, 0), eps=1.0, radii=[1, 2, 3, 4, 5], max_degree=1
    )
    assert sparse.stopped_reason is None
    dense = rips_betti_scan(
        z_lattice(2), (0, 0), eps=math.sqrt(2), radii=[1, 2, 3, 4], max_degree=3
    )
    assert dense.stopped_reason is None
