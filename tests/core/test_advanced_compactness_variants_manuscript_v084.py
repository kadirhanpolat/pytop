from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_TEX = ROOT / "manuscript" / "volume_2" / "main.tex"
CHAPTER_TEX = (
    ROOT
    / "manuscript"
    / "volume_2"
    / "chapters"
    / "23b_advanced_compactness_variants.tex"
)
ROUTE_MAP = ROOT / "docs" / "roadmap" / "pedagogical_volume_reorganization_map.md"


def test_advanced_compactness_variants_manuscript_is_wired_into_volume_main_v084():
    text = MAIN_TEX.read_text(encoding="utf-8")
    assert r"\input{chapters/23b_advanced_compactness_variants.tex}" in text


def test_advanced_compactness_variants_manuscript_contains_core_threshold_terms_v084():
    text = CHAPTER_TEX.read_text(encoding="utf-8").lower()
    for token in (
        "countably compact",
        "sequential compact",
        "pseudocompact",
        "lindelof",
        "ordinal",
        "warning",
    ):
        assert token in text


def test_advanced_compactness_route_map_marks_ms_iii_30_as_active_manuscript_v084():
    text = ROUTE_MAP.read_text(encoding="utf-8")
    assert "`MS-III-30`" in text
    assert (
        "`M:manuscript/volume_2/chapters/"
        "23b_advanced_compactness_variants.tex`"
    ) in text
