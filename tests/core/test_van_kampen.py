"""Tests for the Seifert–van Kampen module.

We verify the fundamental group computation for classical spaces whose π₁
is known from topology, and test the supporting machinery (word arithmetic,
Tietze simplification, abelianization, CW complex route).
"""
from __future__ import annotations

import pytest

from pytop.van_kampen import (
    CW1Complex,
    DirectedEdge,
    Face2,
    GroupPresentation,
    GroupPresentationError,
    _concat,
    # Word utilities
    _free_reduce,
    _invert,
    _substitute,
    _word_to_str,
    cw_complex_pi1,
    cyclic_group,
    free_group,
    # Constructors
    group_homomorphism,
    infinite_cyclic_group,
    surface_group,
    surface_group_nr,
    trivial_group,
    # Main functions
    van_kampen,
    van_kampen_klein_bottle,
    van_kampen_real_projective_plane,
    van_kampen_sphere,
    van_kampen_torus,
    # Convenience decompositions
    van_kampen_wedge_circles,
)

# ── Word arithmetic ───────────────────────────────────────────────────────────

class TestWordArithmetic:
    def test_free_reduce_cancels_adjacent_inverses(self):
        w = (("a", 1), ("a", -1), ("b", 1))
        assert _free_reduce(w) == (("b", 1),)

    def test_free_reduce_merges_same_generator(self):
        w = (("a", 1), ("a", 2))
        assert _free_reduce(w) == (("a", 3),)

    def test_free_reduce_full_cancellation(self):
        w = (("a", 1), ("a", -1))
        assert _free_reduce(w) == ()

    def test_free_reduce_no_cancellation(self):
        w = (("a", 1), ("b", 1))
        assert _free_reduce(w) == (("a", 1), ("b", 1))

    def test_invert_reverses_and_negates(self):
        w = (("a", 1), ("b", -1))
        assert _invert(w) == (("b", 1), ("a", -1))

    def test_invert_empty(self):
        assert _invert(()) == ()

    def test_concat_with_reduction(self):
        w1 = (("a", 1), ("b", 1))
        w2 = (("b", -1), ("c", 1))
        assert _concat(w1, w2) == (("a", 1), ("c", 1))

    def test_concat_inverse_is_trivial(self):
        w = (("a", 1), ("b", 1))
        assert _concat(w, _invert(w)) == ()

    def test_substitute_simple(self):
        w = (("a", 1), ("b", 1), ("a", -1))
        result = _substitute(w, "a", (("x", 1), ("y", 1)))
        assert result == _free_reduce((("x", 1), ("y", 1), ("b", 1), ("y", -1), ("x", -1)))

    def test_substitute_positive_power(self):
        w = (("a", 2),)
        result = _substitute(w, "a", (("x", 1),))
        assert result == (("x", 2),)

    def test_substitute_negative_power(self):
        w = (("a", -1),)
        result = _substitute(w, "a", (("x", 1),))
        assert result == (("x", -1),)

    def test_word_to_str_identity(self):
        assert _word_to_str(()) == "1"

    def test_word_to_str_generators(self):
        w = (("a", 1), ("b", -1), ("a", 2))
        assert _word_to_str(w) == "ab^(-1)a^2"


# ── GroupPresentation ─────────────────────────────────────────────────────────

class TestGroupPresentation:
    def test_trivial_group(self):
        g = trivial_group()
        assert g.generators == ()
        assert g.relators == ()
        assert g.rank == 0
        assert g.is_free

    def test_infinite_cyclic(self):
        g = infinite_cyclic_group("a")
        assert g.generators == ("a",)
        assert g.relators == ()
        assert g.is_free

    def test_free_group(self):
        g = free_group("a", "b")
        assert g.generators == ("a", "b")
        assert g.relators == ()
        assert g.rank == 2

    def test_cyclic_group(self):
        g = cyclic_group(5, "a")
        assert g.generators == ("a",)
        assert g.relators == ((("a", 5),),)

    def test_duplicate_generators_raises(self):
        with pytest.raises(GroupPresentationError):
            GroupPresentation(generators=("a", "a"), relators=())

    def test_unknown_generator_in_relator_raises(self):
        with pytest.raises(GroupPresentationError):
            GroupPresentation(generators=("a",), relators=((("b", 1),),))

    def test_presentation_string_trivial(self):
        s = trivial_group().presentation_string()
        assert "—" in s

    def test_presentation_string_cyclic(self):
        s = cyclic_group(3, "a").presentation_string()
        assert "a" in s

    def test_surface_group_genus_1(self):
        g = surface_group(1)
        assert g.generators == ("a1", "b1")
        assert len(g.relators) == 1

    def test_surface_group_genus_0(self):
        g = surface_group(0)
        assert g == trivial_group()

    def test_surface_group_nr(self):
        g = surface_group_nr(2)
        assert g.generators == ("a1", "a2")
        assert g.relators == ((("a1", 2), ("a2", 2)),)


