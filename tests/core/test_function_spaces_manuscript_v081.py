from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_TEX = ROOT / "manuscript" / "volume_2" / "main.tex"
CHAPTER_TEX = (
    ROOT
    / "manuscript"
    / "volume_2"
    / "chapters"
    / "23a_function_spaces_and_compact_open_topology.tex"
)
ROUTE_MAP = ROOT / "docs" / "roadmap" / "pedagogical_volume_reorganization_map.md"


def test_function_spaces_manuscript_is_wired_into_volume_main_v081():
    text = MAIN_TEX.read_text(encoding="utf-8")
    assert r"\input{chapters/23a_function_spaces_and_compact_open_topology.tex}" in text


def test_function_spaces_manuscript_contains_core_threshold_terms_v081():
    text = CHAPTER_TEX.read_text(encoding="utf-8").lower()
    for token in (
        "pointwise",
        "uniform",
        "compact-open",
        "exponential",
        "equicontinuity",
        "ascoli",
    ):
        assert token in text


def test_function_spaces_route_map_marks_ms_iii_29_as_active_manuscript_v081():
    text = ROUTE_MAP.read_text(encoding="utf-8")
    assert "`MS-III-29`" in text
    assert (
        "`M:manuscript/volume_2/chapters/"
        "23a_function_spaces_and_compact_open_topology.tex`"
    ) in text
