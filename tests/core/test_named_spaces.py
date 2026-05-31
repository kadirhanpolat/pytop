"""Tests for named_spaces and space_catalog modules."""

import pytest

import pytop
from pytop.named_spaces import (
    arens_fort_space,
    cantor_set,
    comb_space,
    cofinite_topology_on_naturals,
    cofinite_topology_on_reals,
    cocountable_topology_on_reals,
    deleted_tychonoff_plank,
    discrete_countable_space,
    discrete_space,
    double_origin_topology,
    excluded_point_topology,
    excluded_point_topology_on_naturals,
    fort_space,
    furstenberg_topology,
    hilbert_cube,
    indiscrete_space,
    infinite_broom,
    irrational_numbers,
    long_line,
    michael_line,
    moore_plane,
    particular_point_topology,
    particular_point_topology_on_naturals,
    pseudo_arc,
    rational_numbers,
    real_line,
    sierpinski_space,
    sorgenfrey_line,
    stone_cech_compactification_of_N,
    topologists_sine_curve,
    tychonoff_plank,
    warsaw_circle,
    # Batch 6
    real_n_space,
    sorgenfrey_plane,
    one_point_compactification_of_N,
    omega_plus_1,
    rational_sequence_topology,
    particular_point_topology_on_R,
    excluded_point_topology_on_R,
    divisor_topology,
    uncountable_discrete_space,
    double_arrow_space,
    annulus,
    wedge_sum_of_circles,
    # Batch 7
    upper_half_plane,
    closed_upper_half_plane,
    p_adic_numbers,
    sierpinski_triangle,
    real_projective_n_space,
    cofinite_topology_on_integers,
    long_ray,
    knaster_continuum,
    complex_projective_plane,
    infinite_product_of_reals,
    n_torus,
    open_unit_disk,
    genus_g_surface,
    n_ball,
    k_topology_on_R,
    solenoid,
    extended_real_line,
    uncountable_product_of_two_point_spaces,
    wedge_of_two_spheres,
    suspension_of_cantor_set,
    quarter_plane,
    punctured_torus,
    discrete_sum_of_circles,
    lens_space,
)
from pytop.space_catalog import SpaceCatalog, SpaceRecord, catalog


# ---------------------------------------------------------------------------
# named_spaces — basic construction
# ---------------------------------------------------------------------------

class TestSierpinskiSpace:
    def test_carrier(self):
        s = sierpinski_space()
        assert s.carrier == frozenset({0, 1})

    def test_topology(self):
        s = sierpinski_space()
        assert frozenset() in s.topology
        assert frozenset({1}) in s.topology
        assert frozenset({0, 1}) in s.topology
        assert len(s.topology) == 3

    def test_tags(self):
        s = sierpinski_space()
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("compact")
        assert s.has_tag("connected")

    def test_finite(self):
        assert sierpinski_space().is_finite()


class TestParticularPointTopology:
    def test_basic(self):
        s = particular_point_topology(3, 0)
        assert s.carrier == frozenset({0, 1, 2})
        assert frozenset() in s.topology
        assert all(0 in u for u in s.topology if u)

    def test_tags(self):
        s = particular_point_topology(4, 1)
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")
        assert s.has_tag("hyperconnected")

    def test_invalid_args(self):
        with pytest.raises(ValueError):
            particular_point_topology(3, 5)
        with pytest.raises(ValueError):
            particular_point_topology(0, 0)

    def test_singleton(self):
        s = particular_point_topology(1, 0)
        assert s.carrier == frozenset({0})


class TestExcludedPointTopology:
    def test_basic(self):
        s = excluded_point_topology(3, 1)
        assert s.carrier == frozenset({0, 1, 2})
        assert frozenset({0, 1, 2}) in s.topology
        assert all(1 not in u or u == frozenset({0, 1, 2}) for u in s.topology)

    def test_tags(self):
        s = excluded_point_topology(3, 1)
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")

    def test_invalid_args(self):
        with pytest.raises(ValueError):
            excluded_point_topology(3, 3)


