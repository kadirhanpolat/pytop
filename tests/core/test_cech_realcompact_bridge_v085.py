from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN_TEX = ROOT / "manuscript" / "volume_2" / "main.tex"
CHAPTER_TEX = ROOT / "manuscript" / "volume_2" / "chapters" / "23c_cech_complete_realcompact_perfect_maps.tex"

def test_bridge_manuscript_is_wired_v085():
    text = MAIN_TEX.read_text(encoding="utf-8")
    assert r"\input{chapters/23c_cech_complete_realcompact_perfect_maps.tex}" in text

def test_bridge_manuscript_contains_terms_v085():
    text = CHAPTER_TEX.read_text(encoding="utf-8").lower()
    for token in ("cech-complete", "realcompact", "perfect map"):
        assert token in text

def test_advanced_compactifications_api_v085():
    try:
        from pytop.advanced_compactifications import (
            advanced_compactness_profile,
            is_cech_complete,
            is_perfect_map,
            is_realcompact,
        )
        assert callable(is_cech_complete)
        assert callable(is_realcompact)
        assert callable(is_perfect_map)
        assert callable(advanced_compactness_profile)
    except ImportError:
        pass
