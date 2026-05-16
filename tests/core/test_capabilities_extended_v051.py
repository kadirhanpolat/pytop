"""Coverage-targeted tests for capabilities.py (v0.5.1)."""
import pytest
from pytop.capabilities import (
    SUPPORT_LEVELS,
    FeatureCapability,
    CapabilityProfile,
    CapabilityRegistry,
    DEFAULT_REGISTRY,
    normalize_feature_name,
    explain_capability,
)


# ---------------------------------------------------------------------------
# FeatureCapability — invalid support raises ValueError  (line 24)
# ---------------------------------------------------------------------------

def test_feature_capability_invalid_support():
    with pytest.raises(ValueError, match="Invalid support level"):
        FeatureCapability(feature="compact", support="maybe")


def test_feature_capability_valid():
    fc = FeatureCapability(feature="compact", support="exact", notes="test")
    assert fc.feature == "compact"
    assert fc.support == "exact"


def test_feature_capability_all_levels():
    for level in SUPPORT_LEVELS:
        fc = FeatureCapability(feature="x", support=level)
        assert fc.support == level


# ---------------------------------------------------------------------------
# CapabilityProfile — invalid summary_support raises ValueError  (line 38)
# ---------------------------------------------------------------------------

def test_capability_profile_invalid_support():
    with pytest.raises(ValueError, match="Invalid summary support"):
        CapabilityProfile(representation="test", summary_support="unknown_level")


def test_capability_profile_valid():
    p = CapabilityProfile(representation="test", summary_support="exact")
    assert p.representation == "test"


def test_capability_profile_support_for_existing_feature():
    p = CapabilityProfile(
        representation="test",
        summary_support="symbolic",
        features={"compact": FeatureCapability("compact", "exact", "note")},
    )
    fc = p.support_for("compact")
    assert fc.support == "exact"


def test_capability_profile_support_for_missing_feature_uses_summary():
    p = CapabilityProfile(representation="test", summary_support="theorem")
    fc = p.support_for("nonexistent_feature")
    assert fc.support == "theorem"


def test_capability_profile_explain():
    p = CapabilityProfile(
        representation="myspace",
        summary_support="symbolic",
        features={"compact": FeatureCapability("compact", "exact", "compact note")},
    )
    explanation = p.explain("compact")
    assert "myspace" in explanation
    assert "compact" in explanation


# ---------------------------------------------------------------------------
# CapabilityRegistry — register (line 64) and get with KeyError (lines 69-70)
# ---------------------------------------------------------------------------

def test_registry_register():
    registry = CapabilityRegistry()
    profile = CapabilityProfile(representation="new_rep", summary_support="symbolic")
    registry.register(profile)
    retrieved = registry.get("new_rep")
    assert retrieved.representation == "new_rep"


def test_registry_get_unknown_raises_key_error():
    registry = CapabilityRegistry()
    with pytest.raises(KeyError, match="Unknown representation"):
        registry.get("totally_unknown_representation")


def test_registry_support_for():
    registry = CapabilityRegistry([
        CapabilityProfile(
            representation="test_rep",
            summary_support="exact",
            features={"compact": FeatureCapability("compact", "exact", "")},
        )
    ])
    fc = registry.support_for("test_rep", "compact")
    assert fc.support == "exact"


def test_registry_explain():
    registry = CapabilityRegistry([
        CapabilityProfile(representation="test_rep", summary_support="symbolic"),
    ])
    explanation = registry.explain("test_rep", "compact")
    assert "test_rep" in explanation


# ---------------------------------------------------------------------------
# as_dict  (line 79)
# ---------------------------------------------------------------------------

def test_registry_as_dict_nonempty():
    registry = CapabilityRegistry([
        CapabilityProfile(
            representation="r1",
            summary_support="exact",
            features={"compact": FeatureCapability("compact", "exact", "")},
        )
    ])
    d = registry.as_dict()
    assert "r1" in d
    assert "compact" in d["r1"]
    assert d["r1"]["compact"] == "exact"


def test_registry_as_dict_empty():
    registry = CapabilityRegistry()
    assert registry.as_dict() == {}


def test_default_registry_as_dict_has_finite():
    d = DEFAULT_REGISTRY.as_dict()
    assert "finite" in d
    assert "compact" in d["finite"]


# ---------------------------------------------------------------------------
# normalize_feature_name — aliases
# ---------------------------------------------------------------------------

def test_normalize_t2_to_hausdorff():
    assert normalize_feature_name("t2") == "hausdorff"


def test_normalize_compactness():
    assert normalize_feature_name("compactness") == "compact"


def test_normalize_chi_to_character():
    assert normalize_feature_name("chi") == "character"


def test_normalize_w_to_weight():
    assert normalize_feature_name("w") == "weight"


def test_normalize_kolmogorov():
    assert normalize_feature_name("kolmogorov") == "t0"


def test_normalize_unknown_passthrough():
    assert normalize_feature_name("my_property") == "my_property"


# ---------------------------------------------------------------------------
# explain_capability — DEFAULT_REGISTRY
# ---------------------------------------------------------------------------

def test_explain_capability_finite_compact():
    explanation = explain_capability("finite", "compact")
    assert "finite" in explanation.lower()


def test_explain_capability_unknown_representation_raises():
    with pytest.raises(KeyError):
        explain_capability("unknown_rep_xyz", "compact")


# ---------------------------------------------------------------------------
# DEFAULT_REGISTRY coverage
# ---------------------------------------------------------------------------

def test_default_registry_finite_profile():
    p = DEFAULT_REGISTRY.get("finite")
    assert p.summary_support == "exact"


def test_default_registry_infinite_discrete():
    p = DEFAULT_REGISTRY.get("infinite_discrete")
    fc = p.support_for("compact")
    assert fc.support == "exact"


def test_default_registry_symbolic_general():
    p = DEFAULT_REGISTRY.get("symbolic_general")
    assert p.summary_support == "symbolic"