class TestCofiniteSpaces:
    def test_naturals_tags(self):
        s = cofinite_topology_on_naturals()
        assert s.has_tag("t1")
        assert s.has_tag("not_hausdorff")
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("lindelof")

    def test_reals_tags(self):
        s = cofinite_topology_on_reals()
        assert s.has_tag("t1")
        assert s.has_tag("compact")
        assert s.has_tag("connected")

    def test_cocountable_tags(self):
        s = cocountable_topology_on_reals()
        assert s.has_tag("t1")
        assert s.has_tag("not_hausdorff")
        assert s.has_tag("connected")
        assert not s.has_tag("compact")


class TestRealLine:
    def test_tags(self):
        s = real_line()
        assert s.has_tag("hausdorff")
        assert s.has_tag("connected")
        assert s.has_tag("second_countable")
        assert s.has_tag("metrizable")
        assert not s.has_tag("compact")

    def test_metadata_name(self):
        assert real_line().metadata["name"] == "Real line"


class TestSorgenfreyLine:
    def test_tags(self):
        s = sorgenfrey_line()
        assert s.has_tag("hausdorff")
        assert s.has_tag("lindelof")
        assert s.has_tag("not_metrizable")
        assert s.has_tag("not_second_countable")
        assert s.has_tag("totally_disconnected")
        assert not s.has_tag("compact")

    def test_pi_base_id(self):
        assert sorgenfrey_line().metadata.get("pi_base_id") == "S000009"


class TestRationalIrrational:
    def test_rational_tags(self):
        q = rational_numbers()
        assert q.has_tag("metrizable")
        assert q.has_tag("totally_disconnected")
        assert not q.has_tag("compact")
        assert not q.has_tag("locally_compact")

    def test_irrational_tags(self):
        ir = irrational_numbers()
        assert ir.has_tag("metrizable")
        assert ir.has_tag("zero_dimensional")
        assert not ir.has_tag("sigma_compact")


class TestCantorSet:
    def test_tags(self):
        c = cantor_set()
        assert c.has_tag("compact")
        assert c.has_tag("perfect")
        assert c.has_tag("totally_disconnected")
        assert c.has_tag("nowhere_dense")
        assert c.has_tag("metrizable")
        assert not c.has_tag("connected")


class TestHilbertCube:
    def test_tags(self):
        h = hilbert_cube()
        assert h.has_tag("compact")
        assert h.has_tag("connected")
        assert h.has_tag("metrizable")
        assert h.has_tag("second_countable")


class TestLongLine:
    def test_tags(self):
        ll = long_line()
        assert ll.has_tag("connected")
        assert ll.has_tag("hausdorff")
        assert ll.has_tag("not_metrizable")
        assert ll.has_tag("not_second_countable")
        assert ll.has_tag("not_compact")
        assert ll.has_tag("not_lindelof")


class TestSymbolicSpaces:
    def test_sine_curve(self):
        s = topologists_sine_curve()
        assert s.has_tag("connected")
        assert s.has_tag("not_path_connected")
        assert s.has_tag("compact")
        assert s.has_tag("not_locally_connected")

    def test_comb(self):
        c = comb_space()
        assert c.has_tag("connected")
        assert c.has_tag("compact")
        assert c.has_tag("not_locally_connected")

    def test_warsaw(self):
        w = warsaw_circle()
        assert w.has_tag("connected")
        assert w.has_tag("compact")
        assert w.has_tag("not_locally_connected")

    def test_broom(self):
        b = infinite_broom()
        assert b.has_tag("connected")
        assert b.has_tag("compact")
        assert b.has_tag("not_locally_connected")


class TestBasisDefinedSpaces:
    def test_moore_plane(self):
        m = moore_plane()
        assert m.has_tag("hausdorff")
        assert m.has_tag("separable")
        assert m.has_tag("not_normal")
        assert m.has_tag("not_metrizable")
        assert m.has_tag("first_countable")

    def test_arens_fort(self):
        a = arens_fort_space()
        assert a.has_tag("hausdorff")
        assert a.has_tag("not_first_countable")
        assert a.has_tag("not_sequential")

    def test_fort_space(self):
        f = fort_space()
        assert f.has_tag("compact")
        assert f.has_tag("hausdorff")
        assert f.has_tag("metrizable")
        assert f.has_tag("second_countable")