# ── GroupHomomorphism ─────────────────────────────────────────────────────────

class TestGroupHomomorphism:
    def test_identity_on_free_group(self):
        g = free_group("a", "b")
        phi = group_homomorphism(g, g, {"a": (("a", 1),), "b": (("b", 1),)})
        assert phi.apply((("a", 1), ("b", 1))) == (("a", 1), ("b", 1))

    def test_trivial_map(self):
        src = infinite_cyclic_group("c")
        tgt = trivial_group()
        phi = group_homomorphism(src, tgt, {"c": ()})
        assert phi.apply((("c", 3),)) == ()

    def test_apply_inverse(self):
        src = infinite_cyclic_group("c")
        tgt = free_group("a", "b")
        commutator: tuple = (("a", 1), ("b", 1), ("a", -1), ("b", -1))
        phi = group_homomorphism(src, tgt, {"c": commutator})
        # φ(c⁻¹) = [b,a] = b a b⁻¹ a⁻¹
        result = phi.apply((("c", -1),))
        assert result == _free_reduce(_invert(commutator))

    def test_missing_image_raises(self):
        src = free_group("a", "b")
        tgt = trivial_group()
        with pytest.raises(GroupPresentationError):
            group_homomorphism(src, tgt, {"a": ()})  # missing b

    def test_image_uses_unknown_generator_raises(self):
        src = infinite_cyclic_group("c")
        tgt = infinite_cyclic_group("a")
        with pytest.raises(GroupPresentationError):
            group_homomorphism(src, tgt, {"c": (("b", 1),)})


# ── van Kampen: classical spaces ──────────────────────────────────────────────

class TestVanKampenSpaces:
    def test_sphere_is_trivial(self):
        r = van_kampen_sphere()
        assert r.group_type == "trivial"
        assert r.simplified_generators == ()
        assert r.simplified_relators == ()
        assert r.abelianization.betti == 0
        assert r.abelianization.torsion == ()

    def test_torus_presentation(self):
        r = van_kampen_torus()
        assert r.group_type == "free_abelian_rank_2"
        assert set(r.simplified_generators) == {"a", "b"}
        assert len(r.simplified_relators) == 1
        # Abelianization: ℤ²
        assert r.abelianization.betti == 2
        assert r.abelianization.torsion == ()

    def test_klein_bottle_presentation(self):
        r = van_kampen_klein_bottle()
        assert r.group_type == "klein_bottle_group"
        assert set(r.simplified_generators) == {"a", "b"}
        assert len(r.simplified_relators) == 1
        # H₁ = ℤ ⊕ ℤ/2ℤ
        assert r.abelianization.betti == 1
        assert r.abelianization.torsion == (2,)

    def test_rp2_presentation(self):
        r = van_kampen_real_projective_plane()
        assert r.group_type == "cyclic_2"
        assert r.simplified_generators == ("a",)
        assert len(r.simplified_relators) == 1
        # H₁ = ℤ/2ℤ
        assert r.abelianization.betti == 0
        assert r.abelianization.torsion == (2,)

    def test_wedge_one_circle(self):
        r = van_kampen_wedge_circles(1)
        assert r.group_type == "infinite_cyclic"
        assert len(r.simplified_generators) == 1
        assert r.simplified_relators == ()

    def test_wedge_two_circles(self):
        r = van_kampen_wedge_circles(2)
        assert r.group_type == "free_rank_2"
        assert len(r.simplified_generators) == 2
        assert r.simplified_relators == ()
        assert r.abelianization.betti == 2
        assert r.abelianization.torsion == ()

    def test_wedge_four_circles(self):
        r = van_kampen_wedge_circles(4)
        assert r.group_type == "free_rank_4"
        assert len(r.simplified_generators) == 4
        assert r.abelianization.betti == 4

    def test_free_product_of_cyclics(self):
        # ℤ/2 * ℤ/3: free product, no amalgamation
        z2 = cyclic_group(2, "a")
        z3 = cyclic_group(3, "b")
        trivial = trivial_group()
        phi_A = group_homomorphism(trivial, z2, {})
        phi_B = group_homomorphism(trivial, z3, {})
        r = van_kampen(z2, z3, trivial, phi_A, phi_B)
        # No Tietze simplification possible — still has 2 generators
        assert set(r.simplified_generators) == {"a", "b"}
        assert len(r.simplified_relators) == 2

    def test_generator_collision_raises(self):
        g = free_group("a", "b")
        trivial = trivial_group()
        phi = group_homomorphism(trivial, g, {})
        with pytest.raises(GroupPresentationError, match="collision"):
            van_kampen(g, g, trivial, phi, phi)


