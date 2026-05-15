"""
test_cilt3_preservation_tables_v064.py
========================================
Test suite for src/pytop/preservation_tables.py v0.1.64 extensions.
Covers: preservation_table, invariance_profile, analyze_preservation,
        PreservationError, and legacy API compatibility.
"""
import importlib.util, sys, os
import pytest

_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "src", "pytop")
def _load(name, rel):
    path = os.path.normpath(os.path.join(_BASE, rel))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "pytop"; sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))
import pytop as _pytop_pkg

_pt = _load("pytop.preservation_tables", "preservation_tables.py")
preservation_table      = _pt.preservation_table
invariance_profile      = _pt.invariance_profile
analyze_preservation    = _pt.analyze_preservation
PreservationError       = _pt.PreservationError
preservation_table_lookup  = _pt.preservation_table_lookup
preservation_table_row     = _pt.preservation_table_row
preservation_table_column  = _pt.preservation_table_column
analyze_preservation_table = _pt.analyze_preservation_table
_KNOWN_PROPERTIES          = _pt._KNOWN_PROPERTIES

class _Tagged:
    def __init__(self):
        self.metadata = {"tags": []}; self.representation = "symbolic_general"


# ---- PreservationError ----
def test_error_is_exception():
    assert issubclass(PreservationError, Exception)

def test_error_can_be_raised():
    with pytest.raises(PreservationError):
        raise PreservationError("test")

def test_unknown_property_raises():
    with pytest.raises(PreservationError):
        preservation_table("totally_fake_property")

def test_unknown_construction_raises():
    with pytest.raises(PreservationError):
        preservation_table_lookup("compactness", "fake_construction")


# ---- preservation_table — structure ----
def test_table_has_required_keys():
    t = preservation_table("compactness")
    for k in ["property","rows","counterexample","always_invariant","known_property","version"]:
        assert k in t

def test_table_rows_count():
    assert len(preservation_table("compactness")["rows"]) == 8

def test_table_row_keys():
    for row in preservation_table("compactness")["rows"]:
        assert "context" in row and "verdict" in row

def test_table_version():
    assert preservation_table("compactness")["version"] == "0.1.64"

def test_table_case_insensitive():
    assert preservation_table("COMPACTNESS")["property"] == "compactness"

def test_table_all_known_properties():
    for prop in _KNOWN_PROPERTIES:
        t = preservation_table(prop)
        assert t["known_property"] is True
        assert t["always_invariant"] is True  # all are homeomorphism invariants


# ---- preservation_table — specific verdicts ----
def test_compactness_arbitrary_product_yes():
    t = preservation_table("compactness")
    row = next(r for r in t["rows"] if r["context"] == "arbitrary_product")
    assert "yes" in row["verdict"].lower() or "Tychonoff" in row["verdict"]

def test_compactness_continuous_image_yes():
    t = preservation_table("compactness")
    row = next(r for r in t["rows"] if r["context"] == "continuous_image")
    assert "yes" in row["verdict"].lower()

def test_compactness_open_subspace_no():
    t = preservation_table("compactness")
    row = next(r for r in t["rows"] if r["context"] == "open_subspace")
    assert "no" in row["verdict"].lower()

def test_hausdorff_arbitrary_subspace_yes():
    t = preservation_table("hausdorff")
    row = next(r for r in t["rows"] if r["context"] == "arbitrary_subspace")
    assert "yes" in row["verdict"].lower()

def test_hausdorff_quotient_no():
    t = preservation_table("hausdorff")
    row = next(r for r in t["rows"] if r["context"] == "quotient")
    assert "no" in row["verdict"].lower()

def test_lindelof_finite_product_no():
    t = preservation_table("lindelof")
    row = next(r for r in t["rows"] if r["context"] == "finite_product")
    assert "no" in row["verdict"].lower()

def test_paracompactness_arbitrary_product_no():
    t = preservation_table("paracompactness")
    row = next(r for r in t["rows"] if r["context"] == "arbitrary_product")
    assert "no" in row["verdict"].lower()

def test_metrizability_arbitrary_subspace_yes():
    t = preservation_table("metrizability")
    row = next(r for r in t["rows"] if r["context"] == "arbitrary_subspace")
    assert "yes" in row["verdict"].lower()

def test_normality_finite_product_no():
    t = preservation_table("normality")
    row = next(r for r in t["rows"] if r["context"] == "finite_product")
    assert "no" in row["verdict"].lower()