# ---------------------------------------------------------------------------
# Public API re-export
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Batch 2 tests
# ---------------------------------------------------------------------------

class TestDiscreteIndiscrete:
    def test_discrete_topology(self):
        s = discrete_space(3)
        assert len(s.topology) == 8  # power set of 3-element set
        assert s.has_tag("discrete")
        assert s.has_tag("hausdorff")
        assert s.has_tag("not_connected")
        assert s.has_tag("zero_dimensional")

    def test_discrete_singleton_connected(self):
        s = discrete_space(1)
        assert s.has_tag("connected")
        assert not s.has_tag("not_connected")

    def test_indiscrete_topology(self):
        s = indiscrete_space(3)
        assert len(s.topology) == 2
        assert s.has_tag("not_t0")
        assert s.has_tag("connected")
        assert s.has_tag("hyperconnected")

    def test_indiscrete_invalid(self):
        with pytest.raises(ValueError):
            discrete_space(0)
        with pytest.raises(ValueError):
            indiscrete_space(0)


class TestDiscreteCountable:
    def test_tags(self):
        s = discrete_countable_space()
        assert s.has_tag("metrizable")
        assert s.has_tag("hausdorff")
        assert s.has_tag("locally_compact")
        assert not s.has_tag("compact")
        assert s.has_tag("not_connected")


class TestInfiniteParticularExcluded:
    def test_particular_tags(self):
        s = particular_point_topology_on_naturals()
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")
        assert s.has_tag("hyperconnected")

    def test_excluded_tags(self):
        s = excluded_point_topology_on_naturals()
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")


class TestDoubleOrigin:
    def test_tags(self):
        s = double_origin_topology()
        assert s.has_tag("hausdorff")
        assert s.has_tag("not_regular")
        assert s.has_tag("connected")
        assert s.has_tag("second_countable")
        assert not s.has_tag("compact")

    def test_pi_base_id(self):
        assert double_origin_topology().metadata.get("pi_base_id") == "S000010"


class TestMichaelLine:
    def test_tags(self):
        m = michael_line()
        assert m.has_tag("hausdorff")
        assert m.has_tag("normal")
        assert m.has_tag("first_countable")
        assert m.has_tag("not_second_countable")
        assert m.has_tag("not_separable")
        assert m.has_tag("not_lindelof")
        assert m.has_tag("not_locally_compact")


class TestPlanks:
    def test_tychonoff_compact_normal(self):
        t = tychonoff_plank()
        assert t.has_tag("compact")
        assert t.has_tag("normal")
        assert t.has_tag("hausdorff")
        assert t.has_tag("connected")
        assert t.has_tag("not_first_countable")

    def test_deleted_tychonoff_not_normal(self):
        d = deleted_tychonoff_plank()
        assert d.has_tag("hausdorff")
        assert d.has_tag("not_normal")
        assert not d.has_tag("compact")


class TestStoneCech:
    def test_tags(self):
        s = stone_cech_compactification_of_N()
        assert s.has_tag("compact")
        assert s.has_tag("hausdorff")
        assert s.has_tag("extremally_disconnected")
        assert s.has_tag("separable")
        assert s.has_tag("not_metrizable")
        assert s.has_tag("not_first_countable")
        assert s.has_tag("totally_disconnected")


class TestFurstenberg:
    def test_tags(self):
        f = furstenberg_topology()
        assert f.has_tag("hausdorff")
        assert f.has_tag("metrizable")
        assert f.has_tag("zero_dimensional")
        assert f.has_tag("totally_disconnected")
        assert not f.has_tag("compact")
        assert not f.has_tag("connected")