# ── van Kampen: Tietze simplification ────────────────────────────────────────

class TestTietzeSimplification:
    def test_eliminate_via_amalgam(self):
        # A = ⟨a | ⟩, B = ⟨b | ⟩, A∩B = ⟨c | ⟩, φ_A(c)=a, φ_B(c)=b
        # Amalgam relator: a · b⁻¹  →  one generator eliminated  →  ℤ
        pi1_A = infinite_cyclic_group("a")
        pi1_B = infinite_cyclic_group("b")
        S1 = infinite_cyclic_group("c")
        phi_A = group_homomorphism(S1, pi1_A, {"c": (("a", 1),)})
        phi_B = group_homomorphism(S1, pi1_B, {"c": (("b", 1),)})
        r = van_kampen(pi1_A, pi1_B, S1, phi_A, phi_B)
        # After simplification: one generator remains, no relators (= ℤ)
        assert len(r.simplified_generators) == 1
        assert r.simplified_relators == ()
        assert r.group_type == "infinite_cyclic"

    def test_no_simplification_when_disabled(self):
        pi1_A = infinite_cyclic_group("a")
        pi1_B = infinite_cyclic_group("b")
        S1 = infinite_cyclic_group("c")
        phi_A = group_homomorphism(S1, pi1_A, {"c": (("a", 1),)})
        phi_B = group_homomorphism(S1, pi1_B, {"c": (("b", 1),)})
        r = van_kampen(pi1_A, pi1_B, S1, phi_A, phi_B, simplify=False)
        # Raw: 2 generators, 1 relator
        assert len(r.generators) == 2
        assert len(r.relators) == 1


# ── Abelianization ────────────────────────────────────────────────────────────

class TestAbelianization:
    def test_free_group_ab(self):
        r = van_kampen_wedge_circles(3)
        assert r.abelianization.betti == 3
        assert r.abelianization.torsion == ()

    def test_torus_ab_is_Z2(self):
        r = van_kampen_torus()
        ab = r.abelianization
        assert ab.betti == 2
        assert ab.torsion == ()

    def test_klein_bottle_ab_is_Z_Z2(self):
        r = van_kampen_klein_bottle()
        ab = r.abelianization
        assert ab.betti == 1
        assert ab.torsion == (2,)

    def test_rp2_ab_is_Z2(self):
        r = van_kampen_real_projective_plane()
        ab = r.abelianization
        assert ab.betti == 0
        assert ab.torsion == (2,)

    def test_sphere_ab_is_trivial(self):
        r = van_kampen_sphere()
        ab = r.abelianization
        assert ab.betti == 0
        assert ab.torsion == ()


# ── CW complex route ──────────────────────────────────────────────────────────

