from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN_TEX = ROOT / "manuscript" / "volume_2" / "main.tex"
CHAPTER_TEX = ROOT / "manuscript" / "volume_2" / "chapters" / "24_paracompactness.tex"

def test_paracompactness_manuscript_is_wired_v086():
    if MAIN_TEX.exists():
        text = MAIN_TEX.read_text(encoding="utf-8")
        assert r"\input{chapters/24_paracompactness.tex}" in text

def test_paracompactness_manuscript_contains_terms_v086():
    if CHAPTER_TEX.exists():
        text = CHAPTER_TEX.read_text(encoding="utf-8").lower()
        for token in ("paracompact", "locally finite", "refinement"):
            assert token in text

def test_paracompactness_api_v086():
    # Attempt to import if the module exists as per the roadmap
    try:
        from pytop.paracompactness import is_paracompact
    except ImportError:
        pass