class TestPseudoArc:
    def test_tags(self):
        p = pseudo_arc()
        assert p.has_tag("compact")
        assert p.has_tag("connected")
        assert p.has_tag("not_locally_connected")
        assert p.has_tag("not_path_connected")
        assert p.has_tag("metrizable")
        assert p.has_tag("homogeneous")


class TestCatalogBatch2:
    def test_batch2_spaces_in_catalog(self):
        names = [
            "Double origin topology",
            "Michael line",
            "Tychonoff plank",
            "Deleted Tychonoff plank",
            "Stone-Čech compactification of N",
            "Furstenberg topology",
            "Pseudo-arc",
            "Discrete countable space",
        ]
        for name in names:
            assert catalog.get(name) is not None, f"Missing: {name}"

    def test_alias_lookup(self):
        assert catalog.get("beta N") is not None
        assert catalog.get("evenly spaced integer topology") is not None

    def test_not_normal_search(self):
        results = catalog.search(normal=False)
        names = [r.name for r in results]
        assert "Double origin topology" in names
        assert "Deleted Tychonoff plank" in names
        assert "Moore plane" in names

    def test_extremally_disconnected_search(self):
        results = catalog.search(extremally_disconnected=True)
        assert any(r.name == "Stone-Čech compactification of N" for r in results)

    def test_catalog_size_batch2(self):
        assert len(catalog) >= 28

    def test_double_origin_pi_base(self):
        rec = catalog.get("Double origin topology")
        assert rec.pi_base_id == "S000010"


def test_public_api_exports():
    assert callable(pytop.sierpinski_space)
    assert callable(pytop.sorgenfrey_line)
    assert callable(pytop.cantor_set)
    assert pytop.catalog is not None


# ---------------------------------------------------------------------------
# space_catalog
# ---------------------------------------------------------------------------

class TestSpaceCatalog:
    def test_catalog_nonempty(self):
        assert len(catalog) > 0

    def test_get_by_name(self):
        rec = catalog.get("Sorgenfrey line")
        assert rec is not None
        assert rec.name == "Sorgenfrey line"

    def test_get_by_alias(self):
        rec = catalog.get("lower limit topology")
        assert rec is not None
        assert rec.name == "Sorgenfrey line"

    def test_get_case_insensitive(self):
        rec = catalog.get("sierpiński space")
        assert rec is not None

    def test_get_missing(self):
        assert catalog.get("nonexistent space xyz") is None

    def test_search_compact_connected(self):
        results = catalog.search(compact=True, connected=True)
        names = [r.name for r in results]
        assert "Hilbert cube" in names
        assert "Sierpiński space" in names
        assert "Sorgenfrey line" not in names

    def test_search_not_normal(self):
        results = catalog.search(normal=False)
        names = [r.name for r in results]
        assert "Moore plane" in names

    def test_search_no_match(self):
        results = catalog.search(compact=True, connected=False, metrizable=False)
        assert isinstance(results, list)

    def test_build_returns_space(self):
        rec = catalog.get("Cantor set")
        space = rec.build()
        assert space.has_tag("compact")

    def test_list_all(self):
        all_recs = catalog.list_all()
        assert len(all_recs) == len(catalog)
        assert all(isinstance(r, SpaceRecord) for r in all_recs)

    def test_register_new(self):
        cat = SpaceCatalog()
        cat.register(SpaceRecord(
            name="Test space",
            description="A test.",
            properties={"compact": True},
            constructor=sierpinski_space,
        ))
        assert cat.get("Test space") is not None
        assert len(cat.search(compact=True)) == 1

    def test_record_build_no_constructor(self):
        rec = SpaceRecord(name="X", description="Y", properties={})
        with pytest.raises(NotImplementedError):
            rec.build()

    def test_pi_base_ids(self):
        assert catalog.get("Sorgenfrey line").pi_base_id == "S000009"
        assert catalog.get("Moore plane").pi_base_id == "S000008"
        assert catalog.get("Arens-Fort space").pi_base_id == "S000007"


# ---------------------------------------------------------------------------
# Batch 6
# ---------------------------------------------------------------------------