def test_connectedness_arbitrary_product_yes():
    t = preservation_table("connectedness")
    row = next(r for r in t["rows"] if r["context"] == "arbitrary_product")
    assert "yes" in row["verdict"].lower()

def test_connectedness_continuous_image_yes():
    t = preservation_table("connectedness")
    row = next(r for r in t["rows"] if r["context"] == "continuous_image")
    assert "yes" in row["verdict"].lower()

def test_counterexample_nonempty():
    for prop in ["compactness","lindelof","paracompactness","normality"]:
        assert len(preservation_table(prop)["counterexample"]) > 0


# ---- legacy API ----
def test_lookup_compact_continuous_image():
    assert preservation_table_lookup("compactness", "continuous_image") is True

def test_lookup_hausdorff_quotient():
    assert preservation_table_lookup("hausdorff", "quotient") is False

def test_lookup_compact_closed_subspace():
    assert preservation_table_lookup("compactness", "closed_subspace") is True

def test_lookup_compact_subspace():
    assert preservation_table_lookup("compactness", "subspace") is False

def test_lookup_hausdorff_subspace():
    assert preservation_table_lookup("hausdorff", "subspace") is True

def test_lookup_lindelof_finite_product():
    assert preservation_table_lookup("lindelof", "finite_product") is False

def test_lookup_case_insensitive():
    assert preservation_table_lookup("COMPACTNESS", "continuous_image") is True

def test_row_length():
    assert len(preservation_table_row("compactness")) == 8

def test_row_has_context_verdict():
    for row in preservation_table_row("compactness"):
        assert "context" in row and "verdict" in row

def test_column_length():
    col = preservation_table_column("continuous_image")
    assert len(col) == len(_KNOWN_PROPERTIES)

def test_column_compact_yes():
    col = preservation_table_column("continuous_image")
    compact = next(r for r in col if r["property"] == "compactness")
    assert "yes" in compact["verdict"].lower()

def test_column_hausdorff_no():
    col = preservation_table_column("continuous_image")
    h = next(r for r in col if r["property"] == "hausdorff")
    assert "no" in h["verdict"].lower()

def test_analyze_table_summary():
    s = analyze_preservation_table("compactness")
    assert s["property"] == "compactness"
    assert s["continuous_image"] is True
    assert s["closed_subspace"] is True
    assert s["open_subspace"] is False
    assert len(s["counterexample"]) > 0


# ---- invariance_profile ----
def test_invariance_profile_keys():
    ip = invariance_profile(_Tagged())
    for k in ["representation","topological_invariants","preservation_summary","difficult_cases","version"]:
        assert k in ip

def test_invariance_profile_all_invariants():
    ip = invariance_profile(_Tagged())
    assert len(ip["topological_invariants"]) >= 10

def test_invariance_profile_difficult_cases():
    ip = invariance_profile(_Tagged())
    assert len(ip["difficult_cases"]) >= 4

def test_invariance_profile_sorgenfrey():
    ip = invariance_profile(_Tagged())
    combined = " ".join(ip["difficult_cases"])
    assert "Sorgenfrey" in combined

def test_invariance_profile_summary_keys():
    ip = invariance_profile(_Tagged())
    ps = ip["preservation_summary"]
    for k in ["best_behaved","tricky_products","continuous_image_yes","continuous_image_no"]:
        assert k in ps

def test_invariance_profile_version():
    assert invariance_profile(_Tagged())["version"] == "0.1.64"


# ---- analyze_preservation ----
def test_analyze_status_true():
    assert analyze_preservation("compactness").status == "true"

def test_analyze_mode_theorem():
    assert analyze_preservation("compactness").mode == "theorem"

def test_analyze_version():
    assert analyze_preservation("compactness").metadata["version"] == "0.1.64"

def test_analyze_property_key():
    assert analyze_preservation("lindelof").metadata["property"] == "lindelof"

def test_analyze_always_invariant():
    assert analyze_preservation("compactness").metadata["always_invariant"] is True

def test_analyze_justification_count():
    assert len(analyze_preservation("compactness").justification) >= 4

def test_analyze_value_is_table():
    r = analyze_preservation("compactness")
    assert isinstance(r.value, dict) and "rows" in r.value

def test_analyze_all_properties():
    for prop in _KNOWN_PROPERTIES:
        r = analyze_preservation(prop)
        assert r.status == "true"

def test_analyze_unknown_raises():
    with pytest.raises(PreservationError):
        analyze_preservation("nonsense_property")
