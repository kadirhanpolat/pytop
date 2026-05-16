"""Tests for inverse_systems.py extended API (v0.5.0)."""
import pytest
from pytop.inverse_systems import (
    InverseSystemDescriptor,
    compute_limit_properties,
    pro_finite_completion,
    solenoid_example,
    p_adic_integers_example,
    inverse_system,
    inverse_limit,
)


# ---------------------------------------------------------------------------
# InverseSystemDescriptor
# ---------------------------------------------------------------------------

class TestInverseSystemDescriptor:
    def _ch(self, tags):
        return {"tags": tags}

    def test_basic_construction(self):
        spaces = [self._ch(["compact", "hausdorff"])] * 3
        maps = [self._ch(["surjective"])] * 2
        isd = InverseSystemDescriptor(spaces=spaces, bonding_maps=maps)
        assert isd.space_count == 3
        assert isd.bonding_map_count == 2

    def test_is_chain_like_true(self):
        spaces = [self._ch(["compact"])] * 4
        maps = [self._ch([])] * 3
        isd = InverseSystemDescriptor(spaces=spaces, bonding_maps=maps)
        assert isd.is_chain_like is True

    def test_is_chain_like_false(self):
        spaces = [self._ch([])] * 3
        maps = [self._ch([])] * 5
        isd = InverseSystemDescriptor(spaces=spaces, bonding_maps=maps)
        assert isd.is_chain_like is False

    def test_invalid_index_type_defaults(self):
        isd = InverseSystemDescriptor(spaces=[], bonding_maps=[], index_type="zigzag")
        assert isd.index_type == "chain"

    def test_directed_index_type_accepted(self):
        isd = InverseSystemDescriptor(spaces=[], bonding_maps=[], index_type="directed")
        assert isd.index_type == "directed"

    def test_as_dict_keys(self):
        isd = InverseSystemDescriptor(
            spaces=[self._ch(["compact", "hausdorff"])],
            bonding_maps=[],
            name="Test",
        )
        d = isd.as_dict()
        for key in ("system_type", "name", "spaces", "bonding_maps",
                    "space_count", "bonding_map_count", "index_type",
                    "is_chain_like", "limit_properties", "version"):
            assert key in d

    def test_compute_limit_properties_compact_hausdorff(self):
        spaces = [self._ch(["compact", "hausdorff"])] * 3
        maps = [self._ch(["surjective"])] * 2
        isd = InverseSystemDescriptor(spaces=spaces, bonding_maps=maps)
        props = isd.compute_limit_properties()
        assert "compact" in props["tags"]
        assert "hausdorff" in props["tags"]


# ---------------------------------------------------------------------------
# compute_limit_properties
# ---------------------------------------------------------------------------