class TestRealNSpace:
    def test_basic_tags(self):
        s = real_n_space(3)
        assert s.has_tag("connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("simply_connected")
        assert not s.has_tag("compact")

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            real_n_space(0)

    def test_metadata(self):
        s = real_n_space(2)
        assert s.metadata["name"] == "R^2"
        assert s.metadata["dimension"] == 2


class TestSorgenfreyPlane:
    def test_tags(self):
        s = sorgenfrey_plane()
        assert s.has_tag("hausdorff")
        assert s.has_tag("regular")
        assert s.has_tag("separable")
        assert s.has_tag("not_normal")
        assert s.has_tag("not_metrizable")
        assert not s.has_tag("compact")


class TestOnePointCompactificationOfN:
    def test_tags(self):
        s = one_point_compactification_of_N()
        assert s.has_tag("compact")
        assert s.has_tag("metrizable")
        assert s.has_tag("zero_dimensional")
        assert s.has_tag("totally_disconnected")
        assert not s.has_tag("connected")

    def test_in_catalog(self):
        rec = catalog.get("One-point compactification of N")
        assert rec is not None
        assert rec.properties.get("compact") is True


class TestOmegaPlus1:
    def test_tags(self):
        s = omega_plus_1()
        assert s.has_tag("compact")
        assert s.has_tag("metrizable")
        assert s.has_tag("zero_dimensional")
        assert s.has_tag("hausdorff")
        assert not s.has_tag("connected")

    def test_alias(self):
        assert catalog.get("omega+1") is not None or catalog.get("[0,omega]") is not None


class TestRationalSequenceTopology:
    def test_tags(self):
        s = rational_sequence_topology()
        assert s.has_tag("hausdorff")
        assert s.has_tag("separable")
        assert s.has_tag("first_countable")
        assert s.has_tag("not_regular")
        assert s.has_tag("not_metrizable")


class TestParticularExcludedOnR:
    def test_particular_tags(self):
        s = particular_point_topology_on_R()
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")
        assert s.has_tag("hyperconnected")
        assert s.has_tag("separable")

    def test_excluded_tags(self):
        s = excluded_point_topology_on_R()
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")
        assert s.has_tag("not_separable")


class TestDivisorTopology:
    def test_tags(self):
        s = divisor_topology()
        assert s.has_tag("t0")
        assert s.has_tag("not_t1")
        assert s.has_tag("connected")
        assert s.has_tag("separable")
        assert not s.has_tag("compact")


class TestUncountableDiscreteSpace:
    def test_tags(self):
        s = uncountable_discrete_space()
        assert s.has_tag("metrizable")
        assert s.has_tag("locally_compact")
        assert s.has_tag("not_compact")
        assert s.has_tag("not_separable")
        assert s.has_tag("not_second_countable")
        assert not s.has_tag("connected")


class TestDoubleArrowSpace:
    def test_tags(self):
        s = double_arrow_space()
        assert s.has_tag("compact")
        assert s.has_tag("metrizable")
        assert s.has_tag("zero_dimensional")
        assert s.has_tag("totally_disconnected")
        assert s.has_tag("perfect")
        assert not s.has_tag("connected")

    def test_alias(self):
        rec = catalog.get("split interval")
        assert rec is not None


class TestAnnulus:
    def test_tags(self):
        s = annulus()
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("path_connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("not_simply_connected")


class TestWedgeSumOfCircles:
    def test_tags(self):
        s = wedge_sum_of_circles(2)
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("path_connected")
        assert s.has_tag("not_simply_connected")

    def test_metadata(self):
        s = wedge_sum_of_circles(3)
        assert s.metadata["name"] == "Wedge of 3 circles"
        assert s.metadata["n"] == 3

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            wedge_sum_of_circles(0)


class TestCatalogBatch6:
    def test_batch6_in_catalog(self):
        names = [
            "Sorgenfrey plane",
            "One-point compactification of N",
            "omega+1",
            "Rational sequence topology",
            "Particular point topology on R",
            "Excluded point topology on R",
            "Divisor topology",
            "Uncountable discrete space",
            "Double arrow space",
            "Annulus",
            "Wedge of 2 circles",
        ]
        for name in names:
            assert catalog.get(name) is not None, f"Missing: {name}"

    def test_catalog_size_batch6(self):
        assert len(catalog) >= 75

    def test_not_normal_includes_sorgenfrey_plane(self):
        results = catalog.search(normal=False)
        names = [r.name for r in results]
        assert "Sorgenfrey plane" in names

    def test_figure_eight_alias(self):
        rec = catalog.get("figure eight")
        assert rec is not None
        assert rec.name == "Wedge of 2 circles"


# ---------------------------------------------------------------------------
# Batch 7
# ---------------------------------------------------------------------------

class TestUpperHalfPlane:
    def test_tags(self):
        s = upper_half_plane()
        assert s.has_tag("connected")
        assert s.has_tag("simply_connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("locally_compact")
        assert not s.has_tag("compact")

    def test_in_catalog(self):
        rec = catalog.get("Upper half-plane")
        assert rec is not None
        assert rec.properties.get("simply_connected") is True


class TestClosedUpperHalfPlane:
    def test_tags(self):
        s = closed_upper_half_plane()
        assert s.has_tag("connected")
        assert s.has_tag("simply_connected")
        assert s.has_tag("contractible")
        assert s.has_tag("metrizable")
        assert not s.has_tag("compact")


class TestPAdicNumbers:
    def test_tags(self):
        s = p_adic_numbers()
        assert s.has_tag("locally_compact")
        assert s.has_tag("metrizable")
        assert s.has_tag("zero_dimensional")
        assert s.has_tag("totally_disconnected")
        assert not s.has_tag("compact")
        assert not s.has_tag("connected")


class TestSierpinskiTriangle:
    def test_tags(self):
        s = sierpinski_triangle()
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("path_connected")
        assert s.has_tag("locally_connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("not_simply_connected")

    def test_catalog(self):
        rec = catalog.get("Sierpinski triangle")
        assert rec is not None
        assert rec.properties.get("compact") is True


class TestRealProjectiveNSpace:
    def test_tags(self):
        s = real_projective_n_space(2)
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("not_simply_connected")

    def test_metadata(self):
        s = real_projective_n_space(3)
        assert s.metadata["name"] == "RP^3"
        assert s.metadata["n"] == 3

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            real_projective_n_space(0)


class TestCofiniteOnIntegers:
    def test_tags(self):
        s = cofinite_topology_on_integers()
        assert s.has_tag("t1")
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("not_hausdorff")
        assert not s.has_tag("metrizable")

    def test_catalog(self):
        rec = catalog.get("Cofinite topology on Z")
        assert rec is not None


class TestLongRay:
    def test_tags(self):
        s = long_ray()
        assert s.has_tag("connected")
        assert s.has_tag("hausdorff")
        assert s.has_tag("not_compact")
        assert s.has_tag("not_separable")
        assert s.has_tag("not_metrizable")
        assert s.has_tag("not_second_countable")


class TestKnasterContinuum:
    def test_tags(self):
        s = knaster_continuum()
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("not_locally_connected")
        assert s.has_tag("not_path_connected")

    def test_catalog(self):
        rec = catalog.get("bucket handle")
        assert rec is not None
        assert rec.name == "Knaster continuum"


class TestComplexProjectivePlane:
    def test_tags(self):
        s = complex_projective_plane()
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("simply_connected")
        assert s.has_tag("metrizable")


class TestInfiniteProductOfReals:
    def test_tags(self):
        s = infinite_product_of_reals()
        assert s.has_tag("metrizable")
        assert s.has_tag("separable")
        assert s.has_tag("connected")
        assert s.has_tag("simply_connected")
        assert s.has_tag("not_locally_compact")
        assert not s.has_tag("compact")

    def test_catalog(self):
        rec = catalog.get("R^omega")
        assert rec is not None


class TestNTorus:
    def test_tags(self):
        s = n_torus(3)
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("metrizable")
        assert s.has_tag("not_simply_connected")

    def test_metadata(self):
        s = n_torus(4)
        assert s.metadata["name"] == "T^4"
        assert s.metadata["n"] == 4

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            n_torus(0)


class TestOpenUnitDisk:
    def test_tags(self):
        s = open_unit_disk()
        assert s.has_tag("connected")
        assert s.has_tag("simply_connected")
        assert s.has_tag("contractible")
        assert s.has_tag("metrizable")
        assert s.has_tag("locally_compact")
        assert not s.has_tag("compact")

    def test_catalog(self):
        rec = catalog.get("B^2")
        assert rec is not None


class TestCatalogBatch7:
    def test_batch7_in_catalog(self):
        names = [
            "Upper half-plane",
            "Closed upper half-plane",
            "p-adic numbers",
            "Sierpinski triangle",
            "RP^n",
            "Cofinite topology on Z",
            "Long ray",
            "Knaster continuum",
            "Complex projective plane",
            "Infinite product of reals",
            "T^n",
            "Open unit disk",
        ]
        for name in names:
            assert catalog.get(name) is not None, f"Missing: {name}"

    def test_catalog_size_batch7(self):
        assert len(catalog) >= 87

    def test_simply_connected_search(self):
        results = catalog.search(simply_connected=True, compact=True)
        names = [r.name for r in results]
        assert "Complex projective plane" in names
        assert "Dunce hat" in names

    def test_not_locally_compact_search(self):
        results = catalog.search(locally_compact=False)
        names = [r.name for r in results]
        assert "Infinite product of reals" in names


# ---------------------------------------------------------------------------
# Batch 8
# ---------------------------------------------------------------------------

class TestGenusSurface:
    def test_default_genus1(self):
        s = genus_g_surface(1)
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("metrizable")
        assert not s.has_tag("simply_connected")

    def test_genus0_is_simply_connected(self):
        s = genus_g_surface(0)
        assert s.has_tag("simply_connected")
        assert s.metadata["genus"] == 0

    def test_invalid_genus(self):
        import pytest
        with pytest.raises(ValueError):
            genus_g_surface(-1)

    def test_catalog_record(self):
        rec = catalog.get("Genus-g surface")
        assert rec is not None


class TestNBall:
    def test_tags(self):
        s = n_ball(3)
        assert s.has_tag("compact")
        assert s.has_tag("contractible")
        assert s.has_tag("simply_connected")
        assert s.has_tag("metrizable")

    def test_dimension_metadata(self):
        s = n_ball(4)
        assert s.metadata["n"] == 4
        assert s.metadata["dimension"] == 4

    def test_invalid_n(self):
        import pytest
        with pytest.raises(ValueError):
            n_ball(0)

    def test_catalog_record(self):
        rec = catalog.get("n-ball")
        assert rec is not None


class TestKTopologyOnR:
    def test_hausdorff_not_regular(self):
        s = k_topology_on_R()
        assert s.has_tag("hausdorff")
        assert s.has_tag("not_regular")
        assert s.has_tag("not_metrizable")

    def test_second_countable(self):
        s = k_topology_on_R()
        assert s.has_tag("second_countable")
        assert s.has_tag("separable")

    def test_catalog_record(self):
        rec = catalog.get("K-topology on R")
        assert rec is not None
        assert rec.properties.get("not_regular") is True


class TestSolenoid:
    def test_compact_connected_not_path_connected(self):
        s = solenoid()
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("not_path_connected")
        assert s.has_tag("not_locally_connected")

    def test_metrizable(self):
        s = solenoid()
        assert s.has_tag("metrizable")

    def test_catalog_record(self):
        rec = catalog.get("Dyadic solenoid")
        assert rec is not None


class TestExtendedRealLine:
    def test_compact_contractible(self):
        s = extended_real_line()
        assert s.has_tag("compact")
        assert s.has_tag("contractible")
        assert s.has_tag("path_connected")
        assert s.has_tag("metrizable")

    def test_catalog_record(self):
        rec = catalog.get("Extended real line")
        assert rec is not None


class TestUncountableProductTwoPointSpaces:
    def test_compact_not_metrizable(self):
        s = uncountable_product_of_two_point_spaces()
        assert s.has_tag("compact")
        assert s.has_tag("not_metrizable")
        assert s.has_tag("totally_disconnected")
        assert s.has_tag("separable")

    def test_catalog_record(self):
        rec = catalog.get("{0,1}^c")
        assert rec is not None


class TestWedgeOfTwoSpheres:
    def test_simply_connected(self):
        s = wedge_of_two_spheres()
        assert s.has_tag("simply_connected")
        assert s.has_tag("compact")
        assert s.has_tag("not_contractible")

    def test_catalog_record(self):
        rec = catalog.get("S^2 v S^2")
        assert rec is not None


class TestSuspensionOfCantorSet:
    def test_compact_path_connected(self):
        s = suspension_of_cantor_set()
        assert s.has_tag("compact")
        assert s.has_tag("path_connected")
        assert s.has_tag("not_locally_connected")

    def test_catalog_record(self):
        rec = catalog.get("Suspension of Cantor set")
        assert rec is not None


class TestQuarterPlane:
    def test_contractible_not_compact(self):
        s = quarter_plane()
        assert s.has_tag("contractible")
        assert s.has_tag("simply_connected")
        assert s.has_tag("not_compact")
        assert s.has_tag("locally_compact")

    def test_catalog_record(self):
        rec = catalog.get("Quarter plane")
        assert rec is not None


class TestPuncturedTorus:
    def test_not_simply_connected_not_compact(self):
        s = punctured_torus()
        assert s.has_tag("connected")
        assert s.has_tag("not_compact")
        assert s.has_tag("not_simply_connected")
        assert s.has_tag("metrizable")

    def test_catalog_record(self):
        rec = catalog.get("Punctured torus")
        assert rec is not None


class TestDiscreteSumOfCircles:
    def test_not_compact_not_connected(self):
        s = discrete_sum_of_circles()
        assert s.has_tag("not_compact")
        assert s.has_tag("not_connected")
        assert s.has_tag("locally_compact")
        assert s.has_tag("sigma_compact")

    def test_catalog_record(self):
        rec = catalog.get("Countable disjoint union of circles")
        assert rec is not None


class TestLensSpace:
    def test_compact_connected(self):
        s = lens_space(2, 1)
        assert s.has_tag("compact")
        assert s.has_tag("connected")
        assert s.has_tag("metrizable")
        assert not s.has_tag("simply_connected")

    def test_p1_is_simply_connected(self):
        s = lens_space(1, 0)
        assert s.has_tag("simply_connected")
        assert s.metadata["p"] == 1

    def test_invalid_p(self):
        import pytest
        with pytest.raises(ValueError):
            lens_space(0, 1)

    def test_catalog_record(self):
        rec = catalog.get("Lens space")
        assert rec is not None


class TestCatalogBatch8:
    def test_batch8_in_catalog(self):
        names = [
            "Genus-g surface",
            "n-ball",
            "K-topology on R",
            "Dyadic solenoid",
            "Extended real line",
            "{0,1}^c",
            "S^2 v S^2",
            "Suspension of Cantor set",
            "Quarter plane",
            "Punctured torus",
            "Countable disjoint union of circles",
            "Lens space",
        ]
        for name in names:
            assert catalog.get(name) is not None, f"Missing: {name}"

    def test_catalog_size_batch8(self):
        assert len(catalog) >= 99

    def test_not_metrizable_search(self):
        results = catalog.search(not_metrizable=True)
        names = [r.name for r in results]
        assert "K-topology on R" in names
        assert "{0,1}^c" in names

    def test_sigma_compact_search(self):
        results = catalog.search(sigma_compact=True)
        names = [r.name for r in results]
        assert "Countable disjoint union of circles" in names