class TestCWComplexPi1:
    def test_circle_from_cw(self):
        # S¹: one vertex v, one loop edge e.  π₁ = ⟨e | ⟩ = ℤ
        cw = CW1Complex(
            vertices=frozenset(["v"]),
            edges=(DirectedEdge("e", "v", "v"),),
            faces=(),
        )
        pres = cw_complex_pi1(cw)
        assert pres.generators == ("e",)
        assert pres.relators == ()

    def test_disk_from_cw(self):
        # D²: vertices {v₀,v₁}, one edge e (not a loop), one 2-cell.
        # After spanning tree: e is in the tree → 0 generators.
        cw = CW1Complex(
            vertices=frozenset(["v0", "v1"]),
            edges=(DirectedEdge("e", "v0", "v1"),),
            faces=(Face2("f", (("e", 1), ("e", -1))),),
        )
        pres = cw_complex_pi1(cw)
        assert pres.generators == ()
        assert pres.relators == ()

    def test_torus_from_cw(self):
        # T²: standard CW structure — 1 vertex, 2 edges (a,b), 1 face.
        # Attaching word of face: a b a⁻¹ b⁻¹  (the commutator).
        cw = CW1Complex(
            vertices=frozenset(["v"]),
            edges=(DirectedEdge("a", "v", "v"), DirectedEdge("b", "v", "v")),
            faces=(Face2("f", (("a", 1), ("b", 1), ("a", -1), ("b", -1))),),
        )
        pres = cw_complex_pi1(cw)
        assert set(pres.generators) == {"a", "b"}
        assert len(pres.relators) == 1
        # Relator should be aba⁻¹b⁻¹
        assert pres.relators[0] == (("a", 1), ("b", 1), ("a", -1), ("b", -1))

    def test_rp2_from_cw(self):
        # RP²: 1 vertex, 1 edge a, 1 face with attaching word a·a = a².
        cw = CW1Complex(
            vertices=frozenset(["v"]),
            edges=(DirectedEdge("a", "v", "v"),),
            faces=(Face2("f", (("a", 1), ("a", 1))),),
        )
        pres = cw_complex_pi1(cw)
        assert pres.generators == ("a",)
        assert pres.relators == ((("a", 2),),)

    def test_wedge_two_circles_from_cw(self):
        # S¹ ∨ S¹: 1 vertex, 2 loop edges, no faces.
        cw = CW1Complex(
            vertices=frozenset(["v"]),
            edges=(
                DirectedEdge("a", "v", "v"),
                DirectedEdge("b", "v", "v"),
            ),
            faces=(),
        )
        pres = cw_complex_pi1(cw)
        assert set(pres.generators) == {"a", "b"}
        assert pres.relators == ()

    def test_sphere_from_cw(self):
        # S²: 1 vertex, 0 edges, 1 face with trivial attaching word.
        # Wait, S² minimal CW: 1 vertex v, 1 edge e (collapses to v via tree),
        # 2 faces f1, f2 — but simplest is: 1 vertex, 1 face, empty attaching.
        # Actually standard minimal S²: one 0-cell, one 2-cell.
        # CW1Complex only knows 0,1,2 cells. No edges → no generators.
        cw = CW1Complex(
            vertices=frozenset(["v"]),
            edges=(),
            faces=(Face2("f", ()),),
        )
        pres = cw_complex_pi1(cw)
        assert pres.generators == ()
        assert pres.relators == ()

    def test_spanning_tree_used_correctly(self):
        # Graph: v0 --a-- v1 --b-- v2 --c-- v0 (triangle), no 2-cells.
        # Any spanning tree covers 2 of the 3 edges; exactly 1 non-tree edge.
        # π₁ = free group of rank 1 = ℤ (regardless of which edge is non-tree).
        cw = CW1Complex(
            vertices=frozenset(["v0", "v1", "v2"]),
            edges=(
                DirectedEdge("a", "v0", "v1"),
                DirectedEdge("b", "v1", "v2"),
                DirectedEdge("c", "v2", "v0"),
            ),
            faces=(),
        )
        pres = cw_complex_pi1(cw)
        assert len(pres.generators) == 1
        assert pres.relators == ()


# ── VanKampenResult: string formatting ───────────────────────────────────────

class TestVanKampenResultStrings:
    def test_trivial_presentation_string(self):
        r = van_kampen_sphere()
        s = r.presentation_string()
        assert "—" in s  # no generators or relators

    def test_torus_presentation_string(self):
        r = van_kampen_torus()
        s = r.presentation_string()
        assert "a" in s and "b" in s

    def test_raw_presentation_string(self):
        r = van_kampen_torus()
        s = r.raw_presentation_string()
        assert "a" in s and "b" in s

    def test_notes_are_nonempty(self):
        r = van_kampen_torus()
        assert len(r.notes) >= 4


# ── Higher genus surface groups ───────────────────────────────────────────────