class TestComputeLimitProperties:
    def _s(self, *tags):
        return {"tags": list(tags)}

    def test_empty_spaces_warning(self):
        props = compute_limit_properties([], [])
        assert len(props["warnings"]) > 0

    def test_hausdorff_inherited(self):
        spaces = [self._s("hausdorff")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "hausdorff" in props["tags"]

    def test_t0_t1_inherited(self):
        spaces = [self._s("t0", "t1")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "t0" in props["tags"]
        assert "t1" in props["tags"]

    def test_compact_hausdorff_gives_compact_hausdorff(self):
        spaces = [self._s("compact", "hausdorff")] * 3
        maps = [self._s("surjective")] * 2
        props = compute_limit_properties(spaces, maps)
        assert "compact" in props["tags"]
        assert "compact_hausdorff" in props["tags"]

    def test_connected_surjective_gives_connected(self):
        spaces = [self._s("connected")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "connected" in props["tags"]

    def test_connected_non_surjective_warning(self):
        spaces = [self._s("connected")] * 2
        maps = [self._s("continuous")]  # not surjective
        props = compute_limit_properties(spaces, maps)
        assert "connected" not in props["tags"]
        assert any("surjective" in w for w in props["warnings"])

    def test_totally_disconnected_inherited(self):
        spaces = [self._s("totally_disconnected")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "totally_disconnected" in props["tags"]

    def test_compact_hausdorff_totally_disconnected_profinite(self):
        spaces = [self._s("compact", "hausdorff", "totally_disconnected")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "profinite" in props["tags"]

    def test_metrizable_second_countable_inherited(self):
        spaces = [self._s("metrizable", "second_countable")] * 3
        maps = [self._s("surjective")] * 2
        props = compute_limit_properties(spaces, maps)
        assert "metrizable" in props["tags"]
        assert "second_countable" in props["tags"]

    def test_path_connected_warning(self):
        spaces = [self._s("path_connected")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert any("path" in w.lower() for w in props["warnings"])

    def test_surjective_maps_nonempty(self):
        spaces = [self._s("compact")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "nonempty" in props["tags"]

    def test_no_maps_defaults_surjective(self):
        spaces = [self._s("compact", "hausdorff")]
        props = compute_limit_properties(spaces, [])
        assert "compact" in props["tags"]

    def test_discrete_spaces_totally_disconnected(self):
        spaces = [self._s("discrete")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert "totally_disconnected" in props["tags"]

    def test_justifications_populated(self):
        spaces = [self._s("compact", "hausdorff")] * 2
        maps = [self._s("surjective")]
        props = compute_limit_properties(spaces, maps)
        assert len(props["justifications"]) > 0


# ---------------------------------------------------------------------------
# pro_finite_completion
# ---------------------------------------------------------------------------

class TestProFiniteCompletion:
    def test_returns_dict_with_keys(self):
        d = pro_finite_completion({"tags": []})
        for key in ("description", "space", "tags", "properties",
                    "examples", "version"):
            assert key in d

    def test_tags_compact_hausdorff_totally_disconnected(self):
        d = pro_finite_completion({})
        assert "compact" in d["tags"]
        assert "hausdorff" in d["tags"]
        assert "totally_disconnected" in d["tags"]
        assert "profinite" in d["tags"]

    def test_properties_dict(self):
        d = pro_finite_completion({})
        assert d["properties"]["compact"] is True
        assert d["properties"]["connected"] is False
        assert d["properties"]["profinite"] is True

    def test_abelian_group_adds_topological_group(self):
        space = {"tags": ["abelian", "group"], "name": "Z"}
        d = pro_finite_completion(space)
        assert "topological_group" in d["tags"]

    def test_examples_non_empty(self):
        d = pro_finite_completion({})
        assert len(d["examples"]) >= 2

    def test_name_extracted_from_dict(self):
        d = pro_finite_completion({"name": "MyGroup", "tags": []})
        assert "MyGroup" in d["space"]


# ---------------------------------------------------------------------------
# solenoid_example
# ---------------------------------------------------------------------------

class TestSolenoidExample:
    def test_returns_dict(self):
        d = solenoid_example()
        assert isinstance(d, dict)

    def test_required_keys(self):
        for key in ("name", "description", "inferred_tags",
                    "path_connected", "path_connected_note", "version"):
            assert key in solenoid_example()

    def test_not_path_connected(self):
        d = solenoid_example()
        assert d["path_connected"] is False

    def test_compact_tag_inferred(self):
        d = solenoid_example()
        assert "compact" in d["inferred_tags"]

    def test_connected_tag_inferred(self):
        d = solenoid_example()
        assert "connected" in d["inferred_tags"]

    def test_hausdorff_tag_inferred(self):
        d = solenoid_example()
        assert "hausdorff" in d["inferred_tags"]

    def test_name_is_solenoid(self):
        d = solenoid_example()
        assert "solenoid" in d["name"].lower()


# ---------------------------------------------------------------------------
# p_adic_integers_example
# ---------------------------------------------------------------------------

class TestPAdicIntegersExample:
    def test_default_p2(self):
        d = p_adic_integers_example()
        assert "2" in d["name"]

    def test_p5(self):
        d = p_adic_integers_example(5)
        assert "5" in d["name"]

    def test_invalid_p_defaults_to_2(self):
        d = p_adic_integers_example(-1)
        assert "2" in d["name"]

    def test_inferred_compact(self):
        d = p_adic_integers_example(3)
        assert "compact" in d["inferred_tags"]

    def test_inferred_hausdorff(self):
        d = p_adic_integers_example(3)
        assert "hausdorff" in d["inferred_tags"]

    def test_inferred_totally_disconnected(self):
        d = p_adic_integers_example(3)
        assert "totally_disconnected" in d["inferred_tags"]

    def test_ultrametric_flag(self):
        d = p_adic_integers_example(7)
        assert d["ultrametric"] is True

    def test_required_keys(self):
        d = p_adic_integers_example(2)
        for key in ("name", "description", "inferred_tags", "ultrametric", "version"):
            assert key in d


# ---------------------------------------------------------------------------
# Backward-compatible API
# ---------------------------------------------------------------------------

class TestBackwardCompatibleAPI:
    def test_inverse_system_returns_dict(self):
        system = inverse_system(["X0", "X1"], ["f01"])
        assert isinstance(system, dict)
        assert system["system_type"] == "inverse_system"

    def test_inverse_system_invalid_returns_none(self):
        assert inverse_system("not a list", []) is None
        assert inverse_system([], "not a list") is None

    def test_inverse_limit_returns_dict(self):
        system = inverse_system(["X0", "X1"], ["f01"])
        limit = inverse_limit(system)
        assert isinstance(limit, dict)
        assert limit["limit_type"] == "inverse_limit"

    def test_inverse_limit_invalid_returns_none(self):
        assert inverse_limit(None) is None
        assert inverse_limit({"system_type": "wrong"}) is None

    def test_inverse_limit_has_inferred_tags(self):
        system = inverse_system(["X0", "X1"], ["f01"])
        limit = inverse_limit(system)
        assert "inferred_tags" in limit
        assert isinstance(limit["inferred_tags"], list)