class TestHigherGenusSurfaces:
    def test_genus_2_surface_generators(self):
        # Σ₂: genus-2 closed orientable surface, π₁ = ⟨a1,b1,a2,b2 | [a1,b1][a2,b2]⟩
        g = surface_group(2)
        assert set(g.generators) == {"a1", "b1", "a2", "b2"}
        assert len(g.relators) == 1

    def test_genus_2_abelianization_is_Z4(self):
        # H₁(Σ₂) = Z⁴
        g = surface_group(2)
        # Abelianize: relator [a1,b1][a2,b2] → 0 in abelian group
        # abelianization betti = 4 (all generators free after abelianization)
        from pytop.van_kampen import _abelianize
        ab = _abelianize(list(g.generators), list(g.relators))
        assert ab.betti == 4
        assert ab.torsion == ()

    def test_genus_3_surface_group_rank(self):
        g = surface_group(3)
        assert g.rank == 6   # 2*3 generators

    def test_surface_group_nr_genus_2_abelianization(self):
        # Non-orientable surface of genus 2 (Klein bottle): ⟨a1,a2 | a1²a2²⟩
        # H₁ = abelianization = Z ⊕ Z/2
        g = surface_group_nr(2)
        from pytop.van_kampen import _abelianize
        ab = _abelianize(list(g.generators), list(g.relators))
        assert ab.betti == 1
        assert ab.torsion == (2,)

    def test_surface_group_nr_genus_3_abelianization(self):
        # Non-orientable genus 3: ⟨a1,a2,a3 | a1²a2²a3²⟩
        # H₁ = Z² ⊕ Z/2
        g = surface_group_nr(3)
        from pytop.van_kampen import _abelianize
        ab = _abelianize(list(g.generators), list(g.relators))
        assert ab.betti == 2
        assert ab.torsion == (2,)

    def test_surface_group_genus_0_is_trivial(self):
        g = surface_group(0)
        assert g == trivial_group()

    def test_surface_group_nr_genus_1_is_z2(self):
        # RP²: ⟨a | a²⟩
        g = surface_group_nr(1)
        assert g.generators == ("a1",)
        assert len(g.relators) == 1


# ── Tietze termination edge cases ────────────────────────────────────────────

class TestTietzeTermination:
    def test_free_product_z2_z2_is_infinite_dihedral(self):
        # Z/2 * Z/2 = infinite dihedral group — no elimination possible
        z2a = cyclic_group(2, "a")
        z2b = cyclic_group(2, "b")
        trivial = trivial_group()
        phi_A = group_homomorphism(trivial, z2a, {})
        phi_B = group_homomorphism(trivial, z2b, {})
        r = van_kampen(z2a, z2b, trivial, phi_A, phi_B)
        # 2 generators, 2 relators (a²=1, b²=1), cannot simplify further
        assert len(r.simplified_generators) == 2
        assert len(r.simplified_relators) == 2

    def test_wedge_three_circles_rank_3(self):
        r = van_kampen_wedge_circles(3)
        assert r.group_type == "free_rank_3"
        assert r.abelianization.betti == 3
        assert r.abelianization.torsion == ()

    def test_amalgam_over_z_gives_z(self):
        # Two copies of Z amalgamated over Z (φ_A = id, φ_B = id) → Z
        za = infinite_cyclic_group("a")
        zb = infinite_cyclic_group("b")
        zc = infinite_cyclic_group("c")
        phi_A = group_homomorphism(zc, za, {"c": (("a", 1),)})
        phi_B = group_homomorphism(zc, zb, {"c": (("b", 1),)})
        r = van_kampen(za, zb, zc, phi_A, phi_B)
        assert r.group_type == "infinite_cyclic"

    def test_cyclic_group_order_5_presentation(self):
        g = cyclic_group(5, "x")
        assert g.rank == 1
        assert g.relators == ((("x", 5),),)

    def test_free_reduce_multi_cancel(self):
        # a a⁻¹ b b⁻¹ = identity
        w = (("a", 1), ("a", -1), ("b", 1), ("b", -1))
        assert _free_reduce(w) == ()

    def test_invert_three_term_word(self):
        w = (("a", 1), ("b", 2), ("c", -1))
        assert _invert(w) == (("c", 1), ("b", -2), ("a", -1))


# ── Surface groups ────────────────────────────────────────────────────────────

class TestSurfaceGroups:
    def test_genus_1_is_free_abelian_rank_2(self):
        # Torus = surface of genus 1 → π₁ = ℤ² (free abelian of rank 2, NOT Z/2)
        r = van_kampen_torus()
        assert r.group_type == "free_abelian_rank_2"

    def test_surface_group_genus_2_identified(self):
        # Genus-2 surface: use van_kampen with two punctured tori
        # Both pieces ≃ genus-1 surface minus disk.
        # Instead: directly verify surface_group(2) presentation.
        g = surface_group(2)
        assert g.generators == ("a1", "b1", "a2", "b2")
        assert len(g.relators) == 1
        rel = g.relators[0]
        assert rel == (
            ("a1", 1), ("b1", 1), ("a1", -1), ("b1", -1),
            ("a2", 1), ("b2", 1), ("a2", -1), ("b2", -1),
        )

    def test_surface_group_nr_rp2(self):
        # RP² = N₁ (one crosscap), relator a₁²
        g = surface_group_nr(1)
        assert g.generators == ("a1",)
        assert g.relators == ((("a1", 2),),)
